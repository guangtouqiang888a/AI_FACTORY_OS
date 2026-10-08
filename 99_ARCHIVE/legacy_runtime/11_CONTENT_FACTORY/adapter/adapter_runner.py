# 11_CONTENT_FACTORY/adapter/adapter_runner.py — Adapter 主入口 CLI

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FACTORY_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = FACTORY_ROOT.parent
sys.path.insert(0, str(FACTORY_ROOT / "pipeline"))
sys.path.insert(0, str(FACTORY_ROOT / "adapter"))

from approval_gate import ApprovalGate, ApprovalGateError  # noqa: E402
from input_mapper import map_production_request_to_input  # noqa: E402
from output_mapper import map_pipeline_result_to_product_asset  # noqa: E402
from production_request_loader import ProductionRequestLoader  # noqa: E402
from content_pipeline import ContentPipeline  # noqa: E402


def run_adapter(
    production_request_id: str,
    *,
    dry_run: bool = True,
    pilot_only: bool = True,
) -> dict:
    """
    Adapter 编排：load → gate → map → pipeline → output asset draft。

    Entry 032-B 默认 dry_run=True — 不生成商业交付文件。
    """
    loader = ProductionRequestLoader()
    gate = ApprovalGate(pilot_only=pilot_only)

    loaded = loader.load_input_package(production_request_id)
    gate_result = gate.validate(loaded)
    input_package = map_production_request_to_input(loaded)

    pipeline = ContentPipeline()
    pipeline_result = pipeline.run_from_production_request(input_package, dry_run=dry_run)

    product_asset_draft = map_pipeline_result_to_product_asset(input_package, pipeline_result)

    return {
        "adapter_status": "ok" if pipeline_result.get("status") in ("ok", "dry_run") else "error",
        "gate": gate_result,
        "input_package": input_package,
        "pipeline_result": pipeline_result,
        "product_asset_draft": product_asset_draft,
        "dry_run": dry_run,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Content Factory Adapter — Production Request → Pipeline")
    parser.add_argument("--preq", required=True, help="production_request_id (Pilot: preq_20260712_005)")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run full production pipeline (generates files). Entry 032-B forbids by default.",
    )
    parser.add_argument(
        "--no-pilot-gate",
        action="store_true",
        help="Disable Pilot whitelist (not recommended)",
    )
    args = parser.parse_args()

    dry_run = not args.execute

    print("=" * 60)
    print("11_CONTENT_FACTORY Adapter — Production Request Entry")
    print("=" * 60)
    print(f"[Input] production_request_id={args.preq}")
    print(f"[Mode] dry_run={dry_run} (Adapter Completed ≠ Production Started)\n")

    try:
        result = run_adapter(
            args.preq,
            dry_run=dry_run,
            pilot_only=not args.no_pilot_gate,
        )
    except ApprovalGateError as exc:
        print(f"[GATE BLOCKED] {exc.code}: {exc.message}")
        sys.exit(2)
    except KeyError as exc:
        print(f"[LOAD ERROR] {exc}")
        sys.exit(3)
    except FileNotFoundError as exc:
        print(f"[FILE ERROR] {exc}")
        sys.exit(4)

    if result["adapter_status"] == "ok":
        draft = result["product_asset_draft"]
        print(f"[Gate] passed approval_id={result['gate'].get('approval_id')}")
        print(f"[Pipeline] status={result['pipeline_result'].get('status')}")
        print(f"[Product Asset Draft] id={draft.get('product_asset_id')}")
        print(f"[Product Asset Draft] generation_status={draft.get('generation_status')}")
        print(f"[Product Asset Draft] creation_method={draft.get('creation_method')}")
        print("\n[OK] Adapter pipeline complete (Code Completed ≠ Commercial Asset Created)")
    else:
        print(f"[ERROR] pipeline failed at {result['pipeline_result'].get('failed_step')}")
        print(json.dumps(result["pipeline_result"], ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
