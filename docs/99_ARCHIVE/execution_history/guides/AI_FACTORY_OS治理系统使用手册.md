# AI_FACTORY_OS治理系统使用手册

> 本文档用于指导 AI_FACTORY_OS 使用流程。  
> 本文档不是最高权威来源。  
>  
> 当本文档与以下文件冲突时，以：  
>  
> **Reality（运行现实）＞ Authority Model（权威模型）＞ Current State（当前状态）＞ Core Governance Set（核心治理集）＞ 本手册**  
>  
> 为判断顺序。

> **定位：** L4 使用说明 / 操作指南  
> **不是：** 新核心控制文件、新权威来源、新架构设计；不替代 Control Center（控制中心）/ Constitution（项目宪法）/ Authority Model  
> **Entry：** 040-F-B | 最后更新：2026-07-15

---

## 1. 这个系统解决什么问题？

长期用 AI（人工智能助手）协作开发时，经常出现这些问题：

| 问题 | 人话解释 |
|------|----------|
| AI 不知道以前做过什么 | 新开一个聊天窗口，上下文就丢了 |
| AI 不知道当前真实状态 | 把「打算做」当成「已经做完」 |
| AI 容易把设计当成完成 | 蓝图写好了，就以为系统已经上线运行 |
| AI 容易忘记商业目标 | 聊着聊着跑去改架构或自动化，忘了先验证能不能卖 |
| AI 容易重复犯错误 | 以前否决过的方向，下一轮又提一遍 |

**治理层（Governance Layer）** 就是一套「长期记忆 + 判断规矩」：  
用固定核心文件告诉 AI——项目为什么存在、现在到哪了、什么不能做、冲突时听谁的。  
这样你不必每次把几百页文档重新讲一遍。

---

## 2. 平时最重要的几个文件是什么？

| 文件 | 用途 | 什么时候看 |
|------|------|------------|
| CONTROL_CENTER（控制中心） | AI 入口和导航 | 每次新对话第一看 |
| PROJECT_CONSTITUTION（项目宪法） | 项目最高原则 | 方向争议时 |
| BUSINESS_STRATEGY（商业战略） | 商业目标 | 商业决策时 |
| CURRENT_STATE（当前状态） | 当前真实状态 | 开始任何工作前 |
| DECISION_LOG（决策日志） | 历史重大决定 | 不确定为什么这么设计时 |
| EXECUTION_PROTOCOL（执行协议） | 工作规则 | 执行任务时 |
| KNOWLEDGE_UPDATE_PROTOCOL（知识更新协议） | 更新规则 | 项目变化时 |
| UNIFIED_ARCHITECTURE（统一架构） | 架构理解 | 架构设计时 |
| AUTHORITY_MODEL（权威模型） | 判断权威顺序 | 出现冲突时 |
| **本手册** | 给你（负责人）的操作指南 | 忘记怎么指挥 AI 时 |

路径均在 `docs/` 下，例如：`docs/00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md`。

---

## 3. 新建聊天窗口应该怎么做？

### 第一步

告诉 AI：

> 请读取 `docs/00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md`，并按其中的 Session Bootstrap Required Reading Order（会话启动必读顺序）恢复项目理解。

### 第二步

等待 AI 确认（可用中文向你汇报）：

- 当前阶段（Current Phase）是什么  
- 当前最高目标（Primary Goal）是什么  
- 禁止事项（Forbidden Actions）有哪些  
- 接下来还需要读哪些核心文件  

若 AI 跳过确认就开写大方案 → **叫停**，要求先完成启动确认。

### 第三步

按议题追加阅读（仍不要加载全部 docs）：

| 若涉及 | 请 AI 再读 |
|--------|------------|
| 商业方向 | `AI_FACTORY_OS_BUSINESS_STRATEGY.md` |
| 架构 | `AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md` |
| 状态 / 能不能开工 | `AI_FACTORY_OS_CURRENT_STATE.md` |
| 历史争议 / 为什么这样定 | `AI_FACTORY_OS_DECISION_LOG.md` |
| 冲突听谁的 | `AI_FACTORY_OS_AUTHORITY_MODEL.md` |

### 第四步

确认 AI 的理解与你一致后，再开始讨论方案或下达 Cursor（编程助手）执行任务。

---

## 4. 以后项目变化怎么处理？

**不是所有变化都需要改文件。** 可按等级判断（与 Knowledge Update Protocol 的 Change Level 对齐，说明从简）：

### Level 0

普通讨论、澄清问题：  
**不用更新**核心文件。

### Level 1

执行任务变化（范围仍在已批准任务内）：  
更新执行记录（如 `CURSOR_EXECUTION_HISTORY`），一般不必动战略。

### Level 2

项目状态变化（完成了某个 Entry、阻塞项变了）：  
更新：

- CURRENT_STATE  
- CURSOR_EXECUTION_HISTORY  

必要时同步 Control Center 的阶段表述。

### Level 3

商业 / 架构 / 规则变化：

必须：

1. 分析影响  
2. 生成更新方案  
3. **你确认**  
4. 更新对应核心文件 + DECISION_LOG（决策日志）

### Level 4

核心原则变化（例如永久禁止项、使命级调整）：

必须：

**重新审核治理体系**（Constitution 等），走完整确认与 DEC（Decision，正式决策编号）记录。

详细规则以 `AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md` 为准。

---

## 5. AI 什么时候必须提醒用户？

以下情况 AI **不可以直接继续闷头做**：

1. 发现商业目标变化。  
2. 发现架构方向变化。  
3. 发现核心规则冲突。  
4. 发现历史文件和当前方向冲突。  
5. 发现需要修改核心治理文件。  
6. 发现自己无法确认真实状态（Reality）。  

此时 AI 必须：

1. **暂停**扩大方案。  
2. 说明：发现的问题、影响范围、需要更新哪些文件。  
3. 给出可供你复制的 **Cursor 更新指令**（含范围与禁止项）。  
4. **等待你确认**后再改核心文件。

---

## 6. Cursor 指令使用规则

以后给 Cursor 的指令，建议至少包含：

1. **目标** — 这一次要完成什么  
2. **修改范围** — 允许改哪些路径  
3. **禁止事项** — 明确不能碰什么（如 Python / Database / commercial_assets）  
4. **需要同步文件** — 如 Current State、执行历史  
5. **验证方式** — 怎么算做完  
6. **完成报告** — 要求输出变更清单与 Yes/No 范围检查  

如果执行过程中发现还需要更新治理文件：

1. **停止扩大范围**  
2. 单独整理「治理更新内容」  
3. **等待你确认**  
4. 再开一小段任务去改文档（不要和未授权的代码/资产改动捆在一起）

---

## 7. 最重要的使用原则（简短版）

1. **不要相信聊天记忆，要相信核心文件。**  
2. **不要相信设计完成，要确认 Reality（代码/数据库/资产真实情况）。**  
3. **不要为了推进项目破坏治理。**  
4. **所有重大变化必须留下记录（DEC / Current State / 执行历史）。**  
5. **AI 负责分析和提醒，你拥有最终决策权（用户最终决策权 / L0）。**

---

## 8. 快捷路径（复制用）

| 文档 | 路径 |
|------|------|
| 控制中心 | `docs/00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md` |
| 本手册 | `docs/05_EXECUTION/guides/AI_FACTORY_OS治理系统使用手册.md` |
| 当前状态 | `docs/01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md` |
| 商业战略 | `docs/03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md` |
| 决策日志 | `docs/00_GOVERNANCE/AI_FACTORY_OS_DECISION_LOG.md` |

---

**Entry 040-F-B：** 治理系统用户操作手册已创建。  
本手册提高人工使用效率，**不修改**核心治理原则本身。
