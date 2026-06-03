# Mission 011: Synthetic Manual Import And Source Adapter Readiness

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO

## Objective
Build a synthetic-only manual import/source-adapter lab that prepares the Personal Performance OS for a future real-data bridge without touching real data, Garmin credentials, live APIs, scraping, package installs, or external integrations.

## Success Criteria
- Synthetic manual export fixtures exist for multiple source families and edge cases.
- A stdlib source-adapter registry can list adapters, parse synthetic export-like files, validate rows, produce mapping previews, detect duplicate/conflict/timezone/unit issues, and preserve provenance.
- SQLite tables persist import sessions, source files, preview rows, validation issues, mapping rows, and conflict reports.
- Local API endpoints expose adapter catalog, synthetic export catalog, preview/validate/import flows, mapping diff, conflicts, and audit summary.
- The static workbench includes a usable source-adapter lab view with preview, validation, mapping, conflict, and audit surfaces.
- Browser QA verifies the source-adapter lab flow on localhost.
- Generated Mission 011 audit JSON records fixture counts, adapter coverage, DB tables, API endpoints, workbench surfaces, verification commands, Browser QA, dependency review, and residual risks.
- No real data, live integrations, package installs, credentials, Telegram live behavior, public deployment, Factory V2, or Factory_V3 repo tooling are used.

## Eligible-Work Rationale
This mission is larger than Mission 010 by natural product surface: it adds synthetic export fixtures, adapter parsing, validation, persistence, API flows, workbench UI, Browser QA, and audit evidence. The mission remains bounded because it is local-only, synthetic-only, stdlib-only, and preview-oriented.

## Non-Goals
- No real personal health, fitness, nutrition, medical, image, voice, or identity data.
- No real Garmin export files.
- No Garmin login, credentials, API calls, scraping, unofficial client, or account access.
- No Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, Telegram, OCR, vision, voice transcription, scheduler, notification, Hermes, public deployment, or production infrastructure.
- No package installation.
- No git commit/push/branch/remote changes unless separately instructed after closeout.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_011_SYNTHETIC_MANUAL_IMPORT_SOURCE_ADAPTER_READINESS.md`
- `.factory-v3/evidence/MISSION_011_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_011_STATE.md`
- `.factory-v3/evidence/MISSION_011_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_011_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_011_RECORD.json`
- `.factory-v3/evidence/MISSION_011_AUDIT_SUMMARY.json`
- `.factory-v3/evidence/MISSION_011_BROWSER_NOTES.md`
- `fixtures/manual_exports/`
- `ppos_core/manual_imports.py`
- `ppos_core/migrations/003_mission_011.sql`
- `ppos_core/storage.py`
- `ppos_core/api.py`
- `ppos_core/workbench.py`
- `workbench/index.html`
- `workbench/app.js`
- `workbench/styles.css`
- `scripts/mission_011_import_lab_qa.py`
- `scripts/verify_mission_011.py`
- `tests/test_mission_011_manual_imports.py`
- `tests/test_mission_011_api.py`
- `tests/test_mission_011_workbench.py`

## Forbidden Scope
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or Factory_V3 repo tooling.
- Real data or real exports from any source.
- Credentials, tokens, account login, OAuth apps, BotFather, webhooks, long polling, live messages, scraping, external API calls, or live third-party integration.
- OCR/vision execution, voice transcription execution, medical PDF ingestion, scheduler/cron/worker/daemon/queue/notification delivery, Hermes, package install, or public deployment.
- Git write operations without a later explicit human instruction.

## Allowed Commands
- Read/search/status commands: `pwd`, `ls`, `find`, `sed`, `rg`, `git status --short --branch`, `git diff --stat`.
- Python stdlib verification: `python3 -B -m unittest discover -s tests`, `python3 -B scripts/mission_011_import_lab_qa.py --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`, `python3 -B scripts/verify_mission_011.py`.
- JSON parse checks: `python3 -m json.tool .factory-v3/evidence/MISSION_011_RECORD.json`, `python3 -m json.tool .factory-v3/evidence/MISSION_011_AUDIT_SUMMARY.json`, `python3 -m json.tool fixtures/manual_exports/manifest.json`.
- Local API server: `python3 -B -m ppos_core.api --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`.
- Mission-owned local process cleanup only: `lsof -ti tcp:<mission port>`, `kill <mission server pid>`.
- Built-in Codex Browser against `http://127.0.0.1:<mission port>/workbench/` only.

## Dependency Policy
- New dependencies allowed: NO
- If YES, approval reference: not applicable
- Install command: not applicable
- Rollback plan: not applicable

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: all existing and Mission 011 tests pass.
- `python3 -B scripts/mission_011_import_lab_qa.py --db /tmp/ppos_mission_011_qa.sqlite --host 127.0.0.1 --port 8780`: local import-lab API/static checks pass and write authorized audit summary.
- `python3 -B scripts/verify_mission_011.py`: mission envelope, state, checkpoints, static workbench, fixture manifest, audit summary, API/source no-go checks pass.
- JSON parse checks for Mission 011 record, audit summary, and manual export manifest pass.
- Browser QA verifies the source-adapter lab flow: adapter catalog mounts, synthetic export selection works, preview runs, validation issues render, mapping diff renders, conflicts render, import session persists, no runtime errors, desktop screenshot attempted, mobile/responsive check attempted.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission envelope, fixture design, adapter implementation, persistence/API, workbench UI, stdlib verification, Browser QA, final closeout.
- Mission state file: `.factory-v3/evidence/MISSION_011_STATE.md`
- Human decision interrupts allowed: YES
- Interrupt surfaces allowed: thread | file | telegram-research-only
- Timeout behavior for unresolved interrupts: pause
- Plan delta required before scope change: YES
- Verification side effects allowed: YES
- If YES, authorized output paths:
  - `.factory-v3/evidence/MISSION_011_AUDIT_SUMMARY.json`
  - `.factory-v3/evidence/MISSION_011_BROWSER_NOTES.md`
  - `.factory-v3/evidence/MISSION_011_CHECKPOINTS.md`
  - `.factory-v3/evidence/MISSION_011_STATE.md`
  - `.factory-v3/evidence/MISSION_011_CLOSEOUT.md`
  - `.factory-v3/evidence/MISSION_011_RECORD.json`

## Halt Rules
Stop if:
- Factory V2 or Factory_V3 repo tooling appears necessary.
- Real data, credentials, live integration, package install, Telegram live behavior, OCR/vision, voice transcription, scheduler, notification, Hermes, public deployment, or production infrastructure appears.
- Verification requires source paths, commands, dependencies, or git authority not authorized by this mission.
- Import preview work becomes real-data ingestion or source-specific live integration.
- Mission state/checkpoint evidence becomes stale or contradicts repository state.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as a fallback while claiming POC readiness.

## Reentry Rules
- Resume only from authored mission artifacts, `.factory-v3/evidence/MISSION_011_STATE.md`, latest checkpoint, and current repository state.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md`.
