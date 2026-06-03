"""Evidence graph construction and queries."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any


def refresh_evidence_graph(conn: sqlite3.Connection, fixture_id: str) -> dict[str, int]:
    with conn:
        conn.execute("DELETE FROM evidence_graph_edges WHERE fixture_id = ?", (fixture_id,))
        conn.execute("DELETE FROM evidence_graph_nodes WHERE fixture_id = ?", (fixture_id,))
        source_rows = conn.execute("SELECT id, domain, source FROM source_records WHERE fixture_id = ?", (fixture_id,)).fetchall()
        fact_rows = conn.execute("SELECT id, domain FROM normalized_facts WHERE fixture_id = ?", (fixture_id,)).fetchall()
        derived_rows = conn.execute("SELECT id, name FROM derived_facts WHERE fixture_id = ?", (fixture_id,)).fetchall()
        evidence_rows = conn.execute("SELECT id, created_by FROM evidence_packs WHERE fixture_id = ?", (fixture_id,)).fetchall()
        workflow_rows = conn.execute("SELECT id, workflow FROM workflow_runs WHERE fixture_id = ?", (fixture_id,)).fetchall()
        report_rows = conn.execute("SELECT id, report_type FROM report_candidates WHERE fixture_id = ?", (fixture_id,)).fetchall()
        rec_rows = conn.execute("SELECT id, workflow FROM recommendations WHERE fixture_id = ?", (fixture_id,)).fetchall()
        follow_rows = conn.execute("SELECT id, recommendation_id FROM follow_up_outcomes WHERE fixture_id = ?", (fixture_id,)).fetchall()

        for row in source_rows:
            _node(conn, fixture_id, f"node_source_{row['id']}", "source_record", row["id"], row["id"], {"domain": row["domain"], "source": row["source"]})
        for row in fact_rows:
            _node(conn, fixture_id, f"node_fact_{row['id']}", "normalized_fact", row["id"], row["id"], {"domain": row["domain"]})
            refs = conn.execute("SELECT source_record_id FROM fact_provenance WHERE fact_id = ?", (row["id"],)).fetchall()
            for ref in refs:
                _edge(conn, fixture_id, f"edge_{ref['source_record_id']}_{row['id']}", f"node_source_{ref['source_record_id']}", f"node_fact_{row['id']}", "normalizes_to")
        for row in derived_rows:
            _node(conn, fixture_id, f"node_derived_{row['id']}", "derived_fact", row["name"], row["id"], {})
            if row["id"].startswith(f"{fixture_id}_"):
                alias = row["id"][len(fixture_id) + 1 :]
                _node(conn, fixture_id, f"node_derived_{alias}", "derived_fact", row["name"], alias, {"alias_for": row["id"]})
            for fact in fact_rows[:8]:
                _edge(conn, fixture_id, f"edge_{fact['id']}_{row['id']}", f"node_fact_{fact['id']}", f"node_derived_{row['id']}", "contributes_to")
        for row in evidence_rows:
            _node(conn, fixture_id, f"node_evidence_{row['id']}", "evidence_pack", row["created_by"], row["id"], {})
            refs = conn.execute("SELECT ref_id FROM evidence_refs WHERE evidence_pack_id = ?", (row["id"],)).fetchall()
            for ref in refs:
                prefix = "node_derived_" if ref["ref_id"].startswith("derived_") else "node_source_"
                _edge(conn, fixture_id, f"edge_{ref['ref_id']}_{row['id']}", f"{prefix}{ref['ref_id']}", f"node_evidence_{row['id']}", "cited_by")
        for row in workflow_rows:
            _node(conn, fixture_id, f"node_workflow_{row['id']}", "workflow_run", row["workflow"], row["id"], {})
            evidence_id = conn.execute("SELECT evidence_pack_id FROM workflow_runs WHERE id = ?", (row["id"],)).fetchone()["evidence_pack_id"]
            _edge(conn, fixture_id, f"edge_{evidence_id}_{row['id']}", f"node_evidence_{evidence_id}", f"node_workflow_{row['id']}", "supports")
        for row in report_rows:
            _node(conn, fixture_id, f"node_report_{row['id']}", "report_candidate", row["report_type"], row["id"], {})
        for row in rec_rows:
            _node(conn, fixture_id, f"node_rec_{row['id']}", "recommendation", row["workflow"], row["id"], {})
        for row in follow_rows:
            _node(conn, fixture_id, f"node_follow_{row['id']}", "follow_up_outcome", row["recommendation_id"], row["id"], {})
            _edge(conn, fixture_id, f"edge_{row['recommendation_id']}_{row['id']}", f"node_rec_{row['recommendation_id']}", f"node_follow_{row['id']}", "followed_by")
    return graph_counts(conn, fixture_id)


def graph_counts(conn: sqlite3.Connection, fixture_id: str) -> dict[str, int]:
    nodes = conn.execute("SELECT COUNT(*) AS count FROM evidence_graph_nodes WHERE fixture_id = ?", (fixture_id,)).fetchone()
    edges = conn.execute("SELECT COUNT(*) AS count FROM evidence_graph_edges WHERE fixture_id = ?", (fixture_id,)).fetchone()
    return {"node_count": int(nodes["count"]), "edge_count": int(edges["count"])}


def graph_payload(conn: sqlite3.Connection, fixture_id: str | None = None) -> dict[str, Any]:
    where = "WHERE fixture_id = ?" if fixture_id else ""
    params = (fixture_id,) if fixture_id else ()
    nodes = conn.execute(f"SELECT * FROM evidence_graph_nodes {where} ORDER BY fixture_id, node_type, id", params).fetchall()
    edges = conn.execute(f"SELECT * FROM evidence_graph_edges {where} ORDER BY fixture_id, relation, id", params).fetchall()
    return {
        "fixture_id": fixture_id,
        "nodes": [_decode(row, "metadata_json") for row in nodes],
        "edges": [_decode(row, "metadata_json") for row in edges],
    }


def _node(conn: sqlite3.Connection, fixture_id: str, node_id: str, node_type: str, label: str, ref_id: str, metadata: dict[str, Any]) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO evidence_graph_nodes(id, fixture_id, node_type, label, ref_id, metadata_json) VALUES (?, ?, ?, ?, ?, ?)",
        (node_id, fixture_id, node_type, label, ref_id, _dump(metadata)),
    )


def _edge(conn: sqlite3.Connection, fixture_id: str, edge_id: str, source: str, target: str, relation: str) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO evidence_graph_edges(id, fixture_id, source_node_id, target_node_id, relation, metadata_json) VALUES (?, ?, ?, ?, ?, ?)",
        (edge_id, fixture_id, source, target, relation, _dump({"created_at": _now()})),
    )


def _decode(row: sqlite3.Row, column: str) -> dict[str, Any]:
    data = {key: row[key] for key in row.keys()}
    data["metadata"] = json.loads(data.pop(column))
    return data


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
