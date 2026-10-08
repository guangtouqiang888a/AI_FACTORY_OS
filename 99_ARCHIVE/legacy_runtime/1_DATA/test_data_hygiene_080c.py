# Entry 080-C — NULL semantics / engagement hygiene tests (temp DB)

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import market_signal_core as msc  # noqa: E402
import market_source_core as msrc  # noqa: E402


class Entry080CNullGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_080c.db"
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
        ]
        for p in self._patches:
            p.start()
        msrc.ensure_market_source_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def test_01_null_view_engagement_unavailable_observation_path(self) -> None:
        listings = [
            {"want_count": 100, "view_count": None, "price": 1.0, "platform": "xianyu"},
            {"want_count": 50, "view_count": None, "price": 2.0, "platform": "xianyu"},
        ]
        sigs = msc._compute_deterministic_signals(
            "Excel模板",
            listings,
            evidence={"lineage": "market_observation"},
            null_as_zero=False,
        )
        eng = next(s for s in sigs if s["signal_type"] == "engagement_signal")
        self.assertEqual(eng["value_status"], "UNAVAILABLE")
        self.assertIsNone(eng["value"])
        self.assertNotEqual(eng["value"], 0)
        self.assertNotEqual(eng["value"], 0.0)

    def test_02_null_want_not_zero_demand_when_all_missing(self) -> None:
        listings = [
            {"want_count": None, "view_count": None, "price": 1.0, "platform": "xianyu"},
        ]
        sigs = msc._compute_deterministic_signals(
            "Excel模板",
            listings,
            evidence={"lineage": "market_observation"},
            null_as_zero=False,
        )
        demand = next(s for s in sigs if s["signal_type"] == "demand_signal")
        self.assertEqual(demand["value_status"], "UNAVAILABLE")
        self.assertIsNone(demand["value"])
        trend = next(s for s in sigs if s["signal_type"] == "trend_signal")
        self.assertEqual(trend["value_status"], "UNAVAILABLE")
        self.assertIsNone(trend["value"])

    def test_03_known_want_sum_ignores_null_wants(self) -> None:
        listings = [
            {"want_count": 100, "view_count": None, "price": 1.0, "platform": "xianyu"},
            {"want_count": None, "view_count": None, "price": 2.0, "platform": "xianyu"},
        ]
        sigs = msc._compute_deterministic_signals(
            "Excel模板",
            listings,
            evidence={"lineage": "market_observation"},
            null_as_zero=False,
        )
        demand = next(s for s in sigs if s["signal_type"] == "demand_signal")
        self.assertEqual(demand["value_status"], "COMPUTED")
        self.assertEqual(demand["value"], 100.0)

    def test_04_product_path_legacy_null_as_zero_unchanged(self) -> None:
        """054 product contract: missing view → engagement 0.0 still allowed."""
        listings = [
            {"want_count": 10, "view_count": None, "price": 1.0, "platform": "xianyu"},
        ]
        sigs = msc._compute_deterministic_signals(
            "legacy",
            listings,
            evidence={"lineage": "product"},
            null_as_zero=True,
        )
        eng = next(s for s in sigs if s["signal_type"] == "engagement_signal")
        self.assertEqual(eng["value_status"], "COMPUTED")
        self.assertEqual(eng["value"], 0.0)

    def test_05_reject_non_real_candidates(self) -> None:
        ok, oid = msrc.insert_market_observation(
            {
                "source_id": "src_xianyu_marketplace",
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": "sample_item_1",
                "source_url": "https://www.goofish.com/item?id=sample_item_1",
                "title": "t",
                "price": 1.0,
                "want_count": 10,
                "view_count": None,
                "data_origin": msrc.ORIGIN_SAMPLE,
                "verification_status": msrc.VERIF_UNVERIFIED,
                "observed_at": "2026-09-05T12:00:00+08:00",
                "collection_query": "Excel模板",
            }
        )
        # SAMPLE as REAL is rejected at insert; force UNKNOWN path
        if not ok:
            ok, oid = msrc.insert_market_observation(
                {
                    "source_id": "src_xianyu_marketplace",
                    "source": "xianyu",
                    "platform": "xianyu",
                    "source_item_id": "hyp_item_1",
                    "source_url": "https://www.goofish.com/item?id=hyp_item_1",
                    "title": "t",
                    "price": 1.0,
                    "want_count": 10,
                    "view_count": None,
                    "data_origin": msrc.ORIGIN_UNKNOWN,
                    "verification_status": msrc.VERIF_UNVERIFIED,
                    "observed_at": "2026-09-05T12:00:01+08:00",
                    "collection_query": "Excel模板",
                }
            )
        self.assertTrue(ok)
        out = msc.derive_signals_from_observation_candidates(
            [
                {
                    "observation_id": oid,
                    "filter_status": "MATCH",
                }
            ]
        )
        self.assertEqual(out["signal_count"], 0)
        reasons = {s.get("reason") for s in out["skipped"]}
        self.assertTrue(
            "data_origin_not_REAL" in reasons
            or "verification_not_MANUAL_VERIFIED" in reasons
        )

    def test_06_collection_query_keyword_resolution(self) -> None:
        kw = msc.resolve_observation_keyword(
            {"collection_query": "Excel模板", "notes": None}
        )
        self.assertEqual(kw, "Excel模板")


if __name__ == "__main__":
    unittest.main()
