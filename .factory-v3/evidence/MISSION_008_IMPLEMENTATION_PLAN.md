# Mission 008 Implementation Plan

## Status
IN_PROGRESS

## Build Choice
Use Python standard-library modules only:
- `sqlite3` for durable local persistence,
- `http.server` for a localhost-only API,
- `json`, `pathlib`, `dataclasses`, and `unittest` for fixtures and verification,
- static HTML/CSS/JS for the workbench.

No package installation is approved or needed.

## Authorized Source Shape
- Keep Mission 007 in-memory fixture loading intact.
- Add `ppos_core/storage.py` for migrations, SQLite import, idempotency, and repositories.
- Add `ppos_core/replay.py` for reconstructing DB-backed fixture state and running workflows from persisted state.
- Add `ppos_core/api.py` for a stdlib HTTP API and testable request handlers.
- Add `ppos_core/workbench.py` for bootstrap payload helpers.
- Add `ppos_core/migrations/001_initial.sql` for schema setup.
- Add static files under `workbench/`.

## Fixture Plan
Total executable fixtures: 22.

Keep Mission 007 fixtures:
- `dtu_baseline_healthy_week`
- `dtu_accumulated_fatigue`
- `dtu_missing_data`
- `dtu_duplicate_import`
- `dtu_timezone_boundary`
- `dtu_greek_yoghurt_label_image`
- `dtu_cross_surface_recovery_handoff`
- `dtu_morning_report_normal`
- `dtu_evening_report_nutrition_gap`

Add Mission 008 fixtures:
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

Deferred separately named fixture files:
- `dtu_deload_recovery`, covered in `dtu_weekly_review_progress`.
- `dtu_nutrition_label_basis_ambiguity`, covered in `dtu_greek_yoghurt_label_image`.

## SQLite Schema Plan
Tables:
- `schema_migrations`
- `fixture_imports`
- `source_records`
- `normalized_facts`
- `fact_provenance`
- `derived_facts`
- `evidence_packs`
- `evidence_refs`
- `conversation_threads`
- `conversation_messages`
- `surface_events`
- `intent_sessions`
- `workflow_runs`
- `report_candidates`

Idempotency:
- `fixture_imports.fixture_id` is unique.
- `source_records`, `normalized_facts`, and other persisted rows are unique by fixture-scoped IDs.
- Re-import deletes and rewrites fixture-owned rows inside a transaction while preserving a stable import row and incrementing `import_count`.

## Workflow Plan
Extend deterministic summaries and workflows with fixture-driven contracts for:
- sleep cause analysis,
- four-week training analysis,
- recovery today,
- ride/rest recommendation,
- nutrition label capture,
- nutrition free-text clarification,
- weight trend checks,
- rapid weight-loss caution,
- protein timing pattern,
- deload recovery trend,
- hard-session suppression,
- contradictory metrics,
- quiet-hours suppression simulation,
- prior recommendation follow-up,
- synthetic voice transcript continuity.

## API Plan
Expose localhost-only JSON routes:
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

The API module must be testable without opening a public server. Server CLI binds to `127.0.0.1` only.

## Static Workbench Plan
Create:
- `workbench/index.html`
- `workbench/styles.css`
- `workbench/app.js`

Required mount points/API calls:
- fixture selector,
- fixture summary,
- workflow runner,
- evidence panel,
- provenance panel,
- derived facts panel,
- report candidate viewer,
- conversation simulation,
- safety/compliance panel.

## Test Plan
Use standard-library `unittest`.

Gate coverage:
- Gate B/C: existing Mission 007 tests plus expanded fixture load tests.
- Gate D/E: `test_mission_008_storage.py`.
- Gate F/G/H: `test_mission_008_primitives.py`, `test_mission_008_replay.py`, `test_mission_008_safety.py`.
- Gate I: `test_mission_008_api.py`.
- Gate J: `test_mission_008_workbench.py`.
- Gate K: `scripts/verify_mission_008.py`.

Target test count: 40-70 tests across Mission 007 and Mission 008 test files.

## Verification Commands
```bash
python3 -m json.tool .factory-v3/evidence/MISSION_008_RECORD.json
python3 -B -m unittest discover -s tests
python3 -B scripts/verify_mission_008.py
rg -n "factoryctl|stage-lint|pack-lint|Factory V2|Factory_V2|STAGE_A|STAGE_I2|Garmin credentials|Garmin Connect login|Apple Health live|Health Connect live|Strava API|Polar AccessLink|Telegram token|webhook_url|bot_token|api_token|ocr api|vision api|voice transcription api|real medical pdf|cron_expression|scheduler live|notification delivery|Hermes installed|Hermes configured" .factory-v3 ppos_core fixtures tests scripts workbench
```

## Drift Guardrails
- Keep all edits inside authorized paths.
- Do not install packages.
- Do not start public servers.
- Use only synthetic fixture data.
- Treat image and voice inputs as prewritten synthetic metadata/transcripts only.
- Do not implement scheduler, queue, worker, daemon, cron, webhook, polling, or notification delivery.
- Keep API and static workbench local-only.
