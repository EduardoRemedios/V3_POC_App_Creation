from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import mission_010_workbench_qa


ROOT = Path(__file__).resolve().parents[1]


class Mission010WorkbenchContractTests(unittest.TestCase):
    def test_workbench_has_operator_ready_test_ids(self) -> None:
        html = (ROOT / "workbench/index.html").read_text(encoding="utf-8")
        required = [
            "workbench-title",
            "operator-toolbar",
            "operator-state",
            "fixture-selector",
            "run-scenario",
            "reset-workbench",
            "view-catalog",
            "view-replay",
            "view-graph",
            "view-runner",
            "view-reports",
            "view-conversation",
            "view-recommendations",
            "view-audit",
            "scenario-runner",
            "scenario-output",
        ]
        for test_id in required:
            with self.subTest(test_id=test_id):
                self.assertIn(f'data-testid="{test_id}"', html)

    def test_workbench_js_has_state_error_and_scenario_controls(self) -> None:
        js = (ROOT / "workbench/app.js").read_text(encoding="utf-8")
        for marker in [
            "ppos.workbench.selectedFixtureId",
            "URLSearchParams(window.location.search).get(\"fixture\")",
            "runScenarioWalkthrough",
            "resetWorkbench",
            "if (!response.ok)",
            "setError(error)",
            "body.dataset.loading",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, js)

    def test_workbench_css_has_responsive_operator_contract(self) -> None:
        css = (ROOT / "workbench/styles.css").read_text(encoding="utf-8")
        for marker in [
            "@media (max-width: 860px)",
            "#view-runner.is-active",
            ".toolbar > select",
            ".scenario-step.pass",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, css)

    def test_static_contract_checker_reports_required_surfaces(self) -> None:
        html = (ROOT / "workbench/index.html").read_text(encoding="utf-8")
        css = (ROOT / "workbench/styles.css").read_text(encoding="utf-8")
        js = (ROOT / "workbench/app.js").read_text(encoding="utf-8")
        result = mission_010_workbench_qa.check_static_contracts(html, css, js)
        self.assertTrue(result["html_served"])
        self.assertTrue(result["css_served"])
        self.assertTrue(result["js_served"])
        self.assertTrue(result["loading_state"])
        self.assertTrue(result["api_error_handling"])
        self.assertTrue(result["fixture_persistence"])
        self.assertTrue(result["url_fixture_selection"])
        self.assertTrue(result["reset_control"])
        self.assertTrue(result["scenario_walkthrough"])
        self.assertFalse([key for key, value in result["required_test_ids"].items() if not value])

    def test_harness_writes_audit_summary(self) -> None:
        audit_path = ROOT / ".factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json"
        prior_audit = audit_path.read_text(encoding="utf-8") if audit_path.exists() else None
        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp) / "mission_010.sqlite")
            try:
                mission_010_workbench_qa.main(["--db", db_path, "--host", "127.0.0.1", "--port", "8771"])
                audit = json.loads(audit_path.read_text(encoding="utf-8"))
                self.assertEqual("pass", audit["status"])
                self.assertTrue(audit["synthetic_only"])
                self.assertTrue(audit["local_only"])
                self.assertTrue(audit["no_package_install"])
                self.assertGreaterEqual(audit["api_scenario"]["fixture_count"], 35)
                self.assertGreaterEqual(audit["api_scenario"]["timeline_step_count"], 3)
            finally:
                if prior_audit is not None:
                    audit_path.write_text(prior_audit, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
