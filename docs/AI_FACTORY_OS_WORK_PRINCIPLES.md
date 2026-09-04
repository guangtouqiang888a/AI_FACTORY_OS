# AI_FACTORY_OS 工作准则（现行对齐版）

> **文档角色：** 协作与工程方法准则（非最高治理裁决）  
> **Entry 066** · 对齐 DEC-011 / DEC-019 / DEC-029–032 / Execution Protocol  
> **Entry 067** · Acquisition Policy + AI Cost Gate  
> **Last updated:** 2026-09-03  
> **历史全文：** [`99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md`](./99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md)（**不得**作为现行最高规则）

**执行效力裁决（高 → 低）：**  
`PROJECT_CONSTITUTION` → `AUTHORITY_MODEL` → `EXECUTION_PROTOCOL` → `DECISION_LOG` → `KNOWLEDGE_UPDATE_PROTOCOL` → **本文件**

---

## 1. 角色分工

| 角色 | 职责 |
|------|------|
| **AI** | 总体架构、商业逻辑、技术路线、工程调度、自主日常商业流程设计 |
| **Cursor** | 工程执行器（施工队） |
| **User** | 目标、边界、反馈、**外部不可逆动作**确认、高风险边界控制 |

**User 不应**逐产品审批商业逻辑。  
**Human Gate** 主要位于：账号、外部发布、付款、广告及其他外部不可逆高风险动作。

系统默认**自主**运行日常流程：采集、分析、发现机会、选品、选择适合的 AI、生产、评分、风险审核、商业实验、学习——在 User 设定的 Policy 边界内。

---

## 2. 与早期准则的冲突处理（Superseded）

以下_ARCHIVE 条文**不再**按字面执行；以 DEC-011 / Scope-Controlled Entry 为准：

| 旧规则（Archive） | 现行语义 |
|-------------------|----------|
| 「一次性整体升级优于碎片化迭代」 | **整体架构一致** + **按 Entry 最小可验证 Scope 实施**；禁止为「整体升级」一次修改大量未知 Reality |
| 「禁止过度 V1/V2/V3 分阶段」 | 允许 **Scope-Controlled Entry**、Reality First、小范围验证；禁止无 Scope 的碎片化乱改 |
| 「自动化默认半自动+人工辅助」 | **系统默认自主运行**日常商业流程；人工负责**边界与外部不可逆动作**，≠ 每产品商业审批 |
| 「用户=执行者+决策确认」 | User 确认**Policy / 边界 / 外部动作**；不是每条 MarketObservation 的商业审批 |

**保留不变：** 风控优先；禁止高风险绕过平台；Reality First；Existing/Missing/Target 区分。

---

## 3. docs/0–6 核心文档域

`docs/00_GOVERNANCE/` … `docs/06_HISTORY/` = **现行核心文档域**（Governance / Current State / Architecture / Business / Execution / History）。

早期 **8+1** = 历史治理阶段产生的核心集合；**不得**简单理解成「8+1 永久高于后续 0–6」。

**解释权：** 以最新有效 Governance、Reality、Current State、Decision 为准。  
**导航入口：** [`AI_FACTORY_OS_DOCUMENTATION_MAP.md`](./AI_FACTORY_OS_DOCUMENTATION_MAP.md)

---

## 4. Core Documentation Creation Principle（Entry 066）

1. **docs/0–6 原则上不轻易增加文件。**
2. **优先**由现有核心文件承载新知识。
3. **仅当**现有核心文件无合理承载位置，且新内容形成**独立、长期、稳定**知识域，才允许新增。
4. 一旦在 docs/0–6 新增 → 即视为 **Core Documentation**。
5. 新增后必须：
   - 向 User **明确报告**
   - 说明为何已有文件无法承载
   - 说明长期职责
   - 纳入 Documentation Map / Control Center / Recovery（仅在实际需要处）
   - 纳入后续 Continuity Check
6. **禁止：**「顺手创建」「为了方便说明」「先单独放着」而未声明 Core 身份。

### Entry 收尾：Core File Changes 格式

```
Core File Changes
新增：0 / <列表>
删除：0 / <列表>
重命名：0 / <列表>

（若新增）
File: docs/0X_xxx/xxx.md
为什么必须新增：...
为什么已有文件无法承载：...
新文件长期职责：...
需要同步：...
```

**Audit（`07_AUDIT/`）** 放详细证据；**不**因存在 Audit 文件而成为 0–6 Core。

---

## 5. Browser-Native Acquisition Pattern

遇到新平台 / 新数据采集问题时，**不预设单一路线**。主动评估：

| 候选 | 说明 |
|------|------|
| A. Official API | 合规官方接口 |
| B. Normal rendered web page | 正常渲染页面 |
| C. Browser Extension / Content Script | 可见浏览器 + DOM |
| D. Normal client | 正常客户端 |
| E. User export | 用户导出 |
| F. Other verified source | 其他已验证来源 |

流程：**小成本验证 → 淘汰失败路线 → 收敛最合理路线**

- 用户提供的插件 / 工具 = **Reality Evidence / Prototype Evidence** ≠ 唯一思路来源
- **没有**现成插件时，仍必须主动思考 Browser-Native Acquisition 及其他候选
- **没有**现成成功案例时，必须通过候选方案 + 小实验寻找路径

---

## 6. Acquisition / Filter / Signal / Opportunity 分层

| 层 | 职责 |
|----|------|
| **Collector** | 记录事实 |
| **Filter** | 筛选（optional min_want_count、price range 等） |
| **Signal** | 分析 |
| **Opportunity** | 判断机会 |
| **Product Factory** | 自主生产 |

**禁止：** Collector 因 `want_count` 缺失直接删除商品。

### Want Count

- 重要市场信号；**不是** Collector 硬门槛
- 允许 `want_count=value` 或 `want_count=NULL`；**NULL ≠ 0**
- 无值 → 降低证据权重 / 使用其他信号（Filter / Signal 层）

### AcquisitionTask 最小模型

`source` + `query/scope` + `max_records` + `schedule` + `filters`（min_want_count, min_price, max_price — 均可空）

Goal 通过 **AcquisitionPolicy**（`policy_id`）绑定；Policy = 目标，Source = 平台，二者分离。

---

## 6.1 AI Cost 原则（Entry 067）

- **AI调用次数不是商业成本核心指标**；核心是 **estimated_cost / actual_cost / allowed_cost**。
- AI成本必须可估算、可约束；预算外 → BLOCKED / REDESIGN_REQUIRED。
- 简单任务优先低成本实现；高成本能力只在价值允许时使用。
- Unknown cost / revenue ≠ 0；估算收入不得当真实收入（ESTIMATE vs ACTUAL）。
- Model Router / 自动选模型：**未实现**；仅保留 ModelSelector 接口。

---

## 7. Source / Sales / Product

- **source_platform ≠ sales_platform**（例：Xianyu discovery → own product → Taobao sales — 合法）
- 市场研究 / 同类产品 / 竞争产品分析：**ALLOWED**
- 未经授权直接搬运他人完整商品：**NOT DEFAULT PRODUCTION PATH**
- 最终产品：自主生产或确认合法使用条件

---

## 8. 工程协作（仍有效）

- Reality First：规划状态 ≠ 已执行状态
- Cursor 输出须可完整执行；User 不承担复杂局部改码
- 重大 Entry 后同步 Current State / Registry / Execution History（DEC-019）
- 平台风控优先；禁止 bypass login / CAPTCHA / anti-bot / hidden API abuse

---

## 9. 本文件位置说明

本文件位于 `docs/` 根目录（与 Documentation Map 同级），作为**现行协作准则**入口。  
冲突时以 `00_GOVERNANCE/` 内 Constitution / Protocol / Decision Log 为准。
