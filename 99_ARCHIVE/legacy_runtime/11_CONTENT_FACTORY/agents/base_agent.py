# 11_CONTENT_FACTORY/agents/base_agent.py — Content Factory Agent 标准接口

from abc import ABC, abstractmethod
from typing import Any


class ContentAgent(ABC):
    """Content Factory Agent 基类 — 独立于核心 OS Agent Runtime。"""

    role: str = "content_worker"

    @abstractmethod
    def execute(self, input_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        """标准执行接口，返回 {status, result, logs}。"""

    def _ok(self, result: dict, logs: list[str] | None = None) -> dict[str, Any]:
        return {"status": "ok", "result": result, "logs": logs or []}

    def _error(self, message: str, logs: list[str] | None = None) -> dict[str, Any]:
        return {"status": "error", "result": {"error": message}, "logs": logs or [message]}

    def meta(self) -> dict[str, Any]:
        return {"agent": self.__class__.__name__, "role": self.role}
