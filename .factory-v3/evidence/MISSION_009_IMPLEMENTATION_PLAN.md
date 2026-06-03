# Mission 009 Implementation Plan

## Status
IN_PROGRESS

## Build Choice
Continue the Mission 008 stack:
- Python standard library only.
- `sqlite3` for local durable synthetic persistence.
- `http.server` for localhost-only API and static workbench serving.
- Static HTML/CSS/JS for the workbench.
- Standard-library `unittest` plus verification scripts.

No package installation is approved or needed.

## Source Shape
Preserve Mission 007/008 modules and add focused Mission 009 modules:
- `ppos_core/fixture_manifest.py`: fixture index parsing, family coverage, workflow/API matrices.
- `ppos_core/repositories.py`: query service/repository objects over SQLite.
- `ppos_core/timeline.py`: workflow replay timeline persistence and comparison.
- `ppos_core/evidence_graph.py`: graph node/edge construction and queries.
- `ppos_core/recommendations.py`: recommendation history, follow-up outcomes, report settings.
- `ppos_core/safety_audit.py`: safety boundary and no-delivery audit records.
- `ppos_core/snapshots.py`: snapshot export/import validation.
- `ppos_core/api_contracts.py`: endpoint matrix and problem-detail-like error examples.
- `ppos_core/audit.py`: generated audit summary payload.

## Fixture Plan
Total executable fixtures: 36.

Keep all 22 Mission 008 fixture files.

Add 14 Mission 009 fixture files:
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

Add `fixtures/dtu_manifest.json` with:
- family metadata,
- risk coverage metadata,
- expected workflow matrix,
- expected API coverage matrix,
- expected negative/edge-case classification.

## SQLite Schema Plan
Keep `001_initial.sql` intact and add `002_mission_009.sql`.

New tables:
- `fixture_families`
- `fixture_manifest_entries`
- `fixture_risk_coverage`
- `fixture_expected_workflows`
- `fixture_expected_api_cases`
- `workflow_timeline_steps`
- `replay_audit_summaries`
- `evidence_graph_nodes`
- `evidence_graph_edges`
- `recommendations`
- `follow_up_outcomes`
- `report_settings`
- `safety_boundary_events`
- `api_contract_cases`
- `snapshot_exports`

## Repository And Query Plan
Implement query services for:
- source records,
- normalized facts,
- derived facts,
- evidence graph,
- workflow timeline,
- conversation state,
- report/recommendation/follow-up state,
- import/replay audit state,
- snapshot export/validation.

## API Plan
Keep all Mission 008 endpoints and add:
- `GET /api/fixture-manifest`
- `GET /api/fixture-families`
- `GET /api/fixtures/expected-workflows`
- `GET /api/imports/audit-summary`
- `GET /api/workflows/{run_id}/timeline`
- `GET /api/evidence-graph`
- `GET /api/evidence-graph/{fixture_id}`
- `GET /api/recommendations`
- `GET /api/follow-up-outcomes`
- `GET /api/report-settings`
- `GET /api/safety-audit`
- `GET /api/snapshot/export`
- `POST /api/snapshot/validate-import`
- `GET /api/contracts`
- `GET /api/error-examples`
- static workbench serving at `/`, `/workbench/styles.css`, and `/workbench/app.js`.

Error responses should use a problem-detail-like JSON shape:
- `type`
- `title`
- `status`
- `detail`
- optional `instance`
- optional `field`

## Workbench Plan
Replace the basic Mission 008 page with an 8-view static product workbench:
- fixture catalog/family view,
- replay debugger/timeline view,
- evidence graph view,
- workflow/API runner view,
- reports view,
- conversation continuity view,
- recommendations/follow-up view,
- safety/audit view.

Use no framework, no CDN, no build, and no decorative landing page.

## Browser/UI QA Plan
Preferred:
- run `python3 -B -m ppos_core.api --db /tmp/ppos_mission_009_browser.sqlite --host 127.0.0.1 --port 8765`,
- use Browser plugin to open `http://127.0.0.1:8765/`,
- check page identity, nonblank render, no console errors, mount points, fixture selection, workflow/API runner, desktop screenshot, and mobile layout.

Fallback:
- if Browser plugin or already available browser tooling is unavailable/blocked, run `python3 -B scripts/mission_009_browser_smoke.py --db /tmp/ppos_mission_009_browser.sqlite --host 127.0.0.1 --port 8765`.
- The fallback must record that it is not equivalent to visual browser QA.

## Test Plan
Use standard-library `unittest`.

Target total checks:
- Existing 66 tests remain.
- Add 75-95 Mission 009 tests/checks across new test files and verification harness.
- Final closeout will report actual test/check count.

Gate coverage:
- Gate D/E: `test_mission_009_manifest.py`.
- Gate F/G: `test_mission_009_repositories.py`.
- Gate H: `test_mission_009_timeline.py`.
- Gate I: `test_mission_009_evidence_graph.py`.
- Gate J: `test_mission_009_recommendations.py`.
- Gate L: `test_mission_009_api.py`.
- Gate M/N: `test_mission_009_workbench.py` and browser smoke script.
- Gate O/P: `test_mission_009_audit.py` and `scripts/verify_mission_009.py`.

## Verification Commands
```bash
python3 -m json.tool .factory-v3/evidence/MISSION_009_RECORD.json
python3 -m json.tool .factory-v3/evidence/MISSION_009_AUDIT_SUMMARY.json
python3 -m json.tool fixtures/dtu_manifest.json
python3 -B -m unittest discover -s tests
python3 -B scripts/verify_mission_009.py
python3 -B scripts/mission_009_browser_smoke.py --db /tmp/ppos_mission_009_browser.sqlite --host 127.0.0.1 --port 8765
rg -n "factoryctl|stage-lint|pack-lint|Factory V2|Factory_V2|STAGE_A|STAGE_I2|Garmin credentials|Garmin Connect login|Apple Health live|Health Connect live|Strava API|Polar AccessLink|Telegram token|webhook_url|bot_token|api_token|ocr api|vision api|voice transcription api|real medical pdf|cron_expression|scheduler live|notification delivery|Hermes installed|Hermes configured|Factory_V3 repo tooling" .factory-v3 ppos_core fixtures tests scripts workbench
```

## Drift Guardrails
- Keep all edits inside authorized paths.
- Do not install packages.
- Do not start public servers.
- Use only synthetic fixture data.
- Treat image and voice inputs as prewritten synthetic metadata/transcripts only.
- Do not implement scheduler, queue, worker, daemon, cron, webhook, polling, or notification delivery.
- Keep API and workbench local-only.
- Record any size tradeoff honestly in closeout.
