# Entry 052 — Publish Queue + Human External Action Gate tests

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "6_EXECUTION"))
sys.path.insert(0, str(ROOT / "3_DECISION"))
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import config  # noqa: E402
import publish_queue as pq  # noqa: E402
from candidate_selector import select_candidates  # noqa: E402


class PublishQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_queue.db"
        self.pkg = base / "publish_package"
        self.pkg.mkdir()
        for name in pq.REQUIRED_PACKAGE_FILES:
            if name.endswith(".json"):
                (self.pkg / name).write_text('{"price": 12.9}', encoding="utf-8")
            else:
                (self.pkg / name).write_text("ok", encoding="utf-8")

        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
        ]
        for p in self._patches:
            p.start()
        pq.ensure_publish_queue_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _eligible(self, **overrides) -> dict:
        base = {
            "product_id": "prod_1",
            "product_asset_id": "asset_1",
            "product_type": "document",
            "experiment_id": "exp_1",
            "production_request_id": "preq_1",
            "platform": "taobao",
            "listing_title": "Test Product",
            "price": 12.9,
            "currency": "CNY",
            "quality_status": "passed",
            "validation_status": "passed",
            "validation_passed": True,
            "risk_status": "passed",
            "commercial_status": "acceptable",
            "commercial_score": 80,
            "package_path": str(self.pkg),
        }
        base.update(overrides)
        return base

    def test_1_eligible_enters_queue(self) -> None:
        result = pq.enqueue_publish_candidate(self._eligible())
        self.assertTrue(result["accepted"])
        self.assertEqual(result["queue_status"], pq.QUEUE_READY)
        self.assertFalse(result["published"])
        self.assertFalse(result["commercial_success"])

    def test_2_quality_fail_blocked(self) -> None:
        result = pq.enqueue_publish_candidate(
            self._eligible(quality_status="failed", product_asset_id="a_qfail")
        )
        self.assertTrue(result["accepted"])
        self.assertEqual(result["queue_status"], pq.QUEUE_BLOCKED)
        self.assertIn("quality_failed", result["blockers"])

    def test_3_risk_unknown_blocked(self) -> None:
        result = pq.enqueue_publish_candidate(
            self._eligible(risk_status="unknown", product_asset_id="a_risk")
        )
        self.assertEqual(result["queue_status"], pq.QUEUE_BLOCKED)
        self.assertIn("risk_unknown", result["blockers"])

        result2 = pq.enqueue_publish_candidate(
            self._eligible(risk_status="failed", product_asset_id="a_risk2")
        )
        self.assertIn("risk_failed", result2["blockers"])

    def test_4_missing_asset_blocked(self) -> None:
        c = self._eligible()
        c.pop("product_asset_id")
        result = pq.enqueue_publish_candidate(c)
        self.assertEqual(result["queue_status"], pq.QUEUE_BLOCKED)
        self.assertTrue(
            any("product_asset" in b or "missing_product" in b for b in result["blockers"])
        )

    def test_5_ready_not_auto_published(self) -> None:
        result = pq.enqueue_publish_candidate(
            self._eligible(product_asset_id="a_ready")
        )
        self.assertEqual(result["queue_status"], pq.QUEUE_READY)
        entry = pq.get_queue_entry(result["publish_queue_id"])
        self.assertNotEqual(entry["queue_status"], pq.QUEUE_PUBLISHED)
        self.assertEqual(entry["observation_eligible"], 0)
        self.assertFalse(result["auto_external_publish"])

    def test_6_human_evidence_to_published(self) -> None:
        enq = pq.enqueue_publish_candidate(
            self._eligible(product_asset_id="a_ev", enter_human_gate=True)
        )
        self.assertEqual(enq["queue_status"], pq.QUEUE_AWAITING_HUMAN)
        pack = pq.get_human_action_pack(enq["publish_queue_id"])
        self.assertTrue(pack["ok"])
        self.assertIn("auto_publish_click", pack["forbidden"])

        ev = pq.record_publish_evidence({
            "queue_id": enq["publish_queue_id"],
            "platform": "taobao",
            "listing_reference": "https://item.taobao.com/item.htm?id=123",
            "verification_status": "MANUAL_VERIFIED",
            "human_operator": "test_operator",
            "published_at": "2026-08-29T16:00:00",
        })
        self.assertTrue(ev["accepted"])
        self.assertEqual(ev["queue_status"], pq.QUEUE_PUBLISHED)
        self.assertTrue(ev["observation_eligible"])
        self.assertFalse(ev["observation_started"])

    def test_7_published_not_commercial_success(self) -> None:
        enq = pq.enqueue_publish_candidate(
            self._eligible(product_asset_id="a_comm", enter_human_gate=True)
        )
        ev = pq.record_publish_evidence({
            "queue_id": enq["publish_queue_id"],
            "listing_reference": "listing_999",
            "verification_status": "VERIFIED",
            "source": "human_screenshot_path",
        })
        self.assertTrue(ev["accepted"])
        self.assertFalse(ev["commercial_success"])
        self.assertFalse(ev.get("observation_started", True))

    def test_8_future_product_type_video(self) -> None:
        result = pq.enqueue_publish_candidate(
            self._eligible(
                product_asset_id="video_asset",
                product_type="video",
                platform="taobao",
            )
        )
        self.assertTrue(result["accepted"])
        entry = pq.get_queue_entry(result["publish_queue_id"])
        self.assertEqual(entry["product_type"], "video")

    def test_9_future_platform(self) -> None:
        result = pq.enqueue_publish_candidate(
            self._eligible(
                product_asset_id="fp_asset",
                platform="hypothetical_future_platform",
            )
        )
        self.assertTrue(result["accepted"])
        entry = pq.get_queue_entry(result["publish_queue_id"])
        self.assertEqual(entry["platform"], "hypothetical_future_platform")

    def test_10_invalid_duplicate_evidence_rejected(self) -> None:
        enq = pq.enqueue_publish_candidate(
            self._eligible(product_asset_id="a_dup", enter_human_gate=True)
        )
        payload = {
            "queue_id": enq["publish_queue_id"],
            "listing_reference": "same_listing",
            "verification_status": "VERIFIED",
            "published_at": "2026-08-29T12:00:00",
            "platform": "taobao",
        }
        r1 = pq.record_publish_evidence(payload)
        r2 = pq.record_publish_evidence(payload)
        self.assertTrue(r1["accepted"])
        self.assertFalse(r2["accepted"])
        self.assertEqual(r2["reason"], "duplicate_evidence")

        bad = pq.record_publish_evidence({
            "queue_id": enq["publish_queue_id"],
            "listing_reference": "other",
            "verification_status": "UNVERIFIED",
        })
        self.assertFalse(bad["accepted"])
        self.assertEqual(bad["reason"], "unverified_evidence_rejected")

    def test_advance_ready_to_human(self) -> None:
        enq = pq.enqueue_publish_candidate(
            self._eligible(product_asset_id="a_adv")
        )
        adv = pq.advance_to_awaiting_human(enq["publish_queue_id"])
        self.assertTrue(adv["ok"])
        self.assertEqual(adv["queue_status"], pq.QUEUE_AWAITING_HUMAN)

    def test_candidate_selector_minimal(self) -> None:
        products = [
            {"title": "A", "keyword": "k", "price": 10, "scores": {"total": 90}},
            {"title": "B赌博", "keyword": "k", "price": 10, "scores": {"total": 99}},
            {"title": "C", "keyword": "k", "price": 10, "scores": {"total": 40}},
        ]
        out = select_candidates(products, top_n=5, min_score=60)
        self.assertFalse(out["auto_external_publish"])
        titles = [c["title"] for c in out["production_candidates"]]
        self.assertIn("A", titles)
        self.assertNotIn("B赌博", titles)
        self.assertTrue(any(c["total_score"] == 90 for c in out["publish_candidates_pregate"]))


if __name__ == "__main__":
    unittest.main()
