"""Minimal V2 settings. No secrets in source; optional env overrides only."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Schema identity constants (not secrets).
SCHEMA_IDENTITY = "ai_factory_os_v2"
SCHEMA_VERSION = "1"


@dataclass(frozen=True)
class Settings:
    """V2 runtime/database configuration."""

    repo_root: Path
    database_path: Path
    schema_identity: str
    schema_version: str


def get_settings() -> Settings:
    """Load settings from environment with safe local defaults.

    Secrets (API keys, tokens, passwords) must never be hardcoded here.
    Use environment variables or a local .env file that is gitignored.
    """
    default_db = REPO_ROOT / "database" / "runtime" / "ai_factory_v2.db"
    raw = os.environ.get("AI_FACTORY_V2_DB", "").strip()
    database_path = Path(raw) if raw else default_db
    if not database_path.is_absolute():
        database_path = (REPO_ROOT / database_path).resolve()
    return Settings(
        repo_root=REPO_ROOT,
        database_path=database_path,
        schema_identity=SCHEMA_IDENTITY,
        schema_version=SCHEMA_VERSION,
    )
