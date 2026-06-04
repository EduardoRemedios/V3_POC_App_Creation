from __future__ import annotations

import unittest

from ppos_core.storage import (
    connect,
    create_synthetic_import_approval,
    list_synthetic_import_approvals,
    manual_import_audit_summary,
    migrate,
)
from ppos_core.workbench import bootstrap_payload


class Mission013ApprovalUXTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        migrate(self.conn)

    def test_synthetic_approval_records_consent_source_label_and_retention(self) -> None:
        approval = create_synthetic_import_approval(
            self.conn,
            "garmin_sleep_clean_json",
            retention_posture="keep-raw-until-verified",
            consent_text="Synthetic Mission 013 approval rehearsal; no real file is read.",
        )

        self.assertTrue(approval["synthetic_only"])
        self.assertTrue(approval["preview_only"])
        self.assertEqual("real_garmin_manual_export", approval["source_label"])
        self.assertEqual("keep-raw-until-verified", approval["retention_posture"])
        self.assertEqual("approved", approval["approval_state"])
        self.assertIn("sleep", approval["data_categories"])
        self.assertFalse(approval["payload"]["real_data_enabled"])

        approvals = list_synthetic_import_approvals(self.conn)
        self.assertEqual(1, len(approvals))
        self.assertEqual(1, manual_import_audit_summary(self.conn)["approval_count"])

    def test_workbench_bootstrap_exposes_garmin_exports_and_approval_state(self) -> None:
        create_synthetic_import_approval(self.conn, "garmin_activities_clean_csv")

        payload = bootstrap_payload(self.conn)

        self.assertTrue(payload["synthetic_only"])
        self.assertIn("garmin_exports", payload)
        self.assertGreaterEqual(len(payload["garmin_exports"]), 7)
        self.assertEqual(1, len(payload["synthetic_import_approvals"]))
        self.assertIn("GET /api/garmin-exports", payload["api_routes"])
        self.assertIn("POST /api/manual-imports/approval", payload["api_routes"])


if __name__ == "__main__":
    unittest.main()
