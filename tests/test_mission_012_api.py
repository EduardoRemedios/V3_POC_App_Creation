from __future__ import annotations

import unittest

from ppos_core.api import WorkbenchAPI


class Mission012APITests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = WorkbenchAPI(":memory:")

    def test_review_row_and_commit_reviewed_endpoints(self) -> None:
        status, preview = self.api.handle("POST", "/api/manual-imports/preview", {"export_id": "manual_activity_csv_clean"})
        self.assertEqual(200, status)
        session_id = preview["session"]["id"]
        self.assertEqual({"accepted": 0, "rejected": 0, "needs_clarification": 3}, preview["session"]["review_summary"])

        for row_index in (1, 2, 3):
            status, reviewed = self.api.handle(
                "POST",
                "/api/manual-imports/review-row",
                {"session_id": session_id, "row_index": row_index, "review_state": "accepted"},
            )
            self.assertEqual(200, status)

        self.assertEqual({"accepted": 3, "rejected": 0, "needs_clarification": 0}, reviewed["session"]["review_summary"])
        status, committed = self.api.handle("POST", "/api/manual-imports/commit-reviewed", {"session_id": session_id})
        self.assertEqual(200, status)
        self.assertEqual("committed", committed["session"]["status"])

    def test_reviewed_commit_error_and_rollback_endpoint(self) -> None:
        status, preview = self.api.handle("POST", "/api/manual-imports/preview", {"export_id": "manual_activity_csv_clean"})
        self.assertEqual(200, status)
        session_id = preview["session"]["id"]

        status, problem = self.api.handle("POST", "/api/manual-imports/commit-reviewed", {"session_id": session_id})
        self.assertEqual(400, status)
        self.assertIn("needing clarification", problem["detail"])

        status, committed = self.api.handle(
            "POST", "/api/manual-imports/commit-synthetic", {"export_id": "manual_activity_csv_clean"}
        )
        self.assertEqual(200, status)
        status, reverted = self.api.handle(
            "POST",
            "/api/manual-imports/rollback",
            {"session_id": committed["session"]["id"], "reason": "synthetic API rollback"},
        )
        self.assertEqual(200, status)
        self.assertEqual("reverted", reverted["session"]["status"])
        self.assertEqual("synthetic API rollback", reverted["session"]["rollback_reason"])

        status, audit = self.api.handle("GET", "/api/manual-imports/audit-summary")
        self.assertEqual(200, status)
        self.assertEqual(1, audit["manual_import_audit"]["reverted_session_count"])


if __name__ == "__main__":
    unittest.main()
