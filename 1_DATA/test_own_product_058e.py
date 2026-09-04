# Entry 058E — Own Product Principle + Public Web feasibility (no Current DB write)

from __future__ import annotations

import json
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import product_origin as po  # noqa: E402

TEST_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_public_web_058e"


class Entry058ETests(unittest.TestCase):
    def test_01_own_product_principle_defined(self) -> None:
        self.assertIn("self-produced", po.OWN_PRODUCT_PRINCIPLE.lower())
        self.assertIn("自主生产", po.OWN_PRODUCT_PRINCIPLE_ZH)
        self.assertIn(po.ORIGIN_MARKET_INSPIRED, po.PRODUCT_ORIGINS)
        self.assertIn(po.ORIGIN_SELF_PRODUCED, po.PRODUCT_ORIGINS)

    def test_02_market_inspired_not_auto_infringement(self) -> None:
        b = po.default_commercial_boundary(product_origin=po.ORIGIN_MARKET_INSPIRED)
        self.assertTrue(b["market_inspired_is_not_auto_infringement"])
        self.assertTrue(b["no_originality_score_hard_gate"])

    def test_03_product_type_neq_business_model(self) -> None:
        r = po.assert_product_type_neq_business_model(
            "digital_template", [po.BM_DIRECT_SALE, po.BM_VOLUME_LOW_PRICE]
        )
        self.assertTrue(r["ok"])
        self.assertIn(po.BM_DIRECT_SALE, r["business_models"])

    def test_04_multi_business_models(self) -> None:
        models = po.normalize_business_models(
            [po.BM_DIRECT_SALE, po.BM_TRAFFIC_ACQUISITION]
        )
        self.assertEqual(len(models), 2)

    def test_05_feasibility_artifacts_exist(self) -> None:
        self.assertTrue((TEST_DIR / "feasibility_report.json").exists())
        report = json.loads((TEST_DIR / "feasibility_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["method"], "PUBLIC_WEB_READ")
        self.assertFalse(report["login_used"])
        self.assertFalse(report["bypass_attempted"])
        self.assertFalse(report["hidden_api_called"])
        self.assertFalse(report["current_db_write"])
        self.assertEqual(report["query"], "虚拟资料")

    def test_06_fields_truthful_no_guess(self) -> None:
        report = json.loads((TEST_DIR / "feasibility_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["fields"]["want_count"], "UNAVAILABLE")
        self.assertEqual(report["fields"]["title"], "UNAVAILABLE")
        self.assertEqual(report["fields"]["price"], "UNAVAILABLE")
        self.assertEqual(report["items_extracted"], 0)
        self.assertIn(report["feasibility"], ("NOT_FEASIBLE", "LIMITED_FIELD_ACCESS", "FEASIBLE"))

    def test_07_current_db_untouched(self) -> None:
        db = Path(config.DB_PATH)
        self.assertTrue(db.exists())
        conn = sqlite3.connect(db)
        try:
            for t in (
                "products",
                "market_observations",
                "market_signals",
                "selection_results",
            ):
                n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                self.assertEqual(n, 0, f"{t} must remain 0 after 058E test")
        finally:
            conn.close()

    def test_08_no_legacy_sample_as_test_input(self) -> None:
        report = json.loads((TEST_DIR / "feasibility_report.json").read_text(encoding="utf-8"))
        blob = json.dumps(report)
        self.assertNotIn("虚拟资料_sample.xlsx", blob)
        self.assertNotIn("ai_factory_legacy_simulation", blob)

    def test_09_source_sales_still_independent(self) -> None:
        import market_source_core as msc

        r = msc.assert_source_sales_independent("xianyu", "taobao")
        self.assertTrue(r["allowed"])
        self.assertFalse(r["auto_bound"])

    def test_10_pipeline_order(self) -> None:
        pipe = po.market_to_product_pipeline()
        self.assertEqual(pipe[0], "Market Intelligence")
        self.assertIn("Own Product Concept", pipe)
        self.assertIn("Risk / Rights", pipe)


if __name__ == "__main__":
    unittest.main()
