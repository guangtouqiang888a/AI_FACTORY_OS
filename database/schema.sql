-- AI_FACTORY_OS V2 — minimal schema (boundary proof only)
-- Identity: ai_factory_os_v2
-- Version: 1
-- No business tables (keywords / products / market / orders / users).

CREATE TABLE IF NOT EXISTS schema_metadata (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    schema_identity TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    initialization_status TEXT NOT NULL,
    initialized_at TEXT NOT NULL
);
