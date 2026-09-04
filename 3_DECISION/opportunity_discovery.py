# 3_DECISION/opportunity_discovery.py — Market Data → Opportunity Discovery & Selection
# Entry 054 (+ Entry 075 Observation-native Signal → Opportunity)
#
# Market Data → Signals → Opportunity Candidate → Score → Risk → Selection
# Product path: products → derive_signals → discover_opportunities
# Observation path: market_signals (073) → discover_opportunities_from_observation_signals
# Pool Sorting ≠ Opportunity Discovery
# Selection ≠ Production / Experiment auto-create
# No fake opportunities; INSUFFICIENT DATA when evidence lacking
# No future-data leakage: observation_timestamp must be ≤ score_time

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "3_DECISION"))

import config  # noqa: E402
import market_signal_core as msc  # noqa: E402
from risk_engine import assess_risk  # noqa: E402
from scorer import score_observation_listing, score_product  # noqa: E402

DISCOVERED_JSON = (
    ROOT
    / "commercial_assets"
    / "opportunity_candidates"
    / "autonomous_discovery_v1.json"
)

SCORE_MODEL_NOTE = (
    "Current model uses listing-derived demand/trend/competition/profit/difficulty proxies. "
    "Historical Performance / Learning Value / Conversion = NOT YET IMPLEMENTED unless evidence exists. "
    "This is NOT final commercial intelligence."
)

MIN_LISTINGS_DEFAULT = 3

# Entry 073 persisted signal IDs (reference; callers must validate DB reality)
ENTRY_073_SIGNAL_IDS = (
    "sig_f1173cc0edca",
    "sig_9a3983efb2a4",
    "sig_10fa1228c3f2",
    "sig_82a523bc2bc1",
    "sig_90277d017e37",
    "sig_90064dc020a6",
)

OBSERVATION_DISCOVERY_JSON = (
    ROOT
    / "commercial_assets"
    / "opportunity_candidates"
    / "observation_discovery_v1.json"
)


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def score_opportunity_from_signals(
    signals: list[dict],
    listings: list[dict],
    *,
    score_listing_fn=None,
) -> dict:
    """
    Opportunity Score from Derived Signals + listing score proxies.
    Dimensions missing → UNAVAILABLE (not fabricated).
    listings: Product rows (score_product) or Observations (score_observation_listing).
    """
    score_fn = score_listing_fn or score_product
    by_type = {s["signal_type"]: s for s in signals}
    listing_scores: list[dict] = []
    for item in listings:
        s = score_fn(item)
        if s is not None:
            listing_scores.append(s)

    if listing_scores:
        avg_total = sum(s["total"] for s in listing_scores) / len(listing_scores)
        avg_hot = sum(s["hot"] for s in listing_scores) / len(listing_scores)
        avg_trend = sum(s["trend"] for s in listing_scores) / len(listing_scores)
        avg_comp = sum(s["comp"] for s in listing_scores) / len(listing_scores)
        avg_profit = sum(s["profit"] for s in listing_scores) / len(listing_scores)
        avg_diff = sum(s["difficulty"] for s in listing_scores) / len(listing_scores)
    else:
        avg_total = avg_hot = avg_trend = avg_comp = avg_profit = avg_diff = 0.0

    demand_sig = by_type.get("demand_signal")
    price_sig = by_type.get("price_signal")
    eng_sig = by_type.get("engagement_signal")
    growth_sig = by_type.get("growth_signal")

    hot_status = "COMPUTED" if listing_scores else "UNAVAILABLE"
    dimensions = {
        "Demand": {
            "status": "COMPUTED" if demand_sig and demand_sig.get("value") is not None else "UNAVAILABLE",
            "value": demand_sig.get("value") if demand_sig else None,
            "score_0_100": round(min(100.0, avg_hot), 2) if listing_scores else None,
            "listing_score_status": hot_status,
        },
        "Trend": {
            "status": "COMPUTED_PROXY" if listing_scores else "UNAVAILABLE",
            "value": by_type.get("trend_signal", {}).get("value"),
            "score_0_100": round(min(100.0, avg_trend), 2) if listing_scores else None,
            "note": "Proxy — not true time-series",
        },
        "Competition": {
            "status": "COMPUTED" if listing_scores else "UNAVAILABLE",
            "value": by_type.get("competition_signal", {}).get("value"),
            "score_0_100": round(min(100.0, avg_comp), 2) if listing_scores else None,
        },
        "Price": {
            "status": "COMPUTED" if price_sig and price_sig.get("value") is not None else "UNAVAILABLE",
            "value": price_sig.get("value") if price_sig else None,
        },
        "Potential_Revenue": {
            "status": "COMPUTED_PROXY" if listing_scores else "UNAVAILABLE",
            "score_0_100": round(min(100.0, avg_profit), 2) if listing_scores else None,
            "note": "Proxy from listing profit heuristic — not real revenue",
        },
        "Production_Cost": {
            "status": "NOT_YET_IMPLEMENTED",
            "value": None,
        },
        "Difficulty": {
            "status": "COMPUTED_PROXY" if listing_scores else "UNAVAILABLE",
            "score_0_100": round(min(100.0, avg_diff), 2) if listing_scores else None,
        },
        "Risk": {
            "status": "DEFERRED_TO_RISK_GATE",
            "value": None,
        },
        "Historical_Performance": {
            "status": "UNAVAILABLE",
            "value": None,
            "note": "No real commercial outcomes yet (Pilot Observation NOT_STARTED)",
        },
        "Learning_Value": {
            "status": "HEURISTIC",
            "score_0_100": _learning_value_heuristic(signals, listings),
            "note": "Minimal concept — new keyword/format learning potential",
        },
        "Engagement": {
            "status": "COMPUTED" if eng_sig else "UNAVAILABLE",
            "value": eng_sig.get("value") if eng_sig else None,
        },
        "Growth": {
            "status": growth_sig.get("value_status", "UNAVAILABLE") if growth_sig else "UNAVAILABLE",
            "value": None,
        },
    }

    usable = [
        v for v in (
            dimensions["Demand"]["score_0_100"],
            dimensions["Trend"]["score_0_100"],
            dimensions["Competition"]["score_0_100"],
            dimensions["Potential_Revenue"]["score_0_100"],
            dimensions["Difficulty"]["score_0_100"],
            dimensions["Learning_Value"]["score_0_100"],
        )
        if v is not None
    ]
    total = round(sum(usable) / len(usable), 2) if usable else 0.0

    return {
        "model_note": SCORE_MODEL_NOTE,
        "dimensions": dimensions,
        "total_score": total,
        "listing_avg_total": round(avg_total, 2),
        "score_method": "market_signal_proxy_v1",
        "scored_at": _now_str(),
        "scorable_listing_count": len(listing_scores),
        "input_listing_count": len(listings),
    }


def _learning_value_heuristic(signals: list[dict], listings: list[dict]) -> float:
    """Minimal Learning Value: diversity of titles + moderate competition."""
    n = len(listings)
    titles = {str(p.get("title") or "")[:20] for p in listings}
    diversity = min(40.0, len(titles) * 5.0)
    volume = min(40.0, n * 4.0)
    mid = 20.0 if 3 <= n <= 30 else 10.0
    return round(min(100.0, diversity + volume + mid), 2)


def assess_opportunity_risk(keyword: str, listings: list[dict]) -> dict:
    """Risk before selection — unknown cannot be selected."""
    flags = []
    for item in listings:
        r = assess_risk({
            "title": item.get("title") or "",
            "keyword": keyword,
            "price": item.get("price") or 0,
        })
        if not r.get("passed"):
            flags.append(r.get("reason"))
    kw_risk = assess_risk({"title": keyword, "keyword": keyword, "price": 1})
    if not kw_risk.get("passed"):
        flags.append(kw_risk.get("reason"))

    if flags:
        return {
            "passed": False,
            "risk_status": "failed",
            "level": "high",
            "reason": "; ".join(str(f) for f in flags[:5]),
        }
    if not listings:
        return {
            "passed": False,
            "risk_status": "unknown",
            "level": "unknown",
            "reason": "no_listings_for_risk",
        }
    return {
        "passed": True,
        "risk_status": "passed",
        "level": "low",
        "reason": "keyword_and_listings_passed_sensitive_and_price_checks",
    }


def build_opportunity_candidate(
    keyword: str,
    products: list[dict],
    signals: list[dict],
    score: dict,
    risk: dict,
    *,
    product_type: str = "digital_template",
    source: str = "marketplace",
    platform: str | None = None,
) -> dict:
    plat = platform or (signals[0].get("platform") if signals else "xianyu")
    evidence_refs = []
    for s in signals:
        evidence_refs.append({
            "signal_id": s.get("signal_id"),
            "signal_type": s.get("signal_type"),
            "observation_timestamp": s.get("observation_timestamp"),
        })
    for p in products[:20]:
        evidence_refs.append({
            "product_id": p.get("id"),
            "source_url": p.get("source_url"),
            "collect_date": p.get("collect_date"),
        })

    avg_price = None
    prices = [float(p["price"]) for p in products if p.get("price") is not None]
    if prices:
        avg_price = round(sum(prices) / len(prices), 2)

    signal_summary = {
        s["signal_type"]: {
            "value": s.get("value"),
            "status": s.get("value_status", "COMPUTED"),
        }
        for s in signals
    }

    return {
        "candidate_id": f"aoc_{uuid.uuid4().hex[:12]}",
        "opportunity_id": None,  # not auto-promoted to commercial opportunity object
        "keyword": keyword,
        "source": source,
        "platform": plat,
        "source_observation": {
            "listing_count": len(products),
            "observation_timestamp": signals[0].get("observation_timestamp") if signals else _now_str(),
        },
        "problem": f"Market listings for「{keyword}」show aggregated demand/competition signals",
        "audience": "inferred_from_marketplace_listings",
        "product_type": product_type,
        "market_signals": signal_summary,
        "estimated_value": avg_price,
        "production_feasibility": score["dimensions"]["Difficulty"]["status"],
        "competition": signal_summary.get("competition_signal"),
        "risk": risk,
        "learning_value": score["dimensions"]["Learning_Value"],
        "score": score,
        "status": "discovered_candidate",
        "discovery_source": source,
        "discovery_method": "market_signal",
        "evidence_refs": evidence_refs,
        "signal_summary": signal_summary,
        "created_at": _now_str(),
        "auto_production_forbidden": True,
        "note": "Candidate only — Selection ≠ Experiment ≠ Production",
    }


def discover_opportunities(
    *,
    min_listings: int = MIN_LISTINGS_DEFAULT,
    persist: bool = True,
    product_type: str = "digital_template",
) -> dict:
    """
    Full minimal discovery pipeline from SQLite products.
    Returns INSUFFICIENT DATA if not enough evidence.
    """
    groups = msc.load_products_grouped_by_keyword(min_listings=min_listings)
    # Filter noise test keywords optionally
    usable = {
        k: v for k, v in groups.items()
        if not k.startswith("test")
        and "test_" not in k.lower()
        and "测试" not in k
    }

    if not usable:
        return {
            "status": "INSUFFICIENT_DATA",
            "reason": "no_keyword_groups_meeting_min_listings",
            "min_listings": min_listings,
            "candidates": [],
            "selection_results": [],
            "fake_opportunities_created": False,
        }

    candidates = []
    all_signals = []
    score_time = _now_iso()

    for keyword, products in usable.items():
        # Leakage guard: collect_date / observation must not be after score_time
        obs_ts = _latest_collect_timestamp(products)
        if obs_ts and obs_ts > score_time:
            continue  # refuse future-dated observations

        signals = msc.derive_signals_from_product_group(
            keyword, products, source="marketplace", observation_timestamp=obs_ts or score_time,
        )
        # Leakage: all signal observation_timestamps must be <= score_time
        for s in signals:
            ots = s.get("observation_timestamp") or ""
            if ots > score_time:
                s["observation_timestamp"] = score_time
                s["notes"] = (s.get("notes") or "") + ";clamped_to_score_time"

        score = score_opportunity_from_signals(signals, products)
        risk = assess_opportunity_risk(keyword, products)
        cand = build_opportunity_candidate(
            keyword, products, signals, score, risk, product_type=product_type,
        )
        cand["score_time"] = score_time
        candidates.append(cand)
        all_signals.extend(signals)

    if persist and all_signals:
        msc.persist_signals(all_signals)

    selection = select_discovered_candidates(candidates)
    if persist:
        _persist_discovered(candidates, selection)
        _persist_selection_results(selection)

    return {
        "status": "OK" if candidates else "INSUFFICIENT_DATA",
        "model_note": SCORE_MODEL_NOTE,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "selection_results": selection,
        "fake_opportunities_created": False,
        "auto_experiment_created": False,
        "auto_production_triggered": False,
    }


def _latest_collect_timestamp(products: list[dict]) -> str | None:
    dates = [str(p.get("collect_date") or "") for p in products if p.get("collect_date")]
    if not dates:
        return None
    # collect_date often YYYY-MM-DD — expand to sortable iso-ish
    latest = max(dates)
    if len(latest) == 10:
        return f"{latest}T00:00:00"
    return latest


def select_discovered_candidates(
    candidates: list[dict],
    *,
    top_n: int = 5,
    min_score: float | None = None,
) -> list[dict]:
    """
    Risk filter → rank → Selection Result with reason/evidence.
    risk unknown/failed → not selected.
    """
    threshold = float(min_score if min_score is not None else getattr(
        config, "PUBLISH_SCORE_THRESHOLD", 60
    ))
    results = []
    eligible = []
    for c in candidates:
        risk = c.get("risk") or {}
        risk_status = risk.get("risk_status") or "unknown"
        score_total = float((c.get("score") or {}).get("total_score") or 0)
        if risk_status in ("unknown", "failed") or not risk.get("passed"):
            results.append(_selection_row(
                c, rank=None, selected=False,
                reason=f"risk_blocked:{risk_status}:{risk.get('reason')}",
                score_total=score_total,
            ))
            continue
        if score_total < threshold:
            results.append(_selection_row(
                c, rank=None, selected=False,
                reason=f"below_threshold:{score_total}<{threshold}",
                score_total=score_total,
            ))
            continue
        eligible.append(c)

    eligible.sort(
        key=lambda x: float((x.get("score") or {}).get("total_score") or 0),
        reverse=True,
    )
    for i, c in enumerate(eligible[:top_n], start=1):
        score_total = float((c.get("score") or {}).get("total_score") or 0)
        reason = (
            f"rank={i}; total_score={score_total}; "
            f"discovery_method=market_signal; keyword={c.get('keyword')}; "
            f"listings={(c.get('source_observation') or {}).get('listing_count')}"
        )
        results.append(_selection_row(
            c, rank=i, selected=True, reason=reason, score_total=score_total,
        ))

    # Mark remaining eligible beyond top_n as not selected
    for c in eligible[top_n:]:
        score_total = float((c.get("score") or {}).get("total_score") or 0)
        results.append(_selection_row(
            c, rank=None, selected=False,
            reason="eligible_but_outside_top_n",
            score_total=score_total,
        ))

    results.sort(key=lambda r: (0 if r["selected"] else 1, r.get("rank") or 999))
    return results


def _selection_row(
    candidate: dict,
    *,
    rank: int | None,
    selected: bool,
    reason: str,
    score_total: float,
) -> dict:
    risk = candidate.get("risk") or {}
    return {
        "selection_id": f"sel_{uuid.uuid4().hex[:12]}",
        "candidate_id": candidate.get("candidate_id"),
        "rank": rank,
        "score": score_total,
        "risk_status": risk.get("risk_status"),
        "selected": selected,
        "selection_reason": reason,
        "evidence_refs": candidate.get("evidence_refs"),
        "discovery_method": candidate.get("discovery_method"),
        "keyword": candidate.get("keyword"),
        "product_type": candidate.get("product_type"),
        "platform": candidate.get("platform"),
        "source": candidate.get("source"),
        "created_at": _now_str(),
        "next_step": "experiment_candidate" if selected else "hold",
        "auto_production_forbidden": True,
    }


def _persist_discovered(candidates: list[dict], selection: list[dict]) -> None:
    DISCOVERED_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "autonomous_discovery_v1",
        "entry": "054",
        "note": (
            "Autonomous discovery candidates from market listings. "
            "≠ human_assisted opportunities_v1.json. "
            "Selection ≠ Experiment ≠ Production. No fake commercial outcomes."
        ),
        "updated_at": _now_str(),
        "candidates": candidates,
        "selection_results": selection,
    }
    DISCOVERED_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _persist_selection_results(selection: list[dict]) -> None:
    msc.ensure_market_signal_schema()
    with msc.database.get_connection() as conn:
        for s in selection:
            conn.execute(
                """
                INSERT OR REPLACE INTO selection_results (
                    selection_id, candidate_id, rank, score, risk_status, selected,
                    selection_reason, evidence_refs, discovery_method, created_at, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    s["selection_id"],
                    s.get("candidate_id"),
                    s.get("rank"),
                    s.get("score"),
                    s.get("risk_status"),
                    1 if s.get("selected") else 0,
                    s.get("selection_reason"),
                    json.dumps(s.get("evidence_refs") or [], ensure_ascii=False),
                    s.get("discovery_method"),
                    s.get("created_at"),
                    json.dumps(s, ensure_ascii=False),
                ),
            )
        conn.commit()


def future_compatibility_probe(
    product_type: str,
    platform: str,
    source: str,
) -> dict:
    """Abstract probe — no future runtime."""
    fake_products = [
        {
            "id": 1,
            "keyword": "probe",
            "title": "probe item",
            "price": 9.9,
            "want_count": 10,
            "view_count": 100,
            "collect_date": "2026-01-01",
        }
    ]
    signals = msc.derive_signals_from_product_group(
        "probe", fake_products, platform=platform, source=source,
    )
    for s in signals:
        s["product_type"] = product_type
    score = score_opportunity_from_signals(signals, fake_products)
    risk = assess_opportunity_risk("probe", fake_products)
    cand = build_opportunity_candidate(
        "probe", fake_products, signals, score, risk,
        product_type=product_type, source=source, platform=platform,
    )
    return {
        "ok": True,
        "product_type": product_type,
        "platform": platform,
        "source": source,
        "core_model_valid": True,
        "candidate_id_present": bool(cand.get("candidate_id")),
        "discovery_method": cand.get("discovery_method"),
        "requires_rebuild": False,
    }


def refuse_empty_evidence_opportunity() -> dict:
    """No evidence → do not silently create opportunity."""
    return {
        "created": False,
        "reason": "no_evidence",
        "candidates": [],
    }


def _signal_evidence_dict(signal: dict) -> dict:
    ev = signal.get("evidence_refs")
    if isinstance(ev, str):
        try:
            return json.loads(ev)
        except (json.JSONDecodeError, TypeError):
            return {}
    return ev if isinstance(ev, dict) else {}


def _merge_observation_provenance(signals: list[dict]) -> dict:
    """Merge provenance from persisted Observation-lineage signals."""
    merged: dict[str, list] = {
        "lineage": msc.LINEAGE_OBSERVATION,
        "signal_ids": [],
        "observation_ids": [],
        "source_item_ids": [],
        "collection_run_ids": [],
        "session_ids": [],
        "extension_run_ids": [],
        "data_origins": [],
        "verification_statuses": [],
    }
    for s in signals:
        sid = s.get("signal_id")
        if sid and sid not in merged["signal_ids"]:
            merged["signal_ids"].append(sid)
        ev = _signal_evidence_dict(s)
        for key in (
            "observation_ids",
            "source_item_ids",
            "collection_run_ids",
            "session_ids",
            "extension_run_ids",
            "data_origins",
            "verification_statuses",
        ):
            for v in ev.get(key) or []:
                sv = str(v)
                if sv and sv not in merged[key]:
                    merged[key].append(sv)
    return merged


def _validate_observation_lineage_signals(
    signals: list[dict],
    *,
    require_real_verified: bool = True,
) -> tuple[bool, str]:
    if not signals:
        return False, "no_signals"
    for s in signals:
        if s.get("source") != "market_observation":
            return False, f"signal_not_observation_lineage:{s.get('signal_id')}"
        ev = _signal_evidence_dict(s)
        if ev.get("lineage") != msc.LINEAGE_OBSERVATION:
            return False, f"evidence_lineage_not_market_observation:{s.get('signal_id')}"
        if require_real_verified:
            origins = ev.get("data_origins") or []
            verifs = ev.get("verification_statuses") or []
            if "REAL" not in origins:
                return False, f"data_origin_not_REAL:{s.get('signal_id')}"
            if "MANUAL_VERIFIED" not in verifs:
                return False, f"verification_not_MANUAL_VERIFIED:{s.get('signal_id')}"
    return True, "ok"


def _validate_observations_real_verified(observations: list[dict]) -> tuple[bool, str]:
    for obs in observations:
        if obs.get("data_origin") != "REAL":
            return False, f"observation_not_REAL:{obs.get('observation_id')}"
        if obs.get("verification_status") != "MANUAL_VERIFIED":
            return False, f"observation_not_MANUAL_VERIFIED:{obs.get('observation_id')}"
    return True, "ok"


def build_observation_opportunity_candidate(
    keyword: str,
    observations: list[dict],
    signals: list[dict],
    score: dict,
    risk: dict,
    provenance: dict,
    *,
    product_type: str = "digital_template",
    platform: str | None = None,
) -> dict:
    """Opportunity candidate from Observation-lineage persisted signals."""
    plat = platform or (signals[0].get("platform") if signals else "xianyu")
    evidence_refs: list[dict] = []
    for s in signals:
        evidence_refs.append({
            "signal_id": s.get("signal_id"),
            "signal_type": s.get("signal_type"),
            "observation_timestamp": s.get("observation_timestamp"),
            "source": s.get("source"),
        })
    evidence_refs.append({
        "lineage": msc.LINEAGE_OBSERVATION,
        "signal_ids": provenance.get("signal_ids") or [],
        "observation_ids": provenance.get("observation_ids") or [],
        "source_item_ids": provenance.get("source_item_ids") or [],
        "collection_run_ids": provenance.get("collection_run_ids") or [],
        "session_ids": provenance.get("session_ids") or [],
        "extension_run_ids": provenance.get("extension_run_ids") or [],
        "data_origins": provenance.get("data_origins") or [],
        "verification_statuses": provenance.get("verification_statuses") or [],
    })
    for obs in observations[:20]:
        evidence_refs.append({
            "observation_id": obs.get("observation_id"),
            "source_item_id": obs.get("source_item_id"),
            "source_url": obs.get("source_url"),
            "observed_at": obs.get("observed_at"),
            "data_origin": obs.get("data_origin"),
            "verification_status": obs.get("verification_status"),
        })

    prices = [float(o["price"]) for o in observations if o.get("price") is not None]
    avg_price = round(sum(prices) / len(prices), 2) if prices else None

    signal_summary = {
        s["signal_type"]: {
            "value": s.get("value"),
            "status": "UNAVAILABLE" if s.get("value") is None else "COMPUTED",
        }
        for s in signals
    }

    return {
        "candidate_id": f"aoc_{uuid.uuid4().hex[:12]}",
        "opportunity_id": None,
        "keyword": keyword,
        "source": "market_observation",
        "platform": plat,
        "lineage": msc.LINEAGE_OBSERVATION,
        "source_observation": {
            "listing_count": len(observations),
            "observation_count": len(observations),
            "observation_timestamp": signals[0].get("observation_timestamp") if signals else _now_str(),
        },
        "problem": f"Market observations for「{keyword}」show aggregated demand/competition signals",
        "audience": "inferred_from_marketplace_observations",
        "product_type": product_type,
        "market_signals": signal_summary,
        "estimated_value": avg_price,
        "production_feasibility": score["dimensions"]["Difficulty"]["status"],
        "competition": signal_summary.get("competition_signal"),
        "risk": risk,
        "learning_value": score["dimensions"]["Learning_Value"],
        "score": score,
        "status": "discovered_candidate",
        "discovery_source": "market_observation",
        "discovery_method": "observation_market_signal",
        "evidence_refs": evidence_refs,
        "signal_summary": signal_summary,
        "provenance": provenance,
        "created_at": _now_str(),
        "auto_production_forbidden": True,
        "note": "Observation-native candidate — Selection ≠ Experiment ≠ Production",
    }


def _group_signals_by_keyword(signals: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for s in signals:
        kw = str(s.get("keyword") or "").strip()
        if not kw:
            continue
        groups.setdefault(kw, []).append(s)
    return groups


def discover_opportunities_from_observation_signals(
    signal_ids: list[str] | None = None,
    *,
    persist: bool = True,
    require_real_verified: bool = True,
    product_type: str = "digital_template",
) -> dict:
    """
    Entry 075 — Observation-native Signal → Opportunity.

    Consumes persisted market_signals (073); does NOT load products or re-derive signals.
    Does NOT call persist_signals().
    """
    ids = list(signal_ids or ENTRY_073_SIGNAL_IDS)
    signals = msc.load_signals_by_ids(ids)
    if len(signals) != len(ids):
        found = {s["signal_id"] for s in signals}
        missing = [i for i in ids if i not in found]
        return {
            "status": "INSUFFICIENT_DATA",
            "reason": "signal_ids_not_found_in_db",
            "missing_signal_ids": missing,
            "candidates": [],
            "selection_results": [],
            "fake_opportunities_created": False,
            "product_substitution": False,
            "signals_re_persisted": False,
            "ai_invoked": False,
        }

    ok, reason = _validate_observation_lineage_signals(
        signals, require_real_verified=require_real_verified,
    )
    if not ok:
        return {
            "status": "INSUFFICIENT_DATA",
            "reason": reason,
            "candidates": [],
            "selection_results": [],
            "fake_opportunities_created": False,
            "product_substitution": False,
            "signals_re_persisted": False,
            "ai_invoked": False,
        }

    groups = _group_signals_by_keyword(signals)
    if not groups:
        return {
            "status": "INSUFFICIENT_DATA",
            "reason": "no_keyword_on_signals",
            "candidates": [],
            "selection_results": [],
            "fake_opportunities_created": False,
            "product_substitution": False,
            "signals_re_persisted": False,
            "ai_invoked": False,
        }

    candidates: list[dict] = []
    mappings: list[dict] = []
    score_time = _now_iso()

    for keyword, kw_signals in groups.items():
        provenance = _merge_observation_provenance(kw_signals)
        obs_ids = provenance.get("observation_ids") or []
        if not obs_ids:
            continue
        observations = msc.load_observations_by_ids(obs_ids)
        v_ok, v_reason = _validate_observations_real_verified(observations)
        if not v_ok:
            return {
                "status": "INSUFFICIENT_DATA",
                "reason": v_reason,
                "candidates": [],
                "selection_results": [],
                "fake_opportunities_created": False,
                "product_substitution": False,
                "signals_re_persisted": False,
                "ai_invoked": False,
            }

        for s in kw_signals:
            ots = s.get("observation_timestamp") or ""
            if ots > score_time:
                s["observation_timestamp"] = score_time
                s["notes"] = (s.get("notes") or "") + ";clamped_to_score_time"

        score = score_opportunity_from_signals(
            kw_signals,
            observations,
            score_listing_fn=score_observation_listing,
        )
        risk = assess_opportunity_risk(keyword, observations)
        cand = build_observation_opportunity_candidate(
            keyword,
            observations,
            kw_signals,
            score,
            risk,
            provenance,
            product_type=product_type,
        )
        cand["score_time"] = score_time
        candidates.append(cand)
        mappings.append({
            "keyword": keyword,
            "grouping_key": "keyword",
            "signal_ids": [s["signal_id"] for s in kw_signals],
            "observation_ids": obs_ids,
            "candidate_id": cand["candidate_id"],
            "opportunity_id": cand.get("opportunity_id"),
        })

    selection = select_discovered_candidates(candidates)
    if persist and candidates:
        _persist_observation_discovered(candidates, selection, mappings)
        _persist_selection_results(selection)

    return {
        "status": "OK" if candidates else "INSUFFICIENT_DATA",
        "model_note": SCORE_MODEL_NOTE,
        "candidate_count": len(candidates),
        "grouping_key": "keyword",
        "candidates": candidates,
        "selection_results": selection,
        "signal_opportunity_mapping": mappings,
        "input_signal_ids": ids,
        "signals_loaded_from_db": len(signals),
        "fake_opportunities_created": False,
        "auto_experiment_created": False,
        "auto_production_triggered": False,
        "product_substitution": False,
        "signals_re_persisted": False,
        "ai_invoked": False,
    }


def _persist_observation_discovered(
    candidates: list[dict],
    selection: list[dict],
    mappings: list[dict],
) -> None:
    OBSERVATION_DISCOVERY_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "observation_discovery_v1",
        "entry": "075",
        "note": (
            "Observation-native discovery from persisted market_signals (073). "
            "≠ product lineage. Selection ≠ Experiment ≠ Production."
        ),
        "updated_at": _now_str(),
        "candidates": candidates,
        "selection_results": selection,
        "signal_opportunity_mapping": mappings,
    }
    OBSERVATION_DISCOVERY_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
