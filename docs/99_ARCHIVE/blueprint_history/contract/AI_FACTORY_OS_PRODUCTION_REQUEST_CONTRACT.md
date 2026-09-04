# AI_FACTORY_OS Production Request Contract v1

> 生产请求协议层 | 最后更新：2026-07-08  
> **状态：Blueprint Completed — Project Intelligence Layer 契约规范，不参与运行计算**

**定位：** Production Request Contract Layer（生产请求协议层）— 定义 **Experiment Object（实验对象）** 与 **Content Factory Runtime（内容工厂运行时）** 之间的标准生产请求协议、生命周期、模块权限与未来数据库映射。

**上级文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — 商业智能五类 Object 总契约
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md) — 实验管理体系
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md) — Experiment Object 登记规范
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md](../commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md) — MVP 验证目标

**说明：** **Blueprint ≠ Implementation（蓝图不等于实施）**。本文档完成 Production Request Contract 设计；不创建代码、不创建数据库表、不生成 Production Request JSON 实例、不调用 Content Factory。**Document Completed ≠ Runtime Connected（文档完成不等于运行时已连接）**。

---

## 1. Production Request Layer Position（生产请求层定位）

### 1.1 三层职责分离

Production Request（生产请求）是 **Experiment Object 与 Content Factory Runtime 之间的转换层（Conversion Layer）**。

| 层 | Object | 职责 |
|----|--------|------|
| **商业验证层** | Experiment Object | 定义**商业验证目标** — hypothesis、validation_goal、success_metrics、category |
| **生产转换层** | Production Request Object | 定义**具体生产要求** — product_type、asset_requirements、quality_requirements、production_priority |
| **生产交付层** | Generated Product / Product Asset Object | 承载**实际生产资产** — artifact_path、quality_score、bundle |

```
Experiment Object          ← 回答「为什么要验证、验证什么假设」
        ↓
Production Request Object  ← 回答「生产什么、按什么规格、优先级如何」
        ↓
Generated Product Object   ← 回答「实际产出了什么文件/资产」
```

### 1.2 在完整商业链路中的位置

**Current Runtime（当前已存在）：**

```
1_DATA → 3_DECISION → 11_CONTENT_FACTORY → Feedback → 7_MEMORY
```

**Future Target（商业验证完整链路 — 设计目标）：**

```
Opportunity
    ↓
Selection
    ↓
Experiment
    ↓
Production Request        ← 本 Contract 定义
    ↓
Content Factory
    ↓
Product Asset
    ↓
Feedback
```

### 1.3 核心门禁规则

| 规则 | 说明 |
|------|------|
| **禁止 Experiment Object 直接调用 Content Factory** | Experiment 只定义验证目标；生产须经 Production Request 转换 |
| **禁止 Content Factory 自行发现商业机会** | 生产输入唯一合法来源为 Production Request（未来） |
| **禁止跳过 Production Request 的实验生产** | 纳入 30 批次统计的实验产品须可追溯到 `source_experiment_id` |
| **Human Assisted ≠ Automation** | MVP Phase 1 可由人工辅助生成 Production Request 资产；不等于 Runtime 自动调度 |

### 1.4 与 Commercial Intelligence Contract 的关系

[Commercial Intelligence Contract v1](AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) §5 已定义 Production Request Object 基础 Schema。本文档为 **Experiment 时代的专项扩展** — 增加 `source_experiment_id`、`asset_requirements`、`quality_requirements`、完整生命周期与未来 DB 映射，不替代总契约，与之 **Additive（叠加）** 共存。

---

## 2. Object Definition（对象定义）

### 2.1 Production Request Object Schema v1

每条生产请求须登记为一条 **Production Request Object（生产请求对象）**。

```json
{
  "object_type": "production_request",
  "contract_version": "1.0",
  "production_request_id": "",
  "source_experiment_id": "",
  "source_opportunity_id": "",
  "product_type": "",
  "asset_requirements": {},
  "target_customer": "",
  "quality_requirements": {},
  "production_priority": "",
  "status": "draft",
  "created_at": ""
}
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 用途 |
|------|------|------|------|
| `object_type` | TEXT | ✅ | 固定 `"production_request"` — Object 类型标识 |
| `contract_version` | TEXT | ✅ | 契约版本，当前固定 `"1.0"` |
| `production_request_id` | TEXT | ✅ | 生产请求唯一 ID，格式建议 `preq_YYYYMMDD_NNN` |
| `source_experiment_id` | TEXT | ✅ | 来源 Experiment Object 的 `experiment_id` — 追溯商业验证目标 |
| `source_opportunity_id` | TEXT | | 来源 Opportunity Object 的 `opportunity_id` — 可选冗余，便于跨层查询 |
| `product_type` | TEXT | ✅ | 产品类型：`ppt` / `excel` / `word` / `pdf` |
| `asset_requirements` | OBJECT | ✅ | 具体生产规格要求 — 见 §2.3 |
| `target_customer` | TEXT | ✅ | 目标用户群 — 自 Experiment 继承或细化 |
| `quality_requirements` | OBJECT | ✅ | 质量与验收标准 — 见 §2.4 |
| `production_priority` | TEXT | ✅ | 生产优先级：`P0` / `P1` / `P2` / `P3` — 见 §2.5 |
| `status` | TEXT | ✅ | 生命周期状态 — 见 §3 |
| `created_at` | TEXT | ✅ | ISO-8601 创建时间 |

**可选扩展字段（v1.0 可选，Implementation 时可补）：**

| 字段 | 用途 |
|------|------|
| `keyword` | 关联市场关键词 — 自 Experiment / Opportunity 继承 |
| `experiment_category` | `A` / `B` / `C` — 影响 quality 阈值与成本预期 |
| `expected_cost` | 预估生产成本（CNY）— 自 Experiment 继承 |
| `publish_channel_planned` | 计划发布渠道 — 生产时不执行发布 |
| `production_method` | `human_assisted` / `automated` — 区分人工辅助与自动调度 |
| `artifact_path` | 生产完成后回填 — Generated Product 物理路径 |
| `content_asset_id` | 关联 Product Asset Object 的 `product_id` |
| `approved_at` | 批准进入生产的时间 |
| `completed_at` | 生产完成时间 |
| `failure_reason` | status=`failed` 时必填 |

### 2.3 asset_requirements 结构

`asset_requirements` 定义 Content Factory **应产出什么**，不含商业假设。

```json
{
  "product_name": "",
  "product_concept": "",
  "deliverable_format": "pptx | xlsx | docx | pdf",
  "deliverable_count": 1,
  "structure_outline": [],
  "content_constraints": {
    "language": "zh-CN",
    "max_pages_or_sheets": 0,
    "include_instructions": true,
    "editable": true
  },
  "reference_from_experiment": {
    "hypothesis_summary": "",
    "validation_goal": ""
  }
}
```

| 子字段 | 用途 |
|--------|------|
| `product_name` | 产品显示名称 |
| `product_concept` | 产品概念描述 — 自 Experiment.product_concept 映射 |
| `deliverable_format` | 交付文件格式 |
| `deliverable_count` | 交付文件数量（Category A 通常为 1） |
| `structure_outline` | 结构大纲（如 PPT 页结构、Excel  sheet 列表） |
| `content_constraints` | 语言、页数/ sheet 数、是否含说明文档等硬约束 |
| `reference_from_experiment` | 实验上下文摘要 — 供 Creator Agent 理解，**非**修改 Experiment 目标 |

### 2.4 quality_requirements 结构

`quality_requirements` 定义验收标准 — Quality Agent 判定依据。

```json
{
  "min_quality_score": 0.80,
  "first_pass_required": true,
  "category_a_threshold": {
    "production_time_minutes_max": 30,
    "production_cost_cny_max": 3.0
  },
  "checklist": [
    "deliverable_format_correct",
    "structure_complete",
    "no_placeholder_text",
    "instructions_included"
  ],
  "reject_conditions": [
    "missing_required_sections",
    "quality_score_below_threshold"
  ]
}
```

| 子字段 | 用途 |
|--------|------|
| `min_quality_score` | 最低质量分 — 对齐 Experiment success_metrics.production_metric |
| `first_pass_required` | 是否要求一次通过质检 |
| `category_a_threshold` | Category A 低成本生产上限（可选） |
| `checklist` | 人工 / Quality Agent 验收清单 |
| `reject_conditions` | 触发返工或 failed 的条件 |

### 2.5 production_priority 定义

| 值 | 含义 | 典型场景 |
|----|------|----------|
| `P0` | 紧急 — 同一批次最高优先 | selection_score 最高、配额窗口有限 |
| `P1` | 高优先 — 标准实验队列 | Category A 首批 selected 实验 |
| `P2` | 普通 — 可排队 | 观察期后二次实验 |
| `P3` | 低优先 — 资源空闲时执行 | 优化迭代、非关键验证 |

**规则：** `production_priority` 由 `3_DECISION` 或人工辅助根据 Experiment `selection_score` / category 配额决定；Content Factory **只读**优先级，**不得**自行调整。

### 2.6 完整登记示例（Blueprint 参考 — 非实例文件）

```json
{
  "object_type": "production_request",
  "contract_version": "1.0",
  "production_request_id": "preq_20260708_001",
  "source_experiment_id": "exp_20260708_005",
  "source_opportunity_id": "opp_20260708_005",
  "product_type": "excel",
  "asset_requirements": {
    "product_name": "小团队 Excel 考勤记录表",
    "product_concept": "含出勤统计、迟到早退自动计算与月度汇总的 xlsx",
    "deliverable_format": "xlsx",
    "deliverable_count": 1,
    "structure_outline": ["考勤明细", "月度汇总", "使用说明"],
    "content_constraints": {
      "language": "zh-CN",
      "max_pages_or_sheets": 3,
      "include_instructions": true,
      "editable": true
    },
    "reference_from_experiment": {
      "hypothesis_summary": "小团队愿为带自动统计的考勤 Excel 模板付费",
      "validation_goal": "验证低竞争细分是否有首单转化"
    }
  },
  "target_customer": "小微商户管理员、培训班负责人、10 人以内小团队",
  "quality_requirements": {
    "min_quality_score": 0.85,
    "first_pass_required": true,
    "category_a_threshold": {
      "production_time_minutes_max": 25,
      "production_cost_cny_max": 2.0
    },
    "checklist": [
      "deliverable_format_correct",
      "structure_complete",
      "formulas_functional",
      "instructions_included"
    ],
    "reject_conditions": [
      "missing_required_sections",
      "quality_score_below_threshold"
    ]
  },
  "production_priority": "P0",
  "status": "draft",
  "created_at": "2026-07-08T15:12:00+08:00"
}
```

**说明：** 以上为 Schema 示例；**本 Contract 不生成 JSON 实例文件**。实例创建属 Implementation 任务。

---

## 3. Lifecycle Design（生命周期设计）

### 3.1 状态定义

| 状态 | 英文 | 含义 |
|------|------|------|
| **Draft（草案）** | draft | 自 Experiment 映射生成，字段可编辑，**未批准生产** |
| **Approved（已批准）** | approved | 人工或 Decision 批准，可进入 Content Factory 队列 |
| **Production（生产中）** | production | Content Factory 已接收并正在执行生产 |
| **Completed（已完成）** | completed | 生产成功，`artifact_path` / `content_asset_id` 已回填 |
| **Failed（失败）** | failed | 生产失败或质检未通过且不可返工 |
| **Archived（归档）** | archived | 请求关闭，记录保留，不再调度 |

### 3.2 状态流转

```
draft
    ↓  Experiment status=prepared；asset/quality requirements 完整；人工或 Decision 批准
approved
    ↓  Content Factory 接收请求；Experiment → production（实验层状态）
production
    ↓  Product Asset 产出 + quality 达标
completed
    ↓  关联 Feedback 录入完成；Experiment 进入 published/testing
archived

production ──→ failed ──→ archived（生产失败 / 质检终拒）
draft ──→ archived（实验取消，未进入生产）
```

### 3.3 转换条件

| 从 | 到 | 条件 |
|----|-----|------|
| draft | approved | `source_experiment_id` 有效；Experiment `status` ≥ prepared；`asset_requirements` + `quality_requirements` 非空；`production_priority` 已指定 |
| approved | production | Content Factory 确认接收；无同 experiment 的 active production 请求 |
| production | completed | `artifact_path` 非空；`quality_score` ≥ `min_quality_score` |
| production | failed | 生产异常或质检终拒；`failure_reason` 已填写 |
| completed | archived | Product Asset 已关联 Experiment；Feedback 流程已启动或明确跳过 |
| failed | archived | `failure_reason` 已填写；Experiment 层记录 learning |
| draft | archived | Experiment 取消或合并；须注明原因 |

### 3.4 与 Experiment Lifecycle 对齐

| Production Request 状态 | Experiment Registry feedback_status（参考） |
|-------------------------|---------------------------------------------|
| draft | prepared |
| approved | prepared → production |
| production | production |
| completed | production → published（上架前） |
| failed | production（实验层可标记 incomplete） |
| archived | archived |

**规则：** Production Request 生命周期 **短于** Experiment 全生命周期；Experiment 的 Testing / Validated 阶段在 Production Request `completed` 之后继续。

---

## 4. Module Responsibility（模块职责）

### 4.1 权限矩阵

| 模块 | 允许 | 禁止 |
|------|------|------|
| **`3_DECISION`** | 读取 Experiment Object（prepared+）；根据 Experiment 状态**生成** Production Request；设置 `production_priority`；draft → approved 裁决 | 直接调用 Content Factory 内部 API；修改 Experiment hypothesis；写入 artifact |
| **`11_CONTENT_FACTORY`** | **读取** approved/production 状态的 Production Request；执行生产；回填 `artifact_path`、`content_asset_id`；production → completed/failed | **自己发现商业机会**；**自己决定生产什么**；**修改 Experiment 目标**；读取 opportunity 内部文件做选品 |
| **`2_COGNITION`** | 产出 Opportunity Object；提供市场情报 | **负责生产**；生成 Production Request；触发 Content Factory |
| **`0_START` / ExecutionRuntime** | 调度 Object 在模块间传递；audit 日志 | 绕过 Contract 直接写 Content Factory 参数 |
| **`1_DATA`** | 持久化 Production Request（未来 DB） | 业务裁决 |
| **`7_MEMORY`** | 吸收生产结果摘要（单向） | 替代 Production Request 登记源 |
| **`10_DEPLOY`** | HTTP 接入 | 商业 Object 持久化 |

### 4.2 3_DECISION — 生产请求生成者

**职责：**

1. 消费 Experiment Object（`status: prepared` 及以上）
2. 将 `product_concept`、`target_customer`、`success_metrics.production_metric` 映射为 `asset_requirements` + `quality_requirements`
3. 分配 `production_priority`
4. 创建 Production Request Object（`status: draft`）
5. 批准后将状态更新为 `approved`

**当前现实：** `3_DECISION` 存在 Legacy ScoringAgent / DecisionAgent，产出语义类似 Production Request，**未标准化**为本 Contract Schema — Implementation Pending。

### 4.3 11_CONTENT_FACTORY — 生产执行者

**职责：**

1. **仅**通过 Production Request 获取生产任务（未来唯一合法入口）
2. 按 `asset_requirements` 调用 Creator / Quality / Packaging Agent
3. 按 `quality_requirements` 执行验收
4. 产出 Product Asset Object；回填 Production Request

**禁止行为（红线）：**

| 禁止 | 原因 |
|------|------|
| 自己发现商业机会 | 破坏 Opportunity → Selection → Experiment 门禁 |
| 自己决定生产什么 | 生产决策权在 Decision + Experiment 层 |
| 修改 Experiment 目标 | Experiment 是商业验证权威源 |
| 跳过 Production Request 生产 | 无法纳入 30 批次实验统计 |

### 4.4 2_COGNITION — 机会提供者

**职责边界：** 只提供 Opportunity Object 与市场情报分析。

**禁止：** 生成 Production Request、触发 Content Factory、修改 Experiment 或 Production Request 状态。

---

## 5. Relationship With Existing Objects（与现有 Object 的关系）

### 5.1 完整 Object 链

```
Opportunity Object
    │  职责：市场机会情报 — demand/trend/competition/profit 评分，recommendation
    ↓
Experiment Object
    │  职责：商业验证设计 — hypothesis, validation_goal, success_metrics, category
    ↓
Production Request Object
    │  职责：生产规格与调度 — asset_requirements, quality_requirements, priority
    ↓
Generated Product Object（Product Asset Object）
    │  职责：实际生产资产 — artifact_path, quality_score, bundle_path
    ↓
Feedback Object
    │  职责：市场与销售反馈 — metrics.market/commercial, final_result
```

### 5.2 各 Object 职责对照

| Object | 核心问题 | 权威字段 | 生产者 | 消费者 |
|--------|----------|----------|--------|--------|
| **Opportunity** | 有没有机会？ | `opportunity_score`, `recommendation` | 2_COGNITION / human_assisted | Selection / Decision |
| **Experiment** | 验证什么假设？ | `hypothesis`, `validation_goal`, `success_metrics` | Selection + human_assisted | 3_DECISION |
| **Production Request** | 生产什么规格？ | `asset_requirements`, `quality_requirements` | 3_DECISION / human_assisted | 11_CONTENT_FACTORY |
| **Generated Product** | 产出了什么？ | `artifact_path`, `quality_score` | 11_CONTENT_FACTORY | Feedback / DB |
| **Feedback** | 市场结果如何？ | `metrics`, `final_result` | Feedback 流程 | 2_COGNITION / 3_DECISION |

### 5.3 字段映射：Experiment → Production Request

| Production Request 字段 | Experiment 来源 |
|-------------------------|-----------------|
| `source_experiment_id` | `experiment_id` |
| `source_opportunity_id` | `source_opportunity_id` |
| `product_type` | `product_type` |
| `target_customer` | `target_customer` |
| `asset_requirements.product_concept` | `product_concept` |
| `asset_requirements.reference_from_experiment.hypothesis_summary` | `hypothesis`（摘要） |
| `asset_requirements.reference_from_experiment.validation_goal` | `validation_goal` |
| `quality_requirements.min_quality_score` | `success_metrics.production_metric.target_quality_score` |
| `quality_requirements.category_a_threshold` | `success_metrics.production_metric` + `expected_cost` |
| `production_priority` | 自 Selection `selection_score` / Experiment category 推导 |

### 5.4 字段映射：Production Request → Product Asset

| Product Asset 字段 | Production Request 来源 |
|--------------------|----------------------|
| `production_request_id` | `production_request_id` |
| `product_type` | `product_type` |
| `product_name` | `asset_requirements.product_name` |
| `source` | `"experiment"`（当 source_experiment_id 非空） |
| `experiment_id`（扩展） | `source_experiment_id` |

### 5.5 与 commercial_assets 实例层关系

当前已存在商业资产实例（**非 Runtime**）：

| 路径 | Object 类型 | Production Request 关系 |
|------|-------------|-------------------------|
| `commercial_assets/opportunities/opportunities_v1.json` | Opportunity | 上游 — 经 Experiment 间接关联 |
| `commercial_assets/experiments/experiments_v1.json` | Experiment | **直接来源** — 4 条 draft，待 prepared 后可生成 Production Request |
| `commercial_assets/experiment_selection/` | Selection | 影响 priority，不直接生成 Production Request |

**当前状态：** Production Request JSON 实例 **未创建** — 本 Contract 仅为设计规范。

---

## 6. Database Future Mapping（未来数据库映射）

### 6.1 设计原则

| 原则 | 说明 |
|------|------|
| **Database Extension Pending** | 表设计仅为 Blueprint，**禁止**在本任务或未经审批的任务中 `CREATE TABLE` |
| **Additive Evolution** | 新表不破坏 Legacy `scores` / `products` |
| **Registry 为权威** | DB 列映射 Registry / Contract 字段，不反向定义语义 |

### 6.2 建议表：production_requests

**状态：Blueprint 设计 — 未创建**

| 列名 | 类型 | 映射 Contract 字段 | 说明 |
|------|------|-------------------|------|
| `id` | INTEGER PK | — | 自增主键 |
| `production_request_id` | TEXT UNIQUE | `production_request_id` | 业务主键 |
| `experiment_id` | TEXT | `source_experiment_id` | FK → commercial_experiments（未来） |
| `opportunity_id` | TEXT | `source_opportunity_id` | 冗余索引 |
| `product_type` | TEXT | `product_type` | ppt / excel / word / pdf |
| `requirements` | TEXT / JSON | `asset_requirements` + `quality_requirements` | JSON 合并存储 |
| `production_priority` | TEXT | `production_priority` | P0–P3 |
| `status` | TEXT | `status` | draft ~ archived |
| `artifact_path` | TEXT | `artifact_path` | 生产完成后回填 |
| `content_asset_id` | TEXT | `content_asset_id` | FK → generated_products（未来） |
| `failure_reason` | TEXT | `failure_reason` | failed 时 |
| `created_at` | TIMESTAMP | `created_at` | |
| `approved_at` | TIMESTAMP | `approved_at` | |
| `completed_at` | TIMESTAMP | `completed_at` | |

### 6.3 ER 关系（Blueprint）

```
commercial_experiments（未来 — Experiment Registry DB）
        ↓ experiment_id
production_requests（未来 — 本 Contract）
        ↓ content_asset_id / artifact_path
generated_products（Blueprint Table 6 — 未创建）
        ↓ product_id
product_feedback（Blueprint Table 7 — 未创建）
```

### 6.4 与 Commercial Intelligence Contract DB 映射对齐

| Contract Object | 原映射（Intelligence Contract §9） | 本 Contract 扩展 |
|-----------------|-------------------------------------|------------------|
| Production Request | OS 运行时传递，可选 audit 表 | 明确 `production_requests` 表设计 |
| Product Asset | `generated_products` | `artifact_path` 回填链路 |
| Experiment | 建议 `commercial_experiments` | `experiment_id` FK |

**实施须走：** [Database Extension Implementation Plan](../database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md) — 须单独审批。

---

## 7. Content Factory Connection（Content Factory 连接）

### 7.1 唯一生产入口原则

**Production Request 是未来 Content Factory 的唯一合法生产入口（Single Entry Point）。**

| 阶段 | 行为 |
|------|------|
| **当前（Runtime 现实）** | Content Factory 可独立运行 demo 生产；**未**接入 Production Request Contract |
| **目标（Post-Implementation）** | Content Factory **仅**消费 `status: approved` 的 Production Request |

### 7.2 未来生产流程

```
Production Request（approved）
        ↓
0_START / ExecutionRuntime 调度
        ↓
11_CONTENT_FACTORY
    ├── Creator Agent    ← 读取 asset_requirements
    ├── Quality Agent    ← 读取 quality_requirements
    └── Packaging Agent  ← 产出 bundle
        ↓
artifact（物理文件）
        ↓
Generated Product Object（Product Asset 登记）
        ↓
Production Request.status → completed
        ↓
Experiment.content_asset 回填（Registry 字段）
        ↓
Feedback Object 录入（Testing 阶段）
```

### 7.3 连接门禁

| # | 门禁 | 说明 |
|---|------|------|
| 1 | 无 Production Request 不生产 | 实验批次产品必须可追溯 |
| 2 | 无 approved 状态不调度 | draft 不得进入 Factory |
| 3 | 无 Experiment 来源不纳入 30 批次 | `source_experiment_id` 必填 |
| 4 | 生产不修改 Experiment | 只读 experiment 上下文 |
| 5 | 发布 ≠ 生产 | Production Request completed 不含 publish；上架属 Experiment published 阶段 |

### 7.4 当前 Gap（差异说明）

| 项 | 设计目标 | 当前现实 |
|----|----------|----------|
| Production Request Schema | 本文档 v1 | Intelligence Contract §5 简版；无 Experiment 链接 |
| Content Factory 入口 | 仅 Production Request | 可独立 CLI / demo 运行 |
| DB 持久化 | production_requests 表 | 未创建 |
| commercial_assets 实例 | production_requests/*.json | 未创建（本任务禁止） |

**明确：Document Completed ≠ Runtime Connected。**

---

## 8. Version Strategy（版本策略）

### 8.1 契约版本

| 字段 | 值 | 说明 |
|------|-----|------|
| `contract_version` | `"1.0"` | 当前 Production Request Contract 首发版本 |

### 8.2 Semver 规则

| 变更类型 | 版本 bump | 示例 |
|----------|-----------|------|
| 新增可选字段 | minor（1.0 → 1.1） | 增加 `estimated_delivery_at` |
| 必填字段变更 / 语义变更 | major（1.x → 2.0） | `production_priority` 枚举变更 |
| 新 status 状态 | minor + 文档化 | 增加 `paused` |
| 新 Object 子结构 | minor | `asset_requirements.templates[]` |

### 8.3 与 Database Schema Version 独立

| 版本体系 | 管辖范围 | 独立原因 |
|----------|----------|----------|
| **Production Request Contract Version** | JSON Object 语义、模块接口 | 可独立于 DB 演进 |
| **Database Schema Version** | 表结构、Migration | Implementation 层 |
| **Experiment Registry Version** | Experiment Object Schema | 实验层独立 |

**规则：** Contract minor bump **不自动要求** DB Migration；DB 列变更须走 Database Extension 审批，并更新本文档 §6 映射表。

### 8.4 与 Commercial Intelligence Contract 版本关系

| 文档 | 版本 | 关系 |
|------|------|------|
| Commercial Intelligence Contract | 1.0 | 总契约 — Production Request 为基础五类之一 |
| Production Request Contract（本文档） | 1.0 | 专项扩展 — Experiment 时代生产协议 |
| Experiment Object Registry | 1.0 | 上游 Experiment Schema |

**兼容性：** 本文档 `production_request_id` 对应 Intelligence Contract 的 `request_id` — Implementation 时须统一别名或提供映射层。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Commercial Experiment System Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md` |
| Experiment Object Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` |
| Commercial MVP Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
| Database Extension Plan | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Production Request Contract Layer v1 设计；代码接入、DB 表、JSON 实例、Content Factory 调度均 **Pending**，须单独审批后实施。
