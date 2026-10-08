# 1_DATA/connectors/xianyu_interactive_connector.py — Entry 061
#
# Interactive (non-headless) PUBLIC_WEB_READ probe.
# Writes ONLY to 1_DATA/_tests/xianyu_interactive_061/ — never Current DB on first pass.
# No login / cookie steal / captcha / anti-bot bypass / hidden mtop.

from __future__ import annotations

import asyncio
import csv
import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

from connectors import xianyu_browser_connector as xbc  # noqa: E402

COLLECTOR_VERSION = "061.1.0"
COLLECTOR_ID = "col_xianyu_browser_interactive"
SOURCE_ID = "src_xianyu_marketplace"
MODE = "PUBLIC_WEB_READ"
BROWSER_MODE = "INTERACTIVE_VISIBLE"
MAX_RECORDS = 20
MAX_DETAIL_PAGES = 3

TZ_CN = timezone(timedelta(hours=8))
ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_interactive_061"
PROFILE_ROOT = ARTIFACT_DIR / "_browser_profile"


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _find_chrome() -> str | None:
    for p in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ):
        if Path(p).exists():
            return p
    return None


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _http_json(url: str, timeout: float = 5.0) -> Any:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def field_availability(records: list[dict]) -> dict:
    n = max(len(records), 1)
    keys = (
        "title",
        "price",
        "want_count",
        "source_url",
        "source_item_id",
        "view_count",
        "comment_count",
        "share_count",
        "published_at",
    )
    rates = {}
    statuses = {}
    for k in keys:
        hits = sum(1 for r in records if r.get(k) is not None and str(r.get(k)).strip() != "")
        rate = hits / n if records else 0.0
        rates[f"{k}_rate"] = round(rate, 4)
        if rate >= 0.8:
            statuses[k] = "AVAILABLE"
        elif rate > 0:
            statuses[k] = "PARTIAL"
        else:
            statuses[k] = "UNAVAILABLE"
    return {
        "records_seen": len(records),
        "records_extracted": len(records),
        "rates": rates,
        "statuses": statuses,
        "note": "data quality stats ≠ opportunity / hotness score",
    }


def _compare_stability(a: list[dict], b: list[dict]) -> dict:
    """Compare first N cards by title/price/want/url — factual only."""
    n = min(len(a), len(b), 10)
    if n == 0:
        return {"comparable": 0, "stable": False, "detail": "no_cards"}
    matches = 0
    diffs = []
    for i in range(n):
        xa, xb = a[i], b[i]
        same = (
            (xa.get("title") or "") == (xb.get("title") or "")
            and xa.get("price") == xb.get("price")
            and xa.get("want_count") == xb.get("want_count")
            and (xa.get("source_url") or "") == (xb.get("source_url") or "")
        )
        if same:
            matches += 1
        else:
            diffs.append({"index": i, "a_title": xa.get("title"), "b_title": xb.get("title")})
    return {
        "comparable": n,
        "matches": matches,
        "stable": matches == n,
        "match_rate": round(matches / n, 4),
        "diffs": diffs[:5],
    }


class _CdpClient:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self._ws = None
        self._id = 0
        self._pending: dict[int, asyncio.Future] = {}
        self._recv_task = None

    async def connect(self) -> None:
        import websockets

        self._ws = await websockets.connect(self.ws_url, max_size=20 * 1024 * 1024)
        self._recv_task = asyncio.create_task(self._reader())

    async def _reader(self) -> None:
        assert self._ws is not None
        async for raw in self._ws:
            msg = json.loads(raw)
            if "id" in msg and msg["id"] in self._pending:
                fut = self._pending.pop(msg["id"])
                if "error" in msg:
                    fut.set_exception(RuntimeError(str(msg["error"])))
                else:
                    fut.set_result(msg.get("result"))

    async def call(self, method: str, params: dict | None = None, timeout: float = 60.0) -> Any:
        assert self._ws is not None
        self._id += 1
        mid = self._id
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        self._pending[mid] = fut
        payload = {"id": mid, "method": method, "params": params or {}}
        await self._ws.send(json.dumps(payload))
        return await asyncio.wait_for(fut, timeout=timeout)

    async def close(self) -> None:
        if self._recv_task:
            self._recv_task.cancel()
            try:
                await self._recv_task
            except asyncio.CancelledError:
                pass
        if self._ws:
            await self._ws.close()


async def _wait_devtools(port: int, timeout: float = 30.0) -> str:
    deadline = time.time() + timeout
    last_err = None
    while time.time() < deadline:
        try:
            data = _http_json(f"http://127.0.0.1:{port}/json/version")
            ws = data.get("webSocketDebuggerUrl")
            if ws:
                return ws
        except Exception as exc:  # noqa: BLE001
            last_err = exc
        await asyncio.sleep(0.3)
    raise RuntimeError(f"devtools_not_ready:{last_err}")


async def _attach_page(port: int, prefer_url_substr: str) -> str:
    """Return page websocket debugger URL."""
    pages = _http_json(f"http://127.0.0.1:{port}/json/list")
    for p in pages:
        if prefer_url_substr in (p.get("url") or "") and p.get("webSocketDebuggerUrl"):
            return p["webSocketDebuggerUrl"]
    for p in pages:
        if p.get("type") == "page" and p.get("webSocketDebuggerUrl"):
            return p["webSocketDebuggerUrl"]
    # open a new tab target via browser ws
    ver = _http_json(f"http://127.0.0.1:{port}/json/version")
    browser_ws = ver["webSocketDebuggerUrl"]
    client = _CdpClient(browser_ws)
    await client.connect()
    try:
        target = await client.call(
            "Target.createTarget", {"url": "about:blank"}
        )
        tid = target["targetId"]
        pages = _http_json(f"http://127.0.0.1:{port}/json/list")
        for p in pages:
            if p.get("id") == tid and p.get("webSocketDebuggerUrl"):
                return p["webSocketDebuggerUrl"]
        raise RuntimeError("page_target_missing")
    finally:
        await client.close()


async def _read_page_html(client: _CdpClient) -> tuple[str, str, str]:
    await client.call("Runtime.enable")
    await client.call("Page.enable")
    title_r = await client.call("Runtime.evaluate", {"expression": "document.title || ''", "returnByValue": True})
    url_r = await client.call("Runtime.evaluate", {"expression": "location.href || ''", "returnByValue": True})
    html_r = await client.call(
        "Runtime.evaluate",
        {
            "expression": "document.documentElement ? document.documentElement.outerHTML : ''",
            "returnByValue": True,
        },
    )
    title = (title_r or {}).get("result", {}).get("value") or ""
    url = (url_r or {}).get("result", {}).get("value") or ""
    html = (html_r or {}).get("result", {}).get("value") or ""
    return html, title, url


async def _gentle_scroll(client: _CdpClient, steps: int = 3) -> None:
    for _ in range(steps):
        await client.call(
            "Runtime.evaluate",
            {"expression": "window.scrollBy(0, Math.min(700, window.innerHeight || 700))", "returnByValue": True},
        )
        await asyncio.sleep(1.2)


async def _wait_for_listings(client: _CdpClient, timeout_sec: float = 35.0) -> dict:
    """
    Poll visible DOM for listing signals. No hidden API.
    Expression only inspects document anchors / body text.
    """
    expr = """
(() => {
  const links = Array.from(document.querySelectorAll('a[href*="/item"]'));
  const body = document.body ? (document.body.innerText || '') : '';
  const denied = body.includes('非法访问') || body.includes('请使用正常浏览器');
  const wants = (body.match(/\d+人想要/g) || []).length;
  const emptySearch = body.includes('没有找到你想要的宝贝');
  const loading = body.includes('加载') || !!document.querySelector('[class*="loading"]');
  return {
    item_links: links.length,
    wants_text: wants,
    empty_search: emptySearch,
    denied: denied,
    loading: loading,
    title: document.title || '',
    href: location.href || ''
  };
})()
"""
    deadline = time.time() + timeout_sec
    last = {}
    while time.time() < deadline:
        r = await client.call(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True},
        )
        last = (r or {}).get("result", {}).get("value") or {}
        if last.get("denied"):
            return {"stopped": "ACCESS_DENIED", **last}
        if int(last.get("item_links") or 0) > 0 or int(last.get("wants_text") or 0) > 0:
            return {"stopped": "LISTINGS_VISIBLE", **last}
        await asyncio.sleep(1.5)
    return {"stopped": "TIMEOUT", **last}


def _extract_records(html: str, max_records: int) -> list[dict]:
    collector = xbc.XianyuBrowserCollector()
    cards = collector._extract_cards_from_html(html, max_records)
    if not any(c.get("title") for c in cards):
        cards = collector._extract_cards_from_rendered_text(html, max_records) or cards
    empty_search = "没有找到你想要的宝贝" in html
    guess_like = "empty-feed-title" in html or "猜你喜欢" in html
    page_section = (
        "guess_you_like_after_empty_search"
        if empty_search and guess_like
        else ("search_results" if not empty_search else "empty_search")
    )
    out = []
    for c in cards[:max_records]:
        title = (c.get("title") or "").strip() or None
        if not title:
            continue
        url = c.get("source_url")
        out.append(
            {
                "title": title,
                "price": c.get("price"),
                "want_count": c.get("want_count"),
                "source_url": url,
                "source_item_id": c.get("source_item_id") or xbc._extract_item_id(url),
                "view_count": c.get("view_count"),
                "comment_count": c.get("comment_count"),
                "share_count": c.get("share_count"),
                "published_at": c.get("published_at"),
                "observed_at": _now_iso(),
                "source_platform": "xianyu",
                "sales_platform": None,
                "page_section": page_section,
                "search_primary_empty": empty_search,
                "candidate_class": "REAL_CANDIDATE_EXTERNAL",
                "not_our_product": True,
                "not_our_listing": True,
            }
        )
    return out


async def _run_interactive_async(
    *,
    query: str,
    max_records: int = 20,
    open_details_if_needed: bool = True,
) -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    error_log: list[str] = []
    chrome = _find_chrome()
    if not chrome:
        return {
            "ok": False,
            "status": "FAILED",
            "error": "chrome_or_edge_missing",
            "browser_mode": BROWSER_MODE,
            "login_used": False,
            "bypass_attempted": False,
            "hidden_api_called": False,
            "current_db_write": False,
        }

    port = _free_port()
    profile = PROFILE_ROOT / f"run_{int(time.time())}"
    profile.mkdir(parents=True, exist_ok=True)
    url = f"https://www.goofish.com/search?q={quote(query)}"
    cmd = [
        chrome,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        # visible window — NOT headless
        "--new-window",
        url,
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    meta_base = {
        "browser_mode": BROWSER_MODE,
        "browser_binary": chrome,
        "devtools_port": port,
        "profile_dir": str(profile),
        "query": query,
        "page_url": url,
        "login_used": False,
        "bypass_attempted": False,
        "hidden_api_called": False,
        "user_profile_reused": False,
        "collector_version": COLLECTOR_VERSION,
        "collector_id": COLLECTOR_ID,
        "started_at": _now_iso(),
        "pid": proc.pid,
    }

    client: _CdpClient | None = None
    try:
        await asyncio.sleep(2.0)
        page_ws = await _attach_page(port, "goofish.com")
        client = _CdpClient(page_ws)
        await client.connect()
        await client.call("Page.enable")
        await client.call("Runtime.enable")
        # ensure navigation settled
        try:
            await client.call("Page.navigate", {"url": url})
            await asyncio.sleep(3.0)
        except Exception as exc:  # noqa: BLE001
            error_log.append(f"navigate_warn:{exc}")
            await asyncio.sleep(3.0)

        # Wait for rendered listing anchors (normal page hydration) — low frequency poll
        wait_meta = await _wait_for_listings(client, timeout_sec=35.0)
        error_log.append(f"listing_wait:{json.dumps(wait_meta, ensure_ascii=False)}")
        await _gentle_scroll(client, steps=3)
        await asyncio.sleep(2.0)
        # second short wait after scroll (lazy cards)
        wait_meta2 = await _wait_for_listings(client, timeout_sec=12.0)
        error_log.append(f"listing_wait_after_scroll:{json.dumps(wait_meta2, ensure_ascii=False)}")

        html1, title1, final_url1 = await _read_page_html(client)
        (ARTIFACT_DIR / "page_dump_pass1.html").write_text(html1, encoding="utf-8")

        access = xbc._detect_access_control(html1, title1)
        if access:
            report = {
                "ok": False,
                "status": "BLOCKED_BY_ACCESS_CONTROL",
                "access_control": access,
                "error_class": access,
                **meta_base,
                "page_title": title1,
                "final_url": final_url1,
                "timestamp": _now_iso(),
                "records": [],
                "field_availability": field_availability([]),
                "stability": None,
                "current_db_write": False,
                "first_real_xianyu_candidate_batch": False,
                "product_created": False,
                "listing_created": False,
                "market_event_created": False,
                "error_log": error_log,
            }
            _write_artifacts(report, [], field_availability([]), error_log)
            return report

        records1 = _extract_records(html1, max_records)

        # Detail pages only if core fields missing and public
        need_detail = (
            open_details_if_needed
            and records1
            and (
                all(r.get("want_count") is None for r in records1)
                or all(r.get("price") is None for r in records1)
            )
        )
        detail_note = None
        if need_detail:
            detail_note = "attempt_detail_for_missing_core_fields"
            for rec in records1[:MAX_DETAIL_PAGES]:
                du = rec.get("source_url")
                if not du:
                    continue
                try:
                    await client.call("Page.navigate", {"url": du})
                    await asyncio.sleep(4.0)
                    dhtml, dtitle, _ = await _read_page_html(client)
                    daccess = xbc._detect_access_control(dhtml, dtitle)
                    if daccess:
                        error_log.append(f"detail_blocked:{daccess}:{du}")
                        break
                    # enrich from detail text if search card lacked fields
                    txt = dhtml
                    if rec.get("want_count") is None:
                        rec["want_count"] = xbc._parse_want(txt)
                    if rec.get("price") is None:
                        rec["price"] = xbc._parse_price(txt)
                    if rec.get("view_count") is None:
                        rec["view_count"] = xbc._safe_int_labeled(txt, ("浏览", "浏览量"))
                except Exception as exc:  # noqa: BLE001
                    error_log.append(f"detail_error:{exc}")
            # return to search for stability pass
            try:
                await client.call("Page.navigate", {"url": url})
                await asyncio.sleep(4.0)
                await _gentle_scroll(client, steps=2)
            except Exception as exc:  # noqa: BLE001
                error_log.append(f"return_search_warn:{exc}")

        # Stability: second read of search page
        html2, title2, final_url2 = await _read_page_html(client)
        (ARTIFACT_DIR / "page_dump_pass2.html").write_text(html2, encoding="utf-8")
        access2 = xbc._detect_access_control(html2, title2)
        records2 = _extract_records(html2, max_records) if not access2 else []
        stability = _compare_stability(records1, records2)

        # Prefer pass1 enriched records as candidate set
        records = records1[:max_records]
        avail = field_availability(records)
        ok = len(records) > 0
        status = "OK" if ok else "NO_LISTING_PAYLOAD"
        search_empty = bool(records and records[0].get("search_primary_empty"))
        page_section = records[0].get("page_section") if records else None
        report = {
            "ok": ok,
            "status": status,
            **meta_base,
            "page_title": title1,
            "final_url": final_url1,
            "pass2_url": final_url2,
            "timestamp": _now_iso(),
            "records_extracted": len(records),
            "search_primary_empty": search_empty,
            "page_section": page_section,
            "field_availability": avail,
            "stability": stability,
            "detail_enrichment": detail_note,
            "access_control": None,
            "current_db_write": False,
            "first_real_xianyu_candidate_batch": ok,
            "candidate_class": "REAL_CANDIDATE_EXTERNAL" if ok else None,
            "data_origin_if_imported_later": "REAL",
            "verification_status_if_imported_later": "MANUAL_VERIFIED",
            "sales_platform": None,
            "product_created": False,
            "listing_created": False,
            "market_event_created": False,
            "opportunity_run": False,
            "learning_run": False,
            "error_log": error_log,
            "finished_at": _now_iso(),
        }
        _write_artifacts(report, records, avail, error_log)
        return report
    except Exception as exc:  # noqa: BLE001
        error_log.append(str(exc))
        report = {
            "ok": False,
            "status": "FAILED",
            "error": str(exc),
            **meta_base,
            "timestamp": _now_iso(),
            "records": [],
            "field_availability": field_availability([]),
            "current_db_write": False,
            "first_real_xianyu_candidate_batch": False,
            "error_log": error_log,
            "login_used": False,
            "bypass_attempted": False,
            "hidden_api_called": False,
        }
        _write_artifacts(report, [], field_availability([]), error_log)
        return report
    finally:
        if client:
            try:
                await client.close()
            except Exception:  # noqa: BLE001
                pass
        # Clean only the process we started
        try:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
        except Exception:  # noqa: BLE001
            pass


def _write_artifacts(
    report: dict, records: list[dict], avail: dict, error_log: list[str]
) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / "run_metadata.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "extracted_records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "field_availability.json").write_text(
        json.dumps(avail, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "error.log").write_text(
        "\n".join(error_log) if error_log else "(none)\n",
        encoding="utf-8",
    )
    # CSV
    fields = [
        "title",
        "price",
        "want_count",
        "source_url",
        "source_item_id",
        "view_count",
        "comment_count",
        "share_count",
        "published_at",
        "observed_at",
        "source_platform",
        "sales_platform",
        "candidate_class",
    ]
    with open(ARTIFACT_DIR / "extracted_records.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow(r)


def run_interactive_collection(
    *,
    query: str = "虚拟资料",
    max_records: int = 20,
) -> dict:
    """Sync entrypoint — Entry 061 first-pass test (no Current DB write)."""
    max_records = max(1, min(int(max_records or 20), MAX_RECORDS))
    query = (query or "").strip()
    if not query or query.lower() in ("xianyu", "taobao"):
        report = {
            "ok": False,
            "status": "FAILED",
            "error": "invalid_query",
            "browser_mode": BROWSER_MODE,
            "current_db_write": False,
            "first_real_xianyu_candidate_batch": False,
        }
        _write_artifacts(report, [], field_availability([]), ["invalid_query"])
        return report
    return asyncio.run(
        _run_interactive_async(query=query, max_records=max_records)
    )


def propose_collector_registry_update(result: dict) -> dict:
    """
    Registry status proposal from interactive run (does not auto-write unless caller asks).
    ACTIVE only if title+price+want+url present with stability.
    """
    avail = (result or {}).get("field_availability", {}).get("statuses") or {}
    stability = (result or {}).get("stability") or {}
    if result.get("status") == "BLOCKED_BY_ACCESS_CONTROL":
        status = "BLOCKED"
    elif not result.get("ok"):
        status = "LIMITED"
    else:
        core = all(
            avail.get(k) in ("AVAILABLE", "PARTIAL")
            for k in ("title", "price", "want_count", "source_url")
        )
        want_ok = avail.get("want_count") == "AVAILABLE"
        if core and want_ok and stability.get("stable"):
            status = "ACTIVE"
        else:
            status = "LIMITED"
    return {
        "collector_id": COLLECTOR_ID,
        "source_id": SOURCE_ID,
        "mode": MODE,
        "version": COLLECTOR_VERSION,
        "status": status,
        "supported_fields": avail,
        "notes": "Entry 061 interactive visible browser; first pass test-dir only",
    }


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "虚拟资料"
    out = run_interactive_collection(query=q, max_records=20)
    print(json.dumps({k: out.get(k) for k in (
        "ok", "status", "access_control", "records_extracted",
        "first_real_xianyu_candidate_batch", "current_db_write",
        "field_availability", "stability",
    )}, ensure_ascii=False, indent=2, default=str))
