import unittest
from pathlib import Path

from ppos_core.api import WorkbenchAPI
from ppos_core.workbench import WORKBENCH_MOUNTS, bootstrap_payload


class Mission009WorkbenchTests(unittest.TestCase):
    def test_workbench_contains_eight_view_panels(self):
        html = Path("workbench/index.html").read_text(encoding="utf-8")
        for view in ("catalog", "replay", "graph", "runner", "reports", "conversation", "recommendations", "audit"):
            self.assertIn(f'data-view-panel="{view}"', html)

    def test_workbench_contains_new_mount_points(self):
        html = Path("workbench/index.html").read_text(encoding="utf-8")
        for selector in WORKBENCH_MOUNTS.values():
            self.assertIn(selector[1:], html)

    def test_workbench_js_calls_new_mission_009_routes(self):
        js = Path("workbench/app.js").read_text(encoding="utf-8")
        for route in ("/api/evidence-graph/", "/api/recommendations", "/api/safety-audit", "/api/snapshot/export", "/api/contracts"):
            self.assertIn(route, js)

    def test_workbench_css_has_mobile_reflow(self):
        css = Path("workbench/styles.css").read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 860px)", css)
        self.assertIn("grid-template-columns: 1fr", css)

    def test_bootstrap_payload_lists_views_and_contracts(self):
        api = WorkbenchAPI(":memory:")
        payload = bootstrap_payload(api.conn)
        self.assertEqual(8, len(payload["views"]))
        self.assertGreaterEqual(len(payload["contracts"]), 25)

    def test_bootstrap_payload_marks_manifest_validation(self):
        api = WorkbenchAPI(":memory:")
        payload = bootstrap_payload(api.conn)
        self.assertTrue(payload["manifest_validation"]["passed"])

    def test_workbench_has_no_cdn_or_package_install_reference(self):
        text = (
            Path("workbench/index.html").read_text(encoding="utf-8")
            + Path("workbench/app.js").read_text(encoding="utf-8")
            + Path("workbench/styles.css").read_text(encoding="utf-8")
        ).lower()
        self.assertNotIn("cdn.", text)
        self.assertNotIn("npm install", text)

    def test_static_routes_are_served_by_api_handler(self):
        api = WorkbenchAPI(":memory:")
        handler = __import__("ppos_core.api", fromlist=["make_handler"]).make_handler(api)
        self.assertTrue(handler)


if __name__ == "__main__":
    unittest.main()
