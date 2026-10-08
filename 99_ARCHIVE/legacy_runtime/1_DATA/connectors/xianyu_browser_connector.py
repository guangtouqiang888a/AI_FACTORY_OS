# 1_DATA/connectors/xianyu_browser_connector.py — Entry 060
#
# Xianyu Browser Collector v1 — Source Adapter only.
# PUBLIC_WEB_READ via normal browser render. No login / captcha bypass / hidden API.
# Reuses market_source_core insert + collection_runs. Never invents want_count/price.

from __future__ import annotations

import json
import re
import sys
import time
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import market_source_core as msc  # noqa: E402

COLLECTOR_VERSION = "060.1.0"
SOURCE_ID = "src_xianyu_marketplace"
SOURCE = "xianyu"
PLATFORM = "xianyu"
MODE = "PUBLIC_WEB_READ"
MAX_RECORDS_HARD_CAP = 20

TZ_CN = timezone(timedelta(hours=8))

ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_browser_collection_060"


def browser_dependency_status() -> dict:
    """Minimal dependency probe — prefers system Chrome headless dump-dom (no pip)."""
    out = {
        "playwright": False,
        "selenium": False,
        "chrome_headless_dump": False,
        "usable_backend": None,
        "chrome_or_edge_hint": None,
        "status": "DEPENDENCY_MISSING",
        "install_hint": (
            "Preferred: system Chrome/Edge headless --dump-dom (no extra pip). "
            "Optional: pip install selenium|playwright if dump-dom insufficient."
        ),
    }
    try:
        import playwright  # noqa: F401

        out["playwright"] = True
        out["usable_backend"] = "playwright"
        out["status"] = "READY"
    except ImportError:
        pass
    try:
        import selenium  # noqa: F401

        out["selenium"] = True
        if not out["usable_backend"]:
            out["usable_backend"] = "selenium"
            out["status"] = "READY"
    except ImportError:
        pass
    for p in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ):
        if Path(p).exists():
            out["chrome_or_edge_hint"] = p
            out["chrome_headless_dump"] = True
            if not out["usable_backend"]:
                out["usable_backend"] = "chrome_headless_dump"
                out["status"] = "READY"
            break
    return out


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _detect_access_control(page_text: str, title: str = "") -> str | None:
    blob = f"{title}\n{page_text}"
    low = blob.lower()
    checks = [
        ("非法访问", "ACCESS_DENIED"),
        ("请使用正常浏览器", "ACCESS_DENIED"),
        ("error-container", "ACCESS_DENIED"),  # goofish headless deny UI shell
        ("验证码", "CAPTCHA"),
        ("captcha", "CAPTCHA"),
        ("滑块", "CAPTCHA"),
        ("请先登录", "LOGIN_REQUIRED"),
        ("登录后继续", "LOGIN_REQUIRED"),
        ("access denied", "ACCESS_DENIED"),
        ("访问受限", "ACCESS_DENIED"),
        ("punish", "BLOCKED"),
        ("deny", "BLOCKED"),
    ]
    for kw, code in checks:
        if kw.lower() in low or kw in blob:
            # avoid false positive from sitemap "登录" alone on CSR shell
            if code == "LOGIN_REQUIRED" and "请先登录" not in blob and "登录后" not in blob:
                continue
            if code == "BLOCKED" and kw in ("deny", "punish") and "ice-container" in low:
                # baxia scripts may mention deny paths without blocking page
                continue
            # error-container alone only if paired with deny messaging or short CSR deny page
            if kw == "error-container":
                if "非法访问" not in blob and "请使用正常浏览器" not in blob:
                    continue
            return code
    return None


def _extract_item_id(url: str | None) -> str | None:
    if not url:
        return None
    # goofish interactive cards: /item?id=123456
    m = re.search(r"[?&]id=(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/item/([^/?#]+)", url)
    if not m:
        return None
    item = m.group(1).strip()
    if not item or item.lower() in ("sample001", "sample002", "test"):
        return item  # still return; origin layer may reject sample
    return item


def _parse_price(text: str | None) -> float | None:
    if text is None or str(text).strip() == "":
        return None
    s = str(text).replace(",", "").replace("￥", "").replace("¥", "").strip()
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def _parse_want(text: str | None) -> int | None:
    if text is None or str(text).strip() == "":
        return None
    s = str(text)
    m = re.search(r"(\d+)\s*人想要|想要\s*[：: ]*\s*(\d+)|(\d+)\s*想要", s)
    if m:
        for g in m.groups():
            if g is not None:
                return int(g)
    # bare number only if explicitly labeled elsewhere — do not guess from random digits
    return None


def _safe_int_labeled(text: str | None, labels: tuple[str, ...]) -> int | None:
    if not text:
        return None
    s = str(text)
    for lab in labels:
        m = re.search(rf"{lab}\s*[：: ]*\s*(\d+)|(\d+)\s*{lab}", s)
        if m:
            return int(m.group(1) or m.group(2))
    return None


class XianyuBrowserCollector:
    """
    Source Adapter: PUBLIC_WEB_READ.
    Does not belong inside Acquisition Engine.
    """

    adapter_id = "adapter_xianyu_browser"
    source_id = SOURCE_ID
    acquisition_mode = MODE
    collector_version = COLLECTOR_VERSION

    def acquire(
        self,
        *,
        collection_query: str,
        max_records: int = 20,
        declared_origin: str = msc.ORIGIN_REAL,
        headless: bool = True,
    ) -> dict:
        msc.ensure_market_source_schema()
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        max_records = max(1, min(int(max_records or 20), MAX_RECORDS_HARD_CAP))
        query = (collection_query or "").strip()
        if not query or query.lower() in ("xianyu", "taobao"):
            return {
                "ok": False,
                "status": "FAILED",
                "error": "invalid_query",
                "acquisition_mode": MODE,
                "sales_platform": None,
                "login_used": False,
                "bypass_attempted": False,
            }

        dep = browser_dependency_status()
        if dep["status"] != "READY":
            report = {
                "ok": False,
                "status": "FAILED",
                "error": "DEPENDENCY_MISSING",
                "dependency": dep,
                "acquisition_mode": MODE,
                "query": query,
                "sales_platform": None,
                "login_used": False,
                "bypass_attempted": False,
                "hidden_api_called": False,
                "product_created": False,
                "listing_created": False,
                "market_event_created": False,
                "items_extracted": 0,
                "collector_version": COLLECTOR_VERSION,
            }
            (ARTIFACT_DIR / "last_run.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            return report

        # Stage raw dir early
        today = date.today().isoformat()
        run_id = msc.start_collection_run(
            source_id=SOURCE_ID,
            source=SOURCE,
            platform=PLATFORM,
            collection_mode=msc.MODE_IMPORT,  # EXTERNAL_IMPORT-compatible column; notes carry PUBLIC_WEB_READ
            raw_reference=None,
            notes=f"mode={MODE}; query={query}; browser_collector={COLLECTOR_VERSION}",
            collection_query=query,
            acquisition_mode=MODE,
        )
        batch_dir = config.RAW_XIANYU_DIR / today / "import_batches" / run_id
        batch_dir.mkdir(parents=True, exist_ok=True)

        stats = {
            "raw_count": 0,
            "accepted_count": 0,
            "rejected_count": 0,
            "duplicate_count": 0,
            "normalized_count": 0,
            "error_count": 0,
            "rejected_rows": [],
            "observation_ids": [],
        }
        field_hits = {
            "title": 0,
            "price": 0,
            "want_count": 0,
            "source_url": 0,
            "source_item_id": 0,
        }

        try:
            backend = dep["usable_backend"]
            if backend == "playwright":
                page_result = self._collect_playwright(query, max_records, headless)
            elif backend == "selenium":
                page_result = self._collect_selenium(query, max_records, headless, dep)
            else:
                page_result = self._collect_chrome_dump(query, max_records, dep)
        except Exception as exc:
            stats["error_count"] = 1
            stats["error_summary"] = str(exc)
            msc.finish_collection_run(run_id, stats, status="FAILED")
            return {
                "ok": False,
                "status": "FAILED",
                "error": "browser_launch_or_navigation_failed",
                "detail": str(exc),
                "run_id": run_id,
                "acquisition_mode": MODE,
                "query": query,
                "sales_platform": None,
                "login_used": False,
                "bypass_attempted": False,
                "stats": stats,
                "collector_version": COLLECTOR_VERSION,
            }

        # Persist technical artifact (not full HTML dump by default)
        meta_path = batch_dir / "browser_run_meta.json"
        meta_path.write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "query": query,
                    "mode": MODE,
                    "page_result_keys": list(page_result.keys()),
                    "access_control": page_result.get("access_control"),
                    "cards_seen": len(page_result.get("cards") or []),
                    "page_url": page_result.get("final_url"),
                    "page_title": page_result.get("page_title"),
                    "backend": dep["usable_backend"],
                    "login_used": False,
                    "bypass_attempted": False,
                    "hidden_api_called": False,
                    "fetched_at": _now_iso(),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        (batch_dir / "extracted_cards.json").write_text(
            json.dumps(page_result.get("cards") or [], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        import database

        with database.get_connection() as conn:
            conn.execute(
                "UPDATE collection_runs SET raw_reference=?, acquisition_mode=?, collection_query=? WHERE run_id=?",
                (str(meta_path), MODE, query, run_id),
            )
            conn.commit()

        if page_result.get("access_control"):
            stats["error_summary"] = page_result["access_control"]
            msc.finish_collection_run(run_id, stats, status="FAILED")
            return {
                "ok": False,
                "status": "BLOCKED_BY_ACCESS_CONTROL",
                "access_control": page_result["access_control"],
                "run_id": run_id,
                "raw_reference": str(meta_path),
                "acquisition_mode": MODE,
                "query": query,
                "sales_platform": None,
                "login_used": False,
                "bypass_attempted": False,
                "stats": stats,
                "collector_version": COLLECTOR_VERSION,
                "product_created": False,
                "listing_created": False,
                "market_event_created": False,
            }

        cards = page_result.get("cards") or []
        if not cards:
            stats["error_summary"] = page_result.get("error") or "NO_LISTING_PAYLOAD"
            msc.finish_collection_run(run_id, stats, status="FAILED")
            return {
                "ok": False,
                "status": "NO_LISTING_PAYLOAD",
                "run_id": run_id,
                "raw_reference": str(meta_path),
                "acquisition_mode": MODE,
                "query": query,
                "page_title": page_result.get("page_title"),
                "final_url": page_result.get("final_url"),
                "sales_platform": None,
                "stats": stats,
                "collector_version": COLLECTOR_VERSION,
                "product_created": False,
                "listing_created": False,
                "market_event_created": False,
                "note": "CSR shell or empty listing after render — not treated as success",
            }

        observed_at = _now_iso()
        for idx, card in enumerate(cards[:max_records]):
            stats["raw_count"] += 1
            title = (card.get("title") or "").strip() or None
            price = card.get("price")
            if isinstance(price, str):
                price = _parse_price(price)
            want = card.get("want_count")
            url = card.get("source_url")
            item_id = card.get("source_item_id") or _extract_item_id(url)

            if not title:
                stats["rejected_count"] += 1
                stats["rejected_rows"].append(
                    {"row_reference": f"card:{idx}", "reason": "missing_title"}
                )
                continue

            if title:
                field_hits["title"] += 1
            if price is not None:
                field_hits["price"] += 1
            if want is not None:
                field_hits["want_count"] += 1
            if url:
                field_hits["source_url"] += 1
            if item_id:
                field_hits["source_item_id"] += 1

            dedupe_key = msc.make_dedupe_key(
                source=SOURCE,
                source_item_id=item_id,
                source_url=url,
                title=title,
                price=price,
            )
            obs = {
                "run_id": run_id,
                "source_id": SOURCE_ID,
                "source": SOURCE,
                "platform": PLATFORM,
                "source_type": "marketplace",
                "source_item_id": item_id,
                "source_url": url,
                "title": title,
                "category": query,
                "price": price,
                "currency": "CNY" if price is not None else None,
                "view_count": card.get("view_count"),
                "want_count": want,
                "comment_count": card.get("comment_count"),
                "share_count": card.get("share_count"),
                "seller_reference": card.get("seller_reference"),
                "published_at": card.get("published_at"),
                "observed_at": observed_at,
                "raw_reference": str(meta_path),
                "data_origin": msc.ORIGIN_REAL,
                "verification_status": msc.VERIF_MANUAL,
                "dedupe_key": dedupe_key,
                "product_category": query,
                "opportunity_product_type": None,
                "notes": json.dumps(
                    {
                        "acquisition_mode": MODE,
                        "sales_platform_not_implied": True,
                        "not_our_product": True,
                        "not_our_listing": True,
                        "not_market_event": True,
                        "not_hotness_judgment": True,
                        "collector_version": COLLECTOR_VERSION,
                    },
                    ensure_ascii=False,
                ),
            }
            stats["normalized_count"] += 1
            ok, detail = msc.insert_market_observation(obs)
            if not ok:
                if detail == "duplicate":
                    stats["duplicate_count"] += 1
                else:
                    stats["rejected_count"] += 1
                    stats["rejected_rows"].append(
                        {"row_reference": f"card:{idx}", "reason": detail}
                    )
                continue
            stats["accepted_count"] += 1
            stats["observation_ids"].append(detail)

        n = max(stats["raw_count"], 1)
        quality = {
            "title_available_rate": field_hits["title"] / n,
            "price_available_rate": field_hits["price"] / n,
            "want_count_available_rate": field_hits["want_count"] / n,
            "url_available_rate": field_hits["source_url"] / n,
            "item_id_available_rate": field_hits["source_item_id"] / n,
            "field_hits": field_hits,
            "note": "data quality stats ≠ opportunity score",
        }

        status = "done" if stats["accepted_count"] > 0 else "FAILED"
        if stats["accepted_count"] and (
            stats["rejected_count"] or stats["duplicate_count"]
        ):
            status = "PARTIAL"
        msc.finish_collection_run(run_id, stats, status=status)

        preview = []
        for card in (page_result.get("cards") or [])[: min(5, max_records)]:
            preview.append(
                {
                    "title": card.get("title"),
                    "price": card.get("price"),
                    "want_count": card.get("want_count"),
                    "source_url": card.get("source_url"),
                    "source_item_id": card.get("source_item_id")
                    or _extract_item_id(card.get("source_url")),
                }
            )

        result = {
            "ok": stats["accepted_count"] > 0,
            "status": status if stats["accepted_count"] else "NO_LISTING_ACCEPTED",
            "run_id": run_id,
            "raw_reference": str(meta_path),
            "acquisition_mode": MODE,
            "collection_mode": MODE,
            "query": query,
            "max_records": max_records,
            "page_count": page_result.get("page_count", 1),
            "records_seen": stats["raw_count"],
            "stats": stats,
            "data_quality": quality,
            "preview": preview,
            "discovery_platform": PLATFORM,
            "sales_platform": None,
            "login_used": False,
            "bypass_attempted": False,
            "hidden_api_called": False,
            "product_created": False,
            "listing_created": False,
            "market_event_created": False,
            "collector_version": COLLECTOR_VERSION,
            "data_origin": msc.ORIGIN_REAL if stats["accepted_count"] else None,
            "verification_status": msc.VERIF_MANUAL if stats["accepted_count"] else None,
        }
        (ARTIFACT_DIR / "last_run.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        return result

    def _collect_chrome_dump(self, query: str, max_records: int, dep: dict) -> dict:
        """
        System Chrome/Edge headless dump-dom — normal browser render, no profile cookies.
        Not urllib CSR-shell-only; not hidden mtop calls.
        """
        import subprocess
        import tempfile

        binary = dep.get("chrome_or_edge_hint")
        if not binary or not Path(binary).exists():
            raise RuntimeError("chrome_or_edge_binary_missing")
        url = f"https://www.goofish.com/search?q={quote(query)}"
        user_data = tempfile.mkdtemp(prefix="aifo_chrome_060_")
        cmd = [
            binary,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={user_data}",
            "--virtual-time-budget=8000",
            "--dump-dom",
            url,
        ]
        # Windows: Chrome headless often needs stdout redirected to a file
        out_file = Path(tempfile.mkdtemp(prefix="aifo_dump_060_")) / "dump.html"
        err_file = out_file.with_suffix(".err.txt")
        with open(out_file, "wb") as out_fh, open(err_file, "wb") as err_fh:
            proc = subprocess.run(
                cmd,
                stdout=out_fh,
                stderr=err_fh,
                timeout=90,
            )
        html = out_file.read_text(encoding="utf-8", errors="replace") if out_file.exists() else ""
        err = ""
        if err_file.exists():
            err = err_file.read_text(encoding="utf-8", errors="replace")[:500]
        # Persist dump artifact for audit (technical evidence, not a market observation)
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        (ARTIFACT_DIR / "last_dump_dom.html").write_text(html, encoding="utf-8")

        title_m = re.search(r"<title[^>]*>([^<]+)", html, re.I)
        title = title_m.group(1).strip() if title_m else ""
        access = _detect_access_control(html, title)
        cards = self._extract_cards_from_html(html, max_records)
        # Also try JSON-LD / window state if present in rendered dump (public page only)
        if not any(c.get("title") for c in cards):
            cards = self._extract_cards_from_rendered_text(html, max_records) or cards
        return {
            "final_url": url,
            "page_title": title,
            "access_control": access,
            "cards": cards,
            "page_count": 1,
            "backend": "chrome_headless_dump",
            "chrome_exit": proc.returncode,
            "chrome_stderr_snip": err,
            "html_bytes": len(html.encode("utf-8", errors="ignore")),
            "error": None if cards and any(c.get("title") for c in cards) else "NO_LISTING_PAYLOAD",
        }

    def _extract_cards_from_rendered_text(self, html: str, max_records: int) -> list[dict]:
        """Best-effort from rendered HTML text nodes near item links."""
        cards = []
        # strip scripts/styles
        cleaned = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
        cleaned = re.sub(r"<style[\s\S]*?</style>", " ", cleaned, flags=re.I)
        for m in re.finditer(
            r'<a[^>]+href=["\']([^"\']*/item/[^"\'?#]+)[^"\']*["\'][^>]*>([\s\S]{0,800}?)</a>',
            cleaned,
            flags=re.I,
        ):
            if len(cards) >= max_records:
                break
            href = m.group(1)
            inner = re.sub(r"<[^>]+>", " ", m.group(2))
            inner = re.sub(r"\s+", " ", inner).strip()
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = "https://www.goofish.com" + href
            title = inner[:200] if inner else None
            # look ahead sibling text in nearby 600 chars
            snip = cleaned[m.start() : m.end() + 600]
            snip_txt = re.sub(r"<[^>]+>", " ", snip)
            snip_txt = re.sub(r"\s+", " ", snip_txt)
            cards.append(
                {
                    "title": title,
                    "price": _parse_price(snip_txt),
                    "want_count": _parse_want(snip_txt),
                    "source_url": href.split("?")[0],
                    "source_item_id": _extract_item_id(href),
                    "view_count": _safe_int_labeled(snip_txt, ("浏览", "浏览量")),
                    "comment_count": _safe_int_labeled(snip_txt, ("评论",)),
                    "share_count": _safe_int_labeled(snip_txt, ("分享",)),
                    "seller_reference": None,
                    "published_at": None,
                }
            )
        return [c for c in cards if c.get("title")]

    def _collect_playwright(self, query: str, max_records: int, headless: bool) -> dict:
        from playwright.sync_api import sync_playwright

        url = f"https://www.goofish.com/search?q={quote(query)}"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                locale="zh-CN",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                # fresh context — no user profile cookies
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            # wait for possible client render — not for hidden API
            page.wait_for_timeout(5000)
            try:
                page.wait_for_selector(
                    "a[href*='/item/'], [class*='item'], [class*='card']",
                    timeout=15000,
                )
            except Exception:
                pass
            html = page.content()
            title = page.title()
            final_url = page.url
            access = _detect_access_control(html, title)
            cards = self._extract_cards_from_dom_playwright(page, max_records)
            if not cards:
                cards = self._extract_cards_from_html(html, max_records)
            browser.close()
        return {
            "final_url": final_url,
            "page_title": title,
            "access_control": access,
            "cards": cards,
            "page_count": 1,
            "error": None if cards else "NO_LISTING_PAYLOAD",
        }

    def _extract_cards_from_dom_playwright(self, page, max_records: int) -> list[dict]:
        cards: list[dict] = []
        # Prefer anchors to item pages after render
        anchors = page.query_selector_all("a[href*='/item/']")
        seen = set()
        for a in anchors:
            if len(cards) >= max_records:
                break
            try:
                href = a.get_attribute("href") or ""
                if "/item/" not in href:
                    continue
                if href.startswith("//"):
                    href = "https:" + href
                elif href.startswith("/"):
                    href = "https://www.goofish.com" + href
                if href in seen:
                    continue
                seen.add(href)
                # climb for card text
                box = a
                text = ""
                for _ in range(4):
                    parent = box.evaluate_handle("e => e.parentElement")
                    el = parent.as_element() if parent else None
                    if not el:
                        break
                    box = el
                    text = (el.inner_text() or "").strip()
                    if len(text) > 8:
                        break
                title = (a.inner_text() or "").strip() or None
                if not title and text:
                    title = text.split("\n")[0].strip()[:200] or None
                price = _parse_price(text)
                want = _parse_want(text)
                cards.append(
                    {
                        "title": title,
                        "price": price,
                        "want_count": want,
                        "source_url": href.split("?")[0],
                        "source_item_id": _extract_item_id(href),
                        "view_count": _safe_int_labeled(text, ("浏览", "浏览量")),
                        "comment_count": _safe_int_labeled(text, ("评论",)),
                        "share_count": _safe_int_labeled(text, ("分享",)),
                        "seller_reference": None,
                        "published_at": None,
                    }
                )
            except Exception:
                continue
        return cards

    def _collect_selenium(
        self, query: str, max_records: int, headless: bool, dep: dict
    ) -> dict:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.common.by import By
        from selenium.webdriver.edge.options import Options as EdgeOptions

        url = f"https://www.goofish.com/search?q={quote(query)}"
        driver = None
        try:
            chrome_path = dep.get("chrome_or_edge_hint") or ""
            if "msedge" in chrome_path.lower() or "edge" in chrome_path.lower():
                opts = EdgeOptions()
                if headless:
                    opts.add_argument("--headless=new")
                opts.add_argument("--disable-gpu")
                opts.add_argument("--no-sandbox")
                opts.add_argument("--window-size=1280,900")
                # no user-data-dir → no stolen profile cookies
                driver = webdriver.Edge(options=opts)
            else:
                opts = ChromeOptions()
                if headless:
                    opts.add_argument("--headless=new")
                opts.add_argument("--disable-gpu")
                opts.add_argument("--no-sandbox")
                opts.add_argument("--window-size=1280,900")
                if chrome_path and Path(chrome_path).exists():
                    opts.binary_location = chrome_path
                driver = webdriver.Chrome(options=opts)

            driver.set_page_load_timeout(45)
            driver.get(url)
            time.sleep(5)
            html = driver.page_source or ""
            title = driver.title or ""
            final_url = driver.current_url
            access = _detect_access_control(html, title)
            cards: list[dict] = []
            seen = set()
            for a in driver.find_elements(By.CSS_SELECTOR, "a[href*='/item/']"):
                if len(cards) >= max_records:
                    break
                try:
                    href = a.get_attribute("href") or ""
                    if "/item/" not in href or href in seen:
                        continue
                    seen.add(href)
                    text = ""
                    try:
                        text = a.find_element(By.XPATH, "./ancestor::*[self::div or self::li][1]").text
                    except Exception:
                        text = a.text or ""
                    title_t = (a.text or "").strip() or (
                        text.split("\n")[0].strip() if text else None
                    )
                    cards.append(
                        {
                            "title": title_t[:200] if title_t else None,
                            "price": _parse_price(text),
                            "want_count": _parse_want(text),
                            "source_url": href.split("?")[0],
                            "source_item_id": _extract_item_id(href),
                            "view_count": _safe_int_labeled(text, ("浏览", "浏览量")),
                            "comment_count": _safe_int_labeled(text, ("评论",)),
                            "share_count": _safe_int_labeled(text, ("分享",)),
                            "seller_reference": None,
                            "published_at": None,
                        }
                    )
                except Exception:
                    continue
            if not cards:
                cards = self._extract_cards_from_html(html, max_records)
            return {
                "final_url": final_url,
                "page_title": title,
                "access_control": access,
                "cards": cards,
                "page_count": 1,
                "error": None if cards else "NO_LISTING_PAYLOAD",
            }
        finally:
            if driver is not None:
                driver.quit()

    def _extract_cards_from_html(self, html: str, max_records: int) -> list[dict]:
        """Fallback: regex on rendered HTML only — not hidden API calls."""
        cards = []
        seen = set()
        # Prefer goofish feed cards: <a class="feeds-item-wrap..." href=".../item?id=...">
        for m in re.finditer(
            r'<a[^>]+class="[^"]*feeds-item-wrap--[^"]*"[^>]*href="([^"]+)"[^>]*>([\s\S]*?)</a>',
            html,
            flags=re.I,
        ):
            if len(cards) >= max_records:
                break
            href = m.group(1).replace("&amp;", "&")
            block = m.group(2)
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = "https://www.goofish.com" + href
            if href in seen:
                continue
            seen.add(href)
            title = None
            tm = re.search(r'row1-wrap-title--[^"]*"\s+title="([^"]+)"', block)
            if tm:
                title = tm.group(1).strip()
            if not title:
                tm2 = re.search(r'class="main-title--[^"]*"[^>]*>([\s\S]*?)</span>', block)
                if tm2:
                    title = re.sub(r"<[^>]+>", "", tm2.group(1))
                    title = re.sub(r"\s+", " ", title).strip() or None
            price = None
            pm = re.search(
                r'number--[^"]*">(\d+)</span>(?:<span class="decimal--[^"]*">(\.\d+)</span>)?',
                block,
            )
            if pm:
                try:
                    price = float(pm.group(1) + (pm.group(2) or ""))
                except ValueError:
                    price = None
            want = None
            wm = re.search(r'title="(\d+)人想要"|>(\d+)人想要<', block)
            if wm:
                want = int(wm.group(1) or wm.group(2))
            seller = None
            sm = re.search(r'seller-text--[^"]*">([^<]+)<', block)
            if sm:
                seller = sm.group(1).strip()
            if not title:
                continue
            cards.append(
                {
                    "title": title,
                    "price": price,
                    "want_count": want,
                    "source_url": href.split("#")[0],
                    "source_item_id": _extract_item_id(href),
                    "view_count": None,
                    "comment_count": None,
                    "share_count": None,
                    "seller_reference": seller,
                    "published_at": None,
                }
            )
        if cards:
            return cards

        # Legacy path patterns /item/...
        for m in re.finditer(
            r'href=["\']([^"\']*(?:/item/[^"\'?#]+|/item\?id=\d+[^"\']*))',
            html,
            flags=re.I,
        ):
            if len(cards) >= max_records:
                break
            href = m.group(1).replace("&amp;", "&")
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = "https://www.goofish.com" + href
            if href in seen:
                continue
            seen.add(href)
            start = max(0, m.start() - 400)
            end = min(len(html), m.end() + 800)
            snip_html = html[start:end]
            snip = re.sub(r"<[^>]+>", " ", snip_html)
            snip = re.sub(r"\s+", " ", snip).strip()
            title = None
            tm = re.search(r'title=["\']([^"\']{2,200})["\']', snip_html)
            if tm and "人想要" not in tm.group(1):
                title = tm.group(1).strip()
            cards.append(
                {
                    "title": title,
                    "price": _parse_price(snip),
                    "want_count": _parse_want(snip),
                    "source_url": href.split("#")[0],
                    "source_item_id": _extract_item_id(href),
                    "view_count": None,
                    "comment_count": None,
                    "share_count": None,
                    "seller_reference": None,
                    "published_at": None,
                }
            )
        return [c for c in cards if c.get("title")] or cards


def run_browser_collection(
    *,
    query: str = "虚拟资料",
    max_records: int = 20,
    declared_origin: str = msc.ORIGIN_REAL,
) -> dict:
    return XianyuBrowserCollector().acquire(
        collection_query=query,
        max_records=max_records,
        declared_origin=declared_origin,
    )


if __name__ == "__main__":
    print(json.dumps(run_browser_collection(), ensure_ascii=False, indent=2, default=str))
