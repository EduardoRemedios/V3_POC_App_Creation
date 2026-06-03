"""Mission 009 local API contract metadata and error shapes."""

from __future__ import annotations

from typing import Any


API_CONTRACTS = (
    ("GET", "/api/health", "mission008", 200, False, "Health and synthetic/local status."),
    ("GET", "/api/fixtures", "mission008", 200, False, "List DTU fixtures."),
    ("GET", "/api/fixtures/{fixture_id}", "mission008", 200, False, "Fixture detail."),
    ("POST", "/api/import-fixture", "mission008", 200, False, "Import fixture into SQLite."),
    ("GET", "/api/imports", "mission008", 200, False, "List fixture imports."),
    ("POST", "/api/workflows/run", "mission008", 200, False, "Run and persist workflow."),
    ("GET", "/api/workflows/{run_id}", "mission008", 200, False, "Get workflow run."),
    ("GET", "/api/evidence-packs/{evidence_pack_id}", "mission008", 200, False, "Get evidence pack."),
    ("GET", "/api/report-candidates", "mission008", 200, False, "List report candidates."),
    ("GET", "/api/conversation-threads/{thread_id}", "mission008", 200, False, "Conversation thread."),
    ("GET", "/api/workbench/bootstrap", "mission008", 200, False, "Workbench bootstrap."),
    ("GET", "/api/fixture-manifest", "mission009", 200, False, "Fixture manifest and consistency."),
    ("GET", "/api/fixture-families", "mission009", 200, False, "Fixture family summary."),
    ("GET", "/api/fixtures/expected-workflows", "mission009", 200, False, "Expected workflow matrix."),
    ("GET", "/api/imports/audit-summary", "mission009", 200, False, "Import and replay audit summary."),
    ("GET", "/api/workflows/{run_id}/timeline", "mission009", 200, False, "Workflow timeline."),
    ("GET", "/api/evidence-graph", "mission009", 200, False, "Evidence graph."),
    ("GET", "/api/evidence-graph/{fixture_id}", "mission009", 200, False, "Fixture evidence graph."),
    ("GET", "/api/recommendations", "mission009", 200, False, "Recommendation history."),
    ("GET", "/api/follow-up-outcomes", "mission009", 200, False, "Follow-up outcomes."),
    ("GET", "/api/report-settings", "mission009", 200, False, "Report settings."),
    ("GET", "/api/safety-audit", "mission009", 200, False, "Safety audit."),
    ("GET", "/api/snapshot/export", "mission009", 200, False, "Snapshot export."),
    ("POST", "/api/snapshot/validate-import", "mission009", 200, False, "Snapshot import validation."),
    ("GET", "/api/contracts", "mission009", 200, False, "API contract matrix."),
    ("GET", "/api/error-examples", "mission009", 200, True, "Problem-detail-like error examples."),
    ("POST", "/api/workflows/run:error_unknown_workflow", "mission009_error", 400, True, "Unknown workflow error."),
    ("POST", "/api/import-fixture:error_missing_fixture_id", "mission009_error", 400, True, "Missing field error."),
    ("GET", "/api/fixtures/{fixture_id}:error_missing_fixture", "mission009_error", 400, True, "Missing fixture error."),
    ("GET", "/api/not-a-route", "mission009_error", 404, True, "Not found error."),
)


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": f"{method} {path}",
            "method": method,
            "path_template": path,
            "category": category,
            "expected_status": status,
            "error_shape": error_shape,
            "description": description,
        }
        for method, path, category, status, error_shape, description in API_CONTRACTS
    ]


def problem_detail(status: int, title: str, detail: str, instance: str = "", field: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": f"local://ppos/errors/{title.lower().replace(' ', '-')}",
        "title": title,
        "status": status,
        "detail": detail,
    }
    if instance:
        payload["instance"] = instance
    if field:
        payload["field"] = field
    return payload


def error_examples() -> list[dict[str, Any]]:
    return [
        problem_detail(400, "Missing Required Field", "Request body must include fixture_id.", field="fixture_id"),
        problem_detail(400, "Unknown Workflow", "Workflow is not in the local synthetic workflow registry.", field="workflow"),
        problem_detail(400, "Fixture Not Found", "Requested synthetic fixture file does not exist.", field="fixture_id"),
        problem_detail(404, "Not Found", "No local API route matches the request path."),
    ]
