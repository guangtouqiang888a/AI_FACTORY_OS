# Entry 065 — Xianyu Browser Extension + Local Bridge

from __future__ import annotations

import json
import re
import socket
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
EXT_DIR = Path(__file__).resolve().parent / "browser_extension" / "xianyu"
ARTIFACT_DIR = Path(__file__).resolve().parent / "_tests" / "xianyu_extension_065"

import sys

sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

from connectors import xianyu_extension_bridge_065 as bridge  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402

SEARCH_FIXTURE = """
<html><body data-spm="search">
<div class="search-result">
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=900001">
  <div class="row1-wrap-title--x" title="Excel模板合集"></div>
  <span class="number--N">9</span><span class="decimal--D">.90</span>
  <div class="text--M" title="61人想要">61人想要</div>
</a>
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=900002">
  <div class="row1-wrap-title--x" title="PPT模板无想要"></div>
  <span class="number--N">5</span>
</a>
</div></body></html>
"""

RECOMMENDED_FIXTURE = """
<html><body>
<div class="empty-text-notfound">没有找到你想要的宝贝</div>
<div class="empty-feed-title--x">猜你喜欢</div>
<div class="empty-feed-container--x">
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=800001">
  <div class="row1-wrap-title--x" title="推荐商品A"></div>
  <span class="number--N">12</span>
  <div title="3人想要">3人想要</div>
</a>
</div></body></html>
"""


def _sample_batch(**overrides) -> dict:
    base = {
        "contract_version": "064.1.0",
        "message_type": "MARKET_RECORD_BATCH",
        "request_id": "req_test_001",
        "run_id": "run_test_001",
        "session_id": "sess_test_001",
        "source": "xianyu",
        "platform": "xianyu",
        "query": "Excel模板",
        "result_origin": "SEARCH_RESULT",
        "page_state": "SEARCH_RESULT",
        "observed_at": "2026-08-30T12:00:00+08:00",
        "collector_version": "065.1.0",
        "adapter_version": "065.1.0",
        "status": "SUCCESS",
        "filter_metadata": {"min_want_count": None},
        "records": [
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "900001",
                "source_url": "https://www.goofish.com/item?id=900001",
                "title": "Excel模板合集",
                "price": 9.9,
                "currency": "CNY",
                "want_count": 61,
                "want_count_status": "VISIBLE_ON_CARD",
                "result_origin": "SEARCH_RESULT",
                "observed_at": "2026-08-30T12:00:01+08:00",
                "query": "Excel模板",
                "session_id": "sess_test_001",
                "collector_version": "065.1.0",
            },
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "900002",
                "source_url": "https://www.goofish.com/item?id=900002",
                "title": "PPT模板无想要",
                "price": 5.0,
                "currency": "CNY",
                "want_count": None,
                "want_count_status": "MISSING_ON_CARD",
                "result_origin": "SEARCH_RESULT",
                "observed_at": "2026-08-30T12:00:02+08:00",
                "query": "Excel模板",
                "session_id": "sess_test_001",
                "collector_version": "065.1.0",
            },
        ],
    }
    base.update(overrides)
    return base


class Entry065ExtensionTests(unittest.TestCase):
    def setUp(self) -> None:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    # --- Extension static ---

    def test_01_manifest_parse(self) -> None:
        m = json.loads((EXT_DIR / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(m["manifest_version"], 3)
        self.assertIn("activeTab", m["permissions"])
        self.assertNotIn("cookies", m.get("permissions", []))
        self.assertNotIn("webRequest", m.get("permissions", []))
        hosts = " ".join(m.get("host_permissions", []))
        self.assertIn("goofish.com", hosts)
        self.assertNotIn("2yuanbao", hosts)
        self.assertIn("127.0.0.1", hosts)

    def test_02_minimal_permissions(self) -> None:
        m = json.loads((EXT_DIR / "manifest.json").read_text(encoding="utf-8"))
        self.assertLessEqual(len(m["permissions"]), 2)

    def test_03_content_script_scope(self) -> None:
        m = json.loads((EXT_DIR / "manifest.json").read_text(encoding="utf-8"))
        matches = m["content_scripts"][0]["matches"]
        self.assertTrue(all("goofish.com" in x for x in matches))

    def test_04_content_dom_not_api(self) -> None:
        c = (EXT_DIR / "content.js").read_text(encoding="utf-8")
        self.assertIn("feeds-item-wrap", c)
        self.assertNotIn("fetch(", c)
        self.assertNotIn("mtop", c.lower())
        self.assertNotIn("cookie", c.lower())
        self.assertNotIn("XMLHttpRequest", c)

    def test_05_no_collector_want_filter(self) -> None:
        c = (EXT_DIR / "content.js").read_text(encoding="utf-8")
        self.assertNotIn("wantCount >=", c)
        self.assertNotIn("if (match)", c)
        self.assertIn("MISSING_ON_CARD", c)

    def test_06_null_not_zero(self) -> None:
        c = (EXT_DIR / "content.js").read_text(encoding="utf-8")
        compact = re.sub(r"\s+", "", c)
        self.assertIn("want_count:null", compact)
        self.assertIn("MISSING_ON_CARD", c)

    def test_07_global_dedupe_not_title_only(self) -> None:
        c = (EXT_DIR / "content.js").read_text(encoding="utf-8")
        self.assertIn("source_item_id", c)
        self.assertNotIn("seenTitles", c)

    def test_08_no_fixed_sleep_5000(self) -> None:
        c = (EXT_DIR / "content.js").read_text(encoding="utf-8")
        self.assertNotIn("sleep(5000)", c)
        self.assertIn("waitForCardStability", c)

    def test_09_popup_message_bridge(self) -> None:
        p = (EXT_DIR / "popup.js").read_text(encoding="utf-8")
        self.assertIn("start_collect", p)
        self.assertIn("stop_collect", p)
        self.assertIn("127.0.0.1", p)

    def test_10_filter_metadata_not_scrape_discard(self) -> None:
        p = (EXT_DIR / "popup.html").read_text(encoding="utf-8")
        self.assertIn("分析筛选条件", p)

    def test_11_no_credentials(self) -> None:
        for name in ("content.js", "popup.js"):
            t = (EXT_DIR / name).read_text(encoding="utf-8").lower()
            self.assertNotIn("chrome.cookies", t)
            self.assertNotIn("localstorage.getitem", t)
            self.assertNotIn("document.cookie", t)

    # --- Classification via 062 parity (HTML fixture) ---

    def test_12_search_result_classification(self) -> None:
        cards = ts062.extract_classified_cards(SEARCH_FIXTURE, max_records=10)
        self.assertEqual(len(cards), 2)
        self.assertTrue(all(c["result_origin"] == ts062.ORIGIN_SEARCH for c in cards))

    def test_13_recommended_result_classification(self) -> None:
        cards = ts062.extract_classified_cards(RECOMMENDED_FIXTURE, max_records=10)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["result_origin"], ts062.ORIGIN_RECOMMENDED)

    def test_14_want_count_extraction(self) -> None:
        cards = ts062.extract_classified_cards(SEARCH_FIXTURE, max_records=10)
        self.assertEqual(cards[0]["want_count"], 61)
        self.assertEqual(cards[0]["want_count_status"], ts062.WANT_VISIBLE_ON_CARD)

    def test_15_want_count_missing_retained(self) -> None:
        cards = ts062.extract_classified_cards(SEARCH_FIXTURE, max_records=10)
        self.assertIsNone(cards[1]["want_count"])
        self.assertEqual(cards[1]["want_count_status"], ts062.WANT_MISSING_ON_CARD)

    def test_16_item_id_from_url(self) -> None:
        cards = ts062.extract_classified_cards(SEARCH_FIXTURE, max_records=10)
        self.assertEqual(cards[0]["source_item_id"], "900001")

    # --- Bridge validation / ingest ---

    def test_17_message_schema_validate(self) -> None:
        ok, errors, _ = bridge.validate_batch(_sample_batch())
        self.assertTrue(ok, errors)
        self.assertEqual(errors, [])

    def test_18_reject_bad_contract(self) -> None:
        bad = _sample_batch(contract_version="0.0.0")
        ok, errors, _ = bridge.validate_batch(bad)
        self.assertFalse(ok)
        self.assertTrue(any("contract_version" in e for e in errors))

    def test_19_reject_business_fields(self) -> None:
        batch = _sample_batch()
        batch["records"][0]["opportunity_score"] = 99
        ok, errors, _ = bridge.validate_batch(batch)
        self.assertFalse(ok)

    def test_20_ingest_test_sink(self) -> None:
        result = bridge.ingest_market_record_batch(_sample_batch(), test_mode=True)
        self.assertTrue(result["ok"])
        self.assertEqual(result["records_normalized"], 2)
        self.assertTrue((ARTIFACT_DIR / "batch.json").exists())
        self.assertTrue((ARTIFACT_DIR / "normalized_preview.json").exists())
        self.assertTrue((ARTIFACT_DIR / "validation_report.json").exists())

    def test_21_normalize_preserves_null_want(self) -> None:
        preview = json.loads((ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8"))
        missing = [c for c in preview if c["want_count_status"] == ts062.WANT_MISSING_ON_CARD]
        self.assertEqual(len(missing), 1)
        self.assertIsNone(missing[0]["want_count"])

    def test_22_source_sales_separation(self) -> None:
        preview = json.loads((ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8"))
        for c in preview:
            self.assertIsNone(c.get("sales_platform"))

    def test_23_observation_product_separation(self) -> None:
        preview = json.loads((ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8"))
        for c in preview:
            self.assertTrue(c.get("not_our_product"))
            self.assertNotIn("product_id", c)

    def test_24_dedupe_in_batch(self) -> None:
        batch = _sample_batch()
        dup = dict(batch["records"][0])
        batch["records"].append(dup)
        result = bridge.ingest_market_record_batch(batch, test_mode=True)
        self.assertEqual(result["records_normalized"], 2)
        self.assertEqual(result["duplicates"], 1)

    def test_25_bridge_localhost_only_binding(self) -> None:
        self.assertEqual(bridge.BRIDGE_HOST, "127.0.0.1")
        self.assertNotEqual(bridge.BRIDGE_HOST, "0.0.0.0")

    def test_26_bridge_http_integration(self) -> None:
        port = _free_port()
        srv = bridge.LocalBridgeServer(port=port, test_mode=True)
        srv.start(blocking=False)
        try:
            resp = bridge.post_batch_to_bridge(_sample_batch(run_id="run_http_001"), port=port)
            self.assertTrue(resp.get("ok"))
        finally:
            srv.stop()

    def test_27_no_current_db_write(self) -> None:
        import sqlite3
        import config

        db = config.DB_PATH
        before_obs = sqlite3.connect(db).execute("SELECT COUNT(*) FROM market_observations").fetchone()[0]
        before_prod = sqlite3.connect(db).execute("SELECT COUNT(*) FROM products").fetchone()[0]
        bridge.ingest_market_record_batch(_sample_batch(run_id="run_db_check"), test_mode=True)
        after_obs = sqlite3.connect(db).execute("SELECT COUNT(*) FROM market_observations").fetchone()[0]
        after_prod = sqlite3.connect(db).execute("SELECT COUNT(*) FROM products").fetchone()[0]
        self.assertEqual(before_obs, after_obs)
        self.assertEqual(before_prod, after_prod)

    def test_28_zero_records_no_fake(self) -> None:
        batch = _sample_batch(records=[], status="NO_RESULTS", run_id="run_empty")
        result = bridge.ingest_market_record_batch(batch, test_mode=True)
        self.assertTrue(result["ok"])
        self.assertEqual(result["records_normalized"], 0)

    def test_29_regression_064_contract_file(self) -> None:
        contract = ROOT / "1_DATA" / "_tests" / "xianyu_extension_forensics_064" / "market_record_contract_064.json"
        self.assertTrue(contract.exists())
        data = json.loads(contract.read_text(encoding="utf-8"))
        self.assertEqual(data["contract_version"], "064.1.0")

    def test_30_extension_directory_packaged(self) -> None:
        for f in ("manifest.json", "content.js", "popup.html", "popup.js"):
            self.assertTrue((EXT_DIR / f).exists(), f)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((bridge.BRIDGE_HOST, 0))
        return s.getsockname()[1]


if __name__ == "__main__":
    unittest.main()
