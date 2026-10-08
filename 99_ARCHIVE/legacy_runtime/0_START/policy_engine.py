# 0_START/policy_engine.py — Policy Engine（Production Grade 加固）

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "7_MEMORY"))

import config  # noqa: E402
import memory_core  # noqa: E402


class PolicyEngine:
    """
    统一决策层。policy_core_lock=True 时 immutable_rules 不可被 evolution 修改。
    输出: { executor, approved, mode }
    """

    policy_core_lock = True
    RULE_AGENTS = ("DataAgent", "ExecutionAgent")

    def __init__(self):
        self.rules = self._load_locked_policy()
        self.session_cost = float(self.rules.get("session_llm_cost", 0.0))

    def reload(self) -> None:
        self.rules = self._load_locked_policy()
        self.session_cost = float(self.rules.get("session_llm_cost", 0.0))

    @classmethod
    def _immutable_rules(cls) -> dict:
        return {
            "policy_core_lock": config.POLICY_CORE_LOCK,
            "llm_routing": config.LLM_ROUTING.copy(),
            "executor_allowlist": list(config.EXECUTOR_ALLOWLIST),
            "llm_cost_budget": config.LLM_COST_BUDGET_CEILING,
        }

    @classmethod
    def _load_locked_policy(cls) -> dict:
        policy = memory_core.load_runtime_policy()
        return cls.enforce_immutable(policy)

    @classmethod
    def enforce_immutable(cls, policy: dict) -> dict:
        """强制注入 immutable_rules，Self-Evolution 无法覆盖。"""
        merged = config.DEFAULT_RUNTIME_POLICY.copy()
        merged.update(policy)
        merged.update(cls._immutable_rules())
        return merged

    def evaluate_pipeline(self, plan: dict) -> dict:
        mode = self.rules.get("mode", "balanced")
        return {
            "executor": "rule",
            "approved": True,
            "mode": mode,
            "reason": "pipeline approved",
        }

    def evaluate_node(self, node: dict, complexity: str) -> dict:
        agent = node.get("agent", "")
        mode = self.rules.get("mode", "balanced")

        if agent in self.RULE_AGENTS:
            return {"executor": "rule", "approved": True, "mode": self._mode_label(mode)}

        tier = config.COMPLEXITY_MAP.get(complexity, "medium")
        canonical = config.LLM_ROUTING.get(tier, "rule")

        if mode == "fast":
            canonical = "rule"
        elif mode == "accurate" and tier != "simple":
            canonical = "gpt"

        executor = self._normalize_executor(canonical)
        approved, reason = self._check_executor(executor)
        if not approved:
            executor = "rule"

        return {
            "executor": executor,
            "approved": approved or executor == "rule",
            "mode": self._mode_label(mode),
            "tier": tier,
            "note": reason,
        }

    def apply_dag_policies(self, dag: dict, complexity: str) -> dict:
        nodes = []
        for node in dag.get("nodes", []):
            policy = self.evaluate_node(node, complexity)
            nodes.append({**node, "policy": policy})
        return {**dag, "nodes": nodes}

    def apply_patch(self, patch: dict) -> dict:
        """仅允许 mode / threshold / weights；immutable 字段拒绝。"""
        applied = {}
        for key, val in patch.items():
            if key in config.IMMUTABLE_POLICY_KEYS:
                continue
            if key not in config.EVOLUTION_ALLOWED_KEYS:
                continue
            if key == "threshold" and isinstance(val, (int, float)):
                current = float(self.rules.get("threshold", config.PUBLISH_SCORE_THRESHOLD))
                max_delta = max(1.0, current * config.MAX_CHANGE_RATE)
                val = max(current - max_delta, min(current + max_delta, float(val)))
            if key == "weights" and isinstance(val, dict):
                val = self._clamp_weights(val)
            self.rules[key] = val
            applied[key] = val
        if applied:
            self.rules = self.enforce_immutable(self.rules)
            self.rules["session_llm_cost"] = self.session_cost
            memory_core.save_runtime_policy(self.rules)
        return applied

    def check_budget(self, executor: str) -> bool:
        est = config.LLM_COST_ESTIMATE.get(executor, 0.01)
        budget = config.LLM_COST_BUDGET_CEILING
        return self.session_cost + est <= budget

    def consume_cost(self, executor: str) -> None:
        self.session_cost += config.LLM_COST_ESTIMATE.get(executor, 0.0)
        self.rules["session_llm_cost"] = round(self.session_cost, 6)
        memory_core.save_runtime_policy(self.enforce_immutable(self.rules))

    def reset_session_cost(self) -> None:
        self.session_cost = 0.0
        self.rules["session_llm_cost"] = 0.0
        memory_core.save_runtime_policy(self.enforce_immutable(self.rules))

    def _normalize_executor(self, executor: str) -> str:
        if executor in ("gpt-4.1-mini", "gpt-4.1", "gpt-4o"):
            return "gpt"
        return executor

    def _check_executor(self, executor: str) -> tuple[bool, str]:
        allowlist = self.rules.get("executor_allowlist", list(config.EXECUTOR_ALLOWLIST))
        if executor == "rule":
            return True, "rule engine"
        if executor not in allowlist:
            return False, f"{executor} not in allowlist"
        if not self.check_budget(executor):
            return False, "cost budget exceeded (immutable ceiling)"
        return True, "approved"

    @staticmethod
    def _clamp_weights(weights: dict) -> dict:
        base = config.SCORE_WEIGHTS.copy()
        merged = {**base, **{k: v for k, v in weights.items() if k in base}}
        total = sum(merged.values()) or 1.0
        return {k: round(v / total, 4) for k, v in merged.items()}

    @staticmethod
    def _mode_label(mode: str) -> str:
        return mode if mode in ("fast", "balanced", "accurate") else "balanced"
