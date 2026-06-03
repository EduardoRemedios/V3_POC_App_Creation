import unittest
from pathlib import Path

from ppos_core.loader import load_fixtures
from ppos_core.reports import evening_report_candidate, morning_report_candidate
from ppos_core.workflows import run_workflow


FORBIDDEN_OPERATIONAL_MARKERS = (
    "api_token=",
    "bot_token=",
    "garmin_password=",
    "oauth_secret=",
    "webhook_url=",
    "cron_expression=",
)


class Mission008SafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures()

    def test_all_fixtures_are_synthetic_only(self):
        self.assertTrue(all(fixture.synthetic_only for fixture in self.fixtures))

    def test_no_fixture_contains_operational_secret_markers(self):
        for path in Path("fixtures/dtu").glob("*.json"):
            text = path.read_text(encoding="utf-8").lower()
            for marker in FORBIDDEN_OPERATIONAL_MARKERS:
                self.assertNotIn(marker, text, path.name)

    def test_no_workflow_output_contains_prohibited_claims(self):
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

    def test_report_candidates_are_not_delivered(self):
        morning = morning_report_candidate(self.fixtures_by_id()["dtu_morning_report_fatigue"])
        evening = evening_report_candidate(self.fixtures_by_id()["dtu_evening_report_recovery_setup"])
        self.assertEqual("candidate_not_delivered", morning.delivery_status)
        self.assertEqual("candidate_not_delivered", evening.delivery_status)

    def test_static_workbench_has_no_live_integration_terms(self):
        text = "\n".join(Path(path).read_text(encoding="utf-8").lower() for path in Path("workbench").glob("*"))
        for term in ("telegram token", "garmin credentials", "webhook_url", "ocr api", "voice transcription api"):
            self.assertNotIn(term, text)

    def test_mission_record_defaults_are_compliant(self):
        text = Path(".factory-v3/evidence/MISSION_008_RECORD.json").read_text(encoding="utf-8")
        self.assertIn('"v3_only": true', text)
        self.assertIn('"synthetic_only": true', text)
        self.assertIn('"packages_installed": []', text)

    def fixtures_by_id(self):
        return {fixture.fixture_id: fixture for fixture in self.fixtures}


if __name__ == "__main__":
    unittest.main()
