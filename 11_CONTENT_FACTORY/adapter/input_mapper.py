# 11_CONTENT_FACTORY/adapter/input_mapper.py — Production Request → Content Factory Input

from __future__ import annotations

from typing import Any

PRODUCT_TYPE_TO_CF = {
    "ppt": "PPT模板",
    "excel": "Excel模板",
    "word": "Word模板",
    "pdf": "PDF资料",
}

EXPERIMENT_MARKET_SCORE = 75.0


def map_production_request_to_input(loaded: dict[str, Any]) -> dict[str, Any]:
    """
    Production Request Object + Approval → Integration Input Package。

    保留：production_request_id, experiment_id, product_name, product_type,
    validation_goal, asset_requirements, quality_requirements。

    不执行 Opportunity / Experiment Selection / Decision Scoring。
    """
    pr = loaded["production_request"]
    approval = loaded["approval"]
    product_type_raw = (pr.get("product_type") or "").lower()
    asset_req = pr.get("asset_requirements") or {}
    quality_req = pr.get("quality_requirements") or {}

    platform = asset_req.get("publish_channel_planned") or "xianyu"
    product_name = pr.get("product_name") or pr.get("keyword") or ""
    cf_product_type = PRODUCT_TYPE_TO_CF.get(product_type_raw, pr.get("product_type", "Excel模板"))

    return {
        "production_request_id": pr.get("production_request_id"),
        "source_experiment_id": pr.get("source_experiment_id"),
        "experiment_id": pr.get("source_experiment_id"),
        "approval_id": approval.get("approval_id") if approval else None,
        "product_name": product_name,
        "keyword": product_name,
        "product_type": product_type_raw,
        "cf_product_type": cf_product_type,
        "target_customer": pr.get("target_customer", ""),
        "validation_goal": pr.get("validation_goal", ""),
        "business_goal": pr.get("business_goal", ""),
        "asset_requirements": asset_req,
        "quality_requirements": quality_req,
        "priority": pr.get("production_priority", ""),
        "platform": platform,
        "expected_price_cny": asset_req.get("expected_price_cny"),
        "structure_outline": asset_req.get("structure_outline") or [],
        "deliverable_format": asset_req.get("deliverable_format", ""),
        "source_opportunity_id": pr.get("source_opportunity_id"),
        "market_stub": {
            "keyword": product_name,
            "category": cf_product_type,
            "market_score": EXPERIMENT_MARKET_SCORE,
            "competition": "pre_approved",
            "recommendation": (
                f"Approved Production Request {pr.get('production_request_id')} — "
                f"market analysis bypassed; validation_goal read-only"
            ),
        },
    }
