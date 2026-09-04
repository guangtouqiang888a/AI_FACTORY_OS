# 6_EXECUTION/test_opportunity_to_product_076.py — Entry 076 tests

from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "6_EXECUTION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402
import market_signal_core as msc  # noqa: E402
import market_source_core as msrc  # noqa: E402
import opportunity_to_product_076 as otp  # noqa: E402


def _seed_obs(oid: str, want_count, *, view_count=None, price=1.0) -> None:
    notes = json.dumps({"query": "Excel模板", "session_id": "sess_t076"}, ensure_ascii=False)
    ok, reason = msrc.insert_market_observation({
        "observation_id": oid,
        "run_id": "crun_t076",
        "source_id": "src_xianyu",
        "source": "xianyu",
        "platform": "xianyu",
        "source_type": "marketplace",
        "source_item_id": f"item_{oid[-4:]}",
        "source_url": f"https://example/{oid}",
        "title": f"third party listing {oid}",
        "price": price,
        "want_count": want_count,
        "view_count": view_count,
        "observed_at": "2026-09-03T15:20:02+08:00",
        "data_origin": "REAL",
        "verification_status": "MANUAL_VERIFIED",
        "dedupe_key": f"dk_{oid}",
        "notes": notes,
        "raw_reference": "tests/076",
    })
    if not ok:
        raise RuntimeError(reason)


def _seed_signal(sid: str, stype: str, obs_ids: list[str], value) -> None:
    msc.persist_signals([{
        "signal_id": sid,
        "signal_type": stype,
        "keyword": "Excel模板",
        "platform": "xianyu",
        "source": "market_observation",
        "value": value,
        "value_status": "COMPUTED" if value is not None else "UNAVAILABLE",
        "unit": "t",
        "evidence_refs": {
            "lineage": msc.LINEAGE_OBSERVATION,
            "observation_ids": obs_ids,
            "source_item_ids": [f"item_{x[-4:]}" for x in obs_ids],
            "collection_run_ids": ["crun_t076"],
            "session_ids": ["sess_t076"],
            "extension_run_ids": ["run_t076"],
            "data_origins": ["REAL"],
            "verification_statuses": ["MANUAL_VERIFIED"],
            "product_ids": [],
        },
        "observation_timestamp": "2026-09-03T15:20:02+08:00",
        "computed_at": "2026-09-03 15:20:02",
        "product_type": "digital_template",
        "notes": "test",
    }])


class OpportunityToProduct076Tests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "t076.db"
        self.discovery = base / "observation_discovery_v1.json"
        self.store = base / "product_definitions_v1.json"
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
        ]
        for p in self._patches:
            p.start()
        database.ensure_schema()
        msrc.ensure_market_source_schema()
        msc.ensure_market_signal_schema()
        self.obs_ids = ["mobs_t076_a", "mobs_t076_b"]
        self.sig_ids = [
            "sig_t076_d", "sig_t076_e", "sig_t076_c",
            "sig_t076_p", "sig_t076_t", "sig_t076_g",
        ]
        for i, oid in enumerate(self.obs_ids):
            _seed_obs(oid, 100 + i * 10, view_count=None)
        types = [
            "demand_signal", "engagement_signal", "competition_signal",
            "price_signal", "trend_signal", "growth_signal",
        ]
        vals = [210.0, 0.0, 2.0, 1.0, 105.0, None]
        for sid, st, v in zip(self.sig_ids, types, vals):
            _seed_signal(sid, st, self.obs_ids, v)
        self.candidate_id = "aoc_t076_test"
        cand = {
            "candidate_id": self.candidate_id,
            "opportunity_id": None,
            "keyword": "Excel模板",
            "source": "market_observation",
            "platform": "xianyu",
            "lineage": "market_observation",
            "product_type": "digital_template",
            "score": {"total_score": 68.92},
            "provenance": {
                "lineage": "market_observation",
                "signal_ids": self.sig_ids,
                "observation_ids": self.obs_ids,
                "source_item_ids": [f"item_{x[-4:]}" for x in self.obs_ids],
                "collection_run_ids": ["crun_t076"],
                "session_ids": ["sess_t076"],
                "extension_run_ids": ["run_t076"],
                "data_origins": ["REAL"],
                "verification_statuses": ["MANUAL_VERIFIED"],
            },
            "status": "discovered_candidate",
            "auto_production_forbidden": True,
        }
        sel = {
            "selection_id": "sel_t076",
            "candidate_id": self.candidate_id,
            "selected": True,
            "rank": 1,
            "score": 68.92,
            "discovery_method": "observation_market_signal",
        }
        self.discovery.write_text(
            json.dumps({"candidates": [cand], "selection_results": [sel]}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _count(self, table: str) -> int:
        with sqlite3.connect(config.DB_PATH) as con:
            return con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    def test_1_opportunity_enters_product(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=True,
            discovery_path=self.discovery, store_path=self.store,
        )
        self.assertEqual(r["status"], "OK")
        self.assertTrue(r["product_id"].startswith("prod_"))
        self.assertEqual(r["product"]["source_opportunity_id"], self.candidate_id)

    def test_2_provenance_to_signals(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=False,
            discovery_path=self.discovery, store_path=self.store,
        )
        for sid in self.sig_ids:
            self.assertIn(sid, r["product"]["source_signal_ids"])
            self.assertIn(sid, r["product"]["provenance"]["signal_ids"])

    def test_3_provenance_to_observations(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=False,
            discovery_path=self.discovery, store_path=self.store,
        )
        for oid in self.obs_ids:
            self.assertIn(oid, r["product"]["source_observation_ids"])

    def test_4_real_manual_verified(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=False,
            discovery_path=self.discovery, store_path=self.store,
        )
        self.assertEqual(r["product"]["provenance"]["data_origins"], ["REAL"])
        self.assertEqual(r["product"]["provenance"]["verification_statuses"], ["MANUAL_VERIFIED"])

    def test_5_no_sqlite_products_write(self) -> None:
        before = self._count("products")
        otp.productize_opportunity(
            self.candidate_id, persist=True,
            discovery_path=self.discovery, store_path=self.store,
        )
        self.assertEqual(self._count("products"), before)
        self.assertEqual(before, 0)

    def test_6_observations_signals_unchanged(self) -> None:
        obs_b = self._count("market_observations")
        sig_b = self._count("market_signals")
        otp.productize_opportunity(
            self.candidate_id, persist=True,
            discovery_path=self.discovery, store_path=self.store,
        )
        self.assertEqual(self._count("market_observations"), obs_b)
        self.assertEqual(self._count("market_signals"), sig_b)

    def test_7_null_view_preserved(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=False,
            discovery_path=self.discovery, store_path=self.store,
        )
        metrics = r["product"]["product_definition"]["observed_marketplace_evidence"]["value"]
        for m in metrics:
            self.assertIsNone(m["view_count"])

    def test_8_unknown_not_fact(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=False,
            discovery_path=self.discovery, store_path=self.store,
        )
        pd = r["product"]["product_definition"]
        self.assertEqual(pd["specific_template_subtype"]["classification"], "UNKNOWN")
        self.assertIsNone(pd["specific_template_subtype"]["value"])
        self.assertEqual(pd["marketing_title"]["classification"], "UNKNOWN")
        self.assertIn("UNKNOWN", r["product"]["evidence_classification"])

    def test_9_no_ai(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=False,
            discovery_path=self.discovery, store_path=self.store,
        )
        self.assertEqual(r["ai_provider_calls"], 0)
        self.assertFalse(r["ai_invoked"])
        src = Path(otp.__file__).read_text(encoding="utf-8")
        self.assertNotIn("ModelBridge", src)
        self.assertNotIn("openai", src.lower())
        self.assertNotIn("deepseek", src.lower())

    def test_10_boundaries(self) -> None:
        r = otp.productize_opportunity(
            self.candidate_id, persist=True,
            discovery_path=self.discovery, store_path=self.store,
        )
        self.assertEqual(r["publish"], "NOT_EXECUTED")
        self.assertEqual(r["external_action"], "NONE")
        self.assertEqual(r["commercial_learning"], "NOT_EXECUTED")
        self.assertEqual(r["product"]["product_status"], "draft")
        self.assertTrue(r["product"]["publish_forbidden"])
        self.assertTrue(r["product"]["e2e_055_forbidden"])
        self.assertNotEqual(r["product_id"], self.candidate_id)

    def test_11_idempotent_soft_reuse(self) -> None:
        r1 = otp.productize_opportunity(
            self.candidate_id, persist=True,
            discovery_path=self.discovery, store_path=self.store,
        )
        r2 = otp.productize_opportunity(
            self.candidate_id, persist=True,
            discovery_path=self.discovery, store_path=self.store,
        )
        self.assertTrue(r2["idempotent_reuse"])
        self.assertEqual(r1["product_id"], r2["product_id"])


if __name__ == "__main__":
    unittest.main()
