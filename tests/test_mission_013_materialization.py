from __future__ import annotations

import json
import unittest

from ppos_core.storage import (
    commit_reviewed_manual_import,
    connect,
    list_manual_import_materialized_facts,
    list_normalized_facts,
    migrate,
    preview_manual_import,
    update_manual_import_row_review,
)


class Mission013MaterializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_reviewed_garmin_commit_materializes_accepted_rows(self) -> None:
        session = preview_manual_import(self.conn, "garmin_activities_clean_csv")
        for row_index in (1, 2, 3):
            update_manual_import_row_review(self.conn, session["id"], row_index, "accepted")

        committed = commit_reviewed_manual_import(self.conn, session["id"])

        self.assertEqual("committed", committed["status"])
        self.assertEqual(3, len(committed["materialized_facts"]))
        self.assertEqual("committed", committed["audit_events"][-1]["event_type"])
        self.assertEqual(3, committed["audit_events"][-1]["payload"]["materialized_count"])

        facts = list_normalized_facts(self.conn, session["id"])
        self.assertEqual(3, len(facts))
        self.assertEqual({"activity"}, {fact["domain"] for fact in facts})
        self.assertEqual([f"{session['id']}_source_1"], facts[0]["provenance_refs"])

        materialized = list_manual_import_materialized_facts(self.conn, session["id"])
        self.assertEqual(3, len(materialized))
        self.assertTrue(all(row["active"] for row in materialized))
        self.assertEqual("version_side_by_side_with_source_precedence", materialized[0]["conflict_strategy"])
        self.assertEqual("reviewed_synthetic", materialized[0]["confidence"])
        self.assertEqual(64, len(materialized[0]["source_file_hash"]))
        self.assertIn("mapping_reference", materialized[0]["provenance"])

    def test_overlapping_fact_versions_side_by_side_with_precedence(self) -> None:
        session = preview_manual_import(self.conn, "garmin_activities_clean_csv")
        first = session["rows"][0]
        self.conn.execute(
            """
            INSERT INTO normalized_facts(id, fixture_id, domain, observed_at, value_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("prior_activity_fact", "prior_fixture", first["domain"], first["observed_at"], json.dumps({"prior": True})),
        )
        for row_index in (1, 2, 3):
            update_manual_import_row_review(self.conn, session["id"], row_index, "accepted")

        committed = commit_reviewed_manual_import(self.conn, session["id"])

        imported = committed["materialized_facts"][0]
        self.assertTrue(imported["active"])
        self.assertEqual(20, imported["precedence_rank"])
        self.assertTrue(imported["conflict_group_id"].startswith("materialization_conflict_"))
        rows = self.conn.execute(
            "SELECT existing_fact_id, conflict_strategy FROM manual_import_materialization_conflicts WHERE session_id = ?",
            (session["id"],),
        ).fetchall()
        self.assertEqual(1, len(rows))
        self.assertEqual("prior_activity_fact", rows[0]["existing_fact_id"])
        self.assertEqual("version_side_by_side_with_source_precedence", rows[0]["conflict_strategy"])
        self.assertIsNotNone(
            self.conn.execute("SELECT 1 FROM normalized_facts WHERE id = ?", ("prior_activity_fact",)).fetchone()
        )
        self.assertIsNotNone(
            self.conn.execute("SELECT 1 FROM normalized_facts WHERE id = ?", (imported["fact_id"],)).fetchone()
        )


if __name__ == "__main__":
    unittest.main()

