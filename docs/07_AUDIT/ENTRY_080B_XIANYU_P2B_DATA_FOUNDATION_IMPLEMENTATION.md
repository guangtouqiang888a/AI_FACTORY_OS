# ENTRY 080-B — Xianyu P2-B Data Foundation Minimal Implementation

**Date:** 2026-09-05  
**Entry ID:** **080-B**  
**Project:** Xianyu Commercial Closed-Loop Project  
**Result:** `PASS_WITH_FINDINGS`  
**AI Cost:** **¥0**  
**DB Impact:** **ADDITIVE MIGRATION + BACKFILL**（no destructive reset）  
**Runtime Impact:** **LIMITED** — `market_source_core.insert/finish` + new `data_foundation_080b`；**Extension unchanged**；**no view collection**

> Cursor Process Output ≠ Formal Audit ≠ Current State ≠ ChatGPT Closure Review.  
> P3 / P4 / Adaptive Engine / Keyword Planner / view capture = **NOT STARTED**.

---

## Original Objective

跑通闲鱼真实商业闭环（市场→采集→数据基础→…→学习）。

## Current Objective

根据 Entry **080-A**，建立 **P2 Data Foundation 最小可靠结构**：Observation / Keyword / Collection Run / Provenance / Product Identity / 跨时间 dedupe 语义 — **不**扩到 P3/P4。

## Scope

- Additive SQLite schema + safe backfill  
- `1_DATA/data_foundation_080b.py`  
- `market_source_core` insert/finish 兼容  
- 自动化测试  
- Continuity docs + Git  

## Out of Scope

Extension parser；view 采集/详情页；AI Keyword Planner；Keyword Discovery；Adaptive Decision Engine；scorer/threshold/pricing；Product Definition/Asset；publish；反馈/收入；P3/P4；删除 20 REAL obs；删除 `a949d2e47cf1`；付费 AI。

## Reality Before

| Metric | Value |
|--------|------:|
| market_observations | 20 |
| REAL / MANUAL_VERIFIED | 20 / 20 |
| want NULL / zero | 6 / 0 |
| view NULL | 20 |
| keywords rows | 0 |
| query as first-class obs column | No |
| product identity table | Absent |
| VIEW_COUNT_STATUS | NOT_STABLELY_AVAILABLE |

## Design Decision

| Topic | Decision |
|-------|----------|
| Schema style | **Additive only**（ALTER / CREATE IF NOT EXISTS） |
| Query linkage | First-class `collection_query` + `keyword_id` on observations；reuse `keywords` table |
| Image / position | Elevate to first-class（commercial UX / ranking later）from raw provenance |
| Product identity | New `market_product_identities`；**≠** Product Asset `a949` / Product Definition |
| Evidence | Minimal `evidence_level` mapped from `data_origin`；never promote SAMPLE/TEST→REAL |
| View | Column retained；**NULL stays NULL**；no collection |
| Want | **NULL ≠ 0** preserved |
| Adaptive depth | Metadata columns only；**engine NOT implemented** |
| Extension | **Unchanged** |

## Schema Changes

### `market_observations` (+additive)

`collection_query`, `keyword_id`, `want_count_status`, `image_url`, `result_position`, `product_identity_id`, `evidence_level`

### `keywords` (+additive)

`keyword_uid`, `canonical_keyword`, `platform`, `keyword_source`, `keyword_type`, `discovery_class`, `evidence_status`, `created_at`, `updated_at`

### `collection_runs` (+additive)

`keyword_id`, `requested_record_count`, `requested_depth`, `actual_depth`, `stop_reason`, `newly_accepted_count`

### New table

`market_product_identities` — stable marketplace item identity across observation timestamps.

## Migration

1. Backup → `99_ARCHIVE/database_history/ai_factory_pre_080b_20260905_155811.db`  
2. `ensure_data_foundation_schema()` / `apply_additive_schema_only()`  
3. `backfill_existing_observations()` from notes + `payload.records` raw batch  
4. Integrity snapshot before/after  

**Finding during migration：** initial raw loader looked at top-level `records`；actual file nests under `payload.records`. Fixed loader；re-backfill filled image/position without touching want/view.

## Data Preservation Verification

| Check | Before | After |
|-------|-------:|------:|
| row_count | 20 | **20** |
| REAL | 20 | **20** |
| MANUAL_VERIFIED | 20 | **20** |
| want NULL | 6 | **6** |
| want zero | 0 | **0** |
| view NULL | 20 | **20** |
| view non-null | 0 | **0** |
| distinct item / url | 20 / 20 | **20 / 20** |
| keywords | 0 | **1**（Excel模板） |
| product identities | 0 | **20** |
| obs with query / keyword_id / product_identity | — | **20 / 20 / 20** |
| image_url / result_position non-null | — | **20 / 20** |
| preservation_ok | — | **true** |

## Tests

| Suite | Result |
|-------|--------|
| `1_DATA.test_data_foundation_080b`（7） | **OK** |
| `1_DATA.test_market_source_058b`（15） regression | **OK** |

Coverage: schema；NULL want/view；keyword upsert/dedupe；run↔obs↔keyword；product identity across timestamps + same-timestamp duplicate；evidence mapping；backfill preservation.

## AI Cost

**¥0**

## Runtime Impact

- **Changed:** `1_DATA/data_foundation_080b.py`（new）；`1_DATA/market_source_core.py`（insert/finish + ensure hook）  
- **Unchanged:** Extension JS；scorer；pricing；publish；a949  

## DB Impact

Additive schema + non-destructive backfill of linkage/provenance fields only.

## Findings

1. Minimal foundation is sufficient for P2 goals without rewriting DB stack.  
2. Raw batch nesting (`payload.records`) must be part of importer knowledge — fixed in foundation loader.  
3. `collection_log` stale rows remain（hygiene deferred；not required for P2-B）。  
4. view still **NOT_STABLELY_AVAILABLE**.  
5. Keyword foundation ≠ discovery（P3）。

## Remaining Risks

- Class-name / DOM drift on future collections（Extension still sole live parser）.  
- Dual legacy `products`/`collection_log` vs market_* continuum.  
- evidence_level is derived mapping — not a full evidence graph.

## P2 Remaining Work（optional later Entries）

- collection_log hygiene  
- Formal Observation Field Contract doc-only polish  
- Analytics guards that refuse view=0 fake engagement  

## P3 / P4 explicitly NOT STARTED

AI Query Planner · Keyword Discovery · Adaptive Collection Decision · depth engine — **NOT STARTED**.

## Evidence

- `1_DATA/data_foundation_080b.py`  
- `1_DATA/test_data_foundation_080b.py`  
- `1_DATA/_tests/xianyu_entry_080b/migration_result.json`  
- Backup DB under `99_ARCHIVE/database_history/`  
- Entry 080-A Audit  

## Decisions

- P2-B = minimal implemented foundation.  
- P2 overall = **PARTIAL**（foundation yes；view/collection-depth engines no）.  

## Pending

ChatGPT Closure Review；optional P2-C hygiene；**do not auto-start P3**.

## Next Step

**STOP** — 等待 Closure Review。

## Git Commit / Push / Remote Verification

| Field | Value |
|-------|-------|
| Git Commit | （closeout） |
| GitHub Push | （closeout） |
| Remote Verification | （closeout） |
