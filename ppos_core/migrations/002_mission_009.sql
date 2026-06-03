CREATE TABLE IF NOT EXISTS fixture_families (
  family_id TEXT PRIMARY KEY,
  description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fixture_manifest_entries (
  fixture_id TEXT PRIMARY KEY,
  families_json TEXT NOT NULL,
  risks_json TEXT NOT NULL,
  workflows_json TEXT NOT NULL,
  api_cases_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fixture_risk_coverage (
  fixture_id TEXT NOT NULL,
  risk TEXT NOT NULL,
  PRIMARY KEY (fixture_id, risk)
);

CREATE TABLE IF NOT EXISTS fixture_expected_workflows (
  fixture_id TEXT NOT NULL,
  workflow TEXT NOT NULL,
  PRIMARY KEY (fixture_id, workflow)
);

CREATE TABLE IF NOT EXISTS fixture_expected_api_cases (
  fixture_id TEXT NOT NULL,
  api_case TEXT NOT NULL,
  PRIMARY KEY (fixture_id, api_case)
);

CREATE TABLE IF NOT EXISTS workflow_timeline_steps (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  run_id TEXT NOT NULL,
  workflow TEXT NOT NULL,
  step_index INTEGER NOT NULL,
  step_name TEXT NOT NULL,
  status TEXT NOT NULL,
  evidence_refs_json TEXT NOT NULL,
  output_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS replay_audit_summaries (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  run_id TEXT,
  workflow TEXT,
  timeline_step_count INTEGER NOT NULL,
  evidence_ref_count INTEGER NOT NULL,
  passed INTEGER NOT NULL,
  summary_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_graph_nodes (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  node_type TEXT NOT NULL,
  label TEXT NOT NULL,
  ref_id TEXT NOT NULL,
  metadata_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_graph_edges (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  source_node_id TEXT NOT NULL,
  target_node_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  metadata_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recommendations (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  workflow TEXT NOT NULL,
  recommendation_class TEXT NOT NULL,
  evidence_pack_id TEXT,
  thread_id TEXT,
  status TEXT NOT NULL,
  confidence TEXT NOT NULL,
  created_at TEXT NOT NULL,
  payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS follow_up_outcomes (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  recommendation_id TEXT NOT NULL,
  outcome_status TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  thread_id TEXT,
  payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS report_settings (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  morning_depth TEXT NOT NULL,
  weekly_depth TEXT NOT NULL,
  quiet_hours_start TEXT NOT NULL,
  quiet_hours_end TEXT NOT NULL,
  cooldown_hours INTEGER NOT NULL,
  proactive_enabled INTEGER NOT NULL,
  payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS safety_boundary_events (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  boundary_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  status TEXT NOT NULL,
  evidence_refs_json TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS api_contract_cases (
  id TEXT PRIMARY KEY,
  method TEXT NOT NULL,
  path_template TEXT NOT NULL,
  category TEXT NOT NULL,
  expected_status INTEGER NOT NULL,
  error_shape INTEGER NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS snapshot_exports (
  id TEXT PRIMARY KEY,
  fixture_count INTEGER NOT NULL,
  table_count INTEGER NOT NULL,
  payload_json TEXT NOT NULL,
  validation_status TEXT NOT NULL,
  created_at TEXT NOT NULL
);
