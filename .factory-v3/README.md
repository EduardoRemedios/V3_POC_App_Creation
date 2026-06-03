# Factory V3 POC Workspace

## Status
Research-only and non-enforcing V3-only POC workspace seed. Do not use Factory V2 to design, build, test, deploy, govern, lint, recover, or validate this POC.

## Operating Contract
This project is testing whether V3 can be used operationally with Codex.

Operational means:

```text
Use V3 with Codex to design, build, test, and privately deploy an application.
```

Pass condition:
- V3 runs the POC lifecycle standalone.

No-go condition:
- Any required step depends on Factory V2.

## Start Order
1. Fill `canons/POC_VISION.md`.
2. Fill `canons/POC_CONSTRAINTS.md`.
3. Fill `canons/POC_VERIFICATION.md`.
4. Fill `canons/DEPENDENCY_RESEARCH.md`.
5. Read `canons/ADAPTIVE_MISSION_CONTROL.md`.
6. Create the first mission from `missions/MISSION_001_START_HERE.md`.
7. Execute only after the mission has explicit objective, files, commands, verification, stop rules, checkpoint rules, and interrupt rules.
8. Close out with `templates/V3_POC_CLOSEOUT_TEMPLATE.md`.
9. Record mission evidence with `templates/V3_POC_MISSION_RECORD_TEMPLATE.json`.
10. Score the POC with `evals/V3_POC_EVAL_RUBRIC.md` and `evals/V3_POC_EVAL_RECORD_TEMPLATE.json`.

## Hard Stops
Stop if:
- V2 is needed,
- mission scope is unclear,
- authorized files or commands are missing,
- verification cannot be run,
- dependency approval is missing,
- human decision interrupt is unresolved,
- mission state or checkpoint evidence is stale,
- Garmin integration is attempted before research approval,
- Hermes is used before research approval,
- public deployment or production infrastructure appears,
- credentials or secrets would be exposed.
