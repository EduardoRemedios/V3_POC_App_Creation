from __future__ import annotations

import unittest
from pathlib import Path

from ppos_core.storage import connect, migrate
from ppos_core.workbench import bootstrap_payload


ROOT = Path(__file__).resolve().parents[1]


class Mission012WorkbenchTests(unittest.TestCase):
    def test_workbench_contains_review_rollback_controls_and_diff_mounts(self) -> None:
        html = (ROOT / "workbench/index.html").read_text(encoding="utf-8")
        for marker in [
            'data-testid="commit-reviewed-manual-import"',
            'data-testid="rollback-manual-import"',
            'data-testid="manual-import-preview"',
            'data-testid="manual-import-audit"',
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, html)

    def test_workbench_js_calls_review_rollback_api_and_renders_diff(self) -> None:
        js = (ROOT / "workbench/app.js").read_text(encoding="utf-8")
        for marker in [
            "/api/manual-imports/review-row",
            "/api/manual-imports/commit-reviewed",
            "/api/manual-imports/rollback",
            "manual-import-raw-normalized-diff",
            "manual-import-review-actions",
            "reviewSummaryText",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, js)

    def test_bootstrap_lists_review_rollback_routes(self) -> None:
        conn = connect(":memory:")
        migrate(conn)
        payload = bootstrap_payload(conn)
        routes = set(payload["api_routes"])
        self.assertIn("POST /api/manual-imports/review-row", routes)
        self.assertIn("POST /api/manual-imports/commit-reviewed", routes)
        self.assertIn("POST /api/manual-imports/rollback", routes)
        self.assertEqual("#manual-import-audit", payload["mounts"]["manual_import_audit"])


if __name__ == "__main__":
    unittest.main()
