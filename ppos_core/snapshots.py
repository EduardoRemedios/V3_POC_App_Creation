"""Snapshot export and validation for synthetic local state."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from .fixture_manifest import load_manifest, validate_manifest


SNAPSHOT_TABLES = (
    "fixture_imports",
    "source_records",
    "normalized_facts",
    "derived_facts",
    "workflow_runs",
    "workflow_timeline_steps",
    "evidence_graph_nodes",
    "evidence_graph_edges",
    "recommendations",
    "follow_up_outcomes",
    "report_settings",
    "safety_boundary_events",
)


def export_snapshot(conn: sqlite3.Connection) -> dict[str, Any]:
    manifest = load_manifest()
    payload = {
        "snapshot_id": "mission_009_synthetic_snapshot",
        "synthetic_only": True,
        "manifest_validation": validate_manifest(manifest),
        "tables": {table: _table_rows(conn, table) for table in SNAPSHOT_TABLES},
    }
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO snapshot_exports
            (id, fixture_count, table_count, payload_json, validation_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload["snapshot_id"],
                payload["manifest_validation"]["fixture_count"],
                len(SNAPSHOT_TABLES),
                json.dumps(payload, sort_keys=True),
                "valid",
                _now(),
            ),
        )
    return payload


def validate_snapshot_import(snapshot: dict[str, Any]) -> dict[str, Any]:
    required = {"snapshot_id", "synthetic_only", "manifest_validation", "tables"}
    missing = sorted(required - set(snapshot))
    table_keys = set(snapshot.get("tables", {}))
    missing_tables = sorted(set(SNAPSHOT_TABLES) - table_keys)
    valid = not missing and not missing_tables and snapshot.get("synthetic_only") is True
    return {
        "valid": valid,
        "missing_keys": missing,
        "missing_tables": missing_tables,
        "synthetic_only": snapshot.get("synthetic_only") is True,
    }


def _table_rows(conn: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    rows = conn.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()
    return [{key: row[key] for key in row.keys()} for row in rows]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
