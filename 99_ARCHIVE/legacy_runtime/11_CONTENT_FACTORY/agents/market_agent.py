# 11_CONTENT_FACTORY/agents/market_agent.py — 市场机会分析

from __future__ import annotations

from base_agent import ContentAgent

_CATEGORY_HINTS = {
    "ppt": ("PPT模板", 85, "medium"),
    "excel": ("Excel模板", 82, "medium"),
    "notion": ("Notion模板", 78, "low"),
    "prompt": ("Prompt合集", 75, "high"),
    "工作流": ("工作流模板", 80, "low"),
    "模板": ("数字模板", 80, "medium"),
}


class MarketAgent(ContentAgent):
    role = "market_analyst"

    def execute(self, input_data: dict, context: dict) -> dict:
        keyword = (input_data.get("keyword") or input_data.get("task") or "").strip()
        if not keyword:
            return self._error("keyword is required")

        logs = [f"analyzing market for keyword={keyword}"]
        category, base_score, competition = self._classify(keyword)
        demand_boost = min(len(keyword), 20) * 0.5
        market_score = min(100.0, base_score + demand_boost)

        if competition == "low":
            recommendation = f"建议优先生产 {category}，竞争较低，适合快速验证"
        elif competition == "high":
            recommendation = f"{category} 竞争激烈，需差异化定位与高质量内容"
        else:
            recommendation = f"{category} 市场需求稳定，建议结合细分场景切入"

        logs.append(f"market_score={market_score:.1f} competition={competition}")

        return self._ok(
            {
                "keyword": keyword,
                "category": category,
                "market_score": round(market_score, 2),
                "competition": competition,
                "recommendation": recommendation,
            },
            logs,
        )

    def _classify(self, keyword: str) -> tuple[str, float, str]:
        lower = keyword.lower()
        for hint, (cat, score, comp) in _CATEGORY_HINTS.items():
            if hint in lower or hint in keyword:
                return cat, score, comp
        return "虚拟资料", 72.0, "medium"
