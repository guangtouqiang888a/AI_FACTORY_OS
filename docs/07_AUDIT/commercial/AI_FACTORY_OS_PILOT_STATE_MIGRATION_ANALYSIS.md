# AI_FACTORY_OS Pilot State Migration Analysis

> Entry 039-D | Focus: exp_005 · preq_005 · Product Asset 8523329941d4  
> **禁止修改任何状态**

---

## Chain (Historical Reality)

```
exp_20260708_005 (status=draft, created 2026-07-08)
  → erev_20260709_005 (decision=prepared)
  → preq_20260712_005 (status=draft)
  → appr_20260713_005 (decision=approved)
  → CF execute (Entry 033-B1)
  → Product Asset 8523329941d4
       generation_status=completed
       validation_status=passed
  → fbk_20260713_001 pending / observation not_started
  → eval_20260713_001 pending
```

---

## Experiment

### 当前

| 项 | 值 |
|----|-----|
| ID | `exp_20260708_005` |
| Field | `status` |
| Value | **`draft`** |

### 目标生命周期

| 选项 | Target lifecycle_status | 何时选用 |
|------|-------------------------|----------|
| A（保守） | `running` | 生产完成但 **观察未开始** — 实验商业验证窗未关 |
| B（激进） | `completed` | 认为「生产验证」阶段已结束，仅待 Evaluation |
| C（过早） | `evaluated` | **不可选** — Evaluation 仍 pending |

**本策略推荐目标：`running`**

### 原因

1. Review=`prepared` + Approval=`approved` + Product Asset 已生成 → **已远超 draft**  
2. Feedback.observation_period=`not_started` → 市场观察 **未开始** → 不宜 `evaluated`  
3. Lifecycle SM：`approved → running → completed → evaluated`  
4. `completed` 易被误读为「实验整体完结/商业成功」——在无观察数据时应避免  
5. **Human Review Required：Yes** — 确认「running vs completed」语义

**中间态（可选 additive）：** 若先加字段不改值：保留 status=draft 并加 `lifecycle_status_proposed=running`（迁移 Entry 设计）；本 Entry 不实施。

---

## Production Request

### 当前

| 项 | 值 |
|----|-----|
| ID | `preq_20260712_005` |
| Field | `status` |
| Value | **`draft`** |

### 目标生命周期

| 字段 | 目标值 | 原因 |
|------|--------|------|
| `lifecycle_status` | **`completed`** | Product Asset generation completed + validation passed |
| `execution_status` | **`succeeded`** | 对应 generation_status=completed（Field Standard：不用 completed 字面） |

### 原因

1. Approval 已 approved；Adapter 已 `--execute` 成功  
2. SoT Product Asset 存在且可追溯  
3. `draft` 与事实冲突（CSC-004）  
4. 001/004 不同：仅 approved、未生产 → 目标 `lifecycle_status=approved`，`execution_status=idle|queued`

**Human Review Required：Yes**（确认 completed，非 released）

---

## Product Asset

### 当前状态字段

| Field | Value |
|-------|-------|
| `generation_status` | `completed` |
| `validation_status` | `passed` |
| `release_status` | **（字段不存在）** |
| `lifecycle_status` | **（字段不存在）** |
| `execution_status` | **（字段不存在）** |

### 目标字段

| Target Field | Target Value | Confidence | Notes |
|--------------|--------------|------------|-------|
| `execution_status` | `succeeded` | High | 映射 generation completed |
| `validation_status` | `passed` | High | 保持 |
| `lifecycle_status` | `validated` | Medium | 验收通过；非 commercial success |
| `release_status` | `unreleased` | Medium | 观察未开始=未上架释放 |

### 禁止目标

| 禁止自动写入 | 原因 |
|--------------|------|
| release_status=`released` | 无上架事实 |
| 任何 sales/revenue success | Human Assisted Boundary |
| 删除 generation_status（无双写期） | 兼容破坏 |

---

## Consistency After Proposed Pilot Migration（设计视图）

```
exp_005.lifecycle_status = running
preq_005.lifecycle_status = completed
preq_005.execution_status = succeeded
PA.execution_status = succeeded
PA.validation_status = passed
PA.lifecycle_status = validated
PA.release_status = unreleased
fbk/eval = pending（不变）
```

**仍不暗示：** 市场验证成功。

---

## 本 Entry 操作

- ✅ 分析完成  
- ❌ 未修改 exp_005 / preq_005 / 8523329941d4  
