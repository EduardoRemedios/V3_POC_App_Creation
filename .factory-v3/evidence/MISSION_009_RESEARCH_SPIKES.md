# Mission 009 Research Spikes

## Status
COMPLETE

Research was bounded to public documentation/articles. No credentials, private accounts, live integrations, package installs, or external product APIs were used.

## Spike 1: SQLite Local-First Replay And Audit Patterns
Sources:
- SQLite appropriate uses: https://www.sqlite.org/whentouse.html
- SQLite as an application file format: https://www.sqlite.org/appfileformat.html
- SQLite atomic commit: https://sqlite.org/atomiccommit.html
- SQLite transactions: https://www.sqlite.org/transactional.html
- SQLite JSON functions: https://www.sqlite.org/json1.html
- SQLite triggers: https://www.sqlite.org/lang_createtrigger.html

Findings:
- SQLite remains appropriate for this POC because it is local, embedded, and commonly used as an application file format.
- Mission 009 should keep the single local DB shape, not introduce a server database.
- Atomic transactions support idempotent fixture import and replay/audit writes in one bounded transaction.
- JSON payloads can remain text-backed source and output snapshots, while typed tables store stable query surfaces.
- Triggers are useful research context for audit trails, but Mission 009 should prefer explicit app-level audit rows for transparency and testability.

Implementation decision:
- Add Mission 009 tables through stdlib migration SQL.
- Preserve existing source/normalized/derived separation.
- Store workflow timeline steps, graph nodes/edges, recommendation/follow-up rows, report settings, safety events, snapshot exports, and audit summaries explicitly.

## Spike 2: Static No-Build Workbench UI Patterns
Sources:
- MDN Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- MDN Using Fetch: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
- MDN CSS media queries: https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries
- MDN media query fundamentals: https://developer.mozilla.org/docs/Learn_web_development/Core/CSS_layout/Media_queries

Findings:
- Browser-native `fetch()` is enough for the workbench API runner and view hydration.
- The workbench should remain static HTML/CSS/JS with no bundler, CDN, package manager, or framework.
- Media queries are sufficient for mobile/desktop layout shifts.

Implementation decision:
- Replace the basic Mission 008 static page with an actual multi-view app shell.
- Use a compact tab/rail model with 8 views, code-native controls, and stable responsive grid rules.
- Avoid a decorative landing page.

## Spike 3: Evidence/Provenance Graph UI Patterns
Sources:
- W3C PROV overview: https://www.w3.org/TR/prov-overview/
- W3C PROV primer: https://www.w3.org/TR/prov-primer/
- W3C PROV access/query: https://www.w3.org/TR/prov-aq/
- Grafana node graph visualization shape: https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/node-graph/

Findings:
- W3C PROV frames provenance as entities, activities, agents, and relations. Mission 009 does not need full PROV serialization, but it should model lineage as explicit nodes and edges.
- A graph UI needs separate node and edge shapes and should avoid rendering unbounded dense graphs.
- The useful POC view is a bounded inspectable graph per fixture/workflow/evidence pack.

Implementation decision:
- Persist graph nodes and edges with type, label, fixture, and relation fields.
- Expose graph query routes by fixture/workflow/evidence pack.
- Render a simple bounded node/edge list and lightweight SVG-like CSS layout without a graph library.

## Spike 4: Health/Performance Coaching Safety Boundaries
Sources:
- WHO physical activity topic: https://www.who.int/health-topics/noncommunicable-diseases/physical-activity
- WHO physical activity fact sheet: https://www.who.int/news-room/fact-sheets/detail/physical-activity
- CDC chronic conditions and disabilities physical activity guidance: https://www.cdc.gov/physical-activity-basics/guidelines/chronic-health-conditions-and-disabilities.html
- American Heart Association endurance exercise safety note: https://www.heart.org/en/healthy-living/fitness/fitness-basics/endurance-exercise-aerobic

Findings:
- The POC can support performance coaching language, but it must stay out of diagnosis, treatment, and clinical claims.
- Safety copy should escalate uncertainty or known cardiac/chronic-condition context to a health professional rather than prescribing.
- Gradual changes and cautious uncertainty are safer than absolute causal claims.

Implementation decision:
- Add safety boundary records and API/workbench audit views.
- Preserve prohibited claims in fixtures.
- Use recommendation classes like `reduce_intensity`, `monitor_cautiously`, and `consult_professional_boundary` rather than medical directives.

## Spike 5: API Contract And Error Shape Patterns
Sources:
- RFC 9457 problem details: https://www.rfc-editor.org/rfc/rfc9457
- IETF RFC 9457 mirror: https://www.ietf.org/rfc/rfc9457.html

Findings:
- Machine-readable error objects reduce one-off error parsing for local tools.
- Mission 009 should not fully implement content negotiation, but should standardize error fields.

Implementation decision:
- Add API matrix metadata and tests for 25-35 route/error cases.
- Return local JSON errors with `type`, `title`, `status`, `detail`, and optional `instance`/`field` keys.

## Spike 6: Browser Smoke Testing Static/Local Apps
Sources:
- Playwright screenshots docs: https://playwright.dev/docs/next/screenshots
- Playwright trace viewer/docs for console and screenshot debugging: https://playwright.dev/docs/trace-viewer
- MDN CSS media queries: https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries
- WCAG reflow explainer: https://wcag.dock.codes/documentation/wcag1410/

Findings:
- A minimal local smoke should check page identity, nonblank rendered content, console health, screenshot evidence, interaction state, and responsive reflow.
- If the Browser plugin cannot be reached, a stdlib fallback can still assert static HTML/API availability and responsive CSS markers, but it cannot replace visual browser confidence.

Implementation decision:
- Prefer Browser plugin for localhost UI QA.
- Add `scripts/mission_009_browser_smoke.py` as a no-package stdlib server/API smoke fallback and evidence helper.
- Record browser pass/fallback in closeout and audit summary.

## Dependency Review
No package installation is justified by these research spikes.

Approved implementation posture remains:
- Python standard library only.
- Static HTML/CSS/JS only.
- Browser plugin or already available browser tooling only for QA; no install.
