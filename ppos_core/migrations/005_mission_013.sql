CREATE TABLE IF NOT EXISTS manual_import_materialized_facts (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  row_index INTEGER NOT NULL,
  fact_id TEXT NOT NULL,
  source_record_id TEXT NOT NULL,
  fixture_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  source_identity TEXT NOT NULL,
  source_file_hash TEXT NOT NULL,
  mapping_reference TEXT NOT NULL,
  mapping_confidence TEXT NOT NULL,
  confidence TEXT NOT NULL,
  conflict_strategy TEXT NOT NULL,
  precedence_rank INTEGER NOT NULL,
  conflict_group_id TEXT NOT NULL,
  active INTEGER NOT NULL,
  materialized_at TEXT NOT NULL,
  reverted_at TEXT,
  rollback_reason TEXT,
  provenance_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_import_materialization_conflicts (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  materialized_fact_id TEXT NOT NULL,
  existing_fact_id TEXT NOT NULL,
  existing_fixture_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  conflict_strategy TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_import_approval_records (
  id TEXT PRIMARY KEY,
  export_id TEXT NOT NULL,
  session_id TEXT,
  source_label TEXT NOT NULL,
  file_reference TEXT NOT NULL,
  data_categories_json TEXT NOT NULL,
  retention_posture TEXT NOT NULL,
  approval_state TEXT NOT NULL,
  preview_only INTEGER NOT NULL,
  synthetic_only INTEGER NOT NULL,
  consent_text TEXT NOT NULL,
  approved_at TEXT,
  created_at TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
