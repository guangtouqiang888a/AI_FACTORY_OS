# 11_CONTENT_FACTORY/artifacts/bundle_builder.py — 商品包打包

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any


class BundleBuilder:
    """将商品文件 + publish_package + publish_assistant 打包为 final_product.zip。"""

    def __init__(self, products_root: Path | None = None):
        from artifact_manager import PRODUCTS_ROOT

        self.root = products_root or PRODUCTS_ROOT

    def build(self, product_id: str, zip_name: str = "final_product.zip") -> dict[str, Any]:
        product_dir = self.root / product_id
        if not product_dir.exists():
            return {"status": "error", "zip_path": "", "error": f"product dir not found: {product_id}"}

        zip_path = product_dir / "package" / zip_name
        zip_path.parent.mkdir(parents=True, exist_ok=True)

        include_dirs = ("source", "documents", "templates", "images")
        include_package_subdirs = ("publish_package", "publish_assistant")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            meta = product_dir / "metadata.json"
            if meta.exists():
                zf.write(meta, "metadata.json")

            for sub in include_dirs:
                sub_path = product_dir / sub
                if sub_path.exists():
                    for f in sub_path.rglob("*"):
                        if f.is_file():
                            arc = f.relative_to(product_dir)
                            zf.write(f, str(arc))

            pkg = product_dir / "package"
            for sub in include_package_subdirs:
                sub_path = pkg / sub
                if sub_path.exists():
                    for f in sub_path.rglob("*"):
                        if f.is_file():
                            arc = f.relative_to(product_dir)
                            zf.write(f, str(arc))

        return {"status": "ok", "zip_path": str(zip_path)}
