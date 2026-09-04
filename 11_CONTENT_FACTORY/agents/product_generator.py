# 11_CONTENT_FACTORY/agents/product_generator.py — 真实产品生成调度器

from __future__ import annotations

import json
import sys
from pathlib import Path

_FACTORY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_FACTORY / "artifacts"))
sys.path.insert(0, str(_FACTORY / "artifact_generators"))
sys.path.insert(0, str(_FACTORY / "visual"))

from artifact_manager import ArtifactManager
from base_agent import ContentAgent
from bundle_builder import BundleBuilder
from cover_generator import generate_cover
from excel_generator import generate_excel
from pdf_generator import generate_pdf
from ppt_generator import generate_ppt
from word_generator import generate_word

PRODUCT_TYPES = ("PDF资料", "PPT模板", "Excel模板", "Word模板", "学习计划", "AI办公模板")

_TYPE_FROM_KEYWORD = [
    ("pdf", "PDF资料"),
    ("ppt", "PPT模板"),
    ("excel", "Excel模板"),
    ("word", "Word模板"),
    ("学习计划", "学习计划"),
    ("ai办公", "AI办公模板"),
    ("办公", "AI办公模板"),
]


class ProductGeneratorAgent(ContentAgent):
    role = "product_generator"

    def __init__(self, artifact_manager: ArtifactManager | None = None):
        self.artifacts = artifact_manager or ArtifactManager()

    def execute(self, input_data: dict, context: dict) -> dict:
        product = input_data.get("product") or context.get("product") or {}
        product_id = product.get("id")
        if not product_id:
            return self._error("product.id is required")

        keyword = input_data.get("keyword") or context.get("keyword", "")
        product_type = (
            input_data.get("product_type")
            or product.get("product_type")
            or product.get("category")
            or self._detect_type(keyword, product.get("category", ""))
        )

        logs = [f"real product generation type={product_type} id={product_id}"]
        self.artifacts.create_product_directory(product_id)
        product_dir = self.artifacts.get_product_path(product_id)

        artifact_files: list[str] = []
        errors: list[str] = []

        primary = self._generate_primary(product_type, product, keyword, product_dir, logs, errors)
        if primary:
            artifact_files.append(primary)

        manual = self._generate_manual_pdf(product, keyword, product_dir, logs, errors)
        if manual:
            artifact_files.append(manual)

        cover_prompt = f"数字商品封面：{product.get('title', keyword)}"
        cover_path = product_dir / "images" / "cover_placeholder.txt"
        cover_result = generate_cover(cover_prompt, cover_path)
        if cover_result.get("status") == "ok":
            artifact_files.append(str(cover_path.relative_to(product_dir)))

        if errors:
            return self._error("; ".join(errors), logs)

        self.artifacts.generate_metadata(product_id, {**product, "product_type": product_type, "artifact_files": artifact_files})

        logs.append(f"artifact_files={len(artifact_files)}")

        return self._ok(
            {
                "product_id": product_id,
                "product_type": product_type,
                "artifact_path": str(product_dir),
                "artifact_files": artifact_files,
                "status": "generated",
            },
            logs,
        )

    def _generate_primary(
        self, product_type: str, product: dict, keyword: str, product_dir: Path, logs: list, errors: list
    ) -> str | None:
        title = product.get("title", keyword)
        style = "professional"

        if product_type == "PPT模板":
            sections = self._ppt_sections(keyword, product)
            out = product_dir / "templates" / f"{product['id']}.pptx"
            result = generate_ppt(title, sections, style, out)
        elif product_type == "Excel模板":
            sheets = [
                {"name": "数据录入", "columns": ["日期", "项目", "类别", "金额", "备注"], "sample_rows": 5, "formulas": ["SUM"]},
                {"name": "汇总", "columns": ["类别", "合计", "占比"], "sample_rows": 3},
            ]
            out = product_dir / "templates" / f"{product['id']}.xlsx"
            result = generate_excel(title, sheets, out)
        elif product_type == "Word模板":
            sections = self._word_sections(keyword, product)
            out = product_dir / "templates" / f"{product['id']}.docx"
            result = generate_word(title, sections, out)
        elif product_type == "PDF资料":
            sections = self._pdf_sections(keyword, product, is_manual=False)
            out = product_dir / "documents" / f"{product['id']}.pdf"
            result = generate_pdf(title, sections, out)
            if result.get("status") == "ok":
                logs.append(f"primary pdf={out.name}")
                return str(out.relative_to(product_dir))
            errors.append(result.get("error", "pdf generation failed"))
            return None
        elif product_type in ("学习计划", "AI办公模板"):
            sections = self._word_sections(keyword, product)
            out = product_dir / "templates" / f"{product['id']}.docx"
            result = generate_word(title, sections, out)
        else:
            sections = self._ppt_sections(keyword, product)
            out = product_dir / "templates" / f"{product['id']}.pptx"
            result = generate_ppt(title, sections, style, out)

        if result.get("status") != "ok":
            errors.append(result.get("error", f"{product_type} generation failed"))
            return None
        logs.append(f"primary file={out.name}")
        return str(out.relative_to(product_dir))

    def _generate_manual_pdf(self, product: dict, keyword: str, product_dir: Path, logs: list, errors: list) -> str | None:
        if product.get("category") == "PDF资料":
            return None
        title = f"{product.get('title', keyword)} — 产品说明"
        sections = self._pdf_sections(keyword, product, is_manual=True)
        out = product_dir / "documents" / "product_manual.pdf"
        result = generate_pdf(title, sections, out)
        if result.get("status") != "ok":
            errors.append(result.get("error", "manual pdf failed"))
            return None
        logs.append(f"manual pdf={out.name}")
        return str(out.relative_to(product_dir))

    def _ppt_sections(self, keyword: str, product: dict) -> list[dict]:
        return [
            {"title": "背景介绍", "bullets": [f"关键词：{keyword}", product.get("problem", ""), "市场机会概述"]},
            {"title": "核心框架", "bullets": ["模块一：基础", "模块二：进阶", "模块三：实战"]},
            {"title": "案例示范", "bullets": ["场景 A", "场景 B", "最佳实践"]},
            {"title": "总结", "bullets": ["核心要点回顾", "行动建议", "延伸资源"]},
        ]

    def _word_sections(self, keyword: str, product: dict) -> list[dict]:
        return [
            {
                "title": "产品概述",
                "paragraphs": [product.get("title", keyword), product.get("problem", "")],
            },
            {
                "title": "使用指南",
                "paragraphs": ["1. 下载并解压文件", "2. 阅读本说明", "3. 按模板填写/使用", "4. 保存并交付"],
                "table": [["步骤", "说明"], ["1", "打开模板"], ["2", "替换示例内容"], ["3", "导出成品"]],
            },
            {
                "title": "注意事项",
                "paragraphs": ["仅供个人/商业授权范围内使用", "禁止二次倒卖未授权版本"],
            },
        ]

    def _pdf_sections(self, keyword: str, product: dict, is_manual: bool) -> list[dict]:
        prefix = "产品说明" if is_manual else "资料内容"
        return [
            {"title": f"{prefix} — 产品介绍", "lines": [product.get("title", keyword), product.get("target_customer", "")]},
            {"title": "使用方法", "lines": ["打开主文件", "按章节阅读/编辑", "保存为最终交付版本"]},
            {"title": "注意事项", "lines": ["数字商品不退不换请知悉", "网盘链接24小时内有效", "有问题请联系客服"]},
        ]

    def _detect_type(self, keyword: str, category: str) -> str:
        text = f"{keyword} {category}".lower()
        for hint, ptype in _TYPE_FROM_KEYWORD:
            if hint in text or hint in keyword:
                return ptype
        return category if category in PRODUCT_TYPES else "PPT模板"
