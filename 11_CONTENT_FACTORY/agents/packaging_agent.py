# 11_CONTENT_FACTORY/agents/packaging_agent.py — 商品包装 + final_product.zip

from __future__ import annotations

import json
import sys
from pathlib import Path

_FACTORY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_FACTORY / "artifacts"))
sys.path.insert(0, str(_FACTORY / "visual"))

from artifact_manager import ArtifactManager
from base_agent import ContentAgent
from bundle_builder import BundleBuilder
from cover_generator import generate_cover


class PackagingAgent(ContentAgent):
    role = "packaging_designer"

    def __init__(self):
        self.artifacts = ArtifactManager()
        self.bundle = BundleBuilder()

    def execute(self, input_data: dict, context: dict) -> dict:
        product = input_data.get("product") or context.get("product") or {}
        quality = input_data.get("quality") or context.get("quality") or {}
        if not product:
            return self._error("product is required")

        commercial_score = quality.get("commercial_score", 0)
        if commercial_score < 80:
            return self._error(
                f"commercial_score {commercial_score} < 80, packaging blocked",
                [f"recommendation: {quality.get('recommendation', '')}"],
            )

        product_id = product.get("id")
        keyword = input_data.get("keyword") or product.get("title", "")
        category = product.get("category", "虚拟资料")
        quality_score = quality.get("quality_score", 0)

        logs = [f"packaging product id={product_id}"]

        selling_points = self._selling_points(category, commercial_score)
        description = self._description(product, selling_points)
        keywords = self._keywords(keyword, category)
        listing_title = self._listing_title(product.get("title", keyword), commercial_score)
        pricing = self._pricing(product)
        cover_prompt = self._cover_prompt(product, keywords)

        cover_path = self.artifacts.get_product_path(product_id) / "images" / "cover_placeholder.txt"
        generate_cover(cover_prompt, cover_path)

        publish_package_path = self._write_publish_package(
            product_id, listing_title, description, keywords, pricing, cover_prompt
        )

        self._write_publish_assistant_stub(product_id, product, listing_title)

        bundle_result = self.bundle.build(product_id, "final_product.zip")
        if bundle_result.get("status") != "ok":
            return self._error(bundle_result.get("error", "bundle failed"), logs)

        zip_path = bundle_result["zip_path"]
        logs.append(f"final_product.zip={zip_path}")

        return self._ok(
            {
                "listing_title": listing_title,
                "selling_points": selling_points,
                "description": description,
                "keywords": keywords,
                "publish_package_path": str(publish_package_path),
                "zip_path": zip_path,
                "final_product_zip": zip_path,
                "publish_package": {
                    "title": listing_title,
                    "description": description,
                    "keywords": keywords,
                    "pricing": pricing,
                    "cover_prompt": cover_prompt,
                },
            },
            logs,
        )

    def _write_publish_assistant_stub(self, product_id: str, product: dict, title: str) -> None:
        assistant_dir = self.artifacts.get_product_path(product_id) / "package" / "publish_assistant"
        assistant_dir.mkdir(parents=True, exist_ok=True)
        (assistant_dir / "publish_checklist.md").write_text(
            f"# 人工发布清单\n\n产品：{title}\n\n- [ ] 确认 final_product.zip 完整\n- [ ] 人工审核内容\n- [ ] 手动上架\n",
            encoding="utf-8",
        )

    def _write_publish_package(
        self, product_id: str, title: str, description: str, keywords: list[str], pricing: dict, cover_prompt: str
    ) -> Path:
        pkg_dir = self.artifacts.get_product_path(product_id) / "package" / "publish_package"
        pkg_dir.mkdir(parents=True, exist_ok=True)
        (pkg_dir / "title.txt").write_text(title, encoding="utf-8")
        (pkg_dir / "description.txt").write_text(description, encoding="utf-8")
        (pkg_dir / "keywords.txt").write_text("\n".join(keywords), encoding="utf-8")
        (pkg_dir / "pricing.json").write_text(json.dumps(pricing, ensure_ascii=False, indent=2), encoding="utf-8")
        (pkg_dir / "cover_prompt.txt").write_text(cover_prompt, encoding="utf-8")
        return pkg_dir

    def _listing_title(self, title: str, score: float) -> str:
        badge = "【精品】" if score >= 80 else "【即用型】"
        return f"{badge}{title}"[:60]

    def _selling_points(self, category: str, score: float) -> list[str]:
        points = [f"专业 {category}，真实可交付文件", "含 PDF 产品说明", "数字交付，拍下即发"]
        if score >= 80:
            points.insert(0, "commercial_score >= 80，质量达标")
        return points

    def _description(self, product: dict, selling_points: list[str]) -> str:
        lines = [
            product.get("title", ""),
            "",
            "【产品亮点】",
            *[f"✓ {p}" for p in selling_points],
            "",
            "【适用人群】",
            product.get("target_customer", ""),
            "",
            "【交付说明】",
            "付款后发送 final_product.zip 网盘链接。",
            f"\n【产物目录】{product.get('artifact_path', '')}",
        ]
        return "\n".join(lines)

    def _keywords(self, keyword: str, category: str) -> list[str]:
        return list(dict.fromkeys([keyword, category, "虚拟资料", "数字商品", "模板"]))[:10]

    def _pricing(self, product: dict) -> dict:
        price = product.get("price", 19.9)
        return {"suggested_price": price, "currency": "CNY", "platform": product.get("platform", "xianyu")}

    def _cover_prompt(self, product: dict, keywords: list[str]) -> str:
        return f"封面设计：{product.get('title', '')}，关键词：{', '.join(keywords[:5])}，16:9"
