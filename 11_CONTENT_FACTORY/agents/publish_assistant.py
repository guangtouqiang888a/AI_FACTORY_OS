# 11_CONTENT_FACTORY/agents/publish_assistant.py — 人工发布辅助（非自动发布）

from __future__ import annotations

import json
import sys
from pathlib import Path

_FACTORY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_FACTORY / "artifacts"))

from artifact_manager import ArtifactManager
from base_agent import ContentAgent

PLATFORM_GUIDES = {
    "xianyu": {
        "name": "闲鱼",
        "category_hint": "电子资料 / 办公文具",
        "delivery": "拍下后通过聊天发送网盘链接",
        "price_range": "9.9 - 49.9",
        "tips": ["标题含关键词", "首图清晰", "描述突出即用型"],
    },
    "taobao": {
        "name": "淘宝",
        "category_hint": "教育培训 / 办公用品",
        "delivery": "自动发货（网盘链接）或人工发货",
        "price_range": "19.9 - 99.9",
        "tips": ["详情页结构化", "支持7天无理由（虚拟需标注）", "关注类目资质"],
    },
    "overseas": {
        "name": "海外数字商品平台（Gumroad / Etsy Digital）",
        "category_hint": "Digital Downloads / Templates",
        "delivery": "Platform digital delivery",
        "price_range": "$4.99 - $29.99",
        "tips": ["English listing required", "Clear license terms", "Preview images"],
    },
}


class PublishAssistantAgent(ContentAgent):
    role = "publish_assistant"

    def __init__(self, artifact_manager: ArtifactManager | None = None):
        self.artifacts = artifact_manager or ArtifactManager()

    def execute(self, input_data: dict, context: dict) -> dict:
        product = input_data.get("product") or context.get("product") or {}
        packaging = input_data.get("packaging") or context.get("packaging") or {}
        product_id = product.get("id")
        if not product_id:
            return self._error("product.id is required")

        publish_package = packaging.get("publish_package_path", "")
        logs = [f"generating publish assistant package id={product_id}"]

        platform_adaptations = {}
        for platform_key, guide in PLATFORM_GUIDES.items():
            platform_adaptations[platform_key] = self._adapt_platform(
                platform_key, guide, product, packaging
            )

        assistant_dir = self.artifacts.get_product_path(product_id) / "package" / "publish_assistant"
        assistant_dir.mkdir(parents=True, exist_ok=True)

        assistant_path = assistant_dir / "platform_guide.json"
        assistant_path.write_text(
            json.dumps(platform_adaptations, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        checklist = self._human_checklist(product, packaging, platform_adaptations)
        checklist_path = assistant_dir / "publish_checklist.md"
        checklist_path.write_text(checklist, encoding="utf-8")

        logs.append("publish assistant ready — manual publish required")

        return self._ok(
            {
                "mode": "manual_assist",
                "product_id": product_id,
                "publish_package": publish_package,
                "assistant_path": str(assistant_dir),
                "platform_adaptations": platform_adaptations,
                "checklist_path": str(checklist_path),
                "notice": "非自动发布 — 请人工确认后操作",
            },
            logs,
        )

    def _adapt_platform(
        self, key: str, guide: dict, product: dict, packaging: dict
    ) -> dict:
        pkg = packaging.get("publish_package", packaging)
        return {
            "platform": guide["name"],
            "suggested_title": pkg.get("title", product.get("title", ""))[:60],
            "category_hint": guide["category_hint"],
            "delivery_method": guide["delivery"],
            "price_suggestion": product.get("price", 19.9),
            "price_range": guide["price_range"],
            "keywords": pkg.get("keywords", []),
            "tips": guide["tips"],
        }

    def _human_checklist(self, product: dict, packaging: dict, platforms: dict) -> str:
        lines = [
            "# 人工发布检查清单\n",
            f"产品 ID：{product.get('id')}\n",
            f"产品状态：{product.get('status')}\n",
            "## 发布前确认\n",
            "- [ ] 质量评分 >= 80（quality_pass）",
            "- [ ] 已检查 publish_package 内所有文件",
            "- [ ] 网盘链接已准备",
            "- [ ] 人工确认内容无侵权风险",
            "- [ ] 遵守平台规则，不使用自动化刷量",
            "\n## 平台适配\n",
        ]
        for key, adapt in platforms.items():
            lines.append(f"### {adapt['platform']}")
            lines.append(f"- 建议标题：{adapt['suggested_title']}")
            lines.append(f"- 类目：{adapt['category_hint']}")
            lines.append(f"- 发货方式：{adapt['delivery_method']}")
            lines.append("")
        return "\n".join(lines)
