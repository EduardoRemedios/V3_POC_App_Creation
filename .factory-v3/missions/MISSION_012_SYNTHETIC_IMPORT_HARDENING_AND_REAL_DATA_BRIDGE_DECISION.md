# Mission 012: Synthetic Import Hardening And Real-Data Bridge Decision

## Mission Status
APPROVED (sponsor: Eduardo dos Remedios, 2026-06-04)

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO

## Roadmap Grounding
- Mission 011 closeout recommended next step: manual import product hardening and operator review workflow, synthetic-only, with side-by-side raw/normalized diff UX, rollback semantics, and explicit future real-data approval interrupt design.
- Mission 006 roadmap placeholder "First Real Data Bridge Decision" (`research_decision`): choose the first real-data bridge candidate using the criteria data value, implementation cost, privacy risk, credential risk, verification ability, and personal-use suitability. The placeholder does not authorize implementation; this mission surfaces that decision as a human decision interrupt and records it. It does not execute any real-data work.
- Interim POC eval (2026-06-04, `PASS_WITH_LIMITATIONS`): this mission is deliberately instrumented to close four named limitations — unproven interrupt lifecycle, no cross-session resume evidence, unfilled budget fields, and no git mission authority.

## Objective
Harden the synthetic manual-import lab into an operator review workflow (raw/normalized diff, commit rollback, review states), and surface the first real-data bridge decision to the sponsor as a structured human decision interrupt — while producing the POC's first replayable interrupt, plan-delta, budget, checkpoint-commit, and cross-session-resume evidence. Synthetic-only throughout.

## Success Criteria

### App outcomes
- Side-by-side raw/normalized diff view exists in the import lab for preview rows.
- Synthetic import sessions support rollback: a committed synthetic import can be reverted with provenance preserved (rollback recorded, not destructive deletion of audit history).
- Operator review workflow exists: preview rows can be marked accepted/rejected/needs-clarification before synthetic commit, persisted in SQLite and surfaced in the workbench.
- A design evidence document specifies the future real-data approval workflow (consent, source labeling, retention, rollback), shaped by the sponsor's interrupt answer. Design only — no real-data behavior is implemented.

### V3 evidence outcomes
- At least one genuine human decision interrupt reaches `applied` status using the file surface: `HDI-012-001` (first real-data bridge choice). The interrupt JSON records question, options with risks, recommended option, the sponsor's answer, interpretation, and continuation decision.
- A plan delta is recorded if and only if the answer changes mission scope; otherwise the record states why no delta was required.
- A deliberate cross-session resume occurs: the session ends while `HDI-012-001` is in `asked` status; the sponsor answers by editing the interrupt JSON; a fresh session resumes from authored artifacts only and continues the mission.
- Every checkpoint fills the Budget State fields with measured values: approximate context usage where visible, tool-call count since last checkpoint, wall-clock time, and an explicit stop-threshold judgment.
- Checkpoint commits exist: each completed checkpoint is followed by a git commit of authorized paths, with before/after hashes recorded in the checkpoint.
- Mission record uses `schema_version: v0.1-poc-standalone` including the `adaptive_mission_control` block.

## Eligible-Work Rationale
Larger than Mission 011 by natural surface: review workflow, rollback semantics, diff UX, decision-interrupt evidence, and resume instrumentation. Bounded because it remains local-only, synthetic-only, stdlib-only, and the real-data decision is recorded, not executed. Size emerges from the objective per `canons/POC_CONSTRAINTS.md`; no padding to hit size targets.

## Human Decision Interrupt Design

### HDI-012-001: First real-data bridge choice (required)
- Decision type: `product_decision` (with `dependency_decision` implications for a future mission).
- Question: which real-data bridge should the future approval workflow be designed around, and which should Mission 013+ research first?
- Options (from the Mission 006 placeholder, scored in `context_summary` against data value, implementation cost, privacy risk, credential risk, verification ability, personal-use suitability):
  - `option_a` manual Garmin export/import (file-based, no credentials),
  - `option_b` Apple Health export/HealthKit bridge,
  - `option_c` Health Connect bridge,
  - `option_d` Strava activity API,
  - `option_e` medical PDF upload,
  - `option_f` nutrition image upload,
  - `option_g` defer the decision.
- Surface: `file` — the mission writes `.factory-v3/evidence/MISSION_012_INTERRUPT_HDI001.json`, sets status `asked`, records the checkpoint, commits, and ends the session. The sponsor answers by editing the `answer` block, then instructs a fresh session to resume.
- Timeout behavior: `pause` (mission stays halted until answered; no continuation without an answer).
- Effect boundary: the answer authorizes design work inside this mission only. It does not approve real data, credentials, exports, API calls, or any implementation in this or any future mission. Garmin/other source implementation still requires its own separately approved mission per `canons/POC_CONSTRAINTS.md` and `canons/DEPENDENCY_RESEARCH.md`.

### HDI-012-002: Rollback semantics (optional, only if genuinely ambiguous)
- Decision type: `product_decision`. Example genuine question: whether rollback should restore prior normalized facts or only mark the import session reverted. Raise only if implementation surfaces a real choice the envelope does not settle; do not invent an interrupt to satisfy evidence goals.

## Non-Goals
- No real personal health, fitness, nutrition, medical, image, voice, or identity data.
- No real export files from any source; synthetic fixtures only.
- No Garmin/Apple/Google/Polar/Strava login, credentials, API calls, scraping, or account access.
- No Telegram, OCR/vision execution, voice transcription, scheduler, notification delivery, Hermes, public deployment, or production infrastructure.
- No package installation.
- No real-data bridge implementation: HDI-012-001 produces a recorded decision and design evidence only.
- No git push, pull, branch, merge, rebase, tag, reset, checkout, remote, or init operations.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_012_SYNTHETIC_IMPORT_HARDENING_AND_REAL_DATA_BRIDGE_DECISION.md`
- `.factory-v3/evidence/MISSION_012_IMPLEMENTATION_PLAN.md`
- `.factory-v3/evidence/MISSION_012_STATE.md`
- `.factory-v3/evidence/MISSION_012_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_012_INTERRUPT_HDI001.json`
- `.factory-v3/evidence/MISSION_012_INTERRUPT_HDI002.json` (only if HDI-012-002 is raised)
- `.factory-v3/evidence/MISSION_012_PLAN_DELTA_001.md` (only if a delta is required)
- `.factory-v3/evidence/MISSION_012_REAL_DATA_APPROVAL_DESIGN.md`
- `.factory-v3/evidence/MISSION_012_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_012_RECORD.json`
- `.factory-v3/evidence/MISSION_012_AUDIT_SUMMARY.json`
- `.factory-v3/evidence/MISSION_012_BROWSER_NOTES.md`
- `fixtures/manual_exports/` (additional synthetic fixtures if needed)
- `ppos_core/manual_imports.py`
- `ppos_core/migrations/004_mission_012.sql`
- `ppos_core/storage.py`
- `ppos_core/api.py`
- `ppos_core/workbench.py`
- `workbench/index.html`
- `workbench/app.js`
- `workbench/styles.css`
- `scripts/mission_012_review_rollback_qa.py`
- `scripts/verify_mission_012.py`
- `tests/test_mission_012_review_workflow.py`
- `tests/test_mission_012_rollback.py`
- `tests/test_mission_012_api.py`

## Forbidden Scope
- Factory V2, `factoryctl`, `stage-lint`, `pack-lint`, V2 stages, V2 fallback, or Factory_V3 repo tooling.
- Real data or real exports from any source.
- Credentials, tokens, account login, OAuth apps, BotFather, webhooks, long polling, live messages, scraping, external API calls, or live third-party integration.
- OCR/vision execution, voice transcription execution, medical PDF ingestion, scheduler/cron/worker/daemon/queue/notification delivery, Hermes, package install, or public deployment.
- Git operations beyond the explicit authority below.
- Continuing past an unanswered interrupt or fabricating/assuming the sponsor's answer.

## Git Authority
- Allowed: `git status --short --branch`, `git diff --stat`, `git log --oneline -n <N>`, `git add <authorized paths only>`, `git commit -m "Mission 012 checkpoint <NNN>: <summary>"`.
- Commit cadence: after each completed checkpoint (verification for that phase passing or explicitly `not_run` with reason), and immediately before ending the session for the HDI-012-001 interrupt pause.
- Commit message convention: `Mission 012 checkpoint 001: <phase summary>` (and `Mission 012 closeout` for the final commit).
- Each checkpoint records `commit_before` and `commit_after` hashes.
- Forbidden: push, pull, fetch, branch, merge, rebase, tag, reset, checkout, remote changes, init, and any commit touching files outside mission authority.

## Allowed Commands
- Read/search/status: `pwd`, `ls`, `find`, `sed`, `rg`, plus the git commands authorized above.
- Python stdlib verification: `python3 -B -m unittest discover -s tests`, `python3 -B scripts/mission_012_review_rollback_qa.py --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`, `python3 -B scripts/verify_mission_012.py`.
- JSON parse checks: `python3 -m json.tool` on the Mission 012 record, audit summary, interrupt file(s), and any touched fixture manifest.
- Local API server: `python3 -B -m ppos_core.api --db <tmp sqlite path> --host 127.0.0.1 --port <localhost port>`.
- Mission-owned local process cleanup only: `lsof -ti tcp:<mission port>`, `kill <mission server pid>`.
- Built-in Codex Browser against `http://127.0.0.1:<mission port>/workbench/` only.

## Dependency Policy
- New dependencies allowed: NO
- If YES, approval reference: not applicable
- Install command: not applicable
- Rollback plan: not applicable

## Budget Instrumentation
- Every checkpoint must fill Budget State with measured values, not `not explicitly set`: approximate context usage if the harness exposes it (otherwise an honest qualitative estimate with method stated), tool-call count since last checkpoint, wall-clock time since last checkpoint, and a stop-threshold judgment.
- Stop threshold: if context or usage pressure makes completing the current phase plus a clean checkpoint uncertain, stop work, write the checkpoint, commit, and end the session with a reentry instruction rather than degrading evidence quality.
- The closeout must include a budget summary across all checkpoints (totals and per-phase), as the POC's first measured mission cost profile.

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: all existing and Mission 012 tests pass.
- `python3 -B scripts/mission_012_review_rollback_qa.py --db /tmp/ppos_mission_012_qa.sqlite --host 127.0.0.1 --port 8790`: review workflow, diff view, and rollback flows pass; writes the authorized audit summary.
- `python3 -B scripts/verify_mission_012.py`: checks mission envelope, state, checkpoints, closeout, and record; verifies HDI-012-001 parses and reached `applied` with a non-empty answer block; verifies the plan-delta rule (delta exists or record states why none was required); verifies every checkpoint Budget State contains measured values; verifies checkpoint commits exist in `git log` matching the message convention; runs the no-go scan.
- JSON parse checks for record, audit summary, and interrupt file(s) pass.
- Browser QA: review workflow states render, raw/normalized diff renders, rollback flow works, audit panel reflects rollback provenance, no runtime errors; desktop and mobile/responsive checks attempted.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission plan authored; interrupt asked (pre-pause); resume completed (post-answer); review/rollback implementation; persistence/API; workbench UI; verification and Browser QA; final closeout.
- Mission state file: `.factory-v3/evidence/MISSION_012_STATE.md`
- Human decision interrupts allowed: YES (HDI-012-001 required; HDI-012-002 optional and only if genuine)
- Interrupt surfaces allowed: file (primary, this mission) | thread (fallback if the sponsor answers in-session instead)
- Timeout behavior for unresolved interrupts: pause
- Cross-session resume: REQUIRED once, at the HDI-012-001 pause. The resuming session must list in the state file exactly which artifacts it read to resume (envelope, state, latest checkpoint, interrupt file, repository state) and must not rely on prior chat context.
- Plan delta required before scope change: YES
- Verification side effects allowed: YES; authorized output paths are the Mission 012 evidence files listed under Authorized Files.

## Halt Rules
Stop if:
- Factory V2 or Factory_V3 repo tooling appears necessary.
- Real data, credentials, live integration, package install, Telegram live behavior, OCR/vision, voice transcription, scheduler, notification, Hermes, public deployment, or production infrastructure appears.
- HDI-012-001 is answered ambiguously, outside the option set without a clear interpretation, or the answer would require unauthorized scope (record the conflict in the interrupt file and halt for sponsor clarification).
- Verification requires source paths, commands, dependencies, or git authority not authorized by this mission.
- Rollback or review work would mutate or destroy prior mission evidence or audit history.
- Mission state/checkpoint evidence becomes stale or contradicts repository state.
- Budget stop threshold is reached (checkpoint, commit, end session with reentry instruction).

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as a fallback while claiming POC readiness.

## Reentry Rules
- Resume only from authored mission artifacts: this envelope, `.factory-v3/evidence/MISSION_012_STATE.md`, the latest checkpoint, the interrupt file(s), and current repository state.
- The HDI-012-001 resume is valid only if the interrupt status is `answered`; if still `asked`, remain paused.
- Halt if derived state conflicts with authored artifacts.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md`. The closeout must additionally report: interrupt lifecycle summary (asked/answered/applied timestamps and surfaces), resume evidence (artifacts read, session boundary), budget summary, checkpoint-commit list, and the recommended Mission 013 informed by the sponsor's bridge decision.
