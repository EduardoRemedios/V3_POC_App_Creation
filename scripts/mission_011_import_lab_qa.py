"""Mission 011 local import-lab QA harness."""

from __future__ import annotations

import argparse
import json
import sys
import threading
from datetime import datetime, timezone
from http.client import HTTPConnection
from http.server import HTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ppos_core.api import WorkbenchAPI, make_handler
from ppos_core.manual_imports import validate_manual_export_manifest


AUDIT_PATH = Path(".factory-v3/evidence/MISSION_011_AUDIT_SUMMARY.json")
REQUIRED_TEST_IDS = [
    "nav-imports",
    "view-imports",
    "source-adapter-lab",
    "adapter-catalog",
    "manual-export-selector",
    "preview-manual-import",
    "commit-manual-import",
    "manual-import-preview",
    "manual-import-mapping",
    "manual-import-conflicts",
    "manual-import-audit",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Mission 011 source-adapter lab QA.")
    parser.add_argument("--db", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8780)
    args = parser.parse_args(argv)
    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Mission 011 QA may bind only to localhost.")

    api = WorkbenchAPI(args.db)
    server = HTTPServer((args.host, args.port), make_handler(api))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://{args.host}:{args.port}"
    command = f"python3 -B scripts/mission_011_import_lab_qa.py --db {args.db} --host {args.host} --port {args.port}"
    prior_browser_qa = load_prior_browser_qa()
    try:
        html = http_get_text(base, "/workbench/?view=imports")
        js = http_get_text(base, "/workbench/app.js")
        css = http_get_text(base, "/workbench/styles.css")
        api_checks = run_api_checks(base)
        audit = {
            "mission_id": "MISSION_011_SYNTHETIC_MANUAL_IMPORT_SOURCE_ADAPTER_READINESS",
            "status": "running",
            "generated_at": now_utc(),
            "synthetic_only": True,
            "local_only": True,
            "no_package_install": True,
            "manual_export_fixture_count": api_checks["manual_export_count"],
            "adapter_count": api_checks["adapter_count"],
            "commands_run": [command],
            "manifest_validation": validate_manual_export_manifest(),
            "api_checks": api_checks,
            "workbench_checks": check_workbench_contracts(html, js, css),
            "browser_qa": prior_browser_qa,
            "residual_risks": [],
        }
        failures = collect_failures(audit)
        audit["status"] = "pass" if not failures else "fail"
        audit["residual_risks"] = failures
        AUDIT_PATH.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if failures:
            raise SystemExit("Mission 011 QA failed: " + "; ".join(failures))
        return 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def check_workbench_contracts(html: str, js: str, css: str) -> dict[str, Any]:
    return {
        "required_test_ids": {test_id: f'data-testid="{test_id}"' in html for test_id in REQUIRED_TEST_IDS},
        "api_calls": {
            "source_adapters": "/api/source-adapters" in js,
            "manual_exports": "/api/manual-exports" in js,
            "preview": "/api/manual-imports/preview" in js,
            "commit": "/api/manual-imports/commit-synthetic" in js,
            "audit": "/api/manual-imports/audit-summary" in js,
        },
        "view_param": 'new URLSearchParams(window.location.search).get("view")' in js,
        "manual_export_param": 'new URLSearchParams(window.location.search).get("manual_export")' in js,
        "warning_style": ".warning" in css,
    }


def run_api_checks(base: str) -> dict[str, Any]:
    adapters = http_json(base, "GET", "/api/source-adapters")["adapters"]
    exports = http_json(base, "GET", "/api/manual-exports")["exports"]
    duplicate = http_json(base, "POST", "/api/manual-imports/preview", {"export_id": "manual_activity_csv_duplicate"})
    duplicate_session = duplicate["session"]
    session_id = duplicate_session["id"]
    mapping = http_json(base, "GET", f"/api/manual-imports/{session_id}/mapping")
    conflicts = http_json(base, "GET", f"/api/manual-imports/{session_id}/conflicts")
    committed = http_json(base, "POST", "/api/manual-imports/commit-synthetic", {"export_id": "manual_unit_conflict_csv"})
    error_preview = http_json(
        base, "POST", "/api/manual-imports/commit-synthetic", {"export_id": "manual_malformed_missing_time_csv"}
    )
    audit = http_json(base, "GET", "/api/manual-imports/audit-summary")["manual_import_audit"]
    return {
        "adapter_count": len(adapters),
        "manual_export_count": len(exports),
        "duplicate_preview_status": duplicate_session["status"],
        "duplicate_preview_rows": duplicate_session["row_count"],
        "duplicate_conflicts": len(conflicts["conflicts"]),
        "mapping_rows": len(mapping["mappings"]),
        "unit_conflict_commit_status": committed["session"]["status"],
        "unit_conflict_count": committed["session"]["conflict_count"],
        "error_commit_status": error_preview.get("status"),
        "error_commit_detail_contains_validation": "validation errors" in error_preview.get("detail", ""),
        "audit_session_count": audit["session_count"],
        "audit_conflict_count": audit["conflict_count"],
        "audit_synthetic_only": audit["synthetic_only"],
    }


def collect_failures(audit: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    manifest = audit["manifest_validation"]
    if not manifest["valid"]:
        failures.extend(manifest["errors"])
    workbench = audit["workbench_checks"]
    missing = [key for key, value in workbench["required_test_ids"].items() if not value]
    if missing:
        failures.append("missing import lab test ids: " + ", ".join(missing))
    for key, value in workbench["api_calls"].items():
        if not value:
            failures.append(f"missing workbench API call: {key}")
    if not workbench["view_param"]:
        failures.append("workbench view query parameter missing")
    if not workbench["manual_export_param"]:
        failures.append("workbench manual_export query parameter missing")
    if not workbench["warning_style"]:
        failures.append("warning style missing")
    api = audit["api_checks"]
    expectations = {
        "adapter_count": api["adapter_count"] >= 5,
        "manual_export_count": api["manual_export_count"] == 9,
        "duplicate_preview_rows": api["duplicate_preview_rows"] == 4,
        "duplicate_conflicts": api["duplicate_conflicts"] == 1,
        "mapping_rows": api["mapping_rows"] > 0,
        "unit_conflict_commit_status": api["unit_conflict_commit_status"] == "committed",
        "unit_conflict_count": api["unit_conflict_count"] >= 1,
        "error_commit_status": api["error_commit_status"] == 400,
        "error_commit_detail_contains_validation": api["error_commit_detail_contains_validation"],
        "audit_session_count": api["audit_session_count"] >= 2,
        "audit_synthetic_only": api["audit_synthetic_only"] is True,
    }
    for key, passed in expectations.items():
        if not passed:
            failures.append(f"api check failed: {key}")
    return failures


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
        if response.status == 400:
            payload["status"] = 400
        elif response.status != 200:
            raise RuntimeError(f"{method} {path} returned {response.status}: {payload}")
        return payload
    finally:
        conn.close()


def connection(base: str) -> HTTPConnection:
    host, port = base.removeprefix("http://").split(":")
    return HTTPConnection(host, int(port), timeout=5)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_prior_browser_qa() -> dict[str, Any]:
    if AUDIT_PATH.exists():
        try:
            prior = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
            browser_qa = prior.get("browser_qa", {})
            if browser_qa.get("status") == "pass":
                return browser_qa
        except json.JSONDecodeError:
            pass
    return {"status": "not_run", "notes": ["Browser QA is recorded separately in MISSION_011_BROWSER_NOTES.md."]}


if __name__ == "__main__":
    raise SystemExit(main())
