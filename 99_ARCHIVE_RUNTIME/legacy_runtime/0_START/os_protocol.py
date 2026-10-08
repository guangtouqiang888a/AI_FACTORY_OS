# 0_START/os_protocol.py — OS 级统一输入输出协议

from typing import Any


def make_input(task: str, data: dict | None = None, meta: dict | None = None) -> dict[str, Any]:
    return {"task": task, "data": data or {}, "meta": meta or {}}


def make_output(
    status: str,
    result: dict,
    score: float | None = None,
    logs: list | None = None,
    executor: str | None = None,
) -> dict[str, Any]:
    output: dict[str, Any] = {"status": status, "result": result}
    if score is not None:
        output["score"] = score
    if logs is not None:
        output["logs"] = logs
    if executor is not None:
        output["executor"] = executor
    return output
