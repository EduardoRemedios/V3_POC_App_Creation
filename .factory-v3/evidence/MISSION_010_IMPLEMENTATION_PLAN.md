# Mission 010 Implementation Plan

## Status
APPROVED

## Baseline
- V3 baseline commit: `abb8ec0 Sync Factory V3 adaptive mission control`
- Prior mission: Mission 009 complete with 36 fixtures, 132 unit tests, 200 recorded checks, 8 workbench views, and browser QA limitation around screenshot capture/mobile viewport.

## Objective
Strengthen the synthetic local workbench as an operator-ready QA surface without adding dependencies, real data, live integrations, or deployment.

## Phases
1. Mission envelope and initial state.
2. Static workbench contract design.
3. Workbench implementation: stable selectors, state persistence, loading/error surfaces, reset/replay controls, scenario walkthrough, responsive layout polish.
4. Stdlib QA harness: local server scenario checks and generated UI QA audit JSON.
5. Unit/static verification: tests for expected selectors, API calls, audit output, no-go markers, and responsive contract.
6. Browser UI QA: built-in Browser first; screenshot/viewport evidence if available; Playwright only if already usable without package installation.
7. Final verification, checkpoint update, closeout, and mission record.

## Authorized Implementation Detail
- `workbench/index.html`: add stable `data-testid` markers, operator scenario controls, status/error regions, reset control, and view metadata.
- `workbench/app.js`: add UI state store, localStorage-backed fixture persistence, guarded API error handling, loading/error rendering, scenario walkthrough runner, reset/replay handling, and stable status updates.
- `workbench/styles.css`: improve responsive layout contracts and overflow resilience without changing to a build pipeline.
- `scripts/mission_010_workbench_qa.py`: stdlib localhost smoke and UI/API scenario harness; writes `.factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json`.
- `scripts/verify_mission_010.py`: mission/evidence/static contract verification.
- `tests/test_mission_010_workbench_qa.py`: focused tests for Mission 010 static contracts and QA output behavior.

## Verification Commands
- `python3 -B -m unittest discover -s tests`
- `python3 -B scripts/mission_010_workbench_qa.py --db /tmp/ppos_mission_010_qa.sqlite --host 127.0.0.1 --port 8770`
- `python3 -B scripts/verify_mission_010.py`
- `python3 -m json.tool .factory-v3/evidence/MISSION_010_RECORD.json`
- `python3 -m json.tool .factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json`

## Browser QA Plan
- Start the stdlib API on `127.0.0.1:8770`.
- Open `/workbench/` in the built-in Codex Browser.
- Verify title, no console errors, nonblank DOM, view buttons, scenario runner, fixture selector, persisted fixture state, replay timeline, audit summary, and desktop overflow checks.
- Attempt screenshot capture and record pass/fail.
- Attempt mobile viewport/responsive evidence if the Browser surface exposes a reliable viewport control; otherwise record fallback static CSS/harness evidence.
- Do not use Playwright CLI if it would fetch/install a package.

## Side Effects
- Authorized writes only to Mission 010 evidence files and authorized source/test/script files.
- Browser interactions are limited to localhost.
- Verification audit script may overwrite `.factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json`.

## Halt/Interrupt Conditions
- Create a human decision interrupt before any package acquisition.
- Create a plan delta before any source path, dependency, verification command, or git write scope expansion.
- Halt on any real-data/live-integration/credential/deployment pressure.
