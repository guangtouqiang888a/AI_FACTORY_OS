# ENTRY 080-C — Xianyu P2-C Data Hygiene & NULL Semantics Guard

**Date:** 2026-09-05  
**Entry ID:** **080-C**  
**Project:** Xianyu Commercial Closed-Loop Project  
**Result:** `PASS_WITH_FINDINGS`  
**AI Cost:** **¥0**  
**DB Impact:** **MINIMAL** — corrected 1 historical `engagement_signal` misread (`0.0` → `NULL`); **20 REAL observations untouched**  
**Runtime Impact:** **LIMITED** — observation-path signal engagement/demand NULL guards in `market_signal_core.py` only  

> Cursor Process Output ≠ Formal Audit ≠ Current State ≠ ChatGPT Closure Review.  
> P3 / P4 / Extension / view collector = **NOT STARTED**.

---

## Original Objective

推进闲鱼真实商业闭环；本 Entry 仅做 P2 Data Foundation **最小卫生与误读防护**。

## Current Objective

审查 `collection_log` vs `market_*`；防止 `view_count`/`want_count` NULL→0 商业误读；强化 evidence 边界；必要时最小代码/测试；文档与 Git 收口。

## Scope

Inspection；NULL/engagement guard；evidence check；最小 signal 修正；tests；docs；Git。

## Out of Scope

Extension；view 采集；Planner/Discovery；Adaptive；scorer/threshold/pricing；PD/Asset/publish；删 obs/audit；强迁 collection_log；P3/P4；付费 AI。

## Reality Before

| Metric | Value |
|--------|------:|
| market_observations | 20 |
| REAL / MANUAL_VERIFIED | 20 / 20 |
| want NULL / zero | 6 / 0 |
| view NULL / non-null | 20 / 0 |
| keywords / product_identities | 1 / 20 |
| collection_log | 14（全部 `running`，totals=0） |
| engagement_signal | **value=0.0**（误读：全 NULL view） |
| a949 | present |

## Reality After

| Metric | Value |
|--------|------:|
| observations / REAL / verified | **20 / 20 / 20** |
| want NULL / zero | **6 / 0** |
| view NULL / non-null | **20 / 0** |
| keywords / identities | **1 / 20** |
| collection_log | **14 KEEP**（未删） |
| engagement_signal `sig_9a3983efb2a4` | **value=NULL**（UNAVAILABLE 语义） |
| selection_results / a949 | **unchanged** |

## collection_log findings

| Question | Answer |
|----------|--------|
| Rows | 14 |
| Overlap with `collection_runs` | Dual-write：`start_collection_run` → `start_collection_log`；**finish_collection_log never called** → stale `running` |
| Commercial dependency | **No**（分析用 `collection_runs` / observations） |
| Runtime dependency | **Yes** — `market_source_core.start_collection_run` still inserts |
| Test dependency | Indirect via schema |
| Historical evidence | Yes（timestamps / keywords） |
| Safe to delete? | **No**（Runtime still starts rows； provenance） |

**Decision：** **KEEP**（不物理删除；不强制迁移）  
**Future：** optional DELETE_CANDIDATE hygiene Entry after wiring finish or deprecating dual-write — **not this Entry**.

## NULL semantics findings

| Risk | Location | Action |
|------|----------|--------|
| Observation engagement `total_view==0` → **0.0** | `market_signal_core._compute_deterministic_signals` | **FIXED** → UNAVAILABLE / NULL |
| All-NULL want → demand/avg_want **0.0** | same | **FIXED** → UNAVAILABLE |
| Product path null_as_zero→0 | 054 contract | **KEEP**（legacy product；非 observation） |
| Scorer `view_contrib=0.0` when null | `3_DECISION/scorer.py` | **NO CHANGE**（禁止改 selection scorer；Finding only） |
| Stats `or 0` on run counts | insert/finish stats | Technical counters — **NO CHANGE** |

## Evidence guard findings

| Check | Status |
|-------|--------|
| Candidate→Signal requires REAL + MANUAL_VERIFIED | Already present（073） |
| SAMPLE/UNKNOWN rejected | Confirmed by test |
| HYPOTHESIS≠FACT at analysis entry | Guarded via origin/verification |
| Stored engagement 0.0 misread | Corrected |

## Code changes

1. `1_DATA/market_signal_core.py` — observation-path NULL engagement/demand/avg_want；`null_view` evidence；`collection_query` keyword resolve  
2. `1_DATA/test_data_hygiene_080c.py` — new tests  
3. `1_DATA/_tests/xianyu_entry_080c/correct_engagement_misread.py` — one-shot historical signal correction  

**Not changed：** Extension；scorer thresholds；pricing；a949；observations rows；collection_log rows.

## Tests

| Suite | Result |
|-------|--------|
| `test_data_hygiene_080c`（6） | **OK** |
| `test_candidate_to_signal_073`（7） | **OK** |

## Database impact

- Observations：**no row mutation**  
- Signals：1 engagement row corrected  
- collection_log：**unchanged**  

## Runtime impact

Future observation-native signal derivation：NULL views ≠ 0 engagement.

## Product/Asset impact

**NONE** — `a949d2e47cf1` preserved；PD/publish untouched.

## AI Cost

**¥0**

## Findings

1. Primary commercial misread was engagement_signal=0.0 under all-NULL views — fixed.  
2. collection_log is stale dual-write residue — KEEP.  
3. Product-path null_as_zero remains by 054 contract (documented).  
4. Scorer still uses view_contrib=0.0 for missing view on observation score path — deferred（scorer out of scope）.

## Remaining Risks

- Historical selection_results still cite pre-correction evidence_refs text — not rewritten（avoid selection mutation）.  
- Dual collection_log continues to accumulate stale rows until finish is wired or dual-write removed（future Entry）.

## Decisions

- Code Change = **YES（minimal）**  
- collection_log = **KEEP**  
- P2 overall = **COMPLETED_WITH_FINDINGS**（foundation + hygiene；view still NOT_STABLELY_AVAILABLE by Reality）  

## Pending

ChatGPT Closure Review；optional collection_log finish wiring Entry；**do not auto-start P3**.

## Next Step

**STOP.**

## Stop Conditions

Violated if Extension/view collector/P3 started or REAL obs deleted.

## Git Commit / Push / Remote Verification

| Field | Value |
|-------|-------|
| Git Commit | （closeout） |
| GitHub Push | （closeout） |
| Remote Verification | （closeout） |

## Final Status

**P2-C DONE** · **P2 COMPLETED_WITH_FINDINGS** · P3/P4 **NOT STARTED**
