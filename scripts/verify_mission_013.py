from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


MISSION_ID = "MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS"


REQUIRED_FILES = [
    ".factory-v3/missions/MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS.md",
    ".factory-v3/evidence/MISSION_013_IMPLEMENTATION_PLAN.md",
    ".factory-v3/evidence/MISSION_013_GARMIN_EXPORT_SHAPE_RESEARCH.md",
    ".factory-v3/evidence/MISSION_013_STATE.md",
    ".factory-v3/evidence/MISSION_013_CHECKPOINTS.md",
    ".factory-v3/evidence/MISSION_013_INTERRUPT_HDI001.json",
    ".factory-v3/evidence/MISSION_013_INTERRUPT_HDI002.json",
    ".factory-v3/evidence/MISSION_013_CLOSEOUT.md",
    ".factory-v3/evidence/MISSION_013_RECORD.json",
    ".factory-v3/evidence/MISSION_013_AUDIT_SUMMARY.json",
    ".factory-v3/evidence/MISSION_013_BROWSER_NOTES.md",
    "fixtures/garmin_exports/manifest.json",
]


def main() -> int:
    failures: list[str] = []
    for path in REQUIRED_FILES:
        if not Path(path).exists():
            failures.append(f"missing required file: {path}")

    _check_interrupt(".factory-v3/evidence/MISSION_013_INTERRUPT_HDI001.json", failures)
    _check_interrupt(".factory-v3/evidence/MISSION_013_INTERRUPT_HDI002.json", failures)
    _check_manifest(failures)
    _check_state_and_checkpoints(failures)
    _check_record(failures)
    _check_audit(failures)
    _check_git_log(failures)
    _check_no_go_scan(failures)

    if failures:
        print(json.dumps({"status": "fail", "failures": failures}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "pass", "mission_id": MISSION_ID}, sort_keys=True))
    return 0


def _check_interrupt(path: str, failures: list[str]) -> None:
    if not Path(path).exists():
        return
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("status") != "applied":
        failures.append(f"{path} status is not applied")
    answer = payload.get("answer", {})
    if not answer.get("answer_text") or not answer.get("selected_option_id"):
        failures.append(f"{path} missing answer text or selected option")
    if payload.get("asked", {}).get("surface") != "codex-mobile-thread":
        failures.append(f"{path} asked surface is not codex-mobile-thread")
    if payload.get("mission_delta", {}).get("required") not in {False, "false"}:
        if not payload.get("mission_delta", {}).get("delta_reference"):
            failures.append(f"{path} requires plan delta without reference")


def _check_manifest(failures: list[str]) -> None:
    path = Path("fixtures/garmin_exports/manifest.json")
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("synthetic_only") is not True:
        failures.append("Garmin manifest is not synthetic_only")
    families = {entry.get("family") for entry in manifest.get("exports", [])}
    for family in {"activities", "sleep", "body_composition"}:
        if family not in families:
            failures.append(f"missing Garmin fixture family: {family}")
    for entry in manifest.get("exports", []):
        if entry.get("synthetic_label") != "SYNTHETIC_MISSION_013_GARMIN_SHAPE":
            failures.append(f"missing synthetic label: {entry.get('export_id')}")


def _check_state_and_checkpoints(failures: list[str]) -> None:
    state = _read(".factory-v3/evidence/MISSION_013_STATE.md")
    checkpoints = _read(".factory-v3/evidence/MISSION_013_CHECKPOINTS.md")
    if "Fresh-session resume occurred" not in state or "read exactly" not in state:
        failures.append("fresh-session resume evidence is missing from state")
    if "Commit after: 9d43abd" not in checkpoints:
        failures.append("checkpoint 007 commit_after was not resolved")
    checkpoint_count = checkpoints.count("## Checkpoint ")
    budget_count = checkpoints.count("## Budget State")
    if budget_count < checkpoint_count:
        failures.append(f"budget states missing: {budget_count}/{checkpoint_count}")
    if checkpoints.count("## Mid-Mission Budget Review") < 2:
        failures.append("expected at least two mid-mission budget reviews")


def _check_record(failures: list[str]) -> None:
    path = Path(".factory-v3/evidence/MISSION_013_RECORD.json")
    if not path.exists():
        return
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("schema_version") != "v0.1-poc-standalone":
        failures.append("record schema_version mismatch")
    if record.get("mission_id") != MISSION_ID:
        failures.append("record mission_id mismatch")
    if "adaptive_mission_control" not in record:
        failures.append("record missing adaptive_mission_control")


def _check_audit(failures: list[str]) -> None:
    path = Path(".factory-v3/evidence/MISSION_013_AUDIT_SUMMARY.json")
    if not path.exists():
        return
    audit = json.loads(path.read_text(encoding="utf-8"))
    if audit.get("synthetic_only") is not True:
        failures.append("audit summary is not synthetic_only")
    if audit.get("real_data_used") is not False:
        failures.append("audit summary does not explicitly reject real data use")


def _check_git_log(failures: list[str]) -> None:
    log = subprocess.check_output(["git", "log", "--oneline", "-n", "40"], text=True)
    for checkpoint in range(1, 12):
        marker = f"Mission 013 checkpoint {checkpoint:03d}"
        if marker not in log:
            failures.append(f"git log missing {marker}")


def _check_no_go_scan(failures: list[str]) -> None:
    fixture_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in Path("fixtures/garmin_exports").glob("*"))
    forbidden = ["access_token", "refresh_token", "oauth", "real personal", "not synthetic"]
    lower = fixture_text.lower()
    for marker in forbidden:
        if marker in lower:
            failures.append(f"forbidden fixture marker found: {marker}")


def _read(path: str) -> str:
    target = Path(path)
    return target.read_text(encoding="utf-8") if target.exists() else ""


if __name__ == "__main__":
    raise SystemExit(main())
