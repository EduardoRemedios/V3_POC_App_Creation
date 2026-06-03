import unittest

from ppos_core.loader import load_fixtures
from ppos_core.primitives import derive_summary, derived_facts
from ppos_core.schema import ALLOWED_SOURCES, MISSION_007_REQUIRED_FIXTURES


class Mission007CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures()
        cls.by_id = {fixture.fixture_id: fixture for fixture in cls.fixtures}

    def test_gate_b_required_fixture_files_load(self):
        self.assertTrue(MISSION_007_REQUIRED_FIXTURES.issubset(set(self.by_id)))

    def test_gate_c_sources_are_synthetic_and_allowed(self):
        for fixture in self.fixtures:
            self.assertTrue(fixture.synthetic_only)
            for source in fixture.sources:
                self.assertIn(source, ALLOWED_SOURCES)
                self.assertTrue(source.startswith("synthetic_") or source == "manual_note")

    def test_gate_c_normalized_facts_preserve_provenance(self):
        for fixture in self.fixtures:
            self.assertEqual(len(fixture.source_records), len(fixture.normalized_facts))
            source_ids = fixture.record_ids()
            for fact in fixture.normalized_facts:
                self.assertEqual(1, len(fact.provenance_refs))
                self.assertIn(fact.provenance_refs[0], source_ids)
                self.assertIn("payload", fact.value)
                self.assertIn("source", fact.value)

    def test_gate_d_derived_facts_match_fixture_expectations(self):
        for fixture in self.fixtures:
            summary = derive_summary(fixture)
            for key, expected_value in fixture.expected.get("derived", {}).items():
                self.assertEqual(expected_value, summary.get(key), f"{fixture.fixture_id}:{key}")

    def test_gate_d_deduplicates_duplicate_import(self):
        fixture = self.by_id["dtu_duplicate_import"]
        summary = derive_summary(fixture)
        self.assertEqual(1, summary["duplicate_activity_pairs"])
        self.assertEqual(1, summary["canonical_activity_count"])
        self.assertEqual(96, summary["training_load_7d"])

    def test_gate_d_timezone_boundary_uses_local_domain_rules(self):
        fixture = self.by_id["dtu_timezone_boundary"]
        summary = derive_summary(fixture)
        self.assertEqual("2026-06-01", summary["activity_local_date"])
        self.assertEqual("2026-06-02", summary["sleep_local_date"])

    def test_gate_d_derived_fact_provenance_refs_exist(self):
        for fixture in self.fixtures:
            source_ids = fixture.record_ids()
            for fact in derived_facts(fixture):
                self.assertTrue(fact.provenance_refs)
                self.assertTrue(set(fact.provenance_refs).issubset(source_ids))


if __name__ == "__main__":
    unittest.main()
