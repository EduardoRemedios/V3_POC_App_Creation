import unittest

from ppos_core.storage import connect, import_fixture, migrate, run_and_persist_workflow
from ppos_core.timeline import get_timeline, replay_audit_summary


class Mission009TimelineTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_workflow_run_persists_five_timeline_steps(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_training_ramp_too_fast.json")
        run = run_and_persist_workflow(self.conn, "dtu_training_ramp_too_fast", "ride_rest_recommendation")
        timeline = get_timeline(self.conn, run["id"])
        self.assertTrue(timeline["passed"])
        self.assertEqual(5, len(timeline["steps"]))

    def test_timeline_records_evidence_at_assembly_step(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_evidence_orphan_ref.json")
        run = run_and_persist_workflow(self.conn, "dtu_evidence_orphan_ref", "recovery_today")
        timeline = get_timeline(self.conn, run["id"])
        refs = [step["evidence_refs"] for step in timeline["steps"] if step["step_name"] == "assemble_evidence"][0]
        self.assertIn("derived_orphan_evidence_ref", refs)

    def test_timeline_output_names_workflow(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_snapshot_export_roundtrip.json")
        run = run_and_persist_workflow(self.conn, "dtu_snapshot_export_roundtrip", "recovery_today")
        timeline = get_timeline(self.conn, run["id"])
        self.assertEqual("recovery_today", timeline["steps"][0]["output"]["workflow"])

    def test_replay_audit_summary_counts_runs(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_body_composition_recomp.json")
        run_and_persist_workflow(self.conn, "dtu_body_composition_recomp", "weight_trend_check")
        summary = replay_audit_summary(self.conn)
        self.assertEqual(1, summary["audit_count"])
        self.assertEqual(1, summary["passed_count"])

    def test_timeline_empty_for_unknown_run(self):
        timeline = get_timeline(self.conn, "missing_run")
        self.assertFalse(timeline["passed"])
        self.assertEqual([], timeline["steps"])

    def test_timeline_step_order_is_stable(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_sleep_recovery_low_hrv_edge.json")
        run = run_and_persist_workflow(self.conn, "dtu_sleep_recovery_low_hrv_edge", "recovery_today")
        names = [step["step_name"] for step in get_timeline(self.conn, run["id"])["steps"]]
        self.assertEqual(["load_fixture", "derive_summary", "assemble_evidence", "safety_check", "persist_output"], names)

    def test_audit_summary_records_evidence_count(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_training_ramp_too_fast.json")
        run_and_persist_workflow(self.conn, "dtu_training_ramp_too_fast", "ride_rest_recommendation")
        item = replay_audit_summary(self.conn)["items"][0]
        self.assertGreaterEqual(item["evidence_ref_count"], 1)


if __name__ == "__main__":
    unittest.main()
