# 3_DECISION/decision_engine.py — 决策逻辑（供 DecisionAgent 调用）

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "3_DECISION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

from risk_engine import assess_risk  # noqa: E402
import config  # noqa: E402


def decide_scored(keyword: str, products: list[dict], strategies: dict | None = None) -> dict:
    """对已评分商品做风险过滤与决策（产品须含 scores 字段）。"""
    if not products:
        return {
            "keyword": keyword,
            "action": "skip",
            "reason": "无可用数据",
            "candidates": [],
        }

    passed = []
    for p in products:
        risk = assess_risk(p)
        if risk["passed"]:
            passed.append({**p, "risk": risk})

    passed.sort(key=lambda x: x.get("scores", {}).get("total", 0), reverse=True)
    top = passed[:3]

    if not top:
        return {
            "keyword": keyword,
            "action": "skip",
            "reason": "无通过风险过滤的候选",
            "candidates": [],
        }

    best = top[0]
    best_score = best.get("scores", {}).get("total", 0)
    try:
        sys.path.insert(0, str(ROOT / "7_MEMORY"))
        import memory_core  # noqa: E402
        threshold = memory_core.load_runtime_policy().get("threshold", config.PUBLISH_SCORE_THRESHOLD)
    except Exception:
        threshold = config.PUBLISH_SCORE_THRESHOLD

    action = "publish" if best_score >= threshold else "observe"
    if strategies:
        for rule in strategies.get("rules", []):
            cond = rule.get("if", {})
            if cond.get("keyword") == keyword and rule.get("then") == "observe":
                if cond.get("outcome") == "failure" and best_score < threshold + 10:
                    action = "observe"
                    break

    return {
        "keyword": keyword,
        "action": action,
        "reason": f"最高分 {best_score} — {best.get('title', '')[:30]}",
        "candidates": top,
        "best": best,
    }


def decide(keyword: str, products: list[dict]) -> dict:
    """兼容旧接口 — 要求 products 已含 scores。"""
    return decide_scored(keyword, products)
