# 0_START/main.py — Production Grade 四层 AI OS 入口

import io
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "0_START"))

from controller import SystemController  # noqa: E402


def main():
    ctrl = SystemController()
    boot = ctrl.boot()

    print("=" * 60)
    print(f"Production Grade AI OS {boot['version']}")
    print("=" * 60)
    print(f"[Layers] {' → '.join(boot['layers'])}")
    print(f"[Hardening] policy_core_lock={boot['policy_core_lock']} deterministic={boot['deterministic_mode']}")
    print(f"[Policy] mode={boot['policy'].get('mode')} budget_ceiling={boot['policy'].get('llm_cost_budget')}")
    print(f"[Allowlist] {boot['policy'].get('executor_allowlist')}")
    print(f"[Memory] patterns={boot['pattern_count']} rules={boot['strategy_rules']}")

    task = sys.argv[1] if len(sys.argv) > 1 else "虚拟资料"
    print(f"\n[Task] {task}")
    result = ctrl.run(task)

    dag = result["dag"]
    print("\n--- DAG (Planner) ---")
    print(f"nodes: {[n['id'] for n in dag['nodes']]}")
    for n in dag["nodes"]:
        p = n.get("policy", {})
        print(f"  [{n['id']}] executor={p.get('executor')} mode={p.get('mode')}")

    print("\n--- Execution (deterministic + hash) ---")
    for nid, nr in result["node_results"].items():
        eh = result.get("execution_hashes", {}).get(nid, "-")
        print(f"  [{nid}] status={nr['status']} executor={nr['executor']} hash={eh}")

    print("\n--- Scoring / Decision ---")
    print(f"  scoring: count={result['scoring']['count']} score={result['scoring'].get('score')}")
    dec = result["decision"]
    print(f"  decision: action={dec.get('action')} reason={dec.get('reason')}")

    print("\n--- Memory (confidence filtered) ---")
    pat = result["memory"]["pattern"]
    print(f"  pattern: outcome={pat.get('outcome')} confidence={pat.get('confidence')} score={pat.get('score')}")
    if result["memory"].get("strategy_skipped"):
        print("  strategy_update: SKIPPED (low confidence)")
    evo = result.get("evolution", {})
    if evo.get("patch"):
        print(f"  policy_patch: {json.dumps(evo['patch'], ensure_ascii=False)}")

    print(f"\n>>> Final Action: {result['final_action']} <<<")
    print("=" * 60)
    print("[OK] Production Grade pipeline complete")


if __name__ == "__main__":
    main()
