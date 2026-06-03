"""Source-agnostic schema objects for the synthetic core."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_SOURCES = {
    "synthetic_garmin_like",
    "synthetic_apple_health_like",
    "synthetic_google_health_fitbit_like",
    "synthetic_health_connect_like",
    "synthetic_strava_like",
    "synthetic_polar_like",
    "synthetic_medical_pdf_like",
    "synthetic_nutrition_image_like",
    "manual_note",
}

REQUIRED_FIXTURES = {
    "dtu_baseline_healthy_week",
    "dtu_accumulated_fatigue",
    "dtu_missing_data",
    "dtu_duplicate_import",
    "dtu_timezone_boundary",
    "dtu_greek_yoghurt_label_image",
    "dtu_cross_surface_recovery_handoff",
    "dtu_morning_report_normal",
    "dtu_evening_report_nutrition_gap",
    "dtu_late_high_fat_dinner_sleep_drop",
    "dtu_protein_distribution_recovery_improves",
    "dtu_weight_loss_plateau",
    "dtu_weight_loss_too_fast",
    "dtu_hard_session_suppressed_recovery",
    "dtu_contradictory_metrics",
    "dtu_nutrition_free_text",
    "dtu_morning_report_fatigue",
    "dtu_evening_report_recovery_setup",
    "dtu_weekly_review_progress",
    "dtu_proactive_suppressed_quiet_hours",
    "dtu_prior_recommendation_followup",
    "dtu_voice_continuation_as_synthetic_transcript",
    "dtu_deload_recovery",
    "dtu_nutrition_label_basis_ambiguity",
    "dtu_sleep_recovery_low_hrv_edge",
    "dtu_training_ramp_too_fast",
    "dtu_body_composition_recomp",
    "dtu_report_settings_quiet_depth",
    "dtu_weekly_report_suppressed_cooldown",
    "dtu_cross_surface_report_review",
    "dtu_synthetic_voice_followup_outcome",
    "dtu_malformed_missing_observed_at",
    "dtu_incomplete_source_payload",
    "dtu_evidence_orphan_ref",
    "dtu_api_unknown_workflow",
    "dtu_snapshot_export_roundtrip",
}

MISSION_007_REQUIRED_FIXTURES = {
    "dtu_baseline_healthy_week",
    "dtu_accumulated_fatigue",
    "dtu_missing_data",
    "dtu_duplicate_import",
    "dtu_timezone_boundary",
    "dtu_greek_yoghurt_label_image",
    "dtu_cross_surface_recovery_handoff",
    "dtu_morning_report_normal",
    "dtu_evening_report_nutrition_gap",
}


@dataclass(frozen=True)
class SourceRecord:
    id: str
    source: str
    source_record_id: str
    domain: str
    observed_at: str
    ingested_at: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class NormalizedFact:
    id: str
    domain: str
    observed_at: str
    value: dict[str, Any]
    provenance_refs: tuple[str, ...]


@dataclass(frozen=True)
class DerivedFact:
    id: str
    name: str
    value: Any
    provenance_refs: tuple[str, ...]


@dataclass(frozen=True)
class EvidencePack:
    id: str
    refs: tuple[str, ...]
    uncertainty: str


@dataclass(frozen=True)
class WorkflowRun:
    id: str
    workflow: str
    status: str
    recommendation_class: str
    evidence_pack: EvidencePack
    output: dict[str, Any]


@dataclass(frozen=True)
class ReportCandidate:
    id: str
    report_type: str
    sections: tuple[str, ...]
    evidence_pack: EvidencePack
    delivery_status: str
    output: dict[str, Any]


@dataclass(frozen=True)
class Fixture:
    path: Path
    fixture_id: str
    synthetic_only: bool
    timezone: str
    scenario: str
    sources: tuple[str, ...]
    source_records: tuple[SourceRecord, ...]
    normalized_facts: tuple[NormalizedFact, ...]
    expected: dict[str, Any]

    def records_by_domain(self, domain: str) -> list[SourceRecord]:
        return [record for record in self.source_records if record.domain == domain]

    def record_ids(self) -> set[str]:
        return {record.id for record in self.source_records}

    def fact_ids(self) -> set[str]:
        return {fact.id for fact in self.normalized_facts}
