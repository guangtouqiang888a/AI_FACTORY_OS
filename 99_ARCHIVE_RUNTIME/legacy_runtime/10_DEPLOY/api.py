# 10_DEPLOY/api.py — FastAPI 部署入口（统一 API 协议）

import sys
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

DEPLOY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DEPLOY_DIR))

from deploy_config import CORS_ORIGINS, SERVICE_NAME, SERVICE_VERSION  # noqa: E402
from logger import log_error, log_request  # noqa: E402
from metrics import record_request  # noqa: E402
from service import (  # noqa: E402
    format_health_data,
    format_run_data,
    format_status_data,
    get_boot_info,
    make_api_response,
    new_request_id,
    run_task,
)
from trace import build_trace_entry, write_trace  # noqa: E402

app = FastAPI(
    title="AI Factory OS Deployment API",
    description="External deployment wrapper — all requests go through SystemController.run()",
    version=SERVICE_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=500, description="Task keyword or description")


def _elapsed(started: float) -> float:
    return time.perf_counter() - started


def _json_response(payload: dict, http_status: int = 200) -> JSONResponse:
    return JSONResponse(content=payload, status_code=http_status)


@app.get("/health")
def health():
    request_id = new_request_id()
    started = time.perf_counter()
    boot = get_boot_info()
    latency = _elapsed(started)
    payload = make_api_response(200, "ok", format_health_data(boot), latency, request_id)
    log_request("GET", "/health", None, latency * 1000, "ok")
    return _json_response(payload)


@app.get("/status")
def status():
    request_id = new_request_id()
    started = time.perf_counter()
    data = format_status_data()
    latency = _elapsed(started)
    payload = make_api_response(200, "ok", data, latency, request_id)
    log_request("GET", "/status", None, latency * 1000, "ok")
    return _json_response(payload)


@app.post("/run")
def run_pipeline(body: RunRequest):
    request_id = new_request_id()
    started = time.perf_counter()
    task = body.task.strip()
    try:
        raw = run_task(task)
        latency = _elapsed(started)
        data = format_run_data(raw)
        write_trace(build_trace_entry(request_id, task, raw, latency))
        record_request(latency * 1000, success=True, session_cost=raw.get("session_cost", 0))
        log_request("POST", "/run", task, latency * 1000, data["status"])
        return _json_response(make_api_response(200, "ok", data, latency, request_id))
    except PermissionError as exc:
        latency = _elapsed(started)
        record_request(latency * 1000, success=False)
        log_error("POST", "/run", str(exc), latency * 1000)
        return _json_response(
            make_api_response(403, str(exc), {}, latency, request_id),
            http_status=403,
        )
    except Exception as exc:
        latency = _elapsed(started)
        record_request(latency * 1000, success=False)
        log_error("POST", "/run", str(exc), latency * 1000)
        return _json_response(
            make_api_response(500, str(exc), {}, latency, request_id),
            http_status=500,
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = new_request_id()
    payload = make_api_response(500, str(exc), {}, 0.0, request_id)
    log_error(request.method, request.url.path, str(exc), 0.0)
    return _json_response(payload, http_status=500)


if __name__ == "__main__":
    import uvicorn

    from deploy_config import HOST, PORT

    uvicorn.run("api:app", host=HOST, port=PORT, reload=False)
