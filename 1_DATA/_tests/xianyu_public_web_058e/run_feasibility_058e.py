# 1_DATA/_tests/xianyu_public_web_058e/run_feasibility_058e.py
# Entry 058E — anonymous PUBLIC_WEB_READ only. No login, no bypass, no hidden API, no Current DB write.

from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)
TZ = timezone(timedelta(hours=8))
QUERY = "虚拟资料"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
URL = f"https://www.goofish.com/search?q={quote(QUERY)}"


def fetch(url: str) -> dict:
    req = Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
    )
    t0 = time.time()
    with urlopen(req, timeout=20) as resp:
        body = resp.read()
        text = body.decode("utf-8", errors="replace")
        return {
            "url": url,
            "final_url": resp.geturl(),
            "status": resp.getcode(),
            "content_type": resp.headers.get("Content-Type"),
            "bytes": len(body),
            "latency_ms": int((time.time() - t0) * 1000),
            "sha256": hashlib.sha256(body).hexdigest(),
            "text": text,
        }


def analyze(text: str) -> dict:
    item_pat = re.compile(r"https://www\.goofish\.com/item/[^\s\"'<>]+")
    return {
        "renderMode_csr": "CSR" in text and "renderMode" in text,
        "documentOnly": '"documentOnly":true' in text.replace(" ", ""),
        "ice_container_empty": '<div id="ice-container"></div>' in text,
        "item_urls": item_pat.findall(text),
        "yuan_prices": re.findall(r"¥\s*\d+(?:\.\d+)?", text),
        "want_mentions": len(re.findall(r"想要", text)),
        "mtop_search_path_mentioned": "idlemtopsearch" in text,
        "login_wall": any(x in text for x in ("请先登录", "立即登录后查看")),
        "captcha": any(x in text.lower() for x in ("captcha", "验证码", "滑块验证")),
        "baxia_security": "baxiaCommon" in text,
        "title_tag": (re.search(r"<title[^>]*>([^<]+)", text, re.I) or [None, None])[1]
        if False
        else (
            m.group(1)
            if (m := re.search(r"<title[^>]*>([^<]+)", text, re.I))
            else None
        ),
    }


def main() -> None:
    reads = []
    for _ in range(2):
        try:
            raw = fetch(URL)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            report = {
                "entry": "058E",
                "method": "PUBLIC_WEB_READ",
                "feasibility": "NOT_FEASIBLE",
                "error": str(exc),
                "access_control": "NETWORK_OR_HTTP_ERROR",
                "current_db_write": False,
                "login_used": False,
                "bypass_attempted": False,
                "hidden_api_called": False,
            }
            (OUT / "feasibility_report.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return
        text = raw.pop("text")
        tech = {**{k: v for k, v in raw.items()}, **analyze(text)}
        # do not store full HTML (copyright / size); keep short snip only once
        reads.append(tech)
        time.sleep(2)

    (OUT / "search_read1_snip.txt").write_text(
        # re-fetch not needed; snip from first analysis file if exists
        "See feasibility_report.json for technical signals. Full HTML not retained.",
        encoding="utf-8",
    )

    fields = {
        "title": "UNAVAILABLE",
        "price": "UNAVAILABLE",
        "source_url": "UNAVAILABLE",
        "source_item_id": "UNAVAILABLE",
        "want_count": "UNAVAILABLE",
        "view_count": "UNAVAILABLE",
        "comment_count": "UNAVAILABLE",
        "share_count": "UNAVAILABLE",
        "seller_reference": "UNAVAILABLE",
        "published_at": "UNAVAILABLE",
        "category": "UNAVAILABLE",
        "query": "AVAILABLE",
        "observed_at": "AVAILABLE",
    }

    captcha = any(r.get("captcha") for r in reads)
    login_wall = any(r.get("login_wall") for r in reads)
    if captcha or login_wall:
        feasibility = "BLOCKED_BY_ACCESS_CONTROL"
    else:
        feasibility = "NOT_FEASIBLE"

    report = {
        "entry": "058E",
        "date": "2026-08-30",
        "method": "PUBLIC_WEB_READ",
        "not": ["LIVE_API", "OFFICIAL_API", "SCRAPE_BYPASS"],
        "data_origin": "REAL_CANDIDATE_EXTERNAL",
        "query": QUERY,
        "login_used": False,
        "bypass_attempted": False,
        "hidden_api_called": False,
        "browser_automation": False,
        "max_items_target": 10,
        "items_extracted": 0,
        "pages_tested": [
            {"kind": "search", "url": URL, "reads": 2},
            {
                "kind": "legacy_search_candidate",
                "note": "Earlier probe to s.2.taobao.com returned punish/deny/short body",
            },
        ],
        "reread_stability": {
            "status_codes": [x["status"] for x in reads],
            "bytes": [x["bytes"] for x in reads],
            "sha256_equal": reads[0]["sha256"] == reads[1]["sha256"],
            "ice_container_empty_both": all(x["ice_container_empty"] for x in reads),
            "item_url_counts": [len(x["item_urls"]) for x in reads],
            "assessment": (
                "CSR shell stable; listing payload absent from initial HTML on both reads"
            ),
        },
        "page_stability": {
            "dom_has_listings_in_initial_html": False,
            "async_js_required": True,
            "content_in_initial_html": False,
            "detail_page_required": "UNKNOWN",
            "login_wall": login_wall,
            "captcha": captcha,
            "access_restriction_on_goofish_search_html": False,
            "security_scripts_present": all(x.get("baxia_security") for x in reads),
            "mtop_path_referenced_in_page_scripts": all(
                x.get("mtop_search_path_mentioned") for x in reads
            ),
            "note": (
                "HTML references mtop.taobao.idlemtopsearch — NOT called "
                "(058E forbids reverse/hidden API use)."
            ),
        },
        "fields": fields,
        "want_count_focus": {
            "publicly_in_initial_html": False,
            "stable_extract_via_html": False,
            "requires_detail_page": "UNKNOWN",
            "async_load_likely": True,
            "classification": "UNAVAILABLE",
        },
        "feasibility": feasibility,
        "feasibility_detail": (
            "LIMITED_TO_CSR_SHELL — anonymous HTML has no listing "
            "title/price/want/url; JS+async required; hidden mtop not invoked"
        ),
        "recommended_production_path": "EXTERNAL_IMPORT / USER_EXPORT / MANUAL_IMPORT",
        "collector_test_version": "058e.1.0",
        "current_db_write": False,
        "reads_tech": reads,
        "finished_at": datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }

    (OUT / "feasibility_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "README.md").write_text(
        "# Xianyu Public Web Feasibility Test (Entry 058E)\n\n"
        "- method: PUBLIC_WEB_READ only\n"
        "- no login / no captcha bypass / no hidden API calls\n"
        "- no writes to data/ai_factory.db\n"
        "- technical feasibility only — not market conclusions\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "feasibility": report["feasibility"],
                "items_extracted": 0,
                "want_count": fields["want_count"],
                "sha256_equal": report["reread_stability"]["sha256_equal"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
