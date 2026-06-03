# Mission 006: Long Horizon Roadmap

## Status
Research/design-only and non-enforcing mission approved by the user request dated 2026-06-03.

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO

## Objective
Define a long-horizon V3 roadmap and mission-sizing framework so future missions can run for larger blocks of work, potentially one to two hours or longer, without losing context, drifting from constraints, or bypassing fixture/evidence gates.

## Success Criteria
- Roadmap placeholders exist for future long-horizon missions.
- Mission sizing rules distinguish micro, standard, and long-horizon missions.
- Drift controls, checkpoint rules, and context-preservation notes are defined.
- Golden fixture gates are mapped onto the roadmap.
- Constraints and verification canons are updated for long-horizon execution.
- Closeout and parseable JSON mission record are created.

## Eligible-Work Rationale
Why this mission is bounded enough for V3:
- The work is operations planning and V3 mission design only.
- It does not require app source code, package installation, external credentials, live integrations, deployment, or real health data.
- Outputs are limited to explicitly authorized `.factory-v3/` mission, canon, evidence, and record files.

## Non-Goals
- App source code creation.
- Package installation.
- Git initialization.
- Running a long build mission in this mission.
- Scheduler, notification, Telegram, OCR/vision, voice, Garmin, Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, or medical PDF live integration.
- Real personal health data ingestion.
- Hermes installation, configuration, execution, or use as an orchestration layer.
- Public deployment or production infrastructure.
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or any Factory V3 repo tooling.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_006_LONG_HORIZON_ROADMAP.md`
- `.factory-v3/canons/POC_CONSTRAINTS.md`
- `.factory-v3/canons/POC_VERIFICATION.md`
- `.factory-v3/evidence/MISSION_006_LONG_HORIZON_ROADMAP.md`
- `.factory-v3/evidence/MISSION_006_ROADMAP_PLACEHOLDERS.md`
- `.factory-v3/evidence/MISSION_006_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_006_RECORD.json`

## Forbidden Scope
- Factory V2 usage of any kind.
- App source code, scaffolding, or dependency manifests.
- Package installation.
- Git initialization unless separately approved.
- Running or simulating long build execution.
- Any third-party API call, credential, token, OAuth app, developer app registration, or live traffic.
- Real personal health data, real medical PDFs, real nutrition images, or real voice files.
- Hermes installation, configuration, execution, or operational use.
- Public deployment, production infrastructure, cloud storage, telemetry, analytics, authentication, or payment setup.
- Edits outside the authorized files and directories.

## Allowed Commands
- `pwd`
- `find . -maxdepth 4 -type f | sort`
- `sed -n '1,260p' <authorized-file>`
- `rg -n "factoryctl|stage-lint|pack-lint|docs/Factory/ORCHESTRATION|STAGE_A|STAGE_I2" .factory-v3`
- `python3 -m json.tool .factory-v3/evidence/MISSION_006_RECORD.json`

## Dependency Policy
- New dependencies allowed: NO
- If YES, approval reference: not applicable
- Install command: not applicable
- Rollback plan: not applicable

## Verification
Commands and expected evidence:
- Confirm current path is `/Users/eduardodosremedios/V3_POC_App_Creation`.
- Confirm edited files are limited to the mission-authorized files.
- Confirm V2 machinery scan shows no Factory V2 tooling use. References to V2 as a forbidden/no-go condition are acceptable.
- Confirm `MISSION_006_RECORD.json` parses with `python3 -m json.tool`.
- Record that no app code, package, live integration, real data, deployment, Hermes, or V2 tooling was used.

## Halt Rules
Stop if:
- V2 is needed.
- Roadmap design requires app source code, package installation, credentials, private health data, live integrations, deployment, or Hermes execution.
- Authorized files or commands are insufficient.
- Verification cannot be run.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as a fallback while claiming POC readiness.

## Reentry Rules
- Resume only from authored mission artifacts and current repository state.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md`.
