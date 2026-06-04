"""Mission 012 local review/rollback QA harness."""

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


AUDIT_PATH = Path(".factory-v3/evidence/MISSION_012_AUDIT_SUMMARY.json")
REQUIRED_TEST_IDS = [
    "view-imports",
    "source-adapter-lab",
    "manual-export-selector",
    "preview-manual-import",
    "commit-manual-import",
    "commit-reviewed-manual-import",
    "rollback-manual-import",
    "manual-import-preview",
    "manual-import-mapping",
    "manual-import-conflicts",
    "manual-import-audit",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Mission 012 review/rollback QA.")
    parser.add_argument("--db", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8790)
    args = parser.parse_args(argv)
    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Mission 012 QA may bind only to localhost.")

    api = WorkbenchAPI(args.db)
    server = HTTPServer((args.host, args.port), make_handler(api))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://{args.host}:{args.port}"
    command = f"python3 -B scripts/mission_012_review_rollback_qa.py --db {args.db} --host {args.host} --port {args.port}"
    try:
        html = http_get_text(base, "/workbench/?view=imports&manual_export=manual_activity_csv_clean")
        js = http_get_text(base, "/workbench/app.js")
        css = http_get_text(base, "/workbench/styles.css")
        api_checks = run_api_checks(base)
        audit = {
            "mission_id": "MISSION_012_SYNTHETIC_IMPORT_HARDENING_AND_REAL_DATA_BRIDGE_DECISION",
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
            "browser_qa": load_browser_qa(),
            "residual_risks": [],
        }
        failures = collect_failures(audit)
        audit["status"] = "pass" if not failures else "fail"
        audit["residual_risks"] = failures
        AUDIT_PATH.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if failures:
            raise SystemExit("Mission 012 QA failed: " + "; ".join(failures))
        return 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def run_api_checks(base: str) -> dict[str, Any]:
    adapters = http_json(base, "GET", "/api/source-adapters")["adapters"]
    exports = http_json(base, "GET", "/api/manual-exports")["exports"]
    preview = http_json(base, "POST", "/api/manual-imports/preview", {"export_id": "manual_activity_csv_clean"})
    session_id = preview["session"]["id"]
    reviewed = None
    for row_index in (1, 2, 3):
        reviewed = http_json(
            base,
            "POST",
            "/api/manual-imports/review-row",
            {"session_id": session_id, "row_index": row_index, "review_state": "accepted"},
        )
    committed = http_json(base, "POST", "/api/manual-imports/commit-reviewed", {"session_id": session_id})
    reverted = http_json(
        base,
        "POST",
        "/api/manual-imports/rollback",
        {"session_id": session_id, "reason": "synthetic QA rollback"},
    )
    audit = http_json(base, "GET", "/api/manual-imports/audit-summary")["manual_import_audit"]
    return {
        "adapter_count": len(adapters),
        "manual_export_count": len(exports),
        "preview_status": preview["session"]["status"],
        "preview_rows": preview["session"]["row_count"],
        "initial_review_summary": preview["session"]["review_summary"],
        "reviewed_summary": reviewed["session"]["review_summary"] if reviewed else {},
        "reviewed_commit_status": committed["session"]["status"],
        "rollback_status": reverted["session"]["status"],
        "rollback_reason": reverted["session"]["rollback_reason"],
        "audit_reverted_session_count": audit["reverted_session_count"],
        "audit_event_count": audit["audit_event_count"],
        "audit_synthetic_only": audit["synthetic_only"],
    }


def check_workbench_contracts(html: str, js: str, css: str) -> dict[str, Any]:
    return {
        "required_test_ids": {test_id: f'data-testid="{test_id}"' in html for test_id in REQUIRED_TEST_IDS},
        "api_calls": {
            "review": "/api/manual-imports/review-row" in js,
            "commit_reviewed": "/api/manual-imports/commit-reviewed" in js,
            "rollback": "/api/manual-imports/rollback" in js,
            "audit": "/api/manual-imports/audit-summary" in js,
        },
        "diff_rendering": "manual-import-raw-normalized-diff" in js and ".diff-grid" in css,
        "review_controls": "manual-import-review-actions" in js,
        "responsive_diff": ".diff-grid" in css and "@media" in css,
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
    for key in ("diff_rendering", "review_controls", "responsive_diff"):
        if not workbench[key]:
            failures.append(f"workbench check failed: {key}")
    api = audit["api_checks"]
    expectations = {
        "adapter_count": api["adapter_count"] >= 5,
        "manual_export_count": api["manual_export_count"] == 9,
        "preview_rows": api["preview_rows"] == 3,
        "initial_needs_clarification": api["initial_review_summary"]["needs_clarification"] == 3,
        "reviewed_all_accepted": api["reviewed_summary"]["accepted"] == 3,
        "reviewed_commit_status": api["reviewed_commit_status"] == "committed",
        "rollback_status": api["rollback_status"] == "reverted",
        "rollback_reason": api["rollback_reason"] == "synthetic QA rollback",
        "audit_reverted_session_count": api["audit_reverted_session_count"] == 1,
        "audit_event_count": api["audit_event_count"] >= 5,
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
        if response.status != 200:
            raise RuntimeError(f"{method} {path} returned {response.status}: {payload}")
        return payload
    finally:
        conn.close()


def connection(base: str) -> HTTPConnection:
    host, port = base.removeprefix("http://").split(":")
    return HTTPConnection(host, int(port), timeout=5)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_browser_qa() -> dict[str, Any]:
    path = Path(".factory-v3/evidence/MISSION_012_BROWSER_NOTES.md")
    if path.exists() and "Browser QA status: PASS" in path.read_text(encoding="utf-8"):
        return {"status": "pass", "notes_reference": str(path)}
    return {"status": "not_run", "notes": ["Browser QA is recorded separately in MISSION_012_BROWSER_NOTES.md."]}


if __name__ == "__main__":
    raise SystemExit(main())
