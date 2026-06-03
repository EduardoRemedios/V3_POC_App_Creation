"""DB-backed fixture replay and contract comparison."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import sqlite3

from .loader import load_fixture
from .reports import evening_report_candidate, morning_report_candidate
from .schema import Fixture, NormalizedFact, SourceRecord
from .storage import import_fixture, list_derived_facts, run_and_persist_workflow
from .workflows import run_workflow


def fixture_from_db(conn: sqlite3.Connection, fixture_id: str) -> Fixture:
    source_rows = conn.execute(
        "SELECT * FROM source_records WHERE fixture_id = ? ORDER BY observed_at, id", (fixture_id,)
    ).fetchall()
    if not source_rows:
        import_fixture(conn, Path("fixtures/dtu") / f"{fixture_id}.json")
        source_rows = conn.execute(
            "SELECT * FROM source_records WHERE fixture_id = ? ORDER BY observed_at, id", (fixture_id,)
        ).fetchall()
    fixture_file = load_fixture(Path("fixtures/dtu") / f"{fixture_id}.json")
    sources = tuple(
        SourceRecord(
            id=row["id"],
            source=row["source"],
            source_record_id=row["source_record_id"],
            domain=row["domain"],
            observed_at=row["observed_at"],
            ingested_at=row["ingested_at"],
            payload=json.loads(row["payload_json"]),
        )
        for row in source_rows
    )
    fact_rows = conn.execute(
        "SELECT * FROM normalized_facts WHERE fixture_id = ? ORDER BY observed_at, id", (fixture_id,)
    ).fetchall()
    facts: list[NormalizedFact] = []
    for row in fact_rows:
        provenance = conn.execute(
            "SELECT source_record_id FROM fact_provenance WHERE fact_id = ? ORDER BY source_record_id", (row["id"],)
        ).fetchall()
        facts.append(
            NormalizedFact(
                id=row["id"],
                domain=row["domain"],
                observed_at=row["observed_at"],
                value=json.loads(row["value_json"]),
                provenance_refs=tuple(item["source_record_id"] for item in provenance),
            )
        )
    return Fixture(
        path=fixture_file.path,
        fixture_id=fixture_file.fixture_id,
        synthetic_only=fixture_file.synthetic_only,
        timezone=fixture_file.timezone,
        scenario=fixture_file.scenario,
        sources=fixture_file.sources,
        source_records=sources,
        normalized_facts=tuple(facts),
        expected=fixture_file.expected,
    )


def replay_fixture(conn: sqlite3.Connection, fixture_id: str) -> dict[str, Any]:
    import_fixture(conn, Path("fixtures/dtu") / f"{fixture_id}.json")
    fixture = fixture_from_db(conn, fixture_id)
    workflow_results = []
    for workflow_name, expected in fixture.expected.get("workflows", {}).items():
        if workflow_name == "morning_report_candidate":
            result = morning_report_candidate(fixture)
            actual = result.output["recommendation_class"]
            refs = result.evidence_pack.refs
        elif workflow_name == "evening_report_candidate":
            result = evening_report_candidate(fixture)
            actual = result.output["recommendation_class"]
            refs = result.evidence_pack.refs
        else:
            persisted = run_and_persist_workflow(conn, fixture_id, workflow_name)
            actual = persisted["recommendation_class"]
            refs = tuple(ref["ref_id"] for ref in _evidence_refs(conn, persisted["evidence_pack_id"]))
        expected_class = expected.get("recommendation_class") or expected.get("status") or expected.get("trend")
        missing_refs = [ref for ref in expected.get("required_evidence_refs", []) if ref not in refs]
        workflow_results.append(
            {
                "workflow": workflow_name,
                "expected": expected_class,
                "actual": actual,
                "passed": actual == expected_class and not missing_refs,
                "missing_evidence_refs": missing_refs,
            }
        )
    return {
        "fixture_id": fixture_id,
        "workflow_results": workflow_results,
        "derived_fact_count": len(list_derived_facts(conn, fixture_id)),
        "passed": all(item["passed"] for item in workflow_results),
    }


def replay_all(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    fixtures = sorted(Path("fixtures/dtu").glob("*.json"))
    return [replay_fixture(conn, path.stem) for path in fixtures]


def _evidence_refs(conn: sqlite3.Connection, evidence_pack_id: str) -> list[dict[str, str]]:
    rows = conn.execute(
        "SELECT ref_id, ref_kind FROM evidence_refs WHERE evidence_pack_id = ? ORDER BY ref_id",
        (evidence_pack_id,),
    ).fetchall()
    return [{"ref_id": row["ref_id"], "ref_kind": row["ref_kind"]} for row in rows]
