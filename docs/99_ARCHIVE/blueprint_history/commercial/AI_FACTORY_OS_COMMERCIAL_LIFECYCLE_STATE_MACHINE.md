# AI_FACTORY_OS Commercial Lifecycle State Machine v1

> Entry 039-B | Target Lifecycle Design  
> **状态：Blueprint Completed — Implementation Not Started**  
> **非：** 当前 JSON 字段已经符合本机（见 Conflict Report）

**原则：** Historical Reality ≠ Target Lifecycle Design · 状态转换须 Entry/人工授权（Human Assisted Boundary）

---

## 1. 总链（目标）

```
Candidate → Opportunity → Selection
  → Experiment → (Exp Review)
  → Production Request → Approval
  → executing(CF) → Validation → Product Asset
  → Feedback → Evaluation → archived
```

---

## 2. Opportunity Candidate

### 合法状态

| 状态 | 含义 |
|------|------|
| `discovered` | 已登记候选 |
| `evaluating` | 评估中 |
| `selected` | 进入 Selection/Opportunity |
| `rejected` | 否决 |
| `converted` | 已转为 Opportunity |
| `archived` | 归档 |

### 允许转换

```
discovered → evaluating → selected → converted
discovered → evaluating → rejected → archived
selected → rejected（例外撤回）
* → archived
```

---

## 3. Opportunity

### 合法状态（lifecycle — 目标）

| 状态 | 含义 |
|------|------|
| `draft` | 机会对象已建 |
| `ready` | 可进入 Selection |
| `selected` | 已选入实验 |
| `rejected` | 否决 |
| `archived` | 归档 |

> **Target 澄清：** 现行字段值 `human_assisted` 属 **creation_method**，目标应拆为：  
> `creation_method` + `lifecycle_status`（见 Conflict CSC-001）。

### 允许转换

```
draft → ready → selected
ready → rejected → archived
selected → archived
```

---

## 4. Experiment

### 合法状态（本 Entry 规范）

| 状态 | 含义 |
|------|------|
| `draft` | 实验设计登记 |
| `approved` | Prepared Review 通过 / 批准开跑 |
| `running` | 观察或生产验证进行中 |
| `completed` | 生产+观察窗结束（可评） |
| `evaluated` | Evaluation 已出结论 |
| `archived` | 归档 |
| `rejected` | Review 拒绝（终态之一） |

### 允许转换

```
draft → approved
approved → running
running → completed
completed → evaluated
evaluated → archived

draft → rejected → archived
```

**禁止：** `draft → completed` 跳过；`evaluated` 无 Feedback/Evaluation 对象支撑时禁止写入。

**与 Exp Review 关系：** Review.`decision=prepared` **建议触发** Experiment.`draft→approved`（同步 Entry，非自动）。

---

## 5. Production Request

### 合法状态

| 状态 | 含义 |
|------|------|
| `draft` | 规格已登记 |
| `approved` | Approval decision=approved 已同步 |
| `queued` | 进入可执行队列（含 Pilot 策略） |
| `executing` | CF Adapter/`--execute` 进行中 |
| `completed` | Product Asset generation completed |
| `failed` | 生产/验收失败 |
| `archived` | 归档 |

### 允许转换

```
draft → approved → queued → executing → completed
executing → failed
failed → queued（重试，须人工）
completed → archived
draft → archived（废弃）
```

**禁止：** 无 Approval 时 `draft→queued`；无 Validation/Asset 时宣称 `completed`。

---

## 6. Approval

### 合法状态（decision）

| 状态 | 含义 |
|------|------|
| `pending` | 待审 |
| `approved` | 批准生产 |
| `rejected` | 拒绝 |
| `superseded` | 被新审批替代 |

Approval 为 **独立实体**；其 `approved` **不自动改写** PR.status（须同步规则或人工 Entry）。

---

## 7. Product Asset

### 合法状态（建议统一为 `asset_status`；现行为双字段）

| 目标状态 | 含义 | 现行近似 |
|----------|------|----------|
| `draft` | 草稿/draft mapper 输出 | generation_status 未 completed |
| `validated` | Validation passed | validation_status=passed |
| `released` | 允许上架观察 | （尚无字段） |
| `deprecated` | 停用 | （尚无） |

**过渡双字段映射（设计）：**

| generation_status | validation_status | 建议 asset_status |
|-------------------|-------------------|-------------------|
| completed | passed | validated（或 released if listed） |
| completed | failed | draft / failed |
| adapter_ready / dry_run | — | draft |

### 允许转换

```
draft → validated → released → deprecated
validated → deprecated
```

---

## 8. Validation

### 合法状态

| 状态 | 含义 |
|------|------|
| `pending` | 待验 |
| `passed` | 通过 |
| `failed` | 失败 |
| `waived` | 人工豁免（须记录） |

---

## 9. Feedback

### 合法状态

| 状态 | 含义 |
|------|------|
| `pending` | 占位实例，观察未开始 |
| `collecting` | 观察窗内采集中 |
| `recorded` | 指标已录入（真实观测） |
| `evaluated` | 已支撑 Evaluation |
| `archived` | 归档 |

### 允许转换

```
pending → collecting → recorded → evaluated → archived
```

**禁止：** 自动生成销量/收入/转化成功（见 Human Assisted Boundary）。

---

## 10. Evaluation

### 合法状态

| 状态 | 含义 |
|------|------|
| `pending` | 等待观察数据 |
| `running` | 评估进行中 |
| `completed` | hypothesis_result 已判定（success/promising/failed 等） |
| `archived` | 归档 |

### 允许转换

```
pending → running → completed → archived
```

**门禁：** `completed` 要求 Feedback 至少 `recorded`（或显式 human waiver）。

---

## 11. 跨对象一致性规则（目标）

| 若 | 则（目标一致性） |
|----|------------------|
| Approval=approved | PR.status ≥ approved |
| Product Asset generation=completed | PR.status=completed；Experiment ≥ running/completed |
| Validation=passed | Product Asset ≥ validated |
| Feedback=collecting | Experiment=running |
| Evaluation=completed | Experiment=evaluated |

**本 Entry 不执行同步。**

---

## 12. 状态声明

| 项 | 状态 |
|----|------|
| Lifecycle State Machine v1 | ✅ Blueprint Completed |
| JSON 字段迁移 / 回写 | ❌ Not Started |
| Runtime 自动状态机 | ❌ Not Started |
