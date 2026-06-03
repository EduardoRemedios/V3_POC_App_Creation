const state = {
  fixtures: [],
  selectedFixtureId: null,
  selectedFixtureDetail: null,
  lastRunId: null,
  busy: false,
  lastError: null,
  scenario: [],
};

window.__PPOS_WORKBENCH_QA__ = {
  errors: [],
  events: [],
};

window.addEventListener("error", (event) => {
  window.__PPOS_WORKBENCH_QA__.errors.push(event.message || "window error");
});

window.addEventListener("unhandledrejection", (event) => {
  const reason = event.reason && event.reason.message ? event.reason.message : String(event.reason);
  window.__PPOS_WORKBENCH_QA__.errors.push(reason);
});

const STORAGE_KEY = "ppos.workbench.selectedFixtureId";

const api = {
  bootstrap: () => fetchJson("/api/workbench/bootstrap"),
  fixture: (fixtureId) => fetchJson(`/api/fixtures/${fixtureId}`),
  importFixture: (fixtureId) => fetchJson("/api/import-fixture", { fixture_id: fixtureId }),
  fixtureState: (fixtureId) => fetchJson(`/api/fixtures/state/${fixtureId}`),
  runWorkflow: (fixtureId, workflow) => fetchJson("/api/workflows/run", { fixture_id: fixtureId, workflow }),
  timeline: (runId) => fetchJson(`/api/workflows/${runId}/timeline`),
  graph: (fixtureId) => fetchJson(`/api/evidence-graph/${fixtureId}`),
  reports: () => fetchJson("/api/report-candidates"),
  recommendations: () => fetchJson("/api/recommendations"),
  followups: () => fetchJson("/api/follow-up-outcomes"),
  reportSettings: () => fetchJson("/api/report-settings"),
  safety: () => fetchJson("/api/safety-audit"),
  snapshot: () => fetchJson("/api/snapshot/export"),
  contracts: () => fetchJson("/api/contracts"),
  sourceAdapters: () => fetchJson("/api/source-adapters"),
  manualExports: () => fetchJson("/api/manual-exports"),
  previewManualImport: (exportId) => fetchJson("/api/manual-imports/preview", { export_id: exportId }),
  commitManualImport: (exportId) => fetchJson("/api/manual-imports/commit-synthetic", { export_id: exportId }),
  manualImportMapping: (sessionId) => fetchJson(`/api/manual-imports/${sessionId}/mapping`),
  manualImportConflicts: (sessionId) => fetchJson(`/api/manual-imports/${sessionId}/conflicts`),
  manualImportAudit: () => fetchJson("/api/manual-imports/audit-summary"),
};

async function fetchJson(path, body) {
  const response = await fetch(path, {
    method: body ? "POST" : "GET",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  const payload = await response.json();
  if (!response.ok) {
    const message = payload.detail || payload.title || `Local API request failed: ${path}`;
    throw new Error(message);
  }
  return payload;
}

function setBusy(isBusy, message) {
  state.busy = isBusy;
  document.body.dataset.loading = isBusy ? "true" : "false";
  document.querySelectorAll("button, select").forEach((control) => {
    control.disabled = isBusy;
  });
  if (message) {
    setStatus(message);
  }
}

function setStatus(message) {
  document.querySelector("#operator-status").textContent = message;
  window.__PPOS_WORKBENCH_QA__.events.push({ type: "status", message });
}

function setError(error) {
  state.lastError = error;
  const panel = document.querySelector("#operator-error");
  if (!error) {
    panel.hidden = true;
    panel.textContent = "";
    return;
  }
  panel.hidden = false;
  panel.textContent = error.message || String(error);
}

async function withOperation(message, operation) {
  setError(null);
  setBusy(true, message);
  try {
    const result = await operation();
    setBusy(false);
    return result;
  } catch (error) {
    setBusy(false, "Workbench operation failed");
    setError(error);
    throw error;
  }
}

function renderSafety(safety) {
  const panel = document.querySelector("#safety-status");
  panel.innerHTML = Object.entries(safety)
    .map(([key, value]) => `<span class="badge">${escapeHtml(key)}: ${escapeHtml(String(value))}</span>`)
    .join("");
}

function renderFixtureSelector(fixtures) {
  const selector = document.querySelector("#fixture-selector");
  selector.innerHTML = fixtures
    .map((fixture) => `<option value="${escapeHtml(fixture.fixture_id)}">${escapeHtml(fixture.fixture_id)}</option>`)
    .join("");
  selector.addEventListener("change", () => selectFixture(selector.value));
  document.querySelector("#fixture-count").textContent = `${fixtures.length} fixtures`;
}

function wireNavigation() {
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.addEventListener("click", () => activateView(button.dataset.view));
  });
}

async function selectFixture(fixtureId) {
  await withOperation(`Loading ${fixtureId}`, async () => {
    state.selectedFixtureId = fixtureId;
    localStorage.setItem(STORAGE_KEY, fixtureId);
    const selector = document.querySelector("#fixture-selector");
    if (selector.value !== fixtureId) {
      selector.value = fixtureId;
    }
    const detail = await api.fixture(fixtureId);
    state.selectedFixtureDetail = detail;
    await api.importFixture(fixtureId);
    const persisted = await api.fixtureState(fixtureId);
    renderFixtureSummary(detail);
    renderProvenance(persisted);
    renderDerivedFacts(persisted.derived_facts);
    renderConversation(detail);
    renderScenarioSteps([]);
    await renderGraph(fixtureId);
    await renderReports();
    await renderRecommendations();
    await renderSafetyAudit();
    setStatus(`Ready: ${fixtureId}`);
  });
}

function renderFixtureSummary(detail) {
  const families = detail.expected.families || [];
  const risks = detail.expected.risk_coverage || [];
  document.querySelector("#fixture-summary").innerHTML = [
    card("Fixture", detail.fixture_id),
    card("Scenario", detail.scenario),
    card("Families", families.join(", ") || "not indexed"),
    card("Risks", risks.join(", ") || "none"),
    card("Records", String(detail.source_records.length)),
    card("Workflows", Object.keys(detail.expected.workflows || {}).join(", ") || "none"),
  ].join("");
}

function renderFamilies(families) {
  document.querySelector("#family-view").innerHTML = families
    .map((family) => card(`${family.family_id} (${family.fixture_count})`, family.description))
    .join("");
}

function renderProvenance(persisted) {
  document.querySelector("#source-list").innerHTML = persisted.source_records
    .slice(0, 20)
    .map((record) => `<div class="item"><strong>${escapeHtml(record.id)}</strong><br>${escapeHtml(record.domain)} / ${escapeHtml(record.source)}</div>`)
    .join("");
  document.querySelector("#normalized-list").innerHTML = persisted.normalized_facts
    .slice(0, 20)
    .map((fact) => `<div class="item"><strong>${escapeHtml(fact.id)}</strong><br>refs: ${escapeHtml(fact.provenance_refs.join(", "))}</div>`)
    .join("");
}

function renderDerivedFacts(facts) {
  document.querySelector("#derived-list").innerHTML = facts
    .map((fact) => `<div class="item"><strong>${escapeHtml(fact.name)}</strong><br>${escapeHtml(JSON.stringify(fact.value))}</div>`)
    .join("");
}

async function renderGraph(fixtureId) {
  const data = await api.graph(fixtureId);
  const nodes = data.graph.nodes.slice(0, 28);
  const edges = data.graph.edges.slice(0, 28);
  document.querySelector("#evidence-graph").innerHTML = [
    ...nodes.map((node) => `<div class="item graph-node"><strong>${escapeHtml(node.node_type)}</strong><br>${escapeHtml(node.label)}</div>`),
    ...edges.map((edge) => `<div class="item graph-edge"><strong>${escapeHtml(edge.relation)}</strong><br>${escapeHtml(edge.source_node_id)} -> ${escapeHtml(edge.target_node_id)}</div>`),
  ].join("");
  document.querySelector("#evidence-panel").textContent = JSON.stringify(
    {
      fixture_id: fixtureId,
      node_count: data.graph.nodes.length,
      edge_count: data.graph.edges.length,
    },
    null,
    2
  );
}

async function renderReports() {
  const data = await api.reports();
  document.querySelector("#report-list").innerHTML = data.report_candidates
    .map((report) => `<div class="item"><strong>${escapeHtml(report.fixture_id)} / ${escapeHtml(report.report_type)}</strong><br>${escapeHtml(report.delivery_status)}</div>`)
    .join("");
  const settings = await api.reportSettings();
  document.querySelector("#report-settings").innerHTML = settings.report_settings
    .map((item) => `<div class="item"><strong>${escapeHtml(item.fixture_id)}</strong><br>${escapeHtml(item.morning_depth)} morning / ${escapeHtml(item.weekly_depth)} weekly</div>`)
    .join("") || '<div class="item">No report settings imported yet</div>';
}

function renderConversation(detail) {
  const messages = detail.source_records.filter((record) => record.domain === "conversation_message");
  document.querySelector("#thread-list").innerHTML = messages.length
    ? messages.map((record) => `<div class="item"><strong>${escapeHtml(record.payload.surface)}</strong><br>${escapeHtml(record.payload.text)}</div>`).join("")
    : '<div class="item">No conversation messages</div>';
}

async function renderRecommendations() {
  const recommendations = await api.recommendations();
  document.querySelector("#recommendation-followup").innerHTML = recommendations.recommendations
    .slice(0, 40)
    .map((item) => `<div class="item"><strong>${escapeHtml(item.recommendation_class)}</strong><br>${escapeHtml(item.fixture_id)} / ${escapeHtml(item.workflow)}</div>`)
    .join("") || '<div class="item">No recommendations imported yet</div>';
  const followups = await api.followups();
  document.querySelector("#followup-list").innerHTML = followups.follow_up_outcomes
    .map((item) => `<div class="item"><strong>${escapeHtml(item.outcome_status)}</strong><br>${escapeHtml(item.fixture_id)}</div>`)
    .join("") || '<div class="item">No follow-up outcomes imported yet</div>';
}

async function renderSafetyAudit() {
  const safety = await api.safety();
  document.querySelector("#audit-summary").innerHTML = [
    card("Events", String(safety.safety_audit.event_count)),
    card("High severity", String(safety.safety_audit.high_severity_count)),
    card("No-delivery", String(safety.safety_audit.no_delivery_count)),
    ...safety.safety_audit.events.slice(0, 30).map((event) =>
      `<div class="item ${event.severity === "high" ? "danger" : ""}"><strong>${escapeHtml(event.boundary_type)}</strong><br>${escapeHtml(event.status)}</div>`
    ),
  ].join("");
}

async function renderContracts() {
  const contracts = await api.contracts();
  document.querySelector("#api-contract-list").innerHTML = contracts.contracts
    .map((item) => `<div class="item"><strong>${escapeHtml(item.method)} ${escapeHtml(item.path_template)}</strong><br>${escapeHtml(item.category)} / ${item.expected_status}</div>`)
    .join("");
}

function renderWorkflowMatrix(rows) {
  document.querySelector("#workflow-matrix").innerHTML = rows
    .slice(0, 80)
    .map((row) => `<div class="item"><strong>${escapeHtml(row.workflow)}</strong><br>${escapeHtml(row.fixture_id)}</div>`)
    .join("");
}

async function runSelectedWorkflow() {
  return withOperation("Running workflow", async () => {
    const workflow = document.querySelector("#workflow-selector").value;
    const result = await api.runWorkflow(state.selectedFixtureId, workflow);
    state.lastRunId = result.workflow_run.id;
    document.querySelector("#workflow-output").textContent = JSON.stringify(result.workflow_run, null, 2);
    const timeline = await api.timeline(state.lastRunId);
    renderTimeline(timeline.timeline);
    document.querySelector("#evidence-panel").textContent = JSON.stringify(timeline.timeline, null, 2);
    await renderGraph(state.selectedFixtureId);
    await renderRecommendations();
    setStatus(`Workflow complete: ${workflow}`);
    return { workflow, result, timeline };
  });
}

async function renderSnapshot() {
  const snapshot = await api.snapshot();
  document.querySelector("#snapshot-output").textContent = JSON.stringify(
    {
      snapshot_id: snapshot.snapshot.snapshot_id,
      synthetic_only: snapshot.snapshot.synthetic_only,
      fixture_count: snapshot.snapshot.manifest_validation.fixture_count,
      table_count: Object.keys(snapshot.snapshot.tables).length,
    },
    null,
    2
  );
}

function renderTimeline(timeline) {
  document.querySelector("#replay-timeline").innerHTML = timeline.steps
    .map((step) => `<div class="item"><strong>${step.step_index}. ${escapeHtml(step.step_name)}</strong><br>${escapeHtml(step.status)} / refs ${step.evidence_refs.length}</div>`)
    .join("");
}

function activateView(viewName) {
  document.querySelectorAll(".nav-button").forEach((item) => item.classList.remove("is-active"));
  document.querySelectorAll("[data-view-panel]").forEach((panel) => panel.classList.remove("is-active"));
  const button = document.querySelector(`[data-view="${viewName}"]`);
  const panel = document.querySelector(`[data-view-panel="${viewName}"]`);
  if (button && panel) {
    button.classList.add("is-active");
    panel.classList.add("is-active");
    setStatus(`View: ${button.textContent.trim()}`);
  }
}

function firstExpectedWorkflow(detail) {
  const workflows = Object.keys(detail.expected.workflows || {});
  return workflows[0] || document.querySelector("#workflow-selector").value;
}

function renderScenarioSteps(steps) {
  const defaults = steps.length
    ? steps
    : [
        { name: "Select fixture", status: "pending" },
        { name: "Import fixture", status: "pending" },
        { name: "Run expected workflow", status: "pending" },
        { name: "Inspect replay timeline", status: "pending" },
        { name: "Refresh evidence and audit surfaces", status: "pending" },
      ];
  document.querySelector("#scenario-steps").innerHTML = defaults
    .map((step) => `<div class="item scenario-step ${escapeHtml(step.status)}"><strong>${escapeHtml(step.name)}</strong><br>${escapeHtml(step.status)}</div>`)
    .join("");
}

async function runScenarioWalkthrough() {
  await withOperation("Running operator scenario", async () => {
    activateView("runner");
    const fixtureId = state.selectedFixtureId;
    const detail = state.selectedFixtureDetail || (await api.fixture(fixtureId));
    const workflow = firstExpectedWorkflow(detail);
    document.querySelector("#workflow-selector").value = workflow;
    const steps = [
      { name: `Selected ${fixtureId}`, status: "pass" },
      { name: "Imported fixture", status: "pass" },
      { name: `Ran ${workflow}`, status: "running" },
      { name: "Inspected replay timeline", status: "pending" },
      { name: "Refreshed evidence and audit surfaces", status: "pending" },
    ];
    renderScenarioSteps(steps);
    const result = await api.runWorkflow(fixtureId, workflow);
    state.lastRunId = result.workflow_run.id;
    document.querySelector("#workflow-output").textContent = JSON.stringify(result.workflow_run, null, 2);
    const timeline = await api.timeline(state.lastRunId);
    renderTimeline(timeline.timeline);
    await renderGraph(fixtureId);
    await renderReports();
    await renderRecommendations();
    await renderSafetyAudit();
    steps[2].status = "pass";
    steps[3].status = timeline.timeline.steps.length ? "pass" : "fail";
    steps[4].status = "pass";
    renderScenarioSteps(steps);
    const summary = {
      fixture_id: fixtureId,
      workflow,
      run_id: state.lastRunId,
      timeline_steps: timeline.timeline.steps.length,
      recommendation_count: document.querySelectorAll("#recommendation-followup .item").length,
      audit_items: document.querySelectorAll("#audit-summary .item").length,
    };
    document.querySelector("#scenario-output").textContent = JSON.stringify(summary, null, 2);
    setStatus(`Scenario complete: ${fixtureId}`);
  });
}

async function resetWorkbench() {
  await withOperation("Resetting workbench state", async () => {
    localStorage.removeItem(STORAGE_KEY);
    state.lastRunId = null;
    state.scenario = [];
    document.querySelector("#workflow-output").textContent = "";
    document.querySelector("#scenario-output").textContent = "";
    document.querySelector("#replay-timeline").innerHTML = "";
    renderScenarioSteps([]);
    if (state.fixtures[0]) {
      await selectFixture(state.fixtures[0].fixture_id);
    }
    activateView("catalog");
    setStatus("Workbench reset");
  });
}

async function init() {
  await withOperation("Bootstrapping synthetic workbench", async () => {
    wireNavigation();
    const boot = await api.bootstrap();
    state.fixtures = boot.fixtures;
    renderSafety(boot.safety);
    renderFamilies(boot.families);
    renderFixtureSelector(boot.fixtures);
    renderWorkflowMatrix(boot.workflow_matrix);
    renderScenarioSteps([]);
    await renderContracts();
    await renderSnapshot();
    const urlManualExport = new URLSearchParams(window.location.search).get("manual_export");
    await renderImportLab(boot.source_adapters || [], boot.manual_exports || [], urlManualExport);
    document.querySelector("#run-workflow").addEventListener("click", runSelectedWorkflow);
    document.querySelector("#run-scenario").addEventListener("click", runScenarioWalkthrough);
    document.querySelector("#reset-workbench").addEventListener("click", resetWorkbench);
    document.querySelector("#import-fixture").addEventListener("click", () => selectFixture(state.selectedFixtureId));
    document.querySelector("#preview-manual-import").addEventListener("click", previewSelectedManualImport);
    document.querySelector("#commit-manual-import").addEventListener("click", commitSelectedManualImport);
    const urlFixture = new URLSearchParams(window.location.search).get("fixture");
    const urlView = new URLSearchParams(window.location.search).get("view");
    const savedFixture = urlFixture || localStorage.getItem(STORAGE_KEY);
    const defaultFixture = boot.fixtures.find((fixture) => fixture.fixture_id === savedFixture) || boot.fixtures[0];
    if (defaultFixture) {
      await selectFixture(defaultFixture.fixture_id);
    }
    if (urlView) {
      activateView(urlView);
    }
    setStatus("Synthetic workbench ready");
  });
}

async function renderImportLab(adapters, exports, selectedExportId) {
  document.querySelector("#adapter-catalog").innerHTML = adapters
    .map((adapter) => card(adapter.label, `${adapter.adapter_id} / ${adapter.domains.join(", ")}`))
    .join("");
  const selector = document.querySelector("#manual-export-selector");
  selector.innerHTML = exports
    .map((item) => `<option value="${escapeHtml(item.export_id)}">${escapeHtml(item.export_id)}</option>`)
    .join("");
  if (selectedExportId && exports.some((item) => item.export_id === selectedExportId)) {
    selector.value = selectedExportId;
  }
  await renderManualImportAudit();
  if (exports[0]) {
    document.querySelector("#manual-import-preview").innerHTML = card("Ready", "Select Preview to inspect a synthetic manual export.");
  }
}

async function previewSelectedManualImport() {
  await withOperation("Previewing manual import", async () => {
    activateView("imports");
    const exportId = document.querySelector("#manual-export-selector").value;
    const result = await api.previewManualImport(exportId);
    renderManualImportSession(result.session);
    setStatus(`Previewed ${exportId}`);
  });
}

async function commitSelectedManualImport() {
  await withOperation("Committing synthetic import preview", async () => {
    activateView("imports");
    const exportId = document.querySelector("#manual-export-selector").value;
    const result = await api.commitManualImport(exportId);
    renderManualImportSession(result.session);
    await renderManualImportAudit();
    setStatus(`Committed synthetic import: ${exportId}`);
  });
}

function renderManualImportSession(session) {
  document.querySelector("#manual-import-preview").innerHTML = [
    card("Session", `${session.id} / ${session.status}`),
    card("Rows", String(session.row_count)),
    card("Issues", String(session.issue_count)),
    card("Conflicts", String(session.conflict_count)),
    ...session.issues.slice(0, 12).map((issue) =>
      `<div class="item ${issue.severity === "error" ? "danger" : "warning"}"><strong>${escapeHtml(issue.issue_type)}</strong><br>${escapeHtml(issue.field)}: ${escapeHtml(issue.message)}</div>`
    ),
    ...session.rows.slice(0, 10).map((row) =>
      `<div class="item"><strong>${escapeHtml(row.domain)} / row ${row.row_index}</strong><br>${escapeHtml(row.source_record_id)} -> ${escapeHtml(JSON.stringify(row.normalized))}</div>`
    ),
  ].join("");
  document.querySelector("#manual-import-mapping").innerHTML = session.mappings
    .slice(0, 28)
    .map((mapping) => `<div class="item"><strong>${escapeHtml(mapping.source_field)} -> ${escapeHtml(mapping.normalized_field)}</strong><br>${escapeHtml(mapping.transform)} / ${escapeHtml(mapping.confidence)}</div>`)
    .join("");
  document.querySelector("#manual-import-conflicts").innerHTML = session.conflicts.length
    ? session.conflicts.map((conflict) => `<div class="item warning"><strong>${escapeHtml(conflict.conflict_type)}</strong><br>${escapeHtml(conflict.message)}</div>`).join("")
    : '<div class="item">No conflicts detected</div>';
}

async function renderManualImportAudit() {
  const audit = await api.manualImportAudit();
  const summary = audit.manual_import_audit;
  document.querySelector("#manual-import-audit").innerHTML = [
    card("Adapters", String(summary.adapter_count)),
    card("Synthetic exports", String(summary.manual_export_count)),
    card("Sessions", String(summary.session_count)),
    card("Issues", String(summary.issue_count)),
    card("Conflicts", String(summary.conflict_count)),
  ].join("");
}

function card(label, value) {
  return `<div class="item"><strong>${escapeHtml(label)}</strong><br>${escapeHtml(value)}</div>`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

init();
