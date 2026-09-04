# Module Boundary Conflict Report

> Entry 038-A | 只读边界冲突分析

---

## Conflict MB-001

**Conflict ID:** MB-001

**涉及模块：** `2_COGNITION` ↔ `11_CONTENT_FACTORY`

**文档定义：**
- `2_COGNITION`：Market Intelligence Layer；Planned Agents: TrendAgent, DemandAgent, CompetitionAgent, OpportunityAgent, InsightAgent（MODULE_REGISTRY §2_COGNITION）
- `11_CONTENT_FACTORY`：Digital Product Production；不负责市场数据发现（MODULE_REGISTRY §11）

**代码实际：**
- `2_COGNITION/`：**空目录，零 Python**
- `11_CONTENT_FACTORY/agents/market_agent.py`：**已实现** `MarketAgent`，基于 keyword 启发式分类，输出 market_score / competition / recommendation
- Legacy pipeline `ContentPipeline.run()` **第一步调用 MarketAgent**
- Experiment path `run_from_production_request()` **跳过 MarketAgent**，使用 JSON market_stub

**潜在风险：**
- 市场认知职责落在 CF 内部 Agent，与 2_COGNITION Blueprint 重叠
- 两套「市场理解」：OS 侧用 SQLite 商品评分；CF 侧用 keyword 规则 — **无统一 Source of Truth**
- 未来实现 2_COGNITION 时可能与 MarketAgent 功能重复或冲突

**建议人工确认：** 是否将 MarketAgent 迁移至 2_COGNITION，或明确 CF MarketAgent 仅为「生产前 stub」而非 Intelligence Layer

---

## Conflict MB-002

**Conflict ID:** MB-002

**涉及模块：** `2_COGNITION` ↔ `3_DECISION`

**文档定义：**
- `2_COGNITION`：market scoring input、opportunity discovery（Blueprint）
- `3_DECISION`：scoring、production decisions；**不负责市场数据发现**（MODULE_REGISTRY §3）

**代码实际：**
- `3_DECISION/scorer.py` 直接对 SQLite products 评分 — **无 2_COGNITION 输入**
- commercial_assets Opportunity/Experiment **不被 3_DECISION 读取**
- CF Adapter 路径 bypass 3_DECISION  entirely

**潜在风险：**
- 商业实验决策链（Opportunity → Experiment → PR）与 OS 决策链（Data → Score → Decide）**完全分离**
- 文档「Decision Intelligence」名称涵盖两套互不连通的决策语义

**建议人工确认：** Commercial Decision 是否应独立于 OS Decision，并在文档中显式拆分命名

---

## Conflict MB-003

**Conflict ID:** MB-003

**涉及模块：** `4_PRODUCT` ↔ `9_PRODUCT` ↔ `11_CONTENT_FACTORY`

**文档定义：**
- `4_PRODUCT`：Product Definition Layer — product specification, SKU, pricing（Reserved）
- `9_PRODUCT`：Future Commercial Layer — SaaS/API（Frozen）
- `11_CONTENT_FACTORY`：product generation, artifact generation（Active）

**代码实际：**
- `4_PRODUCT/`：**空**
- `9_PRODUCT/`：5 个 stub 文件，含无效 `api_server.py`
- `11_CONTENT_FACTORY/schemas/product_schema.py`：**DigitalProduct** 为实际产品对象
- `9_PRODUCT/pricing_engine.py`：`calculate_cost()` 独立，**未被 CF 或 OS 调用**
- Product Asset Contract 在 `commercial_assets/product_assets/`，由 Adapter 输出映射，非 4/9 模块

**潜在风险：**
- 三个「Product」命名空间：4（空）、9（冻结 stub）、11（实际生产）+ commercial_assets Product Asset
- 新成员无法从目录编号推断真实产品定义位置

**建议人工确认：** 归档或重命名 4_PRODUCT / 9_PRODUCT，明确 DigitalProduct vs Product Asset 边界

---

## Conflict MB-004

**Conflict ID:** MB-004

**涉及模块：** `5_CONTENT` ↔ `11_CONTENT_FACTORY`

**文档定义：**
- `5_CONTENT`：Content Knowledge Layer — templates, reusable content（Reserved）
- `11_CONTENT_FACTORY`：Digital Product Production（Active）

**代码实际：**
- `5_CONTENT/`：**空**
- 所有 template/generator/artifact 逻辑在 `11_CONTENT_FACTORY/artifact_generators/` 与 `artifacts/`

**潜在风险：**
- 5 与 11 职责在文档上分离，代码全部集中在 11
- 若未来 5_CONTENT 实现 knowledge base，可能与 CF artifacts 重复存储

**建议人工确认：** 5_CONTENT 是否仍保留为独立模块，或合并进 11 并更新 MODULE_REGISTRY

---

## Conflict MB-005

**Conflict ID:** MB-005

**涉及模块：** `9_PRODUCT` ↔ `10_DEPLOY`

**文档定义：**
- `9_PRODUCT`：SaaS/API productization（Frozen）
- `10_DEPLOY`：API access, service wrapper（Frozen per MODULE_REGISTRY）

**代码实际：**
- `9_PRODUCT/api_server.py`：`POST /run_task` — **SyntaxError**（`from 0_START.controller`）
- `10_DEPLOY/api.py` + `service.py`：**可运行** FastAPI，Service Lock 经 SystemController
- `10_DEPLOY/service.py` 注释明确禁止直接 import memory/planner 等

**潜在风险：**
- 两个 API 层历史并存；9 损坏、10 可用但文档标 Frozen
- `9_PRODUCT/api_server.py` status 返回 `"production_ready"` — 与系统实际阶段不符

**建议人工确认：** 删除或修复 9_PRODUCT API；统一 10_DEPLOY 文档状态为 Active 或明确 Deprecated

---

## Conflict MB-006

**Conflict ID:** MB-006

**涉及模块：** `6_EXECUTION` ↔ `11_CONTENT_FACTORY` (Release/Publish)

**文档定义：**
- `6_EXECUTION`：Execution Runtime — 本地 publish 模拟
- `11_CONTENT_FACTORY`：release_gate、publish_assistant — **非自动发布**

**代码实际：**
- `6_EXECUTION/publisher.py`：写 `output/publish_*.json`（基于 OS decision 的**市场商品**）
- `11_CONTENT_FACTORY/agents/release_gate.py`：对**数字产品 artifact** 做 release 检查
- `11_CONTENT_FACTORY/agents/publish_assistant.py`：生成 publish checklist，**不调用 6_EXECUTION**

**潜在风险：**
- 两个「发布」语义：OS 发布决策 vs CF 发布辅助 — 无代码桥接
- Pilot Product Asset 完成后无自动进入 6_EXECUTION 或真实平台

**建议人工确认：** Release 职责是否应统一到单一 Execution 层

---

## Conflict MB-007

**Conflict ID:** MB-007

**涉及模块：** `7_MEMORY` ↔ `11_CONTENT_FACTORY/storage` ↔ `commercial_assets`

**文档定义（Governance Protocol §2）：**
- Learning Knowledge → `7_MEMORY/`
- Commercial Object → `commercial_assets/`

**代码实际：**
- `7_MEMORY/memory_core.py`：OS pattern/strategy/policy
- `11_CONTENT_FACTORY/storage/product_memory.json`：CF 产品历史（**独立 JSON**）
- `commercial_assets/product_assets/product_assets_v1.json`：正式 Product Asset（Pilot 1 条）

**潜在风险：**
- 同一 Pilot 产品 `8523329941d4` 存在于 CF artifacts + product_assets JSON + pilot_outputs — 三处存储
- CF product_memory 含历史测试产品（如 `e601c17c6977`），**未同步**到 commercial_assets

**建议人工确认：** product_memory.json 是否应降级为 runtime cache，Product Asset JSON 为唯一商业事实源

---

## Summary

| Conflict ID | 模块对 | 严重度 |
|-------------|--------|--------|
| MB-001 | 2 ↔ 11 | P1 |
| MB-002 | 2 ↔ 3 | P1 |
| MB-003 | 4 ↔ 9 ↔ 11 | P1 |
| MB-004 | 5 ↔ 11 | P2 |
| MB-005 | 9 ↔ 10 | P1 |
| MB-006 | 6 ↔ 11 | P2 |
| MB-007 | 7 ↔ 11 ↔ commercial_assets | P1 |
