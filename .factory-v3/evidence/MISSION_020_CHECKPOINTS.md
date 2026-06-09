# Mission 020 Checkpoints

## Checkpoint M020-CP001

## Mission
- Mission ID: MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION
- Checkpoint ID: M020-CP001
- Checkpoint status: complete

## Current Phase
Mission start and private-smoke boundary setup.

## Objective Progress
Mission envelope, initial state, checkpoint log, and private smoke fixture are authored before starting the server or configuring Tailscale Serve.

## Files Changed Since Last Checkpoint
- `.factory-v3/missions/MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION.md`
- `.factory-v3/evidence/MISSION_020_STATE.md`
- `.factory-v3/evidence/MISSION_020_CHECKPOINTS.md`
- `fixtures/mission_020/private_tailscale_smoke.json`

## Commands Run Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `git status --short && git rev-parse HEAD && rg --files .factory-v3 \| sort \| tail -40` | PASS | Current head: `6c7fac6b4c8650d116807ae9dca53251c5a92020`; pre-existing unrelated `.DS_Store` and Mission 014 remain untracked. |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale status --json` | PASS | Backend running, MagicDNS enabled, Tailscale IP `100.87.19.28`, DNS name `eduardos-macbook-pro-work.tail0aaa7b.ts.net.` |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve status` | PASS | `No serve config` before Mission 020 serve changes. |
| `date -u +%Y-%m-%dT%H:%M:%SZ` | PASS | `2026-06-09T06:30:03Z` |

## Verification Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| Not yet run | n/a | Baseline verification pending. |

## Budget State
- Token budget: not specified.
- Tool-call budget: not specified.
- Context/buffer concern: low.
- Stop threshold reached: NO

## Open Risks
- Tailscale Serve command behavior must be verified against the installed CLI.
- Private tailnet HTTP route may require using the Tailscale IP rather than MagicDNS.

## Pending Human Decisions
None.

## Plan Delta References
None.

## Next Planned Action
Run baseline tests, then start the local server and smoke it.

## Reentry Instruction
Resume from this checkpoint, Mission 020 state, the mission envelope, private smoke fixture, and current repository state.

Halt if real data, credentials in evidence, public deployment, Tailscale Funnel, app dependency changes, or Factory V2 become necessary.

## Checkpoint M020-CP002

## Mission
- Mission ID: MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION
- Checkpoint ID: M020-CP002
- Checkpoint status: complete

## Current Phase
Baseline verification and clean preflight.

## Objective Progress
Baseline tests passed, ports were clear, and Tailscale Serve had no pre-existing config before the mission deployment smoke.

## Files Changed Since Last Checkpoint
None.

## Commands Run Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -B -m unittest discover -s tests` | PASS | 170 tests ran in 3.491s. |
| `lsof -nP -iTCP:8770 -sTCP:LISTEN; lsof -nP -iTCP:8771 -sTCP:LISTEN` | PASS | No listeners on local app port `8770` or Serve HTTP port `8771`. |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve status` | PASS | `No serve config`. |

## Verification Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -B -m unittest discover -s tests` | PASS | Baseline app verification passed. |

## Budget State
- Token budget: not specified.
- Tool-call budget: not specified.
- Context/buffer concern: low.
- Stop threshold reached: NO

## Open Risks
- Server process must remain alive across smoke checks.
- Serve route may require MagicDNS hostname rather than direct Tailscale IP.

## Pending Human Decisions
None.

## Plan Delta References
None.

## Next Planned Action
Start the local server and run localhost smoke.

## Reentry Instruction
Resume from this checkpoint, Mission 020 state, the mission envelope, baseline pass evidence, and current repository state.

Halt if real data, credentials in evidence, public deployment, Tailscale Funnel, app dependency changes, or Factory V2 become necessary.

## Checkpoint M020-CP003

## Mission
- Mission ID: MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION
- Checkpoint ID: M020-CP003
- Checkpoint status: complete

## Current Phase
Localhost deployment smoke.

## Objective Progress
The first background server attempt exited before listening in the non-interactive shell, producing an expected connection-refused smoke failure. The server was restarted as a managed long-running session and localhost smoke passed.

## Files Changed Since Last Checkpoint
None.

## Commands Run Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -B -m ppos_core.api --db /tmp/ppos_mission_020_private.sqlite --host 127.0.0.1 --port 8770 > /tmp/ppos_mission_020_server.log 2>&1 & echo $!` | PARTIAL | Background PID `57374` exited before listening; log empty. |
| `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://127.0.0.1:8770 --expect-localhost` | FAIL | Connection refused for `/api/health` and `/workbench/` because the background server attempt was not alive. |
| `sed -n '1,220p' /tmp/ppos_mission_020_server.log` | PASS | Empty log; no app traceback. |
| `ps -p 57374 -o pid=,stat=,command=; lsof -nP -iTCP:8770 -sTCP:LISTEN` | PASS | PID not running and no listener. |
| `python3 -B -m ppos_core.api --help` | PASS | Confirmed server command shape. |
| `python3 -B -m ppos_core.api --db /tmp/ppos_mission_020_private.sqlite --host 127.0.0.1 --port 8770` | PASS | Managed session started and printed `{"status": "serving", "host": "127.0.0.1", "port": 8770, "local_only": true}`; observed listener PID `59210`. |
| `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://127.0.0.1:8770 --expect-localhost` | PASS | Output: mode `localhost`, status `pass`, no failures. |
| `lsof -nP -iTCP:8770 -sTCP:LISTEN; ls -l /tmp/ppos_mission_020_private.sqlite` | PASS | PID `59210` listening on `127.0.0.1:8770`; temp DB existed, size 344064 bytes. |

## Verification Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://127.0.0.1:8770 --expect-localhost` | PASS | `/api/health` and `/workbench/` smoke passed after managed-session server start. |

## Budget State
- Token budget: not specified.
- Tool-call budget: not specified.
- Context/buffer concern: low.
- Stop threshold reached: NO

## Open Risks
- Serve host routing may require testing the advertised MagicDNS name instead of the raw Tailscale IP.

## Pending Human Decisions
None.

## Plan Delta References
None. Managed-session retry was a process-control correction, not scope change.

## Next Planned Action
Configure Tailscale Serve and run private tailnet smoke.

## Reentry Instruction
Resume from this checkpoint, Mission 020 state, the local server session, localhost smoke pass evidence, and current repository state.

Halt if real data, credentials in evidence, public deployment, Tailscale Funnel, app dependency changes, or Factory V2 become necessary.

## Checkpoint M020-CP004

## Mission
- Mission ID: MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION
- Checkpoint ID: M020-CP004
- Checkpoint status: complete

## Current Phase
Private Tailscale smoke.

## Objective Progress
Tailscale Serve was configured for private tailnet HTTP on port `8771`, pointing at the localhost server. The raw Tailscale IP returned 404, while the advertised MagicDNS hostname passed the smoke verifier.

## Files Changed Since Last Checkpoint
None.

## Commands Run Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale status` | PASS | `100.87.19.28  eduardos-macbook-pro-work  EduardoRemedios@  macOS  -` |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve --bg --http=8771 localhost:8770` | PASS | Reported available within tailnet at `http://eduardos-macbook-pro-work.tail0aaa7b.ts.net:8771/`, proxying `http://localhost:8770`. |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve status` | PASS | Reported `http://eduardos-macbook-pro-work:8771` and FQDN as tailnet only, proxy `/` to `http://localhost:8770`. |
| `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://100.87.19.28:8771 --expect-tailscale` | FAIL | Raw Tailscale IP route returned HTTP 404 for `/api/health` and `/workbench/`. |
| `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://eduardos-macbook-pro-work.tail0aaa7b.ts.net:8771 --expect-tailscale` | PASS | Output: mode `tailscale`, status `pass`, no failures. |

## Verification Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `python3 -B scripts/verify_mission_019_private_deployment.py --base-url http://eduardos-macbook-pro-work.tail0aaa7b.ts.net:8771 --expect-tailscale` | PASS | Private tailnet smoke passed using the advertised MagicDNS route. |

## Budget State
- Token budget: not specified.
- Tool-call budget: not specified.
- Context/buffer concern: low.
- Stop threshold reached: NO

## Open Risks
- Direct IP route is not a valid smoke endpoint for this Serve config; future replay should use the advertised MagicDNS URL.

## Pending Human Decisions
None.

## Plan Delta References
None.

## Next Planned Action
Reset Tailscale Serve and roll back local server/temp DB.

## Reentry Instruction
Resume from this checkpoint, Mission 020 state, configured Serve status, MagicDNS smoke pass evidence, and current repository state.

Halt if real data, credentials in evidence, public deployment, Tailscale Funnel, app dependency changes, or Factory V2 become necessary.

## Checkpoint M020-CP005

## Mission
- Mission ID: MISSION_020_TAILSCALE_PRIVATE_SMOKE_COMPLETION
- Checkpoint ID: M020-CP005
- Checkpoint status: complete

## Current Phase
Rollback and closeout.

## Objective Progress
Tailscale Serve config was reset, the local server was stopped, the synthetic temp DB was removed, and post-cleanup checks passed.

## Files Changed Since Last Checkpoint
None.

## Commands Run Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve reset` | PASS | Command exited 0. |
| `date -u +%Y-%m-%dT%H:%M:%SZ` | PASS | `2026-06-09T06:31:59Z` |
| Managed server interrupt | PASS | Server stopped via `KeyboardInterrupt`; no listener remained after cleanup. |
| `rm /tmp/ppos_mission_020_private.sqlite && test ! -e /tmp/ppos_mission_020_private.sqlite` | PASS | Synthetic temp DB removed. |
| `lsof -nP -iTCP:8770 -sTCP:LISTEN; lsof -nP -iTCP:8771 -sTCP:LISTEN` | PASS | No listeners remained on `8770` or `8771`. |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve status` | PASS | `No serve config`. |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale status` | PASS | Tailscale remained authenticated and running on the tailnet. |

## Verification Since Last Checkpoint
| Command | Result | Evidence |
| --- | --- | --- |
| `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve status` | PASS | No serve config after reset. |
| `test ! -e /tmp/ppos_mission_020_private.sqlite` | PASS | Temp DB removed. |
| `lsof -nP -iTCP:8770 -sTCP:LISTEN; lsof -nP -iTCP:8771 -sTCP:LISTEN` | PASS | No deployment listeners remained. |

## Budget State
- Token budget: not specified.
- Tool-call budget: not specified.
- Context/buffer concern: low.
- Stop threshold reached: NO

## Open Risks
- None for Mission 020 private smoke completion.

## Pending Human Decisions
None.

## Plan Delta References
None.

## Next Planned Action
Author closeout and mission record, then verify record JSON.
