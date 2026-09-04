# 0_START/planner.py — Planner（轻量任务拆解）

class Planner:
    """Layer 1: 输入 task，输出 DAG。不做策略决策。"""

    def plan(self, task_input: dict) -> dict:
        task_text = str(task_input.get("task", ""))
        complexity = self._analyze(task_text)
        dag = self._build_dag(complexity)
        dag["task"] = task_text
        return {
            "dag": dag,
            "complexity": complexity["level"],
            "strategy": complexity["strategy"],
            "reason": complexity["reason"],
        }

    def _analyze(self, task_text: str) -> dict:
        text = task_text.lower()
        if "查询" in text or "获取" in text:
            return {"level": "low", "strategy": "simple", "reason": "轻量采集"}
        if "选择" in text or "推荐" in text or "决策" in text:
            return {"level": "mid", "strategy": "standard", "reason": "标准流水线"}
        return {"level": "high", "strategy": "full", "reason": "完整流水线"}

    def _build_dag(self, complexity: dict) -> dict:
        if complexity["level"] == "low":
            return {
                "nodes": [
                    {"id": "data", "agent": "DataAgent"},
                    {"id": "execution", "agent": "ExecutionAgent"},
                ],
                "edges": [["data", "execution"]],
            }
        return {
            "nodes": [
                {"id": "data", "agent": "DataAgent"},
                {"id": "scoring", "agent": "ScoringAgent"},
                {"id": "decision", "agent": "DecisionAgent"},
                {"id": "execution", "agent": "ExecutionAgent"},
            ],
            "edges": [
                ["data", "scoring"],
                ["scoring", "decision"],
                ["decision", "execution"],
            ],
        }
