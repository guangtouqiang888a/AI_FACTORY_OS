# Entry 060 — Xianyu Browser Collector v1 tests (isolated temp DB)

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import acquisition_engine as eng  # noqa: E402
import collector_abstraction as cab  # noqa: E402
import config  # noqa: E402
import market_source_core as msc  # noqa: E402
from connectors import xianyu_browser_connector as xbc  # noqa: E402
from connectors import xianyu_import_connector as xic  # noqa: E402


class Entry060BrowserCollectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_060.db"
        self.raw_dir = base / "raw" / "xianyu"
        self.imports = self.raw_dir / "imports"
        self.imports.mkdir(parents=True)
        self.art = base / "artifacts_060"
        self.art.mkdir()
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(config, "RAW_XIANYU_DIR", self.raw_dir),
            mock.patch.object(xic, "IMPORTS_DIR", self.imports),
            mock.patch.object(xbc, "ARTIFACT_DIR", self.art),
        ]
        for p in self._patches:
            p.start()
        eng.ensure_acquisition_engine_schema()
        msc.ensure_market_source_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def test_01_adapter_wired(self) -> None:
        ad = cab.get_adapter("PUBLIC_WEB_READ")
        self.assertEqual(ad.adapter_id, "adapter_xianyu_browser")
        self.assertEqual(ad.acquisition_mode, "PUBLIC_WEB_READ")

    def test_02_dependency_probe(self) -> None:
        dep = xbc.browser_dependency_status()
        self.assertIn(dep["status"], ("READY", "DEPENDENCY_MISSING"))
        self.assertIn(
            dep.get("usable_backend"),
            (None, "chrome_headless_dump", "selenium", "playwright"),
        )

    def test_03_access_control_detects_illegal_access(self) -> None:
        code = xbc._detect_access_control(
            "非法访问 为了保障您的体验，请使用正常浏览器访问闲鱼~",
            title="搜索_闲鱼",
        )
        self.assertEqual(code, "ACCESS_DENIED")

    def test_04_blocked_does_not_write_observations(self) -> None:
        fake_page = {
            "final_url": "https://www.goofish.com/search?q=x",
            "page_title": "t",
            "access_control": "ACCESS_DENIED",
            "cards": [
                {
                    "title": "should_not_insert",
                    "price": 1.0,
                    "want_count": 9,
                    "source_url": "https://www.goofish.com/item/fake",
                    "source_item_id": "fake",
                }
            ],
            "backend": "mock",
            "error": None,
        }
        with mock.patch.object(
            xbc.XianyuBrowserCollector,
            "_collect_chrome_dump",
            return_value=fake_page,
        ), mock.patch.object(
            xbc,
            "browser_dependency_status",
            return_value={
                "status": "READY",
                "usable_backend": "chrome_headless_dump",
                "chrome_or_edge_hint": r"C:\fake\chrome.exe",
                "playwright": False,
                "selenium": False,
                "chrome_headless_dump": True,
            },
        ):
            r = xbc.XianyuBrowserCollector().acquire(
                collection_query="虚拟资料", max_records=20
            )
        self.assertEqual(r["status"], "BLOCKED_BY_ACCESS_CONTROL")
        self.assertFalse(r["ok"])
        self.assertEqual(msc.count_observations(), 0)
        self.assertFalse(r.get("product_created"))
        self.assertFalse(r.get("listing_created"))
        self.assertFalse(r.get("market_event_created"))
        self.assertFalse(r.get("login_used"))
        self.assertFalse(r.get("bypass_attempted"))

    def test_05_success_inserts_only_real_cards(self) -> None:
        fake_page = {
            "final_url": "https://www.goofish.com/search?q=x",
            "page_title": "ok",
            "access_control": None,
            "cards": [
                {
                    "title": "真实标题模板",
                    "price": 12.5,
                    "want_count": None,
                    "source_url": "https://www.goofish.com/item/ae060001",
                    "source_item_id": "ae060001",
                    "view_count": None,
                    "comment_count": None,
                    "share_count": None,
                    "seller_reference": None,
                    "published_at": None,
                }
            ],
            "backend": "mock",
            "error": None,
        }
        with mock.patch.object(
            xbc.XianyuBrowserCollector,
            "_collect_chrome_dump",
            return_value=fake_page,
        ), mock.patch.object(
            xbc,
            "browser_dependency_status",
            return_value={
                "status": "READY",
                "usable_backend": "chrome_headless_dump",
                "chrome_or_edge_hint": r"C:\fake\chrome.exe",
                "playwright": False,
                "selenium": False,
                "chrome_headless_dump": True,
            },
        ):
            r = xbc.XianyuBrowserCollector().acquire(
                collection_query="虚拟资料", max_records=20
            )
        self.assertTrue(r["ok"])
        self.assertEqual(msc.count_observations(), 1)
        import database
        import json as _json

        with database.get_connection() as conn:
            row = dict(conn.execute("SELECT * FROM market_observations").fetchone())
            run = dict(
                conn.execute(
                    "SELECT acquisition_mode FROM collection_runs WHERE run_id=?",
                    (row["run_id"],),
                ).fetchone()
            )
        self.assertEqual(row["title"], "真实标题模板")
        self.assertIsNone(row["want_count"])  # NULL preserved, not invented
        notes = _json.loads(row["notes"] or "{}")
        self.assertEqual(notes.get("acquisition_mode"), "PUBLIC_WEB_READ")
        self.assertEqual(run["acquisition_mode"], "PUBLIC_WEB_READ")

    def test_06_engine_public_web_task_ready(self) -> None:
        t = eng.create_collection_task(
            query="虚拟资料", acquisition_mode="PUBLIC_WEB_READ", max_records=20
        )
        self.assertEqual(t["status"], eng.TASK_READY)
        self.assertEqual(t["acquisition_mode"], "PUBLIC_WEB_READ")


if __name__ == "__main__":
    unittest.main()
