# ENTRY 044-B Documentation Physical Consolidation Report

> **Entry:** 044-B  
> **Title:** Documentation Physical Consolidation v1  
> **Date:** 2026-07-17  
> **Mode:** Controlled Documentation Migration Only  
> **Scope:** `docs/**`

**禁止范围确认：** Python / Runtime / Database / commercial_assets / API / Assets — **未修改**。

---

## 0. 执行前分类摘要（内容优先）

| 类 | 含义 | 代表 |
|----|------|------|
| A Core Governance | `00_GOVERNANCE` 六文件 | Control Center … Knowledge Update |
| B Current Authority | Current State + Module Registry | `01_CURRENT_STATE/` |
| C Architecture | UA + Data Ownership | `02_ARCHITECTURE/` |
| D Business Current | BUSINESS_STRATEGY only | `03_BUSINESS/` |
| E Blueprint | 设计类 → 子目录 | `04_BLUEPRINT/{commercial,runtime,database,contract,protocol,policy}/` |
| F Execution | History 台账 / 手册 / Map Reference | `05_EXECUTION/` |
| G History | Evolution + Commercial Snapshot | `06_HISTORY/` |
| H Audit | 证据 → 子目录 | `07_AUDIT/{structure,runtime,database,migration,commercial,validation,asset}/` |
| I Archive | 冻结参考 | `99_ARCHIVE/` |
| J Duplicate / Cleanup | 空目录 / 降级平行入口 | 见 `structure/cleanup_candidates.md` |

---

## 1. 移动文件列表（摘要）

### Wave A — 边界硬化（约 49）

| From | To |
|------|-----|
| `02_ARCHITECTURE/*Schema Drift*` | `07_AUDIT/database/` |
| `02_ARCHITECTURE/*Adapter Architecture Audit*` | `07_AUDIT/runtime/` |
| `03_BUSINESS` 非 Strategy 设计 | `04_BLUEPRINT/commercial|policy/` |
| `03_BUSINESS/reports/*` | `07_AUDIT/commercial/` |
| `04_BLUEPRINT/*.md`（平铺） | `04_BLUEPRINT/{commercial,runtime,database,contract,protocol,policy}/` |
| `05_EXECUTION/SYSTEM_GOVERNANCE_PROTOCOL` | `99_ARCHIVE/` |
| `05_EXECUTION/STATE_AUTHORITY_PROTOCOL` | `04_BLUEPRINT/policy/` |
| `05_EXECUTION/reports/BROKEN_ENTRY` | `07_AUDIT/runtime/` |

### Wave B — Audit 子类（约 46）

| From | To |
|------|-----|
| `07_AUDIT` 根下编号审计 / Reality | `07_AUDIT/runtime/` |
| `*_VALIDATION_*` / Acceptance | `07_AUDIT/validation/` |
| 文档结构 / 知识治理设计审计 | `07_AUDIT/structure/` |
| Document Structure Migration Plan/Execution | `07_AUDIT/migration/` |
| `7_COMMERCIAL_ASSET_REPORT` | `07_AUDIT/commercial/` |

**未移动：** `00_GOVERNANCE/*` · Current State / Registry · UA · BUSINESS_STRATEGY · CURSOR_EXECUTION_HISTORY · 治理手册 · Evolution Context · 根 Documentation Map · 既有 Archive 两文件。

---

## 2. 新目录结构（迁移后）

```
docs/
├── AI_FACTORY_OS_DOCUMENTATION_MAP.md          # 导航 SoT
├── 00_GOVERNANCE/                              # 6 Core
├── 01_CURRENT_STATE/                           # State + Registry + reference/
├── 02_ARCHITECTURE/                            # UA + Data Ownership
├── 03_BUSINESS/                                # BUSINESS_STRATEGY only
│   └── reports/                                # 空（cleanup candidate）
├── 04_BLUEPRINT/
│   ├── commercial/ (13)
│   ├── runtime/ (9)
│   ├── database/ (5)
│   ├── contract/ (4)
│   ├── protocol/ (3)
│   └── policy/ (4)
├── 05_EXECUTION/                               # History + Map Reference + guides/
│   └── reports/                                # 空（cleanup candidate）
├── 06_HISTORY/                                 # 2
├── 07_AUDIT/
│   ├── structure/ (+ cleanup_candidates.md)
│   ├── runtime/
│   ├── database/
│   ├── migration/
│   ├── commercial/
│   ├── validation/
│   └── asset/
├── 99_ARCHIVE/                                 # 3（+ SYSTEM_GOVERNANCE_PROTOCOL）
└── audit/                                      # 空壳（cleanup candidate）
```

| 目录 | Markdown 数 |
|------|-------------|
| 00_GOVERNANCE | 6 |
| 01_CURRENT_STATE | 4 |
| 02_ARCHITECTURE | 2 |
| 03_BUSINESS | 1 |
| 04_BLUEPRINT | 38 |
| 05_EXECUTION | 3 |
| 06_HISTORY | 2 |
| 07_AUDIT | 65+（含本报告与 cleanup 清单） |
| 99_ARCHIVE | 3 |
| 根 Documentation Map | 1 |

---

## 3. 引用修复列表

| 项 | 结果 |
|----|------|
| 方式 | 按 basename 重写 `](...md)` 相对路径；同步常见 `docs/.../File.md` 字符串 |
| 触及文件数 | **75** |
| 约计替换操作 | **~1770** |
| Control Center 链接抽检 | **63 链接 · 0 broken** |
| Documentation Map | **已更新**子类说明与 044-B 指针 |

**风险：** 大型台账（MODULE_REGISTRY / PROJECT_STATUS / system_snapshot）内 `docs/...` 字符串替换量大；若存在同名歧义需人工抽检（见风险）。

---

## 4. 重复文件处理结果

| 冲突点 | 权威保留 | 处理 |
|--------|----------|------|
| Documentation Map | 根 `docs/AI_FACTORY_OS_DOCUMENTATION_MAP.md` | `05_EXECUTION` 副本保持 Reference（044-A） |
| Execution 规则 | `00_GOVERNANCE/EXECUTION_PROTOCOL` | `SYSTEM_GOVERNANCE_PROTOCOL` → `99_ARCHIVE` |
| Business Strategy | `03_BUSINESS/BUSINESS_STRATEGY` | 辅文迁出 Business；Archive BUSINESS_PLAN 不动 |
| Current State | `01_CURRENT_STATE/CURRENT_STATE` | reference 快照保留；History 不迁入 State |
| 双 audit 路径 | `07_AUDIT/` | 空 `docs/audit/` 仅登记清理候选 |

**确认：** 无两个 Current State / 两个 Business Strategy / 两个 Execution Protocol（现行目录内）。

---

## 5. 待删除候选

见：[cleanup_candidates.md](../structure/cleanup_candidates.md)

摘要：空目录 `docs/audit/`、`03_BUSINESS/reports/`、`05_EXECUTION/reports/`；降级平行入口文件**不删**。

---

## 6. 未修改范围确认

| 项 | 结果 |
|----|------|
| Python / Runtime / DB / commercial_assets / API / Assets | **No** |
| 高风险文件删除 | **No** |
| 核心文件 basename 重命名 | **No** |
| 第二阶段之外的业务逻辑 | **No** |

---

## 7. 风险与后续建议

| ID | 说明 | 建议 |
|----|------|------|
| R-044B-01 | 大文件 `docs/` 字符串批量替换 | 抽检 Registry / Status / Snapshot |
| R-044B-02 | 空目录残留 | 授权 Entry 删除空目录 |
| R-044B-03 | Blueprint 子类边界主观（cognition→runtime 等） | 可按使用反馈微调（须 Migration Rule） |

---

**Entry 044-B：** Documentation Physical Consolidation v1 — **COMPLETED**。
