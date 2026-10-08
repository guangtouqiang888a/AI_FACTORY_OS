# 10_DEPLOY/deploy_config.py — Deployment Layer production config

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HOST = os.getenv("DEPLOY_HOST", "0.0.0.0")
PORT = int(os.getenv("DEPLOY_PORT", "8080"))
WORKERS = int(os.getenv("DEPLOY_WORKERS", "1"))
LOG_LEVEL = os.getenv("DEPLOY_LOG_LEVEL", "INFO")

SERVICE_NAME = os.getenv("DEPLOY_SERVICE_NAME", "ai-factory-os")
SERVICE_VERSION = os.getenv("DEPLOY_SERVICE_VERSION", "deploy-v1")

DEPLOY_LOG_DIR = ROOT / "logs" / "deploy"
DEPLOY_METRICS_FILE = DEPLOY_LOG_DIR / "metrics.json"
DEPLOY_TRACE_FILE = DEPLOY_LOG_DIR / "trace.jsonl"

REQUEST_TIMEOUT = int(os.getenv("DEPLOY_REQUEST_TIMEOUT", "120"))
CORS_ORIGINS = os.getenv("DEPLOY_CORS_ORIGINS", "*").split(",")
