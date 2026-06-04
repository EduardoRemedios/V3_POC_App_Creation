"""Mission 012 verification harness."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(".")
MISSION = ROOT / ".factory-v3/missions/MISSION_012_SYNTHETIC_IMPORT_HARDENING_AND_REAL_DATA_BRIDGE_DECISION.md"
PLAN = ROOT / ".factory-v3/evidence/MISSION_012_IMPLEMENTATION_PLAN.md"
STATE = ROOT / ".factory-v3/evidence/MISSION_012_STATE.md"
CHECKPOINTS = ROOT / ".factory-v3/evidence/MISSION_012_CHECKPOINTS.md"
INTERRUPT = ROOT / ".factory-v3/evidence/MISSION_012_INTERRUPT_HDI001.json"
DESIGN = ROOT / ".factory-v3/evidence/MISSION_012_REAL_DATA_APPROVAL_DESIGN.md"
CLOSEOUT = ROOT / ".factory-v3/evidence/MISSION_012_CLOSEOUT.md"
RECORD = ROOT / ".factory-v3/evidence/MISSION_012_RECORD.json"
AUDIT = ROOT / ".factory-v3/evidence/MISSION_012_AUDIT_SUMMARY.json"
BROWSER_NOTES = ROOT / ".factory-v3/evidence/MISSION_012_BROWSER_NOTES.md"
AUTHORIZED_OUTPUTS = [
    MISSION,
    PLAN,
    STATE,
    CHECKPOINTS,
    INTERRUPT,
    DESIGN,
    CLOSEOUT,
    RECORD,
    AUDIT,
    BROWSER_NOTES,
    ROOT / "ppos_core/migrations/004_mission_012.sql",
    ROOT / "ppos_core/storage.py",
    ROOT / "ppos_core/api.py",
    ROOT / "ppos_core/workbench.py",
    ROOT / "workbench/index.html",
    ROOT / "workbench/app.js",
    ROOT / "workbench/styles.css",
    ROOT / "scripts/mission_012_review_rollback_qa.py",
    ROOT / "scripts/verify_mission_012.py",
    ROOT / "tests/test_mission_012_review_workflow.py",
    ROOT / "tests/test_mission_012_rollback.py",
    ROOT / "tests/test_mission_012_api.py",
    ROOT / "tests/test_mission_012_workbench.py",
]
FORBIDDEN_RUNTIME_MARKERS = [
    "connect.garmin",
    "strava.com/api",
    "botfather",
    "bot_token",
    "webhook",
    "getupdates",
    "factoryctl",
    "stage-lint",
    "pack-lint",
]


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    for path in AUTHORIZED_OUTPUTS:
        checks.append((f"exists:{path}", path.exists(), str(path)))

    interrupt = load_json(INTERRUPT)
    audit = load_json(AUDIT) if AUDIT.exists() else {}
    record = load_json(RECORD) if RECORD.exists() else {}
    checkpoints = CHECKPOINTS.read_text(encoding="utf-8") if CHECKPOINTS.exists() else ""
    state = STATE.read_text(encoding="utf-8") if STATE.exists() else ""
    design = DESIGN.read_text(encoding="utf-8") if DESIGN.exists() else ""
    git_log = subprocess.check_output(["git", "log", "--oneline", "-n", "40"], text=True)

    checks.extend(
        [
            ("interrupt_applied", interrupt["status"] == "applied", ""),
            ("interrupt_option_a", interrupt["answer"]["selected_option_id"] == "option_a", ""),
            ("interrupt_continues", interrupt["continuation_decision"] == "continue", ""),
            ("interrupt_no_plan_delta", interrupt["mission_delta"]["required"] is False, ""),
            ("interrupt_resume_artifacts_recorded", len(interrupt.get("applied", {}).get("resume_artifacts_read", [])) >= 5, ""),
            ("state_records_resume", "Fresh resume session read" in state, ""),
            ("state_records_applied_hdi", "HDI-012-001 status: `applied`" in state, ""),
            ("checkpoint_budget_tool_counts", checkpoints.count("Tool-call count since last checkpoint:") >= 7, ""),
            ("checkpoint_budget_wall_clock", checkpoints.count("Wall-clock time since last checkpoint:") >= 7, ""),
            ("checkpoint_budget_stop_threshold", checkpoints.count("Stop threshold reached:") >= 7, ""),
            ("plan_delta_rule_satisfied", not (ROOT / ".factory-v3/evidence/MISSION_012_PLAN_DELTA_001.md").exists(), ""),
            ("design_option_a_garmin", "manual Garmin export/import" in design, ""),
            ("design_consent", "Consent" in design or "consent" in design, ""),
            ("design_retention", "Retention" in design or "retention" in design, ""),
            ("design_rollback", "Rollback" in design or "rollback" in design, ""),
        ]
    )
    if audit:
        checks.extend(
            [
                ("audit_status_pass", audit.get("status") == "pass", ""),
                ("audit_synthetic_only", audit.get("synthetic_only") is True, ""),
                ("audit_no_package_install", audit.get("no_package_install") is True, ""),
                ("audit_rollback_passed", audit.get("api_checks", {}).get("rollback_status") == "reverted", ""),
            ]
        )
    if record:
        checks.extend(
            [
                ("record_schema", record["record"]["schema_version"] == "v0.1-poc-standalone", ""),
                ("record_v3_only", record["record"]["v3_only"] is True, ""),
                ("record_no_v2", record["record"]["factory_v2_used"] is False, ""),
                ("record_state_reference", record["adaptive_mission_control"]["mission_state_reference"] == str(STATE), ""),
                ("record_hdi_reference", any(item.get("interrupt_id") == "HDI-012-001" for item in record["adaptive_mission_control"]["human_decision_interrupts"]), ""),
            ]
        )
    if BROWSER_NOTES.exists():
        browser_notes = BROWSER_NOTES.read_text(encoding="utf-8")
        checks.append(("browser_qa_pass", "Browser QA status: PASS" in browser_notes, ""))

    for checkpoint in range(1, 8):
        marker = f"Mission 012 checkpoint {checkpoint:03d}:"
        checks.append((f"git_checkpoint_{checkpoint:03d}", marker in git_log, ""))

    html = (ROOT / "workbench/index.html").read_text(encoding="utf-8")
    js = (ROOT / "workbench/app.js").read_text(encoding="utf-8")
    css = (ROOT / "workbench/styles.css").read_text(encoding="utf-8")
    for marker in [
        'data-testid="manual-import-row-diff"',
        'data-testid="manual-import-raw-normalized-diff"',
        'data-testid="manual-import-review-actions"',
        "/api/manual-imports/review-row",
        "/api/manual-imports/commit-reviewed",
        "/api/manual-imports/rollback",
        ".diff-grid",
    ]:
        haystack = html + js + css
        checks.append((f"workbench_marker:{marker}", marker in haystack, ""))

    source_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "ppos_core/storage.py",
            ROOT / "ppos_core/api.py",
            ROOT / "ppos_core/workbench.py",
            ROOT / "workbench/index.html",
            ROOT / "workbench/app.js",
            ROOT / "workbench/styles.css",
        ]
    ).lower()
    for marker in FORBIDDEN_RUNTIME_MARKERS:
        checks.append((f"runtime_no_go_absent:{marker}", marker not in source_text, ""))

    failed = [check for check in checks if not check[1]]
    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        suffix = f" {detail}" if detail else ""
        print(f"{status} {name}{suffix}")
    if failed:
        raise SystemExit(f"Mission 012 verification failed: {len(failed)} checks failed")
    print(f"Mission 012 verification passed: {len(checks)} checks")
    return 0


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main())
