# Mission 013: Garmin Bridge Synthetic Shape, Fact Materialization, And Remote Interrupts

## Mission Status
APPROVED (sponsor: Eduardo dos Remedios, 2026-06-04). Sponsor intends to initiate and steer this mission from Codex in the ChatGPT app on Android; the connected host machine remains the execution environment. The closeout must record the actual initiation and answer surfaces honestly.

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO
- Secondary evidence target: candidate `V3-OP-003` (long-running remote-interrupt mission) profile input for the Factory_V3 repository. This mission does not create or approve that profile.

## Roadmap Grounding
- Mission 012 closeout recommendation: research the synthetic shape of the future file-based Garmin manual export/import bridge — source labeling, field mapping, timestamp/duplicate handling, retention choices, rollback semantics for materialized normalized facts, and approval UX for selecting a local export file.
- `HDI-012-001` sponsor decision: `option_a`, manual Garmin export/import, design-and-research priority only.
- Mission 011 residual risk: synthetic source adapters "do not yet persist into the main normalized fact tables as real imports" — this mission closes that gap synthetically.
- Mission 012 design evidence: `.factory-v3/evidence/MISSION_012_REAL_DATA_APPROVAL_DESIGN.md` — this mission implements its approval UX surfaces synthetically.
- D3 transport spike (Factory_V3, 2026-06-04): remote interrupts answered from the phone via Codex in the ChatGPT mobile app are the recommended first remote-interrupt evidence path.

## Sponsor Sizing Direction
The sponsor has directed that this mission deliberately attempt roughly twice Mission 012's measured size (Mission 012: ~115 minutes, 77 tool calls, 8 checkpoints) to test long-mission discipline. This is honored by composing genuinely needed roadmap scope — bridge-shape research, realistic fixture families, adapter integration, fact materialization, fact-level rollback, workflow integration, and approval UX — not by padding. Per `canons/POC_CONSTRAINTS.md` and `canons/ADAPTIVE_MISSION_CONTROL.md`, the duration expectation is an observational guardrail, not a quota: if the objective completes faster, close out honestly and record actual size; do not add files, fixtures, tests, or phases to hit a size target. If the objective proves larger than budget allows, checkpoint, commit, and halt cleanly for a successor mission.

## Objective
Research the public shape of Garmin manual export files, build realistic Garmin-shaped synthetic fixture families, run them through the existing adapter/review pipeline, materialize reviewed synthetic imports into the normalized fact tables with provenance, extend rollback to materialized facts, flow imported facts into the existing workflow/timeline/evidence-graph surfaces, and implement the future real-data approval UX synthetically — pausing for sponsor decisions via remote interrupts answered from the phone.

## Success Criteria

### App outcomes
- Research notes document the public shape of Garmin manual export formats (export families, file types, field naming, units, timestamps) from public documentation only — no login, no account, no real export files downloaded or used.
- A Garmin-shaped synthetic fixture pack exists under `fixtures/garmin_exports/` with a manifest: at least activities, sleep, and body-composition families, each with clean and edge cases (duplicates, timezone boundary, unit conflicts, missing fields, malformed rows). All content is synthetic and clearly labeled synthetic.
- The adapter registry parses Garmin-shaped synthetic exports through the Mission 011/012 preview → review → reviewed-commit pipeline.
- Reviewed synthetic commits materialize into the normalized fact tables with full provenance (source identity, file hash, observed/ingested time, mapping reference, confidence) via a new migration.
- Fact-level rollback exists: a materialized synthetic import can be un-materialized with audit provenance preserved, extending Mission 012's session-level rollback.
- Imported synthetic facts flow into existing surfaces: timelines, evidence graph, and at least two workflows or report candidates consume materialized imported facts with correct evidence references.
- The future real-data approval UX from `MISSION_012_REAL_DATA_APPROVAL_DESIGN.md` exists synthetically in the workbench: consent recording, source labeling, retention choice, and approval state surfaces, exercised only against synthetic fixtures.

### V3 evidence outcomes
- At least two genuine remote human decision interrupts reach `applied` status with answers given by the sponsor from the phone via Codex in the ChatGPT mobile app, each recorded in its interrupt JSON with surface `codex-mobile-thread`, answer text, interpretation, and plan-delta determination.
- At least one deliberate cross-session resume occurs at a natural phase boundary: checkpoint, commit, end session, fresh session resumes from authored artifacts only and lists what it read.
- Every checkpoint fills Budget State with measured values (tool calls, wall-clock, qualitative context use, stop-threshold judgment), and the closeout reports a budget summary comparable against Mission 012's baseline (77 tool calls, ~115 minutes).
- Checkpoint commits follow the Mission 012 convention with before/after hashes.
- Mission record uses `schema_version: v0.1-poc-standalone` including the `adaptive_mission_control` block.

## Human Decision Interrupt Design

### Remote interrupt mechanics (all interrupts)
- The mission writes the interrupt JSON (status `asked`), records a checkpoint, commits, and asks the question in-thread.
- The sponsor answers from the phone via Codex in the ChatGPT mobile app (or from desktop if preferred — record the actual surface honestly).
- The mission records the answer into the interrupt JSON (`answered_by`, answer text verbatim, `selected_option_id`, interpretation), determines whether a plan delta is required, sets `applied`, and continues. The session does not need to end for remote-answered interrupts.
- Fallback: if no answer arrives while other authorized work remains, continue unblocked work; if the mission becomes blocked on the answer, checkpoint, commit, and end the session in `pause` (file-surface fallback as in Mission 012).
- Never fabricate, assume, or default an answer. An ambiguous answer is recorded and re-asked once with sharper options; still-ambiguous means halt.

### HDI-013-001: Fixture family scope and retention posture (required)
- Decision type: `product_decision`.
- Question shape: which Garmin export families beyond the required three (activities, sleep, body composition) should the fixture pack include (e.g., wellness/HRV, stress, hydration, none), and which default retention posture should the approval UX present for future real imports (keep-raw-and-normalized, keep-normalized-only, keep-raw-until-verified)?
- Options must include effects and risks; recommended option stated.

### HDI-013-002: Materialization conflict strategy (required)
- Decision type: `product_decision`.
- Question shape: when a materialized imported fact overlaps an existing fact (same domain and time window from DTU fixtures or a prior import), should materialization reject the conflicting rows, version them side by side with source precedence, or overwrite with audit trail? Genuine because it defines the bridge's core data semantics and affects rollback design.

### HDI-013-003: Optional
- Raise only if implementation surfaces a genuine additional decision (e.g., approval UX consent wording, workflow evidence precedence). Do not invent interrupts to satisfy evidence goals.

## Non-Goals
- No real personal health, fitness, nutrition, medical, image, voice, or identity data.
- No real Garmin export files, even publicly posted samples (they may contain a real person's data); shapes are modeled from documentation only.
- No Garmin login, account, credentials, API calls, scraping, or unofficial clients.
- No Apple Health, Google Health/Fitbit, Health Connect, Polar, Strava, Telegram, OCR/vision execution, voice transcription, scheduler, notification delivery, Hermes, public deployment, or production infrastructure.
- No package installation.
- No real-data bridge activation: the approval UX is exercised against synthetic fixtures only; no real import path is enabled.
- No git push, pull, branch, merge, rebase, tag, reset, checkout, remote, or init operations.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_013_GARMIN_BRIDGE_SHAPE_MATERIALIZATION_AND_REMOTE_INTERRUPTS.md`
- `.factory-v3/evidence/MISSION_013_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_013_GARMIN_EXPORT_SHAPE_RESEARCH.md`
- `.factory-v3/evidence/MISSION_013_STATE.md`
- `.factory-v3/evidence/MISSION_013_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_013_INTERRUPT_HDI001.json`
- `.factory-v3/evidence/MISSION_013_INTERRUPT_HDI002.json`
- `.factory-v3/evidence/MISSION_013_INTERRUPT_HDI003.json` (only if HDI-013-003 is raised)
- `.factory-v3/evidence/MISSION_013_PLAN_DELTA_001.md` and `_002.md` (only if deltas are required)
- `.factory-v3/evidence/MISSION_013_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_013_RECORD.json`
- `.factory-v3/evidence/MISSION_013_AUDIT_SUMMARY.json`
- `.factory-v3/evidence/MISSION_013_BROWSER_NOTES.md`
- `fixtures/garmin_exports/` (new synthetic fixture directory and manifest)
- `ppos_core/garmin_bridge.py` (new)
- `ppos_core/manual_imports.py`
- `ppos_core/migrations/005_mission_013.sql`
- `ppos_core/storage.py`
- `ppos_core/repositories.py`
- `ppos_core/schema.py`
- `ppos_core/primitives.py`
- `ppos_core/workflows.py`
- `ppos_core/reports.py`
- `ppos_core/timeline.py`
- `ppos_core/evidence_graph.py`
- `ppos_core/api.py`
- `ppos_core/workbench.py`
- `workbench/index.html`
- `workbench/app.js`
- `workbench/styles.css`
- `scripts/mission_013_bridge_qa.py`
- `scripts/verify_mission_013.py`
- `tests/test_mission_013_garmin_fixtures.py`
- `tests/test_mission_013_bridge_adapter.py`
- `tests/test_mission_013_materialization.py`
- `tests/test_mission_013_fact_rollback.py`
- `tests/test_mission_013_workflow_integration.py`
- `tests/test_mission_013_approval_ux.py`
- `tests/test_mission_013_api.py`

## Forbidden Scope
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or Factory_V3 repo tooling.
- Real data or real export files from any source, including public sample files of real exports.
- Credentials, tokens, account login, OAuth apps, BotFather, webhooks, long polling, live messages, scraping, external API calls (other than authorized public-documentation research), or live third-party integration.
- OCR/vision execution, voice transcription execution, medical PDF ingestion, scheduler/cron/worker/daemon/queue/notification delivery, Hermes, package install, or public deployment.
- Git operations beyond the explicit authority below.
- Continuing past a blocking unanswered interrupt or fabricating the sponsor's answer.
- Padding scope, files, fixtures, or tests to reach the sizing guardrail.

## Git Authority
- Allowed: `git status --short --branch`, `git diff --stat`, `git log --oneline -n <N>`, `git add <authorized paths only>`, `git commit -m "Mission 013 checkpoint <NNN>: <summary>"` (and `Mission 013 closeout`).
- Commit cadence: after each completed checkpoint, immediately before any session end (interrupt pause, budget stop, or deliberate resume boundary).
- Each checkpoint records `commit_before` and `commit_after` hashes.
- Forbidden: push, pull, fetch, branch, merge, rebase, tag, reset, checkout, remote changes, init, and any commit touching files outside mission authority.

## Allowed Commands
- Read/search/status: `pwd`, `ls`, `find`, `sed`, `rg`, plus the git commands authorized above.
- Public-documentation research for Garmin export shapes via the harness's built-in web search/browse against public documentation pages only: no login, no account creation, no file downloads, no real export samples. Citations recorded in `MISSION_013_GARMIN_EXPORT_SHAPE_RESEARCH.md`.
- Python stdlib verification: `python3 -B -m unittest discover -s tests`, `python3 -B scripts/mission_013_bridge_qa.py --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`, `python3 -B scripts/verify_mission_013.py`.
- JSON parse checks: `python3 -m json.tool` on the Mission 013 record, audit summary, interrupt files, and fixture manifests.
- Local API server: `python3 -B -m ppos_core.api --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`.
- Mission-owned local process cleanup only: `lsof -ti tcp:<mission port>`, `kill <mission server pid>`.
- Built-in Codex Browser against `http://127.0.0.1:<mission port>/workbench/` only.

## Dependency Policy
- New dependencies allowed: NO
- If YES, approval reference: not applicable
- Install command: not applicable
- Rollback plan: not applicable

## Budget Instrumentation
- Every checkpoint fills Budget State with measured values per the Mission 012 method: tool-call count since last checkpoint, wall-clock time, qualitative context-use estimate with method stated, stop-threshold judgment.
- Baseline for comparison: Mission 012 totals (77 tool calls, ~115 minutes through checkpoint 008). The closeout must compare actuals against roughly 2x this baseline and state honestly whether the sizing direction was met, exceeded, or not needed.
- Stop threshold: if context or usage pressure makes completing the current phase plus a clean checkpoint uncertain, stop work, write the checkpoint, commit, and end the session with a reentry instruction. A budget-driven session end plus fresh-session resume is acceptable evidence, not a failure.
- Mid-mission budget review: at every third checkpoint, explicitly compare cumulative spend against remaining phases and record a continue/halt/descope judgment.

## Phases And Checkpoint Cadence
Checkpoints at minimum after each of:
1. Mission plan authored.
2. Garmin export shape research complete (research notes written, citations recorded).
3. HDI-013-001 asked (and committed before any pause).
4. HDI-013-001 applied; fixture pack built per the answer; manifest passes parse checks.
5. Bridge adapter parses all fixture families through preview/review.
6. HDI-013-002 asked/applied; materialization implemented per the answer (migration, provenance, conflict strategy).
7. Deliberate cross-session resume boundary: checkpoint, commit, end session; fresh session resumes from artifacts and records what it read.
8. Fact-level rollback implemented and tested.
9. Workflow/timeline/evidence-graph integration passing.
10. Approval UX implemented; stdlib verification and Browser QA complete.
11. Final closeout.

The mission may add checkpoints at natural boundaries but may not skip listed ones.

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: all existing and Mission 013 tests pass.
- `python3 -B scripts/mission_013_bridge_qa.py --db /tmp/ppos_mission_013_qa.sqlite --host 127.0.0.1 --port 8800`: fixture catalog, preview/review, materialization, fact rollback, workflow consumption, and approval UX flows pass; writes the authorized audit summary.
- `python3 -B scripts/verify_mission_013.py`: checks envelope, state, checkpoints, closeout, record; verifies both required interrupts parse and reached `applied` with non-empty answers and recorded surfaces; verifies the plan-delta rule per interrupt; verifies every checkpoint Budget State contains measured values and the two mid-mission budget reviews exist; verifies the cross-session resume evidence; verifies checkpoint commits in `git log` match the convention; verifies no real-data markers in `fixtures/garmin_exports/` (all fixtures carry synthetic labels); runs the no-go scan.
- JSON parse checks for record, audit summary, interrupt files, and fixture manifest pass.
- Browser QA: import lab handles Garmin-shaped fixtures end to end (select, preview, review, reviewed commit, materialize, rollback), approval UX surfaces render and persist state, timelines/evidence graph show imported facts, no runtime errors; desktop and mobile/responsive checks attempted.

## Adaptive Mission Control
- Checkpoints required: YES (cadence above).
- Mission state file: `.factory-v3/evidence/MISSION_013_STATE.md`
- Human decision interrupts allowed: YES (HDI-013-001 and HDI-013-002 required; HDI-013-003 optional and only if genuine).
- Interrupt surfaces allowed: codex-mobile-thread (primary) | thread | file (fallback with pause, as Mission 012).
- Timeout behavior for unresolved blocking interrupts: pause.
- Cross-session resume: REQUIRED at least once (checkpoint 7 boundary, or a budget-driven session end if one occurs earlier — one deliberate resume minimum either way). The resuming session must list in the state file exactly which artifacts it read and must not rely on prior chat context.
- Plan delta required before scope change: YES.
- Verification side effects allowed: YES; authorized output paths are the Mission 013 evidence files listed under Authorized Files.

## Halt Rules
Stop if:
- Factory V2 or Factory_V3 repo tooling appears necessary.
- Real data, real export files, credentials, live integration, package install, Telegram live behavior, OCR/vision, voice transcription, scheduler, notification, Hermes, public deployment, or production infrastructure appears.
- Research requires login, account creation, or downloading real export samples.
- A blocking interrupt answer is missing, ambiguous after one re-ask, or would require unauthorized scope.
- Verification requires source paths, commands, dependencies, or git authority not authorized by this mission.
- Materialization or rollback work would mutate or destroy prior mission evidence or audit history.
- Mission state/checkpoint evidence becomes stale or contradicts repository state.
- Budget stop threshold is reached (checkpoint, commit, end session with reentry instruction).
- The objective is met early: close out honestly rather than padding toward the sizing guardrail.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as a fallback while claiming POC readiness.

## Reentry Rules
- Resume only from authored mission artifacts: this envelope, `.factory-v3/evidence/MISSION_013_STATE.md`, the latest checkpoint, the interrupt files, and current repository state.
- A resume across a blocking interrupt pause is valid only if that interrupt's status is `answered` or `applied`; if still `asked`, remain paused.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md`. The closeout must additionally report: interrupt lifecycle summary per interrupt (timestamps, surfaces, verbatim answers, deltas); remote-surface evidence (which answers came from the phone); resume evidence; budget summary with the 2x-Mission-012 comparison and an honest sizing verdict; checkpoint-commit list; long-mission friction observations (what strained checkpoints, state, or context discipline); and the recommended Mission 014.
