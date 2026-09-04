# AI_FACTORY_OS Commercial State Conflict Report

> Entry 039-B | Historical Reality vs Target Lifecycle  
> 审计日期：2026-07-14  
> **禁止自动修改 JSON**

**对照：** Inventory（现状）× Lifecycle State Machine（目标）

---

## Conflict ID: CSC-001

| 项 | 内容 |
|----|------|
| **Object** | Opportunity |
| **Current State** | `status=human_assisted`（5/5） |
| **Expected Lifecycle** | `lifecycle_status` ∈ {draft, ready, selected, rejected, archived}；creation_method 独立 |
| **Risk** | 无法表达「已进入实验」；与 Experiment/Selection 进度脱节 |
| **Recommendation** | 未来 Entry：拆分字段或映射表；勿在未设计时强改现值为 selected |

---

## Conflict ID: CSC-002

| 项 | 内容 |
|----|------|
| **Object** | Experiment |
| **Current State** | `status=draft`（4/4），含 exp_005（已有 Product Asset completed） |
| **Expected Lifecycle** | Pilot 完成应 ≥ `running` 或 `completed`；Review prepared 应对应 `approved` |
| **Risk** | ZIP/审计误判「实验未开始」；与 PROJECT_STATUS「Pilot Completed」文档投影冲突 |
| **Recommendation** | 授权 Lifecycle Sync Entry：draft→approved→running/completed（人工确认语义） |

---

## Conflict ID: CSC-003

| 项 | 内容 |
|----|------|
| **Object** | Experiment + Experiment Review |
| **Current State** | Review decision=`prepared`（3）/`rejected`（1）；Experiment 仍全部 `draft` |
| **Expected Lifecycle** | prepared → Experiment `approved`；rejected → Experiment `rejected` |
| **Risk** | Review 与 Experiment 双轨字段不同步 |
| **Recommendation** | 定义「Review 写 decision，Experiment 回写 status」的同步 SOP |

---

## Conflict ID: CSC-004

| 项 | 内容 |
|----|------|
| **Object** | Production Request |
| **Current State** | 3 条 `status=draft`；对应 Approval 全 `approved`；preq_005 已产出 Asset |
| **Expected Lifecycle** | approved 后 PR=`approved`/`queued`；生产完成=`completed` |
| **Risk** | Adapter 依赖 ApprovalGate 而非 PR.status；文档与字段双重真相 |
| **Recommendation** | Sync Entry：001/004→approved；005→completed |

---

## Conflict ID: CSC-005

| 项 | 内容 |
|----|------|
| **Object** | Approval vs Pilot Policy |
| **Current State** | 3 approved；代码 whitelist 仅 `preq_20260712_005` |
| **Expected Lifecycle** | `approved` + `queued` 才可执行；策略应文档化而非 silently block |
| **Risk** | 「已批准却不可生产」语义冲突 |
| **Recommendation** | Authority 文档标明 Policy Gate ≠ Approval State；扩展 whitelist 须 Entry |

---

## Conflict ID: CSC-006

| 项 | 内容 |
|----|------|
| **Object** | Product Asset |
| **Current State** | 双字段：generation_status=`completed` + validation_status=`passed` |
| **Expected Lifecycle** | 统一 `asset_status`：validated / released |
| **Risk** | 状态机难落地；下游 Feedback 不知读哪个字段 |
| **Recommendation** | 过渡期：双字段为权威；新增 asset_status 为 additive（非本 Entry） |

---

## Conflict ID: CSC-007

| 项 | 内容 |
|----|------|
| **Object** | Feedback |
| **Current State** | feedback_status=`pending`；observation_period=`not_started` |
| **Expected Lifecycle** | pending 合法；下一步 `collecting` 需 Observation Start |
| **Risk** | 低 — 与目标一致（占位） |
| **Recommendation** | 保持；禁止填假 metric（Human Assisted） |

---

## Conflict ID: CSC-008

| 项 | 内容 |
|----|------|
| **Object** | Evaluation |
| **Current State** | hypothesis_result=`pending`；observation not_started |
| **Expected Lifecycle** | pending 合法；completed 须 Feedback recorded |
| **Risk** | 低 — 一致 |
| **Recommendation** | 保持 |

---

## Conflict ID: CSC-009

| 项 | 内容 |
|----|------|
| **Object** | Candidate |
| **Current State** | 全部 `discovered`；其中 4 个已 converted 到 Opportunity/Experiment |
| **Expected Lifecycle** | converted / selected |
| **Risk** | 候选池状态滞后 |
| **Recommendation** | Sync Entry 更新 converted（可选优先级低于 Experiment/PR） |

---

## Conflict ID: CSC-010

| 项 | 内容 |
|----|------|
| **Object** | Experiment exp_002 |
| **Current State** | status=`draft`；Review=`rejected`；无 PR |
| **Expected Lifecycle** | `rejected` → archived |
| **Risk** | 仍显示 draft 可能被误入生产 |
| **Recommendation** | Sync：draft→rejected |

---

## Summary

| 级别 | Conflict IDs | 数量 |
|------|--------------|------|
| **阻断一致性（P1）** | CSC-002, CSC-003, CSC-004, CSC-005, CSC-010 | 5 |
| **语义/模型（P2）** | CSC-001, CSC-006, CSC-009 | 3 |
| **符合目标（无冲突或可接受）** | CSC-007, CSC-008 | 2（记录用） |
| **状态冲突需处置（P1+P2）** | CSC-001~006, 009, 010 | **8** |

> **报告「状态冲突数量」口径：** 8 个需处置冲突（不含 007/008 可接受 pending）。

---

## 本 Entry 操作

- ✅ 冲突分析  
- ❌ 未修改 commercial_assets  
