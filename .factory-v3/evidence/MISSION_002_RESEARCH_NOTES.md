# Mission 002 Research Notes

## Status
COMPLETE

## Mission
`.factory-v3/missions/MISSION_002_RESEARCH_AND_ARCHITECTURE.md`

## Date
2026-06-03

## Summary Decision
Recommended next architecture path:

```text
synthetic-first local-first coach with Telegram adapter design, manual Garmin export/import as the first future real-data bridge, official Garmin as long-term compliant integration, and Hermes excluded from the first POC.
```

## Garmin Research
Sources:
- Garmin Connect Developer Program overview: https://developer.garmin.com/gc-developer-program/overview/
- Garmin Health API: https://developer.garmin.com/gc-developer-program/health-api/
- Garmin Health SDK overview: https://developer.garmin.com/health-sdk/overview/
- Garmin export support: https://support.garmin.com/en-AU/?=&faq=W1TvTPW8JZ6LfJSfK512Q8
- Garmin TCX support: https://support.garmin.com/en-GB/?faq=euV2pTGMOJ8RtTytcXLJ8A
- Strava Garmin export notes: https://support.strava.com/hc/en-us/articles/216917807-Exporting-Files-from-Garmin-Connect
- python-garminconnect: https://github.com/cyberjunky/python-garminconnect
- garminconnect PyPI: https://pypi.org/project/garminconnect/
- GarminDB: https://github.com/tcgoetz/GarminDB
- Garth: https://garth.readthedocs.io/en/latest/

Findings:
- Official Garmin Connect Developer Program is the best compliance path for automated Garmin data, but it requires approval and may require commercial licensing.
- Official Health API covers the main POC health domains: steps, HR, sleep, stress, Body Battery, body composition, respiration, blood pressure, pulse ox, and related summaries.
- Official Activity API is relevant for full activity data.
- Manual export/import is safer for the first real-data experiment because it avoids storing credentials and avoids unofficial scraping.
- Unofficial clients are active and useful, but they rely on Garmin Connect web/private surfaces and can break when Garmin auth changes. Garth is now deprecated for that reason.
- GarminDB is architecturally useful because it demonstrates a SQLite-backed personal Garmin data model, but it requires credentials and has GPL-2.0 licensing implications.

Recommendation:
- Do not automate Garmin in the next build mission.
- Use synthetic data for first app behavior.
- If real data becomes necessary, approve a manual export/import mission before any automated client work.
- Keep official Garmin API access as a later compliance investigation.

### Garmin Access Matrix
| Approach | Completeness | Ease Of Implementation | Terms-Of-Service Risk | Long-Term Maintenance Burden | Reliability | Personal-Use Suitability |
| --- | --- | --- | --- | --- | --- | --- |
| Synthetic-first | Does not provide real Garmin history, but can cover every desired schema domain with representative data. | Easiest. No external account, dependency, or parser needed. | Very low. | Very low. | High because data is controlled locally. | Preferred first step for the POC. |
| Manual export/import | Partial to medium. Activity exports are practical; full health/recovery coverage must be verified by metric and export format. | Easy to moderate. Requires import parser and user export steps. | Low, because the user manually exports their own data through supported UI paths. | Moderate. User workflow and file formats need maintenance. | Moderate to high. Reliable for files the user can export, but not automatic. | Preferred first real-data bridge after explicit approval. |
| Official Garmin APIs | High for supported API domains, especially Health API and Activity API, after program approval. | Moderate to hard. Requires program approval, consent flow, API integration, and possibly commercial terms. | Low if approved and used under Garmin terms. | Moderate. Official API integrations still need contract, auth, consent, schema, and operational upkeep. | High relative to unofficial routes. | Best long-term automated approach, but not the first POC path. |
| Open-source Garmin clients | Potentially high. Active clients expose many web endpoints; GarminDB covers broad personal data workflows. | Easy to moderate technically, but requires credentials and unapproved client installation. | High or uncertain because access is unofficial/private-surface based. | High. Auth and endpoints can break; Garth is deprecated after Garmin auth changes. | Medium to low. Depends on Garmin web behavior outside the official program. | Not preferred. Research reference only unless later explicitly approved. |
| Defer Garmin | None for Garmin-backed evidence. | Easiest. | Very low. | Very low. | High for project execution. | Acceptable only if next mission is limited to coach UX and local memory mechanics. |

Preferred approach for the POC:

```text
synthetic-first with schema designed for Garmin-like data; manual export/import as the first approved real-data bridge; official Garmin APIs as the long-term compliant automation target.
```

Why:
- It proves the product mechanics without waiting on Garmin program approval.
- It avoids storing Garmin credentials during the first POC.
- It avoids unofficial-client terms and maintenance risk.
- It preserves a clean upgrade path to official automation.

## Digital Twin User Strategy
The synthetic-first approach should become a Digital Twin User strategy.

Working definition:

```text
A Digital Twin User is a realistic synthetic proxy for the sponsor, with controlled longitudinal data, goals, preferences, training history, recovery patterns, nutrition notes, health markers, and known edge cases.
```

Why this helps:
- Garmin access can remain blocked without blocking product design.
- The coach can be tested against known ground-truth scenarios.
- Memory behavior can be tested over weeks or months of synthetic history.
- Proactive recommendations can be evaluated before live notifications exist.
- Data modeling can be validated before importing messy real files.

Recommended DTU domains:
- profile: age band, sport focus, goals, constraints, preferences, timezone, normal training schedule,
- activities: rides, runs, strength, rest days, intensity, duration, load, subjective effort,
- recovery: HRV, resting heart rate, stress, Body Battery-like recharge, readiness-like score,
- sleep: duration, timing, efficiency, wake events, qualitative notes,
- nutrition: meal notes, protein distribution, late dinners, alcohol/caffeine flags, approximate macro quality,
- body composition: weight trend, rate of loss/gain, plateau periods,
- health: synthetic blood-test-like records and manual observations,
- memory: durable preferences, prior recommendations, coaching observations, follow-up outcomes.

DTU design rules:
- Include realistic missingness, noise, and delayed records.
- Include contradictions between subjective notes and device-like metrics.
- Keep raw input records and expected derived facts separate.
- Do not let synthetic fixtures imply medical diagnosis capability.
- Treat DTU records as fixtures with expected behavior, not random sample data.

## Pre-Mortem
Assume the POC failed. Likely failure modes:

| Failure Mode | Why It Matters | Golden Fixture Mitigation |
| --- | --- | --- |
| Garmin access blocks progress | Official access may require approval; unofficial access is risky | DTU fixture pack proves app, schema, retrieval, and coaching without Garmin |
| Synthetic data is too clean | Coach appears good in demos but fails on messy real data | Add missing, delayed, noisy, duplicated, and contradictory records |
| Coach gives generic advice | Product becomes a chatbot, not a persistent performance OS | Fixtures require answers to cite user-specific history and recent facts |
| Coach overclaims medically | Health markers and blood tests can trigger unsafe interpretation | Fixtures define prohibited diagnostic claims and escalation language |
| Memory becomes transcript stuffing | Long chats swamp useful durable facts | Fixtures separate chat logs from promoted durable memories |
| Recommendations lack evidence | User cannot trust or audit suggestions | Fixtures require source record references and uncertainty statements |
| Proactive alerts become noisy | User stops trusting the system | Fixtures test threshold, trend, cooldown, and missing-data behavior |
| Weight and nutrition advice becomes harmful | Aggressive goals can risk muscle loss or disordered patterns | Fixtures require rate-of-change checks and conservative language |
| Training advice ignores recovery | App may recommend hard sessions during fatigue | Fixtures include HRV/RHR/sleep suppression after load spikes |
| Manual import creates bad joins | File formats may duplicate or misalign dates | Fixtures include duplicate source records and timezone boundaries |
| Telegram media handling leaks data | Images, voice, and documents may contain sensitive data | Fixtures require retention/deletion policy and allowed-user checks |
| Nutrition image extraction invents data | Vision/OCR may hallucinate values or miss serving-size context | Fixtures require source image evidence, confidence, units, and follow-up questions for ambiguity |
| Nutrition labels use different bases | Per-serving, per-100g, and consumed quantity can be confused | Fixtures include label basis and quantity-eaten checks |
| Conversation gets trapped in one surface | User cannot move between Telegram and desktop without losing context | Fixtures require shared conversation, intent, evidence, and memory state across surfaces |
| Voice creates a separate context path | Voice notes do not influence the active text conversation correctly | Fixtures normalize voice transcripts into the same intent pipeline |
| Image creates a separate context path | Food label photos are handled as attachments instead of nutrition evidence | Fixtures normalize image extraction into the same nutrition intent pipeline |
| Architecture locks into Garmin | Future sources become hard to add | Fixtures use source-agnostic normalized facts and source provenance |
| External orchestration muddies V3 proof | Hermes or other tools could hide V3 gaps | Fixtures run under V3-only evidence before any orchestration comparison |

## Golden Fixture Recommendations
Create a fixture pack before app implementation.

Minimum fixture set:
- `dtu_baseline_healthy_week`: normal training, sleep, nutrition, and stable recovery.
- `dtu_accumulated_fatigue`: five to seven days of declining HRV, rising RHR, poor sleep, and sustained load.
- `dtu_late_high_fat_dinner_sleep_drop`: late dinner note followed by reduced sleep quality.
- `dtu_protein_distribution_recovery_improves`: nutrition timing improves and recovery markers rise.
- `dtu_weight_loss_plateau`: stable calorie/training pattern with stalled weight trend.
- `dtu_weight_loss_too_fast`: rapid weight loss with muscle-loss risk language expected.
- `dtu_hard_session_suppressed_recovery`: hard workout followed by low HRV and elevated RHR.
- `dtu_deload_recovery`: reduced load with improving sleep and recovery metrics.
- `dtu_missing_data`: absent sleep or HRV records requiring uncertainty.
- `dtu_contradictory_metrics`: user feels good but recovery metrics are poor, or the reverse.
- `dtu_duplicate_import`: duplicated activity export requiring deduplication.
- `dtu_timezone_boundary`: late-night activity/sleep crossing date boundaries.
- `dtu_nutrition_free_text`: meal note without macros requiring cautious inference.
- `dtu_greek_yoghurt_label_image`: synthetic nutrition label image metadata for Greek yoghurt requiring structured nutrition extraction.
- `dtu_nutrition_label_basis_ambiguity`: label contains both per-100g and per-serving values; expected behavior asks quantity eaten.
- `dtu_synthetic_blood_marker`: synthetic blood-test-like result requiring non-diagnostic framing.
- `dtu_cross_surface_recovery_handoff`: Telegram recovery question continued in desktop UI and closed back in Telegram.
- `dtu_desktop_to_telegram_training_followup`: desktop four-week analysis followed by a Telegram ride/rest decision question.
- `dtu_voice_continuation`: voice note updates subjective fatigue inside an existing text conversation.

Each golden fixture should include:
- fixture ID,
- scenario description,
- input records,
- expected normalized rows,
- expected derived facts,
- expected coaching answer traits,
- prohibited answer traits,
- required evidence references,
- privacy and safety notes.

## Telegram Research
Sources:
- Telegram Bot API: https://core.telegram.org/bots/api
- Telegram Bot FAQ: https://core.telegram.org/bots/faq
- Telegram Bot Features: https://core.telegram.org/bots/features
- Telegram Webhooks: https://core.telegram.org/bots/webhooks

Findings:
- Telegram supports the desired interaction shape: text, voice messages, photos/images, documents/files, commands, buttons, and direct chat.
- Updates can be received by long polling or webhook; they are mutually exclusive.
- For a local/private first live POC, long polling is simpler because no public webhook endpoint or TLS setup is required.
- Bot tokens are secrets and live bot creation is out of scope for Mission 002.
- Media handling needs explicit file retention, transcription, OCR/image analysis, document parsing, and deletion rules in future missions.

Recommendation:
- Design a Telegram adapter but do not create a bot yet.
- Later, use strict allowlisting and local/private runtime before any public webhook.

## Cross-Surface Conversation Continuity
New constraint:

```text
Conversation and intent state must persist across Telegram and a desktop conversational web application.
```

Rationale:
- Telegram is a convenient mobile surface, but it should not define the product architecture.
- A desktop web app can provide richer runtime UI for charts, evidence review, editable assumptions, and longer analysis.
- The user should be able to start in Telegram, continue on desktop, and return to Telegram with the same active intent and memory context.

Architectural implications:
- Store conversations, messages, active intents, workflow runs, evidence packs, recommendations, follow-ups, and durable memories in the local database.
- Treat Telegram and web as adapters that render shared state differently.
- Normalize text and voice into the same intent pipeline after transcription/parsing.
- Keep voice artifacts and transcripts as governed records with explicit retention rules.
- Keep image artifacts, OCR output, and extracted structured fields as governed records with explicit retention rules.
- Do not let UI components own business state; runtime UI should be generated from workflow state and evidence records.

Recommended state model:
- `conversation_threads`: user-facing threads independent of surface.
- `conversation_messages`: normalized text messages, transcription outputs, and surface metadata.
- `intent_sessions`: current or completed compiled intents with status and parameters.
- `workflow_runs`: executable workflow records with selected primitives, limits, and results.
- `evidence_packs`: cited source facts, derived facts, and uncertainty notes used by an answer.
- `surface_events`: Telegram/web-specific delivery, click, voice, image, and document events.
- `ui_render_specs`: optional desktop runtime UI descriptors generated from workflow results.
- `follow_ups`: pending checks, reminders, and recommendation review points.

Golden fixture additions:
- Start a recovery question in Telegram-style text, open the same thread in desktop web, inspect richer evidence, then send a follow-up from Telegram.
- Start a training analysis on desktop, then ask a short Telegram follow-up that depends on the prior analysis.
- Continue a text session with a voice note that changes the user's subjective recovery state.
- Upload a Greek yoghurt nutrition-label image on one surface, inspect extracted nutrition fields on another surface, and confirm quantity eaten from either surface.
- Verify that the answer references the same intent session and evidence pack across surfaces.

## Multimodal Nutrition Capture
Design target:

```text
The user should be able to upload a photo of food packaging or a nutrition label from Telegram, mobile, or desktop, and have the system convert visible label information into a structured nutrition log.
```

Example:
- User eats Greek yoghurt.
- User photographs the front package and/or nutrition facts panel.
- User uploads the image instead of typing nutrients manually.
- The system extracts product identity and visible nutrition facts.
- The system asks how much was eaten if quantity or serving basis is unclear.

Recommended extraction workflow:
- store source image reference and surface metadata,
- run OCR/vision extraction only after a later dependency/privacy approval,
- parse visible nutrition fields into structured values with units,
- classify whether values are per 100g/ml, per serving, or package total,
- ask for consumed quantity when not inferable,
- create a nutrition log with source references and confidence,
- preserve the raw extraction output for replay/correction,
- allow user correction through Telegram or desktop.

Candidate nutrition fields:
- product name,
- brand if visible,
- serving size,
- quantity consumed,
- calories or energy,
- protein,
- carbohydrates,
- sugars,
- fat,
- saturated fat,
- fiber,
- salt or sodium,
- visible micronutrients,
- ingredients or allergen notes if relevant and visible.

Safety and quality rules:
- Do not infer exact macros from a package photo if the label is unreadable.
- Do not invent nutrients that are not visible or stated by the user.
- Always keep unit provenance.
- Preserve confidence and extraction method.
- Prefer a short clarification over a false precise log.

State model additions:
- `nutrition_label_images`: source image metadata, surface, retention status, and hash.
- `nutrition_extractions`: OCR/vision output, parsed fields, confidence, and errors.
- `nutrition_log_entries`: confirmed consumed food records linked to extraction evidence.
- `nutrition_corrections`: user edits to extracted or logged values.

## Database And Memory Research
Sources:
- SQLite appropriate uses: https://www.sqlite.org/whentouse.html
- SQLite JSON functions: https://www.sqlite.org/json1.html
- SQLite FTS5: https://www.sqlite.org/fts5.html
- DuckDB: https://duckdb.org/why_duckdb
- PostgreSQL JSON: https://www.postgresql.org/docs/17/datatype-json.html

Findings:
- SQLite is the best first persistent database for a local/private POC: embedded, durable, serverless, and suitable as an application file format.
- SQLite JSON support lets the app preserve raw payload fragments while promoting stable fields into typed tables.
- SQLite FTS5 can support text search for notes, observations, and recommendation history without adding vector dependencies.
- DuckDB is useful later for heavier local analytics, but it is not the right first app state database.
- PostgreSQL is the expansion route once the app needs multi-user or cloud operations.

Recommended first schema domains:
- `source_files`
- `conversation_threads`
- `conversation_messages`
- `intent_sessions`
- `workflow_runs`
- `evidence_packs`
- `surface_events`
- `ui_render_specs`
- `follow_ups`
- `activities`
- `sleep_sessions`
- `hrv_readings`
- `resting_heart_rate_readings`
- `recovery_metrics`
- `weight_entries`
- `nutrition_label_images`
- `nutrition_extractions`
- `nutrition_logs`
- `nutrition_corrections`
- `health_records`
- `blood_tests`
- `manual_notes`
- `derived_daily_metrics`
- `coaching_observations`
- `recommendations`
- `user_preferences`
- `chat_messages`

Memory design:
- Keep chat transcript separate from durable coaching memory.
- Promote durable memories only when they are stable preferences, repeated patterns, user goals, or evidence-backed observations.
- Store provenance and confidence for each insight.
- Preserve raw source references for replay and correction.

## Intelligence And Agent Research
Recommended structure:
- Ingest pipeline: source-specific parser to normalized event/fact tables.
- Derivation pipeline: daily and weekly metrics, trends, anomalies, and missing-data markers.
- Retrieval pipeline: recent facts, comparable history, user preferences, prior recommendations, and source evidence.
- Response pipeline: answer, evidence, uncertainty, recommendation, and follow-up.
- Proactive monitoring: scheduled rules over derived facts, added later after live data and notification authority exist.

Evidence-backed recommendation shape:
- `recommendation_id`
- `created_at`
- `question_or_trigger`
- `claim`
- `evidence_summary`
- `source_record_refs`
- `confidence`
- `risk_or_uncertainty`
- `suggested_action`
- `follow_up_date`
- `status`

### Architectural Pattern From Perplexity Intent-As-Program
Source:
- Perplexity Research, "Rethinking Search as Code Generation": https://research.perplexity.ai/articles/rethinking-search-as-code-generation

Useful architectural idea:
- The relevant lesson is not search itself. Search is the first demonstration domain.
- The deeper shift is compiling human intent into bounded executable programs that can orchestrate primitives, manage intermediate state, perform deterministic operations, and return only the evidence and answer shape the task requires.

Transfer to this POC:
- Do not build a single monolithic coach prompt that always retrieves the same context bundle.
- Do not build a fixed "daily readiness pipeline" as the only way to answer questions.
- Build low-level primitives for normalized fact retrieval, trend calculation, missing-data checks, source evidence lookup, user preference lookup, prior recommendation lookup, safety checks, and response shaping.
- Provide higher-level convenience workflows for common questions, but keep them decomposable.
- Let different user intents compile into different executable workflows:
  - "How recovered am I today?" should emphasize sleep, HRV, resting heart rate, recent load, subjective notes, and uncertainty.
  - "Why was my sleep poor last night?" should emphasize sleep timing, meal/alcohol/caffeine notes, stress, training load, and historical comparables.
  - "Analyse my last four weeks of training" should fan out across weekly load, intensity distribution, recovery response, consistency, and performance markers.
  - "Should I ride tomorrow?" should combine readiness, training plan, fatigue trend, user goals, and risk boundaries.

Design implications:
- Treat the model as the intent compiler and control plane that chooses which primitives to compose, not as the place where all state and computation lives.
- Use deterministic local computation for joins, trend calculations, deduplication, date-window logic, thresholds, and evidence assembly.
- Persist intermediate state explicitly in the local database or replayable artifacts rather than relying on hidden conversation context.
- Keep primitive APIs small and legible enough that a model or future orchestrator can use them correctly.
- Use golden fixtures to verify not just final answers, but the selected pipeline, derived facts, and cited evidence.

POC primitive candidates:
- `load_user_profile`
- `get_metric_window`
- `get_recent_activities`
- `compute_training_load`
- `compute_sleep_summary`
- `compute_recovery_summary`
- `detect_missing_data`
- `find_similar_periods`
- `retrieve_relevant_memories`
- `extract_nutrition_from_image_candidate`
- `normalize_nutrition_label_values`
- `ask_nutrition_quantity_clarification`
- `assemble_evidence_pack`
- `check_safety_boundaries`
- `write_recommendation_record`
- `schedule_follow_up_candidate`

Risk to avoid:
- Over-abstracting before the POC has working behavior. The first implementation should expose only the primitives required by the DTU golden fixtures, then add primitives when a fixture or user question proves the need.
- Letting generated workflows become unbounded. Future build missions should define allowed primitives, execution limits, persistence rules, and evidence requirements before enabling any agentic workflow execution.

## Hermes Research
Sources:
- Hermes docs: https://hermes-agent.nousresearch.com/docs/
- Hermes CLI: https://hermes-agent.nousresearch.com/docs/user-guide/cli/
- Hermes desktop: https://hermes-agent.nousresearch.com/docs/user-guide/desktop
- Hermes messaging gateway: https://hermes-agent.nousresearch.com/docs/user-guide/messaging
- Hermes memory: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
- Hermes MCP: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp

Findings:
- Hermes overlaps with desired long-term capabilities: messaging gateway, Telegram support, persistent memory, MCP tools, background sessions, skills, desktop, and CLI/TUI.
- It also introduces broader runtime authority and credential concerns.
- Using Hermes now would weaken the POC signal because the current objective is to prove V3 standalone operation with Codex.

Recommendation:
- Do not install, configure, or use Hermes in the first POC.
- Revisit later as a comparison harness only after V3 standalone execution is already demonstrated.

## Halt Review
No halt rule was encountered.

No credentials, real personal health data, Garmin API calls, Telegram tokens, bot creation, Hermes execution, package installation, app source code, public deployment, or V2 tooling were needed.
