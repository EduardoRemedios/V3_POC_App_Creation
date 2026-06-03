# POC Constraints

## Version
v0.2

## Status
Research-only and non-enforcing until a separate build mission is approved.

## V3-Only Constraint
Factory V2 must not be used to design, build, test, deploy, govern, lint, recover, or validate this POC.

If V3 cannot proceed without V2, stop and record:
- the missing V3 capability,
- the blocked mission,
- the evidence that proves the gap,
- the recommended V3 improvement.

## Long-Horizon Mission Constraint
Factory V3 missions may be larger than micro-sprints when the mission envelope is explicit enough to prevent drift.

Allowed mission sizes:
- micro mission: narrow artifact or decision,
- standard mission: several related artifacts or a narrow implementation slice,
- long-horizon mission: multi-step design/build/test slice that may run for one to two hours or more.

Long-horizon missions require:
- explicit duration band,
- phases,
- checkpoints,
- fixture gates,
- authorized files/directories,
- allowed commands,
- dependency policy,
- drift audit,
- reentry rules,
- closeout and mission record.

A long-horizon mission must stop if:
- it needs files outside authorization,
- it needs an unapproved dependency,
- it needs credentials or real private data,
- it needs a live integration not approved by the mission,
- fixture failure implies scope expansion rather than implementation correction,
- verification cannot be run.

Larger missions do not weaken V3-only, dependency, privacy, or evidence constraints.

## Deployment Constraint
Deployment is private/internal only unless a later mission explicitly approves a target and scope.

No public deployment is approved by this file.

Initial deployment target:

```text
local development server only
```

## Data Constraint
Allowed by default:
- synthetic data,
- local mock data,
- local manually entered data.

Initial approved data mode:

```text
synthetic
```

Requires separate approval:
- real personal health/fitness data,
- Garmin Connect data,
- blood test data,
- credentials,
- tokens,
- third-party integrations,
- scheduled jobs,
- proactive notifications,
- cloud-hosted storage.

## Ambient Agent Constraint
Persistent ambient behavior is an approved design target but not an approved live runtime feature yet.

Allowed now:
- report contract design,
- monitoring rule design,
- fixture design,
- preference and state schema design,
- privacy and notification-boundary design.

Requires later mission approval:
- scheduler, cron, queue, background worker, or daemon implementation,
- Telegram notifications,
- desktop push notifications,
- mobile notifications,
- always-on cloud runtime,
- unattended third-party data retrieval,
- proactive message delivery.

Required future behavior:
- morning and evening reports must cite evidence and uncertainty,
- proactive alerts must use thresholds, cooldowns, and user preferences,
- quiet hours and opt-out controls must exist before live notifications,
- proactive behavior must never provide medical diagnosis or treatment advice,
- report state and follow-up state must persist independently of surface adapters,
- all scheduled or proactive outputs must be replayable from source facts, derived facts, and report records.

Default POC posture:

```text
ambient_design_only_synthetic_first
```

## Garmin Constraint
Garmin Connect/API work is research-only until `DEPENDENCY_RESEARCH.md` records an approved path and a later mission explicitly authorizes credential handling.

Mission 002 research decision:

```text
synthetic_first_manual_export_candidate
```

Implications:
- Official Garmin Connect Developer Program / Health API is the preferred compliant long-term route, but it depends on program approval and possible commercial terms.
- Manual export/import is the safest first real-data bridge if a later mission approves real data handling.
- Open-source Garmin Connect clients are research references only until legal, terms, credential, and maintenance risks are approved.
- No Garmin credentials, real account login, API calls, scraping, or data retrieval are approved by this file.

## Source-Adapter Constraint
The POC must not make Garmin Connect the core architecture.

Required posture:
- the internal model is source-agnostic,
- every third-party source is an adapter,
- adapters write normalized records plus provenance,
- source-specific raw payloads or replay references stay separate from normalized facts,
- derived analytics must depend on normalized facts, not Garmin-specific fields,
- recommendations must cite source and derived evidence regardless of adapter.

Current adapter candidates:
- Garmin manual export/import or future official API,
- Apple Health / HealthKit,
- Google Health / Fitbit and Health Connect,
- Polar / AccessLink,
- Strava API,
- medical PDFs,
- nutrition label images,
- manual imports and notes.

Requires later mission approval:
- API credentials or OAuth apps,
- mobile platform permissions,
- HealthKit or Health Connect app implementation,
- Strava or Polar app registration,
- real third-party data ingestion,
- external cloud sync,
- adapter-specific packages.

## Medical PDF Constraint
Medical PDF upload is an approved design target but not an approved live ingestion feature yet.

Allowed now:
- schema design,
- fixture design,
- extraction workflow design,
- privacy and retention requirements.

Requires later mission approval:
- PDF parsing or rendering package installation,
- real medical PDF ingestion,
- storage of real medical files,
- extraction of real blood-test values,
- external document AI/OCR/vision API use.

Required future behavior:
- preserve original PDF provenance and retention status,
- extract text/tables with confidence and page references,
- normalize lab markers with units and reference ranges,
- keep doctor comments distinct from generated interpretation,
- ask for correction or confirmation when extraction is uncertain,
- avoid diagnosis, treatment advice, or claims that replace clinician interpretation.

## Telegram Constraint
Telegram is the preferred chat interface, but this POC has not yet approved a live bot.

Allowed now:
- architecture research,
- interface design,
- token handling requirements,
- private/local deployment implications.

Requires later mission approval:
- creating a bot with BotFather,
- using or storing a Telegram token,
- registering webhooks,
- using long polling against the live API,
- sending or receiving live Telegram messages.

## Cross-Surface Conversation Constraint
Conversation, intent, and coaching memory must be independent of the UI surface.

Required architectural posture:
- Telegram, desktop web, and future clients are adapters over shared backend records.
- No surface may be the sole source of truth for conversation state.
- Active intent workflows, evidence packs, follow-up state, and durable memories must persist in the local database.
- Surface-specific renderings must be derived from shared records.
- Text, voice, image, and document inputs must normalize into the same intent pipeline after transcription, OCR, vision extraction, or parsing.

The first POC may implement only one surface, but the schema and architecture must not block handoff between Telegram and a desktop conversational app.

Requires later mission approval:
- live Telegram token handling,
- voice transcription dependency or API use,
- OCR, image understanding, or vision model dependency/API use,
- browser microphone capture,
- mobile or desktop image upload handling,
- desktop web deployment beyond local/private scope.

## Nutrition Image Capture Constraint
Nutrition image capture is an approved design target but not an approved live dependency or data-ingestion feature yet.

Allowed now:
- fixture design,
- schema design,
- extraction workflow design,
- privacy and retention requirements.

Requires later mission approval:
- OCR or vision package installation,
- OpenAI or other external vision API use,
- real food image ingestion,
- storage of real nutrition label photos,
- mobile camera capture,
- desktop file upload implementation.

Required future behavior:
- preserve source image provenance,
- extract structured nutrition fields with confidence and units,
- distinguish label values per serving, per 100g/ml, and consumed quantity,
- ask follow-up questions when quantity eaten or serving interpretation is unclear,
- avoid inventing hidden nutrients not visible in the source or stated by the user.

## Hermes Constraint
Hermes-style orchestration is research-only.

Mission 002 research decision:

```text
exclude_from_first_poc_optional_later_comparison
```

Hermes must not be installed, configured, executed, or used as an operational substitute for V3 standalone execution in the first POC. It may be revisited later as a comparison harness or orchestration reference only after explicit approval.

## Dependency Constraint
No new dependency is allowed unless the active mission names:
- package name,
- purpose,
- risk,
- install command,
- rollback plan,
- verification command,
- human approval.

Initial dependency posture:
- no packages installed in Mission 002,
- no Garmin or Telegram client libraries installed before a build mission,
- no Hermes libraries or tools installed,
- no authentication, payment, analytics, telemetry, or cloud storage dependencies.

## Evidence Constraint
Every mission must produce:
- mission envelope,
- files changed,
- commands run,
- verification result,
- halt/fallback review,
- closeout,
- mission record.
