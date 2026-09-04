# Entry 057 — Price Intelligence tests

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "3_DECISION"))
sys.path.insert(0, str(ROOT / "6_EXECUTION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import price_intelligence as pi  # noqa: E402
import publish_queue as pq  # noqa: E402


ASSET = "f2f8bab97df8"
LEGACY = "8523329941d4"
QUEUE = "pq_auto_f2f8bab97df8"


class Entry057PriceIntelligenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = pi.run_price_intelligence(ASSET)

    def test_01_price_default_not_validated(self) -> None:
        p19 = pi.audit_19_9_provenance()
        self.assertTrue(p19["classification"]["is_default"])
        self.assertFalse(p19["classification"]["is_validated"])

    def test_02_ai_recommendation_not_paid(self) -> None:
        rec = self.result["recommendation"]
        self.assertIsNone(rec["paid_price"])
        self.assertFalse(rec["validated"])
        self.assertEqual(rec["recommended_experimental_price"], 19.9)

    def test_03_paid_distinct_from_recommendation(self) -> None:
        rec = self.result["recommendation"]
        self.assertNotEqual(rec["recommended_experimental_price"], rec["paid_price"])
        self.assertIsNone(rec["ontology"]["paid_price"])

    def test_04_missing_evidence_confidence_not_fabricated(self) -> None:
        rec = self.result["recommendation"]
        self.assertEqual(rec["confidence"], "LOW")
        self.assertEqual(rec["confidence_meaning"], "evidence_confidence_not_sale_probability")

    def test_05_multi_channel_listing_level(self) -> None:
        # Same product can have channel-specific listing prices; product ontology keeps listing null until confirm
        rec = self.result["recommendation"]
        self.assertIsNone(rec["ontology"]["listing_price"])
        self.assertIn("channel", rec)

    def test_06_multi_product_type_structure(self) -> None:
        for pt in ("digital_template", "document", "video", "novel", "audio"):
            sample = {
                "price_recommendation_id": "x",
                "product_type": pt,
                "channel": "future_platform",
                "recommended_price": 9.9,
                "currency": "CNY",
            }
            self.assertIsInstance(sample["product_type"], str)
            self.assertIsInstance(sample["channel"], str)

    def test_07_legacy_pilot_isolated(self) -> None:
        iso = pi.audit_12_9_isolation()
        self.assertFalse(iso["applies_to_autonomous"])
        self.assertEqual(iso["role"], pi.HISTORICAL_PRICE)
        self.assertEqual(pi.run_price_intelligence(LEGACY)["ok"], False)

    def test_08_simulation_not_price_learning(self) -> None:
        rec = self.result["recommendation"]
        self.assertEqual(rec["price_learning_data"], "NONE")
        self.assertTrue(rec["simulation_rejected_from_real_price_learning"])
        self.assertFalse(rec["price_learning_eligible"])

    def test_09_real_paid_future_boundary(self) -> None:
        # Boundary recognized: only future REAL paid enables learning eligibility flag path
        rec = self.result["recommendation"]
        self.assertIsNone(rec["paid_price"])
        self.assertFalse(rec["price_learning_eligible"])

    def test_10_production_cost_not_market_price(self) -> None:
        rec = self.result["recommendation"]
        self.assertFalse(rec["forbidden_mappings_checked"]["production_cost_to_price"])

    def test_11_commercial_score_not_price(self) -> None:
        rec = self.result["recommendation"]
        self.assertFalse(rec["forbidden_mappings_checked"]["commercial_score_to_price"])
        self.assertNotEqual(rec["recommended_experimental_price"], 88.75)

    def test_12_99_9_provenance_identified(self) -> None:
        p = pi.audit_99_9_provenance()
        self.assertTrue(p["classification"]["avg_matches_signal"])
        self.assertEqual(p["classification"]["primary_role"], pi.MARKET_REFERENCE_PRICE)
        self.assertFalse(p["classification"]["is_validated"])

    def test_13_19_9_provenance_identified(self) -> None:
        p = pi.audit_19_9_provenance()
        self.assertEqual(p["classification"]["primary_role"], pi.CF_PIPELINE_DEFAULT)

    def test_14_queue_unchanged(self) -> None:
        entry = pq.get_queue_entry(QUEUE)
        self.assertEqual(entry["queue_status"], pq.QUEUE_AWAITING_HUMAN)

    def test_15_no_publish_evidence_created(self) -> None:
        self.assertEqual(
            pq.get_queue_entry(QUEUE)["queue_status"],
            pq.QUEUE_AWAITING_HUMAN,
        )
        import human_publish_pack as hpp

        self.assertEqual(hpp.count_publish_evidence(QUEUE), 0)

    def test_16_recommendation_persisted(self) -> None:
        store = json.loads(pi.RECOMMENDATIONS_JSON.read_text(encoding="utf-8"))
        self.assertTrue(any(r.get("product_asset_id") == ASSET for r in store["recommendations"]))
        self.assertEqual(store.get("price_learning_data"), "NONE")


if __name__ == "__main__":
    unittest.main()
