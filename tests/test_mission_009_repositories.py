import unittest

from ppos_core.loader import load_fixtures
from ppos_core.repositories import WorkbenchRepository
from ppos_core.storage import connect, import_all_fixtures, import_fixture, migrate


class Mission009RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_mission_009_migration_records_version(self):
        row = self.conn.execute("SELECT version FROM schema_migrations WHERE version = ?", ("002_mission_009",)).fetchone()
        self.assertIsNotNone(row)

    def test_repository_lists_new_tables(self):
        tables = set(WorkbenchRepository(self.conn).table_names())
        for table in ("workflow_timeline_steps", "evidence_graph_nodes", "recommendations", "safety_boundary_events"):
            self.assertIn(table, tables)

    def test_import_all_fixtures_persists_36_imports(self):
        imports = import_all_fixtures(self.conn)
        self.assertEqual(36, len(imports))
        self.assertEqual(len(load_fixtures()), len(imports))

    def test_source_query_returns_payloads(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_training_ramp_too_fast.json")
        records = WorkbenchRepository(self.conn).source_records("dtu_training_ramp_too_fast")
        self.assertTrue(records)
        self.assertIn("payload", records[0])

    def test_normalized_fact_query_returns_provenance_refs(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_nutrition_label_basis_ambiguity.json")
        facts = WorkbenchRepository(self.conn).normalized_facts("dtu_nutrition_label_basis_ambiguity")
        self.assertTrue(all(fact["provenance_refs"] for fact in facts))

    def test_derived_fact_query_includes_edge_signal(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_evidence_orphan_ref.json")
        names = {fact["name"] for fact in WorkbenchRepository(self.conn).derived_facts("dtu_evidence_orphan_ref")}
        self.assertIn("orphan_evidence_ref", names)

    def test_report_settings_query_returns_imported_preferences(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_report_settings_quiet_depth.json")
        settings = WorkbenchRepository(self.conn).report_settings()
        self.assertEqual("concise", settings[0]["morning_depth"])

    def test_replay_audit_query_is_empty_before_workflow_run(self):
        self.assertEqual([], WorkbenchRepository(self.conn).replay_audits())


if __name__ == "__main__":
    unittest.main()
