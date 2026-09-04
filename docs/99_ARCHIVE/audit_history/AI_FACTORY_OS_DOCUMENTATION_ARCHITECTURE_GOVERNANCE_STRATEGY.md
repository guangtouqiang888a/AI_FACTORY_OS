# AI_FACTORY_OS Documentation Architecture Governance Strategy

> **文档架构治理策略** | Entry **041-E**  
> **Date:** 2026-07-16  
> **Type:** Docs-only Governance Strategy（策略 — **不移动 / 不重命名文件**）  
> **权威：** DEC-015 · Reality > Documentation · Blueprint ≠ Production

**本文件定位：** `docs/audit/` 审计/策略层说明。**不是**核心控制文件；**不替代** Authority Model / Current State / Core Governance Set。

---

## 1. 当前文档混杂风险

AI_FACTORY_OS 的 `docs/` 存在大量 Markdown。长期风险：新会话 AI 可能无法区分：

| # | 易混类型 | 误读后果 |
|----|----------|----------|
| 1 | 当前事实 | 把旧审计当 Current State |
| 2 | 架构设计 | Design = Runtime |
| 3 | 商业战略 | 愿景 = 已验证收入 |
| 4 | 历史解释 | 演进背景覆盖 Reality |
| 5 | 审计记录 | 一次性报告当永久规则 |

已完成前提（不得改写为未完成）：Reality 对齐、双轨确认、模块化原则（DEC-013）、能力组合原则（DEC-014）。

---

## 2. 文档角色分类（八层）

| # | 层 | 负责 | 典型文件（示例，非穷尽） | 禁止误用 |
|---|-----|------|--------------------------|----------|
| 1 | **核心治理层** | 系统规则、权威关系、AI 工作方式 | Control Center、Constitution、Authority、Execution/Knowledge Protocol、Decision Log | 用聊天改规则 |
| 2 | **当前状态层** | 当前 Reality 投影 | CURRENT_STATE | 用 Blueprint 覆盖 |
| 3 | **架构设计层** | 目标架构与设计原则 | UNIFIED_ARCHITECTURE、MODULE_REGISTRY（状态须对 Reality） | Design = Runtime |
| 4 | **商业战略层** | 商业方向 | BUSINESS_STRATEGY | 愿景 = 完成态 |
| 5 | **Blueprint 规划层** | 未来规划 | `*_BLUEPRINT.md`、部分 Design/Plan | Blueprint = Production |
| 6 | **历史解释层** | 为何形成现结构 | ARCHITECTURE_EVOLUTION_CONTEXT_RECORD | 覆盖 Reality / Current State |
| 7 | **审计记录层** | 验证历史 | `docs/audit/*` | 当永久 SoT |
| 8 | **执行记录层** | Cursor 执行追踪 | CURSOR_EXECUTION_HISTORY | 当商业/架构规则 |

**冲突时：** Reality > Current State > Authority / Core Governance > 其他文档层 > Conversation Memory。

---

## 3. 不移动文件原则

本策略阶段（及默认）：

- **不**移动文件
- **不**重命名文件
- **不**整理物理目录结构
- **只**通过角色分层 + 读取顺序 + DEC 降低误读

物理整理若需要，须**另开授权 Entry**（明确 Scope）。

---

## 4. 未来整理路线（建议 — 未授权不执行）

| 阶段 | 动作 | 状态 |
|------|------|------|
| Now（041-E） | 角色分层原则 + DEC-015 + Control Center 提示 | **本 Entry** |
| Later | 为高误读 Blueprint 批量加 Document Role banner | 可选 Entry |
| Later | 可选：`docs/` 子目录物理归档（Historical / Blueprint / Audit） | 须授权；非默认 |
| Never by default | 删除历史审计 / 用整理覆盖 Reality | **禁止** |

---

## 5. 与 Reality 原则关系

| 原则 | 在文档治理中的含义 |
|------|-------------------|
| Reality > Documentation | 任何层文档不能覆盖 Code/DB/Assets/Runtime |
| Blueprint ≠ Production | 规划层完成 ≠ 生产完成 |
| Design ≠ Runtime | 架构设计层 ≠ 已融合 Runtime |
| Modular ≠ Fragmented | 分层治理 ≠ 文档散装无权威 |
| Unified ≠ Forced Merge | 统一文档角色 ≠ 强制 Runtime 融合 |

---

## 6. 能力与文件夹（交叉引用）

见 Constitution：**Capability ≠ Folder Mapping Principle**（DEC-014 / 041-E 增补说明）。  
商业能力可跨目录组合；目录是工程组织，不是 SKU 边界。

---

**Entry 041-E：** Documentation Architecture Governance Strategy — **Created**（策略完成；文件未移动）。
