# 11_CONTENT_FACTORY/adapter — Production Request → Content Factory 隔离 Adapter 层

from .adapter_runner import run_adapter
from .approval_gate import ApprovalGate, ApprovalGateError
from .input_mapper import map_production_request_to_input
from .output_mapper import map_pipeline_result_to_product_asset
from .production_request_loader import ProductionRequestLoader

__all__ = [
    "ApprovalGate",
    "ApprovalGateError",
    "ProductionRequestLoader",
    "map_pipeline_result_to_product_asset",
    "map_production_request_to_input",
    "run_adapter",
]
