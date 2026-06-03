# Mission 006 Roadmap Placeholders

## Status
COMPLETE

## Purpose
Define placeholder missions large enough to support long-horizon V3 work while preserving evidence, fixture gates, and halt discipline.

## Roadmap

### Mission 007: Synthetic Core Build
Type:

```text
long_horizon_build
```

Goal:
- Create the first executable local core using synthetic DTU fixtures.

Primary outputs:
- app/project scaffold if approved,
- synthetic fixture files,
- source-agnostic schema,
- fixture loader,
- deterministic primitives,
- workflow/report tests,
- closeout and mission record.

Primary gates:
- Gate B: fixture files exist,
- Gate C: schema can load fixtures,
- Gate D: deterministic primitives pass,
- Gate E: workflow contracts pass.

Do not include:
- live third-party integrations,
- Telegram live bot,
- OCR/vision execution,
- voice transcription,
- real PDFs,
- live scheduling.

### Mission 008: Conversational Surface Prototype
Type:

```text
standard_or_long_horizon_build
```

Goal:
- Build a local/private desktop conversational surface over the synthetic core.

Primary outputs:
- full-screen conversational web app,
- runtime evidence panels,
- fixture-backed conversation flows,
- cross-surface state simulation,
- local verification.

Primary gates:
- cross-surface fixture pass,
- evidence rendering pass,
- text overflow/responsive UI pass,
- no live Telegram.

### Mission 009: Ambient Report Candidate Engine
Type:

```text
standard_or_long_horizon_build
```

Goal:
- Generate morning/evening report candidates locally without live scheduling or notifications.

Primary outputs:
- report schema,
- report candidate generator,
- monitoring rule evaluator,
- cooldown/quiet-hours simulation,
- fixture tests.

Primary gates:
- morning report fixtures pass,
- evening report fixtures pass,
- proactive suppression fixtures pass,
- evidence and safety checks pass.

### Mission 010: Manual Import And Medical PDF Fixture Expansion
Type:

```text
standard_design_or_build
```

Goal:
- Expand synthetic/manual import and medical-PDF-like fixture coverage.

Primary outputs:
- medical PDF fixture schema,
- synthetic lab result extraction fixtures,
- manual import schema,
- source adapter conflict tests.

Do not include:
- real PDF parsing unless separately approved,
- real medical data.

### Mission 011: Telegram Design-To-Live Decision
Type:

```text
research_decision
```

Goal:
- Decide whether to approve live Telegram bot creation and local/private runtime.

Primary outputs:
- token handling plan,
- allowlist plan,
- retention plan,
- long polling vs webhook decision,
- rollback and verification plan.

### Mission 012: First Real Data Bridge Decision
Type:

```text
research_decision
```

Goal:
- Decide first real-data bridge after synthetic core proves value.

Candidate choices:
- manual Garmin export/import,
- Apple Health export/HealthKit bridge,
- Health Connect bridge,
- Strava activity API,
- medical PDF upload,
- nutrition image upload.

Decision criteria:
- data value,
- implementation cost,
- privacy risk,
- credential risk,
- verification ability,
- personal-use suitability.

## Roadmap Rule
These placeholders do not authorize implementation. Each mission still requires its own envelope with authorized files, allowed commands, dependency policy, verification, and halt rules.
