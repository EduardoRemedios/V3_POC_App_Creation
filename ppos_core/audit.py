"""Mission 009 audit summary generation."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .api_contracts import contract_rows
from .fixture_manifest import family_summary, validate_manifest
from .repositories import WorkbenchRepository


WORKBENCH_VIEWS = [
    "fixture catalog",
    "replay debugger",
    "evidence graph",
    "workflow api runner",
    "reports",
    "conversation continuity",
    "recommendations follow-up",
    "safety audit",
]


def build_audit_summary(
    conn: sqlite3.Connection,
    gates: dict[str, str] | None = None,
    commands_run: list[str] | None = None,
    browser_status: str = "pending",
    test_check_count: int = 0,
) -> dict[str, Any]:
    repo = WorkbenchRepository(conn)
    manifest_validation = validate_manifest()
    return {
        "mission_id": "MISSION_009_SYNTHETIC_WORKBENCH_PRODUCT_EXPANSION",
        "status": "COMPLETE" if gates and all(value == "PASS" for value in gates.values()) else "IN_PROGRESS",
        "fixture_count": manifest_validation["fixture_count"],
        "fixture_families": family_summary(),
        "test_check_count": test_check_count,
        "db_tables": repo.table_names(),
        "api_endpoints": [row["path_template"] for row in contract_rows()],
        "workbench_views": WORKBENCH_VIEWS,
        "browser_ui_qa": browser_status,
        "gates": gates or {},
        "commands_run": commands_run or [],
        "dependency_review": {
            "packages_installed": [],
            "policy": "Python standard library and static browser-native APIs only",
            "new_dependencies": "none",
        },
        "compliance": {
            "v3_only": True,
            "synthetic_only": True,
            "no_live_integrations": True,
            "no_real_data": True,
            "no_package_install": True,
            "localhost_only": True,
        },
        "residual_risks": [
            "Synthetic thresholds remain fixture-calibrated, not real-data calibrated.",
            "Browser visual QA covers smoke paths only, not full accessibility certification.",
            "Evidence graph layout is intentionally simple and bounded; it is not a general graph engine.",
        ],
    }


def write_audit_summary(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
