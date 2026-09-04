# 11_CONTENT_FACTORY/agents/release_gate.py — 人工发布前检查（非自动发布）

from __future__ import annotations

import sys
from pathlib import Path

_FACTORY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_FACTORY / "artifacts"))

from artifact_manager import ArtifactManager
from base_agent import ContentAgent

PUBLISH_PACKAGE_FILES = ("title.txt", "description.txt", "keywords.txt", "pricing.json", "cover_prompt.txt")
REAL_EXTENSIONS = (".pptx", ".xlsx", ".docx", ".pdf")
COMMERCIAL_THRESHOLD = 80.0


class ReleaseGateAgent(ContentAgent):
    role = "release_gate"

    def __init__(self):
        self.artifacts = ArtifactManager()

    def execute(self, input_data: dict, context: dict) -> dict:
        product = input_data.get("product") or context.get("product") or {}
        quality = input_data.get("quality") or context.get("quality") or {}
        packaging = input_data.get("packaging") or context.get("packaging") or {}
        artifacts = input_data.get("artifacts") or context.get("artifacts") or {}

        product_id = product.get("id")
        if not product_id:
            return self._error("product.id is required")

        logs = [f"release gate check id={product_id}"]
        checks: list[dict] = []

        # 1. 文件是否存在
        product_dir = self.artifacts.get_product_path(product_id)
        real_files = self._find_real_files(product_dir)
        checks.append({"name": "real_files", "passed": len(real_files) > 0, "detail": real_files})

        zip_path = packaging.get("zip_path") or packaging.get("final_product_zip")
        zip_exists = bool(zip_path and Path(zip_path).exists())
        checks.append({"name": "final_product_zip", "passed": zip_exists, "detail": zip_path})

        # 2. quality_score
        quality_score = quality.get("quality_score", 0)
        checks.append({"name": "quality_score", "passed": quality_score >= 60, "detail": quality_score})

        # 3. commercial_score
        commercial_score = quality.get("commercial_score", 0)
        commercial_ok = commercial_score >= COMMERCIAL_THRESHOLD
        checks.append({"name": "commercial_score", "passed": commercial_ok, "detail": commercial_score})

        # 4. publish_package 完整
        pkg_dir = product_dir / "package" / "publish_package"
        pkg_ok = all((pkg_dir / f).exists() for f in PUBLISH_PACKAGE_FILES)
        checks.append({"name": "publish_package", "passed": pkg_ok, "detail": str(pkg_dir)})

        all_passed = all(c["passed"] for c in checks)
        release_status = "approved" if all_passed else "blocked"

        logs.append(f"release_status={release_status}")

        return self._ok(
            {
                "release_status": release_status,
                "checks": checks,
                "quality_score": quality_score,
                "commercial_score": commercial_score,
                "artifact_files": artifacts.get("artifact_files", []),
                "zip_path": zip_path,
                "notice": "非自动发布 — 人工确认后方可上架",
            },
            logs,
        )

    def _find_real_files(self, product_dir: Path) -> list[str]:
        found = []
        if not product_dir.exists():
            return found
        for f in product_dir.rglob("*"):
            if f.is_file() and f.suffix.lower() in REAL_EXTENSIONS:
                found.append(str(f.relative_to(product_dir)))
        return found
