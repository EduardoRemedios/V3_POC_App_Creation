# Mission 008 Synthetic Local OS Workbench

## Status
IN_PROGRESS

## Mission Type
long_horizon_build

## Duration Band
multi_hour_long_horizon

## Objective
Turn the Mission 007 synthetic fixture core into a local synthetic OS workbench for the Personal Performance OS.

This mission proves a larger product slice while still avoiding all real/live integrations. It adds SQLite standard-library persistence, DB-backed replay, expanded deterministic primitives, evidence/report/conversation state, a localhost-only HTTP API, a static local web workbench, expanded DTU fixtures, and stronger verification.

## Prior Authority
- `.factory-v3/README.md`
- `.factory-v3/canons/POC_VISION.md`
- `.factory-v3/canons/POC_CONSTRAINTS.md`
- `.factory-v3/canons/POC_VERIFICATION.md`
- `.factory-v3/canons/DEPENDENCY_RESEARCH.md`
- `.factory-v3/evidence/MISSION_003_DTU_GOLDEN_FIXTURES.md`
- `.factory-v3/evidence/MISSION_003_ARCHITECTURE_PLAN.md`
- `.factory-v3/evidence/MISSION_003_VERIFICATION_PLAN.md`
- `.factory-v3/evidence/MISSION_004_SOURCE_ADAPTER_RESEARCH.md`
- `.factory-v3/evidence/MISSION_005_AMBIENT_AGENTIC_PARTNER.md`
- `.factory-v3/evidence/MISSION_006_LONG_HORIZON_ROADMAP.md`
- `.factory-v3/evidence/MISSION_006_ROADMAP_PLACEHOLDERS.md`
- `.factory-v3/missions/MISSION_007_SYNTHETIC_CORE_BUILD.md`
- `.factory-v3/evidence/MISSION_007_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_007_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_007_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_007_RECORD.json`

## Authorized Files And Directories
Mission/evidence:
- `.factory-v3/missions/MISSION_008_SYNTHETIC_LOCAL_OS_WORKBENCH.md`
- `.factory-v3/evidence/MISSION_008_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_008_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_008_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_008_RECORD.json`

App/source artifacts:
- `ppos_core/__init__.py`
- `ppos_core/schema.py`
- `ppos_core/loader.py`
- `ppos_core/primitives.py`
- `ppos_core/workflows.py`
- `ppos_core/reports.py`
- `ppos_core/storage.py`
- `ppos_core/replay.py`
- `ppos_core/api.py`
- `ppos_core/workbench.py`
- `ppos_core/migrations/*.sql`
- `fixtures/dtu/*.json`
- `tests/test_mission_007_core.py`
- `tests/test_mission_007_workflows.py`
- `tests/test_mission_008_storage.py`
- `tests/test_mission_008_replay.py`
- `tests/test_mission_008_primitives.py`
- `tests/test_mission_008_api.py`
- `tests/test_mission_008_workbench.py`
- `tests/test_mission_008_safety.py`
- `scripts/verify_mission_007.py`
- `scripts/verify_mission_008.py`
- `workbench/index.html`
- `workbench/styles.css`
- `workbench/app.js`

No other files are authorized unless this mission is halted and the user approves an explicit scope expansion.

## Dependency Policy
No package installation is approved.

Approved runtime:
- Python standard library only.

Approved modules:
- `sqlite3`
- `http.server`
- `json`
- `unittest`
- `pathlib`
- `dataclasses`
- `urllib.request` or `http.client` for localhost API tests

Forbidden during this mission:
- `pip install`, `npm install`, `brew install`, or any package manager.
- Garmin credentials, Garmin account login, API calls, scraping, or real Garmin data.
- Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, Telegram, OCR/vision, voice transcription, real medical PDF ingestion, scheduler, cron, notification delivery, queue, worker, daemon, webhook, polling, Hermes, public deployment, or Factory V2.

Rollback plan:
- SQLite databases created during tests must be temporary files under `/tmp` or in-memory handles only.
- If stdlib-only SQLite/API/static web cannot satisfy the gates, stop and record the missing capability. Do not install packages.

## Fixture Expansion Decision
Mission 008 targets 22 total DTU fixture files: the 9 Mission 007 fixtures plus 13 new fixtures. This is intentionally within the requested 18-22 fixture band.

New fixture files authorized:
- `dtu_late_high_fat_dinner_sleep_drop`
- `dtu_protein_distribution_recovery_improves`
- `dtu_weight_loss_plateau`
- `dtu_weight_loss_too_fast`
- `dtu_hard_session_suppressed_recovery`
- `dtu_contradictory_metrics`
- `dtu_nutrition_free_text`
- `dtu_morning_report_fatigue`
- `dtu_evening_report_recovery_setup`
- `dtu_weekly_review_progress`
- `dtu_proactive_suppressed_quiet_hours`
- `dtu_prior_recommendation_followup`
- `dtu_voice_continuation_as_synthetic_transcript`

Deferred as separate fixture files to respect the 18-22 fixture band:
- `dtu_deload_recovery`: covered in Mission 008 by `dtu_weekly_review_progress`, which includes deload and recovery-ramp expectations.
- `dtu_nutrition_label_basis_ambiguity`: covered in Mission 008 by existing `dtu_greek_yoghurt_label_image` label-basis/quantity ambiguity and by nutrition label capture tests.

This reduced fixture-set decision is made before implementation. If a separate named file for either deferred scenario proves necessary for a required gate, halt for scope expansion rather than exceeding the fixture band silently.

## Required Capabilities
1. SQLite persistence using `sqlite3` only:
   - migrations/schema setup,
   - idempotent fixture import,
   - raw source records separate from normalized facts,
   - fact provenance join table,
   - derived facts, workflow runs, evidence packs, conversation threads/messages, surface events, intent sessions, report candidates.
2. DB-backed replay:
   - import fixture into SQLite,
   - run workflows from DB state,
   - compare outputs to fixture expectations,
   - preserve evidence refs from source and derived facts.
3. Expanded deterministic primitives:
   - sleep cause analysis,
   - four-week training analysis,
   - recovery today,
   - ride/rest recommendation,
   - nutrition label capture,
   - nutrition free-text handling,
   - weight trend checks,
   - rapid weight-loss caution,
   - protein timing pattern,
   - deload recovery trend,
   - hard-session suppression,
   - contradictory metrics,
   - quiet-hours suppression simulation,
   - prior recommendation follow-up,
   - voice transcript continuity simulation.
4. Local HTTP API using `http.server` only:
   - `GET /api/health`
   - `GET /api/fixtures`
   - `GET /api/fixtures/{fixture_id}`
   - `POST /api/import-fixture`
   - `GET /api/imports`
   - `POST /api/workflows/run`
   - `GET /api/workflows/{run_id}`
   - `GET /api/evidence-packs/{evidence_pack_id}`
   - `GET /api/report-candidates`
   - `GET /api/conversation-threads/{thread_id}`
   - `GET /api/workbench/bootstrap`
5. Static local web workbench:
   - fixture selector,
   - fixture summary,
   - workflow runner,
   - evidence panel,
   - normalized/source provenance view,
   - derived facts view,
   - report candidate viewer,
   - cross-surface conversation simulation,
   - safety/compliance status panel.
6. Verification:
   - Mission 008 record JSON parses,
   - all fixture JSON parses,
   - DB schema migrates,
   - fixture import idempotent,
   - provenance preserved,
   - derived facts persist,
   - DB-backed workflow contracts pass,
   - report/conversation/cross-surface contracts pass,
   - HTTP API contract tests pass,
   - static workbench contract checks pass,
   - no live integrations, real data, packages, Factory V2, or Factory_V3 repo tooling were used.

## Allowed Commands
- `pwd`
- `find .factory-v3 -maxdepth 4 -type f | sort`
- `find ppos_core fixtures tests scripts workbench -maxdepth 5 -type f | sort`
- `python3 -m json.tool .factory-v3/evidence/MISSION_008_RECORD.json`
- `python3 -m json.tool fixtures/dtu/<fixture>.json`
- `python3 -B -m unittest discover -s tests`
- `python3 -B scripts/verify_mission_008.py`
- `python3 -B -m ppos_core.api --db /tmp/ppos_mission_008.sqlite --host 127.0.0.1 --port 0`
- `rg -n "factoryctl|stage-lint|pack-lint|Factory V2|Factory_V2|STAGE_A|STAGE_I2|Garmin credentials|Garmin Connect login|Apple Health live|Health Connect live|Strava API|Polar AccessLink|Telegram token|webhook_url|bot_token|api_token|ocr api|vision api|voice transcription api|real medical pdf|cron_expression|scheduler live|notification delivery|Hermes installed|Hermes configured" .factory-v3 ppos_core fixtures tests scripts workbench`

The scan is evidence-only. Expected matches may include forbidden/no-go wording in canons, missions, evidence, tests, fixture text, or verification marker strings. Any match indicating operational use, credentials, package installs, live integration, or V2 tooling is a halt.

## Phases
1. Mission envelope and evidence shell.
2. Implementation plan.
3. Source path authorization checkpoint.
4. Fixture expansion.
5. SQLite schema/migrations.
6. Fixture import and provenance persistence.
7. DB-backed primitives/workflows.
8. Report/conversation/cross-surface replay.
9. HTTP API.
10. Static web workbench.
11. Verification harness.
12. Final verification, drift audit, closeout, and mission record.

## Gates
- Gate A: prior fixture definitions exist.
- Gate B: expanded fixture files exist and parse.
- Gate C: schema/loader can load fixtures.
- Gate D: SQLite schema migrates.
- Gate E: fixture import is idempotent and preserves provenance.
- Gate F: deterministic primitives pass.
- Gate G: DB-backed workflow contracts pass.
- Gate H: report/conversation/cross-surface contracts pass.
- Gate I: HTTP API contract tests pass.
- Gate J: static workbench contract checks pass.
- Gate K: safety, V3-only, no-live-integration, no-real-data evidence passes.

Do not proceed past a failed gate unless the recovery is an implementation correction already authorized by this mission. Halt if failure implies scope expansion, real data, credentials, live integration, unapproved dependency, or V2.

## Required Checkpoints
Record checkpoints in `.factory-v3/evidence/MISSION_008_CHECKPOINTS.md` after:
1. mission envelope creation,
2. implementation plan creation,
3. source path authorization,
4. fixture expansion,
5. SQLite schema/migrations,
6. fixture import and provenance persistence,
7. DB-backed primitives/workflows,
8. report/conversation/cross-surface replay,
9. HTTP API,
10. static web workbench,
11. verification harness,
12. final verification/closeout.

Each checkpoint records phase, files changed, commands run, gate status, open risks, halt status, and next phase.

## Drift Audit
At each checkpoint and closeout, verify:
- edits are within authorized paths,
- no packages were installed,
- no live integrations were used,
- no real personal health data was used,
- no V2 tooling or Factory_V3 repo tooling was used,
- fixture gates are not bypassed,
- SQLite raw source, normalized facts, provenance, derived facts, workflows, evidence, reports, and conversation state remain separate.

## Reentry Rules
If interrupted or compacted, resume by reading:
1. this mission envelope,
2. `.factory-v3/evidence/MISSION_008_IMPLEMENTATION_PLAN.md`,
3. `.factory-v3/evidence/MISSION_008_CHECKPOINTS.md`,
4. current Mission 008 source/test/workbench files,
5. `.factory-v3/evidence/MISSION_008_CLOSEOUT.md` if present.

Continue only from the latest recorded checkpoint. Re-run the last gate before proceeding.

## Scope Expansion Policy
Allowed without new approval:
- Add helper functions inside authorized source files if needed for required fixtures, DB persistence, API contracts, or static workbench contracts.
- Add fixture fields inside authorized fixture files if needed to satisfy existing contracts.
- Add tests inside authorized test files for the required gates.

Requires halt and user approval:
- Any file path outside authorized paths.
- Any package installation.
- Any real data, credential, token, live API call, scheduler, notification, deployment, OCR/vision execution, voice transcription, real PDF ingestion, Hermes use, Factory V2, Factory_V3 repo tooling, or public deployment.
- Exceeding 22 total DTU fixture files.

## Halt Rules
Stop if:
- required behavior needs real Garmin, Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, Telegram, OCR/vision, voice transcription, medical PDF, scheduler, notification, Hermes, Factory V2, Factory_V3 repo tooling, package install, or public deployment,
- schema cannot preserve raw source provenance and normalized facts separately,
- DB-backed replay cannot preserve source and derived evidence refs,
- HTTP API requires public exposure or non-stdlib dependencies,
- static workbench requires package installation,
- tests require unapproved dependencies,
- verification cannot run locally,
- authorized paths or commands are insufficient,
- fixture failure reveals missing product scope rather than an implementation issue.

## Verification Commands
Minimum verification:

```bash
python3 -m json.tool .factory-v3/evidence/MISSION_008_RECORD.json
python3 -B -m unittest discover -s tests
python3 -B scripts/verify_mission_008.py
rg -n "factoryctl|stage-lint|pack-lint|Factory V2|Factory_V2|STAGE_A|STAGE_I2|Garmin credentials|Garmin Connect login|Apple Health live|Health Connect live|Strava API|Polar AccessLink|Telegram token|webhook_url|bot_token|api_token|ocr api|vision api|voice transcription api|real medical pdf|cron_expression|scheduler live|notification delivery|Hermes installed|Hermes configured" .factory-v3 ppos_core fixtures tests scripts workbench
```

## Pass Condition
- Mission 008 record parses as JSON.
- All 22 DTU fixture files parse and load.
- SQLite schema migrates.
- Fixture import is idempotent and preserves raw source, normalized facts, provenance links, derived facts, workflow runs, evidence packs, conversation state, surface events, intent sessions, and report candidates.
- DB-backed workflows pass fixture contracts.
- Report, conversation, and cross-surface replay contracts pass.
- HTTP API contract tests pass on localhost-only handler/server.
- Static workbench contract checks pass.
- No live integrations were used.
- No real data was used.
- No packages were installed.
- V3-only compliance is recorded.
