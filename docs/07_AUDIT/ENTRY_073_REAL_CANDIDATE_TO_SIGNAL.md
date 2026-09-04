# ENTRY_073_REAL_CANDIDATE_TO_SIGNAL

**ENTRY STATUS:** **PASS_WITH_FINDINGS**  
**ENTRY ID:** 073  
**DATE:** 2026-09-03  
**TYPE:** Authorized Runtime Implementation — REAL Candidate → Signal  
**Code Modification:** **YES** — `1_DATA/market_signal_core.py` (+ tests)  
**Schema Modification:** **NONE**  
**DB Modification:** **YES** — `market_signals` only (0 → 6)  
**External Action:** **NONE**  
**AI provider calls:** **0**  
**AI cost:** **0**  
**Opportunity:** **NOT_EXECUTED**  
**Commercial Learning:** **NOT_EXECUTED**

---

## LOCKED CANDIDATES

| observation_id | want_count | data_origin | verification_status | filter_status |
|----------------|------------|-------------|---------------------|---------------|
| mobs_48d5a1daa0ee | 1082 | REAL | MANUAL_VERIFIED | MATCH |
| mobs_4eeed83520dc | 2245 | REAL | MANUAL_VERIFIED | MATCH |
| mobs_77abed5da432 | 660 | REAL | MANUAL_VERIFIED | MATCH |
| mobs_558206dd2057 | 1930 | REAL | MANUAL_VERIFIED | MATCH |
| mobs_2198f9db4742 | 436 | REAL | MANUAL_VERIFIED | MATCH |
| mobs_217cd4886838 | 186 | REAL | MANUAL_VERIFIED | MATCH |
| mobs_a28b1bc7faca | 642 | REAL | MANUAL_VERIFIED | MATCH |

Session / Collection / Extension: `sess_1788419997563` / `crun_378745ca45e0` / `run_1788419997563`  
All 7 validated before Signal — **STOP condition not triggered**.

---

## PRE-EXECUTION REALITY

| Table | Count |
|-------|------:|
| market_observations | 20 |
| market_signals | 0 |
| selection_results | 0 |
| products | 0 |

Signal Runtime: `derive_signals_from_product_group` (054) existed; Candidate path missing (072).

---

## SIGNAL INPUT MAPPING

| Signal field | Observation source |
|--------------|-------------------|
| keyword | `notes.query` (e.g. `Excel模板`) — no invent |
| want_count | `want_count` (**NULL preserved**; not coerced to 0) |
| price | `price` |
| view_count | `view_count` (NULL preserved) |
| comment_count / share_count | columns (NULL preserved) |
| source_url / source_item_id | columns |
| platform | `platform` |
| collect_date / obs ts | `observed_at` |

**PRODUCT SUBSTITUTION = NO** — no `products` INSERT; `evidence_refs.product_ids = []`; `source = market_observation`.

---

## SIGNAL CORE PATH

```text
Filter Candidate (MATCH + REAL + MANUAL_VERIFIED)
  → load market_observations (authoritative metrics)
  → observation_to_listing_input / resolve keyword
  → group by keyword
  → _compute_deterministic_signals (shared with product path; null_as_zero=False)
  → persist_signals → market_signals
```

Formal entry: `derive_signals_from_observation_candidates`  
Shared calc: `_compute_deterministic_signals`  
Product path unchanged contract: `null_as_zero=True` (054).

---

## AI PROVIDER CALLS = 0 / AI COST = 0

No ExecutionRuntime / ModelBridge / OpenAI / DeepSeek on this path.

---

## PROVENANCE

Stored in existing `evidence_refs` JSON (schema unchanged):

- lineage = `market_observation`
- observation_ids, source_item_ids, collection_run_ids, session_ids, extension_run_ids
- data_origins, verification_statuses, observed_ats
- null_want_count_observation_ids
- product_ids = []

**PROVENANCE = SUFFICIENT** via `evidence_refs` (no SCHEMA_CAPABILITY_GAP).

---

## SIGNAL COUNT / MAPPING

| Metric | Value |
|--------|------:|
| candidate_count | 7 |
| keyword_groups | Excel模板 → 7 |
| signal_count | **6** |
| skipped | 0 |

Signal IDs:

```text
sig_f1173cc0edca  demand_signal      value=7181 (want_count_sum)
sig_9a3983efb2a4  engagement_signal  value=0.0 (no known views)
sig_10fa1228c3f2  competition_signal value=7
sig_82a523bc2bc1  price_signal       value=1.0
sig_90277d017e37  trend_signal       value≈1025.86 (avg_want)
sig_90064dc020a6  growth_signal      UNAVAILABLE
```

All 7 Candidates map to the **same** 6 signal IDs (keyword-group aggregation — existing Signal contract).

Evidence: `1_DATA/_tests/xianyu_entry_073/candidate_to_signal_result.json`

---

## DATABASE BEFORE/AFTER

| Table | Before | After | Delta |
|-------|-------:|------:|------:|
| market_observations | 20 | 20 | **0** |
| products | 0 | 0 | **0** |
| selection_results | 0 | 0 | **0** |
| market_signals | 0 | 6 | **+6** |

---

## DUPLICATION / IDEMPOTENCY

`persist_signals` uses `INSERT OR REPLACE` on **signal_id UNIQUE**.  
signal_id = new UUID each derivation → **re-run creates additional rows** (no natural Observation-keyed identity).

**FINDING: IDEMPOTENCY_GAP** — documented; out of scope to redesign persistence.

---

## TEST RESULTS

```text
tests_run: 20  (7 × test_candidate_to_signal_073 + 13 × test_opportunity_discovery)
passed: 20
failed: 0
skipped: 0
```

Coverage: REAL Candidate input; provenance; NULL≠0; no product write; deterministic values; no AI markers; reject non-MATCH/unverified.

---

## CODE / SCHEMA / DB MODIFICATIONS

| Area | Detail |
|------|--------|
| Code | `1_DATA/market_signal_core.py` — Observation-native path + shared deterministic core |
| Tests | `1_DATA/test_candidate_to_signal_073.py` (new) |
| Schema | **NONE** |
| DB | market_signals +6 only |

---

## CAPABILITY GAPS

1. **IDEMPOTENCY_GAP** — re-derive duplicates signals  
2. Signal → Opportunity for Observation lineage — **NOT_EXECUTED** (next auth)  
3. Model Router / AI Cost Gate / Governor — unchanged (072); out of scope  

---

## NEXT AUTHORIZATION

Separate Entry required for:

```text
Signal (Observation lineage) → Opportunity discovery
```

**STOP** — no Opportunity / Product / Publish / Commercial Learning / AI.

---

## DOCUMENTATION SYNC

| File | Action | Why |
|------|--------|-----|
| This Audit | Created | SoT |
| CURRENT_STATE | Modified | Capability: Candidate→Signal IMPLEMENTED |
| MODULE_REGISTRY | Modified | Register Observation Signal path |
| CURSOR_EXECUTION_HISTORY | Modified | Ledger |
| UNIFIED_ARCHITECTURE | Reviewed — Not Modified | No DEC; Reality noted in State/Registry |
| EXECUTION_PROTOCOL | Reviewed — Not Modified | No protocol boundary change |
| Constitution / DEC / Authority / Control Center / KUP / Business Strategy / WORK_PRINCIPLES | Reviewed — Not Modified | No governance conflict |
