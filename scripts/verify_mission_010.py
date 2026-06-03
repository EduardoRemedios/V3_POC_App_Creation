"""Mission 010 verification harness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(".")
MISSION = ROOT / ".factory-v3/missions/MISSION_010_SYNTHETIC_WORKBENCH_QA_AND_OPERATOR_READINESS.md"
PLAN = ROOT / ".factory-v3/evidence/MISSION_010_IMPLEMENTATION_PLAN.md"
STATE = ROOT / ".factory-v3/evidence/MISSION_010_STATE.md"
CHECKPOINTS = ROOT / ".factory-v3/evidence/MISSION_010_CHECKPOINTS.md"
CLOSEOUT = ROOT / ".factory-v3/evidence/MISSION_010_CLOSEOUT.md"
RECORD = ROOT / ".factory-v3/evidence/MISSION_010_RECORD.json"
AUDIT = ROOT / ".factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json"
BROWSER_NOTES = ROOT / ".factory-v3/evidence/MISSION_010_BROWSER_NOTES.md"
WORKBENCH_FILES = [
    ROOT / "workbench/index.html",
    ROOT / "workbench/app.js",
    ROOT / "workbench/styles.css",
]
FORBIDDEN_RUNTIME_MARKERS = [
    "factoryctl",
    "stage-lint",
    "pack-lint",
    "bot_token",
    "webhook",
    "polling loop",
    "garmin.com",
    "strava.com",
]


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    for path in [MISSION, PLAN, STATE, CHECKPOINTS, CLOSEOUT, RECORD, AUDIT, BROWSER_NOTES, *WORKBENCH_FILES]:
        checks.append((f"exists:{path}", path.exists(), str(path)))

    record = load_json(RECORD)
    audit = load_json(AUDIT)
    checks.extend(
        [
            ("record_v3_only", record["record"]["v3_only"] is True, ""),
            ("record_no_v2", record["record"]["factory_v2_used"] is False, ""),
            ("record_state_reference", record["adaptive_mission_control"]["mission_state_reference"] == str(STATE), ""),
            ("audit_status_pass", audit["status"] == "pass", ""),
            ("audit_synthetic_only", audit["synthetic_only"] is True, ""),
            ("audit_no_package_install", audit["no_package_install"] is True, ""),
            ("audit_fixture_count", audit["api_scenario"]["fixture_count"] >= 35, ""),
            ("audit_timeline_steps", audit["api_scenario"]["timeline_step_count"] >= 3, ""),
            ("audit_error_contract", audit["api_scenario"]["error_contract_status"] is True, ""),
        ]
    )

    html = (ROOT / "workbench/index.html").read_text(encoding="utf-8")
    js = (ROOT / "workbench/app.js").read_text(encoding="utf-8")
    css = (ROOT / "workbench/styles.css").read_text(encoding="utf-8")
    for marker in [
        'data-testid="run-scenario"',
        'data-testid="operator-state"',
        'data-testid="scenario-output"',
        'data-testid="view-audit"',
    ]:
        checks.append((f"html_marker:{marker}", marker in html, ""))
    for marker in ["runScenarioWalkthrough", "localStorage", "if (!response.ok)", "resetWorkbench"]:
        checks.append((f"js_marker:{marker}", marker in js, ""))
    for marker in ["@media (max-width: 860px)", "#view-runner.is-active", ".toolbar > select"]:
        checks.append((f"css_marker:{marker}", marker in css, ""))

    source_text = "\n".join(path.read_text(encoding="utf-8") for path in WORKBENCH_FILES)
    for marker in FORBIDDEN_RUNTIME_MARKERS:
        checks.append((f"runtime_no_go_absent:{marker}", marker not in source_text.lower(), ""))

    failed = [check for check in checks if not check[1]]
    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        suffix = f" {detail}" if detail else ""
        print(f"{status} {name}{suffix}")
    if failed:
        raise SystemExit(f"Mission 010 verification failed: {len(failed)} checks failed")
    print(f"Mission 010 verification passed: {len(checks)} checks")
    return 0


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main())
