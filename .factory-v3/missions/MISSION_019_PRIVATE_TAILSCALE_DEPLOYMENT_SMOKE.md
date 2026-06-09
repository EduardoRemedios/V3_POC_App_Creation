# Mission 019: Private Tailscale Deployment Smoke

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO
- Evidence target: private deployment boundary and smoke evidence using Tailscale as deployment-network infrastructure.

## Objective
Produce replayable standalone V3 evidence that the POC can run as a private deployment target over a Tailscale/private-network route without public exposure, app dependency changes, real data, live Garmin integration, Telegram live bot behavior, or Factory V2 help.

## Success Criteria
- Mission envelope exists before install or deployment work begins.
- Baseline local synthetic tests pass.
- Tailscale install status is recorded before and after installation.
- Tailscale is installed only as host/private-network infrastructure, not as an app dependency.
- User login/auth is handled by the user, not by stored credentials in this mission.
- POC server runs from the repository on a synthetic-only temp SQLite DB, bound to localhost.
- Localhost smoke verifies `/api/health` and `/workbench/`.
- If Tailscale is authenticated and Serve is available, Tailscale Serve proxies the localhost server privately within the tailnet and private-network smoke verifies the same server without public exposure.
- If Tailscale auth requires user action, mission records a blocked/partial deployment result without weakening boundaries.
- Rollback/cleanup is recorded: stop server, remove temp DB if created, no secrets retained.
- Mission record parses as JSON.

## Eligible-Work Rationale
This is bounded enough for V3 because it uses the existing stdlib HTTP server and static workbench, installs only the approved Tailscale host app, avoids public deployment, and keeps all app data synthetic/local.

## Non-Goals
- No public deployment.
- No production infrastructure.
- No app source behavior change unless a verifier script is needed for smoke evidence.
- No real personal data, Garmin data, credentials, tokens, live Garmin integration, Telegram live bot, package dependency changes, scheduler, notifications, Hermes, or Factory V2.
- No persistence of Tailscale credentials or secrets in repo evidence.
- No claim of operational readiness beyond this private deployment smoke.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_019_PRIVATE_TAILSCALE_DEPLOYMENT_SMOKE.md`
- `.factory-v3/evidence/MISSION_019_STATE.md`
- `.factory-v3/evidence/MISSION_019_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_019_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_019_RECORD.json`
- `fixtures/mission_019/deployment_plan.json`
- `scripts/verify_mission_019_private_deployment.py`

## Authorized Host/System Changes
- Install Homebrew cask `tailscale-app` if not already installed.
- Launch Tailscale app or CLI only for login/status/private IP discovery.
- Run the POC server locally from this repository.
- Use `/tmp/ppos_mission_019_private.sqlite` as the synthetic deployment DB.

## Forbidden Scope
- Everything in Non-Goals.
- Any file outside the authorized list, except temp DB and process logs under `/tmp`.
- Any command that uses real health data, stores credentials/tokens in evidence, calls live Garmin APIs, sends Telegram messages, deploys publicly, or runs Factory V2 tooling.

## Allowed Commands
- `date -u +%Y-%m-%dT%H:%M:%SZ`
- `git status --short`
- `git rev-parse HEAD`
- `git log --oneline -n 6`
- `python3 -B -m unittest discover -s tests`
- `brew info --cask tailscale-app`
- `brew install --cask tailscale-app`
- `command -v tailscale`
- `tailscale version`
- `tailscale status`
- `tailscale ip -4`
- `open -a Tailscale`
- `python3 -B -m ppos_core.api --db /tmp/ppos_mission_019_private.sqlite --host 127.0.0.1 --port 8770`
- `tailscale serve --http=8771 localhost:8770`
- `tailscale serve status`
- `tailscale serve reset`
- `lsof -nP -iTCP:8770 -sTCP:LISTEN`
- `ls -l /tmp/ppos_mission_019_private.sqlite`
- `kill <SERVER_PID>`
- `rm /tmp/ppos_mission_019_private.sqlite`
- `test ! -e /tmp/ppos_mission_019_private.sqlite`
- `sed -n '1,180p' workbench/index.html`
- `rg -n "bootstrap|workbench|api" workbench/index.html workbench/app.js`
- `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://127.0.0.1:8770 --expect-localhost`
- `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://<TAILSCALE_HOST_OR_IP>:8771 --expect-tailscale`
- `python3 -m json.tool .factory-v3/evidence/MISSION_019_RECORD.json`
- `git diff --check`
- `git add .factory-v3/missions/MISSION_019_PRIVATE_TAILSCALE_DEPLOYMENT_SMOKE.md .factory-v3/evidence/MISSION_019_STATE.md .factory-v3/evidence/MISSION_019_CHECKPOINTS.md .factory-v3/evidence/MISSION_019_CLOSEOUT.md .factory-v3/evidence/MISSION_019_RECORD.json fixtures/mission_019/deployment_plan.json scripts/verify_mission_019_private_deployment.py`
- `git commit -m "Record Mission 019 private Tailscale deployment smoke"`
- `git push origin main`

## Dependency Policy
- App dependencies allowed: NO.
- Host/private-network infrastructure allowed: YES, `tailscale-app` only, based on explicit human approval in the thread.

## Deployment Boundary
- Target: private Tailscale network if authenticated; otherwise localhost-only smoke plus blocked Tailscale-auth evidence.
- Host: current Mac.
- App bind: `127.0.0.1:8770`.
- Tailscale route: `tailscale serve --http=8771 localhost:8770`, private tailnet only.
- Data: synthetic-only temp SQLite DB.
- Secrets: none stored; user handles Tailscale login outside repo evidence.
- Public URL: not approved.
- Rollback: stop server process, remove `/tmp/ppos_mission_019_private.sqlite` if present, leave no app secrets.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission start, baseline verification, Tailscale install/status, local smoke, private-network smoke or blocked-auth finding, closeout.
- Mission state file: `.factory-v3/evidence/MISSION_019_STATE.md`
- Human decision interrupts allowed: YES, only if Tailscale login/auth requires user action.
- Interrupt surfaces allowed: current thread.
- Timeout behavior for unresolved login/auth: close as partial/blocked, not failed app deployment.
- Plan delta required before scope change: YES
- Verification side effects allowed: YES
- Authorized output paths: Mission 019 evidence files listed above.

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: expected PASS baseline.
- Localhost smoke: expected PASS.
- Tailscale smoke: expected PASS if authenticated and Serve/private host URL available; otherwise record blocked-auth or blocked-serve.
- `python3 -m json.tool .factory-v3/evidence/MISSION_019_RECORD.json`: expected PASS after record is authored.

## Halt Rules
Stop if:
- Tailscale install asks for unacceptable system permission or credentials beyond user login.
- Any credential/token would be written to repo evidence.
- Server cannot be run without app dependency changes.
- Public exposure is required.
- Real data, live Garmin integration, Telegram live bot, dependency changes, deployment outside private boundary, or Factory V2 tooling becomes necessary.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as fallback while claiming POC readiness.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md` conventions and explicitly report whether deployment evidence is complete, partial due Tailscale auth, or blocked.
