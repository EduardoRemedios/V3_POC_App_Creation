from __future__ import annotations

import unittest

from ppos_core.api import WorkbenchAPI


class Mission011APITests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = WorkbenchAPI(":memory:")

    def test_source_adapter_and_manual_export_catalog_endpoints(self) -> None:
        status, adapters = self.api.handle("GET", "/api/source-adapters")
        self.assertEqual(200, status)
        self.assertGreaterEqual(len(adapters["adapters"]), 5)

        status, exports = self.api.handle("GET", "/api/manual-exports")
        self.assertEqual(200, status)
        self.assertEqual(9, len(exports["exports"]))

        status, detail = self.api.handle("GET", "/api/manual-exports/manual_activity_csv_duplicate")
        self.assertEqual(200, status)
        self.assertEqual(4, detail["export"]["preview_summary"]["row_count"])

    def test_preview_mapping_conflict_and_audit_endpoints(self) -> None:
        status, preview = self.api.handle(
            "POST", "/api/manual-imports/preview", {"export_id": "manual_activity_csv_duplicate"}
        )
        self.assertEqual(200, status)
        session_id = preview["session"]["id"]
        self.assertEqual("previewed", preview["session"]["status"])
        self.assertEqual(1, preview["session"]["conflict_count"])

        status, mapping = self.api.handle("GET", f"/api/manual-imports/{session_id}/mapping")
        self.assertEqual(200, status)
        self.assertGreater(len(mapping["mappings"]), 0)

        status, conflicts = self.api.handle("GET", f"/api/manual-imports/{session_id}/conflicts")
        self.assertEqual(200, status)
        self.assertEqual(1, len(conflicts["conflicts"]))

        status, audit = self.api.handle("GET", "/api/manual-imports/audit-summary")
        self.assertEqual(200, status)
        self.assertEqual(1, audit["manual_import_audit"]["session_count"])

    def test_commit_synthetic_and_error_contract(self) -> None:
        status, committed = self.api.handle(
            "POST", "/api/manual-imports/commit-synthetic", {"export_id": "manual_weight_body_csv"}
        )
        self.assertEqual(200, status)
        self.assertEqual("committed", committed["session"]["status"])

        status, problem = self.api.handle("POST", "/api/manual-imports/preview", {})
        self.assertEqual(400, status)
        self.assertEqual("Local API Error", problem["title"])

        status, problem = self.api.handle(
            "POST", "/api/manual-imports/commit-synthetic", {"export_id": "manual_malformed_missing_time_csv"}
        )
        self.assertEqual(400, status)
        self.assertIn("validation errors", problem["detail"])


if __name__ == "__main__":
    unittest.main()
