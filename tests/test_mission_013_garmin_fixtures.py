from __future__ import annotations

import unittest

from ppos_core.garmin_bridge import (
    garmin_export_catalog,
    preview_garmin_export,
    validate_garmin_export_manifest,
)


class Mission013GarminFixtureTests(unittest.TestCase):
    def test_garmin_manifest_and_files_are_synthetic_and_consistent(self) -> None:
        validation = validate_garmin_export_manifest()
        self.assertTrue(validation["valid"], validation["errors"])
        self.assertEqual(7, validation["export_count"])
        self.assertEqual(4, validation["adapter_count"])
        self.assertEqual("keep-raw-until-verified", validation["default_retention_posture"])

        catalog = garmin_export_catalog()
        families = {entry["family"] for entry in catalog}
        self.assertEqual({"activities", "sleep", "body_composition", "wellness_hrv_stress"}, families)
        for export in catalog:
            self.assertTrue(export["exists"], export)
            self.assertEqual("SYNTHETIC_MISSION_013_GARMIN_SHAPE", export["synthetic_label"])
            self.assertEqual(64, len(export["sha256"]))

    def test_garmin_preview_contracts_match_manifest_expectations(self) -> None:
        for export in garmin_export_catalog():
            with self.subTest(export_id=export["export_id"]):
                preview = preview_garmin_export(export["export_id"])
                expected = export["expected"]
                self.assertTrue(preview["synthetic_only"])
                self.assertEqual(expected["preview_rows"], preview["summary"]["row_count"])
                self.assertEqual(expected["validation_errors"], preview["summary"]["error_count"])
                self.assertEqual(expected["validation_warnings"], preview["summary"]["warning_count"])
                self.assertEqual(
                    expected["duplicates"],
                    sum(1 for conflict in preview["conflicts"] if conflict["conflict_type"] == "duplicate_candidate"),
                )
                self.assertGreater(len(preview["mappings"]), 0)

    def test_garmin_edge_cases_are_detected(self) -> None:
        activity_edge = preview_garmin_export("garmin_activities_edge_csv")
        self.assertFalse(activity_edge["summary"]["can_commit"])
        self.assertIn("missing_observed_at", {issue["issue_type"] for issue in activity_edge["issues"]})
        self.assertIn("malformed_numeric", {issue["issue_type"] for issue in activity_edge["issues"]})
        self.assertIn("duplicate_candidate", {conflict["conflict_type"] for conflict in activity_edge["conflicts"]})

        sleep_edge = preview_garmin_export("garmin_sleep_edge_json")
        self.assertFalse(sleep_edge["summary"]["can_commit"])
        self.assertIn("timezone_boundary", {issue["issue_type"] for issue in sleep_edge["issues"]})

        body_edge = preview_garmin_export("garmin_body_composition_edge_csv")
        self.assertFalse(body_edge["summary"]["can_commit"])
        self.assertIn("unit_conflict", {conflict["conflict_type"] for conflict in body_edge["conflicts"]})

        wellness = preview_garmin_export("garmin_wellness_hrv_stress_json")
        self.assertFalse(wellness["summary"]["can_commit"])
        self.assertIn("malformed_numeric", {issue["issue_type"] for issue in wellness["issues"]})


if __name__ == "__main__":
    unittest.main()

