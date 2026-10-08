# Entry 054 — Opportunity Discovery & Selection tests

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "3_DECISION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import config  # noqa: E402
import database  # noqa: E402
import market_signal_core as msc  # noqa: E402
import opportunity_discovery as od  # noqa: E402


class OpportunityDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_disc.db"
        self.disc_json = base / "autonomous_discovery_v1.json"
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(od, "DISCOVERED_JSON", self.disc_json),
        ]
        for p in self._patches:
            p.start()
        database.ensure_schema()
        msc.ensure_market_signal_schema()
        self._seed_products()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _seed_products(self) -> None:
        rows = []
        for i in range(5):
            rows.append({
                "platform_id": 1,
                "keyword": "虚拟资料",
                "title": f"PPT模板打包 {i}",
                "price": 19.9,
                "want_count": 50 + i * 10,
                "view_count": 500 + i * 20,
                "comment_count": 1,
                "share_count": 0,
                "seller": "s",
                "tags": "模板",
                "publish_time": "2026-07-01",
                "source_url": f"http://example/{i}",
                "raw_json": "{}",
                "collect_date": "2026-07-04",
            })
        # high risk group
        for i in range(3):
            rows.append({
                "platform_id": 1,
                "keyword": "赌博软件",
                "title": f"赌博工具 {i}",
                "price": 99,
                "want_count": 200,
                "view_count": 1000,
                "comment_count": 0,
                "share_count": 0,
                "seller": "s",
                "tags": "",
                "publish_time": "",
                "source_url": f"http://bad/{i}",
                "raw_json": "{}",
                "collect_date": "2026-07-04",
            })
        for r in rows:
            database.insert_product(r)

    def test_1_real_observation_generates_candidate(self) -> None:
        result = od.discover_opportunities(min_listings=3, persist=True)
        self.assertEqual(result["status"], "OK")
        self.assertFalse(result["fake_opportunities_created"])
        kws = [c["keyword"] for c in result["candidates"]]
        self.assertIn("虚拟资料", kws)

    def test_2_candidate_scored(self) -> None:
        result = od.discover_opportunities(min_listings=3, persist=False)
        cand = next(c for c in result["candidates"] if c["keyword"] == "虚拟资料")
        self.assertIn("total_score", cand["score"])
        self.assertEqual(cand["score"]["score_method"], "market_signal_proxy_v1")
        self.assertIn("Demand", cand["score"]["dimensions"])
        self.assertEqual(
            cand["score"]["dimensions"]["Historical_Performance"]["status"],
            "UNAVAILABLE",
        )

    def test_3_risk_filter(self) -> None:
        result = od.discover_opportunities(min_listings=3, persist=False)
        bad = next(c for c in result["candidates"] if c["keyword"] == "赌博软件")
        self.assertFalse(bad["risk"]["passed"])

    def test_4_eligible_ranked(self) -> None:
        result = od.discover_opportunities(min_listings=3, persist=False)
        selected = [s for s in result["selection_results"] if s["selected"]]
        self.assertTrue(any(s.get("rank") == 1 for s in selected))

    def test_5_selection_has_reason_evidence(self) -> None:
        result = od.discover_opportunities(min_listings=3, persist=False)
        selected = [s for s in result["selection_results"] if s["selected"]]
        self.assertTrue(selected)
        s0 = selected[0]
        self.assertTrue(s0["selection_reason"])
        self.assertTrue(s0["evidence_refs"])
        self.assertEqual(s0["discovery_method"], "market_signal")

    def test_6_no_evidence_no_silent_opportunity(self) -> None:
        r = od.refuse_empty_evidence_opportunity()
        self.assertFalse(r["created"])
        empty = od.discover_opportunities(min_listings=999, persist=False)
        self.assertEqual(empty["status"], "INSUFFICIENT_DATA")
        self.assertEqual(empty["candidates"], [])

    def test_7_high_risk_not_selected(self) -> None:
        result = od.discover_opportunities(min_listings=3, persist=False)
        for s in result["selection_results"]:
            if s.get("keyword") == "赌博软件":
                self.assertFalse(s["selected"])

    def test_8_future_product_type_video(self) -> None:
        p = od.future_compatibility_probe("video", "taobao", "marketplace")
        self.assertTrue(p["ok"])
        self.assertTrue(p["core_model_valid"])

    def test_9_future_product_type_novel(self) -> None:
        p = od.future_compatibility_probe("novel", "xianyu", "marketplace")
        self.assertTrue(p["ok"])

    def test_10_future_platform(self) -> None:
        p = od.future_compatibility_probe("document", "future_platform", "marketplace")
        self.assertEqual(p["platform"], "future_platform")
        self.assertTrue(p["ok"])

    def test_11_future_source(self) -> None:
        p = od.future_compatibility_probe("document", "taobao", "social")
        self.assertEqual(p["source"], "social")
        self.assertTrue(p["ok"])

    def test_12_no_future_data_leakage(self) -> None:
        # Seed a product with future collect_date relative to score — should clamp/skip
        database.insert_product({
            "platform_id": 1,
            "keyword": "未来泄漏测试词",
            "title": "future leak",
            "price": 10,
            "want_count": 10,
            "view_count": 100,
            "comment_count": 0,
            "share_count": 0,
            "seller": "s",
            "tags": "",
            "publish_time": "",
            "source_url": "http://future",
            "raw_json": "{}",
            "collect_date": "2099-01-01",
        })
        # force enough listings
        for i in range(3):
            database.insert_product({
                "platform_id": 1,
                "keyword": "未来泄漏测试词",
                "title": f"future leak {i}",
                "price": 10,
                "want_count": 10,
                "view_count": 100,
                "comment_count": 0,
                "share_count": 0,
                "seller": "s",
                "tags": "",
                "publish_time": "",
                "source_url": f"http://future/{i}",
                "raw_json": "{}",
                "collect_date": "2099-01-01",
            })
        result = od.discover_opportunities(min_listings=3, persist=False)
        # Future-dated groups skipped entirely
        kws = [c["keyword"] for c in result["candidates"]]
        self.assertNotIn("未来泄漏测试词", kws)

    def test_signals_not_overwrite_products(self) -> None:
        before = database.get_products_by_keyword("虚拟资料", limit=10)
        od.discover_opportunities(min_listings=3, persist=True)
        after = database.get_products_by_keyword("虚拟资料", limit=10)
        self.assertEqual(len(before), len(after))
        self.assertEqual(before[0]["title"], after[0]["title"])
        self.assertEqual(before[0]["want_count"], after[0]["want_count"])


if __name__ == "__main__":
    unittest.main()
