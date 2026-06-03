import unittest

from ppos_core.loader import load_fixture, load_fixtures
from ppos_core.schema import REQUIRED_FIXTURES
from ppos_core.storage import (
    connect,
    get_import,
    import_all_fixtures,
    import_fixture,
    list_derived_facts,
    list_imports,
    list_normalized_facts,
    list_report_candidates,
    list_source_records,
    migrate,
)


class Mission008StorageTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_gate_b_loads_required_fixtures(self):
        fixtures = load_fixtures()
        self.assertGreaterEqual(len(fixtures), 22)
        self.assertEqual(REQUIRED_FIXTURES, {fixture.fixture_id for fixture in fixtures})

    def test_gate_d_schema_migration_records_version(self):
        row = self.conn.execute("SELECT version FROM schema_migrations WHERE version = ?", ("001_initial",)).fetchone()
        self.assertIsNotNone(row)

    def test_gate_d_schema_has_required_tables(self):
        names = {
            row["name"]
            for row in self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        }
        for table in ("source_records", "normalized_facts", "fact_provenance", "derived_facts", "workflow_runs"):
            self.assertIn(table, names)

    def test_gate_e_import_fixture_persists_counts(self):
        fixture = load_fixture("fixtures/dtu/dtu_baseline_healthy_week.json")
        result = import_fixture(self.conn, fixture)
        self.assertEqual(fixture.fixture_id, result["fixture_id"])
        self.assertEqual(len(fixture.source_records), result["source_record_count"])
        self.assertEqual(len(fixture.normalized_facts), result["normalized_fact_count"])

    def test_gate_e_import_is_idempotent_for_rows(self):
        fixture = load_fixture("fixtures/dtu/dtu_baseline_healthy_week.json")
        import_fixture(self.conn, fixture)
        import_fixture(self.conn, fixture)
        self.assertEqual(2, get_import(self.conn, fixture.fixture_id)["import_count"])
        self.assertEqual(len(fixture.source_records), len(list_source_records(self.conn, fixture.fixture_id)))
        self.assertEqual(len(fixture.normalized_facts), len(list_normalized_facts(self.conn, fixture.fixture_id)))

    def test_gate_e_raw_source_payloads_are_separate_from_normalized_facts(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_weight_loss_plateau.json")
        source = list_source_records(self.conn, "dtu_weight_loss_plateau")[0]
        fact = list_normalized_facts(self.conn, "dtu_weight_loss_plateau")[0]
        self.assertIn("payload", source)
        self.assertIn("value", fact)
        self.assertNotEqual(source["id"], fact["id"])

    def test_gate_e_normalized_facts_link_to_source_records(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_weight_loss_plateau.json")
        source_ids = {record["id"] for record in list_source_records(self.conn, "dtu_weight_loss_plateau")}
        for fact in list_normalized_facts(self.conn, "dtu_weight_loss_plateau"):
            self.assertTrue(set(fact["provenance_refs"]).issubset(source_ids))

    def test_gate_e_derived_facts_persist(self):
        import_fixture(self.conn, "fixtures/dtu/dtu_weight_loss_too_fast.json")
        names = {fact["name"] for fact in list_derived_facts(self.conn, "dtu_weight_loss_too_fast")}
        self.assertIn("rapid_weight_loss_caution", names)

    def test_import_all_fixtures_persists_all_fixtures(self):
        imports = import_all_fixtures(self.conn)
        self.assertEqual(len(load_fixtures()), len(imports))
        self.assertEqual(len(load_fixtures()), len(list_imports(self.conn)))

    def test_report_candidates_persist_on_import(self):
        import_all_fixtures(self.conn)
        report_ids = {report["fixture_id"] for report in list_report_candidates(self.conn)}
        self.assertIn("dtu_morning_report_fatigue", report_ids)
        self.assertIn("dtu_evening_report_recovery_setup", report_ids)


if __name__ == "__main__":
    unittest.main()
