# AI_FACTORY_OS Human Assisted Boundary Protocol v1

> Entry 039-B | 人机边界  
> **状态：Blueprint Completed**

**原则：** Human Assisted ≠ Automation · 禁止虚假市场数据 · Feedback Created ≠ Market Validation

---

## 1. 必须人工确认的状态 / 数据

### 商业结论类（禁止自动写入为「成功」）

| 禁止自动断言 | 说明 |
|--------------|------|
| 销售成功 / 商业成功 | 订单、成交、Revenue 须人工观测录入 |
| 用户反馈满意度结论 | 须真实来源 |
| 收入 / GMV / 利润实际值 | 禁止估算冒充 actual |
| 市场验证成功 | Evaluation completed=success 须人工签字式 Entry |
| 转化率「已验证」 | 须 observation 数据支撑 |

### Lifecycle 推进类（须 Human Assisted Entry）

| 转换 | 原因 |
|------|------|
| Experiment draft→approved / rejected | Review 决策 |
| Experiment →running / completed / evaluated | 观察与评估判断 |
| PR draft→approved / completed | 与 Approval / Asset 对齐 |
| Product Asset →released | 上架决策 |
| Feedback pending→collecting→recorded | 观测录入 |
| Evaluation pending→completed | 假设判定 |

### 生产放行类

| 动作 | 边界 |
|------|------|
| Adapter `--execute` | 默认 dry_run；execute 须授权 |
| Pilot whitelist 扩展 | 须 Entry |
| 自动 approve PR | **禁止** — Approval 仅人工 |

---

## 2. 允许自动化（或半自动）的范围

| 允许 | 条件 |
|------|------|
| CF artifact 生成（已批准 PR + gate） | 不自动写「市场成功」 |
| QualityAgent 生产域评分 | ≠ 市场验证 |
| ProductAssetValidator check | 结果登记仍建议 Entry 或显式授权写 JSON |
| OS Data/Score/Decide（SQLite listing） | 与 Commercial 链隔离 |
| dry_run Adapter | 默认 |

---

## 3. Feedback / Evaluation 硬边界

```
禁止：
  metric_value ← 模型臆造销量
  hypothesis_result ← success（无 observation）

允许：
  feedback_status = pending
  metric_value = null
  hypothesis_result = pending
  observation_period = not_started
```

**Observation Protocol（036-A）** 启动观察后：仅人工录入 views/clicks/orders 等。

---

## 4. 文档 vs 人工边界

| docs 可写 | docs 不可单独声称 |
|-----------|-------------------|
| Entry Completed（治理） | 「市场验证通过」而无 Feedback recorded |
| Blueprint Completed | 「Production Ready」混淆 Runtime |
| Pilot Production Completed | 「Commercial Success」 |

---

## 5. 违规响应（设计）

1. 拒绝写入假 actuals  
2. 记录 Known Issue / Conflict  
3. 回滚或标注 invalid（须 Entry）  

---

## 6. 状态声明

| 项 | 状态 |
|----|------|
| Human Assisted Boundary Protocol | ✅ Blueprint Completed |
| Runtime 强制校验器 | ❌ Not Started |
