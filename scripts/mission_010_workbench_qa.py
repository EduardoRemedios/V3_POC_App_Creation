"""Mission 010 local workbench QA harness.

Uses Python stdlib only. The harness starts the local API in-process, exercises
the static workbench and UI-facing API scenario, and writes the authorized
Mission 010 UI QA audit summary.
"""

from __future__ import annotations

import argparse
import json
import threading
import time
from datetime import datetime, timezone
from http.client import HTTPConnection
from http.server import HTTPServer
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ppos_core.api import WorkbenchAPI, make_handler


AUDIT_PATH = Path(".factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json")
REQUIRED_TEST_IDS = [
    "workbench-title",
    "operator-toolbar",
    "operator-state",
    "fixture-selector",
    "import-fixture",
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
    "replay-timeline",
    "evidence-graph",
    "audit-summary",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Mission 010 local UI/API QA.")
    parser.add_argument("--db", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8770)
    args = parser.parse_args(argv)
    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Mission 010 QA may bind only to localhost.")

    api = WorkbenchAPI(args.db)
    server = HTTPServer((args.host, args.port), make_handler(api))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://{args.host}:{args.port}"
    commands = [
        f"python3 -B scripts/mission_010_workbench_qa.py --db {args.db} --host {args.host} --port {args.port}"
    ]

    prior_browser_qa = load_prior_browser_qa()
    audit: dict[str, Any] = {
        "mission_id": "MISSION_010_SYNTHETIC_WORKBENCH_QA_AND_OPERATOR_READINESS",
        "status": "running",
        "generated_at": now_utc(),
        "synthetic_only": True,
        "local_only": True,
        "no_package_install": True,
        "commands_run": commands,
        "static_contracts": {},
        "api_scenario": {},
        "browser_qa": prior_browser_qa,
        "residual_risks": [],
    }

    try:
        html = http_get_text(base, "/workbench/")
        css = http_get_text(base, "/workbench/styles.css")
        js = http_get_text(base, "/workbench/app.js")
        audit["static_contracts"] = check_static_contracts(html, css, js)
        audit["api_scenario"] = run_api_scenario(base)
        failed = collect_failures(audit)
        audit["status"] = "pass" if not failed else "fail"
        audit["residual_risks"] = failed
        AUDIT_PATH.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if failed:
            raise SystemExit("Mission 010 QA failed: " + "; ".join(failed))
        return 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def check_static_contracts(html: str, css: str, js: str) -> dict[str, Any]:
    test_id_results = {test_id: f'data-testid="{test_id}"' in html for test_id in REQUIRED_TEST_IDS}
    return {
        "html_served": "<title>Personal Performance OS Synthetic Workbench</title>" in html,
        "css_served": "@media (max-width: 860px)" in css and "#view-runner.is-active" in css,
        "js_served": "runScenarioWalkthrough" in js and "localStorage" in js,
        "required_test_ids": test_id_results,
        "loading_state": 'body.dataset.loading = isBusy ? "true" : "false"' in js,
        "api_error_handling": "if (!response.ok)" in js and "setError(error)" in js,
        "fixture_persistence": "ppos.workbench.selectedFixtureId" in js,
        "url_fixture_selection": "URLSearchParams(window.location.search).get(\"fixture\")" in js,
        "reset_control": "resetWorkbench" in js,
        "scenario_walkthrough": "Scenario Walkthrough" in html and "runScenarioWalkthrough" in js,
        "responsive_contract": ".toolbar > select" in css and "#view-runner.is-active" in css,
    }


def run_api_scenario(base: str) -> dict[str, Any]:
    health = http_json(base, "GET", "/api/health")
    bootstrap = http_json(base, "GET", "/api/workbench/bootstrap")
    fixtures = bootstrap["fixtures"]
    fixture_id = "dtu_training_ramp_too_fast"
    if not any(item["fixture_id"] == fixture_id for item in fixtures):
        fixture_id = fixtures[0]["fixture_id"]
    fixture = http_json(base, "GET", f"/api/fixtures/{fixture_id}")
    import_result = http_json(base, "POST", "/api/import-fixture", {"fixture_id": fixture_id})
    workflow = first_expected_workflow(fixture)
    run = http_json(base, "POST", "/api/workflows/run", {"fixture_id": fixture_id, "workflow": workflow})
    run_id = run["workflow_run"]["id"]
    timeline = http_json(base, "GET", f"/api/workflows/{run_id}/timeline")
    graph = http_json(base, "GET", f"/api/evidence-graph/{fixture_id}")
    recommendations = http_json(base, "GET", "/api/recommendations")
    safety = http_json(base, "GET", "/api/safety-audit")
    snapshot = http_json(base, "GET", "/api/snapshot/export")
    missing_workflow = http_json(base, "POST", "/api/workflows/run", {"fixture_id": fixture_id, "workflow": "not_a_workflow"})
    return {
        "health_ok": health.get("status") == "ok" and health.get("synthetic_only") is True,
        "fixture_count": len(fixtures),
        "selected_fixture": fixture_id,
        "workflow": workflow,
        "import_count": import_result["import"]["import_count"],
        "run_id": run_id,
        "workflow_status": run["workflow_run"]["status"],
        "timeline_step_count": len(timeline["timeline"]["steps"]),
        "graph_node_count": len(graph["graph"]["nodes"]),
        "graph_edge_count": len(graph["graph"]["edges"]),
        "recommendation_count": len(recommendations["recommendations"]),
        "safety_event_count": safety["safety_audit"]["event_count"],
        "snapshot_synthetic_only": snapshot["snapshot"]["synthetic_only"],
        "error_contract_status": missing_workflow.get("status") == 400,
        "error_contract_field": missing_workflow.get("field") == "workflow",
    }


def collect_failures(audit: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    static = audit["static_contracts"]
    if not static["html_served"]:
        failures.append("workbench HTML did not serve expected title")
    if not static["css_served"]:
        failures.append("workbench CSS did not serve responsive contract")
    if not static["js_served"]:
        failures.append("workbench JS did not serve scenario/persistence code")
    missing_test_ids = [key for key, value in static["required_test_ids"].items() if not value]
    if missing_test_ids:
        failures.append("missing data-testid markers: " + ", ".join(missing_test_ids))
    for key in [
        "loading_state",
        "api_error_handling",
        "fixture_persistence",
        "url_fixture_selection",
        "reset_control",
        "scenario_walkthrough",
    ]:
        if not static[key]:
            failures.append(f"static contract failed: {key}")

    scenario = audit["api_scenario"]
    scenario_checks = {
        "health_ok": scenario["health_ok"],
        "fixture_count": scenario["fixture_count"] >= 35,
        "workflow_status": scenario["workflow_status"] in {"candidate", "completed"},
        "timeline_step_count": scenario["timeline_step_count"] >= 3,
        "graph_node_count": scenario["graph_node_count"] > 0,
        "graph_edge_count": scenario["graph_edge_count"] > 0,
        "snapshot_synthetic_only": scenario["snapshot_synthetic_only"] is True,
        "error_contract_status": scenario["error_contract_status"],
        "error_contract_field": scenario["error_contract_field"],
    }
    for key, passed in scenario_checks.items():
        if not passed:
            failures.append(f"api scenario failed: {key}")
    return failures


def first_expected_workflow(fixture: dict[str, Any]) -> str:
    workflows = fixture.get("expected", {}).get("workflows", {})
    if not workflows:
        return "recovery_today"
    return next(iter(workflows))


def load_prior_browser_qa() -> dict[str, Any]:
    if AUDIT_PATH.exists():
        try:
            prior = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
            browser_qa = prior.get("browser_qa", {})
            if browser_qa.get("status") == "pass":
                return browser_qa
        except json.JSONDecodeError:
            pass
    return {
        "status": "not_run_by_stdlib_harness",
        "notes": ["Browser QA is recorded separately in MISSION_010_BROWSER_NOTES.md."],
    }


def http_get_text(base: str, path: str) -> str:
    conn = connection(base)
    try:
        conn.request("GET", path)
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        if response.status != 200:
            raise RuntimeError(f"GET {path} returned {response.status}: {body}")
        return body
    finally:
        conn.close()


def http_json(base: str, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    conn = connection(base)
    try:
        raw = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Content-Type": "application/json"} if raw else {}
        conn.request(method, path, body=raw, headers=headers)
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        if response.status not in {200, 400}:
            raise RuntimeError(f"{method} {path} returned {response.status}: {payload}")
        if response.status == 400:
            payload["status"] = 400
        return payload
    finally:
        conn.close()


def connection(base: str) -> HTTPConnection:
    host_port = base.removeprefix("http://")
    host, port = host_port.split(":")
    for _ in range(20):
        try:
            return HTTPConnection(host, int(port), timeout=5)
        except OSError:
            time.sleep(0.05)
    return HTTPConnection(host, int(port), timeout=5)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
