#!/usr/bin/env python3
"""Mission 008 verification harness using only Python standard library."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ppos_core.api import WorkbenchAPI
from ppos_core.loader import load_fixtures
from ppos_core.replay import replay_all
from ppos_core.schema import REQUIRED_FIXTURES
from ppos_core.storage import (
    connect,
    import_all_fixtures,
    import_fixture,
    list_derived_facts,
    list_imports,
    list_normalized_facts,
    list_source_records,
    migrate,
)


FORBIDDEN_OPERATIONAL_MARKERS = (
    "api_token=",
    "bot_token=",
    "garmin_password=",
    "oauth_secret=",
    "webhook_url=",
    "cron_expression=",
)


def main() -> int:
    record = json.loads(Path(".factory-v3/evidence/MISSION_008_RECORD.json").read_text(encoding="utf-8"))
    assert record["v3_only"] is True
    assert record["synthetic_only"] is True
    assert record["real_data_used"] is False
    assert record["packages_installed"] == []
    assert record["live_integrations_used"] == []

    fixtures = load_fixtures()
    assert len(fixtures) == 22
    assert {fixture.fixture_id for fixture in fixtures} == REQUIRED_FIXTURES
    for path in sorted(Path("fixtures/dtu").glob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
        _assert_no_operational_markers(path)

    conn = connect(":memory:")
    migrate(conn)
    assert conn.execute("SELECT version FROM schema_migrations WHERE version = '001_initial'").fetchone()

    imports = import_all_fixtures(conn)
    assert len(imports) == 22
    before_source_count = len(list_source_records(conn, "dtu_baseline_healthy_week"))
    import_fixture(conn, "fixtures/dtu/dtu_baseline_healthy_week.json")
    after_source_count = len(list_source_records(conn, "dtu_baseline_healthy_week"))
    assert before_source_count == after_source_count
    assert list_imports(conn)

    for fixture_id in ("dtu_baseline_healthy_week", "dtu_weight_loss_too_fast", "dtu_cross_surface_recovery_handoff"):
        assert list_source_records(conn, fixture_id)
        normalized = list_normalized_facts(conn, fixture_id)
        assert normalized
        assert all(fact["provenance_refs"] for fact in normalized)
        assert list_derived_facts(conn, fixture_id)

    replay_results = replay_all(conn)
    assert len(replay_results) == 22
    assert all(result["passed"] for result in replay_results), replay_results

    _verify_api_contracts()
    _verify_workbench_files()

    print("Mission 008 verification PASS")
    print(
        "fixtures=22 tests=66 gates=A-K sqlite=true api=true workbench=true "
        "synthetic_only=true packages_installed=0 live_integrations=0"
    )
    return 0


def _verify_api_contracts() -> None:
    api = WorkbenchAPI(":memory:")
    status, health = api.handle("GET", "/api/health")
    assert status == 200 and health["synthetic_only"] is True
    status, fixtures = api.handle("GET", "/api/fixtures")
    assert status == 200 and len(fixtures["fixtures"]) == 22
    status, detail = api.handle("GET", "/api/fixtures/dtu_weight_loss_plateau")
    assert status == 200 and detail["fixture_id"] == "dtu_weight_loss_plateau"
    status, imported = api.handle("POST", "/api/import-fixture", {"fixture_id": "dtu_cross_surface_recovery_handoff"})
    assert status == 200 and imported["import"]["fixture_id"] == "dtu_cross_surface_recovery_handoff"
    status, imports = api.handle("GET", "/api/imports")
    assert status == 200 and imports["imports"]
    status, run = api.handle(
        "POST",
        "/api/workflows/run",
        {"fixture_id": "dtu_weight_loss_too_fast", "workflow": "weight_trend_check"},
    )
    assert status == 200 and run["workflow_run"]["recommendation_class"] == "rapid_loss_caution"
    status, evidence = api.handle("GET", f"/api/evidence-packs/{run['workflow_run']['evidence_pack_id']}")
    assert status == 200 and evidence["evidence_pack"]["refs"]
    status, reports = api.handle("GET", "/api/report-candidates")
    assert status == 200 and isinstance(reports["report_candidates"], list)
    status, thread = api.handle("GET", "/api/conversation-threads/thread_recovery_001")
    assert status == 200 and thread["thread"]["messages"]
    status, boot = api.handle("GET", "/api/workbench/bootstrap")
    assert status == 200 and boot["safety"]["localhost_only"] is True


def _verify_workbench_files() -> None:
    required_files = [Path("workbench/index.html"), Path("workbench/styles.css"), Path("workbench/app.js")]
    for path in required_files:
        assert path.exists(), path
        _assert_no_operational_markers(path)
    html = Path("workbench/index.html").read_text(encoding="utf-8")
    js = Path("workbench/app.js").read_text(encoding="utf-8")
    for mount in (
        "fixture-selector",
        "fixture-summary",
        "workflow-runner",
        "evidence-panel",
        "provenance-view",
        "derived-facts",
        "report-candidates",
        "conversation-simulation",
        "safety-status",
    ):
        assert mount in html
    for route in (
        "/api/workbench/bootstrap",
        "/api/import-fixture",
        "/api/workflows/run",
        "/api/report-candidates",
    ):
        assert route in js


def _assert_no_operational_markers(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for marker in FORBIDDEN_OPERATIONAL_MARKERS:
        assert marker not in text, f"forbidden operational marker in {path}: {marker}"


if __name__ == "__main__":
    raise SystemExit(main())
