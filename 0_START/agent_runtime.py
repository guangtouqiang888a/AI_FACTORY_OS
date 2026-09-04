# 0_START/agent_runtime.py — Agent Runtime（OS 标准化基类）

from abc import ABC, abstractmethod
from typing import Any

from os_protocol import make_input, make_output  # noqa: F401 — 导出供 Agent 使用


class BaseAgent(ABC):
    """所有 Agent 必须继承此基类。"""

    role: str = "worker"
    tools: list[str] = []
    memory_scope: str = "local"

    @abstractmethod
    def execute(self, input_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        """标准执行接口：input_data={task,data,meta}, context=调度上下文。"""

    def meta(self) -> dict[str, Any]:
        return {
            "agent": self.__class__.__name__,
            "role": self.role,
            "tools": self.tools,
            "memory_scope": self.memory_scope,
        }


class AgentRegistry:
    """Agent 注册表。"""

    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, name: str, agent: BaseAgent) -> None:
        self._agents[name] = agent

    def get(self, name: str) -> BaseAgent:
        if name not in self._agents:
            raise KeyError(f"Agent 未注册: {name}")
        return self._agents[name]

    def list_agents(self) -> list[dict]:
        return [{"name": n, **a.meta()} for n, a in self._agents.items()]


def build_default_registry() -> AgentRegistry:
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    for layer in ("1_DATA", "3_DECISION", "6_EXECUTION"):
        p = str(root / layer)
        if p not in sys.path:
            sys.path.insert(0, p)

    from collector import DataAgent  # noqa: E402
    from scoring_agent import ScoringAgent  # noqa: E402
    from decision_agent import DecisionAgent  # noqa: E402
    from execution_agent import ExecutionAgent  # noqa: E402

    registry = AgentRegistry()
    registry.register("DataAgent", DataAgent())
    registry.register("ScoringAgent", ScoringAgent())
    registry.register("DecisionAgent", DecisionAgent())
    registry.register("ExecutionAgent", ExecutionAgent())
    return registry
