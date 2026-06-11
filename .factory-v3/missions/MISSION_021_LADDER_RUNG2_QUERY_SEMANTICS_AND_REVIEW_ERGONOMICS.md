# Mission 021: Duration-Ladder Rung 2 — Imported-Fact Query Semantics And Operator Review Ergonomics

## Mission Status
DRAFT — PENDING SPONSOR GO. This envelope approves nothing; the rung-2 run starts only on explicit sponsor Go naming the run window, after the pre-mission transport delivery test passes.

Drafting provenance: authored 2026-06-11 in a Claude Code session (model `claude-fable-5`) under Factory_V3 mission `LADDER_RUNG2_PREP` authority chain (sponsor Go in-thread, "ok agree proceed"); the run itself executes under the Codex harness per sponsor decision `HDI-RUNG2-001`. This envelope supersedes the unexecuted `MISSION_014_IMPORTED_FACT_QUERY_SEMANTICS_AND_REVIEW_ERGONOMICS.md` draft (2026-06-04, never committed, never run), carrying its objective and pre-resolved decisions forward with mission-021 artifact names and rung-2 instrumentation.

## Ladder Identity
- POC mission number: 021
- Ladder mission ID: `LADDER_RUNG2_<run date YYYYMMDD, stamped at sponsor Go>`
- Ladder role: rung 2 of 3 per Factory_V3 `DURATION_LADDER_PLAN.md` v0.4; supplies decision-pack evidence items 1-3 for `V3_OP_003_DECISION_PACK.md`
- Headline size: roughly 2 hours (human-readable headline only; measured pass criteria below per `HDI-TT-002`)
- Duration burden: this rung carries the genuine-duration requirement explicitly per `HDI-TT-001` — a run that compresses far below the duration band does not pass the rung regardless of mechanics. No padding to reach the band: if the objective completes early honestly, close out honestly, record the compression, and the rung is rerun later with genuinely larger scope.

## Profile
- Profile ID: `V3-POC-STANDALONE`; executes under existing approved authority per waypoint (`V3-OP-001` eligibility per waypoint); `V3-OP-003` remains a candidate profile — this mission gathers its evidence and is not governed by it.
- V3-only: YES. V2 allowed: NO.
- Harness: Codex (per `HDI-RUNG2-001`); model identity observed and recorded at mission start and at every checkpoint (`MUTABLE_HARNESS_STATE.md` discipline). Transport availability is org-policy-gated runtime state: record the transport's observed working state at mission start.

## Transport (Rung-2 Live Interrupt)
- Transport: Codex mobile (ChatGPT app surface), per sponsor decision `HDI-RUNG2-001` (Factory_V3 `ladder/rung2/RUNG2_TRANSPORT_DECISION_HDI_RUNG2_001.md`).
- Pre-mission delivery test: before Go, one test round-trip must confirm the question reaches the sponsor's phone and an answer reaches the session. A failed delivery test blocks Go.
- Away protocol: the planned Tier 3 interrupt (WP4) fires inside a pre-agreed window during which the sponsor is genuinely away from the terminal (MR_020 focus-suppression finding: an attended sponsor never sees the notification surface). The sponsor answers from the phone.
- Interrupt records store question, options, answer, command-sourced timestamps, and transport name only — no device identifiers, phone numbers, or vendor account metadata.

## Measured Pass Criteria (Budget-And-Waypoint Classes, per HDI-TT-002)
1. Waypoint class: 8 waypoints per the table below, all closed with per-waypoint verification cited.
2. Tool-call budget: forecast 400-600 tool calls (labeled forecast, derived from measured M012/M013 actuals plus rung-2 instrumentation overhead); stop threshold 700.
3. Duration band: 90-180 minutes wall clock from command-sourced timestamps (mission start to closeout), with genuine duration per `HDI-TT-001`.
4. One live Tier 3 interrupt round-trip over Codex mobile with the sponsor away from the terminal, producing a complete interrupt record (full `ADAPTIVE_MISSION_CONTROL.md` field set, named timeout, answer source, plan delta).
5. One deliberate mid-mission pause and fresh-session reentry from authored artifacts alone (envelope, state, checkpoints, deferred-decisions log, git state), with artifacts-read evidence in the state file.
6. Checkpoint series complete: all six `MISSION_HEALTH_VOCABULARY.md` signals with one-line citations at every checkpoint, plus per-checkpoint recording cost, plus model identity.
7. Friction counters recorded at closeout per `DURATION_LADDER_PLAN.md` v0.4: governance-overhead ratio, per-artifact authoring cost, Go-to-first-edit count.
8. Rung-1 criteria hold at duration: budget actuals within stop threshold, no scope-drift findings, advisory/verification suite passing at closeout.

## Objective
Implement source-precedence query semantics, full-provenance conflict drill-down, richer imported-fact filtering, and the visible-but-inert real-data approval checklist over the Mission 013 materialized-fact layer — at rung-2 duration, with one live phone-answered Tier 3 interrupt and one deliberate pause/reentry.

## Waypoint Table (mission_waypoint candidate trial)
This table trials the `mission_waypoint` candidate shape from Factory_V3 `SHADOW_SCHEMA_CANDIDATES.md` v0.3: essential fields plus provisional type labels. It is a documentation shape only — it adds no required fields, validators, or gates. Waypoint `named_scope` is a restriction projection of this envelope's authority and never widens it; a waypoint needing more authority is a Tier 3 interrupt or plan delta. `budget_slice` values are labeled forecasts grounding marginal-burn comparison only; the mission-level stop threshold is the only stop authority. Waypoint completion is recorded in the waypoint-boundary checkpoint, citing the verification output.

| id | type | objective | named_scope | verification | expected_artifacts | budget_slice (forecast) |
| --- | --- | --- | --- | --- | --- | --- |
| WP1 | discovery | Verify POC canon/template parity with AMC v0.2 conventions (sync only if stale); author implementation plan | `.factory-v3/canons/ADAPTIVE_MISSION_CONTROL.md`, `.factory-v3/templates/`, `.factory-v3/evidence/MISSION_021_IMPLEMENTATION_PLAN.md` | `diff` parity check output; plan exists with per-waypoint approach | implementation plan; parity note in state file | 40-60 calls |
| WP2 | build | Deterministic precedence engine per PRD-021-001 with migration and unit tests (including tie cases) | `ppos_core/precedence.py` (new), `ppos_core/migrations/006_mission_021.sql`, `ppos_core/schema.py`, `ppos_core/storage.py`, `ppos_core/repositories.py`, `tests/test_mission_021_precedence.py` | `python3 -B -m unittest` precedence tests pass; full suite still passes | precedence module, migration, tests | 70-100 calls |
| WP3 | build | Query/API endpoints exposing precedence and filtering backend per Tier 2 priority order | `ppos_core/api.py`, `ppos_core/manual_imports.py`, `ppos_core/garmin_bridge.py`, `ppos_core/timeline.py`, `tests/test_mission_021_api.py`, `tests/test_mission_021_filtering.py` | API and filtering tests pass; full suite still passes | endpoints, filtering backend, tests | 70-100 calls |
| WP4 | decision | Raise the planned Tier 3 interrupt over Codex mobile (sponsor away, named timeout); apply the answer; checkpoint; deliberate pause: commit and end session | `.factory-v3/evidence/MISSION_021_INTERRUPT_HDI001.json`, `.factory-v3/evidence/MISSION_021_STATE.md`, `.factory-v3/evidence/MISSION_021_CHECKPOINTS.md` | interrupt record complete (all AMC fields, command-sourced ask/deliver/answer timestamps); pause checkpoint committed | interrupt record; pause checkpoint; plan delta if the answer requires one | 20-40 calls |
| WP5 | build | Fresh-session reentry from authored artifacts alone; conflict drill-down backend and workbench UI per PRD-021-002 | `ppos_core/evidence_graph.py`, `ppos_core/workbench.py`, `workbench/index.html`, `workbench/app.js`, `workbench/styles.css`, `tests/test_mission_021_drilldown.py` | artifacts-read reentry evidence in state file; drill-down tests pass for duplicate, unit-conflict, and overlapping-window fixture cases | reentry evidence; drill-down backend + UI; tests | 80-110 calls |
| WP6 | build | Filtering UI with combined filters persisted as URL state; visible-but-inert real-data approval checklist per PRD-021-003 | `workbench/index.html`, `workbench/app.js`, `workbench/styles.css`, `ppos_core/workbench.py`, `tests/test_mission_021_checklist.py` | checklist tests prove no UI action can enable it; filtering UI test passes | filtering UI, inert checklist, tests | 60-90 calls |
| WP7 | verification | Full stdlib suite, mission QA script, browser QA (desktop and mobile/responsive attempted) | `scripts/mission_021_query_ergonomics_qa.py`, `scripts/verify_mission_021.py`, `tests/` (run only), built-in Codex Browser against the mission localhost port | all 170+ tests pass; QA script passes and writes the authorized audit summary; verify script passes | QA outputs, audit summary, browser notes | 40-70 calls |
| WP8 | closeout | Closeout record, budget actuals vs forecast (timestamp-derived), friction counters, health-signal series review, recommended next mission | `.factory-v3/evidence/MISSION_021_CLOSEOUT.md`, `.factory-v3/evidence/MISSION_021_RECORD.json`, `.factory-v3/evidence/MISSION_021_AUDIT_SUMMARY.json` | JSON parse checks pass; closeout reports every Measured Pass Criteria item with evidence paths | closeout, record, friction-counter block | 30-50 calls |

## Pre-Resolved Decisions (Tier 1)
- PRD-021-001 Source precedence default: imported (Garmin-shaped synthetic) facts rank above DTU fixture facts; ties within the same rank break by most recent ingestion time. Decided by sponsor, 2026-06-04 (carried from M014 draft).
- PRD-021-002 Conflict drill-down depth: full provenance chain — conflicting fact → source file → mapping row → import session → review state → consuming workflows/reports. Decided by sponsor, 2026-06-04 (carried).
- PRD-021-003 Real-data approval checklist posture: visible but inert; all items render with controls disabled and a clear banner that real-data use requires a separately approved real-data mission; no flag-gated hiding. Decided by sponsor, 2026-06-04 (carried).
- PRD-021-004 Rung-2 shape: this mission is the duration-ladder rung 2 with the seeded live interrupt and deliberate pause/reentry; transport is Codex mobile per `HDI-RUNG2-001`. Decided by sponsor, 2026-06-11.
- PRD-021-005 Supersession: the unexecuted Mission 014 draft is superseded by this envelope; its scope carries forward under mission-021 artifact names. Decided at envelope drafting, 2026-06-11; sponsor confirmation at Go.

## Decision Principles (Tier 2)
Resolve-and-log within mission authority; record each choice in the deferred-decisions log:
- Filtering dimensions in priority order: source, domain, date range, review state, conflict status; if scope strains against budget, drop from the tail and log the cut.
- Query API shapes, parameter naming, SQLite index choices, and pagination follow existing `ppos_core` conventions; UI follows existing workbench patterns; precedence and conflict indicators always show source identity and timestamps.
- Precedence is a deterministic, testable ranking function with provenance preserved — never implemented by mutating or deleting lower-ranked facts.
- Checklist banner wording copies the boundary phrasing style of `canons/POC_CONSTRAINTS.md`.

## Planned Tier 3 Interrupt (WP4)
- Question class: operator default landing view for the imported-fact workbench — which filter combination and precedence-display emphasis the operator sees first. This is a genuine, sponsor-undecided user-experience choice (a valid Tier 3 class per `ADAPTIVE_MISSION_CONTROL.md`), reusing the MR_020 finding that genuinely pending decisions make better trial interrupts than synthetic throwaway questions.
- The interrupt record must contain the full AMC field set including pre-resolution check (why Tier 1/2 cannot answer), options with risks, recommended option, named timeout, and command-sourced ask/deliver/answer timestamps.
- No-response rule: if the named timeout expires unanswered, follow the safe-hold rule — record the timeout as the answer-source outcome, checkpoint, commit, enter safe-hold (no further file changes; read-only commands only), and halt cleanly with a reentry instruction after the safe-hold window. Never infer an answer.

## Health-Signal And Instrumentation Requirements
- Every checkpoint records all six `MISSION_HEALTH_VOCABULARY.md` signals with one-line citations, the per-checkpoint recording cost (tool calls spent on the checkpoint itself), model identity, and the AMC v0.2 timestamped Budget State.
- `drift` grounds against the active waypoint's `named_scope` (waypoint-table trial); an edit inside envelope authority but outside the active waypoint's scope is recorded as a drift observation, not a violation, and routes to the deferred-decisions log.
- Telemetry is checkpoint-level, not per-event.
- Economics terms from `MISSION_ECONOMICS_VOCABULARY.md` are NOT recorded in this rung (first economics recording is rung 3); this rung records the friction counters that decide economics affordability.
- Friction counters at closeout per `DURATION_LADDER_PLAN.md` v0.4: (1) governance-overhead ratio (governance tool calls vs objective tool calls), (2) per-artifact authoring cost for envelope-referenced evidence artifacts, (3) Go-to-first-objective-edit count. Advisory observations, never targets.

## Checkpoint Cadence
At minimum: end of every waypoint, before raising the WP4 interrupt, at the pause boundary, immediately after reentry, and at any budget threshold. Listed checkpoints may not be skipped.

## Non-Goals
- No real data, real exports, credentials, live integrations beyond the named Codex mobile interrupt surface, OCR/vision, voice, scheduler, ambient runtime, Telegram, package installs, public deployment, or production infrastructure.
- No enabling path for the real-data checklist.
- No Factory V2 use; no edits to the Factory_V3 repository.
- No economics-term recording; no new vocabulary, schema, or validator work.
- No git push, pull, branch, merge, rebase, tag, reset, checkout, remote, or init.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_021_LADDER_RUNG2_QUERY_SEMANTICS_AND_REVIEW_ERGONOMICS.md`
- `.factory-v3/canons/ADAPTIVE_MISSION_CONTROL.md` and `.factory-v3/templates/` (WP1 parity sync only)
- `.factory-v3/evidence/MISSION_021_IMPLEMENTATION_PLAN.md`, `MISSION_021_STATE.md`, `MISSION_021_CHECKPOINTS.md`, `MISSION_021_DEFERRED_DECISIONS.md`, `MISSION_021_INTERRUPT_HDI001.json`, `MISSION_021_PLAN_DELTA_001.md` (only if required), `MISSION_021_CLOSEOUT.md`, `MISSION_021_RECORD.json`, `MISSION_021_AUDIT_SUMMARY.json`, `MISSION_021_BROWSER_NOTES.md`
- `ppos_core/precedence.py` (new), `ppos_core/migrations/006_mission_021.sql` (new)
- `ppos_core/manual_imports.py`, `ppos_core/garmin_bridge.py`, `ppos_core/repositories.py`, `ppos_core/storage.py`, `ppos_core/schema.py`, `ppos_core/timeline.py`, `ppos_core/evidence_graph.py`, `ppos_core/api.py`, `ppos_core/workbench.py`
- `workbench/index.html`, `workbench/app.js`, `workbench/styles.css`
- `scripts/mission_021_query_ergonomics_qa.py`, `scripts/verify_mission_021.py`
- `tests/test_mission_021_precedence.py`, `test_mission_021_drilldown.py`, `test_mission_021_filtering.py`, `test_mission_021_checklist.py`, `test_mission_021_api.py`

## Forbidden Scope
Everything in Non-Goals; Factory V2 tooling; real data of any kind; deleting or mutating lower-ranked facts to implement precedence; any checklist-enable path; files outside the authorized list; the superseded Mission 014 draft file (leave untouched).

## Git Authority
- Allowed: `git status --short --branch`, `git diff --stat`, `git log --oneline -n <N>`, `git add <authorized paths only>`, `git commit -m "Mission 021 checkpoint <NNN>: <summary>"`, final `git commit -m "Mission 021 closeout"`.
- Commit cadence: after each completed checkpoint, at the WP4 pause, and immediately before any session end.
- Checkpoints record `commit_before`/`commit_after`.
- Forbidden: push, pull, fetch, branch, merge, rebase, tag, reset, checkout, remote changes, init.

## Allowed Commands
- Read/search/status: `pwd`, `ls`, `find`, `sed`, `rg`, plus authorized git commands.
- Timestamps: `date -u +%Y-%m-%dT%H:%M:%SZ` at every checkpoint and interrupt event.
- Python stdlib verification: `python3 -B -m unittest discover -s tests`, `python3 -B scripts/mission_021_query_ergonomics_qa.py --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`, `python3 -B scripts/verify_mission_021.py`.
- JSON parse checks on record, audit summary, and interrupt files.
- Local API server: `python3 -B -m ppos_core.api --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`; mission-owned cleanup: `lsof -ti tcp:<mission port>`, `kill <mission server pid>`.
- Built-in Codex Browser against `http://127.0.0.1:<mission port>/workbench/` only.

## Dependency Policy
New dependencies allowed: NO.

## Halt Rules
Stop if: V2 or Factory_V3 tooling appears necessary; real data/credentials/live integration beyond the named interrupt surface appears; the transport fails with a Tier 3 decision pending (V2 fallback trigger per the candidate profile); a genuine unplanned Tier 3 decision blocks all authorized work; verification requires unauthorized scope; precedence work would mutate or destroy evidence or audit history; state/checkpoint evidence goes stale; checkpoint or state writing fails twice; safe-hold is entered twice; budget stop threshold reached; the objective completes early (close out honestly and record the compression against the duration band).

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap.

## Reentry Rules
- Resume only from authored artifacts (envelope, state, latest checkpoint, deferred-decisions log, interrupt files) and current repository state; record the artifacts read.
- Halt if derived state conflicts with authored artifacts.
- Resolve any open interrupt before further edits.

## Closeout
Must report, with evidence paths: every Measured Pass Criteria item; forecast-vs-actual variance (timestamp-derived); the friction-counter block; per-checkpoint health-signal series with recording costs; waypoint-table trial observations (which fields earned their cost, which did not); interrupt latency observations (ask-to-deliver, deliver-to-answer, command-sourced); pause/reentry evidence; deferred-decisions review; checkpoint-commit list; recommended next mission. The rung is then adjudicated by the sponsor against this envelope's measured criteria in the Factory_V3 ladder lane.
