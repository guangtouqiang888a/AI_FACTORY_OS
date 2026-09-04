# 1_DATA/acquisition_engine.py — Entry 059 Autonomous Market Acquisition Engine
#
# User Policy → Acquisition Engine → Source Adapter → Raw → Normalize → Observation
#
# Engine MUST NOT contain Xianyu HTML/CSS/URL details.
# Discovery Source ≠ Sales Platform ≠ Product ≠ Feedback Source
# Collector records facts only — never "爆款" / business model judgments.
# Cursor = engineering tool ≠ product-generation AI in architecture.
# No fake market data. No Archive read for Current acquisition.

from __future__ import annotations

import json
import sqlite3
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import acquisition_capability as acq  # noqa: E402
import collector_abstraction as cab  # noqa: E402
import config  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
import product_origin as po  # noqa: E402

ENGINE_VERSION = "067.1.0"

# --- Market Acquisition Goals (Entry 067; closed set) ---
GOAL_VOLUME = "VOLUME_DISCOVERY"
GOAL_HIGH_VALUE = "HIGH_VALUE_DISCOVERY"
GOAL_MARKET_GAP = "MARKET_GAP_DISCOVERY"
GOAL_TREND = "TREND_DISCOVERY"
GOAL_TARGETED = "TARGETED_RESEARCH"

ACQUISITION_GOALS = frozenset(
    {
        GOAL_VOLUME,
        GOAL_HIGH_VALUE,
        GOAL_MARKET_GAP,
        GOAL_TREND,
        GOAL_TARGETED,
    }
)

FILTER_MATCH = "MATCH"
FILTER_BELOW = "BELOW_THRESHOLD"
FILTER_ABOVE = "ABOVE_THRESHOLD"
FILTER_UNKNOWN = "UNKNOWN"

# --- Scan strategies (extensible; v1 implements KEYWORD_SEARCH only) ---
SCAN_KEYWORD = "KEYWORD_SEARCH"
SCAN_CATEGORY = "CATEGORY_SCAN"
SCAN_PRICE = "PRICE_SCAN"
SCAN_TREND = "TREND_SCAN"
SCAN_COMPETITOR = "COMPETITOR_SCAN"
SCAN_DEMAND = "DEMAND_SCAN"
SCAN_CUSTOM = "CUSTOM"

SCAN_STRATEGIES = frozenset(
    {
        SCAN_KEYWORD,
        SCAN_CATEGORY,
        SCAN_PRICE,
        SCAN_TREND,
        SCAN_COMPETITOR,
        SCAN_DEMAND,
        SCAN_CUSTOM,
    }
)

# --- Schedules (extensible; v1 MANUAL only) ---
SCHED_MANUAL = "MANUAL"
SCHED_DAILY = "DAILY"
SCHED_INTERVAL = "INTERVAL"
SCHED_EVENT = "EVENT_TRIGGERED"
SCHED_AI = "AI_SCHEDULED"

SCHEDULES = frozenset(
    {SCHED_MANUAL, SCHED_DAILY, SCHED_INTERVAL, SCHED_EVENT, SCHED_AI}
)

TASK_DRAFT = "DRAFT"
TASK_READY = "READY"
TASK_RUNNING = "RUNNING"
TASK_DONE = "DONE"
TASK_FAILED = "FAILED"
TASK_WAITING = "WAITING_FOR_REAL_SOURCE"
TASK_PARTIAL = "PARTIAL"


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_acquisition_engine_schema() -> None:
    msc.ensure_market_source_schema()
    with database.get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS acquisition_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE NOT NULL,
                source_id TEXT NOT NULL,
                market_region TEXT NOT NULL DEFAULT 'CN',
                query TEXT NOT NULL,
                scan_strategy TEXT NOT NULL,
                schedule TEXT NOT NULL DEFAULT 'MANUAL',
                max_records INTEGER,
                data_requirements TEXT,
                acquisition_mode TEXT,
                status TEXT NOT NULL,
                declared_origin TEXT,
                last_run_id TEXT,
                last_result_summary TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                last_run_at TEXT
            );
            CREATE TABLE IF NOT EXISTS acquisition_policy (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                allowed_sources TEXT NOT NULL,
                allowed_regions TEXT NOT NULL,
                allowed_frequency TEXT,
                max_requests INTEGER,
                max_records_per_run INTEGER,
                compliance_policy TEXT,
                automation_enabled INTEGER NOT NULL DEFAULT 0,
                ui_settings_json TEXT,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS market_acquisition_policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                policy_id TEXT UNIQUE NOT NULL,
                goal TEXT NOT NULL,
                source_preferences TEXT,
                query_strategy TEXT,
                scope_json TEXT,
                filters_json TEXT,
                budget_json TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
        # seed default policy once
        row = conn.execute("SELECT id FROM acquisition_policy WHERE id=1").fetchone()
        if not row:
            conn.execute(
                """
                INSERT INTO acquisition_policy (
                    id, allowed_sources, allowed_regions, allowed_frequency,
                    max_requests, max_records_per_run, compliance_policy,
                    automation_enabled, ui_settings_json, updated_at
                ) VALUES (1, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                """,
                (
                    json.dumps(["src_xianyu_marketplace"]),
                    json.dumps(["CN"]),
                    SCHED_MANUAL,
                    100,
                    100,
                    "no_bypass;no_login_automation;no_fake_data;no_archive_as_current",
                    json.dumps(default_ui_settings()),
                    _now(),
                ),
            )
            conn.commit()
        # Additive columns on acquisition_tasks (Entry 067)
        for ddl in (
            "ALTER TABLE acquisition_tasks ADD COLUMN policy_id TEXT",
            "ALTER TABLE acquisition_tasks ADD COLUMN filters_json TEXT",
        ):
            try:
                conn.execute(ddl)
                conn.commit()
            except sqlite3.OperationalError:
                pass
    _refresh_collector_capabilities()


def default_ui_settings() -> dict:
    """Future software UI readiness — settings shape only, no UI built."""
    return {
        "market_sources": True,
        "collection_schedule": True,
        "query_scope": True,
        "region": True,
        "max_collection_budget": True,
        "risk_level": True,
        "data_quality_threshold": True,
        "automation_enabled": True,
        "user_sets": "boundaries_only",
        "system_decides": "how_to_collect",
        "cursor_role": "engineering_not_product_ai",
        "model_router": "PROPOSED_NOT_BUILT",
    }


def get_policy() -> dict:
    ensure_acquisition_engine_schema()
    with database.get_connection() as conn:
        row = conn.execute("SELECT * FROM acquisition_policy WHERE id=1").fetchone()
    d = dict(row)
    for k in ("allowed_sources", "allowed_regions", "ui_settings_json"):
        if d.get(k):
            try:
                d[k] = json.loads(d[k])
            except json.JSONDecodeError:
                pass
    return d


def update_policy(**kwargs) -> dict:
    ensure_acquisition_engine_schema()
    policy = get_policy()
    mapping = {
        "allowed_sources": "allowed_sources",
        "allowed_regions": "allowed_regions",
        "allowed_frequency": "allowed_frequency",
        "max_requests": "max_requests",
        "max_records_per_run": "max_records_per_run",
        "compliance_policy": "compliance_policy",
        "automation_enabled": "automation_enabled",
        "ui_settings_json": "ui_settings_json",
    }
    with database.get_connection() as conn:
        for key, col in mapping.items():
            if key not in kwargs:
                continue
            val = kwargs[key]
            if key in ("allowed_sources", "allowed_regions", "ui_settings_json") and not isinstance(
                val, str
            ):
                val = json.dumps(val, ensure_ascii=False)
            conn.execute(
                f"UPDATE acquisition_policy SET {col}=?, updated_at=? WHERE id=1",
                (val, _now()),
            )
        conn.commit()
    return get_policy()


def _refresh_collector_capabilities() -> None:
    """Document honest mode status on collectors registry."""
    msc.ensure_collector_registry()
    now = _now()
    caps = [
        {
            "collector_id": "col_xianyu_import",
            "source_id": "src_xianyu_marketplace",
            "mode": "MANUAL_IMPORT",
            "version": ENGINE_VERSION,
            "status": "ACTIVE",
            "notes": json.dumps(
                {
                    "supported_modes": ["USER_EXPORT", "MANUAL_IMPORT"],
                    "public_web_read": "LIMITED",
                    "live_api": "NOT_AVAILABLE_CURRENTLY",
                    "priority_fields": [
                        "title",
                        "price",
                        "want_count",
                        "source_url",
                        "source_item_id",
                        "observed_at",
                    ],
                    "field_availability": acq.field_availability_matrix(),
                },
                ensure_ascii=False,
            ),
        },
        {
            "collector_id": "col_xianyu_live_api",
            "source_id": "src_xianyu_marketplace",
            "mode": "LIVE_API",
            "version": ENGINE_VERSION,
            "status": "NOT_AVAILABLE_CURRENTLY",
            "notes": "No project eligibility (058D/059)",
        },
        {
            "collector_id": "col_xianyu_public_web",
            "source_id": "src_xianyu_marketplace",
            "mode": "PUBLIC_WEB_READ",
            "version": ENGINE_VERSION,
            "status": "LIMITED",  # 060: adapter present; ACTIVE only after successful live run
            "notes": "Entry 060 browser adapter; chrome headless dump-dom / optional selenium|playwright; headless may hit ACCESS_DENIED",
        },
        {
            "collector_id": "col_xianyu_browser",
            "source_id": "src_xianyu_marketplace",
            "mode": "PUBLIC_WEB_READ",
            "version": "060.1.0",
            "status": "LIMITED",
            "notes": "Headless dump-dom = ACCESS_DENIED (060); interactive path = col_xianyu_browser_interactive",
        },
        {
            "collector_id": "col_xianyu_browser_interactive",
            "source_id": "src_xianyu_marketplace",
            "mode": "PUBLIC_WEB_READ",
            "version": "061.1.0",
            "status": "LIMITED",
            "notes": (
                "Entry 061 interactive visible Chrome+CDP; title/price/url OK; "
                "want_count PARTIAL; first-pass test-dir only; no Current DB auto-write"
            ),
        },
        {
            "collector_id": "col_xianyu_targeted_search",
            "source_id": "src_xianyu_marketplace",
            "mode": "PUBLIC_WEB_READ",
            "version": "062.1.0",
            "status": "LIMITED",
            "notes": (
                "Entry 062: SEARCH_RESULT vs RECOMMENDED; want_count status model; "
                "anonymous interactive session got empty primary search across tested queries"
            ),
        },
        {
            "collector_id": "col_xianyu_search_session",
            "source_id": "src_xianyu_marketplace",
            "mode": "PUBLIC_WEB_READ",
            "version": "063.1.0",
            "status": "LIMITED",
            "notes": (
                "Entry 063: SearchSession + Control vs Collect split; "
                "SEARCH_CONTROL_NOT_FEASIBLE (empty primary); "
                "Collector feasible when SEARCH_RESULT DOM present"
            ),
        },
        {
            "collector_id": "col_xianyu_browser_extension",
            "source_id": "src_xianyu_marketplace",
            "mode": "BROWSER_EXTENSION",
            "version": "065.1.0",
            "status": "LIMITED",
            "notes": (
                "Entry 065: MV3 Extension + Localhost Bridge; DOM-only; "
                "MarketRecord v064.1.0; test-dir sink first; no Current DB auto-write"
            ),
        },
    ]
    with database.get_connection() as conn:
        for r in caps:
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
        conn.commit()


def create_collection_task(
    *,
    source_id: str = "src_xianyu_marketplace",
    query: str,
    market_region: str = "CN",
    scan_strategy: str = SCAN_KEYWORD,
    schedule: str = SCHED_MANUAL,
    max_records: int | None = 100,
    data_requirements: dict | None = None,
    acquisition_mode: str = acq.MODE_MANUAL_IMPORT,
    declared_origin: str = msc.ORIGIN_UNKNOWN,
    notes: str | None = None,
    policy_id: str | None = None,
    filters: dict | None = None,
) -> dict:
    """Create AcquisitionTask. query is a parameter — never hardcode as platform."""
    ensure_acquisition_engine_schema()
    if not query or not str(query).strip():
        raise ValueError("query_required")
    if query.strip().lower() in ("xianyu", "taobao", "source"):
        raise ValueError("query_must_not_equal_source_platform")
    if scan_strategy not in SCAN_STRATEGIES:
        raise ValueError(f"unknown_scan_strategy:{scan_strategy}")
    if schedule not in SCHEDULES:
        raise ValueError(f"unknown_schedule:{schedule}")
    if scan_strategy != SCAN_KEYWORD:
        # v1: only KEYWORD_SEARCH executable; others may be created as DRAFT/PROPOSED
        status = TASK_DRAFT
        note_extra = "scan_strategy_not_implemented_v1"
    else:
        status = TASK_READY
        note_extra = None

    policy = get_policy()
    allowed = policy.get("allowed_sources") or []
    if isinstance(allowed, str):
        allowed = json.loads(allowed)
    if source_id not in allowed:
        raise ValueError(f"source_not_allowed_by_policy:{source_id}")
    regions = policy.get("allowed_regions") or ["CN"]
    if isinstance(regions, str):
        regions = json.loads(regions)
    if market_region not in regions:
        raise ValueError(f"region_not_allowed_by_policy:{market_region}")

    market_policy = None
    if policy_id:
        market_policy = get_market_acquisition_policy(policy_id)
        # Prefer policy filters when task filters omitted
        if filters is None and market_policy.get("filters"):
            filters = dict(market_policy["filters"])
        scope = market_policy.get("scope") or {}
        if max_records is None and scope.get("max_records") is not None:
            max_records = int(scope["max_records"])

    # Mode honesty at create-time (execute may still probe browser for PUBLIC_WEB_READ)
    if acquisition_mode == acq.MODE_LIVE_API:
        status = TASK_FAILED
        note_extra = "live_api_not_available_currently"
    if acquisition_mode == "PUBLIC_WEB_READ":
        # Entry 060: attempt browser adapter; do not pre-fail as NOT_FEASIBLE forever
        status = TASK_READY if scan_strategy == SCAN_KEYWORD else TASK_DRAFT
        note_extra = "public_web_read_browser_v1"

    task_id = f"atask_{uuid.uuid4().hex[:12]}"
    now = _now()
    req = json.dumps(data_requirements or {"priority_fields": ["title", "price", "want_count"]}, ensure_ascii=False)
    filters_json = json.dumps(normalize_filters(filters), ensure_ascii=False) if filters is not None else None
    notes_blob = json.dumps(
        {
            "user_notes": notes,
            "engine_note": note_extra,
            "sales_platform_not_implied": True,
            "own_product_principle": True,
            "cursor_not_product_ai": True,
            "policy_id": policy_id,
            "goal": (market_policy or {}).get("goal"),
        },
        ensure_ascii=False,
    )
    with database.get_connection() as conn:
        cols = [
            "task_id", "source_id", "market_region", "query", "scan_strategy", "schedule",
            "max_records", "data_requirements", "acquisition_mode", "status",
            "declared_origin", "notes", "created_at", "updated_at",
        ]
        vals: list[Any] = [
            task_id,
            source_id,
            market_region,
            query.strip(),
            scan_strategy,
            schedule,
            max_records,
            req,
            acquisition_mode,
            status,
            declared_origin,
            notes_blob,
            now,
            now,
        ]
        # Optional 067 columns
        try:
            conn.execute("SELECT policy_id FROM acquisition_tasks LIMIT 1")
            cols.extend(["policy_id", "filters_json"])
            vals.extend([policy_id, filters_json])
        except sqlite3.OperationalError:
            pass
        placeholders = ",".join("?" * len(cols))
        conn.execute(
            f"INSERT INTO acquisition_tasks ({','.join(cols)}) VALUES ({placeholders})",
            vals,
        )
        conn.commit()
    return get_task(task_id)


def get_task(task_id: str) -> dict:
    ensure_acquisition_engine_schema()
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM acquisition_tasks WHERE task_id=?", (task_id,)
        ).fetchone()
    if not row:
        raise KeyError(task_id)
    return dict(row)


def list_tasks(*, source_id: str | None = None) -> list[dict]:
    ensure_acquisition_engine_schema()
    with database.get_connection() as conn:
        if source_id:
            rows = conn.execute(
                "SELECT * FROM acquisition_tasks WHERE source_id=? ORDER BY created_at DESC",
                (source_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM acquisition_tasks ORDER BY created_at DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def select_source(task: dict) -> str:
    return task["source_id"]


def select_query(task: dict) -> str:
    """Query is task parameter; future AI Query Planner can replace this."""
    return task["query"]


def _mode_for_execute(task: dict) -> str:
    mode = task.get("acquisition_mode") or acq.MODE_MANUAL_IMPORT
    if mode == "PUBLIC_WEB_READ":
        return mode
    if mode == acq.MODE_LIVE_API:
        return mode
    if mode in (acq.MODE_USER_EXPORT, acq.MODE_MANUAL_IMPORT, msc.MODE_IMPORT, "EXTERNAL_IMPORT"):
        return acq.MODE_MANUAL_IMPORT
    return mode


def execute_collection(task_id: str) -> dict:
    """
    Run AcquisitionTask via Source Adapter.
    Does NOT score opportunities, generate products, or write commercial learning.
    """
    ensure_acquisition_engine_schema()
    task = get_task(task_id)
    if task["status"] in (TASK_FAILED,) and "not_available" in (task.get("notes") or ""):
        pass

    mode = _mode_for_execute(task)
    if mode == acq.MODE_LIVE_API:
        result = cab.run_acquisition(
            acquisition_mode=acq.MODE_LIVE_API,
            collection_query=select_query(task),
            declared_origin=task.get("declared_origin") or msc.ORIGIN_UNKNOWN,
        )
        _finish_task(task_id, TASK_FAILED, result)
        return _engine_result(task, result, status=TASK_FAILED)

    if mode == "PUBLIC_WEB_READ":
        _set_task_status(task_id, TASK_RUNNING)
        result = cab.run_acquisition(
            acquisition_mode="PUBLIC_WEB_READ",
            collection_query=select_query(task),
            declared_origin=task.get("declared_origin") or msc.ORIGIN_REAL,
        )
        # Normalize adapter counts into engine valid/total
        stats = result.get("stats") or {}
        result["total"] = int(stats.get("raw_count") or 0)
        result["valid"] = int(stats.get("accepted_count") or 0)
        if result.get("status") == "BLOCKED_BY_ACCESS_CONTROL":
            status = TASK_FAILED
        elif result.get("error") == "DEPENDENCY_MISSING":
            status = TASK_FAILED
        elif result.get("ok") and result.get("valid", 0) > 0:
            status = TASK_DONE
        elif result.get("status") in ("NO_LISTING_PAYLOAD", "NO_LISTING_ACCEPTED"):
            status = TASK_FAILED
        else:
            status = TASK_PARTIAL if result.get("valid") else TASK_FAILED
        _finish_task(task_id, status, result)
        out = _engine_result(task, result, status=status)
        if result.get("error") == "DEPENDENCY_MISSING":
            out["entry_status"] = "BLOCKED_DEPENDENCY_MISSING"
        elif result.get("status") == "BLOCKED_BY_ACCESS_CONTROL":
            out["entry_status"] = "BLOCKED_BY_ACCESS_CONTROL"
        elif result.get("ok"):
            out["entry_status"] = "FIRST_REAL_BATCH_OK" if result["valid"] else "PARTIAL"
            out["first_real_xianyu_market_batch"] = result["valid"] > 0
        else:
            out["entry_status"] = result.get("status") or "FAILED"
            out["first_real_xianyu_market_batch"] = False
        return out

    if task.get("scan_strategy") != SCAN_KEYWORD:
        result = {
            "ok": False,
            "status": "FAILED",
            "error": "scan_strategy_not_implemented_v1",
            "scan_strategy": task.get("scan_strategy"),
        }
        _finish_task(task_id, TASK_FAILED, result)
        return _engine_result(task, result, status=TASK_FAILED)

    if task.get("schedule") not in (SCHED_MANUAL, None, ""):
        # Non-manual schedules are designed but not auto-run in v1
        if task.get("schedule") != SCHED_MANUAL:
            result = {
                "ok": False,
                "status": "FAILED",
                "error": "schedule_not_implemented_use_manual",
                "schedule": task.get("schedule"),
            }
            _finish_task(task_id, TASK_FAILED, result)
            return _engine_result(task, result, status=TASK_FAILED)

    _set_task_status(task_id, TASK_RUNNING)
    result = cab.run_acquisition(
        acquisition_mode=acq.MODE_MANUAL_IMPORT,
        collection_query=select_query(task),
        declared_origin=task.get("declared_origin") or msc.ORIGIN_UNKNOWN,
    )

    if result.get("error") == "no_import_files" or result.get("status") in (
        "WAITING_FOR_REAL_SOURCE_FILE",
        "WAITING_OR_ZERO_ACCEPTED",
    ):
        status = TASK_WAITING
        _finish_task(task_id, status, result)
        out = _engine_result(task, result, status=status)
        out["entry_status"] = "WAITING_FOR_REAL_SOURCE"
        out["ready_for_real_collection"] = True
        return out

    if result.get("ok"):
        status = TASK_DONE if int(result.get("valid") or 0) > 0 else TASK_PARTIAL
    else:
        status = TASK_FAILED
    _finish_task(task_id, status, result)
    return _engine_result(task, result, status=status)


def _set_task_status(task_id: str, status: str) -> None:
    with database.get_connection() as conn:
        conn.execute(
            "UPDATE acquisition_tasks SET status=?, updated_at=? WHERE task_id=?",
            (status, _now(), task_id),
        )
        conn.commit()


def _finish_task(task_id: str, status: str, result: dict) -> None:
    run_id = None
    runs = result.get("runs") or []
    if runs and isinstance(runs[0], dict):
        run_id = runs[0].get("run_id")
    elif result.get("run_id"):
        run_id = result.get("run_id")
    summary = json.dumps(
        {
            "ok": result.get("ok"),
            "status": result.get("status"),
            "error": result.get("error"),
            "total": result.get("total"),
            "valid": result.get("valid"),
            "acquisition_mode": result.get("acquisition_mode"),
            "sales_platform": None,
        },
        ensure_ascii=False,
    )
    with database.get_connection() as conn:
        conn.execute(
            """
            UPDATE acquisition_tasks SET
                status=?, last_run_id=?, last_result_summary=?,
                last_run_at=?, updated_at=?
            WHERE task_id=?
            """,
            (status, run_id, summary, _now(), _now(), task_id),
        )
        conn.commit()


def _engine_result(task: dict, adapter_result: dict, *, status: str) -> dict:
    return {
        "engine_version": ENGINE_VERSION,
        "task_id": task["task_id"],
        "source_id": task["source_id"],
        "query": task["query"],
        "scan_strategy": task["scan_strategy"],
        "market_region": task["market_region"],
        "status": status,
        "discovery_platform": "xianyu"
        if "xianyu" in task["source_id"]
        else task["source_id"],
        "sales_platform": None,
        "product_created": False,
        "listing_created": False,
        "market_event_created": False,
        "opportunity_scored": False,
        "commercial_learning": False,
        "own_product_principle": po.OWN_PRODUCT_PRINCIPLE_ZH,
        "adapter_result": adapter_result,
        "architecture": {
            "cursor_role": "engineering_not_product_ai",
            "model_router": "PROPOSED_NOT_BUILT",
            "learning_to_acquisition": "RESERVED_NOT_BUILT",
            "ai_query_planner": "RESERVED_NOT_BUILT",
        },
    }


def engine_status() -> dict:
    ensure_acquisition_engine_schema()
    policy = get_policy()
    collectors = msc.list_collectors()
    from connectors.xianyu_import_connector import import_readiness

    ready = import_readiness()
    return {
        "engine_version": ENGINE_VERSION,
        "status": "PARTIAL_IMPLEMENTED",
        "policy": {
            "allowed_sources": policy.get("allowed_sources"),
            "allowed_regions": policy.get("allowed_regions"),
            "automation_enabled": policy.get("automation_enabled"),
        },
        "xianyu_modes": {
            "USER_EXPORT": "AVAILABLE",
            "MANUAL_IMPORT": "AVAILABLE",
            "PUBLIC_WEB_READ": "LIMITED",  # browser adapter exists; deps/runtime may block
            "LIVE_API": "NOT_AVAILABLE_CURRENTLY",
        },
        "collectors": [
            {"collector_id": c["collector_id"], "mode": c["mode"], "status": c["status"]}
            for c in collectors
        ],
        "import_readiness": ready,
        "current_observations": msc.count_observations(),
        "tasks": len(list_tasks()),
        "ui_readiness": default_ui_settings(),
        "separations": {
            "source_neq_sales": True,
            "observation_neq_product": True,
            "product_type_neq_business_model": True,
            "cursor_neq_product_ai": True,
        },
    }


def reality_chain() -> dict[str, str]:
    return {
        "User Policy": "PARTIAL",
        "Acquisition Policy": "PARTIAL",
        "Acquisition Engine": "PARTIAL",
        "Source Strategy": "PARTIAL",
        "Xianyu Adapter": "REALITY",
        "Raw": "REALITY",
        "Normalizer": "REALITY",
        "MarketObservation": "REALITY",
        "Filter Layer": "PARTIAL",
        "MarketSignal": "PARTIAL",
        "Opportunity": "PARTIAL",
        "AI Cost Gate": "PARTIAL",
        "Product": "REALITY",
        "Listing": "REALITY",
        "Sales Platform": "REALITY",
        "Market Event": "REALITY",
        "Evaluation": "MISSING",
        "Learning": "PARTIAL",
        "Acquisition Strategy feedback": "PROPOSED",
    }


# =============================================================================
# Market Acquisition Policy (Entry 067)
# Goal-oriented policy objects — distinct from singleton compliance get_policy().
# Policy = why/how to acquire; Source = where (xianyu/taobao/…). Not bound 1:1.
# =============================================================================


def strategy_registry() -> dict[str, dict[str, Any]]:
    """Closed set of acquisition goals — do not invent open-ended modes."""
    return {
        GOAL_VOLUME: {
            "description": "Discover high-volume / engagement candidates",
            "typical_filters": {"min_want_count": 50, "max_price": 20},
            "requires_want_count": False,
            "notes": "Collector still retains NULL want; Filter classifies UNKNOWN",
        },
        GOAL_HIGH_VALUE: {
            "description": "Discover higher-price / higher-value candidates",
            "typical_filters": {"min_price": 50},
            "requires_want_count": False,
            "notes": "want_count optional",
        },
        GOAL_MARKET_GAP: {
            "description": "Reserve for demand/competition/quality gap analysis",
            "typical_filters": {},
            "requires_want_count": False,
            "status": "RESERVED",
        },
        GOAL_TREND: {
            "description": "Reserve for trend-oriented discovery",
            "typical_filters": {},
            "requires_want_count": False,
            "status": "RESERVED",
        },
        GOAL_TARGETED: {
            "description": "User-specified query research",
            "typical_filters": {},
            "requires_want_count": False,
            "notes": "Query provided by user; system executes collection",
        },
    }


def normalize_filters(filters: dict | None) -> dict[str, Any]:
    """Optional filters only — never coerced into Collector hard gates."""
    f = filters or {}
    out: dict[str, Any] = {
        "min_want_count": None,
        "min_price": None,
        "max_price": None,
    }
    for key in out:
        if key in f and f[key] is not None and f[key] != "":
            try:
                out[key] = float(f[key]) if "price" in key else int(f[key])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid_filter:{key}") from exc
    return out


def create_market_acquisition_policy(
    *,
    goal: str,
    source_preferences: list[str] | None = None,
    query_strategy: str = "USER_CONFIGURED",
    scope: dict | None = None,
    filters: dict | None = None,
    budget: dict | None = None,
    notes: str | None = None,
    policy_id: str | None = None,
) -> dict:
    """
    Create AcquisitionPolicy object.
    goal ≠ source. Same policy may later target xianyu / taobao / overseas.
    """
    ensure_acquisition_engine_schema()
    if goal not in ACQUISITION_GOALS:
        raise ValueError(f"unknown_goal:{goal}")
    pid = policy_id or f"apol_{uuid.uuid4().hex[:12]}"
    now = _now()
    scope = scope or {"max_records": 20, "max_pages": 1, "max_runs_per_day": None}
    budget = budget or {
        "max_records": scope.get("max_records"),
        "max_pages": scope.get("max_pages"),
        "max_runs_per_day": scope.get("max_runs_per_day"),
    }
    prefs = source_preferences or ["src_xianyu_marketplace"]
    with database.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO market_acquisition_policies (
                policy_id, goal, source_preferences, query_strategy,
                scope_json, filters_json, budget_json, notes, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pid,
                goal,
                json.dumps(prefs, ensure_ascii=False),
                query_strategy,
                json.dumps(scope, ensure_ascii=False),
                json.dumps(normalize_filters(filters), ensure_ascii=False),
                json.dumps(budget, ensure_ascii=False),
                notes,
                now,
                now,
            ),
        )
        conn.commit()
    return get_market_acquisition_policy(pid)


def get_market_acquisition_policy(policy_id: str) -> dict:
    ensure_acquisition_engine_schema()
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM market_acquisition_policies WHERE policy_id=?",
            (policy_id,),
        ).fetchone()
    if not row:
        raise KeyError(policy_id)
    d = dict(row)
    for k, out_k in (
        ("source_preferences", "source_preferences"),
        ("scope_json", "scope"),
        ("filters_json", "filters"),
        ("budget_json", "budget"),
    ):
        raw = d.get(k)
        if raw:
            try:
                d[out_k] = json.loads(raw)
            except json.JSONDecodeError:
                d[out_k] = raw
        elif out_k not in d:
            d[out_k] = None
    return d


def list_market_acquisition_policies() -> list[dict]:
    ensure_acquisition_engine_schema()
    with database.get_connection() as conn:
        rows = conn.execute(
            "SELECT policy_id FROM market_acquisition_policies ORDER BY created_at DESC"
        ).fetchall()
    return [get_market_acquisition_policy(r[0] if not hasattr(r, "keys") else r["policy_id"]) for r in rows]


def apply_observation_filters(
    observations: list[dict],
    filters: dict | None,
) -> dict[str, Any]:
    """
    Filter Layer — NOT Collector.
    NULL want_count → UNKNOWN (never coerce to 0).
    Observations are never discarded from the input list semantics:
    returned buckets keep all rows classified.
    """
    f = normalize_filters(filters)
    match: list[dict] = []
    below: list[dict] = []
    above: list[dict] = []
    unknown: list[dict] = []
    classified: list[dict] = []

    for obs in observations:
        row = dict(obs)
        want = obs.get("want_count")
        price = obs.get("price")
        statuses: list[str] = []

        # want_count filter
        if f["min_want_count"] is not None:
            if want is None:
                statuses.append(FILTER_UNKNOWN)
            elif int(want) >= int(f["min_want_count"]):
                statuses.append(FILTER_MATCH)
            else:
                statuses.append(FILTER_BELOW)

        # price filters
        if f["min_price"] is not None:
            if price is None:
                statuses.append(FILTER_UNKNOWN)
            elif float(price) >= float(f["min_price"]):
                statuses.append(FILTER_MATCH)
            else:
                statuses.append(FILTER_BELOW)

        if f["max_price"] is not None:
            if price is None:
                statuses.append(FILTER_UNKNOWN)
            elif float(price) <= float(f["max_price"]):
                statuses.append(FILTER_MATCH)
            else:
                statuses.append(FILTER_ABOVE)

        if not statuses:
            overall = FILTER_MATCH  # no filters active
        elif FILTER_UNKNOWN in statuses:
            overall = FILTER_UNKNOWN
        elif FILTER_BELOW in statuses or FILTER_ABOVE in statuses:
            overall = FILTER_BELOW if FILTER_BELOW in statuses else FILTER_ABOVE
        else:
            overall = FILTER_MATCH

        row["filter_status"] = overall
        classified.append(row)
        if overall == FILTER_MATCH:
            match.append(row)
        elif overall == FILTER_UNKNOWN:
            unknown.append(row)
        elif overall == FILTER_ABOVE:
            above.append(row)
        else:
            below.append(row)

    return {
        "filters": f,
        "total": len(observations),
        "MATCH": match,
        "BELOW_THRESHOLD": below,
        "ABOVE_THRESHOLD": above,
        "UNKNOWN": unknown,
        "classified": classified,
        "counts": {
            "MATCH": len(match),
            "BELOW_THRESHOLD": len(below),
            "ABOVE_THRESHOLD": len(above),
            "UNKNOWN": len(unknown),
        },
        "note": "Collector retains all facts; Filter only classifies. NULL≠0.",
    }


def example_policies() -> list[dict]:
    """Documentation helpers — not auto-seeded into DB."""
    return [
        {
            "goal": GOAL_VOLUME,
            "source_preferences": ["src_xianyu_marketplace"],
            "filters": {"min_want_count": 50, "max_price": 20},
        },
        {
            "goal": GOAL_HIGH_VALUE,
            "source_preferences": ["src_xianyu_marketplace"],
            "filters": {"min_price": 50},
        },
        {
            "goal": GOAL_MARKET_GAP,
            "source_preferences": ["src_xianyu_marketplace"],
            "filters": {},
            "status": "RESERVED",
        },
        {
            "goal": GOAL_TREND,
            "source_preferences": ["src_xianyu_marketplace"],
            "filters": {},
            "status": "RESERVED",
        },
        {
            "goal": GOAL_TARGETED,
            "source_preferences": ["src_xianyu_marketplace"],
            "filters": {},
            "query_strategy": "USER_CONFIGURED",
        },
    ]
