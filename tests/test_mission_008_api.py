import unittest

from ppos_core.api import WorkbenchAPI


class Mission008APITests(unittest.TestCase):
    def setUp(self):
        self.api = WorkbenchAPI(":memory:")

    def test_health_endpoint(self):
        status, payload = self.api.handle("GET", "/api/health")
        self.assertEqual(200, status)
        self.assertTrue(payload["synthetic_only"])

    def test_fixture_list_endpoint(self):
        status, payload = self.api.handle("GET", "/api/fixtures")
        self.assertEqual(200, status)
        self.assertGreaterEqual(len(payload["fixtures"]), 22)

    def test_fixture_detail_endpoint(self):
        status, payload = self.api.handle("GET", "/api/fixtures/dtu_weight_loss_plateau")
        self.assertEqual(200, status)
        self.assertEqual("dtu_weight_loss_plateau", payload["fixture_id"])

    def test_import_fixture_endpoint(self):
        status, payload = self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_weight_loss_plateau"})
        self.assertEqual(200, status)
        self.assertEqual("dtu_weight_loss_plateau", payload["import"]["fixture_id"])

    def test_list_imports_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_weight_loss_plateau"})
        status, payload = self.api.handle("GET", "/api/imports")
        self.assertEqual(200, status)
        self.assertEqual(1, len(payload["imports"]))

    def test_run_and_get_workflow_endpoint(self):
        status, payload = self.api.handle(
            "POST",
            "/api/workflows/run",
            {"fixture_id": "dtu_weight_loss_too_fast", "workflow": "weight_trend_check"},
        )
        self.assertEqual(200, status)
        run_id = payload["workflow_run"]["id"]
        status, payload = self.api.handle("GET", f"/api/workflows/{run_id}")
        self.assertEqual(200, status)
        self.assertEqual("rapid_loss_caution", payload["workflow_run"]["recommendation_class"])

    def test_get_evidence_pack_endpoint(self):
        _, payload = self.api.handle(
            "POST",
            "/api/workflows/run",
            {"fixture_id": "dtu_weight_loss_too_fast", "workflow": "weight_trend_check"},
        )
        evidence_id = payload["workflow_run"]["evidence_pack_id"]
        status, payload = self.api.handle("GET", f"/api/evidence-packs/{evidence_id}")
        self.assertEqual(200, status)
        self.assertTrue(payload["evidence_pack"]["refs"])

    def test_report_candidates_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_morning_report_fatigue"})
        status, payload = self.api.handle("GET", "/api/report-candidates")
        self.assertEqual(200, status)
        self.assertTrue(payload["report_candidates"])

    def test_conversation_thread_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_cross_surface_recovery_handoff"})
        status, payload = self.api.handle("GET", "/api/conversation-threads/thread_recovery_001")
        self.assertEqual(200, status)
        self.assertEqual(2, len(payload["thread"]["messages"]))
        self.assertEqual(1, len(payload["thread"]["surface_events"]))

    def test_workbench_bootstrap_endpoint(self):
        status, payload = self.api.handle("GET", "/api/workbench/bootstrap")
        self.assertEqual(200, status)
        self.assertIn("fixture_selector", payload["mounts"])


if __name__ == "__main__":
    unittest.main()
