import unittest

from ppos_core.loader import load_fixtures
from ppos_core.reports import evening_report_candidate, morning_report_candidate
from ppos_core.workflows import run_workflow


class Mission007WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures()
        cls.by_id = {fixture.fixture_id: fixture for fixture in cls.fixtures}

    def test_gate_e_expected_workflow_contracts_pass(self):
        for fixture in self.fixtures:
            for workflow_name, expected in fixture.expected.get("workflows", {}).items():
                if workflow_name == "morning_report_candidate":
                    result = morning_report_candidate(fixture)
                    self.assertEqual(expected["recommendation_class"], result.output["recommendation_class"])
                    self.assertEqual(tuple(expected["sections"]), result.sections)
                elif workflow_name == "evening_report_candidate":
                    result = evening_report_candidate(fixture)
                    self.assertEqual(expected["recommendation_class"], result.output["recommendation_class"])
                    self.assertEqual(tuple(expected["sections"]), result.sections)
                else:
                    result = run_workflow(workflow_name, fixture)
                    expected_class = expected.get("recommendation_class") or expected.get("status") or expected.get("trend")
                    self.assertEqual(expected_class, result.recommendation_class)
                for ref in expected.get("required_evidence_refs", []):
                    self.assertIn(ref, result.evidence_pack.refs, f"{fixture.fixture_id}:{workflow_name}:{ref}")

    def test_all_initial_workflows_are_callable(self):
        fixture = self.by_id["dtu_baseline_healthy_week"]
        for workflow_name in (
            "recovery_today",
            "sleep_cause_analysis",
            "four_week_training_analysis",
            "ride_rest_recommendation",
        ):
            result = run_workflow(workflow_name, fixture)
            self.assertEqual("candidate", result.status)
            self.assertTrue(result.evidence_pack.refs)
        nutrition = run_workflow("nutrition_label_capture", self.by_id["dtu_greek_yoghurt_label_image"])
        self.assertEqual("pending_quantity_confirmation", nutrition.recommendation_class)

    def test_gate_f_report_candidates_are_not_delivered(self):
        morning = morning_report_candidate(self.by_id["dtu_morning_report_normal"])
        evening = evening_report_candidate(self.by_id["dtu_evening_report_nutrition_gap"])
        self.assertEqual("candidate_not_delivered", morning.delivery_status)
        self.assertEqual("candidate_not_delivered", evening.delivery_status)
        self.assertEqual("What did you eat after the ride?", evening.output["clarification"])

    def test_gate_f_no_prohibited_claims_in_outputs(self):
        for fixture in self.fixtures:
            for workflow_name in fixture.expected.get("workflows", {}):
                if workflow_name == "morning_report_candidate":
                    text = morning_report_candidate(fixture).output["text"]
                elif workflow_name == "evening_report_candidate":
                    text = evening_report_candidate(fixture).output["text"]
                else:
                    text = run_workflow(workflow_name, fixture).output["text"]
                lowered = text.lower()
                for claim in fixture.expected.get("prohibited_claims", []):
                    self.assertNotIn(claim.lower(), lowered, f"{fixture.fixture_id}:{claim}")


if __name__ == "__main__":
    unittest.main()
