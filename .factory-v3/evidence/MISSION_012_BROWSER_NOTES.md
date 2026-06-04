# Mission 012 Browser Notes

## Browser QA status: PASS

## Target
- URL: `http://127.0.0.1:8790/workbench/?view=imports&manual_export=manual_activity_csv_clean`
- Server: `python3 -B -m ppos_core.api --db /tmp/ppos_mission_012_browser.sqlite --host 127.0.0.1 --port 8790`
- Data mode: synthetic-only local SQLite.

## Desktop Flow
- Loaded the imports view in the Codex in-app browser.
- Previewed `manual_activity_csv_clean`.
- Confirmed side-by-side raw/normalized diff rows rendered.
- Marked rows 1, 2, and 3 as `accepted`.
- Committed through `Commit reviewed`.
- Rolled back through `Rollback`.
- Confirmed audit panel reported a reverted session and rollback provenance.
- Runtime errors: none.
- Console errors: none.

## Responsive Flow
- Temporarily set viewport to 390x844.
- Reloaded the imports view and previewed `manual_activity_csv_clean`.
- Confirmed the diff grid collapsed to one column.
- Confirmed no horizontal document overflow.
- Runtime errors: none.
- Viewport override reset after the check.

## Evidence
- Desktop diff count: 3.
- Desktop review action groups: 3.
- Final status text: `Rolled back synthetic import: manual_import_manual_activity_csv_clean`.
- Mobile diff grid width: 303px within a 375px viewport.
- Screenshot was captured through the browser tool for visual QA, but not persisted to disk because Mission 012 authorized output paths do not include screenshot files.
