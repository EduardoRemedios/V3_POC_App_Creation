# Mission 011 Implementation Plan

## Status
APPROVED

## Baseline
- Current commit: `f52c940 Complete Mission 010 workbench QA readiness`
- Mission 010 made the synthetic workbench demoable and Browser-verified.

## Objective
Add a synthetic manual-import/source-adapter readiness lab that proves preview, validation, mapping, conflict detection, provenance, API, UI, and audit flows without using real data or live integrations.

## Phases
1. Mission envelope and initial adaptive state.
2. Synthetic manual export fixture family: manifest plus CSV/JSON synthetic export-like files.
3. Source-adapter module: registry, parsers, validation, mapping previews, conflict detection, provenance records.
4. SQLite persistence: import sessions, source files, preview rows, validation issues, mapping rows, conflict reports.
5. API endpoints and bootstrap integration.
6. Static workbench source-adapter lab view.
7. Stdlib QA harness and Mission 011 verifier.
8. Unit/API/workbench tests.
9. Built-in Browser QA.
10. Closeout, record, final audit summary.

## Authorized Implementation Detail
- `fixtures/manual_exports/`: synthetic files only. CSV/JSON content must be invented and labeled synthetic.
- `ppos_core/manual_imports.py`: no dependencies beyond stdlib.
- `ppos_core/migrations/003_mission_011.sql`: additive tables only.
- `ppos_core/storage.py`: functions for persisting and querying Mission 011 import sessions.
- `ppos_core/api.py`: localhost-only endpoints for adapter/import lab.
- `ppos_core/workbench.py`: bootstrap adapter/import metadata.
- `workbench/*`: add source-adapter lab view and controls.
- `scripts/*mission_011*` and `tests/test_mission_011_*`: verification only.

## Target Synthetic Export Families
- Garmin-like activity CSV.
- Sleep/recovery JSON.
- Weight/body composition CSV.
- Nutrition free-text JSON.
- Multi-source mixed bundle.
- Malformed missing observed time.
- Duplicate activity rows.
- Unit ambiguity/conflict edge case.
- Timezone boundary edge case.

## API Targets
- `GET /api/source-adapters`
- `GET /api/manual-exports`
- `GET /api/manual-exports/{export_id}`
- `POST /api/manual-imports/preview`
- `POST /api/manual-imports/commit-synthetic`
- `GET /api/manual-imports/sessions`
- `GET /api/manual-imports/sessions/{session_id}`
- `GET /api/manual-imports/{session_id}/mapping`
- `GET /api/manual-imports/{session_id}/conflicts`
- `GET /api/manual-imports/audit-summary`

## Verification Commands
- `python3 -B -m unittest discover -s tests`
- `python3 -B scripts/mission_011_import_lab_qa.py --db /tmp/ppos_mission_011_qa.sqlite --host 127.0.0.1 --port 8780`
- `python3 -B scripts/verify_mission_011.py`
- `python3 -m json.tool .factory-v3/evidence/MISSION_011_RECORD.json`
- `python3 -m json.tool .factory-v3/evidence/MISSION_011_AUDIT_SUMMARY.json`
- `python3 -m json.tool fixtures/manual_exports/manifest.json`

## Browser QA Plan
- Start local API on `127.0.0.1:8780`.
- Open `/workbench/?view=imports` in built-in Browser.
- Verify adapter catalog, export selector, preview button, commit button, mapping list, validation issue list, conflict list, and audit summary.
- Run preview/commit flow for a synthetic export with duplicate/conflict coverage.
- Verify no runtime QA errors and no unexpected overflow at desktop/mobile.
- Attempt screenshots through Browser; do not persist screenshot files unless a later plan delta authorizes paths.

## Halt/Interrupt Conditions
- Interrupt for any real sample data request.
- Interrupt for package install or parser dependency.
- Interrupt for git write operations.
- Halt on live integration or credential pressure.
