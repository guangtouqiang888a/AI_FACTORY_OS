# AI_FACTORY_OS State Migration Risk Report

> Entry 039-D | Risk Assessment  
> Focus: Pilot exp_005 / preq_005 / Product Asset 8523329941d4

---

## P0 — 不可接受（阻止盲目迁移）

### RISK-P0-001

| 项 | 内容 |
|----|------|
| **Risk** | 自动把 `hypothesis_result` 或商业成功写入 Pilot |
| **Objects** | eval_001, fbk_001, PA |
| **Impact** | 虚假市场验证；治理崩坏 |
| **Mitigation** | Permission Policy 禁止；仅 Human Assisted |

### RISK-P0-002

| 项 | 内容 |
|----|------|
| **Risk** | 迁移损坏或替换 Product Asset `8523329941d4` ID / 删除 JSON |
| **Impact** | Pilot 链断裂；artifacts 孤儿 |
| **Mitigation** | Rollback Plan；禁止改 ID；备份强制 |

### RISK-P0-003

| 项 | 内容 |
|----|------|
| **Risk** | 无 backup 执行 Wave B 回写 |
| **Impact** | 不可恢复 |
| **Mitigation** | Rollback preconditions gate |

---

## P1 — 高（需人工迁移 Entry）

### RISK-P1-001

| 项 | 内容 |
|----|------|
| **Risk** | exp_005 `draft`→错误选 `completed`/`evaluated` |
| **Impact** | 暗示观察/评估已完成 |
| **Mitigation** | Pilot Analysis 推荐 `running`；Human confirm |

### RISK-P1-002

| 项 | 内容 |
|----|------|
| **Risk** | preq_005 仍 draft，工具误设为 queued 再次触发生产 |
| **Impact** | 重复执行 / Pilot policy 混乱 |
| **Mitigation** | 目标 lifecycle=completed + execution=succeeded；保持 whitelist |

### RISK-P1-003

| 项 | 内容 |
|----|------|
| **Risk** | PA 写入 release_status=released（无上架） |
| **Impact** | 发布状态谎言 |
| **Mitigation** | 默认 unreleased |

### RISK-P1-004

| 项 | 内容 |
|----|------|
| **Risk** | Opportunity.status 直接改 selected 而不建 creation_method |
| **Impact** | 丢失 human_assisted 方法语义 |
| **Mitigation** | 先拆字段再设 lifecycle |

### RISK-P1-005

| 项 | 内容 |
|----|------|
| **Risk** | 只改 docs 声称「已迁移」但 JSON 未改 |
| **Impact** | Documentation ≠ Reality 再现 |
| **Mitigation** | State Authority；同步 Entry 清单 |

---

## P2 — 中低

### RISK-P2-001

| 项 | 内容 |
|----|------|
| **Risk** | generation_status 与 execution_status 双写短暂不一致 |
| **Mitigation** | 双写窗口 + 文档说明 |

### RISK-P2-002

| 项 | 内容 |
|----|------|
| **Risk** | Candidate ID 键名异常（opportunity_id 存 cand_*）导致脚本映射错误 |
| **Mitigation** | 按值匹配；先 inventory |

### RISK-P2-003

| 项 | 内容 |
|----|------|
| **Risk** | 001/004 approved 映射后被误 execute |
| **Mitigation** | Pilot whitelist 保持；execution_status≠queued 直至 Entry |

---

## Pilot-Focused Risk Summary

| Object | Top Risk | Recommended Stance |
|--------|----------|-------------------|
| exp_005 | 阶段标过满 | → running（人工） |
| preq_005 | 假 draft / 再执行 | → completed + succeeded（人工） |
| 8523329941d4 | ID/release 误伤 | 保留；additive fields only |

---

## Residual Risk After Strategy

迁移策略降低「字段不知如何迁」风险；**不消除**「人工选错 running vs completed」风险 — 须 Pilot Migration Entry 明确勾选。
