# Mission 013 State

## Mission
- Mission ID: MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS
- Mission status: active
- Profile: V3-POC-STANDALONE
- Data mode: synthetic only
- V3-only: YES
- V2 allowed: NO

## Current Phase
Phase 4: HDI-013-001 applied; Garmin fixture pack built; manifest parse checks pending.

## Last Checkpoint
M013-CP002 committed as `fcb585c`; M013-CP003 is being authored.

## Active Plan
Use the Mission 013 envelope and `.factory-v3/evidence/MISSION_013_IMPLEMENTATION_PLAN.md`.

## Completed Phases
- Existing repository and Mission 012 artifacts were read for orientation.
- Mission 013 implementation plan, state, and checkpoints files were initialized.
- Public Garmin support/developer documentation was researched without login, account, export download, sample file use, API calls, or scraping.
- `.factory-v3/evidence/MISSION_013_GARMIN_EXPORT_SHAPE_RESEARCH.md` was authored with export families, fields, units, timestamps, duplicate handling, and fixture-shape implications.
- HDI-013-001 was written with status `asked` and options for optional fixture family scope plus default future retention posture.
- HDI-013-001 was answered from the phone via Codex mobile thread and applied as `option_a`; no plan delta was required.
- `fixtures/garmin_exports/` was created with activities, sleep, body-composition, and wellness/HRV/stress synthetic fixture families.
- `ppos_core/garmin_bridge.py` was created and `ppos_core/manual_imports.py` was wired to route Garmin export IDs through the same preview/review pipeline.

## Pending Phases
- Garmin bridge adapter integration.
- HDI-013-002 materialization conflict strategy decision.
- Reviewed import materialization into normalized fact tables.
- Deliberate cross-session resume.
- Fact-level rollback.
- Workflow, timeline, evidence graph, and report consumption.
- Synthetic approval UX.
- Verification, Browser QA, closeout, record, and audit summary.

## Open Human Decision Interrupts
- HDI-013-001: applied as `option_a`; no longer blocking.
- HDI-013-002: not yet asked.
- HDI-013-003: not raised; optional only if a genuine implementation decision appears.

## Accepted Plan Deltas
- None.

## Current Verification State
- Planning checkpoint only; no app behavior changed yet.
- No Mission 013 tests or scripts have been run yet.
- Research evidence authored; citation URLs recorded in the research note.
- HDI-013-001 interrupt JSON updated to `applied`; manifest parse checks are the next verification step.

## Current Budget State
- Token budget: no explicit numeric token budget set by sponsor.
- Tool-call budget: no fixed cap; sponsor requested roughly 2x Mission 012 size as an observational guardrail.
- Context/buffer concern: low-to-moderate based on initial artifact reads; no stop pressure yet.

## Resume Evidence
- No cross-session resume has occurred yet.
- Required future resume must read authored artifacts and current repository state, then list the exact files read here.

## Next Action
Run JSON parse checks for the interrupt and Garmin manifest/JSON fixture files, then commit checkpoint 004.

## Reentry Rule
Resume only from this state file, authored Mission 013 artifacts, current repository state, and the latest checkpoint. Halt if any derived summary conflicts with authored artifacts or disk state.
