# AI_FACTORY_OS Reality Alignment Correction Strategy

> **现实对齐修正策略** | Entry **041-C**  
> **Date:** 2026-07-15  
> **Type:** Docs-only Strategy Analysis（策略分析 — **不执行修复**）  
> **依据：** Entry 041-A Reality Architecture Alignment · Entry 041-B-A Modular Capability Principle（DEC-013）

**原则：** Reality > Documentation · Blueprint ≠ Production · Modular ≠ Forced Merge · Strategy ≠ Execution

**本 Entry 不做：** 修代码、迁库、改 commercial_assets、Runtime 融合、自动状态修复、删历史文件。

---

## 执行摘要

| 项 | 结论 |
|----|------|
| Governance Layer | 已完成（含模块化原则 DEC-013） |
| Reality（041-A） | Core OS ↔ Content Factory = **情况 B 双轨**；Runtime Integration = **未开始** |
| 本 Entry | 建立 **Reality Alignment 修正路线**（差距清单 + 优先级 + 边界 + DEC 候选 + 建议序列） |
| 完成态 | **Strategy Created** — 修复 **Not Started** |

---

# 1. Reality Gap Inventory（现实差距清单）

| ID | Gap | Category | Severity | Current Reality | Target State | Execution Needed |
|----|-----|----------|----------|-----------------|--------------|------------------|
| **RA-001** | `10_DEPLOY` 状态误导 | Documentation Alignment | **Medium** | `10_DEPLOY/api.py` 可运行 FastAPI HTTP 入口，包装 `SystemController` | MODULE_REGISTRY / 状态文与 Reality 一致（如 Active HTTP entry / 非 Frozen 误导） | Docs-only Entry（建议 **041-D**） |
| **RA-002** | Content Factory / 商业对象生命周期状态差异 | Commercial State Alignment | **Medium** | Product Asset 已存在且校验通过；Experiment / PR 部分仍 `draft`；Feedback `pending`、观察 `not_started` | 生命周期字段与审批/生产/观察 Reality 诚实对齐（人辅、可追溯） | 授权人辅同步策略 + 执行 Entry（建议 **041-E**）；**禁止自动修复** |
| **RA-003** | Database Schema Drift | Engineering Alignment | **Medium** | `ai_factory.db` 含 `trends`/`audit_log` 及 `platforms` 扩展列；`ensure_schema()` 未完全管理 | Code schema ↔ DB Reality 可重复对齐（现网与新环境一致） | 另开授权 DB Entry；现状仅 Blueprint（039-A） |
| **RA-004** | Legacy Broken Entry | Code Hygiene | **Low** | 旧入口错误引用（如 `0_START/self_healing_engine.py`、`9_PRODUCT/api_server.py`） | 标注 Frozen/Broken 或归档说明；避免被当作可用入口 | 文档标注优先；代码清理须另开 Engineering Entry |

### RA 明细（必填项展开）

#### RA-001 — 10_DEPLOY 状态误导

| 项 | 内容 |
|----|------|
| **Reality** | `10_DEPLOY` 存在可运行 FastAPI HTTP 入口 |
| **Documentation** | MODULE_REGISTRY 标记 **Frozen** |
| **Category** | Documentation Alignment |
| **Severity** | Medium |
| **Risk** | 会话误以为 Deploy 不可用，或反过来误以为「已全面生产部署」 |

#### RA-002 — Content Factory 生命周期状态差异

| 项 | 内容 |
|----|------|
| **Reality** | commercial_assets：Product Asset 已存在；Experiment / Production Request 部分仍 `draft`；Feedback 未开始观察 |
| **Category** | Commercial State Alignment |
| **Severity** | Medium |
| **Risk** | 降低商业验证可信度；文档「Pilot 完成」与 JSON 字段冲突 |

#### RA-003 — Database Schema Drift

| 项 | 内容 |
|----|------|
| **Reality** | Database 存在未被 `ensure_schema` 管理的表/字段（见 039-A / 041-A） |
| **Category** | Engineering Alignment |
| **Severity** | Medium |
| **Risk** | 新环境 bootstrap ≠ 现网能力；阻碍可重复部署 |

#### RA-004 — Legacy Broken Entry

| 项 | 内容 |
|----|------|
| **Reality** | 部分旧入口存在错误引用 |
| **Category** | Code Hygiene |
| **Severity** | Low |
| **Risk** | 误启动损坏入口；对主路径能力影响有限 |

**补充说明（非新 RA ID，归属已知 P0）：** Core OS 与 CF **Runtime 零连接** 已由 041-A 确认。在 DEC-013 下，这可解释为**模块独立运行**；差距在于「文档/话术宣称统一 Runtime」而非「必须立即融合」。修正优先诚实标注，**禁止自动融合**。

---

# 2. Correction Priority（修正优先级）

## P0 — 真实性（不改变系统能力）

**定义：** 不改变系统能力，只提高真实性。

**包括：**

- 文档状态修正（如 RA-001 MODULE_REGISTRY Deploy 状态）
- Reality 标注（双轨 / Isolated / Runtime Not Connected / Draft≠完成）
- Audit 与 Current State 投影同步

**建议对应：** Entry **041-D** Reality Documentation Alignment

## P1 — 商业验证可信度

**定义：** 影响商业验证可信度。

**包括：**

- commercial_assets 生命周期同步**策略确认与授权执行准备**（RA-002）
- Pilot 观察准备（仍须另开；本策略不启动观察）

**建议对应：** Entry **041-E** Commercial Validation Preparation

## P2 — 未来工程稳定性

**定义：** 未来工程稳定性。

**包括：**

- Schema alignment（RA-003）
- Runtime bridge **preparation / design**（非实施）
- Broken entry 工程清理（RA-004，低优先）

**建议对应：** **041-F** Module Orchestration Design → **041-G** Runtime Integration Decision（决策，非默认开干）

---

# 3. Execution Boundary（执行边界）

### Current Allowed（当前允许）

- Documentation alignment
- State clarification
- Audit / Strategy docs
- DEC 候选记录（不提前拍板）

### Current Forbidden（当前禁止）

- Code modification
- Database migration
- Runtime integration
- Module merge（Core OS ↔ Content Factory 强制融合）
- 自动修复 commercial_assets 状态
- 删除历史文件
- 修改 API / 目录结构 / 模块代码（本策略阶段）

**Strategy Created ≠ Fix Executed.**

---

# 4. Architecture Decision Preparation（架构决策准备）

**注意：以下仅为 Candidate，不得在本 Entry 提前决定。**

## DEC Candidate 1 — Core OS + Content Factory 长期模式

| Option | 含义 |
|--------|------|
| **A** | Permanent Modular Dual Track（永久模块化双轨 + 人辅/文档编排） |
| **B** | Governed Runtime Bridge（授权编排层桥接，模块仍可独立） |
| **C** | Hybrid Model（部分链路桥接、部分保持独立销售入口） |

**约束：** 须服从 DEC-013（统一治理 ≠ 强制融合；Modular ≠ Fragmented）。  
**建议决策入口：** Entry **041-G**（仅 Decision，不自动实施 B/C）。

## DEC Candidate 2 — Database 与 Commercial Asset 数据边界

需正式固定（可与既有 UA §7.1 / DEC 对齐并补 DEC 编号）：

| 域 | 预期 SoT |
|----|----------|
| **Operational Data** | SQLite（`data/ai_factory.db`）— 采集、评分、OS 运行日志等 |
| **Commercial SoT** | `commercial_assets/` — Opportunity / Experiment / PR / Asset / Feedback 等 |

**禁止：** 用 Operational 表「冒充」商业生命周期完成；用文档覆盖 JSON Reality。

---

# 5. Future Execution Sequence（建议后续序列）

| Entry | 标题（建议） | 意图 | 优先级 | 改 Reality？ |
|-------|--------------|------|--------|--------------|
| **041-D** | Reality Documentation Alignment | 修文档/Registry/标注（RA-001 等 P0） | P0 | Docs only |
| **041-E** | Commercial Validation Preparation | RA-002 人辅同步准备/授权边界与观察前检查 | P1 | 仅在明确授权时触达 Assets |
| **041-F** | Module Orchestration Design | 模块编排/契约设计（桥接准备，不实施） | P2 design | Docs only |
| **041-G** | Runtime Integration Decision | DEC Candidate 1（A/B/C）正式裁决 | P2 decision | Decision only |

序列可按授权调整顺序，但 **不得跳过边界**将 041-G 直接变成无授权大融合。

---

# 6. 与 Modular Principle 的关系

| 原则 | 本策略态度 |
|------|------------|
| DEC-013 Modular Capability | **保留并作为边界** |
| Isolated CF 可继续独立演进 | **允许** |
| 文档诚实 > 假统一 | **P0 优先** |
| 自动 Runtime 融合 | **禁止（本阶段）** |

---

## 状态声明

| 项 | 状态 |
|----|------|
| Reality Alignment Correction Strategy | **Created** |
| Gap Inventory RA-001..004 | **Documented** |
| Correction execution | **Not Started** |
| Runtime Integration | **Not Started** |
| Auto merge / auto state fix | **Forbidden** |

---

**Entry 041-C：** Reality Alignment Correction Strategy — **COMPLETED（策略完成，修复未执行）**。
