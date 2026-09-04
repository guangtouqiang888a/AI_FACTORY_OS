# 11_CONTENT_FACTORY/agents/creator_agent.py — Product Creator（数字商品生产）

from __future__ import annotations

import sys
from pathlib import Path

_FACTORY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_FACTORY / "schemas"))
sys.path.insert(0, str(_FACTORY / "artifacts"))

from artifact_manager import ArtifactManager
from base_agent import ContentAgent
from product_schema import DigitalProduct

_LINE_PRODUCT_TYPES = {
    "PDF资料": "PDF资料",
    "PPT模板": "PPT模板",
    "Excel模板": "Excel模板",
    "Word模板": "Word模板",
    "学习计划": "学习计划",
    "AI办公模板": "AI办公模板",
}


class CreatorAgent(ContentAgent):
    role = "product_creator"

    def __init__(self):
        self.artifacts = ArtifactManager()

    def execute(self, input_data: dict, context: dict) -> dict:
        market = input_data.get("market") or context.get("market") or {}
        keyword = (input_data.get("keyword") or market.get("keyword") or "").strip()

        product_type = input_data.get("product_type") or self._resolve_type(keyword, market)
        target_customer = input_data.get("target_customer") or self._target_customer(product_type)
        market_requirement = (
            input_data.get("market_requirement")
            or market.get("recommendation")
            or f"生产 {product_type} 满足「{keyword}」市场需求"
        )

        if not keyword and not product_type:
            return self._error("keyword or product_type is required")

        market_score = market.get("market_score", 72.0)
        logs = [f"product_creator type={product_type} keyword={keyword}"]

        product = DigitalProduct(
            title=self._build_title(keyword, product_type),
            category=product_type,
            target_customer=target_customer,
            problem=self._problem(keyword, product_type),
            content=self._content_outline(keyword, product_type, market_requirement),
            market_score=market_score,
            price=self._suggest_price(product_type, market_score),
            platform=input_data.get("platform", "xianyu"),
            status="creating",
        )

        product_dir = self.artifacts.create_product_directory(product.id)
        logs.append(f"directory created path={product_dir}")

        product.status = "draft"
        product_dict = product.to_dict()
        product_dict["product_type"] = product_type
        product_dict["artifact_path"] = str(product_dir)

        self.artifacts.generate_metadata(product.id, product_dict)
        logs.append(f"product metadata initialized id={product.id}")

        return self._ok(
            {
                "product": product_dict,
                "artifacts": {
                    "artifact_path": str(product_dir),
                    "product_type": product_type,
                    "artifact_files": [],
                },
            },
            logs,
        )

    def _resolve_type(self, keyword: str, market: dict) -> str:
        text = f"{keyword} {market.get('category', '')}".lower()
        mapping = [
            ("pdf", "PDF资料"),
            ("ppt", "PPT模板"),
            ("excel", "Excel模板"),
            ("word", "Word模板"),
            ("学习计划", "学习计划"),
            ("ai办公", "AI办公模板"),
            ("办公", "AI办公模板"),
        ]
        for hint, ptype in mapping:
            if hint in text or hint in keyword:
                return ptype
        cat = market.get("category", "PPT模板")
        return _LINE_PRODUCT_TYPES.get(cat, "PPT模板")

    def _build_title(self, keyword: str, product_type: str) -> str:
        return f"【{product_type}】{keyword} — 专业数字资料包"

    def _target_customer(self, product_type: str) -> str:
        mapping = {
            "PDF资料": "学生、自学者、培训人群",
            "PPT模板": "职场人士、创业者、学生",
            "Excel模板": "财务、运营、项目经理",
            "Word模板": "行政、HR、文档工作者",
            "学习计划": "学生、考证人群、终身学习者",
            "AI办公模板": "白领、效率达人、小团队",
        }
        return mapping.get(product_type, "有数字资料需求的个人用户")

    def _problem(self, keyword: str, product_type: str) -> str:
        return f"用户需要高质量 {product_type} 解决「{keyword}」场景，自行制作耗时且质量不稳定"

    def _content_outline(self, keyword: str, product_type: str, requirement: str) -> str:
        return (
            f"# {product_type} 生产大纲\n\n"
            f"## 关键词\n{keyword}\n\n"
            f"## 市场需求\n{requirement}\n\n"
            f"## 交付物\n"
            f"- source/ 原始素材\n"
            f"- documents/ 文档内容\n"
            f"- templates/ 模板结构\n"
            f"- images/ 封面与配图占位\n"
            f"- package/ 发布包\n"
        )

    def _suggest_price(self, product_type: str, market_score: float) -> float:
        base = {
            "PDF资料": 15.9,
            "PPT模板": 29.9,
            "Excel模板": 19.9,
            "Word模板": 12.9,
            "学习计划": 9.9,
            "AI办公模板": 24.9,
        }.get(product_type, 19.9)
        if market_score >= 85:
            return round(base * 1.2, 2)
        if market_score < 70:
            return round(base * 0.8, 2)
        return base
