# Mission 006 Long-Horizon Roadmap

## Status
COMPLETE

## Mission
`.factory-v3/missions/MISSION_006_LONG_HORIZON_ROADMAP.md`

## Purpose
Move from micro-sprint missions to larger V3 missions without losing context, scope control, fixture discipline, or evidence replay.

The next build mission should be allowed to run as a larger block of work, roughly one to two hours if needed, provided it has explicit checkpoints and fixture gates.

## Mission Size Classes
| Class | Typical Scope | When To Use | Required Controls |
| --- | --- | --- | --- |
| Micro mission | One narrow artifact or decision | Canons, small research, small fixes | Mission envelope, closeout, record |
| Standard mission | Several related artifacts or a narrow implementation slice | Most fixture/schema/design work | Plan, authorized files, verification, closeout, record |
| Long-horizon mission | Multi-step design/build/test slice over one to two hours or more | Coherent build slice with fixtures, schema, primitives, tests | Roadmap link, checkpoints, fixture gates, drift audit, evidence replay |

## Long-Horizon Mission Requirements
A long-horizon mission must define:
- mission objective,
- expected duration band,
- authorized files/directories,
- allowed commands,
- dependency policy,
- implementation phases,
- checkpoint artifacts,
- fixture gates,
- halt rules,
- reentry rules,
- verification commands,
- closeout and mission record.

Long-horizon missions may be larger, but they may not be vague.

## Checkpoint Rules
Long-horizon work should have checkpoints at natural boundaries:
- before app/source code creation,
- after schema design,
- after fixture files are created,
- after primitive implementation,
- after test/verification wiring,
- after first failing test run,
- after passing verification,
- before any dependency or scope expansion.

Each checkpoint should record:
- current phase,
- files changed,
- commands run,
- fixture gates passed/failed,
- open risks,
- whether halt rules were triggered,
- next phase.

For long-running work, the assistant should provide short progress updates roughly every 30 seconds while actively exploring or editing.

## Drift Controls
Use these controls to prevent loss of context:
- Start from authored mission artifacts, not memory alone.
- Re-read relevant canons and prior closeouts at mission start.
- Maintain a visible task plan during long work.
- Keep edits within authorized paths.
- Do not add dependencies unless the mission explicitly authorizes them.
- Prefer fixture-driven scope over opportunistic feature expansion.
- Stop on external integration pressure.
- Stop if a test failure implies changing mission scope rather than implementation.
- Record assumptions in mission evidence, not only chat.

## Context Preservation
Every long-horizon mission should produce at least one durable evidence artifact before implementation or heavy editing begins.

Recommended artifact pattern:
- `MISSION_###_IMPLEMENTATION_PLAN.md`
- `MISSION_###_CHECKPOINTS.md`
- `MISSION_###_CLOSEOUT.md`
- `MISSION_###_RECORD.json`

If context compaction occurs, the next model turn should be able to resume from:
- mission envelope,
- implementation plan,
- checkpoint file,
- current repo state,
- closeout if present.

## Golden Fixture Gates
Fixture gates should move from design to executable verification in stages.

### Gate A: Fixture Definitions Exist
Required before implementation:
- DTU fixture list,
- expected normalized rows,
- expected derived facts,
- expected workflow,
- expected evidence,
- prohibited claims.

Current status:
- Passed by Mission 003 as design evidence.

### Gate B: Fixture Files Exist
Required before primitive implementation:
- synthetic source records in machine-readable files,
- expected output files or snapshots,
- fixture metadata.

Current status:
- Not yet implemented.

### Gate C: Schema Can Load Fixtures
Required before workflow logic:
- local schema exists,
- fixture load succeeds,
- source provenance is preserved,
- no real data needed.

Current status:
- Not yet implemented.

### Gate D: Deterministic Primitives Pass
Required before response generation:
- derivation primitives pass fixture tests,
- missing-data, duplicate, timezone, and source-adapter cases pass.

Current status:
- Not yet implemented.

### Gate E: Workflow Contracts Pass
Required before UI or chat behavior:
- recovery today,
- sleep cause analysis,
- four-week training analysis,
- nutrition image capture fixture,
- ride/rest recommendation,
- morning report,
- evening report.

Current status:
- Not yet implemented.

### Gate F: Safety And Evidence Pass
Required before any live surface:
- no medical diagnosis,
- no invented nutrition,
- uncertainty is present when needed,
- evidence references are present,
- proactive alerts respect suppression rules.

Current status:
- Not yet implemented.

## Recommended Next Long-Horizon Mission
Mission candidate:

```text
MISSION_007_SYNTHETIC_CORE_BUILD
```

Recommended duration band:

```text
one_to_two_hours
```

Objective:
- Implement the first synthetic-only local core: executable fixture files, source-agnostic schema, deterministic primitives, and tests for initial workflows and report candidates.

Allowed implementation scope:
- local app/project scaffold if explicitly approved in Mission 007,
- synthetic fixtures,
- local schema,
- deterministic primitive functions,
- fixture tests,
- local CLI/test harness for verification.

Still forbidden unless separately approved:
- real Garmin/Apple/Google/Polar/Strava data,
- live Telegram,
- OCR/vision execution,
- voice transcription,
- real PDFs,
- live scheduling/notifications,
- Hermes,
- public deployment.

Suggested Mission 007 phases:
1. Stack selection and scaffold, if not already present.
2. Fixture file format and DTU fixture subset.
3. Source-agnostic schema.
4. Fixture loader and provenance.
5. Deterministic primitives.
6. Workflow contract tests.
7. Morning/evening report candidate tests.
8. Closeout and record.

Minimum Mission 007 fixture subset:
- `dtu_baseline_healthy_week`
- `dtu_accumulated_fatigue`
- `dtu_missing_data`
- `dtu_duplicate_import`
- `dtu_timezone_boundary`
- `dtu_greek_yoghurt_label_image`
- `dtu_cross_surface_recovery_handoff`
- `dtu_morning_report_normal`
- `dtu_evening_report_nutrition_gap`

Mission 007 pass condition:
- fixture files load,
- schema preserves provenance,
- deterministic primitives pass tests,
- workflow/report candidates produce expected structured outputs,
- no live integrations are used.

Mission 007 stop condition:
- any required behavior needs real data, credentials, external APIs, live notifications, or unapproved packages.

## Long-Horizon Mission Template Notes
Future mission envelopes should add these sections when long-horizon:
- Duration Band
- Phases
- Checkpoints
- Fixture Gates
- Drift Audit
- Reentry From Checkpoint
- Scope Expansion Policy
- Long-Run Verification

## Scope Expansion Policy
During a long mission:
- If a needed file is outside authorization, stop and update mission authority only with user approval.
- If a package is needed but not authorized, stop and record dependency need.
- If a fixture reveals a missing primitive, add it only if still within mission scope.
- If a feature idea appears that is not needed for fixture pass, record it as a future note, not current work.

## Evidence Standard
A long-horizon mission is successful only if a future reader can reconstruct:
- what was intended,
- what was authorized,
- what was built,
- which fixtures passed,
- which fixtures failed,
- what was deferred,
- why no forbidden integration was used.
