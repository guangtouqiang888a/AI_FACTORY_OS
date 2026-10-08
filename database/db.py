"""V2 SQLite database: initialize, verify, reset. Isolated from legacy DB."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config.settings import SCHEMA_IDENTITY, SCHEMA_VERSION, Settings, get_settings

SCHEMA_SQL_PATH = Path(__file__).resolve().parent / "schema.sql"


def _connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=DELETE")
    return conn


def _apply_schema(conn: sqlite3.Connection) -> None:
    sql = SCHEMA_SQL_PATH.read_text(encoding="utf-8")
    conn.executescript(sql)
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT INTO schema_metadata (
            id, schema_identity, schema_version, initialization_status, initialized_at
        ) VALUES (1, ?, ?, 'initialized', ?)
        ON CONFLICT(id) DO UPDATE SET
            schema_identity = excluded.schema_identity,
            schema_version = excluded.schema_version,
            initialization_status = excluded.initialization_status,
            initialized_at = excluded.initialized_at
        """,
        (SCHEMA_IDENTITY, SCHEMA_VERSION, now),
    )
    conn.commit()


def initialize(settings: Settings | None = None) -> Path:
    """Create V2 DB from zero and write schema_metadata."""
    settings = settings or get_settings()
    conn = _connect(settings.database_path)
    try:
        _apply_schema(conn)
    finally:
        conn.close()
    return settings.database_path


def get_schema_info(settings: Settings | None = None) -> dict[str, Any]:
    """Read schema_metadata row. Raises if DB missing or metadata absent."""
    settings = settings or get_settings()
    path = settings.database_path
    if not path.exists():
        raise FileNotFoundError(f"V2 database not found: {path}")
    conn = _connect(path)
    try:
        row = conn.execute(
            "SELECT schema_identity, schema_version, initialization_status, initialized_at "
            "FROM schema_metadata WHERE id = 1"
        ).fetchone()
        if row is None:
            raise RuntimeError("schema_metadata missing (id=1)")
        return {
            "schema_identity": row["schema_identity"],
            "schema_version": row["schema_version"],
            "initialization_status": row["initialization_status"],
            "initialized_at": row["initialized_at"],
        }
    finally:
        conn.close()


def verify(settings: Settings | None = None) -> dict[str, Any]:
    """Verify schema identity/version/status match V2 baseline expectations."""
    settings = settings or get_settings()
    info = get_schema_info(settings)
    errors: list[str] = []
    if info["schema_identity"] != SCHEMA_IDENTITY:
        errors.append(
            f"identity={info['schema_identity']!r} expected={SCHEMA_IDENTITY!r}"
        )
    if info["schema_version"] != SCHEMA_VERSION:
        errors.append(
            f"version={info['schema_version']!r} expected={SCHEMA_VERSION!r}"
        )
    if info["initialization_status"] != "initialized":
        errors.append(f"status={info['initialization_status']!r}")
    if errors:
        raise RuntimeError("V2 schema verification failed: " + "; ".join(errors))
    return info


def _purge_v2_db_files(path: Path) -> None:
    """Remove V2 DB file and SQLite sidecars; fall back to in-place drop on Windows locks."""
    sidecars = (
        path,
        Path(str(path) + "-wal"),
        Path(str(path) + "-shm"),
        Path(str(path) + "-journal"),
    )
    if path.exists():
        conn = None
        try:
            conn = _connect(path)
            conn.execute("DROP TABLE IF EXISTS schema_metadata")
            conn.commit()
        except sqlite3.Error:
            pass
        finally:
            if conn is not None:
                conn.close()
    for candidate in sidecars:
        if not candidate.exists():
            continue
        try:
            candidate.unlink()
        except OSError:
            # Windows may briefly lock the main file; schema drop above is enough
            # for a safe reinitialize into the same path.
            continue


def reset(settings: Settings | None = None) -> Path:
    """Delete/rebuild V2 local DB only, then reinitialize. Never touches legacy paths."""
    settings = settings or get_settings()
    path = settings.database_path
    if "legacy_runtime" in path.parts:
        raise RuntimeError(f"refusing to reset path that looks like legacy archive: {path}")
    if "99_ARCHIVE" in path.parts:
        raise RuntimeError(f"refusing to reset path under 99_ARCHIVE: {path}")
    _purge_v2_db_files(path)
    return initialize(settings)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="AI_FACTORY_OS V2 database tools")
    parser.add_argument(
        "command",
        choices=("init", "verify", "reset"),
        help="init | verify | reset",
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.command == "init":
        path = initialize(settings)
        print(f"V2 database initialized: {path}")
        info = verify(settings)
        print(
            f"schema_identity={info['schema_identity']} "
            f"schema_version={info['schema_version']} "
            f"status={info['initialization_status']}"
        )
        return 0
    if args.command == "verify":
        info = verify(settings)
        print(
            f"V2 database OK: identity={info['schema_identity']} "
            f"version={info['schema_version']} "
            f"status={info['initialization_status']}"
        )
        return 0
    path = reset(settings)
    info = verify(settings)
    print(f"V2 database reset+reinitialized: {path}")
    print(
        f"schema_identity={info['schema_identity']} "
        f"schema_version={info['schema_version']} "
        f"status={info['initialization_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
