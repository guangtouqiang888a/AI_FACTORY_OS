# 0_START/model_bridge.py — Model Bridge（仅 ExecutionRuntime 可调用）

import json
import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
import config  # noqa: E402

_ALLOWED_CALLER = "ExecutionRuntime"


class ModelBridge:
    """所有 LLM 调用必须经过 ModelBridge，且仅 ExecutionRuntime 可实例化调用。"""

    def __init__(self, caller: str = ""):
        if caller != _ALLOWED_CALLER:
            raise PermissionError(
                "ModelBridge 安全锁: 禁止 Agent 直接调用，必须通过 ExecutionRuntime"
            )
        self._caller = caller
        self.deepseek_key = config.DEEPSEEK_API_KEY
        self.deepseek_base = config.DEEPSEEK_BASE_URL.rstrip("/")
        self.deepseek_model = config.DEEPSEEK_MODEL
        self.openai_key = config.OPENAI_API_KEY
        self.openai_model = config.OPENAI_MODEL

    def call_deepseek(self, prompt: str, json_mode: bool = True) -> dict:
        if not self.deepseek_key:
            return {"ok": False, "error": "missing DEEPSEEK_API_KEY", "data": {}}
        url = f"{self.deepseek_base}/chat/completions"
        content = prompt + ("\n\nRespond with valid JSON only." if json_mode else "")
        payload = {
            "model": self.deepseek_model,
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self.deepseek_key}",
            "Content-Type": "application/json",
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=45)
            body = res.json()
            if res.status_code >= 400:
                return {"ok": False, "error": body.get("error", body), "data": {}}
            text = self.extract_text(body)
            parsed = self.parse_json(text) if json_mode else {"text": text}
            return {"ok": True, "engine": "deepseek", "raw": body, "data": parsed}
        except Exception as exc:
            return {"ok": False, "error": str(exc), "data": {}}

    def call_gpt(self, prompt: str, model: str | None = None, json_mode: bool = True) -> dict:
        if not self.openai_key:
            return {"ok": False, "error": "missing OPENAI_API_KEY", "data": {}}
        model = model or self.openai_model
        if model not in config.MODEL_ALLOWLIST and model not in ("gpt-4.1-mini",):
            return {"ok": False, "error": f"model {model} not in allowlist", "data": {}}
        url = "https://api.openai.com/v1/chat/completions"
        content = prompt + ("\n\nRespond with valid JSON only." if json_mode else "")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json",
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=45)
            body = res.json()
            if res.status_code >= 400:
                return {"ok": False, "error": body.get("error", body), "data": {}}
            text = self.extract_text(body)
            parsed = self.parse_json(text) if json_mode else {"text": text}
            return {"ok": True, "engine": model, "raw": body, "data": parsed}
        except Exception as exc:
            return {"ok": False, "error": str(exc), "data": {}}

    @staticmethod
    def extract_text(response: dict) -> str:
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return str(response)

    @staticmethod
    def parse_json(text: str) -> dict:
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", text)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
        return {"raw_text": text, "parsed": False}
