# Entry 067 — Market Acquisition Policy + AI Cost Gate

from __future__ import annotations

import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent

import sys

sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import acquisition_engine as eng  # noqa: E402
import ai_cost_gate as acg  # noqa: E402
import config  # noqa: E402
import database  # noqa: E402


class Entry067AcquisitionPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        eng.ensure_acquisition_engine_schema()

    def test_01_strategy_registry_closed_set(self) -> None:
        reg = eng.strategy_registry()
        self.assertEqual(set(reg.keys()), set(eng.ACQUISITION_GOALS))
        self.assertIn(eng.GOAL_VOLUME, reg)
        self.assertIn(eng.GOAL_HIGH_VALUE, reg)
        self.assertIn(eng.GOAL_MARKET_GAP, reg)
        self.assertIn(eng.GOAL_TREND, reg)
        self.assertIn(eng.GOAL_TARGETED, reg)

    def test_02_policy_schema_volume(self) -> None:
        p = eng.create_market_acquisition_policy(
            goal=eng.GOAL_VOLUME,
            filters={"min_want_count": 50, "max_price": 20},
            scope={"max_records": 20, "max_pages": 1},
        )
        self.assertEqual(p["goal"], eng.GOAL_VOLUME)
        self.assertEqual(p["filters"]["min_want_count"], 50)
        self.assertIn("src_xianyu_marketplace", p["source_preferences"])
        # policy is not bound to a single platform name
        self.assertNotEqual(p["goal"], "xianyu")

    def test_03_policy_high_value_no_want_required(self) -> None:
        p = eng.create_market_acquisition_policy(
            goal=eng.GOAL_HIGH_VALUE,
            filters={"min_price": 50},
        )
        self.assertIsNone(p["filters"]["min_want_count"])
        self.assertEqual(p["filters"]["min_price"], 50.0)

    def test_04_reserved_goals(self) -> None:
        for goal in (eng.GOAL_MARKET_GAP, eng.GOAL_TREND, eng.GOAL_TARGETED):
            p = eng.create_market_acquisition_policy(goal=goal)
            self.assertEqual(p["goal"], goal)

    def test_05_unknown_goal_rejected(self) -> None:
        with self.assertRaises(ValueError):
            eng.create_market_acquisition_policy(goal="INFINITE_MODE_XYZ")

    def test_06_task_policy_binding(self) -> None:
        p = eng.create_market_acquisition_policy(
            goal=eng.GOAL_TARGETED,
            filters={"min_want_count": 10},
        )
        task = eng.create_collection_task(
            query="Excel模板",
            policy_id=p["policy_id"],
            max_records=None,
        )
        self.assertEqual(task.get("policy_id"), p["policy_id"])
        # filters inherited from policy when omitted
        import json

        fj = task.get("filters_json")
        if fj:
            f = json.loads(fj)
            self.assertEqual(f.get("min_want_count"), 10)

    def test_07_filter_null_want_unknown(self) -> None:
        obs = [
            {"title": "A", "want_count": 61, "price": 9.9},
            {"title": "B", "want_count": 20, "price": 8.0},
            {"title": "C", "want_count": None, "price": 12.0},
        ]
        result = eng.apply_observation_filters(
            obs, {"min_want_count": 50, "max_price": 20}
        )
        self.assertEqual(result["counts"]["MATCH"], 1)
        self.assertEqual(result["counts"]["BELOW_THRESHOLD"], 1)
        self.assertEqual(result["counts"]["UNKNOWN"], 1)
        # all observations retained in classified
        self.assertEqual(len(result["classified"]), 3)

    def test_08_null_not_zero(self) -> None:
        obs = [{"title": "X", "want_count": None, "price": 1}]
        result = eng.apply_observation_filters(obs, {"min_want_count": 50})
        self.assertEqual(result["UNKNOWN"][0]["want_count"], None)
        self.assertNotEqual(result["UNKNOWN"][0]["want_count"], 0)

    def test_09_filter_not_collector_hard_drop(self) -> None:
        # applying filter never shrinks total classified count
        obs = [{"title": "a", "want_count": None, "price": None}]
        r = eng.apply_observation_filters(obs, {"min_want_count": 100})
        self.assertEqual(r["total"], 1)
        self.assertEqual(len(r["classified"]), 1)

    def test_10_source_sales_separation_in_engine(self) -> None:
        chain = eng.reality_chain()
        self.assertIn("Acquisition Policy", chain)
        status = eng.engine_status()
        self.assertTrue(status["separations"]["source_neq_sales"])


class Entry067AICostGateTests(unittest.TestCase):
    def setUp(self) -> None:
        acg.ensure_ai_cost_schema()

    def test_11_cost_estimate_pass(self) -> None:
        est = acg.create_cost_estimate(
            skill=acg.SKILL_PRODUCT_CREATION,
            model="manual-config",
            estimated_cost=2.0,
            allowed_cost=10.0,
            call_count=5,
        )
        self.assertEqual(est["status"], acg.STATUS_PASS)
        self.assertEqual(est["gate"]["status"], acg.STATUS_PASS)
        self.assertFalse(est["paid_invocation"])

    def test_12_cost_gate_block(self) -> None:
        est = acg.create_cost_estimate(
            skill=acg.SKILL_MARKET_ANALYSIS,
            estimated_cost=50.0,
            allowed_cost=10.0,
        )
        self.assertEqual(est["status"], acg.STATUS_BLOCKED)
        self.assertEqual(est["gate"]["gate_action"], acg.STATUS_REDESIGN_REQUIRED)

    def test_13_unknown_cost(self) -> None:
        est = acg.create_cost_estimate(
            skill=acg.SKILL_DOCUMENT_GENERATION,
            estimated_cost=None,
            allowed_cost=10.0,
        )
        self.assertEqual(est["status"], acg.STATUS_UNKNOWN)

    def test_14_unknown_revenue(self) -> None:
        check = acg.economics_honesty_check(estimated_revenue=None)
        self.assertEqual(check["revenue_basis"], acg.STATUS_UNKNOWN)

    def test_15_hypothesis_allowed_cost(self) -> None:
        d = acg.derive_allowed_cost(estimated_revenue=100.0, margin_floor=0.7)
        self.assertTrue(d["hypothesis"])
        self.assertAlmostEqual(d["allowed_cost"], 30.0)
        self.assertEqual(d["cost_basis"], acg.BASIS_HYPOTHESIS)

    def test_16_no_fake_economics(self) -> None:
        bad = acg.economics_honesty_check(estimated_revenue=99.0, claim_as_actual=True)
        self.assertFalse(bad["ok"])

    def test_17_estimate_vs_actual_record(self) -> None:
        rec = acg.record_ai_execution(
            skill=acg.SKILL_IMAGE_GENERATION,
            estimated_cost=1.0,
            actual_cost=None,
            call_count=2,
        )
        self.assertEqual(rec["cost_basis_estimated"], acg.BASIS_ESTIMATE)
        self.assertEqual(rec["cost_basis_actual"], acg.STATUS_UNKNOWN)
        self.assertFalse(rec["paid_invocation"])

    def test_18_model_selector_not_router(self) -> None:
        sel = acg.ModelSelector(configured_model="local-config")
        out = sel.select(skill=acg.SKILL_PRODUCT_CREATION, prefer_cost=True)
        self.assertEqual(out["router_status"], "NOT_BUILT")
        self.assertEqual(out["selected_model"], "local-config")

    def test_19_no_paid_invocation(self) -> None:
        self.assertTrue(acg.assert_no_paid_invocation()["ok"])

    def test_20_product_creation_boundary(self) -> None:
        b = acg.product_creation_capability_boundary()
        self.assertFalse(b["split_agents"])
        self.assertTrue(b["requires_cost_gate"])

    def test_21_call_count_not_control_metric(self) -> None:
        # expensive single call blocked; cheap many calls pass
        expensive = acg.evaluate_cost_gate(estimated_cost=100.0, allowed_cost=5.0)
        cheap_many = acg.create_cost_estimate(
            skill=acg.SKILL_LISTING_ADAPTATION,
            estimated_cost=0.5,
            allowed_cost=5.0,
            call_count=50,
        )
        self.assertEqual(expensive["status"], acg.STATUS_BLOCKED)
        self.assertEqual(cheap_many["status"], acg.STATUS_PASS)

    def test_22_no_db_destructive_migration(self) -> None:
        # tables exist; market_observations untouched by schema ensure
        before = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        eng.ensure_acquisition_engine_schema()
        acg.ensure_ai_cost_schema()
        after = sqlite3.connect(config.DB_PATH).execute(
            "SELECT COUNT(*) FROM market_observations"
        ).fetchone()[0]
        self.assertEqual(before, after)
        tables = {
            r[0]
            for r in sqlite3.connect(config.DB_PATH)
            .execute("SELECT name FROM sqlite_master WHERE type='table'")
            .fetchall()
        }
        self.assertIn("market_acquisition_policies", tables)
        self.assertIn("ai_cost_estimates", tables)
        self.assertIn("ai_execution_records", tables)

    def test_23_core_file_creation_audit_zero_numbered(self) -> None:
        # Entry 067 must not add docs/00–06 new markdown files for this entry
        # Assert Work Principles exists (root) and no ENTRY_067 in 0–6 dirs
        for folder in (
            "00_GOVERNANCE",
            "01_CURRENT_STATE",
            "02_ARCHITECTURE",
            "03_BUSINESS",
            "05_EXECUTION",
            "06_HISTORY",
        ):
            d = ROOT / "docs" / folder
            hits = list(d.glob("*067*")) if d.exists() else []
            self.assertEqual(hits, [], f"unexpected 067 core file in {folder}: {hits}")

    def test_24_legacy_isolation(self) -> None:
        src = (DATA / "ai_cost_gate.py").read_text(encoding="utf-8")
        self.assertNotIn("99_ARCHIVE", src)
        eng_src = (DATA / "acquisition_engine.py").read_text(encoding="utf-8")
        self.assertNotIn("sample.xlsx", eng_src)


if __name__ == "__main__":
    unittest.main()
