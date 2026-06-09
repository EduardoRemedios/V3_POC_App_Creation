# Mission 017: Stale Reentry Detection Evidence

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO
- Evidence target: first deliberately seeded stale-reentry detection mission.

## Objective
Produce replayable standalone V3 evidence that stale authored reentry state is detected before continuation and causes a clean halt rather than hidden-memory continuation.

## Success Criteria
- Mission envelope exists before stale-reentry verification is run.
- Baseline local synthetic tests pass before the stale-reentry probe.
- A mission-owned stale-reentry fixture records an intentionally stale expected git head.
- A mission-owned verifier compares the authored expected head with the actual repository head.
- The verifier fails because the expected head is stale.
- Mission state, checkpoints, closeout, and mission record classify the failure as stale reentry and halt without reconciliation.
- No app source, test suite, database, UI, API, dependency, real-data, integration, deployment, or Factory V2 work occurs.
- Mission record parses as JSON.

## Eligible-Work Rationale
This is bounded enough for V3 because it is evidence-only and uses a synthetic mission-owned fixture to prove stale reentry detection without changing app behavior.

## Non-Goals
- No app source behavior change.
- No test-suite change outside the mission-owned verifier.
- No stale-state reconciliation in this mission.
- No recovery or continuation after stale reentry is detected.
- No database migration.
- No real personal data, Garmin data, credentials, tokens, live integrations, package installs, deployment, scheduler, notifications, Telegram, Hermes, or Factory V2.
- No public release or operational-readiness claim.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_017_STALE_REENTRY_DETECTION.md`
- `.factory-v3/evidence/MISSION_017_STATE.md`
- `.factory-v3/evidence/MISSION_017_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_017_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_017_RECORD.json`
- `fixtures/mission_017/stale_reentry.json`
- `scripts/verify_mission_017_stale_reentry.py`

## Forbidden Scope
- Everything in Non-Goals.
- Any file outside the authorized list.
- Any command that installs dependencies, uses credentials, calls external services, deploys, runs Factory V2 tooling, or mutates app behavior.

## Allowed Commands
- `date -u +%Y-%m-%dT%H:%M:%SZ`
- `git status --short`
- `git rev-parse HEAD`
- `git log --oneline -n 6`
- `python3 -B -m unittest discover -s tests`
- `python3 -B scripts/verify_mission_017_stale_reentry.py`
- `python3 -m json.tool .factory-v3/evidence/MISSION_017_RECORD.json`
- `git diff --check`
- `git add .factory-v3/missions/MISSION_017_STALE_REENTRY_DETECTION.md .factory-v3/evidence/MISSION_017_STATE.md .factory-v3/evidence/MISSION_017_CHECKPOINTS.md .factory-v3/evidence/MISSION_017_CLOSEOUT.md .factory-v3/evidence/MISSION_017_RECORD.json fixtures/mission_017/stale_reentry.json scripts/verify_mission_017_stale_reentry.py`
- `git commit -m "Record Mission 017 stale reentry detection evidence"`
- `git push origin main`

## Dependency Policy
- New dependencies allowed: NO.

## Stale-Reentry Probe
Mission 017 intentionally seeds:

```text
expected_head: c48dd02ad1262ea74c72fa0f121e56f253f1c4e2
actual_head_at_start: 425766ffcd80243358f659696abc6dc05e08c3d3
```

The verifier must fail when those values differ. That failure is the expected stale-reentry evidence. Mission 017 must halt after recording the mismatch and must not reconcile the stale state inside this same mission.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission start, baseline verification, stale-reentry probe, halted closeout.
- Mission state file: `.factory-v3/evidence/MISSION_017_STATE.md`
- Human decision interrupts allowed: NO
- Interrupt surfaces allowed: none
- Timeout behavior for unresolved interrupts: halt
- Plan delta required before scope change: YES
- Verification side effects allowed: YES
- Authorized output paths: Mission 017 evidence files listed above.

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: expected PASS baseline.
- `python3 -B scripts/verify_mission_017_stale_reentry.py`: expected FAIL because expected head is stale.
- `python3 -m json.tool .factory-v3/evidence/MISSION_017_RECORD.json`: expected PASS after halted record is authored.

## Halt Rules
Stop if:
- the stale-reentry verifier unexpectedly passes,
- stale expected head does not differ from actual head,
- full tests fail before the stale-reentry probe,
- reconciliation would be needed,
- recovery would be needed,
- V2 or Factory_V3 tooling appears necessary,
- real data, credentials, live integration, dependency install, deployment, or unauthorized files are implicated,
- mission state or checkpoint evidence conflicts with disk state.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as fallback while claiming POC readiness.

## Reentry Rules
- Resume only from this mission envelope, Mission 017 state, Mission 017 checkpoints, Mission 017 closeout, Mission 017 record, and current repository state.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md` conventions and explicitly report the stale-reentry halt decision.
