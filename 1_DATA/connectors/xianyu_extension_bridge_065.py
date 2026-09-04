# 1_DATA/connectors/xianyu_extension_bridge_065.py — Entry 065
#
# Localhost HTTP bridge: Extension → Acquisition Engine → test sink (Raw/Normalize preview).
# TEST_MODE default: writes 1_DATA/_tests/xianyu_extension_065/ — no Current DB observations.
# No login / cookie / captcha bypass / hidden API.

from __future__ import annotations

import hashlib
import json
import re
import sys
import threading
import uuid
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import market_source_core as msc  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402

COLLECTOR_VERSION = "065.1.0"
COLLECTOR_ID = "col_xianyu_browser_extension"
ADAPTER_VERSION = "065.1.0"
CONTRACT_VERSION = "064.1.0"
SOURCE_ID = "src_xianyu_marketplace"
SOURCE = "xianyu"
PLATFORM = "xianyu"
MODE = "BROWSER_EXTENSION"

BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 8765
BRIDGE_PATH = "/acquisition/v1/market-record-batch"
MAX_PAYLOAD_BYTES = 2 * 1024 * 1024
REQUEST_TIMEOUT_SEC = 30

ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_extension_065"
TZ_CN = timezone(timedelta(hours=8))

WANT_STATUSES = frozenset(
    {
        ts062.WANT_VISIBLE_ON_CARD,
        ts062.WANT_MISSING_ON_CARD,
        ts062.WANT_AVAILABLE_ON_DETAIL,
        ts062.WANT_UNAVAILABLE,
        ts062.WANT_UNKNOWN,
    }
)
ORIGIN_STATUSES = frozenset(
    {ts062.ORIGIN_SEARCH, ts062.ORIGIN_RECOMMENDED, ts062.ORIGIN_UNKNOWN}
)
RUN_STATUSES = frozenset(
    {
        "SUCCESS",
        "PARTIAL",
        "NO_RESULTS",
        "ACCESS_BLOCKED",
        "PAGE_STRUCTURE_CHANGED",
        "UNKNOWN",
    }
)

BUSINESS_FIELDS_FORBIDDEN = frozenset(
    {
        "opportunity_score",
        "commercial_score",
        "profit_score",
        "business_model",
        "commercial_success",
        "product_id",
        "sales_platform",
    }
)


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def extension_dir() -> Path:
    return ROOT / "1_DATA" / "browser_extension" / "xianyu"


def validate_batch(payload: dict[str, Any]) -> tuple[bool, list[str], list[str]]:
    """Returns ok, errors, warnings."""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return False, ["payload_not_object"], warnings

    cv = payload.get("contract_version")
    if cv != CONTRACT_VERSION:
        errors.append(f"contract_version_mismatch:{cv}")

    if payload.get("message_type") != "MARKET_RECORD_BATCH":
        errors.append("invalid_message_type")

    for field in ("run_id", "session_id", "source", "platform"):
        if not payload.get(field):
            errors.append(f"missing_{field}")

    if payload.get("source") != SOURCE:
        warnings.append(f"unexpected_source:{payload.get('source')}")

    records = payload.get("records")
    if not isinstance(records, list):
        errors.append("records_not_list")
        records = []

    if payload.get("status") not in RUN_STATUSES:
        warnings.append(f"unknown_run_status:{payload.get('status')}")

    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            errors.append(f"record_{i}_not_object")
            continue
        for bf in BUSINESS_FIELDS_FORBIDDEN:
            if bf in rec and rec[bf] is not None:
                errors.append(f"forbidden_field_{bf}_in_record_{i}")
        if rec.get("want_count_status") not in WANT_STATUSES:
            warnings.append(f"record_{i}_want_status:{rec.get('want_count_status')}")
        if rec.get("result_origin") not in ORIGIN_STATUSES:
            warnings.append(f"record_{i}_origin:{rec.get('result_origin')}")
        wc = rec.get("want_count")
        if wc is not None and wc == 0 and rec.get("want_count_status") != ts062.WANT_VISIBLE_ON_CARD:
            warnings.append(f"record_{i}_zero_want_without_visible_status")
        if wc is None and rec.get("want_count") == 0:
            pass  # explicit None OK
        if "password" in json.dumps(rec, ensure_ascii=False).lower():
            errors.append(f"record_{i}_credential_like_content")

    return len(errors) == 0, errors, warnings


def normalize_record(rec: dict[str, Any], batch: dict[str, Any]) -> dict[str, Any]:
    """MarketRecord → MarketObservation candidate (not inserted when test_mode)."""
    source_url = rec.get("source_url")
    source_item_id = rec.get("source_item_id") or msc.extract_source_item_id(source_url)
    if source_url and "/item?id=" in source_url and not source_item_id:
        m = re.search(r"[?&]id=(\d+)", source_url)
        if m:
            source_item_id = m.group(1)

    price = rec.get("price")
    if isinstance(price, str):
        try:
            price = float(re.sub(r"[^\d.]", "", price) or "nan")
        except ValueError:
            price = None
        if price != price:  # NaN
            price = None

    want_count = rec.get("want_count")
    if want_count is not None:
        try:
            want_count = int(want_count)
        except (TypeError, ValueError):
            want_count = None

    observed_at = rec.get("observed_at") or batch.get("observed_at") or _now_iso()
    dedupe_key = msc.make_dedupe_key(
        source=SOURCE,
        source_item_id=source_item_id,
        source_url=source_url,
        title=rec.get("title"),
        price=price if isinstance(price, (int, float)) else None,
    )

    return {
        "observation_id": f"mobs_{uuid.uuid4().hex[:12]}",
        "run_id": batch.get("run_id"),
        "source_id": SOURCE_ID,
        "source": SOURCE,
        "platform": PLATFORM,
        "source_type": "marketplace",
        "source_item_id": source_item_id,
        "source_url": source_url,
        "title": rec.get("title"),
        "price": price,
        "currency": rec.get("currency") or "CNY",
        "want_count": want_count,
        "want_count_status": rec.get("want_count_status") or ts062.WANT_UNKNOWN,
        "view_count": rec.get("view_count"),
        "comment_count": rec.get("comment_count"),
        "share_count": rec.get("share_count"),
        "observed_at": observed_at,
        "data_origin": msc.ORIGIN_REAL,
        "verification_status": msc.VERIF_UNVERIFIED,
        "collector_version": rec.get("collector_version") or COLLECTOR_VERSION,
        "normalizer_version": msc.NORMALIZER_VERSION,
        "dedupe_key": dedupe_key,
        "content_hash": hashlib.sha256(
            json.dumps(rec, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()[:24],
        "result_origin": rec.get("result_origin") or batch.get("result_origin"),
        "query": rec.get("query") or batch.get("query"),
        "session_id": rec.get("session_id") or batch.get("session_id"),
        "collection_mode": msc.MODE_LIVE,
        "acquisition_mode": MODE,
        "sales_platform": None,
        "not_our_product": True,
        "not_our_listing": True,
        "candidate_class": "REAL_CANDIDATE_EXTERNAL",
        "valid_without_want_count": True,
        "notes": json.dumps(
            {
                "adapter_version": batch.get("adapter_version", ADAPTER_VERSION),
                "page_state": batch.get("page_state"),
                "filter_metadata": batch.get("filter_metadata"),
            },
            ensure_ascii=False,
        ),
    }


def write_raw_reference(batch: dict[str, Any], run_id: str) -> Path:
    raw_dir = ARTIFACT_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{run_id}.json"
    raw_doc = {
        "acquisition_run_id": run_id,
        "raw_record_id": f"raw_{uuid.uuid4().hex[:12]}",
        "source": SOURCE,
        "timestamp": _now_iso(),
        "payload": batch,
        "collector_version": COLLECTOR_VERSION,
    }
    path.write_text(json.dumps(raw_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def ingest_market_record_batch(
    payload: dict[str, Any],
    *,
    test_mode: bool = True,
) -> dict[str, Any]:
    """
    Validate Extension batch → Raw reference → Normalize preview.
    test_mode=True: test sink only, no market_observations insert.
    """
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    ok, errors, warnings = validate_batch(payload)
    run_id = payload.get("run_id") or f"run_{uuid.uuid4().hex[:12]}"
    request_id = payload.get("request_id") or run_id

    result: dict[str, Any] = {
        "ok": ok,
        "status": "REJECTED" if not ok else (payload.get("status") or "SUCCESS"),
        "run_id": run_id,
        "request_id": request_id,
        "contract_version": CONTRACT_VERSION,
        "test_mode": test_mode,
        "errors": errors,
        "warnings": warnings,
        "records_in": len(payload.get("records") or []),
        "records_normalized": 0,
        "duplicates": 0,
        "sink_path": str(ARTIFACT_DIR),
    }

    if not ok:
        err_log = ARTIFACT_DIR / "errors.log"
        with err_log.open("a", encoding="utf-8") as f:
            f.write(f"{_now_iso()} {run_id} VALIDATION_FAILED {errors}\n")
        (ARTIFACT_DIR / "validation_report.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return result

    raw_path = write_raw_reference(payload, run_id)
    result["raw_reference"] = str(raw_path)

    records = payload.get("records") or []
    normalized: list[dict[str, Any]] = []
    seen_dedupe: set[str] = set()
    duplicates = 0

    for rec in records:
        if not isinstance(rec, dict):
            continue
        cand = normalize_record(rec, payload)
        dk = cand["dedupe_key"]
        if dk in seen_dedupe:
            duplicates += 1
            continue
        seen_dedupe.add(dk)
        normalized.append(cand)

    result["records_normalized"] = len(normalized)
    result["duplicates"] = duplicates

    field_stats = {
        "title": sum(1 for c in normalized if c.get("title")),
        "price": sum(1 for c in normalized if c.get("price") is not None),
        "want_count_visible": sum(
            1 for c in normalized if c.get("want_count_status") == ts062.WANT_VISIBLE_ON_CARD
        ),
        "want_count_missing": sum(
            1 for c in normalized if c.get("want_count_status") == ts062.WANT_MISSING_ON_CARD
        ),
        "source_url": sum(1 for c in normalized if c.get("source_url")),
        "source_item_id": sum(1 for c in normalized if c.get("source_item_id")),
        "search_result": sum(
            1 for c in normalized if c.get("result_origin") == ts062.ORIGIN_SEARCH
        ),
        "recommended_result": sum(
            1 for c in normalized if c.get("result_origin") == ts062.ORIGIN_RECOMMENDED
        ),
    }
    result["field_availability"] = field_stats

    batch_out = {**payload, "ingested_at": _now_iso(), "normalized_count": len(normalized)}
    (ARTIFACT_DIR / "batch.json").write_text(
        json.dumps(batch_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (ARTIFACT_DIR / "normalized_preview.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result["validation_report"] = {
        "run_id": run_id,
        "page_state": payload.get("page_state"),
        "result_origin": payload.get("result_origin"),
        "filter_metadata": payload.get("filter_metadata"),
        "field_availability": field_stats,
        "first_real_search_candidate": (
            field_stats["search_result"] > 0
            and field_stats["title"] > 0
            and field_stats["source_url"] > 0
        ),
    }
    (ARTIFACT_DIR / "validation_report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if not test_mode:
        # Entry 065: explicitly test-dir first; production DB import deferred to Entry 066
        result["db_write"] = "SKIPPED_BY_POLICY_065"

    search_candidates = [
        c for c in normalized if c.get("result_origin") == ts062.ORIGIN_SEARCH
    ]
    result["first_real_candidate_batch"] = len(search_candidates) > 0

    return result


class _BridgeState:
    test_mode: bool = True


def make_handler(state: _BridgeState):
    class BridgeHandler(BaseHTTPRequestHandler):
        server_version = "AIFO-Xianyu-Bridge/065"

        def log_message(self, fmt: str, *args) -> None:
            return

        def _reject(self, code: int, body: dict) -> None:
            raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _accept(self, body: dict) -> None:
            raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_OPTIONS(self) -> None:
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "chrome-extension://*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-AIFO-Contract-Version, X-AIFO-Request-Id")
            self.end_headers()

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path != BRIDGE_PATH:
                self._reject(404, {"error": "not_found"})
                return

            client = self.client_address[0]
            if client not in ("127.0.0.1", "::1"):
                self._reject(403, {"error": "non_localhost_client"})
                return

            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > MAX_PAYLOAD_BYTES:
                self._reject(413, {"error": "payload_size_invalid"})
                return

            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if ctype != "application/json":
                self._reject(415, {"error": "content_type_must_be_json"})
                return

            body_bytes = self.rfile.read(length)
            try:
                payload = json.loads(body_bytes.decode("utf-8"))
            except json.JSONDecodeError:
                self._reject(400, {"error": "invalid_json"})
                return

            if not payload.get("request_id"):
                payload["request_id"] = self.headers.get("X-AIFO-Request-Id") or payload.get("run_id")

            result = ingest_market_record_batch(payload, test_mode=state.test_mode)
            code = 200 if result.get("ok") else 422
            self._accept(result)

    return BridgeHandler


class LocalBridgeServer:
    def __init__(self, *, host: str = BRIDGE_HOST, port: int = BRIDGE_PORT, test_mode: bool = True):
        self.host = host
        self.port = port
        self.test_mode = test_mode
        self._state = _BridgeState()
        self._state.test_mode = test_mode
        self._httpd: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    def start(self, *, blocking: bool = False) -> None:
        handler = make_handler(self._state)
        self._httpd = ThreadingHTTPServer((self.host, self.port), handler)
        if blocking:
            self._httpd.serve_forever()
        else:
            self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
            self._thread.start()

    def stop(self) -> None:
        if self._httpd:
            self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None


def post_batch_to_bridge(payload: dict[str, Any], *, port: int = BRIDGE_PORT) -> dict[str, Any]:
    """Test helper — POST JSON to running bridge."""
    import urllib.error
    import urllib.request

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"http://{BRIDGE_HOST}:{port}{BRIDGE_PATH}",
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-AIFO-Contract-Version": CONTRACT_VERSION,
            "X-AIFO-Request-Id": payload.get("request_id") or payload.get("run_id", "test"),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SEC) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"ok": False, "error": body, "http_status": e.code}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI_FACTORY_OS Xianyu Extension Local Bridge (065)")
    parser.add_argument("--port", type=int, default=BRIDGE_PORT)
    parser.add_argument("--test-mode", action="store_true", default=True)
    args = parser.parse_args()
    srv = LocalBridgeServer(port=args.port, test_mode=args.test_mode)
    print(f"Bridge listening on http://{BRIDGE_HOST}:{args.port}{BRIDGE_PATH}")
    srv.start(blocking=True)
