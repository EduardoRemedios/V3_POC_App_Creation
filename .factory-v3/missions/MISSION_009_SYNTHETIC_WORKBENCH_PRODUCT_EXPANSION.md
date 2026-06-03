# Mission 009 Synthetic Workbench Product Expansion

## Status
IN_PROGRESS

## Mission Type
long_horizon_build

## Duration Band
one_hour_plus_long_horizon

## Objective
Expand the Mission 008 synthetic-only local OS workbench into a richer local product workbench for the Personal Performance OS.

This mission proves a larger end-to-end synthetic operating environment with expanded fixture families, a fixture manifest/index, richer SQLite repositories and query services, replay timeline debugging, evidence graph queries, recommendation history, follow-up outcomes, report settings, safety/audit surfaces, expanded localhost-only API contracts, multi-view static workbench UI, browser/UI smoke evidence where feasible, and a generated machine-readable audit summary.

No real data, live integrations, package installation, public deployment, schedulers, notifications, OCR/vision execution, voice transcription execution, real medical PDF ingestion, Hermes, Factory V2, or Factory_V3 repo tooling are authorized.

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
- `.factory-v3/missions/MISSION_008_SYNTHETIC_LOCAL_OS_WORKBENCH.md`
- `.factory-v3/evidence/MISSION_008_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_008_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_008_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_008_RECORD.json`

## Required Outputs
Mission/evidence:
- `.factory-v3/missions/MISSION_009_SYNTHETIC_WORKBENCH_PRODUCT_EXPANSION.md`
- `.factory-v3/evidence/MISSION_009_RESEARCH_SPIKES.md`
- `.factory-v3/evidence/MISSION_009_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_009_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_009_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_009_RECORD.json`
- `.factory-v3/evidence/MISSION_009_AUDIT_SUMMARY.json`

## Authorized Files And Directories
Mission/evidence:
- `.factory-v3/missions/MISSION_009_SYNTHETIC_WORKBENCH_PRODUCT_EXPANSION.md`
- `.factory-v3/evidence/MISSION_009_RESEARCH_SPIKES.md`
- `.factory-v3/evidence/MISSION_009_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_009_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_009_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_009_RECORD.json`
- `.factory-v3/evidence/MISSION_009_AUDIT_SUMMARY.json`

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
- `ppos_core/fixture_manifest.py`
- `ppos_core/repositories.py`
- `ppos_core/timeline.py`
- `ppos_core/evidence_graph.py`
- `ppos_core/recommendations.py`
- `ppos_core/safety_audit.py`
- `ppos_core/snapshots.py`
- `ppos_core/api_contracts.py`
- `ppos_core/audit.py`
- `ppos_core/migrations/*.sql`
- `fixtures/dtu/*.json`
- `fixtures/dtu_manifest.json`
- `tests/test_mission_007_core.py`
- `tests/test_mission_007_workflows.py`
- `tests/test_mission_008_storage.py`
- `tests/test_mission_008_replay.py`
- `tests/test_mission_008_primitives.py`
- `tests/test_mission_008_api.py`
- `tests/test_mission_008_workbench.py`
- `tests/test_mission_008_safety.py`
- `tests/test_mission_009_manifest.py`
- `tests/test_mission_009_repositories.py`
- `tests/test_mission_009_timeline.py`
- `tests/test_mission_009_evidence_graph.py`
- `tests/test_mission_009_recommendations.py`
- `tests/test_mission_009_api.py`
- `tests/test_mission_009_workbench.py`
- `tests/test_mission_009_audit.py`
- `scripts/verify_mission_007.py`
- `scripts/verify_mission_008.py`
- `scripts/verify_mission_009.py`
- `scripts/mission_009_browser_smoke.py`
- `workbench/index.html`
- `workbench/styles.css`
- `workbench/app.js`

No other files are authorized unless this mission halts and the user approves a scope expansion.

## Dependency Policy
No package installation is approved by default.

Approved runtime/modules:
- Python standard library only.
- `sqlite3`, `http.server`, `json`, `unittest`, `pathlib`, `dataclasses`, `urllib.request`, `http.client`, `subprocess`, `socket`, `threading`, and `tempfile`.
- Static HTML/CSS/JS with browser-native APIs only.

Browser/UI QA may use already available Codex Browser or already available Playwright/browser tooling. This does not authorize package installation. If browser tooling requires a package install or unavailable runtime, halt browser QA and record a justified static-contract fallback in closeout and audit summary.

Forbidden during this mission:
- `pip install`, `npm install`, `pnpm install`, `yarn install`, `brew install`, or any package manager.
- Garmin credentials, Garmin account login, API calls, scraping, or real Garmin data.
- Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava live integration.
- Telegram bot/token/webhook/polling/live traffic.
- OCR/vision execution.
- Voice transcription execution.
- Real medical PDF ingestion.
- Scheduler, cron, worker, daemon, queue, or notification delivery.
- Hermes installation/configuration/use.
- Public deployment.
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or Factory_V3 repo tooling.

Rollback plan:
- SQLite databases created during tests and browser smoke must be temporary files under `/tmp` or in-memory handles only.
- The stdlib server may bind only to `127.0.0.1` or `localhost` and must be stopped after QA.
- If a dependency is needed, stop and record the dependency gap. Do not install packages.
- If the 35-fixture minimum cannot be met, halt before implementation unless a reduced fixture count is explicitly justified here. This mission does not justify a reduced fixture count.

## Research Spikes
Bounded public web research is authorized for:
- SQLite local-first app/replay/audit patterns.
- Static no-build dashboard/workbench UI patterns.
- Evidence/provenance graph UI patterns.
- Health/performance coaching safety language boundaries.
- API contract/error-shape patterns for local tools.
- Browser smoke testing approaches for static/local stdlib apps.

Research constraints:
- Public documentation/articles only.
- No credentials, private accounts, live integrations, package installs, or external service calls beyond public web page reads.
- Record citations and practical implications in `.factory-v3/evidence/MISSION_009_RESEARCH_SPIKES.md`.

## Fixture Expansion Decision
Mission 009 must keep all 22 Mission 008 fixture files and expand to 35-45 total DTU fixtures.

Target total: 36 DTU fixture files.

New fixture files authorized:
- `dtu_deload_recovery`
- `dtu_nutrition_label_basis_ambiguity`
- `dtu_sleep_recovery_low_hrv_edge`
- `dtu_training_ramp_too_fast`
- `dtu_body_composition_recomp`
- `dtu_report_settings_quiet_depth`
- `dtu_weekly_report_suppressed_cooldown`
- `dtu_cross_surface_report_review`
- `dtu_synthetic_voice_followup_outcome`
- `dtu_malformed_missing_observed_at`
- `dtu_incomplete_source_payload`
- `dtu_evidence_orphan_ref`
- `dtu_api_unknown_workflow`
- `dtu_snapshot_export_roundtrip`

If implementation reveals that fewer than 35 fixture files are technically cleaner, halt before fixture implementation unless a user-approved mission update changes this count.

## Required Capabilities
1. Fixture manifest and families:
   - `fixtures/dtu_manifest.json`,
   - family/category metadata,
   - risk coverage metadata,
   - expected workflow matrix,
   - expected API coverage matrix,
   - parse and consistency tests.
2. SQLite repository/query layer:
   - migration/schema setup with Mission 009 tables,
   - repository/query classes or equivalent module functions,
   - source, normalized, derived, evidence graph, timeline, conversation, report, recommendation, follow-up, audit, and snapshot queries.
3. Replay timeline debugger:
   - persist workflow steps/intermediate results,
   - expose replay timeline records,
   - compare timeline to fixture expectations,
   - show evidence used at each step,
   - support replay audit summary.
4. Evidence graph:
   - nodes/edges for source records, normalized facts, derived facts, evidence packs, workflow runs, reports, recommendations, and follow-ups,
   - query graph by fixture/workflow/evidence pack,
   - expose through API and static workbench.
5. Recommendation history and follow-up outcomes:
   - persist recommendation records,
   - persist follow-up outcome records,
   - link to prior evidence and conversation thread,
   - verify prior recommendation follow-up behavior.
6. Report settings and safety/audit state:
   - report preferences/settings records,
   - quiet-hours/cooldown simulation,
   - report candidate severity/confidence,
   - safety boundary records,
   - no-delivery status,
   - audit summary generation.
7. Expanded localhost-only HTTP API:
   - all Mission 008 endpoints,
   - fixture manifest,
   - fixture families,
   - expected workflow matrix,
   - import/replay audit summary,
   - workflow timeline,
   - evidence graph,
   - recommendations,
   - follow-up outcomes,
   - report settings,
   - safety audit,
   - snapshot export,
   - snapshot import validation,
   - API error contract examples.
8. Multi-view static web workbench:
   - fixture catalog/family view,
   - replay debugger/timeline view,
   - evidence graph view,
   - workflow/API runner view,
   - reports view,
   - conversation continuity view,
   - recommendations/follow-up view,
   - safety/audit view.
9. Browser/UI QA:
   - run localhost stdlib server if feasible,
   - verify workbench loads, no console errors, key panels mount, fixture selection works, workflow/API runner works, and desktop/mobile layouts do not visibly overlap,
   - record fallback reason if Browser/Playwright is unavailable or blocked.
10. Audit summary:
   - generate `.factory-v3/evidence/MISSION_009_AUDIT_SUMMARY.json` with fixture count/families, tests/checks, DB tables, API endpoints, workbench views, gates, commands, dependency review, V3-only/no-live/no-real-data compliance, and residual risks.

## Allowed Commands
- `pwd`
- `rg --files .factory-v3 ppos_core fixtures tests scripts workbench`
- `find .factory-v3 -maxdepth 4 -type f | sort`
- `find ppos_core fixtures tests scripts workbench -maxdepth 5 -type f | sort`
- `python3 -m json.tool .factory-v3/evidence/MISSION_009_RECORD.json`
- `python3 -m json.tool .factory-v3/evidence/MISSION_009_AUDIT_SUMMARY.json`
- `python3 -m json.tool fixtures/dtu_manifest.json`
- `python3 -m json.tool fixtures/dtu/<fixture>.json`
- `python3 -B -m unittest discover -s tests`
- `python3 -B scripts/verify_mission_009.py`
- `python3 -B scripts/mission_009_browser_smoke.py --db /tmp/ppos_mission_009_browser.sqlite --host 127.0.0.1 --port 8765`
- `python3 -B -m ppos_core.api --db /tmp/ppos_mission_009.sqlite --host 127.0.0.1 --port 8765`
- Browser plugin or already available Playwright/browser runtime commands for localhost smoke only, with no install.
- `rg -n "factoryctl|stage-lint|pack-lint|Factory V2|Factory_V2|STAGE_A|STAGE_I2|Garmin credentials|Garmin Connect login|Apple Health live|Health Connect live|Strava API|Polar AccessLink|Telegram token|webhook_url|bot_token|api_token|ocr api|vision api|voice transcription api|real medical pdf|cron_expression|scheduler live|notification delivery|Hermes installed|Hermes configured|Factory_V3 repo tooling" .factory-v3 ppos_core fixtures tests scripts workbench`

The `rg` scan is evidence-only. Expected matches may include forbidden/no-go wording, prior evidence, source research text, synthetic fixture text, or verification marker strings. Any match indicating operational use, credentials, package installs, live integration, V2 tooling, or Factory_V3 repo tooling is a halt.

## Phases
1. Mission envelope creation.
2. Research spikes.
3. Implementation plan/checkpoint/record/audit shell.
4. Source path authorization checkpoint.
5. Fixture manifest/family design.
6. Fixture expansion to 35-45 fixtures.
7. SQLite schema/repositories.
8. Import/replay audit persistence.
9. Workflow timeline debugger.
10. Evidence graph.
11. Recommendations/follow-up/report settings/safety state.
12. Expanded HTTP API and error matrix.
13. Static multi-view workbench.
14. Browser/UI QA or documented fallback.
15. Verification harness/audit summary.
16. Final verification/closeout.

## Required Checkpoints
Record checkpoints in `.factory-v3/evidence/MISSION_009_CHECKPOINTS.md` after:
1. mission envelope creation,
2. research spikes,
3. implementation plan creation,
4. source path authorization,
5. fixture manifest/family design,
6. fixture expansion,
7. SQLite schema/repositories,
8. import/replay audit persistence,
9. workflow timeline debugger,
10. evidence graph,
11. recommendations/follow-up/report settings,
12. expanded HTTP API,
13. static multi-view workbench,
14. browser/UI QA or fallback,
15. verification harness/audit summary,
16. final verification/closeout.

Each checkpoint records phase, files changed, commands run, gate status, open risks, halt status, and next phase.

## Gates
- Gate A: prior mission evidence exists.
- Gate B: research spikes complete and cited.
- Gate C: mission envelope/plan/checkpoint/record shell complete.
- Gate D: fixture manifest and 35-45 fixtures exist and parse.
- Gate E: manifest consistency and fixture family coverage pass.
- Gate F: schema/repositories migrate.
- Gate G: fixture import idempotent and preserves provenance.
- Gate H: replay timeline persistence passes.
- Gate I: evidence graph contracts pass.
- Gate J: recommendation/follow-up/report settings contracts pass.
- Gate K: DB-backed workflow contracts pass.
- Gate L: HTTP API matrix and error contracts pass.
- Gate M: static workbench contract checks pass.
- Gate N: browser/UI smoke passes or fallback is justified.
- Gate O: audit summary JSON passes.
- Gate P: safety, V3-only, no-live-integration, no-real-data, no-package evidence passes.

Do not proceed past a failed gate unless the recovery is an implementation bug within authorized scope. Halt if the failure implies scope expansion, real data, credentials, live integration, unapproved dependency, V2, Factory_V3 repo tooling, scheduler/notification behavior, or package installation.

## Drift Audit
At each checkpoint and closeout, verify:
- edits are within authorized paths,
- no packages were installed,
- no live integrations were used,
- no real personal health data was used,
- no V2 tooling or Factory_V3 repo tooling was used,
- fixture gates are not bypassed,
- SQLite raw source, normalized facts, provenance, derived facts, workflows, timeline, evidence graph, reports, recommendations, follow-ups, safety state, and conversation state remain separate.

## Reentry Rules
If interrupted or compacted, resume by reading:
1. this mission envelope,
2. `.factory-v3/evidence/MISSION_009_RESEARCH_SPIKES.md`,
3. `.factory-v3/evidence/MISSION_009_IMPLEMENTATION_PLAN.md`,
4. `.factory-v3/evidence/MISSION_009_CHECKPOINTS.md`,
5. current Mission 009 source/test/workbench files,
6. `.factory-v3/evidence/MISSION_009_CLOSEOUT.md` if present.

Continue only from the latest recorded checkpoint. Re-run the last gate before proceeding.

## Scope Expansion Policy
Allowed without new approval:
- Add helper functions inside authorized source files if needed for required fixtures, DB persistence, API contracts, workbench contracts, browser smoke, or audit summary.
- Add fixture fields inside authorized fixture files if needed to satisfy existing contracts.
- Add tests inside authorized test files for required gates.
- Add static UI sections inside authorized workbench files for required views.

Requires halt and user approval:
- Any file path outside authorized paths.
- Any package installation.
- Any real data, credential, token, live API call, scheduler, notification, deployment, OCR/vision execution, voice transcription, real PDF ingestion, Hermes use, Factory V2, Factory_V3 repo tooling, or public deployment.
- Fewer than 35 fixture files.
- More than 45 fixture files.

## Verification Commands
Minimum verification:

```bash
python3 -m json.tool .factory-v3/evidence/MISSION_009_RECORD.json
python3 -m json.tool .factory-v3/evidence/MISSION_009_AUDIT_SUMMARY.json
python3 -m json.tool fixtures/dtu_manifest.json
python3 -B -m unittest discover -s tests
python3 -B scripts/verify_mission_009.py
python3 -B scripts/mission_009_browser_smoke.py --db /tmp/ppos_mission_009_browser.sqlite --host 127.0.0.1 --port 8765
rg -n "factoryctl|stage-lint|pack-lint|Factory V2|Factory_V2|STAGE_A|STAGE_I2|Garmin credentials|Garmin Connect login|Apple Health live|Health Connect live|Strava API|Polar AccessLink|Telegram token|webhook_url|bot_token|api_token|ocr api|vision api|voice transcription api|real medical pdf|cron_expression|scheduler live|notification delivery|Hermes installed|Hermes configured|Factory_V3 repo tooling" .factory-v3 ppos_core fixtures tests scripts workbench
```

Browser plugin smoke is preferred when available. The stdlib browser smoke script is an authorized fallback only when it uses no package install and verifies localhost HTML/API contracts.

## Pass Condition
- Required Mission 009 evidence files exist.
- Mission 009 record parses as JSON.
- Mission 009 audit summary parses as JSON.
- Research spike evidence exists with citations.
- All fixture JSON files parse.
- Fixture manifest parses and matches fixture files.
- 35-45 DTU fixtures exist.
- DB schema migrates.
- Repository/query tests pass.
- Fixture import is idempotent.
- Raw source provenance is preserved.
- Normalized facts link to source records.
- Derived facts persist.
- Workflow timelines persist.
- Evidence graph contracts pass.
- Recommendation/follow-up contracts pass.
- Report settings and safety/audit contracts pass.
- DB-backed workflows pass fixture contracts.
- HTTP API contract matrix and error contracts pass.
- Static workbench files exist and contain expected views/mount points/API calls.
- Browser/UI smoke checks pass or fallback is justified.
- No live integrations were used.
- No real data was used.
- No packages were installed.
- V2/no-go scan finds only forbidden/no-go wording, prior evidence, synthetic fixture text, research text, or verification marker strings.
