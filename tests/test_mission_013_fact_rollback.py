from __future__ import annotations

import unittest

from ppos_core.storage import (
    commit_reviewed_manual_import,
    connect,
    list_manual_import_materialized_facts,
    list_normalized_facts,
    manual_import_audit_summary,
    migrate,
    preview_manual_import,
    rollback_manual_import,
    update_manual_import_row_review,
)


class Mission013FactRollbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_rollback_unmaterializes_imported_facts_and_preserves_ledger(self) -> None:
        session = preview_manual_import(self.conn, "garmin_body_composition_clean_csv")
        for row_index in (1, 2, 3):
            update_manual_import_row_review(self.conn, session["id"], row_index, "accepted")
        committed = commit_reviewed_manual_import(self.conn, session["id"])
        self.assertEqual(3, len(list_normalized_facts(self.conn, session["id"])))
        self.assertEqual(3, len(committed["materialized_facts"]))

        reverted = rollback_manual_import(self.conn, session["id"], "Mission 013 fact rollback")

        self.assertEqual("reverted", reverted["status"])
        self.assertEqual([], list_normalized_facts(self.conn, session["id"]))
        materialized = list_manual_import_materialized_facts(self.conn, session["id"])
        self.assertEqual(3, len(materialized))
        self.assertTrue(all(not row["active"] for row in materialized))
        self.assertTrue(all(row["rollback_reason"] == "Mission 013 fact rollback" for row in materialized))

        audit = manual_import_audit_summary(self.conn)
        self.assertEqual(0, audit["materialized_fact_count"])
        self.assertEqual(3, audit["reverted_materialized_fact_count"])


if __name__ == "__main__":
    unittest.main()

