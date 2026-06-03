"""Mission 011 verification harness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ppos_core.manual_imports import validate_manual_export_manifest


ROOT = Path(".")
MISSION = ROOT / ".factory-v3/missions/MISSION_011_SYNTHETIC_MANUAL_IMPORT_SOURCE_ADAPTER_READINESS.md"
PLAN = ROOT / ".factory-v3/evidence/MISSION_011_IMPLEMENTATION_PLAN.md"
STATE = ROOT / ".factory-v3/evidence/MISSION_011_STATE.md"
CHECKPOINTS = ROOT / ".factory-v3/evidence/MISSION_011_CHECKPOINTS.md"
CLOSEOUT = ROOT / ".factory-v3/evidence/MISSION_011_CLOSEOUT.md"
RECORD = ROOT / ".factory-v3/evidence/MISSION_011_RECORD.json"
AUDIT = ROOT / ".factory-v3/evidence/MISSION_011_AUDIT_SUMMARY.json"
BROWSER_NOTES = ROOT / ".factory-v3/evidence/MISSION_011_BROWSER_NOTES.md"
MANIFEST = ROOT / "fixtures/manual_exports/manifest.json"
WORKBENCH_FILES = [ROOT / "workbench/index.html", ROOT / "workbench/app.js", ROOT / "workbench/styles.css"]
SOURCE_FILES = [
    ROOT / "ppos_core/manual_imports.py",
    ROOT / "ppos_core/storage.py",
    ROOT / "ppos_core/api.py",
    ROOT / "ppos_core/workbench.py",
]
FORBIDDEN_RUNTIME_MARKERS = [
    "garmin.com",
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
    for path in [MISSION, PLAN, STATE, CHECKPOINTS, CLOSEOUT, RECORD, AUDIT, BROWSER_NOTES, MANIFEST, *WORKBENCH_FILES, *SOURCE_FILES]:
        checks.append((f"exists:{path}", path.exists(), str(path)))

    record = load_json(RECORD)
    audit = load_json(AUDIT)
    manifest_validation = validate_manual_export_manifest()
    checks.extend(
        [
            ("record_v3_only", record["record"]["v3_only"] is True, ""),
            ("record_no_v2", record["record"]["factory_v2_used"] is False, ""),
            ("record_state_reference", record["adaptive_mission_control"]["mission_state_reference"] == str(STATE), ""),
            ("audit_status_pass", audit["status"] == "pass", ""),
            ("audit_synthetic_only", audit["synthetic_only"] is True, ""),
            ("audit_no_package_install", audit["no_package_install"] is True, ""),
            ("audit_export_count", audit["manual_export_fixture_count"] == 9, ""),
            ("audit_adapter_count", audit["adapter_count"] >= 5, ""),
            ("manifest_valid", manifest_validation["valid"], "; ".join(manifest_validation["errors"])),
            ("manifest_synthetic_only", manifest_validation["synthetic_only"] is True, ""),
        ]
    )

    html = (ROOT / "workbench/index.html").read_text(encoding="utf-8")
    js = (ROOT / "workbench/app.js").read_text(encoding="utf-8")
    css = (ROOT / "workbench/styles.css").read_text(encoding="utf-8")
    for marker in [
        'data-testid="view-imports"',
        'data-testid="source-adapter-lab"',
        'data-testid="manual-import-preview"',
        'data-testid="manual-import-mapping"',
        'data-testid="manual-import-conflicts"',
    ]:
        checks.append((f"html_marker:{marker}", marker in html, ""))
    for marker in [
        "/api/manual-imports/preview",
        "/api/manual-imports/commit-synthetic",
        "renderManualImportSession",
        "previewSelectedManualImport",
        "commitSelectedManualImport",
        "manual_export",
    ]:
        checks.append((f"js_marker:{marker}", marker in js, ""))
    checks.append(("css_warning_style", ".warning" in css, ""))

    source_text = "\n".join(path.read_text(encoding="utf-8") for path in WORKBENCH_FILES + SOURCE_FILES).lower()
    for marker in FORBIDDEN_RUNTIME_MARKERS:
        checks.append((f"runtime_no_go_absent:{marker}", marker not in source_text, ""))

    failed = [check for check in checks if not check[1]]
    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        suffix = f" {detail}" if detail else ""
        print(f"{status} {name}{suffix}")
    if failed:
        raise SystemExit(f"Mission 011 verification failed: {len(failed)} checks failed")
    print(f"Mission 011 verification passed: {len(checks)} checks")
    return 0


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main())
