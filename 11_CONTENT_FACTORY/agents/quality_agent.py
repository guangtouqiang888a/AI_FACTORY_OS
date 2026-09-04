# 11_CONTENT_FACTORY/agents/quality_agent.py — 产品质量 + 商业评分

from __future__ import annotations

import sys
from pathlib import Path

_FACTORY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_FACTORY / "artifacts"))

from artifact_manager import ArtifactManager
from base_agent import ContentAgent

REAL_EXTENSIONS = {".pptx", ".xlsx", ".docx", ".pdf"}
COMMERCIAL_THRESHOLD = 80.0


class QualityAgent(ContentAgent):
    role = "quality_inspector"

    _REQUIRED_FIELDS = ("title", "category", "target_customer", "problem", "content")

    def __init__(self):
        self.artifacts = ArtifactManager()

    def execute(self, input_data: dict, context: dict) -> dict:
        product = input_data.get("product") or context.get("product") or {}
        artifacts = input_data.get("artifacts") or context.get("artifacts") or {}
        if not product:
            return self._error("product is required")

        product_id = product.get("id")
        logs = [f"inspecting product id={product_id or '?'}"]

        artifact_files = artifacts.get("artifact_files") or artifacts.get("files") or []
        if product_id and not artifact_files:
            artifact_files = self.artifacts.list_artifacts(product_id)

        content_score = self._score_content(product, artifact_files)
        usability_score = self._score_usability(product, artifact_files)
        market_score = min(100.0, float(product.get("market_score", 0)))
        selling_score = self._score_selling(product, artifact_files)
        production_cost_score = self._score_production_cost(artifact_files)

        quality_score = round(
            content_score * 0.35 + usability_score * 0.35 + market_score * 0.30,
            2,
        )
        commercial_score = round(
            (content_score + selling_score + market_score + production_cost_score) / 4,
            2,
        )

        passed_commercial = commercial_score >= COMMERCIAL_THRESHOLD
        status = "quality_pass" if passed_commercial else "need_revision"
        recommendation = self._recommendation(commercial_score, artifact_files)

        issues = self._collect_issues(product, artifact_files, commercial_score)

        logs.append(f"quality_score={quality_score} commercial_score={commercial_score} status={status}")

        return self._ok(
            {
                "quality_score": quality_score,
                "commercial_score": commercial_score,
                "content_score": round(content_score, 2),
                "usability_score": round(usability_score, 2),
                "market_score": round(market_score, 2),
                "selling_score": round(selling_score, 2),
                "production_cost_score": round(production_cost_score, 2),
                "passed": passed_commercial,
                "status": status,
                "recommendation": recommendation,
                "issues": issues,
            },
            logs,
        )

    def _score_content(self, product: dict, files: list) -> float:
        score = 0.0
        filled = sum(1 for f in self._REQUIRED_FIELDS if product.get(f))
        score += (filled / len(self._REQUIRED_FIELDS)) * 40
        if len(product.get("content", "")) >= 100:
            score += 20
        real = sum(1 for f in files if Path(f).suffix.lower() in REAL_EXTENSIONS)
        score += min(40, real * 15)
        return min(100.0, score)

    def _score_usability(self, product: dict, files: list) -> float:
        score = 30.0
        if product.get("artifact_path"):
            score += 20
        real = [f for f in files if Path(f).suffix.lower() in REAL_EXTENSIONS]
        if real:
            score += 30
        if any("manual" in f.lower() or f.endswith(".pdf") for f in files):
            score += 20
        return min(100.0, score)

    def _score_selling(self, product: dict, files: list) -> float:
        score = 40.0
        if product.get("price", 0) > 0:
            score += 25
        if product.get("target_customer"):
            score += 15
        if any(Path(f).suffix.lower() in REAL_EXTENSIONS for f in files):
            score += 20
        return min(100.0, score)

    def _score_production_cost(self, files: list) -> float:
        real_count = sum(1 for f in files if Path(f).suffix.lower() in REAL_EXTENSIONS)
        if real_count >= 2:
            return 90.0
        if real_count == 1:
            return 75.0
        return 40.0

    def _recommendation(self, commercial_score: float, files: list) -> str:
        if commercial_score >= COMMERCIAL_THRESHOLD:
            return "commercial_score >= 80，可进入包装与发布辅助流程"
        real = sum(1 for f in files if Path(f).suffix.lower() in REAL_EXTENSIONS)
        if real == 0:
            return "缺少真实交付文件，需重新运行 ProductGenerator"
        return "商业评分未达标，建议优化内容完整度与定价策略"

    def _collect_issues(self, product: dict, files: list, commercial_score: float) -> list[str]:
        issues = []
        for field in self._REQUIRED_FIELDS:
            if not product.get(field):
                issues.append(f"missing field: {field}")
        if not any(Path(f).suffix.lower() in REAL_EXTENSIONS for f in files):
            issues.append("no real deliverable files (.pptx/.xlsx/.docx/.pdf)")
        if commercial_score < COMMERCIAL_THRESHOLD:
            issues.append(f"commercial_score {commercial_score} below {COMMERCIAL_THRESHOLD}")
        return issues
