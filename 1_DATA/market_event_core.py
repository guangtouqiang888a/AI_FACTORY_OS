# 1_DATA/market_event_core.py — Market Event & Commercial Observation Pipeline
# Entry 051 — 最小可扩展真实市场事件回流基础设施
#
# 原则：
#   Market Event ≠ Observation Conclusion ≠ Commercial Success
#   REAL/SIMULATION 隔离（延续 Entry 050）
#   Platform ≠ Core Product Model（无 taobao_product / xianyu_product 表）
#   不伪造 Pilot 观察数据；本模块是接收能力，不是启动观察

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "7_MEMORY"))

import config  # noqa: E402
import database  # noqa: E402

# ---------------------------------------------------------------------------
# Ontology constants
# ---------------------------------------------------------------------------

EVENT_TYPES = frozenset({
    "VIEW", "CLICK", "FAVORITE", "INQUIRY", "SHARE",
    "PURCHASE", "REFUND", "REVIEW", "REVENUE", "COST",
    "WATCH_TIME", "COMPLETION", "RETENTION",
    "CONVERSION", "PROFIT",
})

COMMERCIAL_LEARNING_EVENT_TYPES = frozenset({
    "PURCHASE", "REVENUE", "REFUND", "CONVERSION", "PROFIT",
})

MARKET_OBSERVATION_EVENT_TYPES = frozenset(EVENT_TYPES)

DATA_ORIGIN_REAL = "REAL"
DATA_ORIGIN_SIMULATION = "SIMULATION"
DATA_ORIGIN_SYNTHETIC = "SYNTHETIC"
DATA_ORIGIN_UNKNOWN = "UNKNOWN"

VERIFICATION_UNVERIFIED = "UNVERIFIED"
VERIFICATION_VERIFIED = "VERIFIED"
VERIFICATION_MANUAL = "MANUAL_VERIFIED"

LINKAGE_RESOLVED = "RESOLVED"
LINKAGE_UNRESOLVED = "UNRESOLVED"

OBSERVATIONS_JSON = (
    ROOT / "commercial_assets" / "observations" / "observations_v1.json"
)


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_market_event_schema() -> None:
    """
    最小 Market Event 表 — 平台无关、产品类型无关。
    新增平台 → platforms.name + Connector；不改本表结构。
    新增产品类型 → product_type 文本字段；不改本表结构。
    """
    # 仅确保 platforms 存在（不递归调用 database.ensure_schema 全量）
    with database.get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS platforms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
            """
        )
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS market_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                event_type TEXT NOT NULL,
                source TEXT,
                platform TEXT,
                event_timestamp TEXT,
                product_id TEXT,
                product_asset_id TEXT,
                product_type TEXT,
                experiment_id TEXT,
                listing_id TEXT,
                value REAL,
                currency TEXT,
                data_origin TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                verified_source TEXT,
                raw_reference TEXT,
                dedupe_key TEXT UNIQUE,
                linkage_status TEXT,
                linkage_notes TEXT,
                raw_payload TEXT,
                ingested_at TEXT NOT NULL,
                learning_routed INTEGER DEFAULT 0,
                learning_result TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_market_events_origin
                ON market_events(data_origin);
            CREATE INDEX IF NOT EXISTS idx_market_events_type
                ON market_events(event_type);
            CREATE INDEX IF NOT EXISTS idx_market_events_experiment
                ON market_events(experiment_id);
            """
        )
        for name in ("xianyu", "taobao"):
            conn.execute(
                "INSERT OR IGNORE INTO platforms (name) VALUES (?)", (name,)
            )
        conn.commit()


def compute_dedupe_key(raw: dict) -> str:
    external = raw.get("external_event_id") or raw.get("raw_reference")
    platform = str(raw.get("platform") or "").lower()
    source = str(raw.get("source") or "").lower()
    if external:
        material = f"{source}|{platform}|{external}"
    else:
        material = "|".join([
            source,
            platform,
            str(raw.get("event_type") or "").upper(),
            str(raw.get("event_timestamp") or raw.get("timestamp") or ""),
            str(raw.get("product_asset_id") or raw.get("product_id") or ""),
            str(raw.get("listing_id") or ""),
            str(raw.get("value") if raw.get("value") is not None else ""),
            str(raw.get("currency") or ""),
        ])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:32]


def validate_raw_event(raw: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not isinstance(raw, dict):
        return False, ["raw_not_dict"]
    et = str(raw.get("event_type") or "").upper()
    if not et:
        errors.append("missing_event_type")
    elif et not in EVENT_TYPES:
        errors.append(f"event_type_not_in_reserved_set:{et}")
    origin = str(raw.get("data_origin") or DATA_ORIGIN_UNKNOWN).upper()
    if origin not in (
        DATA_ORIGIN_REAL,
        DATA_ORIGIN_SIMULATION,
        DATA_ORIGIN_SYNTHETIC,
        DATA_ORIGIN_UNKNOWN,
    ):
        errors.append(f"invalid_data_origin:{origin}")
    ts = raw.get("event_timestamp") or raw.get("timestamp")
    if ts is not None and str(ts).strip() == "":
        errors.append("invalid_timestamp_empty")
    if et in ("REVENUE", "PURCHASE", "REFUND", "COST") and "value" in raw:
        try:
            if raw["value"] is not None:
                float(raw["value"])
        except (TypeError, ValueError):
            errors.append("invalid_value_not_numeric")
    hard = [e for e in errors if not e.startswith("event_type_not_in_reserved_set")]
    return len(hard) == 0, errors


def resolve_linkage(raw: dict) -> tuple[str, str]:
    notes = []
    has_product = bool(raw.get("product_asset_id") or raw.get("product_id"))
    has_experiment = bool(raw.get("experiment_id"))
    if not has_product:
        notes.append("missing_product_or_asset_id")
    if not has_experiment:
        notes.append("missing_experiment_id")
    if notes:
        return LINKAGE_UNRESOLVED, ";".join(notes)
    return LINKAGE_RESOLVED, "product_and_experiment_linked"


def normalize_market_event(raw: dict) -> dict:
    et = str(raw.get("event_type") or "").upper()
    origin = str(raw.get("data_origin") or DATA_ORIGIN_UNKNOWN).upper()
    vstatus = str(raw.get("verification_status") or VERIFICATION_UNVERIFIED).upper()
    if vstatus not in (
        VERIFICATION_UNVERIFIED,
        VERIFICATION_VERIFIED,
        VERIFICATION_MANUAL,
    ):
        vstatus = VERIFICATION_UNVERIFIED

    linkage_status, linkage_notes = resolve_linkage(raw)
    event_id = raw.get("event_id") or f"mevt_{uuid.uuid4().hex[:12]}"
    dedupe_key = raw.get("dedupe_key") or compute_dedupe_key(raw)

    verified_source = raw.get("verified_source")
    if vstatus in (VERIFICATION_VERIFIED, VERIFICATION_MANUAL):
        if not verified_source or str(verified_source).strip().lower() in (
            "", "unknown", "simulation",
        ):
            verified_source = (
                raw.get("source")
                or f"manual:{raw.get('platform') or 'unknown'}"
            )
    else:
        verified_source = None

    value = raw.get("value")
    if value is not None:
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = None

    return {
        "event_id": event_id,
        "event_type": et,
        "source": raw.get("source"),
        "platform": raw.get("platform"),
        "event_timestamp": raw.get("event_timestamp") or raw.get("timestamp"),
        "product_id": raw.get("product_id"),
        "product_asset_id": raw.get("product_asset_id"),
        "product_type": raw.get("product_type") or "document",
        "experiment_id": raw.get("experiment_id"),
        "listing_id": raw.get("listing_id"),
        "value": value,
        "currency": raw.get("currency"),
        "data_origin": origin,
        "verification_status": vstatus,
        "verified_source": verified_source,
        "raw_reference": raw.get("raw_reference") or raw.get("external_event_id"),
        "dedupe_key": dedupe_key,
        "linkage_status": linkage_status,
        "linkage_notes": linkage_notes,
        "raw_payload": json.dumps(raw, ensure_ascii=False),
        "ingested_at": _now_str(),
    }


def get_event_by_dedupe_key(dedupe_key: str) -> dict | None:
    ensure_market_event_schema()
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM market_events WHERE dedupe_key = ?",
            (dedupe_key,),
        ).fetchone()
    return dict(row) if row else None


def get_event_by_id(event_id: str) -> dict | None:
    ensure_market_event_schema()
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM market_events WHERE event_id = ?",
            (event_id,),
        ).fetchone()
    return dict(row) if row else None


def persist_normalized_event(event: dict) -> dict:
    ensure_market_event_schema()
    existing = get_event_by_dedupe_key(event["dedupe_key"])
    if existing:
        return {
            "accepted": False,
            "reason": "duplicate_event",
            "event_id": existing.get("event_id"),
            "duplicate_of": existing.get("event_id"),
        }
    cols = [
        "event_id", "event_type", "source", "platform", "event_timestamp",
        "product_id", "product_asset_id", "product_type", "experiment_id",
        "listing_id", "value", "currency", "data_origin", "verification_status",
        "verified_source", "raw_reference", "dedupe_key", "linkage_status",
        "linkage_notes", "raw_payload", "ingested_at",
    ]
    values = [event.get(c) for c in cols]
    with database.get_connection() as conn:
        conn.execute(
            f"INSERT INTO market_events ({', '.join(cols)}) "
            f"VALUES ({', '.join('?' * len(cols))})",
            values,
        )
        conn.commit()
    return {"accepted": True, "reason": "persisted", "event_id": event["event_id"]}


def is_market_observation_eligible(event: dict) -> tuple[bool, str]:
    origin = str(event.get("data_origin") or "").upper()
    if origin != DATA_ORIGIN_REAL:
        return False, f"observation_requires_REAL_got_{origin}"
    et = str(event.get("event_type") or "").upper()
    if et not in MARKET_OBSERVATION_EVENT_TYPES:
        return False, f"event_type_not_observation_capable:{et}"
    return True, "eligible_for_market_observation"


def is_verified_for_learning(event: dict) -> bool:
    return str(event.get("verification_status") or "").upper() in (
        VERIFICATION_VERIFIED,
        VERIFICATION_MANUAL,
    ) and bool(event.get("verified_source"))


def market_event_to_learning_record(event: dict) -> dict:
    et = str(event.get("event_type") or "").upper()
    commercial_map = {
        "PURCHASE": "purchase",
        "REVENUE": "revenue",
        "REFUND": "refund",
        "CONVERSION": "conversion",
        "PROFIT": "profit",
    }
    return {
        "commercial_outcome": commercial_map.get(et),
        "market_outcome": et.lower() if et not in commercial_map else None,
        "data_origin": event.get("data_origin"),
        "verified_source": event.get("verified_source"),
        "commercial_evidence_id": event.get("event_id"),
        "source_event_id": event.get("event_id"),
        "source": event.get("source"),
        "platform": event.get("platform"),
        "timestamp": event.get("event_timestamp"),
        "product_id": event.get("product_id"),
        "product_asset_id": event.get("product_asset_id"),
        "experiment_id": event.get("experiment_id"),
        "listing_id": event.get("listing_id"),
        "original_event_type": et,
        "original_value": event.get("value"),
        "currency": event.get("currency"),
        "verification_status": event.get("verification_status"),
        "keyword": event.get("product_asset_id") or event.get("product_id") or "",
        "task": f"market_event:{et}",
        "has_real_commercial_evidence": True,
    }


def route_to_commercial_learning(event: dict) -> dict:
    et = str(event.get("event_type") or "").upper()
    if et not in COMMERCIAL_LEARNING_EVENT_TYPES:
        return {
            "routed": False,
            "reason": "not_commercial_learning_event_type",
            "event_type": et,
            "commercial_success": False,
        }
    if str(event.get("data_origin") or "").upper() != DATA_ORIGIN_REAL:
        return {
            "routed": False,
            "reason": "data_origin_not_REAL",
            "commercial_success": False,
        }
    if not is_verified_for_learning(event):
        return {
            "routed": False,
            "reason": "unverified_blocked_from_real_commercial_learning",
            "commercial_success": False,
        }

    import memory_core  # noqa: E402

    record = market_event_to_learning_record(event)
    result = memory_core.ingest_commercial_learning_event(record)
    ensure_market_event_schema()
    with database.get_connection() as conn:
        conn.execute(
            """UPDATE market_events
               SET learning_routed=?, learning_result=?
               WHERE event_id=?""",
            (
                1 if result.get("accepted") else 0,
                json.dumps(result, ensure_ascii=False),
                event.get("event_id"),
            ),
        )
        conn.commit()
    return {
        "routed": True,
        "ingest": result,
        "commercial_success": bool(result.get("commercial_success")),
        "source_event_id": event.get("event_id"),
    }


def _load_observations_store() -> dict:
    OBSERVATIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    if not OBSERVATIONS_JSON.exists() or OBSERVATIONS_JSON.stat().st_size == 0:
        return {"schema": "observations_v1", "observations": [], "updated_at": None}
    try:
        return json.loads(OBSERVATIONS_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"schema": "observations_v1", "observations": [], "updated_at": None}


def _save_observations_store(store: dict) -> None:
    OBSERVATIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    store["updated_at"] = _now_str()
    OBSERVATIONS_JSON.write_text(
        json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def append_observation_event_ref(event: dict) -> dict:
    ok, reason = is_market_observation_eligible(event)
    if not ok:
        return {"accepted": False, "reason": reason}

    store = _load_observations_store()
    obs_list = store.get("observations", [])
    experiment_id = event.get("experiment_id")
    product_key = event.get("product_asset_id") or event.get("product_id")

    match = None
    for o in obs_list:
        if (
            o.get("experiment_id") == experiment_id
            and (o.get("product_asset_id") or o.get("product_id")) == product_key
            and o.get("status") == "collecting"
        ):
            match = o
            break

    if match is None:
        match = {
            "observation_id": f"obs_{uuid.uuid4().hex[:10]}",
            "experiment_id": experiment_id,
            "product_id": event.get("product_id"),
            "product_asset_id": event.get("product_asset_id"),
            "window_start": None,
            "window_end": None,
            "event_counts": {},
            "real_event_count": 0,
            "simulation_event_count": 0,
            "revenue": None,
            "refunds": None,
            "feedback_count": 0,
            "source_reliability": event.get("verification_status"),
            "status": "collecting",
            "event_ids": [],
            "note": (
                "Observation record collects facts only; "
                "does not imply commercial success or Pilot observation started"
            ),
            "created_at": _now_str(),
        }
        obs_list.append(match)

    et = str(event.get("event_type") or "").upper()
    counts = match.setdefault("event_counts", {})
    counts[et] = int(counts.get(et, 0)) + 1
    if event.get("data_origin") == DATA_ORIGIN_REAL:
        match["real_event_count"] = int(match.get("real_event_count", 0)) + 1
    elif event.get("data_origin") == DATA_ORIGIN_SIMULATION:
        match["simulation_event_count"] = int(match.get("simulation_event_count", 0)) + 1

    if et == "REVENUE" and event.get("value") is not None:
        prev = match.get("revenue")
        match["revenue"] = (0.0 if prev is None else float(prev)) + float(event["value"])
    if et == "REFUND" and event.get("value") is not None:
        prev = match.get("refunds")
        match["refunds"] = (0.0 if prev is None else float(prev)) + float(event["value"])

    eids = match.setdefault("event_ids", [])
    if event.get("event_id") not in eids:
        eids.append(event.get("event_id"))

    match["updated_at"] = _now_str()
    store["observations"] = obs_list
    _save_observations_store(store)
    return {
        "accepted": True,
        "reason": "observation_fact_recorded",
        "observation_id": match["observation_id"],
        "commercial_success": False,
        "conclusion": None,
    }


def ingest_raw_market_event(raw: dict) -> dict:
    """Raw → Validate → Normalize → Persist → Observation? → Commercial Learning?"""
    ok, errors = validate_raw_event(raw)
    hard_errors = [e for e in errors if not e.startswith("event_type_not_in_reserved_set")]
    if hard_errors:
        return {
            "accepted": False,
            "stage": "validation",
            "errors": hard_errors,
            "warnings": [e for e in errors if e not in hard_errors],
        }

    event = normalize_market_event(raw)
    if errors:
        event["linkage_notes"] = (
            (event.get("linkage_notes") or "") + ";warnings:" + ",".join(errors)
        ).strip(";")

    persist = persist_normalized_event(event)
    if not persist.get("accepted"):
        return {
            "accepted": False,
            "stage": "persist",
            "reason": persist.get("reason"),
            "duplicate_of": persist.get("duplicate_of"),
            "event_id": persist.get("event_id"),
            "normalized": event,
        }

    observation = None
    obs_ok, _ = is_market_observation_eligible(event)
    if obs_ok:
        observation = append_observation_event_ref(event)

    learning = route_to_commercial_learning(event)

    return {
        "accepted": True,
        "stage": "complete",
        "event_id": event["event_id"],
        "normalized": {
            k: event[k]
            for k in (
                "event_id", "event_type", "platform", "data_origin",
                "verification_status", "linkage_status", "linkage_notes",
                "product_asset_id", "experiment_id", "product_type",
                "value", "currency",
            )
        },
        "observation": observation,
        "learning": learning,
        "warnings": [e for e in errors if e.startswith("event_type_not_in_reserved_set")],
        "commercial_success": bool(learning and learning.get("commercial_success")),
    }


def build_evaluation_input(observation_id: str) -> dict:
    store = _load_observations_store()
    obs = next(
        (o for o in store.get("observations", []) if o.get("observation_id") == observation_id),
        None,
    )
    if not obs:
        return {"ok": False, "reason": "observation_not_found"}
    return {
        "ok": True,
        "evaluation_input": {
            "observation_id": observation_id,
            "experiment_id": obs.get("experiment_id"),
            "product_asset_id": obs.get("product_asset_id"),
            "event_counts": obs.get("event_counts"),
            "real_event_count": obs.get("real_event_count"),
            "revenue": obs.get("revenue"),
            "refunds": obs.get("refunds"),
            "note": "Facts only — not commercial success / not auto decision",
        },
    }
