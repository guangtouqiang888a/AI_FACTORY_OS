# Entry 058A — Legacy DB archive + clean Current DB tests

from __future__ import annotations

import hashlib
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "6_EXECUTION"))
sys.path.insert(0, str(ROOT / "3_DECISION"))
sys.path.insert(0, str(ROOT / "7_MEMORY"))

import config  # noqa: E402
import database  # noqa: E402
import publish_queue as pq  # noqa: E402
import price_intelligence as pi  # noqa: E402
import memory_core  # noqa: E402

ARCHIVE = ROOT / "99_ARCHIVE" / "database_history" / "ai_factory_legacy_simulation_20260830.db"
MANIFEST = ROOT / "99_ARCHIVE" / "database_history" / "DATABASE_ARCHIVE_MANIFEST.md"
RAW = ROOT / "data" / "raw" / "xianyu"


class Entry058ADatabaseResetTests(unittest.TestCase):
    def test_01_current_db_exists(self) -> None:
        self.assertTrue(Path(config.DB_PATH).exists())

    def test_02_current_db_opens(self) -> None:
        with database.get_connection() as conn:
            n = conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
            ).fetchone()[0]
        self.assertGreater(n, 0)

    def test_03_schema_tables_present(self) -> None:
        with database.get_connection() as conn:
            names = {
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        for t in (
            "products",
            "scores",
            "platforms",
            "market_events",
            "market_signals",
            "selection_results",
            "publish_queue",
            "publish_evidence",
        ):
            self.assertIn(t, names)

    def test_04_no_legacy_product_rows(self) -> None:
        with database.get_connection() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM products").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM market_signals").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM keywords").fetchone()[0], 0)

    def test_05_app_connects(self) -> None:
        database.ensure_schema()
        with database.get_connection() as conn:
            conn.execute("SELECT 1").fetchone()

    def test_06_modules_init_clean(self) -> None:
        import market_event_core as mec
        import market_signal_core as msc

        mec.ensure_market_event_schema()
        msc.ensure_market_signal_schema()
        pq.ensure_publish_queue_schema()
        with database.get_connection() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM products").fetchone()[0], 0)

    def test_07_legacy_archived(self) -> None:
        self.assertTrue(ARCHIVE.exists())
        self.assertTrue(MANIFEST.exists())
        conn = sqlite3.connect(f"file:{ARCHIVE.as_posix()}?mode=ro", uri=True)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM products").fetchone()[0], 61)
        conn.close()

    def test_08_legacy_hash_recorded(self) -> None:
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("sha256", text.lower())
        h = hashlib.sha256()
        with open(ARCHIVE, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        self.assertIn(h.hexdigest(), text)

    def test_09_raw_preserved(self) -> None:
        self.assertTrue(RAW.exists())
        samples = list(RAW.rglob("*sample*.xlsx"))
        self.assertTrue(samples)

    def test_10_sample_cannot_enter_commercial_learning(self) -> None:
        ok, reason = memory_core.is_commercial_learning_eligible({
            "event_type": "purchase",
            "data_origin": "simulation",
            "verification_status": "VERIFIED",
        })
        self.assertFalse(ok)

    def test_11_99_9_reads_legacy_archive(self) -> None:
        p = pi.audit_99_9_provenance()
        self.assertFalse(p["classification"].get("is_real_market", True))
        self.assertIn("SAMPLE", p["classification"]["data_origin"])
        self.assertEqual(p["classification"]["db_role"], "legacy_archive")

    def test_12_publish_queue_operational_restored(self) -> None:
        entry = pq.get_queue_entry("pq_auto_f2f8bab97df8")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["queue_status"], pq.QUEUE_AWAITING_HUMAN)
        self.assertEqual(entry["product_asset_id"], "f2f8bab97df8")


if __name__ == "__main__":
    unittest.main()
