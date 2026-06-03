"""Fixture manifest parsing and consistency checks for Mission 009."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANIFEST_PATH = Path("fixtures/dtu_manifest.json")


def load_manifest(path: str | Path = MANIFEST_PATH) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("synthetic_only") is not True:
        raise ValueError("fixture manifest must be synthetic_only")
    return data


def manifest_fixture_ids(manifest: dict[str, Any] | None = None) -> set[str]:
    manifest = manifest or load_manifest()
    return set(manifest.get("fixtures", {}))


def fixture_file_ids(directory: str | Path = "fixtures/dtu") -> set[str]:
    return {path.stem for path in Path(directory).glob("*.json")}


def validate_manifest(manifest: dict[str, Any] | None = None, directory: str | Path = "fixtures/dtu") -> dict[str, Any]:
    manifest = manifest or load_manifest()
    manifest_ids = manifest_fixture_ids(manifest)
    file_ids = fixture_file_ids(directory)
    families = set(manifest.get("families", {}))
    min_count = int(manifest["required_fixture_count_range"]["min"])
    max_count = int(manifest["required_fixture_count_range"]["max"])
    missing_files = sorted(manifest_ids - file_ids)
    unindexed_files = sorted(file_ids - manifest_ids)
    unknown_families = sorted(
        {
            family
            for entry in manifest["fixtures"].values()
            for family in entry.get("families", [])
            if family not in families
        }
    )
    uncovered_families = sorted(
        family
        for family in families
        if not any(family in entry.get("families", []) for entry in manifest["fixtures"].values())
    )
    passed = (
        not missing_files
        and not unindexed_files
        and not unknown_families
        and not uncovered_families
        and min_count <= len(file_ids) <= max_count
    )
    return {
        "fixture_count": len(file_ids),
        "manifest_count": len(manifest_ids),
        "family_count": len(families),
        "missing_files": missing_files,
        "unindexed_files": unindexed_files,
        "unknown_families": unknown_families,
        "uncovered_families": uncovered_families,
        "passed": passed,
    }


def family_summary(manifest: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    manifest = manifest or load_manifest()
    rows = []
    for family_id, family in sorted(manifest["families"].items()):
        fixtures = [
            fixture_id
            for fixture_id, entry in manifest["fixtures"].items()
            if family_id in entry.get("families", [])
        ]
        rows.append(
            {
                "family_id": family_id,
                "description": family["description"],
                "fixture_count": len(fixtures),
                "fixtures": sorted(fixtures),
            }
        )
    return rows


def workflow_matrix(manifest: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    manifest = manifest or load_manifest()
    rows = []
    for fixture_id, entry in sorted(manifest["fixtures"].items()):
        for workflow in entry.get("workflows", []):
            rows.append({"fixture_id": fixture_id, "workflow": workflow})
    return rows


def api_matrix(manifest: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    manifest = manifest or load_manifest()
    rows = []
    for fixture_id, entry in sorted(manifest["fixtures"].items()):
        for api_case in entry.get("api_cases", []):
            rows.append({"fixture_id": fixture_id, "api_case": api_case})
    return rows
