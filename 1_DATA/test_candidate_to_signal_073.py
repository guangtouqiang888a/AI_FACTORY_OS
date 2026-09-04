# 1_DATA/test_candidate_to_signal_073.py — Entry 073 Candidate → Signal

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "1_DATA"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import config  # noqa: E402
import database  # noqa: E402
import market_signal_core as msc  # noqa: E402
import market_source_core as msrc  # noqa: E402


LOCKED_IDS = list(msc.ENTRY_070_LOCKED_MATCH_IDS)


def _seed_observation(
    *,
    observation_id: str,
    want_count,
    price=1.0,
    view_count=None,
    query="Excel模板",
    session_id="sess_test_073",
    run_id="crun_test_073",
    source_item_id="item_1",
    data_origin="REAL",
    verification_status="MANUAL_VERIFIED",
) -> dict:
    notes = json.dumps(
        {
            "result_origin": "SEARCH_RESULT",
            "want_count_status": "VISIBLE_ON_CARD" if want_count is not None else "MISSING_ON_CARD",
            "query": query,
            "session_id": session_id,
            "entry_import": "066.1.0",
        },
        ensure_ascii=False,
    )
    row = {
        "observation_id": observation_id,
        "run_id": run_id,
        "source_id": "src_xianyu",
        "source": "xianyu",
        "platform": "xianyu",
        "source_type": "marketplace",
        "source_item_id": source_item_id,
        "source_url": f"https://www.goofish.com/item?id={source_item_id}",
        "title": f"test title {observation_id}",
        "price": price,
        "currency": "CNY",
        "want_count": want_count,
        "view_count": view_count,
        "comment_count": None,
        "share_count": None,
        "observed_at": "2026-09-03T15:20:02+08:00",
        "data_origin": data_origin,
        "verification_status": verification_status,
        "dedupe_key": f"dedupe_{observation_id}",
        "notes": notes,
        "raw_reference": "tests/entry_073",
    }
    ok, reason = msrc.insert_market_observation(row)
    if not ok:
        raise RuntimeError(f"seed failed: {reason}")
    return row


class CandidateToSignal073Tests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_073.db"
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
        ]
        for p in self._patches:
            p.start()
        database.ensure_schema()
        msrc.ensure_market_source_schema()
        msc.ensure_market_signal_schema()
        self._ai_calls = {"execution_runtime": 0, "model_bridge": 0, "openai": 0, "deepseek": 0}

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _count(self, table: str) -> int:
        with database.get_connection() as conn:
            return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    def test_a_real_candidate_input_produces_signals(self) -> None:
        ids = LOCKED_IDS[:3]
        for i, oid in enumerate(ids):
            _seed_observation(
                observation_id=oid,
                want_count=100 + i * 10,
                source_item_id=f"item_{i}",
            )
        candidates = [
            {
                "observation_id": oid,
                "filter_status": "MATCH",
                "extension_run_id": "run_test_073",
                "session_id": "sess_test_073",
                "collection_run_id": "crun_test_073",
            }
            for oid in ids
        ]
        products_before = self._count("products")
        result = msc.derive_signals_from_observation_candidates(candidates)
        self.assertEqual(result["status"], "OK")
        self.assertGreater(result["signal_count"], 0)
        self.assertEqual(result["accepted_count"], 3)
        self.assertFalse(result["product_substitution"])
        self.assertFalse(result["ai_invoked"])
        persisted = msc.persist_signals(result["signals"])
        self.assertEqual(persisted, result["signal_count"])
        self.assertEqual(self._count("products"), products_before)
        self.assertEqual(self._count("market_signals"), result["signal_count"])
        # one keyword group → 6 signal types
        types = {s["signal_type"] for s in result["signals"]}
        self.assertIn("demand_signal", types)
        self.assertEqual(result["keyword_groups"].get("Excel模板"), 3)

    def test_b_provenance_traceable(self) -> None:
        oid = LOCKED_IDS[0]
        _seed_observation(observation_id=oid, want_count=500, source_item_id="805580867741")
        candidates = [{
            "observation_id": oid,
            "filter_status": "MATCH",
            "extension_run_id": "run_1788419997563",
            "session_id": "sess_1788419997563",
            "collection_run_id": "crun_test_073",
        }]
        result = msc.derive_signals_from_observation_candidates(candidates)
        self.assertEqual(result["status"], "OK")
        ev = result["signals"][0]["evidence_refs"]
        self.assertEqual(ev["lineage"], msc.LINEAGE_OBSERVATION)
        self.assertIn(oid, ev["observation_ids"])
        self.assertIn("805580867741", ev["source_item_ids"])
        self.assertIn("crun_test_073", ev["collection_run_ids"])
        self.assertIn("sess_1788419997563", ev["session_ids"])
        self.assertIn("run_1788419997563", ev["extension_run_ids"])
        self.assertIn("REAL", ev["data_origins"])
        self.assertIn("MANUAL_VERIFIED", ev["verification_statuses"])
        self.assertEqual(ev["product_ids"], [])
        mapping = result["candidate_signal_mapping"]
        self.assertEqual(mapping[0]["observation_id"], oid)
        self.assertTrue(mapping[0]["signal_ids"])

    def test_c_null_want_not_coerced_to_zero(self) -> None:
        # Known want + NULL want in same group
        _seed_observation(observation_id="mobs_null_a", want_count=100, source_item_id="a")
        _seed_observation(observation_id="mobs_null_b", want_count=None, source_item_id="b")
        candidates = [
            {"observation_id": "mobs_null_a", "filter_status": "MATCH"},
            {"observation_id": "mobs_null_b", "filter_status": "MATCH"},
        ]
        # Temporarily allow MATCH without re-check of want — filter_status provided
        result = msc.derive_signals_from_observation_candidates(candidates)
        demand = next(s for s in result["signals"] if s["signal_type"] == "demand_signal")
        # NULL must not become 0 contribution → total_want = 100 not 100+0
        self.assertEqual(demand["value"], 100)
        ev = demand["evidence_refs"]
        self.assertIn("mobs_null_b", ev["null_want_count_observation_ids"])
        rows = msc.load_observations_by_ids(["mobs_null_b"])
        listing = msc.observation_to_listing_input(rows[0])
        self.assertIsNone(listing["want_count"])

    def test_d_no_product_substitution(self) -> None:
        oid = LOCKED_IDS[1]
        _seed_observation(observation_id=oid, want_count=200)
        before = self._count("products")
        result = msc.derive_signals_from_observation_candidates(
            [{"observation_id": oid, "filter_status": "MATCH"}]
        )
        msc.persist_signals(result["signals"])
        self.assertEqual(self._count("products"), before)
        self.assertEqual(before, 0)
        self.assertFalse(result["product_substitution"])
        for s in result["signals"]:
            self.assertEqual(s["evidence_refs"].get("product_ids"), [])
            self.assertEqual(s["source"], "market_observation")

    def test_e_deterministic_same_input(self) -> None:
        oid = LOCKED_IDS[2]
        _seed_observation(observation_id=oid, want_count=660, price=1.0)
        cand = [{"observation_id": oid, "filter_status": "MATCH"}]
        r1 = msc.derive_signals_from_observation_candidates(cand)
        r2 = msc.derive_signals_from_observation_candidates(cand)
        # signal_ids differ (uuid) but values/types/keyword must match
        v1 = {(s["signal_type"], s["value"], s["unit"], s["keyword"]) for s in r1["signals"]}
        v2 = {(s["signal_type"], s["value"], s["unit"], s["keyword"]) for s in r2["signals"]}
        self.assertEqual(v1, v2)

    def test_f_no_ai_flags(self) -> None:
        oid = LOCKED_IDS[3]
        _seed_observation(observation_id=oid, want_count=1930)
        result = msc.derive_signals_from_observation_candidates(
            [{"observation_id": oid, "filter_status": "MATCH"}]
        )
        self.assertFalse(result["ai_invoked"])
        # Path must not import/call ModelBridge / ExecutionRuntime
        import market_signal_core as core_mod
        src = Path(core_mod.__file__).read_text(encoding="utf-8")
        self.assertNotIn("ModelBridge", src)
        self.assertNotIn("ExecutionRuntime", src)
        self.assertNotIn("openai", src.lower().replace("openaitest", ""))
        self.assertNotIn("deepseek", src.lower())
        self.assertNotIn("requests.", src)
        self.assertEqual(self._ai_calls["execution_runtime"], 0)
        self.assertEqual(self._ai_calls["model_bridge"], 0)

    def test_reject_non_match_and_unverified(self) -> None:
        _seed_observation(observation_id="mobs_rej_1", want_count=10)
        _seed_observation(
            observation_id="mobs_rej_2",
            want_count=100,
            verification_status="UNVERIFIED",
        )
        result = msc.derive_signals_from_observation_candidates(
            [
                {"observation_id": "mobs_rej_1", "filter_status": "BELOW_THRESHOLD"},
                {"observation_id": "mobs_rej_2", "filter_status": "MATCH"},
            ]
        )
        self.assertEqual(result["status"], "NO_SIGNALS")
        reasons = {s["reason"] for s in result["skipped"]}
        self.assertIn("filter_status_not_MATCH", reasons)
        self.assertIn("verification_not_MANUAL_VERIFIED", reasons)


if __name__ == "__main__":
    unittest.main()
