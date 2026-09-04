# 1_DATA/collector.py — 数据采集 + DataAgent（标准化接口）
#
# Entry 058B–058D Reality:
# - XianyuCollector = EXTERNAL_IMPORT facade (B), NOT Live Collector
# - Architecture: Source → Acquisition Adapter → Raw → Normalizer → MarketObservation
# - LIVE_API / LIVE_COLLECTION = NOT_AVAILABLE_CURRENTLY (no project eligibility)
# - discovery platform must NOT auto-bind sales_platform

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for layer in ("8_CONFIG", "1_DATA", "0_START"):
    p = str(ROOT / layer)
    if p not in sys.path:
        sys.path.insert(0, p)

import acquisition_capability as acq  # noqa: E402
import collector_abstraction as cab  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
from agent_runtime import BaseAgent  # noqa: E402
from connectors.xianyu_import_connector import (  # noqa: E402
    IMPORTS_DIR,
    import_readiness,
)
from os_protocol import make_output  # noqa: E402


class XianyuCollector:
    """
    Compatibility facade over collector_abstraction.

    Reality (058D evidence):
    - collect_from_excel / collect → MANUAL_IMPORT / USER_EXPORT only
    - live_collect → fails honestly (NOT Live Collector)
    - Definition: B. External Import (not A Live, not C both)
    """

    platform_id = 1
    platform_name = "xianyu"
    discovery_platform = "xianyu"
    sales_platform = None  # NEVER auto-bound
    collector_kind = "EXTERNAL_IMPORT"
    acquisition_modes = [acq.MODE_USER_EXPORT, acq.MODE_MANUAL_IMPORT]

    def __init__(self):
        database.ensure_schema()
        msc.ensure_market_source_schema()

    def collect_from_excel(
        self,
        keyword: str = "",
        *,
        declared_origin: str = msc.ORIGIN_UNKNOWN,
        collection_query: str | None = None,
    ) -> dict:
        """EXTERNAL_IMPORT — keyword/collection_query is topic, not source=platform."""
        query = collection_query if collection_query is not None else keyword
        result = cab.run_acquisition(
            acquisition_mode=acq.MODE_MANUAL_IMPORT,
            collection_query=query,
            declared_origin=declared_origin,
        )
        # Normalize legacy keys for callers
        if result.get("error") == "no_import_files":
            return {
                "total": 0,
                "valid": 0,
                "files": 0,
                "collection_mode": msc.MODE_IMPORT,
                "acquisition_mode": acq.MODE_MANUAL_IMPORT,
                "collection_query": query,
                "status": "FAILED",
                "error": "no_import_files",
                "imports_dir": str(IMPORTS_DIR),
                "live_collection": msc.live_collection_status(),
                "readiness": import_readiness(),
                "note": (
                    "Place a real user-exported xlsx/csv/json under data/raw/xianyu/imports/. "
                    "Legacy sample.xlsx is rejected. LIVE_API unavailable for this project."
                ),
                "sales_platform": None,
                "discovery_platform": "xianyu",
            }
        return {
            "total": result.get("total", 0),
            "valid": result.get("valid", 0),
            "files": len(result.get("runs") or []),
            "runs": result.get("runs"),
            "collection_mode": msc.MODE_IMPORT,
            "acquisition_mode": result.get("acquisition_mode"),
            "collection_query": query,
            "status": result.get("status"),
            "ok": result.get("ok"),
            "live_collection": msc.live_collection_status(),
            "sales_platform": None,
            "discovery_platform": "xianyu",
            "adapter_id": result.get("adapter_id"),
        }

    def collect(
        self,
        keyword: str = "",
        *,
        declared_origin: str = msc.ORIGIN_UNKNOWN,
        collection_query: str | None = None,
    ) -> dict:
        result = self.collect_from_excel(
            keyword, declared_origin=declared_origin, collection_query=collection_query
        )
        if result.get("valid", 0) == 0 and result.get("total", 0) == 0:
            result["from_db"] = len(
                database.get_products_by_keyword(
                    collection_query or keyword or ""
                )
            )
            result["observations"] = msc.count_observations()
        return result

    def live_collect(self, keyword: str = "", *, collection_query: str | None = None) -> dict:
        """Explicitly unavailable — compliance + eligibility boundary."""
        query = collection_query if collection_query is not None else keyword
        return cab.run_acquisition(
            acquisition_mode=acq.MODE_LIVE_API,
            collection_query=query,
            declared_origin=msc.ORIGIN_UNKNOWN,
        )


# Back-compat alias
XianyuImportConnector = XianyuCollector


class DataAgent(BaseAgent):
    role = "data_collector"
    tools = ["XianyuCollector", "database.get_products_by_keyword"]
    memory_scope = "1_DATA"

    def execute(self, input_data: dict, context: dict) -> dict:
        task = input_data["task"]
        data = input_data.get("data") or {}
        keyword = data.get("keyword", task)
        collection_query = data.get("collection_query", keyword)
        declared_origin = data.get("declared_origin", msc.ORIGIN_UNKNOWN)
        logs: list[str] = []
        try:
            collector = XianyuCollector()
            data_result = collector.collect(
                keyword,
                declared_origin=declared_origin,
                collection_query=collection_query,
            )
            products = database.get_products_by_keyword(collection_query or keyword)
            logs.append(
                f"import valid={data_result.get('valid', 0)} "
                f"obs={msc.count_observations()} products={len(products)} "
                f"live={msc.LIVE_COLLECTION_AVAILABLE} "
                f"query={collection_query}"
            )
            return make_output(
                "ok" if data_result.get("status") not in ("FAILED", None) or data_result.get("ok") else "error",
                {
                    "keyword": keyword,
                    "collection_query": collection_query,
                    "data_result": data_result,
                    "products": products,
                    "product_count": len(products),
                    "observation_count": msc.count_observations(),
                    "sales_platform": None,
                    "discovery_platform": "xianyu",
                    "acquisition_capability": acq.capability_snapshot()["recommended_acquisition_mode"],
                },
                logs=logs,
            )
        except Exception as exc:
            logs.append(str(exc))
            return make_output("error", {"keyword": keyword, "error": str(exc)}, logs=logs)
