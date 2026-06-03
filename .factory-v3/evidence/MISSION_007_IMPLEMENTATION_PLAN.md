# Mission 007 Implementation Plan

## Status
IN_PROGRESS

## Build Choice
Use a local Python standard-library core with JSON fixtures and `unittest`.

Rationale:
- no package installation,
- deterministic fixture execution,
- source files are small and inspectable,
- JSON fixtures are replayable,
- standard-library tests satisfy the first synthetic core gates.

## Authorized Scaffold
- `ppos_core/`: source-agnostic synthetic core.
- `fixtures/dtu/`: executable fixture JSON files.
- `tests/`: standard-library unit tests.
- `scripts/verify_mission_007.py`: local verification harness.

## Data Model Shape
The loader will preserve:
- raw `source_records` with `source`, `source_record_id`, `observed_at`, `ingested_at`, `payload`, and provenance metadata,
- normalized facts with fact IDs and provenance links,
- derived facts computed from normalized facts,
- evidence packs citing source and derived facts,
- conversation threads and surface events independent of Telegram or desktop clients,
- intent sessions and workflow runs,
- report candidate records.

## Fixture Format
Each fixture JSON contains:
- `fixture_id`,
- `scenario`,
- `synthetic_only`,
- `sources`,
- `source_records`,
- `expected`,
- optional `conversation_threads`, `surface_events`, `intent_sessions`, `workflow_runs`, and `report_candidates`.

Every required fixture must include expected gates for provenance, derived facts, workflow outputs, prohibited claims, and required evidence references.

## Implementation Phases
1. Create mission envelope and evidence shell.
2. Create the nine fixture JSON files.
3. Implement schema dataclasses and validation.
4. Implement fixture loader that validates synthetic-only data and provenance links.
5. Implement deterministic primitives:
   - training load,
   - recovery summary,
   - missing-data detection,
   - duplicate activity detection,
   - timezone attribution,
   - nutrition label normalization,
   - evidence assembly,
   - safety checks.
6. Implement workflow/report functions:
   - recovery today,
   - sleep cause analysis,
   - four-week training analysis,
   - nutrition label capture,
   - ride/rest recommendation,
   - morning report candidate,
   - evening report candidate.
7. Implement tests for gates C-F.
8. Run verification and close out.

## Fixture Gates
| Gate | Check | Recovery |
| --- | --- | --- |
| A | Prior fixture definitions exist in Mission 003/005/006 evidence. | Halt if missing. |
| B | Nine JSON fixture files exist and parse. | Fix fixture syntax or missing fields within authorized files. |
| C | Loader validates fixtures and provenance links. | Fix schema/loader or fixture links within authorized files. |
| D | Primitive tests pass. | Fix deterministic logic within authorized files. |
| E | Workflow/report tests pass. | Fix workflow composition within authorized files. |
| F | Safety/evidence verification passes. | Fix checks, evidence references, or fixture expectations within authorized files. |

## Verification Commands
```bash
python3 -m json.tool .factory-v3/evidence/MISSION_007_RECORD.json
python3 -m unittest discover -s tests
python3 scripts/verify_mission_007.py
rg -n "factoryctl|stage-lint|pack-lint|Factory V2|Factory_V2|STAGE_A|STAGE_I2|Hermes|Telegram token|Garmin credentials|Garmin Connect login|cron|scheduler|daemon|worker|webhook|polling|OCR|vision API|voice transcription|real medical PDF|Apple Health live|Health Connect live|Strava API|Polar AccessLink" .
```

## Dependency Review
No packages are approved or required. If `python3` standard-library execution is not enough, halt and record the dependency gap.

## Drift Guardrails
- Keep all app/source edits inside `ppos_core/`, `fixtures/dtu/`, `tests/`, and `scripts/verify_mission_007.py`.
- Do not create a UI, database server, scheduler, notification system, or live adapter.
- Keep all source names synthetic or manual-note only.
- Treat synthetic nutrition image fixtures as OCR-like text metadata, not real OCR/vision execution.
