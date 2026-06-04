"""Garmin-shaped synthetic bridge fixtures for Mission 013."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


GARMIN_EXPORT_ROOT = Path("fixtures/garmin_exports")
GARMIN_MANIFEST_PATH = GARMIN_EXPORT_ROOT / "manifest.json"
GARMIN_SOURCE_LABEL = "synthetic_garmin_manual_export"
SYNTHETIC_LABEL = "SYNTHETIC_MISSION_013_GARMIN_SHAPE"


@dataclass(frozen=True)
class GarminAdapter:
    adapter_id: str
    label: str
    source_family: str
    file_kind: str
    domains: tuple[str, ...]
    description: str


GARMIN_ADAPTERS: dict[str, GarminAdapter] = {
    "garmin_bridge_activities_csv": GarminAdapter(
        "garmin_bridge_activities_csv",
        "Garmin activities CSV",
        "synthetic_garmin_manual_export",
        "csv",
        ("activity",),
        "Synthetic Garmin-shaped activity summaries with FIT/TCX/GPX/CSV family hints.",
    ),
    "garmin_bridge_sleep_json": GarminAdapter(
        "garmin_bridge_sleep_json",
        "Garmin sleep JSON",
        "synthetic_garmin_manual_export",
        "json",
        ("sleep",),
        "Synthetic Garmin-shaped sleep windows with local date, HRV, resting HR, and respiration.",
    ),
    "garmin_bridge_body_composition_csv": GarminAdapter(
        "garmin_bridge_body_composition_csv",
        "Garmin body composition CSV",
        "synthetic_garmin_manual_export",
        "csv",
        ("body_composition",),
        "Synthetic Garmin-shaped Index Scale/body-composition rows with unit conversion checks.",
    ),
    "garmin_bridge_wellness_json": GarminAdapter(
        "garmin_bridge_wellness_json",
        "Garmin wellness HRV/stress JSON",
        "synthetic_garmin_manual_export",
        "json",
        ("wellness", "hrv", "stress"),
        "Synthetic optional Mission 013 wellness rows selected by HDI-013-001 option_a.",
    ),
}


def garmin_adapter_catalog() -> list[dict[str, Any]]:
    return [
        {
            "adapter_id": adapter.adapter_id,
            "label": adapter.label,
            "source_family": adapter.source_family,
            "file_kind": adapter.file_kind,
            "domains": list(adapter.domains),
            "description": adapter.description,
            "synthetic_only": True,
        }
        for adapter in GARMIN_ADAPTERS.values()
    ]


def load_garmin_export_manifest() -> dict[str, Any]:
    return json.loads(GARMIN_MANIFEST_PATH.read_text(encoding="utf-8"))


def garmin_export_catalog() -> list[dict[str, Any]]:
    manifest = load_garmin_export_manifest()
    exports = []
    for entry in manifest["exports"]:
        path = Path(entry["path"])
        exports.append({**entry, "exists": path.exists(), "sha256": file_sha256(path) if path.exists() else None})
    return exports


def get_garmin_export(export_id: str) -> dict[str, Any]:
    for entry in garmin_export_catalog():
        if entry["export_id"] == export_id:
            return entry
    raise KeyError(f"Garmin export not found: {export_id}")


def is_garmin_export(export_id: str) -> bool:
    return any(entry["export_id"] == export_id for entry in load_garmin_export_manifest().get("exports", []))


def preview_garmin_export(export_id: str) -> dict[str, Any]:
    export = get_garmin_export(export_id)
    adapter = GARMIN_ADAPTERS[export["adapter_id"]]
    path = Path(export["path"])
    raw_rows = _read_rows(path, adapter.file_kind)
    preview_rows = [_normalize_row(adapter, export, row, index) for index, row in enumerate(raw_rows, start=1)]
    issues = _validation_issues(adapter, preview_rows)
    conflicts = _conflicts(preview_rows)
    mappings = _mapping_rows(preview_rows)
    summary = {
        "row_count": len(preview_rows),
        "issue_count": len(issues),
        "error_count": sum(1 for issue in issues if issue["severity"] == "error"),
        "warning_count": sum(1 for issue in issues if issue["severity"] == "warning"),
        "conflict_count": len(conflicts),
        "can_commit": not any(issue["severity"] == "error" for issue in issues),
    }
    return {
        "session_id": session_id(export_id),
        "export": export,
        "adapter": {
            "adapter_id": adapter.adapter_id,
            "label": adapter.label,
            "source_family": adapter.source_family,
            "domains": list(adapter.domains),
        },
        "source_file": {"path": str(path), "sha256": file_sha256(path), "parser": adapter.file_kind},
        "rows": preview_rows,
        "issues": issues,
        "conflicts": conflicts,
        "mappings": mappings,
        "summary": summary,
        "approval_defaults": load_garmin_export_manifest().get("hdi_selection", {}),
        "synthetic_only": True,
        "generated_at": now_utc(),
    }


def validate_garmin_export_manifest() -> dict[str, Any]:
    manifest = load_garmin_export_manifest()
    errors: list[str] = []
    exports = manifest.get("exports", [])
    export_ids = [entry.get("export_id") for entry in exports]
    if manifest.get("synthetic_only") is not True:
        errors.append("Garmin manifest must be synthetic_only")
    if manifest.get("source_label") != GARMIN_SOURCE_LABEL:
        errors.append("Garmin manifest source_label must be synthetic_garmin_manual_export")
    if len(export_ids) != len(set(export_ids)):
        errors.append("duplicate export_id in Garmin export manifest")
    families = {entry.get("family") for entry in exports}
    for required in {"activities", "sleep", "body_composition", "wellness_hrv_stress"}:
        if required not in families:
            errors.append(f"missing Garmin fixture family: {required}")
    for family in {"activities", "sleep", "body_composition"}:
        if not any(entry.get("family") == family and entry.get("case_type") == "clean" for entry in exports):
            errors.append(f"missing clean Garmin fixture for family: {family}")
        if not any(entry.get("family") == family and entry.get("case_type") == "edge" for entry in exports):
            errors.append(f"missing edge Garmin fixture for family: {family}")
    for entry in exports:
        path = Path(entry["path"])
        if not path.exists():
            errors.append(f"Garmin export path missing: {path}")
        if entry["adapter_id"] not in GARMIN_ADAPTERS:
            errors.append(f"unknown Garmin adapter_id: {entry['adapter_id']}")
        if entry.get("synthetic_label") != SYNTHETIC_LABEL:
            errors.append(f"missing synthetic label for Garmin export: {entry.get('export_id')}")
        if not entry.get("expected"):
            errors.append(f"missing expected metadata: {entry.get('export_id')}")
    return {
        "valid": not errors,
        "errors": errors,
        "export_count": len(exports),
        "adapter_count": len(GARMIN_ADAPTERS),
        "synthetic_only": manifest.get("synthetic_only") is True,
        "default_retention_posture": manifest.get("hdi_selection", {}).get("default_retention_posture"),
    }


def session_id(export_id: str) -> str:
    return f"garmin_import_{export_id}"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_rows(path: Path, file_kind: str) -> list[dict[str, Any]]:
    if file_kind == "csv":
        with path.open(newline="", encoding="utf-8") as handle:
            rows = [dict(row) for row in csv.DictReader(handle)]
        for row in rows:
            if row.get("synthetic_label") != SYNTHETIC_LABEL:
                raise ValueError(f"Garmin CSV fixture must carry synthetic label: {path}")
        return rows
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("synthetic_only") is not True or payload.get("synthetic_label") != SYNTHETIC_LABEL:
        raise ValueError(f"Garmin JSON fixture must be synthetic_only and labeled: {path}")
    return [dict(row) for row in payload.get("records", [])]


def _normalize_row(adapter: GarminAdapter, export: dict[str, Any], row: dict[str, Any], row_index: int) -> dict[str, Any]:
    normalizers: dict[str, Callable[[dict[str, Any]], tuple[str, str, dict[str, Any]]]] = {
        "garmin_bridge_activities_csv": _normalize_activity,
        "garmin_bridge_sleep_json": _normalize_sleep,
        "garmin_bridge_body_composition_csv": _normalize_body_composition,
        "garmin_bridge_wellness_json": _normalize_wellness,
    }
    domain, observed_at, normalized = normalizers[adapter.adapter_id](row)
    source_record_id = row.get("record_id") or f"{export['export_id']}_row_{row_index}"
    return {
        "row_index": row_index,
        "source_record_id": source_record_id,
        "source": GARMIN_SOURCE_LABEL,
        "domain": domain,
        "observed_at": observed_at,
        "timezone": row.get("timezone") or "unknown",
        "raw": row,
        "normalized": normalized,
        "provenance": {
            "export_id": export["export_id"],
            "adapter_id": adapter.adapter_id,
            "source_family": adapter.source_family,
            "source_record_id": source_record_id,
            "source_file_family": export.get("family"),
            "case_type": export.get("case_type"),
            "mapping_reference": "MISSION_013_GARMIN_EXPORT_SHAPE_RESEARCH.md",
            "synthetic_only": True,
        },
        "signature": _signature(domain, observed_at, normalized),
    }


def _normalize_activity(row: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    observed_at = str(row.get("start_time", "") or "")
    return (
        "activity",
        observed_at,
        {
            "activity_name": row.get("activity_name"),
            "activity_type": row.get("activity_type"),
            "start_time": observed_at,
            "duration_seconds": _number(row.get("duration_seconds")),
            "distance_meters": _number(row.get("distance_meters")),
            "calories_kcal": _number(row.get("calories_kcal")),
            "average_hr_bpm": _number(row.get("average_hr_bpm")),
            "training_load": _number(row.get("training_load")),
            "source_file_type": row.get("source_file_type"),
        },
    )


def _normalize_sleep(row: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    observed_at = str(row.get("sleep_start", "") or "")
    return (
        "sleep",
        observed_at,
        {
            "local_date": row.get("local_date"),
            "sleep_start": observed_at,
            "sleep_end": row.get("sleep_end"),
            "sleep_hours": _number(row.get("sleep_hours")),
            "sleep_score": _number(row.get("sleep_score")),
            "hrv_rmssd_ms": _number(row.get("hrv_rmssd_ms")),
            "resting_hr_bpm": _number(row.get("resting_hr_bpm")),
            "respiration_avg_brpm": _number(row.get("respiration_avg_brpm")),
        },
    )


def _normalize_body_composition(row: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    observed_at = str(row.get("measured_at", "") or "")
    kg = _number(row.get("weight_kg"))
    lb = _number(row.get("weight_lb"))
    inferred_kg = round(float(lb) / 2.20462, 2) if lb is not None else None
    return (
        "body_composition",
        observed_at,
        {
            "measured_at": observed_at,
            "weight_kg": kg if kg is not None else inferred_kg,
            "source_weight_kg": kg,
            "source_weight_lb": lb,
            "body_fat_percent": _number(row.get("body_fat_percent")),
            "muscle_mass_kg": _number(row.get("muscle_mass_kg")),
            "bone_mass_kg": _number(row.get("bone_mass_kg")),
            "unit_system": row.get("unit_system") or ("imperial" if lb is not None and kg is None else "metric"),
        },
    )


def _normalize_wellness(row: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    observed_at = str(row.get("measured_at", "") or "")
    return (
        "wellness",
        observed_at,
        {
            "measured_at": observed_at,
            "hrv_rmssd_ms": _number(row.get("hrv_rmssd_ms")),
            "stress_avg": _number(row.get("stress_avg")),
            "body_battery": _number(row.get("body_battery")),
            "resting_hr_bpm": _number(row.get("resting_hr_bpm")),
        },
    )


def _validation_issues(adapter: GarminAdapter, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    for row in rows:
        row_index = row["row_index"]
        raw = row["raw"]
        observed_at = row["observed_at"]
        if not observed_at:
            issues.append(_issue(row_index, "error", "missing_observed_at", _time_field(adapter), "Observed time is required."))
        elif "T" not in observed_at:
            issues.append(_issue(row_index, "error", "invalid_observed_at", _time_field(adapter), "Observed time must be ISO-like."))
        if row["timezone"] == "UTC" and observed_at.endswith("+00:00"):
            issues.append(_issue(row_index, "warning", "timezone_boundary", "timezone", "UTC export row may need local-date attribution."))
        signature = row["signature"]
        if signature in seen:
            issues.append(_issue(row_index, "warning", "duplicate_candidate", "record", f"Duplicate candidate of row {seen[signature]}."))
        else:
            seen[signature] = row_index
        for field in _required_numeric_fields(adapter.adapter_id):
            if _is_malformed_number(raw.get(field)):
                issues.append(_issue(row_index, "error", "malformed_numeric", field, f"{field} must be numeric when present."))
        if adapter.adapter_id == "garmin_bridge_body_composition_csv":
            kg = _number(raw.get("weight_kg"))
            lb = _number(raw.get("weight_lb"))
            if kg is not None and lb is not None and abs(float(kg) - (float(lb) / 2.20462)) > 1.0:
                issues.append(_issue(row_index, "warning", "unit_conflict", "weight", "kg and lb values disagree."))
            if kg is None and lb is not None:
                issues.append(_issue(row_index, "warning", "unit_inferred", "weight_lb", "Converted lb to kg for preview."))
    return issues


def _conflicts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    by_signature: dict[str, list[int]] = {}
    for row in rows:
        by_signature.setdefault(row["signature"], []).append(row["row_index"])
    for signature, indexes in by_signature.items():
        if len(indexes) > 1:
            conflicts.append(
                {
                    "conflict_type": "duplicate_candidate",
                    "signature": signature,
                    "row_indexes": indexes,
                    "message": "Rows share the same Garmin-shaped domain, observed time, and normalized value signature.",
                }
            )
    for row in rows:
        normalized = row["normalized"]
        kg = normalized.get("source_weight_kg")
        lb = normalized.get("source_weight_lb")
        if kg is not None and lb is not None and abs(float(kg) - (float(lb) / 2.20462)) > 1.0:
            conflicts.append(
                {
                    "conflict_type": "unit_conflict",
                    "signature": row["signature"],
                    "row_indexes": [row["row_index"]],
                    "message": "Garmin-shaped kg/lb body-composition values conflict and require review.",
                }
            )
    return conflicts


def _mapping_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mappings: list[dict[str, Any]] = []
    for row in rows:
        normalized_keys = sorted(row["normalized"])
        for key in sorted(row["raw"]):
            target = _target_field(key, normalized_keys)
            mappings.append(
                {
                    "row_index": row["row_index"],
                    "source_field": key,
                    "normalized_field": target,
                    "transform": _transform_name(key, target),
                    "confidence": "high" if target != "ignored" else "low",
                }
            )
    return mappings


def _target_field(source_field: str, normalized_keys: list[str]) -> str:
    mapping = {
        "record_id": "source_record_id",
        "synthetic_label": "ignored",
        "source_file_type": "source_file_type",
        "activity_name": "activity_name",
        "activity_type": "activity_type",
        "start_time": "start_time",
        "duration_seconds": "duration_seconds",
        "distance_meters": "distance_meters",
        "calories_kcal": "calories_kcal",
        "average_hr_bpm": "average_hr_bpm",
        "training_load": "training_load",
        "local_date": "local_date",
        "sleep_start": "sleep_start",
        "sleep_end": "sleep_end",
        "sleep_hours": "sleep_hours",
        "sleep_score": "sleep_score",
        "hrv_rmssd_ms": "hrv_rmssd_ms",
        "resting_hr_bpm": "resting_hr_bpm",
        "respiration_avg_brpm": "respiration_avg_brpm",
        "measured_at": "measured_at",
        "weight_kg": "weight_kg",
        "weight_lb": "weight_kg",
        "body_fat_percent": "body_fat_percent",
        "muscle_mass_kg": "muscle_mass_kg",
        "bone_mass_kg": "bone_mass_kg",
        "unit_system": "unit_system",
        "stress_avg": "stress_avg",
        "body_battery": "body_battery",
        "timezone": "timezone",
    }
    target = mapping.get(source_field, "ignored")
    if target in normalized_keys or target in {"source_record_id", "timezone"}:
        return target
    return "ignored"


def _transform_name(source_field: str, target: str) -> str:
    if source_field == "weight_lb" and target == "weight_kg":
        return "lb_to_kg"
    if target == "ignored":
        return "not_imported"
    return "copy"


def _signature(domain: str, observed_at: str, normalized: dict[str, Any]) -> str:
    stable = json.dumps({"domain": domain, "observed_at": observed_at, "value": normalized}, sort_keys=True)
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]


def _issue(row_index: int, severity: str, issue_type: str, field: str, message: str) -> dict[str, Any]:
    return {"row_index": row_index, "severity": severity, "issue_type": issue_type, "field": field, "message": message}


def _number(value: Any) -> float | int | None:
    if value is None or value == "":
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return int(parsed) if parsed.is_integer() else parsed


def _is_malformed_number(value: Any) -> bool:
    if value is None or value == "":
        return False
    try:
        float(value)
        return False
    except (TypeError, ValueError):
        return True


def _required_numeric_fields(adapter_id: str) -> tuple[str, ...]:
    return {
        "garmin_bridge_activities_csv": ("duration_seconds", "distance_meters", "calories_kcal", "average_hr_bpm", "training_load"),
        "garmin_bridge_sleep_json": ("sleep_hours", "sleep_score", "hrv_rmssd_ms", "resting_hr_bpm", "respiration_avg_brpm"),
        "garmin_bridge_body_composition_csv": ("weight_kg", "weight_lb", "body_fat_percent", "muscle_mass_kg", "bone_mass_kg"),
        "garmin_bridge_wellness_json": ("hrv_rmssd_ms", "stress_avg", "body_battery", "resting_hr_bpm"),
    }[adapter_id]


def _time_field(adapter: GarminAdapter) -> str:
    if adapter.adapter_id == "garmin_bridge_activities_csv":
        return "start_time"
    if adapter.adapter_id == "garmin_bridge_sleep_json":
        return "sleep_start"
    return "measured_at"

