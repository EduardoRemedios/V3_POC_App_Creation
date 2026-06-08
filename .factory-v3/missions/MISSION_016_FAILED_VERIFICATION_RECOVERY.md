# Mission 016: Failed Verification Recovery Evidence

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO
- Evidence target: first deliberately seeded recovery-after-failed-verification mission.

## Objective
Produce replayable standalone V3 evidence that a failed verification can be classified, recovered, and re-verified when a separate mission explicitly authorizes the recovery path.

## Success Criteria
- Mission envelope exists before recovery work begins.
- Baseline local synthetic tests pass before the seeded recovery check.
- A mission-owned synthetic recovery fixture deliberately fails a mission-owned verifier.
- The failure is recorded honestly and classified as an authorized recovery fixture issue.
- The fixture is corrected within authorized scope.
- The verifier passes after correction.
- Full local synthetic tests still pass after recovery.
- Mission state, checkpoints, closeout, and mission record explain why Mission 016 may recover while Mission 015 could not.
- Mission record parses as JSON.

## Eligible-Work Rationale
This is bounded enough for V3 because it uses only a synthetic mission-owned fixture and verifier, has no app behavior change, and explicitly authorizes the recovery path that Mission 015 forbade.

## Non-Goals
- No app source behavior change.
- No production code refactor.
- No database migration.
- No real personal data, Garmin data, credentials, tokens, live integrations, package installs, deployment, scheduler, notifications, Telegram, Hermes, or Factory V2.
- No recovery of Mission 015 itself.
- No public release or operational-readiness claim.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_016_FAILED_VERIFICATION_RECOVERY.md`
- `.factory-v3/evidence/MISSION_016_STATE.md`
- `.factory-v3/evidence/MISSION_016_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_016_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_016_RECORD.json`
- `fixtures/mission_016/recovery_gate.json`
- `scripts/verify_mission_016_recovery.py`

## Forbidden Scope
- Everything in Non-Goals.
- Any file outside the authorized list.
- Any command that installs dependencies, uses credentials, calls external services, deploys, runs Factory V2 tooling, or mutates app behavior outside the authorized synthetic fixture.

## Allowed Commands
- `date -u +%Y-%m-%dT%H:%M:%SZ`
- `git status --short`
- `git rev-parse HEAD`
- `python3 -B -m unittest discover -s tests`
- `python3 -B scripts/verify_mission_016_recovery.py`
- `python3 -m json.tool .factory-v3/evidence/MISSION_016_RECORD.json`
- `git diff --check`
- `git add .factory-v3/missions/MISSION_016_FAILED_VERIFICATION_RECOVERY.md .factory-v3/evidence/MISSION_016_STATE.md .factory-v3/evidence/MISSION_016_CHECKPOINTS.md .factory-v3/evidence/MISSION_016_CLOSEOUT.md .factory-v3/evidence/MISSION_016_RECORD.json fixtures/mission_016/recovery_gate.json scripts/verify_mission_016_recovery.py`
- `git commit -m "Record Mission 016 failed verification recovery evidence"`
- `git push origin main`

## Dependency Policy
- New dependencies allowed: NO.

## Recovery Authority
Mission 016 explicitly authorizes one recovery path:

1. Run `python3 -B scripts/verify_mission_016_recovery.py` against the intentionally failing synthetic fixture.
2. Record the failed verifier result.
3. Correct only `fixtures/mission_016/recovery_gate.json`.
4. Re-run the verifier.
5. Re-run full local synthetic tests.

If recovery requires any other file, command, dependency, real data, live integration, deployment, or app behavior change, halt and record a scope gap.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission start, baseline verification, failed verifier classification, recovery applied, final verification, closeout.
- Mission state file: `.factory-v3/evidence/MISSION_016_STATE.md`
- Human decision interrupts allowed: NO
- Interrupt surfaces allowed: none
- Timeout behavior for unresolved interrupts: halt
- Plan delta required before scope change: YES
- Verification side effects allowed: YES
- Authorized output paths: Mission 016 evidence files listed above.

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: expected PASS baseline and final.
- `python3 -B scripts/verify_mission_016_recovery.py`: expected FAIL before correction, PASS after correction.
- `python3 -m json.tool .factory-v3/evidence/MISSION_016_RECORD.json`: expected PASS after record is authored.

## Halt Rules
Stop if:
- the seeded verifier unexpectedly passes before recovery,
- full tests fail before or after recovery,
- recovery needs anything outside authorized files,
- V2 or Factory_V3 tooling appears necessary,
- real data, credentials, live integration, dependency install, deployment, or unauthorized files are implicated,
- mission state or checkpoint evidence conflicts with disk state.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as fallback while claiming POC readiness.

## Reentry Rules
- Resume only from this mission envelope, Mission 016 state, Mission 016 checkpoints, Mission 016 closeout, Mission 016 record, and current repository state.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md` conventions and explicitly compare Mission 016 recovery authority against Mission 015 halt-only authority.
