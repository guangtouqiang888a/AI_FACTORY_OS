# Entry 058C — Real Xianyu Import Pilot tests
# Isolated temp DB — never pollutes data/ai_factory.db with fixtures.
# Does not fabricate Current-DB REAL batches.

from __future__ import annotations

import csv
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
from connectors import xianyu_import_connector as xic  # noqa: E402
import xianyu_import_pilot_058c as pilot  # noqa: E402


class Entry058CImportPilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_058c.db"
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

    def test_01_real_external_import_accepted(self) -> None:
        path = self._csv(
            "batch_real.csv",
            [
                {
                    "title": "模板A",
                    "price": "12.5",
                    "want_count": "3",
                    "view_count": "50",
                    "链接": "https://www.goofish.com/item/realitem001",
                }
            ],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_REAL, mirror_to_products=False)
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["stats"]["accepted_count"], 1)
        self.assertFalse(r["product_created"])
        self.assertFalse(r["listing_created"])
        self.assertFalse(r["market_event_created"])

    def test_02_raw_preserved(self) -> None:
        path = self._csv(
            "rawkeep.csv",
            [{"title": "T", "price": "1", "链接": "https://www.goofish.com/item/rk1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        self.assertTrue(Path(r["raw_reference"]).exists())
        self.assertIn("import_batches", r["raw_reference"].replace("\\", "/"))
        self.assertIn(r["run_id"], r["raw_reference"].replace("\\", "/"))

    def test_03_provenance_preserved(self) -> None:
        path = self._csv(
            "prov.csv",
            [{"title": "P", "price": "2", "链接": "https://www.goofish.com/item/pv1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_REAL)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT * FROM market_observations LIMIT 1").fetchone())
            run = dict(
                conn.execute(
                    "SELECT * FROM collection_runs WHERE run_id=?", (r["run_id"],)
                ).fetchone()
            )
        self.assertEqual(row["run_id"], r["run_id"])
        self.assertTrue(row["raw_reference"])
        self.assertTrue(row["collector_version"])
        self.assertTrue(row["normalizer_version"])
        self.assertEqual(run["collection_mode"], msc.MODE_IMPORT)

    def test_04_real_only_when_justified(self) -> None:
        path = self._csv(
            "just.csv",
            [{"title": "J", "price": "3", "链接": "https://www.goofish.com/item/j1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_REAL)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT data_origin, verification_status FROM market_observations").fetchone())
        self.assertEqual(row["data_origin"], msc.ORIGIN_REAL)
        self.assertEqual(row["verification_status"], msc.VERIF_MANUAL)

    def test_05_unknown_when_not_declared(self) -> None:
        path = self._csv(
            "unk.csv",
            [{"title": "U", "price": "3", "链接": "https://www.goofish.com/item/u1"}],
        )
        xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT data_origin, verification_status FROM market_observations").fetchone())
        self.assertEqual(row["data_origin"], msc.ORIGIN_UNKNOWN)
        self.assertEqual(row["verification_status"], msc.VERIF_UNVERIFIED)

    def test_06_missing_counts_null(self) -> None:
        path = self._csv(
            "nullcounts.csv",
            [{"title": "N", "price": "9.9", "链接": "https://www.goofish.com/item/nc1"}],
        )
        xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT * FROM market_observations").fetchone())
        self.assertIsNone(row["view_count"])
        self.assertIsNone(row["want_count"])
        self.assertIsNone(row["share_count"])
        self.assertIsNone(row["comment_count"])

    def test_07_explicit_zero_preserved(self) -> None:
        path = self._csv(
            "zero.csv",
            [
                {
                    "title": "Z",
                    "price": "1",
                    "want_count": "0",
                    "view_count": "0",
                    "链接": "https://www.goofish.com/item/z0",
                }
            ],
        )
        xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT want_count, view_count FROM market_observations").fetchone())
        self.assertEqual(row["want_count"], 0)
        self.assertEqual(row["view_count"], 0)

    def test_08_duplicate_same_item_rejected(self) -> None:
        path = self._csv(
            "dup.csv",
            [
                {"title": "D", "price": "1", "链接": "https://www.goofish.com/item/dup1"},
                {"title": "D", "price": "1", "链接": "https://www.goofish.com/item/dup1"},
            ],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        self.assertEqual(r["stats"]["accepted_count"], 1)
        self.assertEqual(r["stats"]["duplicate_count"], 1)

    def test_09_historical_observation_retained(self) -> None:
        path = self._csv(
            "hist.csv",
            [{"title": "H", "price": "1", "链接": "https://www.goofish.com/item/hist1"}],
        )
        r1 = xic.import_file(
            path, declared_origin=msc.ORIGIN_UNKNOWN, observed_at="2026-08-01T00:00:00+08:00"
        )
        r2 = xic.import_file(
            path, declared_origin=msc.ORIGIN_UNKNOWN, observed_at="2026-08-07T00:00:00+08:00"
        )
        self.assertTrue(r1["ok"] and r2["ok"])
        with database.get_connection() as conn:
            n = conn.execute(
                "SELECT COUNT(*) FROM market_observations WHERE source_item_id='hist1'"
            ).fetchone()[0]
        self.assertEqual(n, 2)

    def test_10_observation_not_market_event(self) -> None:
        path = self._csv(
            "noe.csv",
            [{"title": "E", "price": "1", "链接": "https://www.goofish.com/item/noe1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_REAL)
        self.assertFalse(r["market_event_created"])
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT notes FROM market_observations").fetchone())
            tables = {
                t[0]
                for t in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
        notes = json.loads(row["notes"])
        self.assertTrue(notes["not_market_event"])
        if "market_events" in tables:
            with database.get_connection() as conn:
                n = conn.execute("SELECT COUNT(*) FROM market_events").fetchone()[0]
            self.assertEqual(n, 0)

    def test_11_observation_not_product(self) -> None:
        path = self._csv(
            "nop.csv",
            [{"title": "P", "price": "1", "链接": "https://www.goofish.com/item/nop1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_REAL, mirror_to_products=False)
        self.assertFalse(r["product_created"])
        with database.get_connection() as conn:
            n = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        self.assertEqual(n, 0)

    def test_12_observation_not_our_listing(self) -> None:
        path = self._csv(
            "nol.csv",
            [{"title": "L", "price": "1", "链接": "https://www.goofish.com/item/nol1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_REAL)
        self.assertFalse(r["listing_created"])
        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT notes FROM market_observations").fetchone())
        notes = json.loads(row["notes"])
        self.assertTrue(notes["not_our_listing"])

    def test_13_source_not_sales(self) -> None:
        path = self._csv(
            "sns.csv",
            [{"title": "S", "price": "1", "链接": "https://www.goofish.com/item/sns1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_REAL)
        self.assertIsNone(r["sales_platform"])
        self.assertEqual(r["discovery_platform"], "xianyu")
        sep = msc.assert_source_sales_independent("xianyu", "taobao")
        self.assertTrue(sep["allowed"])
        self.assertFalse(sep["auto_bound"])

    def test_14_old_sample_rejected(self) -> None:
        sample_dir = self.raw_dir / "2026-07-04"
        sample_dir.mkdir(parents=True)
        sample = sample_dir / "虚拟资料_sample.xlsx"
        # write csv bytes under sample name marker (path classify)
        sample.write_text("not-needed", encoding="utf-8")
        # Also place marked name in imports
        marked = self.imports / "export_sample.csv"
        self._csv = None
        with open(marked, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["title", "price", "链接"])
            w.writeheader()
            w.writerow({"title": "测试", "price": "99.9", "链接": "https://goofish.com/item/ok"})
        r = xic.import_file(marked, declared_origin=msc.ORIGIN_REAL, allow_sample=False)
        self.assertFalse(r["ok"])
        self.assertEqual(r["error"], "sample_or_fixture_file_rejected")
        # path sample xlsx
        r2 = xic.import_file(sample, declared_origin=msc.ORIGIN_REAL, allow_sample=False)
        self.assertFalse(r2["ok"])

    def test_15_legacy_db_not_read(self) -> None:
        readiness = xic.import_readiness()
        self.assertEqual(readiness["status"], "WAITING_FOR_REAL_SOURCE_FILE")
        self.assertEqual(msc.count_observations(), 0)
        # Pilot does not pull archive DB
        report = pilot.run_pilot(auto_import=False)
        self.assertEqual(report["entry_status"], "READY_FOR_REAL_IMPORT")
        self.assertEqual(report["waiting"], "WAITING_FOR_REAL_SOURCE_FILE")

    def test_16_batch_rollback_on_fatal(self) -> None:
        path = self._csv(
            "fatal.csv",
            [
                {"title": "A", "price": "1", "链接": "https://www.goofish.com/item/fa1"},
                {"title": "B", "price": "2", "链接": "https://www.goofish.com/item/fa2"},
            ],
        )
        # Force second row to raise by patching normalize after first success is hard;
        # use fatal_on_row_error with a custom bad row via monkeypatch insert
        original = msc.insert_market_observation
        calls = {"n": 0}

        def flaky(obs):
            calls["n"] += 1
            if calls["n"] >= 2:
                raise RuntimeError("forced_fatal")
            return original(obs)

        with mock.patch.object(msc, "insert_market_observation", side_effect=flaky):
            # re-bind module reference used inside import_file — patch xic.msc
            with mock.patch.object(xic.msc, "insert_market_observation", side_effect=flaky):
                r = xic.import_file(
                    path,
                    declared_origin=msc.ORIGIN_UNKNOWN,
                    fatal_on_row_error=True,
                )
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], "FAILED")
        self.assertEqual(msc.count_observations(), 0)

    def test_17_collection_run_counts(self) -> None:
        path = self._csv(
            "counts.csv",
            [
                {"title": "C1", "price": "1", "链接": "https://www.goofish.com/item/c1"},
                {"title": "", "price": "1", "链接": "https://www.goofish.com/item/c2"},
                {"title": "C1", "price": "1", "链接": "https://www.goofish.com/item/c1"},
            ],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        s = r["stats"]
        self.assertEqual(s["raw_count"], 3)
        self.assertEqual(s["accepted_count"], 1)
        self.assertEqual(s["rejected_count"], 1)
        self.assertEqual(s["duplicate_count"], 1)
        self.assertEqual(
            s["accepted_count"] + s["rejected_count"] + s["duplicate_count"],
            s["raw_count"],
        )
        with database.get_connection() as conn:
            run = dict(
                conn.execute(
                    "SELECT * FROM collection_runs WHERE run_id=?", (r["run_id"],)
                ).fetchone()
            )
        self.assertEqual(run["raw_count"], 3)
        self.assertEqual(run["accepted_count"], 1)

    def test_18_invalid_price_rejected_not_zero(self) -> None:
        path = self._csv(
            "badprice.csv",
            [{"title": "Bad", "price": "not-a-number", "链接": "https://www.goofish.com/item/bp1"}],
        )
        r = xic.import_file(path, declared_origin=msc.ORIGIN_UNKNOWN)
        self.assertEqual(r["stats"]["accepted_count"], 0)
        self.assertEqual(r["stats"]["rejected_count"], 1)
        self.assertIn("invalid_price", r["stats"]["rejected_reasons"])

    def test_19_import_readiness_waiting(self) -> None:
        st = xic.import_readiness()
        self.assertTrue(st["import_ready"])
        self.assertEqual(st["status"], "WAITING_FOR_REAL_SOURCE_FILE")
        self.assertEqual(st["entry_status"], "READY_FOR_REAL_IMPORT")


if __name__ == "__main__":
    unittest.main()
