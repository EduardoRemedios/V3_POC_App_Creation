import unittest

from ppos_core.loader import load_fixture
from ppos_core.primitives import derive_summary, derived_facts


class Mission008PrimitiveTests(unittest.TestCase):
    def summary(self, fixture_id):
        return derive_summary(load_fixture(f"fixtures/dtu/{fixture_id}.json"))

    def test_sleep_cause_signal(self):
        summary = self.summary("dtu_late_high_fat_dinner_sleep_drop")
        self.assertTrue(summary["late_meal_sleep_association"])
        self.assertEqual(1.8, summary["sleep_drop_hours"])

    def test_protein_timing_signal(self):
        self.assertEqual(
            "distributed_improved",
            self.summary("dtu_protein_distribution_recovery_improves")["protein_distribution_pattern"],
        )

    def test_weight_plateau_signal(self):
        summary = self.summary("dtu_weight_loss_plateau")
        self.assertEqual("plateau", summary["weight_trend"])
        self.assertEqual(-0.1, summary["weight_change_kg"])

    def test_rapid_weight_loss_signal(self):
        summary = self.summary("dtu_weight_loss_too_fast")
        self.assertEqual("rapid_loss", summary["weight_trend"])
        self.assertTrue(summary["rapid_weight_loss_caution"])

    def test_hard_session_suppression_signal(self):
        self.assertTrue(self.summary("dtu_hard_session_suppressed_recovery")["hard_session_suppression"])

    def test_contradictory_metrics_signal(self):
        summary = self.summary("dtu_contradictory_metrics")
        self.assertTrue(summary["contradictory_metrics"])
        self.assertEqual("conflicted", summary["recovery_status"])

    def test_nutrition_free_text_signal(self):
        self.assertTrue(self.summary("dtu_nutrition_free_text")["nutrition_free_text_needs_clarification"])

    def test_morning_fatigue_signal(self):
        self.assertTrue(self.summary("dtu_morning_report_fatigue")["morning_fatigue_flag"])

    def test_evening_recovery_setup_signal(self):
        self.assertTrue(self.summary("dtu_evening_report_recovery_setup")["evening_recovery_setup"])

    def test_deload_recovery_trend_signal(self):
        self.assertEqual(
            "improving_after_deload",
            self.summary("dtu_weekly_review_progress")["deload_recovery_trend"],
        )

    def test_quiet_hours_suppression_signal(self):
        summary = self.summary("dtu_proactive_suppressed_quiet_hours")
        self.assertTrue(summary["quiet_hours_suppressed"])
        self.assertEqual("suppressed_quiet_hours", summary["proactive_delivery_status"])

    def test_prior_recommendation_followup_signal(self):
        summary = self.summary("dtu_prior_recommendation_followup")
        self.assertTrue(summary["prior_recommendation_followup_due"])
        self.assertEqual("improved_with_uncertainty", summary["sleep_followup_direction"])

    def test_voice_transcript_continuity_signal(self):
        self.assertTrue(self.summary("dtu_voice_continuation_as_synthetic_transcript")["voice_transcript_continuity"])

    def test_derived_fact_ids_cover_expanded_signals(self):
        fixture = load_fixture("fixtures/dtu/dtu_proactive_suppressed_quiet_hours.json")
        ids = {fact.id for fact in derived_facts(fixture)}
        self.assertIn("derived_quiet_hours_suppressed", ids)


if __name__ == "__main__":
    unittest.main()
