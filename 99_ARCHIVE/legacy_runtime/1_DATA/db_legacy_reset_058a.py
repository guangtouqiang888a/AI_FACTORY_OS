# 1_DATA/db_legacy_reset_058a.py — Entry 058A Legacy Archive → Clean Current DB
#
# ONLY after provenance confirms SAMPLE/TEST_FIXTURE/SIMULATION.
# Archives entire DB (including mixed 051–057 operational rows), then
# recreates Current DB via existing ensure_* schema APIs.
# Restores publish_queue operational rows (not sample products) from archive snapshot.

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "6_EXECUTION"))

import config  # noqa: E402
import database  # noqa: E402
import market_event_core as mec  # noqa: E402
import market_signal_core as msc  # noqa: E402
import publish_queue as pq  # noqa: E402

TZ_CN = timezone(timedelta(hours=8))
ARCHIVE_DIR = ROOT / "99_ARCHIVE" / "database_history"
LEGACY_NAME = "ai_factory_legacy_simulation_20260830.db"
MANIFEST_NAME = "DATABASE_ARCHIVE_MANIFEST.md"
SNAPSHOT_NAME = "legacy_operational_snapshot_v1.json"


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_row_counts(db_path: Path) -> dict:
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    tables = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    ]
    counts = {}
    for t in tables:
        counts[t] = conn.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
    conn.close()
    return counts


def snapshot_operational_queue(db_path: Path) -> list[dict]:
    """Preserve publish_queue rows (commercial lifecycle runtime), not sample products."""
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = [dict(r) for r in conn.execute("SELECT * FROM publish_queue")]
    except sqlite3.Error:
        rows = []
    conn.close()
    return rows


def write_manifest(
    *,
    original: Path,
    archive: Path,
    digest: str,
    counts: dict,
    classification: str,
) -> Path:
    path = ARCHIVE_DIR / MANIFEST_NAME
    md = f"""# DATABASE ARCHIVE MANIFEST
# Entry 058A

| Field | Value |
|-------|-------|
| original_path | `{original}` |
| archive_path | `{archive}` |
| sha256 | `{digest}` |
| size_bytes | {archive.stat().st_size} |
| archived_at | {_now_iso()} |
| not_current_sot | **true** |
| origin_classification | **{classification}** |
| reason | Early scoring-practice / sample-fixture database; source_url uses sample/test; raw file named `*_sample.xlsx`; product titles/keywords marked 测试/test. Mixed later Entry 051–057 schema rows archived together. |

## Table Row Counts (at archive)

| Table | Rows |
|-------|------|
"""
    for t, n in sorted(counts.items()):
        md += f"| `{t}` | {n} |\n"
    md += """
## Rules

- LEGACY / Archive only — **not** Current Operational SoT
- Do not feed archived SAMPLE rows into Real Commercial Learning
- Raw xianyu files preserved separately under `data/raw/xianyu/`
"""
    path.write_text(md, encoding="utf-8")
    return path


def init_clean_current_db() -> dict:
    """Create empty Current DB using existing schema mechanisms."""
    db = Path(config.DB_PATH)
    if db.exists():
        raise RuntimeError(
            f"Refusing to init while {db} still exists — archive/replace first"
        )
    database.ensure_schema()
    mec.ensure_market_event_schema()
    msc.ensure_market_signal_schema()
    pq.ensure_publish_queue_schema()
    # Ensure baseline platform metadata only (system, not commercial rows)
    with database.get_connection() as conn:
        conn.execute("INSERT OR IGNORE INTO platforms (id, name) VALUES (1, 'xianyu')")
        conn.commit()
    counts = collect_row_counts(db)
    return {"db_path": str(db), "row_counts": counts}


def restore_publish_queue_rows(rows: list[dict]) -> int:
    if not rows:
        return 0
    pq.ensure_publish_queue_schema()
    restored = 0
    with database.get_connection() as conn:
        cols = [
            "publish_queue_id",
            "product_id",
            "product_asset_id",
            "product_type",
            "experiment_id",
            "production_request_id",
            "platform",
            "listing_title",
            "price",
            "currency",
            "risk_status",
            "quality_status",
            "commercial_status",
            "commercial_score",
            "queue_status",
            "blockers",
            "package_path",
            "notes",
            "observation_eligible",
            "created_at",
            "updated_at",
        ]
        for row in rows:
            payload = {c: row.get(c) for c in cols}
            # Never mark published without evidence
            if payload.get("queue_status") == "PUBLISHED" and not row.get("publish_evidence"):
                pass
            placeholders = ", ".join("?" * len(cols))
            conn.execute(
                f"INSERT OR REPLACE INTO publish_queue ({', '.join(cols)}) VALUES ({placeholders})",
                [payload[c] for c in cols],
            )
            restored += 1
        conn.commit()
    return restored


def run_archive_and_reset(*, force: bool = False) -> dict:
    original = Path(config.DB_PATH)
    if not original.exists():
        return {"ok": False, "reason": "current_db_missing"}

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = ARCHIVE_DIR / LEGACY_NAME
    if archive_path.exists() and not force:
        return {"ok": False, "reason": "archive_already_exists", "path": str(archive_path)}

    counts_before = collect_row_counts(original)
    queue_rows = snapshot_operational_queue(original)

    # Evidence gate: refuse if products look REAL (has non-sample URLs)
    conn = sqlite3.connect(f"file:{original.as_posix()}?mode=ro", uri=True)
    urls = [
        r[0]
        for r in conn.execute(
            "SELECT DISTINCT source_url FROM products WHERE source_url IS NOT NULL AND source_url != ''"
        )
    ]
    conn.close()
    sample_markers = ("sample", "/item/test", "fixture", "mock", "localhost")
    non_sample = [
        u
        for u in urls
        if u and not any(m in str(u).lower() for m in sample_markers)
    ]
    if non_sample and not force:
        return {
            "ok": False,
            "reason": "non_sample_urls_present_manual_review_required",
            "urls": non_sample[:20],
        }

    classification = "SAMPLE / TEST_FIXTURE / SIMULATION (scoring-practice legacy)"
    shutil.copy2(original, archive_path)
    digest = sha256_file(archive_path)

    # Verify archive opens
    vconn = sqlite3.connect(f"file:{archive_path.as_posix()}?mode=ro", uri=True)
    v_ok = vconn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == counts_before.get(
        "products", -1
    )
    vconn.close()
    if not v_ok:
        return {"ok": False, "reason": "archive_verification_failed"}

    snap = {
        "entry": "058A",
        "archived_at": _now_iso(),
        "archive_path": str(archive_path),
        "sha256": digest,
        "row_counts": counts_before,
        "publish_queue_rows": queue_rows,
        "origin_classification": classification,
        "unique_source_urls": urls,
    }
    (ARCHIVE_DIR / SNAPSHOT_NAME).write_text(
        json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    manifest = write_manifest(
        original=original,
        archive=archive_path,
        digest=digest,
        counts=counts_before,
        classification=classification,
    )

    # Replace Current DB: remove original only after archive verified
    original.unlink()
    init_info = init_clean_current_db()
    restored = restore_publish_queue_rows(queue_rows)
    counts_after = collect_row_counts(Path(config.DB_PATH))

    return {
        "ok": True,
        "entry": "058A",
        "classification": classification,
        "archive_path": str(archive_path),
        "sha256": digest,
        "manifest": str(manifest),
        "counts_before": counts_before,
        "counts_after": counts_after,
        "publish_queue_restored": restored,
        "init": init_info,
        "raw_preserved": True,
        "not_current_sot_legacy": True,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Archive + reset (destructive to Current path only after archive)")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps({"ok": False, "reason": "pass --execute after provenance confirmation"}, indent=2))
        return
    result = run_archive_and_reset(force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
