"""Recommendation, follow-up, and report-setting persistence."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from .schema import Fixture, WorkflowRun


def persist_fixture_recommendation_state(conn: sqlite3.Connection, fixture: Fixture) -> None:
    with conn:
        conn.execute("DELETE FROM recommendations WHERE fixture_id = ?", (fixture.fixture_id,))
        conn.execute("DELETE FROM follow_up_outcomes WHERE fixture_id = ?", (fixture.fixture_id,))
        conn.execute("DELETE FROM report_settings WHERE fixture_id = ?", (fixture.fixture_id,))
        for record in fixture.records_by_domain("recommendation"):
            rec_id = record.payload.get("recommendation_id", f"rec_{record.id}")
            conn.execute(
                """
                INSERT OR REPLACE INTO recommendations
                (id, fixture_id, workflow, recommendation_class, evidence_pack_id, thread_id, status, confidence, created_at, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rec_id,
                    fixture.fixture_id,
                    "prior_recommendation_followup",
                    "prior_recommendation",
                    None,
                    record.payload.get("thread_id"),
                    "follow_up_due" if record.payload.get("follow_up_due") else "recorded",
                    "moderate",
                    record.observed_at,
                    _dump(record.payload),
                ),
            )
        for workflow, expected in fixture.expected.get("workflows", {}).items():
            if workflow.endswith("candidate"):
                continue
            rec_id = f"rec_{fixture.fixture_id}_{workflow}"
            conn.execute(
                """
                INSERT OR REPLACE INTO recommendations
                (id, fixture_id, workflow, recommendation_class, evidence_pack_id, thread_id, status, confidence, created_at, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rec_id,
                    fixture.fixture_id,
                    workflow,
                    expected.get("recommendation_class") or expected.get("trend") or expected.get("status") or "expected",
                    None,
                    _first_thread_id(fixture),
                    "candidate_history",
                    expected.get("confidence", "moderate"),
                    _now(),
                    _dump({"expected": expected}),
                ),
            )
        for record in fixture.source_records:
            if record.domain == "conversation_message" and (
                "did the" in record.payload.get("text", "").lower()
                or "follow" in record.payload.get("intent_id", "")
            ):
                rec_id = _first_recommendation_id(conn, fixture.fixture_id)
                conn.execute(
                    """
                    INSERT OR REPLACE INTO follow_up_outcomes
                    (id, fixture_id, recommendation_id, outcome_status, observed_at, thread_id, payload_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"follow_{fixture.fixture_id}_{record.id}",
                        fixture.fixture_id,
                        rec_id,
                        "outcome_recorded",
                        record.observed_at,
                        record.payload.get("thread_id"),
                        _dump(record.payload),
                    ),
                )
        _persist_report_settings(conn, fixture)


def persist_workflow_recommendation(conn: sqlite3.Connection, fixture: Fixture, run_id: str, result: WorkflowRun) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO recommendations
        (id, fixture_id, workflow, recommendation_class, evidence_pack_id, thread_id, status, confidence, created_at, payload_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"rec_{run_id}",
            fixture.fixture_id,
            result.workflow,
            result.recommendation_class,
            f"{fixture.fixture_id}_{result.evidence_pack.id}_{result.workflow}",
            _first_thread_id(fixture),
            "workflow_recorded",
            result.evidence_pack.uncertainty,
            _now(),
            _dump(result.output),
        ),
    )


def list_recommendations(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM recommendations ORDER BY fixture_id, workflow, id").fetchall()
    return [_row(row, "payload_json", "payload") for row in rows]


def list_follow_up_outcomes(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM follow_up_outcomes ORDER BY fixture_id, id").fetchall()
    return [_row(row, "payload_json", "payload") for row in rows]


def list_report_settings(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM report_settings ORDER BY fixture_id, id").fetchall()
    return [_row(row, "payload_json", "payload") for row in rows]


def _persist_report_settings(conn: sqlite3.Connection, fixture: Fixture) -> None:
    prefs = fixture.records_by_domain("report_preferences")
    if not prefs and any("report" in family for family in fixture.expected.get("families", [])):
        prefs = []
    if not prefs:
        return
    for record in prefs:
        payload = record.payload
        conn.execute(
            """
            INSERT OR REPLACE INTO report_settings
            (id, fixture_id, morning_depth, weekly_depth, quiet_hours_start, quiet_hours_end, cooldown_hours, proactive_enabled, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"settings_{record.id}",
                fixture.fixture_id,
                payload.get("morning_depth", "standard"),
                payload.get("weekly_depth", "standard"),
                payload.get("quiet_hours_start", "21:30"),
                payload.get("quiet_hours_end", "07:30"),
                int(payload.get("cooldown_hours", 24)),
                1 if payload.get("proactive_enabled", True) else 0,
                _dump(payload),
            ),
        )


def _first_thread_id(fixture: Fixture) -> str | None:
    for record in fixture.source_records:
        if record.payload.get("thread_id"):
            return record.payload["thread_id"]
    return None


def _first_recommendation_id(conn: sqlite3.Connection, fixture_id: str) -> str:
    row = conn.execute("SELECT id FROM recommendations WHERE fixture_id = ? ORDER BY id", (fixture_id,)).fetchone()
    return row["id"] if row else f"rec_{fixture_id}_unknown"


def _row(row: sqlite3.Row, json_column: str, output_key: str) -> dict[str, Any]:
    data = {key: row[key] for key in row.keys()}
    data[output_key] = json.loads(data.pop(json_column))
    return data


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
