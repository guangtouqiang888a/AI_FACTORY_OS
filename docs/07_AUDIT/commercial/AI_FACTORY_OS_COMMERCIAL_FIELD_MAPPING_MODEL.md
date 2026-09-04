# AI_FACTORY_OS Commercial Field Mapping Model v1

> Entry 039-C | Object → Standard Fields  
> **状态：Blueprint Completed — Implementation Not Started**

---

## Experiment

| 标准字段 | 用途 | 历史字段映射 |
|----------|------|--------------|
| `lifecycle_status` | draft / approved / running / completed / evaluated / archived / rejected | ← `status` |
| `evaluation_status` | 评估过程（可选镜像 Eval 对象） | 无；或读 Evaluation SoT |
| （保留）`validation_goal` | 文本目标 | 保持；**不**映射 validation_status |
| （保留）`experiment_method` | creation method | — |

**不使用：** execution_status（生产在 PR）、release_status、validation_status（产品级）

---

## Production Request

| 标准字段 | 用途 | 历史字段映射 |
|----------|------|--------------|
| `lifecycle_status` | draft / approved / completed / failed / archived | ← `status` |
| `execution_status` | idle / queued / executing / succeeded / failed | **新增**；现无 |

**不使用：** validation_status、release_status、evaluation_status（属下游）

---

## Product Asset

| 标准字段 | 用途 | 历史字段映射 |
|----------|------|--------------|
| `lifecycle_status` | draft / validated / released / deprecated | **新增/推导** |
| `execution_status` | 生成执行 | ← `generation_status`（completed→succeeded） |
| `validation_status` | 验收 | ← `validation_status`（保持） |
| `release_status` | 发布 | **新增**；Commercial JSON 现缺失 |

**嵌套：** `artifact_information.quality_result.status` → 归 CF quality 域；不提升为 lifecycle

---

## Feedback

| 标准字段 | 用途 | 历史字段映射 |
|----------|------|--------------|
| `lifecycle_status` | pending / collecting / recorded / evaluated / archived | ← 部分 `feedback_status` |
| `collection_status` | not_started / collecting / recorded / closed | ← `observation_period`（string）规范化 |

**不使用：** evaluation_status（在 Evaluation 对象）、release_status

---

## Evaluation

| 标准字段 | 用途 | 历史字段映射 |
|----------|------|--------------|
| `lifecycle_status` | pending / running / completed / archived | 可与 evaluation_status 对齐或二选一主字段 |
| `evaluation_status` | pending / running / completed | ← 现有 `evaluation_status` |
| （结论）`hypothesis_result` | success / promising / failed / … | ← 现有；**隔离**于 status |

---

## Opportunity

| 标准字段 | 用途 | 历史字段映射 |
|----------|------|--------------|
| `lifecycle_status` | draft / ready / selected / rejected / archived | **新语义**；现 `status=human_assisted` → 迁至 `creation_method` |
| （保留）`creation_method` | human_assisted | ← 从错误 status 迁出 |

---

## Candidate

| 标准字段 | 用途 | 历史字段映射 |
|----------|------|--------------|
| `lifecycle_status` | discovered / evaluating / selected / converted / rejected / archived | ← `status` |
| （重命名建议） | 竞争描述 | `competition_status` → `competition_summary`（非状态维） |

---

## Approval / Exp Review / Selection

| 对象 | 主权威字段 | lifecycle_status |
|------|------------|------------------|
| Approval | `decision` | 可选镜像 approved/rejected |
| Exp Review | `decision`（与 review_status 合并择一） | 可选 |
| Selection | `decision` | 可选；`conversion_status` → 派生或独立 |

---

## Validation Object

| 标准字段 | 映射 |
|----------|------|
| `validation_status` | ← 现有（权威） |

---

## Mapping Diagram

```
Experiment.lifecycle_status  <── status
PR.lifecycle_status          <── status
PR.execution_status          <── (new) / Adapter runtime
ProductAsset.execution_status<── generation_status
ProductAsset.validation_status ← validation_status
ProductAsset.release_status  <── (new)
Feedback.lifecycle_status    <── feedback_status
Feedback.collection_status   <── observation_period
Evaluation.evaluation_status <── evaluation_status
Evaluation.hypothesis_result <── hypothesis_result (outcome)
Opportunity.creation_method  <── status(human_assisted)
Opportunity.lifecycle_status <── (new values)
```
