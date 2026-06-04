from __future__ import annotations

import unittest

from ppos_core.storage import (
    commit_reviewed_manual_import,
    connect,
    get_workflow_timeline,
    list_evidence_graph,
    list_report_candidates,
    migrate,
    preview_manual_import,
    run_manual_import_consumption,
    update_manual_import_row_review,
)


class Mission013WorkflowIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_materialized_import_facts_feed_workflows_timeline_graph_and_reports(self) -> None:
        session = preview_manual_import(self.conn, "garmin_activities_clean_csv")
        for row_index in (1, 2, 3):
            update_manual_import_row_review(self.conn, session["id"], row_index, "accepted")
        committed = commit_reviewed_manual_import(self.conn, session["id"])

        consumption = run_manual_import_consumption(self.conn, committed["id"])

        self.assertEqual(committed["id"], consumption["session_id"])
        self.assertGreaterEqual(consumption["workflow_count"], 2)
        self.assertIn("recovery_today", {run["workflow"] for run in consumption["workflows"]})
        self.assertIn("four_week_training_analysis", {run["workflow"] for run in consumption["workflows"]})
        for run_id in consumption["timeline_run_ids"]:
            timeline = get_workflow_timeline(self.conn, run_id)
            self.assertTrue(timeline["passed"])
            self.assertGreaterEqual(len(timeline["steps"]), 5)

        reports = [report for report in list_report_candidates(self.conn) if report["fixture_id"] == committed["id"]]
        self.assertEqual({"morning", "evening"}, {report["report_type"] for report in reports})
        self.assertTrue(all(report["delivery_status"] == "candidate_not_delivered" for report in reports))

        graph = list_evidence_graph(self.conn, committed["id"])
        self.assertGreater(consumption["graph"]["node_count"], 0)
        self.assertGreater(len(graph["nodes"]), 0)
        self.assertIn("workflow_run", {node["node_type"] for node in graph["nodes"]})
        self.assertIn("report_candidate", {node["node_type"] for node in graph["nodes"]})


if __name__ == "__main__":
    unittest.main()
