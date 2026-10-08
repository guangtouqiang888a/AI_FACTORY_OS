# 6_EXECUTION/commercial_handoff.py — Product → Commercial Product → Listing Handoff
# Entry 053
#
# Product Asset ≠ Commercial Product ≠ Listing Package ≠ Listing
# ≠ Published Listing ≠ Observation ≠ Commercial Success
# Phase 1: virtual materials only; product_type + asset_type extensible

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import config  # noqa: E402

CP_DRAFT = "DRAFT"
CP_COMMERCIAL_READY = "COMMERCIAL_READY"
CP_BLOCKED = "BLOCKED"
CP_QUEUED = "QUEUED"
CP_PUBLISHED = "PUBLISHED"
CP_OBSERVING = "OBSERVING"
CP_VALIDATED = "VALIDATED"
CP_RETIRED = "RETIRED"

LIST_DRAFT = "DRAFT"
LIST_READY = "READY"
LIST_AWAITING_HUMAN = "AWAITING_HUMAN_ACTION"
LIST_PUBLISHED = "PUBLISHED"
LIST_PAUSED = "PAUSED"
LIST_ENDED = "ENDED"
LIST_FAILED = "FAILED"
LIST_CANCELLED = "CANCELLED"

PKG_MISSING = "MISSING"
PKG_PREPARED = "PREPARED"
PKG_PREPARED_PLACEHOLDER = "PREPARED_WITH_PLACEHOLDER"
PKG_MARKETING_READY = "MARKETING_READY"

PRICE_HYPOTHESIS = "PRODUCT_PRICE_HYPOTHESIS"

COMMERCIAL_PRODUCTS_JSON = (
    ROOT / "commercial_assets" / "commercial_products" / "commercial_products_v1.json"
)
LISTINGS_JSON = ROOT / "commercial_assets" / "listings" / "listings_v1.json"

REQUIRED_COMMERCIAL_METADATA = (
    "target_user",
    "problem",
    "offer",
    "delivery_method",
)

REQUIRED_PACKAGE_FILES = (
    "title.txt",
    "description.txt",
    "keywords.txt",
    "faq.txt",
    "delivery_description.txt",
    "version_information.txt",
    "pricing.json",
)


def _now_str() -> str:
    from datetime import datetime
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


def classify_price_role(price_info: dict) -> dict:
    return {
        "product_price_hypothesis": price_info.get("product_price_hypothesis"),
        "listing_price": price_info.get("listing_price"),
        "actual_paid_price": price_info.get("actual_paid_price"),
        "cf_packaging_default": price_info.get("cf_packaging_default"),
        "currency": price_info.get("currency") or "CNY",
        "note": (
            "Product Price Hypothesis ≠ Listing Price ≠ Actual Paid Price ≠ CF Default"
        ),
    }


def evaluate_commercial_readiness(record: dict) -> dict:
    blockers: list[str] = []

    if not record.get("product_id"):
        blockers.append("missing_product_id")
    if not record.get("product_version"):
        blockers.append("missing_product_version")
    if not record.get("product_asset_id"):
        blockers.append("missing_product_asset")

    quality = str(record.get("quality_status") or "").lower()
    if quality not in ("passed", "pass", "quality_pass", "ok"):
        blockers.append("quality_not_passed")

    risk = str(record.get("risk_status") or "unknown").lower()
    if risk in ("unknown", "", "none"):
        blockers.append("risk_unknown")
    elif risk in ("failed", "fail", "high", "blocked"):
        blockers.append("risk_failed")

    meta = record.get("commercial_metadata") or {}
    for key in REQUIRED_COMMERCIAL_METADATA:
        if not meta.get(key) and not record.get(key):
            blockers.append(f"missing_commercial_metadata:{key}")

    delivery = (
        record.get("delivery_method")
        or meta.get("delivery_method")
        or record.get("delivery")
    )
    if not delivery:
        blockers.append("missing_delivery")

    ready = len(blockers) == 0
    return {
        "ready": ready,
        "commercial_status": CP_COMMERCIAL_READY if ready else CP_BLOCKED,
        "blockers": blockers,
        "published": False,
        "commercial_success": False,
        "note": "COMMERCIAL_READY ≠ PUBLISHED ≠ Commercial Success",
    }


def evaluate_listing_package(package_dir: str | Path | None) -> dict:
    if not package_dir:
        return {
            "package_status": PKG_MISSING,
            "missing": ["missing_package_path"],
            "marketing_ready": False,
            "published": False,
        }
    path = Path(package_dir)
    if not path.is_dir():
        return {
            "package_status": PKG_MISSING,
            "missing": ["package_path_not_directory"],
            "marketing_ready": False,
            "published": False,
        }

    missing = [n for n in REQUIRED_PACKAGE_FILES if not (path / n).exists()]
    if missing:
        return {
            "package_status": PKG_MISSING,
            "missing": [f"missing_package_file:{n}" for n in missing],
            "marketing_ready": False,
            "published": False,
        }

    cover_placeholder = False
    candidates = [
        path.parent / "images" / "cover_placeholder.txt",
        path.parent.parent / "images" / "cover_placeholder.txt",
        ROOT
        / "commercial_assets"
        / "pilot_outputs"
        / "preq_20260712_005"
        / "artifacts"
        / "images"
        / "cover_placeholder.txt",
    ]
    for c in candidates:
        if c.exists():
            cover_placeholder = True
            break

    status = PKG_PREPARED_PLACEHOLDER if cover_placeholder else PKG_PREPARED
    return {
        "package_status": status,
        "missing": [],
        "cover_placeholder": cover_placeholder,
        "marketing_ready": False,
        "published": False,
        "note": (
            "Listing Package is Platform-specific Presentation; "
            "PREPARED ≠ PUBLISHED; placeholder cover ≠ Marketing Ready"
        ),
    }


def evaluate_listing_publish_readiness(
    commercial_product: dict,
    listing: dict,
    package_eval: dict,
) -> dict:
    blockers: list[str] = []
    cp_status = commercial_product.get("commercial_status")
    ready_flag = bool((commercial_product.get("readiness") or {}).get("ready"))
    if cp_status not in (CP_COMMERCIAL_READY, CP_QUEUED) and not ready_flag:
        blockers.append("commercial_product_not_ready")
    if package_eval.get("package_status") in (PKG_MISSING, None):
        blockers.append("listing_package_not_ready")
    if not listing.get("platform"):
        blockers.append("missing_platform")
    if listing.get("listing_price") is None and listing.get("price") is None:
        blockers.append("missing_listing_price")
    if not (
        listing.get("delivery_method")
        or (commercial_product.get("commercial_metadata") or {}).get("delivery_method")
    ):
        blockers.append("missing_delivery")
    risk = str(
        listing.get("risk_status") or commercial_product.get("risk_status") or ""
    ).lower()
    if risk not in ("passed", "pass", "ok"):
        blockers.append("risk_not_passed")

    ok = len(blockers) == 0
    return {
        "ready_for_human_action": ok,
        "listing_status": LIST_AWAITING_HUMAN if ok else LIST_DRAFT,
        "blockers": blockers,
        "auto_publish": False,
        "published": False,
    }


def upsert_commercial_product(product: dict) -> dict:
    store = _load_json(
        COMMERCIAL_PRODUCTS_JSON,
        {
            "schema": "commercial_products_v1",
            "entry": "053",
            "note": "Commercial Product lifecycle. ≠ Product Asset ≠ Listing ≠ Published.",
            "commercial_products": [],
        },
    )
    items = store.get("commercial_products", [])
    pid = product.get("commercial_product_id") or product.get("product_id")
    gate = evaluate_commercial_readiness(product)
    product = {
        **product,
        "object_type": "commercial_product",
        "readiness": gate,
        "published": False,
        "commercial_success": False,
        "updated_at": _now_str(),
    }
    if product.get("commercial_status") not in (CP_QUEUED, CP_PUBLISHED, CP_OBSERVING):
        product["commercial_status"] = (
            CP_COMMERCIAL_READY if gate["ready"] else CP_BLOCKED
        )

    replaced = False
    for i, it in enumerate(items):
        if it.get("commercial_product_id") == pid or it.get("product_id") == pid:
            items[i] = {**it, **product}
            replaced = True
            break
    if not replaced:
        if not product.get("commercial_product_id"):
            product["commercial_product_id"] = f"cp_{uuid.uuid4().hex[:10]}"
        if not product.get("created_at"):
            product["created_at"] = _now_str()
        items.append(product)

    store["commercial_products"] = items
    _save_json(COMMERCIAL_PRODUCTS_JSON, store)
    return product


def upsert_listing(listing: dict) -> dict:
    store = _load_json(
        LISTINGS_JSON,
        {
            "schema": "listings_v1",
            "entry": "053",
            "note": (
                "Listing = platform presentation instance. "
                "Published Listing requires Publish Evidence. "
                "No TaobaoProduct / XianyuProduct core tables."
            ),
            "listings": [],
        },
    )
    items = store.get("listings", [])
    lid = listing.get("listing_id")
    listing = {
        **listing,
        "object_type": "listing",
        "published": listing.get("listing_status") == LIST_PUBLISHED,
        "commercial_success": False,
        "updated_at": _now_str(),
    }
    if listing.get("listing_status") == LIST_PUBLISHED and not listing.get(
        "publish_evidence_id"
    ):
        listing["listing_status"] = LIST_AWAITING_HUMAN
        listing["published"] = False
        listing["block_note"] = "published_requires_publish_evidence"

    replaced = False
    for i, it in enumerate(items):
        if it.get("listing_id") == lid:
            items[i] = {**it, **listing}
            replaced = True
            break
    if not replaced:
        if not listing.get("listing_id"):
            listing["listing_id"] = f"lst_{uuid.uuid4().hex[:10]}"
        if not listing.get("created_at"):
            listing["created_at"] = _now_str()
        items.append(listing)

    store["listings"] = items
    _save_json(LISTINGS_JSON, store)
    return listing


def mark_published_listing_from_evidence(
    listing_id: str,
    evidence_id: str,
    *,
    verification_status: str,
) -> dict:
    if verification_status.upper() not in ("VERIFIED", "MANUAL_VERIFIED"):
        return {
            "accepted": False,
            "reason": "evidence_not_verified",
            "commercial_success": False,
        }
    store = _load_json(LISTINGS_JSON, {"listings": []})
    items = store.get("listings", [])
    found = None
    for i, it in enumerate(items):
        if it.get("listing_id") == listing_id:
            it["listing_status"] = LIST_PUBLISHED
            it["publish_evidence_id"] = evidence_id
            it["published"] = True
            it["observation_eligible"] = True
            it["observation_started"] = False
            it["commercial_success"] = False
            it["updated_at"] = _now_str()
            items[i] = it
            found = it
            break
    if not found:
        return {"accepted": False, "reason": "listing_not_found"}
    store["listings"] = items
    _save_json(LISTINGS_JSON, store)
    return {
        "accepted": True,
        "listing": found,
        "observation_eligible": True,
        "observation_started": False,
        "commercial_success": False,
    }


def build_pilot_commercial_product() -> dict:
    return {
        "commercial_product_id": "cp_pilot_excel_attendance",
        "product_id": "prod_excel_attendance",
        "product_name": "小团队考勤记录表",
        "product_type": "digital_template",
        "product_version": "pilot_v1",
        "product_asset_id": "8523329941d4",
        "asset_refs": [
            {"asset_type": "xlsx", "ref": "templates/8523329941d4.xlsx"},
            {"asset_type": "pdf", "ref": "documents/product_manual.pdf"},
            {"asset_type": "zip", "ref": "package/final_product.zip"},
            {
                "asset_type": "preview_image",
                "ref": "images/cover_placeholder.txt",
                "placeholder": True,
            },
        ],
        "source_experiment_id": "exp_20260708_005",
        "source_production_request_id": "preq_20260712_005",
        "quality_status": "passed",
        "risk_status": "passed",
        "delivery_method": "digital_download_zip",
        "commercial_metadata": {
            "target_user": "小团队 / 个体经营者需要简单考勤记录",
            "problem": "手工考勤易错、格式不统一",
            "offer": "可立即使用的 Excel 考勤记录表模板 + 说明 PDF",
            "delivery_method": "digital_download_zip",
        },
        "price_boundary": classify_price_role({
            "product_price_hypothesis": 12.9,
            "listing_price": None,
            "actual_paid_price": None,
            "cf_packaging_default": 19.9,
            "currency": "CNY",
        }),
        "phase1_scope": "virtual_materials_only",
        "future_extensible": True,
        "notes": (
            "Entry 053: Commercial Product from Asset+metadata. "
            "COMMERCIAL_READY ≠ PUBLISHED. Cover placeholder ≠ Marketing Ready."
        ),
    }


def build_pilot_listing(commercial_product: dict, package_eval: dict) -> dict:
    package = (
        ROOT
        / "commercial_assets"
        / "pilot_outputs"
        / "preq_20260712_005"
        / "artifacts"
        / "package"
        / "publish_package"
    )
    listing = {
        "listing_id": "lst_pilot_taobao_preq_20260712_005",
        "commercial_product_id": commercial_product.get("commercial_product_id"),
        "product_id": commercial_product.get("product_id"),
        "product_asset_id": commercial_product.get("product_asset_id"),
        "experiment_id": "exp_20260708_005",
        "production_request_id": "preq_20260712_005",
        "publish_queue_id": "pq_pilot_preq_20260712_005",
        "platform": "taobao",
        "listing_package_path": str(package),
        "listing_package_status": package_eval.get("package_status"),
        "listing_price": 12.9,
        "price_role": PRICE_HYPOTHESIS,
        "currency": "CNY",
        "delivery_method": "digital_download_zip",
        "risk_status": "passed",
        "listing_status": LIST_DRAFT,
        "publish_evidence_id": None,
        "published": False,
        "observation_eligible": False,
        "observation_started": False,
        "commercial_success": False,
        "notes": (
            "Listing is platform presentation instance. "
            "Human confirms final listing price/platform before external publish."
        ),
    }
    # Ensure CP status is COMMERCIAL_READY for gate if readiness says so
    cp = dict(commercial_product)
    if (cp.get("readiness") or {}).get("ready"):
        cp["commercial_status"] = CP_COMMERCIAL_READY
    pub_ready = evaluate_listing_publish_readiness(cp, listing, package_eval)
    if pub_ready["ready_for_human_action"]:
        listing["listing_status"] = LIST_AWAITING_HUMAN
    listing["human_action_readiness"] = pub_ready
    return listing


def materialize_pilot_handoff() -> dict:
    cp = build_pilot_commercial_product()
    gate = evaluate_commercial_readiness(cp)
    cp["readiness"] = gate
    cp["commercial_status"] = CP_COMMERCIAL_READY if gate["ready"] else CP_BLOCKED
    saved_cp = upsert_commercial_product(cp)

    package = (
        ROOT
        / "commercial_assets"
        / "pilot_outputs"
        / "preq_20260712_005"
        / "artifacts"
        / "package"
        / "publish_package"
    )
    pkg = evaluate_listing_package(package)
    listing = build_pilot_listing(saved_cp, pkg)
    saved_listing = upsert_listing(listing)

    if (
        saved_cp.get("commercial_status") == CP_COMMERCIAL_READY
        and saved_listing.get("listing_status") == LIST_AWAITING_HUMAN
    ):
        saved_cp["commercial_status"] = CP_QUEUED
        saved_cp = upsert_commercial_product(saved_cp)

    return {
        "commercial_product": saved_cp,
        "listing_package": pkg,
        "listing": saved_listing,
        "published_listing": None,
        "observation": "NOT_STARTED",
        "commercial_learning": "NONE",
        "auto_publish": False,
    }


def future_compatibility_probe(
    product_type: str,
    asset_type: str,
    platform: str,
) -> dict:
    record = {
        "product_id": f"prod_probe_{product_type}",
        "product_version": "v0_probe",
        "product_asset_id": f"asset_probe_{asset_type}",
        "product_type": product_type,
        "asset_refs": [{"asset_type": asset_type, "ref": f"probe.{asset_type}"}],
        "quality_status": "passed",
        "risk_status": "passed",
        "delivery_method": "digital_delivery",
        "commercial_metadata": {
            "target_user": "probe",
            "problem": "probe",
            "offer": "probe",
            "delivery_method": "digital_delivery",
        },
    }
    gate = evaluate_commercial_readiness(record)
    return {
        "ok": gate["ready"],
        "product_type": product_type,
        "asset_type": asset_type,
        "platform": platform,
        "commercial_ready": gate["ready"],
        "core_model_valid": True,
        "requires_runtime_rebuild": False,
        "note": "Probe only — Future-Extensible ≠ Future-Built",
    }
