# AI_FACTORY_OS Architecture Evolution Context Record

> **架构演进上下文记录** | Entry **041-D-A Revision**  
> **Date:** 2026-07-16  
> **定位：架构历史解释文件（Historical / Explanatory）**

---

## 文件角色声明（必须保留）

**本文件用于解释架构演进背景，不定义当前系统状态，不覆盖 Reality，不替代 Core Governance。**

任何模块状态必须以：

- **Reality**（Code / Database / commercial_assets / 可运行入口）
- **Current State**
- **Authority Model**

为准。

| 本文件 **不是** | 本文件 **是** |
|-----------------|---------------|
| 核心治理文件 | 架构历史解释 |
| Current State | 目录/模块「为何长这样」的背景 |
| Architecture 规则文件（如 UNIFIED_ARCHITECTURE） | 误读缓冲层 |
| Business Strategy | 与 DEC / Blueprint 并列的「为什么」说明 |

**权威冲突时：** Reality > Current State > Authority / Core Governance > 本文件。  
**禁止：** 把本文「规划过」写成「已实现」；把本文当成 MODULE_REGISTRY 替代品。

**原则：** Reality > Documentation · Blueprint ≠ Production · Design ≠ Runtime · Modular ≠ Fragmented · Unified ≠ Forced Merge

---

## 一、整体演进一句话

AI_FACTORY_OS 的 `0`–`11` 目录编号，大体来自早期「数据→认知→决策→产品→内容→执行→记忆→配置→商业化→部署」的**分层规划习惯**；后续在商业验证压力下涌现 `11_CONTENT_FACTORY` 与 `commercial_assets`，形成与 Core OS **同仓库、不同 Runtime** 的现实（情况 B）。这属于 **Intentional Isolation + Unfinished Convergence** 的解释背景——**不是**失败复制项目的判决书，也**不是**已融合系统的证明。

### 0–11 目录定位（041-H / DEC-018）

`0`–`11` 目录属于**历史演进形成的工程结构**。

- **Folder Structure ≠ Capability Architecture ≠ Product Architecture**
- 未来状态变化：**必须先更新** Current State、Module Registry；**再更新**本 Evolution Context
- **禁止：** 历史解释覆盖现实状态；禁止用目录名推断商业能力边界

---

## 二、目录演进背景（0–11）

> 以下仅记录**历史原因与现实对照提示**。未来规划≠事实。状态以 Current State / Reality 为准。

### 0_START

**历史：** 核心运行入口与编排中枢（controller / planner / policy / runtime）建设位置。  
**演进意图：** 把「系统怎么跑起来」集中在一起。  
**当前 Reality 提示：** Active — Core OS 编排入口（详见 Current State / MODULE_REGISTRY）。

### 1_DATA

**历史：** 数据能力建设背景 — 外部采集、SQLite operational 存储、数据源管理。  
**演进意图：** 先有可积累的市场/商品操作数据，再谈上层决策。  
**当前 Reality 提示：** Active — Operational Data 域（≠ Commercial Object SoT）。

### 2_COGNITION

**历史：** 早期规划中的认知 / 市场智能能力**预留目录**。  
**演进意图：** 计划承接趋势理解、机会发现等。  
**当前 Reality：** **未实现**（空/Planned）。不得写成已具备 Cognition Runtime。

### 3_DECISION

**历史：** 评分、风险与 OS 域决策逻辑落地位置。  
**演进意图：** 在数据之上形成可执行的打分/裁决。  
**当前 Reality 提示：** Active — 主要服务 Core OS Track A。

### 4_PRODUCT

**历史：** 产品能力规划目录（产品定义/规格类能力预留）。  
**演进意图：** 为「产品层」留编号槽位。  
**当前 Reality：** **未形成独立 Runtime**（Planned / 空或未接入主链）。

### 5_CONTENT

**历史：** 内容知识 / 内容策略类规划目录。  
**演进意图：** 与「内容」相关的非工厂流水线能力预留。  
**当前 Reality 提示：** Planned — 未实现独立运行能力。内容生产现实主要在 `11_CONTENT_FACTORY`。

### 6_EXECUTION

**历史：** OS 执行发布/任务落地（本地 execution agent 等）。  
**演进意图：** Decision 之后的执行闭环。  
**当前 Reality 提示：** Active — Track A 执行侧。

### 7_MEMORY

**历史：** 运行记忆、策略/模式沉淀位置。  
**演进意图：** 从执行反馈中学习。  
**当前 Reality 提示：** Active（文件型 memory）；个别资产可能 orphan（以 Reality 为准）。

### 8_CONFIG

**历史：** 配置与模块激活清单集中地。  
**演进意图：** 可配置、可声明 Active modules。  
**当前 Reality 提示：** Active — 配置 Reality 以代码/config 为准（如 ACTIVE_MODULES 不含 CF）。

### 9_PRODUCT

**历史：** 早期 SaaS / Product 方向探索产生的**历史目录**。  
**演进意图：** 曾尝试产品化/API/计价等。  
**当前：** **保留历史上下文。**  
**禁止：** 在本文件中定义其未来用途；不得写成现行主商业路径。状态以 Registry（Frozen / Broken legacy）与 Reality 为准。

### 10_DEPLOY

**历史：** 早期服务化 / SaaS 探索相关的部署与 HTTP 包装目录。  
**演进意图：** 把 Core OS 能力以服务形式暴露。  
**当前 Reality 提示：** 存在 **HTTP Runtime 能力**；**不代表 Production Ready / Fully Deployed**（见 041-D）。

### 11_CONTENT_FACTORY

**历史：** 数字产品验证阶段形成的内容 / 数字商品生产能力。  
**演进意图：** 快速验证「能生产可交付资产」，对接 `commercial_assets` 商业对象链。  
**当前 Reality 提示：** **独立商业能力轨道（Track B）**；Runtime **尚未**与 Core OS 融合（Integration Not Started）。不是失败复制项目。

---

## 三、如何与其他文件分工

| 问题 | 去哪看 |
|------|--------|
| 现在系统什么阶段、阻塞什么？ | Current State |
| 模块 Status Active/Frozen？ | MODULE_REGISTRY + Reality |
| 目标架构原则 / 模块化规则？ | UNIFIED_ARCHITECTURE + Constitution / DEC-013 |
| 商业现阶段做什么？ | BUSINESS_STRATEGY |
| 为什么目录叫这些名字、为何空目录还在？ | **本文件** |

---

## 四、维护规则

- 仅追加/修订**历史解释**；不在此写入新 Runtime 完成声明。  
- 模块状态变更后：**先**更新 Current State / Registry（及 Reality），**再**可选地修订本文件措辞。  
- 本文件变更属 **Historical layer**（见 Knowledge Update Protocol 文档生命周期）。

### 4.1 历史解释 vs Reality 更新顺序（041-G / DEC-017）

**历史解释文件不是当前状态来源。**

如果 Reality 变化：

1. **必须优先更新：** Current State、Module Registry、相关 Architecture 文件（如 UNIFIED_ARCHITECTURE 摘要）
2. **然后再**调整本历史解释文件

**禁止：** 用本文件推断当前系统；禁止只改本文件、不同步 Current State / Module Registry。

---

**Entry 041-D-A：** Architecture Evolution Context Record created（历史解释层）。  
**Entry 041-G：** 明确更新顺序 — Reality 投影优先于历史解释修订（DEC-017）。  
**Entry 041-H：** 明确 0–11 = 工程结构；Folder ≠ Capability ≠ Product（DEC-018）。
