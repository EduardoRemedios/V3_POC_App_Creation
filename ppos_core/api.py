"""Localhost-only stdlib HTTP API for the synthetic workbench."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .api_contracts import error_examples, problem_detail
from .loader import load_fixture
from .replay import replay_fixture
from .storage import (
    connect,
    fixture_manifest_payload,
    get_conversation_thread,
    get_evidence_pack,
    get_fixture_detail,
    get_workflow_run,
    get_workflow_timeline,
    import_fixture,
    import_audit_summary,
    list_api_contracts,
    list_derived_facts,
    list_evidence_graph,
    list_expected_api_cases,
    list_expected_workflows,
    list_fixture_families,
    list_fixture_files,
    list_followup_history,
    list_imports,
    list_manual_exports,
    list_manual_import_sessions,
    list_normalized_facts,
    list_persisted_report_settings,
    list_recommendation_history,
    list_report_candidates,
    list_safety_audit,
    list_source_adapters,
    list_snapshot_export,
    list_source_records,
    manual_import_audit_summary,
    migrate,
    get_manual_export_detail,
    get_manual_import_conflicts,
    get_manual_import_mapping,
    get_manual_import_session,
    preview_manual_import,
    run_and_persist_workflow,
    validate_snapshot_payload,
)
from .workbench import bootstrap_payload


class WorkbenchAPI:
    def __init__(self, db_path: str | Path = ":memory:"):
        self.conn = connect(db_path)
        migrate(self.conn)

    def handle(self, method: str, path: str, body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
        parsed = urlparse(path)
        parts = [part for part in parsed.path.strip("/").split("/") if part]
        try:
            if method == "GET" and parts == ["api", "health"]:
                return 200, {"status": "ok", "synthetic_only": True, "local_only": True}
            if method == "GET" and parts == ["api", "fixtures"]:
                return 200, {"fixtures": list_fixture_files()}
            if method == "GET" and parts == ["api", "fixture-manifest"]:
                return 200, fixture_manifest_payload()
            if method == "GET" and parts == ["api", "fixture-families"]:
                return 200, {"families": list_fixture_families()}
            if method == "GET" and parts == ["api", "fixtures", "expected-workflows"]:
                return 200, {"workflow_matrix": list_expected_workflows()}
            if method == "GET" and len(parts) == 3 and parts[:2] == ["api", "fixtures"]:
                detail = get_fixture_detail(parts[2])
                return 200, detail
            if method == "POST" and parts == ["api", "import-fixture"]:
                fixture_id = _required(body, "fixture_id")
                result = import_fixture(self.conn, Path("fixtures/dtu") / f"{fixture_id}.json")
                return 200, {"import": result}
            if method == "GET" and parts == ["api", "imports"]:
                return 200, {"imports": list_imports(self.conn)}
            if method == "GET" and parts == ["api", "imports", "audit-summary"]:
                return 200, import_audit_summary(self.conn)
            if method == "POST" and parts == ["api", "workflows", "run"]:
                fixture_id = _required(body, "fixture_id")
                workflow = _required(body, "workflow")
                import_fixture(self.conn, Path("fixtures/dtu") / f"{fixture_id}.json")
                return 200, {"workflow_run": run_and_persist_workflow(self.conn, fixture_id, workflow)}
            if method == "GET" and len(parts) == 3 and parts[:2] == ["api", "workflows"]:
                return 200, {"workflow_run": get_workflow_run(self.conn, parts[2])}
            if method == "GET" and len(parts) == 4 and parts[:2] == ["api", "workflows"] and parts[3] == "timeline":
                return 200, {"timeline": get_workflow_timeline(self.conn, parts[2])}
            if method == "GET" and len(parts) == 3 and parts[:2] == ["api", "evidence-packs"]:
                return 200, {"evidence_pack": get_evidence_pack(self.conn, parts[2])}
            if method == "GET" and parts == ["api", "evidence-graph"]:
                return 200, {"graph": list_evidence_graph(self.conn)}
            if method == "GET" and len(parts) == 3 and parts[:2] == ["api", "evidence-graph"]:
                return 200, {"graph": list_evidence_graph(self.conn, parts[2])}
            if method == "GET" and parts == ["api", "recommendations"]:
                return 200, {"recommendations": list_recommendation_history(self.conn)}
            if method == "GET" and parts == ["api", "follow-up-outcomes"]:
                return 200, {"follow_up_outcomes": list_followup_history(self.conn)}
            if method == "GET" and parts == ["api", "report-settings"]:
                return 200, {"report_settings": list_persisted_report_settings(self.conn)}
            if method == "GET" and parts == ["api", "safety-audit"]:
                return 200, {"safety_audit": list_safety_audit(self.conn)}
            if method == "GET" and parts == ["api", "snapshot", "export"]:
                return 200, {"snapshot": list_snapshot_export(self.conn)}
            if method == "POST" and parts == ["api", "snapshot", "validate-import"]:
                return 200, {"validation": validate_snapshot_payload(_required(body, "snapshot"))}
            if method == "GET" and parts == ["api", "contracts"]:
                return 200, {"contracts": list_api_contracts(), "fixture_api_matrix": list_expected_api_cases()}
            if method == "GET" and parts == ["api", "error-examples"]:
                return 200, {"errors": error_examples()}
            if method == "GET" and parts == ["api", "report-candidates"]:
                return 200, {"report_candidates": list_report_candidates(self.conn)}
            if method == "GET" and len(parts) == 3 and parts[:2] == ["api", "conversation-threads"]:
                return 200, {"thread": get_conversation_thread(self.conn, parts[2])}
            if method == "GET" and parts == ["api", "workbench", "bootstrap"]:
                return 200, bootstrap_payload(self.conn)
            if method == "GET" and parts == ["api", "source-adapters"]:
                return 200, {"adapters": list_source_adapters()}
            if method == "GET" and parts == ["api", "manual-exports"]:
                return 200, {"exports": list_manual_exports()}
            if method == "GET" and len(parts) == 3 and parts[:2] == ["api", "manual-exports"]:
                return 200, {"export": get_manual_export_detail(parts[2])}
            if method == "POST" and parts == ["api", "manual-imports", "preview"]:
                export_id = _required(body, "export_id")
                return 200, {"session": preview_manual_import(self.conn, export_id, commit=False)}
            if method == "POST" and parts == ["api", "manual-imports", "commit-synthetic"]:
                export_id = _required(body, "export_id")
                return 200, {"session": preview_manual_import(self.conn, export_id, commit=True)}
            if method == "GET" and parts == ["api", "manual-imports", "sessions"]:
                return 200, {"sessions": list_manual_import_sessions(self.conn)}
            if method == "GET" and len(parts) == 4 and parts[:3] == ["api", "manual-imports", "sessions"]:
                return 200, {"session": get_manual_import_session(self.conn, parts[3])}
            if method == "GET" and len(parts) == 4 and parts[:2] == ["api", "manual-imports"] and parts[3] == "mapping":
                return 200, get_manual_import_mapping(self.conn, parts[2])
            if method == "GET" and len(parts) == 4 and parts[:2] == ["api", "manual-imports"] and parts[3] == "conflicts":
                return 200, get_manual_import_conflicts(self.conn, parts[2])
            if method == "GET" and parts == ["api", "manual-imports", "audit-summary"]:
                return 200, {"manual_import_audit": manual_import_audit_summary(self.conn)}
            if method == "GET" and len(parts) == 4 and parts[:3] == ["api", "fixtures", "state"]:
                fixture_id = parts[3]
                import_fixture(self.conn, load_fixture(Path("fixtures/dtu") / f"{fixture_id}.json"))
                return 200, {
                    "fixture_id": fixture_id,
                    "source_records": list_source_records(self.conn, fixture_id),
                    "normalized_facts": list_normalized_facts(self.conn, fixture_id),
                    "derived_facts": list_derived_facts(self.conn, fixture_id),
                }
            if method == "POST" and parts == ["api", "replay-fixture"]:
                fixture_id = _required(body, "fixture_id")
                return 200, {"replay": replay_fixture(self.conn, fixture_id)}
            return 404, problem_detail(404, "Not Found", f"No local API route matches {parsed.path}.", parsed.path)
        except (KeyError, FileNotFoundError, ValueError) as exc:
            field = None
            detail = str(exc).strip("'")
            if "fixture_id" in detail:
                field = "fixture_id"
            elif "workflow" in detail:
                field = "workflow"
            return 400, problem_detail(400, "Local API Error", detail, parsed.path, field)


def make_handler(api: WorkbenchAPI):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self._handle("GET")

        def do_POST(self) -> None:
            self._handle("POST")

        def _handle(self, method: str) -> None:
            if method == "GET" and self._serve_static():
                return
            length = int(self.headers.get("Content-Length", "0"))
            body = None
            if length:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
            status, payload = api.handle(method, self.path, body)
            raw = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _serve_static(self) -> bool:
            static_map = {
                "/": ("workbench/index.html", "text/html; charset=utf-8"),
                "/workbench/": ("workbench/index.html", "text/html; charset=utf-8"),
                "/workbench/index.html": ("workbench/index.html", "text/html; charset=utf-8"),
                "/workbench/styles.css": ("workbench/styles.css", "text/css; charset=utf-8"),
                "/workbench/app.js": ("workbench/app.js", "application/javascript; charset=utf-8"),
            }
            parsed = urlparse(self.path)
            if parsed.path not in static_map:
                return False
            path, content_type = static_map[parsed.path]
            raw = Path(path).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return True

        def log_message(self, format: str, *args: Any) -> None:
            return

    return Handler


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic local OS workbench API.")
    parser.add_argument("--db", default=":memory:")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Mission 008 API may bind only to localhost.")
    api = WorkbenchAPI(args.db)
    server = HTTPServer((args.host, args.port), make_handler(api))
    host, port = server.server_address
    print(json.dumps({"status": "serving", "host": host, "port": port, "local_only": True}))
    server.serve_forever()
    return 0


def _required(body: dict[str, Any] | None, key: str) -> Any:
    if body is None or key not in body:
        raise KeyError(f"missing required field: {key}")
    return body[key]


if __name__ == "__main__":
    raise SystemExit(main())
