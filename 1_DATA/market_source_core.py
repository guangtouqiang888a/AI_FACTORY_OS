# 1_DATA/market_source_core.py — Entry 058B Market Source / Collection / Observation
#
# External Source → Connector → Raw → Normalizer → MarketObservation → (Signals later)
# Discovery Source ≠ Sales Channel ≠ Product ≠ Feedback Source
# LIVE_COLLECTION ≠ EXTERNAL_IMPORT ≠ TEST_FIXTURE
# SAMPLE / SIMULATION must not enter Current DB as REAL

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402

COLLECTOR_VERSION = "058d.1.0"
NORMALIZER_VERSION = "058d.1.0"

MODE_LIVE = "LIVE_COLLECTION"
MODE_IMPORT = "EXTERNAL_IMPORT"
MODE_FIXTURE = "TEST_FIXTURE"

ORIGIN_REAL = "REAL"
ORIGIN_SIMULATION = "SIMULATION"
ORIGIN_SYNTHETIC = "SYNTHETIC"
ORIGIN_SAMPLE = "SAMPLE"
ORIGIN_FIXTURE = "TEST_FIXTURE"
ORIGIN_UNKNOWN = "UNKNOWN"

# Verification: never forge platform-official verification
VERIF_UNVERIFIED = "UNVERIFIED"
VERIF_MANUAL = "MANUAL_VERIFIED"
VERIF_REVIEW = "REVIEW_REQUIRED"

# Live Xianyu HTTP/API/browser adapter: NOT present in Reality (Entry 058B audit)
LIVE_COLLECTION_AVAILABLE = False
LIVE_COLLECTION_REASON = (
    "No compliant live Xianyu HTTP/API/browser connector in codebase; "
    "existing collector is Excel→SQLite only. Auto bypass of login/captcha/anti-bot forbidden."
)

SAMPLE_URL_MARKERS = (
    "/item/sample",
    "/item/test",
    "example.com",
    "localhost",
    "fixture",
    "mock://",
)
SAMPLE_NAME_MARKERS = (
    "_sample",
    "sample_",
    "fixture",
    "mock_",
    "_demo",
    "test_fixture",
)

TZ_CN = timezone(timedelta(hours=8))


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_market_source_schema() -> None:
    database.ensure_schema()
    with database.get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS market_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT UNIQUE NOT NULL,
                source_type TEXT NOT NULL,
                platform TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                collection_mode TEXT NOT NULL,
                verification_mode TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS collection_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT UNIQUE NOT NULL,
                source_id TEXT NOT NULL,
                source TEXT NOT NULL,
                platform TEXT NOT NULL,
                collection_mode TEXT NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                raw_count INTEGER DEFAULT 0,
                accepted_count INTEGER DEFAULT 0,
                rejected_count INTEGER DEFAULT 0,
                duplicate_count INTEGER DEFAULT 0,
                normalized_count INTEGER DEFAULT 0,
                error_count INTEGER DEFAULT 0,
                collector_version TEXT,
                normalizer_version TEXT,
                raw_reference TEXT,
                error_summary TEXT,
                notes TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS market_observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id TEXT UNIQUE NOT NULL,
                run_id TEXT,
                source_id TEXT NOT NULL,
                source TEXT NOT NULL,
                platform TEXT NOT NULL,
                source_type TEXT,
                source_item_id TEXT,
                source_url TEXT,
                title TEXT,
                category TEXT,
                price REAL,
                currency TEXT DEFAULT 'CNY',
                view_count INTEGER,
                want_count INTEGER,
                comment_count INTEGER,
                share_count INTEGER,
                seller_reference TEXT,
                published_at TEXT,
                observed_at TEXT NOT NULL,
                raw_reference TEXT,
                data_origin TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                collector_version TEXT,
                normalizer_version TEXT,
                content_hash TEXT,
                dedupe_key TEXT NOT NULL,
                product_category TEXT,
                opportunity_product_type TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                UNIQUE(source, dedupe_key, observed_at)
            );
            CREATE INDEX IF NOT EXISTS idx_mobs_source_item
                ON market_observations(source, source_item_id);
            CREATE INDEX IF NOT EXISTS idx_mobs_run
                ON market_observations(run_id);
            CREATE INDEX IF NOT EXISTS idx_mobs_origin
                ON market_observations(data_origin);
            CREATE TABLE IF NOT EXISTS collectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collector_id TEXT UNIQUE NOT NULL,
                source_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                version TEXT NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
        # Additive columns for 058D (safe if already present)
        for ddl in (
            "ALTER TABLE market_sources ADD COLUMN acquisition_mode TEXT",
            "ALTER TABLE collection_runs ADD COLUMN collection_query TEXT",
            "ALTER TABLE collection_runs ADD COLUMN acquisition_mode TEXT",
            "ALTER TABLE collection_runs ADD COLUMN raw_sha256 TEXT",
        ):
            try:
                conn.execute(ddl)
                conn.commit()
            except sqlite3.OperationalError:
                pass
    seed_default_sources()
    ensure_collector_registry()


def ensure_collector_registry() -> None:
    database.ensure_schema()
    now = _now_str()
    rows = [
        {
            "collector_id": "col_xianyu_import",
            "source_id": "src_xianyu_marketplace",
            "mode": "MANUAL_IMPORT",
            "version": COLLECTOR_VERSION,
            "status": "ACTIVE",
            "notes": "USER_EXPORT/MANUAL_IMPORT via drop zone — Entry 058D",
        },
        {
            "collector_id": "col_xianyu_live_api",
            "source_id": "src_xianyu_marketplace",
            "mode": "LIVE_API",
            "version": COLLECTOR_VERSION,
            "status": "NOT_AVAILABLE_CURRENTLY",
            "notes": "No project eligibility; invitation/enterprise AppKey required",
        },
    ]
    with database.get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS collectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collector_id TEXT UNIQUE NOT NULL,
                source_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                version TEXT NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        for r in rows:
            conn.execute(
                """
                INSERT INTO collectors (
                    collector_id, source_id, mode, version, status, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(collector_id) DO UPDATE SET
                    version=excluded.version,
                    status=excluded.status,
                    notes=excluded.notes,
                    updated_at=excluded.updated_at
                """,
                (
                    r["collector_id"],
                    r["source_id"],
                    r["mode"],
                    r["version"],
                    r["status"],
                    r["notes"],
                    now,
                    now,
                ),
            )
        try:
            conn.execute(
                """
                UPDATE market_sources
                SET acquisition_mode=COALESCE(acquisition_mode, ?)
                WHERE source_id='src_xianyu_marketplace'
                """,
                ("MANUAL_IMPORT",),
            )
        except sqlite3.OperationalError:
            pass
        conn.commit()


def list_collectors() -> list[dict]:
    ensure_collector_registry()
    with database.get_connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM collectors ORDER BY collector_id")]


def seed_default_sources() -> None:
    now = _now_str()
    defaults = [
        {
            "source_id": "src_xianyu_marketplace",
            "source_type": "marketplace",
            "platform": "xianyu",
            "enabled": 1,
            "collection_mode": MODE_IMPORT if not LIVE_COLLECTION_AVAILABLE else MODE_LIVE,
            "verification_mode": "human_export_or_public_compliant",
            "notes": (
                "Discovery Source only. Does NOT imply sales_platform=xianyu. "
                f"LIVE_COLLECTION_AVAILABLE={LIVE_COLLECTION_AVAILABLE}"
            ),
        },
        # Future placeholders — registered disabled, not implemented
        {
            "source_id": "src_taobao_marketplace",
            "source_type": "marketplace",
            "platform": "taobao",
            "enabled": 0,
            "collection_mode": MODE_IMPORT,
            "verification_mode": "not_implemented",
            "notes": "Future source placeholder — connector NOT built (Entry 058B)",
        },
        {
            "source_id": "src_search_generic",
            "source_type": "search",
            "platform": "search",
            "enabled": 0,
            "collection_mode": MODE_IMPORT,
            "verification_mode": "not_implemented",
            "notes": "Future source placeholder — connector NOT built",
        },
        {
            "source_id": "src_social_generic",
            "source_type": "social",
            "platform": "social",
            "enabled": 0,
            "collection_mode": MODE_IMPORT,
            "verification_mode": "not_implemented",
            "notes": "Future source placeholder — connector NOT built",
        },
    ]
    with database.get_connection() as conn:
        for s in defaults:
            conn.execute(
                """
                INSERT OR IGNORE INTO market_sources (
                    source_id, source_type, platform, enabled, collection_mode,
                    verification_mode, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    s["source_id"],
                    s["source_type"],
                    s["platform"],
                    s["enabled"],
                    s["collection_mode"],
                    s["verification_mode"],
                    s["notes"],
                    now,
                    now,
                ),
            )
        conn.commit()


def list_sources(*, enabled_only: bool = False) -> list[dict]:
    ensure_market_source_schema()
    with database.get_connection() as conn:
        q = "SELECT * FROM market_sources"
        if enabled_only:
            q += " WHERE enabled=1"
        q += " ORDER BY source_id"
        return [dict(r) for r in conn.execute(q)]


def classify_path_origin(path: str | Path | None) -> str:
    if not path:
        return ORIGIN_UNKNOWN
    name = Path(path).name.lower()
    full = str(path).lower().replace("\\", "/")
    if any(m in name or m in full for m in SAMPLE_NAME_MARKERS):
        return ORIGIN_SAMPLE
    if "fixture" in name or "test_fixture" in full:
        return ORIGIN_FIXTURE
    return ORIGIN_UNKNOWN


def classify_url_origin(url: str | None) -> str:
    if not url:
        return ORIGIN_UNKNOWN
    u = str(url).lower()
    if any(m in u for m in SAMPLE_URL_MARKERS):
        return ORIGIN_SAMPLE
    if "goofish.com" in u or "xianyu" in u or "taobao.com" in u:
        # Platform domain alone ≠ proven REAL (058A lesson)
        return ORIGIN_UNKNOWN
    return ORIGIN_UNKNOWN


def resolve_data_origin(
    *,
    declared_origin: str | None,
    path: str | Path | None,
    url: str | None,
    collection_mode: str,
) -> tuple[str, list[str]]:
    """
    REAL only if explicitly declared AND no sample markers.
    Never promote SAMPLE to REAL because platform looks like xianyu.
    """
    reasons: list[str] = []
    path_o = classify_path_origin(path)
    url_o = classify_url_origin(url)
    if path_o in (ORIGIN_SAMPLE, ORIGIN_FIXTURE):
        return path_o, [f"path_marker:{path_o}"]
    if url_o in (ORIGIN_SAMPLE, ORIGIN_FIXTURE):
        return url_o, [f"url_marker:{url_o}"]

    declared = (declared_origin or ORIGIN_UNKNOWN).upper()
    if collection_mode == MODE_FIXTURE:
        return ORIGIN_FIXTURE, ["mode=TEST_FIXTURE"]
    if declared == ORIGIN_REAL:
        if path_o != ORIGIN_UNKNOWN or url_o == ORIGIN_SAMPLE:
            return ORIGIN_UNKNOWN, ["declared_REAL_but_markers_or_unproven"]
        # Explicit human/operator declaration for EXTERNAL_IMPORT of non-sample file
        reasons.append("declared_REAL_external_import")
        return ORIGIN_REAL, reasons
    if declared in (
        ORIGIN_SIMULATION,
        ORIGIN_SYNTHETIC,
        ORIGIN_SAMPLE,
        ORIGIN_FIXTURE,
        ORIGIN_UNKNOWN,
    ):
        return declared, [f"declared:{declared}"]
    return ORIGIN_UNKNOWN, ["unresolved"]


def make_dedupe_key(
    *,
    source: str,
    source_item_id: str | None,
    source_url: str | None,
    title: str | None,
    price: float | None,
) -> str:
    if source_item_id and str(source_item_id).strip():
        return f"item:{source}:{source_item_id.strip()}"
    if source_url and str(source_url).strip():
        return f"url:{hashlib.sha256(str(source_url).strip().encode()).hexdigest()[:24]}"
    material = f"{title or ''}|{price if price is not None else ''}"
    return f"hash:{hashlib.sha256(material.encode()).hexdigest()[:24]}"


def extract_source_item_id(url: str | None) -> str | None:
    if not url:
        return None
    # goofish/xianyu style path tail if present
    u = str(url).rstrip("/")
    if "/item/" in u:
        tail = u.split("/item/")[-1].split("?")[0].strip()
        if tail and tail.lower() not in ("sample001", "sample002", "test"):
            return tail
        if tail:
            return tail  # still return; origin layer rejects SAMPLE
    return None


def start_collection_run(
    *,
    source_id: str,
    source: str,
    platform: str,
    collection_mode: str,
    raw_reference: str | None = None,
    notes: str | None = None,
    collection_query: str | None = None,
    acquisition_mode: str | None = None,
    raw_sha256: str | None = None,
) -> str:
    ensure_market_source_schema()
    run_id = f"crun_{uuid.uuid4().hex[:12]}"
    now = _now_str()
    with database.get_connection() as conn:
        cols = [
            "run_id", "source_id", "source", "platform", "collection_mode",
            "started_at", "status", "collector_version", "normalizer_version",
            "raw_reference", "notes", "created_at",
        ]
        vals = [
            run_id,
            source_id,
            source,
            platform,
            collection_mode,
            now,
            "running",
            COLLECTOR_VERSION,
            NORMALIZER_VERSION,
            raw_reference,
            notes,
            now,
        ]
        # Optional 058D columns
        try:
            conn.execute("SELECT collection_query FROM collection_runs LIMIT 1")
            cols.extend(["collection_query", "acquisition_mode", "raw_sha256"])
            vals.extend([collection_query, acquisition_mode, raw_sha256])
        except sqlite3.OperationalError:
            pass
        placeholders = ",".join("?" * len(cols))
        conn.execute(
            f"INSERT INTO collection_runs ({','.join(cols)}) VALUES ({placeholders})",
            vals,
        )
        conn.commit()
    # Also record query in legacy collection_log (reuse, do not duplicate systems)
    try:
        log_id = database.start_collection_log(collection_query or notes or source, platform_id=1)
        # stash log_id in notes via side channel not needed — finish later optional
        _ = log_id
    except Exception:
        pass
    return run_id


def finish_collection_run(run_id: str, stats: dict, *, status: str = "done") -> None:
    with database.get_connection() as conn:
        conn.execute(
            """
            UPDATE collection_runs SET
                finished_at=?, status=?,
                raw_count=?, accepted_count=?, rejected_count=?,
                duplicate_count=?, normalized_count=?, error_count=?,
                error_summary=?
            WHERE run_id=?
            """,
            (
                _now_str(),
                status,
                int(stats.get("raw_count") or 0),
                int(stats.get("accepted_count") or 0),
                int(stats.get("rejected_count") or 0),
                int(stats.get("duplicate_count") or 0),
                int(stats.get("normalized_count") or 0),
                int(stats.get("error_count") or 0),
                stats.get("error_summary"),
                run_id,
            ),
        )
        conn.commit()


def insert_market_observation(obs: dict) -> tuple[bool, str]:
    """
    Insert observation. Same external item on different observed_at = new row (history).
    Same source+dedupe_key+observed_at = duplicate.
    """
    ensure_market_source_schema()
    observation_id = obs.get("observation_id") or f"mobs_{uuid.uuid4().hex[:12]}"
    observed_at = obs.get("observed_at") or _now_iso()
    dedupe_key = obs.get("dedupe_key") or make_dedupe_key(
        source=obs["source"],
        source_item_id=obs.get("source_item_id"),
        source_url=obs.get("source_url"),
        title=obs.get("title"),
        price=obs.get("price"),
    )
    with database.get_connection() as conn:
        existing = conn.execute(
            """
            SELECT observation_id FROM market_observations
            WHERE source=? AND dedupe_key=? AND observed_at=?
            """,
            (obs["source"], dedupe_key, observed_at),
        ).fetchone()
        if existing:
            return False, "duplicate"

        # Never write SAMPLE/FIXTURE/SIMULATION as if they were silent REAL
        origin = (obs.get("data_origin") or ORIGIN_UNKNOWN).upper()
        if origin not in (
            ORIGIN_REAL,
            ORIGIN_SIMULATION,
            ORIGIN_SYNTHETIC,
            ORIGIN_SAMPLE,
            ORIGIN_FIXTURE,
            ORIGIN_UNKNOWN,
        ):
            origin = ORIGIN_UNKNOWN

        # Hard block: SAMPLE must not be forced into Current as REAL
        if origin == ORIGIN_REAL:
            path_o = classify_path_origin(obs.get("raw_reference"))
            url_o = classify_url_origin(obs.get("source_url"))
            if path_o in (ORIGIN_SAMPLE, ORIGIN_FIXTURE) or url_o == ORIGIN_SAMPLE:
                return False, "rejected_sample_as_real"

        try:
            conn.execute(
                """
                INSERT INTO market_observations (
                    observation_id, run_id, source_id, source, platform, source_type,
                    source_item_id, source_url, title, category, price, currency,
                    view_count, want_count, comment_count, share_count,
                    seller_reference, published_at, observed_at, raw_reference,
                    data_origin, verification_status, collector_version,
                    normalizer_version, content_hash, dedupe_key,
                    product_category, opportunity_product_type, notes, created_at
                ) VALUES (
                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                )
                """,
                (
                    observation_id,
                    obs.get("run_id"),
                    obs["source_id"],
                    obs["source"],
                    obs["platform"],
                    obs.get("source_type") or "marketplace",
                    obs.get("source_item_id"),
                    obs.get("source_url"),
                    obs.get("title"),
                    obs.get("category"),
                    obs.get("price"),
                    obs.get("currency") or "CNY",
                    obs.get("view_count"),
                    obs.get("want_count"),
                    obs.get("comment_count"),
                    obs.get("share_count"),
                    obs.get("seller_reference"),
                    obs.get("published_at"),
                    observed_at,
                    obs.get("raw_reference"),
                    origin,
                    obs.get("verification_status") or "UNVERIFIED",
                    obs.get("collector_version") or COLLECTOR_VERSION,
                    obs.get("normalizer_version") or NORMALIZER_VERSION,
                    obs.get("content_hash"),
                    dedupe_key,
                    obs.get("product_category"),
                    obs.get("opportunity_product_type"),
                    obs.get("notes"),
                    _now_str(),
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return False, "duplicate"
    return True, observation_id


def assert_source_sales_independent(discovery_platform: str, sales_platform: str) -> dict:
    """Structural rule: platforms may differ; no auto-bind."""
    return {
        "discovery_platform": discovery_platform,
        "sales_platform": sales_platform,
        "auto_bound": False,
        "allowed": True,
        "note": "Discovery Source ≠ Sales Channel (DEC-029 / Entry 058B)",
    }


def live_collection_status() -> dict:
    return {
        "live_collection_available": LIVE_COLLECTION_AVAILABLE,
        "mode_if_xianyu": MODE_IMPORT,
        "reason": LIVE_COLLECTION_REASON,
        "forbidden": [
            "captcha_bypass",
            "login_bypass",
            "anti_bot_evasion",
            "unauthorized_account_automation",
            "api_cracking",
        ],
    }


def count_observations(*, data_origin: str | None = None) -> int:
    ensure_market_source_schema()
    with database.get_connection() as conn:
        if data_origin:
            row = conn.execute(
                "SELECT COUNT(*) AS c FROM market_observations WHERE data_origin=?",
                (data_origin,),
            ).fetchone()
        else:
            row = conn.execute("SELECT COUNT(*) AS c FROM market_observations").fetchone()
    return int(row["c"] if row and "c" in row.keys() else row[0])


def delete_observations_for_run(run_id: str) -> int:
    """Batch rollback helper — remove all observations written for a failed run."""
    ensure_market_source_schema()
    with database.get_connection() as conn:
        cur = conn.execute(
            "DELETE FROM market_observations WHERE run_id=?",
            (run_id,),
        )
        conn.commit()
        return int(cur.rowcount or 0)


def verification_for_origin(origin: str, *, operator_attested: bool = False) -> str:
    """
    User-provided export may be MANUAL_VERIFIED when operator attests REAL.
    Never auto-set platform-official VERIFIED.
    """
    o = (origin or ORIGIN_UNKNOWN).upper()
    if o == ORIGIN_REAL and operator_attested:
        return VERIF_MANUAL
    if o == ORIGIN_REAL:
        return VERIF_MANUAL  # EXTERNAL_IMPORT REAL = operator declaration only
    if o in (ORIGIN_SAMPLE, ORIGIN_FIXTURE, ORIGIN_SIMULATION):
        return VERIF_REVIEW
    return VERIF_UNVERIFIED
