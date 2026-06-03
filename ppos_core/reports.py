"""Report candidate generation without live scheduling or delivery."""

from __future__ import annotations

from .primitives import assemble_evidence_refs, derive_summary, safety_check_text
from .schema import EvidencePack, Fixture, ReportCandidate


MORNING_SECTIONS = ("readiness", "key_evidence", "training_suggestion", "uncertainty", "next_action")
EVENING_SECTIONS = ("what_changed_today", "recovery_setup", "nutrition_observation", "data_gaps", "follow_up_state")


def morning_report_candidate(fixture: Fixture) -> ReportCandidate:
    summary = derive_summary(fixture)
    if summary.get("report_settings") and not fixture.records_by_domain("sleep"):
        recommendation = "settings_recorded"
    else:
        recommendation = (
            "reduce_intensity"
            if summary["recovery_status"] != "stable" or summary.get("morning_fatigue_flag")
            else "normal_training"
        )
    expected = fixture.expected.get("workflows", {}).get("morning_report_candidate", {})
    refs = assemble_evidence_refs(fixture, expected.get("required_evidence_refs", _morning_refs(fixture)))
    text = f"Morning readiness is {summary['recovery_status']}; training suggestion is {recommendation}."
    _check_report_safety(fixture, text)
    return ReportCandidate(
        id="report_morning_candidate",
        report_type="morning",
        sections=tuple(expected.get("sections", MORNING_SECTIONS)),
        evidence_pack=EvidencePack("evidence_morning_report", refs, "low"),
        delivery_status="candidate_not_delivered",
        output={"recommendation_class": recommendation, "summary": summary, "text": text},
    )


def evening_report_candidate(fixture: Fixture) -> ReportCandidate:
    summary = derive_summary(fixture)
    if summary.get("evening_recovery_setup"):
        recommendation = "recovery_setup_caution"
    elif summary.get("nutrition_gap"):
        recommendation = "ask_nutrition_followup"
    else:
        recommendation = "standard_evening_reflection"
    expected = fixture.expected.get("workflows", {}).get("evening_report_candidate", {})
    refs = assemble_evidence_refs(fixture, expected.get("required_evidence_refs", _evening_refs(fixture, summary)))
    clarification = expected.get("clarification")
    if summary.get("evening_recovery_setup"):
        text = "Evening report suggests a cautious recovery setup after heavy training."
    elif summary.get("nutrition_gap"):
        text = "Evening report notes a nutrition gap."
    else:
        text = "Evening report candidate is complete."
    _check_report_safety(fixture, text)
    return ReportCandidate(
        id="report_evening_candidate",
        report_type="evening",
        sections=tuple(expected.get("sections", EVENING_SECTIONS)),
        evidence_pack=EvidencePack("evidence_evening_report", refs, "moderate"),
        delivery_status="candidate_not_delivered",
        output={
            "recommendation_class": recommendation,
            "summary": summary,
            "clarification": clarification,
            "text": text,
        },
    )


def _morning_refs(fixture: Fixture) -> list[str]:
    refs = []
    for domain in ("sleep", "hrv", "resting_heart_rate", "manual_note"):
        records = fixture.records_by_domain(domain)
        if records:
            refs.append(records[-1].id)
    return refs or ["derived_missing_data"]


def _evening_refs(fixture: Fixture, summary: dict) -> list[str]:
    refs = [record.id for record in fixture.records_by_domain("activity")]
    if summary.get("nutrition_gap"):
        refs.append("derived_nutrition_gap")
    return refs or ["derived_missing_data"]


def _check_report_safety(fixture: Fixture, text: str) -> None:
    prohibited = fixture.expected.get("prohibited_claims", [])
    if not safety_check_text(text, prohibited):
        raise ValueError(f"report text violates prohibited claims for {fixture.fixture_id}")
