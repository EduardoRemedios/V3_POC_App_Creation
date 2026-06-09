from __future__ import annotations

import json
import subprocess
from pathlib import Path


FIXTURE = Path("fixtures/mission_017/stale_reentry.json")
MISSION_ID = "MISSION_017_STALE_REENTRY_DETECTION"


def main() -> int:
    failures: list[str] = []
    actual_head = _current_head()
    if not FIXTURE.exists():
        failures.append(f"missing fixture: {FIXTURE}")
        expected_head = ""
        payload = {}
    else:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        expected_head = str(payload.get("expected_head", ""))
        if payload.get("mission_id") != MISSION_ID:
            failures.append("mission_id mismatch")
        if payload.get("synthetic_only") is not True:
            failures.append("fixture must be synthetic_only")
        if payload.get("real_data_used") is not False:
            failures.append("fixture must not use real data")
        if payload.get("live_integrations_used") is not False:
            failures.append("fixture must not use live integrations")
        if payload.get("new_dependencies_used") is not False:
            failures.append("fixture must not use new dependencies")
        if payload.get("reentry_state") != "stale":
            failures.append("reentry_state must be stale")
        if payload.get("required_decision") != "halt_without_reconciliation":
            failures.append("required_decision must be halt_without_reconciliation")
        if payload.get("reconciliation_allowed") is not False:
            failures.append("reconciliation_allowed must be false")
        if not expected_head:
            failures.append("expected_head is required")
        if expected_head == actual_head:
            failures.append("expected_head unexpectedly matches actual head; stale reentry was not reproduced")
        else:
            failures.append(f"stale reentry detected: expected {expected_head}, actual {actual_head}")

    result = {
        "actual_head": actual_head,
        "expected_head": expected_head,
        "failures": failures,
        "mission_id": MISSION_ID,
        "status": "fail" if failures else "pass"
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


def _current_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


if __name__ == "__main__":
    raise SystemExit(main())
