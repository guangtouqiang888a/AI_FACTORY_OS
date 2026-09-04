# 10_DEPLOY/logger.py — 请求与延迟日志

import logging
import sys
from pathlib import Path

from deploy_config import DEPLOY_LOG_DIR, LOG_LEVEL, SERVICE_NAME

DEPLOY_LOG_DIR.mkdir(parents=True, exist_ok=True)

_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_file_handler = logging.FileHandler(DEPLOY_LOG_DIR / "requests.log", encoding="utf-8")
_file_handler.setFormatter(_formatter)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(_formatter)

logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
if not logger.handlers:
    logger.addHandler(_file_handler)
    logger.addHandler(_console_handler)


def log_request(method: str, path: str, task: str | None, latency_ms: float, status: str) -> None:
    logger.info(
        "request method=%s path=%s task=%s latency_ms=%.2f status=%s",
        method,
        path,
        task or "-",
        latency_ms,
        status,
    )


def log_error(method: str, path: str, error: str, latency_ms: float) -> None:
    logger.error(
        "error method=%s path=%s error=%s latency_ms=%.2f",
        method,
        path,
        error,
        latency_ms,
    )
