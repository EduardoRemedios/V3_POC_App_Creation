# Mission 020: Tailscale Private Smoke Completion

## Mission Status
APPROVED

## Profile
- Profile ID: `V3-POC-STANDALONE`
- Profile status: POC proof profile, not general production approval.
- V3-only: YES
- V2 allowed: NO
- Evidence target: complete the private Tailscale deployment smoke left open by Mission 019.

## Objective
Produce replayable standalone V3 evidence that the existing POC app can run from this repository on localhost and be reached privately through Tailscale Serve within the authenticated tailnet, without public exposure, app dependency changes, real data, live Garmin integration, Telegram live bot behavior, or Factory V2 help.

## Success Criteria
- Mission envelope exists before starting server or changing Tailscale Serve config.
- Baseline local synthetic tests pass.
- Tailscale status confirms authenticated running backend and private tailnet identity.
- POC server runs from the repository on a synthetic-only temp SQLite DB, bound to localhost.
- Localhost smoke verifies `/api/health` and `/workbench/`.
- Tailscale Serve proxies localhost privately within the tailnet.
- Private tailnet smoke verifies the same `/api/health` and `/workbench/` contract through the Tailscale IP or MagicDNS name.
- Serve config is reset after smoke.
- Rollback/cleanup is recorded: stop server, remove temp DB if created, no secrets retained.
- Mission record parses as JSON.

## Eligible-Work Rationale
This is bounded enough for V3 because Mission 019 already proved the local deployment path and identified only the missing user-authenticated Tailscale step. Mission 020 uses the existing stdlib HTTP server, existing smoke verifier, authenticated host Tailscale app, and synthetic/local data only.

## Non-Goals
- No public deployment.
- No Tailscale Funnel.
- No production infrastructure.
- No app source behavior change.
- No real personal data, Garmin data, credentials, tokens, live Garmin integration, Telegram live bot, package dependency changes, scheduler, notifications, Hermes, or Factory V2.
- No persistence of Tailscale credentials, auth URLs, tokens, or secrets in repo evidence.
- No claim of operational readiness beyond this private deployment smoke.

## Authorized Files And Directories
- `.factory-v3/missions/MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION.md`
- `.factory-v3/evidence/MISSION_020_STATE.md`
- `.factory-v3/evidence/MISSION_020_CHECKPOINTS.md`
- `.factory-v3/evidence/MISSION_020_CLOSEOUT.md`
- `.factory-v3/evidence/MISSION_020_RECORD.json`
- `fixtures/mission_020/private_tailscale_smoke.json`

## Authorized Existing Read/Execute Artifacts
- `scripts/verify_mission_019_private_deployment.py`
- `ppos_core/api.py`
- `workbench/index.html`
- `workbench/app.js`

## Authorized Host/System Changes
- Run the POC server locally from this repository.
- Use `/tmp/ppos_mission_020_private.sqlite` as the synthetic deployment DB.
- Configure Tailscale Serve for the current node only during smoke.
- Reset Tailscale Serve config after smoke.

## Forbidden Scope
- Everything in Non-Goals.
- Any file outside the authorized list, except temp DB and process logs under `/tmp`.
- Any command that uses real health data, stores credentials/tokens in evidence, calls live Garmin APIs, sends Telegram messages, deploys publicly, runs Tailscale Funnel, or runs Factory V2 tooling.

## Allowed Commands
- `date -u +%Y-%m-%dT%H:%M:%SZ`
- `git status --short`
- `git rev-parse HEAD`
- `git log --oneline -n 6`
- `python3 -B -m unittest discover -s tests`
- `/Applications/Tailscale.app/Contents/MacOS/Tailscale version`
- `/Applications/Tailscale.app/Contents/MacOS/Tailscale status`
- `/Applications/Tailscale.app/Contents/MacOS/Tailscale status --json`
- `/Applications/Tailscale.app/Contents/MacOS/Tailscale ip -4`
- `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve status`
- `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve --bg --http=8771 localhost:8770`
- `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve reset`
- `lsof -nP -iTCP:8770 -sTCP:LISTEN`
- `lsof -nP -iTCP:8771 -sTCP:LISTEN`
- `python3 -B -m ppos_core.api --db /tmp/ppos_mission_020_private.sqlite --host 127.0.0.1 --port 8770`
- `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://127.0.0.1:8770 --expect-localhost`
- `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://<TAILSCALE_IP_OR_DNS>:8771 --expect-tailscale`
- `ls -l /tmp/ppos_mission_020_private.sqlite`
- `kill <SERVER_PID>`
- `rm /tmp/ppos_mission_020_private.sqlite`
- `test ! -e /tmp/ppos_mission_020_private.sqlite`
- `python3 -m json.tool .factory-v3/evidence/MISSION_020_RECORD.json`
- `git diff --check`
- `git add .factory-v3/missions/MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION.md .factory-v3/evidence/MISSION_020_STATE.md .factory-v3/evidence/MISSION_020_CHECKPOINTS.md .factory-v3/evidence/MISSION_020_CLOSEOUT.md .factory-v3/evidence/MISSION_020_RECORD.json fixtures/mission_020/private_tailscale_smoke.json`
- `git commit -m "Record Mission 020 Tailscale private smoke"`
- `git push origin main`

## Dependency Policy
- App dependencies allowed: NO.
- Host/private-network infrastructure allowed: YES, existing authenticated Tailscale app only.

## Deployment Boundary
- Target: private Tailscale tailnet.
- Host: current Mac.
- App bind: `127.0.0.1:8770`.
- Tailscale route: `tailscale serve --bg --http=8771 localhost:8770`, private tailnet only.
- Data: synthetic-only temp SQLite DB.
- Secrets: none stored; Tailscale auth already handled by user outside repo evidence.
- Public URL: not approved.
- Rollback: reset Serve config, stop server process, remove `/tmp/ppos_mission_020_private.sqlite` if present.

## Adaptive Mission Control
- Checkpoints required: YES
- Checkpoint cadence: mission start, baseline verification, Tailscale status, local smoke, private tailnet smoke, rollback/closeout.
- Mission state file: `.factory-v3/evidence/MISSION_020_STATE.md`
- Human decision interrupts allowed: YES, only if Tailscale auth or macOS permission requires user action.
- Interrupt surfaces allowed: current thread.
- Timeout behavior for unresolved auth/permission: close as partial/blocked, not failed app deployment.
- Plan delta required before scope change: YES
- Verification side effects allowed: YES
- Authorized output paths: Mission 020 evidence files listed above.

## Verification
Commands and expected evidence:
- `python3 -B -m unittest discover -s tests`: expected PASS baseline.
- Localhost smoke: expected PASS.
- Tailscale smoke: expected PASS through private tailnet address.
- `tailscale serve reset`: expected PASS cleanup.
- `python3 -m json.tool .factory-v3/evidence/MISSION_020_RECORD.json`: expected PASS after record is authored.

## Halt Rules
Stop if:
- Tailscale status is logged out or unhealthy and cannot be resolved without user action.
- Any credential/token would be written to repo evidence.
- Server cannot be run without app dependency changes.
- Public exposure or Tailscale Funnel is required.
- Real data, live Garmin integration, Telegram live bot, dependency changes, deployment outside private boundary, or Factory V2 tooling becomes necessary.

## Standalone Gap Rule
If this mission cannot proceed without Factory V2, stop and record a V3 standalone gap. Do not use V2 as fallback while claiming POC readiness.

## Closeout
Use `.factory-v3/templates/V3_POC_CLOSEOUT_TEMPLATE.md` conventions and explicitly report whether private Tailscale deployment smoke is complete, partial, or blocked.
