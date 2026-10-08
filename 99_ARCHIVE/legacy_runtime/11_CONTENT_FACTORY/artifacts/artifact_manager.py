# 11_CONTENT_FACTORY/artifacts/artifact_manager.py — 产品文件产物管理

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ARTIFACTS_ROOT = Path(__file__).resolve().parent
PRODUCTS_ROOT = ARTIFACTS_ROOT / "products"

SUBDIRS = ("source", "documents", "templates", "images", "package")


class ArtifactManager:
    """管理数字产品目录结构与文件产物。"""

    def __init__(self, root: Path | None = None):
        self.root = root or PRODUCTS_ROOT
        self.root.mkdir(parents=True, exist_ok=True)

    def create_product_directory(self, product_id: str) -> Path:
        product_dir = self.root / product_id
        for sub in SUBDIRS:
            (product_dir / sub).mkdir(parents=True, exist_ok=True)
        return product_dir

    def save_artifact(
        self,
        product_id: str,
        subdir: str,
        filename: str,
        content: str | bytes,
    ) -> Path:
        if subdir not in SUBDIRS:
            raise ValueError(f"invalid subdir: {subdir}, must be one of {SUBDIRS}")
        target_dir = self.root / product_id / subdir
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / filename
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def generate_metadata(self, product_id: str, product_data: dict[str, Any]) -> Path:
        product_dir = self.root / product_id
        product_dir.mkdir(parents=True, exist_ok=True)
        metadata = {
            "product_id": product_id,
            "title": product_data.get("title", ""),
            "category": product_data.get("category", ""),
            "product_type": product_data.get("product_type", ""),
            "target_customer": product_data.get("target_customer", ""),
            "status": product_data.get("status", "draft"),
            "artifact_path": str(product_dir),
            "created_at": product_data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "directories": {sub: str(product_dir / sub) for sub in SUBDIRS},
        }
        path = product_dir / "metadata.json"
        path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def get_product_path(self, product_id: str) -> Path:
        return self.root / product_id

    def list_artifacts(self, product_id: str) -> list[str]:
        product_dir = self.root / product_id
        if not product_dir.exists():
            return []
        files = []
        for sub in SUBDIRS:
            sub_path = product_dir / sub
            if sub_path.exists():
                for f in sub_path.rglob("*"):
                    if f.is_file():
                        files.append(str(f.relative_to(product_dir)))
        meta = product_dir / "metadata.json"
        if meta.exists():
            files.append("metadata.json")
        return sorted(files)
