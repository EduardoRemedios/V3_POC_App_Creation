import unittest

from ppos_core.evidence_graph import graph_counts, graph_payload, refresh_evidence_graph
from ppos_core.storage import connect, import_fixture, run_and_persist_workflow


class Mission009EvidenceGraphTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")

    def test_import_persists_graph_nodes_and_edges(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_nutrition_label_basis_ambiguity.json")
        counts = graph_counts(self.conn, "dtu_nutrition_label_basis_ambiguity")
        self.assertGreater(counts["node_count"], 0)
        self.assertGreater(counts["edge_count"], 0)

    def test_graph_payload_can_filter_by_fixture(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_deload_recovery.json")
        payload = graph_payload(self.conn, "dtu_deload_recovery")
        self.assertTrue(payload["nodes"])
        self.assertTrue(all(node["fixture_id"] == "dtu_deload_recovery" for node in payload["nodes"]))

    def test_workflow_run_adds_workflow_node(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_training_ramp_too_fast.json")
        run_and_persist_workflow(self.conn, "dtu_training_ramp_too_fast", "ride_rest_recommendation")
        node_types = {node["node_type"] for node in graph_payload(self.conn, "dtu_training_ramp_too_fast")["nodes"]}
        self.assertIn("workflow_run", node_types)

    def test_evidence_pack_edges_are_present(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_evidence_orphan_ref.json")
        run_and_persist_workflow(self.conn, "dtu_evidence_orphan_ref", "recovery_today")
        relations = {edge["relation"] for edge in graph_payload(self.conn, "dtu_evidence_orphan_ref")["edges"]}
        self.assertIn("cited_by", relations)

    def test_recommendation_nodes_are_present_on_import(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_synthetic_voice_followup_outcome.json")
        node_types = {node["node_type"] for node in graph_payload(self.conn, "dtu_synthetic_voice_followup_outcome")["nodes"]}
        self.assertIn("recommendation", node_types)

    def test_followup_edges_are_present(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_synthetic_voice_followup_outcome.json")
        relations = {edge["relation"] for edge in graph_payload(self.conn, "dtu_synthetic_voice_followup_outcome")["edges"]}
        self.assertIn("followed_by", relations)

    def test_refresh_graph_is_idempotent_for_counts(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_body_composition_recomp.json")
        before = graph_counts(self.conn, "dtu_body_composition_recomp")
        refresh_evidence_graph(self.conn, "dtu_body_composition_recomp")
        after = graph_counts(self.conn, "dtu_body_composition_recomp")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
