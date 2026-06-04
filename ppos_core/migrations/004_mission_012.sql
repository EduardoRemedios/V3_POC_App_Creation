ALTER TABLE manual_import_sessions ADD COLUMN reverted_at TEXT;
ALTER TABLE manual_import_sessions ADD COLUMN rollback_reason TEXT;
ALTER TABLE manual_import_sessions ADD COLUMN review_summary_json TEXT NOT NULL DEFAULT '{}';

ALTER TABLE manual_import_preview_rows ADD COLUMN review_state TEXT NOT NULL DEFAULT 'needs_clarification';
ALTER TABLE manual_import_preview_rows ADD COLUMN review_note TEXT NOT NULL DEFAULT '';
ALTER TABLE manual_import_preview_rows ADD COLUMN reviewed_at TEXT;

CREATE TABLE IF NOT EXISTS manual_import_audit_events (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
