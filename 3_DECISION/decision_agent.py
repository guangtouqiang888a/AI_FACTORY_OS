# 3_DECISION/decision_agent.py — DecisionAgent（标准化接口）

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for layer in ("3_DECISION", "0_START", "8_CONFIG", "7_MEMORY"):
    p = str(ROOT / layer)
    if p not in sys.path:
        sys.path.insert(0, p)

from decision_engine import decide_scored  # noqa: E402
from agent_runtime import BaseAgent  # noqa: E402
from os_protocol import make_output  # noqa: E402
import memory_core  # noqa: E402


class DecisionAgent(BaseAgent):
    role = "decision_maker"
    tools = ["decide_scored", "assess_risk", "strategy_memory"]
    memory_scope = "3_DECISION"

    def execute(self, input_data: dict, context: dict) -> dict:
        task = input_data["task"]
        keyword = input_data["data"].get("keyword", task)
        products = input_data["data"].get("products", [])
        strategies = memory_core.load_strategy_memory()
        decision = decide_scored(keyword, products, strategies)
        best_score = (decision.get("best") or {}).get("scores", {}).get("total")
        status = "ok" if decision.get("action") != "skip" or products else "skip"
        return make_output(
            status,
            decision,
            score=best_score,
            logs=[f"action={decision.get('action')}, reason={decision.get('reason', '')}"],
        )
