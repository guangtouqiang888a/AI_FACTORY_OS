# AI_FACTORY_OS Commercial State Migration Matrix

> Entry 039-D | Current → Target field/value mapping  
> **Design only — no writes**

**Refs：** Field Standard / Mapping (039-C) · Lifecycle SM (039-B) · Historical Snapshot

---

## Legend

| Confidence | Meaning |
|------------|---------|
| High | 机械映射，风险低 |
| Medium | 需核对关联对象 |
| Low | 商业语义需人工裁决 |

---

## Opportunity

| Object | Current Field | Current Value | Target Field | Target Value | Confidence | Human Review Required |
|--------|---------------|---------------|--------------|--------------|------------|------------------------|
| opp_* (all 5) | status | human_assisted | creation_method | human_assisted | High | No（搬迁） |
| opp_001/002/004/005 | status | human_assisted | lifecycle_status | selected | Medium | **Yes** — 已有 Experiment |
| opp_003 | status | human_assisted | lifecycle_status | ready 或 draft | Low | **Yes** — watch only |

---

## Candidate

| Object | Current Field | Current Value | Target Field | Target Value | Confidence | Human Review Required |
|--------|---------------|---------------|--------------|--------------|------------|------------------------|
| cand_001/002/004/005 | status | discovered | lifecycle_status | converted | Medium | Yes |
| cand_003 | status | discovered | lifecycle_status | discovered 或 evaluating | Medium | Yes（watch） |
| cand_* | competition_status | 叙述文本 | competition_summary | （原文本） | High | No |

---

## Experiment

| Object | Current Field | Current Value | Target Field | Target Value | Confidence | Human Review Required |
|--------|---------------|---------------|--------------|--------------|------------|------------------------|
| exp_001 | status | draft | lifecycle_status | approved | Medium | Yes（Review prepared + PR approved，未生产） |
| exp_002 | status | draft | lifecycle_status | rejected | High | Yes（确认归档） |
| exp_004 | status | draft | lifecycle_status | approved | Medium | Yes |
| exp_005 | status | draft | lifecycle_status | **running** 或 **completed** | Low | **Yes — Pilot 裁决**（见 Pilot Analysis） |

---

## Production Request

| Object | Current Field | Current Value | Target Field | Target Value | Confidence | Human Review Required |
|--------|---------------|---------------|--------------|--------------|------------|------------------------|
| preq_001 | status | draft | lifecycle_status | approved | High | Yes |
| preq_004 | status | draft | lifecycle_status | approved | High | Yes |
| preq_005 | status | draft | lifecycle_status | **completed** | High | Yes（确认） |
| preq_001/004 | — | — | execution_status | idle 或 queued | Medium | Yes（Pilot policy） |
| preq_005 | — | — | execution_status | **succeeded** | High | Yes |

---

## Approval

| Object | Current Field | Current Value | Target Field | Target Value | Confidence | Human Review Required |
|--------|---------------|---------------|--------------|--------------|------------|------------------------|
| appr_* | decision | approved | decision | approved | High | No（保持） |
| appr_* | — | — | lifecycle_status（可选镜像） | approved | High | No |

---

## Product Asset

| Object | Current Field | Current Value | Target Field | Target Value | Confidence | Human Review Required |
|--------|---------------|---------------|--------------|--------------|------------|------------------------|
| 8523329941d4 | generation_status | completed | execution_status | succeeded | High | No（字面映射）可双写 |
| 8523329941d4 | validation_status | passed | validation_status | passed | High | No |
| 8523329941d4 | — | — | lifecycle_status | validated | Medium | Yes |
| 8523329941d4 | — | — | release_status | unreleased | Medium | Yes（未上架观察） |

**禁止自动：** release_status=released；任何商业成功字段。

---

## Feedback / Evaluation

| Object | Current Field | Current Value | Target Field | Target Value | Confidence | Human Review Required |
|--------|---------------|---------------|--------------|--------------|------------|------------------------|
| fbk_001 | feedback_status | pending | lifecycle_status | pending | High | No |
| fbk_001 | observation_period | not_started | collection_status | not_started | High | No |
| eval_001 | evaluation_status | pending | evaluation_status | pending | High | No |
| eval_001 | hypothesis_result | pending | hypothesis_result | pending | High | No |

**禁止自动：** hypothesis_result→success/failed；metric 填数。

---

## Exp Review / Selection（summary）

| Object | Current | Target | Confidence | Human Review |
|--------|---------|--------|------------|--------------|
| erev prepared | decision=prepared | keep decision；Experiment sync | High | Yes for Exp write |
| erev rejected | decision=rejected | keep；Exp→rejected | High | Yes |
| selection selected/watch | decision | keep decision | High | No |

---

## Migration Waves (recommended order)

1. **Wave A — Additive fields only**（双写 execution_status / creation_method）  
2. **Wave B — Pilot value sync**（exp_005 / preq_005 / PA）Human Assisted  
3. **Wave C — Non-pilot PR/Exp approved**  
4. **Wave D — Opportunity/Candidate semantic split**  
5. **Never auto — commercial outcomes**
