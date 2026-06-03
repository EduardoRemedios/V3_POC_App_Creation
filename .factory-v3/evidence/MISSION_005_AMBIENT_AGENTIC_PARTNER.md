# Mission 005 Ambient Agentic Partner

## Status
COMPLETE

## Mission
`.factory-v3/missions/MISSION_005_AMBIENT_AGENTIC_PARTNER.md`

## Date
2026-06-03

## Core Frame
The Personal Performance OS should be a persistent, always-on, ambient agentic partner.

It should not be only:
- a dashboard,
- a reactive chatbot,
- a Garmin clone,
- a report generator,
- a static health database.

It should maintain context over time and engage when useful.

## Product Behavior
The agent should:
- remember goals, preferences, constraints, active experiments, prior recommendations, and follow-up outcomes,
- monitor synthetic or later approved real data for meaningful trends,
- prepare morning and evening reports,
- produce proactive observations only when evidence justifies them,
- ask brief clarification questions when needed,
- avoid noisy or repetitive messaging,
- stay explainable and evidence-backed,
- respect quiet hours, user preferences, and opt-out settings,
- avoid diagnosis, treatment advice, or regulated medical claims.

## Ambient Routines

### Morning Report
Purpose:
- help the user decide how to approach the day.

Inputs:
- last night's sleep,
- HRV/resting heart rate/recovery metrics,
- recent training load,
- subjective notes,
- planned training or active goals,
- unresolved follow-ups,
- missing-data flags.

Required sections:
- readiness summary,
- key evidence,
- today's training suggestion,
- recovery/nutrition note if relevant,
- uncertainty or missing-data note,
- one suggested next action.

Prohibited behavior:
- exact readiness scoring without supporting data,
- hard-session recommendation during sustained fatigue without caveat,
- medical diagnosis,
- long noisy report when nothing changed.

### Evening Report
Purpose:
- close the day and prepare tomorrow.

Inputs:
- completed activities,
- nutrition logs or missing nutrition,
- recovery trend,
- sleep setup factors,
- weight/body-composition trend if relevant,
- active experiments,
- morning recommendation outcome.

Required sections:
- what changed today,
- recovery setup for tomorrow,
- nutrition observation if supported,
- data gaps or clarification questions,
- follow-up state.

Prohibited behavior:
- guilt or shame language,
- invented macros,
- excessive notifications,
- medical interpretation of symptoms or labs.

### Weekly Review
Purpose:
- provide longitudinal learning and planning.

Inputs:
- weekly load,
- intensity distribution,
- sleep/recovery response,
- weight/nutrition trend,
- adherence to experiments,
- recommendations and outcomes.

Required sections:
- main pattern,
- evidence table or summary,
- what worked,
- what to adjust,
- next-week suggestion.

### Proactive Alerts
Allowed alert classes for future approval:
- sustained recovery deterioration,
- unusually rapid weight loss,
- repeated poor sleep pattern,
- missing critical data,
- hard training opportunity after improved recovery,
- follow-up due on prior recommendation,
- medical PDF/lab extraction needs confirmation.

Suppression rules:
- quiet hours suppress non-urgent reports,
- repeated alerts require cooldown,
- low-confidence alerts should become passive report notes,
- user opt-out overrides proactive behavior,
- medical uncertainty should not become alarming notification copy.

## Ambient State Model
Candidate records:
- `report_preferences`: morning/evening times, timezone, quiet hours, report depth, opt-in/out.
- `report_runs`: report type, generated time, status, source facts, and rendered surfaces.
- `report_sections`: readiness, sleep, training, nutrition, weight, health, follow-up, uncertainty.
- `monitoring_rules`: rule definition, thresholds, cooldowns, enabled state.
- `monitoring_events`: detected condition, evidence, severity, confidence, suppression state.
- `proactive_messages`: message candidate, delivery status, surface, reason, and user feedback.
- `active_experiments`: behavior change being tested, start date, evidence criteria, follow-up date.
- `follow_up_outcomes`: whether a recommendation was followed and what changed.

## Intent-To-Executable Impact
Ambient routines are compiled intents too.

Examples:
- "generate morning report" compiles into a readiness/report workflow.
- "generate evening report" compiles into a day-close workflow.
- "monitor recovery trend" compiles into a trend-detection workflow with cooldown rules.
- "follow up on protein timing experiment" compiles into an experiment-review workflow.

The future implementation should not run an unbounded agent loop. It should run named, bounded routines over approved primitives with explicit limits, evidence requirements, and persistence.

## Golden Fixture Additions
Add fixtures before live scheduling:

### `dtu_morning_report_normal`
Scenario:
- complete overnight data,
- stable recovery,
- normal planned training.

Expected behavior:
- concise readiness report,
- normal training suggestion,
- no alert language.

### `dtu_morning_report_fatigue`
Scenario:
- poor sleep, suppressed HRV, elevated RHR, high recent load.

Expected behavior:
- conservative training suggestion,
- evidence-backed uncertainty,
- no medical diagnosis.

### `dtu_evening_report_nutrition_gap`
Scenario:
- activity completed but nutrition data missing.

Expected behavior:
- ask concise nutrition follow-up,
- avoid macro assumptions.

### `dtu_evening_report_recovery_setup`
Scenario:
- heavy training day plus late meal pattern risk.

Expected behavior:
- suggest recovery-supporting evening behavior cautiously,
- cite prior pattern if available.

### `dtu_weekly_review_progress`
Scenario:
- consistent training and improved recovery after deload.

Expected behavior:
- identify what worked,
- recommend gradual ramp.

### `dtu_proactive_recovery_decline`
Scenario:
- five-day recovery decline crosses threshold.

Expected behavior:
- create proactive observation candidate,
- cite trend evidence,
- recommend lower intensity,
- respect delivery preferences.

### `dtu_proactive_suppressed_quiet_hours`
Scenario:
- alert condition detected during quiet hours.

Expected behavior:
- suppress delivery,
- queue for morning report or passive note.

### `dtu_prior_recommendation_followup`
Scenario:
- prior recommendation asked user to test earlier dinner timing for three nights.

Expected behavior:
- follow up when due,
- compare sleep before/after,
- avoid causal overclaiming.

## Build Guidance
First build should:
- implement report and monitoring schemas,
- implement synthetic report fixtures,
- generate report candidates without sending notifications,
- render report output locally or in test snapshots,
- verify evidence references,
- verify suppression and cooldown logic,
- avoid live scheduling until approved.

Mission 005 does not approve:
- cron,
- background workers,
- notification delivery,
- Telegram proactive messages,
- desktop/mobile push,
- live third-party sync,
- Hermes orchestration.
