# Entry 061 — Interactive Browser Collector tests (no live network required)

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
from connectors import xianyu_browser_connector as xbc  # noqa: E402
from connectors import xianyu_interactive_connector as xic  # noqa: E402


SAMPLE_CARD_HTML = """
<html><body>
<div class="empty-text-notfound--x">小闲鱼没有找到你想要的宝贝~</div>
<p class="empty-feed-title--q">猜你喜欢</p>
<a class="feeds-item-wrap--rGdH_KoF" href="https://www.goofish.com/item?id=111222333&amp;categoryId=1">
  <div class="row1-wrap-title--qIlOySTh" title="测试商品标题A">
    <span class="main-title--sMrtWSJa">测试商品标题A</span>
  </div>
  <div class="price-wrap--YzmU5cUl">
    <span class="number--NKh1vXWM">9</span><span class="decimal--lSAcITCN">.90</span>
  </div>
  <div class="text--MaM9Cmdn" title="7人想要">7人想要</div>
</a>
<a class="feeds-item-wrap--rGdH_KoF" href="https://www.goofish.com/item?id=444555666&amp;categoryId=1">
  <div class="row1-wrap-title--qIlOySTh" title="测试商品标题B">
    <span class="main-title--sMrtWSJa">测试商品标题B</span>
  </div>
  <div class="price-wrap--YzmU5cUl">
    <span class="number--NKh1vXWM">3</span><span class="decimal--lSAcITCN">.00</span>
  </div>
</a>
</body></html>
"""


class Entry061InteractiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_061.db"
        self.art = base / "art_061"
        self.art.mkdir()
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(xic, "ARTIFACT_DIR", self.art),
        ]
        for p in self._patches:
            p.start()
        msc.ensure_market_source_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def test_01_item_id_from_query_param(self) -> None:
        self.assertEqual(
            xbc._extract_item_id("https://www.goofish.com/item?id=784911677987&categoryId=1"),
            "784911677987",
        )

    def test_02_feed_card_extraction(self) -> None:
        cards = xbc.XianyuBrowserCollector()._extract_cards_from_html(SAMPLE_CARD_HTML, 20)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["title"], "测试商品标题A")
        self.assertEqual(cards[0]["price"], 9.9)
        self.assertEqual(cards[0]["want_count"], 7)
        self.assertEqual(cards[0]["source_item_id"], "111222333")
        self.assertIsNone(cards[1]["want_count"])

    def test_03_records_mark_guess_you_like(self) -> None:
        recs = xic._extract_records(SAMPLE_CARD_HTML, 20)
        self.assertEqual(len(recs), 2)
        self.assertTrue(recs[0]["search_primary_empty"])
        self.assertEqual(recs[0]["page_section"], "guess_you_like_after_empty_search")
        self.assertIsNone(recs[0]["sales_platform"])

    def test_04_field_availability(self) -> None:
        recs = xic._extract_records(SAMPLE_CARD_HTML, 20)
        avail = xic.field_availability(recs)
        self.assertEqual(avail["statuses"]["title"], "AVAILABLE")
        self.assertEqual(avail["statuses"]["price"], "AVAILABLE")
        self.assertEqual(avail["statuses"]["want_count"], "PARTIAL")
        self.assertEqual(avail["statuses"]["view_count"], "UNAVAILABLE")

    def test_05_access_control_stop(self) -> None:
        code = xbc._detect_access_control("非法访问 请使用正常浏览器访问闲鱼~")
        self.assertEqual(code, "ACCESS_DENIED")

    def test_06_no_fake_want(self) -> None:
        self.assertIsNone(xbc._parse_want("热门商品 999 浏览"))
        self.assertEqual(xbc._parse_want("12人想要"), 12)

    def test_07_stability_compare(self) -> None:
        a = [{"title": "t", "price": 1.0, "want_count": 2, "source_url": "u"}]
        b = [{"title": "t", "price": 1.0, "want_count": 2, "source_url": "u"}]
        st = xic._compare_stability(a, b)
        self.assertTrue(st["stable"])

    def test_08_write_artifacts_no_db(self) -> None:
        before = msc.count_observations()
        recs = xic._extract_records(SAMPLE_CARD_HTML, 20)
        avail = xic.field_availability(recs)
        report = {
            "ok": True,
            "status": "OK",
            "current_db_write": False,
            "login_used": False,
            "bypass_attempted": False,
            "hidden_api_called": False,
        }
        xic._write_artifacts(report, recs, avail, [])
        self.assertTrue((self.art / "extracted_records.json").exists())
        self.assertTrue((self.art / "extracted_records.csv").exists())
        self.assertEqual(msc.count_observations(), before)

    def test_09_registry_proposal_limited_without_full_want(self) -> None:
        result = {
            "ok": True,
            "status": "OK",
            "field_availability": {
                "statuses": {
                    "title": "AVAILABLE",
                    "price": "AVAILABLE",
                    "want_count": "PARTIAL",
                    "source_url": "AVAILABLE",
                }
            },
            "stability": {"stable": True},
        }
        prop = xic.propose_collector_registry_update(result)
        self.assertEqual(prop["status"], "LIMITED")

    def test_10_source_neq_sales(self) -> None:
        recs = xic._extract_records(SAMPLE_CARD_HTML, 1)
        self.assertEqual(recs[0]["source_platform"], "xianyu")
        self.assertIsNone(recs[0]["sales_platform"])
        self.assertTrue(recs[0]["not_our_product"])


if __name__ == "__main__":
    unittest.main()
