# Dependency Research

## Version
v0.2

## Status
Mission 002 research complete. No dependency use approved.

## Garmin Connect/API Research
Decision:

```text
SYNTHETIC_FIRST_MANUAL_EXPORT_CANDIDATE
```

Approved now:
- synthetic data,
- architecture design,
- source-backed dependency research.

Not approved:
- Garmin credentials,
- Garmin account login,
- Garmin API calls,
- Garmin scraping,
- open-source Garmin client installation,
- automated Garmin integration.

### Official Garmin Path
Official source links:
- Garmin Connect Developer Program overview: https://developer.garmin.com/gc-developer-program/overview/
- Garmin Health API: https://developer.garmin.com/gc-developer-program/health-api/
- Garmin Health SDK overview: https://developer.garmin.com/health-sdk/overview/
- Garmin API brand guidelines: https://developer.garmin.com/brand-guidelines/api-brand-guidelines/

Findings:
- Garmin Connect Developer Program exposes Health API, Activity API, Women's Health API, Training API, and Courses API surfaces.
- Health API supports all-day health metrics including steps, heart rate, sleep, stress, pulse ox, Body Battery, body composition, respiration, blood pressure, and enhanced beat-to-beat interval.
- The API is cloud-to-cloud and requires end-user consent after program approval.
- Garmin states commercial use requires a license fee payment.
- Official access is the best long-term compliance path, but likely too heavy for the first private personal POC unless Garmin grants developer access for the use case.

### Manual Export/Import Path
Official/supporting source links:
- Garmin export support: https://support.garmin.com/en-AU/?=&faq=W1TvTPW8JZ6LfJSfK512Q8
- Garmin support on TCX export: https://support.garmin.com/en-GB/?faq=euV2pTGMOJ8RtTytcXLJ8A
- Strava support summary of Garmin file export: https://support.strava.com/hc/en-us/articles/216917807-Exporting-Files-from-Garmin-Connect

Findings:
- Garmin Connect supports exporting individual activities in formats such as original device file, TCX, GPX, Google Earth, splits CSV, and activity-list CSV depending on context.
- Manual import avoids storing Garmin credentials and avoids unofficial API automation in the first real-data step.
- Manual export may be incomplete for all health domains and can be operationally clumsy, but it is the lowest-risk real-data bridge.

### Open-Source Garmin Clients
Source links:
- python-garminconnect GitHub: https://github.com/cyberjunky/python-garminconnect
- garminconnect PyPI: https://pypi.org/project/garminconnect/
- GarminDB GitHub: https://github.com/tcgoetz/GarminDB
- Garth docs: https://garth.readthedocs.io/en/latest/

Findings:
- `garminconnect` is an active unofficial Python wrapper with broad Garmin Connect method coverage and a recent PyPI release.
- GarminDB can download, parse, store, and analyze Garmin Connect/watch data in SQLite databases, but requires Garmin credentials in local config and is GPL-2.0 licensed.
- Garth is deprecated after Garmin auth flow changes broke the mobile auth approach, which illustrates reliability risk for unofficial clients.
- Open-source clients are valuable for schema discovery and data-domain mapping, but should not be used in the first POC without explicit approval for terms, credentials, maintenance risk, and licensing.

### Recommended Garmin Posture
Use synthetic data first. If real data is approved later, start with manual export/import into the local database. Treat official Garmin access as the compliant long-term integration candidate. Keep unofficial clients as research references only unless a later mission explicitly approves the risk.

### Garmin Data Access Recommendation Matrix
| Approach | Completeness | Ease Of Implementation | Terms-Of-Service Risk | Long-Term Maintenance Burden | Reliability | Suitability For Personal-Use POC |
| --- | --- | --- | --- | --- | --- | --- |
| Synthetic-first | Low for real Garmin data; high for proving app workflows, schema, and coaching UX | Very easy | Very low | Very low | High | Best starting point because it proves the app and V3 workflow without credentials or external dependencies |
| Manual export/import | Medium; strong for activities and selected exports, weaker for full continuous health history unless Garmin export coverage is confirmed per metric | Easy to moderate | Low when using user-initiated exports | Moderate because import formats and user steps must be handled | Moderate to high; exports are user-controlled but not fully automated | Best first real-data bridge after explicit personal-data approval |
| Official Garmin Connect Developer Program / Health API and Activity API | High for supported health/activity domains after approval; best automated path for all-day metrics and activities | Moderate to hard because program approval, app setup, consent, and API integration are required | Low if approved and implemented under Garmin terms | Moderate; official APIs still require contract, consent, schema, and operational maintenance | High relative to unofficial options | Best long-term compliant automation path, but likely too heavy for the first private POC |
| Open-source Garmin Connect clients | Potentially high because some clients expose many Garmin Connect web endpoints | Easy to moderate technically, once credentials and client setup are approved | High/uncertain because they rely on unofficial/private Garmin Connect surfaces | High because auth and endpoints can break; Garth deprecation is a concrete warning | Medium to low; depends on Garmin auth and endpoint stability | Not preferred for the POC; useful for research and schema discovery only |
| Defer Garmin integration | None for Garmin-backed evidence | Very easy | Very low | Very low | High for scope control | Suitable if the next mission focuses purely on coach UX, memory, and analytics mechanics |

Preferred POC approach:

```text
synthetic-first, then manual export/import if real personal data is explicitly approved
```

Rationale:
- It maximizes V3 scope discipline and avoids credentials, bot tokens, package installs, and unofficial API risk.
- It still keeps the product architecture honest by modeling Garmin-like activities, sleep, HRV, recovery, weight, and health metrics.
- It allows a later build mission to prove ingestion, persistence, retrieval, and coaching behavior before negotiating official Garmin access.
- It avoids using unofficial clients as the first integration authority, while preserving them as references for data-domain mapping.

## Telegram Interaction Layer Research
Decision:

```text
DESIGN_NOW_CREATE_BOT_LATER
```

Source links:
- Telegram Bot API: https://core.telegram.org/bots/api
- Telegram Bot FAQ: https://core.telegram.org/bots/faq
- Telegram Bot Features: https://core.telegram.org/bots/features
- Telegram webhook guide: https://core.telegram.org/bots/webhooks

Findings:
- Telegram Bot API is HTTP-based and returns JSON responses.
- Updates can be received through mutually exclusive long polling (`getUpdates`) or webhooks (`setWebhook`).
- Bot updates include message objects for text, photo, document, voice, and other message types.
- `getFile` supports downloading bot-received files, with default Bot API limits; Telegram also documents a local Bot API server for larger local file handling, but that would be a separate dependency/ops decision.
- Telegram bot security must include a token secret policy, allowed user IDs, local/private deployment boundaries, rate-limit handling, and media retention rules.

Recommended Telegram posture:
- Design the adapter now but do not create the bot.
- For the first live private POC, prefer long polling on a local/private runtime if later approved, because it avoids public webhook infrastructure.
- Use a strict allowlist for the sponsor's Telegram user ID.
- Treat voice, image, and document processing as separate ingest pipelines with explicit retention and deletion rules.

## Database And Memory Layer Research
Decision:

```text
LOCAL_FIRST_SQLITE_PRIMARY_DUCKDB_OPTIONAL_ANALYTICS
```

Source links:
- SQLite appropriate uses: https://www.sqlite.org/whentouse.html
- SQLite JSON functions: https://www.sqlite.org/json1.html
- SQLite FTS5: https://www.sqlite.org/fts5.html
- DuckDB why DuckDB: https://duckdb.org/why_duckdb
- PostgreSQL JSON documentation: https://www.postgresql.org/docs/17/datatype-json.html

Findings:
- SQLite fits the first local/private POC because it is embedded, serverless, durable, and works well as an application file format.
- SQLite JSON functions allow flexible raw payload storage beside typed tables; FTS5 can support keyword memory search for notes and coaching observations.
- DuckDB is a strong optional sidecar for local analytical workloads but should not be the first transactional app database.
- PostgreSQL is the best expansion candidate when multi-user, cloud deployment, concurrent writes, managed backups, row-level security, or production operations become necessary.

Recommended schema posture:
- Use typed tables for stable facts: activities, sleep sessions, HRV, resting heart rate, body battery/stress if available, weight/body composition, nutrition logs, blood tests, notes, preferences, observations, recommendations, and source files.
- Keep raw source payloads/files referenced separately for replay.
- Store derived analytics as materialized daily/weekly facts with provenance back to source rows.
- Store coaching observations as evidence-backed records, not just chat transcript text.
- Maintain `source`, `source_record_id`, `observed_at`, `ingested_at`, `confidence`, and `provenance` fields wherever practical.

## Intelligence And Agent Layer Research
Decision:

```text
PIPELINE_PLUS_RETRIEVAL_FIRST_AGENTIC_MONITORING_LATER
```

Recommended architecture:
- Ingest layer normalizes source events from synthetic data, manual import, and future Garmin/Telegram inputs.
- Feature layer derives daily and weekly facts such as sleep quality, training load, recovery indicators, weight trend, nutrition signals, and missing-data flags.
- Retrieval layer fetches recent facts, relevant history, preferences, and prior coaching observations for each user question.
- Coaching layer produces answer-first responses with evidence, uncertainty, and next action.
- Recommendation records preserve claim, evidence rows, confidence, contraindications, and follow-up state.
- Proactive monitoring runs later as scheduled checks over derived facts and emits observations only when thresholds, trend breaks, or missing-data rules are met.

Medical safety posture:
- The system can support health and performance coaching, but must not diagnose, treat, or replace medical care.
- Blood tests and health markers require cautious interpretation, source provenance, and escalation language.

## Hermes-Style Orchestration Research
Decision:

```text
EXCLUDE_FROM_FIRST_POC_OPTIONAL_LATER_COMPARISON
```

Source links:
- Hermes Agent docs: https://hermes-agent.nousresearch.com/docs/
- Hermes CLI: https://hermes-agent.nousresearch.com/docs/user-guide/cli/
- Hermes desktop: https://hermes-agent.nousresearch.com/docs/user-guide/desktop
- Hermes messaging gateway: https://hermes-agent.nousresearch.com/docs/user-guide/messaging
- Hermes persistent memory: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
- Hermes MCP: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp

Findings:
- Hermes has surfaces that overlap with the long-term vision: CLI/TUI, desktop, messaging gateway, persistent memory, MCP, skills, background sessions, and multi-platform messaging including Telegram.
- That overlap makes Hermes useful as an orchestration reference, but risky for this V3 POC because it could become a hidden substitute for V3 standalone operation.
- Hermes gateway and tool execution imply credential, terminal, allowlist, and unattended automation boundaries that are broader than Mission 002.

Recommended Hermes posture:
- Do not install, configure, or use Hermes in the first POC.
- Use Hermes only as a reference for future orchestration concepts such as task routing, tool boundaries, persistent memory policies, and gateway security.
- Revisit only in a later mission if the POC needs a comparison harness after V3 standalone execution is already proven.

## Dependency Approval Rule
No dependency may be used in a mission until this file records an explicit decision and the active mission names the dependency authority.

Mission 002 approved no dependency use.

## Source Adapter Research
Decision:

```text
SOURCE_AGNOSTIC_CORE_WITH_ADAPTERS
```

Mission 004 recommendation:
- Do not tie the POC to Garmin Connect.
- Build normalized internal facts first.
- Treat Garmin, Apple Health, Google Health/Health Connect, Polar, Strava, medical PDFs, nutrition images, manual imports, and future systems as adapters.
- Preserve raw source provenance and confidence separately from normalized facts.

### Apple Health / HealthKit
Source links:
- Apple HealthKit documentation: https://developer.apple.com/documentation/healthkit
- Apple health-data privacy support: https://support.apple.com/en-mide/guide/security/sec88be9900f/web

Findings:
- HealthKit is the primary Apple developer framework for reading/writing health and fitness data with user permission.
- Apple emphasizes user permission, privacy, and protection of health data.
- HealthKit is strong for iPhone/Apple Watch users but implies an Apple-platform app or mobile bridge in a later mission.

POC posture:
- Design adapter now.
- Do not implement HealthKit until a later mobile/platform mission approves permissions, app scope, and data handling.

### Google Health / Fitbit / Health Connect
Source links:
- Google Health app and Fitbit Air announcement: https://blog.google/products-and-platforms/products/google-health/google-health-fitbit/
- Google Health app announcement: https://blog.google/products-and-platforms/products/google-health/google-health-app/
- Health Connect data format: https://developer.android.com/health-and-fitness/guides/health-connect/data-format
- Android Help: Learn about Health Connect: https://support.google.com/android/answer/13770320
- Google Fit REST API: https://developers.google.com/fit/rest/

Findings:
- Google announced the Fitbit Air and the Google Health app on May 7, 2026.
- Google says the Fitbit app is becoming the Google Health app, with existing Fitbit users upgraded and Google Fit users planned for migration later in 2026.
- Fitbit Air and the Google Health app make Google Health/Fitbit a first-class source ecosystem for the POC roadmap.
- Health Connect is the current Android health-data hub; it stores health and fitness data on device and shares it across apps with user permission.
- Health Connect records include metadata such as Health Connect ID, last modified time, data origin, device, client ID, client record version, and recording method.
- Google Fit REST API documentation still exists, but the architectural posture should favor Google Health/Fitbit and Health Connect for new design.

POC posture:
- Treat Google Health/Fitbit as a consumer source ecosystem and Health Connect as the Android integration substrate.
- Keep Google Fit as legacy/transition research only unless a later mission proves it is required.
- Do not assume Google Health exposes every needed field through a public API; preserve an adapter boundary and verify access in a later source-specific mission.

### Polar
Source links:
- Polar AccessLink API: https://www.polar.com/accesslink-api/
- Polar AccessLink announcement: https://www.polar.com/blog/introducing-polar-open-accesslink-api/

Findings:
- Polar AccessLink provides API access to Polar Flow data with a transaction model.
- Polar is a plausible official adapter path, but it requires app registration, authorization, transaction handling, and possibly webhook/pull-notification design.

POC posture:
- Design adapter now.
- Do not register apps, use credentials, or call Polar APIs until later approval.

### Strava
Source links:
- Strava authentication documentation: https://developers.strava.com/docs/authentication
- Strava API reference: https://strava.github.io/api/

Findings:
- Strava uses OAuth2 and registered applications.
- Strava APIs expose athlete, activity, streams, segments, uploads, and related resources, with rate limits.
- Strava is strongest as an activity/training source, not as a complete recovery, sleep, nutrition, or medical source.

POC posture:
- Treat Strava as an activity adapter candidate.
- Do not register apps, use tokens, or call Strava APIs until later approval.

### Medical PDFs
Decision:

```text
DESIGN_NOW_EXTRACT_LATER
```

Findings:
- Doctor-provided PDFs are likely to contain blood work, reference ranges, collection dates, lab/provider names, doctor comments, and report layout that matters.
- PDF extraction must preserve page/table references, confidence, units, and original-file provenance.
- Medical PDF interpretation must be non-diagnostic and should distinguish clinician text from generated summaries.

POC posture:
- Design schema and fixtures now.
- Do not ingest or parse real medical PDFs until a later approved mission.
