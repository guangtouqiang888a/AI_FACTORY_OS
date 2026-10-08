# 1_DATA/connectors/xianyu_search_session_063.py — Entry 063
#
# SearchSession + Search Controller (minimal) + Page Collector (attach/read).
# Search Control ≠ Data Collection. SEARCH_RESULT ≠ RECOMMENDED_FEED.
# Test-dir only. No login / cookies / bypass / hidden API / Current DB write.

from __future__ import annotations

import asyncio
import csv
import json
import secrets
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

from connectors import xianyu_browser_connector as xbc  # noqa: E402
from connectors import xianyu_interactive_connector as xic  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402

COLLECTOR_VERSION = "063.1.0"
COLLECTOR_ID = "col_xianyu_search_session"
MODE = "PUBLIC_WEB_READ"
BROWSER_MODE = "INTERACTIVE_VISIBLE"
MAX_RECORDS = 20
MAX_DETAIL = 3

ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_search_session_063"
PROFILE_ROOT = ARTIFACT_DIR / "_browser_profile"

# Page-level search states (Entry 063)
STATE_SEARCH_RESULT = "SEARCH_RESULT"
STATE_EMPTY = "EMPTY_SEARCH_RESULT"
STATE_RECOMMENDED = "RECOMMENDED_FEED"
STATE_ERROR = "ERROR"
STATE_BLOCKED = "ACCESS_BLOCKED"
STATE_UNKNOWN = "UNKNOWN"


@dataclass
class SearchSession:
    session_id: str
    browser: str
    source: str = "xianyu"
    query: str | None = None
    search_url: str | None = None
    started_at: str = ""
    status: str = "CREATED"
    browser_version: str | None = None
    operating_mode: str = BROWSER_MODE
    login_used: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        # never include secrets
        d.pop("password", None)
        d.pop("cookie", None)
        d.pop("token", None)
        return d


def new_session(*, browser: str = "chrome", query: str | None = None) -> SearchSession:
    return SearchSession(
        session_id=f"ss_{secrets.token_hex(6)}",
        browser=browser,
        query=query,
        started_at=ts062._now(),
        status="CREATED",
    )


def classify_search_state(html: str, *, page_title: str = "", final_url: str = "") -> dict:
    """
    Evidence-based page state. URL alone is insufficient for SEARCH_RESULT.
    """
    access = xbc._detect_access_control(html, page_title)
    if access:
        return {
            "search_state": STATE_BLOCKED,
            "access_control": access,
            "evidence": {"access_control": access, "url": final_url},
        }
    page = ts062.classify_page_search_state(html)
    cards = ts062.extract_classified_cards(html, max_records=50)
    search_n = sum(1 for c in cards if c.get("result_origin") == ts062.ORIGIN_SEARCH)
    rec_n = sum(1 for c in cards if c.get("result_origin") == ts062.ORIGIN_RECOMMENDED)

    if page["search_primary_empty"]:
        state = STATE_EMPTY
        if page["has_guess_you_like"] or rec_n > 0:
            # empty primary + recommendations present
            secondary = STATE_RECOMMENDED
        else:
            secondary = None
        return {
            "search_state": state,
            "secondary_feed": secondary,
            "search_result_count": 0,
            "recommended_count": rec_n,
            "evidence": {
                "empty_text": True,
                "guess_you_like": page["has_guess_you_like"],
                "url": final_url,
                "url_is_search": "/search" in (final_url or ""),
                "note": "URL /search alone does not imply SEARCH_RESULT",
            },
        }
    if search_n > 0:
        return {
            "search_state": STATE_SEARCH_RESULT,
            "secondary_feed": STATE_RECOMMENDED if rec_n else None,
            "search_result_count": search_n,
            "recommended_count": rec_n,
            "evidence": {
                "empty_text": False,
                "search_cards": search_n,
                "url": final_url,
            },
        }
    if rec_n > 0:
        return {
            "search_state": STATE_RECOMMENDED,
            "search_result_count": 0,
            "recommended_count": rec_n,
            "evidence": {"url": final_url},
        }
    return {
        "search_state": STATE_UNKNOWN,
        "search_result_count": 0,
        "recommended_count": 0,
        "evidence": {"url": final_url, "has_feeds": page["has_feeds"]},
    }


def apply_result_positions(records: list[dict]) -> list[dict]:
    out = []
    for i, r in enumerate(records, start=1):
        rr = dict(r)
        rr["result_position"] = i
        out.append(rr)
    return out


def filter_minimum_want(
    records: list[dict],
    minimum_want_count: int | None,
) -> dict:
    """
    Filter only records with want_count != NULL.
    NULL → separate bucket (never treat as 0).
    """
    if minimum_want_count is None:
        return {
            "minimum_want_count": None,
            "included": list(records),
            "excluded_below_min": [],
            "unknown_null_want": [],
            "note": "filter disabled",
        }
    included, excluded, unknown = [], [], []
    for r in records:
        w = r.get("want_count")
        if w is None:
            unknown.append(r)
        elif int(w) >= int(minimum_want_count):
            included.append(r)
        else:
            excluded.append(r)
    return {
        "minimum_want_count": minimum_want_count,
        "included": included,
        "excluded_below_min": excluded,
        "unknown_null_want": unknown,
        "counts": {
            "included": len(included),
            "excluded_below_min": len(excluded),
            "unknown_null_want": len(unknown),
        },
        "note": "NULL want_count never treated as 0 for filter",
    }


def collect_from_html(
    html: str,
    *,
    session: SearchSession,
    page_title: str = "",
    final_url: str = "",
    max_records: int = 20,
    minimum_want_count: int | None = None,
) -> dict:
    """Page Collection only — does not perform search control."""
    state = classify_search_state(html, page_title=page_title, final_url=final_url)
    all_cards = ts062.extract_classified_cards(html, max_records=50)
    search = ts062.filter_search_results(all_cards, max_records=max_records)
    search = apply_result_positions(search)
    for r in search:
        r["query"] = session.query
        r["search_url"] = final_url or session.search_url
        r["session_id"] = session.session_id
        r["collector_version"] = COLLECTOR_VERSION
        r["source"] = "xianyu"
        r["source_platform"] = "xianyu"
        r["sales_platform"] = None

    recommended = [
        c for c in all_cards if c.get("result_origin") == ts062.ORIGIN_RECOMMENDED
    ][:max_records]
    recommended = apply_result_positions(recommended)

    want_audit = ts062.want_count_audit(search)
    avail = ts062.field_availability_search(search)
    want_filter = filter_minimum_want(search, minimum_want_count)

    if state["search_state"] == STATE_SEARCH_RESULT and search:
        collector_status = (
            "COLLECTOR_FEASIBLE"
            if want_audit.get("still_null_rate", 1) == 0
            else "COLLECTOR_FEASIBLE_WITH_MISSING_FIELDS"
        )
    elif search:
        collector_status = "COLLECTOR_FEASIBLE_WITH_MISSING_FIELDS"
    else:
        collector_status = "COLLECTOR_NO_SEARCH_RESULT_ON_PAGE"

    return {
        "ok": state["search_state"] == STATE_SEARCH_RESULT and len(search) > 0,
        "collector_status": collector_status,
        "search_state": state,
        "search_records": search,
        "recommended_records": recommended,
        "field_availability": avail,
        "want_count_audit": want_audit,
        "minimum_want_filter": {
            k: v
            for k, v in want_filter.items()
            if k not in ("included", "excluded_below_min", "unknown_null_want")
        },
        "minimum_want_included": want_filter["included"],
        "minimum_want_unknown_null": want_filter["unknown_null_want"],
        "first_real_xianyu_search_candidate": len(search) > 0,
        "login_used": False,
        "bypass_attempted": False,
        "hidden_api_called": False,
    }


def _write_artifacts(
    *,
    session: SearchSession,
    search_control: dict,
    collection: dict,
    error_log: list[str],
) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / "session_metadata.json").write_text(
        json.dumps(
            {
                "session": session.to_dict(),
                "search_control": search_control,
                "collector_status": collection.get("collector_status"),
                "first_real_xianyu_search_candidate": collection.get(
                    "first_real_xianyu_search_candidate"
                ),
                "current_db_write": False,
                "collector_version": COLLECTOR_VERSION,
                "finished_at": ts062._now(),
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "search_state.json").write_text(
        json.dumps(collection.get("search_state") or {}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    records = collection.get("search_records") or []
    (ARTIFACT_DIR / "extracted_records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (ARTIFACT_DIR / "field_availability.json").write_text(
        json.dumps(collection.get("field_availability") or {}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "want_count_audit.json").write_text(
        json.dumps(collection.get("want_count_audit") or {}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "recommended_excluded.json").write_text(
        json.dumps(
            {
                "count": len(collection.get("recommended_records") or []),
                "note": "RECOMMENDED_FEED excluded from target search evidence",
                "sample": (collection.get("recommended_records") or [])[:3],
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    (ARTIFACT_DIR / "errors.log").write_text(
        "\n".join(error_log) if error_log else "(none)\n", encoding="utf-8"
    )
    fields = [
        "result_position",
        "result_origin",
        "title",
        "price",
        "want_count",
        "want_count_status",
        "source_url",
        "source_item_id",
        "query",
        "search_url",
        "session_id",
        "observed_at",
        "source_platform",
        "sales_platform",
        "valid_without_want_count",
    ]
    with open(ARTIFACT_DIR / "extracted_records.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow(r)


async def attach_existing_browser_session(
    port: int,
    *,
    url_substr: str = "goofish.com",
) -> tuple[xic._CdpClient, dict]:
    """
    Attach to an already-running Chrome with --remote-debugging-port.
    Reads page DOM only — does not read cookies/storage/credentials.
    """
    page_ws = await xic._attach_page(port, url_substr)
    client = xic._CdpClient(page_ws)
    await client.connect()
    await client.call("Page.enable")
    await client.call("Runtime.enable")
    # Explicitly do NOT call Network.getAllCookies / Storage APIs
    meta = {
        "attach_mode": "existing_devtools",
        "devtools_port": port,
        "cookies_read": False,
        "storage_read": False,
        "credentials_read": False,
    }
    return client, meta


async def _search_control(
    client: xic._CdpClient,
    query: str,
    error_log: list[str],
) -> dict:
    """Minimal Search Controller: navigate / UI type / submit. No bypass."""
    url = f"https://www.goofish.com/search?q={quote(query)}"
    try:
        await client.call("Page.navigate", {"url": "https://www.goofish.com/"})
        await asyncio.sleep(3.0)
        await ts062._search_via_ui(client, query, error_log)
        await asyncio.sleep(4.0)
        html, title, href = await xic._read_page_html(client)
        if "/search" not in (href or ""):
            error_log.append("search_control_fallback_url")
            await client.call("Page.navigate", {"url": url})
            await asyncio.sleep(4.0)
            html, title, href = await xic._read_page_html(client)
        await xic._gentle_scroll(client, steps=2)
        await asyncio.sleep(1.5)
        wait = await xic._wait_for_listings(client, timeout_sec=25.0)
        error_log.append(f"search_control_wait:{json.dumps(wait, ensure_ascii=False)}")
        html, title, href = await xic._read_page_html(client)
        state = classify_search_state(html, page_title=title, final_url=href)
        # Map empty primary to PARTIAL (control reached search page but not SEARCH_RESULT)
        if state["search_state"] == STATE_BLOCKED:
            return {
                "status": "BLOCKED",
                "search_control_feasibility": "SEARCH_CONTROL_NOT_FEASIBLE",
                "state": state,
                "search_url": href or url,
                "page_title": title,
                "html": html,
            }
        if state["search_state"] == STATE_SEARCH_RESULT:
            return {
                "status": "OK",
                "search_control_feasibility": "SEARCH_CONTROL_FEASIBLE",
                "state": state,
                "search_url": href or url,
                "page_title": title,
                "html": html,
            }
        if state["search_state"] in (STATE_EMPTY, STATE_RECOMMENDED):
            return {
                "status": "PARTIAL",
                "search_control_feasibility": "SEARCH_CONTROL_NOT_FEASIBLE",
                "reason": "reached_search_page_without_SEARCH_RESULT",
                "state": state,
                "search_url": href or url,
                "page_title": title,
                "html": html,
            }
        return {
            "status": "FAILED",
            "search_control_feasibility": "SEARCH_CONTROL_NOT_FEASIBLE",
            "reason": "unknown_or_unhydrated_page",
            "state": state,
            "search_url": href or url,
            "page_title": title,
            "html": html,
        }
    except Exception as exc:  # noqa: BLE001
        error_log.append(f"search_control_error:{exc}")
        return {
            "status": "FAILED",
            "search_control_feasibility": "SEARCH_CONTROL_NOT_FEASIBLE",
            "error": str(exc),
            "html": "",
            "page_title": "",
            "search_url": url,
        }


async def _optional_detail_enrich(
    client: xic._CdpClient, records: list[dict], error_log: list[str]
) -> None:
    await ts062._enrich_want_from_detail(client, records, error_log)


async def run_search_session_async(
    *,
    query: str = "Excel模板",
    max_records: int = 20,
    minimum_want_count: int | None = None,
    attach_port: int | None = None,
    also_prove_collector_on_fixture: bool = True,
) -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    error_log: list[str] = []
    session = new_session(query=query)
    chrome = xic._find_chrome()
    if not chrome and attach_port is None:
        out = {
            "ok": False,
            "status": "FAILED",
            "error": "chrome_missing",
            "session": session.to_dict(),
            "search_control": {"status": "FAILED"},
            "collection": {"collector_status": "FAILED"},
            "current_db_write": False,
        }
        _write_artifacts(
            session=session,
            search_control=out["search_control"],
            collection=out["collection"],
            error_log=["chrome_missing"],
        )
        return out

    proc = None
    client: xic._CdpClient | None = None
    attach_meta: dict = {}
    try:
        if attach_port is not None:
            session.status = "ATTACHING"
            client, attach_meta = await attach_existing_browser_session(attach_port)
            session.notes.append("attached_existing_session")
            session.status = "ATTACHED"
            # collect whatever is on page first
            html, title, href = await xic._read_page_html(client)
            (ARTIFACT_DIR / "page_dump_attach.html").write_text(html, encoding="utf-8")
            session.search_url = href
            collection = collect_from_html(
                html,
                session=session,
                page_title=title,
                final_url=href,
                max_records=max_records,
                minimum_want_count=minimum_want_count,
            )
            search_control = {
                "status": "SKIPPED",
                "search_control_feasibility": "NOT_RUN_ATTACH_MODE",
                "attach": attach_meta,
            }
            if collection.get("ok"):
                session.status = "SEARCH_RESULT_SUCCESS"
            else:
                # try search control on attached browser
                sc = await _search_control(client, query, error_log)
                search_control = {
                    k: v for k, v in sc.items() if k != "html"
                }
                search_control["attach"] = attach_meta
                html = sc.get("html") or html
                title = sc.get("page_title") or title
                href = sc.get("search_url") or href
                session.query = query
                session.search_url = href
                (ARTIFACT_DIR / "page_dump_after_control.html").write_text(
                    html or "", encoding="utf-8"
                )
                collection = collect_from_html(
                    html or "",
                    session=session,
                    page_title=title or "",
                    final_url=href or "",
                    max_records=max_records,
                    minimum_want_count=minimum_want_count,
                )
                if collection.get("search_records") and client:
                    await _optional_detail_enrich(
                        client, collection["search_records"], error_log
                    )
                    collection["want_count_audit"] = ts062.want_count_audit(
                        collection["search_records"]
                    )
        else:
            port = xic._free_port()
            profile = PROFILE_ROOT / f"run_{int(time.time())}"
            profile.mkdir(parents=True, exist_ok=True)
            session.browser = chrome or "chrome"
            cmd = [
                chrome,
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile}",
                "--no-first-run",
                "--no-default-browser-check",
                "--new-window",
                "about:blank",
            ]
            proc = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            session.notes.append(f"launched_pid={proc.pid}")
            await asyncio.sleep(2.0)
            page_ws = await xic._attach_page(port, "about:")
            client = xic._CdpClient(page_ws)
            await client.connect()
            await client.call("Page.enable")
            await client.call("Runtime.enable")
            try:
                ver = await client.call("Browser.getVersion")
                session.browser_version = (ver or {}).get("product")
            except Exception:  # noqa: BLE001
                pass
            session.status = "SEARCH_CONTROL"
            sc = await _search_control(client, query, error_log)
            search_control = {k: v for k, v in sc.items() if k != "html"}
            html = sc.get("html") or ""
            title = sc.get("page_title") or ""
            href = sc.get("search_url") or ""
            session.search_url = href
            session.query = query
            (ARTIFACT_DIR / f"page_dump_{query}.html").write_text(html, encoding="utf-8")
            collection = collect_from_html(
                html,
                session=session,
                page_title=title,
                final_url=href,
                max_records=max_records,
                minimum_want_count=minimum_want_count,
            )
            if collection.get("search_records"):
                await _optional_detail_enrich(
                    client, collection["search_records"], error_log
                )
                collection["want_count_audit"] = ts062.want_count_audit(
                    collection["search_records"]
                )
                collection["field_availability"] = ts062.field_availability_search(
                    collection["search_records"]
                )
                session.status = "SEARCH_RESULT_SUCCESS"
            else:
                session.status = search_control.get("status") or "NO_SEARCH_RESULT"

        # Fixture proof: collector can read SEARCH_RESULT HTML when present
        fixture_proof = None
        if also_prove_collector_on_fixture:
            fixture = """
            <html><body>
            <div class="feeds-list-container--Uk">
            <a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=900001">
              <div class="row1-wrap-title--q" title="夹具搜索商品A"><span class="main-title--s">夹具搜索商品A</span></div>
              <span class="number--N">12</span><span class="decimal--d">.50</span>
              <div title="61人想要">61人想要</div>
            </a>
            <a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=900002">
              <div class="row1-wrap-title--q" title="夹具搜索商品B"><span class="main-title--s">夹具搜索商品B</span></div>
              <span class="number--N">3</span><span class="decimal--d">.00</span>
            </a>
            </div></body></html>
            """
            fx_session = new_session(query="__fixture_search_result__")
            fx_session.notes.append("html_fixture_only_not_live_page")
            fixture_proof = collect_from_html(
                fixture,
                session=fx_session,
                page_title="fixture",
                final_url="https://www.goofish.com/search?q=fixture",
                max_records=20,
                minimum_want_count=50,
            )
            (ARTIFACT_DIR / "fixture_collector_proof.json").write_text(
                json.dumps(
                    {
                        "purpose": "Prove Page Collector when SEARCH_RESULT DOM is present",
                        "not_live_xianyu": True,
                        "collector_status": fixture_proof.get("collector_status"),
                        "search_state": fixture_proof.get("search_state"),
                        "records": fixture_proof.get("search_records"),
                        "minimum_want_filter": fixture_proof.get("minimum_want_filter"),
                        "want_count_audit": fixture_proof.get("want_count_audit"),
                    },
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                ),
                encoding="utf-8",
            )

        report = {
            "ok": bool(collection.get("ok")),
            "status": session.status,
            "session": session.to_dict(),
            "search_control": search_control,
            "collection": {
                k: v
                for k, v in collection.items()
                if k
                not in (
                    "minimum_want_included",
                    "minimum_want_unknown_null",
                    "recommended_records",
                )
            },
            "recommended_excluded_count": len(collection.get("recommended_records") or []),
            "fixture_collector_proof_status": (fixture_proof or {}).get("collector_status"),
            "search_control_feasibility": search_control.get("search_control_feasibility"),
            "collector_feasibility_live": collection.get("collector_status"),
            "collector_feasibility_when_search_dom_present": (fixture_proof or {}).get(
                "collector_status"
            ),
            "first_real_xianyu_search_candidate": collection.get(
                "first_real_xianyu_search_candidate"
            ),
            "current_db_write": False,
            "product_created": False,
            "listing_created": False,
            "opportunity_run": False,
            "learning_run": False,
            "error_log": error_log,
            "finished_at": ts062._now(),
        }
        _write_artifacts(
            session=session,
            search_control=search_control,
            collection=collection,
            error_log=error_log,
        )
        (ARTIFACT_DIR / "run_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        return report
    finally:
        if client:
            try:
                await client.close()
            except Exception:  # noqa: BLE001
                pass
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:  # noqa: BLE001
                try:
                    proc.kill()
                except Exception:  # noqa: BLE001
                    pass


def run_search_session(**kwargs: Any) -> dict:
    return asyncio.run(run_search_session_async(**kwargs))


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "Excel模板"
    out = run_search_session(query=q, minimum_want_count=50)
    print(
        json.dumps(
            {
                k: out.get(k)
                for k in (
                    "status",
                    "search_control_feasibility",
                    "collector_feasibility_live",
                    "collector_feasibility_when_search_dom_present",
                    "first_real_xianyu_search_candidate",
                    "recommended_excluded_count",
                )
            },
            ensure_ascii=False,
            indent=2,
        )
    )
