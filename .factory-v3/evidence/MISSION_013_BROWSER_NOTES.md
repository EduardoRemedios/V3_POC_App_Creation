# Mission 013 Browser QA Notes

## Scope
- Target: `http://127.0.0.1:8800/workbench/?view=imports&manual_export=garmin_activities_clean_csv`
- Server command: `python3 -B -m ppos_core.api --db /tmp/ppos_mission_013_browser.sqlite --host 127.0.0.1 --port 8800`
- Browser surface: Codex in-app Browser (`iab`)
- Data mode: synthetic only; no real Garmin exports, credentials, live integrations, uploads, or external calls.

## Desktop Flow Result
PASS.

Exercised in the workbench UI:
- Opened Imports view with `garmin_activities_clean_csv` selected.
- Recorded synthetic approval with consent checked and retention `keep-raw-until-verified`.
- Confirmed approval surface rendered source label `real_garmin_manual_export` while remaining synthetic-only.
- Previewed Garmin activities fixture.
- Accepted rows 1, 2, and 3.
- Committed reviewed import.
- Consumed materialized facts into workflows, timeline, graph, and report candidates.
- Inspected Graph, Reports, and Replay views.
- Rolled back the committed synthetic import.

Browser assertions:
- Approval state rendered.
- Consumed workflow/report/graph summary rendered.
- Evidence graph rendered workflow and report candidate nodes.
- Reports rendered `garmin_import_garmin_activities_clean_csv` candidates with `candidate_not_delivered`.
- Replay timeline rendered workflow steps including evidence assembly or output persistence.
- Rollback state rendered after rollback action.
- `window.__PPOS_WORKBENCH_QA__.errors` was empty.
- Browser console error log was empty.

## Responsive Attempt
Attempted to resize the in-app browser viewport via browser automation. The viewport remained `1280x720`, `matchMedia('(max-width: 860px)')` remained false, and the Imports grid stayed two-column. This means desktop Browser QA passed, and mobile/responsive verification was attempted but could not be completed in the available in-app browser surface.

Static CSS still contains the Mission 013 responsive rule path for `#view-imports.is-active`, `.summary-grid`, `.list-grid`, `.two-column`, and `.diff-grid` under `@media (max-width: 860px)`.

## Notes
- The visible screenshot after rollback showed the Imports view, approval rehearsal panel, Garmin fixture selector, synthetic consent checked, and rollback status message.
- No real-data path was enabled or exercised.
