# AI_FACTORY_OS Commercial Field Compatibility Report

> Entry 039-C | Historical ↔ Future Field Compatibility  
> **禁止修改 / 禁止自动迁移**

---

## Current Field: `status`（Experiment / PR / Candidate）

| 项 | 内容 |
|----|------|
| **Future Standard** | `lifecycle_status` |
| **Compatibility** | 名称变更；值集合扩展（approved/running/completed…） |
| **Migration Risk** | **High** — 现多 draft；扩展值需人工 Lifecycle Sync（039-B CSC） |

---

## Current Field: `status`（Opportunity = human_assisted）

| 项 | 内容 |
|----|------|
| **Future Standard** | `creation_method` + 新 `lifecycle_status` |
| **Compatibility** | **Breaking semantic** — 不能直接 rename |
| **Migration Risk** | **High** — 须拆分字段，禁止把 human_assisted 当作 lifecycle 枚举 |

---

## Current Field: `generation_status`

| 项 | 内容 |
|----|------|
| **Future Standard** | `execution_status`（completed → succeeded） |
| **Compatibility** | 可双写过渡 |
| **Migration Risk** | Medium — Adapter/文档引用 generation_status |

---

## Current Field: `validation_status`（Product Asset / Validation）

| 项 | 内容 |
|----|------|
| **Future Standard** | `validation_status`（保持） |
| **Compatibility** | ✅ High |
| **Migration Risk** | Low |

---

## Current Field: `release_status`

| 项 | 内容 |
|----|------|
| **Current Reality** | Commercial Product Asset JSON **缺失**；CF pipeline 可能有独立 release_gate 输出 |
| **Future Standard** | Product Asset.`release_status` |
| **Compatibility** | Additive |
| **Migration Risk** | Low–Medium — 需避免与 CF 内存字段冲突 |

---

## Current Field: `feedback_status`

| 项 | 内容 |
|----|------|
| **Future Standard** | `lifecycle_status` + `collection_status` |
| **Compatibility** | pending 可保留在 lifecycle；observation_period 迁 collection |
| **Migration Risk** | Medium — 一字段拆两字段 |

---

## Current Field: `evaluation_status`

| 项 | 内容 |
|----|------|
| **Future Standard** | `evaluation_status`（保持）或对齐 `lifecycle_status` |
| **Compatibility** | ✅ High |
| **Migration Risk** | Low — 与 `hypothesis_result` 双 pending 需文档澄清 |

---

## Current Field: `hypothesis_result`

| 项 | 内容 |
|----|------|
| **Future Standard** | 保持为 **outcome** 字段（非 status 维） |
| **Compatibility** | ✅ |
| **Migration Risk** | Low — 禁止把 success 写入 evaluation_status 替代结论 |

---

## Current Field: `decision`（Approval / Review / Selection）

| 项 | 内容 |
|----|------|
| **Future Standard** | 保留 decision 维 |
| **Compatibility** | ✅ |
| **Migration Risk** | Low — 同步 lifecycle 仍须人工 |

---

## Current Field: `competition_status`（Candidate）

| 项 | 内容 |
|----|------|
| **Future Standard** | `competition_summary`（非状态维） |
| **Compatibility** | Rename |
| **Migration Risk** | Low |

---

## Current Field: `review_status` + `decision`（Exp Review）

| 项 | 内容 |
|----|------|
| **Future Standard** | 单权威 `decision`；废弃重复 review_status |
| **Compatibility** | Dedup |
| **Migration Risk** | Low |

---

## Current Field: `observation_period`（Feedback string vs Evaluation object）

| 项 | 内容 |
|----|------|
| **Future Standard** | 统一 object 或统一 `collection_status` |
| **Compatibility** | Structure diverge |
| **Migration Risk** | Medium |

---

## Collision: word `completed`

| Context | Risk |
|---------|------|
| generation_status=completed | 执行成功 |
| lifecycle completed（目标） | 阶段结束 |
| evaluation_status=completed | 评估结束 |

**Mitigation：** 标准禁用 execution 使用 `completed` 字面量。

---

## Summary Risk Table

| Current | Future | Risk |
|---------|--------|------|
| Opportunity.status | creation_method + lifecycle_status | High |
| Experiment/PR.status | lifecycle_status + value sync | High |
| generation_status | execution_status | Medium |
| feedback_status | lifecycle + collection | Medium |
| validation_status | same | Low |
| evaluation_status | same | Low |
| release_status (missing) | additive | Low–Med |

**本 Entry：** 仅兼容性分析；**Implementation Not Started**
