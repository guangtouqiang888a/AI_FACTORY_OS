# Entry 063 — Search Session + Collector tests

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import market_source_core as msc  # noqa: E402
from connectors import xianyu_search_session_063 as ss  # noqa: E402

HTML_EMPTY = """
<html><body>
<div class="empty-text-notfound--x">小闲鱼没有找到你想要的宝贝~</div>
<div class="empty-feed-container--Xp">
<p class="empty-feed-title--q">猜你喜欢</p>
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=1">
  <div class="row1-wrap-title--q" title="推荐A"><span class="main-title--s">推荐A</span></div>
  <span class="number--N">1</span><span class="decimal--d">.00</span>
  <div title="2人想要">2人想要</div>
</a>
</div></body></html>
"""

HTML_SEARCH = """
<html><body>
<div class="feeds-list-container--Uk">
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=10">
  <div class="row1-wrap-title--q" title="搜索A"><span class="main-title--s">搜索A</span></div>
  <span class="number--N">9</span><span class="decimal--d">.90</span>
  <div title="0人想要">0人想要</div>
</a>
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=11">
  <div class="row1-wrap-title--q" title="搜索B"><span class="main-title--s">搜索B</span></div>
  <span class="number--N">61</span><span class="decimal--d">.00</span>
  <div title="61人想要">61人想要</div>
</a>
<a class="feeds-item-wrap--r" href="https://www.goofish.com/item?id=12">
  <div class="row1-wrap-title--q" title="搜索C"><span class="main-title--s">搜索C</span></div>
  <span class="number--N">5</span><span class="decimal--d">.00</span>
</a>
</div></body></html>
"""


class Entry063Tests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.art = base / "art"
        self.art.mkdir()
        self._patches = [
            mock.patch.object(config, "DB_PATH", base / "t063.db"),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(ss, "ARTIFACT_DIR", self.art),
        ]
        for p in self._patches:
            p.start()
        msc.ensure_market_source_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def test_01_session_created(self) -> None:
        s = ss.new_session(query="Excel模板")
        self.assertTrue(s.session_id.startswith("ss_"))
        self.assertEqual(s.query, "Excel模板")
        self.assertNotIn("cookie", s.to_dict())

    def test_02_empty_vs_search_state(self) -> None:
        e = ss.classify_search_state(HTML_EMPTY, final_url="https://www.goofish.com/search?q=x")
        self.assertEqual(e["search_state"], ss.STATE_EMPTY)
        s = ss.classify_search_state(HTML_SEARCH, final_url="https://www.goofish.com/search?q=x")
        self.assertEqual(s["search_state"], ss.STATE_SEARCH_RESULT)
        self.assertGreater(s["search_result_count"], 0)

    def test_03_url_alone_not_enough(self) -> None:
        e = ss.classify_search_state(HTML_EMPTY, final_url="https://www.goofish.com/search?q=Excel")
        self.assertEqual(e["search_state"], ss.STATE_EMPTY)
        self.assertTrue(e["evidence"]["url_is_search"])

    def test_04_collect_search_fields(self) -> None:
        sess = ss.new_session(query="q")
        col = ss.collect_from_html(HTML_SEARCH, session=sess, final_url="u")
        self.assertTrue(col["ok"])
        self.assertEqual(col["collector_status"], "COLLECTOR_FEASIBLE_WITH_MISSING_FIELDS")
        recs = col["search_records"]
        self.assertEqual(recs[0]["result_position"], 1)
        self.assertEqual(recs[0]["want_count"], 0)
        self.assertIsNone(recs[2]["want_count"])

    def test_05_recommended_excluded_from_search(self) -> None:
        sess = ss.new_session(query="q")
        col = ss.collect_from_html(HTML_EMPTY, session=sess, final_url="u")
        self.assertFalse(col["ok"])
        self.assertEqual(len(col["search_records"]), 0)
        self.assertGreater(len(col["recommended_records"]), 0)

    def test_06_null_not_zero_filter(self) -> None:
        sess = ss.new_session(query="q")
        col = ss.collect_from_html(
            HTML_SEARCH, session=sess, final_url="u", minimum_want_count=50
        )
        f = col["minimum_want_filter"]["counts"]
        self.assertEqual(f["included"], 1)  # 61
        self.assertEqual(f["excluded_below_min"], 1)  # 0
        self.assertEqual(f["unknown_null_want"], 1)  # missing
        # 0 is excluded as below min, not as null
        self.assertEqual(len(col["minimum_want_unknown_null"]), 1)

    def test_07_access_blocked_state(self) -> None:
        html = "<html><body>非法访问 请使用正常浏览器访问闲鱼~</body></html>"
        st = ss.classify_search_state(html, page_title="x")
        self.assertEqual(st["search_state"], ss.STATE_BLOCKED)

    def test_08_no_db_write_on_artifacts(self) -> None:
        before = msc.count_observations()
        sess = ss.new_session(query="q")
        col = ss.collect_from_html(HTML_SEARCH, session=sess, final_url="u")
        ss._write_artifacts(
            session=sess,
            search_control={"status": "OK"},
            collection=col,
            error_log=[],
        )
        self.assertTrue((self.art / "session_metadata.json").exists())
        self.assertEqual(msc.count_observations(), before)

    def test_09_sales_platform_null(self) -> None:
        sess = ss.new_session(query="q")
        col = ss.collect_from_html(HTML_SEARCH, session=sess, final_url="u")
        self.assertIsNone(col["search_records"][0]["sales_platform"])


if __name__ == "__main__":
    unittest.main()
