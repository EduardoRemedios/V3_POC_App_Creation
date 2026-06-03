# Mission 003: Digital Twin User And Intent Workflows

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
Define the first Digital Twin User golden fixture pack, source-agnostic state model, and intent-to-executable workflow primitives for the Personal Performance OS POC.

## Success Criteria
- Digital Twin User fixture specification exists with scenarios, inputs, expected derived facts, expected coaching behavior, prohibited claims, evidence requirements, and cross-surface continuity expectations.
- Source-agnostic schema plan exists for health/performance facts, conversations, intent sessions, workflow runs, evidence packs, multimodal nutrition capture, memories, and recommendations.
- Initial intent-to-executable workflow catalog exists for recovery today, sleep cause analysis, four-week training analysis, nutrition label capture, and ride/rest recommendation.
- Verification plan exists for checking fixture behavior before Garmin, Telegram, OCR/vision, or Hermes integration.
- Closeout and parseable JSON mission record are created.

## Eligible-Work Rationale
Why this mission is bounded enough for V3:
- The work is fixture design, architecture planning, and verification planning only.
- It does not require application source code, runtime integration, external credentials, package installation, deployment, or live bot/account creation.
- Outputs are limited to explicitly authorized `.factory-v3/` mission and evidence files.

## Non-Goals
- App source code creation.
- Package installation.
- Git initialization.
- Garmin credential use, Garmin API calls, scraping, or production Garmin integration.
- Telegram bot creation, Telegram token use, webhook registration, polling, or live Telegram traffic.
- OCR package installation, external vision API use, real food image ingestion, or storage of real nutrition label photos.
- Voice transcription API use or browser microphone capture.
- Hermes installation, configuration, execution, or use as an orchestration layer.
- Public deployment or production infrastructure.
- Medical diagnosis, treatment advice, or regulated health claims.
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or any Factory V3 repo tooling.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_003_DTU_AND_INTENT_WORKFLOWS.md`
- `.factory-v3/evidence/MISSION_003_DTU_GOLDEN_FIXTURES.md`
- `.factory-v3/evidence/MISSION_003_ARCHITECTURE_PLAN.md`
- `.factory-v3/evidence/MISSION_003_VERIFICATION_PLAN.md`
- `.factory-v3/evidence/MISSION_003_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_003_RECORD.json`

## Forbidden Scope
- Factory V2 usage of any kind.
- App source code, scaffolding, or dependency manifests.
- Package installation.
- Git initialization unless separately approved.
- Garmin credentials, real account login, API calls, scraping, or data retrieval.
- Telegram bot creation, tokens, webhook setup, polling, or live Telegram traffic.
- OCR/vision package installation, external vision API use, or real nutrition image ingestion.
- Voice transcription API use or microphone capture.
- Hermes installation, configuration, execution, or operational use.
- Real personal health data ingestion.
- Public deployment, production infrastructure, cloud storage, telemetry, analytics, authentication, or payment setup.
- Edits outside the authorized files and directories.

## Allowed Commands
- `pwd`
- `find . -maxdepth 4 -type f | sort`
- `sed -n '1,260p' <authorized-file>`
- `rg -n "factoryctl|stage-lint|pack-lint|docs/Factory/ORCHESTRATION|STAGE_A|STAGE_I2" .factory-v3`
- `python3 -m json.tool .factory-v3/evidence/MISSION_003_RECORD.json`

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
- Confirm `MISSION_003_RECORD.json` parses with `python3 -m json.tool`.
- Record that no packages were installed.
- Record that no Garmin credentials or API calls were used.
- Record that Telegram was not used live and no bot/token was created.
- Record that OCR/vision and voice transcription were design-only.
- Record that Hermes was not installed, configured, or used.

## Halt Rules
Stop if:
- V2 is needed.
- Fixture or schema design requires credentials, private health data, Garmin login, Telegram token use, OCR/vision execution, voice transcription execution, or Hermes execution.
- A package install is needed.
- App source code becomes necessary.
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
