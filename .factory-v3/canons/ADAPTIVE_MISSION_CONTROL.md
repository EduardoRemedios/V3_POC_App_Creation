# Adaptive Mission Control

## Version
v0.1

## Status
Research-only and non-enforcing until a separate POC mission is approved.

## Purpose
Allow V3 missions to grow as large as the work genuinely requires without forcing artificial size targets.

Mission size should emerge from:
- objective,
- approved scope,
- implementation facts,
- verification requirements,
- budget,
- human decisions,
- evidence quality.

Do not pad files, fixtures, tests, or phases just to make a mission larger.

## Continuation Rule
A mission may continue while all of these remain true:
- objective is still clear,
- scope remains authorized,
- verification remains passing or intentionally halted,
- budget remains acceptable,
- no unresolved human decision blocks progress,
- mission state and checkpoints are current,
- no Factory V2 help is needed.

## Stop Or Interrupt Triggers
Stop or ask the human if any of these appear:
- product ambiguity,
- scope expansion,
- dependency decision,
- credential or token decision,
- deployment decision,
- safety or privacy boundary,
- failed verification recovery choice,
- budget/context risk,
- unclear reentry state.

## Human Decision Interrupts
Use `.factory-v3/templates/V3_HUMAN_DECISION_INTERRUPT_TEMPLATE.json`.

Interrupts may be file/thread based first. Telegram is a future bridge candidate only. Do not create a Telegram bot, use tokens, poll, webhook, or send live messages unless a mission explicitly approves that work.

## Checkpoints
Use `.factory-v3/templates/V3_MISSION_CHECKPOINT_TEMPLATE.md`.

Record checkpoints at phase boundaries, before risky transitions, and before pausing. Do not rely only on elapsed time.

## Mission State
Use `.factory-v3/templates/V3_MISSION_STATE_TEMPLATE.md`.

Mission state must be authored evidence, not hidden agent memory.

## Plan Deltas
Use `.factory-v3/templates/V3_MISSION_PLAN_DELTA_TEMPLATE.md`.

Record a plan delta when a human answer changes scope, files, commands, dependencies, verification, or continuation.

## Git Authority
Git operations require explicit mission authority. If a mission initializes git, commits, pushes, or changes remotes, record the command authority and commit evidence.

## Verification Side Effects
Verification should be read-only by default. If a verifier writes or updates evidence, the mission must authorize the output path and overwrite policy.

