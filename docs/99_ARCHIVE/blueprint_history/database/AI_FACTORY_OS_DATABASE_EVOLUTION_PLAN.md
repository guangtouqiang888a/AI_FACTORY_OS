# AI_FACTORY_OS Database Evolution Plan v1

> Entry 039-A — Future Migration Plan（**仅规划，不实现**）  
> **状态：Planning Blueprint Completed — Implementation Not Started**

**原则：** Additive Evolution · 禁止破坏现有 Operational 数据 · Commercial JSON 迁移须双写验证 · Design ≠ Production

**前置事实：** Inventory + Schema Drift（039-A）；Alignment（038-B）；Schema Blueprint / Migration Plan（历史文档）

---

## 1. 是否需要 Schema Migration？

### 结论：**需要（未来 Entry）— 非本 Entry**

| 驱动 | 说明 |
|------|------|
| SD-004 | ensure_schema 与现网文件分叉 — **优先对齐** |
| SD-001~003 | platforms 列 / trends / audit_log orphan |
| 历史 Blueprint | market_* / opportunity_scores / generated_products / product_feedback — **未建** |

### 推荐顺序（规划）

```
Phase 0 — Backup ai_factory.db（强制）
    ↓
Phase 1 — Schema Reality Alignment
         （additive：platforms 列；决定 trends/audit_log deprecate 或 CREATE 进 ensure_schema）
    ↓
Phase 2 — Optional Intelligence Tables（须审批）
         （仅当 Cognition/Feedback 时序需求确认）
    ↓
Phase 3 — Optional Commercial Mirror Tables
         （JSON 仍为 SoT；DB 为查询副本）
```

**禁止：** 本计划执行前 CREATE/ALTER；禁止把 JSON Commercial 直接「搬空」到 DB。

---

## 2. 是否需要 ORM？

### 结论：**近期不需要；中期可选轻量封装**

| 选项 | 建议 |
|------|------|
| 现状 | 手写 sqlite3 + `database.py` — **保持** |
| SQLAlchemy / 全量 ORM | ❌ 过早 — 表少、双轨、治理优先 |
| 轻量 repository 层 | ⚠️ Phase 2+ — 统一 ensure_schema 与 query API |

**理由：** 当前问题是 **权威与漂移**，不是查询复杂度。

---

## 3. 是否需要 Unified Data Layer？

### 结论：**需要定义接口；不建议过早实现单一存储**

目标形态（设计）：

```
┌──────────────────────────────────────┐
│     Unified Data Access Contracts    │  ← 文档/协议层（可先）
│  Operational API | Commercial API    │
└─────────────┬────────────┬───────────┘
              ↓            ↓
     data/ai_factory.db   commercial_assets/
```

| 层 | 近期 | 远期 |
|----|------|------|
| Contract 文档 | ✅ 本 Entry Ownership + Authority + Boundary | 扩展 |
| 单一物理库 | ❌ | 仅当公司化多用户/API 后评估 |
| 双写同步器 | ❌ | Commercial mirror 阶段 |

**Unified Architecture（038-B）** 的 Data→…→Memory 流是 **逻辑层**；物理上可长期双存储。

---

## 4. 是否需要 Event System？

### 结论：**扩展现有 event_log；不新建消息队列（近期）**

| 现状 | `7_MEMORY/event_log.jsonl` + execution_hash |
|------|---------------------------------------------|
| 缺口 | Commercial 状态变更 **无** 统一 event（人工 Entry 改 JSON） |
| 近期 | 可选：人工 Entry checklist 写一条 governance event（仍 JSONL） |
| 远期 | Domain events（product_asset.created、feedback.updated）— 在镜像 DB 或 bus 前先定 Authority |

**禁止：** 未治理前引入 Kafka/Redis 等重型事件系统。

---

## 5. 与既有计划文档关系

| 文档 | 角色 |
|------|------|
| `DATABASE_SCHEMA_BLUEPRINT.md` | 目标表设计（非现网） |
| `DATABASE_MIGRATION_PLAN.md` | Additive 路线（历史） |
| `DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md` | 实施步骤（**Pending**） |
| **本文档** | 039 治理视角：对齐优先 → 可选智能表 → 可选镜像 |

**冲突解决：** 以 **Inventory / Schema Drift 事实** 为先；Blueprint 不得覆盖 Reality。

---

## 6. 规划决策摘要

| 议题 | 决策 |
|------|------|
| Schema migration | **Yes — future authorized Entry**；先 Reality Alignment |
| ORM | **No for now** |
| Unified Data Layer | **Contract first**；单一存储 **No** |
| Event system | **Extend event_log**；无 MQ |
| Commercial → DB | **JSON Keep**；Feedback 未来优先候选镜像 |
| Pilot data | **Preserve** preq_005 / 8523329941d4 |

---

## 7. 下一授权 Entry 候选（不自动执行）

1. **039-B / Schema Reality Alignment** — ensure_schema additive + orphan 处置  
2. **Commercial Lifecycle Status Sync** — JSON status 字段（非 DB）  
3. **Validation Gate Adapter 接入** — 非 DB  
4. **Observation / Feedback writer** — JSON 优先；DB 表另批  

---

## 本 Entry 操作

- ✅ 规划完成  
- ❌ 未 migration、未 ORM、未建表、未改 Runtime  
