# Mission 013 Implementation Plan

## Mission
- Mission ID: MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS
- Status: active until a required human decision interrupt becomes blocking or the deliberate resume boundary is reached.
- Profile: V3-POC-STANDALONE
- Data mode: synthetic only; no real Garmin exports, accounts, credentials, API calls, scraping, or sample files.

## Authority Summary
Execute only the files, commands, git operations, verification paths, and public-documentation research authorized by `.factory-v3/missions/MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS.md`.

Do not use Factory V2, Factory_V3 tooling, real personal data, public sample export files, live integrations, package installation, OCR/vision, voice transcription, schedulers, notifications, public deployment, or unauthorized git operations.

## Phase Plan

### Phase 1: Mission Control Setup
- Author this implementation plan.
- Initialize `.factory-v3/evidence/MISSION_013_STATE.md`.
- Initialize `.factory-v3/evidence/MISSION_013_CHECKPOINTS.md`.
- Commit checkpoint 001 with the authorized Mission 013 checkpoint convention.

### Phase 2: Garmin Public Shape Research
- Research only public documentation pages about Garmin manual export surfaces and documented field/format hints.
- Do not log in, create accounts, download export files, or use public sample exports that may contain real-person data.
- Write `.factory-v3/evidence/MISSION_013_GARMIN_EXPORT_SHAPE_RESEARCH.md` with citations, synthesis, timestamp/unit/duplicate implications, and synthetic fixture design constraints.
- Commit checkpoint 002.

### Phase 3: HDI-013-001 Fixture Scope And Retention
- Write `.factory-v3/evidence/MISSION_013_INTERRUPT_HDI001.json` with status `asked`.
- Record checkpoint 003 and commit it before asking in-thread.
- Ask the sponsor to answer from the phone via Codex in the ChatGPT mobile app when possible; record the actual surface honestly.
- If unanswered and blocking, pause. If answered clearly, apply the interrupt without fabricating defaults.

### Phase 4: Fixture Pack And Garmin Adapter
- Apply HDI-013-001.
- Create `fixtures/garmin_exports/` with a manifest and Garmin-shaped synthetic fixture families.
- Implement `ppos_core/garmin_bridge.py` and integrate it through `ppos_core/manual_imports.py`.
- Ensure preview, validation, duplicate, timezone, unit-conflict, missing-field, and malformed-row behaviors are exercised.
- Commit checkpoints 004 and 005 as fixture and adapter milestones complete.

### Phase 5: HDI-013-002 And Fact Materialization
- Ask/apply HDI-013-002 before finalizing conflict behavior.
- Add `ppos_core/migrations/005_mission_013.sql`.
- Materialize accepted reviewed imports into normalized fact tables with source identity, file hash, observed/ingested time, mapping reference, confidence, and synthetic labels.
- Implement the selected conflict strategy and preserve audit provenance.
- Commit checkpoint 006.

### Phase 6: Deliberate Resume Boundary
- At a natural boundary after materialization, write checkpoint 007, commit it, and end the session.
- The fresh session must resume from authored artifacts only and list exactly what it read in the state file.

### Phase 7: Rollback And Surface Integration
- Implement fact-level rollback that un-materializes imported facts without deleting audit history.
- Flow imported facts into timelines, evidence graph, and at least two workflow/report candidates with evidence references.
- Commit checkpoints 008 and 009.

### Phase 8: Approval UX And Verification
- Implement the synthetic future real-data approval UX from Mission 012 design: consent recording, source labeling, retention choice, and approval state surfaces.
- Exercise only synthetic fixtures.
- Add Mission 013 QA and verification scripts plus focused tests.
- Run stdlib unit tests, Mission 013 QA, JSON parse checks, verifier, and Browser QA against the local workbench.
- Commit checkpoint 010.

### Phase 9: Closeout
- Write closeout, mission record, audit summary, and browser notes.
- Compare actual budget to Mission 012 baseline and sponsor 2x sizing direction honestly.
- Record interrupt lifecycles, answer surfaces, resume evidence, checkpoint commits, friction, and Mission 014 recommendation.
- Commit final closeout.

## Checkpoint Cadence
- M013-CP001: mission plan authored.
- M013-CP002: Garmin export shape research complete.
- M013-CP003: HDI-013-001 asked and committed before the thread question.
- M013-CP004: HDI-013-001 applied; fixture pack built; manifest parse check passes.
- M013-CP005: bridge adapter parses fixture families through preview/review.
- M013-CP006: HDI-013-002 asked/applied; materialization implemented per answer.
- M013-CP007: deliberate resume boundary committed; session ends.
- M013-CP008: fresh-session resume recorded; fact rollback implemented and tested.
- M013-CP009: workflow/timeline/evidence-graph integration passing.
- M013-CP010: approval UX, stdlib verification, and Browser QA complete.
- M013-CP011: final closeout complete.

## Plan Delta Rule
If a sponsor answer changes mission scope, create `.factory-v3/evidence/MISSION_013_PLAN_DELTA_001.md` or `_002.md` before implementing the changed scope. If no scope change is required, record why no delta was required in the interrupt JSON, state file, checkpoints, record, and closeout.

## Budget Method
Every checkpoint records:
- Tool-call count since the prior checkpoint, counting wrapped subcalls.
- Wall-clock estimate based on observed session elapsed time and command wall times.
- Qualitative context-use estimate based on visible thread volume, artifact reads, and tool output volume.
- Stop-threshold judgment for whether the next phase plus a clean checkpoint is feasible.

Every third checkpoint includes a mid-mission budget review comparing cumulative spend to remaining phases and deciding continue, halt, or descope.

