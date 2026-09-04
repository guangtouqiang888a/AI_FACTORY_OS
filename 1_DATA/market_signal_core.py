# 1_DATA/market_signal_core.py — Raw Observation → Derived Market Signals
# Entry 054 (+ Entry 073 Observation/Candidate → Signal)
#
# Raw Data ≠ Signal ≠ Opportunity Score
# Does not overwrite products / collection_log fields.
# Platform/source remain text fields (not product-core locked).
#
# Lineages:
#   products keyword group → derive_signals_from_product_group (054)
#   MarketObservation / Filter Candidate → derive_signals_from_observation_candidates (073)
# Shared deterministic calculations; Observation path does NOT insert products.

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402

# Entry 070 locked MATCH Candidate observation_ids (Reference only; callers pass explicitly)
ENTRY_070_LOCKED_MATCH_IDS = (
    "mobs_48d5a1daa0ee",
    "mobs_4eeed83520dc",
    "mobs_77abed5da432",
    "mobs_558206dd2057",
    "mobs_2198f9db4742",
    "mobs_217cd4886838",
    "mobs_a28b1bc7faca",
)

LINEAGE_PRODUCT = "product"
LINEAGE_OBSERVATION = "market_observation"


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_market_signal_schema() -> None:
    with database.get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS market_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT UNIQUE NOT NULL,
                signal_type TEXT NOT NULL,
                keyword TEXT,
                platform TEXT,
                source TEXT,
                value REAL,
                unit TEXT,
                evidence_refs TEXT,
                observation_timestamp TEXT,
                computed_at TEXT NOT NULL,
                product_type TEXT,
                notes TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_market_signals_keyword
                ON market_signals(keyword);
            CREATE TABLE IF NOT EXISTS selection_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                selection_id TEXT UNIQUE NOT NULL,
                candidate_id TEXT,
                rank INTEGER,
                score REAL,
                risk_status TEXT,
                selected INTEGER DEFAULT 0,
                selection_reason TEXT,
                evidence_refs TEXT,
                discovery_method TEXT,
                created_at TEXT NOT NULL,
                payload TEXT
            );
            """
        )
        conn.commit()


def _parse_notes(notes: Any) -> dict:
    if isinstance(notes, dict):
        return notes
    if not notes:
        return {}
    try:
        data = json.loads(str(notes))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, TypeError):
        return {}


def _signal(
    signal_type: str,
    keyword: str,
    platform: str,
    source: str,
    value: float | None,
    unit: str,
    evidence: dict,
    obs_ts: str,
    notes: str = "",
    value_unavailable: bool = False,
    product_type: str = "digital_template",
) -> dict:
    return {
        "signal_id": f"sig_{uuid.uuid4().hex[:12]}",
        "signal_type": signal_type,
        "keyword": keyword,
        "platform": platform,
        "source": source,
        "value": value,
        "value_status": "UNAVAILABLE" if value_unavailable else "COMPUTED",
        "unit": unit,
        "evidence_refs": evidence,
        "observation_timestamp": obs_ts,
        "computed_at": _now_str(),
        "product_type": product_type,
        "notes": notes,
    }


def _infer_platform(listings: list[dict]) -> str:
    for p in listings:
        if p.get("platform"):
            return str(p["platform"])
    return "xianyu"


def _metric_values(
    listings: list[dict],
    key: str,
    *,
    null_as_zero: bool,
    cast,
) -> list:
    """
    Extract metric list.
    Product lineage (null_as_zero=True): missing → 0 (054 contract).
    Observation lineage (null_as_zero=False): missing stays None (NULL ≠ 0).
    """
    out = []
    for item in listings:
        v = item.get(key)
        if v is None:
            out.append(0 if null_as_zero else None)
        else:
            out.append(cast(v))
    return out


def _sum_known(values: list) -> tuple[float, int]:
    known = [v for v in values if v is not None]
    if not known:
        return 0.0, 0
    return float(sum(known)), len(known)


def _compute_deterministic_signals(
    keyword: str,
    listings: list[dict],
    *,
    evidence: dict,
    platform: str | None = None,
    source: str = "marketplace",
    observation_timestamp: str | None = None,
    null_as_zero: bool = True,
    extra_notes: str = "",
) -> list[dict]:
    """
    Shared deterministic Signal calculations for any normalized listing group.
    Does not invent values; null handling controlled by null_as_zero.
    """
    if not listings:
        return []

    obs_ts = observation_timestamp or _now_str()
    n = len(listings)

    wants = _metric_values(listings, "want_count", null_as_zero=null_as_zero, cast=int)
    views = _metric_values(listings, "view_count", null_as_zero=null_as_zero, cast=int)
    comments = _metric_values(listings, "comment_count", null_as_zero=null_as_zero, cast=int)
    shares = _metric_values(listings, "share_count", null_as_zero=null_as_zero, cast=int)

    # price: only known prices enter average (None skipped even when null_as_zero —
    # matches 054: `if p.get("price") is not None`)
    prices: list[float] = []
    for item in listings:
        if item.get("price") is not None:
            prices.append(float(item["price"]))

    total_want, want_n = _sum_known(wants)
    total_view, _view_n = _sum_known(views)
    # Preserve 054 avg_want = sum(wants)/n when null_as_zero (zeros included in n)
    if null_as_zero:
        avg_want = total_want / n if n else 0.0
    else:
        avg_want = (total_want / want_n) if want_n else 0.0

    avg_price = sum(prices) / len(prices) if prices else 0.0
    engagement = (total_want / total_view) if total_view > 0 else 0.0
    growth_available = False

    # comments/shares retained for future; not used in v1 signal set (054)
    _ = (comments, shares)

    plat = platform or _infer_platform(listings)
    note_suffix = f";{extra_notes}" if extra_notes else ""

    signals = [
        _signal(
            "demand_signal", keyword, plat, source, total_want, "want_count_sum",
            evidence, obs_ts, notes=extra_notes,
        ),
        _signal(
            "engagement_signal", keyword, plat, source, round(engagement, 4), "want_per_view",
            evidence, obs_ts, notes=extra_notes,
        ),
        _signal(
            "competition_signal", keyword, plat, source, float(n), "listing_count",
            evidence, obs_ts, notes=extra_notes,
        ),
        _signal(
            "price_signal", keyword, plat, source, round(avg_price, 2), "avg_price",
            evidence, obs_ts, notes=extra_notes,
        ),
        _signal(
            "trend_signal", keyword, plat, source, round(avg_want, 2), "avg_want_proxy",
            evidence, obs_ts,
            notes=("Proxy from want intensity — not true time-series trend" + note_suffix).strip(";"),
        ),
    ]
    if not growth_available:
        signals.append(_signal(
            "growth_signal", keyword, plat, source, None, "unavailable",
            evidence, obs_ts,
            notes=("NOT YET IMPLEMENTED — no time-series growth data" + note_suffix).strip(";"),
            value_unavailable=True,
        ))
    return signals


def derive_signals_from_product_group(
    keyword: str,
    products: list[dict],
    *,
    platform: str | None = None,
    source: str = "marketplace",
    observation_timestamp: str | None = None,
) -> list[dict]:
    """
    Aggregate listing facts into Derived Signals (product lineage).
    Does not mutate raw product rows.
    Missing want/view/comment/share coerce to 0 (054 contract).
    """
    if not products:
        return []

    product_ids = [str(p.get("id") or p.get("source_url") or "") for p in products]
    evidence = {
        "lineage": LINEAGE_PRODUCT,
        "product_ids": [x for x in product_ids if x][:50],
        "listing_count": len(products),
        "collect_dates": list(
            {str(p.get("collect_date") or "") for p in products if p.get("collect_date")}
        ),
    }
    return _compute_deterministic_signals(
        keyword,
        products,
        evidence=evidence,
        platform=platform,
        source=source,
        observation_timestamp=observation_timestamp,
        null_as_zero=True,
    )


def resolve_observation_keyword(obs: dict) -> str | None:
    """Keyword from explicit field or notes.query — never invented."""
    if obs.get("keyword"):
        return str(obs["keyword"]).strip() or None
    notes = _parse_notes(obs.get("notes"))
    q = notes.get("query")
    if q:
        return str(q).strip() or None
    return None


def observation_to_listing_input(obs: dict) -> dict:
    """
    Map MarketObservation / Candidate → Signal listing input.
    Does not fabricate metrics. NULL stays NULL.
    """
    notes = _parse_notes(obs.get("notes"))
    session_id = obs.get("session_id") or notes.get("session_id")
    extension_run_id = obs.get("extension_run_id") or notes.get("extension_run_id")
    # raw_reference often holds extension evidence path; extension_run may be in candidate
    return {
        "id": obs.get("observation_id") or obs.get("id"),
        "observation_id": obs.get("observation_id"),
        "source_item_id": obs.get("source_item_id"),
        "source_url": obs.get("source_url"),
        "keyword": resolve_observation_keyword(obs),
        "want_count": obs.get("want_count"),  # may be None
        "view_count": obs.get("view_count"),
        "price": obs.get("price"),
        "comment_count": obs.get("comment_count"),
        "share_count": obs.get("share_count"),
        "platform": obs.get("platform"),
        "collect_date": obs.get("observed_at") or obs.get("collect_date"),
        "observed_at": obs.get("observed_at"),
        "run_id": obs.get("run_id") or obs.get("collection_run_id"),
        "collection_run_id": obs.get("collection_run_id") or obs.get("run_id"),
        "session_id": session_id,
        "extension_run_id": extension_run_id,
        "data_origin": obs.get("data_origin"),
        "verification_status": obs.get("verification_status"),
        "filter_status": obs.get("filter_status"),
        "notes": notes,
    }


def _build_observation_evidence(listings: list[dict]) -> dict:
    def _uniq(key: str) -> list:
        seen = []
        for item in listings:
            v = item.get(key)
            if v is not None and str(v) and str(v) not in seen:
                seen.append(str(v))
        return seen[:50]

    null_want = [
        str(x.get("observation_id"))
        for x in listings
        if x.get("want_count") is None and x.get("observation_id")
    ]
    return {
        "lineage": LINEAGE_OBSERVATION,
        "observation_ids": _uniq("observation_id"),
        "source_item_ids": _uniq("source_item_id"),
        "collection_run_ids": _uniq("collection_run_id"),
        "session_ids": _uniq("session_id"),
        "extension_run_ids": _uniq("extension_run_id"),
        "data_origins": _uniq("data_origin"),
        "verification_statuses": _uniq("verification_status"),
        "listing_count": len(listings),
        "observed_ats": _uniq("observed_at"),
        "null_want_count_observation_ids": null_want,
        "product_ids": [],  # explicit: no product substitution
    }


def derive_signals_from_observation_group(
    keyword: str,
    observations: list[dict],
    *,
    platform: str | None = None,
    source: str = "market_observation",
    observation_timestamp: str | None = None,
) -> list[dict]:
    """
    Observation-native Signal derivation.
    Shares deterministic calculations with product path.
    NULL metrics are NOT coerced to 0.
    """
    if not observations:
        return []
    listings = [observation_to_listing_input(o) for o in observations]
    evidence = _build_observation_evidence(listings)
    obs_ts = observation_timestamp
    if not obs_ts:
        ats = [str(x.get("observed_at") or "") for x in listings if x.get("observed_at")]
        obs_ts = max(ats) if ats else _now_str()
    return _compute_deterministic_signals(
        keyword,
        listings,
        evidence=evidence,
        platform=platform,
        source=source,
        observation_timestamp=obs_ts,
        null_as_zero=False,
        extra_notes="observation_candidate_lineage",
    )


def load_observations_by_ids(observation_ids: list[str]) -> list[dict]:
    """Read market_observations by id — does not mutate rows."""
    database.ensure_schema()
    if not observation_ids:
        return []
    with database.get_connection() as conn:
        placeholders = ",".join("?" * len(observation_ids))
        rows = conn.execute(
            f"SELECT * FROM market_observations WHERE observation_id IN ({placeholders})",
            list(observation_ids),
        ).fetchall()
    by_id = {dict(r)["observation_id"]: dict(r) for r in rows}
    # Preserve caller order
    return [by_id[i] for i in observation_ids if i in by_id]


def derive_signals_from_observation_candidates(
    candidates: list[dict],
    *,
    require_match: bool = True,
    require_real_verified: bool = True,
    source: str = "market_observation",
) -> dict[str, Any]:
    """
    Formal Candidate → Signal entry (Entry 073).

    Input: Filter Candidate dicts and/or Observation dicts (must carry observation_id).
    Does NOT write products. Does NOT call AI.
    Groups by resolved keyword; shared deterministic Signal logic.
    """
    skipped: list[dict] = []
    accepted: list[dict] = []

    for c in candidates:
        row = dict(c)
        oid = row.get("observation_id")
        if not oid:
            skipped.append({"candidate": c, "reason": "missing_observation_id"})
            continue

        # Merge DB observation if present (authoritative metrics)
        db_rows = load_observations_by_ids([str(oid)])
        if db_rows:
            merged = dict(db_rows[0])
            # Candidate may carry filter/session/extension not stored as columns
            for k in (
                "filter_status",
                "session_id",
                "extension_run_id",
                "collection_run_id",
                "keyword",
            ):
                if row.get(k) is not None and merged.get(k) is None:
                    merged[k] = row[k]
            # Prefer candidate filter_status when provided
            if row.get("filter_status") is not None:
                merged["filter_status"] = row["filter_status"]
            row = merged
        else:
            skipped.append({"observation_id": oid, "reason": "observation_not_found_in_db"})
            continue

        if require_real_verified:
            if row.get("data_origin") != "REAL":
                skipped.append({"observation_id": oid, "reason": "data_origin_not_REAL"})
                continue
            if row.get("verification_status") != "MANUAL_VERIFIED":
                skipped.append({"observation_id": oid, "reason": "verification_not_MANUAL_VERIFIED"})
                continue

        if require_match and row.get("filter_status") != "MATCH":
            skipped.append({
                "observation_id": oid,
                "reason": "filter_status_not_MATCH",
                "filter_status": row.get("filter_status"),
            })
            continue

        accepted.append(row)

    groups: dict[str, list[dict]] = {}
    no_keyword: list[dict] = []
    for row in accepted:
        kw = resolve_observation_keyword(row)
        if not kw:
            no_keyword.append(row)
            skipped.append({
                "observation_id": row.get("observation_id"),
                "reason": "keyword_unresolved",
            })
            continue
        groups.setdefault(kw, []).append(row)

    all_signals: list[dict] = []
    mapping: list[dict] = []
    for keyword, obs_list in groups.items():
        signals = derive_signals_from_observation_group(
            keyword, obs_list, source=source,
        )
        all_signals.extend(signals)
        sig_ids = [s["signal_id"] for s in signals]
        for obs in obs_list:
            mapping.append({
                "observation_id": obs.get("observation_id"),
                "source_item_id": obs.get("source_item_id"),
                "keyword": keyword,
                "signal_ids": sig_ids,
                "signal_types": [s["signal_type"] for s in signals],
            })

    return {
        "status": "OK" if all_signals else "NO_SIGNALS",
        "candidate_input_count": len(candidates),
        "accepted_count": len(accepted) - len(no_keyword),
        "skipped": skipped,
        "keyword_groups": {k: len(v) for k, v in groups.items()},
        "signals": all_signals,
        "signal_count": len(all_signals),
        "candidate_signal_mapping": mapping,
        "product_substitution": False,
        "ai_invoked": False,
    }


def persist_signals(signals: list[dict]) -> int:
    ensure_market_signal_schema()
    n = 0
    with database.get_connection() as conn:
        for s in signals:
            if s.get("value_status") == "UNAVAILABLE" and s.get("value") is None:
                # still record unavailable for auditability
                pass
            conn.execute(
                """
                INSERT OR REPLACE INTO market_signals (
                    signal_id, signal_type, keyword, platform, source, value, unit,
                    evidence_refs, observation_timestamp, computed_at, product_type, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    s["signal_id"],
                    s["signal_type"],
                    s.get("keyword"),
                    s.get("platform"),
                    s.get("source"),
                    s.get("value"),
                    s.get("unit"),
                    json.dumps(s.get("evidence_refs") or {}, ensure_ascii=False),
                    s.get("observation_timestamp"),
                    s.get("computed_at"),
                    s.get("product_type"),
                    s.get("notes"),
                ),
            )
            n += 1
        conn.commit()
    return n


def load_signals_by_ids(signal_ids: list[str]) -> list[dict]:
    """Read persisted market_signals by signal_id — does not mutate rows."""
    ensure_market_signal_schema()
    if not signal_ids:
        return []
    with database.get_connection() as conn:
        placeholders = ",".join("?" * len(signal_ids))
        rows = conn.execute(
            f"SELECT * FROM market_signals WHERE signal_id IN ({placeholders})",
            list(signal_ids),
        ).fetchall()
    by_id: dict[str, dict] = {}
    for r in rows:
        d = dict(r)
        ev = d.get("evidence_refs")
        if isinstance(ev, str):
            try:
                d["evidence_refs"] = json.loads(ev)
            except (json.JSONDecodeError, TypeError):
                d["evidence_refs"] = {}
        elif not isinstance(ev, dict):
            d["evidence_refs"] = {}
        by_id[d["signal_id"]] = d
    return [by_id[sid] for sid in signal_ids if sid in by_id]


def load_products_grouped_by_keyword(min_listings: int = 1) -> dict[str, list[dict]]:
    """Read raw products without modifying them."""
    database.ensure_schema()
    with database.get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM products ORDER BY keyword, id"
        ).fetchall()
    groups: dict[str, list[dict]] = {}
    for r in rows:
        d = dict(r)
        kw = str(d.get("keyword") or "").strip()
        if not kw:
            continue
        groups.setdefault(kw, []).append(d)
    return {k: v for k, v in groups.items() if len(v) >= min_listings}
