# 0_START/controller.py — 工业级四层 Controller

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for layer in ("8_CONFIG", "7_MEMORY", "1_DATA", "0_START"):
    p = str(ROOT / layer)
    if p not in sys.path:
        sys.path.insert(0, p)

import config  # noqa: E402
import memory_core  # noqa: E402
import database  # noqa: E402
from planner import Planner  # noqa: E402
from policy_engine import PolicyEngine  # noqa: E402
from execution_runtime import ExecutionRuntime  # noqa: E402
from self_evolution import SelfEvolutionEngine  # noqa: E402


class SystemController:
    """Planner → PolicyEngine → ExecutionRuntime → Memory"""

    def __init__(self):
        self.planner = Planner()
        self.policy = PolicyEngine()
        self.runtime = ExecutionRuntime()
        self.evolution = SelfEvolutionEngine()
        self.last_run: dict | None = None

    def boot(self) -> dict:
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        database.ensure_schema()
        init = memory_core.init_memory()
        self.policy.reset_session_cost()

        memory_core.write_event({
            "type": "boot",
            "version": config.SYSTEM_VERSION,
            "layers": list(config.OS_LAYERS),
            "policy_core_lock": config.POLICY_CORE_LOCK,
            "deterministic_mode": config.DETERMINISTIC_MODE,
            "agents": self.runtime.registry.list_agents(),
        })

        return {
            "status": "ok",
            "version": config.SYSTEM_VERSION,
            "layers": list(config.OS_LAYERS),
            "pattern_count": init.get("pattern_count", 0),
            "strategy_rules": init.get("strategy_rules", 0),
            "agents": self.runtime.registry.list_agents(),
            "policy": self.policy.rules,
            "policy_core_lock": config.POLICY_CORE_LOCK,
            "deterministic_mode": config.DETERMINISTIC_MODE,
        }

    def run(self, task: str = "虚拟资料") -> dict:
        evo = self.evolution.evolve(self.policy)

        plan = self.planner.plan({"task": task, "data": {}, "meta": {}})
        pipeline_policy = self.policy.evaluate_pipeline(plan)
        if not pipeline_policy.get("approved"):
            raise PermissionError(pipeline_policy.get("reason", "pipeline blocked"))

        dag = self.policy.apply_dag_policies(plan["dag"], plan["complexity"])
        dag["task"] = task

        memory_core.write_event({
            "type": "dag_ready",
            "task": task,
            "complexity": plan["complexity"],
            "pipeline_policy": pipeline_policy,
            "evolution": evo,
        })

        ctx = self.runtime.execute_dag(dag, plan["complexity"], self.policy)

        pattern = memory_core.extract_pattern(ctx)
        strategy = memory_core.update_strategy(pattern)

        memory_core.write_event({
            "type": "pipeline_complete",
            "task": task,
            "pattern": pattern,
            "evolution": evo,
            "session_cost": self.policy.session_cost,
        })

        nodes = ctx.get("nodes", {})
        decision_r = nodes.get("decision", {}).get("result", {})
        execution_r = nodes.get("execution", {}).get("result", {})
        scoring_r = nodes.get("scoring", {}).get("result", {})
        data_r = nodes.get("data", {}).get("result", {})

        result = {
            "task": task,
            "version": config.SYSTEM_VERSION,
            "layers": list(config.OS_LAYERS),
            "plan": plan,
            "pipeline_policy": pipeline_policy,
            "dag": dag,
            "node_results": {
                nid: {
                    "status": n.get("status"),
                    "executor": n.get("executor"),
                    "policy": n.get("policy"),
                    "score": n.get("score"),
                }
                for nid, n in nodes.items()
            },
            "data": data_r.get("data_result", data_r),
            "scoring": {"count": scoring_r.get("count", 0), "score": nodes.get("scoring", {}).get("score")},
            "decision": {"action": decision_r.get("action"), "reason": decision_r.get("reason"), "score": nodes.get("decision", {}).get("score")},
            "execution": execution_r,
            "final_action": decision_r.get("action", "skip") if decision_r else "skip",
            "memory": {
                "pattern": pattern,
                "strategy_rules": len(strategy.get("rules", [])),
                "strategy_skipped": strategy.get("skipped", False),
                "pattern_confidence": pattern.get("confidence"),
            },
            "execution_hashes": {
                nid: n.get("execution_hash") for nid, n in nodes.items()
            },
            "evolution": evo,
            "session_cost": self.policy.session_cost,
            "finished_at": ctx.get("finished_at"),
        }
        self.last_run = result
        return result
