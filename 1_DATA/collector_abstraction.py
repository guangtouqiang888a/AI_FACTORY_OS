# 1_DATA/collector_abstraction.py — Entry 058D
#
# Source → Acquisition Adapter → Raw → Normalizer → MarketObservation
# XianyuCollector remains a compatibility facade over this layer.
# Discovery Source ≠ Sales Platform. Observation ≠ Product/Listing/Event.

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import acquisition_capability as acq  # noqa: E402
import market_source_core as msc  # noqa: E402
from connectors import xianyu_import_connector as xic  # noqa: E402

COLLECTOR_ABSTRACTION_VERSION = "058d.1.0"


@dataclass
class MarketSourceDesc:
    source_id: str
    source_type: str
    platform: str
    enabled: bool
    acquisition_modes: list[str] = field(default_factory=list)
    sales_platform: str | None = None  # ALWAYS None at source layer


class AcquisitionAdapter(Protocol):
    adapter_id: str
    source_id: str
    acquisition_mode: str

    def acquire(self, *, collection_query: str = "", declared_origin: str = "UNKNOWN") -> dict:
        ...


class XianyuImportAdapter:
    """USER_EXPORT / MANUAL_IMPORT — only implemented LIVE path for Xianyu."""

    adapter_id = "adapter_xianyu_import"
    source_id = "src_xianyu_marketplace"
    acquisition_mode = acq.MODE_MANUAL_IMPORT

    def acquire(
        self,
        *,
        collection_query: str = "",
        declared_origin: str = msc.ORIGIN_UNKNOWN,
        path: Path | None = None,
    ) -> dict:
        msc.ensure_market_source_schema()
        msc.ensure_collector_registry()
        if path is not None:
            result = xic.import_file(
                path,
                keyword=collection_query,
                declared_origin=declared_origin,
                collection_mode=msc.MODE_IMPORT,
                allow_sample=False,
                mirror_to_products=False,
                collection_query=collection_query,
                acquisition_mode=acq.MODE_MANUAL_IMPORT
                if path.parent.name == "imports" or "imports" in str(path).replace("\\", "/")
                else acq.MODE_USER_EXPORT,
            )
            return _annotate(result, self)

        files = xic.list_import_candidates()
        if not files:
            ready = xic.import_readiness()
            return {
                "ok": False,
                "status": ready.get("status", "WAITING_FOR_REAL_SOURCE_FILE"),
                "acquisition_mode": self.acquisition_mode,
                "collection_mode": msc.MODE_IMPORT,
                "collection_query": collection_query,
                "discovery_platform": "xianyu",
                "sales_platform": None,
                "error": "no_import_files",
                "readiness": ready,
                "adapter_id": self.adapter_id,
            }

        runs = []
        total = valid = 0
        for fp in files:
            mode = acq.MODE_MANUAL_IMPORT
            r = xic.import_file(
                fp,
                keyword=collection_query,
                declared_origin=declared_origin,
                collection_mode=msc.MODE_IMPORT,
                allow_sample=False,
                mirror_to_products=False,
                collection_query=collection_query,
                acquisition_mode=mode,
            )
            runs.append(r)
            stats = r.get("stats") or {}
            total += int(stats.get("raw_count") or 0)
            valid += int(stats.get("accepted_count") or 0)

        return _annotate(
            {
                "ok": valid > 0,
                "status": "done" if valid else "WAITING_OR_ZERO_ACCEPTED",
                "runs": runs,
                "total": total,
                "valid": valid,
                "collection_query": collection_query,
                "collection_mode": msc.MODE_IMPORT,
                "acquisition_mode": self.acquisition_mode,
                "discovery_platform": "xianyu",
                "sales_platform": None,
            },
            self,
        )


class XianyuBrowserAdapter:
    """PUBLIC_WEB_READ via browser render — Entry 060 Source Adapter."""

    adapter_id = "adapter_xianyu_browser"
    source_id = "src_xianyu_marketplace"
    acquisition_mode = "PUBLIC_WEB_READ"

    def acquire(
        self,
        *,
        collection_query: str = "",
        declared_origin: str = msc.ORIGIN_REAL,
        max_records: int = 20,
        path: Path | None = None,
    ) -> dict:
        from connectors.xianyu_browser_connector import XianyuBrowserCollector

        result = XianyuBrowserCollector().acquire(
            collection_query=collection_query,
            max_records=max_records,
            declared_origin=declared_origin or msc.ORIGIN_REAL,
        )
        return _annotate(result, self)


class XianyuLiveApiAdapter:
    """LIVE_API — honestly unavailable for this project (no eligibility)."""

    adapter_id = "adapter_xianyu_live_api"
    source_id = "src_xianyu_marketplace"
    acquisition_mode = acq.MODE_LIVE_API

    def acquire(self, *, collection_query: str = "", declared_origin: str = "UNKNOWN") -> dict:
        elig = acq.current_eligibility()
        official = acq.xianyu_official_capability()
        return {
            "ok": False,
            "status": "FAILED",
            "error": "live_collection_not_available",
            "error_detail": "live_api_not_available_currently",
            "classification": elig["classification"],
            "acquisition_mode": self.acquisition_mode,
            "collection_mode": msc.MODE_LIVE,
            "collection_query": collection_query,
            "discovery_platform": "xianyu",
            "sales_platform": None,
            "access_requirements": elig["access_requirements"],
            "official_status_market_observation": official[
                "status_for_ai_factory_market_observation"
            ],
            "adapter_id": self.adapter_id,
            "forbidden": sorted(acq.FORBIDDEN_MODES),
            **msc.live_collection_status(),
        }


def xianyu_source() -> MarketSourceDesc:
    return MarketSourceDesc(
        source_id="src_xianyu_marketplace",
        source_type="marketplace",
        platform="xianyu",
        enabled=True,
        acquisition_modes=[
            acq.MODE_USER_EXPORT,
            acq.MODE_MANUAL_IMPORT,
            "PUBLIC_WEB_READ",
        ],
        sales_platform=None,
    )


def get_adapter(acquisition_mode: str) -> AcquisitionAdapter:
    if acquisition_mode in (acq.MODE_USER_EXPORT, acq.MODE_MANUAL_IMPORT):
        return XianyuImportAdapter()
    if acquisition_mode == "PUBLIC_WEB_READ":
        return XianyuBrowserAdapter()
    if acquisition_mode in (acq.MODE_LIVE_API, acq.MODE_PARTNER_API):
        return XianyuLiveApiAdapter()
    raise ValueError(f"unsupported_or_forbidden_mode:{acquisition_mode}")


def run_acquisition(
    *,
    acquisition_mode: str = acq.MODE_MANUAL_IMPORT,
    collection_query: str = "",
    declared_origin: str = msc.ORIGIN_UNKNOWN,
    max_records: int = 20,
) -> dict:
    """
    Orchestration: Source → Adapter → (Raw/Normalize inside adapter) → Observation.
    Does not run Opportunity / Scoring / CF / Learning.
    """
    if acquisition_mode in acq.FORBIDDEN_MODES:
        return {
            "ok": False,
            "status": "FAILED",
            "error": "forbidden_acquisition_mode",
            "mode": acquisition_mode,
        }
    source = xianyu_source()
    adapter = get_adapter(acquisition_mode)
    if acquisition_mode == "PUBLIC_WEB_READ":
        result = adapter.acquire(
            collection_query=collection_query,
            declared_origin=declared_origin or msc.ORIGIN_REAL,
            max_records=max_records,
        )
    else:
        result = adapter.acquire(
            collection_query=collection_query,
            declared_origin=declared_origin,
        )
    result["source"] = {
        "source_id": source.source_id,
        "platform": source.platform,
        "source_type": source.source_type,
        "sales_platform": None,
    }
    result["collector_abstraction_version"] = COLLECTOR_ABSTRACTION_VERSION
    result["query_note"] = "collection_query is search/topic — not equal to source platform"
    return result


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _annotate(result: dict, adapter: AcquisitionAdapter) -> dict:
    result = dict(result)
    result.setdefault("adapter_id", adapter.adapter_id)
    result.setdefault("acquisition_mode", adapter.acquisition_mode)
    result.setdefault("sales_platform", None)
    result.setdefault("discovery_platform", "xianyu")
    result["product_created"] = False
    result["listing_created"] = False
    result["market_event_created"] = False
    result["opportunity_discovery_run"] = False
    return result
