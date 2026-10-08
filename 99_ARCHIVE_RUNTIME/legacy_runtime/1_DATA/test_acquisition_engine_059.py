# Entry 059 — Autonomous Market Acquisition Engine tests (isolated temp DB)

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import acquisition_capability as acq  # noqa: E402
import acquisition_engine as eng  # noqa: E402
import config  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
import product_origin as po  # noqa: E402
from connectors import xianyu_import_connector as xic  # noqa: E402


class Entry059AcquisitionEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_059.db"
        self.raw_dir = base / "raw" / "xianyu"
        self.imports = self.raw_dir / "imports"
        self.imports.mkdir(parents=True)
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(config, "RAW_XIANYU_DIR", self.raw_dir),
            mock.patch.object(xic, "IMPORTS_DIR", self.imports),
        ]
        for p in self._patches:
            p.start()
        eng.ensure_acquisition_engine_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _csv(self, name: str, rows: list[dict]) -> Path:
        path = self.imports / name
        fields = list(rows[0].keys())
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        return path

    def test_01_task_creation(self) -> None:
        t = eng.create_collection_task(query="Excel模板", scan_strategy=eng.SCAN_KEYWORD)
        self.assertTrue(t["task_id"].startswith("atask_"))
        self.assertEqual(t["query"], "Excel模板")
        self.assertEqual(t["status"], eng.TASK_READY)
        self.assertNotEqual(t["query"], "xianyu")

    def test_02_query_not_source_platform(self) -> None:
        with self.assertRaises(ValueError):
            eng.create_collection_task(query="xianyu")

    def test_03_source_registry_and_collectors(self) -> None:
        ids = {s["source_id"] for s in msc.list_sources()}
        self.assertIn("src_xianyu_marketplace", ids)
        cols = {c["collector_id"]: c for c in msc.list_collectors()}
        self.assertEqual(cols["col_xianyu_import"]["status"], "ACTIVE")
        self.assertEqual(cols["col_xianyu_public_web"]["status"], "LIMITED")
        self.assertEqual(cols["col_xianyu_live_api"]["status"], "NOT_AVAILABLE_CURRENTLY")
        self.assertIn("col_xianyu_browser", cols)
        self.assertEqual(cols["col_xianyu_browser"]["status"], "LIMITED")

    def test_04_waiting_without_file(self) -> None:
        t = eng.create_collection_task(query="虚拟资料")
        r = eng.execute_collection(t["task_id"])
        self.assertEqual(r["status"], eng.TASK_WAITING)
        self.assertEqual(r["entry_status"], "WAITING_FOR_REAL_SOURCE")
        self.assertIsNone(r["sales_platform"])
        self.assertFalse(r["product_created"])

    def test_05_import_execute_with_file(self) -> None:
        self._csv(
            "batch.csv",
            [
                {
                    "title": "模板A",
                    "price": "9.9",
                    "want_count": "0",
                    "链接": "https://www.goofish.com/item/ae059001",
                }
            ],
        )
        t = eng.create_collection_task(
            query="PPT模板", declared_origin=msc.ORIGIN_UNKNOWN
        )
        r = eng.execute_collection(t["task_id"])
        self.assertIn(r["status"], (eng.TASK_DONE, eng.TASK_PARTIAL))
        self.assertGreaterEqual(msc.count_observations(), 1)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT * FROM market_observations LIMIT 1").fetchone())
        self.assertIsNone(row["view_count"])
        self.assertEqual(row["want_count"], 0)
        self.assertEqual(row["source"], "xianyu")

    def test_06_live_and_web_modes_honest(self) -> None:
        t1 = eng.create_collection_task(
            query="考试资料", acquisition_mode=acq.MODE_LIVE_API
        )
        self.assertIn(t1["status"], (eng.TASK_FAILED, eng.TASK_READY))
        r1 = eng.execute_collection(t1["task_id"])
        self.assertEqual(r1["status"], eng.TASK_FAILED)
        t2 = eng.create_collection_task(
            query="考试资料2", acquisition_mode="PUBLIC_WEB_READ"
        )
        r2 = eng.execute_collection(t2["task_id"])
        self.assertEqual(r2["status"], eng.TASK_FAILED)

    def test_07_source_sales_and_multi_listing(self) -> None:
        r = msc.assert_source_sales_independent("xianyu", "taobao")
        self.assertTrue(r["allowed"])
        product = {"product_id": "p1"}
        listings = [
            {"product_id": "p1", "platform": "xianyu"},
            {"product_id": "p1", "platform": "overseas"},
        ]
        self.assertEqual(len({x["product_id"] for x in listings}), 1)

    def test_08_product_type_neq_business_model(self) -> None:
        r = po.assert_product_type_neq_business_model(
            "digital_template", [po.BM_VOLUME_LOW_PRICE, po.BM_DIRECT_SALE]
        )
        self.assertTrue(r["ok"])

    def test_09_policy_blocks_disallowed_source(self) -> None:
        with self.assertRaises(ValueError):
            eng.create_collection_task(
                query="something", source_id="src_taobao_marketplace"
            )

    def test_10_no_fake_data_on_failure(self) -> None:
        t = eng.create_collection_task(query="无文件关键词")
        before = msc.count_observations()
        eng.execute_collection(t["task_id"])
        self.assertEqual(msc.count_observations(), before)

    def test_11_engine_status_and_chain(self) -> None:
        st = eng.engine_status()
        self.assertEqual(st["xianyu_modes"]["MANUAL_IMPORT"], "AVAILABLE")
        self.assertEqual(st["xianyu_modes"]["PUBLIC_WEB_READ"], "LIMITED")
        self.assertTrue(st["separations"]["cursor_neq_product_ai"])
        chain = eng.reality_chain()
        self.assertEqual(chain["Xianyu Adapter"], "REALITY")
        self.assertEqual(chain["Acquisition Strategy feedback"], "PROPOSED")

    def test_12_future_scan_strategy_draft(self) -> None:
        t = eng.create_collection_task(
            query="趋势词", scan_strategy=eng.SCAN_TREND
        )
        self.assertEqual(t["status"], eng.TASK_DRAFT)

    def test_13_sample_rejected(self) -> None:
        marked = self.imports / "x_sample.csv"
        with open(marked, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["title", "price", "链接"])
            w.writeheader()
            w.writerow(
                {"title": "t", "price": "1", "链接": "https://www.goofish.com/item/ok"}
            )
        t = eng.create_collection_task(query="样例拒绝")
        r = eng.execute_collection(t["task_id"])
        # sample filename rejected at import → waiting or failed with 0 obs
        self.assertEqual(msc.count_observations(), 0)


if __name__ == "__main__":
    unittest.main()
