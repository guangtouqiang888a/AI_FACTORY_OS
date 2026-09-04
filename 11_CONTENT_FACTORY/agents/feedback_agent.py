# 11_CONTENT_FACTORY/agents/feedback_agent.py — 销售反馈分析（预留）

from __future__ import annotations

from base_agent import ContentAgent


class FeedbackAgent(ContentAgent):
    role = "feedback_analyst"

    def execute(self, input_data: dict, context: dict) -> dict:
        """
        预留接口 — 接收销售数据与用户反馈，输出优化建议。
        第一阶段：支持手动传入模拟数据。
        """
        product_id = input_data.get("product_id") or context.get("product_id")
        sales_data = input_data.get("sales_data") or {}
        user_feedback = input_data.get("user_feedback") or []

        logs = [f"feedback analysis product_id={product_id or 'unknown'}"]

        if not sales_data and not user_feedback:
            return self._ok(
                {
                    "product_id": product_id,
                    "status": "no_data",
                    "message": "等待销售数据与用户反馈（预留接口）",
                    "suggestions": [],
                },
                logs + ["no feedback data provided — stub mode"],
            )

        sales_count = sales_data.get("sales_count", 0)
        conversion_rate = sales_data.get("conversion_rate", 0.0)
        avg_rating = sales_data.get("avg_rating", 0.0)

        suggestions = []
        if conversion_rate < 0.05:
            suggestions.append("转化率偏低，建议优化商品标题与首图")
        if avg_rating < 4.0 and user_feedback:
            suggestions.append("用户评分偏低，建议改进内容完整度或售后说明")
        if sales_count >= 10:
            suggestions.append("销售表现良好，可扩展同品类产品线")

        logs.append(f"sales_count={sales_count} suggestions={len(suggestions)}")

        return self._ok(
            {
                "product_id": product_id,
                "status": "analyzed",
                "sales_summary": {
                    "sales_count": sales_count,
                    "conversion_rate": conversion_rate,
                    "avg_rating": avg_rating,
                },
                "feedback_count": len(user_feedback),
                "suggestions": suggestions,
            },
            logs,
        )
