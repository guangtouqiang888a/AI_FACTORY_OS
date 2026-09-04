# 11_CONTENT_FACTORY/llm_adapter.py — LLM 接口预留（禁止直接调用 API）

"""
未来 LLM 调用须经 PolicyEngine 统一控制。
本模块仅提供接口定义，不实现任何外部 API 调用。
"""

from typing import Any


class LLMAdapterNotConfiguredError(NotImplementedError):
    """LLM 尚未接入 PolicyEngine 管控。"""


def generate_text(prompt: str, context: dict | None = None) -> str:
    """
    预留：文本生成接口。
    未来由 PolicyEngine 路由至 ModelBridge。
    """
    raise LLMAdapterNotConfiguredError(
        "generate_text() is reserved — LLM calls must go through PolicyEngine / ModelBridge"
    )


def generate_product(spec: dict[str, Any]) -> dict[str, Any]:
    """
    预留：结构化产品生成接口。
    未来由 PolicyEngine 路由至 ModelBridge。
    """
    raise LLMAdapterNotConfiguredError(
        "generate_product() is reserved — LLM calls must go through PolicyEngine / ModelBridge"
    )
