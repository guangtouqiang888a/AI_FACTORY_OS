# 6_EXECUTION/human_publish_pack.py — Entry 056 Human Publish Pack + Evidence Prep
#
# Builds a Human Publish Pack from Reality for a queued autonomous (or any) product.
# Does NOT publish, does NOT fabricate Publish Evidence / Market Events / Observation.
#
# Product-type and platform are string fields — extensible beyond excel/xianyu.
# Legacy Pilot 8523329941d4 must not be mixed into autonomous packs.

from __future__ import annotations

import json
import sqlite3
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LEGACY_PILOT_ASSET = "8523329941d4"
DEFAULT_ASSET_ID = "f2f8bab97df8"

TZ_CN = timezone(timedelta(hours=8))


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def find_commercial_product(product_asset_id: str) -> dict | None:
    store = _load_json(
        ROOT / "commercial_assets" / "commercial_products" / "commercial_products_v1.json"
    )
    for it in store.get("commercial_products") or []:
        if it.get("product_asset_id") == product_asset_id or it.get("product_id") == product_asset_id:
            return it
    return None


def find_listing(product_asset_id: str) -> dict | None:
    store = _load_json(ROOT / "commercial_assets" / "listings" / "listings_v1.json")
    for it in store.get("listings") or []:
        if it.get("product_asset_id") == product_asset_id:
            return it
    return None


def find_product_asset(product_asset_id: str) -> dict | None:
    store = _load_json(
        ROOT / "commercial_assets" / "product_assets" / "product_assets_v1.json"
    )
    for it in store.get("product_assets") or []:
        if it.get("product_asset_id") == product_asset_id:
            return it
    return None


def get_queue_row(publish_queue_id: str) -> dict | None:
    import sys

    sys.path.insert(0, str(ROOT / "8_CONFIG"))
    sys.path.insert(0, str(ROOT / "6_EXECUTION"))
    import publish_queue as pq  # noqa: WPS433

    pq.ensure_publish_queue_schema()
    return pq.get_queue_entry(publish_queue_id)


def count_publish_evidence(queue_id: str) -> int:
    import sys

    sys.path.insert(0, str(ROOT / "8_CONFIG"))
    import database  # noqa: WPS433

    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM publish_evidence WHERE queue_id=?",
            (queue_id,),
        ).fetchone()
    return int(row["c"] if row and "c" in row.keys() else row[0])


def artifact_root(product_asset_id: str) -> Path:
    return ROOT / "11_CONTENT_FACTORY" / "artifacts" / "products" / product_asset_id


def package_dir_from_listing(listing: dict, product_asset_id: str) -> Path:
    raw = listing.get("listing_package_path") if listing else None
    if raw:
        p = Path(raw)
        if p.is_dir():
            return p
    return (
        ROOT
        / "commercial_assets"
        / "e2e_outputs"
        / product_asset_id
        / "package"
        / "publish_package"
    )


def verify_asset_integrity(product_asset_id: str) -> dict:
    """File Integrity / Openability / Packaging / Delivery checks."""
    art = artifact_root(product_asset_id)
    blockers: list[str] = []
    assets: list[dict] = []

    if not art.exists():
        return {
            "ok": False,
            "blockers": ["artifact_root_missing"],
            "assets": [],
            "publish_readiness_blocked": True,
        }

    xlsx = list(art.glob("templates/*.*"))
    pdf = art / "documents" / "product_manual.pdf"
    zpath = art / "package" / "final_product.zip"
    cover = art / "images" / "cover_placeholder.txt"

    for p in xlsx:
        magic = p.read_bytes()[:2] if p.exists() else b""
        openable = magic == b"PK"  # OOXML / zip-based
        assets.append({
            "file_name": p.name,
            "type": p.suffix.lstrip(".").lower() or "file",
            "path": str(p),
            "exists": p.exists(),
            "openable_ooxml_zip": openable,
            "validated": openable,
        })
        if not openable:
            blockers.append(f"primary_file_not_openable:{p.name}")

    if not xlsx:
        # Generic: any primary under templates/ or documents/
        primary_candidates = list(art.glob("templates/*")) + list(art.glob("documents/*"))
        if not primary_candidates:
            blockers.append("no_primary_deliverable_file")

    if pdf.exists():
        assets.append({
            "file_name": pdf.name,
            "type": "pdf",
            "path": str(pdf),
            "exists": True,
            "size_bytes": pdf.stat().st_size,
            "validated": pdf.stat().st_size > 0,
        })
        if pdf.stat().st_size == 0:
            blockers.append("pdf_empty")
    else:
        assets.append({
            "file_name": "product_manual.pdf",
            "type": "pdf",
            "path": str(pdf),
            "exists": False,
            "validated": False,
            "note": "optional_manual_missing",
        })

    zip_ok = False
    zip_names: list[str] = []
    if zpath.exists():
        try:
            with zipfile.ZipFile(zpath) as zf:
                bad = zf.testzip()
                zip_names = zf.namelist()
                zip_ok = bad is None
                if bad:
                    blockers.append(f"zip_corrupt_member:{bad}")
        except zipfile.BadZipFile:
            blockers.append("zip_bad_format")
        assets.append({
            "file_name": zpath.name,
            "type": "zip",
            "path": str(zpath),
            "exists": True,
            "zip_integrity_ok": zip_ok,
            "member_count": len(zip_names),
            "validated": zip_ok,
        })
    else:
        blockers.append("final_product_zip_missing")
        assets.append({
            "file_name": "final_product.zip",
            "type": "zip",
            "path": str(zpath),
            "exists": False,
            "validated": False,
        })

    cover_placeholder = cover.exists()
    assets.append({
        "file_name": "cover_placeholder.txt",
        "type": "cover_placeholder",
        "path": str(cover),
        "exists": cover_placeholder,
        "placeholder": True,
        "validated": cover_placeholder,
        "note": "PLACEHOLDER — Replace before publish recommended; not Marketing Ready",
    })

    return {
        "ok": len(blockers) == 0,
        "blockers": blockers,
        "assets": assets,
        "cover_placeholder": cover_placeholder,
        "publish_readiness_blocked": len(blockers) > 0,
        "artifact_root": str(art),
    }


def verify_listing_package(package_dir: Path) -> dict:
    required = (
        "title.txt",
        "description.txt",
        "keywords.txt",
        "faq.txt",
        "delivery_description.txt",
        "version_information.txt",
        "pricing.json",
    )
    missing = [n for n in required if not (package_dir / n).exists()]
    contents = {}
    for n in required:
        p = package_dir / n
        if not p.exists():
            continue
        if n.endswith(".json"):
            try:
                contents[n] = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                contents[n] = {"error": "unreadable"}
                missing.append(f"unreadable:{n}")
        else:
            contents[n] = _read_text(p)
    return {
        "ok": len(missing) == 0,
        "missing": missing,
        "package_dir": str(package_dir),
        "contents": contents,
    }


def build_publish_evidence_template(queue_id: str, listing: dict, commercial: dict) -> dict:
    """Blank template for human fill — NOT recorded as evidence."""
    return {
        "schema": "publish_evidence_template_v1",
        "entry": "056",
        "status": "TEMPLATE_ONLY_NOT_RECORDED",
        "note": (
            "Human fills AFTER real platform publish. "
            "AI must NOT invent listing_reference / URL / published_at. "
            "Call publish_queue.record_publish_evidence() only with real values."
        ),
        "fields_to_fill": {
            "queue_id": queue_id,
            "platform": listing.get("platform") or "HUMAN_CONFIRM",
            "listing_reference": "",
            "published_at": "",
            "source": "human_manual_entry",
            "verification_status": "MANUAL_VERIFIED",
            "human_operator": "",
            "notes": "",
            "screenshot_path_or_ref": "",
        },
        "forbidden": [
            "ai_generated_listing_id",
            "ai_generated_listing_url",
            "ai_force_queue_published_without_evidence",
            "fabricated_market_event",
            "commercial_success_claim",
        ],
        "after_accepted_evidence": {
            "queue_becomes": "PUBLISHED",
            "observation_eligible": True,
            "observation_started": False,
            "commercial_success": False,
            "observation_start": "NEXT_ENTRY_ONLY",
        },
        "commercial_product_id": commercial.get("commercial_product_id"),
        "listing_id": listing.get("listing_id"),
        "product_asset_id": commercial.get("product_asset_id"),
    }


def observation_preconditions(queue_id: str, listing: dict) -> dict:
    ev_count = count_publish_evidence(queue_id)
    published_listing = bool(listing.get("published")) or listing.get("listing_status") == "PUBLISHED"
    return {
        "published_listing_exists": published_listing,
        "verified_publish_evidence_exists": ev_count > 0,
        "observation_window_defined": False,
        "market_event_collector_available": True,
        "market_event_collector_note": (
            "1_DATA/market_event_core.py ingest API exists; live connectors Not Built"
        ),
        "observation_may_start": False,
        "observation_status": "NOT_STARTED",
        "blockers": [
            b
            for b, ok in [
                ("published_listing_missing", not published_listing),
                ("publish_evidence_missing", ev_count == 0),
                ("observation_window_undefined", True),
            ]
            if ok
        ],
    }


def build_reality_snapshot(product_asset_id: str = DEFAULT_ASSET_ID) -> dict:
    if product_asset_id == LEGACY_PILOT_ASSET:
        return {
            "ok": False,
            "reason": "legacy_pilot_isolated",
            "note": "Use HISTORICAL pack under pilot_outputs; Entry 056 targets autonomous product only.",
        }

    commercial = find_commercial_product(product_asset_id)
    listing = find_listing(product_asset_id)
    asset_rec = find_product_asset(product_asset_id)
    if not commercial or not listing:
        return {
            "ok": False,
            "reason": "missing_commercial_or_listing",
            "commercial_found": commercial is not None,
            "listing_found": listing is not None,
        }

    queue_id = listing.get("publish_queue_id") or f"pq_auto_{product_asset_id[:12]}"
    queue = get_queue_row(queue_id)
    integrity = verify_asset_integrity(product_asset_id)
    pkg = package_dir_from_listing(listing, product_asset_id)
    pkg_eval = verify_listing_package(pkg)
    ev_count = count_publish_evidence(queue_id)
    obs = observation_preconditions(queue_id, listing)

    price_boundary = commercial.get("price_boundary") or {}
    pricing_pkg = (pkg_eval.get("contents") or {}).get("pricing.json") or {}

    selection_origin = "AUTONOMOUSLY SELECTED + AUTONOMOUSLY PRODUCED"
    if commercial.get("entry") == "055" or (commercial.get("source_opportunity_id") or "").startswith("aoc_"):
        selection_origin = "AUTONOMOUSLY SELECTED + AUTONOMOUSLY PRODUCED"

    platform_recorded = listing.get("platform") or (queue or {}).get("platform")
    platform_report = {
        "system_recorded_platform": platform_recorded,
        "human_confirmed_platform": None,
        "status": "SYSTEM_RECORDED_PENDING_HUMAN_CONFIRM" if platform_recorded else "NOT_YET_SELECTED",
        "note": (
            "Report Reality as-is. Human confirms platform for external action. "
            "AI does not auto-select or switch platforms."
        ),
    }

    return {
        "ok": True,
        "entry": "056",
        "generated_at": _now_iso(),
        "selection_origin": selection_origin,
        "commercially_validated": False,
        "product_identity": {
            "product_id": commercial.get("product_id"),
            "product_type": commercial.get("product_type"),
            "product_version": commercial.get("product_version"),
            "product_asset_id": product_asset_id,
            "commercial_product_id": commercial.get("commercial_product_id"),
            "listing_id": listing.get("listing_id"),
            "publish_queue_id": queue_id,
            "experiment_id": commercial.get("source_experiment_id"),
            "production_request_id": commercial.get("source_production_request_id"),
            "opportunity_id": commercial.get("source_opportunity_id"),
        },
        "product_name": commercial.get("product_name"),
        "commercial": commercial,
        "listing": listing,
        "product_asset_record": asset_rec,
        "queue": queue,
        "integrity": integrity,
        "listing_package": pkg_eval,
        "price": {
            "price_hypothesis": price_boundary.get("product_price_hypothesis"),
            "listing_price_field": listing.get("listing_price"),
            "listing_price_role": listing.get("price_role"),
            "listing_price_note": listing.get("listing_price_note"),
            "cf_packaging_default": price_boundary.get("cf_packaging_default"),
            "suggested_price_in_package": pricing_pkg.get("suggested_price"),
            "actual_paid_price": None,
            "ai_recommendation_only": True,
            "labels": {
                "99.9": "PRODUCT_PRICE_HYPOTHESIS (opportunity estimated_value proxy)",
                "19.9": "CF_PACKAGING_DEFAULT / AI_RECOMMENDATION_ONLY",
                "listing_field_99.9": "mirrored hypothesis for gate — NOT validated Listing Price",
            },
            "note": "Price Hypothesis ≠ Listing Price ≠ Actual Paid Price",
        },
        "platform": platform_report,
        "quality": commercial.get("quality_detail") or {},
        "risk_status": commercial.get("risk_status"),
        "quality_status": commercial.get("quality_status"),
        "publish_evidence_count": ev_count,
        "publish_evidence_status": "MISSING" if ev_count == 0 else "PRESENT",
        "observation": obs,
        "commercial_learning": "NONE",
        "legacy_pilot_isolated": product_asset_id != LEGACY_PILOT_ASSET,
        "publish_readiness": (
            "BLOCKED"
            if integrity.get("publish_readiness_blocked") or not pkg_eval.get("ok")
            else "READY FOR HUMAN EXTERNAL ACTION"
        ),
        "score_note": "Score ≠ Commercial Success. commercial_score is eligibility only.",
    }


def render_human_publish_pack_markdown(snap: dict) -> str:
    if not snap.get("ok"):
        return f"# HUMAN PUBLISH PACK\n\nBLOCKED: {snap.get('reason')}\n"

    ident = snap["product_identity"]
    meta = (snap["commercial"].get("commercial_metadata") or {})
    pkg = snap["listing_package"]
    contents = pkg.get("contents") or {}
    q = snap.get("quality") or {}
    price = snap["price"]
    plat = snap["platform"]
    integ = snap["integrity"]
    obs = snap["observation"]

    asset_lines = []
    for a in integ.get("assets") or []:
        asset_lines.append(
            f"- **{a.get('file_name')}** | type=`{a.get('type')}` | exists={a.get('exists')} | "
            f"validated={a.get('validated')} | path=`{a.get('path')}`"
            + (f" | note={a.get('note')}" if a.get("note") else "")
        )

    checklist = """
- [ ] Product file verified
- [ ] Package verified
- [ ] Listing title verified
- [ ] Description verified
- [ ] Price verified (human chooses Listing Price)
- [ ] Delivery verified
- [ ] Platform verified / confirmed
- [ ] Risk status verified
- [ ] Human publish authorization confirmed
- [ ] After publish: capture listing reference (URL / ID)
- [ ] After publish: capture publish time
- [ ] After publish: create Publish Evidence via `record_publish_evidence()`
""".strip()

    md = f"""# HUMAN PUBLISH PACK
# Entry 056 | Autonomous Product Handoff

生成时间：{snap.get("generated_at")}
Selection Origin：**{snap.get("selection_origin")}**
Commercially Validated：**NO**（无真实市场成交证据）
系统状态：**{snap.get("publish_readiness")}**
Queue：**{(snap.get("queue") or {}).get("queue_status", "UNKNOWN")}**
Published Listing：**MISSING**
Publish Evidence：**{snap.get("publish_evidence_status")}**
Observation：**NOT_STARTED**
Commercial Learning：**NONE**

> Human Gate = External Action Gate（登录 / 发布点击 / 价格确认 / 付款风险）  
> Human Gate ≠ Product Approval Gate（选品与生产已由自主链完成）  
> Publish ≠ Commercial Success · Score ≠ Commercial Success

**Legacy Pilot Isolation：** `8523329941d4` / `exp_20260708_005` = HISTORICAL — 与本包无关。

---

## A. Product Identity

| Field | Value |
|-------|-------|
| product_id | `{ident.get("product_id")}` |
| product_type | `{ident.get("product_type")}` |
| product_version | `{ident.get("product_version")}` |
| product_asset_id | `{ident.get("product_asset_id")}` |
| commercial_product_id | `{ident.get("commercial_product_id")}` |
| listing_id | `{ident.get("listing_id")}` |
| publish_queue_id | `{ident.get("publish_queue_id")}` |
| opportunity_id | `{ident.get("opportunity_id")}` |
| experiment_id | `{ident.get("experiment_id")}` |
| production_request_id | `{ident.get("production_request_id")}` |

---

## B. Product Summary

- **产品名称：** {snap.get("product_name")}
- **是什么：** 可交付的 `digital_template`（本轮 CF 产出为可编辑 Excel / OOXML）数字资料包。**产品形态假设 = HYPOTHESIS**（由机会 keyword 映射生产，尚未被市场验证）。
- **给谁使用：** {meta.get("target_user") or "HYPOTHESIS"}
- **解决什么问题：** {meta.get("problem") or "HYPOTHESIS"}
- **包含什么：** Excel 主文件 + PDF 说明（若存在）+ `final_product.zip` + Listing Package 文案
- **不包含什么：** 真实平台已发布 Listing；真实成交；封面成品图（当前为 placeholder）；Commercial Validation

---

## C. Product Assets（可追溯路径）

Artifact root: `{integ.get("artifact_root")}`

{chr(10).join(asset_lines)}

Integrity OK: **{integ.get("ok")}**  
Blockers: `{integ.get("blockers")}`

---

## D. Quality / Commercial / Risk

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Quality Status | `{snap.get("quality_status")}` | Gate only |
| Quality Score | `{q.get("quality_score")}` | ≠ Commercial Success |
| Commercial Score | `{q.get("commercial_score")}` | Eligibility only — **不是**「已证明有商业需求」 |
| Usability | `{q.get("usability_score")}` | Production usability |
| Market Score | `{q.get("market_score")}` | Heuristic ≠ market validation |
| Production Cost Score | `{q.get("production_cost_score")}` | Heuristic |
| Risk | `{snap.get("risk_status")}` | passed required for queue |

**Score ≠ Commercial Success.**

---

## E. Listing Package（预写好，人工无需重写）

Package dir: `{pkg.get("package_dir")}`  
Package OK: **{pkg.get("ok")}** Missing: `{pkg.get("missing")}`

### Title
```
{contents.get("title.txt", "")}
```

### Description
```
{contents.get("description.txt", "")}
```

### Keywords
```
{contents.get("keywords.txt", "")}
```

### FAQ
```
{contents.get("faq.txt", "")}
```

### Delivery
```
{contents.get("delivery_description.txt", "")}
```

### Version
```
{contents.get("version_information.txt", "")}
```

### Cover
- Status: **PLACEHOLDER** (`cover_placeholder.txt`)
- Recommendation: Replace before publish if low-cost image available; Keep acceptable for first digital test
- Marketing Ready: **false**

---

## F. Price Boundary

| Role | Value | Label |
|------|-------|-------|
| Price Hypothesis | `{price.get("price_hypothesis")}` CNY | PRODUCT_PRICE_HYPOTHESIS |
| Listing field (mirrored) | `{price.get("listing_price_field")}` | NOT validated Listing Price |
| CF packaging default / suggested | `{price.get("cf_packaging_default")}` / `{price.get("suggested_price_in_package")}` | **AI_RECOMMENDATION_ONLY** |
| Actual Paid Price | `null` | — |

**Human must choose Listing Price at publish time.**  
禁止把 99.9 或 19.9 写成「实际售价」或「已验证价格」。

---

## G. Platform Boundary

| Field | Value |
|-------|-------|
| System recorded platform | `{plat.get("system_recorded_platform")}` |
| Human confirmed | `{plat.get("human_confirmed_platform")}` |
| Status | `{plat.get("status")}` |

{plat.get("note")}

Human confirms: use recorded platform / change / defer — AI does not auto-switch.

---

## H. What You Need To Do（最小人工动作）

1. **Open platform**（人工登录 — 系统禁止代登）
2. **Create / Edit Listing** on chosen platform
3. **Paste** prepared Title / Description / Keywords / FAQ / Delivery from package above
4. **Attach** `final_product.zip` (or platform-allowed digital delivery of the xlsx pack)
5. **Verify** price & delivery method yourself
6. **Publish**（人工点击）
7. **Copy** listing URL / listing ID + publish time
8. **Record Publish Evidence** using template + `publish_queue.record_publish_evidence()`

**You do NOT need to：** re-select the product, rewrite product concept, or rebuild files.

---

## I. Pre-Publish Checklist

{checklist}

Overall: **{snap.get("publish_readiness")}**

---

## J. Publish Evidence（接口已就绪 / 记录尚未创建）

- API: `6_EXECUTION/publish_queue.py` → `record_publish_evidence()`
- Table: `publish_evidence`（evidence_id, queue_id, platform, listing_reference, published_at, source, verification_status, human_operator, notes, …）
- Current evidence for this queue: **{snap.get("publish_evidence_count")}**
- Template file: `PUBLISH_EVIDENCE_TEMPLATE.json`（同目录）

Allowed after real publish: Listing URL / ID / platform reference / time / MANUAL_VERIFIED / screenshot path.

Forbidden: AI-invented URL/ID; AI forcing Queue→PUBLISHED; fake Market Events.

State machine:

```text
AWAITING_HUMAN_ACTION
  → (human publish + verified evidence)
PUBLISHED + observation_eligible=1 + observation_started=false
  → (NEXT Entry) Observation Start
```

PUBLISHED ≠ COMMERCIAL_SUCCESS.

---

## K. Observation Preconditions（本 Entry 不启动）

| Precondition | Status |
|--------------|--------|
| Published Listing exists | {obs.get("published_listing_exists")} |
| Verified Publish Evidence exists | {obs.get("verified_publish_evidence_exists")} |
| Observation Window defined | {obs.get("observation_window_defined")} |
| Market Event Collector available | {obs.get("market_event_collector_available")} ({obs.get("market_event_collector_note")}) |
| Observation may start | **false** |
| Observation status | **NOT_STARTED** |

Blockers: `{obs.get("blockers")}`

---

## L. Forbidden Actions (AI & Automation)

- 登录平台 / 自动发布 / 改真实售价 / 付款 / 广告 / 私信 / 注册账号
- 伪造 Publish Evidence / Market Event / Revenue / Purchase
- 启动 Observation / Commercial Learning
- 把本产品与 Legacy Pilot `8523329941d4` 混用结果

---

## M. Future Extensibility Note

本 Pack / Evidence 结构使用 `product_type` / `platform` 字符串字段，不绑定 Excel 或闲鱼为永久唯一类型。  
未来 document / video / novel / audio 与 taobao / future_platform 可复用同一 Handoff 形状。  
**Future-Extensible ≠ Future-Built** — 本 Entry 不实现未来媒体 Runtime。
"""
    return md


def materialize_human_publish_pack(product_asset_id: str = DEFAULT_ASSET_ID) -> dict:
    snap = build_reality_snapshot(product_asset_id)
    out_dir = ROOT / "commercial_assets" / "e2e_outputs" / product_asset_id
    out_dir.mkdir(parents=True, exist_ok=True)

    if not snap.get("ok"):
        report = {"ok": False, "snapshot": snap}
        (out_dir / "HUMAN_PUBLISH_PACK_ERROR.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return report

    md = render_human_publish_pack_markdown(snap)
    pack_path = out_dir / "HUMAN_PUBLISH_PACK.md"
    pack_path.write_text(md, encoding="utf-8")
    # Naming continuity with Entry 048 Decision Pack
    (out_dir / "HUMAN_COMMERCIAL_DECISION_PACK.md").write_text(
        md
        + "\n\n---\n\n> Alias note: This file mirrors HUMAN_PUBLISH_PACK.md for Entry 048 naming continuity.\n"
        + "> Entry 056 focus = Human External Action Pack（非逐产品重新选品）。\n",
        encoding="utf-8",
    )

    template = build_publish_evidence_template(
        snap["product_identity"]["publish_queue_id"],
        snap["listing"],
        snap["commercial"],
    )
    tpl_path = out_dir / "PUBLISH_EVIDENCE_TEMPLATE.json"
    tpl_path.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")

    # Refresh publish_assistant checklist under CF artifacts (minimal)
    assist = artifact_root(product_asset_id) / "package" / "publish_assistant"
    assist.mkdir(parents=True, exist_ok=True)
    (assist / "HUMAN_PUBLISH_PACK.md").write_text(
        f"See canonical pack:\n{pack_path}\n", encoding="utf-8"
    )
    (assist / "publish_checklist.md").write_text(
        "# Human External Publish Checklist (Entry 056)\n\n"
        + "Status: READY FOR HUMAN EXTERNAL ACTION\n\n"
        + "- [ ] Product file verified\n"
        + "- [ ] Package verified\n"
        + "- [ ] Listing title verified\n"
        + "- [ ] Description verified\n"
        + "- [ ] Price verified\n"
        + "- [ ] Delivery verified\n"
        + "- [ ] Platform verified\n"
        + "- [ ] Risk status verified\n"
        + "- [ ] Human publish authorization confirmed\n"
        + "- [ ] After publish: capture listing reference\n"
        + "- [ ] After publish: capture publish time\n"
        + "- [ ] After publish: create Publish Evidence\n\n"
        + "Do NOT mark Queue PUBLISHED without verified evidence.\n"
        + "Observation remains NOT_STARTED until next Entry.\n",
        encoding="utf-8",
    )

    snap_path = out_dir / "human_publish_pack_snapshot_v1.json"
    # Slim snapshot for machine use (drop huge evidence_refs duplication if needed)
    slim = {k: v for k, v in snap.items() if k not in ("commercial", "listing", "product_asset_record")}
    slim["commercial_product_id"] = snap["commercial"].get("commercial_product_id")
    slim["listing_id"] = snap["listing"].get("listing_id")
    slim["listing_status"] = snap["listing"].get("listing_status")
    slim["commercial_status"] = snap["commercial"].get("commercial_status")
    slim["paths"] = {
        "human_publish_pack": str(pack_path),
        "decision_pack_alias": str(out_dir / "HUMAN_COMMERCIAL_DECISION_PACK.md"),
        "evidence_template": str(tpl_path),
        "listing_package": snap["listing_package"].get("package_dir"),
        "artifact_root": snap["integrity"].get("artifact_root"),
    }
    snap_path.write_text(json.dumps(slim, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "publish_readiness": snap.get("publish_readiness"),
        "paths": slim["paths"],
        "queue_status": (snap.get("queue") or {}).get("queue_status"),
        "publish_evidence_status": snap.get("publish_evidence_status"),
        "observation_status": "NOT_STARTED",
        "commercial_learning": "NONE",
        "published": False,
        "integrity_ok": snap["integrity"].get("ok"),
        "package_ok": snap["listing_package"].get("ok"),
        "legacy_pilot_isolated": True,
        "snapshot": slim,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Entry 056 Human Publish Pack builder")
    parser.add_argument("--product-asset-id", default=DEFAULT_ASSET_ID)
    args = parser.parse_args()
    result = materialize_human_publish_pack(args.product_asset_id)
    print(json.dumps({k: v for k, v in result.items() if k != "snapshot"}, ensure_ascii=False, indent=2))
    if result.get("ok"):
        print("\nPack:", result["paths"]["human_publish_pack"])


if __name__ == "__main__":
    main()
