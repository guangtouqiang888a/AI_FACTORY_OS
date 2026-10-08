# 1_DATA/product_origin.py — Entry 058E Own Product / Rights / Commercial Model
#
# Market Intelligence ≠ Product Copying
# MARKET_INSPIRED ≠ infringement automatically
# No originality_score hard gate

from __future__ import annotations

from typing import Any

# --- Product Origin ---
ORIGIN_SELF_PRODUCED = "SELF_PRODUCED"
ORIGIN_LAWFULLY_USED = "LAWFULLY_USED"
ORIGIN_USER_PROVIDED = "USER_PROVIDED"
ORIGIN_LICENSED = "LICENSED"
ORIGIN_MARKET_INSPIRED = "MARKET_INSPIRED"
ORIGIN_UNKNOWN = "UNKNOWN"

PRODUCT_ORIGINS = frozenset(
    {
        ORIGIN_SELF_PRODUCED,
        ORIGIN_LAWFULLY_USED,
        ORIGIN_USER_PROVIDED,
        ORIGIN_LICENSED,
        ORIGIN_MARKET_INSPIRED,
        ORIGIN_UNKNOWN,
    }
)

# --- Rights / Risk (minimal; no copyright AI) ---
RIGHTS_CLEAR = "CLEAR"
RIGHTS_REVIEW = "REVIEW_REQUIRED"
RIGHTS_UNKNOWN = "UNKNOWN"
RIGHTS_BLOCKED = "BLOCKED"

PROVENANCE_DOCUMENTED = "DOCUMENTED"
PROVENANCE_PARTIAL = "PARTIAL"
PROVENANCE_UNKNOWN = "UNKNOWN"

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_UNKNOWN = "UNKNOWN"

# --- Business Model (≠ Product Type) ---
BM_DIRECT_SALE = "DIRECT_SALE"
BM_VOLUME_LOW_PRICE = "VOLUME_LOW_PRICE"
BM_LEAD_GENERATION = "LEAD_GENERATION"
BM_SUBSCRIPTION = "SUBSCRIPTION"
BM_CROSS_SELL = "CROSS_SELL"
BM_PREMIUM_SCARCE = "PREMIUM_SCARCE"
BM_B2B_HIGH_VALUE = "B2B_HIGH_VALUE"
BM_TRAFFIC_ACQUISITION = "TRAFFIC_ACQUISITION"
BM_UNKNOWN = "UNKNOWN"

BUSINESS_MODELS = frozenset(
    {
        BM_DIRECT_SALE,
        BM_VOLUME_LOW_PRICE,
        BM_LEAD_GENERATION,
        BM_SUBSCRIPTION,
        BM_CROSS_SELL,
        BM_PREMIUM_SCARCE,
        BM_B2B_HIGH_VALUE,
        BM_TRAFFIC_ACQUISITION,
        BM_UNKNOWN,
    }
)

# --- Market region (extensible; overseas not implemented) ---
REGION_CN = "CN"
REGION_GLOBAL = "GLOBAL"
REGION_OTHER = "OTHER"

OWN_PRODUCT_PRINCIPLE = (
    "AI_FACTORY_OS may study, benchmark, imitate market directions, "
    "and create competing products based on observed demand, "
    "but commercial assets released by AI_FACTORY_OS should be "
    "self-produced or lawfully usable by the system; direct "
    "unauthorized redistribution or simple repackaging of third-party "
    "protected assets is not the default production path."
)

OWN_PRODUCT_PRINCIPLE_ZH = (
    "AI_FACTORY_OS 可以研究市场、参考成熟产品方向、"
    "生产同类/竞品产品，但进入商业发布链的产品应当由系统自主生产，"
    "或确认具备合法使用条件；未经授权直接搬运、传播或简单重新包装"
    "第三方受保护内容，不得作为常规产品生产路线。"
)

FORBIDDEN_DEFAULT_PRODUCTION = frozenset(
    {
        "direct_redistribute_third_party_file",
        "repackage_third_party_protected_asset",
        "unauthorized_content_reuse_as_our_product",
        "pass_off_others_product_as_ai_factory_os",
    }
)


def normalize_product_origin(value: str | None) -> str:
    v = (value or ORIGIN_UNKNOWN).upper()
    return v if v in PRODUCT_ORIGINS else ORIGIN_UNKNOWN


def normalize_business_models(values: list[str] | str | None) -> list[str]:
    if values is None:
        return [BM_UNKNOWN]
    if isinstance(values, str):
        values = [values]
    out = []
    for v in values:
        u = str(v).upper()
        out.append(u if u in BUSINESS_MODELS else BM_UNKNOWN)
    return out or [BM_UNKNOWN]


def assert_product_type_neq_business_model(product_type: str, business_models: list[str]) -> dict:
    """Structural rule: digital_template ≠ DIRECT_SALE."""
    pts = {"digital_template", "video", "novel", "audio", "document", "excel", "ppt"}
    bms = set(normalize_business_models(business_models))
    return {
        "product_type": product_type,
        "business_models": sorted(bms),
        "separated": product_type.lower() not in {b.lower() for b in BUSINESS_MODELS},
        "ok": True,
        "note": "Product Type and Business Model are independent dimensions",
    }


def default_commercial_boundary(
    *,
    product_origin: str = ORIGIN_UNKNOWN,
    rights_status: str = RIGHTS_UNKNOWN,
    provenance_status: str = PROVENANCE_UNKNOWN,
    risk_status: str = RISK_UNKNOWN,
    business_models: list[str] | None = None,
    market_region: str = REGION_CN,
    platform: str | None = None,
    audience: str | None = None,
) -> dict[str, Any]:
    """Minimal attachable metadata for future Product / Commercial gates."""
    origin = normalize_product_origin(product_origin)
    return {
        "own_product_principle": True,
        "product_origin": origin,
        "rights_status": rights_status,
        "provenance_status": provenance_status,
        "risk_status": risk_status,
        "business_models": normalize_business_models(business_models),
        "market_region": market_region,
        "platform": platform,  # sales or discovery — caller must label which
        "audience": audience,
        "market_inspired_is_not_auto_infringement": origin == ORIGIN_MARKET_INSPIRED,
        "default_forbidden_paths": sorted(FORBIDDEN_DEFAULT_PRODUCTION),
        "no_originality_score_hard_gate": True,
    }


def market_to_product_pipeline() -> list[str]:
    return [
        "Market Intelligence",
        "Opportunity",
        "Own Product Concept",
        "AI Product Design",
        "AI Product Generation",
        "Quality",
        "Risk / Rights",
        "Commercial Product",
        "Listing",
        "Market",
    ]
