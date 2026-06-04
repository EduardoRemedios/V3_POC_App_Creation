"""SQLite persistence for the synthetic Personal Performance OS workbench."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .api_contracts import contract_rows
from .evidence_graph import graph_payload, refresh_evidence_graph
from .fixture_manifest import api_matrix, family_summary, load_manifest, validate_manifest, workflow_matrix
from .garmin_bridge import garmin_export_catalog
from .loader import load_fixture, load_fixtures
from .manual_imports import (
    adapter_catalog,
    get_manual_export,
    manual_export_catalog,
    preview_manual_export,
    validate_manual_export_manifest,
)
from .primitives import derived_facts
from .recommendations import (
    list_follow_up_outcomes,
    list_recommendations,
    list_report_settings,
    persist_fixture_recommendation_state,
    persist_workflow_recommendation,
)
from .reports import evening_report_candidate, morning_report_candidate
from .safety_audit import list_safety_events, persist_safety_events, safety_summary
from .schema import Fixture, NormalizedFact, SourceRecord
from .snapshots import export_snapshot, validate_snapshot_import
from .timeline import get_timeline, persist_workflow_timeline, replay_audit_summary
from .workflows import run_workflow


MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
DEFAULT_WORKFLOWS = (
    "recovery_today",
    "sleep_cause_analysis",
    "four_week_training_analysis",
    "nutrition_label_capture",
    "ride_rest_recommendation",
    "nutrition_free_text_handling",
    "weight_trend_check",
    "protein_timing_pattern",
    "weekly_review_report",
    "proactive_suppression_check",
    "prior_recommendation_followup",
    "voice_transcript_continuity",
)


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
          version TEXT PRIMARY KEY,
          applied_at TEXT NOT NULL
        )
        """
    )
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        version = path.stem
        applied = conn.execute("SELECT 1 FROM schema_migrations WHERE version = ?", (version,)).fetchone()
        if applied:
            continue
        conn.executescript(path.read_text(encoding="utf-8"))
        conn.execute(
            "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES (?, ?)",
            (version, _now()),
        )
    conn.commit()


def import_fixture(conn: sqlite3.Connection, fixture_or_path: Fixture | str | Path) -> dict[str, Any]:
    fixture = fixture_or_path if isinstance(fixture_or_path, Fixture) else load_fixture(fixture_or_path)
    migrate(conn)
    with conn:
        previous = conn.execute(
            "SELECT import_count FROM fixture_imports WHERE fixture_id = ?", (fixture.fixture_id,)
        ).fetchone()
        import_count = int(previous["import_count"]) + 1 if previous else 1
        _delete_fixture_rows(conn, fixture.fixture_id)
        _insert_sources(conn, fixture)
        _insert_normalized_facts(conn, fixture)
        persisted_derived = derived_facts(fixture)
        _insert_derived_facts(conn, fixture, persisted_derived)
        _insert_conversation_state(conn, fixture)
        _insert_reports(conn, fixture)
        _sync_manifest_tables(conn)
        _sync_api_contract_cases(conn)
        persist_fixture_recommendation_state(conn, fixture)
        persist_safety_events(conn, fixture)
        _insert_fixture_import(conn, fixture, import_count, len(persisted_derived))
        refresh_evidence_graph(conn, fixture.fixture_id)
    return get_import(conn, fixture.fixture_id)


def list_source_adapters() -> list[dict[str, Any]]:
    return adapter_catalog()


def list_manual_exports() -> list[dict[str, Any]]:
    return manual_export_catalog()


def list_garmin_exports() -> list[dict[str, Any]]:
    return garmin_export_catalog()


def get_manual_export_detail(export_id: str) -> dict[str, Any]:
    export = get_manual_export(export_id)
    preview = preview_manual_export(export_id)
    return {**export, "preview_summary": preview["summary"]}


def preview_manual_import(conn: sqlite3.Connection, export_id: str, commit: bool = False) -> dict[str, Any]:
    migrate(conn)
    preview = preview_manual_export(export_id)
    if commit and not preview["summary"]["can_commit"]:
        raise ValueError("manual import preview has validation errors and cannot be committed")
    status = "committed" if commit else "previewed"
    with conn:
        _persist_manual_import_preview(conn, preview, status, default_review_state="accepted" if commit else "needs_clarification")
    return get_manual_import_session(conn, preview["session_id"])


def update_manual_import_row_review(
    conn: sqlite3.Connection, session_id: str, row_index: int, review_state: str, review_note: str = ""
) -> dict[str, Any]:
    migrate(conn)
    if review_state not in {"accepted", "rejected", "needs_clarification"}:
        raise ValueError("manual import review_state must be accepted, rejected, or needs_clarification")
    session = get_manual_import_session(conn, session_id)
    if session["status"] not in {"previewed", "committed"}:
        raise ValueError(f"manual import session cannot be reviewed while status is {session['status']}")
    row = conn.execute(
        "SELECT id FROM manual_import_preview_rows WHERE session_id = ? AND row_index = ?",
        (session_id, row_index),
    ).fetchone()
    if row is None:
        raise KeyError(f"manual import row not found: {session_id} row {row_index}")
    now = _now()
    with conn:
        conn.execute(
            """
            UPDATE manual_import_preview_rows
            SET review_state = ?, review_note = ?, reviewed_at = ?
            WHERE session_id = ? AND row_index = ?
            """,
            (review_state, review_note, now, session_id, row_index),
        )
        _update_manual_import_review_summary(conn, session_id)
        _insert_manual_import_audit_event(
            conn,
            session_id,
            "row_reviewed",
            {
                "row_index": row_index,
                "review_state": review_state,
                "review_note": review_note,
                "synthetic_only": True,
            },
        )
    return get_manual_import_session(conn, session_id)


def commit_reviewed_manual_import(conn: sqlite3.Connection, session_id: str) -> dict[str, Any]:
    migrate(conn)
    session = get_manual_import_session(conn, session_id)
    if session["status"] != "previewed":
        raise ValueError(f"manual import session must be previewed before reviewed commit, got {session['status']}")
    if not session["summary"]["can_commit"]:
        raise ValueError("manual import preview has validation errors and cannot be committed")
    review = session["review_summary"]
    if review.get("needs_clarification", 0):
        raise ValueError("manual import session has rows needing clarification")
    if not review.get("accepted", 0):
        raise ValueError("manual import session has no accepted rows to commit")
    now = _now()
    with conn:
        conn.execute(
            """
            UPDATE manual_import_sessions
            SET status = ?, committed_at = ?, reverted_at = NULL, rollback_reason = NULL
            WHERE id = ?
            """,
            ("committed", now, session_id),
        )
        materialized = _materialize_manual_import_facts(conn, session_id)
        _insert_manual_import_audit_event(
            conn,
            session_id,
            "committed",
            {
                "commit_mode": "reviewed",
                "accepted_rows": review.get("accepted", 0),
                "rejected_rows": review.get("rejected", 0),
                "materialized_count": materialized["materialized_count"],
                "conflict_count": materialized["conflict_count"],
                "conflict_strategy": materialized["conflict_strategy"],
                "synthetic_only": True,
            },
        )
    return get_manual_import_session(conn, session_id)


def rollback_manual_import(conn: sqlite3.Connection, session_id: str, reason: str = "") -> dict[str, Any]:
    migrate(conn)
    session = get_manual_import_session(conn, session_id)
    if session["status"] != "committed":
        raise ValueError(f"manual import session must be committed before rollback, got {session['status']}")
    now = _now()
    with conn:
        _rollback_materialized_import_facts(conn, session_id, reason, now)
        conn.execute(
            """
            UPDATE manual_import_sessions
            SET status = ?, reverted_at = ?, rollback_reason = ?
            WHERE id = ?
            """,
            ("reverted", now, reason, session_id),
        )
        _insert_manual_import_audit_event(
            conn,
            session_id,
            "rolled_back",
            {"reason": reason, "synthetic_only": True, "rollback_mode": "fact_unmaterialize_with_audit_history"},
        )
    return get_manual_import_session(conn, session_id)


def list_manual_import_sessions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    migrate(conn)
    rows = conn.execute("SELECT * FROM manual_import_sessions ORDER BY created_at DESC, id").fetchall()
    return [_manual_session_row(conn, row) for row in rows]


def get_manual_import_session(conn: sqlite3.Connection, session_id: str) -> dict[str, Any]:
    migrate(conn)
    row = conn.execute("SELECT * FROM manual_import_sessions WHERE id = ?", (session_id,)).fetchone()
    if row is None:
        raise KeyError(f"manual import session not found: {session_id}")
    return _manual_session_row(conn, row)


def list_manual_import_materialized_facts(conn: sqlite3.Connection, session_id: str | None = None) -> list[dict[str, Any]]:
    migrate(conn)
    if session_id:
        rows = conn.execute(
            "SELECT * FROM manual_import_materialized_facts WHERE session_id = ? ORDER BY row_index",
            (session_id,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM manual_import_materialized_facts ORDER BY session_id, row_index").fetchall()
    return [_materialized_fact_row(row) for row in rows]


def run_manual_import_consumption(conn: sqlite3.Connection, session_id: str) -> dict[str, Any]:
    migrate(conn)
    session = get_manual_import_session(conn, session_id)
    if session["status"] != "committed":
        raise ValueError(f"manual import session must be committed before consumption, got {session['status']}")
    fixture = _fixture_from_materialized_import(conn, session_id)
    if not fixture.normalized_facts:
        raise ValueError(f"manual import session has no active materialized facts: {session_id}")
    workflow_names = _import_workflow_names(fixture)
    workflow_runs: list[dict[str, Any]] = []
    report_ids: list[str] = []
    with conn:
        conn.execute("DELETE FROM derived_facts WHERE fixture_id = ?", (session_id,))
        _insert_derived_facts(conn, fixture, derived_facts(fixture))
        for workflow_name in workflow_names:
            result = run_workflow(workflow_name, fixture)
            evidence_id = f"{session_id}_{result.evidence_pack.id}_{workflow_name}"
            run_id = f"{session_id}_{result.id}"
            _upsert_evidence_pack(
                conn,
                evidence_id,
                session_id,
                result.evidence_pack.uncertainty,
                workflow_name,
                result.evidence_pack.refs,
            )
            conn.execute(
                """
                INSERT OR REPLACE INTO workflow_runs
                (id, fixture_id, workflow, status, recommendation_class, evidence_pack_id, output_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    session_id,
                    result.workflow,
                    result.status,
                    result.recommendation_class,
                    evidence_id,
                    _dump(result.output),
                    _now(),
                ),
            )
            persist_workflow_timeline(conn, fixture, run_id, result)
            persist_workflow_recommendation(conn, fixture, run_id, result)
            workflow_runs.append(get_workflow_run(conn, run_id))
        report_ids = _insert_import_reports(conn, fixture)
        _insert_manual_import_audit_event(
            conn,
            session_id,
            "consumed_by_workflows_reports",
            {
                "workflow_count": len(workflow_names),
                "workflows": workflow_names,
                "report_count": len(report_ids),
                "report_ids": report_ids,
                "synthetic_only": True,
            },
        )
        graph = refresh_evidence_graph(conn, session_id)
    return {
        "session_id": session_id,
        "synthetic_only": True,
        "workflow_count": len(workflow_runs),
        "workflows": workflow_runs,
        "report_ids": report_ids,
        "graph": graph,
        "timeline_run_ids": [run["id"] for run in workflow_runs],
    }


def get_manual_import_mapping(conn: sqlite3.Connection, session_id: str) -> dict[str, Any]:
    session = get_manual_import_session(conn, session_id)
    return {
        "session_id": session_id,
        "export_id": session["export_id"],
        "adapter_id": session["adapter_id"],
        "mappings": session["mappings"],
    }


def get_manual_import_conflicts(conn: sqlite3.Connection, session_id: str) -> dict[str, Any]:
    session = get_manual_import_session(conn, session_id)
    return {
        "session_id": session_id,
        "export_id": session["export_id"],
        "adapter_id": session["adapter_id"],
        "conflicts": session["conflicts"],
    }


def manual_import_audit_summary(conn: sqlite3.Connection) -> dict[str, Any]:
    migrate(conn)
    sessions = list_manual_import_sessions(conn)
    manifest_validation = validate_manual_export_manifest()
    return {
        "synthetic_only": True,
        "manifest_validation": manifest_validation,
        "adapter_count": len(adapter_catalog()),
        "manual_export_count": len(manual_export_catalog()),
        "session_count": len(sessions),
        "committed_session_count": sum(1 for session in sessions if session["status"] == "committed"),
        "reverted_session_count": sum(1 for session in sessions if session["status"] == "reverted"),
        "issue_count": sum(session["issue_count"] for session in sessions),
        "conflict_count": sum(session["conflict_count"] for session in sessions),
        "review_summary": _aggregate_manual_import_reviews(sessions),
        "audit_event_count": conn.execute("SELECT COUNT(*) AS count FROM manual_import_audit_events").fetchone()["count"],
        "materialized_fact_count": conn.execute(
            "SELECT COUNT(*) AS count FROM manual_import_materialized_facts WHERE active = 1"
        ).fetchone()["count"],
        "reverted_materialized_fact_count": conn.execute(
            "SELECT COUNT(*) AS count FROM manual_import_materialized_facts WHERE active = 0"
        ).fetchone()["count"],
        "approval_count": conn.execute("SELECT COUNT(*) AS count FROM manual_import_approval_records").fetchone()["count"],
        "sessions": [
            {
                "session_id": session["id"],
                "export_id": session["export_id"],
                "adapter_id": session["adapter_id"],
                "status": session["status"],
                "row_count": session["row_count"],
                "issue_count": session["issue_count"],
                "conflict_count": session["conflict_count"],
                "review_summary": session["review_summary"],
                "reverted_at": session.get("reverted_at"),
                "rollback_reason": session.get("rollback_reason"),
            }
            for session in sessions
        ],
    }


def create_synthetic_import_approval(
    conn: sqlite3.Connection,
    export_id: str,
    retention_posture: str = "keep-raw-until-verified",
    approval_state: str = "approved",
    preview_only: bool = True,
    consent_text: str = "",
) -> dict[str, Any]:
    migrate(conn)
    if retention_posture not in {"keep-raw-until-verified", "keep-normalized-only", "keep-raw-and-normalized"}:
        raise ValueError("unsupported retention posture")
    if approval_state not in {"draft", "approved", "revoked"}:
        raise ValueError("approval_state must be draft, approved, or revoked")
    export = get_manual_export(export_id)
    preview = preview_manual_export(export_id)
    now = _now()
    count = conn.execute("SELECT COUNT(*) AS count FROM manual_import_approval_records").fetchone()["count"] + 1
    approval_id = f"mission013_approval_{count:03d}"
    categories = sorted(set(preview["adapter"].get("domains", [])) | {export.get("family", "manual_export")})
    source_label = "real_garmin_manual_export" if str(export.get("adapter_id", "")).startswith("garmin_bridge_") else "real_manual_export"
    text = consent_text or "Synthetic rehearsal approval only; no real file is read and no live Garmin integration is enabled."
    payload = {
        "mission_id": "MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS",
        "synthetic_rehearsal": True,
        "real_data_enabled": False,
        "source_label": source_label,
        "synthetic_fixture_export_id": export_id,
        "approval_defaults": preview.get("approval_defaults", {}),
    }
    with conn:
        conn.execute(
            """
            INSERT INTO manual_import_approval_records
            (id, export_id, session_id, source_label, file_reference, data_categories_json, retention_posture, approval_state, preview_only, synthetic_only, consent_text, approved_at, created_at, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                approval_id,
                export_id,
                preview["session_id"],
                source_label,
                export.get("path", export_id),
                _dump(categories),
                retention_posture,
                approval_state,
                1 if preview_only else 0,
                1,
                text,
                now if approval_state == "approved" else None,
                now,
                _dump(payload),
            ),
        )
    return get_synthetic_import_approval(conn, approval_id)


def get_synthetic_import_approval(conn: sqlite3.Connection, approval_id: str) -> dict[str, Any]:
    migrate(conn)
    row = conn.execute("SELECT * FROM manual_import_approval_records WHERE id = ?", (approval_id,)).fetchone()
    if row is None:
        raise KeyError(f"synthetic import approval not found: {approval_id}")
    return _approval_row(row)


def list_synthetic_import_approvals(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    migrate(conn)
    rows = conn.execute("SELECT * FROM manual_import_approval_records ORDER BY created_at DESC, id").fetchall()
    return [_approval_row(row) for row in rows]


def import_all_fixtures(conn: sqlite3.Connection, directory: str | Path = "fixtures/dtu") -> list[dict[str, Any]]:
    return [import_fixture(conn, fixture) for fixture in load_fixtures(directory)]


def run_and_persist_workflow(conn: sqlite3.Connection, fixture_id: str, workflow: str) -> dict[str, Any]:
    fixture = load_fixture(Path("fixtures/dtu") / f"{fixture_id}.json")
    result = run_workflow(workflow, fixture)
    evidence_id = f"{fixture_id}_{result.evidence_pack.id}_{workflow}"
    run_id = f"{fixture_id}_{result.id}"
    with conn:
        _upsert_evidence_pack(
            conn,
            evidence_id,
            fixture_id,
            result.evidence_pack.uncertainty,
            workflow,
            result.evidence_pack.refs,
        )
        conn.execute(
            """
            INSERT OR REPLACE INTO workflow_runs
            (id, fixture_id, workflow, status, recommendation_class, evidence_pack_id, output_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                fixture_id,
                result.workflow,
                result.status,
                result.recommendation_class,
                evidence_id,
                _dump(result.output),
                _now(),
            ),
        )
        persist_workflow_timeline(conn, fixture, run_id, result)
        persist_workflow_recommendation(conn, fixture, run_id, result)
        refresh_evidence_graph(conn, fixture_id)
    return get_workflow_run(conn, run_id)


def list_fixture_files(directory: str | Path = "fixtures/dtu") -> list[dict[str, Any]]:
    fixtures = load_fixtures(directory)
    return [
        {
            "fixture_id": fixture.fixture_id,
            "scenario": fixture.scenario,
            "source_record_count": len(fixture.source_records),
            "workflow_count": len(fixture.expected.get("workflows", {})),
        }
        for fixture in fixtures
    ]


def fixture_manifest_payload() -> dict[str, Any]:
    manifest = load_manifest()
    return {"manifest": manifest, "validation": validate_manifest(manifest)}


def list_fixture_families() -> list[dict[str, Any]]:
    return family_summary()


def list_expected_workflows() -> list[dict[str, Any]]:
    return workflow_matrix()


def list_expected_api_cases() -> list[dict[str, Any]]:
    return api_matrix()


def get_fixture_detail(fixture_id: str, directory: str | Path = "fixtures/dtu") -> dict[str, Any]:
    fixture = load_fixture(Path(directory) / f"{fixture_id}.json")
    return {
        "fixture_id": fixture.fixture_id,
        "scenario": fixture.scenario,
        "synthetic_only": fixture.synthetic_only,
        "timezone": fixture.timezone,
        "sources": list(fixture.sources),
        "source_records": [record.__dict__ for record in fixture.source_records],
        "expected": fixture.expected,
    }


def list_imports(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM fixture_imports ORDER BY fixture_id").fetchall()
    return [_row(row) for row in rows]


def import_audit_summary(conn: sqlite3.Connection) -> dict[str, Any]:
    imports = list_imports(conn)
    replay = replay_audit_summary(conn)
    return {
        "import_count": len(imports),
        "fixture_ids": [item["fixture_id"] for item in imports],
        "replay_audit": replay,
    }


def get_import(conn: sqlite3.Connection, fixture_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM fixture_imports WHERE fixture_id = ?", (fixture_id,)).fetchone()
    if row is None:
        raise KeyError(f"fixture not imported: {fixture_id}")
    return _row(row)


def get_workflow_run(conn: sqlite3.Connection, run_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM workflow_runs WHERE id = ?", (run_id,)).fetchone()
    if row is None:
        raise KeyError(f"workflow run not found: {run_id}")
    data = _row(row)
    data["output"] = json.loads(data.pop("output_json"))
    return data


def get_workflow_timeline(conn: sqlite3.Connection, run_id: str) -> dict[str, Any]:
    return get_timeline(conn, run_id)


def get_evidence_pack(conn: sqlite3.Connection, evidence_pack_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM evidence_packs WHERE id = ?", (evidence_pack_id,)).fetchone()
    if row is None:
        raise KeyError(f"evidence pack not found: {evidence_pack_id}")
    refs = conn.execute(
        "SELECT ref_id, ref_kind FROM evidence_refs WHERE evidence_pack_id = ? ORDER BY ref_id",
        (evidence_pack_id,),
    ).fetchall()
    data = _row(row)
    data["refs"] = [_row(ref) for ref in refs]
    return data


def list_report_candidates(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM report_candidates ORDER BY fixture_id, report_type").fetchall()
    reports = []
    for row in rows:
        data = _row(row)
        data["sections"] = json.loads(data.pop("sections_json"))
        data["output"] = json.loads(data.pop("output_json"))
        reports.append(data)
    return reports


def list_evidence_graph(conn: sqlite3.Connection, fixture_id: str | None = None) -> dict[str, Any]:
    return graph_payload(conn, fixture_id)


def list_api_contracts() -> list[dict[str, Any]]:
    return contract_rows()


def list_snapshot_export(conn: sqlite3.Connection) -> dict[str, Any]:
    return export_snapshot(conn)


def validate_snapshot_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return validate_snapshot_import(payload)


def list_recommendation_history(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return list_recommendations(conn)


def list_followup_history(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return list_follow_up_outcomes(conn)


def list_persisted_report_settings(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return list_report_settings(conn)


def list_safety_audit(conn: sqlite3.Connection) -> dict[str, Any]:
    return safety_summary(conn)


def get_conversation_thread(conn: sqlite3.Connection, thread_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM conversation_threads WHERE id = ?", (thread_id,)).fetchone()
    if row is None:
        raise KeyError(f"thread not found: {thread_id}")
    messages = conn.execute(
        "SELECT * FROM conversation_messages WHERE thread_id = ? ORDER BY observed_at", (thread_id,)
    ).fetchall()
    events = conn.execute("SELECT * FROM surface_events WHERE thread_id = ? ORDER BY observed_at", (thread_id,)).fetchall()
    data = _row(row)
    data["messages"] = [_row(message) for message in messages]
    data["surface_events"] = [_row(event) for event in events]
    return data


def list_source_records(conn: sqlite3.Connection, fixture_id: str) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM source_records WHERE fixture_id = ? ORDER BY observed_at", (fixture_id,)).fetchall()
    records = []
    for row in rows:
        data = _row(row)
        data["payload"] = json.loads(data.pop("payload_json"))
        records.append(data)
    return records


def list_normalized_facts(conn: sqlite3.Connection, fixture_id: str) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM normalized_facts WHERE fixture_id = ? ORDER BY observed_at", (fixture_id,)).fetchall()
    facts = []
    for row in rows:
        data = _row(row)
        data["value"] = json.loads(data.pop("value_json"))
        provenance = conn.execute(
            "SELECT source_record_id FROM fact_provenance WHERE fact_id = ? ORDER BY source_record_id", (data["id"],)
        ).fetchall()
        data["provenance_refs"] = [item["source_record_id"] for item in provenance]
        facts.append(data)
    return facts


def list_derived_facts(conn: sqlite3.Connection, fixture_id: str) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM derived_facts WHERE fixture_id = ? ORDER BY id", (fixture_id,)).fetchall()
    facts = []
    for row in rows:
        data = _row(row)
        data["value"] = json.loads(data.pop("value_json"))
        facts.append(data)
    return facts


def _delete_fixture_rows(conn: sqlite3.Connection, fixture_id: str) -> None:
    for table in (
        "safety_boundary_events",
        "report_settings",
        "follow_up_outcomes",
        "recommendations",
        "evidence_graph_edges",
        "evidence_graph_nodes",
        "replay_audit_summaries",
        "workflow_timeline_steps",
        "workflow_runs",
        "report_candidates",
        "evidence_refs",
        "evidence_packs",
        "intent_sessions",
        "surface_events",
        "conversation_messages",
        "conversation_threads",
        "derived_facts",
        "fact_provenance",
        "normalized_facts",
        "source_records",
    ):
        conn.execute(f"DELETE FROM {table} WHERE fixture_id = ?", (fixture_id,))


def _insert_sources(conn: sqlite3.Connection, fixture: Fixture) -> None:
    for record in fixture.source_records:
        conn.execute(
            """
            INSERT INTO source_records
            (id, fixture_id, source, source_record_id, domain, observed_at, ingested_at, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                fixture.fixture_id,
                record.source,
                record.source_record_id,
                record.domain,
                record.observed_at,
                record.ingested_at,
                _dump(record.payload),
            ),
        )


def _insert_normalized_facts(conn: sqlite3.Connection, fixture: Fixture) -> None:
    for fact in fixture.normalized_facts:
        conn.execute(
            """
            INSERT INTO normalized_facts(id, fixture_id, domain, observed_at, value_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (fact.id, fixture.fixture_id, fact.domain, fact.observed_at, _dump(fact.value)),
        )
        for ref in fact.provenance_refs:
            conn.execute(
                "INSERT INTO fact_provenance(fact_id, source_record_id, fixture_id) VALUES (?, ?, ?)",
                (fact.id, ref, fixture.fixture_id),
            )


def _insert_derived_facts(conn: sqlite3.Connection, fixture: Fixture, facts) -> None:
    for fact in facts:
        conn.execute(
            "INSERT INTO derived_facts(id, fixture_id, name, value_json) VALUES (?, ?, ?, ?)",
            (f"{fixture.fixture_id}_{fact.id}", fixture.fixture_id, fact.name, _dump(fact.value)),
        )


def _insert_conversation_state(conn: sqlite3.Connection, fixture: Fixture) -> None:
    thread_ids: dict[str, str] = {}
    intent_ids: dict[str, tuple[str, str]] = {}
    for record in fixture.source_records:
        payload = record.payload
        thread_id = payload.get("thread_id")
        intent_id = payload.get("intent_id")
        if thread_id:
            thread_ids[thread_id] = payload.get("text", fixture.scenario)[:80]
        if thread_id and intent_id:
            intent_ids[intent_id] = (thread_id, _workflow_from_intent(intent_id))
        if record.domain == "conversation_message" and thread_id:
            conn.execute(
                """
                INSERT OR REPLACE INTO conversation_messages
                (id, fixture_id, thread_id, surface, observed_at, text, input_mode, source_record_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    fixture.fixture_id,
                    thread_id,
                    payload.get("surface", "synthetic_surface"),
                    record.observed_at,
                    payload.get("text", ""),
                    payload.get("input_mode", "text"),
                    record.id,
                ),
            )
        if record.domain == "surface_event" and thread_id:
            conn.execute(
                """
                INSERT OR REPLACE INTO surface_events
                (id, fixture_id, thread_id, surface, observed_at, event_type, source_record_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    fixture.fixture_id,
                    thread_id,
                    payload.get("surface", "synthetic_surface"),
                    record.observed_at,
                    payload.get("event", "surface_event"),
                    record.id,
                ),
            )
    for thread_id, title in thread_ids.items():
        conn.execute(
            "INSERT OR REPLACE INTO conversation_threads(id, fixture_id, title, status) VALUES (?, ?, ?, ?)",
            (thread_id, fixture.fixture_id, title or fixture.scenario[:80], "open"),
        )
    for intent_id, (thread_id, workflow) in intent_ids.items():
        conn.execute(
            "INSERT OR REPLACE INTO intent_sessions(id, fixture_id, thread_id, workflow, status) VALUES (?, ?, ?, ?, ?)",
            (intent_id, fixture.fixture_id, thread_id, workflow, "active_or_completed"),
        )


def _insert_reports(conn: sqlite3.Connection, fixture: Fixture) -> None:
    for workflow_name in fixture.expected.get("workflows", {}):
        if workflow_name == "morning_report_candidate":
            report = morning_report_candidate(fixture)
        elif workflow_name == "evening_report_candidate":
            report = evening_report_candidate(fixture)
        else:
            continue
        evidence_id = f"{fixture.fixture_id}_{report.evidence_pack.id}"
        _upsert_evidence_pack(
            conn, evidence_id, fixture.fixture_id, report.evidence_pack.uncertainty, workflow_name, report.evidence_pack.refs
        )
        conn.execute(
            """
            INSERT OR REPLACE INTO report_candidates
            (id, fixture_id, report_type, sections_json, evidence_pack_id, delivery_status, output_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"{fixture.fixture_id}_{report.id}",
                fixture.fixture_id,
                report.report_type,
                _dump(list(report.sections)),
                evidence_id,
                report.delivery_status,
                _dump(report.output),
            ),
        )


def _insert_fixture_import(conn: sqlite3.Connection, fixture: Fixture, import_count: int, derived_count: int) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO fixture_imports
        (fixture_id, scenario, synthetic_only, timezone, imported_at, import_count, source_record_count, normalized_fact_count, derived_fact_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fixture.fixture_id,
            fixture.scenario,
            1,
            fixture.timezone,
            _now(),
            import_count,
            len(fixture.source_records),
            len(fixture.normalized_facts),
            derived_count,
        ),
    )


def _sync_manifest_tables(conn: sqlite3.Connection) -> None:
    manifest = load_manifest()
    conn.execute("DELETE FROM fixture_families")
    conn.execute("DELETE FROM fixture_manifest_entries")
    conn.execute("DELETE FROM fixture_risk_coverage")
    conn.execute("DELETE FROM fixture_expected_workflows")
    conn.execute("DELETE FROM fixture_expected_api_cases")
    for family_id, family in manifest["families"].items():
        conn.execute(
            "INSERT OR REPLACE INTO fixture_families(family_id, description) VALUES (?, ?)",
            (family_id, family["description"]),
        )
    for fixture_id, entry in manifest["fixtures"].items():
        conn.execute(
            """
            INSERT OR REPLACE INTO fixture_manifest_entries
            (fixture_id, families_json, risks_json, workflows_json, api_cases_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                fixture_id,
                _dump(entry.get("families", [])),
                _dump(entry.get("risks", [])),
                _dump(entry.get("workflows", [])),
                _dump(entry.get("api_cases", [])),
            ),
        )
        for risk in entry.get("risks", []):
            conn.execute(
                "INSERT OR REPLACE INTO fixture_risk_coverage(fixture_id, risk) VALUES (?, ?)", (fixture_id, risk)
            )
        for workflow in entry.get("workflows", []):
            conn.execute(
                "INSERT OR REPLACE INTO fixture_expected_workflows(fixture_id, workflow) VALUES (?, ?)",
                (fixture_id, workflow),
            )
        for api_case in entry.get("api_cases", []):
            conn.execute(
                "INSERT OR REPLACE INTO fixture_expected_api_cases(fixture_id, api_case) VALUES (?, ?)",
                (fixture_id, api_case),
            )


def _sync_api_contract_cases(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM api_contract_cases")
    for row in contract_rows():
        conn.execute(
            """
            INSERT OR REPLACE INTO api_contract_cases
            (id, method, path_template, category, expected_status, error_shape, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["method"],
                row["path_template"],
                row["category"],
                row["expected_status"],
                1 if row["error_shape"] else 0,
                row["description"],
            ),
        )


def _persist_manual_import_preview(
    conn: sqlite3.Connection, preview: dict[str, Any], status: str, default_review_state: str
) -> None:
    session_id = preview["session_id"]
    now = _now()
    conn.execute("DELETE FROM manual_import_source_files WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM manual_import_preview_rows WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM manual_import_validation_issues WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM manual_import_mapping_rows WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM manual_import_conflicts WHERE session_id = ?", (session_id,))
    conn.execute(
        """
        INSERT OR REPLACE INTO manual_import_sessions
        (id, export_id, adapter_id, status, synthetic_only, row_count, issue_count, conflict_count, created_at, committed_at, summary_json, reverted_at, rollback_reason, review_summary_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            preview["export"]["export_id"],
            preview["adapter"]["adapter_id"],
            status,
            1,
            preview["summary"]["row_count"],
            preview["summary"]["issue_count"],
            preview["summary"]["conflict_count"],
            now,
            now if status == "committed" else None,
            _dump(preview["summary"]),
            None,
            None,
            _dump(_review_summary_for_rows(preview["summary"]["row_count"], default_review_state)),
        ),
    )
    conn.execute(
        """
        INSERT OR REPLACE INTO manual_import_source_files
        (id, session_id, export_id, path, sha256, parser, row_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"{session_id}_source_file",
            session_id,
            preview["export"]["export_id"],
            preview["source_file"]["path"],
            preview["source_file"]["sha256"],
            preview["source_file"]["parser"],
            preview["summary"]["row_count"],
        ),
    )
    for row in preview["rows"]:
        conn.execute(
            """
            INSERT OR REPLACE INTO manual_import_preview_rows
            (id, session_id, row_index, source_record_id, domain, observed_at, raw_json, normalized_json, provenance_json, review_state, review_note, reviewed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"{session_id}_row_{row['row_index']}",
                session_id,
                row["row_index"],
                row["source_record_id"],
                row["domain"],
                row["observed_at"],
                _dump(row["raw"]),
                _dump(row["normalized"]),
                _dump(row["provenance"]),
                default_review_state,
                "",
                now if default_review_state == "accepted" else None,
            ),
        )
    for index, issue in enumerate(preview["issues"], start=1):
        conn.execute(
            """
            INSERT OR REPLACE INTO manual_import_validation_issues
            (id, session_id, row_index, severity, issue_type, field, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"{session_id}_issue_{index}",
                session_id,
                issue["row_index"],
                issue["severity"],
                issue["issue_type"],
                issue["field"],
                issue["message"],
            ),
        )
    for index, mapping in enumerate(preview["mappings"], start=1):
        conn.execute(
            """
            INSERT OR REPLACE INTO manual_import_mapping_rows
            (id, session_id, row_index, source_field, normalized_field, transform, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"{session_id}_mapping_{index}",
                session_id,
                mapping["row_index"],
                mapping["source_field"],
                mapping["normalized_field"],
                mapping["transform"],
                mapping["confidence"],
            ),
        )
    for index, conflict in enumerate(preview["conflicts"], start=1):
        conn.execute(
            """
            INSERT OR REPLACE INTO manual_import_conflicts
            (id, session_id, conflict_type, signature, message, related_rows_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                f"{session_id}_conflict_{index}",
                session_id,
                conflict["conflict_type"],
                conflict["signature"],
                conflict["message"],
                _dump(conflict["row_indexes"]),
            ),
        )
    _insert_manual_import_audit_event(
        conn,
        session_id,
        "committed" if status == "committed" else "previewed",
        {
            "export_id": preview["export"]["export_id"],
            "row_count": preview["summary"]["row_count"],
            "default_review_state": default_review_state,
            "synthetic_only": True,
        },
    )


def _materialize_manual_import_facts(conn: sqlite3.Connection, session_id: str) -> dict[str, Any]:
    session = get_manual_import_session(conn, session_id)
    if conn.execute(
        "SELECT 1 FROM manual_import_materialized_facts WHERE session_id = ? AND active = 1",
        (session_id,),
    ).fetchone():
        raise ValueError(f"manual import session already has active materialized facts: {session_id}")
    source_file = session["source_files"][0] if session["source_files"] else {}
    accepted_rows = [row for row in session["rows"] if row["review_state"] == "accepted"]
    materialized_count = 0
    conflict_count = 0
    conflict_strategy = "version_side_by_side_with_source_precedence"
    for row in accepted_rows:
        source_record_id = f"{session_id}_source_{row['row_index']}"
        fact_id = f"{session_id}_fact_{row['row_index']}"
        existing = conn.execute(
            """
            SELECT id, fixture_id FROM normalized_facts
            WHERE domain = ? AND observed_at = ? AND id != ?
            ORDER BY fixture_id, id
            """,
            (row["domain"], row["observed_at"], fact_id),
        ).fetchall()
        conflict_group_id = _conflict_group_id(row["domain"], row["observed_at"]) if existing else ""
        now = _now()
        mapping_confidence = _mapping_confidence(conn, session_id, row["row_index"])
        mapping_reference = row["provenance"].get("mapping_reference", "manual_import_mapping_rows")
        source_identity = row["provenance"].get("source_family", "synthetic_manual_import")
        provenance = {
            **row["provenance"],
            "manual_import_session_id": session_id,
            "row_index": row["row_index"],
            "source_file_hash": source_file.get("sha256", ""),
            "observed_at": row["observed_at"],
            "ingested_at": now,
            "mapping_reference": mapping_reference,
            "mapping_confidence": mapping_confidence,
            "confidence": "reviewed_synthetic",
            "conflict_strategy": conflict_strategy,
            "conflict_group_id": conflict_group_id,
            "source_precedence": "imported_garmin_reviewed",
            "synthetic_only": True,
        }
        conn.execute(
            """
            INSERT OR REPLACE INTO source_records
            (id, fixture_id, source, source_record_id, domain, observed_at, ingested_at, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source_record_id,
                session_id,
                source_identity,
                row["source_record_id"],
                row["domain"],
                row["observed_at"],
                now,
                _dump(row["raw"]),
            ),
        )
        conn.execute(
            """
            INSERT OR REPLACE INTO normalized_facts(id, fixture_id, domain, observed_at, value_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (fact_id, session_id, row["domain"], row["observed_at"], _dump(row["normalized"])),
        )
        conn.execute(
            "INSERT OR REPLACE INTO fact_provenance(fact_id, source_record_id, fixture_id) VALUES (?, ?, ?)",
            (fact_id, source_record_id, session_id),
        )
        materialized_id = f"{session_id}_materialized_{row['row_index']}"
        conn.execute(
            """
            INSERT OR REPLACE INTO manual_import_materialized_facts
            (id, session_id, row_index, fact_id, source_record_id, fixture_id, domain, observed_at, source_identity, source_file_hash, mapping_reference, mapping_confidence, confidence, conflict_strategy, precedence_rank, conflict_group_id, active, materialized_at, reverted_at, rollback_reason, provenance_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                materialized_id,
                session_id,
                row["row_index"],
                fact_id,
                source_record_id,
                session_id,
                row["domain"],
                row["observed_at"],
                source_identity,
                source_file.get("sha256", ""),
                mapping_reference,
                mapping_confidence,
                "reviewed_synthetic",
                conflict_strategy,
                20,
                conflict_group_id,
                1,
                now,
                None,
                None,
                _dump(provenance),
            ),
        )
        for index, existing_fact in enumerate(existing, start=1):
            conflict_count += 1
            conn.execute(
                """
                INSERT OR REPLACE INTO manual_import_materialization_conflicts
                (id, session_id, materialized_fact_id, existing_fact_id, existing_fixture_id, domain, observed_at, conflict_strategy, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{materialized_id}_conflict_{index}",
                    session_id,
                    materialized_id,
                    existing_fact["id"],
                    existing_fact["fixture_id"],
                    row["domain"],
                    row["observed_at"],
                    conflict_strategy,
                    now,
                ),
            )
        materialized_count += 1
    if materialized_count:
        refresh_evidence_graph(conn, session_id)
    return {
        "materialized_count": materialized_count,
        "conflict_count": conflict_count,
        "conflict_strategy": conflict_strategy,
    }


def _rollback_materialized_import_facts(conn: sqlite3.Connection, session_id: str, reason: str, now: str) -> None:
    rows = conn.execute(
        "SELECT * FROM manual_import_materialized_facts WHERE session_id = ? AND active = 1",
        (session_id,),
    ).fetchall()
    for row in rows:
        conn.execute("DELETE FROM fact_provenance WHERE fact_id = ? AND fixture_id = ?", (row["fact_id"], session_id))
        conn.execute("DELETE FROM normalized_facts WHERE id = ? AND fixture_id = ?", (row["fact_id"], session_id))
        conn.execute("DELETE FROM source_records WHERE id = ? AND fixture_id = ?", (row["source_record_id"], session_id))
        conn.execute(
            """
            UPDATE manual_import_materialized_facts
            SET active = 0, reverted_at = ?, rollback_reason = ?
            WHERE id = ?
            """,
            (now, reason, row["id"]),
        )
    if rows:
        refresh_evidence_graph(conn, session_id)


def _fixture_from_materialized_import(conn: sqlite3.Connection, session_id: str) -> Fixture:
    session = get_manual_import_session(conn, session_id)
    rows = conn.execute(
        """
        SELECT mf.*, nf.value_json, sr.source, sr.source_record_id AS original_source_record_id, sr.payload_json
        FROM manual_import_materialized_facts mf
        JOIN normalized_facts nf ON nf.id = mf.fact_id AND nf.fixture_id = mf.fixture_id
        JOIN source_records sr ON sr.id = mf.source_record_id AND sr.fixture_id = mf.fixture_id
        WHERE mf.session_id = ? AND mf.active = 1
        ORDER BY mf.row_index
        """,
        (session_id,),
    ).fetchall()
    source_records: list[SourceRecord] = []
    normalized_facts: list[NormalizedFact] = []
    sources: set[str] = set()
    for row in rows:
        value = json.loads(row["value_json"])
        payload = _workflow_payload_for_import(row["domain"], value, json.loads(row["payload_json"]))
        source = row["source_identity"]
        sources.add(source)
        source_records.append(
            SourceRecord(
                id=row["source_record_id"],
                source=source,
                source_record_id=row["original_source_record_id"],
                domain=_workflow_domain_for_import(row["domain"]),
                observed_at=row["observed_at"],
                ingested_at=row["materialized_at"],
                payload=payload,
            )
        )
        source_records.extend(_supplemental_import_records(row, value, source))
        normalized_facts.append(
            NormalizedFact(
                id=row["fact_id"],
                domain=row["domain"],
                observed_at=row["observed_at"],
                value=value,
                provenance_refs=(row["source_record_id"],),
            )
        )
    expected = _import_expected_contracts(source_records)
    return Fixture(
        path=Path(f"fixtures/garmin_exports/{session['export_id']}"),
        fixture_id=session_id,
        synthetic_only=True,
        timezone="synthetic_import_timezone",
        scenario=f"Mission 013 materialized Garmin import consumption for {session['export_id']}",
        sources=tuple(sorted(sources or {"synthetic_garmin_manual_export"})),
        source_records=tuple(source_records),
        normalized_facts=tuple(normalized_facts),
        expected=expected,
    )


def _workflow_payload_for_import(domain: str, value: dict[str, Any], raw: dict[str, Any]) -> dict[str, Any]:
    payload = dict(value)
    if domain == "activity":
        payload.setdefault("load", value.get("training_load", 0))
        payload.setdefault("ended_at", value.get("start_time") or raw.get("start_time"))
        payload.setdefault("intensity", "hard" if int(value.get("training_load") or 0) >= 140 else "moderate")
    elif domain == "sleep":
        payload.setdefault("ended_at", value.get("sleep_end"))
    elif domain == "body_composition":
        payload.setdefault("weight_kg", value.get("weight_kg"))
    elif domain == "wellness":
        payload.setdefault("rmssd_ms", value.get("hrv_rmssd_ms"))
        payload.setdefault("baseline_ms", max(int(value.get("hrv_rmssd_ms") or 0) + 8, 8))
    payload["synthetic_import_source"] = "mission_013_materialized_fact"
    return payload


def _workflow_domain_for_import(domain: str) -> str:
    if domain == "body_composition":
        return "weight"
    if domain == "wellness":
        return "hrv"
    return domain


def _supplemental_import_records(row: sqlite3.Row, value: dict[str, Any], source: str) -> list[SourceRecord]:
    records: list[SourceRecord] = []
    if row["domain"] == "sleep":
        if value.get("hrv_rmssd_ms") is not None:
            records.append(
                SourceRecord(
                    id=f"{row['source_record_id']}_hrv",
                    source=source,
                    source_record_id=f"{row['original_source_record_id']}_hrv",
                    domain="hrv",
                    observed_at=row["observed_at"],
                    ingested_at=row["materialized_at"],
                    payload={
                        "rmssd_ms": value.get("hrv_rmssd_ms"),
                        "baseline_ms": int(value.get("hrv_rmssd_ms") or 0) + 8,
                        "synthetic_import_source": "mission_013_sleep_row",
                    },
                )
            )
        if value.get("resting_hr_bpm") is not None:
            records.append(
                SourceRecord(
                    id=f"{row['source_record_id']}_rhr",
                    source=source,
                    source_record_id=f"{row['original_source_record_id']}_rhr",
                    domain="resting_heart_rate",
                    observed_at=row["observed_at"],
                    ingested_at=row["materialized_at"],
                    payload={
                        "bpm": value.get("resting_hr_bpm"),
                        "baseline_bpm": int(value.get("resting_hr_bpm") or 0) + 2,
                        "synthetic_import_source": "mission_013_sleep_row",
                    },
                )
            )
    return records


def _import_expected_contracts(source_records: list[SourceRecord]) -> dict[str, Any]:
    refs = [record.id for record in source_records[:4]]
    if not refs:
        refs = ["derived_missing_data"]
    workflows = {
        "recovery_today": {"required_evidence_refs": refs + ["derived_training_load_7d"]},
        "morning_report_candidate": {"required_evidence_refs": refs, "sections": list(MORNING_SECTIONS_FOR_IMPORT)},
        "evening_report_candidate": {"required_evidence_refs": refs, "sections": list(EVENING_SECTIONS_FOR_IMPORT)},
    }
    domains = {record.domain for record in source_records}
    if "activity" in domains:
        workflows["four_week_training_analysis"] = {"required_evidence_refs": ["derived_training_load_7d"]}
    if "weight" in domains:
        workflows["weight_trend_check"] = {"required_evidence_refs": ["derived_weight_trend"]}
    return {"workflows": workflows, "prohibited_claims": [], "families": ["mission_013_imported_garmin_facts"]}


MORNING_SECTIONS_FOR_IMPORT = ("readiness", "imported_key_evidence", "training_suggestion", "uncertainty")
EVENING_SECTIONS_FOR_IMPORT = ("imported_facts", "recovery_setup", "data_gaps", "follow_up_state")


def _import_workflow_names(fixture: Fixture) -> list[str]:
    names = ["recovery_today"]
    domains = {record.domain for record in fixture.source_records}
    if "activity" in domains:
        names.append("four_week_training_analysis")
    if "weight" in domains:
        names.append("weight_trend_check")
    if len(names) == 1:
        names.append("sleep_cause_analysis")
    return names


def _insert_import_reports(conn: sqlite3.Connection, fixture: Fixture) -> list[str]:
    report_ids: list[str] = []
    for workflow_name, report in (
        ("morning_report_candidate", morning_report_candidate(fixture)),
        ("evening_report_candidate", evening_report_candidate(fixture)),
    ):
        evidence_id = f"{fixture.fixture_id}_{report.evidence_pack.id}_{workflow_name}"
        _upsert_evidence_pack(
            conn,
            evidence_id,
            fixture.fixture_id,
            report.evidence_pack.uncertainty,
            workflow_name,
            report.evidence_pack.refs,
        )
        report_id = f"{fixture.fixture_id}_{report.id}"
        conn.execute(
            """
            INSERT OR REPLACE INTO report_candidates
            (id, fixture_id, report_type, sections_json, evidence_pack_id, delivery_status, output_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report_id,
                fixture.fixture_id,
                report.report_type,
                _dump(list(report.sections)),
                evidence_id,
                report.delivery_status,
                _dump(report.output),
            ),
        )
        report_ids.append(report_id)
    return report_ids


def _manual_session_row(conn: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
    data = _row(row)
    data["synthetic_only"] = bool(data["synthetic_only"])
    data["summary"] = json.loads(data.pop("summary_json"))
    data["review_summary"] = json.loads(data.pop("review_summary_json") or "{}")
    rows = conn.execute(
        "SELECT * FROM manual_import_preview_rows WHERE session_id = ? ORDER BY row_index", (data["id"],)
    ).fetchall()
    issues = conn.execute(
        "SELECT * FROM manual_import_validation_issues WHERE session_id = ? ORDER BY row_index, id", (data["id"],)
    ).fetchall()
    mappings = conn.execute(
        "SELECT * FROM manual_import_mapping_rows WHERE session_id = ? ORDER BY row_index, id", (data["id"],)
    ).fetchall()
    conflicts = conn.execute(
        "SELECT * FROM manual_import_conflicts WHERE session_id = ? ORDER BY id", (data["id"],)
    ).fetchall()
    files = conn.execute("SELECT * FROM manual_import_source_files WHERE session_id = ?", (data["id"],)).fetchall()
    data["source_files"] = [_row(item) for item in files]
    data["rows"] = [
        {
            **_row(item),
            "raw": json.loads(item["raw_json"]),
            "normalized": json.loads(item["normalized_json"]),
            "provenance": json.loads(item["provenance_json"]),
        }
        for item in rows
    ]
    for item in data["rows"]:
        item.pop("raw_json")
        item.pop("normalized_json")
        item.pop("provenance_json")
    data["issues"] = [_row(item) for item in issues]
    data["mappings"] = [_row(item) for item in mappings]
    data["conflicts"] = [
        {
            **_row(item),
            "related_rows": json.loads(item["related_rows_json"]),
        }
        for item in conflicts
    ]
    for item in data["conflicts"]:
        item.pop("related_rows_json")
    events = conn.execute(
        "SELECT * FROM manual_import_audit_events WHERE session_id = ? ORDER BY created_at, id", (data["id"],)
    ).fetchall()
    data["audit_events"] = [
        {
            **_row(item),
            "payload": json.loads(item["payload_json"]),
        }
        for item in events
    ]
    for item in data["audit_events"]:
        item.pop("payload_json")
    data["materialized_facts"] = list_manual_import_materialized_facts(conn, data["id"])
    return data


def _review_summary_for_rows(row_count: int, state: str) -> dict[str, int]:
    summary = {"accepted": 0, "rejected": 0, "needs_clarification": 0}
    summary[state] = row_count
    return summary


def _update_manual_import_review_summary(conn: sqlite3.Connection, session_id: str) -> None:
    counts = {"accepted": 0, "rejected": 0, "needs_clarification": 0}
    rows = conn.execute(
        """
        SELECT review_state, COUNT(*) AS count
        FROM manual_import_preview_rows
        WHERE session_id = ?
        GROUP BY review_state
        """,
        (session_id,),
    ).fetchall()
    for row in rows:
        counts[row["review_state"]] = row["count"]
    conn.execute("UPDATE manual_import_sessions SET review_summary_json = ? WHERE id = ?", (_dump(counts), session_id))


def _mapping_confidence(conn: sqlite3.Connection, session_id: str, row_index: int) -> str:
    rows = conn.execute(
        "SELECT confidence FROM manual_import_mapping_rows WHERE session_id = ? AND row_index = ?",
        (session_id, row_index),
    ).fetchall()
    confidences = {row["confidence"] for row in rows}
    if not confidences:
        return "unknown"
    if confidences == {"high"}:
        return "high"
    if "high" in confidences:
        return "mixed"
    return "low"


def _conflict_group_id(domain: str, observed_at: str) -> str:
    stable = f"{domain}|{observed_at}".encode("utf-8")
    return "materialization_conflict_" + hashlib.sha256(stable).hexdigest()[:16]


def _materialized_fact_row(row: sqlite3.Row) -> dict[str, Any]:
    data = _row(row)
    data["active"] = bool(data["active"])
    data["provenance"] = json.loads(data.pop("provenance_json"))
    return data


def _approval_row(row: sqlite3.Row) -> dict[str, Any]:
    data = _row(row)
    data["preview_only"] = bool(data["preview_only"])
    data["synthetic_only"] = bool(data["synthetic_only"])
    data["data_categories"] = json.loads(data.pop("data_categories_json"))
    data["payload"] = json.loads(data.pop("payload_json"))
    return data


def _aggregate_manual_import_reviews(sessions: list[dict[str, Any]]) -> dict[str, int]:
    totals = {"accepted": 0, "rejected": 0, "needs_clarification": 0}
    for session in sessions:
        for state in totals:
            totals[state] += int(session["review_summary"].get(state, 0))
    return totals


def _insert_manual_import_audit_event(
    conn: sqlite3.Connection, session_id: str, event_type: str, payload: dict[str, Any]
) -> None:
    created_at = _now()
    count = conn.execute(
        "SELECT COUNT(*) AS count FROM manual_import_audit_events WHERE session_id = ?", (session_id,)
    ).fetchone()["count"]
    conn.execute(
        """
        INSERT INTO manual_import_audit_events
        (id, session_id, event_type, created_at, payload_json)
        VALUES (?, ?, ?, ?, ?)
        """,
        (f"{session_id}_event_{count + 1:03d}", session_id, event_type, created_at, _dump(payload)),
    )


def _upsert_evidence_pack(
    conn: sqlite3.Connection, evidence_id: str, fixture_id: str, uncertainty: str, created_by: str, refs: tuple[str, ...]
) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO evidence_packs(id, fixture_id, uncertainty, created_by) VALUES (?, ?, ?, ?)",
        (evidence_id, fixture_id, uncertainty, created_by),
    )
    conn.execute("DELETE FROM evidence_refs WHERE evidence_pack_id = ?", (evidence_id,))
    for ref in refs:
        conn.execute(
            "INSERT INTO evidence_refs(evidence_pack_id, ref_id, ref_kind, fixture_id) VALUES (?, ?, ?, ?)",
            (evidence_id, ref, "derived" if ref.startswith("derived_") else "source", fixture_id),
        )


def _workflow_from_intent(intent_id: str) -> str:
    if "followup" in intent_id:
        return "prior_recommendation_followup"
    if "nutrition" in intent_id:
        return "nutrition_free_text_handling"
    if "alert" in intent_id:
        return "proactive_suppression_check"
    return "recovery_today"


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _row(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in row.keys()}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
