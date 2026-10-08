# Entry 068 — First REAL Observation + Filter Wiring

from __future__ import annotations

import json
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent
ARTIFACT = DATA / "_tests" / "xianyu_entry_068"

import sys

sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
from connectors import xianyu_entry_068_pipeline as pipe068  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402


def _search_batch(**overrides) -> dict:
    base = {
        "contract_version": "064.1.0",
        "message_type": "MARKET_RECORD_BATCH",
        "run_id": "run_068_filter_test",
        "session_id": "sess_068_test",
        "source": "xianyu",
        "platform": "xianyu",
        "query": "手机壳",
        "result_origin": "SEARCH_RESULT",
        "page_state": "SEARCH_RESULT",
        "status": "SUCCESS",
        "records": [
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "880068001",
                "source_url": "https://www.goofish.com/item?id=880068001",
                "title": "MATCH商品",
                "price": 9.9,
                "currency": "CNY",
                "want_count": 61,
                "want_count_status": "VISIBLE_ON_CARD",
                "result_origin": "SEARCH_RESULT",
                "observed_at": "2026-09-03T12:00:00+08:00",
                "query": "手机壳",
                "session_id": "sess_068_test",
                "collector_version": "065.1.0",
            },
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "880068002",
                "source_url": "https://www.goofish.com/item?id=880068002",
                "title": "BELOW商品",
                "price": 5.0,
                "currency": "CNY",
                "want_count": 10,
                "want_count_status": "VISIBLE_ON_CARD",
                "result_origin": "SEARCH_RESULT",
                "observed_at": "2026-09-03T12:00:01+08:00",
                "query": "手机壳",
                "session_id": "sess_068_test",
                "collector_version": "065.1.0",
            },
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "880068003",
                "source_url": "https://www.goofish.com/item?id=880068003",
                "title": "NULL want商品",
                "price": 8.0,
                "currency": "CNY",
                "want_count": None,
                "want_count_status": "MISSING_ON_CARD",
                "result_origin": "SEARCH_RESULT",
                "observed_at": "2026-09-03T12:00:02+08:00",
                "query": "手机壳",
                "session_id": "sess_068_test",
                "collector_version": "065.1.0",
            },
        ],
    }
    base.update(overrides)
    return base


class Entry068FilterWiringTests(unittest.TestCase):
    def setUp(self) -> None:
        ARTIFACT.mkdir(parents=True, exist_ok=True)

    def test_01_filter_match_below_unknown(self) -> None:
        candidates = [
            {"title": "A", "want_count": 61, "price": 9.9, "result_origin": "SEARCH_RESULT"},
            {"title": "B", "want_count": 10, "price": 5.0, "result_origin": "SEARCH_RESULT"},
            {"title": "C", "want_count": None, "price": 8.0, "result_origin": "SEARCH_RESULT"},
        ]
        fr = pipe068.apply_filter_to_observation_candidates(
            candidates, filters={"min_want_count": 50}
        )
        self.assertEqual(fr["MATCH"], 1)
        self.assertEqual(fr["BELOW_THRESHOLD"], 1)
        self.assertEqual(fr["UNKNOWN"], 1)
        self.assertFalse(fr["filter_deleted_observations"])
        self.assertEqual(fr["observations_retained"], 3)

    def test_02_null_not_zero(self) -> None:
        fr = pipe068.apply_filter_to_observation_candidates(
            [{"title": "x", "want_count": None}], filters={"min_want_count": 50}
        )
        self.assertIsNone(fr["originals"][0]["want_count"])
        self.assertEqual(fr["UNKNOWN"], 1)

    def test_03_observation_retained_after_filter(self) -> None:
        originals = [
            {"title": "a", "want_count": 1},
            {"title": "b", "want_count": None},
        ]
        fr = pipe068.apply_filter_to_observation_candidates(
            originals, filters={"min_want_count": 50}
        )
        self.assertEqual(len(fr["originals"]), 2)
        self.assertEqual(len(fr["classified"]), 2)

    def test_04_pipeline_filter_wired_no_db_without_verify(self) -> None:
        before = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        out = pipe068.run_pipeline(_search_batch(), human_verified=False)
        after = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        self.assertEqual(before, after)
        self.assertEqual(out["filter"]["MATCH"], 1)
        self.assertEqual(out["filter"]["BELOW_THRESHOLD"], 1)
        self.assertEqual(out["filter"]["UNKNOWN"], 1)
        self.assertFalse(out["first_real_xianyu_market_observation"])

    def test_05_recommended_not_imported_as_real(self) -> None:
        before = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        batch = _search_batch(run_id="run_068_rec")
        batch["records"] = [
            {
                **batch["records"][0],
                "source_item_id": "880068999",
                "source_url": "https://www.goofish.com/item?id=880068999",
                "result_origin": "RECOMMENDED_RESULT",
                "title": "推荐冒充",
            }
        ]
        batch["result_origin"] = "RECOMMENDED_RESULT"
        batch["page_state"] = "RECOMMENDED_FEED"
        out = pipe068.run_pipeline(batch, human_verified=True)
        after = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        self.assertEqual(before, after)
        self.assertEqual(out["block_reason"], "RECOMMENDED_ONLY_NOT_SEARCH_EVIDENCE")
        self.assertFalse(out["first_real_xianyu_market_observation"])

    def test_06_db_write_search_only_with_verify_then_cleanup(self) -> None:
        before = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        before_prod = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
        out = pipe068.run_pipeline(
            _search_batch(run_id="run_068_db"), human_verified=True
        )
        after = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        after_prod = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
        self.assertTrue(out["first_real_xianyu_market_observation"])
        self.assertGreater(after, before)
        self.assertEqual(before_prod, after_prod)
        run_id = (out.get("pipeline") or {}).get("import", {}).get("collection_run_id")
        if run_id:
            import market_source_core as msc

            msc.delete_observations_for_run(run_id)
        cleaned = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        self.assertEqual(cleaned, before)

    def test_07_source_sales_separation(self) -> None:
        out = pipe068.run_pipeline(_search_batch(run_id="run_068_sep"), human_verified=False)
        preview = json.loads(
            (ARTIFACT / "normalized_preview.json").read_text(encoding="utf-8")
        )
        for c in preview:
            self.assertIsNone(c.get("sales_platform"))

    def test_08_no_parallel_filter_module(self) -> None:
        for name in (
            "xianyu_filter.py",
            "market_observation_filter_v2.py",
            "simple_filter.py",
        ):
            self.assertFalse((DATA / name).exists())
            self.assertFalse((DATA / "connectors" / name).exists())

    def test_09_reuse_apply_observation_filters(self) -> None:
        src = (DATA / "connectors" / "xianyu_entry_068_pipeline.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("apply_observation_filters", src)
        self.assertNotIn("99_ARCHIVE", src)
        self.assertNotIn("sample.xlsx", src)

    def test_10_core_file_creation_zero(self) -> None:
        for folder in (
            "00_GOVERNANCE",
            "01_CURRENT_STATE",
            "02_ARCHITECTURE",
            "03_BUSINESS",
            "05_EXECUTION",
            "06_HISTORY",
        ):
            d = ROOT / "docs" / folder
            hits = list(d.glob("*068*")) if d.exists() else []
            self.assertEqual(hits, [])

    def test_11_want_count_report(self) -> None:
        report = pipe068.want_count_status_report(
            [
                {"want_count_status": ts062.WANT_VISIBLE_ON_CARD},
                {"want_count_status": ts062.WANT_MISSING_ON_CARD},
            ]
        )
        self.assertEqual(report["counts"][ts062.WANT_VISIBLE_ON_CARD], 1)
        self.assertEqual(report["counts"][ts062.WANT_MISSING_ON_CARD], 1)


if __name__ == "__main__":
    unittest.main()
