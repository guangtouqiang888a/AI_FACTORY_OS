# Entry 055 — End-to-End Autonomous Product Generation Pilot tests

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
sys.path.insert(0, str(ROOT / "1_DATA"))

import e2e_autonomous_pilot as e2e  # noqa: E402
import commercial_handoff as ch  # noqa: E402
import publish_queue as pq  # noqa: E402


class Entry055E2ETests(unittest.TestCase):
    def test_01_real_market_data_to_candidate(self) -> None:
        bundle = e2e.load_rank1_selection()
        self.assertIsNotNone(bundle)
        self.assertTrue(bundle["selection"].get("selected"))
        self.assertIsNotNone(bundle["selection"].get("candidate_id"))

    def test_02_candidate_has_score(self) -> None:
        bundle = e2e.load_rank1_selection()
        self.assertIsNotNone(bundle["selection"].get("score"))

    def test_03_candidate_has_risk(self) -> None:
        bundle = e2e.load_rank1_selection()
        self.assertEqual(str(bundle["selection"].get("risk_status")).lower(), "passed")

    def test_04_experiment_candidate_fields(self) -> None:
        bundle = e2e.load_rank1_selection()
        ec = e2e.build_experiment_candidate(bundle)
        for key in (
            "experiment_candidate_id",
            "source_opportunity",
            "target_user",
            "problem",
            "product_type",
            "hypothesis",
            "test_goal",
            "candidate_score",
            "risk_status",
            "evidence_refs",
            "selection_reason",
            "status",
        ):
            self.assertIn(key, ec)
        self.assertEqual(ec["hypothesis"]["status"], "HYPOTHESIS")

    def test_05_cf_type_mapping_virtual_only(self) -> None:
        self.assertEqual(e2e.map_product_type_for_cf("digital_template"), "excel")
        with self.assertRaises(ValueError):
            e2e.map_product_type_for_cf("short_video")

    def test_06_no_fake_opportunity_when_empty(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            empty = Path(td) / "empty.json"
            empty.write_text(json.dumps({"candidates": [], "selection_results": []}), encoding="utf-8")
            self.assertIsNone(e2e.load_rank1_selection(empty))

    def test_07_future_video_structurally_valid_lifecycle_fields(self) -> None:
        # Structural: product_type is a string field — video would not break object shape
        sample = {
            "product_type": "short_video",
            "product_asset_id": "future_vid",
            "product_version": "v1",
            "quality_status": "passed",
            "risk_status": "passed",
            "delivery_method": "stream_link",
            "commercial_metadata": {
                "target_user": "u",
                "problem": "p",
                "offer": "o",
                "delivery_method": "stream_link",
            },
        }
        gate = ch.evaluate_commercial_readiness({**sample, "product_id": "p1"})
        self.assertTrue(gate["ready"])
        # Runtime generation forbidden now
        with self.assertRaises(ValueError):
            e2e.map_product_type_for_cf("short_video")

    def test_08_future_novel_structurally_valid(self) -> None:
        sample = {
            "product_id": "n1",
            "product_type": "novel",
            "product_asset_id": "novel_asset",
            "product_version": "v1",
            "quality_status": "passed",
            "risk_status": "passed",
            "delivery_method": "epub",
            "commercial_metadata": {
                "target_user": "u",
                "problem": "p",
                "offer": "o",
                "delivery_method": "epub",
            },
        }
        self.assertTrue(ch.evaluate_commercial_readiness(sample)["ready"])
        with self.assertRaises(ValueError):
            e2e.map_product_type_for_cf("novel")

    def test_09_future_platform_listing_field(self) -> None:
        listing = {
            "listing_id": "lst_future_tb",
            "platform": "taobao",
            "listing_price": 9.9,
            "delivery_method": "zip",
            "risk_status": "passed",
        }
        # Platform is metadata on Listing — core remains valid
        self.assertEqual(listing["platform"], "taobao")
        self.assertNotIn("taobao_product_table", listing)

    def test_10_production_success_not_commercial_success(self) -> None:
        trace_path = e2e.TRACE_JSON
        if not trace_path.exists():
            self.skipTest("Entry 055 trace not yet materialized")
        data = json.loads(trace_path.read_text(encoding="utf-8"))
        tr = data.get("trace") or data
        self.assertFalse(tr.get("commercial_success"))
        self.assertFalse(tr.get("published"))
        self.assertFalse(tr.get("market_events_created"))
        self.assertFalse(tr.get("commercial_learning_ingested"))

    def test_11_awaiting_human_does_not_publish(self) -> None:
        trace_path = e2e.TRACE_JSON
        if not trace_path.exists():
            self.skipTest("Entry 055 trace not yet materialized")
        tr = json.loads(trace_path.read_text(encoding="utf-8"))["trace"]
        self.assertEqual(tr.get("queue_status"), pq.QUEUE_AWAITING_HUMAN)
        self.assertFalse(tr.get("published"))
        entry = pq.get_queue_entry(tr["publish_queue_id"])
        self.assertIsNotNone(entry)
        self.assertEqual(entry["queue_status"], pq.QUEUE_AWAITING_HUMAN)

    def test_12_trace_ids_linked(self) -> None:
        trace_path = e2e.TRACE_JSON
        if not trace_path.exists():
            self.skipTest("Entry 055 trace not yet materialized")
        tr = json.loads(trace_path.read_text(encoding="utf-8"))["trace"]
        for key in (
            "opportunity_id",
            "experiment_id",
            "production_request_id",
            "product_asset_id",
            "commercial_product_id",
            "listing_id",
            "publish_queue_id",
        ):
            self.assertTrue(tr.get(key), msg=f"missing {key}")

    def test_13_legacy_pilot_not_used(self) -> None:
        trace_path = e2e.TRACE_JSON
        if not trace_path.exists():
            self.skipTest("Entry 055 trace not yet materialized")
        tr = json.loads(trace_path.read_text(encoding="utf-8"))["trace"]
        self.assertFalse(tr.get("legacy_pilot_used"))
        self.assertNotEqual(tr.get("product_asset_id"), "8523329941d4")
        self.assertNotEqual(tr.get("experiment_id"), "exp_20260708_005")

    def test_14_real_product_asset_file(self) -> None:
        trace_path = e2e.TRACE_JSON
        if not trace_path.exists():
            self.skipTest("Entry 055 trace not yet materialized")
        tr = json.loads(trace_path.read_text(encoding="utf-8"))["trace"]
        pid = tr["product_asset_id"]
        art = ROOT / "11_CONTENT_FACTORY" / "artifacts" / "products" / pid
        self.assertTrue(art.exists())
        xlsx = list(art.glob("templates/*.xlsx"))
        self.assertTrue(xlsx, "xlsx missing")
        # OLE/ZIP magic for xlsx
        magic = xlsx[0].read_bytes()[:2]
        self.assertEqual(magic, b"PK")

    def test_15_listing_package_minimum(self) -> None:
        trace_path = e2e.TRACE_JSON
        if not trace_path.exists():
            self.skipTest("Entry 055 trace not yet materialized")
        tr = json.loads(trace_path.read_text(encoding="utf-8"))["trace"]
        pkg = Path(tr["package_path"])
        ok, missing = pq.check_publish_package(pkg)
        self.assertTrue(ok, missing)


class Entry055RegressionSmoke(unittest.TestCase):
    """Smoke that prior Entry modules still import and key invariants hold."""

    def test_regression_imports(self) -> None:
        sys.path.insert(0, str(ROOT / "7_MEMORY"))
        sys.path.insert(0, str(ROOT / "1_DATA"))
        sys.path.insert(0, str(ROOT / "3_DECISION"))
        import memory_core  # noqa: F401
        import market_event_core  # noqa: F401
        import market_signal_core  # noqa: F401
        import opportunity_discovery  # noqa: F401
        ok, reason = memory_core.is_commercial_learning_eligible({
            "event_type": "publish",
            "data_origin": "simulation",
        })
        self.assertFalse(ok)
        self.assertIn("simulation", reason)


if __name__ == "__main__":
    unittest.main()
