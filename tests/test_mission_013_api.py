from __future__ import annotations

import unittest

from ppos_core.api import WorkbenchAPI


class Mission013APITests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = WorkbenchAPI(":memory:")

    def test_garmin_exports_and_approval_routes(self) -> None:
        status, exports = self.api.handle("GET", "/api/garmin-exports")
        self.assertEqual(200, status)
        self.assertGreaterEqual(len(exports["exports"]), 7)

        status, approval = self.api.handle(
            "POST",
            "/api/manual-imports/approval",
            {
                "export_id": "garmin_activities_clean_csv",
                "retention_posture": "keep-raw-until-verified",
                "approval_state": "approved",
                "preview_only": True,
                "consent_text": "Synthetic API approval rehearsal.",
            },
        )
        self.assertEqual(200, status)
        self.assertEqual("real_garmin_manual_export", approval["approval"]["source_label"])

        status, approvals = self.api.handle("GET", "/api/manual-imports/approvals")
        self.assertEqual(200, status)
        self.assertEqual(1, len(approvals["approvals"]))

    def test_committed_garmin_import_can_be_consumed_by_api(self) -> None:
        status, preview = self.api.handle("POST", "/api/manual-imports/preview", {"export_id": "garmin_activities_clean_csv"})
        self.assertEqual(200, status)
        session_id = preview["session"]["id"]
        for row_index in (1, 2, 3):
            status, _ = self.api.handle(
                "POST",
                "/api/manual-imports/review-row",
                {"session_id": session_id, "row_index": row_index, "review_state": "accepted"},
            )
            self.assertEqual(200, status)

        status, committed = self.api.handle("POST", "/api/manual-imports/commit-reviewed", {"session_id": session_id})
        self.assertEqual(200, status)
        self.assertEqual("committed", committed["session"]["status"])

        status, consumed = self.api.handle("POST", f"/api/manual-imports/{session_id}/consume", {})
        self.assertEqual(200, status)
        self.assertGreaterEqual(consumed["consumption"]["workflow_count"], 2)
        self.assertGreater(consumed["consumption"]["graph"]["node_count"], 0)


if __name__ == "__main__":
    unittest.main()
