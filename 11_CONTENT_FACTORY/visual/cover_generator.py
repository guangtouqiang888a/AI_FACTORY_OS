# 11_CONTENT_FACTORY/visual/cover_generator.py — 封面生成接口（占位）

from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_cover(prompt: str, output_path: Path) -> dict[str, Any]:
    """
    封面生成接口 — 当前版本生成占位封面文件。
    未来可接入图片模型，禁止绑定具体 AI 服务。
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    placeholder = (
        f"COVER PLACEHOLDER\n\n"
        f"Prompt: {prompt}\n\n"
        f"Replace with image model output (future).\n"
        f"Recommended ratio: 16:9\n"
    )
    output_path.write_text(placeholder, encoding="utf-8")
    return {
        "status": "ok",
        "file_path": str(output_path),
        "mode": "placeholder",
        "notice": "封面占位文件 — 未来接入 visual model",
    }
