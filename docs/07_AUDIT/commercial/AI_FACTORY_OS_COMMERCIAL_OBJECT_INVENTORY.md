# AI_FACTORY_OS Commercial Object Inventory

> Entry 039-B — Commercial Lifecycle State Authority Design v1  
> 盘点日期：2026-07-14  
> **方法：** 只读 `commercial_assets/` JSON  
> **禁止：** 本 Entry 未修改任何 JSON

**原则：** Historical Reality ≠ Target Lifecycle Design · Commercial SoT = `commercial_assets/`（非 SQLite）

---

## Chain Overview

```
Opportunity Candidate → Opportunity → Selection
  → Experiment → Experiment Review
  → Production Request → Approval
  → Production (CF) → Validation → Product Asset
  → Feedback → Evaluation
```

---

## Opportunity Candidate

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/opportunity_candidates/opportunity_candidates_v1.json` |
| **当前数量** | 5 |
| **当前状态字段** | `status` |
| **当前状态值** | 全部 `discovered`（cand_20260708_001~005） |
| **上游对象** | —（入口池） |
| **下游对象** | Opportunity；Selection |

---

## Opportunity

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/opportunities/opportunities_v1.json` |
| **当前数量** | 5 |
| **当前状态字段** | `status` |
| **当前状态值** | 全部 `human_assisted`（**注意：创建方式语义，非 lifecycle**） |
| **上游对象** | Candidate（source_candidate_id） |
| **下游对象** | Selection / Experiment |

---

## Experiment Selection Record

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/experiment_selection/experiment_selection_records_v1.json` |
| **当前数量** | 5 |
| **当前状态字段** | `decision` |
| **当前状态值** | selected×4（001,002,004,005）；watch×1（003） |
| **上游对象** | Candidate / Opportunity |
| **下游对象** | Experiment |

---

## Experiment

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/experiments/experiments_v1.json` |
| **当前数量** | 4（无 exp_003 — watch 未建实验） |
| **当前状态字段** | `status` |
| **当前状态值** | 全部 `draft`（001, 002, 004, 005） |
| **上游对象** | Opportunity, Selection, Candidate |
| **下游对象** | Experiment Review → Production Request；Evaluation |

---

## Experiment Review（Prepared Review）

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/experiment_reviews/experiment_reviews_v1.json` |
| **当前数量** | 4 |
| **当前状态字段** | `decision` |
| **当前状态值** | prepared×3（001,004,005）；rejected×1（002） |
| **上游对象** | Experiment / Opportunity / Selection |
| **下游对象** | Production Request（仅 prepared） |

---

## Production Request

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/production_requests/production_requests_v1.json` |
| **当前数量** | 3 |
| **当前状态字段** | `status` |
| **当前状态值** | 全部 `draft`（preq_001, 004, 005） |
| **上游对象** | Experiment, Experiment Review, Opportunity, Selection |
| **下游对象** | Approval → CF Adapter → Product Asset |

---

## Approval（Production Request Review）

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/production_request_reviews/production_request_reviews_v1.json` |
| **当前数量** | 3 |
| **当前状态字段** | `decision` |
| **当前状态值** | 全部 `approved`（appr_001, 004, 005） |
| **上游对象** | Production Request, Experiment |
| **下游对象** | CF Adapter（ApprovalGate）；Product Asset |

---

## Product Asset

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/product_assets/product_assets_v1.json` |
| **当前数量** | 1 |
| **当前状态字段** | `generation_status`, `validation_status` |
| **当前状态值** | `8523329941d4` → generation_status=`completed`, validation_status=`passed` |
| **上游对象** | PR `preq_20260712_005`, Experiment `exp_20260708_005`, Approval `appr_20260713_005`, Opportunity `opp_20260708_005` |
| **下游对象** | Validation 记录；Feedback；Evaluation |

**物理交付物（非 JSON SoT）：** `11_CONTENT_FACTORY/artifacts/products/8523329941d4/`

---

## Validation

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/product_asset_validations/product_asset_validations_v1.json` |
| **当前数量** | 1 |
| **当前状态字段** | `validation_status` |
| **当前状态值** | `pval_20260713_ac223d` → `passed` |
| **上游对象** | Product Asset `8523329941d4`, PR, Experiment, Approval |
| **下游对象** | 支撑 Product Asset.validation_status；门禁下游 Feedback |

---

## Feedback

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/feedback/feedback_v1.json` |
| **当前数量** | 1 |
| **当前状态字段** | `feedback_status`, `observation_period` |
| **当前状态值** | `fbk_20260713_001` → feedback_status=`pending`, observation_period=`not_started`；metric_value=`null` |
| **上游对象** | Product Asset, Experiment, PR |
| **下游对象** | Evaluation |

---

## Evaluation

| 字段 | 值 |
|------|-----|
| **当前存储位置** | `commercial_assets/experiment_evaluations/experiment_evaluations_v1.json` |
| **当前数量** | 1 |
| **当前状态字段** | `hypothesis_result`；`observation_period.status`（嵌套） |
| **当前状态值** | `eval_20260713_001` → hypothesis_result=`pending`；observation_period.status=`not_started` |
| **上游对象** | Experiment / Feedback / Product Asset / PR |
| **下游对象** | Memory Learning（设计）；Selection Failure Learning（设计） |

---

## Summary Counts

| 对象 | 数量 | 主导状态字段值 |
|------|------|----------------|
| Candidate | 5 | discovered |
| Opportunity | 5 | human_assisted |
| Selection | 5 | selected/watch |
| Experiment | 4 | draft |
| Exp Review | 4 | prepared/rejected |
| Production Request | 3 | draft |
| Approval | 3 | approved |
| Product Asset | 1 | completed + passed |
| Validation | 1 | passed |
| Feedback | 1 | pending |
| Evaluation | 1 | pending |

**存储结论：** 全部位于 `commercial_assets/` JSON；**不在** `data/ai_factory.db`。
