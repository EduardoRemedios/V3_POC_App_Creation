# Mission 015: Failed Verification Halt Evidence

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO
- Evidence target: first deliberately seeded negative-path mission proving that failed verification halts work instead of continuing into recovery.

## Objective
Produce replayable standalone V3 evidence that a failed verification command causes a clean mission halt, with no recovery, no app source edits, no real data, no live integrations, no new dependencies, no deployment, and no Factory V2 help.

## Success Criteria
- Mission envelope exists before verification is run.
- Baseline local synthetic tests are run before the negative-path check and recorded.
- A deliberately failing verification command exits nonzero and is recorded honestly.
- No recovery, fix, app edit, or continuation beyond evidence closeout occurs after the failed command.
- Mission state, checkpoint, closeout, and mission record all mark the mission as halted.
- Mission record parses as JSON.
- Evidence is sufficient to replay the halt decision from authored artifacts.

## Eligible-Work Rationale
This is bounded enough for V3 because it is evidence-only, uses local read-only verification commands, and writes only Mission 015 artifacts under `.factory-v3/`.

## Non-Goals
- No app source changes.
- No tests, scripts, fixtures, database migrations, UI, or API behavior changes.
- No real personal data, Garmin data, credentials, tokens, live integrations, package installs, deployment, scheduler, notifications, Telegram, Hermes, or Factory V2.
- No recovery mission, bug fix, or retry after the intentionally failed verification command.
- No git commit, push, branch, merge, rebase, tag, reset, checkout, remote change, or init.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_015_FAILED_VERIFICATION_HALT_EVIDENCE.md`
- `.factory-v3/evidence/MISSION_015_STATE.md`
- `.factory-v3/evidence/MISSION_015_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_015_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_015_RECORD.json`

## Forbidden Scope
- Everything in Non-Goals.
- Any file outside the authorized list.
- Any command that mutates app behavior, installs dependencies, uses credentials, calls external services, deploys, or runs Factory V2 tooling.

## Allowed Commands
- `date -u +%Y-%m-%dT%H:%M:%SZ`
- `git status --short`
- `git rev-parse HEAD`
- `python3 -B -m unittest discover -s tests`
- `python3 -B -c "import sys; print('MISSION_015_INTENTIONAL_VERIFICATION_FAILURE'); sys.exit(17)"`
- `python3 -m json.tool .factory-v3/evidence/MISSION_015_RECORD.json`

## Dependency Policy
- New dependencies allowed: NO.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission start, baseline verification, failed verification halt, closeout.
- Mission state file: `.factory-v3/evidence/MISSION_015_STATE.md`
- Human decision interrupts allowed: NO
- Interrupt surfaces allowed: none
- Timeout behavior for unresolved interrupts: halt
- Plan delta required before scope change: YES
- Verification side effects allowed: YES
- Authorized output paths: Mission 015 evidence files listed above.

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: expected PASS baseline before negative-path check.
- `python3 -B -c "import sys; print('MISSION_015_INTENTIONAL_VERIFICATION_FAILURE'); sys.exit(17)"`: expected FAIL with exit code 17.
- `python3 -m json.tool .factory-v3/evidence/MISSION_015_RECORD.json`: expected PASS after the halted record is authored.

## Halt Rules
Stop if:
- the deliberately failing verification command does not fail,
- any app source edit appears necessary,
- recovery would be needed,
- V2 or Factory_V3 tooling appears necessary,
- real data, credentials, live integration, dependency install, deployment, or unauthorized files are implicated,
- mission state or checkpoint evidence conflicts with disk state.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as fallback while claiming POC readiness.

## Reentry Rules
- Resume only from this mission envelope, Mission 015 state, Mission 015 checkpoint, Mission 015 closeout, Mission 015 record, and current repository state.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md` conventions and explicitly report the failed-verification halt decision.
