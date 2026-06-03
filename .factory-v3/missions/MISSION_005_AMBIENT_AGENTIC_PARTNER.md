# Mission 005: Ambient Agentic Partner

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
Frame the Personal Performance OS as a persistent, always-on, ambient agentic partner that can provide morning and evening reports, monitor trends, preserve context over time, and proactively surface evidence-based observations while remaining bounded, private, and non-medical.

## Success Criteria
- POC vision reflects persistent ambient partnership, not only reactive chat or dashboard behavior.
- Constraints define what proactive and scheduled behavior may be designed now versus implemented later.
- Verification expectations include morning report, evening report, proactive monitoring, alert noise control, and evidence-backed recommendations.
- Evidence artifact defines ambient agent behaviors, boundaries, report contracts, and fixture implications.
- Closeout and parseable JSON mission record are created.

## Eligible-Work Rationale
Why this mission is bounded enough for V3:
- The work is product framing, architecture design, and verification planning only.
- It does not require scheduler implementation, notifications, Telegram live use, app source code, external credentials, package installation, deployment, or real health data.
- Outputs are limited to explicitly authorized `.factory-v3/` mission, canon, evidence, and record files.

## Non-Goals
- App source code creation.
- Scheduler, cron, queue, worker, or notification implementation.
- Package installation.
- Git initialization.
- Telegram bot creation, Telegram token use, webhook registration, polling, or live Telegram traffic.
- Garmin, Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, OCR/vision, voice, or medical PDF live integration.
- Real personal health data ingestion.
- Hermes installation, configuration, execution, or use as an orchestration layer.
- Public deployment or production infrastructure.
- Medical diagnosis, treatment advice, or regulated health claims.
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or any Factory V3 repo tooling.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_005_AMBIENT_AGENTIC_PARTNER.md`
- `.factory-v3/canons/POC_VISION.md`
- `.factory-v3/canons/POC_CONSTRAINTS.md`
- `.factory-v3/canons/POC_VERIFICATION.md`
- `.factory-v3/evidence/MISSION_005_AMBIENT_AGENTIC_PARTNER.md`
- `.factory-v3/evidence/MISSION_005_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_005_RECORD.json`

## Forbidden Scope
- Factory V2 usage of any kind.
- App source code, scaffolding, or dependency manifests.
- Package installation.
- Git initialization unless separately approved.
- Live scheduler, worker, queue, cron, notification, Telegram, webhook, or polling behavior.
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
- `python3 -m json.tool .factory-v3/evidence/MISSION_005_RECORD.json`

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
- Confirm `MISSION_005_RECORD.json` parses with `python3 -m json.tool`.
- Record that no scheduler, notification, live Telegram, third-party API, package, credential, real health data, Hermes, or app source code was used.

## Halt Rules
Stop if:
- V2 is needed.
- Framing requires app source code, scheduler execution, notification sending, credentials, private health data, API calls, token use, or Hermes execution.
- A package install is needed.
- Authorized files or commands are insufficient.
- Verification cannot be run.
- Public deployment or production infrastructure appears necessary.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as a fallback while claiming POC readiness.

## Reentry Rules
- Resume only from authored mission artifacts and current repository state.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md`.
