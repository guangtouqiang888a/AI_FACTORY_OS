# 6_EXECUTION/execution_agent.py — ExecutionAgent（标准化接口）

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for layer in ("6_EXECUTION", "0_START"):
    p = str(ROOT / layer)
    if p not in sys.path:
        sys.path.insert(0, p)

from publisher import publish  # noqa: E402
from agent_runtime import BaseAgent  # noqa: E402
from os_protocol import make_output  # noqa: E402


class ExecutionAgent(BaseAgent):
    role = "publisher"
    tools = ["publish", "output_writer"]
    memory_scope = "6_EXECUTION"

    def execute(self, input_data: dict, context: dict) -> dict:
        decision = input_data["data"].get("decision", {})
        logs: list[str] = []
        try:
            result = publish(decision)
            status = "ok" if result.get("status") not in ("error",) else "error"
            logs.append(f"exec_status={result.get('status')}")
            return make_output(
                status,
                result,
                score=result.get("total_score"),
                logs=logs,
            )
        except Exception as exc:
            logs.append(str(exc))
            return make_output("error", {"error": str(exc), "decision": decision}, logs=logs)
