# 1_DATA/connectors/xianyu_targeted_search_062.py — Entry 062
#
# Targeted interactive search: SEARCH_RESULT only (exclude 猜你喜欢).
# Want-count availability audit: VISIBLE_ON_CARD / MISSING_ON_CARD /
# AVAILABLE_ON_DETAIL / UNAVAILABLE / UNKNOWN.
# Test-dir output only — no Current DB write.
# No login / cookie / captcha bypass / hidden API.

from __future__ import annotations

import asyncio
import csv
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

from connectors import xianyu_browser_connector as xbc  # noqa: E402
from connectors import xianyu_interactive_connector as xic  # noqa: E402

COLLECTOR_VERSION = "062.1.0"
COLLECTOR_ID = "col_xianyu_targeted_search"
MODE = "PUBLIC_WEB_READ"
BROWSER_MODE = "INTERACTIVE_VISIBLE"
MAX_RECORDS = 20
MAX_QUERIES = 3
MAX_DETAIL = 3

ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_targeted_search_062"
PROFILE_ROOT = ARTIFACT_DIR / "_browser_profile"

WANT_VISIBLE_ON_CARD = "VISIBLE_ON_CARD"
WANT_MISSING_ON_CARD = "MISSING_ON_CARD"
WANT_AVAILABLE_ON_DETAIL = "AVAILABLE_ON_DETAIL"
WANT_UNAVAILABLE = "UNAVAILABLE"
WANT_UNKNOWN = "UNKNOWN"

ORIGIN_SEARCH = "SEARCH_RESULT"
ORIGIN_RECOMMENDED = "RECOMMENDED_RESULT"
ORIGIN_UNKNOWN = "UNKNOWN"

# Prefer queries likely to yield primary SEARCH_RESULT in anonymous browser.
# Digital-template queries (Excel模板/PPT模板/简历模板) returned empty+猜你喜欢 in 062 probe.
CANDIDATE_QUERIES = ("手机壳", "电子书", "Excel模板")


def _now() -> str:
    return xic._now_iso()


def classify_page_search_state(html: str) -> dict:
    empty = "没有找到你想要的宝贝" in html or "empty-text-notfound" in html
    guess = "猜你喜欢" in html or "empty-feed-title" in html
    return {
        "search_primary_empty": empty,
        "has_guess_you_like": guess,
        "has_feeds": "feeds-item-wrap--" in html,
    }


def _parse_want_from_card_block(block: str) -> tuple[int | None, str]:
    """
    Returns (value, status).
    Explicit 0人想要 → (0, VISIBLE_ON_CARD).
    No field → (None, MISSING_ON_CARD).
    Never invent.
    """
    # title="N人想要" or visible text N人想要
    m = re.search(r'title="(\d+)人想要"', block)
    if m:
        return int(m.group(1)), WANT_VISIBLE_ON_CARD
    m = re.search(r">(\d+)人想要<", block)
    if m:
        return int(m.group(1)), WANT_VISIBLE_ON_CARD
    m = re.search(r"(\d+)\s*人想要", block)
    if m:
        return int(m.group(1)), WANT_VISIBLE_ON_CARD
    # Explicit zero variants already covered by \d+
    return None, WANT_MISSING_ON_CARD


def _parse_price_from_card(block: str) -> float | None:
    pm = re.search(
        r'number--[^"]*">(\d+)</span>(?:<span class="decimal--[^"]*">(\.\d+)</span>)?',
        block,
    )
    if not pm:
        return None
    try:
        return float(pm.group(1) + (pm.group(2) or ""))
    except ValueError:
        return None


def extract_classified_cards(html: str, max_records: int = 20) -> list[dict]:
    """
    Extract feed cards with result_origin.
    Cards inside empty-feed-container / after 猜你喜欢 → RECOMMENDED_RESULT.
    Other feeds-item-wrap on non-empty search page → SEARCH_RESULT.
    """
    state = classify_page_search_state(html)
    # Mark recommended regions by slicing empty-feed blocks
    recommended_spans: list[tuple[int, int]] = []
    for m in re.finditer(
        r'class="[^"]*empty-feed-container--[^"]*"[\s\S]*?(?=<div class="[^"]*footer|</body>|$)',
        html,
        flags=re.I,
    ):
        recommended_spans.append((m.start(), m.end()))
    # Also treat any card after empty-feed-title as recommended until end of that container
    for m in re.finditer(r'empty-feed-title--[^"]*"[\s\S]{0,200000}', html):
        recommended_spans.append((m.start(), min(len(html), m.start() + 200000)))

    def in_recommended(pos: int) -> bool:
        return any(a <= pos < b for a, b in recommended_spans)

    cards: list[dict] = []
    seen: set[str] = set()
    for m in re.finditer(
        r'<a[^>]+class="[^"]*feeds-item-wrap--[^"]*"[^>]*href="([^"]+)"[^>]*>([\s\S]*?)</a>',
        html,
        flags=re.I,
    ):
        href = m.group(1).replace("&amp;", "&")
        block = m.group(2)
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = "https://www.goofish.com" + href
        if href in seen:
            continue
        seen.add(href)

        if in_recommended(m.start()) or state["search_primary_empty"]:
            # On empty primary search, all visible feed cards are recommendations
            origin = ORIGIN_RECOMMENDED
        else:
            origin = ORIGIN_SEARCH

        title = None
        tm = re.search(r'row1-wrap-title--[^"]*"\s+title="([^"]+)"', block)
        if tm:
            title = tm.group(1).strip()
        if not title:
            tm2 = re.search(r'class="main-title--[^"]*"[^>]*>([\s\S]*?)</span>', block)
            if tm2:
                title = re.sub(r"<[^>]+>", "", tm2.group(1))
                title = re.sub(r"\s+", " ", title).strip() or None
        if not title:
            continue

        price = _parse_price_from_card(block)
        want, want_status = _parse_want_from_card_block(block)
        item_id = xbc._extract_item_id(href)
        seller = None
        sm = re.search(r'seller-text--[^"]*">([^<]+)<', block)
        if sm:
            seller = sm.group(1).strip()

        cards.append(
            {
                "title": title,
                "price": price,
                "want_count": want,  # may be 0 or None — never coerce None→0
                "want_count_status": want_status,
                "want_count_card": want,
                "want_count_detail": None,
                "source_url": href.split("#")[0],
                "source_item_id": item_id,
                "view_count": None,
                "comment_count": None,
                "share_count": None,
                "published_at": None,
                "observed_at": _now(),
                "result_origin": origin,
                "source_platform": "xianyu",
                "sales_platform": None,
                "seller_reference": seller,
                "candidate_class": "REAL_CANDIDATE_EXTERNAL",
                "valid_without_want_count": True,
                "not_our_product": True,
                "not_our_listing": True,
                "evidence": {
                    "card_has_want_text": want_status == WANT_VISIBLE_ON_CARD,
                    "card_selector": "a.feeds-item-wrap",
                },
            }
        )

    return cards


def filter_search_results(cards: list[dict], max_records: int = 20) -> list[dict]:
    return [c for c in cards if c.get("result_origin") == ORIGIN_SEARCH][:max_records]


def want_count_audit(search_records: list[dict]) -> dict:
    n = len(search_records)
    visible = sum(1 for r in search_records if r.get("want_count_status") == WANT_VISIBLE_ON_CARD)
    missing = sum(1 for r in search_records if r.get("want_count_status") == WANT_MISSING_ON_CARD)
    detail = sum(1 for r in search_records if r.get("want_count_status") == WANT_AVAILABLE_ON_DETAIL)
    unavail = sum(1 for r in search_records if r.get("want_count_status") == WANT_UNAVAILABLE)
    unknown = sum(1 for r in search_records if r.get("want_count_status") == WANT_UNKNOWN)
    # After detail enrichment, total observable = visible on card OR detail
    observable = sum(
        1
        for r in search_records
        if r.get("want_count") is not None
        and r.get("want_count_status")
        in (WANT_VISIBLE_ON_CARD, WANT_AVAILABLE_ON_DETAIL)
    )
    still_missing = sum(1 for r in search_records if r.get("want_count") is None)
    return {
        "search_results_count": n,
        "status_distribution": {
            WANT_VISIBLE_ON_CARD: visible,
            WANT_MISSING_ON_CARD: missing,
            WANT_AVAILABLE_ON_DETAIL: detail,
            WANT_UNAVAILABLE: unavail,
            WANT_UNKNOWN: unknown,
        },
        "card_visible_rate": round(visible / n, 4) if n else 0.0,
        "detail_available_rate": round(detail / n, 4) if n else 0.0,
        "total_observable_rate": round(observable / n, 4) if n else 0.0,
        "still_null_count": still_missing,
        "still_null_rate": round(still_missing / n, 4) if n else 0.0,
        "null_vs_zero_rule": "NULL means field absent; 0 means page showed 0人想要",
        "login_causation": {
            "login_used": False,
            "conclusion": "NOT_PROVEN",
            "note": (
                "Anonymous browser only. Cannot conclude missing want_count "
                "is caused by not being logged in."
            ),
        },
        "valid_without_want_count": True,
        "note": "missing ≠ zero; unavailable ≠ proven login-related",
    }


def field_availability_search(records: list[dict]) -> dict:
    n = max(len(records), 1)
    def rate(key: str) -> float:
        if not records:
            return 0.0
        hits = sum(
            1
            for r in records
            if r.get(key) is not None and str(r.get(key)).strip() != ""
        )
        return round(hits / len(records), 4)

    want_visible = sum(
        1 for r in records if r.get("want_count_status") == WANT_VISIBLE_ON_CARD
    )
    want_missing = sum(
        1 for r in records if r.get("want_count_status") == WANT_MISSING_ON_CARD
    )
    return {
        "search_results_seen": len(records),
        "accepted": len(records),
        "rejected": 0,
        "duplicate": 0,
        "title_rate": rate("title"),
        "price_rate": rate("price"),
        "want_count_visible_rate": round(want_visible / n, 4) if records else 0.0,
        "want_count_missing_rate": round(want_missing / n, 4) if records else 0.0,
        "url_rate": rate("source_url"),
        "item_id_rate": rate("source_item_id"),
        "note": "data availability ≠ commercial score",
    }


def _write_outputs(
    report: dict,
    records: list[dict],
    avail: dict,
    want_audit: dict,
    error_log: list[str],
) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / "run_metadata.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (ARTIFACT_DIR / "extracted_records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (ARTIFACT_DIR / "field_availability.json").write_text(
        json.dumps(avail, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (ARTIFACT_DIR / "want_count_audit.json").write_text(
        json.dumps(want_audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (ARTIFACT_DIR / "error.log").write_text(
        "\n".join(error_log) if error_log else "(none)\n", encoding="utf-8"
    )
    fields = [
        "result_origin",
        "title",
        "price",
        "want_count",
        "want_count_status",
        "want_count_card",
        "want_count_detail",
        "source_url",
        "source_item_id",
        "observed_at",
        "query",
        "source_platform",
        "sales_platform",
        "valid_without_want_count",
        "candidate_class",
    ]
    with open(ARTIFACT_DIR / "extracted_records.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow(r)


async def _enrich_want_from_detail(
    client: xic._CdpClient, records: list[dict], error_log: list[str]
) -> None:
    """Open up to 3 SEARCH_RESULT cards missing want_count on public detail pages."""
    targets = [
        r
        for r in records
        if r.get("result_origin") == ORIGIN_SEARCH
        and r.get("want_count_status") == WANT_MISSING_ON_CARD
        and r.get("source_url")
    ][:MAX_DETAIL]
    for rec in targets:
        url = rec["source_url"]
        try:
            await client.call("Page.navigate", {"url": url})
            await asyncio.sleep(4.0)
            html, title, _ = await xic._read_page_html(client)
            access = xbc._detect_access_control(html, title)
            if access:
                error_log.append(f"detail_blocked:{access}:{url}")
                rec["want_count_status"] = WANT_UNAVAILABLE
                rec["evidence"] = {
                    **(rec.get("evidence") or {}),
                    "detail_access_control": access,
                }
                break
            # login wall soft check
            if "请先登录" in html or "登录后继续" in html:
                error_log.append(f"detail_login_wall:{url}")
                rec["want_count_status"] = WANT_UNAVAILABLE
                rec["evidence"] = {
                    **(rec.get("evidence") or {}),
                    "detail_login_wall": True,
                }
                continue
            want = xbc._parse_want(html)
            # also title="N人想要" on detail
            if want is None:
                m = re.search(r'title="(\d+)人想要"|>(\d+)人想要<', html)
                if m:
                    want = int(m.group(1) or m.group(2))
            rec["want_count_detail"] = want
            if want is not None:
                rec["want_count"] = want
                rec["want_count_status"] = WANT_AVAILABLE_ON_DETAIL
            else:
                rec["want_count_status"] = WANT_UNAVAILABLE
            rec["evidence"] = {
                **(rec.get("evidence") or {}),
                "detail_checked": True,
                "detail_url": url,
            }
        except Exception as exc:  # noqa: BLE001
            error_log.append(f"detail_error:{exc}")
            rec["want_count_status"] = WANT_UNKNOWN


async def _search_via_ui(client: xic._CdpClient, query: str, error_log: list[str]) -> None:
    """
    Normal browser interaction: focus search input, type query, submit.
    Not a bypass — mirrors user typing in the visible search box.
    """
    # Escape for JS string
    q = json.dumps(query, ensure_ascii=False)
    expr = f"""
(async () => {{
  const input = document.querySelector('input.search-input--WY2l9QD3, input[class*="search-input"], form[class*="search"] input[type="text"]');
  if (!input) return {{ok:false, reason:'no_input'}};
  input.focus();
  input.value = '';
  const nativeSet = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  nativeSet.call(input, {q});
  input.dispatchEvent(new Event('input', {{bubbles:true}}));
  input.dispatchEvent(new Event('change', {{bubbles:true}}));
  const btn = document.querySelector('button.search-icon--bewLHteU, button[class*="search-icon"], form[class*="search"] button[type="submit"]');
  if (btn) {{ btn.click(); return {{ok:true, method:'button_click'}}; }}
  const form = input.closest('form');
  if (form) {{ form.requestSubmit ? form.requestSubmit() : form.submit(); return {{ok:true, method:'form_submit'}}; }}
  input.dispatchEvent(new KeyboardEvent('keydown', {{key:'Enter', code:'Enter', keyCode:13, bubbles:true}}));
  return {{ok:true, method:'enter_key'}};
}})()
"""
    try:
        r = await client.call("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True})
        error_log.append(f"ui_search:{json.dumps((r or {}).get('result', {}).get('value'), ensure_ascii=False)}")
    except Exception as exc:  # noqa: BLE001
        error_log.append(f"ui_search_error:{exc}")


async def _collect_one_query(
    client: xic._CdpClient,
    query: str,
    max_records: int,
    error_log: list[str],
) -> dict:
    url = f"https://www.goofish.com/search?q={quote(query)}"
    # First land on home, then UI-search (closer to normal browsing than deep-link only)
    try:
        await client.call("Page.navigate", {"url": "https://www.goofish.com/"})
        await asyncio.sleep(3.0)
        await _search_via_ui(client, query, error_log)
        await asyncio.sleep(4.0)
    except Exception as exc:  # noqa: BLE001
        error_log.append(f"ui_path_fallback:{exc}")
        await client.call("Page.navigate", {"url": url})
        await asyncio.sleep(3.0)

    # If still not on search, navigate directly
    html_probe, _, href_probe = await xic._read_page_html(client)
    if "/search" not in (href_probe or ""):
        error_log.append("fallback_direct_search_url")
        await client.call("Page.navigate", {"url": url})
        await asyncio.sleep(3.0)
    wait1 = await xic._wait_for_listings(client, timeout_sec=30.0)
    error_log.append(f"wait:{query}:{json.dumps(wait1, ensure_ascii=False)}")
    if wait1.get("denied"):
        return {
            "ok": False,
            "status": "BLOCKED_BY_ACCESS_CONTROL",
            "access_control": "ACCESS_DENIED",
            "query": query,
            "search_url": url,
            "records": [],
        }
    await xic._gentle_scroll(client, steps=3)
    await asyncio.sleep(1.5)
    wait2 = await xic._wait_for_listings(client, timeout_sec=10.0)
    error_log.append(f"wait2:{query}:{json.dumps(wait2, ensure_ascii=False)}")

    html1, title1, final_url = await xic._read_page_html(client)
    dump = ARTIFACT_DIR / f"page_dump_{query}.html"
    dump.write_text(html1, encoding="utf-8")

    access = xbc._detect_access_control(html1, title1)
    if access:
        return {
            "ok": False,
            "status": "BLOCKED_BY_ACCESS_CONTROL",
            "access_control": access,
            "query": query,
            "search_url": url,
            "page_title": title1,
            "records": [],
        }

    all_cards = extract_classified_cards(html1, max_records=50)
    search_cards = filter_search_results(all_cards, max_records=max_records)
    recommended_n = sum(1 for c in all_cards if c.get("result_origin") == ORIGIN_RECOMMENDED)
    state = classify_page_search_state(html1)

    # Stability pass on search page
    html2, _, _ = await xic._read_page_html(client)
    cards2 = filter_search_results(extract_classified_cards(html2, 50), max_records)
    stability = xic._compare_stability(search_cards, cards2)

    # Detail enrichment for missing want
    if search_cards:
        await _enrich_want_from_detail(client, search_cards, error_log)
        # return to search
        try:
            await client.call("Page.navigate", {"url": url})
            await asyncio.sleep(3.0)
        except Exception as exc:  # noqa: BLE001
            error_log.append(f"return_search:{exc}")

    for r in search_cards:
        r["query"] = query
        r["search_url"] = final_url or url

    return {
        "ok": len(search_cards) > 0,
        "status": "OK" if search_cards else "NO_SEARCH_RESULTS",
        "query": query,
        "search_url": final_url or url,
        "page_title": title1,
        "page_state": state,
        "all_cards_seen": len(all_cards),
        "recommended_excluded": recommended_n,
        "search_results": len(search_cards),
        "records": search_cards,
        "stability": stability,
        "access_control": None,
    }


async def run_targeted_search_async(
    queries: tuple[str, ...] | list[str] | None = None,
    max_records: int = 20,
) -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    error_log: list[str] = []
    queries = list(queries or CANDIDATE_QUERIES)[:MAX_QUERIES]
    chrome = xic._find_chrome()
    if not chrome:
        report = {
            "ok": False,
            "status": "FAILED",
            "error": "chrome_or_edge_missing",
            "login_used": False,
            "current_db_write": False,
            "first_real_xianyu_search_batch": False,
        }
        _write_outputs(report, [], field_availability_search([]), want_count_audit([]), ["chrome_missing"])
        return report

    port = xic._free_port()
    profile = PROFILE_ROOT / f"run_{int(time.time())}"
    profile.mkdir(parents=True, exist_ok=True)
    # start on about:blank
    cmd = [
        chrome,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        "--new-window",
        "about:blank",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    meta = {
        "browser_mode": BROWSER_MODE,
        "browser_binary": chrome,
        "operating_mode": BROWSER_MODE,
        "collector_version": COLLECTOR_VERSION,
        "collector_id": COLLECTOR_ID,
        "devtools_port": port,
        "profile_dir": str(profile),
        "user_profile_reused": False,
        "login_used": False,
        "bypass_attempted": False,
        "hidden_api_called": False,
        "pid": proc.pid,
        "started_at": _now(),
        "queries_planned": queries,
    }
    client: xic._CdpClient | None = None
    try:
        await asyncio.sleep(2.0)
        page_ws = await xic._attach_page(port, "about:")
        client = xic._CdpClient(page_ws)
        await client.connect()
        await client.call("Page.enable")
        await client.call("Runtime.enable")
        # browser version
        try:
            ver = await client.call("Browser.getVersion")
            meta["browser_version"] = (ver or {}).get("product") or (ver or {}).get("userAgent")
        except Exception:  # noqa: BLE001
            meta["browser_version"] = None

        attempt_log = []
        chosen = None
        for q in queries:
            result = await _collect_one_query(client, q, max_records, error_log)
            attempt_log.append(
                {
                    "query": q,
                    "status": result.get("status"),
                    "search_results": result.get("search_results", 0),
                    "recommended_excluded": result.get("recommended_excluded", 0),
                    "page_state": result.get("page_state"),
                }
            )
            if result.get("status") == "BLOCKED_BY_ACCESS_CONTROL":
                report = {
                    "ok": False,
                    "status": "BLOCKED_BY_ACCESS_CONTROL",
                    **meta,
                    "access_control": result.get("access_control"),
                    "query_attempts": attempt_log,
                    "current_db_write": False,
                    "first_real_xianyu_search_batch": False,
                    "error_log": error_log,
                    "finished_at": _now(),
                }
                _write_outputs(
                    report, [], field_availability_search([]), want_count_audit([]), error_log
                )
                return report
            if result.get("ok") and result.get("records"):
                chosen = result
                break

        if not chosen:
            report = {
                "ok": False,
                "status": "NO_SEARCH_RESULTS_IN_TEST_SCOPE",
                **meta,
                "query_attempts": attempt_log,
                "current_db_write": False,
                "first_real_xianyu_search_batch": False,
                "note": "Did not fill with 猜你喜欢 / RECOMMENDED_RESULT",
                "error_log": error_log,
                "finished_at": _now(),
            }
            _write_outputs(
                report, [], field_availability_search([]), want_count_audit([]), error_log
            )
            return report

        records = chosen["records"]
        avail = field_availability_search(records)
        want_audit = want_count_audit(records)
        report = {
            "ok": True,
            "status": "OK",
            **meta,
            "query": chosen["query"],
            "search_url": chosen["search_url"],
            "page_title": chosen.get("page_title"),
            "page_state": chosen.get("page_state"),
            "query_attempts": attempt_log,
            "search_results_count": len(records),
            "recommended_excluded": chosen.get("recommended_excluded"),
            "result_origin_policy": "only SEARCH_RESULT accepted for this batch",
            "field_availability": avail,
            "want_count_audit": want_audit,
            "stability": chosen.get("stability"),
            "access_control": None,
            "current_db_write": False,
            "first_real_xianyu_search_batch": True,
            "candidate_class": "REAL_CANDIDATE_EXTERNAL",
            "data_origin_if_imported_later": "REAL",
            "verification_status_if_imported_later": "MANUAL_VERIFIED",
            "product_created": False,
            "listing_created": False,
            "market_event_created": False,
            "opportunity_run": False,
            "learning_run": False,
            "sales_platform": None,
            "error_log": error_log,
            "finished_at": _now(),
        }
        _write_outputs(report, records, avail, want_audit, error_log)
        return report
    except Exception as exc:  # noqa: BLE001
        error_log.append(str(exc))
        report = {
            "ok": False,
            "status": "FAILED",
            "error": str(exc),
            **meta,
            "current_db_write": False,
            "first_real_xianyu_search_batch": False,
            "error_log": error_log,
            "finished_at": _now(),
        }
        _write_outputs(report, [], field_availability_search([]), want_count_audit([]), error_log)
        return report
    finally:
        if client:
            try:
                await client.close()
            except Exception:  # noqa: BLE001
                pass
        try:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
        except Exception:  # noqa: BLE001
            pass


def run_targeted_search(
    queries: tuple[str, ...] | list[str] | None = None,
    max_records: int = 20,
) -> dict:
    max_records = max(1, min(int(max_records or 20), MAX_RECORDS))
    return asyncio.run(run_targeted_search_async(queries=queries, max_records=max_records))


if __name__ == "__main__":
    out = run_targeted_search()
    print(
        json.dumps(
            {
                k: out.get(k)
                for k in (
                    "ok",
                    "status",
                    "query",
                    "search_results_count",
                    "first_real_xianyu_search_batch",
                    "want_count_audit",
                    "field_availability",
                    "query_attempts",
                )
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )
