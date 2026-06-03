import unittest

from ppos_core.recommendations import list_follow_up_outcomes, list_recommendations, list_report_settings
from ppos_core.safety_audit import list_safety_events, safety_summary
from ppos_core.storage import connect, import_fixture, run_and_persist_workflow


class Mission009RecommendationsTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")

    def test_expected_workflow_creates_recommendation_history(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_training_ramp_too_fast.json")
        classes = {item["recommendation_class"] for item in list_recommendations(self.conn)}
        self.assertIn("ramp_caution", classes)

    def test_workflow_run_records_recommendation_history(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_body_composition_recomp.json")
        run_and_persist_workflow(self.conn, "dtu_body_composition_recomp", "weight_trend_check")
        statuses = {item["status"] for item in list_recommendations(self.conn)}
        self.assertIn("workflow_recorded", statuses)

    def test_followup_outcome_records_synthetic_voice_result(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_synthetic_voice_followup_outcome.json")
        outcomes = list_follow_up_outcomes(self.conn)
        self.assertEqual(1, len(outcomes))
        self.assertEqual("outcome_recorded", outcomes[0]["outcome_status"])

    def test_report_settings_persist_quiet_hours(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_report_settings_quiet_depth.json")
        settings = list_report_settings(self.conn)[0]
        self.assertEqual("21:30", settings["quiet_hours_start"])
        self.assertEqual("07:30", settings["quiet_hours_end"])

    def test_safety_events_include_input_quality_boundary(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_malformed_missing_observed_at.json")
        boundary_types = {event["boundary_type"] for event in list_safety_events(self.conn)}
        self.assertIn("input_quality_boundary", boundary_types)

    def test_safety_summary_counts_no_delivery(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_weekly_report_suppressed_cooldown.json")
        self.assertGreaterEqual(safety_summary(self.conn)["no_delivery_count"], 1)

    def test_recommendation_links_thread_when_present(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_cross_surface_report_review.json")
        threads = {item["thread_id"] for item in list_recommendations(self.conn)}
        self.assertIn("thread_report_review_001", threads)


if __name__ == "__main__":
    unittest.main()
