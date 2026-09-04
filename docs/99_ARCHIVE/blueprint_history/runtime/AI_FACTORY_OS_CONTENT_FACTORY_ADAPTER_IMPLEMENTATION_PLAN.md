# AI_FACTORY_OS Content Factory Adapter Implementation Plan v1

> Content Factory Adapter 实施方案 | 最后更新：2026-07-13  
> **状态：Plan Completed — Project Intelligence Layer 实施规划，不参与运行计算**

**定位：** Content Factory Adapter Implementation Plan（Content Factory 适配器实施方案）— 在 [Content Factory Integration Design v1](AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md) 契约基础上，规划 **Production Request Object** 进入 **`11_CONTENT_FACTORY` Runtime** 的 Adapter 层实施路径、文件结构、字段映射、试点范围与风险控制。

**上级文档：**

- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md) — 集成契约（Design Completed）
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md) — Production Request 协议
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — Product Asset Object 总契约

**当前资产状态（只读审计）：**

| 资产 | 状态 |
|------|------|
| `production_requests_v1.json` | 3 条 `draft` |
| `production_request_reviews_v1.json` | 3 条 `approved` |
| P0 试点目标 | `preq_20260712_005` — Excel 考勤记录表 |
| Adapter 代码 | ❌ **未创建** |
| Product Asset 实例 | ❌ **未创建** |

**说明：** **Blueprint ≠ Implementation**。本文档为 **Implementation Plan（实施方案）** — 只设计如何实施，**不修改 Python、不创建目录、不调用 Content Factory、不生成产品**。**Plan Completed ≠ Code Implemented**。

---

## 1. Adapter Layer Position（Adapter 层定位）

### 1.1 为什么需要 Adapter

Production Request Object（商业资产 JSON）与 Content Factory Runtime（Python Pipeline）之间存在 **语义鸿沟（Semantic Gap）**：

| 维度 | Production Request 层 | Content Factory Runtime |
|------|----------------------|-------------------------|
| 数据形态 | `commercial_assets/*.json` — 商业 Object | Python dict / Agent input |
| 入口 | `production_request_id` + Approval | `content_pipeline.run(keyword)` |
| 选品 | 已由上游 Selection / Review 决定 | MarketAgent 自行分析 keyword |
| 追溯 | `source_experiment_id` 全链路 | `product_memory.json` 局部 |
| 门禁 | Approval `decision=approved` | 无 |

**Adapter 是 Production Request 与 Content Factory Runtime 之间的隔离层（Isolation Layer）** — 负责翻译、校验、调度，**不承担商业裁决**。

### 1.2 目标链（Design Target）

```
Production Request Object（commercial_assets/production_requests/）
        ↓
Production Request Approval（commercial_assets/production_request_reviews/）
        ↓
Content Factory Adapter（未来 — 本 Plan 规划）
        ↓
11_CONTENT_FACTORY Pipeline（agents/ + pipeline/）
        ↓
Product Asset Object（commercial_assets/product_assets/ — 未来）
```

### 1.3 Adapter 不做的事

| Adapter 不做 | 负责层 |
|--------------|--------|
| 商业选品 | Opportunity → Selection → Experiment |
| 实验审核 | Experiment Prepared Review |
| 生产审批 | Production Request Approval |
| 商业评分 | 2_COGNITION / Opportunity Score |
| OS 调度 | 0_START（Phase 5+） |

---

## 2. Current Legacy Flow Analysis（当前 Legacy 路径分析）

### 2.1 Legacy Pipeline 结构（只读审计）

**入口：** `11_CONTENT_FACTORY/pipeline/content_pipeline.py`

```python
ContentPipeline.run(keyword: str, platform: str = "xianyu") -> dict
```

**Legacy 序列：**

```
keyword（字符串）
    ↓
MarketAgent.execute()           ← 市场分析、recommendation
    ↓
CreatorAgent.execute()          ← 产品概念、目录创建
    ↓
ProductGeneratorAgent.execute() ← pptx/xlsx/docx/pdf 生成
    ↓
QualityAgent.execute()          ← 质量评分
    ↓
PackagingAgent.execute()        ← 发布包
    ↓
ReleaseGateAgent.execute()      ← 发布门禁
    ↓
product_memory.json 写入
```

### 2.2 Legacy 路径特征

| 特征 | 说明 | 与实验链冲突 |
|------|------|--------------|
| 入口为 `keyword` | 无 `production_request_id` | ❌ 无法纳入 30 批次统计 |
| MarketAgent 选品 | 自行产出 market_score / recommendation | ❌ 绕过商业链 |
| 无 Approval 校验 | 任意 keyword 可生产 | ❌ 绕过 Production Authorization Gate |
| 输出至 `product_memory.json` | 非 Product Asset Object | ❌ 无 experiment 追溯 |

### 2.3 Legacy 兼容策略

| 策略 | 说明 |
|------|------|
| **保留 Legacy 路径** | `ContentPipeline.run(keyword)` **不删除** — demo / 独立测试用途 |
| **新增 Experiment 路径** | Adapter 调用 **新入口** `ContentPipeline.run_from_production_request(input_package)` — Implementation 时添加 |
| **路径隔离** | Legacy 产物 **不写入** `commercial_assets/product_assets/`；实验产物 **必须** 带 `production_request_id` |
| **MarketAgent bypass** | Experiment 路径 **跳过** MarketAgent；Legacy 路径 **保留** MarketAgent |
| **CLI 双模式** | 未来 CLI：`--keyword`（Legacy）vs `--production-request-id`（Experiment） |

**规则：** Legacy Path Protection — 任何 Adapter Implementation **不得破坏** 现有 `run(keyword)` 行为。

---

## 3. Adapter Responsibility（Adapter 职责）

### 3.1 Adapter 负责

| # | 职责 | 说明 |
|---|------|------|
| 1 | **读取 Production Request** | 从 `commercial_assets/production_requests/production_requests_v1.json` 加载 |
| 2 | **校验 Approval** | 匹配 `production_request_reviews_v1.json`；`decision=approved` |
| 3 | **字段映射** | PR Object → Integration Input Package → Agent input dict |
| 4 | **调用 Content Factory Pipeline** | 调用 Experiment 路径（bypass MarketAgent） |
| 5 | **返回 Product Asset** | 映射 Pipeline output → Product Asset Object JSON |
| 6 | **可选写回** | PR status → production/completed（Implementation 配置，默认 Pilot 阶段人工确认） |

### 3.2 Adapter 禁止

| 禁止 | 原因 |
|------|------|
| **选品** | 产品已由上游决定 |
| **商业评分** | 不产出 / 修改 opportunity_score |
| **修改 Opportunity** | 只读消费 commercial_assets |
| **绕过审批** | 无 Approval 记录拒绝执行 |
| **调用 MarketAgent** | Experiment 路径 bypass |
| **自动上架平台** | 半自动 + 人工 — Work Principles |
| **修改 Experiment hypothesis** | 只读 `validation_goal` |

### 3.3 Adapter 与 3_DECISION / 0_START 边界

| 模块 | Phase 1（Pilot） | Phase 5+（Future） |
|------|------------------|-------------------|
| **Adapter** | 人工 CLI 触发 | 可被 0_START 调度 |
| **3_DECISION** | 不参与 Adapter 调用 | 可选 Policy 校验 |
| **0_START** | 不接入 | ExecutionRuntime 调度 Adapter |

---

## 4. Future File Structure（未来文件结构 — 仅设计）

### 4.1 规划目录 — **不创建**

以下目录结构为 Implementation 目标布局，**本 Plan 不创建任何文件**：

```
11_CONTENT_FACTORY/
├── agents/                    ← 现有 — 不移动
├── artifacts/                 ← 现有 — 不移动
├── pipeline/                  ← 现有 — 扩展 run_from_production_request()
├── schemas/                   ← 现有 — 扩展 product_schema.py
├── storage/                   ← 现有
├── adapter/                   ← 【未来新增】Adapter 层
│   ├── __init__.py
│   ├── production_request_loader.py    # 读取 commercial_assets JSON
│   ├── approval_gate.py                # Approval 校验
│   ├── input_mapper.py                 # PR → Integration Input
│   ├── output_mapper.py                # Pipeline result → Product Asset
│   └── adapter_runner.py               # 主入口 CLI
├── contracts/                 ← 【未来新增】契约常量 / schema 校验
│   ├── integration_input_v1.json       # Input Contract JSON Schema
│   └── product_asset_output_v1.json    # Output Contract JSON Schema
└── services/                  ← 【未来新增】编排服务
    └── experiment_production_service.py  # 单次实验生产编排
```

### 4.2 commercial_assets 扩展（未来）

```
commercial_assets/
├── production_requests/           ← 已有
├── production_request_reviews/    ← 已有
└── product_assets/                ← 【未来】Product Asset 实例
    └── product_assets_v1.json
```

### 4.3 文件职责对照

| 文件（未来） | 职责 |
|--------------|------|
| `production_request_loader.py` | 加载 PR + Review JSON |
| `approval_gate.py` | 校验 approval_id、decision、ID 匹配 |
| `input_mapper.py` | PR fields → ContentPipeline input |
| `output_mapper.py` | Pipeline trace → Product Asset Object |
| `adapter_runner.py` | CLI：`python -m adapter.adapter_runner --preq preq_20260712_005` |
| `experiment_production_service.py` | 编排：gate → map → pipeline → asset |

---

## 5. Input Mapping（输入映射）

### 5.1 映射总览

```
Production Request Object（production_requests_v1.json 单条）
        +
Production Request Review（production_request_reviews_v1.json 匹配条）
        ↓
Adapter input_mapper
        ↓
Integration Input Package（Integration Design §2.1）
        ↓
ContentPipeline.run_from_production_request() 参数
```

### 5.2 字段映射表

| Production Request 字段 | Integration Input | ContentPipeline / Agent 参数 |
|-------------------------|-------------------|------------------------------|
| `production_request_id` | `production_request_id` | `context["production_request_id"]` |
| `source_experiment_id` | `source_experiment_id` | `context["source_experiment_id"]` |
| Review.`approval_id` | `approval_id` | `context["approval_id"]` |
| `product_name` | `product_name` | Creator: `keyword`, `title` |
| `product_type` | `product_type` | Creator/Generator: `product_type` |
| `target_customer` | `target_customer` | Creator: `target_customer` |
| `asset_requirements` | `asset_requirements` | Creator/Generator: 完整传入 |
| `quality_requirements` | `quality_requirements` | Quality/ReleaseGate: 完整传入 |
| `validation_goal` | `validation_goal` | `context["validation_goal"]` — **只读** |
| `production_priority` | `priority` | `context["priority"]` — 队列参考 |
| `asset_requirements.publish_channel_planned` | — | Creator: `platform` |
| `asset_requirements.expected_price_cny` | — | Packaging: `price` |

### 5.3 asset_requirements 细映射

| PR 子字段 | Agent | 参数名 |
|-----------|-------|--------|
| `product_concept` | CreatorAgent | `content` / outline 生成依据 |
| `deliverable_format` | ProductGeneratorAgent | 文件类型路由（xlsx/pptx/...） |
| `structure_outline[]` | CreatorAgent, Generator | `structure_outline` |
| `content_constraints.language` | Generator | `language` |
| `content_constraints.max_pages_or_sheets` | Generator | 页数/sheet 上限 |
| `content_constraints.formulas_required` | Generator (excel) | 公式生成 flag |
| `reference_from_experiment.hypothesis_summary` | CreatorAgent | 只读上下文 |

### 5.4 Pilot 输入实例（preq_20260712_005 — 映射预览）

| 字段 | 值 |
|------|-----|
| `production_request_id` | `preq_20260712_005` |
| `source_experiment_id` | `exp_20260708_005` |
| `approval_id` | `appr_20260713_005` |
| `product_name` | Excel 考勤记录表 |
| `product_type` | excel |
| `priority` | P0 |
| `deliverable_format` | xlsx |
| `structure_outline` | 考勤明细表, 月度汇总, 使用说明 |
| `platform` | taobao（来自 publish_channel_planned） |

---

## 6. Output Mapping（输出映射）

### 6.1 映射总览

```
ContentPipeline.run_from_production_request() 返回 dict
    ├── trace[]（各 Agent 步骤）
    ├── product（DigitalProduct dict）
    ├── artifacts（artifact_path, artifact_files）
    └── quality（quality_score, passed）
        ↓
Adapter output_mapper
        ↓
Product Asset Object
        ↓
commercial_assets/product_assets/product_assets_v1.json（追加）
```

### 6.2 字段映射表

| Pipeline 输出 | Product Asset 字段 | 说明 |
|---------------|-------------------|------|
| 新生成 / 复用 | `product_asset_id` | `passet_YYYYMMDD_NNN` 或 CF `product.id` |
| PR.`production_request_id` | `source_production_request_id` | 追溯 |
| PR.`source_experiment_id` | `source_experiment_id` | 追溯 |
| Review.`approval_id` | `approval_id` | 追溯 |
| PR.`product_name` | `product_name` | |
| PR.`product_type` | `product_type` | |
| `artifacts.artifact_path` | `artifact_path` | 如 `11_CONTENT_FACTORY/artifacts/products/{id}/` |
| `artifacts` 主文件后缀 | `asset_type` | xlsx / pptx / docx / pdf |
| `quality.quality_score` | `quality_score` | Product Quality Score |
| 成功 / 失败 | `generation_status` | `completed` / `failed` |
| 执行时间 | `created_at` / `completed_at` | ISO-8601 |
| `quality.checklist_result` | `quality_checklist_result` | 逐项验收 |

### 6.3 Product Asset Object 示例（Pilot 预期 — 非实例）

```json
{
  "object_type": "product_asset",
  "contract_version": "1.0",
  "product_asset_id": "passet_20260713_001",
  "source_production_request_id": "preq_20260712_005",
  "source_experiment_id": "exp_20260708_005",
  "approval_id": "appr_20260713_005",
  "product_name": "Excel 考勤记录表",
  "product_type": "excel",
  "artifact_path": "11_CONTENT_FACTORY/artifacts/products/{product_id}/",
  "asset_type": "xlsx",
  "quality_score": 0.0,
  "generation_status": "completed",
  "created_at": "ISO-8601",
  "completed_at": "ISO-8601"
}
```

**说明：** Pilot 执行前 `quality_score` 为 0；完成后由 QualityAgent 回填。

---

## 7. Pilot Production Scope（试点生产范围）

### 7.1 第一次生产 — 仅允许一条

| 项 | 值 |
|----|-----|
| **production_request_id** | `preq_20260712_005` |
| **product_name** | Excel 考勤记录表 |
| **source_experiment_id** | `exp_20260708_005` |
| **approval_id** | `appr_20260713_005` |
| **production_priority** | **P0** |
| **product_type** | excel |
| **deliverable_format** | xlsx |

### 7.2 选择 P0 的理由

| # | 理由 |
|---|------|
| 1 | **selection_score 最高（69）** — 本批次首选实验 |
| 2 | **竞争低风险** — competition ease=0.72 |
| 3 | **生产成本最低档** — `expected_cost` ¥1.5，`category_a_threshold` ≤ ¥2.0 |
| 4 | **结构简单** — 3 sheet：明细 + 汇总 + 说明；含公式但复杂度可控 |
| 5 | **Excel 单文件交付** — Generator 路径成熟 |
| 6 | **Approval 明确建议 P0 优先试点** |

### 7.3 Pilot 禁止范围

| production_request_id | 产品 | Pilot 阶段 |
|----------------------|------|------------|
| preq_20260712_001 | 商业计划书 PPT | ❌ 禁止 — P1，待 Pilot 成功后 |
| preq_20260712_004 | 工作总结 PPT | ❌ 禁止 — P1，待 Pilot 成功后 |
| preq_20260712_005 | Excel 考勤记录表 | ✅ **唯一允许** |

### 7.4 Pilot 成功标准

| # | 标准 |
|---|------|
| 1 | Approval Gate 校验通过 |
| 2 | 产出有效 `.xlsx` 文件 |
| 3 | `quality_score` ≥ `min_quality_score`（0.85） |
| 4 | Product Asset Object 登记完整 |
| 5 | `production_request_id` 全链路可追溯 |
| 6 | Legacy `run(keyword)` 仍正常工作 |

---

## 8. Risk Control（风险控制）

### 8.1 Approval Gate（审批门禁）

| 控制 | 实现（未来） |
|------|-------------|
| 无 Approval 记录 | Adapter 拒绝执行，返回 `gate_error: NO_APPROVAL` |
| `decision != approved` | 拒绝执行 |
| `approval_id` 与 `production_request_id` 不匹配 | 拒绝执行 |
| Pilot 非 P0 请求 | 拒绝执行（Pilot 阶段硬编码 whitelist） |

### 8.2 Single Product Pilot（单产品试点）

| 控制 | 说明 |
|------|------|
| Whitelist | Pilot 仅 `preq_20260712_005` |
| 单次执行 | 同 `production_request_id` 无并发 active production |
| 人工触发 | MVP Phase 1 须人工 CLI 确认 — Human Assisted |
| 无批量 | Pilot 禁止一次生产 3 条 |

### 8.3 Rollback Strategy（回滚策略）

| 场景 | 回滚动作 |
|------|----------|
| 生产失败 | `generation_status=failed`；保留 trace log；**不**写 Product Asset completed |
| 质检未通过 | 不登记 Product Asset；PR 保持 draft/approved |
| Adapter 代码缺陷 | 删除错误 artifact 目录；回退至 Legacy-only 模式 |
| 误触发 Pilot | Whitelist + 人工 confirm 双重防护 |
| 资产写回错误 | Product Asset JSON 独立文件 — 可人工删除单条，不影响 PR 源文件 |

**原则：** commercial_assets 源文件（PR / Approval）**Pilot 阶段默认只读** — status 写回须显式 flag。

### 8.4 Legacy Path Protection（Legacy 路径保护）

| 规则 | 说明 |
|------|------|
| 不删除 `run(keyword)` | Legacy demo 路径保留 |
| 不修改 MarketAgent 签名 | Experiment 路径 bypass，非替换 |
| Adapter 为 **additive** | 新增文件 / 新入口，非重构现有 Agent |
| Legacy 产物不带 `production_request_id` | 与实验产物隔离 |
| 回归测试 | Implementation 后须验证 `content_pipeline.py "办公PPT模板"` 仍成功 |

---

## 9. Implementation Roadmap（实施路线图）

### 9.1 阶段状态

| 阶段 | 名称 | 状态 |
|------|------|------|
| Phase 0 | 商业资产链 | ✅ Completed |
| Phase 1 | Integration Design | ✅ Design Completed |
| Phase 1.5 | **Adapter Implementation Plan** | ✅ **Plan Completed（本任务）** |
| Phase 2 | Adapter Code Implementation | ⏳ **Code Implementation Pending** |
| Phase 3 | Pilot Execution（preq_005） | ⏳ **Pilot Execution Pending** |
| Phase 4 | Product Asset 实例层 | ⏳ Pending |
| Phase 5 | 扩展 P1 生产 + Runtime 调度 | ⏳ Pending |

### 9.2 Phase 2 — Code Implementation Checklist（待执行）

- [ ] 创建 `11_CONTENT_FACTORY/adapter/` 目录及模块（须单独授权）
- [ ] 实现 `approval_gate.py` — 读取 reviews JSON，校验 approved
- [ ] 实现 `input_mapper.py` — PR → Integration Input
- [ ] 实现 `output_mapper.py` — Pipeline result → Product Asset
- [ ] 扩展 `ContentPipeline` — 新增 `run_from_production_request()`，bypass MarketAgent
- [ ] 实现 `adapter_runner.py` — CLI 入口 + Pilot whitelist
- [ ] **不修改** `0_START` / `3_DECISION` / `7_MEMORY`

### 9.3 Phase 3 — Pilot Execution Checklist（待执行）

- [ ] 人工确认 Pilot 授权
- [ ] 执行：`adapter_runner --preq preq_20260712_005`
- [ ] 验证 xlsx 产出 + quality_score ≥ 0.85
- [ ] 创建 `commercial_assets/product_assets/product_assets_v1.json`
- [ ] 验证 Legacy `run(keyword)` 回归
- [ ] 更新 PROJECT_STATUS / CURSOR_EXECUTION_HISTORY

### 9.4 明确声明

| 声明 | 含义 |
|------|------|
| **Plan Completed** | 本文档 — 实施方案已定义 |
| **Code Implementation Pending** | 无 Python 变更 |
| **Pilot Execution Pending** | 无产品生成 |
| **Design Completed ≠ Runtime Connected** | CF 仍 Legacy 入口 |
| **Approval ≠ Production Started** | 3 条 approved 不等于已生产 |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Content Factory Integration Design | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md` |
| Production Request Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md` |
| Production Requests 实例 | `commercial_assets/production_requests/production_requests_v1.json` |
| Production Request Reviews | `commercial_assets/production_request_reviews/production_request_reviews_v1.json` |
| Content Factory README | `11_CONTENT_FACTORY/README.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Content Factory Adapter Implementation Plan v1；Adapter 代码、目录创建、Pilot 生产均 **Pending**，须 Entry 031+ 单独授权后实施。
