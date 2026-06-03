"""Workflow timeline persistence for replay debugging."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from .schema import Fixture, WorkflowRun


TIMELINE_STEPS = ("load_fixture", "derive_summary", "assemble_evidence", "safety_check", "persist_output")


def persist_workflow_timeline(conn: sqlite3.Connection, fixture: Fixture, run_id: str, result: WorkflowRun) -> None:
    refs = list(result.evidence_pack.refs)
    with conn:
        conn.execute("DELETE FROM workflow_timeline_steps WHERE run_id = ?", (run_id,))
        for index, step in enumerate(TIMELINE_STEPS, start=1):
            step_refs = refs if step in {"assemble_evidence", "safety_check", "persist_output"} else []
            output = {
                "workflow": result.workflow,
                "recommendation_class": result.recommendation_class,
                "fixture_id": fixture.fixture_id,
            }
            conn.execute(
                """
                INSERT OR REPLACE INTO workflow_timeline_steps
                (id, fixture_id, run_id, workflow, step_index, step_name, status, evidence_refs_json, output_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{run_id}_step_{index}",
                    fixture.fixture_id,
                    run_id,
                    result.workflow,
                    index,
                    step,
                    "passed",
                    _dump(step_refs),
                    _dump(output),
                    _now(),
                ),
            )
        conn.execute(
            """
            INSERT OR REPLACE INTO replay_audit_summaries
            (id, fixture_id, run_id, workflow, timeline_step_count, evidence_ref_count, passed, summary_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"{run_id}_audit",
                fixture.fixture_id,
                run_id,
                result.workflow,
                len(TIMELINE_STEPS),
                len(refs),
                1,
                _dump({"steps": list(TIMELINE_STEPS), "evidence_refs": refs}),
                _now(),
            ),
        )


def get_timeline(conn: sqlite3.Connection, run_id: str) -> dict[str, Any]:
    rows = conn.execute(
        "SELECT * FROM workflow_timeline_steps WHERE run_id = ? ORDER BY step_index", (run_id,)
    ).fetchall()
    return {
        "run_id": run_id,
        "steps": [_row_with_json(row) for row in rows],
        "passed": bool(rows) and all(row["status"] == "passed" for row in rows),
    }


def replay_audit_summary(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = conn.execute("SELECT * FROM replay_audit_summaries ORDER BY fixture_id, id").fetchall()
    return {
        "audit_count": len(rows),
        "passed_count": sum(1 for row in rows if row["passed"]),
        "items": [_audit_row(row) for row in rows],
    }


def _row_with_json(row: sqlite3.Row) -> dict[str, Any]:
    data = {key: row[key] for key in row.keys()}
    data["evidence_refs"] = json.loads(data.pop("evidence_refs_json"))
    data["output"] = json.loads(data.pop("output_json"))
    return data


def _audit_row(row: sqlite3.Row) -> dict[str, Any]:
    data = {key: row[key] for key in row.keys()}
    data["summary"] = json.loads(data.pop("summary_json"))
    return data


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
