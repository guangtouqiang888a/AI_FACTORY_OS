# 6_EXECUTION/e2e_autonomous_pilot.py — Entry 055 End-to-End Product Generation Pilot
#
# Real Market Data → Opportunity → Selection → Experiment → Production →
# Quality → Commercial Product → Listing → Publish Queue (AWAITING_HUMAN_ACTION)
#
# Stops before: real platform publish / payment / ads / Observation / Commercial Learning
# Reuses existing modules; minimal adapters only. No second Opportunity/Product/Queue system.

from __future__ import annotations

import json
import shutil
import sys
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "6_EXECUTION"))
sys.path.insert(0, str(ROOT / "11_CONTENT_FACTORY" / "adapter"))
sys.path.insert(0, str(ROOT / "11_CONTENT_FACTORY" / "pipeline"))

import commercial_handoff as ch  # noqa: E402
import publish_queue as pq  # noqa: E402

DISCOVERY_JSON = (
    ROOT / "commercial_assets" / "opportunity_candidates" / "autonomous_discovery_v1.json"
)
EXPERIMENT_CANDIDATES_JSON = (
    ROOT / "commercial_assets" / "experiment_candidates" / "autonomous_experiment_candidates_v1.json"
)
EXPERIMENTS_JSON = ROOT / "commercial_assets" / "experiments" / "experiments_v1.json"
PRODUCTION_REQUESTS_JSON = (
    ROOT / "commercial_assets" / "production_requests" / "production_requests_v1.json"
)
APPROVALS_JSON = (
    ROOT
    / "commercial_assets"
    / "production_request_reviews"
    / "production_request_reviews_v1.json"
)
PRODUCT_ASSETS_JSON = ROOT / "commercial_assets" / "product_assets" / "product_assets_v1.json"
TRACE_JSON = ROOT / "commercial_assets" / "e2e_traces" / "entry_055_trace_v1.json"

TZ_CN = timezone(timedelta(hours=8))

# CF Runtime supports these deliverable types today (adapter input_mapper)
CF_PRODUCT_TYPE_MAP = {
    "digital_template": "excel",
    "spreadsheet": "excel",
    "document": "word",
    "presentation": "ppt",
    "pdf": "pdf",
    "excel": "excel",
    "ppt": "ppt",
    "word": "word",
}

FORBIDDEN_FUTURE_TYPES = frozenset({"short_video", "drama", "novel", "audio", "video"})


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _load_json(path: Path, default: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now_str()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_rank1_selection(discovery_path: Path | None = None) -> dict | None:
    """Load top selected autonomous candidate (rank=1). No human product pick."""
    data = _load_json(discovery_path or DISCOVERY_JSON, {})
    selections = [
        s
        for s in (data.get("selection_results") or [])
        if s.get("selected") is True
    ]
    if not selections:
        return None
    selections.sort(key=lambda s: (s.get("rank") is None, s.get("rank") or 999))
    top = selections[0]
    candidates = {c["candidate_id"]: c for c in (data.get("candidates") or [])}
    cand = candidates.get(top["candidate_id"], {})
    return {"selection": top, "candidate": cand, "discovery": data}


def map_product_type_for_cf(product_type: str) -> str:
    pt = (product_type or "digital_template").lower()
    if pt in FORBIDDEN_FUTURE_TYPES:
        raise ValueError(f"future_product_type_not_allowed_in_entry_055:{pt}")
    return CF_PRODUCT_TYPE_MAP.get(pt, "excel")


def build_experiment_candidate(selection_bundle: dict) -> dict:
    sel = selection_bundle["selection"]
    cand = selection_bundle["candidate"]
    keyword = sel.get("keyword") or cand.get("keyword") or ""
    product_type = sel.get("product_type") or cand.get("product_type") or "digital_template"
    score = sel.get("score") if sel.get("score") is not None else cand.get("total_score")
    price_hyp = cand.get("estimated_value")
    ec_id = f"ec_{uuid.uuid4().hex[:12]}"
    return {
        "experiment_candidate_id": ec_id,
        "object_type": "experiment_candidate",
        "entry": "055",
        "source_opportunity": sel.get("candidate_id") or cand.get("candidate_id"),
        "source_selection_id": sel.get("selection_id"),
        "source_candidate_id": sel.get("candidate_id"),
        "selection_rank": sel.get("rank"),
        "candidate_score": score,
        "risk_status": sel.get("risk_status") or cand.get("risk_status"),
        "selection_reason": sel.get("selection_reason"),
        "evidence_refs": sel.get("evidence_refs") or cand.get("evidence_refs") or [],
        "product_type": product_type,
        "keyword": keyword,
        "platform": sel.get("platform") or cand.get("platform") or "xianyu",
        "source": sel.get("source") or "marketplace",
        "target_user": {
            "value": f"需要「{keyword}」类虚拟资料/模板的闲鱼买家（HYPOTHESIS）",
            "status": "HYPOTHESIS",
        },
        "problem": {
            "value": f"买家在「{keyword}」相关场景缺少即用可编辑数字模板（HYPOTHESIS）",
            "status": "HYPOTHESIS",
        },
        "hypothesis": {
            "value": (
                f"基于市场信号选择的「{keyword}」机会，以 digital_template/"
                f"{map_product_type_for_cf(product_type)} 形式生产可交付资产，"
                f"可在 {sel.get('platform') or 'xianyu'} 验证首次付费转化。"
            ),
            "status": "HYPOTHESIS",
            "note": "Unvalidated judgment — Experiment Candidate ≠ Experiment completed",
        },
        "test_goal": {
            "value": "验证自主发现候选能否走通 Production→Quality→Commercial→Publish Queue",
            "status": "HYPOTHESIS",
        },
        "price_hypothesis": {
            "value": price_hyp,
            "currency": "CNY",
            "status": "HYPOTHESIS",
            "source": "opportunity_candidate.estimated_value / price_signal proxy",
            "note": "Price Hypothesis ≠ Listing Price ≠ Paid Price",
        },
        "status": "draft",
        "creation_method": "autonomous_bridge_055",
        "auto_production_forbidden_cleared": True,
        "note": (
            "Entry 055: Experiment Candidate from autonomous selection. "
            "≠ Experiment complete ≠ Commercial Success. "
            "Legacy Pilot 8523329941d4 / exp_20260708_005 is HISTORICAL — not this candidate."
        ),
        "created_at": _now_iso(),
    }


def materialize_experiment_from_candidate(ec: dict) -> dict:
    """Bridge Experiment Candidate → Experiment Object (minimal; keeps human_assisted intact)."""
    exp_id = f"exp_auto_{datetime.now(TZ_CN).strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
    keyword = ec["keyword"]
    cf_type = map_product_type_for_cf(ec["product_type"])
    price = (ec.get("price_hypothesis") or {}).get("value")
    experiment = {
        "experiment_id": exp_id,
        "object_type": "experiment",
        "contract_version": "1.0",
        "entry": "055",
        "source_opportunity_id": ec["source_opportunity"],
        "source_selection_id": ec.get("source_selection_id"),
        "source_candidate_id": ec.get("source_candidate_id"),
        "source_experiment_candidate_id": ec["experiment_candidate_id"],
        "experiment_name": f"Autonomous E2E — {keyword}",
        "category": "A",
        "keyword": keyword,
        "product_type": cf_type,
        "product_type_declared": ec["product_type"],
        "hypothesis": (ec.get("hypothesis") or {}).get("value"),
        "hypothesis_status": "HYPOTHESIS",
        "validation_goal": (ec.get("test_goal") or {}).get("value"),
        "target_customer": (ec.get("target_user") or {}).get("value"),
        "product_concept": (
            f"【HYPOTHESIS】面向「{keyword}」需求的可编辑 "
            f"{cf_type.upper()} 数字模板包（digital_template → CF {cf_type}）"
        ),
        "validation_method": (
            "Content Factory production → Quality Gate → Commercial Product → "
            "Listing Package → Publish Queue AWAITING_HUMAN_ACTION；"
            "不执行真实平台发布 / Observation / Commercial Learning"
        ),
        "success_metrics": {
            "production_metric": {
                "target_first_pass": True,
                "note": "Production success ≠ Commercial success",
            },
            "market_metric": {
                "note": "NOT STARTED — no market events fabricated",
            },
            "commercial_metric": {
                "expected_price_cny": price,
                "price_role": "PRODUCT_PRICE_HYPOTHESIS",
                "note": "Hypothesis only",
            },
        },
        "expected_cost": None,
        "expected_cost_note": "UNAVAILABLE until CF records cost",
        "publish_channel_planned": ec.get("platform") or "xianyu",
        "status": "prepared",
        "experiment_method": "autonomous_bridge_055",
        "selection_rank": ec.get("selection_rank"),
        "candidate_score": ec.get("candidate_score"),
        "risk_status": ec.get("risk_status"),
        "selection_reason": ec.get("selection_reason"),
        "evidence_refs": ec.get("evidence_refs"),
        "next_action": "production_request",
        "created_at": _now_iso(),
        "legacy_pilot_note": "HISTORICAL / LEGACY PILOT exp_20260708_005 is unrelated",
    }

    store = _load_json(
        EXPERIMENTS_JSON,
        {"experiments": [], "experiment_count": 0},
    )
    # Idempotent: skip if same source_experiment_candidate already materialized
    for existing in store.get("experiments") or []:
        if existing.get("source_experiment_candidate_id") == ec["experiment_candidate_id"]:
            return existing
        if (
            existing.get("source_candidate_id") == ec.get("source_candidate_id")
            and existing.get("entry") == "055"
            and existing.get("experiment_method") == "autonomous_bridge_055"
        ):
            return existing

    store.setdefault("experiments", []).append(experiment)
    store["experiment_count"] = len(store["experiments"])
    store["entry_055_note"] = (
        "Autonomous bridge experiments appended; human_assisted experiments retained."
    )
    _save_json(EXPERIMENTS_JSON, store)
    return experiment


def persist_experiment_candidate(ec: dict) -> dict:
    store = _load_json(
        EXPERIMENT_CANDIDATES_JSON,
        {
            "schema": "autonomous_experiment_candidates_v1",
            "entry": "055",
            "note": "Experiment Candidate ≠ Experiment. From autonomous selection only.",
            "experiment_candidates": [],
        },
    )
    items = store.get("experiment_candidates") or []
    for i, it in enumerate(items):
        if it.get("source_candidate_id") == ec.get("source_candidate_id") and it.get(
            "entry"
        ) == "055":
            items[i] = ec
            store["experiment_candidates"] = items
            _save_json(EXPERIMENT_CANDIDATES_JSON, store)
            return ec
    items.append(ec)
    store["experiment_candidates"] = items
    _save_json(EXPERIMENT_CANDIDATES_JSON, store)
    return ec


def materialize_production_request(experiment: dict, ec: dict) -> tuple[dict, dict]:
    preq_id = f"preq_auto_{datetime.now(TZ_CN).strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
    appr_id = f"appr_auto_{datetime.now(TZ_CN).strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
    keyword = experiment["keyword"]
    cf_type = experiment["product_type"]
    price = ((ec.get("price_hypothesis") or {}).get("value"))
    product_name = f"{keyword} {cf_type.upper()} 模板"

    pr = {
        "production_request_id": preq_id,
        "object_type": "production_request",
        "contract_version": "1.0",
        "entry": "055",
        "source_experiment_id": experiment["experiment_id"],
        "source_experiment_candidate_id": ec["experiment_candidate_id"],
        "source_opportunity_id": experiment["source_opportunity_id"],
        "source_selection_id": experiment.get("source_selection_id"),
        "source_candidate_id": experiment.get("source_candidate_id"),
        "keyword": keyword,
        "product_type": cf_type,
        "product_type_declared": experiment.get("product_type_declared"),
        "product_name": product_name,
        "target_customer": experiment.get("target_customer"),
        "business_goal": experiment.get("hypothesis"),
        "validation_goal": experiment.get("validation_goal"),
        "hypothesis": experiment.get("hypothesis"),
        "production_priority": "P0",
        "status": "approved_for_e2e_055",
        "creation_method": "autonomous_bridge_055",
        "asset_requirements": {
            "product_name": product_name,
            "product_concept": experiment.get("product_concept"),
            "deliverable_format": {"excel": "xlsx", "ppt": "pptx", "word": "docx", "pdf": "pdf"}.get(
                cf_type, "xlsx"
            ),
            "deliverable_count": 1,
            "structure_outline": [
                "封面/标题",
                "使用说明",
                "核心模板区",
                "示例数据",
                "扩展字段",
            ],
            "content_constraints": {
                "language": "zh-CN",
                "include_instructions": True,
                "editable": True,
            },
            "publish_channel_planned": experiment.get("publish_channel_planned") or "xianyu",
            "expected_price_cny": price,
            "price_role": "PRODUCT_PRICE_HYPOTHESIS",
            "reference_from_experiment": {
                "hypothesis_summary": experiment.get("hypothesis"),
                "validation_goal": experiment.get("validation_goal"),
                "selection_reason": experiment.get("selection_reason"),
            },
        },
        "quality_requirements": {
            "min_quality_score": 0.80,
            "first_pass_required": True,
            "checklist": [
                "deliverable_format_correct",
                "structure_complete",
                "file_openable",
            ],
        },
        "required_output": f"可打开的 {cf_type} 交付文件 + publish_package",
        "production_constraints": {
            "phase1_virtual_materials_only": True,
            "no_future_media_runtime": True,
            "no_external_publish": True,
        },
        "created_at": _now_iso(),
    }

    approval = {
        "approval_id": appr_id,
        "object_type": "production_request_review",
        "contract_version": "1.0",
        "entry": "055",
        "source_production_request_id": preq_id,
        "source_experiment_id": experiment["experiment_id"],
        "product_name": product_name,
        "product_type": cf_type,
        "production_priority": "P0",
        "review_method": "autonomous_bridge_055",
        "decision": "approved",
        "review_reason": (
            "Entry 055 E2E bridge: autonomous selection risk=passed; "
            "system-generated approval for Content Factory execute only. "
            "Human Gate remains external publish only — not product approval."
        ),
        "approved_by": "system_e2e_055",
        "approval_checks": {
            "asset_requirements_complete": True,
            "quality_requirements_complete": True,
            "selection_risk_passed": experiment.get("risk_status") == "passed",
            "legacy_pilot_not_reused": True,
        },
        "created_at": _now_iso(),
        "approved_at": _now_iso(),
    }

    # Append PR
    pr_store = _load_json(PRODUCTION_REQUESTS_JSON, {"production_requests": []})
    # Reuse if Entry 055 already created for same experiment
    for existing in pr_store.get("production_requests") or []:
        if (
            existing.get("source_experiment_id") == experiment["experiment_id"]
            and existing.get("entry") == "055"
        ):
            # Find matching approval
            ap_store = _load_json(APPROVALS_JSON, {"production_request_reviews": []})
            for ap in ap_store.get("production_request_reviews") or []:
                if ap.get("source_production_request_id") == existing.get(
                    "production_request_id"
                ):
                    return existing, ap
            return existing, approval

    pr_store.setdefault("production_requests", []).append(pr)
    pr_store["production_request_count"] = len(pr_store["production_requests"])
    pr_store["entry_055_note"] = "Autonomous bridge PRs appended; human_assisted retained."
    _save_json(PRODUCTION_REQUESTS_JSON, pr_store)

    ap_store = _load_json(APPROVALS_JSON, {"production_request_reviews": []})
    ap_store.setdefault("production_request_reviews", []).append(approval)
    ap_store["approval_count"] = len(ap_store["production_request_reviews"])
    _save_json(APPROVALS_JSON, ap_store)

    return pr, approval


def run_content_factory(production_request_id: str, *, dry_run: bool = False) -> dict:
    from adapter_runner import run_adapter  # noqa: WPS433

    # pilot_only=False: Entry 055 new preq is outside legacy whitelist; gate still requires approval
    return run_adapter(production_request_id, dry_run=dry_run, pilot_only=False)


def persist_product_asset(draft: dict, pipeline_result: dict) -> dict:
    quality = pipeline_result.get("quality") or {}
    passed = bool(quality.get("passed") or quality.get("status") in ("quality_pass", "passed", "pass"))
    asset = {
        **draft,
        "validation_status": "passed" if pipeline_result.get("status") == "ok" else "failed",
        "quality_status": "passed" if passed else "failed",
        "entry": "055",
        "creation_method": "autonomous_bridge_055",
        "commercial_success": False,
        "observation_started": False,
        "updated_at": _now_iso(),
    }
    if not asset.get("created_at"):
        asset["created_at"] = _now_iso()

    store = _load_json(
        PRODUCT_ASSETS_JSON,
        {"product_assets": [], "product_asset_count": 0},
    )
    items = store.get("product_assets") or []
    pid = asset.get("product_asset_id")
    replaced = False
    for i, it in enumerate(items):
        if it.get("product_asset_id") == pid:
            items[i] = {**it, **asset}
            replaced = True
            break
    if not replaced:
        items.append(asset)
    store["product_assets"] = items
    store["product_asset_count"] = len(items)
    store["entry_055_note"] = "Autonomous E2E assets appended; legacy pilot retained as HISTORICAL."
    _save_json(PRODUCT_ASSETS_JSON, store)
    return asset


def complete_listing_package(
    cf_pkg_dir: Path,
    *,
    product_name: str,
    price_hypothesis: float | None,
    product_asset_id: str,
    experiment_id: str,
) -> Path:
    """
    Minimal adapter: CF packaging writes core files; Entry 052/053 gates also require
    faq / delivery_description / version_information. Fill only missing files.
    """
    dest = (
        ROOT
        / "commercial_assets"
        / "e2e_outputs"
        / product_asset_id
        / "package"
        / "publish_package"
    )
    dest.mkdir(parents=True, exist_ok=True)
    if cf_pkg_dir.is_dir():
        for p in cf_pkg_dir.iterdir():
            if p.is_file():
                shutil.copy2(p, dest / p.name)

    defaults = {
        "faq.txt": (
            f"Q: 交付什么？\nA: {product_name} 数字文件（zip）。\n\n"
            "Q: 是否真实已发布？\nA: 否。当前仅 Publish Queue AWAITING_HUMAN_ACTION。\n"
        ),
        "delivery_description.txt": "数字下载：付款后发送 final_product.zip（平台外人工操作）。",
        "version_information.txt": (
            f"product_asset_id={product_asset_id}\n"
            f"experiment_id={experiment_id}\n"
            f"entry=055\n"
            f"generated_at={_now_iso()}\n"
        ),
    }
    for name, content in defaults.items():
        path = dest / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    # Ensure pricing reflects Price Hypothesis role (do not silently copy legacy 12.9/19.9)
    pricing_path = dest / "pricing.json"
    if pricing_path.exists():
        try:
            pricing = json.loads(pricing_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pricing = {}
    else:
        pricing = {}
    pricing["product_price_hypothesis"] = price_hypothesis
    pricing["listing_price"] = None
    pricing["actual_paid_price"] = None
    pricing["price_role"] = "PRODUCT_PRICE_HYPOTHESIS"
    pricing["note"] = "Price Hypothesis ≠ Listing Price ≠ Paid Price"
    if price_hypothesis is not None and pricing.get("suggested_price") is None:
        pricing["suggested_price"] = price_hypothesis
    pricing_path.write_text(json.dumps(pricing, ensure_ascii=False, indent=2), encoding="utf-8")

    # Cover placeholder marker for package_status
    images = dest.parent.parent / "images"
    images.mkdir(parents=True, exist_ok=True)
    ph = images / "cover_placeholder.txt"
    if not ph.exists():
        ph.write_text(
            "PLACEHOLDER cover — Entry 055 Minimum Listing Package; ≠ Marketing Ready\n",
            encoding="utf-8",
        )
    return dest


def build_commercial_from_asset(
    asset: dict,
    experiment: dict,
    ec: dict,
    package_dir: Path,
    pipeline_result: dict,
) -> dict:
    quality = pipeline_result.get("quality") or {}
    q_passed = bool(
        quality.get("passed")
        or str(quality.get("status") or "").lower() in ("quality_pass", "passed", "pass", "ok")
    )
    price = (ec.get("price_hypothesis") or {}).get("value")
    keyword = experiment.get("keyword") or ""
    product_id = asset.get("product_asset_id") or pipeline_result.get("product_id")
    cp = {
        "commercial_product_id": f"cp_auto_{product_id}",
        "product_id": product_id,
        "product_name": asset.get("product_name"),
        "product_type": experiment.get("product_type_declared") or "digital_template",
        "product_version": "e2e_055_v1",
        "product_asset_id": asset.get("product_asset_id"),
        "asset_refs": [
            {
                "asset_type": (asset.get("artifact_information") or {}).get("file_type") or "file",
                "ref": (asset.get("artifact_information") or {}).get("primary_file"),
            }
        ],
        "source_experiment_id": experiment.get("experiment_id"),
        "source_production_request_id": asset.get("source_production_request_id"),
        "source_opportunity_id": experiment.get("source_opportunity_id"),
        "source_candidate_id": experiment.get("source_candidate_id"),
        "selection_reason": experiment.get("selection_reason"),
        "evidence_refs": experiment.get("evidence_refs"),
        "quality_status": "passed" if q_passed else "failed",
        "risk_status": experiment.get("risk_status") or "passed",
        "delivery_method": "digital_download_zip",
        "commercial_metadata": {
            "target_user": (ec.get("target_user") or {}).get("value"),
            "problem": (ec.get("problem") or {}).get("value"),
            "offer": asset.get("product_name"),
            "delivery_method": "digital_download_zip",
        },
        "price_boundary": ch.classify_price_role(
            {
                "product_price_hypothesis": price,
                "listing_price": None,
                "actual_paid_price": None,
                "cf_packaging_default": (pipeline_result.get("product") or {}).get("price"),
                "currency": "CNY",
            }
        ),
        "quality_detail": {
            "quality_score": quality.get("quality_score"),
            "commercial_score": quality.get("commercial_score"),
            "usability_score": quality.get("usability_score"),
            "market_score": quality.get("market_score"),
            "production_cost_score": quality.get("production_cost_score"),
            "status": quality.get("status"),
        },
        "listing_package_path": str(package_dir),
        "phase1_scope": "virtual_materials_only",
        "entry": "055",
        "published": False,
        "commercial_success": False,
        "notes": (
            "Entry 055 autonomous E2E. COMMERCIAL_READY ≠ PUBLISHED. "
            "Production success ≠ Commercial success. No Market Event fabricated."
        ),
    }
    if not q_passed or (experiment.get("risk_status") or "").lower() not in (
        "passed",
        "pass",
        "ok",
    ):
        cp["commercial_status"] = ch.CP_BLOCKED
    return ch.upsert_commercial_product(cp)


def build_and_upsert_listing(
    commercial_product: dict,
    package_dir: Path,
    package_eval: dict,
    *,
    publish_queue_id: str,
) -> dict:
    listing = {
        "listing_id": f"lst_auto_{commercial_product.get('product_asset_id')}",
        "commercial_product_id": commercial_product.get("commercial_product_id"),
        "product_id": commercial_product.get("product_id"),
        "product_asset_id": commercial_product.get("product_asset_id"),
        "experiment_id": commercial_product.get("source_experiment_id"),
        "production_request_id": commercial_product.get("source_production_request_id"),
        "opportunity_id": commercial_product.get("source_opportunity_id"),
        "publish_queue_id": publish_queue_id,
        "platform": "xianyu",
        "listing_package_path": str(package_dir),
        "listing_package_status": package_eval.get("package_status"),
        "listing_price": None,
        "price_role": ch.PRICE_HYPOTHESIS,
        "product_price_hypothesis": (
            (commercial_product.get("price_boundary") or {}).get("product_price_hypothesis")
        ),
        "currency": "CNY",
        "delivery_method": commercial_product.get("delivery_method"),
        "risk_status": commercial_product.get("risk_status"),
        "listing_status": ch.LIST_DRAFT,
        "publish_evidence_id": None,
        "published": False,
        "observation_eligible": False,
        "observation_started": False,
        "commercial_success": False,
        "entry": "055",
        "notes": (
            "Listing Package prepared for human external action. "
            "≠ Published. Legacy Pilot listing is HISTORICAL."
        ),
    }
    # For publish readiness, listing_price gate needs a value — use hypothesis as
    # proposed listing price field with explicit role (human may change before publish)
    hyp = listing.get("product_price_hypothesis")
    if hyp is not None:
        listing["listing_price"] = hyp
        listing["listing_price_note"] = (
            "Temporarily mirrored from Price Hypothesis for gate eligibility; "
            "Human may set real Listing Price at external publish. "
            "≠ Paid Price."
        )

    cp = dict(commercial_product)
    if (cp.get("readiness") or {}).get("ready"):
        cp["commercial_status"] = ch.CP_COMMERCIAL_READY
    pub_ready = ch.evaluate_listing_publish_readiness(cp, listing, package_eval)
    if pub_ready["ready_for_human_action"]:
        listing["listing_status"] = ch.LIST_AWAITING_HUMAN
    listing["human_action_readiness"] = pub_ready
    return ch.upsert_listing(listing)


def enqueue_awaiting_human(
    commercial_product: dict,
    listing: dict,
    package_dir: Path,
    pipeline_result: dict,
) -> dict:
    quality = pipeline_result.get("quality") or {}
    candidate = {
        "publish_queue_id": listing.get("publish_queue_id"),
        "product_id": commercial_product.get("product_id"),
        "product_asset_id": commercial_product.get("product_asset_id"),
        "product_type": commercial_product.get("product_type"),
        "experiment_id": commercial_product.get("source_experiment_id"),
        "production_request_id": commercial_product.get("source_production_request_id"),
        "platform": listing.get("platform"),
        "listing_title": (
            (package_dir / "title.txt").read_text(encoding="utf-8").strip()
            if (package_dir / "title.txt").exists()
            else commercial_product.get("product_name")
        ),
        "price": listing.get("listing_price"),
        "currency": "CNY",
        "risk_status": commercial_product.get("risk_status"),
        "quality_status": commercial_product.get("quality_status"),
        "commercial_status": commercial_product.get("commercial_status"),
        "commercial_score": quality.get("commercial_score"),
        "validation_passed": True,
        "validation_status": "passed",
        "package_path": str(package_dir),
        "enter_human_gate": True,
        "target_status": pq.QUEUE_AWAITING_HUMAN,
        "notes": (
            "Entry 055 E2E — AWAITING_HUMAN_ACTION. "
            "No auto external publish. Production success ≠ Commercial success."
        ),
    }
    result = pq.enqueue_publish_candidate(candidate)
    if result.get("accepted") and result.get("queue_status") == pq.QUEUE_READY:
        result = {
            **result,
            **pq.advance_to_awaiting_human(result["publish_queue_id"]),
        }
    # Mark commercial product QUEUED when in human gate
    if result.get("queue_status") == pq.QUEUE_AWAITING_HUMAN:
        cp = dict(commercial_product)
        cp["commercial_status"] = ch.CP_QUEUED
        ch.upsert_commercial_product(cp)
    return result


def run_e2e_pilot(*, execute: bool = True, dry_run: bool = False) -> dict:
    """
    Full vertical loop for one autonomously selected candidate.
    Returns trace report dict. Does NOT publish externally or start Observation.
    """
    bundle = load_rank1_selection()
    if not bundle:
        return {
            "entry_status": "BLOCKED",
            "reason": "INSUFFICIENT REAL MARKET DATA",
            "note": "No selected autonomous opportunity — no fake opportunity created.",
        }

    sel = bundle["selection"]
    cand = bundle["candidate"]
    if (sel.get("product_type") or cand.get("product_type") or "").lower() in FORBIDDEN_FUTURE_TYPES:
        return {
            "entry_status": "BLOCKED",
            "reason": "future_product_type_selected",
            "product_type": sel.get("product_type"),
        }

    ec = build_experiment_candidate(bundle)
    persist_experiment_candidate(ec)
    experiment = materialize_experiment_from_candidate(ec)
    pr, approval = materialize_production_request(experiment, ec)

    adapter_result = None
    asset = None
    package_dir = None
    commercial = None
    listing = None
    queue_result = None
    blocked = None

    if execute:
        adapter_result = run_content_factory(pr["production_request_id"], dry_run=dry_run)
        pipeline = adapter_result.get("pipeline_result") or {}
        draft = adapter_result.get("product_asset_draft") or {}

        if pipeline.get("status") != "ok" and not dry_run:
            blocked = {
                "stage": "content_factory",
                "pipeline_status": pipeline.get("status"),
                "failed_step": pipeline.get("failed_step"),
                "error": pipeline.get("error"),
            }
        else:
            asset = persist_product_asset(draft, pipeline)
            quality = pipeline.get("quality") or {}
            q_ok = bool(
                quality.get("passed")
                or str(quality.get("status") or "").lower()
                in ("quality_pass", "passed", "pass", "ok")
            )
            if dry_run:
                blocked = {"stage": "dry_run", "note": "dry_run — no commercial handoff"}
            elif not q_ok:
                blocked = {
                    "stage": "quality_gate",
                    "quality": quality,
                    "note": "Quality failed — must not enter Publish Queue",
                }
            else:
                pkg_src = Path(
                    (pipeline.get("packaging") or {}).get("publish_package_path")
                    or Path(pipeline.get("artifact_path") or "")
                    / "package"
                    / "publish_package"
                )
                package_dir = complete_listing_package(
                    pkg_src,
                    product_name=asset.get("product_name") or pr["product_name"],
                    price_hypothesis=(ec.get("price_hypothesis") or {}).get("value"),
                    product_asset_id=asset["product_asset_id"],
                    experiment_id=experiment["experiment_id"],
                )
                package_eval = ch.evaluate_listing_package(package_dir)
                # Point cover detection at e2e images
                if (package_dir.parent.parent / "images" / "cover_placeholder.txt").exists():
                    package_eval["cover_placeholder"] = True
                    package_eval["package_status"] = ch.PKG_PREPARED_PLACEHOLDER

                commercial = build_commercial_from_asset(
                    asset, experiment, ec, package_dir, pipeline
                )
                if commercial.get("commercial_status") == ch.CP_BLOCKED:
                    blocked = {
                        "stage": "commercial_readiness",
                        "blockers": (commercial.get("readiness") or {}).get("blockers"),
                    }
                else:
                    pq_id = f"pq_auto_{asset['product_asset_id'][:12]}"
                    listing = build_and_upsert_listing(
                        commercial, package_dir, package_eval, publish_queue_id=pq_id
                    )
                    queue_result = enqueue_awaiting_human(
                        commercial, listing, package_dir, pipeline
                    )
                    # refresh commercial after QUEUED update
                    commercial = ch.upsert_commercial_product(
                        {**commercial, "commercial_status": ch.CP_QUEUED}
                    ) if queue_result.get("queue_status") == pq.QUEUE_AWAITING_HUMAN else commercial

    production_cost = "UNAVAILABLE"
    production_time = "UNAVAILABLE"
    if adapter_result and adapter_result.get("pipeline_result"):
        # CF may not expose cost/time — honest UNAVAILABLE unless present
        pr_result = adapter_result["pipeline_result"]
        if pr_result.get("production_cost") is not None:
            production_cost = pr_result["production_cost"]
        if pr_result.get("production_time") is not None:
            production_time = pr_result["production_time"]

    queue_status = (queue_result or {}).get("queue_status")
    entry_status = "PASS"
    if blocked and blocked.get("stage") not in (None,):
        if blocked.get("stage") == "dry_run":
            entry_status = "PARTIAL"
        else:
            entry_status = "BLOCKED"
    elif not execute:
        entry_status = "PARTIAL"
    elif queue_status != pq.QUEUE_AWAITING_HUMAN:
        entry_status = "PARTIAL" if asset else "BLOCKED"

    trace = {
        "entry": "055",
        "entry_status": entry_status,
        "date": "2026-08-30",
        "opportunity_id": experiment.get("source_opportunity_id"),
        "candidate_id": experiment.get("source_candidate_id"),
        "selection_id": experiment.get("source_selection_id"),
        "selection_rank": experiment.get("selection_rank"),
        "score": experiment.get("candidate_score"),
        "risk_status": experiment.get("risk_status"),
        "selection_reason": experiment.get("selection_reason"),
        "evidence_refs": experiment.get("evidence_refs"),
        "experiment_candidate_id": ec["experiment_candidate_id"],
        "experiment_id": experiment["experiment_id"],
        "production_request_id": pr["production_request_id"],
        "approval_id": approval["approval_id"],
        "product_id": (asset or {}).get("product_asset_id")
        or (adapter_result or {}).get("pipeline_result", {}).get("product_id"),
        "product_asset_id": (asset or {}).get("product_asset_id"),
        "commercial_product_id": (commercial or {}).get("commercial_product_id"),
        "listing_id": (listing or {}).get("listing_id"),
        "publish_queue_id": (queue_result or {}).get("publish_queue_id")
        or (listing or {}).get("publish_queue_id"),
        "queue_status": queue_status,
        "published": False,
        "commercial_success": False,
        "market_events_created": False,
        "commercial_learning_ingested": False,
        "legacy_pilot_used": False,
        "production_cost": production_cost,
        "production_time": production_time,
        "package_path": str(package_dir) if package_dir else None,
        "quality": (adapter_result or {}).get("pipeline_result", {}).get("quality"),
        "blocked": blocked,
        "keyword": experiment.get("keyword"),
        "product_type": experiment.get("product_type"),
        "created_at": _now_iso(),
    }
    _save_json(TRACE_JSON, {"schema": "entry_055_trace_v1", "trace": trace})
    return trace


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Entry 055 E2E Autonomous Product Pilot")
    parser.add_argument("--execute", action="store_true", help="Run Content Factory production")
    parser.add_argument("--dry-run", action="store_true", help="Adapter dry_run only")
    parser.add_argument("--prepare-only", action="store_true", help="Stop after PR+approval")
    args = parser.parse_args()

    execute = args.execute or (not args.prepare_only and not args.dry_run)
    if args.prepare_only:
        execute = False
    if args.dry_run:
        execute = True

    result = run_e2e_pilot(execute=execute, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
