# Mission 010: Synthetic Workbench QA And Operator Readiness

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO

## Objective
Improve the Mission 009 synthetic local workbench into a more reliable operator-ready QA surface by strengthening browser/UI verification, scenario walkthrough coverage, UI state/error handling, responsive layout contracts, and generated audit evidence.

## Success Criteria
- The static workbench remains local-only, synthetic-only, no-build, and package-free.
- The workbench has stable test selectors, clear loading/error/empty states, selected fixture persistence, reset/replay controls, and an operator scenario walkthrough.
- UI-facing API flows are covered by stdlib smoke checks and unit tests.
- Browser UI QA is attempted through the built-in Codex Browser first, with screenshot and viewport evidence when the Browser surface permits it.
- Playwright CLI/MCP is used only if already available without package installation, or after a human decision interrupt explicitly approves package acquisition.
- Generated Mission 010 UI QA/audit summary JSON records commands, viewport checks, console checks, scenario checks, screenshots if available, dependency review, and residual risks.
- Mission 010 closeout and record are replayable from authored artifacts, checkpoints, mission state, and repository state.

## Eligible-Work Rationale
This mission is bounded enough for V3 because it extends the already-local synthetic Mission 009 workbench without introducing real data, live integrations, external credentials, scheduler behavior, notification delivery, public deployment, or new dependencies. The primary risks are verification-tool ambiguity and UI regression; both are handled through checkpoints, authored mission state, and halt/interrupt rules.

## Non-Goals
- No real personal health data.
- No Garmin, Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, or other live integration.
- No Telegram bot, token, webhook, polling loop, or live message traffic.
- No OCR/vision execution against real medical documents.
- No voice transcription execution.
- No package installation by default.
- No public deployment.
- No scheduler, cron, worker, daemon, queue, or notification delivery.
- No Factory V2 or Factory_V3 repo tooling.
- No forced file/test inflation.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_010_SYNTHETIC_WORKBENCH_QA_AND_OPERATOR_READINESS.md`
- `.factory-v3/evidence/MISSION_010_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_010_STATE.md`
- `.factory-v3/evidence/MISSION_010_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_010_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_010_RECORD.json`
- `.factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json`
- `.factory-v3/evidence/MISSION_010_BROWSER_NOTES.md`
- `workbench/index.html`
- `workbench/app.js`
- `workbench/styles.css`
- `scripts/mission_010_workbench_qa.py`
- `scripts/verify_mission_010.py`
- `tests/test_mission_010_workbench_qa.py`

## Forbidden Scope
- Any Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stage, V2 fallback, or Factory_V3 repo tooling.
- Any real health, fitness, nutrition, body, medical, voice, image, or identity data.
- Any live Garmin, Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, Telegram, OCR, vision, transcription, medical PDF, scheduler, notification, Hermes, production infrastructure, or public deployment work.
- Any package manager install or `npx --package` download unless a human decision interrupt approves the dependency acquisition and a plan delta records the change.
- Any git commit, push, remote change, or branch creation unless a later explicit human instruction grants git write authority.

## Allowed Commands
- Read/search/status commands: `pwd`, `ls`, `find`, `sed`, `rg`, `git status --short --branch`, `git log --oneline --decorate -8`, `git diff --stat`, `git diff -- workbench scripts tests .factory-v3`.
- Python stdlib checks: `python3 -B -m unittest discover -s tests`, `python3 -B scripts/verify_mission_010.py`, `python3 -B scripts/mission_010_workbench_qa.py --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`.
- JSON parse checks: `python3 -m json.tool .factory-v3/evidence/MISSION_010_RECORD.json`, `python3 -m json.tool .factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json`.
- Local API server: `python3 -B -m ppos_core.api --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`.
- Local process cleanup for mission-owned localhost server only: `lsof -ti tcp:<mission port>`, `kill <mission server pid>`.
- Browser surface: built-in Codex Browser against `http://127.0.0.1:<mission port>/workbench/` only.
- Playwright prerequisite check only: `command -v npx`. Playwright CLI execution is allowed only if it does not install/fetch packages; otherwise halt and create a human decision interrupt.

## Dependency Policy
- New dependencies allowed: NO
- If YES, approval reference: not applicable
- Install command: not applicable
- Rollback plan: not applicable

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: all existing and Mission 010 tests pass.
- `python3 -B scripts/verify_mission_010.py`: mission record, UI QA audit JSON, static workbench contracts, mission state, checkpoints, and no-go scans pass.
- `python3 -B scripts/mission_010_workbench_qa.py --db /tmp/ppos_mission_010_qa.sqlite --host 127.0.0.1 --port 8770`: local stdlib UI/API scenario checks pass and write authorized UI QA audit evidence.
- Browser UI QA: built-in Browser opens localhost workbench, verifies no console errors, key views mount, fixture selection persists, scenario walkthrough runs, desktop layout has no obvious overflow, screenshot attempted, and mobile/viewport attempt recorded.
- JSON parse checks for Mission 010 record and UI QA audit pass.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission envelope, implementation plan, workbench contract changes, stdlib QA harness, unit verification, Browser QA, final closeout.
- Mission state file: `.factory-v3/evidence/MISSION_010_STATE.md`
- Human decision interrupts allowed: YES
- Interrupt surfaces allowed: thread | file | telegram-research-only
- Timeout behavior for unresolved interrupts: pause
- Plan delta required before scope change: YES
- Verification side effects allowed: YES
- If YES, authorized output paths:
  - `.factory-v3/evidence/MISSION_010_UI_QA_AUDIT.json`
  - `.factory-v3/evidence/MISSION_010_BROWSER_NOTES.md`
  - `.factory-v3/evidence/MISSION_010_CHECKPOINTS.md`
  - `.factory-v3/evidence/MISSION_010_STATE.md`
  - `.factory-v3/evidence/MISSION_010_CLOSEOUT.md`
  - `.factory-v3/evidence/MISSION_010_RECORD.json`

## Halt Rules
Stop if:
- Factory V2 or Factory_V3 repo tooling appears necessary.
- Mission scope or authorized files/commands are insufficient.
- Browser/Playwright verification requires package installation without an approved human decision interrupt and plan delta.
- Any live integration, credential, token, real data, Telegram bot/polling/webhook, OCR, voice transcription, scheduler, notification, Hermes, public deployment, or production infrastructure appears.
- Verification fails for reasons that require a product/scope decision rather than an implementation fix inside authorized paths.
- Mission state or checkpoint evidence becomes stale or contradicts repository state.
- Git write operations are needed without explicit human git authority.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as a fallback while claiming POC readiness.

## Reentry Rules
- Resume only from authored mission artifacts, `.factory-v3/evidence/MISSION_010_STATE.md`, latest checkpoint, and current repository state.
- Halt if derived state conflicts with authored artifacts.
- If a browser or local server session is interrupted, restart from the latest checkpoint and record the interruption in Mission 010 browser notes or closeout.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md`.
