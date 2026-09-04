# AI_FACTORY_OS Documentation Map Reference

> **文档角色：** Documentation Map Reference（参考索引 · 非唯一导航入口）  
> Entry **044-A** · 由原 Documentation Map 降级  
> Last updated: 2026-07-17

**唯一导航入口已迁移至：**

→ [docs/AI_FACTORY_OS_DOCUMENTATION_MAP.md](../AI_FACTORY_OS_DOCUMENTATION_MAP.md)

请以该文件为 Documentation Map SoT。本文件仅保留历史协作控制层说明，**不再**作为文档结构权威入口。

---

## Legacy: Two Layers（历史说明 · 保留）

### Control Layer (session authority for interpretation)

| File | Role |
|------|------|
| `AI_FACTORY_OS_CONTROL_CENTER.md` | **Single session entry point** |
| `AI_FACTORY_OS_PROJECT_CONSTITUTION.md` | Permanent mission / principles |
| `AI_FACTORY_OS_CURRENT_STATE.md` | Factual now |
| `AI_FACTORY_OS_DECISION_LOG.md` | Durable decisions |
| `AI_FACTORY_OS_EXECUTION_PROTOCOL.md` | How tasks run |
| `AI_FACTORY_OS_AUTHORITY_MODEL.md` | Truth hierarchy |
| `AI_FACTORY_OS_DOCUMENTATION_MAP.md` | **现指向根目录唯一导航入口** |

These files **have authority over how documentation is interpreted** in a session (what to read, what not to claim).

They do **not** override Runtime / Code / DB / Asset Reality.

---

### Knowledge / Reference Layer

Includes (non-exhaustive):

- `PROJECT_STATUS.md`, `system_snapshot.md`, `CURSOR_EXECUTION_HISTORY.md`
- Blueprints / Contracts / Protocols
- Audits under `docs/07_AUDIT/`
- Archive under `docs/99_ARCHIVE/`（默认不参与判断）

Purpose: designs, history, deep reference.

---

## Authority of Interpretation

When docs disagree with each other:

1. Check **Reality** (Authority Model levels 1–4)
2. Check **Current State** + **Decision Log**
3. Use [DOCUMENTATION_MAP](AI_FACTORY_OS_DOCUMENTATION_MAP.md) + Control Center Required Reading
4. Treat long narratives in Project Status / Snapshot as **projections** until validated

---

## Anti-Explosion Rules（仍适用）

- New design docs require a Decision or Entry justifying why Control Center / Documentation Map is insufficient
- Prefer updating Current State / Decision Log over adding parallel “status” files
- Audits go to `docs/07_AUDIT/`; do not promote every audit to Required Reading
- Structure rules: see Knowledge Update Protocol — **Documentation Structure Governance Rules**

---

**Entry 044-A：** 本文件降级为 Documentation Map Reference；唯一入口见根目录 Documentation Map。


---

# REFERENCE_ONLY_STATUS

本文档：

仅作为历史引用。

不是 Documentation Map 唯一入口。

当前唯一导航入口：

docs/AI_FACTORY_OS_DOCUMENTATION_MAP.md

---

# REFERENCE_HISTORY_STATUS


状态：

历史参考文件。


禁止：

作为当前导航入口。


当前唯一导航入口：

docs/AI_FACTORY_OS_DOCUMENTATION_MAP.md

