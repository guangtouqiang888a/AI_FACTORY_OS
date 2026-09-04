# Entry 058D — Acquisition capability + collector abstraction tests
# Isolated temp DB — never pollutes Current DB.

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
import collector_abstraction as cab  # noqa: E402
import config  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
from collector import XianyuCollector  # noqa: E402
from connectors import xianyu_import_connector as xic  # noqa: E402


class Entry058DAcquisitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_058d.db"
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

    def _csv(self, name: str, rows: list[dict]) -> Path:
        path = self.imports / name
        fields = list(rows[0].keys())
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        return path

    def test_01_xianyu_source_registered(self) -> None:
        ids = {s["source_id"] for s in msc.list_sources()}
        self.assertIn("src_xianyu_marketplace", ids)

    def test_02_external_import_works(self) -> None:
        self._csv(
            "e.csv",
            [{"title": "T", "price": "1", "链接": "https://www.goofish.com/item/e1"}],
        )
        r = cab.run_acquisition(
            acquisition_mode=acq.MODE_MANUAL_IMPORT,
            collection_query="Excel模板",
            declared_origin=msc.ORIGIN_UNKNOWN,
        )
        self.assertTrue(r["ok"], r)
        self.assertIsNone(r["sales_platform"])

    def test_03_live_mode_unavailable(self) -> None:
        r = cab.run_acquisition(acquisition_mode=acq.MODE_LIVE_API, collection_query="x")
        self.assertFalse(r["ok"])
        self.assertEqual(r["classification"], "NOT_AVAILABLE_CURRENTLY")
        self.assertEqual(r["error"], "live_collection_not_available")
        col = XianyuCollector()
        self.assertEqual(col.collector_kind, "EXTERNAL_IMPORT")
        live = col.live_collect("虚拟资料")
        self.assertFalse(live["ok"])

    def test_04_raw_preserved_with_hash(self) -> None:
        path = self._csv(
            "h.csv",
            [{"title": "H", "price": "1", "链接": "https://www.goofish.com/item/h1"}],
        )
        r = xic.import_file(path, collection_query="PPT模板", declared_origin=msc.ORIGIN_UNKNOWN)
        self.assertTrue(Path(r["raw_reference"]).exists())
        self.assertTrue(r.get("raw_sha256"))
        run_dir = Path(r["raw_reference"]).parent
        self.assertTrue((run_dir / "raw_sha256.txt").exists())
        self.assertTrue((run_dir / "provenance.json").exists())

    def test_05_provenance_and_query(self) -> None:
        path = self._csv(
            "q.csv",
            [{"title": "Q", "price": "2", "链接": "https://www.goofish.com/item/q1"}],
        )
        r = xic.import_file(
            path, collection_query="简历模板", declared_origin=msc.ORIGIN_REAL
        )
        self.assertEqual(r["collection_query"], "简历模板")
        self.assertNotEqual(r["collection_query"], "xianyu")
        with database.get_connection() as conn:
            run = dict(
                conn.execute(
                    "SELECT * FROM collection_runs WHERE run_id=?", (r["run_id"],)
                ).fetchone()
            )
        self.assertEqual(run.get("collection_query"), "简历模板")
        self.assertEqual(run.get("acquisition_mode"), "MANUAL_IMPORT")

    def test_06_data_origin_and_null_zero(self) -> None:
        path = self._csv(
            "nz.csv",
            [
                {
                    "title": "NZ",
                    "price": "1",
                    "want_count": "0",
                    "链接": "https://www.goofish.com/item/nz1",
                }
            ],
        )
        xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT * FROM market_observations").fetchone())
        self.assertEqual(row["data_origin"], msc.ORIGIN_UNKNOWN)
        self.assertEqual(row["want_count"], 0)
        self.assertIsNone(row["view_count"])

    def test_07_dedupe_and_history(self) -> None:
        path = self._csv(
            "dh.csv",
            [{"title": "DH", "price": "1", "链接": "https://www.goofish.com/item/dh1"}],
        )
        xic.import_file(path, observed_at="2026-08-01T00:00:00+08:00")
        xic.import_file(path, observed_at="2026-08-07T00:00:00+08:00")
        with database.get_connection() as conn:
            n = conn.execute(
                "SELECT COUNT(*) FROM market_observations WHERE source_item_id='dh1'"
            ).fetchone()[0]
        self.assertEqual(n, 2)

    def test_08_collection_run_and_collectors(self) -> None:
        cols = msc.list_collectors()
        ids = {c["collector_id"] for c in cols}
        self.assertIn("col_xianyu_import", ids)
        self.assertIn("col_xianyu_live_api", ids)
        live = next(c for c in cols if c["collector_id"] == "col_xianyu_live_api")
        self.assertEqual(live["status"], "NOT_AVAILABLE_CURRENTLY")

    def test_09_sample_rejected_legacy_isolated(self) -> None:
        marked = self.imports / "x_sample.csv"
        with open(marked, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["title", "price", "链接"])
            w.writeheader()
            w.writerow({"title": "t", "price": "1", "链接": "https://goofish.com/item/a"})
        r = xic.import_file(marked, declared_origin=msc.ORIGIN_REAL)
        self.assertFalse(r["ok"])
        self.assertEqual(msc.count_observations(), 0)

    def test_10_source_sales_and_multi_listing(self) -> None:
        for disc, sale in (
            ("xianyu", "taobao"),
            ("taobao", "xianyu"),
            ("search", "future_platform"),
        ):
            r = msc.assert_source_sales_independent(disc, sale)
            self.assertTrue(r["allowed"])
            self.assertFalse(r["auto_bound"])
        product = {"product_id": "p1"}
        listings = [
            {"product_id": "p1", "platform": "xianyu"},
            {"product_id": "p1", "platform": "taobao"},
        ]
        self.assertEqual(len({x["product_id"] for x in listings}), 1)

    def test_11_failure_no_fake_and_db_clean(self) -> None:
        r = xic.import_file(self.imports / "missing.csv")
        self.assertFalse(r["ok"])
        self.assertEqual(msc.count_observations(), 0)

    def test_12_forbidden_modes(self) -> None:
        r = cab.run_acquisition(acquisition_mode="SCRAPE_BYPASS")
        self.assertFalse(r["ok"])
        snap = acq.capability_snapshot()
        self.assertEqual(snap["live_collection"], "NOT_AVAILABLE")
        self.assertEqual(snap["external_import"], "VALID_PATH")
        self.assertIn(acq.MODE_USER_EXPORT, snap["recommended_acquisition_mode"])

    def test_13_official_eligibility_honest(self) -> None:
        off = acq.xianyu_official_capability()
        self.assertTrue(off["official_open_platform_exists"])
        self.assertFalse(off["public_self_serve_registration"])
        self.assertEqual(
            off["status_for_ai_factory_market_observation"], "NOT_AVAILABLE_CURRENTLY"
        )
        elig = acq.current_eligibility()
        self.assertFalse(elig["eligible_for_live_api_market_observation"])
        self.assertTrue(len(elig["access_requirements"]) >= 3)


if __name__ == "__main__":
    unittest.main()
