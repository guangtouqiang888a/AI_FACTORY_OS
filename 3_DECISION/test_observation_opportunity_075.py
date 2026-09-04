# 3_DECISION/test_observation_opportunity_075.py — Entry 075 Observation Signal → Opportunity

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "3_DECISION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import config  # noqa: E402
import database  # noqa: E402
import market_signal_core as msc  # noqa: E402
import market_source_core as msrc  # noqa: E402
import opportunity_discovery as od  # noqa: E402
from scorer import score_observation_listing, score_product  # noqa: E402


def _seed_obs(
    *,
    observation_id: str,
    want_count,
    price=1.0,
    view_count=None,
    query="Excel模板",
    data_origin="REAL",
    verification_status="MANUAL_VERIFIED",
) -> dict:
    notes = json.dumps(
        {"query": query, "session_id": "sess_test_075", "result_origin": "SEARCH_RESULT"},
        ensure_ascii=False,
    )
    row = {
        "observation_id": observation_id,
        "run_id": "crun_test_075",
        "source_id": "src_xianyu",
        "source": "xianyu",
        "platform": "xianyu",
        "source_type": "marketplace",
        "source_item_id": f"item_{observation_id[-6:]}",
        "source_url": f"https://example/item/{observation_id}",
        "title": f"title {observation_id}",
        "price": price,
        "currency": "CNY",
        "want_count": want_count,
        "view_count": view_count,
        "observed_at": "2026-09-03T15:20:02+08:00",
        "data_origin": data_origin,
        "verification_status": verification_status,
        "dedupe_key": f"dedupe_{observation_id}",
        "notes": notes,
        "raw_reference": "tests/entry_075",
    }
    ok, reason = msrc.insert_market_observation(row)
    if not ok:
        raise RuntimeError(reason)
    return row


def _seed_signal(
    signal_id: str,
    signal_type: str,
    keyword: str,
    value,
    observation_ids: list[str],
    *,
    data_origin="REAL",
    verification_status="MANUAL_VERIFIED",
) -> None:
    evidence = {
        "lineage": msc.LINEAGE_OBSERVATION,
        "observation_ids": observation_ids,
        "source_item_ids": [f"item_{oid[-6:]}" for oid in observation_ids],
        "collection_run_ids": ["crun_test_075"],
        "session_ids": ["sess_test_075"],
        "extension_run_ids": ["run_test_075"],
        "data_origins": [data_origin],
        "verification_statuses": [verification_status],
        "listing_count": len(observation_ids),
        "product_ids": [],
    }
    sig = {
        "signal_id": signal_id,
        "signal_type": signal_type,
        "keyword": keyword,
        "platform": "xianyu",
        "source": "market_observation",
        "value": value,
        "value_status": "UNAVAILABLE" if value is None else "COMPUTED",
        "unit": "test",
        "evidence_refs": evidence,
        "observation_timestamp": "2026-09-03T15:20:02+08:00",
        "computed_at": "2026-09-03T15:20:02",
        "product_type": "digital_template",
        "notes": "observation_candidate_lineage",
    }
    msc.persist_signals([sig])


class ObservationOpportunity075Tests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_075.db"
        self.obs_json = base / "observation_discovery_v1.json"
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
            mock.patch.object(od, "OBSERVATION_DISCOVERY_JSON", self.obs_json),
        ]
        for p in self._patches:
            p.start()
        database.ensure_schema()
        msrc.ensure_market_source_schema()
        msc.ensure_market_signal_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _count(self, table: str) -> int:
        with database.get_connection() as conn:
            return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    def _seed_full_group(self) -> list[str]:
        obs_ids = ["mobs_t075_a", "mobs_t075_b", "mobs_t075_c"]
        for i, oid in enumerate(obs_ids):
            _seed_obs(observation_id=oid, want_count=100 + i * 50)
        sig_ids = [
            "sig_t075_demand",
            "sig_t075_eng",
            "sig_t075_comp",
            "sig_t075_price",
            "sig_t075_trend",
            "sig_t075_growth",
        ]
        types = [
            "demand_signal",
            "engagement_signal",
            "competition_signal",
            "price_signal",
            "trend_signal",
            "growth_signal",
        ]
        values = [300.0, 0.0, 3.0, 1.0, 150.0, None]
        for sid, st, val in zip(sig_ids, types, values):
            _seed_signal(sid, st, "Excel模板", val, obs_ids)
        return sig_ids

    def test_a_consumes_persisted_signals(self) -> None:
        sig_ids = self._seed_full_group()
        products_before = self._count("products")
        signals_before = self._count("market_signals")
        result = od.discover_opportunities_from_observation_signals(sig_ids, persist=True)
        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["candidate_count"], 1)
        self.assertEqual(result["signals_loaded_from_db"], 6)
        self.assertFalse(result["signals_re_persisted"])
        self.assertFalse(result["product_substitution"])
        self.assertFalse(result["ai_invoked"])
        self.assertEqual(self._count("products"), products_before)
        self.assertEqual(self._count("market_signals"), signals_before)

    def test_b_provenance_preserved(self) -> None:
        sig_ids = self._seed_full_group()
        result = od.discover_opportunities_from_observation_signals(sig_ids, persist=False)
        cand = result["candidates"][0]
        prov = cand["provenance"]
        self.assertEqual(prov["lineage"], msc.LINEAGE_OBSERVATION)
        self.assertEqual(len(prov["observation_ids"]), 3)
        self.assertIn("sig_t075_demand", prov["signal_ids"])
        ev_types = {e.get("signal_id") for e in cand["evidence_refs"] if e.get("signal_id")}
        self.assertIn("sig_t075_demand", ev_types)
        lineage_ev = next(e for e in cand["evidence_refs"] if e.get("lineage"))
        self.assertIn("mobs_t075_a", lineage_ev["observation_ids"])

    def test_c_null_want_not_zero(self) -> None:
        self.assertIsNone(score_observation_listing({"want_count": None, "price": 1.0}))
        scored = score_observation_listing({"want_count": 100, "price": 1.0, "view_count": None})
        self.assertIsNotNone(scored)
        # Product path still coerces NULL want → 0 (054 contract)
        product_scored = score_product({"want_count": None, "price": 1.0})
        self.assertIsNotNone(product_scored)

    def test_d_reject_unverified(self) -> None:
        sig_ids = self._seed_full_group()
        _seed_signal(
            "sig_t075_bad",
            "demand_signal",
            "Excel模板",
            1.0,
            ["mobs_t075_a"],
            data_origin="REAL",
            verification_status="UNVERIFIED",
        )
        result = od.discover_opportunities_from_observation_signals(
            sig_ids + ["sig_t075_bad"], persist=False,
        )
        self.assertEqual(result["status"], "INSUFFICIENT_DATA")
        self.assertIn("verification", result["reason"])

    def test_e_no_ai_in_module(self) -> None:
        src = Path(od.__file__).read_text(encoding="utf-8")
        self.assertNotIn("ModelBridge", src)
        self.assertNotIn("ExecutionRuntime", src)
        self.assertNotIn("openai", src.lower())
        self.assertNotIn("deepseek", src.lower())

    def test_f_mapping_signal_to_opportunity(self) -> None:
        sig_ids = self._seed_full_group()
        result = od.discover_opportunities_from_observation_signals(sig_ids, persist=False)
        mapping = result["signal_opportunity_mapping"][0]
        self.assertEqual(mapping["grouping_key"], "keyword")
        self.assertEqual(len(mapping["signal_ids"]), 6)
        self.assertTrue(mapping["candidate_id"].startswith("aoc_"))


if __name__ == "__main__":
    unittest.main()
