from __future__ import annotations

import unittest

from ppos_core.storage import (
    commit_reviewed_manual_import,
    connect,
    get_manual_import_conflicts,
    get_manual_import_mapping,
    migrate,
    preview_manual_import,
    update_manual_import_row_review,
)


class Mission013BridgeAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_garmin_exports_use_existing_preview_review_commit_pipeline(self) -> None:
        session = preview_manual_import(self.conn, "garmin_activities_clean_csv")
        self.assertEqual("garmin_import_garmin_activities_clean_csv", session["id"])
        self.assertEqual("previewed", session["status"])
        self.assertEqual({"accepted": 0, "rejected": 0, "needs_clarification": 3}, session["review_summary"])
        self.assertEqual("garmin_bridge_activities_csv", session["adapter_id"])

        for row_index in (1, 2, 3):
            update_manual_import_row_review(self.conn, session["id"], row_index, "accepted", "Mission 013 synthetic Garmin row")

        committed = commit_reviewed_manual_import(self.conn, session["id"])
        self.assertEqual("committed", committed["status"])
        self.assertEqual({"accepted": 3, "rejected": 0, "needs_clarification": 0}, committed["review_summary"])
        self.assertEqual("committed", committed["audit_events"][-1]["event_type"])

    def test_garmin_mapping_and_conflicts_persist_for_edge_preview(self) -> None:
        session = preview_manual_import(self.conn, "garmin_body_composition_edge_csv")
        self.assertEqual("previewed", session["status"])
        self.assertEqual(1, session["conflict_count"])
        self.assertFalse(session["summary"]["can_commit"])

        mapping = get_manual_import_mapping(self.conn, session["id"])
        conflicts = get_manual_import_conflicts(self.conn, session["id"])
        self.assertEqual(session["id"], mapping["session_id"])
        self.assertGreater(len(mapping["mappings"]), 0)
        self.assertEqual("unit_conflict", conflicts["conflicts"][0]["conflict_type"])


if __name__ == "__main__":
    unittest.main()

