#!/usr/bin/env python3
"""Mission 007 verification harness using only Python standard library."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ppos_core.loader import load_fixtures
from ppos_core.primitives import derive_summary, derived_facts
from ppos_core.reports import evening_report_candidate, morning_report_candidate
from ppos_core.schema import REQUIRED_FIXTURES
from ppos_core.workflows import run_workflow


FORBIDDEN_OPERATIONAL_MARKERS = (
    "api_token",
    "bot_token",
    "garmin_password",
    "oauth_secret",
    "webhook_url",
    "cron_expression",
)


def main() -> int:
    record = json.loads(Path(".factory-v3/evidence/MISSION_007_RECORD.json").read_text(encoding="utf-8"))
    assert record["v3_only"] is True
    assert record["synthetic_only"] is True
    assert record["real_data_used"] is False
    assert record["packages_installed"] == []
    assert record["live_integrations_used"] == []

    fixtures = load_fixtures()
    assert {fixture.fixture_id for fixture in fixtures} == REQUIRED_FIXTURES

    for fixture in fixtures:
        _verify_fixture(fixture)
        for workflow_name in fixture.expected.get("workflows", {}):
            if workflow_name == "morning_report_candidate":
                result = morning_report_candidate(fixture)
                refs = result.evidence_pack.refs
            elif workflow_name == "evening_report_candidate":
                result = evening_report_candidate(fixture)
                refs = result.evidence_pack.refs
            else:
                result = run_workflow(workflow_name, fixture)
                refs = result.evidence_pack.refs
            for ref in fixture.expected["workflows"][workflow_name].get("required_evidence_refs", []):
                assert ref in refs, f"{fixture.fixture_id}:{workflow_name}:{ref}"

    print("Mission 007 verification PASS")
    print(f"fixtures={len(fixtures)} gates=A-F synthetic_only=true packages_installed=0 live_integrations=0")
    return 0


def _verify_fixture(fixture) -> None:
    text = fixture.path.read_text(encoding="utf-8").lower()
    for marker in FORBIDDEN_OPERATIONAL_MARKERS:
        assert marker not in text, f"forbidden operational marker in {fixture.path}: {marker}"
    summary = derive_summary(fixture)
    for key, expected_value in fixture.expected.get("derived", {}).items():
        assert summary.get(key) == expected_value, f"{fixture.fixture_id}:{key}"
    source_ids = fixture.record_ids()
    for fact in fixture.normalized_facts:
        assert set(fact.provenance_refs).issubset(source_ids)
    for fact in derived_facts(fixture):
        assert set(fact.provenance_refs).issubset(source_ids)


if __name__ == "__main__":
    raise SystemExit(main())
