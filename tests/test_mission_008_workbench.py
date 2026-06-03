import unittest
from pathlib import Path

from ppos_core.api import WorkbenchAPI
from ppos_core.workbench import WORKBENCH_MOUNTS, bootstrap_payload


class Mission008WorkbenchTests(unittest.TestCase):
    def test_static_files_exist(self):
        for path in ("workbench/index.html", "workbench/styles.css", "workbench/app.js"):
            self.assertTrue(Path(path).exists(), path)

    def test_index_contains_required_mount_points(self):
        html = Path("workbench/index.html").read_text(encoding="utf-8")
        for selector in WORKBENCH_MOUNTS.values():
            self.assertIn(selector[1:], html)

    def test_app_js_contains_required_api_calls(self):
        js = Path("workbench/app.js").read_text(encoding="utf-8")
        for route in (
            "/api/workbench/bootstrap",
            "/api/fixtures/",
            "/api/import-fixture",
            "/api/workflows/run",
            "/api/report-candidates",
        ):
            self.assertIn(route, js)

    def test_bootstrap_payload_marks_local_synthetic_compliance(self):
        api = WorkbenchAPI(":memory:")
        payload = bootstrap_payload(api.conn)
        self.assertTrue(payload["synthetic_only"])
        self.assertTrue(payload["local_only"])
        self.assertEqual([], payload["packages_installed"])
        self.assertEqual([], payload["live_integrations"])

    def test_bootstrap_payload_lists_required_fixtures(self):
        api = WorkbenchAPI(":memory:")
        payload = bootstrap_payload(api.conn)
        self.assertGreaterEqual(len(payload["fixtures"]), 22)

    def test_styles_include_responsive_layout(self):
        css = Path("workbench/styles.css").read_text(encoding="utf-8")
        self.assertIn("@media", css)
        self.assertIn("grid-template-columns", css)

    def test_workbench_has_no_package_bootstrap(self):
        html = Path("workbench/index.html").read_text(encoding="utf-8").lower()
        js = Path("workbench/app.js").read_text(encoding="utf-8").lower()
        self.assertNotIn("npm", html + js)
        self.assertNotIn("cdn.jsdelivr", html + js)


if __name__ == "__main__":
    unittest.main()
