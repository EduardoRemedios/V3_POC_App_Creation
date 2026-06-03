"""SQLite repository/query layer for Mission 009."""

from __future__ import annotations

import json
import sqlite3
from typing import Any


class WorkbenchRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def table_names(self) -> list[str]:
        rows = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name").fetchall()
        return [row["name"] for row in rows]

    def source_records(self, fixture_id: str) -> list[dict[str, Any]]:
        return self._json_rows("source_records", fixture_id, "payload_json", "payload")

    def normalized_facts(self, fixture_id: str) -> list[dict[str, Any]]:
        rows = self._json_rows("normalized_facts", fixture_id, "value_json", "value")
        for row in rows:
            refs = self.conn.execute(
                "SELECT source_record_id FROM fact_provenance WHERE fact_id = ? ORDER BY source_record_id",
                (row["id"],),
            ).fetchall()
            row["provenance_refs"] = [ref["source_record_id"] for ref in refs]
        return rows

    def derived_facts(self, fixture_id: str) -> list[dict[str, Any]]:
        return self._json_rows("derived_facts", fixture_id, "value_json", "value")

    def timeline(self, run_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM workflow_timeline_steps WHERE run_id = ? ORDER BY step_index", (run_id,)
        ).fetchall()
        return [_decode(row, ("evidence_refs_json", "output_json")) for row in rows]

    def evidence_graph(self, fixture_id: str | None = None) -> dict[str, list[dict[str, Any]]]:
        if fixture_id:
            node_rows = self.conn.execute(
                "SELECT * FROM evidence_graph_nodes WHERE fixture_id = ? ORDER BY node_type, id", (fixture_id,)
            ).fetchall()
            edge_rows = self.conn.execute(
                "SELECT * FROM evidence_graph_edges WHERE fixture_id = ? ORDER BY relation, id", (fixture_id,)
            ).fetchall()
        else:
            node_rows = self.conn.execute("SELECT * FROM evidence_graph_nodes ORDER BY fixture_id, node_type, id").fetchall()
            edge_rows = self.conn.execute("SELECT * FROM evidence_graph_edges ORDER BY fixture_id, relation, id").fetchall()
        return {
            "nodes": [_decode(row, ("metadata_json",)) for row in node_rows],
            "edges": [_decode(row, ("metadata_json",)) for row in edge_rows],
        }

    def recommendations(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM recommendations ORDER BY fixture_id, workflow, id").fetchall()
        return [_decode(row, ("payload_json",)) for row in rows]

    def follow_up_outcomes(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM follow_up_outcomes ORDER BY fixture_id, id").fetchall()
        return [_decode(row, ("payload_json",)) for row in rows]

    def report_settings(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM report_settings ORDER BY fixture_id, id").fetchall()
        return [_decode(row, ("payload_json",)) for row in rows]

    def safety_events(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM safety_boundary_events ORDER BY fixture_id, id").fetchall()
        return [_decode(row, ("evidence_refs_json",)) for row in rows]

    def replay_audits(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM replay_audit_summaries ORDER BY fixture_id, id").fetchall()
        return [_decode(row, ("summary_json",)) for row in rows]

    def _json_rows(self, table: str, fixture_id: str, json_column: str, output_key: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(f"SELECT * FROM {table} WHERE fixture_id = ? ORDER BY id", (fixture_id,)).fetchall()
        decoded = []
        for row in rows:
            data = {key: row[key] for key in row.keys()}
            data[output_key] = json.loads(data.pop(json_column))
            decoded.append(data)
        return decoded


def _decode(row: sqlite3.Row, json_columns: tuple[str, ...]) -> dict[str, Any]:
    data = {key: row[key] for key in row.keys()}
    for column in json_columns:
        if column in data:
            out_key = column.removesuffix("_json")
            data[out_key] = json.loads(data.pop(column))
    return data
