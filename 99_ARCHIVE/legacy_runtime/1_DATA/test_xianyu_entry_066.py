# Entry 066 — Work Principles alignment + First Real Observation import gate

from __future__ import annotations

import json
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent
ARTIFACT = DATA / "_tests" / "xianyu_entry_066"

import sys

sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
from connectors import xianyu_extension_bridge_065 as bridge  # noqa: E402
from connectors import xianyu_market_observation_import_066 as imp066  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402


def _search_batch(**overrides) -> dict:
    base = {
        "contract_version": "064.1.0",
        "message_type": "MARKET_RECORD_BATCH",
        "run_id": "run_066_test",
        "session_id": "sess_066_test",
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
                "source_item_id": "880010001",
                "source_url": "https://www.goofish.com/item?id=880010001",
                "title": "测试搜索商品A",
                "price": 19.9,
                "currency": "CNY",
                "want_count": 55,
                "want_count_status": "VISIBLE_ON_CARD",
                "result_origin": "SEARCH_RESULT",
                "observed_at": "2026-08-30T14:00:00+08:00",
                "query": "手机壳",
                "session_id": "sess_066_test",
                "collector_version": "065.1.0",
            },
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "880010002",
                "source_url": "https://www.goofish.com/item?id=880010002",
                "title": "测试搜索商品B",
                "price": 8.0,
                "currency": "CNY",
                "want_count": None,
                "want_count_status": "MISSING_ON_CARD",
                "result_origin": "SEARCH_RESULT",
                "observed_at": "2026-08-30T14:00:01+08:00",
                "query": "手机壳",
                "session_id": "sess_066_test",
                "collector_version": "065.1.0",
            },
        ],
    }
    base.update(overrides)
    return base


class Entry066GovernanceTests(unittest.TestCase):
    WP = ROOT / "docs" / "AI_FACTORY_OS_WORK_PRINCIPLES.md"
    MAP = ROOT / "docs" / "AI_FACTORY_OS_DOCUMENTATION_MAP.md"
    BLUEPRINT = ROOT / "docs" / "02_ARCHITECTURE" / "XIANYU_BROWSER_EXTENSION_BLUEPRINT_064.md"

    def test_01_work_principles_exists(self) -> None:
        self.assertTrue(self.WP.exists())
        t = self.WP.read_text(encoding="utf-8")
        self.assertIn("Core Documentation Creation Principle", t)
        self.assertIn("Browser-Native Acquisition", t)
        self.assertIn("Collector", t)
        self.assertIn("Filter", t)

    def test_02_human_gate_not_per_product(self) -> None:
        t = self.WP.read_text(encoding="utf-8")
        self.assertIn("不应", t)
        self.assertIn("逐产品", t)
        self.assertIn("自主", t)

    def test_03_supersedes_whole_upgrade_conflict(self) -> None:
        t = self.WP.read_text(encoding="utf-8")
        self.assertIn("Scope-Controlled Entry", t)
        self.assertIn("Superseded", t)

    def test_04_browser_native_without_plugin(self) -> None:
        t = self.WP.read_text(encoding="utf-8")
        self.assertIn("没有", t)
        self.assertIn("现成插件", t)

    def test_05_acquisition_filter_separation(self) -> None:
        t = self.WP.read_text(encoding="utf-8")
        self.assertIn("NULL ≠ 0", t)
        self.assertIn("want_count", t)

    def test_06_blueprint_in_documentation_map(self) -> None:
        m = self.MAP.read_text(encoding="utf-8")
        self.assertIn("XIANYU_BROWSER_EXTENSION_BLUEPRINT_064", m)

    def test_07_no_duplicate_blueprint_v2(self) -> None:
        arch = ROOT / "docs" / "02_ARCHITECTURE"
        names = [p.name.lower() for p in arch.glob("*xianyu*extension*")]
        blueprint_like = [n for n in names if "blueprint" in n or "implementation" in n]
        self.assertLessEqual(len(blueprint_like), 1)

    def test_08_core_file_creation_report_format(self) -> None:
        t = self.WP.read_text(encoding="utf-8")
        self.assertIn("Core File Changes", t)


class Entry066ImportGateTests(unittest.TestCase):
    def setUp(self) -> None:
        ARTIFACT.mkdir(parents=True, exist_ok=True)

    def test_09_verification_report_search_vs_recommended(self) -> None:
        batch = _search_batch()
        batch["records"].append(
            {
                **batch["records"][0],
                "source_item_id": "880019999",
                "source_url": "https://www.goofish.com/item?id=880019999",
                "title": "推荐商品",
                "result_origin": "RECOMMENDED_RESULT",
            }
        )
        sink = bridge.ingest_market_record_batch(batch, test_mode=True)
        normalized = json.loads(
            (bridge.ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8")
        )
        report = imp066.build_verification_report(batch, normalized)
        self.assertEqual(report["search_result_count"], 2)
        self.assertEqual(report["recommended_count"], 1)

    def test_10_null_want_retained(self) -> None:
        batch = _search_batch()
        sink = bridge.ingest_market_record_batch(batch, test_mode=True)
        normalized = json.loads(
            (bridge.ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8")
        )
        missing = [c for c in normalized if c.get("want_count") is None]
        self.assertEqual(len(missing), 1)

    def test_11_pending_without_human_verified(self) -> None:
        batch = _search_batch(run_id="run_pending")
        result = imp066.process_extension_batch_for_entry(batch, human_verified=False)
        self.assertEqual(result["import"]["status"], "PENDING_HUMAN_VERIFICATION")
        self.assertFalse(result["import"]["first_real_market_observation"])

    def test_12_db_import_with_human_verified(self) -> None:
        before = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        batch = _search_batch(run_id="run_066_db_test")
        result = imp066.process_extension_batch_for_entry(batch, human_verified=True)
        after = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        self.assertTrue(result["import"]["first_real_market_observation"])
        self.assertGreater(after, before)
        run_id = result["import"]["collection_run_id"]
        imp066.msc.delete_observations_for_run(run_id)
        after_cleanup = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        self.assertEqual(after_cleanup, before)

    def test_13_no_product_creation(self) -> None:
        before = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
        batch = _search_batch(run_id="run_066_prod_check")
        imp066.process_extension_batch_for_entry(batch, human_verified=True)
        after = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]
        self.assertEqual(before, after)
        run_id = json.loads(
            (ARTIFACT / "import_result.json").read_text(encoding="utf-8")
        ).get("collection_run_id")
        if run_id:
            imp066.msc.delete_observations_for_run(run_id)

    def test_14_recommended_not_imported_as_search_evidence(self) -> None:
        batch = _search_batch(run_id="run_rec_only")
        batch["records"] = [
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "880020001",
                "source_url": "https://www.goofish.com/item?id=880020001",
                "title": "纯推荐",
                "price": 5.0,
                "currency": "CNY",
                "want_count": 3,
                "want_count_status": "VISIBLE_ON_CARD",
                "result_origin": "RECOMMENDED_RESULT",
                "observed_at": "2026-08-30T14:00:00+08:00",
                "query": "手机壳",
                "session_id": "sess_066_test",
                "collector_version": "065.1.0",
            }
        ]
        result = imp066.process_extension_batch_for_entry(batch, human_verified=True)
        self.assertEqual(result["import"]["inserted"], 0)

    def test_15_source_sales_separation(self) -> None:
        batch = _search_batch(run_id="run_sep")
        result = imp066.process_extension_batch_for_entry(batch, human_verified=True)
        if result["import"].get("collection_run_id"):
            imp066.msc.delete_observations_for_run(result["import"]["collection_run_id"])
        preview = json.loads(
            (ARTIFACT / "normalized_preview.json").read_text(encoding="utf-8")
        )
        for c in preview:
            self.assertIsNone(c.get("sales_platform"))

    def test_16_filter_simulation_does_not_drop(self) -> None:
        batch = _search_batch()
        sink = bridge.ingest_market_record_batch(batch, test_mode=True)
        normalized = json.loads(
            (bridge.ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8")
        )
        report = imp066.build_verification_report(batch, normalized)
        sim = report["filter_simulation_min_want_50"]
        self.assertGreater(sim["unknown_null"], 0)
        self.assertEqual(len(report["search_result_eligible"]), 2)

    def test_17_regression_065_tests_importable(self) -> None:
        import test_xianyu_extension_065  # noqa: F401

    def test_18_legacy_isolation_no_archive_read_in_import(self) -> None:
        src = (DATA / "connectors" / "xianyu_market_observation_import_066.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("99_ARCHIVE", src)
        self.assertNotIn("sample.xlsx", src)


if __name__ == "__main__":
    unittest.main()
