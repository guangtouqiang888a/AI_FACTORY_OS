# AI_FACTORY_OS Product Asset Contract v1

> 产品资产契约层 | 最后更新：2026-07-13  
> **状态：Blueprint Completed — Project Intelligence Layer 契约规范，不参与运行计算**

**定位：** Product Asset Contract Layer（产品资产契约层）— 定义 **Content Factory（内容工厂）** 生产完成后 **Product Asset Object（产品资产对象）** 的标准 Schema、生命周期、模块职责、Feedback 连接与未来数据库映射。

**上级文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — 五类商业 Object 总契约 §6
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md) — Production Request 协议
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md) — CF 集成设计与 Output 映射
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md) — Experiment 生命周期与 content_asset 回填

**说明：** **Blueprint ≠ Implementation**。本文档完成 Product Asset Contract 设计；不创建代码、不创建数据库表、不生成 `product_assets` JSON 实例、不调用 Content Factory。**Contract Completed ≠ Runtime Connected**。**Production Request Approved ≠ Product Created**。

---

## §1 Layer Position（层定位）

### 1.1 在商业生产链中的位置

```
Production Request Object（+ Approval approved）
        ↓
Content Factory（11_CONTENT_FACTORY — 生产执行）
        ↓
Product Asset Object                    ← 本 Contract 定义
        ↓
Feedback Object（市场 / 销售 / 用户反馈）
        ↓
Experiment Evaluation（假设验证）
```

### 1.2 完整商业资产链（Current Design）

```
Opportunity Candidate
        ↓
Opportunity Object
        ↓
Experiment Object
        ↓
Experiment Review
        ↓
Production Request
        ↓
Production Request Approval
        ↓
Product Asset Object                    ← 本任务补齐的契约层
        ↓
Feedback
```

### 1.3 Product Asset 的职责 — 不是什么

| Product Asset **是** | Product Asset **不是** |
|---------------------|------------------------|
| 记录**实际生成资产**的登记对象 | 生产任务（那是 Production Request） |
| 承载 `artifact_path`、质量分、生成状态 | 实验定义（那是 Experiment Object） |
| Content Factory 产出的**权威登记** | 市场机会（那是 Opportunity Object） |
| Feedback 与 Experiment 评估的**产品锚点** | 商业方向裁决层 |

### 1.4 核心原则

| 原则 | 说明 |
|------|------|
| **Production Request Approved ≠ Product Created** | Approval 只授权生产；Product Asset 须 CF 执行后才存在 |
| **Human Assisted ≠ Automation** | MVP Phase 1 资产可人工辅助登记；不等于 Runtime 自动创建 |
| **Product Quality Score ≠ Opportunity Score** | 语义隔离 — 见 Commercial Intelligence Contract |
| **Blueprint ≠ Implementation** | 本文档为契约；`commercial_assets/product_assets/` 实例 Pending |

---

## §2 Product Asset Object Definition（对象定义）

### 2.1 Product Asset Object Schema v1

每条生产完成的产品须登记为一条 **Product Asset Object**：

```json
{
  "object_type": "product_asset",
  "contract_version": "1.0",
  "product_asset_id": "",
  "source_production_request_id": "",
  "source_experiment_id": "",
  "source_opportunity_id": "",
  "approval_id": "",
  "product_name": "",
  "product_type": "ppt | excel | word | pdf",
  "asset_category": "",
  "artifact_information": {},
  "generation_status": "generated",
  "quality_score": 0.0,
  "creation_method": "human_assisted",
  "created_at": "",
  "updated_at": ""
}
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 用途 |
|------|------|------|------|
| `object_type` | TEXT | ✅ | 固定 `"product_asset"` |
| `contract_version` | TEXT | ✅ | 契约版本，当前 `"1.0"` |
| `product_asset_id` | TEXT | ✅ | 产品资产唯一 ID；格式建议 `passet_YYYYMMDD_NNN` 或 CF `product.id` |
| `source_production_request_id` | TEXT | ✅ | FK → Production Request — 追溯生产授权 |
| `source_experiment_id` | TEXT | ✅ | FK → Experiment — 评估追溯 |
| `source_opportunity_id` | TEXT | | 冗余 — 跨层查询 |
| `approval_id` | TEXT | ✅ | FK → Production Request Approval |
| `product_name` | TEXT | ✅ | 产品显示名称 |
| `product_type` | TEXT | ✅ | ppt / excel / word / pdf |
| `asset_category` | TEXT | ✅ | 资产分类 — 见 §2.3 |
| `artifact_information` | OBJECT | ✅ | 物理资产详情 — 见 §2.4 |
| `generation_status` | TEXT | ✅ | 生命周期状态 — 见 §3 |
| `quality_score` | NUMBER | ✅ | Product Quality Score（0.0–1.0）— QualityAgent 产出 |
| `creation_method` | TEXT | ✅ | `human_assisted` / `automated` — MVP Phase 1 固定 `human_assisted` |
| `created_at` | TEXT | ✅ | ISO-8601 创建时间 |
| `updated_at` | TEXT | | 最后状态更新时间 |

**可选扩展字段（v1.0 可选）：**

| 字段 | 用途 |
|------|------|
| `source_selection_id` | Selection 追溯 |
| `bundle_path` | 发布包路径 |
| `publish_channel` | 实际上架渠道 |
| `expected_price_cny` | 来自 PR asset_requirements |
| `production_cost_estimate` | 生产成本估算 |
| `metadata_path` | `artifacts/products/{id}/metadata.json` |
| `experiment_content_asset_ref` | Experiment Registry `content_asset` 回填指针 |
| `failure_reason` | `generation_status=failed` 时必填 |

### 2.3 asset_category 定义

| 值 | 含义 | 典型 product_type |
|----|------|-------------------|
| `office_template` | 办公效率模板 | ppt, excel, word |
| `digital_document` | 数字文档资料 | pdf |
| `ai_toolkit` | AI 工具包 | pdf, ppt |
| `industry_package` | 行业垂直资料包 | pdf, word |

**Category A 首批试点（preq_005）：** `asset_category: office_template`，`product_type: excel`。

### 2.4 artifact_information 结构

`artifact_information` 承载**实际生成资产**的物理与逻辑信息：

```json
{
  "artifact_path": "11_CONTENT_FACTORY/artifacts/products/{product_id}/",
  "primary_file": "documents/考勤记录表.xlsx",
  "file_type": "xlsx",
  "file_size_bytes": 0,
  "deliverable_count": 1,
  "artifact_files": [],
  "bundle_path": "package/publish_package/",
  "metadata_path": "metadata.json",
  "generation_log_ref": "",
  "quality_result": {
    "passed": true,
    "checklist_results": {},
    "first_pass": true,
    "reject_reason": null
  }
}
```

| 子字段 | 用途 |
|--------|------|
| `artifact_path` | 产品根目录 — 权威物理路径 |
| `primary_file` | 主交付文件相对路径 |
| `file_type` | xlsx / pptx / docx / pdf |
| `artifact_files` | 全部交付文件列表 |
| `bundle_path` | Packaging 产出路径 |
| `generation_log_ref` | Pipeline trace / 日志指针 |
| `quality_result` | QualityAgent 验收详情 |

### 2.5 Human Assisted ≠ Automation

| Human Assisted | Automation（未来） |
|----------------|-------------------|
| 人工触发 Pilot 生产后登记 Product Asset JSON | Adapter 自动产出并写回 |
| `creation_method: human_assisted` | `creation_method: automated` |
| 人工确认 artifact 路径与 quality_score | Runtime 自动回填 |
| 不等于 Cognition 或 Decision 自动创建 | 须 Adapter + Approval Gate |

---

## §3 Product Asset Lifecycle（生命周期）

### 3.1 状态定义

| 状态 | 英文 | 含义 |
|------|------|------|
| **Generated（已生成）** | generated | CF 已产出 artifact 文件，登记初始 |
| **Quality Checking（质检中）** | quality_checking | QualityAgent / ReleaseGate 验收中 |
| **Completed（生产完成）** | completed | 质检通过，可进入发布流程 |
| **Published（已发布）** | published | 已人工确认平台上架 |
| **Testing（测试观察）** | testing | 观察期，收集 Feedback |
| **Validated（验证成功）** | validated | Experiment 评估 success |
| **Archived（归档）** | archived | 资产关闭，记录保留 |
| **Failed（失败）** | failed | 生产或质检失败 |

### 3.2 状态流转

```
generated
    ↓  artifact 文件存在
quality_checking
    ↓  quality_score ≥ min_quality_score；checklist pass
completed
    ↓  人工确认上架；publish_channel 指定
published
    ↓  test_period 开始
testing
    ↓  Feedback 录入 + Experiment Evaluation
validated ──→ archived

quality_checking ──→ failed ──→ archived
generated ──→ failed（生成异常）
```

### 3.3 与 Production Request / Experiment 状态联动

| Product Asset 状态 | Production Request（参考） | Experiment Registry（参考） |
|--------------------|---------------------------|----------------------------|
| generated / quality_checking | production | production |
| completed | completed | production |
| published | completed | published |
| testing | completed | testing |
| validated | archived | validated |
| failed | failed | — |

### 3.4 转换条件

| 从 | 到 | 条件 |
|----|-----|------|
| — | generated | CF 产出 artifact；`artifact_information.primary_file` 非空 |
| generated | quality_checking | QualityAgent 开始验收 |
| quality_checking | completed | `quality_score` ≥ PR.quality_requirements.min_quality_score |
| quality_checking | failed | checklist 终拒；`failure_reason` 已填 |
| completed | published | 人工上架确认；`publish_channel` 非空 |
| published | testing | 观察期开始 |
| testing | validated | Experiment Evaluation = success |
| validated / failed | archived | `learning_summary` 或归档说明已填 |

---

## §4 Module Responsibility（模块职责）

### 4.1 权限矩阵

| 模块 | 允许 | 禁止 |
|------|------|------|
| **`11_CONTENT_FACTORY`** | 生成 artifact；产出 quality_score；写入 artifact 目录 | 修改 Opportunity Score；修改 Experiment；决定商业方向；绕过 Approval |
| **`3_DECISION`** | 产出 / 批准 Production Request | 生成 Product Asset；写 artifact 文件 |
| **`7_MEMORY`** | 吸收 Feedback 摘要；记录学习与 pattern | 替代 Product Asset Registry；覆盖完整资产记录 |
| **Adapter（未来）** | 映射 CF Output → Product Asset Object | 商业裁决 |
| **`2_COGNITION`** | 未来读 Feedback / validated 实验 | 生产资产；修改 Product Asset |
| **`0_START`** | 未来调度生产（Phase 5+） | 直接写 Product Asset 不经 CF |

### 4.2 11_CONTENT_FACTORY — 生产执行者

**负责：**
- 按 Production Request Input Contract 生成数字商品文件
- 产出 `quality_score`（Product Quality Score）
- 写入 `11_CONTENT_FACTORY/artifacts/products/{product_id}/`

**禁止：**
- 修改 Opportunity Score
- 修改 Experiment hypothesis / validation_goal
- 自行选品（Experiment 路径 bypass MarketAgent）
- 无 Approval 生产

### 4.3 3_DECISION — 生产请求层

**负责：** Production Request 生成与批准裁决（商业资产层 / 未来 Runtime）

**禁止：** 生成 Product Asset；操作 artifact 文件

### 4.4 7_MEMORY — 运行记忆层

**负责：** 吸收 Experiment `learning_summary` 与 Feedback 摘要；OS 运行 pattern

**禁止：** 作为 Product Asset 权威源；Product Asset 完整记录存 Registry / commercial_assets

---

## §5 Relationship（对象关系）

### 5.1 完整 Object 链与职责边界

```
Opportunity Object
    │  职责：市场机会情报 — 有没有机会
    ↓
Experiment Object
    │  职责：商业验证设计 — 验证什么假设
    ↓
Production Request Object
    │  职责：生产规格 — 生产什么、按什么标准
    ↓
Product Asset Object
    │  职责：实际生成资产登记 — 产出了什么文件
    ↓
Feedback Object
    │  职责：市场与销售结果 — 卖得怎么样
```

### 5.2 各 Object 对照

| Object | 核心问题 | 权威字段 | Product Asset 关系 |
|--------|----------|----------|-------------------|
| **Opportunity** | 有没有机会？ | `opportunity_score` | 只读追溯 `source_opportunity_id` |
| **Experiment** | 验证什么？ | `hypothesis`, `success_metrics` | `source_experiment_id`；回填 `content_asset` |
| **Production Request** | 生产什么规格？ | `asset_requirements` | `source_production_request_id` |
| **Product Asset** | 产出了什么？ | `artifact_information`, `quality_score` | **本 Contract 权威定义** |
| **Feedback** | 结果如何？ | `metrics`, `final_result` | 关联 `product_asset_id` |

### 5.3 与 commercial_assets 实例层

| 路径 | 状态 | Product Asset 关系 |
|------|------|-------------------|
| `production_requests_v1.json` | 3 条 draft | 上游 — 1:N（一次 PR 一次 Asset） |
| `production_request_reviews_v1.json` | 3 条 approved | 门禁 — `approval_id` |
| `experiments_v1.json` | 4 条 draft | 评估源 — `source_experiment_id` |
| `product_assets/` | **未创建** | 本 Contract 目标实例层 |

---

## §6 Content Factory Output Mapping（Content Factory 输出映射）

### 6.1 映射总览

```
ContentPipeline.run_from_production_request() 返回 dict
    ├── product（DigitalProduct dict）
    ├── artifacts（artifact_path, artifact_files）
    ├── quality（quality_score, passed, checklist）
    └── trace[]（generation_log）
        ↓
Adapter output_mapper（未来 — 见 Adapter Plan）
        ↓
Product Asset Object
```

### 6.2 字段映射表

| CF Output | Product Asset 字段 | 说明 |
|-----------|-------------------|------|
| `product.id` | `product_asset_id`（或映射） | 可与 CF product_id 共用 |
| PR.`production_request_id` | `source_production_request_id` | |
| PR.`source_experiment_id` | `source_experiment_id` | |
| Review.`approval_id` | `approval_id` | |
| `product.title` | `product_name` | |
| PR.`product_type` | `product_type` | |
| 推导 | `asset_category` | office_template 等 |
| `artifacts.artifact_path` | `artifact_information.artifact_path` | |
| 主文件路径 | `artifact_information.primary_file` | |
| 文件后缀 | `artifact_information.file_type` | |
| `artifacts.artifact_files` | `artifact_information.artifact_files` | |
| `trace[]` | `artifact_information.generation_log_ref` | 或内嵌 summary |
| `quality.quality_score` | `quality_score` | |
| `quality.checklist` | `artifact_information.quality_result` | |
| 成功/失败 | `generation_status` | completed / failed |
| 执行时间 | `created_at`, `updated_at` | |

### 6.3 generation_log 结构（映射参考）

```json
{
  "pipeline_version": "content_factory_v1",
  "steps": [
    { "agent": "creator", "status": "ok", "duration_ms": 0 },
    { "agent": "product_generator", "status": "ok", "duration_ms": 0 },
    { "agent": "quality", "status": "ok", "quality_score": 0.85 },
    { "agent": "packaging", "status": "ok" }
  ],
  "market_agent_bypassed": true,
  "production_request_id": "preq_20260712_005"
}
```

**说明：** 本 Contract **只设计映射** — 不修改 `content_pipeline.py` 或 Adapter 代码。

### 6.4 与 Legacy 路径隔离

| 路径 | Product Asset 登记 |
|------|-------------------|
| `run(keyword)` — Legacy | **不登记** commercial_assets Product Asset（或 `source=manual` 扩展） |
| `run_from_production_request()` — Experiment | **必须** 登记，带 full 追溯字段 |

---

## §7 Database Mapping（数据库映射 — 仅设计）

### 7.1 设计原则

| 原则 | 说明 |
|------|------|
| **Database Extension Pending** | 禁止 CREATE TABLE / migration |
| **Additive Evolution** | 对齐 Blueprint `generated_products` |
| **Registry 为权威** | DB 列映射 Contract 字段 |

### 7.2 建议表：product_assets

**状态：Blueprint 设计 — 未创建**

| 列名 | 类型 | 映射 Contract 字段 | 说明 |
|------|------|-------------------|------|
| `id` | INTEGER PK | — | 自增 |
| `product_asset_id` | TEXT UNIQUE | `product_asset_id` | 业务主键 |
| `production_request_id` | TEXT | `source_production_request_id` | FK → production_requests |
| `experiment_id` | TEXT | `source_experiment_id` | FK → commercial_experiments |
| `opportunity_id` | TEXT | `source_opportunity_id` | 冗余索引 |
| `approval_id` | TEXT | `approval_id` | |
| `product_name` | TEXT | `product_name` | |
| `product_type` | TEXT | `product_type` | |
| `asset_category` | TEXT | `asset_category` | |
| `artifact_path` | TEXT | `artifact_information.artifact_path` | |
| `primary_file` | TEXT | `artifact_information.primary_file` | |
| `file_type` | TEXT | `artifact_information.file_type` | |
| `artifact_json` | TEXT / JSON | `artifact_information` 完整 | |
| `generation_status` | TEXT | `generation_status` | |
| `quality_score` | REAL | `quality_score` | |
| `creation_method` | TEXT | `creation_method` | |
| `created_at` | TIMESTAMP | `created_at` | |
| `updated_at` | TIMESTAMP | `updated_at` | |

### 7.3 索引方向

| 索引 | 列 | 用途 |
|------|-----|------|
| PK | `product_asset_id` | 主键查询 |
| IDX | `production_request_id` | PR → Asset 1:1 查 |
| IDX | `experiment_id` | Experiment 评估聚合 |
| IDX | `generation_status` | 状态筛选 |
| IDX | `created_at` | 时间序 |

### 7.4 ER 关系

```
production_requests
        ↓ production_request_id
product_assets（未来 — 本 Contract）
        ↓ product_asset_id
product_feedback（Blueprint Table 7 — 未创建）
        ↓
experiment evaluation / opportunity_scores 学习
```

**与 Blueprint `generated_products` 关系：** Implementation 时可 **合并或 FK 关联** — 须 Database Extension 审批。

---

## §8 Feedback Connection（Feedback 连接）

### 8.1 反馈链路

```
Product Asset Object（published / testing）
        ↓  上架 + 观察期
Feedback Object 录入
        ↓
Experiment success_metrics 对比
        ↓
Experiment result（success / promising / failed）
```

### 8.2 Feedback 四类与 Product Asset 关联

| Feedback 类型 | 字段域 | Product Asset 关联 | 用途 |
|---------------|--------|-------------------|------|
| **market_feedback** | views, clicks, favorites, ctr | `product_asset_id` + 渠道 | 需求验证 |
| **customer_feedback** | 评论、咨询、满意度 | `product_asset_id` | 定性洞察 |
| **sales_feedback** | orders, revenue, conversion | `product_asset_id` + 定价 | 商业验证 |
| **quality_feedback** | 返工、投诉、质量复评 | `quality_score` 对比 | 生产改进 |

### 8.3 Feedback Object 映射（扩展 Intelligence Contract §7）

| Feedback 字段 | Product Asset 来源 |
|---------------|-------------------|
| `product_id` | `product_asset_id` |
| `experiment_id` | `source_experiment_id` |
| `production_request_id` | `source_production_request_id` |
| `artifact_path` | `artifact_information.artifact_path` |
| `traffic_data.*` | market_feedback |
| `sales_data.*` | sales_feedback |
| `customer_feedback` | customer_feedback |

### 8.4 进入 Feedback 的门禁

| # | 条件 |
|---|------|
| 1 | Product Asset `generation_status` ≥ completed |
| 2 | 人工确认 published（上架） |
| 3 | `source_experiment_id` 非空 — 实验批次产品 |
| 4 | 观察期 `validation_period` 自 Experiment 继承 |

**规则：** Feedback **不得** 直接修改 Product Asset `quality_score` 或 Opportunity Score。

---

## §9 Version Strategy（版本策略）

### 9.1 契约版本

| 字段 | 值 | 说明 |
|------|-----|------|
| `contract_version` | `"1.0"` | Product Asset Contract 首发版本 |

### 9.2 版本独立体系

| 版本体系 | 管辖范围 | 独立原因 |
|----------|----------|----------|
| **Product Asset Contract Version** | JSON Object 语义 | 商业资产层演进 |
| **Database Schema Version** | 表结构 Migration | Implementation 层 |
| **Runtime Version** | CF Pipeline / Agent | 代码发布 |
| **Integration Design Version** | Input/Output Contract | 集成层 |

**规则：** Contract minor bump **不自动要求** DB Migration；DB 变更须走 Database Extension 审批。

### 9.3 Semver 规则

| 变更类型 | bump | 示例 |
|----------|------|------|
| 新增可选字段 | minor（1.0 → 1.1） | 增加 `publish_date` |
| 必填字段变更 | major（1.x → 2.0） | `generation_status` 枚举变更 |
| 新 lifecycle 状态 | minor + 文档化 | 增加 `paused` |

### 9.4 与上级契约对齐

| 文档 | 版本 | 关系 |
|------|------|------|
| Commercial Intelligence Contract §6 | 1.0 | 总契约 — Product Asset 基础 |
| Content Factory Integration Design §4 | 1.0 | Output Schema — 本 Contract 扩展 |
| Production Request Contract | 1.0 | 上游 Input |
| Experiment Object Registry | 1.0 | content_asset 回填 |

**字段别名：** Intelligence Contract `product_id` = 本 Contract `product_asset_id`（Implementation 时统一）。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Production Request Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md` |
| Content Factory Integration Design | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md` |
| Content Factory Adapter Plan | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md` |
| Experiment Object Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Product Asset Contract Layer v1；`product_assets` JSON 实例、Adapter 代码、Pilot 生产、DB 表均 **Pending**。

**Contract Completed ≠ Runtime Connected。** **Production Request Approved ≠ Product Created.** **Human Assisted ≠ Automation.**
