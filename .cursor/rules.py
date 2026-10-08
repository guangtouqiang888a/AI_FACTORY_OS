# AI_FACTORY_OS V2 - local Cursor boundary (not Runtime Authority).
# Authority: AGENTS.md + docs/01_CURRENT_STATE + docs/05_EXECUTION/ACTIVE_TASK.md
# Legacy Entry-driven rules archived at:
#   99_ARCHIVE_RUNTIME/legacy_runtime/cursor_rules_production_grade_v1.py

RULES = {
    "version": "v2-baseline",
    "runtime_authority": ["app", "database", "config", "tests"],
    "legacy_archive": ["99_ARCHIVE_RUNTIME", "docs/99_ARCHIVE"],
    "forbid": [
        "treat_legacy_runtime_as_current",
        "delete_historical_assets",
        "silent_authority_from_conversation",
    ],
}
