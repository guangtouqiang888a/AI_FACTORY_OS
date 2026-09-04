# AI_FACTORY_OS Experiment Evaluation Framework v1

> 实验评估框架层 | 最后更新：2026-07-13  
> **状态：Blueprint Completed — Project Intelligence Layer 评估规范，不参与运行计算**

**定位：** Experiment Evaluation Framework Layer（实验评估框架层）— 定义 **Feedback Object（反馈对象）** 聚合后如何产生 **Experiment Evaluation Object（实验评估对象）**、如何对照 Experiment `success_metrics` 判定假设结果、如何产出 **Learning Signal（学习信号）** 并影响未来 Selection，同时严格隔离四类评分体系。

**上级文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md](../contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md) — Feedback Object Schema
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md) — Experiment Object 与 success_metrics
- [docs/04_BLUEPRINT/protocol/AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md](../protocol/AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md) — Prepared Review 门禁
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md](AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md) — Selection 与 Priority Score
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](../contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md) — Product Asset → Feedback 链路

**当前资产状态（只读审计）：**

| 资产 | 状态 |
|------|------|
| Pilot Product Asset | ✅ `8523329941d4` — exp_20260708_005 |
| Feedback 实例 | ❌ **未创建** |
| Evaluation 实例 | ❌ **未创建** |
| 市场验证 | ❌ **未执行** |

**说明：** **Blueprint ≠ Implementation**。**Feedback Design ≠ Market Validation**。**Human Assisted ≠ Automation**。**Production Completed ≠ Commercial Success**。本文档只定义评估框架；不创建 Evaluation JSON、不修改 Runtime、不执行市场验证。

---

## §1 Evaluation Layer Position（评估层定位）

### 1.1 完整学习链路

```
Product Asset Object
        ↓
Feedback Object（多条 — 五类）
        ↓
Experiment Evaluation Object          ← 本 Framework 定义
        ↓
Learning Signal
        ↓
Failure / Success Learning
        ↓
Selection Framework
        ↓
Future Experiment Priority
```

### 1.2 Experiment Evaluation 不是什么

| Evaluation **是** | Evaluation **不是** |
|-------------------|---------------------|
| 对照 Experiment hypothesis 的**结构化裁决** | 单条 Feedback 的简单加总 |
| 基于 success_metrics / failure_metrics 的**可审计结论** | Market Success 的最终财务认定 |
| 产生 learning_summary 供 Selection 消费 | Opportunity Score 的替代品 |
| **Failure 也是资产** — 记录失败原因与信号 | 伪造数据以达成 success |

---

## §2 Experiment Evaluation Object Schema v1

### 2.1 标准 Object

```json
{
  "evaluation_id": "eval_20260720_001",
  "object_type": "experiment_evaluation",
  "contract_version": "1.0",
  "experiment_id": "exp_20260708_005",
  "product_asset_id": "8523329941d4",
  "source_production_request_id": "preq_20260712_005",
  "evaluation_method": "human_assisted",
  "hypothesis_result": "pending",
  "success_metrics": {},
  "failure_metrics": {},
  "feedback_summary": {},
  "experiment_evaluation_score": null,
  "learning_summary": "",
  "recommendation": "continue_observation",
  "evaluation_status": "draft",
  "observation_period": {
    "start": "ISO-8601",
    "end": "ISO-8601"
  },
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 用途 |
|------|------|------|------|
| `evaluation_id` | TEXT | ✅ | 唯一 ID；格式 `eval_YYYYMMDD_NNN` |
| `object_type` | TEXT | ✅ | 固定 `"experiment_evaluation"` |
| `contract_version` | TEXT | ✅ | `"1.0"` |
| `experiment_id` | TEXT | ✅ | FK → Experiment |
| `product_asset_id` | TEXT | ✅ | FK → Product Asset |
| `source_production_request_id` | TEXT | | PR 追溯 |
| `evaluation_method` | TEXT | ✅ | MVP Phase 1：`human_assisted` |
| `hypothesis_result` | TEXT | ✅ | 见 §4 |
| `success_metrics` | OBJECT | ✅ | 对照 Experiment 成功指标 — 实际 vs 目标 |
| `failure_metrics` | OBJECT | ✅ | 触发的失败条件 |
| `feedback_summary` | OBJECT | | 聚合 Feedback 引用 |
| `experiment_evaluation_score` | NUMBER | | 0.0–1.0 — 见 §5（独立评分） |
| `learning_summary` | TEXT | ✅ | 可复述的学习结论 |
| `recommendation` | TEXT | ✅ | 见 §4.3 |
| `evaluation_status` | TEXT | ✅ | draft / in_review / finalized / archived |
| `observation_period` | OBJECT | | 评估窗口 |
| `created_at` | TEXT | ✅ | ISO-8601 |
| `updated_at` | TEXT | | ISO-8601 |

### 2.3 success_metrics / failure_metrics 结构

```json
{
  "success_metrics": {
    "market": {
      "listing_views_7d": { "target": 100, "actual": 0, "met": false },
      "ctr_7d": { "target": 0.02, "actual": null, "met": null }
    },
    "sales": {
      "orders_7d": { "target": 1, "actual": 0, "met": false },
      "conversion_rate_7d": { "target": 0.01, "actual": null, "met": null }
    },
    "quality": {
      "post_publish_quality_score": { "target": 0.85, "actual": null, "met": null }
    }
  },
  "failure_metrics": {
    "zero_orders_after_14d": { "triggered": false },
    "quality_complaint": { "triggered": false }
  }
}
```

**规则：** `actual` 来自 Feedback Object 聚合；**禁止**无 Feedback 时填非 null 假值。

---

## §3 Evaluation Process（评估流程）

### 3.1 触发条件

| # | 条件 |
|---|------|
| 1 | Product Asset 存在且 `validation_status=passed` |
| 2 | 至少一条 `feedback_status=recorded` 的 Feedback（按类型覆盖观察期） |
| 3 | Experiment `validation_period` 观察窗口结束 |
| 4 | 人工触发 Evaluation（Human Assisted） |

### 3.2 评估步骤（Design SOP）

```
1. 加载 Experiment Object — hypothesis, success_metrics, failure_condition
2. 加载 Product Asset — product_asset_id, source_experiment_id
3. 聚合 Feedback Objects — 按 feedback_type + metric_name
4. 填充 success_metrics.actual / failure_metrics.triggered
5. 判定 hypothesis_result
6. 计算 experiment_evaluation_score（独立公式 — §5）
7. 撰写 learning_summary + recommendation
8. 产出 Experiment Evaluation Object — evaluation_status=finalized
```

### 3.3 Pilot exp_20260708_005 评估预览（非实例）

| 项 | 设计值 |
|----|--------|
| hypothesis | 小团队管理员愿为考勤 Excel 支付 ¥12.9 |
| validation_goal | 低竞争细分是否有首单转化 |
| product_asset_id | `8523329941d4` |
| **当前状态** | Evaluation **Pending** — 无 Feedback、未上架 |

---

## §4 Hypothesis Result & Recommendation（假设结果与建议）

### 4.1 hypothesis_result 枚举

| 值 | 含义 | 条件（Design） |
|----|------|----------------|
| `success` | 假设成立 | 核心 success_metrics 达标且无 failure 触发 |
| `promising` | 有信号但未达标 | 部分 metrics 正向；可延长观察 |
| `failed` | 假设不成立 | failure_metrics 触发或核心 metrics 明确未达标 |
| `inconclusive` | 数据不足 | 观察期内 Feedback 不足 |
| `pending` | 未评估 | 初始状态 |

### 4.2 Failure 也是资产

| 原则 | 说明 |
|------|------|
| **Failed experiments 须完整记录** | failure_metrics、learning_summary 必填 |
| **失败信号进入 Selection** | 降低同类 experiment_priority；不删除历史 |
| **禁止隐藏失败** | 不得因 Pilot 情感而改为 success |
| **可复用 learning** | 结构/定价/渠道洞察供 Future Experiment |

### 4.3 recommendation 枚举

| 值 | 含义 |
|----|------|
| `scale` | 扩大生产 / 同品类更多实验 |
| `iterate` | 改进产品后再测 |
| `continue_observation` | 延长观察期 |
| `pause` | 暂停同方向实验 |
| `stop` | 停止该假设方向 |
| `watch` | 保持观察、不消耗配额 |

---

## §5 Score Isolation（评分隔离 — 四者禁止混用）

### 5.1 四类评分对照

| 评分 | 英文 | 负责层 | 核心问题 | 消费者 |
|------|------|--------|----------|--------|
| **Candidate Readiness Score** | candidate_readiness_score | Opportunity Candidate Registry | Candidate **是否进入** Opportunity？ | Selection 前置 |
| **Opportunity Score** | opportunity_score | 2_COGNITION | 机会**本身质量**如何？ | Opportunity 排序 |
| **Experiment Priority Score** | experiment_priority_score | Experiment Selection | **是否值得**消耗配额验证？ | Experiment 创建队列 |
| **Experiment Evaluation Score** | experiment_evaluation_score | **本 Framework** | 实验**结果**如何？ | Learning、Future Priority |

### 5.2 禁止混用规则

| 禁止 | 原因 |
|------|------|
| 用 Opportunity Score 代替 Evaluation Score | 机会质量 ≠ 实验结果 |
| 用 Experiment Priority Score 判定 hypothesis_result | 优先级是事前；Evaluation 是事后 |
| 用 Product Asset quality_score 代替 Evaluation Score | 生产质量 ≠ 市场验证 |
| 用 Feedback 单指标直接作为 Evaluation Score | 须经 Framework 聚合与对照 success_metrics |
| 用 Candidate Readiness 回溯修改 Evaluation | 方向只读消费 |

### 5.3 Experiment Evaluation Score 公式（Blueprint v1）

```
experiment_evaluation_score =
      0.35 × success_metric_achievement_rate
    + 0.25 × sales_signal_score
    + 0.20 × market_signal_score
    + 0.10 × quality_signal_score
    + 0.10 × operational_efficiency_score
```

| 分量 | 来源 |
|------|------|
| `success_metric_achievement_rate` | success_metrics 中 met=true 占比 |
| `sales_signal_score` | sales_feedback 归一化 |
| `market_signal_score` | market_feedback 归一化 |
| `quality_signal_score` | quality_feedback vs target |
| `operational_efficiency_score` | operational_feedback vs PR category_a_threshold |

**尺度：** 0.0–1.0。**独立存储** — 不与 opportunity_score / experiment_priority_score 共字段。

---

## §6 Learning Loop（学习闭环）

### 6.1 闭环图

```
Feedback（多条观测）
        ↓
Experiment Evaluation（hypothesis_result + learning_summary）
        ↓
Learning Signal（结构化摘要 — 非 Score 替代）
        ↓
Selection Framework 更新
    ├── 成功 → 同品类 Priority 上调（有限幅度）
    ├── 失败 → 同假设方向 Priority 下调 + 记录 failure pattern
    └── promising → watch 队列
        ↓
Future Experiment Priority / Opportunity Candidate 特征
```

### 6.2 Learning Signal 结构（Design）

```json
{
  "signal_id": "learn_20260720_001",
  "source_evaluation_id": "eval_20260720_001",
  "experiment_id": "exp_20260708_005",
  "signal_type": "failure_learning",
  "pattern": "zero_conversion_7d_excel_attendance",
  "confidence": "human_assisted",
  "summary": "7 日零订单 — 渠道曝光不足或定价需验证",
  "recommended_action": "continue_observation",
  "created_at": "ISO-8601"
}
```

**存储（Future）：** `7_MEMORY` 可消费摘要；**权威源**仍为 Evaluation + Feedback JSON。

### 6.3 与 Experiment Registry 状态回填

| hypothesis_result | Experiment status 建议（Future） |
|-------------------|----------------------------------|
| success | `validated` |
| promising | `testing` |
| failed | `failed` |
| inconclusive | `testing` |

**规则：** Evaluation finalized **不自动**修改 Experiment JSON（MVP 人工确认写回）。

---

## §7 Human Assisted Phase（人工辅助阶段）

| 项 | MVP Phase 1 |
|----|-------------|
| `evaluation_method` | `human_assisted` |
| 数据录入 | 人工聚合 Feedback → 填 success_metrics.actual |
| 裁决 | 人工确认 hypothesis_result |
| **禁止** | 伪造销售/用户/市场数据 |
| **禁止** | 无 Feedback 时 finalized=success |

---

## §8 Future Automation（未来自动化）

| 阶段 | 行为 |
|------|------|
| Phase 1 | Human Assisted Evaluation |
| Phase 2 | 系统自动聚合 Feedback + 人工确认 hypothesis_result |
| Phase 3 | CustomerAgent / SalesAgent / MarketAgent 写入 Feedback → Cognition 辅助 Evaluation |
| Phase 4 | 2_COGNITION 读取 Evaluation 优化 Selection 特征（不替代 Evaluation Score） |

**Agent 边界：** QualityAgent（CF）产出生产质量；**不**产出 Experiment Evaluation Score。

---

## §9 Database Mapping（数据库映射 — Blueprint Only）

### 9.1 表：`experiment_evaluations`（预留 — 禁止 CREATE TABLE）

| 列 | 类型 | 映射字段 |
|----|------|----------|
| `id` | INTEGER PK | 内部 ID |
| `evaluation_id` | TEXT UNIQUE | `evaluation_id` |
| `experiment_id` | TEXT | `experiment_id` |
| `product_asset_id` | TEXT | `product_asset_id` |
| `production_request_id` | TEXT | `source_production_request_id` |
| `evaluation_method` | TEXT | `evaluation_method` |
| `hypothesis_result` | TEXT | `hypothesis_result` |
| `experiment_evaluation_score` | REAL | `experiment_evaluation_score` |
| `success_metrics_json` | TEXT / JSON | `success_metrics` |
| `failure_metrics_json` | TEXT / JSON | `failure_metrics` |
| `feedback_summary_json` | TEXT / JSON | `feedback_summary` |
| `learning_summary` | TEXT | `learning_summary` |
| `recommendation` | TEXT | `recommendation` |
| `evaluation_status` | TEXT | `evaluation_status` |
| `created_at` | TEXT | `created_at` |
| `updated_at` | TEXT | `updated_at` |

**索引（设计）：** `(experiment_id)`, `(product_asset_id)`, `(hypothesis_result)`

### 9.2 commercial_assets 扩展（Future）

```
commercial_assets/
├── feedback/                    ← 【未来】
├── experiment_evaluations/      ← 【未来】
│   └── experiment_evaluations_v1.json
└── product_assets/              ← 已有
```

**本任务：** ❌ 不创建 evaluation JSON 实例

---

## §10 Version Strategy（版本策略）

| 版本 | 范围 | 当前 |
|------|------|------|
| Experiment Evaluation Framework | 评估流程、Score 公式、Object Schema | **1.0** |
| Feedback Object Contract | Feedback Schema | 1.0 |
| Experiment Object Registry | success_metrics 定义 | 1.0 |
| Database Schema | 表结构 | Pending |

**规则：** success_metrics 字段变更须同步 minor bump Evaluation Framework 文档。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Feedback Object Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md` |
| Experiment Prepared Review Protocol | `docs/04_BLUEPRINT/protocol/AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md` |
| Experiment Selection Framework | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md` |
| Product Asset 实例 | `commercial_assets/product_assets/product_assets_v1.json` |

---

**Blueprint ≠ Implementation。** **Feedback Design ≠ Market Validation。** 本文档完成 Experiment Evaluation Framework v1；Evaluation 实例、Feedback 实例、市场验证均 **Pending**。
