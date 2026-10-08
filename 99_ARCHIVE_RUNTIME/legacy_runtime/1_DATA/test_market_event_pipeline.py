# Entry 051 — Market Event / Commercial Observation Pipeline tests

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "7_MEMORY"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import config  # noqa: E402
import database  # noqa: E402
import market_event_core as mec  # noqa: E402
import memory_core  # noqa: E402


class MarketEventPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_market.db"
        self.obs_path = base / "observations_v1.json"
        self.pattern_path = base / "pattern_memory.json"
        self.events_path = base / "event_log.jsonl"
        self.strategy_path = base / "strategy_memory.json"
        self.policy_path = base / "runtime_policy.json"

        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(config, "MEMORY_DIR", base),
            mock.patch.object(config, "LOGS_DIR", base),
            mock.patch.object(config, "PATTERN_MEMORY_PATH", self.pattern_path),
            mock.patch.object(config, "EVENT_LOG_PATH", self.events_path),
            mock.patch.object(config, "STRATEGY_MEMORY_PATH", self.strategy_path),
            mock.patch.object(config, "RUNTIME_POLICY_PATH", self.policy_path),
            mock.patch.object(mec, "OBSERVATIONS_JSON", self.obs_path),
        ]
        for p in self._patches:
            p.start()
        self.pattern_path.write_text(
            json.dumps({"patterns": []}, ensure_ascii=False), encoding="utf-8"
        )
        mec.ensure_market_event_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _base_ids(self) -> dict:
        return {
            "product_asset_id": "8523329941d4",
            "product_id": "prod_pilot",
            "experiment_id": "exp_20260708_005",
            "listing_id": "listing_test_001",
            "source": "manual_entry_test",
        }

    def test_1_real_verified_purchase_commercial_learning(self) -> None:
        raw = {
            **self._base_ids(),
            "event_type": "PURCHASE",
            "platform": "taobao",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "taobao_order_export",
            "event_timestamp": "2026-08-29T10:00:00",
            "value": 12.9,
            "currency": "CNY",
            "external_event_id": "order_t1",
        }
        result = mec.ingest_raw_market_event(raw)
        self.assertTrue(result["accepted"])
        self.assertTrue(result["commercial_success"])
        self.assertTrue(result["learning"]["ingest"]["accepted"])
        patterns = memory_core.load_pattern_memory()["patterns"]
        commercial = [p for p in patterns if p.get("commercial_success")]
        self.assertEqual(len(commercial), 1)
        self.assertEqual(commercial[0].get("source_event_id"), result["event_id"])
        self.assertEqual(commercial[0].get("original_event_type"), "PURCHASE")

    def test_2_real_verified_view_observation_not_commercial(self) -> None:
        raw = {
            **self._base_ids(),
            "event_type": "VIEW",
            "platform": "taobao",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "taobao_analytics",
            "event_timestamp": "2026-08-29T11:00:00",
            "external_event_id": "view_t2",
        }
        result = mec.ingest_raw_market_event(raw)
        self.assertTrue(result["accepted"])
        self.assertFalse(result["commercial_success"])
        self.assertTrue(result["observation"]["accepted"])
        self.assertFalse(result["observation"]["commercial_success"])
        self.assertEqual(
            result["learning"]["reason"], "not_commercial_learning_event_type"
        )
        patterns = memory_core.load_pattern_memory()["patterns"]
        self.assertEqual(sum(1 for p in patterns if p.get("commercial_success")), 0)

    def test_3_simulation_purchase_rejected(self) -> None:
        raw = {
            **self._base_ids(),
            "event_type": "PURCHASE",
            "platform": "taobao",
            "data_origin": "SIMULATION",
            "verification_status": "VERIFIED",
            "verified_source": "sim",
            "external_event_id": "sim_purchase_1",
        }
        result = mec.ingest_raw_market_event(raw)
        self.assertTrue(result["accepted"])  # persisted as simulation fact
        self.assertFalse(result["commercial_success"])
        self.assertEqual(result["learning"]["reason"], "data_origin_not_REAL")
        # SIMULATION not observation-eligible under REAL rule
        self.assertIsNone(result["observation"])

    def test_4_real_unverified_purchase_blocked(self) -> None:
        raw = {
            **self._base_ids(),
            "event_type": "PURCHASE",
            "platform": "taobao",
            "data_origin": "REAL",
            "verification_status": "UNVERIFIED",
            "external_event_id": "unverified_p1",
            "value": 12.9,
            "currency": "CNY",
        }
        result = mec.ingest_raw_market_event(raw)
        self.assertTrue(result["accepted"])
        self.assertFalse(result["commercial_success"])
        self.assertIn("unverified", result["learning"]["reason"])

    def test_5_real_verified_refund_eligible(self) -> None:
        raw = {
            **self._base_ids(),
            "event_type": "REFUND",
            "platform": "taobao",
            "data_origin": "REAL",
            "verification_status": "MANUAL_VERIFIED",
            "verified_source": "human_order_confirm",
            "value": 12.9,
            "currency": "CNY",
            "external_event_id": "refund_1",
        }
        result = mec.ingest_raw_market_event(raw)
        self.assertTrue(result["accepted"])
        self.assertTrue(result["commercial_success"])
        self.assertEqual(
            result["learning"]["ingest"]["reason"],
            "eligible_for_real_commercial_learning",
        )

    def test_6_duplicate_deduped(self) -> None:
        raw = {
            **self._base_ids(),
            "event_type": "CLICK",
            "platform": "xianyu",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "xianyu_export",
            "external_event_id": "click_dup",
        }
        r1 = mec.ingest_raw_market_event(raw)
        r2 = mec.ingest_raw_market_event(raw)
        self.assertTrue(r1["accepted"])
        self.assertFalse(r2["accepted"])
        self.assertEqual(r2["reason"], "duplicate_event")
        self.assertEqual(r2["duplicate_of"], r1["event_id"])

    def test_7_missing_linkage_unresolved_not_guessed(self) -> None:
        raw = {
            "event_type": "INQUIRY",
            "platform": "taobao",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "seller_msg",
            "external_event_id": "inq_nolink",
            # no product / experiment
        }
        result = mec.ingest_raw_market_event(raw)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["normalized"]["linkage_status"], "UNRESOLVED")
        self.assertIn("missing_product", result["normalized"]["linkage_notes"])
        self.assertIn("missing_experiment", result["normalized"]["linkage_notes"])
        stored = mec.get_event_by_id(result["event_id"])
        self.assertEqual(stored["linkage_status"], "UNRESOLVED")
        self.assertIsNone(stored["experiment_id"])

    def test_8_new_platform_no_schema_rewrite(self) -> None:
        raw = {
            **self._base_ids(),
            "event_type": "FAVORITE",
            "platform": "hypothetical_future_platform",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "future_connector",
            "external_event_id": "fav_future_1",
            "product_type": "document",
        }
        result = mec.ingest_raw_market_event(raw)
        self.assertTrue(result["accepted"])
        self.assertEqual(
            result["normalized"]["platform"], "hypothetical_future_platform"
        )
        # core table still works — no platform-specific table required
        with database.get_connection() as conn:
            tables = {
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
        self.assertIn("market_events", tables)
        self.assertNotIn("hypothetical_future_platform_product", tables)
        self.assertNotIn("taobao_product", tables)

    def test_future_product_type_video_and_watch_time(self) -> None:
        """Abstract compatibility: document + video product_type on same schema."""
        doc = mec.ingest_raw_market_event({
            **self._base_ids(),
            "event_type": "PURCHASE",
            "platform": "xianyu",
            "product_type": "document",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "xianyu_order",
            "external_event_id": "doc_buy",
            "value": 9.9,
            "currency": "CNY",
        })
        vid = mec.ingest_raw_market_event({
            **self._base_ids(),
            "event_type": "WATCH_TIME",
            "platform": "hypothetical_future_platform",
            "product_type": "video",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "future_analytics",
            "value": 120.0,
            "external_event_id": "vid_watch",
            "experiment_id": "exp_future_video",
            "product_asset_id": "video_asset_placeholder",
        })
        self.assertTrue(doc["accepted"])
        self.assertTrue(vid["accepted"])
        self.assertEqual(doc["normalized"]["product_type"], "document")
        self.assertEqual(vid["normalized"]["product_type"], "video")
        # WATCH_TIME → observation only, not commercial success
        self.assertFalse(vid["commercial_success"])
        self.assertTrue(vid["observation"]["accepted"])

    def test_revenue_none_vs_zero(self) -> None:
        """Revenue None (unknown) vs 0 (explicit zero) must remain distinct."""
        view = mec.ingest_raw_market_event({
            **self._base_ids(),
            "event_type": "VIEW",
            "platform": "taobao",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "taobao",
            "external_event_id": "rev_view_only",
        })
        obs_id = view["observation"]["observation_id"]
        store = json.loads(self.obs_path.read_text(encoding="utf-8"))
        obs = next(o for o in store["observations"] if o["observation_id"] == obs_id)
        self.assertIsNone(obs["revenue"])

        mec.ingest_raw_market_event({
            **self._base_ids(),
            "event_type": "REVENUE",
            "platform": "taobao",
            "data_origin": "REAL",
            "verification_status": "VERIFIED",
            "verified_source": "taobao",
            "value": 0,
            "currency": "CNY",
            "external_event_id": "rev_zero",
        })
        store2 = json.loads(self.obs_path.read_text(encoding="utf-8"))
        obs2 = next(o for o in store2["observations"] if o["observation_id"] == obs_id)
        self.assertEqual(obs2["revenue"], 0.0)


if __name__ == "__main__":
    unittest.main()
