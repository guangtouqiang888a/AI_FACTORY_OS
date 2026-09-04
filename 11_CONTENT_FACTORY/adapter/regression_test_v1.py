# 11_CONTENT_FACTORY/adapter/regression_test_v1.py — Entry 032-C Adapter Regression Tests
# Dry Run ≠ Production | Regression Completed ≠ Commercial Launch

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

FACTORY_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = FACTORY_ROOT.parent
sys.path.insert(0, str(FACTORY_ROOT / "pipeline"))
sys.path.insert(0, str(FACTORY_ROOT / "adapter"))
sys.path.insert(0, str(FACTORY_ROOT / "agents"))

PILOT_PREQ = "preq_20260712_005"
BLOCKED_PREQ = "preq_20260712_001"
COMMERCIAL_EXTENSIONS = (".xlsx", ".pptx", ".docx", ".pdf")

_results: list[dict] = []


def _record(test_id: str, name: str, passed: bool, detail: str = "") -> None:
    _results.append({"id": test_id, "name": name, "passed": passed, "detail": detail})
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {test_id}: {name}" + (f" — {detail}" if detail else ""))


def _mock_agent_ok(result: dict):
    mock = MagicMock()
    mock.execute.return_value = {"status": "ok", "result": result, "logs": []}
    return mock


def test_1_legacy_flow_regression() -> None:
    """Test 1 — Legacy run(keyword) exists; market→creator→generator path unchanged; no real generation."""
    from content_pipeline import ContentPipeline

    pipeline = ContentPipeline()
    assert hasattr(pipeline, "run"), "run(keyword) missing"
    assert callable(pipeline.run), "run(keyword) not callable"

    src = inspect.getsource(pipeline.run)
    market_idx = src.index("self.market.execute")
    creator_idx = src.index("self.creator.execute")
    generator_idx = src.index("self.generator.execute")
    assert market_idx < creator_idx < generator_idx, "Legacy agent call order changed"

    product_stub = {
        "id": "regtest_legacy",
        "title": "Legacy Regression",
        "category": "PPT模板",
        "product_type": "PPT模板",
        "market_score": 72.0,
        "platform": "xianyu",
        "status": "draft",
        "created_at": "2026-07-13 00:00:00",
    }
    market_result = {"keyword": "regression-test", "market_score": 72.0, "recommendation": "test"}
    gen_result = {
        "artifact_path": str(FACTORY_ROOT / "artifacts" / "products" / "regtest_legacy"),
        "artifact_files": ["templates/regtest.pptx"],
        "product_type": "PPT模板",
    }

    market_mock = MagicMock(return_value={"status": "ok", "result": market_result, "logs": []})
    creator_mock = MagicMock(return_value={"status": "ok", "result": {"product": product_stub, "artifacts": {}}, "logs": []})
    generator_mock = MagicMock(return_value={"status": "ok", "result": gen_result, "logs": []})

    save_mock = MagicMock()
    with patch.object(pipeline.market, "execute", market_mock), \
         patch.object(pipeline.creator, "execute", creator_mock), \
         patch.object(pipeline.generator, "execute", generator_mock), \
         patch.object(pipeline.quality, "execute", return_value={"status": "ok", "result": {"quality_score": 85, "commercial_score": 85, "status": "quality_pass"}, "logs": []}), \
         patch.object(pipeline.packaging, "execute", return_value={"status": "ok", "result": {"zip_path": ""}, "logs": []}), \
         patch.object(pipeline.release_gate, "execute", return_value={"status": "ok", "result": {"release_status": "ready"}, "logs": []}), \
         patch.object(pipeline, "_save_product", save_mock), \
         patch("content_pipeline.validate_artifacts", return_value={"passed": True, "artifact_files": []}):

        result = pipeline.run("regression-test-keyword")

    market_mock.assert_called_once()
    creator_mock.assert_called_once()
    generator_mock.assert_called_once()
    save_mock.assert_called_once()
    passed = result.get("status") == "ok"
    _record("Test 1", "Legacy Flow Regression", passed, "run(keyword) market→creator→generator (mocked, no files)")


def test_2_adapter_module_import() -> None:
    """Test 2 — Adapter modules import."""
    try:
        from production_request_loader import ProductionRequestLoader  # noqa: F401
        from approval_gate import ApprovalGate, ApprovalGateError  # noqa: F401
        from input_mapper import map_production_request_to_input  # noqa: F401
        from output_mapper import map_pipeline_result_to_product_asset  # noqa: F401
        _record("Test 2", "Adapter Module Import", True, "all modules imported")
    except Exception as exc:
        _record("Test 2", "Adapter Module Import", False, str(exc))


def test_3_approval_gate_positive() -> None:
    """Test 3 — preq_20260712_005 passes gate."""
    from approval_gate import ApprovalGate, ApprovalGateError
    from production_request_loader import ProductionRequestLoader

    loader = ProductionRequestLoader()
    loaded = loader.load_input_package(PILOT_PREQ)
    gate = ApprovalGate(pilot_only=True)

    try:
        result = gate.validate(loaded)
        pr = loaded["production_request"]
        approval = loaded["approval"]
        ok = (
            result["gate_status"] == "passed"
            and pr is not None
            and approval is not None
            and approval.get("decision") == "approved"
            and approval.get("source_production_request_id") == PILOT_PREQ
        )
        _record("Test 3", "Approval Gate Positive (preq_005)", ok, f"approval_id={result.get('approval_id')}")
    except ApprovalGateError as exc:
        _record("Test 3", "Approval Gate Positive (preq_005)", False, exc.code)


def test_4_pilot_whitelist_blocking() -> None:
    """Test 4 — preq_20260712_001 blocked with PILOT_NOT_ALLOWED."""
    from approval_gate import ApprovalGate, ApprovalGateError
    from production_request_loader import ProductionRequestLoader

    loader = ProductionRequestLoader()
    loaded = loader.load_input_package(BLOCKED_PREQ)
    gate = ApprovalGate(pilot_only=True)

    try:
        gate.validate(loaded)
        _record("Test 4", "Pilot Whitelist Blocking (preq_001)", False, "expected PILOT_NOT_ALLOWED")
    except ApprovalGateError as exc:
        ok = exc.code == "PILOT_NOT_ALLOWED"
        _record("Test 4", "Pilot Whitelist Blocking (preq_001)", ok, exc.code)


def test_5_missing_approval_blocking() -> None:
    """Test 5 — in-memory missing approval → NO_APPROVAL (no commercial_assets change)."""
    from approval_gate import ApprovalGate, ApprovalGateError
    from production_request_loader import ProductionRequestLoader

    loader = ProductionRequestLoader()
    loaded = loader.load_input_package(PILOT_PREQ)
    loaded_no_approval = {**loaded, "approval": None}

    gate = ApprovalGate(pilot_only=False)
    try:
        gate.validate(loaded_no_approval)
        _record("Test 5", "Missing Approval Blocking", False, "expected NO_APPROVAL")
    except ApprovalGateError as exc:
        ok = exc.code == "NO_APPROVAL"
        _record("Test 5", "Missing Approval Blocking", ok, exc.code)


def test_6_dry_run() -> None:
    """Test 6 — dry_run: load PR, approval, input package, gate; no Generator / no commercial files."""
    from adapter_runner import run_adapter
    from content_pipeline import ContentPipeline

    artifacts_before = set(FACTORY_ROOT.glob("artifacts/products/**/*"))

    original_run = ContentPipeline.run_from_production_request

    def _tracked_run(self, input_package, *, dry_run=False):
        assert dry_run is True, "Test 6 must use dry_run=True"
        result = original_run(self, input_package, dry_run=dry_run)
        assert result.get("status") == "dry_run", f"expected dry_run status, got {result.get('status')}"
        trace_steps = [t.get("step") for t in result.get("pipeline_trace", [])]
        assert "product_generator" not in trace_steps, "Generator must not run in dry_run"
        return result

    with patch.object(ContentPipeline, "run_from_production_request", _tracked_run):
        result = run_adapter(PILOT_PREQ, dry_run=True, pilot_only=True)

    artifacts_after = set(FACTORY_ROOT.glob("artifacts/products/**/*"))
    new_commercial = [
        p for p in (artifacts_after - artifacts_before)
        if p.suffix.lower() in COMMERCIAL_EXTENSIONS
    ]

    ok = (
        result.get("adapter_status") == "ok"
        and result.get("dry_run") is True
        and result.get("gate", {}).get("gate_status") == "passed"
        and result.get("input_package", {}).get("production_request_id") == PILOT_PREQ
        and result.get("input_package", {}).get("product_name")
        and result.get("pipeline_result", {}).get("status") == "dry_run"
        and len(new_commercial) == 0
    )
    detail = (
        f"gate=passed input={result.get('input_package', {}).get('product_name')} "
        f"pipeline=dry_run new_commercial_files={len(new_commercial)}"
    )
    _record("Test 6", "Dry Run (preq_005)", ok, detail)


def main() -> int:
    print("=" * 60)
    print("Entry 032-C — Content Factory Adapter Regression Test v1")
    print("Dry Run ≠ Production | Regression Completed ≠ Commercial Launch")
    print("=" * 60)

    test_1_legacy_flow_regression()
    test_2_adapter_module_import()
    test_3_approval_gate_positive()
    test_4_pilot_whitelist_blocking()
    test_5_missing_approval_blocking()
    test_6_dry_run()

    passed = sum(1 for r in _results if r["passed"])
    total = len(_results)
    print("=" * 60)
    print(f"SUMMARY: {passed}/{total} PASS")
    for r in _results:
        if not r["passed"]:
            print(f"  FAILED: {r['id']} — {r['detail']}")
    print("=" * 60)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
