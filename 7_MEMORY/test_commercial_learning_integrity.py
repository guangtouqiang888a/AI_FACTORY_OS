# Entry 050 — Commercial Learning Integrity Hardening tests
"""
验证：
1. published_local → execution success ≠ commercial success
2. simulation purchase ≠ real commercial learning
3. real purchase + verified source → commercial learning eligible
4. unknown source → rejected
5. quality_passed ≠ commercial success
6. production_completed ≠ commercial success
7. Execution Learning 仍可运行
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "7_MEMORY"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import config  # noqa: E402
import memory_core  # noqa: E402


class CommercialLearningIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        base = Path(self._tmpdir.name)
        self.pattern_path = base / "pattern_memory.json"
        self.strategy_path = base / "strategy_memory.json"
        self.events_path = base / "events.jsonl"
        self.policy_path = base / "runtime_policy.json"
        self.patch_path = base / "policy_patch.json"
        self.snapshot_path = base / "policy_snapshot.json"

        self._patches = [
            mock.patch.object(config, "PATTERN_MEMORY_PATH", self.pattern_path),
            mock.patch.object(config, "STRATEGY_MEMORY_PATH", self.strategy_path),
            mock.patch.object(config, "EVENT_LOG_PATH", self.events_path),
            mock.patch.object(config, "RUNTIME_POLICY_PATH", self.policy_path),
            mock.patch.object(config, "POLICY_PATCH_PATH", self.patch_path),
            mock.patch.object(config, "RUNTIME_POLICY_SNAPSHOT_PATH", self.snapshot_path),
            mock.patch.object(config, "MEMORY_DIR", base),
            mock.patch.object(config, "LOGS_DIR", base),
        ]
        for p in self._patches:
            p.start()
        self.pattern_path.write_text(
            json.dumps({"patterns": []}, ensure_ascii=False), encoding="utf-8"
        )

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _published_local_context(self) -> dict:
        return {
            "task": "excel_template",
            "nodes": {
                "decision": {
                    "result": {
                        "action": "publish",
                        "keyword": "excel_template",
                        "best": {"scores": {"total": 80}},
                    },
                    "score": 80,
                },
                "execution": {"result": {"status": "published_local"}},
                "scoring": {"result": {"count": 3}},
            },
        }

    def test_published_local_is_execution_not_commercial(self) -> None:
        pattern = memory_core.extract_pattern(self._published_local_context())
        self.assertEqual(pattern["outcome"], "success")
        self.assertEqual(pattern["exec_status"], "published_local")
        self.assertEqual(pattern["outcome_domain"], "EXECUTION")
        self.assertFalse(pattern["commercial_success"])
        self.assertIsNone(pattern.get("commercial_outcome"))
        self.assertEqual(pattern["data_origin"], memory_core.DATA_ORIGIN_SIMULATION)
        self.assertEqual(pattern["learning_lane"], memory_core.LEARNING_LANE_EXECUTION)

        ok, reason = memory_core.is_commercial_learning_eligible({
            "exec_status": "published_local",
            "data_origin": memory_core.DATA_ORIGIN_SIMULATION,
        })
        self.assertFalse(ok)
        self.assertIn("published_local", reason)

    def test_simulation_purchase_rejected_from_real_commercial(self) -> None:
        ok, reason = memory_core.is_commercial_learning_eligible({
            "commercial_outcome": "purchase",
            "data_origin": memory_core.DATA_ORIGIN_SIMULATION,
            "verified_source": "sim_store",
        })
        self.assertFalse(ok)
        self.assertIn("simulation", reason)

        result = memory_core.ingest_commercial_learning_event({
            "commercial_outcome": "purchase",
            "data_origin": memory_core.DATA_ORIGIN_SIMULATION,
            "verified_source": "sim_store",
        })
        self.assertFalse(result["accepted"])
        self.assertFalse(result["commercial_success"])

    def test_real_purchase_eligible(self) -> None:
        record = {
            "commercial_outcome": "purchase",
            "data_origin": memory_core.DATA_ORIGIN_REAL,
            "verified_source": "taobao_order_api",
            "commercial_evidence_id": "order_123",
            "keyword": "考勤记录表",
        }
        ok, reason = memory_core.is_commercial_learning_eligible(record)
        self.assertTrue(ok, reason)
        self.assertEqual(reason, "eligible_for_real_commercial_learning")

        result = memory_core.ingest_commercial_learning_event(record)
        self.assertTrue(result["accepted"])
        self.assertTrue(result["commercial_success"])
        self.assertEqual(result["learning_lane"], memory_core.LEARNING_LANE_COMMERCIAL)

        patterns = memory_core.load_pattern_memory()["patterns"]
        commercial = [p for p in patterns if p.get("commercial_success")]
        self.assertEqual(len(commercial), 1)
        skipped = memory_core.update_strategy(commercial[0])
        self.assertTrue(skipped.get("skipped"))

    def test_unknown_source_rejected(self) -> None:
        ok, reason = memory_core.is_commercial_learning_eligible({
            "commercial_outcome": "purchase",
            "data_origin": memory_core.DATA_ORIGIN_UNKNOWN,
            "verified_source": "maybe_shop",
        })
        self.assertFalse(ok)
        self.assertIn("UNKNOWN", reason)

        ok2, reason2 = memory_core.is_commercial_learning_eligible({
            "commercial_outcome": "revenue",
            "data_origin": memory_core.DATA_ORIGIN_REAL,
            "verified_source": "unknown",
        })
        self.assertFalse(ok2)
        self.assertIn("verified_source", reason2)

    def test_quality_pass_not_commercial(self) -> None:
        ok, reason = memory_core.is_commercial_learning_eligible({
            "quality_outcome": "quality_pass",
            "data_origin": memory_core.DATA_ORIGIN_REAL,
            "verified_source": "qa_pipeline",
        })
        self.assertFalse(ok)
        self.assertIn("quality", reason)

    def test_production_completed_not_commercial(self) -> None:
        ok, reason = memory_core.is_commercial_learning_eligible({
            "production_outcome": "production_completed",
            "data_origin": memory_core.DATA_ORIGIN_REAL,
            "verified_source": "content_factory",
        })
        self.assertFalse(ok)
        self.assertIn("production", reason)

    def test_execution_learning_still_works(self) -> None:
        pattern = memory_core.extract_pattern(self._published_local_context())
        self.assertEqual(pattern["outcome"], "success")
        self.assertFalse(pattern.get("discarded", False) or pattern["confidence"] < 0)

        store = memory_core.update_strategy(pattern)
        self.assertFalse(store.get("skipped", False), store)
        self.assertEqual(store.get("strategy_domain"), "EXECUTION")

        stats = memory_core.get_pattern_stats()
        self.assertEqual(stats["learning_lane"], memory_core.LEARNING_LANE_EXECUTION)
        self.assertEqual(stats["strategy_domain"], "EXECUTION")
        self.assertGreaterEqual(stats["total"], 1)
        self.assertGreater(stats["success_rate"], 0)

        memory_core.ingest_commercial_learning_event({
            "commercial_outcome": "purchase",
            "data_origin": memory_core.DATA_ORIGIN_REAL,
            "verified_source": "taobao_order_api",
            "keyword": "other",
        })
        stats2 = memory_core.get_pattern_stats(
            learning_lane=memory_core.LEARNING_LANE_EXECUTION,
        )
        for p in memory_core.load_pattern_memory()["patterns"]:
            if p.get("commercial_success"):
                self.assertFalse(memory_core.is_execution_learning_pattern(p))
        self.assertEqual(stats2["total"], stats["total"])


if __name__ == "__main__":
    unittest.main()