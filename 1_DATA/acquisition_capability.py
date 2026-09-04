# 1_DATA/acquisition_capability.py — Entry 058D
#
# Xianyu acquisition strategy Reality (no fake data, no bypass).
# Official open platform may exist ≠ this project is eligible.

from __future__ import annotations

from typing import Any

# --- Allowed acquisition modes ---
MODE_LIVE_API = "LIVE_API"
MODE_USER_EXPORT = "USER_EXPORT"
MODE_MANUAL_IMPORT = "MANUAL_IMPORT"
MODE_PARTNER_API = "PARTNER_API"
MODE_OTHER_ALLOWED = "OTHER_ALLOWED_SOURCE"

# --- Forbidden (never register as capability) ---
FORBIDDEN_MODES = frozenset(
    {
        "SCRAPE_BYPASS",
        "LOGIN_AUTOMATION_BYPASS",
        "ANTI_BOT_BYPASS",
        "CAPTCHA_BYPASS",
        "UNAUTHORIZED_API",
    }
)

# Compatibility mapping to 058B collection_mode strings
COLLECTION_MODE_IMPORT = "EXTERNAL_IMPORT"
COLLECTION_MODE_LIVE = "LIVE_COLLECTION"
COLLECTION_MODE_FIXTURE = "TEST_FIXTURE"

RECOMMENDED_CURRENT = (MODE_USER_EXPORT, MODE_MANUAL_IMPORT)


def xianyu_official_capability() -> dict[str, Any]:
    """
    Based on public docs (open.goofish.com / Taobao Open Platform), 2026-08-30 audit.

    Evidence:
    - https://open.goofish.com/doc/quick-start.html
      「闲鱼小程序目前不对外公开开放申请，只面向闲鱼运营小二定向邀请的服务商」
    - Partner server APIs focus on ISV order/user (alibaba.idle.isv.*) — not public
      marketplace listing search for competitive market observations.
    - Requires enterprise 入驻, AppKey, accessToken; 聚石塔 for many server paths.
    - Personal account not recommended / not convertible later.
    """
    return {
        "platform": "xianyu",
        "open_platform_url": "https://open.goofish.com/",
        "taobao_open_platform": "https://open.taobao.com",
        "official_open_platform_exists": True,
        "public_self_serve_registration": False,
        "invitation_only_service_providers": True,
        "published_api_focus": [
            "ISV order create/query/ship/refund",
            "user basic info / age / alipay bind",
            "mini-program Windvane / TOP auth",
        ],
        "public_marketplace_listing_search_api_for_competitors": False,
        "status_for_partner_isv_order_apis": "AVAILABLE_WITH_REQUIREMENTS",
        "status_for_ai_factory_market_observation": "NOT_AVAILABLE_CURRENTLY",
        "notes": (
            "Official APIs exist for invited enterprise ISV / mini-program partners. "
            "They are not a drop-in LIVE market-observation feed for this project today. "
            "Having an API document ≠ project eligibility."
        ),
    }


def current_eligibility() -> dict[str, Any]:
    """Project Reality: no AppKey / invitation / enterprise partner status recorded."""
    return {
        "project": "AI_FACTORY_OS",
        "has_xianyu_partner_invitation": False,
        "has_enterprise_taobao_open_identity": False,
        "has_app_key": False,
        "has_access_token": False,
        "has_jushita_deploy": False,
        "eligible_for_live_api_market_observation": False,
        "eligible_for_partner_order_apis": False,
        "classification": "NOT_AVAILABLE_CURRENTLY",
        "access_requirements": ACCESS_REQUIREMENTS,
    }


ACCESS_REQUIREMENTS = [
    "闲鱼运营定向邀请（服务商）— open.goofish.com 明确非公开开放申请",
    "淘宝开放平台企业身份入驻（应用软件开发商 / 阿里生态 API）",
    "AppKey / AppSecret（小程序 C 端 / 商家 B 端类目按业务）",
    "OAuth accessToken（用户/商家授权）",
    "所需 API 权限审批（订单/用户等；市场竞品搜索未证实为公开可用）",
    "部分服务端能力需聚石塔等合规部署",
    "主体一致：淘宝开放平台入驻主体 / 闲鱼入驻主体 / 合同签约主体",
]


def acquisition_modes_matrix() -> dict[str, Any]:
    return {
        "allowed": {
            MODE_USER_EXPORT: {
                "status": "IMPLEMENTED",
                "maps_to_collection_mode": COLLECTION_MODE_IMPORT,
                "description": "User legally exports/downloads own or permitted data files",
                "recommended_phase1": True,
            },
            MODE_MANUAL_IMPORT: {
                "status": "IMPLEMENTED",
                "maps_to_collection_mode": COLLECTION_MODE_IMPORT,
                "description": "Operator places attested file in data/raw/xianyu/imports/",
                "recommended_phase1": True,
            },
            MODE_LIVE_API: {
                "status": "NOT_AVAILABLE_CURRENTLY",
                "maps_to_collection_mode": COLLECTION_MODE_LIVE,
                "eligibility": "AVAILABLE_WITH_REQUIREMENTS at platform; project NOT eligible",
                "recommended_phase1": False,
            },
            MODE_PARTNER_API: {
                "status": "NOT_AVAILABLE_CURRENTLY",
                "maps_to_collection_mode": COLLECTION_MODE_LIVE,
                "description": "Future authorized partner feed",
                "recommended_phase1": False,
            },
            MODE_OTHER_ALLOWED: {
                "status": "DESIGNED_ONLY",
                "maps_to_collection_mode": COLLECTION_MODE_IMPORT,
                "description": "Other compliant sources with REVIEW_REQUIRED",
                "recommended_phase1": False,
            },
        },
        "forbidden": sorted(FORBIDDEN_MODES),
        "recommended_current": list(RECOMMENDED_CURRENT),
    }


def field_availability_matrix() -> dict[str, str]:
    """
    Field classification for Xianyu market observation path.
    Must not invent LIVE availability.
    """
    via_export = "AVAILABLE_VIA_EXPORT"
    return {
        "title": via_export,
        "price": via_export,
        "view_count": via_export,  # if present in export; else UNAVAILABLE/NULL
        "want_count": via_export,
        "comment_count": via_export,
        "share_count": via_export,
        "seller_reference": via_export,
        "source_item_id": via_export,  # or PARTIAL via URL
        "source_url": via_export,
        "published_at": via_export,
        "observed_at": "CURRENTLY_AVAILABLE",  # set at import time
        "live_api_listing_fields": "UNAVAILABLE",
        "official_api_competitor_search": "UNAVAILABLE",
    }


def capability_snapshot() -> dict[str, Any]:
    return {
        "entry": "058D",
        "date": "2026-08-30",
        "official": xianyu_official_capability(),
        "eligibility": current_eligibility(),
        "modes": acquisition_modes_matrix(),
        "fields": field_availability_matrix(),
        "recommended_acquisition_mode": list(RECOMMENDED_CURRENT),
        "live_collection": "NOT_AVAILABLE",
        "external_import": "VALID_PATH",
        "waiting": "WAITING_FOR_REAL_SOURCE" if True else None,
        "forbidden_commercial_conclusions": True,
        "source_neq_sales": True,
    }
