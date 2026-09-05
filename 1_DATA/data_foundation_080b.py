# 1_DATA/data_foundation_080b.py — Entry 080-B P2 Data Foundation (minimal)
#
# Additive schema + keyword / product-identity / observation linkage.
# Does NOT collect view_count, modify Extension, or implement P3/P4 planners.
# NULL want_count / view_count must never be coerced to 0.

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402

ENTRY_ID = "080-B"
FOUNDATION_VERSION = "080b.1.0"

TZ_CN = timezone(timedelta(hours=8))

EVIDENCE_REAL_OBSERVATION = "REAL_OBSERVATION"
EVIDENCE_TEST = "TEST"
EVIDENCE_SAMPLE = "SAMPLE"
EVIDENCE_SIMULATION = "SIMULATION"
EVIDENCE_HYPOTHESIS = "HYPOTHESIS"
EVIDENCE_UNKNOWN = "UNKNOWN"

KEYWORD_SOURCE_COLLECTION_QUERY = "COLLECTION_QUERY"
KEYWORD_SOURCE_MANUAL = "MANUAL"
KEYWORD_SOURCE_SEED = "SEED"
KEYWORD_SOURCE_DISCOVERED = "DISCOVERED"

DISCOVERY_SEED = "SEED"
DISCOVERY_DISCOVERED = "DISCOVERED"

EVIDENCE_STATUS_HYPOTHESIS = "HYPOTHESIS"
EVIDENCE_STATUS_EVIDENCE_BACKED = "EVIDENCE_BACKED"
EVIDENCE_STATUS_UNKNOWN = "UNKNOWN"

OBS_ADDITIVE_COLUMNS = (
    ("collection_query", "TEXT"),
    ("keyword_id", "INTEGER"),
    ("want_count_status", "TEXT"),
    ("image_url", "TEXT"),
    ("result_position", "INTEGER"),
    ("product_identity_id", "TEXT"),
    ("evidence_level", "TEXT"),
)

KEYWORD_ADDITIVE_COLUMNS = (
    ("keyword_uid", "TEXT"),
    ("canonical_keyword", "TEXT"),
    ("platform", "TEXT"),
    ("keyword_source", "TEXT"),
    ("keyword_type", "TEXT"),
    ("discovery_class", "TEXT"),
    ("evidence_status", "TEXT"),
    ("created_at", "TEXT"),
    ("updated_at", "TEXT"),
)

RUN_ADDITIVE_COLUMNS = (
    ("keyword_id", "INTEGER"),
    ("requested_record_count", "INTEGER"),
    ("requested_depth", "INTEGER"),
    ("actual_depth", "INTEGER"),
    ("stop_reason", "TEXT"),
    ("newly_accepted_count", "INTEGER"),
)


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _add_column_if_missing(conn: sqlite3.Connection, table: str, col: str, typedef: str) -> bool:
    cols = {r[1] for r in conn.execute(f"PRAGMA table_info([{table}])")}
    if col in cols:
        return False
    conn.execute(f"ALTER TABLE [{table}] ADD COLUMN [{col}] {typedef}")
    return True


def map_evidence_level(data_origin: str | None) -> str:
    o = (data_origin or "").upper()
    if o == "REAL":
        return EVIDENCE_REAL_OBSERVATION
    if o in ("TEST_FIXTURE", "TEST"):
        return EVIDENCE_TEST
    if o == "SAMPLE":
        return EVIDENCE_SAMPLE
    if o == "SIMULATION":
        return EVIDENCE_SIMULATION
    if o == "HYPOTHESIS":
        return EVIDENCE_HYPOTHESIS
    if o == "SYNTHETIC":
        return EVIDENCE_SIMULATION
    return EVIDENCE_UNKNOWN


def make_product_identity_id(*, source: str, source_item_id: str) -> str:
    material = f"{source}|{source_item_id}".encode("utf-8")
    return f"mpid_{hashlib.sha256(material).hexdigest()[:16]}"


def apply_additive_schema_only() -> dict[str, Any]:
    """Additive columns/tables only. Safe from market_source_core without recursion."""
    database.ensure_schema()
    added: list[str] = []
    with database.get_connection() as conn:
        # Require market_observations; if missing, caller must create base first
        tables = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        if "market_observations" not in tables or "collection_runs" not in tables:
            return {
                "entry": ENTRY_ID,
                "foundation_version": FOUNDATION_VERSION,
                "columns_added": [],
                "skipped": "base_market_tables_missing",
            }
        for col, typedef in KEYWORD_ADDITIVE_COLUMNS:
            if _add_column_if_missing(conn, "keywords", col, typedef):
                added.append(f"keywords.{col}")

        try:
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_keywords_uid "
                "ON keywords(keyword_uid) WHERE keyword_uid IS NOT NULL"
            )
        except sqlite3.OperationalError:
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_keywords_uid_nonuniq ON keywords(keyword_uid)"
            )

        for col, typedef in OBS_ADDITIVE_COLUMNS:
            if _add_column_if_missing(conn, "market_observations", col, typedef):
                added.append(f"market_observations.{col}")

        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mobs_keyword_id ON market_observations(keyword_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mobs_product_identity "
            "ON market_observations(product_identity_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_mobs_collection_query "
            "ON market_observations(collection_query)"
        )

        for col, typedef in RUN_ADDITIVE_COLUMNS:
            if _add_column_if_missing(conn, "collection_runs", col, typedef):
                added.append(f"collection_runs.{col}")

        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS market_product_identities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_identity_id TEXT UNIQUE NOT NULL,
                source TEXT NOT NULL,
                platform TEXT NOT NULL,
                source_item_id TEXT NOT NULL,
                canonical_url TEXT,
                first_seen_at TEXT,
                last_seen_at TEXT,
                observation_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(source, source_item_id)
            );
            CREATE INDEX IF NOT EXISTS idx_mpid_source_item
                ON market_product_identities(source, source_item_id);
            """
        )
        conn.commit()

    return {
        "entry": ENTRY_ID,
        "foundation_version": FOUNDATION_VERSION,
        "columns_added": added,
        "product_identity_table": "market_product_identities",
    }


def ensure_data_foundation_schema() -> dict[str, Any]:
    database.ensure_schema()
    import market_source_core as msc  # noqa: WPS433

    msc.ensure_market_source_schema()
    return apply_additive_schema_only()


def upsert_keyword_foundation(
    keyword: str,
    *,
    platform: str | None = "xianyu",
    keyword_source: str = KEYWORD_SOURCE_MANUAL,
    keyword_type: str = "QUERY",
    discovery_class: str = DISCOVERY_SEED,
    evidence_status: str = EVIDENCE_STATUS_UNKNOWN,
    category: str | None = None,
) -> dict[str, Any]:
    ensure_data_foundation_schema()
    kw = (keyword or "").strip()
    if not kw:
        raise ValueError("keyword required")
    now = _now_str()
    today = datetime.now().date().isoformat()
    with database.get_connection() as conn:
        row = conn.execute("SELECT * FROM keywords WHERE keyword = ?", (kw,)).fetchone()
        if row:
            rid = row["id"]
            conn.execute(
                """
                UPDATE keywords SET
                    last_seen_date=?, last_search_date=?,
                    canonical_keyword=COALESCE(canonical_keyword, ?),
                    platform=COALESCE(platform, ?),
                    keyword_source=COALESCE(keyword_source, ?),
                    keyword_type=COALESCE(keyword_type, ?),
                    discovery_class=COALESCE(discovery_class, ?),
                    evidence_status=?,
                    updated_at=?,
                    category=COALESCE(category, ?)
                WHERE id=?
                """,
                (
                    today,
                    today,
                    kw,
                    platform,
                    keyword_source,
                    keyword_type,
                    discovery_class,
                    evidence_status,
                    now,
                    category,
                    rid,
                ),
            )
            if not row["keyword_uid"]:
                uid = f"kw_{hashlib.sha256(kw.encode('utf-8')).hexdigest()[:12]}"
                conn.execute("UPDATE keywords SET keyword_uid=? WHERE id=?", (uid, rid))
            conn.commit()
            return dict(conn.execute("SELECT * FROM keywords WHERE id=?", (rid,)).fetchone())

        uid = f"kw_{hashlib.sha256(kw.encode('utf-8')).hexdigest()[:12]}"
        cur = conn.execute(
            """
            INSERT INTO keywords (
                keyword, category, first_seen_date, last_seen_date, last_search_date,
                keyword_uid, canonical_keyword, platform, keyword_source, keyword_type,
                discovery_class, evidence_status, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                kw,
                category or "query",
                today,
                today,
                today,
                uid,
                kw,
                platform,
                keyword_source,
                keyword_type,
                discovery_class,
                evidence_status,
                now,
                now,
            ),
        )
        conn.commit()
        return dict(conn.execute("SELECT * FROM keywords WHERE id=?", (cur.lastrowid,)).fetchone())


def get_keyword_by_text(keyword: str) -> dict[str, Any] | None:
    ensure_data_foundation_schema()
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM keywords WHERE keyword = ?", (keyword.strip(),)
        ).fetchone()
        return dict(row) if row else None


def ensure_product_identity(
    *,
    source: str,
    platform: str,
    source_item_id: str,
    canonical_url: str | None = None,
    seen_at: str | None = None,
) -> str:
    ensure_data_foundation_schema()
    if not source_item_id or not str(source_item_id).strip():
        raise ValueError("source_item_id required for product identity")
    sid = str(source_item_id).strip()
    pid = make_product_identity_id(source=source, source_item_id=sid)
    now = _now_str()
    seen = seen_at or _now_iso()
    with database.get_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM market_product_identities WHERE product_identity_id=?",
            (pid,),
        ).fetchone()
        if existing:
            conn.execute(
                """
                UPDATE market_product_identities SET
                    last_seen_at=?,
                    canonical_url=COALESCE(?, canonical_url),
                    updated_at=?,
                    observation_count=(
                        SELECT COUNT(*) FROM market_observations
                        WHERE product_identity_id=?
                    )
                WHERE product_identity_id=?
                """,
                (seen, canonical_url, now, pid, pid),
            )
            conn.commit()
            return pid
        conn.execute(
            """
            INSERT INTO market_product_identities (
                product_identity_id, source, platform, source_item_id,
                canonical_url, first_seen_at, last_seen_at,
                observation_count, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,0,?,?)
            """,
            (pid, source, platform, sid, canonical_url, seen, seen, now, now),
        )
        conn.commit()
        return pid


def backup_current_db() -> Path:
    src = Path(config.DB_PATH)
    if not src.exists():
        raise FileNotFoundError(src)
    dest_dir = ROOT / "99_ARCHIVE" / "database_history"
    dest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(TZ_CN).strftime("%Y%m%d_%H%M%S")
    dest = dest_dir / f"ai_factory_pre_080b_{stamp}.db"
    shutil.copy2(src, dest)
    return dest


def _parse_notes(notes: str | None) -> dict[str, Any]:
    if not notes:
        return {}
    try:
        obj = json.loads(notes)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _load_raw_index(raw_path: str | None) -> dict[str, dict[str, Any]]:
    if not raw_path:
        return {}
    p = Path(raw_path)
    if not p.exists():
        return {}
    try:
        batch = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    records = batch.get("records") or batch.get("candidates") or []
    if not records and isinstance(batch.get("payload"), dict):
        payload = batch["payload"]
        records = payload.get("records") or payload.get("candidates") or []
    out: dict[str, dict[str, Any]] = {}
    for rec in records:
        if not isinstance(rec, dict):
            continue
        iid = rec.get("source_item_id")
        if iid:
            out[str(iid)] = rec
    return out


def snapshot_observation_integrity(conn: sqlite3.Connection | None = None) -> dict[str, Any]:
    own = conn is None
    if own:
        conn = database.get_connection()
    try:
        n = conn.execute("SELECT COUNT(*) FROM market_observations").fetchone()[0]
        real = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE data_origin='REAL'"
        ).fetchone()[0]
        verified = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE verification_status='MANUAL_VERIFIED'"
        ).fetchone()[0]
        want_null = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE want_count IS NULL"
        ).fetchone()[0]
        want_zero = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE want_count = 0"
        ).fetchone()[0]
        view_null = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE view_count IS NULL"
        ).fetchone()[0]
        view_nonnull = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE view_count IS NOT NULL"
        ).fetchone()[0]
        items = conn.execute(
            "SELECT COUNT(DISTINCT source_item_id) FROM market_observations"
        ).fetchone()[0]
        urls = conn.execute(
            "SELECT COUNT(DISTINCT source_url) FROM market_observations"
        ).fetchone()[0]
        return {
            "row_count": n,
            "real_count": real,
            "manual_verified_count": verified,
            "want_null_count": want_null,
            "want_zero_count": want_zero,
            "view_null_count": view_null,
            "view_nonnull_count": view_nonnull,
            "distinct_source_item_id": items,
            "distinct_source_url": urls,
        }
    finally:
        if own:
            conn.close()


def backfill_existing_observations() -> dict[str, Any]:
    ensure_data_foundation_schema()
    before = snapshot_observation_integrity()
    with database.get_connection() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM market_observations")]
        raw_cache: dict[str | None, dict[str, dict[str, Any]]] = {}
        keyword_cache: dict[str, int] = {}
        linked = 0
        for r in rows:
            notes = _parse_notes(r.get("notes"))
            query = notes.get("query") or None
            if not query and r.get("run_id"):
                run = conn.execute(
                    "SELECT collection_query FROM collection_runs WHERE run_id=?",
                    (r["run_id"],),
                ).fetchone()
                if run and run["collection_query"]:
                    query = run["collection_query"]

            want_status = notes.get("want_count_status")
            if want_status is None and r.get("want_count") is None:
                want_status = "MISSING_ON_CARD"
            elif want_status is None and r.get("want_count") is not None:
                want_status = "VISIBLE_ON_CARD"

            raw_ref = r.get("raw_reference")
            if raw_ref not in raw_cache:
                raw_cache[raw_ref] = _load_raw_index(raw_ref)
            raw_rec = raw_cache.get(raw_ref, {}).get(str(r.get("source_item_id") or ""), {})

            image_url = raw_rec.get("image_url")
            result_position = raw_rec.get("result_position")
            if result_position is not None:
                try:
                    result_position = int(result_position)
                except (TypeError, ValueError):
                    result_position = None

            keyword_id = None
            if query:
                if query not in keyword_cache:
                    kw_row = conn.execute(
                        "SELECT id FROM keywords WHERE keyword=?", (query,)
                    ).fetchone()
                    if kw_row:
                        keyword_cache[query] = kw_row["id"]
                    else:
                        now = _now_str()
                        today = datetime.now().date().isoformat()
                        uid = f"kw_{hashlib.sha256(query.encode('utf-8')).hexdigest()[:12]}"
                        cur = conn.execute(
                            """
                            INSERT INTO keywords (
                                keyword, category, first_seen_date, last_seen_date,
                                last_search_date, keyword_uid, canonical_keyword, platform,
                                keyword_source, keyword_type, discovery_class,
                                evidence_status, created_at, updated_at
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                            """,
                            (
                                query,
                                "query",
                                today,
                                today,
                                today,
                                uid,
                                query,
                                r.get("platform") or "xianyu",
                                KEYWORD_SOURCE_COLLECTION_QUERY,
                                "QUERY",
                                DISCOVERY_SEED,
                                EVIDENCE_STATUS_EVIDENCE_BACKED
                                if r.get("data_origin") == "REAL"
                                else EVIDENCE_STATUS_UNKNOWN,
                                now,
                                now,
                            ),
                        )
                        keyword_cache[query] = cur.lastrowid
                keyword_id = keyword_cache[query]

            pid = None
            if r.get("source_item_id"):
                pid = make_product_identity_id(
                    source=r["source"], source_item_id=str(r["source_item_id"])
                )
                existing = conn.execute(
                    "SELECT id FROM market_product_identities WHERE product_identity_id=?",
                    (pid,),
                ).fetchone()
                now = _now_str()
                seen = r.get("observed_at") or _now_iso()
                if existing:
                    conn.execute(
                        """
                        UPDATE market_product_identities SET
                            last_seen_at=?,
                            canonical_url=COALESCE(?, canonical_url),
                            updated_at=?
                        WHERE product_identity_id=?
                        """,
                        (seen, r.get("source_url"), now, pid),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO market_product_identities (
                            product_identity_id, source, platform, source_item_id,
                            canonical_url, first_seen_at, last_seen_at,
                            observation_count, created_at, updated_at
                        ) VALUES (?,?,?,?,?,?,?,0,?,?)
                        """,
                        (
                            pid,
                            r["source"],
                            r.get("platform") or "xianyu",
                            str(r["source_item_id"]),
                            r.get("source_url"),
                            seen,
                            seen,
                            now,
                            now,
                        ),
                    )

            evidence = map_evidence_level(r.get("data_origin"))

            conn.execute(
                """
                UPDATE market_observations SET
                    collection_query=?,
                    keyword_id=?,
                    want_count_status=?,
                    image_url=?,
                    result_position=?,
                    product_identity_id=?,
                    evidence_level=?
                WHERE observation_id=?
                """,
                (
                    query,
                    keyword_id,
                    want_status,
                    image_url,
                    result_position,
                    pid,
                    evidence,
                    r["observation_id"],
                ),
            )
            linked += 1

        conn.execute(
            """
            UPDATE market_product_identities SET observation_count=(
                SELECT COUNT(*) FROM market_observations m
                WHERE m.product_identity_id = market_product_identities.product_identity_id
            )
            """
        )

        for query, kid in keyword_cache.items():
            conn.execute(
                "UPDATE collection_runs SET keyword_id=? WHERE collection_query=?",
                (kid, query),
            )
            conn.execute(
                "UPDATE keywords SET evidence_status=?, updated_at=? WHERE id=?",
                (EVIDENCE_STATUS_EVIDENCE_BACKED, _now_str(), kid),
            )

        conn.execute(
            """
            UPDATE collection_runs SET newly_accepted_count=accepted_count
            WHERE newly_accepted_count IS NULL AND accepted_count IS NOT NULL
            """
        )
        conn.commit()

    after = snapshot_observation_integrity()
    return {
        "before": before,
        "after": after,
        "rows_backfilled": linked,
        "preservation_ok": (
            before["row_count"] == after["row_count"]
            and before["real_count"] == after["real_count"]
            and before["manual_verified_count"] == after["manual_verified_count"]
            and before["want_null_count"] == after["want_null_count"]
            and before["view_null_count"] == after["view_null_count"]
            and after["view_nonnull_count"] == 0
            and before["want_zero_count"] == after["want_zero_count"]
        ),
    }


def run_migration(*, do_backup: bool = True) -> dict[str, Any]:
    backup_path = None
    if do_backup:
        backup_path = str(backup_current_db())
    schema = ensure_data_foundation_schema()
    backfill = backfill_existing_observations()
    with database.get_connection() as conn:
        kw_n = conn.execute("SELECT COUNT(*) FROM keywords").fetchone()[0]
        pid_n = conn.execute(
            "SELECT COUNT(*) FROM market_product_identities"
        ).fetchone()[0]
        linked_q = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE collection_query IS NOT NULL"
        ).fetchone()[0]
        linked_kw = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE keyword_id IS NOT NULL"
        ).fetchone()[0]
        linked_pid = conn.execute(
            "SELECT COUNT(*) FROM market_observations WHERE product_identity_id IS NOT NULL"
        ).fetchone()[0]
    return {
        "entry": ENTRY_ID,
        "backup_path": backup_path,
        "schema": schema,
        "backfill": backfill,
        "keywords_count": kw_n,
        "product_identities_count": pid_n,
        "obs_with_query": linked_q,
        "obs_with_keyword_id": linked_kw,
        "obs_with_product_identity": linked_pid,
        "ai_cost": 0,
    }


if __name__ == "__main__":
    report = run_migration(do_backup=True)
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
