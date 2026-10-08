# 6_EXECUTION/opportunity_to_product_076.py — Entry 076 Opportunity → Product Definition
#
# Evidence-first Product Definition / Draft Product only.
# Does NOT run Entry 055 E2E, Content Factory, Listing, Publish Queue, or AI.
# Does NOT write SQLite products (marketplace listings table).

from __future__ import annotations

import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402

OBSERVATION_DISCOVERY_JSON = (
    ROOT / "commercial_assets" / "opportunity_candidates" / "observation_discovery_v1.json"
)
PRODUCT_DEFINITIONS_JSON = (
    ROOT / "commercial_assets" / "product_definitions" / "product_definitions_v1.json"
)

ENTRY_076_LOCKED_CANDIDATE = "aoc_19399677b7ba"

STATUS_DRAFT = "draft"
OBJECT_TYPE = "product_definition"

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
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now_str()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _db_counts() -> dict[str, int]:
    with sqlite3.connect(config.DB_PATH) as con:
        return {
            t: int(con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
            for t in (
                "market_observations",
                "market_signals",
                "selection_results",
                "products",
            )
        }


def _load_observations(observation_ids: list[str]) -> list[dict]:
    if not observation_ids:
        return []
    with sqlite3.connect(config.DB_PATH) as con:
        con.row_factory = sqlite3.Row
        ph = ",".join("?" * len(observation_ids))
        rows = con.execute(
            f"SELECT * FROM market_observations WHERE observation_id IN ({ph})",
            list(observation_ids),
        ).fetchall()
    by_id = {dict(r)["observation_id"]: dict(r) for r in rows}
    return [by_id[i] for i in observation_ids if i in by_id]


def _load_signals(signal_ids: list[str]) -> list[dict]:
    if not signal_ids:
        return []
    with sqlite3.connect(config.DB_PATH) as con:
        con.row_factory = sqlite3.Row
        ph = ",".join("?" * len(signal_ids))
        rows = con.execute(
            f"SELECT signal_id, signal_type, keyword, source, value, unit, evidence_refs "
            f"FROM market_signals WHERE signal_id IN ({ph})",
            list(signal_ids),
        ).fetchall()
    by_id = {dict(r)["signal_id"]: dict(r) for r in rows}
    return [by_id[i] for i in signal_ids if i in by_id]


def load_opportunity_candidate(
    candidate_id: str,
    *,
    discovery_path: Path | None = None,
) -> dict | None:
    data = _load_json(discovery_path or OBSERVATION_DISCOVERY_JSON, {})
    for c in data.get("candidates") or []:
        if c.get("candidate_id") == candidate_id:
            return dict(c)
    return None


def load_selection_for_candidate(
    candidate_id: str,
    *,
    discovery_path: Path | None = None,
) -> dict | None:
    data = _load_json(discovery_path or OBSERVATION_DISCOVERY_JSON, {})
    for s in data.get("selection_results") or []:
        if s.get("candidate_id") == candidate_id and s.get("selected"):
            return dict(s)
    # Fallback: DB selection_results
    with sqlite3.connect(config.DB_PATH) as con:
        con.row_factory = sqlite3.Row
        row = con.execute(
            "SELECT * FROM selection_results WHERE candidate_id=? AND selected=1 "
            "ORDER BY id DESC LIMIT 1",
            (candidate_id,),
        ).fetchone()
    return dict(row) if row else None


def find_existing_product_by_opportunity(
    source_opportunity_id: str,
    *,
    store_path: Path | None = None,
) -> dict | None:
    store = _load_json(
        store_path or PRODUCT_DEFINITIONS_JSON,
        {"schema": "product_definitions_v1", "product_definitions": []},
    )
    for p in store.get("product_definitions") or []:
        if p.get("source_opportunity_id") == source_opportunity_id:
            return dict(p)
    return None


def _validate_lineage(candidate: dict) -> tuple[bool, str, dict]:
    prov = dict(candidate.get("provenance") or {})
    signal_ids = list(prov.get("signal_ids") or [])
    observation_ids = list(prov.get("observation_ids") or [])
    if not signal_ids:
        return False, "missing_signal_ids_in_provenance", {}
    if not observation_ids:
        return False, "missing_observation_ids_in_provenance", {}

    signals = _load_signals(signal_ids)
    if len(signals) != len(signal_ids):
        found = {s["signal_id"] for s in signals}
        missing = [i for i in signal_ids if i not in found]
        return False, f"signals_missing_in_db:{missing}", {}

    for s in signals:
        if s.get("source") != "market_observation":
            return False, f"signal_not_observation_lineage:{s.get('signal_id')}", {}

    observations = _load_observations(observation_ids)
    if len(observations) != len(observation_ids):
        found = {o["observation_id"] for o in observations}
        missing = [i for i in observation_ids if i not in found]
        return False, f"observations_missing_in_db:{missing}", {}

    for o in observations:
        if o.get("data_origin") != "REAL":
            return False, f"observation_not_REAL:{o.get('observation_id')}", {}
        if o.get("verification_status") != "MANUAL_VERIFIED":
            return False, f"observation_not_MANUAL_VERIFIED:{o.get('observation_id')}", {}

    return True, "ok", {
        "signals": signals,
        "observations": observations,
        "provenance": prov,
    }


def _field(value: Any, classification: str, *, note: str = "") -> dict:
    out = {"value": value, "classification": classification}
    if note:
        out["note"] = note
    return out


def build_product_definition(
    candidate: dict,
    *,
    selection: dict | None,
    signals: list[dict],
    observations: list[dict],
    provenance: dict,
) -> dict:
    """Build Evidence-first Product Definition — not Opportunity rename."""
    keyword = candidate.get("keyword")
    product_type = candidate.get("product_type") or "digital_template"

    # Observed metrics — preserve NULL (do not coerce)
    observed_metrics = []
    for o in observations:
        observed_metrics.append({
            "observation_id": o.get("observation_id"),
            "source_item_id": o.get("source_item_id"),
            "source_url": o.get("source_url"),
            "want_count": o.get("want_count"),  # may be None
            "view_count": o.get("view_count"),  # may be None
            "comment_count": o.get("comment_count"),
            "share_count": o.get("share_count"),
            "price": o.get("price"),
            "observed_at": o.get("observed_at"),
            "data_origin": o.get("data_origin"),
            "verification_status": o.get("verification_status"),
            # Third-party titles are market evidence, NOT our product content
            "observed_marketplace_title": o.get("title"),
            "title_role": "THIRD_PARTY_MARKETPLACE_LISTING_NOT_OWN_PRODUCT",
        })

    signal_summary = {
        s["signal_type"]: {
            "signal_id": s.get("signal_id"),
            "value": s.get("value"),
            "unit": s.get("unit"),
        }
        for s in signals
    }

    evidence_classification = {
        "DIRECT_EVIDENCE": [
            "keyword",
            "observed_metrics",
            "source_observation_ids",
            "source_signal_ids",
            "source_item_ids",
            "collection_run_ids",
            "session_ids",
            "extension_run_ids",
            "data_origin",
            "verification_status",
            "source_urls",
            "observed_at",
        ],
        "DERIVED": [
            "product_type_digital_template",
            "market_class_excel_template",
            "opportunity_score_from_075",
        ],
        "UNKNOWN": [
            "specific_template_subtype",
            "specific_template_content",
            "target_user_persona",
            "deliverable_file_content",
            "feature_list",
            "product_positioning_copy",
            "marketing_title",
            "marketing_description",
            "differentiated_selling_points",
            "final_listing_price",
        ],
    }

    product_definition = {
        "market_class": _field(
            keyword,
            "DIRECT_EVIDENCE",
            note="Search/query keyword from Observation notes — market class only",
        ),
        "product_type": _field(
            product_type,
            "DERIVED",
            note="From Opportunity product_type default; not a specific template design",
        ),
        "specific_template_subtype": _field(
            None,
            "UNKNOWN",
            note="Excel模板 ≠ 考勤/进销存/财务/人事 — subtype not evidenced",
        ),
        "specific_template_content": _field(None, "UNKNOWN"),
        "target_user_persona": _field(None, "UNKNOWN"),
        "deliverable_file_content": _field(None, "UNKNOWN"),
        "feature_list": _field(None, "UNKNOWN"),
        "marketing_title": _field(None, "UNKNOWN"),
        "marketing_description": _field(None, "UNKNOWN"),
        "differentiated_selling_points": _field(None, "UNKNOWN"),
        "observed_marketplace_evidence": _field(
            observed_metrics,
            "DIRECT_EVIDENCE",
            note="Competitor/marketplace listings — not own product content",
        ),
        "market_signals_summary": _field(signal_summary, "DERIVED"),
        "opportunity_score": _field(
            (candidate.get("score") or {}).get("total_score"),
            "DERIVED",
            note="075 Opportunity score — not commercial success",
        ),
    }

    evidence_refs: list[dict] = [
        {
            "source_opportunity_id": candidate.get("candidate_id"),
            "source_selection_id": (selection or {}).get("selection_id"),
            "lineage": "market_observation",
        }
    ]
    for s in signals:
        evidence_refs.append({
            "signal_id": s.get("signal_id"),
            "signal_type": s.get("signal_type"),
            "value": s.get("value"),
        })
    for o in observations:
        evidence_refs.append({
            "observation_id": o.get("observation_id"),
            "source_item_id": o.get("source_item_id"),
            "source_url": o.get("source_url"),
            "observed_at": o.get("observed_at"),
            "data_origin": o.get("data_origin"),
            "verification_status": o.get("verification_status"),
            "want_count": o.get("want_count"),
            "view_count": o.get("view_count"),
            "price": o.get("price"),
        })

    product_id = f"prod_{uuid.uuid4().hex[:12]}"
    return {
        "product_id": product_id,
        "object_type": OBJECT_TYPE,
        "product_status": STATUS_DRAFT,
        "product_type": product_type,
        "product_category": keyword,
        "product_definition": product_definition,
        "evidence_classification": evidence_classification,
        "source_opportunity_id": candidate.get("candidate_id"),
        "source_selection_id": (selection or {}).get("selection_id"),
        "source_signal_ids": list(provenance.get("signal_ids") or []),
        "source_observation_ids": list(provenance.get("observation_ids") or []),
        "provenance": {
            "lineage": provenance.get("lineage") or "market_observation",
            "signal_ids": list(provenance.get("signal_ids") or []),
            "observation_ids": list(provenance.get("observation_ids") or []),
            "source_item_ids": list(provenance.get("source_item_ids") or []),
            "collection_run_ids": list(provenance.get("collection_run_ids") or []),
            "session_ids": list(provenance.get("session_ids") or []),
            "extension_run_ids": list(provenance.get("extension_run_ids") or []),
            "data_origins": list(provenance.get("data_origins") or []),
            "verification_statuses": list(provenance.get("verification_statuses") or []),
        },
        "evidence_refs": evidence_refs,
        "created_at": _now_iso(),
        "entry": "076",
        "creation_method": "opportunity_to_product_definition_076",
        "auto_production_forbidden": True,
        "publish_forbidden": True,
        "content_factory_forbidden": True,
        "e2e_055_forbidden": True,
        "commercial_learning": "NOT_EXECUTED",
        "commercial_success": False,
        "published": False,
        "ai_invoked": False,
        "note": (
            "Evidence-first Product Definition / Draft Product. "
            "≠ Opportunity rename. ≠ Content Factory asset. ≠ Published. "
            "Specific template content UNKNOWN."
        ),
    }


def persist_product_definition(
    product: dict,
    *,
    store_path: Path | None = None,
) -> dict:
    path = store_path or PRODUCT_DEFINITIONS_JSON
    store = _load_json(
        path,
        {
            "schema": "product_definitions_v1",
            "entry": "076",
            "note": (
                "Evidence-first Product Definitions from Observation-lineage Opportunities. "
                "≠ product_assets (CF files). ≠ commercial_products. ≠ marketplace products table."
            ),
            "product_definitions": [],
        },
    )
    items = list(store.get("product_definitions") or [])
    oid = product.get("source_opportunity_id")
    replaced = False
    for i, it in enumerate(items):
        if oid and it.get("source_opportunity_id") == oid:
            # Soft dedupe by opportunity — keep first product_id if re-run updates
            merged = {**it, **product, "product_id": it.get("product_id") or product["product_id"]}
            items[i] = merged
            product = merged
            replaced = True
            break
    if not replaced:
        items.append(product)
    store["product_definitions"] = items
    store["product_definition_count"] = len(items)
    store["schema"] = "product_definitions_v1"
    store["entry"] = "076"
    _save_json(path, store)
    return {
        "persisted": True,
        "replaced_existing": replaced,
        "path": str(path),
        "product_id": product["product_id"],
    }


def productize_opportunity(
    candidate_id: str = ENTRY_076_LOCKED_CANDIDATE,
    *,
    persist: bool = True,
    discovery_path: Path | None = None,
    store_path: Path | None = None,
) -> dict:
    """
    Formal Entry 076 entry:
    Opportunity Candidate → Evidence-first Product Definition (draft).
    """
    before = _db_counts()
    existing = find_existing_product_by_opportunity(candidate_id, store_path=store_path)

    candidate = load_opportunity_candidate(candidate_id, discovery_path=discovery_path)
    if not candidate:
        return {
            "status": "BLOCKED",
            "reason": "opportunity_candidate_not_found",
            "candidate_id": candidate_id,
            "db_before": before,
            "db_after": before,
            "ai_provider_calls": 0,
            "ai_cost": 0,
        }

    selection = load_selection_for_candidate(candidate_id, discovery_path=discovery_path)
    ok, reason, packed = _validate_lineage(candidate)
    if not ok:
        return {
            "status": "BLOCKED",
            "reason": reason,
            "candidate_id": candidate_id,
            "db_before": before,
            "db_after": before,
            "ai_provider_calls": 0,
            "ai_cost": 0,
        }

    if existing and persist:
        after = _db_counts()
        return {
            "status": "OK",
            "idempotent_reuse": True,
            "product": existing,
            "product_id": existing.get("product_id"),
            "product_status": existing.get("product_status"),
            "product_storage": str(store_path or PRODUCT_DEFINITIONS_JSON),
            "candidate_id": candidate_id,
            "selection_id": (selection or {}).get("selection_id") or existing.get("source_selection_id"),
            "db_before": before,
            "db_after": after,
            "deltas": {k: after[k] - before[k] for k in before},
            "ai_provider_calls": 0,
            "ai_cost": 0,
            "external_action": "NONE",
            "commercial_learning": "NOT_EXECUTED",
            "publish": "NOT_EXECUTED",
            "sqlite_products_written": False,
            "findings": ["PRODUCT_IDEMPOTENCY_GAP: soft dedupe by source_opportunity_id only"],
            "product_substitution": False,
            "ai_invoked": False,
        }

    product = build_product_definition(
        candidate,
        selection=selection,
        signals=packed["signals"],
        observations=packed["observations"],
        provenance=packed["provenance"],
    )

    persist_info = None
    if persist:
        persist_info = persist_product_definition(product, store_path=store_path)

    after = _db_counts()
    return {
        "status": "OK",
        "idempotent_reuse": False,
        "product": product,
        "product_id": product["product_id"],
        "product_status": product["product_status"],
        "product_storage": str(store_path or PRODUCT_DEFINITIONS_JSON),
        "persist": persist_info,
        "candidate_id": candidate_id,
        "selection_id": (selection or {}).get("selection_id"),
        "db_before": before,
        "db_after": after,
        "deltas": {k: after[k] - before[k] for k in before},
        "ai_provider_calls": 0,
        "ai_cost": 0,
        "external_action": "NONE",
        "commercial_learning": "NOT_EXECUTED",
        "publish": "NOT_EXECUTED",
        "sqlite_products_written": False,
        "findings": [
            "PRODUCT_IDEMPOTENCY_GAP: soft dedupe by source_opportunity_id; no hard unique constraint"
        ],
        "product_substitution": False,
        "ai_invoked": False,
    }


if __name__ == "__main__":
    result = productize_opportunity(persist=True)
    print(json.dumps({
        "status": result.get("status"),
        "product_id": result.get("product_id"),
        "product_status": result.get("product_status"),
        "deltas": result.get("deltas"),
        "reason": result.get("reason"),
    }, ensure_ascii=False, indent=2))
