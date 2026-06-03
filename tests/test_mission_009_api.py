import unittest

from ppos_core.api import WorkbenchAPI


class Mission009APITests(unittest.TestCase):
    def setUp(self):
        self.api = WorkbenchAPI(":memory:")

    def test_fixture_manifest_endpoint(self):
        status, payload = self.api.handle("GET", "/api/fixture-manifest")
        self.assertEqual(200, status)
        self.assertTrue(payload["validation"]["passed"])

    def test_fixture_families_endpoint(self):
        status, payload = self.api.handle("GET", "/api/fixture-families")
        self.assertEqual(200, status)
        self.assertGreaterEqual(len(payload["families"]), 8)

    def test_expected_workflows_endpoint(self):
        status, payload = self.api.handle("GET", "/api/fixtures/expected-workflows")
        self.assertEqual(200, status)
        self.assertIn({"fixture_id": "dtu_training_ramp_too_fast", "workflow": "ride_rest_recommendation"}, payload["workflow_matrix"])

    def test_import_audit_summary_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_deload_recovery"})
        status, payload = self.api.handle("GET", "/api/imports/audit-summary")
        self.assertEqual(200, status)
        self.assertEqual(1, payload["import_count"])

    def test_workflow_timeline_endpoint(self):
        _, payload = self.api.handle("POST", "/api/workflows/run", {"fixture_id": "dtu_training_ramp_too_fast", "workflow": "ride_rest_recommendation"})
        run_id = payload["workflow_run"]["id"]
        status, payload = self.api.handle("GET", f"/api/workflows/{run_id}/timeline")
        self.assertEqual(200, status)
        self.assertEqual(5, len(payload["timeline"]["steps"]))

    def test_evidence_graph_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_evidence_orphan_ref"})
        status, payload = self.api.handle("GET", "/api/evidence-graph/dtu_evidence_orphan_ref")
        self.assertEqual(200, status)
        self.assertTrue(payload["graph"]["nodes"])

    def test_recommendations_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_training_ramp_too_fast"})
        status, payload = self.api.handle("GET", "/api/recommendations")
        self.assertEqual(200, status)
        self.assertTrue(payload["recommendations"])

    def test_followup_outcomes_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_synthetic_voice_followup_outcome"})
        status, payload = self.api.handle("GET", "/api/follow-up-outcomes")
        self.assertEqual(200, status)
        self.assertEqual(1, len(payload["follow_up_outcomes"]))

    def test_report_settings_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_report_settings_quiet_depth"})
        status, payload = self.api.handle("GET", "/api/report-settings")
        self.assertEqual(200, status)
        self.assertEqual("concise", payload["report_settings"][0]["morning_depth"])

    def test_safety_audit_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_incomplete_source_payload"})
        status, payload = self.api.handle("GET", "/api/safety-audit")
        self.assertEqual(200, status)
        self.assertGreater(payload["safety_audit"]["event_count"], 0)

    def test_snapshot_export_and_validate_endpoint(self):
        self.api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_snapshot_export_roundtrip"})
        status, payload = self.api.handle("GET", "/api/snapshot/export")
        self.assertEqual(200, status)
        status, validation = self.api.handle("POST", "/api/snapshot/validate-import", {"snapshot": payload["snapshot"]})
        self.assertEqual(200, status)
        self.assertTrue(validation["validation"]["valid"])

    def test_contracts_and_error_examples_endpoint(self):
        status, contracts = self.api.handle("GET", "/api/contracts")
        self.assertEqual(200, status)
        self.assertGreaterEqual(len(contracts["contracts"]), 25)
        status, errors = self.api.handle("GET", "/api/error-examples")
        self.assertEqual(200, status)
        self.assertIn("type", errors["errors"][0])

    def test_unknown_workflow_returns_problem_detail_shape(self):
        status, payload = self.api.handle("POST", "/api/workflows/run", {"fixture_id": "dtu_api_unknown_workflow", "workflow": "not_a_workflow"})
        self.assertEqual(400, status)
        self.assertEqual(400, payload["status"])
        self.assertIn("type", payload)

    def test_missing_route_returns_404_problem_detail(self):
        status, payload = self.api.handle("GET", "/api/not-a-route")
        self.assertEqual(404, status)
        self.assertEqual("Not Found", payload["title"])


if __name__ == "__main__":
    unittest.main()
