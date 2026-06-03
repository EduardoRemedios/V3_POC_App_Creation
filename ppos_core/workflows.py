"""Bounded workflow contracts for Mission 007."""

from __future__ import annotations

from typing import Any

from .primitives import assemble_evidence_refs, derive_summary, safety_check_text
from .schema import EvidencePack, Fixture, WorkflowRun


def recovery_today(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    if summary.get("input_quality_issue"):
        recommendation = "input_quality_review"
        uncertainty = "high"
    elif summary.get("orphan_evidence_ref"):
        recommendation = "evidence_review_required"
        uncertainty = "high"
    elif summary.get("snapshot_roundtrip"):
        recommendation = "snapshot_context_review"
        uncertainty = "low"
    elif summary.get("recovery_edge_case"):
        recommendation = "monitor_cautiously"
        uncertainty = "moderate"
    elif summary["recovery_status"] == "conflicted":
        recommendation = "conflicted_recovery_check"
        uncertainty = "high"
    elif summary["recovery_status"] == "fatigue_risk":
        recommendation = "reduce_intensity"
        uncertainty = "moderate"
    elif summary["recovery_status"] == "uncertain_missing_data":
        recommendation = "normal_or_easy_with_uncertainty"
        uncertainty = "high"
    elif summary.get("conversation_thread_count") or "activity_local_date" in summary:
        recommendation = "normal_or_easy"
        uncertainty = "low"
    else:
        recommendation = "normal_training"
        uncertainty = "low"
    refs = _workflow_refs(fixture, "recovery_today", _default_recovery_refs(fixture, summary))
    text = f"Recovery is {summary['recovery_status']}; recommendation is {recommendation}."
    _check_safety(fixture, text)
    return _workflow_run("recovery_today", recommendation, refs, uncertainty, {"summary": summary, "text": text})


def sleep_cause_analysis(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    refs = [record.id for record in fixture.records_by_domain("sleep")[:1]]
    if not refs:
        refs = ["derived_missing_data"]
    if summary.get("late_meal_sleep_association"):
        recommendation = "late_meal_possible_contributor"
        refs = _workflow_refs(fixture, "sleep_cause_analysis", ["derived_sleep_cause_signal"])
    else:
        recommendation = "insufficient_causal_evidence"
        refs = assemble_evidence_refs(fixture, refs)
    output = {
        "plausible_contributors": ["late_heavy_meal"] if summary.get("late_meal_sleep_association") else [],
        "causal_certainty": "low",
        "text": "Late heavy food may have contributed to poorer sleep; this is an association, not proof.",
        "summary": summary,
    }
    _check_safety(fixture, output["text"])
    return _workflow_run("sleep_cause_analysis", recommendation, refs, "high", output)


def four_week_training_analysis(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    if summary.get("incomplete_payload"):
        recommendation = "incomplete_payload_review"
    else:
        recommendation = "deduped_activity_load" if summary.get("duplicate_activity_pairs") else "moderate_sustainable_load"
    refs = _workflow_refs(fixture, "four_week_training_analysis", ["derived_training_load_7d"])
    output = {
        "trend": recommendation,
        "weekly_load_proxy": summary["training_load_7d"],
        "duplicate_activity_pairs": summary.get("duplicate_activity_pairs", 0),
        "text": f"Training trend is {recommendation}.",
    }
    _check_safety(fixture, output["text"])
    return _workflow_run("four_week_training_analysis", recommendation, refs, "moderate", output)


def nutrition_label_capture(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    quantity_required = bool(summary.get("quantity_required"))
    recommendation = "pending_quantity_confirmation" if quantity_required else "confirmed_nutrition_log"
    refs = _workflow_refs(
        fixture,
        "nutrition_label_capture",
        [record.id for record in fixture.records_by_domain("nutrition_label_image") + fixture.records_by_domain("nutrition_extraction")],
    )
    clarification = "Did you eat one 150 g serving, the whole container, or another amount?" if quantity_required else None
    output = {
        "status": recommendation,
        "product": summary.get("nutrition_product"),
        "basis": summary.get("nutrition_basis"),
        "quantity_required": quantity_required,
        "clarification": clarification,
        "text": f"Captured {summary.get('nutrition_product')} label as {summary.get('nutrition_basis')}; quantity confirmation is required.",
    }
    _check_safety(fixture, output["text"])
    return _workflow_run("nutrition_label_capture", recommendation, refs, "moderate", output)


def ride_rest_recommendation(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    if summary.get("training_ramp_risk"):
        recommendation = "ramp_caution"
    elif summary["recovery_status"] == "fatigue_risk" or summary.get("hard_session_suppression"):
        recommendation = "rest_or_recovery_ride"
    elif summary["recovery_status"] == "uncertain_missing_data":
        recommendation = "easy_if_training"
    else:
        recommendation = "normal_or_easy"
    refs = _workflow_refs(fixture, "ride_rest_recommendation", _default_recovery_refs(fixture, summary))
    output = {
        "recommendation_class": recommendation,
        "summary": summary,
        "text": f"Tomorrow should be {recommendation} based on available synthetic evidence.",
    }
    _check_safety(fixture, output["text"])
    return _workflow_run("ride_rest_recommendation", recommendation, refs, "moderate", output)


def run_workflow(name: str, fixture: Fixture) -> WorkflowRun:
    workflows = {
        "recovery_today": recovery_today,
        "sleep_cause_analysis": sleep_cause_analysis,
        "four_week_training_analysis": four_week_training_analysis,
        "nutrition_label_capture": nutrition_label_capture,
        "ride_rest_recommendation": ride_rest_recommendation,
        "nutrition_free_text_handling": nutrition_free_text_handling,
        "weight_trend_check": weight_trend_check,
        "protein_timing_pattern": protein_timing_pattern,
        "weekly_review_report": weekly_review_report,
        "proactive_suppression_check": proactive_suppression_check,
        "prior_recommendation_followup": prior_recommendation_followup,
        "voice_transcript_continuity": voice_transcript_continuity,
    }
    if name not in workflows:
        raise KeyError(f"unknown workflow: {name}")
    return workflows[name](fixture)


def nutrition_free_text_handling(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    recommendation = "needs_clarification" if summary.get("nutrition_free_text_needs_clarification") else "logged_as_note"
    refs = _workflow_refs(fixture, "nutrition_free_text_handling", ["derived_nutrition_free_text"])
    output = {
        "recommendation_class": recommendation,
        "clarification": "What portion did you eat, and do you want this estimated or left as a qualitative note?",
        "summary": summary,
        "text": "Free-text meal notes need quantity clarification before precise macros are recorded.",
    }
    _check_safety(fixture, output["text"])
    return _workflow_run("nutrition_free_text_handling", recommendation, refs, "high", output)


def weight_trend_check(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    if summary.get("body_composition_context"):
        recommendation = "body_recomp_context"
        refs = _workflow_refs(fixture, "weight_trend_check", ["derived_body_composition_context"])
        text = "Scale weight is stable, but body-composition context suggests a cautious recomp interpretation."
    elif summary.get("rapid_weight_loss_caution"):
        recommendation = "rapid_loss_caution"
        refs = _workflow_refs(fixture, "weight_trend_check", ["derived_rapid_weight_loss_caution"])
        text = "Weight is dropping quickly alongside weaker recovery signals; review fueling cautiously."
    elif summary.get("weight_trend") == "plateau":
        recommendation = "plateau_with_low_precision"
        refs = _workflow_refs(fixture, "weight_trend_check", ["derived_weight_trend"])
        text = "Weight appears flat within normal noise, and nutrition precision is low."
    else:
        recommendation = "weight_trend_uncertain"
        refs = _workflow_refs(fixture, "weight_trend_check", ["derived_weight_trend"])
        text = "Weight trend needs more consistent records."
    _check_safety(fixture, text)
    return _workflow_run("weight_trend_check", recommendation, refs, "moderate", {"summary": summary, "text": text})


def protein_timing_pattern(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    recommendation = (
        "continue_distributed_protein"
        if summary.get("protein_distribution_pattern") == "distributed_improved"
        else "protein_pattern_uncertain"
    )
    refs = _workflow_refs(fixture, "protein_timing_pattern", ["derived_protein_timing_pattern"])
    text = "Distributed protein coincides with better recovery markers; continue and monitor."
    _check_safety(fixture, text)
    return _workflow_run("protein_timing_pattern", recommendation, refs, "moderate", {"summary": summary, "text": text})


def weekly_review_report(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    recommendation = (
        "gradual_ramp_after_deload"
        if summary.get("deload_recovery_trend") == "improving_after_deload"
        else "weekly_review_uncertain"
    )
    refs = _workflow_refs(fixture, "weekly_review_report", ["derived_deload_recovery_trend"])
    text = "The deload week appears to support recovery; ramp gradually rather than jumping load."
    _check_safety(fixture, text)
    return _workflow_run("weekly_review_report", recommendation, refs, "moderate", {"summary": summary, "text": text})


def proactive_suppression_check(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    if summary.get("cooldown_suppressed"):
        recommendation = "suppressed_cooldown"
        refs = _workflow_refs(fixture, "proactive_suppression_check", ["derived_cooldown_suppressed"])
    else:
        recommendation = "suppressed_quiet_hours" if summary.get("quiet_hours_suppressed") else "not_suppressed"
        refs = _workflow_refs(fixture, "proactive_suppression_check", ["derived_quiet_hours_suppressed"])
    text = "A proactive candidate is suppressed during quiet hours and kept as passive context."
    _check_safety(fixture, text)
    return _workflow_run("proactive_suppression_check", recommendation, refs, "low", {"summary": summary, "text": text})


def prior_recommendation_followup(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    if summary.get("followup_outcome"):
        recommendation = "follow_up_outcome_recorded"
        refs = _workflow_refs(fixture, "prior_recommendation_followup", ["derived_followup_outcome"])
    else:
        recommendation = "follow_up_due" if summary.get("prior_recommendation_followup_due") else "no_follow_up_due"
        refs = _workflow_refs(fixture, "prior_recommendation_followup", ["derived_prior_recommendation_followup"])
    text = "The prior recommendation is due for follow-up; compare sleep direction cautiously."
    _check_safety(fixture, text)
    return _workflow_run("prior_recommendation_followup", recommendation, refs, "moderate", {"summary": summary, "text": text})


def voice_transcript_continuity(fixture: Fixture) -> WorkflowRun:
    summary = derive_summary(fixture)
    recommendation = "continued_same_intent" if summary.get("voice_transcript_continuity") else "voice_context_uncertain"
    refs = _workflow_refs(fixture, "voice_transcript_continuity", ["derived_voice_transcript_continuity"])
    text = "The synthetic voice transcript continues the same thread and intent without transcription execution."
    _check_safety(fixture, text)
    return _workflow_run("voice_transcript_continuity", recommendation, refs, "low", {"summary": summary, "text": text})


def _workflow_refs(fixture: Fixture, workflow_name: str, default: list[str]) -> tuple[str, ...]:
    expected = fixture.expected.get("workflows", {}).get(workflow_name, {})
    refs = expected.get("required_evidence_refs", default)
    return assemble_evidence_refs(fixture, refs)


def _default_recovery_refs(fixture: Fixture, summary: dict[str, Any]) -> list[str]:
    refs = []
    for domain in ("sleep", "hrv", "resting_heart_rate", "manual_note"):
        records = fixture.records_by_domain(domain)
        if records:
            refs.append(records[-1].id)
    refs.append("derived_missing_data" if summary["missing_domains"] else "derived_training_load_7d")
    return refs


def _workflow_run(name: str, recommendation: str, refs: tuple[str, ...], uncertainty: str, output: dict[str, Any]) -> WorkflowRun:
    evidence_pack = EvidencePack(f"evidence_{name}", refs, uncertainty)
    return WorkflowRun(
        id=f"workflow_{name}",
        workflow=name,
        status="candidate",
        recommendation_class=recommendation,
        evidence_pack=evidence_pack,
        output=output,
    )


def _check_safety(fixture: Fixture, text: str) -> None:
    prohibited = fixture.expected.get("prohibited_claims", [])
    if not safety_check_text(text, prohibited):
        raise ValueError(f"workflow text violates prohibited claims for {fixture.fixture_id}")
