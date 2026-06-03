CREATE TABLE IF NOT EXISTS manual_import_sessions (
  id TEXT PRIMARY KEY,
  export_id TEXT NOT NULL,
  adapter_id TEXT NOT NULL,
  status TEXT NOT NULL,
  synthetic_only INTEGER NOT NULL,
  row_count INTEGER NOT NULL,
  issue_count INTEGER NOT NULL,
  conflict_count INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  committed_at TEXT,
  summary_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_import_source_files (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  export_id TEXT NOT NULL,
  path TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  parser TEXT NOT NULL,
  row_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_import_preview_rows (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  row_index INTEGER NOT NULL,
  source_record_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  raw_json TEXT NOT NULL,
  normalized_json TEXT NOT NULL,
  provenance_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_import_validation_issues (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  row_index INTEGER NOT NULL,
  severity TEXT NOT NULL,
  issue_type TEXT NOT NULL,
  field TEXT NOT NULL,
  message TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_import_mapping_rows (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  row_index INTEGER NOT NULL,
  source_field TEXT NOT NULL,
  normalized_field TEXT NOT NULL,
  transform TEXT NOT NULL,
  confidence TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_import_conflicts (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  conflict_type TEXT NOT NULL,
  signature TEXT NOT NULL,
  message TEXT NOT NULL,
  related_rows_json TEXT NOT NULL
);
