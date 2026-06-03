#!/usr/bin/env python3
"""No-package local workbench smoke for Mission 009.

This is a stdlib fallback. It verifies localhost serving, static workbench
content, API calls, and workflow interaction contracts. Browser plugin smoke,
when available, provides stronger visual/console evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from http.server import HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ppos_core.api import WorkbenchAPI, make_handler


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mission 009 local workbench smoke.")
    parser.add_argument("--db", default="/tmp/ppos_mission_009_browser.sqlite")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Mission 009 smoke may bind only to localhost.")

    api = WorkbenchAPI(args.db)
    server = HTTPServer((args.host, args.port), make_handler(api))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://{args.host}:{server.server_address[1]}"
    try:
        time.sleep(0.1)
        checks = []
        html = _get_text(f"{base}/")
        _check("Personal Performance OS" in html, "page_identity", checks)
        _check("data-view-panel=\"catalog\"" in html, "catalog_panel_mount", checks)
        _check("data-view-panel=\"audit\"" in html, "audit_panel_mount", checks)
        css = _get_text(f"{base}/workbench/styles.css")
        _check("@media (max-width: 860px)" in css, "responsive_css", checks)
        js = _get_text(f"{base}/workbench/app.js")
        _check("/api/workflows/run" in js, "workflow_runner_api_call", checks)
        health = _get_json(f"{base}/api/health")
        _check(health["synthetic_only"] is True and health["local_only"] is True, "health_local_synthetic", checks)
        boot = _get_json(f"{base}/api/workbench/bootstrap")
        _check(len(boot["fixtures"]) == 36, "bootstrap_fixture_count", checks)
        imported = _post_json(f"{base}/api/import-fixture", {"fixture_id": "dtu_training_ramp_too_fast"})
        _check(imported["import"]["fixture_id"] == "dtu_training_ramp_too_fast", "fixture_selection_import", checks)
        run = _post_json(
            f"{base}/api/workflows/run",
            {"fixture_id": "dtu_training_ramp_too_fast", "workflow": "ride_rest_recommendation"},
        )
        _check(run["workflow_run"]["recommendation_class"] == "ramp_caution", "workflow_runner_state", checks)
        timeline = _get_json(f"{base}/api/workflows/{run['workflow_run']['id']}/timeline")
        _check(len(timeline["timeline"]["steps"]) == 5, "timeline_panel_data", checks)
        graph = _get_json(f"{base}/api/evidence-graph/dtu_training_ramp_too_fast")
        _check(bool(graph["graph"]["nodes"]), "graph_panel_data", checks)
        missing = _get_json(f"{base}/api/not-a-route", expected_status=404)
        _check(missing["status"] == 404 and "type" in missing, "error_contract_shape", checks)
        print("Mission 009 local workbench smoke PASS")
        print(f"url={base} checks={len(checks)} fallback=stdlib_no_visual_browser")
        return 0
    finally:
        server.shutdown()
        server.server_close()


def _get_text(url: str) -> str:
    with urlopen(url, timeout=5) as response:
        return response.read().decode("utf-8")


def _get_json(url: str, expected_status: int = 200) -> dict:
    try:
        with urlopen(url, timeout=5) as response:
            assert response.status == expected_status
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code != expected_status:
            raise
        return json.loads(exc.read().decode("utf-8"))


def _post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def _check(condition, label: str, checks: list[str]) -> None:
    assert condition, label
    checks.append(label)


if __name__ == "__main__":
    raise SystemExit(main())
