import unittest
from pathlib import Path

from ppos_core.fixture_manifest import (
    api_matrix,
    family_summary,
    fixture_file_ids,
    load_manifest,
    manifest_fixture_ids,
    validate_manifest,
    workflow_matrix,
)
from ppos_core.loader import load_fixtures


class Mission009ManifestTests(unittest.TestCase):
    def test_manifest_parses_and_is_synthetic_only(self):
        manifest = load_manifest()
        self.assertTrue(manifest["synthetic_only"])
        self.assertEqual("dtu_manifest_mission_009", manifest["manifest_id"])

    def test_fixture_count_is_inside_mission_range(self):
        validation = validate_manifest()
        self.assertGreaterEqual(validation["fixture_count"], 35)
        self.assertLessEqual(validation["fixture_count"], 45)
        self.assertEqual(36, validation["fixture_count"])

    def test_manifest_matches_fixture_files(self):
        self.assertEqual(fixture_file_ids(), manifest_fixture_ids())
        self.assertTrue(validate_manifest()["passed"])

    def test_all_fixture_files_parse_through_loader(self):
        fixtures = load_fixtures()
        self.assertEqual(36, len(fixtures))
        self.assertTrue(all(fixture.synthetic_only for fixture in fixtures))

    def test_family_summary_covers_required_families(self):
        families = {row["family_id"]: row for row in family_summary()}
        for required in ("sleep_and_recovery", "nutrition_ambiguity", "api_replay_edge_cases", "safety_audit"):
            self.assertIn(required, families)
            self.assertGreater(families[required]["fixture_count"], 0)

    def test_workflow_matrix_includes_new_edge_workflows(self):
        matrix = {(row["fixture_id"], row["workflow"]) for row in workflow_matrix()}
        self.assertIn(("dtu_training_ramp_too_fast", "ride_rest_recommendation"), matrix)
        self.assertIn(("dtu_snapshot_export_roundtrip", "recovery_today"), matrix)

    def test_api_matrix_includes_snapshot_and_error_cases(self):
        cases = {row["api_case"] for row in api_matrix()}
        self.assertIn("GET /api/snapshot/export", cases)
        self.assertIn("POST /api/workflows/run:error_unknown_workflow", cases)

    def test_manifest_file_is_in_authorized_path(self):
        self.assertTrue(Path("fixtures/dtu_manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
