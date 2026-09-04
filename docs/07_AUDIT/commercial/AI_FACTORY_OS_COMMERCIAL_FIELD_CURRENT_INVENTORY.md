# AI_FACTORY_OS Commercial Field Current Inventory

> Entry 039-C — Commercial Lifecycle Field Normalization Design v1  
> 盘点日期：2026-07-14  
> **方法：** 只读 `commercial_assets/`  
> **禁止：** 未修改 JSON

**原则：** Historical Field Reality ≠ Target Field Standard

---

## Candidate

| 字段名 | 类型 | 当前值（样例） | 语义 | 问题 |
|--------|------|----------------|------|------|
| `status` | string | `discovered` | 候选生命周期（近似） | 名称为泛化 `status`；converted 后未更新 |
| `competition_status` | string | 叙述文本 | **竞争描述**，非 enum 状态 | 名称含 status 易误解为 lifecycle |
| `quality_assessment` | object | 结构体 | 质量评估内容 | 非状态字段 |

---

## Opportunity

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `status` | string | `human_assisted` | 实际为 **创建方式** | **严重：** 占用 lifecycle 语义；与 Experiment.status 不可比 |
| `score_method` | string | `human_assisted_score` | 评分方法 | OK |
| `validation_reason` | string | 长文本 | 为何值得验证 | 非 validation_status |

---

## Experiment Selection

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `decision` | string | `selected` / `watch` | 选择决策 | 非统一 lifecycle_status |
| `conversion_status` | string | `pending_experiment` / `none` | 转化进度 | 与 Candidate.status 未联动 |
| `selection_method` | string | `human_assisted` | 方法 | OK |

---

## Experiment

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `status` | string | `draft`（4/4） | 意图为 lifecycle | 与 Review/PR/Asset 完成态冲突；无 `approved/running/completed` |
| `experiment_method` | string | `human_assisted` | 创建方法 | OK |
| `validation_goal` | string | 文本 | 验证目标描述 | **不是** validation_status |
| `validation_method` | string | 文本 | 验证方法描述 | 易与 validation_status 混淆 |
| `hypothesis` | string | 文本 | 假设 | OK |

---

## Experiment Review

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `decision` | string | `prepared` / `rejected` | 审核决定 | 与 `review_status` 重复语义 |
| `review_status` | string | `prepared` / `rejected` | 审核状态 | **与 decision 双字段同值** |
| `review_method` | string | `human_assisted` | 方法 | OK |
| `validation_review` | object | 含 validation_pass bool | 审核清单结果 | 嵌套「validation」≠ Product validation_status |

---

## Production Request

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `status` | string | `draft`（3/3） | 意图 lifecycle | Approval 后仍 draft；无 execution_status |
| `creation_method` | string | `human_assisted` | 创建方法 | OK |
| `validation_goal` | string | 文本 | 继承实验目标 | 非状态 |
| `quality_requirements` | object | 阈值/checklist | 质量门禁配置 | 非 validation_status |

---

## Approval

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `decision` | string | `approved` | 审批决定 | 权威；但未映射到 PR.status |
| `review_method` | string | `human_assisted` | 方法 | OK |
| （无 status） | — | — | — | 对象只用 decision |

---

## Product Asset

| 字段名 | 类型 | 当前值（8523329941d4） | 语义 | 问题 |
|--------|------|--------------------------|------|------|
| `generation_status` | string | `completed` | **执行/生成**完成 | 名非 execution_status；`completed` 易与 lifecycle completed 混淆 |
| `validation_status` | string | `passed` | 验收 | ✅ 接近标准 validation_status |
| `creation_method` | string | `adapter_generated` | 创建方式 | OK |
| `quality_score` | number | 0.89 | 分数 | 非状态 |
| `artifact_information.quality_result.status` | string | `quality_pass` | CF 质量闸 | **第三套 status**；与 validation_status 并存 |
| `release_status` | — | **JSON 中不存在** | — | CF pipeline 内存/product_memory 可能有；Commercial SoT 未统一 |

---

## Validation

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `validation_status` | string | `passed` | 验收总状态 | ✅ |
| `validation_result.overall` | string | `passed` | 与上重复 | 冗余 |
| `validation_method` | string | `human_assisted` | 方法 | OK |

---

## Feedback

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `feedback_status` | string | `pending` | 反馈生命周期近似 | 应拆 lifecycle vs collection |
| `observation_period` | string | `not_started` | 观察窗 | 类型为 string；Evaluation 同概念为 object |
| `feedback_type` / `feedback_method` / `feedback_source` | string | market_feedback / human_assisted / human_observation | 分类 | OK |
| （无 evaluation_status） | — | — | — | Feedback 不含评估字段（正确） |

---

## Evaluation

| 字段名 | 类型 | 当前值 | 语义 | 问题 |
|--------|------|--------|------|------|
| `evaluation_status` | string | `pending` | 评估过程状态 | ✅ 接近标准 |
| `hypothesis_result` | string | `pending` | **结论**语义 | 与 evaluation_status 双 pending；结论域应用 success/failed 等 |
| `observation_period` | object | status=`not_started` | 观察窗 | 与 Feedback 结构不一致 |
| `evaluation_method` | string | `human_assisted` | 方法 | OK |

---

## Cross-Object Field Collision Summary

| 泛化名 `status` / `*status` | 出现对象 | 实际含义是否相同 |
|----------------------------|----------|------------------|
| `status` | Candidate, Opportunity, Experiment, PR | **否** — discovery / creation_method / lifecycle / lifecycle |
| `validation_*` | Experiment 文本、Review 嵌套、Product/Validation | **否** — 目标描述 vs 验收 enum |
| `completed` | Product Asset `generation_status` | ≠ Experiment lifecycle `completed` |
| `pending` | Feedback, Evaluation | 相近但维度不同（采集 vs 评估） |
| `decision` | Selection, ExpReview, Approval | 决策类 — 应与 lifecycle_status 区分 |

**Commercial SoT 中未见统一 `release_status` 字段**（背景举例 vs Reality：字段缺失/分散）。
