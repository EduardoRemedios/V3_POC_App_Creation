# Mission 012 Implementation Plan

## Mission
- Mission ID: MISSION_012_SYNTHETIC_IMPORT_HARDENING_AND_REAL_DATA_BRIDGE_DECISION
- Status: active until HDI-012-001 is asked, then paused for required cross-session resume.
- Profile: V3-POC-STANDALONE
- Data mode: synthetic only.

## Authority Summary
Execute only the files, commands, git operations, and verification paths authorized by `.factory-v3/missions/MISSION_012_SYNTHETIC_IMPORT_HARDENING_AND_REAL_DATA_BRIDGE_DECISION.md`.

Do not use Factory V2, real exports, credentials, package installation, live APIs, OCR/vision execution, voice transcription, schedulers, notifications, public deployment, or git operations outside the mission authority.

## Phase Plan

### Phase 1: Mission Plan And Interrupt Pause
- Author this implementation plan.
- Initialize `.factory-v3/evidence/MISSION_012_STATE.md`.
- Initialize `.factory-v3/evidence/MISSION_012_CHECKPOINTS.md`.
- Ask HDI-012-001 through `.factory-v3/evidence/MISSION_012_INTERRUPT_HDI001.json` with status `asked`.
- Commit checkpoint evidence using the authorized Mission 012 checkpoint message convention.
- End the session while HDI-012-001 remains `asked`.

### Phase 2: Fresh-Session Resume
- Resume only from the mission envelope, state file, latest checkpoint, interrupt JSON, and current repository state.
- Continue only if `.factory-v3/evidence/MISSION_012_INTERRUPT_HDI001.json` has status `answered` and a clear option selection.
- Apply the sponsor answer to the interrupt file by setting status `applied`, interpretation, continuation decision, and plan-delta handling.
- Record exactly which artifacts were read for resume.
- Commit the resume checkpoint.

### Phase 3: Review And Rollback Model
- Extend synthetic manual import persistence with review state per preview row.
- Add rollback provenance for committed synthetic import sessions without destructive audit deletion.
- Add or update migration `ppos_core/migrations/004_mission_012.sql`.
- Keep all data synthetic and local SQLite only.

### Phase 4: API And Workbench UX
- Expose review-state mutation, commit, rollback, and audit/provenance data through authorized API/workbench files.
- Add side-by-side raw/normalized diff rendering for preview rows.
- Surface accepted/rejected/needs-clarification states and rollback provenance in the workbench.

### Phase 5: Verification Harnesses
- Add Mission 012 unit tests for review workflow, rollback, and API behavior.
- Add `scripts/mission_012_review_rollback_qa.py`.
- Add `scripts/verify_mission_012.py` to validate envelope discipline, evidence completeness, interrupt lifecycle, checkpoint commits, budget state, JSON parsing, and no-go scope.

### Phase 6: Browser QA And Closeout
- Run full unit verification and Mission 012 verifier.
- Run local API server and Browser QA against `/workbench/`.
- Record `.factory-v3/evidence/MISSION_012_BROWSER_NOTES.md`.
- Write closeout, record, and audit summary.
- Commit final closeout with authorized paths only.

## Checkpoint Cadence
- M012-CP001: mission plan authored.
- M012-CP002: HDI-012-001 asked and mission paused.
- M012-CP003: bridge answer recorded while still paused for fresh-session resume.
- M012-CP004: fresh-session resume completed after sponsor answer.
- M012-CP005: review/rollback implementation completed.
- M012-CP006: persistence/API completed.
- M012-CP007: workbench UI completed.
- M012-CP008: verification and Browser QA completed.
- M012-CP009: final closeout completed.

## Plan Delta Rule
If the sponsor answer changes mission scope, create `.factory-v3/evidence/MISSION_012_PLAN_DELTA_001.md` before implementation proceeds. If no scope change is required, record why no delta was required in the interrupt and mission record.

## Budget Method
Every checkpoint records:
- Context usage estimate based on visible conversation/tool volume when exact harness percentage is unavailable.
- Tool-call count since the prior checkpoint, counting wrapped subcalls.
- Wall-clock estimate based on observed session elapsed time and command wall times.
- Stop-threshold judgment for whether the next phase plus a clean checkpoint is feasible.
