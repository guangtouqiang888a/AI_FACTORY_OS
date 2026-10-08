# 3_DECISION/scoring_agent.py — ScoringAgent（标准化接口）

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for layer in ("8_CONFIG", "1_DATA", "3_DECISION", "0_START"):
    p = str(ROOT / layer)
    if p not in sys.path:
        sys.path.insert(0, p)

import database  # noqa: E402
from scorer import score_product  # noqa: E402
from agent_runtime import BaseAgent  # noqa: E402
from os_protocol import make_output  # noqa: E402


class ScoringAgent(BaseAgent):
    role = "scorer"
    tools = ["score_product", "database.save_score"]
    memory_scope = "3_DECISION"

    def execute(self, input_data: dict, context: dict) -> dict:
        task = input_data["task"]
        keyword = input_data["data"].get("keyword", task)
        products = input_data["data"].get("products") or database.get_products_by_keyword(keyword)
        logs: list[str] = []
        scored = []
        for p in products:
            scores = score_product(p)
            database.save_score(p["id"], scores)
            scored.append({**p, "scores": scores})
        max_score = max((s["scores"]["total"] for s in scored), default=0.0)
        logs.append(f"scored {len(scored)} products, max_score={max_score}")
        return make_output(
            "ok",
            {"keyword": keyword, "products": scored, "count": len(scored)},
            score=max_score,
            logs=logs,
        )
