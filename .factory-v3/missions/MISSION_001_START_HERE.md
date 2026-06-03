# Mission 001: Start Here

## Mission Status
DRAFT. Research-only and non-enforcing. This mission is the bootstrap dry run and does not authorize app implementation.

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO

## Objective
Validate that the clean POC folder can operate from the copied `.factory-v3/` bootstrap package without Factory V2.

## Success Criteria
- POC folder exists outside the `Factory_V3` repository.
- `.factory-v3/` bootstrap package is present.
- No Factory V2 stage, pack, lint, or `factoryctl` machinery is copied into the POC folder.
- POC vision, constraints, verification, and dependency research canons have initial values.
- JSON templates parse.
- Dry-run evidence records whether the bootstrap is usable standalone.

## Authorized Files And Directories
- `.factory-v3/README.md`
- `.factory-v3/canons/POC_VISION.md`
- `.factory-v3/canons/POC_CONSTRAINTS.md`
- `.factory-v3/canons/POC_VERIFICATION.md`
- `.factory-v3/canons/DEPENDENCY_RESEARCH.md`
- `.factory-v3/missions/MISSION_001_START_HERE.md`
- `.factory-v3/evidence/BOOTSTRAP_DRY_RUN.md`

## Forbidden Scope
- Factory V2 usage.
- Public deployment.
- Production infrastructure unless explicitly approved.
- Garmin integration before dependency research approval.
- Hermes use before dependency research approval.
- Credentials or secrets in prompts, files, logs, or evidence.
- Broad architecture changes outside this mission.
- App source code.
- App stack selection.
- Package installation.
- Git initialization unless separately approved.

## Allowed Commands
- `pwd`
- `find . -maxdepth 4 -type f | sort`
- `rg -n "factoryctl|stage-lint|pack-lint|docs/Factory/ORCHESTRATION|STAGE_A|STAGE_I2" .factory-v3`
- `python3 -m json.tool .factory-v3/templates/V3_POC_MISSION_RECORD_TEMPLATE.json`
- `python3 -m json.tool .factory-v3/evals/V3_POC_EVAL_RECORD_TEMPLATE.json`

## Dependency Policy
- New dependencies allowed: NO by default.
- If YES, name the dependency, approval, install command, rollback plan, and verification.

## Verification
Commands and expected evidence:
- Confirm current path is `/Users/eduardodosremedios/V3_POC_App_Creation`.
- Confirm file list contains `.factory-v3/` only.
- Confirm V2 machinery scan shows no copied V2 tooling dependency. References to V2 as a forbidden/no-go condition are acceptable.
- Confirm both JSON templates parse.

## Halt Rules
Stop if:
- V2 is needed,
- objective or scope is ambiguous,
- authorized files are insufficient,
- an unapproved dependency is needed,
- verification fails,
- deployment scope expands,
- credentials or private data would be exposed.

## Reentry Rules
- Resume only from this mission, current repo state, and the latest closeout.
- If a derived summary conflicts with files on disk, trust files on disk.

## Closeout Required
Use:

```text
.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md
```

Dry-run closeout path:

```text
.factory-v3/evidence/BOOTSTRAP_DRY_RUN.md
```

## Mission Record Required
Use:

```text
.factory-v3/templates/V3_POC_MISSION_RECORD_TEMPLATE.json
```
