# Entry 062 — Targeted search + want_count audit tests

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import market_source_core as msc  # noqa: E402
import config  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts  # noqa: E402

HTML_EMPTY_REC = """
<html><body>
<div class="empty-text-notfound--x">小闲鱼没有找到你想要的宝贝~</div>
<div class="empty-feed-container--Xp">
<p class="empty-feed-title--q">猜你喜欢</p>
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=111">
  <div class="row1-wrap-title--q" title="推荐商品A"><span class="main-title--s">推荐商品A</span></div>
  <span class="number--N">10</span><span class="decimal--d">.00</span>
  <div title="5人想要">5人想要</div>
</a>
</div>
</body></html>
"""

HTML_SEARCH = """
<html><body>
<div class="feeds-list-container--Uk">
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=222">
  <div class="row1-wrap-title--q" title="搜索商品B"><span class="main-title--s">搜索商品B</span></div>
  <span class="number--N">8</span><span class="decimal--d">.50</span>
  <div title="0人想要">0人想要</div>
</a>
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=333">
  <div class="row1-wrap-title--q" title="搜索商品C"><span class="main-title--s">搜索商品C</span></div>
  <span class="number--N">3</span><span class="decimal--d">.00</span>
</a>
</div>
</body></html>
"""


class Entry062Tests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.art = base / "art"
        self.art.mkdir()
        self._patches = [
            mock.patch.object(config, "DB_PATH", base / "t062.db"),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(ts, "ARTIFACT_DIR", self.art),
        ]
        for p in self._patches:
            p.start()
        msc.ensure_market_source_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def test_01_empty_search_cards_are_recommended(self) -> None:
        cards = ts.extract_classified_cards(HTML_EMPTY_REC, 20)
        self.assertTrue(all(c["result_origin"] == ts.ORIGIN_RECOMMENDED for c in cards))
        self.assertEqual(ts.filter_search_results(cards), [])

    def test_02_search_results_classified(self) -> None:
        cards = ts.extract_classified_cards(HTML_SEARCH, 20)
        sr = ts.filter_search_results(cards)
        self.assertEqual(len(sr), 2)
        self.assertEqual(sr[0]["result_origin"], ts.ORIGIN_SEARCH)
        self.assertEqual(sr[0]["want_count"], 0)
        self.assertEqual(sr[0]["want_count_status"], ts.WANT_VISIBLE_ON_CARD)
        self.assertIsNone(sr[1]["want_count"])
        self.assertEqual(sr[1]["want_count_status"], ts.WANT_MISSING_ON_CARD)

    def test_03_null_not_coerced_to_zero(self) -> None:
        cards = ts.extract_classified_cards(HTML_SEARCH, 20)
        c = [x for x in cards if x["source_item_id"] == "333"][0]
        self.assertIsNone(c["want_count"])
        self.assertNotEqual(c["want_count"], 0)

    def test_04_zero_want_preserved(self) -> None:
        cards = ts.extract_classified_cards(HTML_SEARCH, 20)
        c = [x for x in cards if x["source_item_id"] == "222"][0]
        self.assertEqual(c["want_count"], 0)

    def test_05_want_audit_rates(self) -> None:
        sr = ts.filter_search_results(ts.extract_classified_cards(HTML_SEARCH, 20))
        audit = ts.want_count_audit(sr)
        self.assertEqual(audit["status_distribution"][ts.WANT_VISIBLE_ON_CARD], 1)
        self.assertEqual(audit["status_distribution"][ts.WANT_MISSING_ON_CARD], 1)
        self.assertEqual(audit["login_causation"]["conclusion"], "NOT_PROVEN")
        self.assertTrue(audit["valid_without_want_count"])

    def test_06_sales_platform_null(self) -> None:
        sr = ts.filter_search_results(ts.extract_classified_cards(HTML_SEARCH, 20))
        self.assertIsNone(sr[0]["sales_platform"])
        self.assertTrue(sr[0]["valid_without_want_count"])

    def test_07_write_artifacts_no_db(self) -> None:
        before = msc.count_observations()
        sr = ts.filter_search_results(ts.extract_classified_cards(HTML_SEARCH, 20))
        for r in sr:
            r["query"] = "t"
        avail = ts.field_availability_search(sr)
        audit = ts.want_count_audit(sr)
        ts._write_outputs({"ok": True, "status": "OK"}, sr, avail, audit, [])
        self.assertTrue((self.art / "want_count_audit.json").exists())
        self.assertEqual(msc.count_observations(), before)

    def test_08_page_state_empty(self) -> None:
        st = ts.classify_page_search_state(HTML_EMPTY_REC)
        self.assertTrue(st["search_primary_empty"])
        self.assertTrue(st["has_guess_you_like"])


if __name__ == "__main__":
    unittest.main()
