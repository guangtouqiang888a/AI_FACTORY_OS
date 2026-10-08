# 10_DEPLOY — Deployment Layer

AI Factory OS 的外部 HTTP 部署包装层，**不修改核心 OS 架构**。

## 架构

```
HTTP Client → 10_DEPLOY/api.py → service.py → 0_START/controller.run()
                                              ↓
                    Planner → PolicyEngine → ExecutionRuntime → Memory
```

## 本地运行

```powershell
cd D:\AI_FACTORY_OS
pip install -r requirements.txt
pip install -r 10_DEPLOY/requirements.txt
cd 10_DEPLOY
python api.py
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/status` | 服务状态 + metrics |
| POST | `/run` | 执行任务 |

### POST /run

```json
{"task": "虚拟资料"}
```

响应（统一协议）：

```json
{
  "code": 200,
  "message": "ok",
  "data": {
    "task": "虚拟资料",
    "result": "最高分 82.91 — PPT模板打包",
    "score": 82.91,
    "status": "publish"
  },
  "meta": {
    "latency": 0.534,
    "request_id": "abc123..."
  }
}
```

执行链追踪写入 `logs/deploy/trace.jsonl`（planner / policy / execution_hash / memory）。

## Docker

```powershell
cd D:\AI_FACTORY_OS\10_DEPLOY
docker compose up --build
```

## 环境变量（`deploy_config.py`）

| 变量 | 默认 | 说明 |
|------|------|------|
| DEPLOY_PORT | 8080 | HTTP 端口 |
| DEPLOY_HOST | 0.0.0.0 | 绑定地址 |
| DEPLOY_LOG_LEVEL | INFO | 日志级别 |
