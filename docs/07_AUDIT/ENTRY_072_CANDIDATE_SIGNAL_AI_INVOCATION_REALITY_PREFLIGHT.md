# ENTRY_072_CANDIDATE_SIGNAL_AI_INVOCATION_REALITY_PREFLIGHT

**ENTRY STATUS:** **PASS_WITH_FINDINGS**  
**ENTRY ID:** 072  
**DATE:** 2026-09-03  
**TYPE:** Read-Only Reality Preflight — Candidate → Signal + AI Invocation  
**Code Modification:** **NONE**  
**Schema Modification:** **NONE**  
**DB Modification:** **NONE**  
**External Action:** **NONE**  
**AI provider calls:** **0**  
**AI cost:** **0**

---

## REALITY SNAPSHOT

| Item | Value |
|------|--------|
| DB | `D:\AI_FACTORY_OS\data\ai_factory.db` |
| market_observations | **20** (unchanged) |
| 070 MATCH Candidate | **7** locked IDs match |
| data_origin / verification | REAL / MANUAL_VERIFIED (all 7) |
| Session / Collection | `sess_1788419997563` / `crun_378745ca45e0` |
| products | **0** |
| market_signals | **0** |
| selection_results | **0** |

Locked Candidate IDs (070):

`mobs_48d5a1daa0ee`, `mobs_4eeed83520dc`, `mobs_77abed5da432`, `mobs_558206dd2057`, `mobs_2198f9db4742`, `mobs_217cd4886838`, `mobs_a28b1bc7faca`

---

## SIGNAL RUNTIME

| Field | Reality |
|-------|---------|
| module | `1_DATA/market_signal_core.py` |
| function | `derive_signals_from_product_group(keyword, products, …)` |
| persistence | `persist_signals(signals)` → SQLite `market_signals` |
| caller | `3_DECISION/opportunity_discovery.py` (`discover_opportunities`, helpers); tests; price_intelligence refs |
| input type | **Product list / keyword group** (dicts with want_count, price, view_count, … from `products` table via `load_products_grouped_by_keyword`) |
| output type | list of signal dicts (`demand_signal`, `engagement_signal`, `competition_signal`, `price_signal`, `trend_signal`, `growth_signal`) |
| AI inside Signal | **NONE** — no OpenAI/DeepSeek/requests in `market_signal_core.py` |

### A2 Input taxonomy (code-evidence)

| Input | Accepted by current Signal Runtime? |
|-------|-------------------------------------|
| Product / Product Group | **YES** (official) |
| Keyword Group from `products` | **YES** |
| MarketObservation | **NO** dedicated API |
| Filter Candidate | **NO** dedicated API |

### A4 Missing APIs (searched)

`derive_signals_from_observations` / `derive_signals_from_candidates` / `observation_to_signal` / `candidate_to_signal` — **NOT_FOUND** in Runtime code under `0_START`/`1_DATA`/`3_DECISION`/`6_EXECUTION`/`10_DEPLOY`/`11_CONTENT_FACTORY`.

### CANDIDATE → SIGNAL STATUS

**NOT_IMPLEMENTED**

Evidence: only product-group entry exists; 071 gap confirmed; no Observation/Candidate bridge.

---

## EXECUTIONRUNTIME STATUS

| Field | Reality |
|-------|---------|
| file | `0_START/execution_runtime.py` |
| class | `ExecutionRuntime` |
| callers | `0_START/controller.py` (`SystemController`); Deploy forbids direct import bypass |
| used by Track A | **YES** — Controller DAG path |
| ModelBridge | Instantiated with caller=`ExecutionRuntime` |
| deterministic default | `config.DETERMINISTIC_MODE = True` → forces **rule** executor |
| tests proving live model call | **NONE found** (no dedicated execution/model bridge test suite located) |

**Classification:** **IMPLEMENTED_AND_USED** (Track A Controller path; typically rule-forced under deterministic mode)

---

## MODEL ROUTER STATUS

| Field | Reality |
|-------|---------|
| Class `ModelRouter` / `model_router.py` | **NOT_FOUND** |
| Closest Reality | `PolicyEngine.evaluate_node` + `config.LLM_ROUTING` (`simple→rule`, `medium→deepseek`, `complex→gpt`) |
| `ai_cost_gate.ModelSelector` | Interface only; returns `router_status: NOT_BUILT` |
| `acquisition_engine` | Explicit `model_router: PROPOSED_NOT_BUILT` |
| Wired to Signal | **NO** |

**MODEL_ROUTER_REALITY = NOT_IMPLEMENTED** (routing table exists inside PolicyEngine; no dedicated Model Router / cost-aware auto selection)

**Classification:** **NOT_IMPLEMENTED** as named Model Router; **PARTIAL** as static LLM_ROUTING in PolicyEngine

---

## MODELBRIDGE STATUS

| Field | Reality |
|-------|---------|
| file | `0_START/model_bridge.py` |
| class | `ModelBridge` |
| lock | Only callable when `caller == "ExecutionRuntime"` |
| DeepSeek entry | `call_deepseek` → `DEEPSEEK_BASE_URL` + `/chat/completions` via `requests.post` |
| OpenAI entry | `call_gpt` → `https://api.openai.com/v1/chat/completions` |
| env vars (names only) | `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`, `OPENAI_API_KEY`, `OPENAI_MODEL` |
| used by | `ExecutionRuntime._run_llm` only |
| CF `llm_adapter` | Raises reserved — not a live bridge |

**Classification:** **IMPLEMENTED_AND_USED** (by ExecutionRuntime when non-rule executor; Entry 072 did **not** invoke)

---

## AI COST GATE STATUS

| Field | Reality |
|-------|---------|
| file | `1_DATA/ai_cost_gate.py` (067) |
| estimated_cost / actual_cost / allowed_cost | **YES** — `evaluate_cost_gate`, `record_ai_cost_estimate`, `record_ai_execution` |
| PASS / BLOCKED / UNKNOWN / REDESIGN_REQUIRED | **YES** |
| call_count | Metadata only — not primary control |
| ModelSelector | Manual/configured; Router NOT_BUILT |
| Called by ExecutionRuntime / ModelBridge / Signal? | **NO** — only `test_acquisition_policy_067` imports |
| Parallel Track A cost | `PolicyEngine.check_budget` / `consume_cost` using `LLM_COST_ESTIMATE` session ceiling — **separate** from `ai_cost_gate` |

**Classification:** **IMPLEMENTED_BUT_UNUSED** by Track A AI invocation path (unit-tested; not wired before ModelBridge)

---

## RULE-FIRST STATUS

| Field | Reality |
|-------|---------|
| Track A | `DETERMINISTIC_MODE=True` forces rule; `PolicyEngine` prefers rule for DataAgent/ExecutionAgent; budget fail → rule fallback |
| Signal Runtime | Pure deterministic aggregation — **no AI path** |
| Candidate → Signal rule-first entry for Observation lineage | **NOT_IMPLEMENTED** (no Candidate→Signal entry at all) |

**Classification:** **IMPLEMENTED_AND_USED** for Track A DAG / Signal product aggregation; **NOT_IMPLEMENTED** as a Candidate→Signal-specific rule entry

---

## GOVERNOR / PLANNER / SELF-EVOLUTION

| Component | Reality | Class |
|-----------|---------|-------|
| Governor | **No class/file named Governor** | **NOT IMPLEMENTED** |
| Router (Model) | No ModelRouter; PolicyEngine LLM_ROUTING only | **PARTIAL** / DESIGN+static config |
| Planner | `0_START/planner.py` `Planner.plan` → DAG | **REAL IMPLEMENTATION** |
| SelfEvolution | `0_START/self_evolution.py` `SelfEvolutionEngine` via Controller | **REAL IMPLEMENTATION** (execution-strategy domain; commercial_learning=False per 050) |
| PolicyEngine | `0_START/policy_engine.py` | **REAL IMPLEMENTATION** |

Actual Track A chain (code):

```text
SystemController
  → Planner
  → PolicyEngine
  → ExecutionRuntime (+ optional ModelBridge)
  → Memory
(+ SelfEvolutionEngine on Controller — not “Governor→Router→SelfEvolution→Planner”)
```

Documented Governor→Router→SelfEvolution→Planner cascade: **DESIGN ONLY / NOT Runtime as named**.

---

## SIGNAL → AI RELATIONSHIP

```text
Signal deterministic logic: YES
Signal → ExecutionRuntime: NO
Signal → ModelRouter: NO
Signal → ModelBridge: NO
Signal → direct provider: NO
```

**FINDING:** none for DIRECT_PROVIDER_CALL inside Signal.  
Provider calls exist only under `ModelBridge` when ExecutionRuntime chooses non-rule executor.

---

## PROVENANCE STATUS (future Candidate→Signal)

Current Signal evidence shape uses `product_ids`, `listing_count`, `collect_dates` — **not** Observation provenance fields.

| Field on 070 Candidate | Present on Observation | Consumed by current Signal API |
|------------------------|------------------------|--------------------------------|
| observation_id | YES | NO |
| source_item_id | YES | via product id/url if mapped — **no official map** |
| collection_run_id | YES (`run_id`=crun_*) | NO |
| session_id | YES (notes) | NO |
| extension_run_id | YES (070 evidence) | NO |
| data_origin | YES | NO |
| verification_status | YES | NO |

**PROVENANCE:** **PROVENANCE_PARTIAL** on Observation side; **PROVENANCE_MISSING** in Signal Runtime contract for Observation lineage.

Minimal fields existing Signal product-group path actually uses: keyword, listing dicts with want_count/price/view_count/comment_count/share_count/source_url/id/platform/collect_date.

---

## DATABASE BEFORE/AFTER

| Table | Before | After | Delta |
|-------|--------|-------|-------|
| market_observations | 20 | 20 | **0** |
| market_signals | 0 | 0 | **0** |
| selection_results | 0 | 0 | **0** |
| products | 0 | 0 | **0** |

---

## TEST RESULTS

| Suite | Result |
|-------|--------|
| `1_DATA.test_acquisition_policy_067` | included in 37 OK |
| `3_DECISION.test_opportunity_discovery` | included in 37 OK |
| ExecutionRuntime / ModelBridge live provider tests | **NONE / SKIPPED — REAL_PROVIDER_REQUIRED** (not run; no fake keys) |

```text
tests_run: 37
passed: 37
failed: 0
skipped: 0 (provider suites absent)
```

---

## CAPABILITY GAP

1. **Candidate → Signal bridge** — NOT_IMPLEMENTED  
2. **Model Router** (cost-aware) — NOT_IMPLEMENTED (`ModelSelector.router_status=NOT_BUILT`)  
3. **AI Cost Gate ↔ ExecutionRuntime/ModelBridge** — not wired  
4. **Governor** named component — NOT IMPLEMENTED  
5. Observation provenance → Signal evidence_refs — missing contract  

---

## NEXT REQUIRED AUTHORIZATION

Separate Entry (examples; not started):

- Implement Observation/Filter-Candidate → Signal bridge **with provenance** (no inventing products; no commercial outcome)  
- Optionally wire AI Cost Gate before ModelBridge (if AI Signal analysis ever authorized)  
- Rule-first Signal for Candidate without paid AI by default  

**STOP — do not auto-implement.**

---

## DOCUMENTATION SYNC

| File | Action | Why |
|------|--------|-----|
| This Audit | Created | Preflight SoT |
| CURRENT_STATE | Modified | Record 072 PASS_WITH_FINDINGS + gaps |
| MODULE_REGISTRY | Modified | AI/Signal Reality classifications |
| CURSOR_EXECUTION_HISTORY | Modified | Ledger |
| Constitution / DEC / Authority / Control Center / KUP / UA / Business Strategy / WORK_PRINCIPLES / Execution Protocol | Reviewed — Not Modified | No boundary change; no DOCUMENTATION_REALITY_DRIFT requiring fix |

---

## CODE / SCHEMA / DB / EXTERNAL

```text
CODE MODIFICATION = NONE
SCHEMA MODIFICATION = NONE
DB WRITE = NONE
EXTERNAL ACTION = NONE
AI PROVIDER CALLS = 0
AI COST = 0
```
