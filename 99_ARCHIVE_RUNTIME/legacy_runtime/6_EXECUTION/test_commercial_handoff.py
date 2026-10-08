# Entry 053 — Commercial Handoff / Product-Listing separation tests

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "6_EXECUTION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import commercial_handoff as ch  # noqa: E402


class CommercialHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.cp_path = base / "commercial_products_v1.json"
        self.list_path = base / "listings_v1.json"
        self.pkg = base / "publish_package"
        self.pkg.mkdir()
        for name in ch.REQUIRED_PACKAGE_FILES:
            if name.endswith(".json"):
                (self.pkg / name).write_text('{"suggested_price": 12.9}', encoding="utf-8")
            else:
                (self.pkg / name).write_text("ok", encoding="utf-8")

        self._patches = [
            mock.patch.object(ch, "COMMERCIAL_PRODUCTS_JSON", self.cp_path),
            mock.patch.object(ch, "LISTINGS_JSON", self.list_path),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _full_cp(self, **over) -> dict:
        base = {
            "product_id": "prod_1",
            "product_version": "v1",
            "product_asset_id": "asset_1",
            "product_type": "digital_template",
            "quality_status": "passed",
            "risk_status": "passed",
            "delivery_method": "zip",
            "commercial_metadata": {
                "target_user": "u",
                "problem": "p",
                "offer": "o",
                "delivery_method": "zip",
            },
        }
        base.update(over)
        return base

    def test_1_full_commercial_ready(self) -> None:
        g = ch.evaluate_commercial_readiness(self._full_cp())
        self.assertTrue(g["ready"])
        self.assertEqual(g["commercial_status"], ch.CP_COMMERCIAL_READY)
        self.assertFalse(g["published"])

    def test_2_asset_only_not_ready(self) -> None:
        g = ch.evaluate_commercial_readiness({
            "product_asset_id": "8523329941d4",
            "quality_status": "passed",
        })
        self.assertFalse(g["ready"])
        self.assertTrue(any("missing_product" in b for b in g["blockers"]))

    def test_3_commercial_ready_not_published(self) -> None:
        cp = ch.upsert_commercial_product(self._full_cp())
        self.assertEqual(cp["commercial_status"], ch.CP_COMMERCIAL_READY)
        self.assertFalse(cp["published"])
        self.assertFalse(cp["commercial_success"])

    def test_4_listing_package_ready_not_published(self) -> None:
        pkg = ch.evaluate_listing_package(self.pkg)
        self.assertIn(pkg["package_status"], (ch.PKG_PREPARED, ch.PKG_PREPARED_PLACEHOLDER))
        self.assertFalse(pkg["published"])
        self.assertFalse(pkg["marketing_ready"])

    def test_5_awaiting_human_no_auto_publish(self) -> None:
        cp = self._full_cp()
        cp["commercial_status"] = ch.CP_COMMERCIAL_READY
        cp["readiness"] = {"ready": True}
        pkg = ch.evaluate_listing_package(self.pkg)
        listing = {
            "platform": "taobao",
            "listing_price": 12.9,
            "delivery_method": "zip",
            "risk_status": "passed",
        }
        r = ch.evaluate_listing_publish_readiness(cp, listing, pkg)
        self.assertTrue(r["ready_for_human_action"])
        self.assertEqual(r["listing_status"], ch.LIST_AWAITING_HUMAN)
        self.assertFalse(r["auto_publish"])
        self.assertFalse(r["published"])

    def test_6_evidence_creates_published_listing_eligible(self) -> None:
        listing = ch.upsert_listing({
            "listing_id": "lst_ev",
            "platform": "taobao",
            "listing_status": ch.LIST_AWAITING_HUMAN,
            "listing_price": 12.9,
        })
        r = ch.mark_published_listing_from_evidence(
            "lst_ev", "pev_test", verification_status="MANUAL_VERIFIED"
        )
        self.assertTrue(r["accepted"])
        self.assertTrue(r["observation_eligible"])
        self.assertFalse(r["observation_started"])
        self.assertEqual(r["listing"]["listing_status"], ch.LIST_PUBLISHED)

    def test_7_published_not_commercial_success(self) -> None:
        ch.upsert_listing({
            "listing_id": "lst_cs",
            "platform": "xianyu",
            "listing_status": ch.LIST_AWAITING_HUMAN,
        })
        r = ch.mark_published_listing_from_evidence(
            "lst_cs", "pev_2", verification_status="VERIFIED"
        )
        self.assertFalse(r["commercial_success"])

    def test_8_product_type_document(self) -> None:
        p = ch.future_compatibility_probe("document", "xlsx", "taobao")
        self.assertTrue(p["ok"])
        self.assertTrue(p["core_model_valid"])

    def test_9_product_type_video(self) -> None:
        p = ch.future_compatibility_probe("video", "mp4", "taobao")
        self.assertTrue(p["ok"])
        self.assertFalse(p["requires_runtime_rebuild"])

    def test_10_asset_type_xlsx(self) -> None:
        p = ch.future_compatibility_probe("digital_template", "xlsx", "xianyu")
        self.assertEqual(p["asset_type"], "xlsx")
        self.assertTrue(p["ok"])

    def test_11_asset_type_mp4(self) -> None:
        p = ch.future_compatibility_probe("short_video", "mp4", "future_platform")
        self.assertEqual(p["asset_type"], "mp4")
        self.assertTrue(p["core_model_valid"])

    def test_12_platform_xianyu(self) -> None:
        self.assertTrue(ch.future_compatibility_probe("document", "pdf", "xianyu")["ok"])

    def test_13_platform_taobao(self) -> None:
        self.assertTrue(ch.future_compatibility_probe("document", "pdf", "taobao")["ok"])

    def test_14_platform_future(self) -> None:
        p = ch.future_compatibility_probe("novel", "epub", "future_platform")
        self.assertTrue(p["ok"])
        self.assertEqual(p["platform"], "future_platform")

    def test_published_without_evidence_blocked(self) -> None:
        listing = ch.upsert_listing({
            "listing_id": "lst_noev",
            "platform": "taobao",
            "listing_status": ch.LIST_PUBLISHED,
            # no evidence_id
        })
        self.assertNotEqual(listing["listing_status"], ch.LIST_PUBLISHED)
        self.assertFalse(listing["published"])

    def test_price_boundary_roles(self) -> None:
        roles = ch.classify_price_role({
            "product_price_hypothesis": 12.9,
            "cf_packaging_default": 19.9,
            "listing_price": None,
            "actual_paid_price": None,
        })
        self.assertEqual(roles["product_price_hypothesis"], 12.9)
        self.assertEqual(roles["cf_packaging_default"], 19.9)
        self.assertIsNone(roles["actual_paid_price"])


if __name__ == "__main__":
    unittest.main()
