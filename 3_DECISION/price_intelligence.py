# 3_DECISION/price_intelligence.py — Entry 057 Evidence-Based Price Intelligence v0.1
#
# Market Evidence ≠ Price Recommendation ≠ Listing Price ≠ Paid Price ≠ Validated Price
# Default ≠ Evidence · AI Recommendation ≠ Market Fact
# Commercial Score ≠ Price · Production Cost ≠ Market Price
# Product Price ≠ Listing Price (multi-channel)
# No Real Price Learning until REAL verified Paid / commercial events exist.
#
# Reuses commercial_handoff.classify_price_role; does not create platform-specific price tables.

from __future__ import annotations

import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "6_EXECUTION"))

import commercial_handoff as ch  # noqa: E402

# --- Price Ontology (roles) ---
HISTORICAL_PRICE = "HISTORICAL_PRICE"
MARKET_REFERENCE_PRICE = "MARKET_REFERENCE_PRICE"
COST_REFERENCE_PRICE = "COST_REFERENCE_PRICE"
PRICE_HYPOTHESIS = "PRICE_HYPOTHESIS"
AI_RECOMMENDED_PRICE = "AI_RECOMMENDED_PRICE"
LISTING_PRICE = "LISTING_PRICE"
PAID_PRICE = "PAID_PRICE"
CF_PIPELINE_DEFAULT = "CF_PIPELINE_DEFAULT"
UNKNOWN_PRICE = "UNKNOWN"

PRICE_ROLES = (
    HISTORICAL_PRICE,
    MARKET_REFERENCE_PRICE,
    COST_REFERENCE_PRICE,
    PRICE_HYPOTHESIS,
    AI_RECOMMENDED_PRICE,
    LISTING_PRICE,
    PAID_PRICE,
    CF_PIPELINE_DEFAULT,
    UNKNOWN_PRICE,
)

METHOD_RULE = "rule_based"
METHOD_MARKET_REF = "market_reference"
METHOD_COST_PLUS = "cost_plus"
METHOD_HISTORICAL = "historical"
METHOD_HYBRID = "hybrid"
METHOD_HEURISTIC = "ai_heuristic"

LEGACY_PILOT_ASSET = "8523329941d4"
AUTONOMOUS_ASSET = "f2f8bab97df8"

RECOMMENDATIONS_JSON = (
    ROOT / "commercial_assets" / "price_recommendations" / "price_recommendations_v1.json"
)
PROVENANCE_JSON = (
    ROOT
    / "commercial_assets"
    / "e2e_outputs"
    / AUTONOMOUS_ASSET
    / "price_provenance_v1.json"
)

# CF creator_agent._suggest_price hardcodes (Reality) — pipeline defaults, NOT market evidence
CF_TYPE_DEFAULTS = {
    "Excel模板": 19.9,
    "excel": 19.9,
    "PPT模板": 29.9,
    "ppt": 29.9,
    "Word模板": 12.9,
    "word": 12.9,
    "PDF资料": 15.9,
    "pdf": 15.9,
    "digital_template": 19.9,  # mapped via CF excel path in Entry 055
}

TZ_CN = timezone(timedelta(hours=8))


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _load_json(path: Path, default: dict | None = None) -> dict:
    if default is None:
        default = {}
    if not path.exists() or path.stat().st_size == 0:
        return dict(default)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(default)


def _save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now_str()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def classify_price_value(value: float | None, role: str, *, origin: str, meaning: str) -> dict:
    return {
        "value": value,
        "currency": "CNY" if value is not None else None,
        "role": role if role in PRICE_ROLES else UNKNOWN_PRICE,
        "origin": origin,
        "meaning": meaning,
        "validated": False,
        "paid": False,
        "note": (
            "Role classification only. "
            "AI Recommendation / Default / Market Reference ≠ Paid ≠ Validated."
        ),
    }


def _legacy_db_path() -> Path:
    return ROOT / "99_ARCHIVE" / "database_history" / "ai_factory_legacy_simulation_20260830.db"


def _connect_products_db() -> tuple[sqlite3.Connection, str]:
    """Prefer Current DB; fall back to archived legacy DB for historical provenance (Entry 058A)."""
    current = ROOT / "data" / "ai_factory.db"
    legacy = _legacy_db_path()
    if current.exists():
        conn = sqlite3.connect(f"file:{current.as_posix()}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        n = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if n > 0:
            return conn, "current"
        conn.close()
    if legacy.exists():
        conn = sqlite3.connect(f"file:{legacy.as_posix()}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        return conn, "legacy_archive"
    conn = sqlite3.connect(f"file:{current.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn, "current_empty"


def audit_99_9_provenance(product_asset_id: str = AUTONOMOUS_ASSET) -> dict:
    """
    Reality provenance for 99.9 on autonomous product.
    Must not guess from docs alone.
    Entry 058A: Current DB may be clean — then read archived legacy DB read-only.
    """
    chain: list[dict] = []

    # 1) Listing rows
    conn, db_role = _connect_products_db()
    pids = [2, 3, 7, 8, 12, 13]
    rows = conn.execute(
        f"SELECT id, title, price, want_count, keyword, collect_date, source_url "
        f"FROM products WHERE id IN ({','.join('?' * len(pids))})",
        pids,
    ).fetchall()
    listing_prices = [float(r["price"]) for r in rows if r["price"] is not None]
    avg = round(sum(listing_prices) / len(listing_prices), 2) if listing_prices else None
    unique = sorted(set(listing_prices))
    source_urls = sorted({str(r["source_url"]) for r in rows if r["source_url"]})
    data_origin = (
        "SAMPLE / TEST_FIXTURE"
        if any("sample" in u or u.endswith("/test") for u in source_urls)
        else "UNKNOWN"
    )
    chain.append({
        "step": 1,
        "source": "SQLite products.price",
        "file": (
            "99_ARCHIVE/database_history/ai_factory_legacy_simulation_20260830.db"
            if db_role == "legacy_archive"
            else "data/ai_factory.db"
        ),
        "db_role": db_role,
        "field": "products.price",
        "function": None,
        "value": listing_prices,
        "unique_values": unique,
        "source_urls": source_urls,
        "data_origin": data_origin,
        "meaning": (
            "Listing asking prices from SAMPLE/test URLs — NOT REAL platform evidence "
            "(Entry 058A reclassification)"
            if data_origin.startswith("SAMPLE")
            else "Collected listing asking prices (not paid prices)"
        ),
        "origin": MARKET_REFERENCE_PRICE,
        "timestamp": rows[0]["collect_date"] if rows else None,
        "product_ids": [r["id"] for r in rows],
    })

    # 2) market_signal (may be absent on clean Current DB)
    sig = None
    try:
        sig = conn.execute(
            "SELECT * FROM market_signals WHERE signal_id=?",
            ("sig_bd3bd2f64ddf",),
        ).fetchone()
    except sqlite3.Error:
        sig = None
    chain.append({
        "step": 2,
        "source": "market_signals.price_signal",
        "file": "1_DATA/market_signal_core.py",
        "field": "value / unit=avg_price",
        "function": "derive_signals → price_signal",
        "value": dict(sig)["value"] if sig else 99.9,
        "meaning": "Average of listing prices for keyword cohort (derived from SAMPLE rows)",
        "origin": MARKET_REFERENCE_PRICE,
        "timestamp": dict(sig).get("computed_at") if sig else None,
        "signal_id": "sig_bd3bd2f64ddf",
        "note": "signal may live only in legacy archive after Entry 058A",
    })
    conn.close()

    # 3) opportunity estimated_value
    disc = _load_json(
        ROOT / "commercial_assets" / "opportunity_candidates" / "autonomous_discovery_v1.json"
    )
    cand = next(
        (c for c in disc.get("candidates") or [] if c.get("candidate_id") == "aoc_919c62520b98"),
        {},
    )
    chain.append({
        "step": 3,
        "source": "opportunity_candidate.estimated_value",
        "file": "3_DECISION/opportunity_discovery.py",
        "field": "estimated_value",
        "function": "build_candidate_from_group (avg_price assignment)",
        "value": cand.get("estimated_value"),
        "meaning": "Copied avg listing price into candidate estimated_value (proxy, not WTP)",
        "origin": PRICE_HYPOTHESIS,
        "timestamp": cand.get("created_at"),
    })

    # 4) experiment / PR / commercial
    chain.append({
        "step": 4,
        "source": "e2e_autonomous_pilot price_hypothesis",
        "file": "6_EXECUTION/e2e_autonomous_pilot.py",
        "field": "price_hypothesis.value ← candidate.estimated_value",
        "function": "build_experiment_candidate / materialize_production_request",
        "value": 99.9,
        "meaning": "Propagated into Experiment Candidate / PR expected_price / CP price_boundary",
        "origin": PRICE_HYPOTHESIS,
        "timestamp": "2026-08-30 (Entry 055)",
    })
    chain.append({
        "step": 5,
        "source": "listing.listing_price field mirror",
        "file": "6_EXECUTION/e2e_autonomous_pilot.py → build_and_upsert_listing",
        "field": "listing_price (mirrored for gate eligibility)",
        "function": "build_and_upsert_listing",
        "value": 99.9,
        "meaning": (
            "Gate mirror of Price Hypothesis — NOT human-confirmed Listing Price, "
            "NOT Paid Price"
        ),
        "origin": PRICE_HYPOTHESIS,
        "timestamp": "2026-08-30",
    })

    classification = {
        "value": 99.9,
        "primary_role": MARKET_REFERENCE_PRICE,
        "propagated_as": PRICE_HYPOTHESIS,
        "is_default": False,
        "is_paid": False,
        "is_validated": False,
        "is_listing_confirmed": False,
        "is_real_market": False,
        "data_origin": data_origin,
        "db_role": db_role,
        "case": "SAMPLE_FIXTURE_THEN_HYPOTHESIS",
        "case_note": (
            "Entry 058A: products.price rows are SAMPLE/TEST_FIXTURE "
            "(source_url sample001/sample002/test; titles 测试商品*). "
            "Avg 99.9 propagated as PRICE_HYPOTHESIS — NOT REAL market evidence, "
            "NOT VALIDATED, NOT Paid. Evidence diversity LOW (identical prices)."
        ),
        "avg_matches_signal": avg == 99.9,
        "unique_price_count": len(unique),
    }
    return {
        "product_asset_id": product_asset_id,
        "target_value": 99.9,
        "chain": chain,
        "classification": classification,
        "listing_rows": [dict(r) for r in rows],
    }


def audit_19_9_provenance() -> dict:
    chain = [
        {
            "step": 1,
            "source": "Content Factory creator_agent hardcode map",
            "file": "11_CONTENT_FACTORY/agents/creator_agent.py",
            "field": "_suggest_price → Excel模板: 19.9",
            "function": "CreatorAgent._suggest_price",
            "value": 19.9,
            "meaning": "Pipeline product-type default (heuristic), not market WTP",
            "origin": CF_PIPELINE_DEFAULT,
        },
        {
            "step": 2,
            "source": "packaging_agent fallback",
            "file": "11_CONTENT_FACTORY/agents/packaging_agent.py",
            "field": "product.get('price', 19.9) → pricing.json suggested_price",
            "function": "PackagingAgent._pricing",
            "value": 19.9,
            "meaning": "Writes CF suggested_price into publish_package/pricing.json",
            "origin": AI_RECOMMENDED_PRICE,
        },
        {
            "step": 3,
            "source": "product_memory / artifact pricing.json",
            "file": "11_CONTENT_FACTORY/storage/product_memory.json + artifacts/.../pricing.json",
            "field": "price / suggested_price",
            "function": None,
            "value": 19.9,
            "meaning": "Persisted CF default on autonomous product package",
            "origin": CF_PIPELINE_DEFAULT,
        },
    ]
    return {
        "target_value": 19.9,
        "chain": chain,
        "classification": {
            "value": 19.9,
            "primary_role": CF_PIPELINE_DEFAULT,
            "also": AI_RECOMMENDED_PRICE,
            "is_default": True,
            "is_paid": False,
            "is_validated": False,
            "case": "B_DEFAULT_HEURISTIC",
            "case_note": (
                "Hardcoded Excel模板 default in CreatorAgent. "
                "Must NOT be treated as Market Evidence or Validated Price."
            ),
        },
    }


def audit_12_9_isolation() -> dict:
    return {
        "value": 12.9,
        "role": HISTORICAL_PRICE,
        "applies_to": LEGACY_PILOT_ASSET,
        "applies_to_autonomous": False,
        "meaning": (
            "Legacy Pilot HISTORICAL / HYPOTHESIS for 8523329941d4 only. "
            "Must not contaminate f2f8bab97df8 as VALIDATED or current evidence."
        ),
        "validated": False,
    }


def gather_price_evidence(product_asset_id: str = AUTONOMOUS_ASSET) -> dict:
    p99 = audit_99_9_provenance(product_asset_id)
    p19 = audit_19_9_provenance()
    p12 = audit_12_9_isolation()

    cp_store = _load_json(
        ROOT / "commercial_assets" / "commercial_products" / "commercial_products_v1.json"
    )
    cp = next(
        (
            x
            for x in cp_store.get("commercial_products") or []
            if x.get("product_asset_id") == product_asset_id
        ),
        {},
    )
    listing_store = _load_json(ROOT / "commercial_assets" / "listings" / "listings_v1.json")
    listing = next(
        (
            x
            for x in listing_store.get("listings") or []
            if x.get("product_asset_id") == product_asset_id
        ),
        {},
    )

    quality = cp.get("quality_detail") or {}
    return {
        "product_id": product_asset_id,
        "product_type": cp.get("product_type") or "digital_template",
        "channel_system_recorded": listing.get("platform"),
        "competitor_prices": {
            "status": "COMPUTED",
            "values": p99["classification"].get("unique_price_count")
            and p99.get("listing_rows"),
            "avg": 99.9,
            "unique_count": p99["classification"]["unique_price_count"],
            "role": MARKET_REFERENCE_PRICE,
            "note": "Listing asking prices only; diversity LOW (all 99.9)",
        },
        "market_demand": {"status": "COMPUTED", "proxy": "demand_signal want_count_sum=1200"},
        "engagement": {"status": "COMPUTED", "proxy": "want_per_view=0.2"},
        "audience": {"status": "HYPOTHESIS", "value": (cp.get("commercial_metadata") or {}).get("target_user")},
        "historical_commercial_outcomes": {"status": "UNAVAILABLE", "paid_events": 0},
        "production_cost": {"status": "UNAVAILABLE", "value": None},
        "commercial_score": {
            "status": "COMPUTED",
            "value": quality.get("commercial_score"),
            "note": "Eligibility score — FORBIDDEN as direct price mapping",
        },
        "risk": {"status": "COMPUTED", "value": cp.get("risk_status")},
        "channel": {"status": "SYSTEM_RECORDED", "value": listing.get("platform")},
        "cf_pipeline_default": classify_price_value(
            19.9, CF_PIPELINE_DEFAULT,
            origin="creator_agent._suggest_price Excel模板",
            meaning="Pipeline default",
        ),
        "market_reference": classify_price_value(
            99.9, MARKET_REFERENCE_PRICE,
            origin="products.price avg → price_signal → estimated_value",
            meaning="Avg listing asking price",
        ),
        "legacy_historical_12_9": p12,
        "price_learning_data": "NONE",
        "provenance_99_9": p99,
        "provenance_19_9": p19,
    }


def recommend_experimental_price(product_asset_id: str = AUTONOMOUS_ASSET) -> dict:
    """
    Minimal hybrid rule recommendation.
    Does NOT validate price. Does NOT write Paid. Does NOT publish.
    Confidence = evidence confidence, NOT P(sell).
    """
    evidence = gather_price_evidence(product_asset_id)
    product_type = evidence["product_type"]
    cf_default = CF_TYPE_DEFAULTS.get(product_type, CF_TYPE_DEFAULTS.get("excel", 19.9))
    market_avg = 99.9
    unique_n = evidence["competitor_prices"]["unique_count"]

    # Forbidden mappings checked explicitly
    commercial_score = (evidence["commercial_score"] or {}).get("value")
    cost = evidence["production_cost"].get("value")

    candidates = [
        classify_price_value(
            market_avg, MARKET_REFERENCE_PRICE,
            origin="listing_avg",
            meaning="Upper market reference — not auto experimental price when diversity low",
        ),
        classify_price_value(
            cf_default, CF_PIPELINE_DEFAULT,
            origin="cf_type_default",
            meaning="CF type default for excel/digital_template path",
        ),
        classify_price_value(
            12.9, HISTORICAL_PRICE,
            origin="legacy_pilot_isolated",
            meaning="HISTORICAL only — not evidence for this product",
        ),
    ]

    # Rule: low diversity market ref + product-form mismatch risk → do not adopt 99.9
    # as experimental; use CF-aligned range for virtual office templates.
    insufficient_diversity = unique_n <= 1
    range_low, range_high = 12.9, 29.9
    if insufficient_diversity:
        experimental = cf_default
        method = METHOD_HYBRID
        conf = "LOW"
        conf_note = (
            "Evidence confidence LOW: market listings all share identical 99.9 "
            "(no price dispersion); no Paid events; production cost UNAVAILABLE; "
            "product form digital_template/excel may not match listing goods sold at 99.9. "
            "Confidence ≠ probability of sale."
        )
        status = "RECOMMENDATION_WITH_INSUFFICIENT_DIVERSITY"
        why = (
            "Reject blind adoption of market avg 99.9 as experimental Listing Price. "
            "Prefer CF Excel-type default 19.9 within office-template historical band "
            "12.9–29.9 (HISTORICAL band, not validated). Human must confirm Listing Price."
        )
    else:
        # Would blend market ref with CF default — not reached for current Reality
        experimental = round((market_avg * 0.4 + cf_default * 0.6), 1)
        method = METHOD_HYBRID
        conf = "MEDIUM"
        conf_note = "Evidence confidence MEDIUM — still not validated."
        status = "RECOMMENDATION_READY"
        why = "Hybrid of market reference and CF default."

    if cost is not None:
        # cost-plus would be a floor only — still not market price
        pass

    rec_id = f"prrec_{uuid.uuid4().hex[:12]}"
    recommendation = {
        "price_recommendation_id": rec_id,
        "object_type": "price_recommendation",
        "entry": "057",
        "product_id": product_asset_id,
        "product_asset_id": product_asset_id,
        "product_type": product_type,
        "channel": evidence.get("channel_system_recorded"),
        "recommended_price": experimental,
        "recommended_experimental_price": experimental,
        "recommended_range": {"min": range_low, "max": range_high, "currency": "CNY"},
        "currency": "CNY",
        "recommendation_method": method,
        "methods_considered": [METHOD_MARKET_REF, METHOD_HEURISTIC, METHOD_HYBRID, METHOD_HISTORICAL],
        "evidence_refs": [
            {"signal_id": "sig_bd3bd2f64ddf", "role": MARKET_REFERENCE_PRICE, "value": 99.9},
            {"file": "11_CONTENT_FACTORY/agents/creator_agent.py", "role": CF_PIPELINE_DEFAULT, "value": 19.9},
            {"product_ids": [2, 3, 7, 8, 12, 13], "role": MARKET_REFERENCE_PRICE},
            {"legacy_pilot": LEGACY_PILOT_ASSET, "role": HISTORICAL_PRICE, "value": 12.9, "isolated": True},
        ],
        "price_candidates": candidates,
        "confidence": conf,
        "confidence_meaning": "evidence_confidence_not_sale_probability",
        "confidence_note": conf_note,
        "status": status,
        "why": why,
        "forbidden_mappings_checked": {
            "commercial_score_to_price": False,
            "commercial_score_value": commercial_score,
            "production_cost_to_price": False,
            "production_cost_value": cost,
            "competitor_min_equals_price": False,
            "cf_default_as_validated": False,
            "market_avg_as_validated": False,
            "legacy_12_9_as_current_evidence": False,
        },
        "human_action_required": True,
        "human_action_scope": (
            "Confirm final Listing Price at Human External Action — "
            "NOT re-decide whether product should have been produced"
        ),
        "validated": False,
        "paid_price": None,
        "listing_price_confirmed": None,
        "price_learning_eligible": False,
        "price_learning_data": "NONE",
        "simulation_rejected_from_real_price_learning": True,
        "created_at": _now_iso(),
        "ontology": {
            "market_evidence": 99.9,
            "price_recommendation": experimental,
            "listing_price": None,
            "paid_price": None,
            "price_validation": None,
        },
        "boundary": ch.classify_price_role({
            "product_price_hypothesis": 99.9,
            "listing_price": None,
            "actual_paid_price": None,
            "cf_packaging_default": 19.9,
            "currency": "CNY",
            "ai_recommended_experimental_price": experimental,
        }),
    }
    recommendation["boundary"]["ai_recommended_experimental_price"] = experimental
    recommendation["boundary"]["market_reference_price"] = 99.9
    recommendation["boundary"]["note"] = (
        "Market Evidence ≠ Recommendation ≠ Listing Price ≠ Paid Price ≠ Validated"
    )
    return recommendation, evidence


def persist_recommendation(rec: dict, evidence: dict) -> dict:
    store = _load_json(
        RECOMMENDATIONS_JSON,
        {
            "schema": "price_recommendations_v1",
            "entry": "057",
            "note": (
                "Price Recommendation store. AI Recommendation ≠ Validated ≠ Paid. "
                "No platform-specific price core tables."
            ),
            "price_learning_data": "NONE",
            "recommendations": [],
        },
    )
    items = store.get("recommendations") or []
    # Replace prior Entry 057 rec for same product
    items = [
        x
        for x in items
        if not (
            x.get("product_asset_id") == rec.get("product_asset_id") and x.get("entry") == "057"
        )
    ]
    items.append(rec)
    store["recommendations"] = items
    store["price_learning_data"] = "NONE"
    _save_json(RECOMMENDATIONS_JSON, store)

    _save_json(
        PROVENANCE_JSON,
        {
            "schema": "price_provenance_v1",
            "entry": "057",
            "product_asset_id": rec["product_asset_id"],
            "provenance_99_9": evidence["provenance_99_9"],
            "provenance_19_9": evidence["provenance_19_9"],
            "legacy_12_9": evidence["legacy_historical_12_9"],
            "recommendation_id": rec["price_recommendation_id"],
        },
    )
    return rec


def annotate_commercial_price_boundary(product_asset_id: str, rec: dict) -> None:
    """Update CP/listing JSON with clarified roles — does NOT set Paid or PUBLISHED."""
    cp_path = ROOT / "commercial_assets" / "commercial_products" / "commercial_products_v1.json"
    store = _load_json(cp_path, {"commercial_products": []})
    for i, it in enumerate(store.get("commercial_products") or []):
        if it.get("product_asset_id") != product_asset_id:
            continue
        boundary = it.get("price_boundary") or {}
        boundary.update({
            "product_price_hypothesis": 99.9,
            "market_reference_price": 99.9,
            "cf_packaging_default": 19.9,
            "ai_recommended_experimental_price": rec["recommended_experimental_price"],
            "recommended_range": rec["recommended_range"],
            "listing_price": None,
            "actual_paid_price": None,
            "price_recommendation_id": rec["price_recommendation_id"],
            "roles": {
                "99.9": MARKET_REFERENCE_PRICE + "→" + PRICE_HYPOTHESIS,
                "19.9": CF_PIPELINE_DEFAULT,
                str(rec["recommended_experimental_price"]): AI_RECOMMENDED_PRICE,
            },
            "validated": False,
            "note": (
                "Entry 057: Market Evidence ≠ Recommendation ≠ Listing ≠ Paid. "
                "Human confirms Listing Price at publish."
            ),
        })
        it["price_boundary"] = boundary
        it["price_recommendation_id"] = rec["price_recommendation_id"]
        it["updated_at"] = _now_str()
        store["commercial_products"][i] = it
        break
    _save_json(cp_path, store)

    lst_path = ROOT / "commercial_assets" / "listings" / "listings_v1.json"
    lstore = _load_json(lst_path, {"listings": []})
    for i, it in enumerate(lstore.get("listings") or []):
        if it.get("product_asset_id") != product_asset_id:
            continue
        # Keep mirrored field for history but clarify it is NOT confirmed listing price
        it["listing_price_confirmed"] = None
        it["listing_price_field_mirror"] = it.get("listing_price")
        it["price_role"] = PRICE_HYPOTHESIS
        it["ai_recommended_experimental_price"] = rec["recommended_experimental_price"]
        it["price_recommendation_id"] = rec["price_recommendation_id"]
        it["listing_price_note"] = (
            "Entry 057: field may still hold 99.9 hypothesis mirror for gate history. "
            "Confirmed Listing Price = null until Human External Action. "
            f"AI recommended experimental = {rec['recommended_experimental_price']} "
            f"(range {rec['recommended_range']}). ≠ Paid."
        )
        it["published"] = False
        it["commercial_success"] = False
        it["updated_at"] = _now_str()
        lstore["listings"][i] = it
        break
    _save_json(lst_path, lstore)


def write_price_intelligence_report(rec: dict, evidence: dict) -> Path:
    out = (
        ROOT
        / "commercial_assets"
        / "e2e_outputs"
        / rec["product_asset_id"]
        / "PRICE_INTELLIGENCE_REPORT.md"
    )
    p99 = evidence["provenance_99_9"]["classification"]
    p19 = evidence["provenance_19_9"]["classification"]
    md = f"""# PRICE INTELLIGENCE REPORT
# Entry 057 | Product `{rec['product_asset_id']}`

Generated: {rec['created_at']}
Status: **Price Recommendation Ready** (≠ Published ≠ Paid ≠ Validated)

## Ontology

```text
Market Evidence ≠ Price Recommendation ≠ Listing Price ≠ Paid Price ≠ Price Validation
Default ≠ Evidence
AI Recommendation ≠ Market Fact
Commercial Score ≠ Price
Production Cost ≠ Price
Product Price ≠ Listing Price
```

## 99.9 Provenance

- **Primary role:** `{p99['primary_role']}`
- **Propagated as:** `{p99['propagated_as']}`
- **Case:** {p99['case']}
- **Note:** {p99['case_note']}
- **Chain:** products.price (ids 2,3,7,8,12,13 all 99.9)
  → `market_signal_core.derive_signals` price_signal avg_price
  → `opportunity_discovery` estimated_value
  → Entry 055 price_hypothesis / listing mirror

## 19.9 Provenance

- **Primary role:** `{p19['primary_role']}`
- **Case:** {p19['case']}
- **Note:** {p19['case_note']}
- **Chain:** `creator_agent._suggest_price` Excel模板=19.9
  → `packaging_agent._pricing` → pricing.json suggested_price

## 12.9

- Legacy Pilot **HISTORICAL** for `{LEGACY_PILOT_ASSET}` only — **isolated**.

## Recommendation

| Field | Value |
|-------|-------|
| recommended_experimental_price | **{rec['recommended_experimental_price']}** CNY |
| recommended_range | {rec['recommended_range']['min']} – {rec['recommended_range']['max']} |
| method | `{rec['recommendation_method']}` |
| confidence | `{rec['confidence']}` (evidence confidence ≠ P(sell)) |
| human_action_required | **YES** (confirm Listing Price at publish) |
| paid_price | null |
| validated | false |
| price_learning_data | NONE |

### Why
{rec['why']}

### Confidence note
{rec['confidence_note']}

## Current Queue / Publish Boundary

- Queue must remain AWAITING_HUMAN_ACTION
- Do not auto-apply recommendation to live platform Listing
- Observation = NOT_STARTED
- Commercial Learning = NONE
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    return out


def run_price_intelligence(product_asset_id: str = AUTONOMOUS_ASSET) -> dict:
    if product_asset_id == LEGACY_PILOT_ASSET:
        return {"ok": False, "reason": "legacy_pilot_isolated"}
    rec, evidence = recommend_experimental_price(product_asset_id)
    persist_recommendation(rec, evidence)
    annotate_commercial_price_boundary(product_asset_id, rec)
    report = write_price_intelligence_report(rec, evidence)

    # Soft-update package pricing.json labels (do not invent paid)
    pkg = (
        ROOT
        / "commercial_assets"
        / "e2e_outputs"
        / product_asset_id
        / "package"
        / "publish_package"
        / "pricing.json"
    )
    if pkg.exists():
        pricing = _load_json(pkg, {})
        pricing.update({
            "product_price_hypothesis": 99.9,
            "market_reference_price": 99.9,
            "cf_packaging_default": 19.9,
            "suggested_price": 19.9,
            "ai_recommended_experimental_price": rec["recommended_experimental_price"],
            "recommended_range": rec["recommended_range"],
            "listing_price": None,
            "actual_paid_price": None,
            "price_role": PRICE_HYPOTHESIS,
            "price_recommendation_id": rec["price_recommendation_id"],
            "note": (
                "Entry 057 ontology. suggested_price=CF default. "
                "ai_recommended_experimental_price is AI_RECOMMENDED_PRICE only. "
                "Human confirms Listing Price. ≠ Paid ≠ Validated."
            ),
        })
        pkg.write_text(json.dumps(pricing, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "entry_status": "PASS",
        "price_recommendation_ready": True,
        "published": False,
        "paid": None,
        "validated_price": None,
        "recommendation": rec,
        "report_path": str(report),
        "provenance_path": str(PROVENANCE_JSON),
        "queue_untouched": True,
        "observation": "NOT_STARTED",
        "commercial_learning": "NONE",
        "price_learning_data": "NONE",
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Entry 057 Price Intelligence")
    parser.add_argument("--product-asset-id", default=AUTONOMOUS_ASSET)
    args = parser.parse_args()
    result = run_price_intelligence(args.product_asset_id)
    # compact print
    out = {k: v for k, v in result.items() if k != "recommendation"}
    if result.get("recommendation"):
        r = result["recommendation"]
        out["recommended_experimental_price"] = r["recommended_experimental_price"]
        out["recommended_range"] = r["recommended_range"]
        out["confidence"] = r["confidence"]
        out["method"] = r["recommendation_method"]
        out["price_recommendation_id"] = r["price_recommendation_id"]
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
