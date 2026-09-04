# AI_FACTORY_OS Broken Entry Report

> Entry 038-B | Broken Entry Assessment | 2026-07-13  
> **本 Entry 不修复代码。**

---

## BE-001 — 0_START/self_healing_engine.py

### 问题

| 项 | 详情 |
|----|------|
| **文件** | `0_START/self_healing_engine.py` |
| **错误类型** | Python 语法错误 + API 不存在 |
| **问题行** | `from 7_MEMORY.memory_core import write_memory` |

**语法：** 模块名 `7_MEMORY` 以数字开头，**非法 Python import 路径**。

**API：** `memory_core.py` **无** `write_memory()` 函数。可用 API 为 `write_event()`, `log_event()`。

### 影响

| 影响域 | 说明 |
|--------|------|
| 可运行性 | `python self_healing_engine.py` **无法启动** |
| 架构 | 文件声称「自愈系统内核 v1.0」，与 Core OS 主链无集成 |
| 误导 | 可能被误认为 Active 入口（存在 `__main__` 块） |
| 主链 | **不影响** `main.py` / `SystemController` / `10_DEPLOY` |

### 修复建议（供未来 Entry）

| 选项 | 操作 | 风险 |
|------|------|------|
| A — 最小修复 | 改为 `sys.path` + `import memory_core` + `write_event` | 低 |
| B — 归档 | 移至 `docs/archive/` 或标注 Deprecated | 无 runtime 影响 |
| C — 重写 | 对接 SelfEvolutionEngine / execution hash 做真实 healing loop | 中 — 需设计 Entry |

**推荐：** 选项 B（归档）或 A（最小修复）— 须单独 Entry 授权修改 Python。

---

## BE-002 — 9_PRODUCT/api_server.py

### 问题

| 项 | 详情 |
|----|------|
| **文件** | `9_PRODUCT/api_server.py` |
| **错误类型** | Python 语法错误 |
| **问题行** | `from 0_START.controller import SystemController` |

**语法：** 模块名 `0_START` 以数字开头，**非法 import**。

### 影响

| 影响域 | 说明 |
|--------|------|
| 可运行性 | 无法 import 或启动 FastAPI app |
| 重复入口 | 与 `10_DEPLOY/api.py` 功能重叠 |
| 状态误导 | `GET /status` 返回 `"state": "production_ready"` — 与项目阶段不符 |
| 主链 | **不影响** — `10_DEPLOY/service.py` 为实际 HTTP 入口 |

### 修复建议（供未来 Entry）

| 选项 | 操作 | 风险 |
|------|------|------|
| A — 删除/归档 | MODULE_REGISTRY 已标 9_PRODUCT Frozen | 低 |
| B — 修复 import | 使用 `sys.path.insert` + `from controller import SystemController` | 低 — 但仍与 10_DEPLOY 重复 |
| C — 重定向文档 | 明确「使用 10_DEPLOY/api.py」 | 无代码变更 |

**推荐：** 选项 C + A — 文档指向 10_DEPLOY；api_server.py 归档或删除（须 Entry 授权）。

---

## 对比：有效入口

| 入口 | 文件 | 状态 |
|------|------|------|
| Core CLI | `0_START/main.py` | ✅ Active |
| HTTP API | `10_DEPLOY/api.py` | ✅ Active |
| CF Legacy | `11_CONTENT_FACTORY/pipeline/content_pipeline.py` | ✅ Active |
| CF Adapter | `11_CONTENT_FACTORY/adapter/adapter_runner.py` | ✅ Active |
| Self Healing | `0_START/self_healing_engine.py` | ❌ Broken |
| 9_PRODUCT API | `9_PRODUCT/api_server.py` | ❌ Broken |

---

## 与 Unified Architecture 关系

- Broken entries 位于 **Legacy / Frozen** 层，不参与目标统一链
- 收敛时应 **避免修复后引入第三 API 入口** — 统一经 10_DEPLOY

---

## 本 Entry 操作

- ✅ 评估并文档化
- ❌ 未修改 Python 文件
