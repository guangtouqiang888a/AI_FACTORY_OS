# GITHUB_SYNC_AUDIT_DIRECTORY_STRUCTURE_PROBE

> **This is a temporary READ-ONLY directory-structure probe report. Its final archival location will be determined after the existing 07_AUDIT classification rules are verified.**

**Report Type:** Temporary structure probe (READ-ONLY)  
**Document Role:** Directory map + classification Reality for GitHub sync Phase report placement  
**Status:** READ-ONLY COMPLETE  
**Execution time:** 2026-09-04 (local)  
**Project root:** `D:\AI_FACTORY_OS`  
**Scope:** `docs/07_AUDIT/` only  

**Execution boundary:**

* 未修改业务代码
* 未修改治理文件
* 未修改 `.gitignore`
* 未执行 git add / commit / push
* 未启动 Entry 077
* 未移动/重命名/删除既有报告
* 未新建 07_AUDIT 子目录（本探测报告按指令落于 07_AUDIT **根目录**）

---

## 1. `docs/07_AUDIT/` 完整目录地图

```text
docs/07_AUDIT/
├── README.md
├── [ROOT Entry / capability audits — 21 Entry-like + README = 22 md]
│   ├── ENTRY_066_… through ENTRY_076_…
│   ├── XIANYU_*_ENTRY_058D/058E/062/063/064/065.md
│   ├── REAL_XIANYU_*_ENTRY_060/061.md
│   ├── AUTONOMOUS_MARKET_ACQUISITION_ENTRY_059.md
│   └── (this temporary probe) GITHUB_SYNC_AUDIT_DIRECTORY_STRUCTURE_PROBE.md
├── asset/          (3 md)
├── commercial/     (8 md)
├── database/       (8 md)
├── migration/      (9 md)
├── runtime/        (12 md)
├── structure/      (21 md)
└── validation/     (18 md)
```

**Totals (Reality at probe time):**

| Location | `.md` count |
|----------|------------:|
| `(root)` | 22 (+ this probe after write) |
| `asset/` | 3 |
| `commercial/` | 8 |
| `database/` | 8 |
| `migration/` | 9 |
| `runtime/` | 12 |
| `structure/` | 21 |
| `validation/` | 18 |
| **Total** | **101** before this probe file |

**No further nested subdirectories** under the seven named folders (flat one-level taxonomy).

---

## 2. 正式目录规则（已发现）

### Source: `docs/07_AUDIT/README.md` (highest local SoT for this folder)

```text
用途：保存验证、迁移、检查报告。

分类：
- structure
- runtime
- database
- migration
- commercial
- validation
- asset
```

**Not defined in README:**

* dedicated `entry/` directory
* dedicated `cursor/` / `execution/` directory
* dedicated `git/` / `github/` / `sync/` directory
* dedicated `phase/` directory
* one-Entry-one-directory rule
* prohibition of root-level reports

### Related Reality (not a second taxonomy)

* Continuous Cursor ledger lives in **`docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md`** (Execution directory), **not** as per-phase files under `07_AUDIT`.
* ENTRY 044-R moved many **historical** governance/strategy reports to `99_ARCHIVE/audit_history/`, while keeping ENTRY_044 series under `07_AUDIT`.
* No separate “report registry” file found inside `07_AUDIT` beyond README + scattered references in CURRENT_STATE / MODULE_REGISTRY / CURSOR_EXECUTION_HISTORY.

---

## 3. 各目录实际职责判断

| Directory | Actual role (from README + sample titles/content) |
|-----------|-----------------------------------------------------|
| **(root)** | **Operational Entry / capability audit landing zone** for recent numbered Entries (066–076) and many 058–065 Xianyu/acquisition audits. Also holds README. |
| **structure/** | Documentation structure, role purification, conflict, cleanup, directory-role audits (heavy ENTRY_044_* series). |
| **runtime/** | Module/runtime/architecture reality audits (numbered 1–10 series + Content Factory / Reality Alignment). |
| **database/** | DB inventory, schema drift, provenance, import pilots (incl. some `*_ENTRY_058*` reports). |
| **migration/** | Document/structure migration plans/execution; also some pilot Entry reports (044-A/B, 045-A, 055, 056, 057). |
| **commercial/** | Commercial object/state/field alignment & pilot migration analysis. |
| **validation/** | Acceptance / validation reports (`*_VALIDATION_REPORT.md`), often paired with governance/docs work (incl. ENTRY_044_S/T/U). |
| **asset/** | Asset scan / asset audit templates & reports. |

---

## 4. Entry 报告实际归属

### Pattern A — Root (dominant for recent capability Entries)

Examples:

* `ENTRY_066_…` … **`ENTRY_076_OPPORTUNITY_TO_PRODUCT.md`**
* `XIANYU_EXTENSION_IMPLEMENTATION_ENTRY_065.md`
* `REAL_XIANYU_BROWSER_COLLECTION_ENTRY_060.md`
* `AUTONOMOUS_MARKET_ACQUISITION_ENTRY_059.md`

**ENTRY_076 Reality path:**

```text
D:\AI_FACTORY_OS\docs\07_AUDIT\ENTRY_076_OPPORTUNITY_TO_PRODUCT.md
```

(= **`docs/07_AUDIT/` root**, not a subdirectory)

### Pattern B — Thematic subdirectory (older / domain-tied)

Examples:

* `migration/ENTRY_055_E2E_PRODUCT_GENERATION_PILOT_REPORT.md`
* `database/DATABASE_PROVENANCE_AUDIT_ENTRY_058A.md`
* `structure/ENTRY_044_M_CORE_DIRECTORY_ROLE_AUDIT_REPORT.md`
* `validation/ENTRY_044_S_DOCUMENTATION_FINAL_STABILITY_VALIDATION_REPORT.md`

**Conclusion:** There is **no single mandatory Entry subdirectory**. Recent market/product Entry audits **uniformly use the 07_AUDIT root** with names `ENTRY_NNN_…` or `TOPIC_ENTRY_NNN`.

---

## 5. Cursor 执行报告实际归属

| Kind | Location | Notes |
|------|----------|-------|
| Continuous Cursor execution ledger | `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` | **Outside** `07_AUDIT` |
| Per-Entry audit detail | `docs/07_AUDIT/` (root or thematic) | Linked from History / Current State |
| Dedicated `07_AUDIT/cursor/` | **Not found** | No existing instance |

**Conclusion:** Cursor *process ledger* ≠ Audit *Entry report*. Phase sync write-ups are closer to Audit/verification artifacts than to replacing `CURSOR_EXECUTION_HISTORY.md`.

---

## 6. Git / GitHub / Phase 类报告实际归属

| Kind | Existing directory | Instances |
|------|--------------------|-----------|
| GitHub sync Phase 1/2/3 reports | **None** | **No existing instance found.** |
| Dedicated git/sync/infra audit folder | **None** | Not in README taxonomy |
| Mentions of `.gitignore` / git status inside audits | Occasional (e.g. `asset/` scans) | Not a placement rule |
| “Phase 1/2/3” wording in validation | Often means **governance recovery reading phases**, not GitHub sync | Do not confuse |

---

## 7. 关键已有报告列表（按目录）

### Root — Entry / capability audits

| File | Type (from title/header) |
|------|--------------------------|
| `ENTRY_066_CORE_WORK_PRINCIPLES_AND_FIRST_REAL_XIANYU_OBSERVATION.md` | Entry audit |
| `ENTRY_067_ACQUISITION_POLICY_AND_AI_COST_GATE.md` | Entry audit |
| `ENTRY_068_FIRST_REAL_XIANYU_OBSERVATION_AND_FILTER.md` | Entry audit |
| `ENTRY_069A_XIANYU_EXTENSION_LIVE_SEARCH_RESULT_VERIFICATION.md` | Entry audit / verification |
| `ENTRY_069B_XIANYU_HUMAN_VERIFIED_MARKET_OBSERVATION_IMPORT.md` | Entry audit |
| `ENTRY_070_XIANYU_REAL_OBSERVATION_FILTER_CANDIDATE_SET.md` | Entry audit |
| `ENTRY_071_XIANYU_REAL_CANDIDATE_TO_SIGNAL_TO_OPPORTUNITY.md` | Entry audit |
| `ENTRY_072_CANDIDATE_SIGNAL_AI_INVOCATION_REALITY_PREFLIGHT.md` | Entry preflight audit |
| `ENTRY_073_REAL_CANDIDATE_TO_SIGNAL.md` | Entry audit |
| `ENTRY_074_REAL_SIGNAL_TO_OPPORTUNITY.md` | Entry audit |
| `ENTRY_075_REAL_OBSERVATION_NATIVE_OPPORTUNITY.md` | Entry audit |
| `ENTRY_076_OPPORTUNITY_TO_PRODUCT.md` | Entry audit (PASS_WITH_FINDINGS) |
| `AUTONOMOUS_MARKET_ACQUISITION_ENTRY_059.md` | Entry audit |
| `REAL_XIANYU_BROWSER_COLLECTION_ENTRY_060.md` | Entry audit |
| `REAL_XIANYU_INTERACTIVE_BROWSER_ENTRY_061.md` | Entry audit |
| `XIANYU_TARGETED_SEARCH_WANT_COUNT_ENTRY_062.md` | Entry audit |
| `XIANYU_SEARCH_SESSION_ENTRY_063.md` | Entry audit |
| `XIANYU_EXTENSION_FORENSICS_ENTRY_064.md` | Entry audit |
| `XIANYU_EXTENSION_IMPLEMENTATION_ENTRY_065.md` | Entry audit |
| `XIANYU_ACQUISITION_CAPABILITY_ENTRY_058D.md` | Entry / capability audit |
| `XIANYU_PUBLIC_WEB_FEASIBILITY_ENTRY_058E.md` | Entry / feasibility audit |
| `README.md` | Directory role / taxonomy |

### asset/

| File | Type |
|------|------|
| `AI_FACTORY_OS_ASSET_AUDIT.md` | Asset audit |
| `AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md` | Template |
| `AI_FACTORY_OS_ASSET_SCAN_REPORT.md` | Asset scan |

### commercial/

| File | Type |
|------|------|
| `7_COMMERCIAL_ASSET_REPORT.md` | Commercial asset report |
| `AI_FACTORY_OS_COMMERCIAL_FIELD_COMPATIBILITY_REPORT.md` | Commercial field |
| `AI_FACTORY_OS_COMMERCIAL_FIELD_CURRENT_INVENTORY.md` | Inventory |
| `AI_FACTORY_OS_COMMERCIAL_FIELD_MAPPING_MODEL.md` | Mapping model |
| `AI_FACTORY_OS_COMMERCIAL_OBJECT_INVENTORY.md` | Inventory |
| `AI_FACTORY_OS_COMMERCIAL_STATE_ALIGNMENT_REPORT.md` | State alignment |
| `AI_FACTORY_OS_COMMERCIAL_STATE_CONFLICT_REPORT.md` | Conflict |
| `AI_FACTORY_OS_PILOT_STATE_MIGRATION_ANALYSIS.md` | Pilot migration analysis |

### database/

| File | Type |
|------|------|
| `AI_FACTORY_OS_DATABASE_ALIGNMENT_REPORT.md` | DB alignment |
| `AI_FACTORY_OS_DATABASE_INVENTORY_REPORT.md` | Inventory |
| `AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md` | Reality audit |
| `AI_FACTORY_OS_JSON_DATABASE_BOUNDARY_REPORT.md` | Boundary |
| `AI_FACTORY_OS_SCHEMA_DRIFT_REPORT.md` | Schema drift |
| `DATABASE_PROVENANCE_AUDIT_ENTRY_058A.md` | Entry 058A (domain-placed) |
| `REAL_XIANYU_IMPORT_PILOT_ENTRY_058C.md` | Entry 058C |
| `SOURCE_TO_SALES_DATA_BOUNDARY_ENTRY_058B.md` | Entry 058B |

### migration/

| File | Type |
|------|------|
| `AI_FACTORY_OS_DOCUMENT_STRUCTURE_MIGRATION_*.md` | Migration plan/execution |
| `AI_FACTORY_OS_STATE_MIGRATION_RISK_REPORT.md` | Migration risk |
| `ENTRY_044_A/B_…` | Doc governance / consolidation |
| `ENTRY_045_A_…` | Minimal core consolidation |
| `ENTRY_055_E2E_PRODUCT_GENERATION_PILOT_REPORT.md` | Entry 055 pilot |
| `ENTRY_056_HUMAN_PUBLISH_PACK_REPORT.md` | Entry 056 |
| `ENTRY_057_PRICE_INTELLIGENCE_REPORT.md` | Entry 057 |

### runtime/

| File | Type |
|------|------|
| `1_AI_FACTORY_OS_MODULE_AUDIT.md` … `10_KNOWN_ISSUES.md` | Numbered runtime series |
| `AI_FACTORY_OS_BROKEN_ENTRY_REPORT.md` | Broken entry |
| `AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md` | CF architecture |
| `AI_FACTORY_OS_REALITY_*` | Reality alignment |

### structure/

| File | Type |
|------|------|
| `8_DOCUMENT_CONFLICT_REPORT.md` | Conflict |
| `AI_FACTORY_OS_*CONSOLIDATION/VALIDATION/MAP*.md` | Structure/knowledge |
| `cleanup_candidates.md` | Cleanup list |
| Many `ENTRY_044_D`…`ENTRY_044_R`… | Doc role / integrity / audit separation |

### validation/

| File | Type |
|------|------|
| Many `AI_FACTORY_OS_*_VALIDATION_REPORT.md` | Validation / acceptance |
| `ENTRY_044_S/T/U_…` | Final stability / freeze validation |
| Session recovery acceptance/validation | Recovery validation |

---

## 8. 报告归属矩阵

| 报告类型 | 应放目录 | 判断依据 | 现有实例 |
|----------|----------|----------|----------|
| Entry 审计报告（近期能力链） | **`docs/07_AUDIT/` root** | ENTRY_066–076 Reality | `ENTRY_076_OPPORTUNITY_TO_PRODUCT.md` 等 |
| Entry 审计（主题域） | thematic subdir when historically used | 058*/044*/055 in domain folders | `database/*ENTRY_058*`, `migration/ENTRY_055_*` |
| Cursor 执行台账 | **`docs/05_EXECUTION/`**（非 07） | Execution directory role | `CURSOR_EXECUTION_HISTORY.md` |
| Cursor 单次执行细节审计 | usually Entry audit at 07 root | linked from History | Entry 076 audit |
| Git/GitHub 同步报告 | **No dedicated dir** | README taxonomy has none | **No existing instance found.** |
| Phase 审查报告（GitHub sync） | **No dedicated dir** | “Phase” in validation ≠ Git sync | **No existing instance found.** |
| Verification 报告 | often root Entry `*VERIFICATION*` or `validation/` | mixed | `ENTRY_069A_*VERIFICATION*`; many `validation/*` |
| Governance 相关报告 | historically `structure/` / `validation/`; ledger in `00_GOVERNANCE` | 044 series | `structure/ENTRY_044_*`, `validation/*GOVERNANCE*` |
| Recovery / 迁移报告 | `migration/` + `validation/*RECOVERY*` | names + content | migration docs; recovery validation reports |

---

## 9. Phase 1 / 2 / 3 推荐落盘位置

**Recommendation (Reality-constrained, no new subdirectory invented):**

| Phase | Recommended directory | Why |
|-------|----------------------|-----|
| **Phase 1** (Git install / init / gitignore / remote / candidate scan / READY_FOR_FIRST_COMMIT) | **`docs/07_AUDIT/` root** | Same landing zone as temporary probe instruction; no git/sync category in README; not an Entry 077 audit; root already hosts operational verification audits |
| **Phase 2** (`.cursor` / `7_MEMORY` / commit boundary / branch) | **`docs/07_AUDIT/` root** | Same series as Phase 1; keep trio co-located; not `structure/` unless later reclassified as doc-structure audit |
| **Phase 3** (first commit / push / GitHub Reality) | **`docs/07_AUDIT/` root** | Completes the sync series; still no dedicated sync folder |

**Why not split across `validation/` vs `structure/`:** no prior GitHub-sync instance; splitting would invent a finer rule than README provides.  
**Why not `05_EXECUTION`:** that path holds the **ledger** (`CURSOR_EXECUTION_HISTORY`); Phase reports are audit artifacts akin to `07_AUDIT` verification write-ups. History may *link* to them after authorization.  
**Why not create `07_AUDIT/github/` now:** forbidden without explicit authorization; README does not list it.

**Alternative (only if later authorized):** introduce a README taxonomy entry such as `infrastructure` / `sync` — **not done in this probe**.

---

## 10. 推荐文件命名（遵循已有风格，不新造体系）

Observed patterns:

* `ENTRY_NNN_TOPIC.md` — numbered Entry audits (root)
* `TOPIC_ENTRY_NNN.md` — older root naming
* `AI_FACTORY_OS_*_VALIDATION_REPORT.md` — validation/
* `AI_FACTORY_OS_*_AUDIT.md` — thematic audits
* This probe: `GITHUB_SYNC_*` prefix already used

**Suggested names (same series prefix as this probe):**

| Phase | Suggested filename |
|-------|--------------------|
| Phase 1 | `GITHUB_SYNC_PHASE_1_GIT_FOUNDATION_REPORT.md` |
| Phase 2 | `GITHUB_SYNC_PHASE_2_COMMIT_BOUNDARY_REVIEW.md` |
| Phase 3 | `GITHUB_SYNC_PHASE_3_FIRST_COMMIT_PUSH_REPORT.md` |

Do **not** invent `ENTRY_077_*` for sync work unless an Entry 077 is formally authorized.

---

## 11. 未确定事项

1. Whether GitHub sync reports should later move into a **new** README category (requires governance authorization).  
2. Whether Phase reports should also get a short pointer row in `CURSOR_EXECUTION_HISTORY.md` (Execution ledger sync — separate decision).  
3. Final archival location of **this** temporary probe file (explicitly deferred).  
4. Whether Phase 2’s boundary content is closer to `structure/` than root (possible later reclassification only).

---

## 12. 本次执行边界 / STOP

```text
READ-ONLY COMPLETE
```

* Probe report path: `docs/07_AUDIT/GITHUB_SYNC_AUDIT_DIRECTORY_STRUCTURE_PROBE.md`
* No Phase 1 / Phase 2 / Phase 3 execution
* No git write operations
* No new 07_AUDIT subdirectories created
* This report not moved

---

## STOP
