# 0_START/self_evolution.py — Self-Evolution（Production Grade 护栏）

# Entry 050 — 仅消费 Execution Learning；不得将 published_local 当作 Real Commercial Learning



import sys

from pathlib import Path



ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "7_MEMORY"))

sys.path.insert(0, str(ROOT / "8_CONFIG"))



import config  # noqa: E402

import memory_core  # noqa: E402





class SelfEvolutionEngine:

    """

    只能修改 mode / threshold / weights，immutable policy 禁止触碰。



    Entry 050：

    - 本引擎驱动的是 Execution Strategy（Track A 发布策略），不是 Commercial Strategy。

    - get_pattern_stats 默认仅统计 learning_lane=EXECUTION（含 simulation 执行层）。

    - 不得将 stats 解释为 Real Commercial Learning。

    """



    STRATEGY_DOMAIN = "EXECUTION"



    def evolve(self, policy_engine: object) -> dict:

        rules = memory_core.load_runtime_policy()

        cooldown = int(rules.get("cooldown_remaining", 0))

        if cooldown > 0:

            rules["cooldown_remaining"] = cooldown - 1

            memory_core.save_runtime_policy(policy_engine.enforce_immutable(rules))

            policy_engine.reload()

            return {

                "updated": False,

                "reason": f"cooldown {cooldown - 1}",

                "strategy_domain": self.STRATEGY_DOMAIN,

            }



        # 明确：仅 Execution Learning 统计

        stats = memory_core.get_pattern_stats(

            learning_lane=memory_core.LEARNING_LANE_EXECUTION,

        )



        if stats.get("fail_rate", 0) > config.ROLLBACK_FAILURE_RATE:

            rolled = memory_core.rollback_policy_snapshot()

            policy_engine.reload()

            patch = {"mode": "balanced"}

            memory_core.save_policy_patch(patch, source="rollback_execution")

            return {

                "updated": False,

                "rolled_back": True,

                "patch": patch,

                "stats": stats,

                "strategy_domain": self.STRATEGY_DOMAIN,

                "commercial_learning": False,

            }



        patch = self._build_patch(stats)

        ok, safe_patch, violations = self.evolution_guardrail_check(patch)

        if not ok or not safe_patch:

            return {

                "updated": False,

                "reason": "guardrail blocked",

                "violations": violations,

                "strategy_domain": self.STRATEGY_DOMAIN,

            }



        memory_core.save_policy_snapshot()

        memory_core.save_policy_patch(safe_patch, source="self_evolution_execution")

        applied = policy_engine.apply_patch(safe_patch)



        rules = memory_core.load_runtime_policy()

        rules["cooldown_remaining"] = config.COOLDOWN_STEPS

        rules["evolution_step"] = int(rules.get("evolution_step", 0)) + 1

        rules["last_evolution_strategy_domain"] = self.STRATEGY_DOMAIN

        memory_core.save_runtime_policy(policy_engine.enforce_immutable(rules))

        policy_engine.reload()



        memory_core.write_event({

            "type": "self_evolution",

            "strategy_domain": self.STRATEGY_DOMAIN,

            "commercial_learning": False,

            "note": "Execution Policy Learning only; not Real Commercial Learning",

            "patch": safe_patch,

            "applied": applied,

            "stats": stats,

            "guardrail": "passed",

        })

        return {

            "updated": True,

            "patch": safe_patch,

            "applied": applied,

            "stats": stats,

            "strategy_domain": self.STRATEGY_DOMAIN,

            "commercial_learning": False,

        }



    @staticmethod

    def evolution_guardrail_check(patch: dict) -> tuple[bool, dict, list[str]]:

        """禁止修改 immutable policy，只允许 mode/threshold/weights。"""

        violations = []

        safe = {}

        for key, val in patch.items():

            if key in config.IMMUTABLE_POLICY_KEYS:

                violations.append(f"immutable key blocked: {key}")

                continue

            if key not in config.EVOLUTION_ALLOWED_KEYS:

                violations.append(f"key not allowed: {key}")

                continue

            safe[key] = val

        if violations and not safe:

            return False, {}, violations

        return True, safe, violations



    @staticmethod

    def _build_patch(stats: dict) -> dict:

        if stats.get("total", 0) < 5:

            return {"mode": "balanced"}



        # success_rate 此处 = Execution Learning success（含 published_local）

        # ≠ Commercial Success

        if stats.get("success_rate", 0) > 0.7:

            return {"mode": "fast", "threshold": config.PUBLISH_SCORE_THRESHOLD}



        if stats.get("fail_rate", 0) > 0.3:

            return {

                "mode": "accurate",

                "threshold": max(config.PUBLISH_SCORE_THRESHOLD - 5, 30),

                "weights": {**config.SCORE_WEIGHTS, "hot": 0.35, "profit": 0.18},

            }



        return {"mode": "balanced"}


