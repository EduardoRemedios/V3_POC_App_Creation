from __future__ import annotations

import unittest

from ppos_core.storage import connect, manual_import_audit_summary, migrate, preview_manual_import, rollback_manual_import


class Mission012RollbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_rollback_marks_committed_session_reverted_without_deleting_audit_history(self) -> None:
        committed = preview_manual_import(self.conn, "manual_weight_body_csv", commit=True)
        self.assertEqual("committed", committed["status"])
        self.assertEqual(1, len(committed["audit_events"]))

        reverted = rollback_manual_import(self.conn, committed["id"], "synthetic operator rollback check")
        self.assertEqual("reverted", reverted["status"])
        self.assertIsNotNone(reverted["reverted_at"])
        self.assertEqual("synthetic operator rollback check", reverted["rollback_reason"])
        self.assertEqual("rolled_back", reverted["audit_events"][-1]["event_type"])
        self.assertEqual(2, len(reverted["audit_events"]))
        self.assertEqual(committed["row_count"], len(reverted["rows"]))

        audit = manual_import_audit_summary(self.conn)
        self.assertEqual(0, audit["committed_session_count"])
        self.assertEqual(1, audit["reverted_session_count"])
        self.assertEqual(2, audit["audit_event_count"])

    def test_rollback_requires_committed_session(self) -> None:
        previewed = preview_manual_import(self.conn, "manual_activity_csv_clean")
        with self.assertRaises(ValueError):
            rollback_manual_import(self.conn, previewed["id"])


if __name__ == "__main__":
    unittest.main()
