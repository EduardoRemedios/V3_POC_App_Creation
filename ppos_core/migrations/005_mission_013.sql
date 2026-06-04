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

