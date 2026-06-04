from __future__ import annotations

import unittest

from ppos_core.storage import (
    commit_reviewed_manual_import,
    connect,
    manual_import_audit_summary,
    migrate,
    preview_manual_import,
    update_manual_import_row_review,
)


class Mission012ReviewWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_preview_rows_default_to_needs_clarification_and_can_be_reviewed(self) -> None:
        session = preview_manual_import(self.conn, "manual_activity_csv_clean")
        self.assertEqual("previewed", session["status"])
        self.assertEqual({"accepted": 0, "rejected": 0, "needs_clarification": 3}, session["review_summary"])

        reviewed = update_manual_import_row_review(self.conn, session["id"], 1, "accepted", "synthetic row checked")
        self.assertEqual({"accepted": 1, "rejected": 0, "needs_clarification": 2}, reviewed["review_summary"])
        self.assertEqual("accepted", reviewed["rows"][0]["review_state"])
        self.assertEqual("synthetic row checked", reviewed["rows"][0]["review_note"])
        self.assertEqual("row_reviewed", reviewed["audit_events"][-1]["event_type"])

    def test_reviewed_commit_requires_no_needs_clarification_rows(self) -> None:
        session = preview_manual_import(self.conn, "manual_activity_csv_clean")
        update_manual_import_row_review(self.conn, session["id"], 1, "accepted")
        update_manual_import_row_review(self.conn, session["id"], 2, "accepted")

        with self.assertRaises(ValueError):
            commit_reviewed_manual_import(self.conn, session["id"])

        update_manual_import_row_review(self.conn, session["id"], 3, "rejected", "duplicate synthetic operator choice")
        committed = commit_reviewed_manual_import(self.conn, session["id"])
        self.assertEqual("committed", committed["status"])
        self.assertEqual({"accepted": 2, "rejected": 1, "needs_clarification": 0}, committed["review_summary"])
        self.assertEqual("committed", committed["audit_events"][-1]["event_type"])

        audit = manual_import_audit_summary(self.conn)
        self.assertEqual(1, audit["committed_session_count"])
        self.assertEqual({"accepted": 2, "rejected": 1, "needs_clarification": 0}, audit["review_summary"])


if __name__ == "__main__":
    unittest.main()
