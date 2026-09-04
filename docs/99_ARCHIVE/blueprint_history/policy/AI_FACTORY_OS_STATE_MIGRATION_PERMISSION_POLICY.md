# AI_FACTORY_OS State Migration Permission Policy

> Entry 039-D | Automatic Migration Boundary  
> **Blueprint Completed — Enforcement Not Started**

---

## 1. 允许自动迁移（未来工具 / 脚本，仍须 Entry 授权启用）

| 类别 | 例 | 条件 |
|------|-----|------|
| **字段重命名（同义）** | validation_status 保持 | 值集合不变 |
| **方法字段搬迁** | Opportunity.status(human_assisted) → creation_method | 值字面复制 |
| **执行枚举映射** | generation_status completed → execution_status succeeded | 固定对照表 |
| **结构整形** | observation_period string → object.status | 可逆 |
| **双写 additive** | 新增 execution_status，保留旧字段 | 不删旧键 |
| **decision 去重** | review_status 复制自 decision 后标记 deprecated | 不改 decision 值 |

**自动迁移仍必须：** backup + audit log + dry-run report。

---

## 2. 禁止自动迁移

| 禁止 | 例 |
|------|-----|
| 市场成功 / 商业成功 | commercial_success=true |
| 收入 / 订单 / GMV actual | metric_value ← 估算 |
| 用户满意度结论 | 无来源问卷 |
| 实验成功判定 | hypothesis_result ← success |
| 观察完成 | collection_status=recorded（无数据） |
| 上架释放 | release_status=released（无上架） |
| 删除 Product Asset / 改 Pilot ID | — |
| 静默覆盖 conflict 对象为「看起来合理」的值 | exp_005 draft→completed 无人工确认 |

---

## 3. 必须 Human Assisted

| 变更 | 原因 |
|------|------|
| Experiment lifecycle draft→running/completed | 商业阶段语义 |
| PR lifecycle → completed | 确认生产闭合 |
| PA lifecycle_status / release_status | 发布决策 |
| Candidate converted / Opportunity selected | 链一致性裁决 |
| exp_002 → rejected | 终态确认 |
| **一切 commercial outcome** | Human Assisted Boundary Protocol |
| Feedback collecting 开始 | Observation Start Entry |
| Evaluation completed + hypothesis_result | 人工评估 |

---

## 4. Actor Permissions（迁移场景）

| Actor | Auto map | Human confirm values | Commercial outcome |
|-------|----------|----------------------|--------------------|
| Migration tool | ✅ 允许类 | ❌ | ❌ |
| Human Assisted Entry | ✅ 可触发 | ✅ | ✅ |
| Content Factory | ❌ | ❌ | ❌ |
| Validation Gate | ❌（除 validation 计算登记授权） | — | ❌ |

---

## 5. Default Stance

```
IF change affects commercial meaning of Pilot chain
  THEN Human Assisted ONLY
ELSE IF mechanical field rename / enum synonym
  THEN Auto allowed AFTER Entry enable + backup
ELSE
  DENY
```
