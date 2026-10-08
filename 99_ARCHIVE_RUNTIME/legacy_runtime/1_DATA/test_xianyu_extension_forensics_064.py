# Entry 064 — Reference plugin forensics (static)

from __future__ import annotations

import json
import unittest
import zipfile
from pathlib import Path

PLUGIN_ROOT = (
    Path(__file__).resolve().parent
    / "_tests"
    / "xianyu_extension_forensics_064"
    / "reference_plugin"
    / "my-xianyu-scraper"
)
FORENSICS_ROOT = PLUGIN_ROOT.parent.parent
ZIP_PATH = Path(r"D:\闲鱼全自动采集插件1.zip")


class Entry064ExtensionForensicsTests(unittest.TestCase):
    def test_01_zip_integrity(self) -> None:
        self.assertTrue(ZIP_PATH.exists(), f"missing {ZIP_PATH}")
        with zipfile.ZipFile(ZIP_PATH) as z:
            self.assertGreater(len(z.namelist()), 0)
            bad = z.testzip()
            self.assertIsNone(bad)

    def test_02_manifest_parse(self) -> None:
        manifest = json.loads((PLUGIN_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["manifest_version"], 3)
        self.assertEqual(manifest["name"], "闲鱼全自动高热度采集器")
        self.assertIn("activeTab", manifest["permissions"])
        self.assertFalse((PLUGIN_ROOT / "background.js").exists())

    def test_03_content_script_dom_not_api(self) -> None:
        c = (PLUGIN_ROOT / "content.js").read_text(encoding="utf-8")
        self.assertIn("document.querySelectorAll", c)
        self.assertNotIn("fetch(", c)
        self.assertNotIn("mtop", c.lower())
        self.assertNotIn("cookie", c.lower())

    def test_04_want_count_regex(self) -> None:
        c = (PLUGIN_ROOT / "content.js").read_text(encoding="utf-8")
        self.assertIn(r"(\d+)\s*人想要", c)
        self.assertIn("text.match", c)
        self.assertIn("人想要", c)

    def test_05_filter_in_collector_not_separate(self) -> None:
        c = (PLUGIN_ROOT / "content.js").read_text(encoding="utf-8")
        self.assertIn("wantCount >= minWant", c)
        self.assertIn("if (match)", c)  # skips cards without want text

    def test_06_dedupe_by_title(self) -> None:
        c = (PLUGIN_ROOT / "content.js").read_text(encoding="utf-8")
        self.assertIn("seenTitles", c)
        self.assertIn("seenTitles.has(title)", c)

    def test_07_pagination_selector(self) -> None:
        c = (PLUGIN_ROOT / "content.js").read_text(encoding="utf-8")
        self.assertIn("search-pagination-page-box", c)
        self.assertIn("sleep(5000)", c)

    def test_08_popup_message_bridge(self) -> None:
        p = (PLUGIN_ROOT / "popup.js").read_text(encoding="utf-8")
        c = (PLUGIN_ROOT / "content.js").read_text(encoding="utf-8")
        self.assertIn("start_auto_scrape", p)
        self.assertIn("start_auto_scrape", c)
        self.assertIn("chrome.tabs.sendMessage", p)
        self.assertIn("chrome.runtime.onMessage", c)

    def test_09_export_csv_blob(self) -> None:
        p = (PLUGIN_ROOT / "popup.js").read_text(encoding="utf-8")
        self.assertIn("Blob", p)
        self.assertIn("createObjectURL", p)
        self.assertIn("download", p)

    def test_10_no_credential_extraction(self) -> None:
        for name in ("content.js", "popup.js"):
            t = (PLUGIN_ROOT / name).read_text(encoding="utf-8").lower()
            self.assertNotIn("password", t)
            self.assertNotIn("localstorage.getitem", t)
            self.assertNotIn("chrome.cookies", t)

    def test_11_inventory_file_exists(self) -> None:
        inv = FORENSICS_ROOT / "file_inventory.json"
        self.assertTrue(inv.exists())
        data = json.loads(inv.read_text(encoding="utf-8"))
        self.assertIn("files", data)

    def test_12_ai_factory_duplicate_modules_present(self) -> None:
        data = Path(__file__).resolve().parent
        for mod in (
            "acquisition_engine.py",
            "collector_abstraction.py",
            "market_source_core.py",
        ):
            self.assertTrue((data / mod).exists(), mod)


if __name__ == "__main__":
    unittest.main()
