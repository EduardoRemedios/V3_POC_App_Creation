# POC Vision

## Version
v0.2

## Status
Research-only and non-enforcing until a separate build mission is approved.

## Product Vision
Build a private proof-of-concept Personal Performance OS.

The product should function as a persistent, always-on, agentic performance partner that collects or imports training, recovery, sleep, nutrition, body composition, and health context, then interacts with the user through Telegram and a future desktop conversational web app. The goal is not another dashboard. The goal is an ambient coaching system with long-term memory, explainable analysis, and enough situational awareness to reduce manual screenshot sharing, manual trend correlation, and repeated context-setting.

The system should feel like a partner that is quietly maintaining context in the background, then engaging at the right moments with useful reports, questions, observations, or recommendations.

## Primary Interaction Surface
Telegram is the preferred first lightweight user experience surface for the POC, but it must not own conversation state.

Target interaction modes:
- text questions and commands,
- voice messages,
- images,
- documents,
- proactive coaching notifications if a later mission approves a bot and scheduler.

The conversation should persist across surfaces. The user should be able to start an interaction in Telegram, continue it in a desktop web application, and return to Telegram without losing intent, context, follow-up state, or coaching memory.

Candidate surfaces:
- Telegram mobile chat,
- Telegram desktop chat,
- full-screen desktop conversational web app,
- future dashboard or evidence-review view.

The desktop web app may use a runtime-composed conversational interface where controls, charts, evidence panels, and follow-up prompts are generated from the active intent workflow rather than pre-fixed as a static dashboard.

Example user questions:
- How recovered am I today?
- What training should I do?
- Show me my weight trend over the last 30 days.
- Why was my sleep poor last night?
- I just ate chicken, rice, and vegetables.
- I uploaded a photo of this yoghurt label. Log the nutrition.
- Analyse my last four weeks of training.
- Should I ride tomorrow or take a recovery day?

Example ambient outputs:
- morning readiness report,
- evening recovery and nutrition reflection,
- weekly training/recovery review,
- quiet proactive alerts when risk or opportunity thresholds are crossed,
- follow-up on prior recommendations or experiments.

Example multimodal capture:
- The user photographs Greek yoghurt packaging or a nutrition label.
- The user uploads the image from Telegram, mobile, or desktop.
- The system extracts product name, serving size, calories, protein, carbohydrates, fat, sugars, salt/sodium, and any visible micronutrients where practical.
- The system stores the source image reference, extracted fields, confidence, and unanswered ambiguities.
- The system asks a short follow-up only when serving size, quantity eaten, or label interpretation is materially unclear.

## Operational Proof Vision
The POC is also a V3 operations test.

The proof succeeds if V3 with Codex can:
- shape the app vision,
- lock constraints,
- plan bounded missions,
- research dependencies before using them,
- implement the app in later missions,
- run verification,
- privately deploy only after approval,
- record evidence,
- recover or halt correctly,
- produce a defensible readiness decision,
- do all of that without Factory V2.

## First Useful App Outcome
The first app should be useful enough for private sponsor use, while staying small enough to test V3 rather than burying the proof under product scope.

Recommended first POC shape after Mission 002 research:
- synthetic-first local data model,
- Digital Twin User model for representative training, recovery, sleep, nutrition, and health patterns,
- persistent ambient agent model for reports, monitoring, follow-ups, and quiet proactive observations,
- local-first persistent database,
- surface-independent conversation, intent, evidence, and memory state,
- source-adapter architecture so Garmin, Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, medical PDFs, manual imports, and future sources all map into a normalized internal model,
- Telegram adapter designed but not created until a later approved mission,
- desktop conversational app architecture designed but not deployed beyond local/private scope until approved,
- multimodal nutrition capture designed for image uploads, OCR/vision extraction, and structured nutrition logs,
- Garmin integration deferred behind approved research and credential decisions,
- manual Garmin export/import as the first real-data bridge if later approved,
- optional dashboard or evidence view only as support for the chat-first coach.

## Digital Twin User Model
Synthetic-first should be treated as a deliberate Digital Twin User strategy, not placeholder fake data.

The DTU should model a realistic personal performance history with:
- stable user goals and constraints,
- multi-week training blocks,
- recovery cycles,
- sleep variability,
- HRV and resting-heart-rate changes,
- weight trend changes,
- nutrition patterns,
- manual observations,
- blood-test-like records if later approved for synthetic modeling,
- missing, delayed, noisy, and contradictory records.

Purpose:
- design the product before Garmin blocks progress,
- test coaching answers against known scenarios,
- verify memory and recommendation behavior,
- create replayable golden fixtures,
- preserve V3 operational momentum without external credentials.

The DTU is not a substitute for real validation. It is a controlled design and verification harness for the first POC.

## Ambient Agentic Partner Model
The product should behave like a persistent partner, not a stateless assistant.

Core behavior:
- maintain a running understanding of the user's goals, preferences, constraints, training state, recovery state, nutrition patterns, health context, and active experiments,
- produce scheduled reports when later approved,
- monitor trends and missing data in the background when later approved,
- follow up on prior recommendations,
- ask concise clarifying questions when data is incomplete,
- avoid noisy notifications by using thresholds, cooldowns, and user preferences,
- explain every proactive recommendation with evidence and uncertainty.

Candidate ambient routines:
- morning report: readiness, sleep, recovery, today's training recommendation, notable risks, and one suggested action,
- evening report: training completed, nutrition quality, recovery setup for tomorrow, unresolved data gaps, and follow-up questions,
- weekly review: load, consistency, recovery response, weight/nutrition patterns, experiments, and next-week suggestions,
- alert: only for meaningful trend breaks, missing critical data, aggressive weight loss, sustained poor recovery, or important follow-ups.

The ambient agent should be interruptible and adjustable. The user should be able to change report times, report depth, quiet hours, notification thresholds, and whether proactive messages are enabled.

No live scheduling, background workers, notifications, or Telegram bot behavior are approved by this vision file. They require later mission approval.

## Intent-To-Executable Architecture
The Personal Performance OS should avoid becoming a monolithic prompt or fixed dashboard/report pipeline.

Architectural mental model:
- treat human intent as something the system compiles into a bounded executable workflow,
- expose small, inspectable primitives for data ingestion, normalization, feature derivation, retrieval, evidence selection, safety checks, recommendation writing, and follow-up scheduling,
- keep high-level workflows as convenient compositions of those primitives,
- allow task-specific pipelines for different user questions instead of forcing every question through the same context assembly path,
- persist intermediate state explicitly through database records or serialized artifacts rather than hidden chat context,
- keep active intent/session state independent of any specific client surface,
- make every coaching answer traceable to source records, derived facts, and prior memories.

This is inspired by the deeper architectural shift described in Perplexity's "Rethinking Search as Code Generation" article: search is only the demonstration domain; the larger pattern is compiling intent into executable, inspectable, task-specific programs.

Applied to personal performance intelligence:
- "How recovered am I today?" compiles into a recovery-readiness workflow.
- "Why was my sleep poor last night?" compiles into a causal-investigation workflow.
- "Analyse my last four weeks of training" compiles into a longitudinal-analysis workflow.
- "Should I ride tomorrow?" compiles into a decision-support workflow with safety and uncertainty checks.

Applied to surfaces:
- Telegram should render the workflow as compact conversational messages, voice replies if later approved, and short evidence summaries.
- The desktop conversational app should render the same workflow as a richer full-screen interaction with charts, tables, evidence panels, editable assumptions, and follow-up controls.
- Both surfaces should read and write through the same conversation, intent, evidence, and memory records.
- Image uploads should be normalized into the same intent pipeline as text and voice, with source evidence retained according to approved privacy rules.

Candidate first memory domains:
- activities and training load,
- sleep,
- HRV and resting heart rate,
- weight and body composition,
- nutrition observations,
- blood test records,
- medical PDF records,
- manual notes,
- derived insights,
- user preferences,
- coaching observations and recommendation history.

## Source-Adapter Vision
The product must not be tied to Garmin Connect.

Garmin is one possible source adapter. The core product is the normalized performance, recovery, nutrition, medical, conversation, evidence, and memory model.

Adapter targets:
- Garmin Connect or manual Garmin export/import,
- Apple Health / HealthKit,
- Google Health / Fitbit and Health Connect,
- Polar / AccessLink,
- Strava API,
- medical PDF uploads,
- nutrition label images,
- manual notes and manual imports,
- future smart scales, nutrition systems, labs, and coaching notes.

Each adapter should preserve:
- source identity,
- source record ID or file hash,
- observed time,
- ingested time,
- user permission/consent status,
- source-specific raw payload or replay reference,
- normalized facts,
- confidence and extraction method,
- provenance links used by recommendations.

## Medical PDF Vision
The user should be able to upload doctor-provided medical PDFs, usually containing blood work and periodic analysis.

Target behavior:
- accept PDF upload from an approved surface,
- preserve the original file provenance and retention status,
- extract text/tables only after a later approved PDF extraction mission,
- normalize lab markers with units, reference ranges, collection date, lab/provider, and confidence,
- store doctor comments or report conclusions as source text with provenance,
- allow user correction,
- trend repeated markers over time,
- avoid diagnosis or treatment claims.

Medical PDFs should become evidence for cautious health context, not a medical decision engine.

## Non-Goals
- Public launch.
- Medical advice, diagnosis, treatment, or regulated health claims.
- Production infrastructure unless separately approved.
- Garmin integration before research approval and explicit credential approval.
- Telegram bot creation before a later mission approves bot/token handling.
- Hermes use before separate approval.
- V2-assisted execution.
