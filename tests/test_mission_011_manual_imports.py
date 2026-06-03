from __future__ import annotations

import sqlite3
import unittest
from pathlib import Path

from ppos_core.manual_imports import (
    adapter_catalog,
    manual_export_catalog,
    preview_manual_export,
    validate_manual_export_manifest,
)
from ppos_core.storage import (
    connect,
    get_manual_import_conflicts,
    get_manual_import_mapping,
    manual_import_audit_summary,
    migrate,
    preview_manual_import,
)


class Mission011ManualImportTests(unittest.TestCase):
    def test_manifest_and_files_are_consistent(self) -> None:
        validation = validate_manual_export_manifest()
        self.assertTrue(validation["valid"], validation["errors"])
        self.assertEqual(9, validation["export_count"])
        self.assertEqual(5, validation["adapter_count"])
        for export in manual_export_catalog():
            self.assertTrue(export["exists"], export)
            self.assertEqual(64, len(export["sha256"]))

    def test_preview_contracts_match_manifest_expectations(self) -> None:
        for export in manual_export_catalog():
            with self.subTest(export_id=export["export_id"]):
                preview = preview_manual_export(export["export_id"])
                expected = export["expected"]
                self.assertTrue(preview["synthetic_only"])
                self.assertEqual(expected["preview_rows"], preview["summary"]["row_count"])
                self.assertEqual(expected["validation_errors"], preview["summary"]["error_count"])
                self.assertEqual(expected["validation_warnings"], preview["summary"]["warning_count"])
                self.assertEqual(expected["duplicates"], sum(1 for conflict in preview["conflicts"] if conflict["conflict_type"] == "duplicate_candidate"))
                self.assertGreater(len(preview["mappings"]), 0)

    def test_validation_detects_missing_time_duplicate_timezone_and_unit_conflict(self) -> None:
        missing_time = preview_manual_export("manual_malformed_missing_time_csv")
        self.assertFalse(missing_time["summary"]["can_commit"])
        self.assertIn("missing_observed_at", {issue["issue_type"] for issue in missing_time["issues"]})

        duplicate = preview_manual_export("manual_activity_csv_duplicate")
        self.assertTrue(duplicate["summary"]["can_commit"])
        self.assertIn("duplicate_candidate", {conflict["conflict_type"] for conflict in duplicate["conflicts"]})

        timezone = preview_manual_export("manual_timezone_boundary_csv")
        self.assertIn("timezone_boundary", {issue["issue_type"] for issue in timezone["issues"]})

        unit_conflict = preview_manual_export("manual_unit_conflict_csv")
        self.assertIn("unit_conflict", {conflict["conflict_type"] for conflict in unit_conflict["conflicts"]})

    def test_preview_persistence_and_commit(self) -> None:
        conn = connect(":memory:")
        migrate(conn)
        preview = preview_manual_import(conn, "manual_activity_csv_duplicate")
        self.assertEqual("previewed", preview["status"])
        self.assertEqual(4, preview["row_count"])
        self.assertEqual(1, preview["conflict_count"])

        mapping = get_manual_import_mapping(conn, preview["id"])
        conflicts = get_manual_import_conflicts(conn, preview["id"])
        self.assertEqual(preview["id"], mapping["session_id"])
        self.assertEqual(1, len(conflicts["conflicts"]))

        committed = preview_manual_import(conn, "manual_activity_csv_duplicate", commit=True)
        self.assertEqual("committed", committed["status"])
        audit = manual_import_audit_summary(conn)
        self.assertEqual(1, audit["session_count"])
        self.assertEqual(1, audit["committed_session_count"])

    def test_commit_blocks_error_preview(self) -> None:
        conn = connect(":memory:")
        migrate(conn)
        with self.assertRaises(ValueError):
            preview_manual_import(conn, "manual_malformed_missing_time_csv", commit=True)


if __name__ == "__main__":
    unittest.main()
