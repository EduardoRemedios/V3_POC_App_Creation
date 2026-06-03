CREATE TABLE IF NOT EXISTS schema_migrations (
  version TEXT PRIMARY KEY,
  applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fixture_imports (
  fixture_id TEXT PRIMARY KEY,
  scenario TEXT NOT NULL,
  synthetic_only INTEGER NOT NULL,
  timezone TEXT NOT NULL,
  imported_at TEXT NOT NULL,
  import_count INTEGER NOT NULL DEFAULT 1,
  source_record_count INTEGER NOT NULL,
  normalized_fact_count INTEGER NOT NULL,
  derived_fact_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS source_records (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  source TEXT NOT NULL,
  source_record_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  ingested_at TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  UNIQUE(fixture_id, source, source_record_id)
);

CREATE TABLE IF NOT EXISTS normalized_facts (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  value_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_provenance (
  fact_id TEXT NOT NULL,
  source_record_id TEXT NOT NULL,
  fixture_id TEXT NOT NULL,
  PRIMARY KEY (fact_id, source_record_id)
);

CREATE TABLE IF NOT EXISTS derived_facts (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  name TEXT NOT NULL,
  value_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_packs (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  uncertainty TEXT NOT NULL,
  created_by TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_refs (
  evidence_pack_id TEXT NOT NULL,
  ref_id TEXT NOT NULL,
  ref_kind TEXT NOT NULL,
  fixture_id TEXT NOT NULL,
  PRIMARY KEY (evidence_pack_id, ref_id)
);

CREATE TABLE IF NOT EXISTS conversation_threads (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conversation_messages (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  thread_id TEXT NOT NULL,
  surface TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  text TEXT NOT NULL,
  input_mode TEXT NOT NULL,
  source_record_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS surface_events (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  thread_id TEXT NOT NULL,
  surface TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  event_type TEXT NOT NULL,
  source_record_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS intent_sessions (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  thread_id TEXT NOT NULL,
  workflow TEXT NOT NULL,
  status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workflow_runs (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  workflow TEXT NOT NULL,
  status TEXT NOT NULL,
  recommendation_class TEXT NOT NULL,
  evidence_pack_id TEXT NOT NULL,
  output_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS report_candidates (
  id TEXT PRIMARY KEY,
  fixture_id TEXT NOT NULL,
  report_type TEXT NOT NULL,
  sections_json TEXT NOT NULL,
  evidence_pack_id TEXT NOT NULL,
  delivery_status TEXT NOT NULL,
  output_json TEXT NOT NULL
);
