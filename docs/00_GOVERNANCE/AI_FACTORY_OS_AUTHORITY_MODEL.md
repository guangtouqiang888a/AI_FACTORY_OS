# AI_FACTORY_OS Authority Model

> Collaboration Control — truth hierarchy（权威模型）  
> Last updated: 2026-09-04（**Core Documentation Continuity Hardening**；权威层级未改）

Aligned with System Governance / State Authority Protocol; this file is the **session-facing** control summary（会话侧权威摘要）。

**Document Role（041-F）：** 权威层级裁决。**不是** Current State 事实清单；**不是**商业战略正文；**不是**历史演进主文。  
信息类型归属见 Constitution **Information Ownership Principle**（DEC-016）；本文件定义**谁优先**，不重复定义各域业务内容。

---

## 文档和现实权威层级（Documentation & Reality Authority Levels）

数字越小，权威越高。**如果高层和低层冲突：优先相信高层。**

| Level | 名称 | 包含 | 中文说明 |
|-------|------|------|----------|
| **L0** | 用户最终决策权（User Final Authority） | 用户在本任务中的明确授权、否决与范围裁定 | 高于一切文档解释；**仍不能口头伪造 Reality**（例如磁盘未改却宣称迁移完成） |
| **L1** | Reality（现实） | **代码真实状态** · **数据库真实状态** · **资产真实状态**（commercial_assets 等）· **Runtime 真实状态**（被调用时实际跑什么） | 文档与现实冲突时 → **改文档**，不静默改现实（除非用户授权 Entry） |
| **L2** | Authority Model + Current State | 本文件 · `CURRENT_STATE` | 裁决规则 + 当前事实投影；State 落后于 Reality 时先恢复 State |
| **L3** | Core Governance（核心治理） | Constitution · Business Strategy · Decision Log | 使命、商业方向、正式裁决；慢变、战略级 |
| **L4** | Architecture / Execution / Update | Unified Architecture · Execution Protocol · Knowledge Update Protocol | 目标架构、如何执行、变化如何同步 |
| **L5** | Historical Documents（历史文档） | 历史文件 · 审计报告 · 过程记录 · 旧 PLAN / 旧 WORK_PRINCIPLES 等 | **证据与详文**；不作为默认最高判断来源 |

### 特别说明（强制）

- **Blueprint ≠ Production（蓝图 ≠ 生产完成）**  
- **Design ≠ Runtime（设计 ≠ 运行时已实现）**  
- 聊天上下文 **低于** L5；不得只靠长对话改项目方向（见 DEC-012）

```
冲突时：
L0 > L1 > L2 > L3 > L4 > L5 > Conversation Memory
```

---

## Authority Order (highest → lowest) — Reality Detail

| Rank | Layer | Meaning |
|------|-------|---------|
| 1 | **Runtime Reality** | What actually runs when invoked |
| 2 | **Code Reality** | Python / config source as written |
| 3 | **Database Reality** | `data/ai_factory.db` contents & schema on disk |
| 4 | **Asset Reality** | `commercial_assets/`, CF artifacts on disk |
| 5 | **Current State** | `AI_FACTORY_OS_CURRENT_STATE.md` |
| 6 | **Decision Log** | Durable decisions |
| 7 | **Documentation** | Blueprints, PROJECT_STATUS, snapshots, contracts |
| 8 | **Conversation Memory** | Chat history / summaries |

上表 Rank 1–4 属于 **L1 Reality** 内部细节；Rank 5+ 对应 L2–L5 与聊天。

---

## Conflict Resolution

```
IF Conversation Memory ≠ Documentation
  → prefer Documentation, then verify Reality

IF Documentation ≠ Current State
  → prefer Current State if recently synced from Reality;
    else verify Reality and update Current State

IF Current State ≠ Code/DB/Assets
  → Reality wins; update Current State; log Decision if strategic

IF Decision Log ≠ new Evidence
  → supersede Decision with new ID; do not erase old entry

IF lower Level (e.g. L5 History) ≠ higher Level (e.g. L3 Decision)
  → 优先相信高层（higher Level）
```

---

## Domain SoT Reminders

| Domain | SoT |
|--------|-----|
| Behavior | Code |
| Operational market listings/scores | SQLite |
| Commercial objects | commercial_assets JSON |
| OS learning | 7_MEMORY |
| Session control | Control Center + Current State + Decision Log |

---

## Explicit Non-Authorities

- `PRODUCT_STATUS` alone does not prove Runtime Connected  
- “Blueprint Completed” does not mean Implementation  
- `product_memory.json` is not Commercial Product Asset SoT  
- Chat claims of “migration done” without Asset Reality changes are false  
- Long chat consensus without Core Governance 回溯 does not change project direction（DEC-012）
- Long-term collaboration rules that exist **only** in Conversation Memory are **not** project authority（DEC-019）；must enter `docs/0–6` Governance when lasting
- **Control Center state projections**（Phase / Goal / Focus / Active Risks）are **not** Reality SoT；conflict → Current State / Reality win
- **Audit reports** are evidence — **not** Current State substitutes
- **GitHub** Documentation / Commit / Audit are continuity / versioning infrastructure — **not** Runtime / Code / DB / Assets Reality Authority；sync ≠ Production / commercial success

### Human Gate vs User Authority（DEC-020 / DEC-023）

- **User Final Authority（L0）** 仍高于一切文档解释。  
- **Human Gate**（商业闭环中的人工闸门）专指：高风险/不可逆外部行为（账号、付款、广告、当前真实发布）的确认节点。  
- Human Gate **≠**「每个产品都必须人工商业审批」。  
- **DEC-023：** Human Gate = **External Action Gate**。系统可自主经门控将候选放入 Publish Queue（`READY` / `AWAITING_HUMAN_ACTION`）；不得自动执行外部发布。  
- AI 低风险决策可在授权规则内自动继续；不得把模拟执行成功（如 `published_local`）提升为商业 Reality。  
- **DEC-021：** Real Commercial Learning 仅接受已验证真实商业证据；Execution Strategy ≠ Commercial Strategy。

---

## Continuity Domain Note（连续性记录域说明）

`docs/0–6` 是项目**当前核心连续性记录域**（DEC-019）。  
历史 **Core Governance Set v1（8+1）**（DEC-009）是结构版本 / 核心认知检查清单，**≠**「当前完整核心文件集合仅此 8+1」。  
这**不改变**上表 L0–L5 权威层级：User / Reality 仍高于文档治理。  
连续性规则要求：可恢复的项目认知必须能从 `docs/0–6` 重建，而不是从聊天记忆猜测。  
Control Center = 导航 / Recovery 控制层（Navigation Authority），**不是** Reality Authority。
