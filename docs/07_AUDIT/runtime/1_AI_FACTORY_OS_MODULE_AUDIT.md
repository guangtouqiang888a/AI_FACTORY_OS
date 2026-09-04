# AI_FACTORY_OS Module Audit

> Entry 038-A — Full System Audit v1 | 审计日期：2026-07-13  
> **方法：** 只读扫描代码、文件、JSON、Database；不假设文档等于实现。

---

## Module Inventory

---

### 模块：0_START

**名称：** Core Runtime Layer（系统启动与编排内核）

**实际文件数量：** 21（含 10 个 `.py`，11 个 `__pycache__` 产物）

**入口文件：**
- `0_START/main.py` — CLI 主入口（`python main.py [task]`）
- `0_START/self_healing_engine.py` — 自愈演示（**语法错误，不可运行**）

**实际职责（代码）：**
- `SystemController`：Planner → PolicyEngine → ExecutionRuntime → Memory 四层编排
- `SelfEvolutionEngine`：运行前策略演化
- `AgentRegistry`：注册 DataAgent / ScoringAgent / DecisionAgent / ExecutionAgent
- `ModelBridge`：LLM 调用（仅 ExecutionRuntime 内）

**输入：** CLI task 字符串（默认 `"虚拟资料"`）

**输出：** 完整 pipeline result dict（DAG、node results、decision、execution、memory pattern）

**被谁调用：** `10_DEPLOY/service.py` → `SystemController`；`0_START/main.py`

**调用谁：** `1_DATA/database`、`7_MEMORY/memory_core`、`3_DECISION`（经 AgentRegistry）、`6_EXECUTION`（经 AgentRegistry）、`8_CONFIG/config`

**状态：** **Active — Runtime Connected（Core OS 链可运行）**；**未连接** `11_CONTENT_FACTORY` 或 `commercial_assets/`

---

### 模块：1_DATA

**名称：** Data Foundation Layer

**实际文件数量：** 6（3 个 `.py`）

**入口文件：** 无独立 CLI；经 `DataAgent` 被 ExecutionRuntime 调用

**实际职责：**
- `XianyuCollector`：从 `data/raw/xianyu/*.xlsx` 读取闲鱼商品数据
- `database.py`：SQLite CRUD（products, keywords, collection_log, scores）
- `sources.py`：行数据规范化

**输入：** `{task, data: {keyword}}` from ExecutionRuntime

**输出：** `{keyword, products[], data_result, product_count}`

**被谁调用：** `0_START/execution_runtime.py` → `DataAgent`

**调用谁：** `1_DATA/database.py`、`8_CONFIG/config`

**状态：** **Active** — 数据采集存在，**依赖本地 Excel 文件**；无实时 API 抓取

---

### 模块：2_COGNITION

**名称：** Market Intelligence Layer（占位）

**实际文件数量：** 0

**入口文件：** 无

**实际职责：** **未实现**

**输入 / 输出：** 无

**被谁调用：** 无 Python 引用

**调用谁：** 无

**状态：** **Empty Placeholder** — 目录存在，零文件；文档称 Blueprint Completed

---

### 模块：3_DECISION

**名称：** Decision Intelligence Layer

**实际文件数量：** 10（5 个 `.py`）

**入口文件：** 无独立 CLI；经 AgentRegistry 调用

**实际职责：**
- `scorer.py` / `ScoringAgent`：五维评分（hot/trend/comp/profit/difficulty）
- `decision_engine.py` / `DecisionAgent`：风险过滤 + publish/observe/skip
- `risk_engine.py`：风险规则

**输入：** 已采集并评分的 products 列表

**输出：** `{action, reason, candidates, best}`

**被谁调用：** `0_START/execution_runtime.py`

**调用谁：** `1_DATA/database`、`7_MEMORY/memory_core`、`8_CONFIG/config`

**状态：** **Active** — 决策针对 **SQLite 市场商品**，非 commercial_assets Experiment/Opportunity

---

### 模块：4_PRODUCT

**名称：** Product Definition Layer（占位）

**实际文件数量：** 0

**入口文件：** 无

**实际职责：** **未实现**

**状态：** **Empty Placeholder**

---

### 模块：5_CONTENT

**名称：** Content Knowledge Layer（占位）

**实际文件数量：** 0

**入口文件：** 无

**实际职责：** **未实现**

**状态：** **Empty Placeholder**

---

### 模块：6_EXECUTION

**名称：** Execution / Publish Layer

**实际文件数量：** 4（2 个 `.py`）

**入口文件：** 无独立 CLI

**实际职责：** `publisher.publish()` — 本地模拟发布，写 `output/skip_*.json` 或 `output/publish_*.json`

**输入：** decision dict from DecisionAgent

**输出：** `{status: skipped|published_local, path?}`

**被谁调用：** `0_START/execution_runtime.py` → `ExecutionAgent`

**调用谁：** `8_CONFIG/config`

**状态：** **Active** — **Human Assisted 本地模拟**；无真实平台 API

---

### 模块：7_MEMORY

**名称：** System Memory Layer

**实际文件数量：** 10（1 个 `.py` + 6 JSON + 1 JSONL + 1 MD + 1 其他）

**入口文件：** 无 CLI；库模块

**实际职责：**
- `memory_core.py`：pattern/strategy/runtime_policy/event_log/execution_hash 持久化
- JSON 资产：`pattern_memory.json`、`strategy_memory.json`、`runtime_policy.json` 等

**输入：** run context、policy patches、events

**输出：** patterns、strategies、policies

**被谁调用：** `0_START/controller`、`policy_engine`、`execution_runtime`、`3_DECISION`

**调用谁：** `8_CONFIG/config`

**状态：** **Active** — OS 运行时记忆；**与 commercial_assets 隔离**

---

### 模块：8_CONFIG

**名称：** Configuration Layer

**实际文件数量：** 2（1 个 `.py`）

**入口文件：** 无（全局 import）

**实际职责：** 路径、API keys、评分权重、LLM 路由、`ACTIVE_MODULES` 定义

**状态：** **Active** — `ACTIVE_MODULES` 不含 `2_COGNITION`、`11_CONTENT_FACTORY`、`9_PRODUCT`、`10_DEPLOY`

---

### 模块：9_PRODUCT

**名称：** Future Commercial Layer（冻结 stub）

**实际文件数量：** 5（5 个 `.py`）

**入口文件：** `9_PRODUCT/api_server.py`（**语法无效**）

**实际职责：** 早期 SaaS/API 方向 stub；`pricing_engine.calculate_cost()` 独立函数

**被谁调用：** 无有效运行时调用

**调用谁：** 意图调用 `SystemController`（import 失败）

**状态：** **Frozen / Broken** — 未接入主链；被 `10_DEPLOY` 替代

---

### 模块：10_DEPLOY

**名称：** Deployment / API Layer

**实际文件数量：** 17（6 个 `.py` + Docker/requirements/logs）

**入口文件：** `10_DEPLOY/api.py`（FastAPI + uvicorn）

**实际职责：** HTTP wrapper；Service Lock 强制经 `SystemController.run()`

**输入：** `POST /run {task}`、`GET /health`、`GET /status`

**输出：** 统一 API 响应格式

**被谁调用：** 外部 HTTP 客户端

**调用谁：** `0_START/controller.SystemController`

**状态：** **Active（代码可运行）** — 文档 MODULE_REGISTRY 标注 **Frozen**，存在文档/代码状态不一致

---

### 模块：11_CONTENT_FACTORY

**名称：** Digital Product Production Layer

**实际文件数量：** 97（36 个 `.py` + artifacts/templates/storage）

**入口文件：**
- `pipeline/content_pipeline.py` — Legacy keyword CLI
- `adapter/adapter_runner.py` — Production Request Adapter CLI
- `adapter/regression_test_v1.py`、`validation/test_product_asset_validator.py` — 测试

**实际职责：**
- Legacy：`run(keyword)` → Market → Creator → Generator → Quality → Packaging → ReleaseGate
- Adapter：`run_from_production_request()` → 跳过 Market → 同上（experiment path）
- Validation：`ProductAssetValidator`（独立，未接入 adapter_runner）
- Artifact 生成：pptx/xlsx/docx/pdf

**输入：** keyword 或 production_request_id（经 commercial_assets JSON）

**输出：** product dict、artifact paths、product_asset draft dict

**被谁调用：** 独立 CLI；**不被 0_START 调用**

**调用谁：** `commercial_assets/`（只读 PR + Approval）；`11_CONTENT_FACTORY/storage/product_memory.json`（写入）

**状态：** **Active — Runtime Connected（CF 独立链）**；Pilot 仅 `preq_20260712_005` 白名单

---

## Summary Table

| 模块 | 文件数 | Python | 入口 | 运行时状态 |
|------|--------|--------|------|------------|
| 0_START | 21 | 10 | main.py | Active |
| 1_DATA | 6 | 3 | Agent | Active |
| 2_COGNITION | 0 | 0 | — | Empty |
| 3_DECISION | 10 | 5 | Agent | Active |
| 4_PRODUCT | 0 | 0 | — | Empty |
| 5_CONTENT | 0 | 0 | — | Empty |
| 6_EXECUTION | 4 | 2 | Agent | Active |
| 7_MEMORY | 10 | 1 | Library | Active |
| 8_CONFIG | 2 | 1 | Import | Active |
| 9_PRODUCT | 5 | 5 | Broken API | Frozen |
| 10_DEPLOY | 17 | 6 | api.py | Active |
| 11_CONTENT_FACTORY | 97 | 36 | 2 CLI | Active (isolated) |

---

## 审计结论

1. **双轨架构确认：** Core OS（0→1→3→6→7）与 Content Factory（11 + commercial_assets）**代码层面无 import 连接**。
2. **三个空模块：** `2_COGNITION`、`4_PRODUCT`、`5_CONTENT` 零实现。
3. **两个损坏入口：** `9_PRODUCT/api_server.py`、`0_START/self_healing_engine.py`。
4. **ACTIVE_MODULES** 仅覆盖 Core OS 六模块，不含 CF 与商业 JSON 链。
