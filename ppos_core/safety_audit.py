"""Safety and compliance audit records for the synthetic workbench."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from .schema import Fixture


def persist_safety_events(conn: sqlite3.Connection, fixture: Fixture) -> None:
    with conn:
        conn.execute("DELETE FROM safety_boundary_events WHERE fixture_id = ?", (fixture.fixture_id,))
        prohibited = fixture.expected.get("prohibited_claims", [])
        _event(
            conn,
            fixture.fixture_id,
            "prohibited_claim_boundary",
            "medium" if prohibited else "low",
            "active",
            list(prohibited),
            f"{len(prohibited)} prohibited claim markers enforced for synthetic fixture.",
        )
        for risk in fixture.expected.get("risk_coverage", []):
            severity = "high" if any(token in risk for token in ("rapid", "medical", "orphan", "missing", "incomplete")) else "medium"
            _event(conn, fixture.fixture_id, f"risk:{risk}", severity, "recorded", [], "Risk coverage recorded.")
        for record in fixture.source_records:
            payload = record.payload
            if payload.get("input_quality") or payload.get("orphan_ref"):
                _event(
                    conn,
                    fixture.fixture_id,
                    "input_quality_boundary",
                    "high",
                    "review_required",
                    [record.id],
                    "Synthetic source quality issue requires audit-aware handling.",
                )
            if record.domain == "surface_event" and (
                payload.get("cooldown_state") == "inside_window"
                or payload.get("event") == "proactive_candidate_detected"
            ):
                _event(
                    conn,
                    fixture.fixture_id,
                    "no_delivery_boundary",
                    "medium",
                    "not_delivered",
                    [record.id],
                    "Proactive candidate remains local and undelivered.",
                )


def list_safety_events(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute("SELECT * FROM safety_boundary_events ORDER BY fixture_id, id").fetchall()
    output = []
    for row in rows:
        data = {key: row[key] for key in row.keys()}
        data["evidence_refs"] = json.loads(data.pop("evidence_refs_json"))
        output.append(data)
    return output


def safety_summary(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = list_safety_events(conn)
    return {
        "event_count": len(rows),
        "high_severity_count": sum(1 for row in rows if row["severity"] == "high"),
        "no_delivery_count": sum(1 for row in rows if row["status"] == "not_delivered"),
        "events": rows,
    }


def _event(
    conn: sqlite3.Connection,
    fixture_id: str,
    boundary_type: str,
    severity: str,
    status: str,
    evidence_refs: list[str],
    message: str,
) -> None:
    event_id = f"safety_{fixture_id}_{boundary_type}".replace(":", "_").replace("/", "_")
    conn.execute(
        """
        INSERT OR REPLACE INTO safety_boundary_events
        (id, fixture_id, boundary_type, severity, status, evidence_refs_json, message, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (event_id, fixture_id, boundary_type, severity, status, _dump(evidence_refs), message, _now()),
    )


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
