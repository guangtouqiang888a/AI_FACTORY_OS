# 8_CONFIG/config.py — Production Grade 四层 AI OS 配置

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

ROOT = Path(__file__).resolve().parent.parent
SYSTEM_VERSION = "production-grade-v1"
OS_LAYERS = ("Planner", "PolicyEngine", "ExecutionRuntime", "Memory")

if load_dotenv:
    load_dotenv(ROOT / ".env")

MEMORY_DIR = ROOT / "7_MEMORY"
CORE_MEMORY_PATH = MEMORY_DIR / "PROJECT_CORE_MEMORY.md"
EVENT_LOG_PATH = MEMORY_DIR / "event_log.jsonl"
PATTERN_MEMORY_PATH = MEMORY_DIR / "pattern_memory.json"
STRATEGY_MEMORY_PATH = MEMORY_DIR / "strategy_memory.json"
RUNTIME_POLICY_PATH = MEMORY_DIR / "runtime_policy.json"
POLICY_PATCH_PATH = MEMORY_DIR / "policy_patch.json"
RUNTIME_POLICY_SNAPSHOT_PATH = MEMORY_DIR / "runtime_policy_snapshot.json"
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "ai_factory.db"
RAW_XIANYU_DIR = DATA_DIR / "raw" / "xianyu"
OUTPUT_DIR = ROOT / "output"
LOGS_DIR = ROOT / "logs"
EXECUTION_HASH_LOG_PATH = LOGS_DIR / "execution_hash.log"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SCORE_WEIGHTS = {
    "hot": 0.31,
    "trend": 0.25,
    "competition": 0.19,
    "profit": 0.15,
    "difficulty": 0.10,
}

PUBLISH_SCORE_THRESHOLD = 40
PATTERN_CONFIDENCE_THRESHOLD = 0.6

# LLM 路由（immutable，Self-Evolution 不可修改）
LLM_ROUTING = {"simple": "rule", "medium": "deepseek", "complex": "gpt"}
COMPLEXITY_MAP = {"low": "simple", "mid": "medium", "high": "complex"}
EXECUTOR_ALLOWLIST = ("rule", "deepseek", "gpt")

LLM_COST_BUDGET_CEILING = 0.5
LLM_COST_ESTIMATE = {"rule": 0.0, "deepseek": 0.001, "gpt": 0.01, "gpt-4.1-mini": 0.01}

# Policy Engine 加固
POLICY_CORE_LOCK = True
IMMUTABLE_POLICY_KEYS = frozenset({
    "llm_routing",
    "executor_allowlist",
    "llm_cost_budget",
    "policy_core_lock",
})

# Self-Evolution 仅允许修改
EVOLUTION_ALLOWED_KEYS = frozenset({"mode", "threshold", "weights"})
MAX_CHANGE_RATE = 0.2
COOLDOWN_STEPS = 3
ROLLBACK_FAILURE_RATE = 0.4

# Execution Runtime 加固
DETERMINISTIC_MODE = True

DEFAULT_RUNTIME_POLICY = {
    "mode": "balanced",
    "threshold": PUBLISH_SCORE_THRESHOLD,
    "weights": SCORE_WEIGHTS.copy(),
    "cooldown_remaining": 0,
    "evolution_step": 0,
    "session_llm_cost": 0.0,
    "policy_core_lock": POLICY_CORE_LOCK,
    "llm_routing": LLM_ROUTING.copy(),
    "executor_allowlist": list(EXECUTOR_ALLOWLIST),
    "llm_cost_budget": LLM_COST_BUDGET_CEILING,
}

ACTIVE_MODULES = ("0_START", "1_DATA", "3_DECISION", "6_EXECUTION", "7_MEMORY", "8_CONFIG")
