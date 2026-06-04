from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ppos_core.api import WorkbenchAPI


AUDIT_PATH = Path(".factory-v3/evidence/MISSION_013_AUDIT_SUMMARY.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Mission 013 Garmin bridge QA")
    parser.add_argument("--db", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8800)
    args = parser.parse_args()

    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Mission 013 QA may only target localhost.")

    db_path = Path(args.db)
    if db_path.exists():
        db_path.unlink()
    api = WorkbenchAPI(db_path)
    checks: list[dict[str, Any]] = []

    exports = _expect(api, "GET", "/api/garmin-exports", None, checks, "garmin export catalog")
    _assert(len(exports["exports"]) >= 7, "expected Garmin fixture catalog entries")

    approval = _expect(
        api,
        "POST",
        "/api/manual-imports/approval",
        {
            "export_id": "garmin_activities_clean_csv",
            "retention_posture": "keep-raw-until-verified",
            "approval_state": "approved",
            "preview_only": True,
            "consent_text": "Synthetic Mission 013 QA approval rehearsal; no real file is read.",
        },
        checks,
        "synthetic approval",
    )["approval"]
    _assert(approval["synthetic_only"] and approval["source_label"] == "real_garmin_manual_export", "approval source label")

    preview = _expect(
        api,
        "POST",
        "/api/manual-imports/preview",
        {"export_id": "garmin_activities_clean_csv"},
        checks,
        "preview Garmin activities",
    )["session"]
    for row_index in (1, 2, 3):
        _expect(
            api,
            "POST",
            "/api/manual-imports/review-row",
            {"session_id": preview["id"], "row_index": row_index, "review_state": "accepted"},
            checks,
            f"accept row {row_index}",
        )
    committed = _expect(
        api,
        "POST",
        "/api/manual-imports/commit-reviewed",
        {"session_id": preview["id"]},
        checks,
        "commit reviewed Garmin activities",
    )["session"]
    _assert(len(committed["materialized_facts"]) == 3, "materialized activity facts")

    consumed = _expect(api, "POST", f"/api/manual-imports/{committed['id']}/consume", {}, checks, "consume imported facts")[
        "consumption"
    ]
    _assert(consumed["workflow_count"] >= 2, "imported facts consumed by at least two workflows")
    _assert(consumed["graph"]["node_count"] > 0, "evidence graph nodes created")
    timeline = _expect(api, "GET", f"/api/workflows/{consumed['timeline_run_ids'][0]}/timeline", None, checks, "timeline read")[
        "timeline"
    ]
    _assert(timeline["passed"], "workflow timeline passed")
    reports = _expect(api, "GET", "/api/report-candidates", None, checks, "report candidates")["report_candidates"]
    _assert(any(report["fixture_id"] == committed["id"] for report in reports), "import report candidates persisted")

    rollback_preview = _expect(
        api,
        "POST",
        "/api/manual-imports/preview",
        {"export_id": "garmin_body_composition_clean_csv"},
        checks,
        "preview Garmin body composition",
    )["session"]
    for row_index in (1, 2, 3):
        _expect(
            api,
            "POST",
            "/api/manual-imports/review-row",
            {"session_id": rollback_preview["id"], "row_index": row_index, "review_state": "accepted"},
            checks,
            f"accept body row {row_index}",
        )
    rollback_committed = _expect(
        api,
        "POST",
        "/api/manual-imports/commit-reviewed",
        {"session_id": rollback_preview["id"]},
        checks,
        "commit reviewed body composition",
    )["session"]
    reverted = _expect(
        api,
        "POST",
        "/api/manual-imports/rollback",
        {"session_id": rollback_committed["id"], "reason": "Mission 013 QA rollback"},
        checks,
        "rollback materialized facts",
    )["session"]
    _assert(reverted["status"] == "reverted", "rollback session status")
    _assert(all(not fact["active"] for fact in reverted["materialized_facts"]), "rollback ledger inactive")

    audit = _expect(api, "GET", "/api/manual-imports/audit-summary", None, checks, "manual import audit")["manual_import_audit"]
    payload = {
        "schema_version": "mission_013_audit_summary_v1",
        "mission_id": "MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS",
        "synthetic_only": True,
        "local_only": True,
        "db_path": str(db_path),
        "host": args.host,
        "port": args.port,
        "checks": checks,
        "manual_import_audit": audit,
        "consumption": consumed,
        "approval": approval,
        "real_data_used": False,
        "live_integrations_used": False,
    }
    AUDIT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "checks": len(checks), "audit_path": str(AUDIT_PATH)}, sort_keys=True))
    return 0


def _expect(
    api: WorkbenchAPI, method: str, path: str, body: dict[str, Any] | None, checks: list[dict[str, Any]], label: str
) -> dict[str, Any]:
    status, payload = api.handle(method, path, body)
    checks.append({"label": label, "method": method, "path": path, "status": status})
    _assert(status == 200, f"{label} returned {status}: {payload}")
    return payload


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    raise SystemExit(main())
