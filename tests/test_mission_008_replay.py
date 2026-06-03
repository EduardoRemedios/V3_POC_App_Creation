import unittest

from ppos_core.loader import load_fixtures
from ppos_core.replay import fixture_from_db, replay_all, replay_fixture
from ppos_core.storage import connect, get_evidence_pack, import_fixture, run_and_persist_workflow


class Mission008ReplayTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")

    def test_fixture_reconstructs_from_db_records(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_nutrition_free_text.json")
        fixture = fixture_from_db(self.conn, "dtu_nutrition_free_text")
        self.assertEqual("dtu_nutrition_free_text", fixture.fixture_id)
        self.assertEqual(2, len(fixture.source_records))
        self.assertEqual(2, len(fixture.normalized_facts))

    def test_db_workflow_run_persists_output(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_weight_loss_too_fast.json")
        run = run_and_persist_workflow(self.conn, "dtu_weight_loss_too_fast", "weight_trend_check")
        self.assertEqual("rapid_loss_caution", run["recommendation_class"])
        self.assertIn("summary", run["output"])

    def test_db_workflow_run_persists_evidence_refs(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_weight_loss_too_fast.json")
        run = run_and_persist_workflow(self.conn, "dtu_weight_loss_too_fast", "weight_trend_check")
        evidence = get_evidence_pack(self.conn, run["evidence_pack_id"])
        refs = {ref["ref_id"] for ref in evidence["refs"]}
        self.assertIn("derived_rapid_weight_loss_caution", refs)

    def test_replay_late_meal_contract_passes(self):
        replay = replay_fixture(self.conn, "dtu_late_high_fat_dinner_sleep_drop")
        self.assertTrue(replay["passed"])

    def test_replay_voice_contract_passes(self):
        replay = replay_fixture(self.conn, "dtu_voice_continuation_as_synthetic_transcript")
        self.assertTrue(replay["passed"])

    def test_replay_all_contracts_pass(self):
        results = replay_all(self.conn)
        self.assertEqual(len(load_fixtures()), len(results))
        self.assertTrue(all(result["passed"] for result in results))

    def test_replay_records_derived_fact_count(self):
        replay = replay_fixture(self.conn, "dtu_weekly_review_progress")
        self.assertGreaterEqual(replay["derived_fact_count"], 4)

    def test_report_workflows_are_compared_without_delivery(self):
        replay = replay_fixture(self.conn, "dtu_morning_report_fatigue")
        item = replay["workflow_results"][0]
        self.assertEqual("morning_report_candidate", item["workflow"])
        self.assertTrue(item["passed"])


if __name__ == "__main__":
    unittest.main()
