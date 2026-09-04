# AI_FACTORY_OS Content Factory Integration Design v1

> Content Factory 集成设计 | Last updated: 2026-07-15（Entry **041-D**）  
> **Document Role:** Architecture Reference · **Reality Status:** Design Reference · **Runtime Status:** Requires Reality Validation  
> **状态：Design Completed — 集成规范。** Design Completed ≠ Core OS DAG Connected · Blueprint ≠ Production

**定位：** Content Factory Integration Layer（Content Factory 集成层）— 定义 **Production Request Object（生产请求对象）** 如何进入 **`11_CONTENT_FACTORY`（内容工厂运行时）** 并产出 **Product Asset Object（产品资产对象）** 的接口契约、Agent 映射、反馈链路与 Runtime 保护规则。

**上级文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md) — Production Request 协议
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — 五类商业 Object 总契约
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md) — Experiment 登记与评估
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md) — 实验管理体系

**当前 Runtime 现实（只读审计）：**

| 项 | 状态 |
|----|------|
| `11_CONTENT_FACTORY/` | ✅ Active — Agents + Pipeline 可独立运行 |
| 当前 Pipeline 入口 | `content_pipeline.run(keyword)` — **非** Production Request |
| `commercial_assets/production_requests/` | ✅ 3 条 draft + Approval approved |
| Production Request → CF Adapter（Track B） | ✅ Adapter 已实现；人辅登记 |
| `0_START` DAG → CF（Track A↔B） | ❌ **Runtime Integration Not Started** |

**说明：** **Blueprint ≠ Implementation ≠ Core OS↔CF 已融合**。本文档是 Design Reference；**Design Completed ≠ Runtime Connected**。

---

## 1. Integration Position（集成层定位）

### 1.1 三层职责边界

| 层 | 模块 / Object | 职责 | 禁止 |
|----|---------------|------|------|
| **生产授权层** | Production Request + Approval | 定义生产规格、审批门禁 | 执行生产 |
| **生产执行层** | `11_CONTENT_FACTORY` | 按 Input Contract 生产文件、质检、打包 | 选品、改 Opportunity Score、绕过 Approval |
| **生产交付层** | Product Asset Object | 登记 artifact_path、quality_score | 商业裁决 |

```
Production Request Object（+ Approval approved）
        ↓
Content Factory Integration Adapter（未来 — 本 Design 定义契约）
        ↓
11_CONTENT_FACTORY Pipeline
        ↓
Product Asset Object
        ↓
Feedback Object → Experiment Evaluation
```

### 1.2 与当前 Runtime 的差异（Gap）

**当前 `11_CONTENT_FACTORY` Pipeline（Legacy Demo 路径）：**

```
keyword → MarketAgent → CreatorAgent → ProductGenerator → QualityAgent → PackagingAgent → ReleaseGate
```

**目标集成路径（Design Target）：**

```
Production Request（approved）+ Approval Record
        ↓
Integration Adapter（映射 Input Contract）
        ↓
CreatorAgent → ProductGenerator → QualityAgent → PackagingAgent
        ↓
Product Asset Object 登记
```

| 差异项 | 当前 Runtime | 目标 Design |
|--------|-------------|-------------|
| 入口 | `keyword` 字符串 | Production Request Object JSON |
| 选品 | MarketAgent 自行分析 | **禁止** — 输入已由上游决定 |
| 追溯 | `product_memory.json` | `production_request_id` + `source_experiment_id` |
| 门禁 | 无 Approval 校验 | 须 `production_request_reviews.decision=approved` |

### 1.3 与 commercial_assets 实例层关系

| 资产 | 当前状态 | Integration 角色 |
|------|----------|------------------|
| `production_requests_v1.json` | 3 条 `draft` | Input Contract 来源 |
| `production_request_reviews_v1.json` | 3 条 `approved` | 生产授权门禁 |
| `experiments_v1.json` | 4 条 `draft` | `validation_goal` 上下文（只读） |
| Product Asset JSON 实例 | ❌ 未创建 | Integration 产出（Implementation 任务） |

---

## 2. Input Contract（输入契约）

### 2.1 Content Factory 接收字段 — Integration Input v1

Content Factory **未来唯一合法生产入口**须接收以下标准化输入包（Integration Input Package）：

```json
{
  "contract_version": "1.0",
  "object_type": "content_factory_input",
  "production_request_id": "",
  "source_experiment_id": "",
  "approval_id": "",
  "product_name": "",
  "product_type": "ppt | excel | word | pdf",
  "target_customer": "",
  "asset_requirements": {},
  "quality_requirements": {},
  "validation_goal": "",
  "priority": "P0 | P1 | P2 | P3",
  "creation_method": "human_assisted",
  "submitted_at": "ISO-8601"
}
```

### 2.2 字段说明与来源映射

| 字段 | 必填 | 来源 | 用途 |
|------|------|------|------|
| `production_request_id` | ✅ | `production_requests.*.production_request_id` | 全链路追溯主键 |
| `source_experiment_id` | ✅ | `production_requests.*.source_experiment_id` | 关联 Experiment 评估 |
| `approval_id` | ✅ | `production_request_reviews.*.approval_id` | 授权门禁校验 |
| `product_name` | ✅ | `production_requests.*.product_name` | Creator / Packaging 标题 |
| `product_type` | ✅ | `production_requests.*.product_type` | 路由 artifact generator |
| `target_customer` | ✅ | `production_requests.*.target_customer` | Creator 上下文 |
| `asset_requirements` | ✅ | `production_requests.*.asset_requirements` | 结构、格式、约束 |
| `quality_requirements` | ✅ | `production_requests.*.quality_requirements` | QualityAgent 验收 |
| `validation_goal` | ✅ | `production_requests.*.validation_goal` | 只读上下文 — **非**修改目标 |
| `priority` | ✅ | `production_requests.*.production_priority` | 队列调度参考 |
| `creation_method` | | 固定 `human_assisted`（MVP Phase 1） | 区分人工触发 vs 自动调度 |

### 2.3 asset_requirements 传入子集

Integration Adapter 须完整传递：

| 子字段 | Content Factory 消费方 |
|--------|------------------------|
| `product_concept` | CreatorAgent — 内容大纲 |
| `deliverable_format` | ProductGeneratorAgent — 文件类型路由 |
| `structure_outline` | CreatorAgent / Generator — 页/ sheet 结构 |
| `content_constraints` | Generator — 语言、页数、editable |
| `reference_from_experiment` | CreatorAgent — **只读** hypothesis 摘要 |

### 2.4 quality_requirements 传入子集

| 子字段 | Content Factory 消费方 |
|--------|------------------------|
| `min_quality_score` | QualityAgent — 通过阈值 |
| `first_pass_required` | QualityAgent — 返工策略 |
| `checklist` | QualityAgent / ReleaseGate — 验收项 |
| `reject_conditions` | QualityAgent — 失败判定 |
| `category_a_threshold` | 成本/时间上限参考 |

### 2.5 入口门禁 — 生产前校验

Integration Adapter **必须**在调用 Pipeline 前校验：

| # | 条件 | 失败动作 |
|---|------|----------|
| 1 | `production_request_reviews` 存在且 `decision=approved` | 拒绝执行 |
| 2 | `production_request_id` 与 Approval 记录匹配 | 拒绝执行 |
| 3 | `asset_requirements` + `quality_requirements` 非空 | 拒绝执行 |
| 4 | `product_type` ∈ {ppt, excel, word, pdf} | 拒绝执行 |
| 5 | 同 `production_request_id` 无 active `generation_status=production` | 拒绝重复生产 |

**说明：** MVP Phase 1 可由 **人工触发 Integration Adapter**（CLI / 脚本）；不等于 Runtime 自动调度。

---

## 3. Agent Mapping（Agent 映射）

### 3.1 当前 `11_CONTENT_FACTORY` Agent 清单（只读审计）

| Agent | 文件 | 当前职责 |
|-------|------|----------|
| **MarketAgent** | `agents/market_agent.py` | 关键词市场分析 — **Integration 路径须 bypass** |
| **CreatorAgent** | `agents/creator_agent.py` | 产品概念、目录创建、metadata |
| **ProductGeneratorAgent** | `agents/product_generator.py` | pptx/xlsx/docx/pdf 文件生成 |
| **QualityAgent** | `agents/quality_agent.py` | 质量评分与验收 |
| **PackagingAgent** | `agents/packaging_agent.py` | 发布包、title/description/pricing |
| **ReleaseGateAgent** | `agents/release_gate.py` | 发布前门禁 |
| **FeedbackAgent** | `agents/feedback_agent.py` | 反馈录入（过渡） |

**Artifact Generators：** `artifact_generators/{ppt,excel,word,pdf}_generator.py`

**Pipeline 入口：** `pipeline/content_pipeline.py` — `ContentPipeline.run(keyword)`

### 3.2 Production Request → Agent 映射表

| Production Request 字段 | 目标 Agent | 输入映射 | 输出 |
|-------------------------|------------|----------|------|
| `product_name` + `asset_requirements` | **CreatorAgent** | `keyword`←product_name；`product_type`；`target_customer`；`content`←structure_outline | `product` dict, `artifact_path` |
| `asset_requirements.deliverable_format` | **ProductGeneratorAgent** | `product_type`；`structure_outline`；`content_constraints` | 真实文件 (.pptx/.xlsx/.docx/.pdf) |
| `quality_requirements` | **QualityAgent** | `min_quality_score`；`checklist`；`product` + artifact files | `quality_score`, pass/fail |
| `asset_requirements` + product dict | **PackagingAgent** | `product_name`；`expected_price_cny`；platform | `publish_package/` |
| `quality_requirements` + packaging | **ReleaseGateAgent** | checklist 终验 | release_ready boolean |
| — | **MarketAgent** | **禁止调用** — 选品已由上游完成 | — |

### 3.3 目标 Pipeline 序列（Integration v1）

```
Integration Input Package（Production Request approved）
        ↓
[Gate] Approval + schema 校验
        ↓
CreatorAgent          ← asset_requirements, target_customer, product_type
        ↓
ProductGeneratorAgent ← deliverable_format, structure_outline, content_constraints
        ↓
QualityAgent          ← quality_requirements.min_quality_score, checklist
        ↓
PackagingAgent        ← product_name, publish_channel_planned, expected_price_cny
        ↓
ReleaseGateAgent      ← first_pass_required, reject_conditions
        ↓
Product Asset Object 登记 + production_request status → production/completed
```

### 3.4 Agent 禁止职责（红线）

| Agent | 禁止 | 原因 |
|-------|------|------|
| **MarketAgent** | Integration 路径调用 | 绕过 Production Request 选品 |
| **CreatorAgent** | 修改 `validation_goal` / hypothesis | 商业目标属 Experiment 层 |
| **QualityAgent** | 修改 `opportunity_score` | 评分语义隔离 |
| **所有 Agent** | 读取 `commercial_assets/opportunities/` 做选品 | 破坏商业链门禁 |
| **所有 Agent** | 无 Approval 记录执行生产 | 绕过 Production Authorization Gate |
| **Pipeline** | 接受裸 `keyword` 作为实验批次入口 | 须 `production_request_id` 追溯 |

---

## 4. Product Asset Object（产品资产对象）

### 4.1 Integration Output Schema v1

Content Factory 生产完成后须登记 **Product Asset Object**：

```json
{
  "object_type": "product_asset",
  "contract_version": "1.0",
  "product_asset_id": "",
  "source_production_request_id": "",
  "source_experiment_id": "",
  "approval_id": "",
  "product_name": "",
  "product_type": "ppt | excel | word | pdf",
  "artifact_path": "",
  "bundle_path": "",
  "asset_type": "",
  "quality_score": 0.0,
  "generation_status": "completed | failed",
  "quality_checklist_result": {},
  "production_cost_estimate": 0.0,
  "created_at": "",
  "completed_at": ""
}
```

### 4.2 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `product_asset_id` | TEXT | ✅ | 产品资产 ID；格式建议 `passet_YYYYMMDD_NNN` 或复用 CF `product_id` |
| `source_production_request_id` | TEXT | ✅ | FK → Production Request |
| `source_experiment_id` | TEXT | ✅ | FK → Experiment — 评估追溯 |
| `approval_id` | TEXT | ✅ | FK → Approval 记录 |
| `product_name` | TEXT | ✅ | 产品名称 |
| `product_type` | TEXT | ✅ | ppt / excel / word / pdf |
| `artifact_path` | TEXT | ✅ | 物理路径 — 如 `11_CONTENT_FACTORY/artifacts/products/{id}/` |
| `bundle_path` | TEXT | | `package/publish_package/` 路径 |
| `asset_type` | TEXT | ✅ | 主交付格式 — pptx / xlsx / docx / pdf |
| `quality_score` | NUMBER | ✅ | QualityAgent 产出 — **Product Quality Score** |
| `generation_status` | TEXT | ✅ | `production` / `completed` / `failed` |
| `quality_checklist_result` | OBJECT | | checklist 逐项结果 |
| `production_cost_estimate` | NUMBER | | AI + 人工估算成本 |
| `created_at` | TEXT | ✅ | ISO-8601 |
| `completed_at` | TEXT | | 生产完成时间 |

### 4.3 与 Commercial Intelligence Contract 对齐

| Integration Output | Intelligence Contract §6 | 说明 |
|--------------------|---------------------------|------|
| `product_asset_id` | `product_id` | 业务 ID 统一 |
| `source_production_request_id` | `production_request_id` | 追溯链 |
| `artifact_path` | `artifact_path` | 路径一致 |
| `quality_score` | `quality_score` | Product Quality ≠ Opportunity Score |
| `generation_status=completed` | `status=released`（上架前） | 状态映射见 Implementation |

### 4.4 产出路径约定

```
11_CONTENT_FACTORY/artifacts/products/{product_id}/
├── documents/          ← 主交付文件 (.pptx/.xlsx/.docx/.pdf)
├── templates/
├── images/
├── package/
│   ├── publish_package/
│   └── publish_assistant/
└── metadata.json       ← 过渡 — 未来映射 Product Asset Object
```

**规则：** Product Asset Object 为 **commercial_assets 登记层**（未来）；物理文件存 `artifacts/`；DB 存指针（Implementation Pending）。

---

## 5. Feedback Connection（反馈连接）

### 5.1 反馈链路

```
Product Asset Object
        ↓  上架 + 观察期
Feedback Object（metrics.market / metrics.commercial）
        ↓
Experiment Evaluation（success_metrics 对比）
        ↓
Experiment Registry result（success / promising / failed）
        ↓
learning_summary → 7_MEMORY 摘要（单向）
```

### 5.2 字段映射：Product Asset → Feedback

| Feedback 字段 | Product Asset 来源 |
|---------------|-------------------|
| `product_id` / `product_asset_id` | `product_asset_id` |
| `experiment_id` | `source_experiment_id` |
| `production_request_id` | `source_production_request_id` |
| `artifact_path` | `artifact_path` |

### 5.3 Experiment Evaluation 对照

| Experiment success_metrics | Feedback 录入 | 评估 |
|----------------------------|---------------|------|
| `market_metric.target_views` | `metrics.market.views` | 需求验证 |
| `market_metric.target_clicks` | `metrics.market.clicks` | 互动验证 |
| `commercial_metric.target_orders` | `metrics.commercial.orders` | 转化验证 |
| `commercial_metric.expected_price_cny` | 实际上架价 | 定价验证 |
| `production_metric.target_quality_score` | `quality_score` | 生产质量 |
| `validation_review.failure_condition` | 观察期结果 | failed 判定 |

### 5.4 反馈录入规则

| 规则 | 说明 |
|------|------|
| Feedback **不得** overwrite Opportunity Score | 须批次聚合 |
| Product Asset `quality_score` **不得** 当作 `opportunity_score` | 语义隔离 |
| Experiment Evaluation 须等 `validation_period` 期满 | 见 Experiment Registry §6 |
| Feedback 可人工录入（MVP Phase 1） | Human Assisted |

---

## 6. Runtime Protection Rules（Runtime 保护规则）

### 6.1 Content Factory — 允许

| 允许 | 说明 |
|------|------|
| **生产** | 按 Input Contract 生成 artifact |
| **质检** | 按 quality_requirements 验收 |
| **打包** | 生成 publish_package |
| **登记 Product Asset** | 产出 Output Object |
| **回填 Production Request** | `artifact_path`、`generation_status`（Implementation） |
| **写入 product_memory.json** | 过渡存储 — 未来映射 DB |

### 6.2 Content Factory — 禁止

| 禁止 | 原因 |
|------|------|
| **选择产品** | 选品权在 Opportunity → Selection → Experiment → PR |
| **修改 Opportunity Score** | 认知层评分 — CF 无权限 |
| **绕过 Production Approval** | 须 Approval `decision=approved` |
| **读取 opportunities 内部文件做裁决** | 破坏 Module Contract |
| **调用 MarketAgent 做实验批次选品** | 替代上游商业链 |
| **修改 Experiment / Production Request 目标字段** | 只读消费 |
| **自动上架平台** | 半自动 + 人工 — Work Principles |
| **无 production_request_id 的生产** | 不纳入 30 批次统计 |

### 6.3 模块边界总览

| 模块 | Integration 角色 |
|------|------------------|
| `0_START` / ExecutionRuntime | 未来调度 Integration Adapter — **Implementation Pending** |
| `3_DECISION` | 不直接调用 CF；产出 PR — 已设计 |
| `11_CONTENT_FACTORY` | 生产执行 — 本 Design 定义输入/输出 |
| `2_COGNITION` | 不参与生产；未来读 Feedback |
| `7_MEMORY` | 只读 learning 摘要 — 不替代 Registry |
| `commercial_assets/` | 资产登记源 — CF 不直接写（Implementation 定 adapter 写回策略） |

---

## 7. Future Implementation Roadmap（未来实施路线图）

### 7.1 阶段划分

| 阶段 | 名称 | 状态 | 内容 |
|------|------|------|------|
| **Phase 0** | 商业资产链建设 | ✅ Completed | Candidate → PR → Approval 实例 |
| **Phase 1** | Integration Design | ✅ **Design Completed（本任务）** | 本文档 — Input/Output Contract |
| **Phase 2** | Adapter Implementation | ⏳ **Code Implementation Pending** | `integration_adapter.py` — PR JSON → Pipeline |
| **Phase 3** | Pilot Production | ⏳ Pending | P0 单条 — preq_20260712_005 |
| **Phase 4** | Product Asset 实例层 | ⏳ Pending | `commercial_assets/product_assets/` |
| **Phase 5** | Runtime 调度 | ⏳ Pending | `0_START` 接入 — 须审批 |
| **Phase 6** | Database Extension | ⏳ Pending | `generated_products` + FK |

### 7.2 Phase 2 Implementation Checklist（待执行 — 非本任务）

- [ ] 新建 Integration Adapter — 读取 `production_requests_v1.json` + `production_request_reviews_v1.json`
- [ ] Approval 门禁校验逻辑
- [ ] Input Contract → CreatorAgent / ProductGeneratorAgent 字段映射
- [ ] bypass MarketAgent 的实验生产路径
- [ ] QualityAgent 对接 `quality_requirements`
- [ ] 产出 Product Asset Object JSON
- [ ] 回填 Production Request `status` → production / completed
- [ ] **不修改** 0_START 直至 Phase 5 单独审批

### 7.3 Pilot 建议顺序

| 顺序 | production_request_id | 产品 | priority | 理由 |
|------|----------------------|------|----------|------|
| 1 | preq_20260712_005 | Excel 考勤记录表 | P0 | 竞争低、结构简单、Approval 首选 |
| 2 | preq_20260712_001 | 商业计划书 PPT | P1 | PPT 验证 |
| 3 | preq_20260712_004 | 工作总结 PPT | P1 | 周期性场景 |

### 7.4 明确声明

| 声明 | 含义 |
|------|------|
| **Design Completed** | 本文档 — Input/Output/Agent/Feedback/Protection 已定义 |
| **Code Implementation Pending** | 无 Python 变更；Pipeline 仍 `run(keyword)` |
| **Runtime Connected** | Content Factory 未接入 commercial_assets 生产链 |
| **Approval ≠ Production Started** | 3 条 approved 不等于已生产 |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Production Request Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md` |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Experiment Object Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` |
| Content Factory README | `11_CONTENT_FACTORY/README.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Content Factory Integration Design v1；Adapter 代码、Pilot 生产、Runtime 调度、DB 表均 **Pending**，须单独审批后实施。
