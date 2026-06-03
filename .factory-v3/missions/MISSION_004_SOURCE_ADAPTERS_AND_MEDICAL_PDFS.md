# Mission 004: Source Adapters And Medical PDFs

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
Add medical PDF ingestion and source-adapter architecture constraints so the Personal Performance OS is not locked to Garmin Connect and can later support Apple Health, Polar, Strava, medical PDFs, manual imports, and other sources.

## Success Criteria
- Canons reflect that Garmin is one adapter, not the core product dependency.
- Medical PDF upload is captured as a design target for blood work and doctor-provided analysis files.
- Source-adapter architecture is documented for Garmin, Apple Health, Polar, Strava, manual imports, medical PDFs, and future sources.
- Verification expectations include source-agnostic normalized facts, provenance, adapter boundaries, and PDF extraction safety.
- Closeout and parseable JSON mission record are created.

## Eligible-Work Rationale
Why this mission is bounded enough for V3:
- The work is research, architecture framing, and canon/evidence updates only.
- No application source code, runtime integration, external credentials, package installation, live API call, or real medical file ingestion is required.
- Outputs are limited to explicitly authorized `.factory-v3/` mission, canon, evidence, and record files.

## Non-Goals
- App source code creation.
- Package installation.
- Git initialization.
- Real medical PDF ingestion or extraction.
- Real blood-test data handling.
- Apple Health, Polar, Strava, Garmin, Telegram, OCR/vision, or voice API calls.
- Credentials, tokens, OAuth apps, developer app registration, or live third-party integrations.
- Hermes installation, configuration, execution, or use as an orchestration layer.
- Public deployment or production infrastructure.
- Medical diagnosis, treatment advice, or regulated health claims.
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or any Factory V3 repo tooling.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_004_SOURCE_ADAPTERS_AND_MEDICAL_PDFS.md`
- `.factory-v3/canons/POC_VISION.md`
- `.factory-v3/canons/POC_CONSTRAINTS.md`
- `.factory-v3/canons/POC_VERIFICATION.md`
- `.factory-v3/canons/DEPENDENCY_RESEARCH.md`
- `.factory-v3/evidence/MISSION_004_SOURCE_ADAPTER_RESEARCH.md`
- `.factory-v3/evidence/MISSION_004_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_004_RECORD.json`

## Forbidden Scope
- Factory V2 usage of any kind.
- App source code, scaffolding, or dependency manifests.
- Package installation.
- Git initialization unless separately approved.
- Real medical PDF ingestion, extraction, or storage.
- Real personal health data ingestion.
- Apple Health, Polar, Strava, Garmin, Telegram, OCR/vision, or voice API calls.
- Credentials, tokens, OAuth apps, developer app registration, webhook setup, polling, or live traffic.
- Hermes installation, configuration, execution, or operational use.
- Public deployment, production infrastructure, cloud storage, telemetry, analytics, authentication, or payment setup.
- Edits outside the authorized files and directories.

## Allowed Commands
- `pwd`
- `find . -maxdepth 4 -type f | sort`
- `sed -n '1,260p' <authorized-file>`
- `rg -n "factoryctl|stage-lint|pack-lint|docs/Factory/ORCHESTRATION|STAGE_A|STAGE_I2" .factory-v3`
- `python3 -m json.tool .factory-v3/evidence/MISSION_004_RECORD.json`
- Public web search and source review through Codex browsing tools for research only.

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
- Confirm `MISSION_004_RECORD.json` parses with `python3 -m json.tool`.
- Record that no packages were installed.
- Record that no real medical PDFs or blood-test data were ingested.
- Record that no Apple Health, Polar, Strava, Garmin, Telegram, OCR/vision, voice, or Hermes live integration was used.

## Halt Rules
Stop if:
- V2 is needed.
- Research requires credentials, private health data, real PDFs, API calls, token use, OCR/vision execution, voice transcription execution, or Hermes execution.
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
