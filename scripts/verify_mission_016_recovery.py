from __future__ import annotations

import json
from pathlib import Path


FIXTURE = Path("fixtures/mission_016/recovery_gate.json")
MISSION_ID = "MISSION_016_FAILED_VERIFICATION_RECOVERY"


def main() -> int:
    failures: list[str] = []
    if not FIXTURE.exists():
        failures.append(f"missing fixture: {FIXTURE}")
    else:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
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
        if payload.get("failure_classification") != "authorized_recovery_fixture_issue":
            failures.append("failure classification mismatch")
        if payload.get("recovery_gate") != "pass":
            failures.append("recovery_gate must be pass after authorized recovery")
        if payload.get("recovered_after_failure") is not True:
            failures.append("recovered_after_failure must be true after authorized recovery")

    if failures:
        print(json.dumps({"status": "fail", "failures": failures}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "pass", "mission_id": MISSION_ID}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
