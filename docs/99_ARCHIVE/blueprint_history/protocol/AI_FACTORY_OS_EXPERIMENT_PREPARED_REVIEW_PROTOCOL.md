# AI_FACTORY_OS Experiment Prepared Review Protocol v1

> 实验准备审核协议层 | 最后更新：2026-07-08  
> **状态：Blueprint Completed — Project Intelligence Layer 审核规范，不参与运行计算**

**定位：** Experiment Prepared Review Layer（实验准备审核层）— 在 **Experiment Object（实验对象）** 与 **Production Request Object（生产请求对象）** 之间建立**人工审核门槛（Human Review Gate）**，确保只有商业目标清晰、验证指标明确、生产成本可接受的实验才能进入生产流程。

**上级文档：**

- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md) — Experiment Object 登记与生命周期
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md) — Production Request 协议
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md](../commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md) — 实验选择框架
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md) — 实验管理体系

**说明：** **Blueprint ≠ Implementation（蓝图不等于实施）**。本文档完成 Prepared Review Protocol 设计；不创建代码、不创建数据库表、不生成 experiment_review JSON 实例、不创建 Production Request 实例、不调用 Content Factory。**Document Completed ≠ Runtime Connected（文档完成不等于运行时已连接）**。

---

## 1. Layer Position（层定位）

### 1.1 三层职责 — 不可混淆

| 层 | Object / 活动 | 核心职责 | 回答的问题 |
|----|---------------|----------|------------|
| **实验设计层** | Experiment Object | 商业实验设计 | 「验证什么假设？成功标准是什么？」 |
| **审核门禁层** | Prepared Review | 生产前审核 | 「是否满足进入生产的条件？」 |
| **生产转换层** | Production Request | 生成生产规格 | 「具体生产什么、按什么标准？」 |

```
Experiment Object          ← 负责商业实验设计
        ↓
Prepared Review            ← 负责生产前审核（本 Protocol 定义）
        ↓
Production Request         ← 负责生成生产规格
```

### 1.2 在完整商业链路中的位置

```
Opportunity Candidate
        ↓
Opportunity Object
        ↓
Experiment Selection
        ↓
Experiment Object（status: draft）
        ↓
Prepared Review              ← 本 Layer（人工审核门槛）
        ↓
Experiment Object（status: prepared）
        ↓
Production Request Contract
        ↓
Content Factory（未接入 — Runtime Pending）
```

### 1.3 核心门禁规则

| 规则 | 说明 |
|------|------|
| **prepared ≠ production** | Experiment `prepared` 仅表示审核通过、可创建 Production Request；**不等于**已生产或已上架 |
| **review approved ≠ Content Factory execution** | 审核批准 **不自动触发** Content Factory；生产须 Production Request `approved` + 单独授权 |
| **无 Review 不得 prepared** | Experiment 从 `draft` → `prepared` **必须**有对应 Experiment Review `decision: approve` |
| **rejected 禁止生产** | Review `decision: reject` 的实验 **不得** 创建 Production Request |
| **Human Assisted ≠ Automation** | MVP Phase 1 审核由人工完成；不等于 Decision Agent 自动裁决 |

### 1.4 与 Experiment Registry Lifecycle 对齐

Experiment Object Registry 定义 `draft → prepared` 转换条件（hypothesis、category 等字段非空）。**本 Protocol 在 Registry 条件之上增加审核门禁** — 字段完整 **且** Review 批准，方可进入 `prepared`。

---

## 2. Review Purpose（审核目标）

### 2.1 审核使命

Prepared Review 的目标是：**在消耗 Content Factory 生产资源之前**，确认实验是否具备可验证、可生产、可度量的商业实验条件。

### 2.2 五维确认

审核须确认实验满足以下维度：

| # | 维度 | 确认内容 |
|---|------|----------|
| 1 | **商业目标明确** | hypothesis、validation_goal 可复述；验证假设清晰、可证伪 |
| 2 | **用户对象明确** | target_customer 具体；非「所有人」式模糊描述 |
| 3 | **产品方向明确** | product_concept、product_type 与 Experiment 一致；Content Factory 可执行 |
| 4 | **验证指标明确** | success_metrics 四类完整；failure_condition 可定义 |
| 5 | **生产成本可接受** | expected_cost 在 Category 预算内；production_complexity 与 Category A/B/C 匹配 |

### 2.3 避免的问题

| 禁止进入 prepared 的情况 | 说明 |
|--------------------------|------|
| **无目标生产** | hypothesis 空泛或不可验证 |
| **无用户生产** | target_customer 未定义 |
| **无指标生产** | success_metrics 缺失或全为占位 |
| **超预算生产** | expected_cost 超出 Category 上限且无 override 理由 |
| **不可生产** | product_type 与 Content Factory 能力不兼容 |
| **跳过 Selection** | 无 source_selection_id / 未经过 Selection 门禁 |

---

## 3. Review Checklist（审核清单）

审核人须逐项填写四类 Review，全部通过方可 `decision: approve`。

### 3.1 Business Review（商业审核）

| 字段 | 类型 | 审核问题 | Experiment 来源字段 |
|------|------|----------|---------------------|
| `target_customer` | TEXT | 目标用户是否具体、可触达？ | `target_customer` |
| `customer_problem` | TEXT | 用户痛点是否清晰、有证据？ | Opportunity `market_problem` / Experiment `hypothesis` |
| `market_reason` | TEXT | 为何现在验证？市场需求依据？ | `validation_goal` + Opportunity `demand_evidence` |
| `expected_value` | TEXT / NUMBER | 预期定价与商业价值是否合理？ | `success_metrics.commercial_metric.expected_price_cny` |
| `business_pass` | BOOLEAN | 商业维度是否通过 | 审核人判定 |

**通过标准：** 四字段非空；`business_pass: true`；expected_value 在 Category 定价带内。

### 3.2 Product Review（产品审核）

| 字段 | 类型 | 审核问题 | Experiment 来源字段 |
|------|------|----------|---------------------|
| `product_type` | TEXT | ppt / excel / word / pdf 是否明确？ | `product_type` |
| `asset_format` | TEXT | 交付格式是否明确（pptx/xlsx/docx/pdf）？ | `product_concept` + product_type 推导 |
| `production_complexity` | TEXT | 复杂度评级：`low` / `medium` / `high` | difficulty + product_concept 评估 |
| `content_factory_compatibility` | BOOLEAN | Content Factory 当前能力是否可交付？ | 对照 CF Blueprint |
| `product_pass` | BOOLEAN | 产品维度是否通过 | 审核人判定 |

**通过标准：** Category A 须 `production_complexity: low`；`content_factory_compatibility: true`；`product_pass: true`。

### 3.3 Validation Review（验证审核）

| 字段 | 类型 | 审核问题 | Experiment 来源字段 |
|------|------|----------|---------------------|
| `hypothesis` | TEXT | 假设是否可证伪、表述完整？ | `hypothesis` |
| `success_metrics` | OBJECT | 四类 metrics 是否有明确目标值？ | `success_metrics` |
| `failure_condition` | TEXT | 何种结果判定实验失败？ | 自 Registry §6.3 Failed 规则推导 |
| `validation_period` | TEXT | 观察期多长？ | `expected_cycle` |
| `validation_pass` | BOOLEAN | 验证维度是否通过 | 审核人判定 |

**通过标准：** hypothesis 非空；success_metrics 四类均有 target；failure_condition 已定义；`validation_pass: true`。

**failure_condition 参考（Category A）：**

```
views < 20 且 clicks = 0；或 validation_period 期满且 orders = 0
```

### 3.4 Commercial Review（商业运营审核）

| 字段 | 类型 | 审核问题 | Experiment 来源字段 |
|------|------|----------|---------------------|
| `price_estimate` | NUMBER | 定价是否在 Category 定价带？ | `success_metrics.commercial_metric.expected_price_cny` |
| `distribution_channel` | TEXT | 计划发布渠道是否明确？ | `publish_channel_planned` / `validation_method` |
| `commercial_potential` | TEXT | 短期验证价值与长期潜力评估 | 审核人综合判定 |
| `commercial_pass` | BOOLEAN | 商业运营维度是否通过 | 审核人判定 |

**通过标准：** Category A 定价带 ¥9.9–¥19.9；distribution_channel 非空；`commercial_pass: true`。

### 3.5 总体判定规则

| 条件 | decision |
|------|----------|
| 四类 Review 全部 `*_pass: true` | `approve` |
| 任一 `*_pass: false` 且不可修正 | `reject` |
| 部分字段待补充 | 保持 `reviewing`，不 approve |

---

## 4. Review Object Schema v1（审核对象 Schema）

### 4.1 Experiment Review Object Schema

每条 Prepared Review 须登记为一条 **Experiment Review Object（实验审核对象）**。

```json
{
  "object_type": "experiment_review",
  "contract_version": "1.0",
  "review_id": "",
  "experiment_id": "",
  "source_opportunity_id": "",
  "source_selection_id": "",
  "review_status": "reviewing",
  "business_review": {},
  "product_review": {},
  "validation_review": {},
  "commercial_review": {},
  "decision": "approve",
  "decision_reason": "",
  "review_method": "human_assisted",
  "reviewer_note": "",
  "created_at": "",
  "completed_at": ""
}
```

### 4.2 字段说明

| 字段 | 类型 | 必填 | 用途 |
|------|------|------|------|
| `object_type` | TEXT | ✅ | 固定 `"experiment_review"` |
| `contract_version` | TEXT | ✅ | 契约版本，当前 `"1.0"` |
| `review_id` | TEXT | ✅ | 审核唯一 ID，格式建议 `erev_YYYYMMDD_NNN` |
| `experiment_id` | TEXT | ✅ | 被审核 Experiment 的 `experiment_id` |
| `source_opportunity_id` | TEXT | | 冗余 — 便于跨层查询 |
| `source_selection_id` | TEXT | | 冗余 — 追溯 Selection 决策 |
| `review_status` | TEXT | ✅ | 审核生命周期状态 — 见 §5 |
| `business_review` | OBJECT | ✅ | §3.1 商业审核清单及判定 |
| `product_review` | OBJECT | ✅ | §3.2 产品审核清单及判定 |
| `validation_review` | OBJECT | ✅ | §3.3 验证审核清单及判定 |
| `commercial_review` | OBJECT | ✅ | §3.4 商业运营审核清单及判定 |
| `decision` | TEXT | | 终态判定：`approve` / `reject` / `pending` |
| `decision_reason` | TEXT | | approve/reject 理由 — 必填于 completed |
| `review_method` | TEXT | ✅ | 当前固定 `human_assisted` — 见 §9 |
| `reviewer_note` | TEXT | | 审核人自由备注 |
| `created_at` | TEXT | ✅ | ISO-8601 创建时间 |
| `completed_at` | TEXT | | 审核完成时间 |

### 4.3 子结构示例（Blueprint 参考 — 非实例文件）

```json
{
  "business_review": {
    "target_customer": "创业初期中小企业主、独立创业者",
    "customer_problem": "缺少专业 PPT 设计能力，商业计划书排版耗时",
    "market_reason": "闲鱼同类 listing 有稳定想要数；创业类长期搜索需求",
    "expected_value": 19.9,
    "business_pass": true
  },
  "product_review": {
    "product_type": "ppt",
    "asset_format": "pptx",
    "production_complexity": "low",
    "content_factory_compatibility": true,
    "product_pass": true
  },
  "validation_review": {
    "hypothesis": "用户愿为省时间+专业外观支付 ¥19.9",
    "success_metrics": {
      "production_metric": { "target_production_cost_cny": 2.5 },
      "market_metric": { "target_views": 50, "target_clicks": 5 },
      "commercial_metric": { "target_orders": 1 },
      "system_metric": { "target_data_completeness": 0.80 }
    },
    "failure_condition": "14 天观察期 views < 20 且 clicks = 0，或 orders = 0",
    "validation_period": "14 days",
    "validation_pass": true
  },
  "commercial_review": {
    "price_estimate": 19.9,
    "distribution_channel": "xianyu",
    "commercial_potential": "Category A 首批验证；竞争中等可差异化",
    "commercial_pass": true
  }
}
```

**说明：** 以上为 Schema 示例；**本 Protocol 不生成 JSON 实例文件**。

---

## 5. Lifecycle Design（生命周期设计）

### 5.1 Review 状态定义

| 状态 | 英文 | 含义 |
|------|------|------|
| **Draft（草案）** | draft | Review 记录已创建，尚未开始审核 |
| **Reviewing（审核中）** | reviewing | 审核人正在填写四类 Checklist |
| **Prepared（已通过）** | prepared | 审核批准 — **允许** Experiment 进入 `prepared` 并创建 Production Request |
| **Rejected（已拒绝）** | rejected | 审核拒绝 — **禁止** 进入生产流程 |
| **Archived（归档）** | archived | 审核记录关闭，不再修改 |

### 5.2 Review 状态流转

```
draft
    ↓  审核人开始填写 Checklist
reviewing
    ↓  四类 Review 全部 pass
prepared（decision: approve）
    ↓  Experiment.status → prepared；可创建 Production Request
archived

reviewing
    ↓  任一维度不可通过
rejected（decision: reject）
    ↓  Experiment 保持 draft；禁止 Production Request
archived
```

### 5.3 Experiment 状态联动

| Review 终态 | Experiment 状态变化 | Production Request |
|-------------|---------------------|-------------------|
| `prepared` + `decision: approve` | `draft` → `prepared` | **允许**创建（draft） |
| `rejected` + `decision: reject` | 保持 `draft` 或标记 `review_rejected`（扩展） | **禁止** |
| `reviewing` | 保持 `draft` | **禁止** |
| `archived` | 不变 | 依 Experiment 当前状态 |

### 5.4 转换条件

| 从 | 到 | 条件 |
|----|-----|------|
| draft | reviewing | `experiment_id` 有效；Experiment `status: draft` |
| reviewing | prepared | 四类 `*_pass: true`；`decision: approve`；`decision_reason` 非空 |
| reviewing | rejected | 任一 `*_pass: false` 且不可修正；`decision: reject`；`decision_reason` 非空 |
| prepared / rejected | archived | 记录完成；Experiment 后续流程已启动或明确取消 |

### 5.5 与 Production Request Contract 衔接

Production Request Contract §3 要求 Experiment `status ≥ prepared` 方可 draft → approved。**本 Protocol 的 `prepared` Review 状态是满足该条件的必要前置**。

---

## 6. Module Responsibility（模块职责）

### 6.1 权限矩阵

| 模块 / 角色 | 允许 | 禁止 |
|-------------|------|------|
| **Human Reviewer（人工审核员）** | 创建 Experiment Review；填写四类 Checklist；作出 approve/reject 判定 | 直接调用 Content Factory；修改 Opportunity Score |
| **`3_DECISION`（未来）** | 执行 Review Policy；辅助生成 Review 草稿；批量门禁检查 | 绕过 Human Review 在 MVP Phase 1 自动 approve（须配置显式启用） |
| **`11_CONTENT_FACTORY`** | — | **审核实验**；读取 Review 做商业裁决；自行决定生产 |
| **`2_COGNITION`** | 产出 Opportunity | **不负责实验审核**；不生成 Experiment Review |
| **Experiment Review 流程** | 更新 Experiment `status`（approve 时） | **修改 Opportunity Score**；覆盖 Selection 决策 |

### 6.2 Human Reviewer — 当前唯一审核执行者

MVP Phase 1 下，Prepared Review **仅由人工完成**：

1. 读取 Experiment Object（`status: draft`）
2. 对照 §3 Checklist 逐项审核
3. 创建 Experiment Review Object
4. 作出 `approve` 或 `reject` 判定
5. approve 时更新 Experiment `status: prepared`（Implementation 时写回 assets 或 DB）

### 6.3 3_DECISION — 未来 Review Policy 执行者

**Implementation Pending。** 未来 Decision Layer 可：

- 自动预填 Review 字段（自 Experiment 映射）
- 执行 Policy 规则（如 Category A 成本上限硬门禁）
- **不得**在 MVP Phase 1 默认替代人工 approve

### 6.4 红线 — Content Factory 与 Cognition

| 禁止行为 | 原因 |
|----------|------|
| Content Factory 审核实验 | 生产层无商业裁决权 |
| 2_COGNITION 审核实验 | 认知层只提供 Opportunity，不参与 Experiment 门禁 |
| Review 修改 Opportunity Score | 评分语义隔离 — Selection 层已独立评分 |

---

## 7. Object Relationship（对象关系）

### 7.1 完整 Object 链

```
Opportunity Object
    │  职责：市场机会情报 — 有没有机会、recommendation
    ↓
Experiment Object
    │  职责：商业实验设计 — hypothesis、success_metrics、category
    ↓
Experiment Review Object
    │  职责：生产前审核 — 五维确认、approve/reject 门禁
    ↓
Production Request Object
    │  职责：生产规格 — asset/quality requirements
    ↓
Generated Product Object
    │  职责：实际生产资产 — artifact_path
    ↓
Feedback Object
    │  职责：市场反馈 — metrics、final_result
```

### 7.2 各 Object 职责对照

| Object | 核心问题 | 关键状态 / 字段 | 本 Layer 关系 |
|--------|----------|-----------------|---------------|
| **Opportunity** | 有没有机会？ | `recommendation`, `opportunity_score` | Review 只读引用，不修改 |
| **Experiment** | 验证什么？ | `status: draft → prepared` | Review 的上游输入 |
| **Experiment Review** | 能否生产？ | `decision: approve/reject` | **本 Protocol 定义** |
| **Production Request** | 生产什么规格？ | `status: draft → approved` | Review approve 后的下游 |
| **Generated Product** | 产出了什么？ | `artifact_path` | Review 不参与 |
| **Feedback** | 结果如何？ | `final_result` | Review 不参与 |

### 7.3 与 commercial_assets 实例层关系

| 路径 | 当前状态 | Review 关系 |
|------|----------|-------------|
| `commercial_assets/experiments/experiments_v1.json` | 4 条 `draft` | **待审核** — Review 实例未创建 |
| `commercial_assets/experiment_selection/` | 4 selected | Review 可读 selection 理由 |
| `commercial_assets/opportunities/` | 5 条 | Review 可读 market_problem / demand_evidence |
| `commercial_assets/experiment_reviews/` | **未创建** | 本 Protocol 仅为设计规范 |

---

## 8. Database Future Mapping（未来数据库映射）

### 8.1 设计原则

| 原则 | 说明 |
|------|------|
| **Database Extension Pending** | 表设计仅为 Blueprint — **禁止 CREATE TABLE** |
| **Additive Evolution** | 不破坏现有 Legacy 表 |
| **Review 为独立登记** | 不与 Experiment 表合并 — 保留审核历史 |

### 8.2 建议表：experiment_reviews

**状态：Blueprint 设计 — 未创建**

| 列名 | 类型 | 映射字段 | 说明 |
|------|------|----------|------|
| `id` | INTEGER PK | — | 自增主键 |
| `review_id` | TEXT UNIQUE | `review_id` | 业务主键 |
| `experiment_id` | TEXT | `experiment_id` | FK → commercial_experiments（未来） |
| `status` | TEXT | `review_status` | draft / reviewing / prepared / rejected / archived |
| `decision` | TEXT | `decision` | approve / reject / pending |
| `review_data` | TEXT / JSON | 四类 Review 合并 | business + product + validation + commercial |
| `review_method` | TEXT | `review_method` | human_assisted |
| `decision_reason` | TEXT | `decision_reason` | |
| `created_at` | TIMESTAMP | `created_at` | |
| `completed_at` | TIMESTAMP | `completed_at` | |

### 8.3 ER 关系（Blueprint）

```
commercial_experiments（未来）
        ↓ experiment_id
experiment_reviews（未来 — 本 Protocol）
        ↓ decision=approve
production_requests（未来 — Production Request Contract）
        ↓
generated_products（未来）
```

**实施须走：** [Database Extension Implementation Plan](../database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md) — 须单独审批。

---

## 9. Human Assisted Phase（人工辅助阶段）

### 9.1 当前阶段定义

| 项 | MVP Phase 1 现实 |
|----|------------------|
| **审核执行者** | Human Reviewer（人工审核员） |
| **review_method** | 固定 `"human_assisted"` |
| **Decision Agent** | ❌ 不参与 Review approve |
| **Policy Engine** | ❌ 未接入 Review 流程 |
| **Review JSON 实例** | ❌ 未创建 — 本任务禁止 |

### 9.2 Human Assisted ≠ Automation

| Human Assisted | Automation（未来） |
|----------------|-------------------|
| 人工逐项填写 Checklist | Decision Agent 预填 + Policy 硬门禁 |
| 人工作出 approve/reject | 满足 Policy 可辅助建议，默认不自动 approve |
| 人工更新 Experiment status | Runtime 写回 assets / DB |
| 明确标注 `review_method: human_assisted` | 未来可增 `policy_assisted` / `automated` |

**规则：** 文档或资产中出现 `human_assisted` **不等于** Cognition Automation 或 Runtime 自动执行。

### 9.3 未来演进路径

```
Phase 1（当前）: Human Reviewer + human_assisted
        ↓
Phase 2: Decision Layer Review Policy — 预填 + 硬门禁，人工 confirm
        ↓
Phase 3: Policy Engine 辅助 — 批量审核建议，关键实验仍须人工 approve
```

**门禁：** Phase 2+ 任何自动化 **不得** 默认跳过 Human Review；须配置显式启用并审计。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Experiment Object Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` |
| Production Request Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md` |
| Commercial Experiment Selection Framework | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md` |
| Commercial Experiment System Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Experiment Prepared Review Protocol v1 设计；Review JSON 实例、Experiment status 写回、Decision Policy 接入均 **Pending**，须单独审批后实施。
