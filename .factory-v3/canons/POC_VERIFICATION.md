# POC Verification

## Version
v0.2

## Status
Research-only and non-enforcing until a separate build mission is approved.

## Verification Goal
Prove both:
- the application works for the approved private POC scope,
- V3 operated standalone during the lifecycle.

## Required Verification Classes
| Class | Required Evidence |
| --- | --- |
| V3-only compliance | No Factory V2 stage, pack, lint, fallback, recovery, or validation was used. |
| Scope discipline | Every edit maps to an approved mission. |
| App behavior | The app meets the mission success criteria. |
| Test quality | Tests or checks run and results are recorded. |
| Deployment | Private/internal deployment target works if deployment is in scope. |
| Evidence replay | Mission records and closeouts are enough to reconstruct what happened. |
| Halt behavior | Failures stop work until a human decision or a new mission. |
| Long-horizon control | Larger missions have checkpoints, fixture gates, drift audits, and replayable intermediate evidence. |
| Dependency discipline | Garmin, Telegram, Hermes, or other dependencies are approved before use. |
| Privacy discipline | Health data, credentials, tokens, and personal records are not handled before explicit approval. |
| Cross-surface continuity | Conversation, intent, evidence, and memory state persist independently of Telegram or desktop UI clients. |
| Multimodal nutrition capture | Image/document nutrition inputs preserve source evidence, extraction confidence, units, and ambiguity handling. |
| Source-adapter discipline | Garmin, Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, PDFs, and future sources map into normalized facts through adapters. |
| Medical PDF handling | PDF evidence preserves file provenance, page/table references, extraction confidence, lab units, reference ranges, and non-diagnostic boundaries. |
| Ambient agent behavior | Morning reports, evening reports, proactive observations, follow-ups, thresholds, cooldowns, quiet hours, and report evidence are verified before live scheduling. |

## Default Verification Commands
Fill these after the app stack is chosen:

```bash
# lint
not_selected_yet

# typecheck
not_selected_yet

# test
not_selected_yet

# build
not_selected_yet

# local/private deployment smoke check
not_selected_yet
```

## Research Mission Verification
For V3-only dependency and architecture research missions, verify:
- the active mission exists and authorizes every edited file,
- the POC folder is outside `Factory_V3`,
- no Factory V2 scripts or docs were copied into the POC folder,
- V2 references are limited to forbidden/no-go wording,
- no packages were installed,
- no Garmin credentials or API calls were used,
- Telegram was researched only and no bot/token was created,
- Hermes was researched only and not installed, configured, or used,
- JSON mission records parse.

## Long-Horizon Mission Verification
For long-horizon missions, verify:
- mission envelope declares duration band, phases, checkpoints, fixture gates, drift audit, and reentry rules,
- each checkpoint records phase, files changed, commands run, fixture gate status, open risks, and next phase,
- fixture gates are run before dependent work proceeds,
- failures are classified as implementation bug, fixture issue, scope gap, dependency gap, or standalone V3 gap,
- scope expansion is recorded and halted unless already authorized,
- closeout can replay what changed across the full mission.

Recommended fixture gate order:
- Gate A: fixture definitions exist,
- Gate B: fixture files exist,
- Gate C: schema can load fixtures,
- Gate D: deterministic primitives pass,
- Gate E: workflow contracts pass,
- Gate F: safety and evidence pass.

## Digital Twin And Golden Fixture Verification
Future build missions should use a Digital Twin User fixture set before any Garmin-backed evidence is required.

Golden fixtures should include:
- baseline healthy training week,
- accumulated fatigue week,
- poor sleep after late meal scenario,
- improving recovery after adjusted nutrition timing,
- weight-loss plateau scenario,
- excessive weight-loss risk scenario,
- missing Garmin-like data scenario,
- contradictory metrics scenario,
- hard workout followed by HRV/resting-heart-rate suppression,
- deload/recovery week with improving metrics,
- nutrition note without precise macros,
- nutrition label image for Greek yoghurt with serving-size ambiguity,
- nutrition label image with per-100g and per-serving values,
- synthetic medical PDF blood-work report with table extraction ambiguity,
- repeated synthetic blood-work PDFs requiring trend comparison,
- morning readiness report from synthetic daily state,
- evening recovery/nutrition report from synthetic daily state,
- proactive alert suppressed by cooldown or quiet hours,
- follow-up on a prior recommendation,
- blood-test-like synthetic record with safe non-diagnostic handling,
- cross-surface handoff from Telegram-style text to desktop-style rich conversation and back,
- voice-to-text intent continuation after a prior text session.

Each fixture should define:
- input records,
- expected derived facts,
- expected retrieved context,
- acceptable coaching response properties,
- prohibited claims,
- evidence references that must appear in the answer,
- expected persisted conversation and intent state across surfaces,
- expected extracted nutrition fields, confidence, units, and follow-up questions,
- expected adapter provenance, source identity, and raw-to-normalized mapping,
- expected medical PDF marker units, reference ranges, page references, and prohibited diagnostic claims,
- expected ambient report sections, triggers, suppression behavior, evidence references, and follow-up state.

Golden fixtures are required to prevent synthetic data from becoming arbitrary demo data. They should become regression tests once the app stack is selected.

## Evidence Rules
- Summarize command output; do not paste secrets or private tokens.
- Record failed checks honestly.
- Do not continue after failed verification unless a new mission explicitly authorizes the recovery path.
- Label synthetic-only evidence separately from Garmin-backed evidence.
- Label manual-import evidence separately from automated Garmin API evidence.
- Label Hermes-assisted evidence separately if Hermes is later approved.
- Label Telegram live-bot evidence separately if Telegram is later approved.
