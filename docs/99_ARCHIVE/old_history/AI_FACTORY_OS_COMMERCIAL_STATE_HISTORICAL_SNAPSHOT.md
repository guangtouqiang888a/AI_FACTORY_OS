# AI_FACTORY_OS Commercial State Historical Snapshot

> Entry 039-D — Commercial State Migration Strategy v1  
> Snapshot Date: **2026-07-14**  
> **用途：** 迁移前历史事实冻结（只读）  
> **禁止：** 本 Entry 未修改任何 JSON

**Store：** `commercial_assets/` exclusively  

---

## Snapshot Scope

Opportunity · Candidate · Experiment · Production Request · Approval · Product Asset · Feedback · Evaluation  
(+ Selection / Exp Review / Validation as related)

**Note:** `updated_at` 多数为 null — last_update 以 `created_at` / `approved_at` / 文件写入时间为准。

---

## Candidate

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| cand_20260708_001 | status | discovered | → opp_001 | 2026-07-08T08:44:00+08:00 | （无 updated_at） |
| cand_20260708_002 | status | discovered | → opp_002 | 2026-07-08T08:44:00+08:00 | — |
| cand_20260708_003 | status | discovered | → opp_003 (watch) | 2026-07-08T08:44:00+08:00 | — |
| cand_20260708_004 | status | discovered | → opp_004 | 2026-07-08T08:44:00+08:00 | — |
| cand_20260708_005 | status | discovered | → opp_005 → … → PA | 2026-07-08T08:44:00+08:00 | — |

**Schema note：** 文件内 ID 键名曾出现 `opportunity_id` 承载 cand_* 值 — 迁移时须以值为准。

---

## Opportunity

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| opp_20260708_001 | status | human_assisted | cand_001 → sel_001 → exp_001 | 2026-07-08T10:35:00+08:00 | — |
| opp_20260708_002 | status | human_assisted | cand_002 → exp_002 (rejected review) | 2026-07-08T10:35:00+08:00 | — |
| opp_20260708_003 | status | human_assisted | cand_003 → sel watch | 2026-07-08T10:35:00+08:00 | — |
| opp_20260708_004 | status | human_assisted | → exp_004 → preq_004 | 2026-07-08T10:35:00+08:00 | — |
| opp_20260708_005 | status | human_assisted | → exp_005 → preq_005 → 8523329941d4 | 2026-07-08T10:35:00+08:00 | — |

---

## Experiment

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| exp_20260708_001 | status | draft | opp_001, erev_001=prepared, preq_001, appr_001 | 2026-07-08T14:51:00+08:00 | — |
| exp_20260708_002 | status | draft | opp_002, erev_002=**rejected**, 无 PR | 2026-07-08T14:51:00+08:00 | — |
| exp_20260708_004 | status | draft | opp_004, erev_004=prepared, preq_004, appr_004 | 2026-07-08T14:51:00+08:00 | — |
| exp_20260708_005 | status | draft | opp_005, erev_005=prepared, preq_005, appr_005, **PA 8523329941d4**, fbk, eval | 2026-07-08T14:51:00+08:00 | — |

---

## Production Request

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| preq_20260712_001 | status | draft | exp_001, appr_001=approved | 2026-07-12T17:03:00+08:00 | — |
| preq_20260712_004 | status | draft | exp_004, appr_004=approved | 2026-07-12T17:03:00+08:00 | — |
| preq_20260712_005 | status | draft | exp_005, appr_005=approved, **PA completed** | 2026-07-12T17:03:00+08:00 | — |

---

## Approval

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| appr_20260713_001 | decision | approved | preq_001 | 2026-07-13T17:43:00+08:00 | approved_at same |
| appr_20260713_004 | decision | approved | preq_004 | 2026-07-13T17:43:00+08:00 | same |
| appr_20260713_005 | decision | approved | preq_005 → PA | 2026-07-13T17:43:00+08:00 | same |

---

## Product Asset

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| 8523329941d4 | generation_status | completed | preq_005, exp_005, appr_005 | 2026-07-13T18:37:11+08:00 | 2026-07-13T18:37:11+08:00 |
| 8523329941d4 | validation_status | passed | pval_20260713_ac223d | （同上） | （同上） |

**release_status：** 字段不存在于 SoT。

---

## Feedback

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| fbk_20260713_001 | feedback_status | pending | PA 8523329941d4 | 2026-07-13T18:54:00+08:00 | same |
| fbk_20260713_001 | observation_period | not_started | — | — | — |

---

## Evaluation

| object_id | current_status_field | current_value | related_objects | creation_time | last_update |
|-----------|---------------------|---------------|-----------------|---------------|-------------|
| eval_20260713_001 | evaluation_status | pending | fbk_001, exp_005（链） | 2026-07-13T18:54:00+08:00 | same |
| eval_20260713_001 | hypothesis_result | pending | — | — | — |

---

## Related (compact)

| Object | IDs / states |
|--------|----------------|
| Exp Review | erev_001/004/005 prepared；erev_002 rejected（2026-07-09） |
| Validation | pval_20260713_ac223d validation_status=passed |
| Selection | sel_001/002/004/005 selected；sel_003 watch |

---

## Pilot Chain Freeze (critical)

```
cand_005 → opp_005 → sel_005 → exp_005(status=draft)
  → erev_005(prepared) → preq_005(status=draft) → appr_005(approved)
  → PA 8523329941d4(generation=completed, validation=passed)
  → fbk_001(pending) → eval_001(pending)
```

**Snapshot hash intent：** 任何未来迁移 Entry 必须以本表为 before-image。
