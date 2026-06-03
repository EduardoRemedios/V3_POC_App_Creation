import json
import unittest
from pathlib import Path

from ppos_core.audit import WORKBENCH_VIEWS, build_audit_summary
from ppos_core.api_contracts import contract_rows, error_examples, problem_detail
from ppos_core.storage import connect, import_all_fixtures


class Mission009AuditTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        import_all_fixtures(self.conn)

    def test_audit_summary_contains_fixture_count(self):
        payload = build_audit_summary(self.conn, gates={"A": "PASS"}, test_check_count=140)
        self.assertEqual(36, payload["fixture_count"])

    def test_audit_summary_contains_db_tables(self):
        payload = build_audit_summary(self.conn, gates={"A": "PASS"}, test_check_count=140)
        self.assertIn("workflow_timeline_steps", payload["db_tables"])
        self.assertIn("evidence_graph_nodes", payload["db_tables"])

    def test_audit_summary_contains_workbench_views(self):
        payload = build_audit_summary(self.conn, gates={"A": "PASS"}, test_check_count=140)
        self.assertEqual(WORKBENCH_VIEWS, payload["workbench_views"])

    def test_api_contract_matrix_has_error_cases(self):
        rows = contract_rows()
        self.assertGreaterEqual(len(rows), 25)
        self.assertTrue(any(row["error_shape"] for row in rows))

    def test_problem_detail_shape_is_machine_readable(self):
        payload = problem_detail(400, "Example Error", "Example detail.", "/api/example", "field")
        self.assertEqual({"type", "title", "status", "detail", "instance", "field"}, set(payload))

    def test_error_examples_include_unknown_workflow(self):
        titles = {item["title"] for item in error_examples()}
        self.assertIn("Unknown Workflow", titles)

    def test_audit_summary_shell_json_parses(self):
        path = Path(".factory-v3/evidence/MISSION_009_AUDIT_SUMMARY.json")
        self.assertIsInstance(json.loads(path.read_text(encoding="utf-8")), dict)


if __name__ == "__main__":
    unittest.main()
