# AI_FACTORY_OS Commercial State Alignment Report

> **文档角色（Document Role）：** 本文档为历史参考资料，用于理解演进过程，不作为当前最高判断来源。  
> Current highest judgment（当前最高判断）：CURRENT_STATE + Asset Reality（`commercial_assets/`）+ BUSINESS_STRATEGY。

> Entry 038-B | commercial_assets/ 状态对齐报告 | 2026-07-13  
> **不自动修改 JSON。不猜测业务状态。**

**方法：** 读取 JSON 实际字段；列出 ID 关系与 **字段间状态冲突**；供人工决策后续同步 Entry。

---

## 1. ID 关系链（Pilot 完整路径）

```
cand_20260708_005
  → opp_20260708_005
  → sel_20260708_005 (decision: selected)
  → exp_20260708_005
  → erev_20260709_005 (decision: prepared)
  → preq_20260712_005
  → appr_20260713_005 (decision: approved)
  → Product Asset 8523329941d4 (generation_status: completed, validation_status: passed)
  → pval_20260713_ac223d (validation_status: passed)
  → fbk_20260713_001 (feedback_status: pending, observation_period: not_started)
  → eval_20260713_001 (hypothesis_result: pending)
```

**ID 引用一致性：** ✅ 全部 cross-reference 字段匹配（038-A 已确认）

---

## 2. 各层对象状态快照（JSON 原文）

### Opportunity（5 条）

| opportunity_id | status 字段值 |
|----------------|---------------|
| opp_20260708_001 ~ 005 | `human_assisted` |

**说明：** Opportunity 使用 creation method 语义作 status，非 lifecycle status。

---

### Experiment Selection（5 条）

| selection_id | decision |
|--------------|----------|
| sel_20260708_001,003,004,005 | `selected` |
| sel_20260708_002 | `watch` |

---

### Experiment（4 条）

| experiment_id | status | experiment_review decision |
|---------------|--------|--------------------------|
| exp_20260708_001 | `draft` | prepared |
| exp_20260708_002 | `draft` | rejected |
| exp_20260708_004 | `draft` | prepared |
| exp_20260708_005 | `draft` | prepared |

---

### Production Request（3 条）

| production_request_id | status | approval decision |
|-----------------------|--------|-------------------|
| preq_20260712_001 | `draft` | approved |
| preq_20260712_004 | `draft` | approved |
| preq_20260712_005 | `draft` | approved |

---

### Product Asset（1 条 — Pilot）

| product_asset_id | generation_status | validation_status |
|------------------|-------------------|-------------------|
| 8523329941d4 | `completed` | `passed` |

**source_production_request_id:** `preq_20260712_005`  
**source_experiment_id:** `exp_20260708_005`

---

### Feedback（1 条）

| feedback_id | feedback_status | observation_period | metric_value |
|-------------|-----------------|-------------------|--------------|
| fbk_20260713_001 | `pending` | `not_started` | null |

---

### Evaluation（1 条）

| eval_id | hypothesis_result | observation_period.status |
|---------|---------------------|---------------------------|
| eval_20260713_001 | `pending` | `not_started` |

---

## 3. 状态冲突清单

> **冲突定义：** 同一对象链上，上游 status 与下游已完成事实 **字段值不一致**（非业务推断）。

### CSA-001 — Experiment status vs Production 完成

| 字段 | 值 A | 值 B |
|------|------|------|
| `experiments_v1.json` → exp_20260708_005.status | `draft` | |
| `product_assets_v1.json` → 8523329941d4.generation_status | | `completed` |
| PROJECT_STATUS 声明 | | Pilot Production Completed |

**冲突：** Experiment 对象 status 未反映 Pilot 生产已完成。  
**不猜测：** 是否应改为 `in_production` / `produced` 须 Contract/人工 Entry 定义。

---

### CSA-002 — Production Request status vs Approval + Production

| 字段 | 值 |
|------|-----|
| preq_20260712_005.status | `draft` |
| appr_20260713_005.decision | `approved` |
| 8523329941d4.generation_status | `completed` |

**同样适用于：** preq_001, preq_004（approved 但 PR status=draft，且无 Product Asset）

**冲突：** PR.status 与 Approval 及 Pilot 生产事实不同步。

---

### CSA-003 — Experiment Review prepared vs Experiment draft

| 字段 | 值 |
|------|-----|
| exp_20260708_001.status | `draft` |
| erev_20260709_001.decision | `prepared` |

**冲突：** Review 层 decision=prepared 未回写 Experiment.status。

---

### CSA-004 — Opportunity status 语义 vs Lifecycle

| 字段 | 值 |
|------|-----|
| opp_*.status | `human_assisted` |

**冲突类型：** 语义歧义 — 非 lifecycle 状态字段，与 Experiment `draft` 不可直接比较。  
**建议：** 文档区分 `creation_method` vs `lifecycle_status`（设计项，非 JSON 修改）。

---

### CSA-005 — Pilot artifact metadata vs Product Asset

| 位置 | status |
|------|--------|
| `pilot_outputs/.../artifacts/metadata.json` | `draft` |
| `product_assets_v1.json` → 8523329941d4 | generation_status: `completed` |

**冲突：** Pilot 输出副本 metadata 与 canonical Product Asset 状态不一致。

---

### CSA-006 — 无冲突（预期 pending）

| 对象 | 状态 | 说明 |
|------|------|------|
| fbk_20260713_001 | pending / not_started | 与 Observation Protocol planned 一致 ✅ |
| eval_20260713_001 | pending | 与 Feedback 未开始一致 ✅ |

---

## 4. Pilot 外 PR 状态

| PR | Approval | Adapter 可执行 | Product Asset |
|----|----------|--------------|---------------|
| preq_20260712_001 | approved | ❌ pilot whitelist | ❌ |
| preq_20260712_004 | approved | ❌ pilot whitelist | ❌ |
| preq_20260712_005 | approved | ✅ executed | ✅ 8523329941d4 |

**冲突 CSA-007：** Approval `approved` 与 Adapter Pilot Gate 白名单策略并存 — 非 JSON 字段冲突，属 **策略 vs 登记** 差异。

---

## 5. 与文档声明对照

| 文档声明 | JSON 事实 | 一致？ |
|----------|-----------|--------|
| PROJECT_STATUS: PR Approval approved 3 | reviews: 3 approved | ✅ |
| PROJECT_STATUS: PR Instance 3 draft | PR status 全 draft | ✅（自洽但未反映 downstream） |
| PROJECT_STATUS: Pilot Production Completed | product_asset completed | ✅ |
| experiments 4 draft | exp_005 已有 product | ❌ CSA-001 |

---

## 6. 建议方向（不实施）

| ID | 建议 |
|----|------|
| CSA-001/002/003 | 单独 Entry：Commercial JSON lifecycle status 同步（human_assisted 授权） |
| CSA-004 | Contract 文档区分 status 字段语义 |
| CSA-005 | pilot_outputs 标注为 snapshot copy，非 SoT |
| CSA-007 | 文档明确 Pilot Policy；或 Entry 扩展 whitelist |

---

## 7. 本 Entry 操作

- ✅ 只读分析
- ❌ 未修改任何 commercial_assets JSON
- ✅ Pilot 8523329941d4 / preq_005 可追溯性保持
