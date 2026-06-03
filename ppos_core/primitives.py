"""Deterministic primitive functions over normalized synthetic fixtures."""

from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import Any

from .schema import DerivedFact, Fixture, SourceRecord


def derive_summary(fixture: Fixture) -> dict[str, Any]:
    duplicate_pairs = detect_duplicate_activity_candidates(fixture)
    canonical_activities = canonical_activity_records(fixture)
    load = sum(int(record.payload.get("load", 0)) for record in canonical_activities)
    sleep_avg = compute_sleep_average(fixture)
    missing = detect_missing_data(fixture)
    recovery = compute_recovery_status(fixture, load, sleep_avg, missing)
    nutrition = normalize_nutrition_label_values(fixture)
    continuity = compute_cross_surface_continuity(fixture)
    timezone = compute_timezone_attribution(fixture)
    nutrition_gap = detect_nutrition_gap(fixture)
    expanded = compute_expanded_signals(fixture)

    summary: dict[str, Any] = {
        "training_load_7d": load,
        "sleep_average_hours": sleep_avg,
        "missing_domains": missing,
        "recovery_status": recovery,
        "duplicate_activity_pairs": len(duplicate_pairs),
        "canonical_activity_count": len(canonical_activities),
        "nutrition_gap": nutrition_gap,
    }
    summary.update(nutrition)
    summary.update(continuity)
    summary.update(timezone)
    summary.update(expanded)
    if summary.get("contradictory_metrics"):
        summary["recovery_status"] = "conflicted"
    return summary


def derived_facts(fixture: Fixture) -> tuple[DerivedFact, ...]:
    summary = derive_summary(fixture)
    source_refs = tuple(record.id for record in fixture.source_records)
    facts = [
        DerivedFact("derived_training_load_7d", "training_load_7d", summary["training_load_7d"], source_refs),
        DerivedFact("derived_missing_data", "missing_domains", summary["missing_domains"], source_refs),
        DerivedFact("derived_recovery_status", "recovery_status", summary["recovery_status"], source_refs),
    ]
    if summary.get("duplicate_activity_pairs"):
        facts.append(
            DerivedFact(
                "derived_duplicate_activity_candidates",
                "duplicate_activity_pairs",
                summary["duplicate_activity_pairs"],
                source_refs,
            )
        )
    if "activity_local_date" in summary or "sleep_local_date" in summary:
        facts.append(DerivedFact("derived_timezone_attribution", "timezone_attribution", summary, source_refs))
    if "quantity_required" in summary:
        facts.append(DerivedFact("derived_nutrition_label", "nutrition_label", summary, source_refs))
    if summary.get("nutrition_gap"):
        facts.append(DerivedFact("derived_nutrition_gap", "nutrition_gap", True, source_refs))
    if summary.get("conversation_thread_count"):
        facts.append(DerivedFact("derived_cross_surface_continuity", "cross_surface_continuity", summary, source_refs))
    expanded_fact_map = {
        "late_meal_sleep_association": ("derived_sleep_cause_signal", "sleep_cause_signal"),
        "protein_distribution_pattern": ("derived_protein_timing_pattern", "protein_timing_pattern"),
        "weight_trend": ("derived_weight_trend", "weight_trend"),
        "rapid_weight_loss_caution": ("derived_rapid_weight_loss_caution", "rapid_weight_loss_caution"),
        "hard_session_suppression": ("derived_hard_session_suppression", "hard_session_suppression"),
        "contradictory_metrics": ("derived_contradictory_metrics", "contradictory_metrics"),
        "nutrition_free_text_needs_clarification": ("derived_nutrition_free_text", "nutrition_free_text"),
        "morning_fatigue_flag": ("derived_morning_fatigue_flag", "morning_fatigue_flag"),
        "evening_recovery_setup": ("derived_evening_recovery_setup", "evening_recovery_setup"),
        "deload_recovery_trend": ("derived_deload_recovery_trend", "deload_recovery_trend"),
        "quiet_hours_suppressed": ("derived_quiet_hours_suppressed", "quiet_hours_suppressed"),
        "prior_recommendation_followup_due": ("derived_prior_recommendation_followup", "prior_recommendation_followup"),
        "voice_transcript_continuity": ("derived_voice_transcript_continuity", "voice_transcript_continuity"),
        "recovery_edge_case": ("derived_recovery_edge_case", "recovery_edge_case"),
        "training_ramp_risk": ("derived_training_ramp_risk", "training_ramp_risk"),
        "body_composition_context": ("derived_body_composition_context", "body_composition_context"),
        "report_settings": ("derived_report_settings", "report_settings"),
        "cooldown_suppressed": ("derived_cooldown_suppressed", "cooldown_suppressed"),
        "followup_outcome": ("derived_followup_outcome", "followup_outcome"),
        "input_quality_issue": ("derived_input_quality_issue", "input_quality_issue"),
        "incomplete_payload": ("derived_incomplete_payload", "incomplete_payload"),
        "orphan_evidence_ref": ("derived_orphan_evidence_ref", "orphan_evidence_ref"),
        "snapshot_roundtrip": ("derived_snapshot_roundtrip", "snapshot_roundtrip"),
    }
    for key, (fact_id, name) in expanded_fact_map.items():
        if key in summary:
            facts.append(DerivedFact(fact_id, name, summary[key], source_refs))
    return tuple(facts)


def canonical_activity_records(fixture: Fixture) -> list[SourceRecord]:
    seen: set[tuple[Any, ...]] = set()
    canonical: list[SourceRecord] = []
    for record in fixture.records_by_domain("activity"):
        key = _activity_key(record)
        if key in seen:
            continue
        seen.add(key)
        canonical.append(record)
    return canonical


def detect_duplicate_activity_candidates(fixture: Fixture) -> list[tuple[str, str]]:
    activities = fixture.records_by_domain("activity")
    pairs: list[tuple[str, str]] = []
    for index, left in enumerate(activities):
        for right in activities[index + 1 :]:
            if _activity_key(left) == _activity_key(right):
                pairs.append((left.id, right.id))
    return pairs


def compute_sleep_average(fixture: Fixture) -> float | None:
    sleeps = [record.payload.get("sleep_hours") for record in fixture.records_by_domain("sleep")]
    values = [float(value) for value in sleeps if value is not None]
    if not values:
        return None
    return round(mean(values), 2)


def detect_missing_data(fixture: Fixture) -> list[str]:
    domains = {record.domain for record in fixture.source_records}
    if "sleep" in domains:
        return []
    missing = []
    for required in ("sleep", "hrv", "resting_heart_rate"):
        if required not in domains:
            missing.append(required)
    return missing


def compute_recovery_status(
    fixture: Fixture, training_load: int, sleep_average_hours: float | None, missing_domains: list[str]
) -> str:
    if missing_domains:
        return "uncertain_missing_data"
    latest_hrv = _latest(fixture.records_by_domain("hrv"))
    latest_rhr = _latest(fixture.records_by_domain("resting_heart_rate"))
    hrv_suppressed = False
    rhr_elevated = False
    if latest_hrv:
        hrv_suppressed = latest_hrv.payload.get("rmssd_ms", 0) <= latest_hrv.payload.get("baseline_ms", 0) - 10
    if latest_rhr:
        rhr_elevated = latest_rhr.payload.get("bpm", 0) >= latest_rhr.payload.get("baseline_bpm", 0) + 5
    short_sleep = sleep_average_hours is not None and sleep_average_hours < 6.75
    if training_load >= 300 and short_sleep and hrv_suppressed and rhr_elevated:
        return "fatigue_risk"
    return "stable"


def compute_timezone_attribution(fixture: Fixture) -> dict[str, str]:
    output: dict[str, str] = {}
    activity = _latest(fixture.records_by_domain("activity"))
    sleep = _latest(fixture.records_by_domain("sleep"))
    if activity and activity.payload.get("ended_at"):
        output["activity_local_date"] = _date_part(activity.observed_at)
    if sleep and sleep.payload.get("ended_at"):
        output["sleep_local_date"] = _date_part(sleep.payload["ended_at"])
    return output


def normalize_nutrition_label_values(fixture: Fixture) -> dict[str, Any]:
    extraction = _latest(fixture.records_by_domain("nutrition_extraction"))
    if not extraction:
        return {}
    nutrients = extraction.payload.get("nutrients", {})
    known = set(nutrients)
    return {
        "nutrition_basis": extraction.payload.get("basis"),
        "quantity_required": extraction.payload.get("quantity_consumed") is None,
        "invented_nutrients": sorted(known - set(nutrients)),
        "nutrition_product": extraction.payload.get("product"),
        "nutrition_confidence": extraction.payload.get("confidence"),
    }


def compute_cross_surface_continuity(fixture: Fixture) -> dict[str, int]:
    thread_ids = set()
    intent_ids = set()
    surfaces = set()
    for record in fixture.source_records:
        payload = record.payload
        if "thread_id" in payload:
            thread_ids.add(payload["thread_id"])
        if "intent_id" in payload:
            intent_ids.add(payload["intent_id"])
        if "surface" in payload:
            surfaces.add(payload["surface"])
    if not thread_ids and not intent_ids and not surfaces:
        return {}
    return {
        "conversation_thread_count": len(thread_ids),
        "intent_session_count": len(intent_ids),
        "surface_count": len(surfaces),
    }


def detect_nutrition_gap(fixture: Fixture) -> bool:
    has_activity = bool(fixture.records_by_domain("activity"))
    has_nutrition = bool(fixture.records_by_domain("nutrition_log") or fixture.records_by_domain("nutrition_extraction"))
    mentions_missing_meal = any(
        "no meal details" in str(record.payload.get("note", "")).lower() for record in fixture.records_by_domain("manual_note")
    )
    return has_activity and not has_nutrition and mentions_missing_meal


def compute_expanded_signals(fixture: Fixture) -> dict[str, Any]:
    output: dict[str, Any] = {}
    output.update(_sleep_cause_signals(fixture))
    output.update(_protein_timing_signals(fixture))
    output.update(_weight_signals(fixture))
    output.update(_nutrition_free_text_signals(fixture))
    output.update(_load_recovery_signals(fixture))
    output.update(_conversation_signals(fixture))
    output.update(_ambient_signals(fixture))
    output.update(_quality_and_audit_signals(fixture))
    return output


def _sleep_cause_signals(fixture: Fixture) -> dict[str, Any]:
    meals = [record for record in fixture.records_by_domain("nutrition_log") if record.payload.get("timing") == "late"]
    if not meals:
        return {}
    sleeps = sorted(fixture.records_by_domain("sleep"), key=lambda record: record.observed_at)
    if len(sleeps) < 2:
        return {}
    poor = min(sleeps, key=lambda record: float(record.payload.get("efficiency", 1)))
    baseline_values = [
        float(record.payload.get("sleep_hours", 0))
        for record in sleeps
        if record.id != poor.id and float(record.payload.get("efficiency", 1)) >= 0.85
    ]
    if not baseline_values:
        return {}
    drop = round(mean(baseline_values) - float(poor.payload.get("sleep_hours", 0)), 1)
    if drop <= 0:
        return {}
    return {
        "late_meal_sleep_association": True,
        "sleep_drop_hours": drop,
    }


def _protein_timing_signals(fixture: Fixture) -> dict[str, Any]:
    distributions = [record.payload.get("protein_distribution") for record in fixture.records_by_domain("nutrition_log")]
    if "dinner_concentrated" in distributions and "distributed" in distributions:
        return {"protein_distribution_pattern": "distributed_improved"}
    return {}


def _weight_signals(fixture: Fixture) -> dict[str, Any]:
    weights = sorted(fixture.records_by_domain("weight"), key=lambda record: record.observed_at)
    if len(weights) < 2:
        return {}
    first = float(weights[0].payload["weight_kg"])
    latest = float(weights[-1].payload["weight_kg"])
    change = round(latest - first, 1)
    output: dict[str, Any] = {"weight_change_kg": change}
    if change <= -1.5:
        output["weight_trend"] = "rapid_loss"
        output["rapid_weight_loss_caution"] = True
    elif abs(change) <= 0.3:
        output["weight_trend"] = "plateau"
    else:
        output["weight_trend"] = "changing"
    precision = _latest(fixture.records_by_domain("nutrition_log"))
    if precision and precision.payload.get("precision"):
        output["nutrition_precision"] = precision.payload["precision"]
    if any(record.payload.get("body_composition_signal") == "recomp" for record in fixture.records_by_domain("manual_note")):
        output["body_composition_context"] = "stable_weight_waist_improved"
        output["weight_trend"] = "body_recomp_context"
    return output


def _nutrition_free_text_signals(fixture: Fixture) -> dict[str, Any]:
    for record in fixture.records_by_domain("nutrition_log"):
        if record.payload.get("precision") == "free_text" or record.payload.get("quantity") is None:
            return {"nutrition_free_text_needs_clarification": True}
    return {}


def _load_recovery_signals(fixture: Fixture) -> dict[str, Any]:
    latest_hrv = _latest(fixture.records_by_domain("hrv"))
    latest_rhr = _latest(fixture.records_by_domain("resting_heart_rate"))
    hrv_suppressed = bool(
        latest_hrv and latest_hrv.payload.get("rmssd_ms", 0) <= latest_hrv.payload.get("baseline_ms", 0) - 10
    )
    rhr_elevated = bool(
        latest_rhr and latest_rhr.payload.get("bpm", 0) >= latest_rhr.payload.get("baseline_bpm", 0) + 5
    )
    output: dict[str, Any] = {}
    hard_activity = any(
        record.payload.get("intensity") == "hard" or int(record.payload.get("load", 0)) >= 140
        for record in fixture.records_by_domain("activity")
    )
    if hard_activity and hrv_suppressed and rhr_elevated:
        output["hard_session_suppression"] = True
    subjective_good = any(
        record.payload.get("subjective_readiness") == "good" for record in fixture.records_by_domain("manual_note")
    )
    if subjective_good and hrv_suppressed and rhr_elevated:
        output["contradictory_metrics"] = True
    subjective_low = any(
        record.payload.get("subjective_readiness") == "low" for record in fixture.records_by_domain("manual_note")
    )
    if subjective_low and hrv_suppressed and rhr_elevated:
        output["recovery_edge_case"] = "adequate_sleep_low_hrv"
    sleep_avg = compute_sleep_average(fixture)
    if sleep_avg is not None and sleep_avg < 6.5 and hrv_suppressed and rhr_elevated:
        output["morning_fatigue_flag"] = True
    prior_load = sum(
        int(record.payload.get("load", 0))
        for record in fixture.records_by_domain("activity")
        if record.payload.get("week") == "prior"
    )
    deload_load = sum(
        int(record.payload.get("load", 0))
        for record in fixture.records_by_domain("activity")
        if record.payload.get("week") == "deload"
    )
    hrv_values = sorted(
        [record.payload.get("rmssd_ms") for record in fixture.records_by_domain("hrv") if record.payload.get("rmssd_ms")],
    )
    if prior_load and deload_load and deload_load < prior_load and len(hrv_values) >= 2 and hrv_values[-1] > hrv_values[0]:
        output["deload_recovery_trend"] = "improving_after_deload"
        output["weekly_review_progress"] = True
    current_load = sum(
        int(record.payload.get("load", 0))
        for record in fixture.records_by_domain("activity")
        if record.payload.get("week") == "current"
    )
    if prior_load and current_load and current_load >= prior_load * 3:
        output["training_ramp_risk"] = "ramp_too_fast"
    return output


def _conversation_signals(fixture: Fixture) -> dict[str, Any]:
    messages = fixture.records_by_domain("conversation_message")
    has_voice_transcript = any(
        record.payload.get("input_mode") == "synthetic_voice_transcript" for record in messages
    )
    if not has_voice_transcript:
        return {}
    thread_ids = {record.payload.get("thread_id") for record in messages}
    intent_ids = {record.payload.get("intent_id") for record in messages}
    if len(thread_ids) == 1 and len(intent_ids) == 1:
        return {"voice_transcript_continuity": True}
    return {}


def _ambient_signals(fixture: Fixture) -> dict[str, Any]:
    output: dict[str, Any] = {}
    if any(record.payload.get("evening_context") == "recovery_setup" for record in fixture.records_by_domain("manual_note")):
        output["evening_recovery_setup"] = True
    pref = _latest(fixture.records_by_domain("report_preferences"))
    event = _latest(fixture.records_by_domain("surface_event"))
    if pref and event and event.payload.get("event") == "proactive_candidate_detected":
        event_time = event.observed_at[11:16]
        start = pref.payload.get("quiet_hours_start", "21:30")
        end = pref.payload.get("quiet_hours_end", "07:30")
        if event_time >= start or event_time <= end:
            output["quiet_hours_suppressed"] = True
            output["proactive_delivery_status"] = "suppressed_quiet_hours"
        if event.payload.get("cooldown_state") == "inside_window":
            output["cooldown_suppressed"] = True
            output["proactive_delivery_status"] = "suppressed_cooldown"
    if pref:
        output["report_settings"] = {
            "morning_depth": pref.payload.get("morning_depth", "standard"),
            "weekly_depth": pref.payload.get("weekly_depth", "standard"),
            "quiet_hours_start": pref.payload.get("quiet_hours_start", "21:30"),
            "quiet_hours_end": pref.payload.get("quiet_hours_end", "07:30"),
        }
    recommendation = _latest(fixture.records_by_domain("recommendation"))
    if recommendation and recommendation.payload.get("follow_up_due"):
        sleeps = sorted(fixture.records_by_domain("sleep"), key=lambda record: record.observed_at)
        output["prior_recommendation_followup_due"] = True
        if len(sleeps) >= 2 and float(sleeps[-1].payload.get("sleep_hours", 0)) > float(
            sleeps[0].payload.get("sleep_hours", 0)
        ):
            output["sleep_followup_direction"] = "improved_with_uncertainty"
    if output.get("prior_recommendation_followup_due") and any(
        "did the" in record.payload.get("text", "").lower() for record in fixture.records_by_domain("conversation_message")
    ):
        output["followup_outcome"] = "outcome_recorded_with_uncertainty"
    return output


def _quality_and_audit_signals(fixture: Fixture) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for record in fixture.source_records:
        quality = record.payload.get("input_quality")
        if quality:
            output["input_quality_issue"] = quality
        if quality == "incomplete_payload":
            output["incomplete_payload"] = True
        if record.payload.get("orphan_ref"):
            output["orphan_evidence_ref"] = record.payload["orphan_ref"]
        if record.payload.get("snapshot_case") == "roundtrip":
            output["snapshot_roundtrip"] = True
    return output


def assemble_evidence_refs(fixture: Fixture, refs: list[str]) -> tuple[str, ...]:
    source_ids = fixture.record_ids()
    derived_ids = {fact.id for fact in derived_facts(fixture)}
    missing = [ref for ref in refs if ref not in source_ids and ref not in derived_ids]
    if missing:
        raise ValueError(f"unknown evidence refs for {fixture.fixture_id}: {missing}")
    return tuple(refs)


def safety_check_text(text: str, prohibited_claims: list[str]) -> bool:
    lowered = text.lower()
    return not any(claim.lower() in lowered for claim in prohibited_claims)


def _activity_key(record: SourceRecord) -> tuple[Any, ...]:
    payload = record.payload
    if payload.get("file_hash"):
        return ("file_hash", payload["file_hash"])
    distance = payload.get("distance_km", 0)
    if distance is None:
        distance = 0
    return (
        "activity",
        _date_part(record.observed_at),
        payload.get("duration_min"),
        round(float(distance), 1),
        payload.get("sport"),
    )


def _latest(records: list[SourceRecord]) -> SourceRecord | None:
    if not records:
        return None
    return sorted(records, key=lambda record: record.observed_at)[-1]


def _date_part(value: str) -> str:
    return datetime.fromisoformat(value).date().isoformat()
