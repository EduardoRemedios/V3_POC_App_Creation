from __future__ import annotations

import json
from pathlib import Path


FIXTURE = Path("fixtures/mission_018/no_go_request.json")
MISSION_ID = "MISSION_018_FALLBACK_NO_GO_EVIDENCE"
FORBIDDEN_ACTIONS = {
    "real_data",
    "credentials_or_tokens",
    "live_garmin_integration",
    "telegram_live_bot",
    "new_dependency_install",
    "deployment",
    "factory_v2_fallback",
}


def main() -> int:
    failures: list[str] = []
    if not FIXTURE.exists():
        failures.append(f"missing fixture: {FIXTURE}")
        payload = {}
    else:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        _check_payload(payload, failures)

    result = {
        "decision": payload.get("decision"),
        "execution_allowed": payload.get("execution_allowed"),
        "failures": failures,
        "mission_id": MISSION_ID,
        "status": "fail" if failures else "pass"
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


def _check_payload(payload: dict, failures: list[str]) -> None:
    if payload.get("mission_id") != MISSION_ID:
        failures.append("mission_id mismatch")
    if payload.get("synthetic_only") is not True:
        failures.append("fixture must be synthetic_only")
    if payload.get("decision") != "no_go":
        failures.append("decision must be no_go")
    if payload.get("execution_allowed") is not False:
        failures.append("execution_allowed must be false")
    if payload.get("fallback_to_v2_allowed") is not False:
        failures.append("fallback_to_v2_allowed must be false")
    if payload.get("required_next_step") != "separate_human_approved_mission_or_no_go":
        failures.append("required_next_step mismatch")
    if payload.get("executed") is not False:
        failures.append("forbidden request must not be executed")

    requested = payload.get("requested_actions", {})
    authority = payload.get("approved_authority", {})
    for action in sorted(FORBIDDEN_ACTIONS):
        if requested.get(action) is not True:
            failures.append(f"requested_actions.{action} must be true for this no-go fixture")
        if authority.get(action) is not False:
            failures.append(f"approved_authority.{action} must be false")


if __name__ == "__main__":
    raise SystemExit(main())
