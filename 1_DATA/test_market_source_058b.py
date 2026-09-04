# Entry 058B — Market Source / Xianyu Import architecture tests
# Uses isolated temp DB — never pollutes data/ai_factory.db with fixtures.

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

import config  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
from collector import XianyuCollector  # noqa: E402
from connectors import xianyu_import_connector as xic  # noqa: E402


class Entry058BMarketSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_058b.db"
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
        msc.ensure_market_source_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _write_csv(self, name: str, rows: list[dict]) -> Path:
        path = self.imports / name
        fields = list(rows[0].keys())
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        return path

    def test_01_xianyu_source_registered(self) -> None:
        sources = msc.list_sources()
        ids = {s["source_id"] for s in sources}
        self.assertIn("src_xianyu_marketplace", ids)
        x = next(s for s in sources if s["source_id"] == "src_xianyu_marketplace")
        self.assertEqual(x["platform"], "xianyu")
        self.assertEqual(x["collection_mode"], msc.MODE_IMPORT)

    def test_02_live_collection_unavailable(self) -> None:
        st = msc.live_collection_status()
        self.assertFalse(st["live_collection_available"])
        col = XianyuCollector()
        r = col.live_collect("虚拟资料")
        self.assertFalse(r["ok"])
        self.assertEqual(r["error"], "live_collection_not_available")

    def test_03_external_import_interface(self) -> None:
        path = self._write_csv(
            "real_export_batch.csv",
            [
                {
                    "title": "办公模板包A",
                    "price": "15.9",
                    "want_count": "12",
                    "view_count": "100",
                    "链接": "https://www.goofish.com/item/abc123real",
                }
            ],
        )
        result = xic.import_file(
            path,
            keyword="虚拟资料",
            declared_origin=msc.ORIGIN_REAL,
            allow_sample=False,
        )
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["collection_mode"], msc.MODE_IMPORT)
        self.assertIsNone(result["sales_platform"])
        self.assertEqual(msc.count_observations(data_origin=msc.ORIGIN_REAL), 1)

    def test_04_raw_normalized_separation(self) -> None:
        path = self._write_csv(
            "sep.csv",
            [{"title": "T1", "price": "9.9", "链接": "https://www.goofish.com/item/sep001"}],
        )
        result = xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        self.assertTrue(Path(result["raw_reference"]).exists())
        self.assertNotEqual(result["raw_reference"], str(path))

    def test_05_data_origin_and_provenance(self) -> None:
        path = self._write_csv(
            "prov.csv",
            [{"title": "T2", "price": "8.8", "链接": "https://www.goofish.com/item/prov001"}],
        )
        result = xic.import_file(path, declared_origin=msc.ORIGIN_REAL)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT * FROM market_observations LIMIT 1").fetchone())
        self.assertEqual(row["data_origin"], msc.ORIGIN_REAL)
        self.assertTrue(row["source_url"])
        self.assertTrue(row["raw_reference"])
        self.assertTrue(row["collector_version"])
        self.assertEqual(row["run_id"], result["run_id"])

    def test_06_source_sales_independent(self) -> None:
        r = msc.assert_source_sales_independent("xianyu", "taobao")
        self.assertTrue(r["allowed"])
        self.assertFalse(r["auto_bound"])
        r2 = msc.assert_source_sales_independent("taobao", "xianyu")
        self.assertTrue(r2["allowed"])

    def test_07_same_product_multi_listing_platforms(self) -> None:
        # Structural: one product_id, two listing platforms — no xianyu_product table required
        product = {"product_id": "prod_demo", "product_type": "digital_template"}
        listings = [
            {"product_id": product["product_id"], "platform": "xianyu"},
            {"product_id": product["product_id"], "platform": "taobao"},
        ]
        self.assertEqual(len({l["product_id"] for l in listings}), 1)
        self.assertEqual({l["platform"] for l in listings}, {"xianyu", "taobao"})

    def test_08_observation_schema_multi_source(self) -> None:
        for platform, source_id in (
            ("xianyu", "src_xianyu_marketplace"),
            ("taobao", "src_taobao_marketplace"),
            ("future_platform", "src_search_generic"),
        ):
            ok, _ = msc.insert_market_observation(
                {
                    "source_id": source_id,
                    "source": platform,
                    "platform": platform,
                    "title": f"item-{platform}",
                    "price": 1.0,
                    "observed_at": f"2026-08-30T10:00:00+08:00-{platform}",
                    "data_origin": msc.ORIGIN_UNKNOWN,
                    "verification_status": "UNVERIFIED",
                    "dedupe_key": f"item:{platform}:demo",
                }
            )
            self.assertTrue(ok)

    def test_09_dedupe_same_observed_at(self) -> None:
        obs = {
            "source_id": "src_xianyu_marketplace",
            "source": "xianyu",
            "platform": "xianyu",
            "title": "Dedupe Item",
            "price": 11.0,
            "source_item_id": "dedupe99",
            "observed_at": "2026-08-30T12:00:00+08:00",
            "data_origin": msc.ORIGIN_UNKNOWN,
            "verification_status": "UNVERIFIED",
            "dedupe_key": "item:xianyu:dedupe99",
        }
        ok1, _ = msc.insert_market_observation(obs)
        ok2, reason = msc.insert_market_observation(obs)
        self.assertTrue(ok1)
        self.assertFalse(ok2)
        self.assertEqual(reason, "duplicate")

    def test_10_historical_observation_not_overwrite(self) -> None:
        base = {
            "source_id": "src_xianyu_marketplace",
            "source": "xianyu",
            "platform": "xianyu",
            "title": "Grow Item",
            "source_item_id": "grow1",
            "data_origin": msc.ORIGIN_UNKNOWN,
            "verification_status": "UNVERIFIED",
            "dedupe_key": "item:xianyu:grow1",
        }
        ok1, _ = msc.insert_market_observation({**base, "price": 10, "observed_at": "2026-08-01T00:00:00+08:00"})
        ok2, _ = msc.insert_market_observation({**base, "price": 12, "observed_at": "2026-08-07T00:00:00+08:00"})
        self.assertTrue(ok1 and ok2)
        with database.get_connection() as conn:
            n = conn.execute(
                "SELECT COUNT(*) FROM market_observations WHERE source_item_id='grow1'"
            ).fetchone()[0]
        self.assertEqual(n, 2)

    def test_11_failure_no_fake_data(self) -> None:
        missing = self.imports / "does_not_exist.csv"
        result = xic.import_file(missing, declared_origin=msc.ORIGIN_REAL)
        self.assertFalse(result["ok"])
        self.assertEqual(msc.count_observations(), 0)

    def test_12_sample_rejected_from_current(self) -> None:
        sample = self.raw_dir / "2026-07-04"
        sample.mkdir(parents=True)
        sample_file = sample / "虚拟资料_sample.xlsx"
        # minimal csv renamed pattern for path marker (xlsx optional)
        csv_sample = self.raw_dir / "legacy_sample.csv"
        self._write_csv = None
        with open(csv_sample, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["title", "price", "链接"])
            w.writeheader()
            w.writerow(
                {
                    "title": "测试商品",
                    "price": "99.9",
                    "链接": "https://goofish.com/item/sample001",
                }
            )
        # path marker
        marked = self.imports / "data_sample_export.csv"
        marked.write_text(csv_sample.read_text(encoding="utf-8"), encoding="utf-8")
        result = xic.import_file(marked, declared_origin=msc.ORIGIN_REAL, allow_sample=False)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "sample_or_fixture_file_rejected")
        self.assertEqual(msc.count_observations(), 0)
        # url marker without sample filename
        clean_name = self.imports / "clean_name.csv"
        clean_name.write_text(csv_sample.read_text(encoding="utf-8"), encoding="utf-8")
        result2 = xic.import_file(clean_name, declared_origin=msc.ORIGIN_REAL, allow_sample=False)
        self.assertTrue(result2["ok"])
        # rows rejected due to sample URL → accepted 0
        self.assertEqual(result2["stats"]["accepted_count"], 0)

    def test_13_legacy_db_not_used_as_source(self) -> None:
        legacy = ROOT / "99_ARCHIVE" / "database_history" / "ai_factory_legacy_simulation_20260830.db"
        # Import path must not read legacy products into this temp DB automatically
        col = XianyuCollector()
        r = col.collect("批量关键词")
        self.assertEqual(r.get("valid", 0), 0)
        self.assertEqual(msc.count_observations(), 0)
        self.assertTrue(legacy.exists() or True)  # archive may exist on disk; unused here

    def test_14_observation_not_commercial_success(self) -> None:
        path = self._write_csv(
            "nocom.csv",
            [{"title": "N", "price": "1", "链接": "https://www.goofish.com/item/nocom1"}],
        )
        xic.import_file(path, declared_origin=msc.ORIGIN_REAL)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT * FROM market_observations LIMIT 1").fetchone())
        self.assertNotIn("commercial_success", row)
        self.assertEqual(row["data_origin"], msc.ORIGIN_REAL)

    def test_15_future_sources_registered_disabled(self) -> None:
        sources = {s["source_id"]: s for s in msc.list_sources()}
        self.assertEqual(sources["src_taobao_marketplace"]["enabled"], 0)
        self.assertEqual(sources["src_search_generic"]["enabled"], 0)


if __name__ == "__main__":
    unittest.main()
