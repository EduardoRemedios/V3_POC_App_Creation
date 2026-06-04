"""Synthetic manual import adapter registry and preview engine."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .garmin_bridge import (
    garmin_adapter_catalog,
    garmin_export_catalog,
    get_garmin_export,
    is_garmin_export,
    preview_garmin_export,
)


MANUAL_EXPORT_ROOT = Path("fixtures/manual_exports")
MANIFEST_PATH = MANUAL_EXPORT_ROOT / "manifest.json"
SYNTHETIC_SOURCE_PREFIX = "synthetic_manual_import"


@dataclass(frozen=True)
class Adapter:
    adapter_id: str
    label: str
    source_family: str
    file_kind: str
    domains: tuple[str, ...]
    description: str


ADAPTERS: dict[str, Adapter] = {
    "garmin_activity_csv": Adapter(
        "garmin_activity_csv",
        "Garmin-like activity CSV",
        "garmin_manual_export_candidate",
        "csv",
        ("activity",),
        "Synthetic activity rows with duration, distance, load, timezone, and duplicate detection.",
    ),
    "sleep_recovery_json": Adapter(
        "sleep_recovery_json",
        "Sleep/recovery JSON",
        "manual_sleep_recovery_export",
        "json",
        ("sleep", "hrv", "resting_heart_rate"),
        "Synthetic sleep, HRV, and resting-heart-rate records from a user-controlled export.",
    ),
    "weight_body_csv": Adapter(
        "weight_body_csv",
        "Weight/body CSV",
        "manual_body_export",
        "csv",
        ("body_weight", "body_composition"),
        "Synthetic weight and body-composition rows with unit ambiguity checks.",
    ),
    "nutrition_notes_json": Adapter(
        "nutrition_notes_json",
        "Nutrition notes JSON",
        "manual_nutrition_note_export",
        "json",
        ("nutrition_log",),
        "Synthetic free-text nutrition observations with quantity ambiguity checks.",
    ),
    "mixed_bundle_json": Adapter(
        "mixed_bundle_json",
        "Mixed manual bundle JSON",
        "manual_mixed_bundle_export",
        "json",
        ("activity", "sleep", "body_weight", "nutrition_log", "manual_note"),
        "Synthetic multi-domain manual bundle for cross-source mapping previews.",
    ),
}


def adapter_catalog() -> list[dict[str, Any]]:
    legacy = [
        {
            "adapter_id": adapter.adapter_id,
            "label": adapter.label,
            "source_family": adapter.source_family,
            "file_kind": adapter.file_kind,
            "domains": list(adapter.domains),
            "description": adapter.description,
            "synthetic_only": True,
        }
        for adapter in ADAPTERS.values()
    ]
    return legacy + garmin_adapter_catalog()


def load_manual_export_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def manual_export_catalog() -> list[dict[str, Any]]:
    manifest = load_manual_export_manifest()
    exports = []
    for entry in manifest["exports"]:
        path = Path(entry["path"])
        exports.append(
            {
                **entry,
                "exists": path.exists(),
                "sha256": file_sha256(path) if path.exists() else None,
            }
        )
    return exports + garmin_export_catalog()


def get_manual_export(export_id: str) -> dict[str, Any]:
    for entry in _legacy_manual_export_catalog():
        if entry["export_id"] == export_id:
            return entry
    if is_garmin_export(export_id):
        return get_garmin_export(export_id)
    raise KeyError(f"manual export not found: {export_id}")


def preview_manual_export(export_id: str) -> dict[str, Any]:
    if is_garmin_export(export_id):
        return preview_garmin_export(export_id)
    export = get_manual_export(export_id)
    adapter = ADAPTERS[export["adapter_id"]]
    path = Path(export["path"])
    raw_rows = _read_rows(path, adapter.file_kind)
    preview_rows = [_normalize_row(adapter, export_id, row, index) for index, row in enumerate(raw_rows, start=1)]
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
        "source_file": {
            "path": str(path),
            "sha256": file_sha256(path),
            "parser": adapter.file_kind,
        },
        "rows": preview_rows,
        "issues": issues,
        "conflicts": conflicts,
        "mappings": mappings,
        "summary": summary,
        "synthetic_only": True,
        "generated_at": now_utc(),
    }


def validate_manual_export_manifest() -> dict[str, Any]:
    manifest = load_manual_export_manifest()
    errors: list[str] = []
    exports = manifest.get("exports", [])
    export_ids = [entry.get("export_id") for entry in exports]
    if len(export_ids) != len(set(export_ids)):
        errors.append("duplicate export_id in manual export manifest")
    for entry in exports:
        path = Path(entry["path"])
        if not path.exists():
            errors.append(f"manual export path missing: {path}")
        if entry["adapter_id"] not in ADAPTERS:
            errors.append(f"unknown adapter_id: {entry['adapter_id']}")
        if not entry.get("expected"):
            errors.append(f"missing expected metadata: {entry['export_id']}")
    return {
        "valid": not errors,
        "errors": errors,
        "export_count": len(exports),
        "adapter_count": len(ADAPTERS),
        "synthetic_only": manifest.get("synthetic_only") is True,
    }


def _legacy_manual_export_catalog() -> list[dict[str, Any]]:
    manifest = load_manual_export_manifest()
    exports = []
    for entry in manifest["exports"]:
        path = Path(entry["path"])
        exports.append(
            {
                **entry,
                "exists": path.exists(),
                "sha256": file_sha256(path) if path.exists() else None,
            }
        )
    return exports


def session_id(export_id: str) -> str:
    return f"manual_import_{export_id}"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_rows(path: Path, file_kind: str) -> list[dict[str, Any]]:
    if file_kind == "csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("synthetic_only") is not True:
        raise ValueError(f"manual export JSON must be synthetic_only: {path}")
    return [dict(row) for row in payload.get("records", [])]


def _normalize_row(adapter: Adapter, export_id: str, row: dict[str, Any], row_index: int) -> dict[str, Any]:
    normalizers: dict[str, Callable[[dict[str, Any]], tuple[str, dict[str, Any]]]] = {
        "garmin_activity_csv": _normalize_activity,
        "sleep_recovery_json": _normalize_sleep,
        "weight_body_csv": _normalize_weight,
        "nutrition_notes_json": _normalize_nutrition,
        "mixed_bundle_json": _normalize_mixed,
    }
    domain, normalized = normalizers[adapter.adapter_id](row)
    source_record_id = row.get("record_id") or f"{export_id}_row_{row_index}"
    observed_at = str(row.get("observed_at", "") or "")
    return {
        "row_index": row_index,
        "source_record_id": source_record_id,
        "source": SYNTHETIC_SOURCE_PREFIX,
        "domain": domain,
        "observed_at": observed_at,
        "timezone": row.get("timezone") or "unknown",
        "raw": row,
        "normalized": normalized,
        "provenance": {
            "export_id": export_id,
            "adapter_id": adapter.adapter_id,
            "source_record_id": source_record_id,
            "synthetic_only": True,
        },
        "signature": _signature(domain, observed_at, normalized),
    }


def _normalize_activity(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    return (
        "activity",
        {
            "activity_type": row.get("activity_type"),
            "duration_min": _number(row.get("duration_min")),
            "distance_km": _number(row.get("distance_km")),
            "training_load": _number(row.get("load")),
            "unit_system": "metric",
        },
    )


def _normalize_sleep(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    return (
        "sleep",
        {
            "sleep_hours": _number(row.get("sleep_hours")),
            "hrv_rmssd_ms": _number(row.get("hrv_rmssd_ms")),
            "resting_hr_bpm": _number(row.get("resting_hr_bpm")),
        },
    )


def _normalize_weight(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    kg = _number(row.get("weight_kg"))
    lb = _number(row.get("weight_lb"))
    inferred_kg = round(lb / 2.20462, 2) if lb is not None else None
    return (
        "body_weight",
        {
            "weight_kg": kg if kg is not None else inferred_kg,
            "source_weight_kg": kg,
            "source_weight_lb": lb,
            "body_fat_percent": _number(row.get("body_fat_percent")),
            "unit_system": "mixed" if kg is not None and lb is not None else ("imperial" if lb is not None else "metric"),
        },
    )


def _normalize_nutrition(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    return (
        "nutrition_log",
        {
            "text": row.get("text", ""),
            "meal_type": row.get("meal_type", "unknown"),
            "quantity_status": "ambiguous" if _text_has_ambiguity(row.get("text", "")) else "usable_note",
        },
    )


def _normalize_mixed(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    domain = row.get("domain", "manual_note")
    if domain == "activity":
        _, normalized = _normalize_activity(row)
    elif domain == "sleep":
        _, normalized = _normalize_sleep(row)
    elif domain == "body_weight":
        _, normalized = _normalize_weight(row)
    elif domain == "nutrition_log":
        _, normalized = _normalize_nutrition(row)
    else:
        normalized = {"text": row.get("text", ""), "note_type": domain}
    return domain, normalized


def _validation_issues(adapter: Adapter, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    for row in rows:
        row_index = row["row_index"]
        raw = row["raw"]
        if not row["observed_at"]:
            issues.append(_issue(row_index, "error", "missing_observed_at", "observed_at", "Observed time is required."))
        elif "T" not in row["observed_at"]:
            issues.append(_issue(row_index, "error", "invalid_observed_at", "observed_at", "Observed time must be ISO-like."))
        if row["timezone"] == "UTC" and row["observed_at"].endswith("+00:00"):
            issues.append(_issue(row_index, "warning", "timezone_boundary", "timezone", "UTC export row may need local-date attribution."))
        signature = row["signature"]
        if signature in seen:
            issues.append(
                _issue(
                    row_index,
                    "warning",
                    "duplicate_candidate",
                    "record",
                    f"Duplicate candidate of row {seen[signature]}.",
                )
            )
        else:
            seen[signature] = row_index
        if adapter.adapter_id == "weight_body_csv":
            kg = _number(raw.get("weight_kg"))
            lb = _number(raw.get("weight_lb"))
            if kg is not None and lb is not None and abs(kg - (lb / 2.20462)) > 1.0:
                issues.append(_issue(row_index, "warning", "unit_conflict", "weight", "kg and lb values disagree."))
            if kg is None and lb is not None:
                issues.append(_issue(row_index, "warning", "unit_inferred", "weight_lb", "Converted lb to kg for preview."))
        if row["domain"] == "nutrition_log" and _text_has_ambiguity(row["normalized"].get("text", "")):
            issues.append(_issue(row_index, "warning", "quantity_ambiguous", "text", "Food quantity is approximate or unclear."))
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
                    "message": "Rows share the same domain, observed time, and normalized value signature.",
                }
            )
    for row in rows:
        normalized = row["normalized"]
        if normalized.get("unit_system") == "mixed":
            kg = normalized.get("source_weight_kg")
            lb = normalized.get("source_weight_lb")
            if kg is not None and lb is not None and abs(float(kg) - (float(lb) / 2.20462)) > 1.0:
                conflicts.append(
                    {
                        "conflict_type": "unit_conflict",
                        "signature": row["signature"],
                        "row_indexes": [row["row_index"]],
                        "message": "Weight kg/lb values conflict and require user review before real import.",
                    }
                )
    return conflicts


def _mapping_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mappings: list[dict[str, Any]] = []
    for row in rows:
        raw_keys = sorted(row["raw"])
        normalized_keys = sorted(row["normalized"])
        for key in raw_keys:
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
        "observed_at": "observed_at",
        "timezone": "timezone",
        "activity_type": "activity_type",
        "duration_min": "duration_min",
        "distance_km": "distance_km",
        "load": "training_load",
        "weight_kg": "weight_kg",
        "weight_lb": "weight_kg",
        "body_fat_percent": "body_fat_percent",
        "sleep_hours": "sleep_hours",
        "hrv_rmssd_ms": "hrv_rmssd_ms",
        "resting_hr_bpm": "resting_hr_bpm",
        "text": "text",
        "meal_type": "meal_type",
        "domain": "domain",
    }
    target = mapping.get(source_field, "ignored")
    if target in normalized_keys or target in {"source_record_id", "observed_at", "timezone", "domain"}:
        return target
    return "ignored"


def _transform_name(source_field: str, target: str) -> str:
    if source_field == "weight_lb" and target == "weight_kg":
        return "lb_to_kg"
    if source_field == "load":
        return "rename_load_to_training_load"
    if target == "ignored":
        return "not_imported"
    return "copy"


def _signature(domain: str, observed_at: str, normalized: dict[str, Any]) -> str:
    stable = json.dumps({"domain": domain, "observed_at": observed_at, "value": normalized}, sort_keys=True)
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]


def _issue(row_index: int, severity: str, issue_type: str, field: str, message: str) -> dict[str, Any]:
    return {
        "row_index": row_index,
        "severity": severity,
        "issue_type": issue_type,
        "field": field,
        "message": message,
    }


def _number(value: Any) -> float | int | None:
    if value is None or value == "":
        return None
    parsed = float(value)
    return int(parsed) if parsed.is_integer() else parsed


def _text_has_ambiguity(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in ("roughly", "approx", "unclear", "not weighed", "quantity unclear"))
