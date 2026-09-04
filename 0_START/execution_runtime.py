# 0_START/execution_runtime.py — Execution Runtime（Production Grade 加固）

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "0_START"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "7_MEMORY"))

import config  # noqa: E402
import memory_core  # noqa: E402
from model_bridge import ModelBridge  # noqa: E402
from os_protocol import make_input, make_output  # noqa: E402
from agent_runtime import AgentRegistry, build_default_registry  # noqa: E402

_RUNTIME_CALLER = "ExecutionRuntime"


class ExecutionRuntime:
    """唯一执行入口：deterministic mode + execution_hash_log。"""

    def __init__(self, registry: AgentRegistry | None = None):
        self.registry = registry or build_default_registry()
        self.bridge = ModelBridge(caller=_RUNTIME_CALLER)
        self.deterministic = config.DETERMINISTIC_MODE

    def execute_dag(self, dag: dict, complexity: str, policy_engine: Any) -> dict:
        task = dag.get("task", "")
        context: dict = {
            "task": task,
            "dag": dag,
            "complexity": complexity,
            "deterministic": self.deterministic,
            "nodes": {},
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        for node in self._topo_order(dag["nodes"], dag["edges"]):
            policy = node.get("policy", {"executor": "rule", "approved": True})
            input_data = self._build_input(node, context)
            output = self.execute_node(node, input_data, context, policy, policy_engine)
            context["nodes"][node["id"]] = {
                **output,
                "node_id": node["id"],
                "agent": node["agent"],
                "policy": policy,
                "execution_hash": output.get("execution_hash"),
                "finished_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        context["finished_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return context

    def execute_node(
        self,
        node: dict,
        input_data: dict,
        context: dict,
        policy: dict,
        policy_engine: Any,
    ) -> dict:
        executor = policy.get("executor", "rule")
        agent_name = node.get("agent", "")
        logs = [f"policy_executor={executor}", f"mode={policy.get('mode')}"]

        if self.deterministic and executor != "rule":
            logs.append("deterministic mode: force rule executor")
            executor = "rule"

        if not policy.get("approved", True) and executor != "rule":
            executor = "rule"
            logs.append("policy not approved, fallback rule")

        try:
            rule_output = self._run_rule(agent_name, input_data, context, logs)

            if executor == "rule":
                rule_output["executor"] = "rule"
                rule_output["execution_hash"] = self._hash_execution(
                    node["id"], input_data, policy, rule_output
                )
                self._log_hash(node, input_data, policy, rule_output)
                return rule_output

            if not policy_engine.check_budget(executor):
                logs.append("budget exceeded, fallback rule")
                rule_output["logs"] = logs
                rule_output["executor"] = "rule"
                rule_output["execution_hash"] = self._hash_execution(
                    node["id"], input_data, policy, rule_output
                )
                self._log_hash(node, input_data, policy, rule_output)
                return rule_output

            llm_out = self._run_llm(executor, node, input_data)
            if llm_out["status"] == "ok":
                policy_engine.consume_cost(executor)
                rule_output["result"]["llm_insight"] = llm_out["result"].get("llm", {})
                rule_output["logs"] = logs + llm_out.get("logs", [])
                rule_output["executor"] = f"rule+{executor}"
            else:
                rule_output["logs"] = logs + [f"llm fallback: {llm_out['result'].get('error')}"]
                rule_output["executor"] = "rule"

            rule_output["execution_hash"] = self._hash_execution(
                node["id"], input_data, policy, rule_output
            )
            self._log_hash(node, input_data, policy, rule_output)
            return rule_output

        except Exception as exc:
            fallback = self._run_rule(agent_name, input_data, context, logs + [str(exc)])
            fallback["status"] = "fallback"
            fallback["result"]["runtime_error"] = str(exc)
            fallback["execution_hash"] = self._hash_execution(
                node["id"], input_data, policy, fallback
            )
            self._log_hash(node, input_data, policy, fallback)
            return fallback

    def _run_rule(self, agent_name: str, input_data: dict, context: dict, logs: list) -> dict:
        output = self.registry.get(agent_name).execute(input_data, context)
        output["logs"] = logs + output.get("logs", [])
        return output

    def _run_llm(self, executor: str, node: dict, input_data: dict) -> dict:
        prompt = (
            f"Node: {node.get('id')}\nAgent: {node.get('agent')}\n"
            f"Input: {json.dumps(input_data, ensure_ascii=False, sort_keys=True)}\n"
            f"Return JSON: summary, recommendation, score"
        )
        if executor == "deepseek":
            response = self.bridge.call_deepseek(prompt)
        else:
            response = self.bridge.call_gpt(prompt, model="gpt-4.1-mini")
        if not response.get("ok"):
            return make_output("error", {"error": response.get("error"), "engine": executor})
        return make_output("ok", {"llm": response.get("data", {}), "engine": executor})

    @staticmethod
    def _canonical(obj: dict) -> str:
        return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)

    def _hash_execution(self, node_id: str, input_data: dict, policy: dict, output: dict) -> str:
        payload = {
            "node_id": node_id,
            "input": input_data,
            "policy": {k: policy.get(k) for k in ("executor", "approved", "mode")},
            "output": {
                "status": output.get("status"),
                "executor": output.get("executor"),
                "result_keys": sorted((output.get("result") or {}).keys()),
            },
            "deterministic": self.deterministic,
        }
        return hashlib.sha256(self._canonical(payload).encode()).hexdigest()[:16]

    @staticmethod
    def _log_hash(node: dict, input_data: dict, policy: dict, output: dict) -> None:
        memory_core.log_execution_hash({
            "node_id": node.get("id"),
            "agent": node.get("agent"),
            "hash": output.get("execution_hash"),
            "executor": output.get("executor"),
            "status": output.get("status"),
            "policy_executor": policy.get("executor"),
        })

    @staticmethod
    def _topo_order(nodes: list, edges: list) -> list:
        deps = {n["id"]: [] for n in nodes}
        for frm, to in edges:
            deps[to].append(frm)
        ordered, pending = [], {n["id"]: n for n in nodes}
        while len(ordered) < len(nodes):
            for nid, node in list(pending.items()):
                if all(any(o["id"] == d for o in ordered) for d in deps[nid]):
                    ordered.append(node)
                    del pending[nid]
        return ordered

    def _build_input(self, node: dict, context: dict) -> dict:
        task, meta = context["task"], {"node_id": node["id"], "agent": node["agent"]}
        nodes = context.get("nodes", {})
        if node["id"] == "data":
            return make_input(task, data={"keyword": task}, meta=meta)
        if node["id"] == "scoring":
            prev = nodes["data"]["result"]
            return make_input(task, data={"keyword": prev.get("keyword", task), "products": prev.get("products", []), "data_result": prev.get("data_result", {})}, meta=meta)
        if node["id"] == "decision":
            products = nodes.get("scoring", {}).get("result", {}).get("products", []) if "scoring" in nodes else nodes.get("data", {}).get("result", {}).get("products", [])
            return make_input(task, data={"keyword": task, "products": products}, meta=meta)
        if node["id"] == "execution":
            decision = nodes.get("decision", {}).get("result", {"action": "skip", "keyword": task, "reason": "no decision"})
            return make_input(task, data={"decision": decision}, meta=meta)
        return make_input(task, meta=meta)
