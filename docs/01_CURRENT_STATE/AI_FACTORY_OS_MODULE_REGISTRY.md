# AI_FACTORY_OS Module Registry

> Project Intelligence Layer — 模块登记表  
> Last updated: 2026-09-04（Entry **076**）

| Document Role | **模块 Status 唯一登记归属**（DEC-016）— Active / Frozen / Planned / Isolated |
|---------------|----------------------------------|
| Reality Status | Must match Runtime / Code Reality when describing *Current* state |
| Runtime Status | Requires Reality Validation — see Entry 041-A / CURRENT_STATE |

**原则：** Reality > Documentation · Blueprint ≠ Production · Design ≠ Runtime · Modular ≠ Fragmented · Unified ≠ Forced Merge · **Folder ≠ Capability ≠ Product**（DEC-018）

**Module Registry 管理：** 工程模块状态（目录/实现载体的 Active / Frozen / Planned 等）。  
**不负责定义：** 全部商业能力清单。

| Module（本表） | 不是 |
|----------------|------|
| 工程模块 Status 登记 | **Product** |
| 实现载体状态 | **Solution** |

**不是：** 商业战略正文；**不是**历史演进主文（见 Evolution Context）；**不是**目标架构唯一来源（见 UNIFIED_ARCHITECTURE）；**不是**商业能力完整目录。

**Project Intelligence 总览：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md)

**Unified Architecture：** [docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md)

**Reality baseline（041-A / 041-D）：** AI_FACTORY_OS **不是**单一 Runtime。存在 **Track A（Core OS）** 与 **Track B（Content Factory + commercial_assets）**；同仓库、不同 Runtime；**Runtime Integration = Not Started**。性质：`Intentional Isolation + Unfinished Convergence`（有意隔离 + 收敛未完成）— **不是**失败复制项目，**不是**已融合系统。

本文档为 AI Factory OS 的**模块自描述注册表**，记录各目录模块的状态、职责与架构位置。未来 AI 恢复项目上下文时，必须优先读取本文档，不得仅凭目录名称推测模块实际状态。

---

## Capability Composition Note（认知说明 — 非 DEC）

> Entry 041-D。**不新增治理决策**；不改变 DEC-013。

**Module is reusable capability, not necessarily final product.**

```
Multiple capabilities
        ↓
    Solution
        ↓
Commercial Product
```

| 禁止误解 | 正确理解 |
|----------|----------|
| Module = Product | 模块是可复用能力，可独立演进/商业化，也可以组合成解决方案与商业产品 |
| Capability Composition = 已自动闭环 | 组合是目标/设计；须 Reality Validation |
---

## System Governance Layer（系统治理层）

**Status:** Blueprint Completed

**Role:** System Governance Layer（系统治理层 — 横向治理）

**Responsibility:** Cross-module consistency governance（跨模块一致性治理）

**Protocol:** [docs/99_ARCHIVE/AI_FACTORY_OS_SYSTEM_GOVERNANCE_PROTOCOL.md](../99_ARCHIVE/AI_FACTORY_OS_SYSTEM_GOVERNANCE_PROTOCOL.md)

**Scope:**
- Documentation synchronization（文档同步）
- State governance（状态治理 — Blueprint / Design / Implementation / Runtime / Production）
- Evolution control（演化控制 — Entry Completion Governance）
- Audit protocol（ZIP Full Audit Protocol）

**Responsibilities:**
- Source of Truth 定义（Runtime / DB / commercial_assets / Memory / docs）
- Entry 完成闭环（State Review 五项检查）
- Module Boundary Protection
- User Direction Optimization Rule

**不负责:**
- 业务功能实现
- Runtime 代码修改
- Commercial Object 创造（除非 Entry 授权）

**当前状态:** Governance Protocol v1 ✅ Blueprint Completed | Governance Runtime ⏳ Not Started

**明确:** Blueprint ≠ Runtime；Governance Before Expansion。

---

## 0_START

**Status:** Active

**Role:** Core OS — Governance + Operational Runtime 编排入口

**Track:** A（Core OS Runtime）

**Responsibilities:**
- controller
- planner
- policy engine
- execution orchestration
- self_evolution（**Execution Strategy only** · Entry 050 / DEC-021；`commercial_learning=False`）

**不调用：** `11_CONTENT_FACTORY` / `commercial_assets`（Runtime 零连接）

---

## 1_DATA

**Status:** Active

**Role:** Data Foundation Layer（Operational Data）

**Track:** A（Core OS Runtime）

**Responsibilities:**
- external data collection
- database storage
- data source management

**Current Implementation:**
- `collector.py` — **EXTERNAL_IMPORT facade**（058D：`collector_kind=EXTERNAL_IMPORT`；非 Live）
- `collector_abstraction.py` — Source → Adapter → Raw → Observation（058D）
- `acquisition_capability.py` — modes / eligibility / field matrix / recommended path（058D）
- `market_source_core.py` — Source Registry / Collection Run / Observation / collectors registry
- `connectors/xianyu_import_connector.py` — Import Adapter 实现（xlsx/csv/json/jsonl；query；sha256）
- `xianyu_import_pilot_058c.py` — IMPORT_READY / WAITING
- `sources.py` — column map
- `database.py` — ensure_schema + collection_log（query 复用）
- `market_event_core.py` / `market_signal_core.py` — Event ≠ Observation；Signal bridge PARTIAL
- Tests：`test_acquisition_058d` / `test_xianyu_import_pilot_058c` / `test_market_source_058b`
- `data/ai_factory.db` — observations=0；collectors ACTIVE import + LIVE NOT_AVAILABLE
- `data/raw/xianyu/imports/` — drop zone（等待真实文件）
- `acquisition_engine.py` — Entry **059**：Acquisition Engine（tasks/policy/execute；不含平台 DOM）
- `product_origin.py` — Entry **058E**：Own Product / rights / business_models（≠ Product Type）
- `connectors/xianyu_browser_connector.py` — Entry **060**：Browser Collector v1（PUBLIC_WEB_READ；LIMITED / headless denied）
- `connectors/xianyu_interactive_connector.py` — Entry **061**：Interactive visible Chrome+CDP（LIMITED；test-dir candidates）
- `xianyu_interactive_pilot_061.py` — 061 pilot runner（Current DB delta=0）
- `1_DATA/_tests/xianyu_public_web_058e/` — Public Web feasibility artifacts（058E）
- `1_DATA/_tests/xianyu_browser_collection_060/` — Browser run artifacts（060）
- `1_DATA/_tests/xianyu_interactive_061/` — Interactive candidates（061；未入库）
- Tests：`test_xianyu_interactive_061` / `test_xianyu_browser_060` / `test_acquisition_engine_059` …
- `connectors/xianyu_targeted_search_062.py` — Entry **062**：SEARCH_RESULT 分类 + want_count 状态审计  
- `xianyu_targeted_search_pilot_062.py` — 062 pilot（Current DB delta=0）  
- `1_DATA/_tests/xianyu_targeted_search_062/` — 062 artifacts  
- Tests：`test_xianyu_targeted_search_062` / `test_xianyu_interactive_061` / `test_xianyu_browser_060` …  
- `connectors/xianyu_search_session_063.py` — Entry **063**：SearchSession / Control / Collect 分离  
- `xianyu_search_session_pilot_063.py` — 063 pilot  
- `1_DATA/_tests/xianyu_search_session_063/` — 063 artifacts  
- Tests：`test_xianyu_search_session_063` …  
- Audit：`docs/07_AUDIT/XIANYU_SEARCH_SESSION_ENTRY_063.md`

### Xianyu Extension Forensics（Entry 064 · Blueprint）

- `1_DATA/_tests/xianyu_extension_forensics_064/` — reference plugin extract + forensics artifacts  
- `reference_plugin/my-xianyu-scraper/` — read-only reference（manifest, content.js, popup.js）  
- `market_record_contract_064.json` — Extension→Bridge contract v064.1.0  
- `forensics_analysis.json` — structured KEEP/REWRITE/REMOVE  
- Tests：`test_xianyu_extension_forensics_064`（12 OK）  
- Audit：`docs/07_AUDIT/XIANYU_EXTENSION_FORENSICS_ENTRY_064.md`  
- Blueprint：`docs/02_ARCHITECTURE/XIANYU_BROWSER_EXTENSION_BLUEPRINT_064.md`  
- **Status：** Forensics complete；implementation → Entry 065

### Xianyu Browser Extension v1（Entry 065 · IMPLEMENTED）

- `1_DATA/browser_extension/xianyu/` — MV3 Extension（manifest, content.js, popup）  
- `connectors/xianyu_extension_bridge_065.py` — Localhost Bridge + ingest  
- `1_DATA/_tests/xianyu_extension_065/` — test sink（batch, normalized_preview, validation_report）  
- Tests：`test_xianyu_extension_065`（30 OK）  
- Audit：`docs/07_AUDIT/XIANYU_EXTENSION_IMPLEMENTATION_ENTRY_065.md`  
- **Status：** Extension + Bridge = **IMPLEMENTED / LIMITED**；Current DB auto-write = **NO**  
- **Entry 078 Reality：** `want_count` 可采；`view_count` = **COLLECTION GAP**；maxRecords≤50 / maxPages≤5 = **IMPLEMENTATION_LIMIT ≠ BUSINESS_THRESHOLD**；AI Query Planner = **NOT IMPLEMENTED**；Bridge 默认 TEST sink

### Xianyu MarketObservation Import Gate（Entry 066）

- `connectors/xianyu_market_observation_import_066.py` — verification report + optional DB import  
- `xianyu_first_real_probe_066.py` — live probe runner（`--human-verified` gate）  
- `1_DATA/_tests/xianyu_entry_066/` — probe + verification artifacts  
- `docs/AI_FACTORY_OS_WORK_PRINCIPLES.md` — 现行协作准则（Entry 066）  
- Tests：`test_xianyu_entry_066`（18 OK）  
- Audit：`docs/07_AUDIT/ENTRY_066_CORE_WORK_PRINCIPLES_AND_FIRST_REAL_XIANYU_OBSERVATION.md`  
- **Status：** Import gate **USED (069-B)**；**FIRST_REAL_XIANYU_MARKET_OBSERVATION=YES**（20 rows）；`market_observations=20`

### Acquisition Policy + AI Cost Gate（Entry 067）

- `acquisition_engine.py` — `market_acquisition_policies` + `apply_observation_filters` + goal registry  
- `ai_cost_gate.py` — AICostEstimate / gate / ai_execution_records；ModelSelector interface  
- Tables：`market_acquisition_policies`, `ai_cost_estimates`, `ai_execution_records`（additive）  
- Tests：`test_acquisition_policy_067`（24 OK）  
- Audit：`docs/07_AUDIT/ENTRY_067_ACQUISITION_POLICY_AND_AI_COST_GATE.md`  
- **Status：** Policy **PARTIAL**；Cost Gate **PARTIAL**；Model Router **NOT_BUILT**；paid AI **NONE**

### First REAL Observation + Filter Wiring（Entry 068）

- `connectors/xianyu_entry_068_pipeline.py` — Observation → Filter（reuse 067）  
- `xianyu_first_real_probe_068.py` — live Route A probe  
- `1_DATA/_tests/xianyu_entry_068/` — probe + filter + quality reports  
- Tests：`test_xianyu_entry_068`（11 OK）  
- Audit：`docs/07_AUDIT/ENTRY_068_FIRST_REAL_XIANYU_OBSERVATION_AND_FILTER.md`  
- **Status：** Filter **WIRED**；FIRST_REAL **NO**；Search Controller **NOT_FEASIBLE**；DB delta=0  

### Extension Live SEARCH_RESULT Verification（Entry 069-A）

- Code change：**NONE**（复用 065 Extension + Bridge test_mode）  
- Live run：`run_1788419997563` @ 2026-09-03T15:20:02+08:00  
- Evidence：`raw/run_1788419997563.json` + validation SUCCESS；records=**20**；SEARCH_RESULT  
- **FIRST_REAL_XIANYU_CANDIDATE_BATCH=YES**；Import deferred to 069-B  
- Verify：`1_DATA/_tests/xianyu_entry_069a/live_verification_run_1788419997563.json`  
- Audit：`docs/07_AUDIT/ENTRY_069A_XIANYU_EXTENSION_LIVE_SEARCH_RESULT_VERIFICATION.md`  
- **Status：** **PASS**

### Human-Verified MarketObservation Import（Entry 069-B）

- Gate：`xianyu_market_observation_import_066.process_extension_batch_for_entry(human_verified=True)`  
- Input：`run_1788419997563` → **20** MarketObservation（REAL / MANUAL_VERIFIED）  
- DB：`market_observations` 0→**20**；want NULL=6 zero=0；duplicates=0  
- Collection run：`crun_378745ca45e0`  
- Evidence：`1_DATA/_tests/xianyu_entry_069b/`  
- Audit：`docs/07_AUDIT/ENTRY_069B_XIANYU_HUMAN_VERIFIED_MARKET_OBSERVATION_IMPORT.md`  
- **Status：** **PASS**；**FIRST_REAL_XIANYU_MARKET_OBSERVATION=YES**；Code change **NONE**

### Observation → Filter → Candidate Set（Entry 070）

- Entry：`apply_filter_to_observation_candidates` + `apply_observation_filters`  
- Filters：`min_want_count=50`（068 DEFAULT_FILTER）  
- Result：MATCH=**7** · BELOW=**7** · UNKNOWN=**6** · ABOVE=0；Candidate Set=**7**；PERSISTENCE=**NONE**  
- Observation integrity：20→20；NULL want 保持  
- Evidence：`1_DATA/_tests/xianyu_entry_070/filter_candidate_result.json`  
- Audit：`docs/07_AUDIT/ENTRY_070_XIANYU_REAL_OBSERVATION_FILTER_CANDIDATE_SET.md`  
- **Status：** **PASS**；Code change **NONE**；无 Signal

### Candidate → Signal → Opportunity（Entry 071 · accelerated）

- Signal Runtime：**PARTIAL**（`market_signal_core` / products keyword groups）  
- **Candidate→Signal entry：NOT_IMPLEMENTED** → Signal **NOT_EXECUTED** for 7 MATCH  
- Opportunity：`discover_opportunities` dry-run = `INSUFFICIENT_DATA`（products=0）；lineage **NOT_EXECUTED**  
- DB：observations 20→20；signals 0→0；Code/Schema **NONE**  
- Evidence：`1_DATA/_tests/xianyu_entry_071/reality_boundary_result.json`  
- Audit：`docs/07_AUDIT/ENTRY_071_XIANYU_REAL_CANDIDATE_TO_SIGNAL_TO_OPPORTUNITY.md`  
- **Status：** **BLOCKED AT SIGNAL**；NEXT GAP = Observation/Candidate → Signal bridge

### Candidate→Signal + AI Invocation Preflight（Entry 072 · read-only）

- Candidate→Signal：**NOT_IMPLEMENTED**（as of 072）  
- ExecutionRuntime：**IMPLEMENTED_AND_USED**；ModelBridge：**IMPLEMENTED_AND_USED**（Runtime-only）  
- Model Router：**NOT_IMPLEMENTED**（PolicyEngine `LLM_ROUTING` only；`ModelSelector` NOT_BUILT）  
- AI Cost Gate：**IMPLEMENTED_BUT_UNUSED** on Track A provider path  
- Rule-first：**IMPLEMENTED_AND_USED**（deterministic + Signal aggregation）；no Candidate→Signal rule entry  
- Governor：**NOT IMPLEMENTED**；Planner / PolicyEngine / SelfEvolution：**REAL**  
- AI provider calls this Entry：**0**；DB delta：**0**  
- Audit：`docs/07_AUDIT/ENTRY_072_CANDIDATE_SIGNAL_AI_INVOCATION_REALITY_PREFLIGHT.md`  
- **Status：** **PASS_WITH_FINDINGS**；Code/Schema **NONE**

### Candidate → Signal（Entry 073 · Observation-native）

- Entry：`derive_signals_from_observation_candidates` / `derive_signals_from_observation_group`  
- Shared：`_compute_deterministic_signals`（product path keeps null_as_zero=True）  
- Observation path：NULL≠0；provenance in `evidence_refs`；**no products write**  
- Executed：7 MATCH → **6** signals（`Excel模板` group）；market_signals 0→6  
- AI：**0**；Opportunity：**NOT_EXECUTED**  
- FINDING：`IDEMPOTENCY_GAP`  
- Tests：`1_DATA/test_candidate_to_signal_073.py`  
- Evidence：`1_DATA/_tests/xianyu_entry_073/candidate_to_signal_result.json`  
- Audit：`docs/07_AUDIT/ENTRY_073_REAL_CANDIDATE_TO_SIGNAL.md`  
- **Status：** **PASS_WITH_FINDINGS**；Schema **NONE**

### Signal → Opportunity（Entry 074 · Observation lineage preflight）

- Preflight：`discover_opportunities` **Product-hard**  
- **Status：** **BLOCKED** (`BLOCKED_AT_SIGNAL_TO_OPPORTUNITY`)

### Signal → Opportunity（Entry 075 · Observation-native）

- Entry：`discover_opportunities_from_observation_signals`  
- Executed：6 Signals → **1** candidate（keyword `Excel模板`）；selection_results +1  
- AI：**0**；Product：**NOT_CREATED**（as of 075）  
- Audit：`docs/07_AUDIT/ENTRY_075_REAL_OBSERVATION_NATIVE_OPPORTUNITY.md`  
- **Status：** **PASS_WITH_FINDINGS**

### Opportunity → Product Definition（Entry 076）

- Entry：`6_EXECUTION/opportunity_to_product_076.productize_opportunity`  
- Input：`aoc_19399677b7ba` / `sel_53e7c414624f`  
- Output：`prod_a0638789fc2b` · status=`draft` · object_type=`product_definition`  
- Storage：`commercial_assets/product_definitions/product_definitions_v1.json`  
- Evidence-first classification；UNKNOWN content fields；NULL≠0  
- 055 E2E / CF / Publish / SQLite `products`：**NOT used**  
- AI：**0**；DB deltas：**0**  
- FINDING：`PRODUCT_IDEMPOTENCY_GAP`  
- Tests：`6_EXECUTION/test_opportunity_to_product_076.py`  
- Evidence：`1_DATA/_tests/xianyu_entry_076/opportunity_to_product_result.json`  
- Audit：`docs/07_AUDIT/ENTRY_076_OPPORTUNITY_TO_PRODUCT.md`  
- **Status：** **PASS_WITH_FINDINGS**

**说明：** Observation lineage：Filter→Signal（073）→Opportunity（075）→Product Definition（076）。Publish/CF = **NOT_EXECUTED**。

---

## 2_COGNITION

**Status:** Planned — Not Implemented

**Role:** Market Intelligence Layer（Cognition Layer — Unified Architecture）

**说明：** 目录当前为空（0 文件）。Blueprint 文档存在，**禁止标记 Completed / Active**。Blueprint ≠ Implementation。

**Blueprint:** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md)

**Agent Architecture:** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md)

**Planned Agents:** TrendAgent, DemandAgent, CompetitionAgent, OpportunityAgent, InsightAgent

**Future Responsibilities:**
- market understanding
- trend analysis
- opportunity discovery
- market scoring input for Decision Layer
- 接管 CF Legacy MarketAgent 职责（收敛目标 — 未实施）

**当前替代（临时）：** `11_CONTENT_FACTORY/agents/market_agent.py` 仅 Legacy keyword 路径 — **非 Cognition Layer 实现**

**不负责：** 产品生产、产品发布、最终决策执行、Commercial Object 登记

---

## 3_DECISION

**Status:** Active

**Role:** Decision Intelligence Layer

**Responsibilities:**
- scoring
- risk evaluation
- production decisions

**Current Implementation:**
- `decision_engine.py`
- `decision_agent.py`
- `scorer.py`
- `scoring_agent.py`
- `risk_engine.py`
- `candidate_selector.py` — Entry **052**：最小 Candidate Pool→Score→Risk→Rank（非最终商业智慧）
- `opportunity_discovery.py` — Entry **054**：Market Signal → Opportunity Candidate → Selection（含 evidence）
- `price_intelligence.py` — Entry **057**：Price provenance + recommendation（≠ Validated ≠ Paid）
- `test_opportunity_discovery.py`
- `test_price_intelligence.py`

**说明：** 负责决策评分与机会发现。Selection ≠ Experiment ≠ Production。不自动外部发布。

---

## 4_PRODUCT

**Status:** Planned — Not Implemented

**Role:** Product Definition Layer（Unified Architecture — 规划层）

**说明：** 目录当前为空（0 文件）。**禁止标记 Completed / Active**。

**Future Responsibilities:**
- product specification（与 Commercial Product Asset Contract 对齐）
- SKU definition
- pricing strategy（与 9_PRODUCT/pricing_engine 解耦后重建）

**当前替代（临时）：** `11_CONTENT_FACTORY/schemas/product_schema.py`（DigitalProduct）+ `commercial_assets/product_assets/`（Product Asset Object）

---

## 5_CONTENT

**Status:** Planned — Not Implemented

**Role:** Content Knowledge Layer（Unified Architecture — 规划层）

**说明：** 目录当前为空（0 文件）。**禁止标记 Completed / Active**。

**Future Responsibilities:**
- knowledge assets
- reusable template library（跨产品复用）
- content resource registry

**当前替代（临时）：** `11_CONTENT_FACTORY/artifact_generators/` + `artifacts/` — 生产实现，非 Knowledge Layer

---

## 6_EXECUTION

**Status:** Active

**Role:** Execution Runtime Layer

**Current Implementation:**
- `publisher.py` — Track A `published_local` only（≠ real publish）
- `execution_agent.py`
- `publish_queue.py` — Entry **052**：Publish Queue + Human External Action Gate + Publish Evidence
- `commercial_handoff.py` — Entry **053**：Commercial Product / Listing Package / Listing separation + readiness gates
- `e2e_autonomous_pilot.py` — Entry **055**：End-to-End Market→Queue bridge（reuse CF Adapter / Handoff / Queue）
- `human_publish_pack.py` — Entry **056**：Human Publish Pack + Evidence template（no auto publish）
- `test_publish_queue.py`
- `test_commercial_handoff.py`
- `test_e2e_autonomous_pilot.py`
- `test_human_publish_pack.py`

**说明：** Queue 可入队；外部发布禁止自动化。Pilot = AWAITING_HUMAN_ACTION。Commercial Product ≠ Published Listing。

---

## 7_MEMORY

**Status:** Active

**Role:** System Memory Layer

**Current Implementation:**
- `memory_core.py` — Entry **050**：Outcome Ontology + Execution/Commercial learning lanes + commercial ingest guardrail
- `test_commercial_learning_integrity.py` — Integrity tests 1–7
- memory json assets（`event_log.jsonl`、`pattern_memory.json`、`strategy_memory.json`、`runtime_policy.json`、`policy_patch.json`、`runtime_policy_snapshot.json`）

**Learning Integrity（050）：**
- Track A `extract_pattern` → Execution Learning only（`published_local` ≠ commercial success）
- Real Commercial Learning requires `commercial_outcome` + `data_origin=REAL` + `verified_source`
- SelfEvolution consumes Execution stats only

**Asset Review:**

| 文件 | Status | 说明 |
|------|--------|------|
| `core_state.json` | Deprecated / Review | 未发现当前代码引用，保留等待归档判断 |

---

## 8_CONFIG

**Status:** Active

**Role:** Configuration Layer

---

## 9_PRODUCT

**Status:** Frozen — Broken Legacy Entry

**Role:** Future Commercial Layer（历史残留）

**Historical Purpose:** Early SaaS/API productization direction

**说明：** 来源于早期 SaaS/API 商业化方向。当前不开发。含损坏引用（如 `api_server.py`）— **不可当作可用入口**。

**Future:**
- SaaS
- API Service
- User Management
- Pricing

**Current Implementation（Frozen，未接入主链）：**
- `api_server.py`
- `auth.py`
- `pricing_engine.py`
- `schemas.py`
- `service_layer.py`

---

## 10_DEPLOY

**Status:** Active — HTTP Runtime Entry（非 Production Ready）

**Role:** Deployment / Service Wrapper Layer — Core OS HTTP 入口

**Track:** A（Core OS Runtime）

**Responsibilities:**
- API access（FastAPI）
- service wrapper → `SystemController.run()`
- monitoring / trace（按实现存在）

**Reality（Entry 041-A / 041-D）：**
- 存在**可运行** HTTP Runtime Capability（`10_DEPLOY/api.py`）
- **不等于** Production Ready / Fully Deployed / Production Complete / System Finished
- **不**调用 Content Factory；**不**读写 `commercial_assets`

**历史误读：** 曾标 Frozen（旧 DC-005）— 与 Reality 不符；041-D 已校正。

**说明：** Deployment Layer 提供 Core OS 的 HTTP 包装能力。稳定可用作开发/验证入口；**禁止**写成已全面生产部署。

---

## 11_CONTENT_FACTORY

**Status:** Active — Isolated（Independent Runtime Track）

**Role:** Reusable Commercial Capability — Digital Product Production

**Track:** B（Content Factory / Commercial Capability Track）

**Architecture Ref:** [docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) §3

**关系澄清（041-D）：**

| 项 | 正确表达 |
|----|----------|
| Core OS | Governance + Operational Runtime（Track A） |
| Content Factory | Reusable Commercial Capability（Track B） |
| Current Reality | Independent Runtime Track（同仓库、不同入口） |
| Future Direction | Composable Capability（编排组合；**非**必须立即融合） |
| 禁止表述 | 「失败复制项目」「必须立即融合」「已统一 Runtime」 |

**Commercial Object SoT:** `commercial_assets/`（CF 生产交付；不替代商业对象持久化权威）

**Responsibilities:**
- product generation
- artifact generation
- packaging
- quality control（生产域）
- release workflow（人工发布辅助）

**Runtime Integration:** ❌ Not Connected to `0_START` DAG — **Not Started**（目标可选 Phase C；DEC-013：非强制默认）

**入口 Reality：** `11_CONTENT_FACTORY/adapter/adapter_runner.py`（及 Pipeline CLI）— **独立于** Core OS DAG

**Current Implementation:**

**Agents:**
- MarketAgent
- CreatorAgent
- QualityAgent
- PackagingAgent
- FeedbackAgent

**Artifact:**
- PDF
- PPT
- Word
- Excel

**Storage:**
- `storage/product_memory.json`
- `artifacts/products/`

**说明：** Intentional Isolation + Unfinished Convergence。Isolated Active = 可独立生产 ≠ 全系统自动商业闭环。

---

# Architecture Flow

## Target Flow（目标架构 — Design Reference）

> Document Role: Architecture Reference · Reality Status: Design Reference · Runtime Status: Requires Reality Validation

```
Governance / Orchestration（目标）
        ↓
1_DATA → 2_COGNITION → 3_DECISION
        ↓
Composable capabilities（含 Content Factory）
        ↓
Deploy / Feedback / Memory（按契约）
```

**注意：** 目标流 ≠ 当前 Runtime。不得写成已实现。

## Current Runtime Flow（当前真实运行流 — Reality）

```
【Track A — Core OS Runtime】
  0_START/main.py  或  10_DEPLOY/api.py
       ↓
  SystemController → 1_DATA → 3_DECISION → 6_EXECUTION → 7_MEMORY
  ✗ 不调用 11_CONTENT_FACTORY
  ✗ 不读写 commercial_assets

【Track B — Content Factory / Commercial】
  11_CONTENT_FACTORY/adapter/adapter_runner.py
       ↓
  commercial_assets（PR 等）→ ApprovalGate → ContentPipeline → Product Asset 产物
  ✗ 不进入 0_START DAG
```

**当前缺口（事实）：** `2_COGNITION` 未实现；Track A↔B **Runtime Integration Not Started**；商业 JSON 生命周期字段与生产现实可能不一致（RA-002，另开 Entry）。

**说明：** `9_PRODUCT` 为 Frozen Broken Legacy，不参与主执行流。

---

# Database Asset Layer

> **Document Role:** Architecture Reference · **Reality Status:** Design + partial Operational Reality · **Runtime Status:** Requires Reality Validation  
> Entry 041-D：下列「目标消费关系」**不等于**已全部实现。Operational SoT = `data/ai_factory.db`；Commercial SoT = `commercial_assets/`。

## 定位

**Database is cross-layer operational asset（运行/操作数据），不是 Commercial Object 生命周期 SoT。**

物理路径：`data/ai_factory.db`

数据库是 **Operational / Long-term Intelligence Store（运行域）**，跨 Core OS 模块共享。**不得**把商业 Experiment/PR/Asset 生命周期假装写在本库里已完成。

## 层级归属

| 模块 | 与数据库关系（Design / Reality） |
|------|--------------|
| **`1_DATA`** | Reality：管理采集 — 写入 products 等 Operational 表 |
| **`2_COGNITION`** | Design：消费分析 — **模块未实现** |
| **`3_DECISION`** | Reality：OS 域评分/决策读库 |
| **`11_CONTENT_FACTORY`** | Reality：**主商业产物写 commercial_assets / CF storage**；勿假设已写齐 DB 商业表 |
| **`7_MEMORY`** | Reality：文件型 memory；与 DB 物理隔离 |

## Blueprint

**Schema 设计：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md)

**状态：** Schema Blueprint v1 ✅ | Reality Audit v1 ✅ | Migration Plan v1 ✅ | Integration Design v1 ✅ | Implementation Plan v1 ✅ | **Database Implementation Pending**

**Reality Audit：** [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md](../07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md)

**Migration Plan：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md)

**Implementation Plan：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md)

## Database Evolution Status

| 阶段 | 状态 |
|------|------|
| Reality Audit Completed | ✅ |
| Migration Plan Completed | ✅ |
| Integration Design Completed | ✅ |
| Implementation Plan Completed | ✅ |
| Database Implementation Pending | ⏳ |

## Database Integration Contract

跨模块数据交换的**权威接口规范**： [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md)

| Interface | 路径 | 写入 | 读取 |
|-----------|------|------|------|
| **Interface 1** | `1_DATA` → Database | Raw Tables（market_* + Legacy） | — |
| **Interface 2** | Database → `2_COGNITION` | `opportunity_scores` | Raw Tables |
| **Interface 3** | `2_COGNITION` → `3_DECISION` | —（OS JSON 传递） | `opportunity_scores` |
| **Interface 4** | `11_CONTENT_FACTORY` → Database | `generated_products` | — |
| **Interface 5** | Feedback Loop | `product_feedback` | `2_COGNITION`, `3_DECISION` |

**规则：** 模块禁止直接读其他模块内部文件；必须通过 Database Contract 或 OS 标准 JSON。

**Integration Design：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md)

## Commercial Intelligence Contract

**商业智能模块数据契约：** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)

| Object | Producer | Consumer |
|--------|----------|----------|
| Market Signal | `1_DATA` | `2_COGNITION` / DB |
| Opportunity | `2_COGNITION` | `3_DECISION` |
| Production Request | `3_DECISION` | `11_CONTENT_FACTORY` |
| Product Asset | `11_CONTENT_FACTORY` | DB / Feedback |
| Feedback | Feedback 流程 | `2_COGNITION`, `3_DECISION` |

**Version：** Contract v1.0

---

## Commercial Validation Layer（商业验证层）

**Status:** Blueprint Completed

**Role:** Commercial MVP Validation Layer（商业最小验证层）

**说明：** 非独立运行目录，而是 **docs 认知层** — 定义商业实验、反馈闭环与 MVP 验证路径。负责将生产能力转化为可度量商业结果。

**Blueprint:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md)

**Responsibilities:**
- 30 产品商业实验设计
- MVP Business Loop（商业闭环）定义
- Feedback Data Architecture（反馈数据架构）
- Commercial Metrics（商业指标）与成功标准
- Product Selection Strategy（选品策略 — Opportunity Score vs Quality Score 分离）

**不负责：**
- 代码实现（Implementation Pending）
- 数据库 DDL 执行
- 修改 Core OS 或 Content Factory 运行逻辑

**关联模块：**

| 模块 | 关系 |
|------|------|
| `11_CONTENT_FACTORY` | 生产 Product Asset |
| `3_DECISION` | 产出 Production Request |
| `2_COGNITION` | 未来产出 Opportunity（MVP Phase 1 人工过渡） |
| `1_DATA` | Market Signal 采集与 Database 持久化 |
| Feedback 流程 | Customer Feedback → Database → Optimization |

**当前状态：** Blueprint v1 ✅ | MVP 实验执行 ⏳ Pending | Database Feedback 表 ⏳ Pending

---

## Commercial Experiment Layer（商业实验层）

**Status:** Blueprint Completed

**Role:** Commercial Experiment Management Layer（商业实验管理层）

**说明：** 非独立运行目录，而是 **docs 认知层** — 管理 30 产品商业验证实验的设计、记录、评估与反馈沉淀。为 Database Extension、Product Feedback Loop、2_COGNITION 提供数据结构基础。

**Blueprint:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md)

**上级 Blueprint:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md)

**Responsibilities:**
- Experiment Object（实验对象）与 Experiment Lifecycle（实验生命周期）定义
- 30 产品实验分类（Category A / B / C）与 Hypothesis System（假设系统）
- Feedback Object v1 与 Experiment Evaluation Model（评估模型）
- Experiment Metrics（四类指标）与 Commercial Experiment Workflow（工作流）

**不负责：**
- Content Factory 生产执行（属 `11_CONTENT_FACTORY`）
- 数据库 DDL 与代码实现
- 修改 Core OS 运行逻辑

**关联模块：**

| 模块 | 关系 |
|------|------|
| Commercial Validation Layer | 上级 — MVP 目标与商业闭环 |
| `11_CONTENT_FACTORY` | Production 阶段执行 |
| `3_DECISION` | Evaluation 结果影响生产阈值 |
| `2_COGNITION` | Feedback 驱动 Opportunity Score 优化 |
| `1_DATA` / Database | Experiment / Feedback 未来持久化 |

**当前状态：** Blueprint v1 ✅ | 实验台账 Implementation ⏳ Pending | DB `commercial_experiments` ⏳ Pending（建议表，未创建）

---

## Commercial Experiment Object Registry（商业实验对象登记体系）

**Status:** Blueprint Completed

**Role:** Experiment Object Registry Layer（实验对象登记层）

**说明：** docs 认知层登记规范 — 定义 Experiment Object JSON Schema v1、生命周期、30 产品管理规则、评价规则与 AI 读取规则。为实验资产标准化登记提供权威格式。

**Registry:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)

**上级 Blueprint:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md)

**Responsibilities:**
- Experiment Object（实验对象）标准 JSON Schema v1
- Experiment Lifecycle（9 状态）登记规则
- Category A / B / C 各 10 产品实验管理规则
- Success / Promising / Failed 评价规则
- 未来 DB 映射（commercial_experiments / generated_products / product_feedback）
- AI / Cognition 后续读取规则

**不负责：**
- 创建实验台账 JSON 文件（Implementation Pending）
- 数据库 DDL
- Python 运行代码

**当前状态：** Registry v1 ✅ | 台账文件 ⏳ Pending | DB 表 ⏳ Pending

---

## Commercial Experiment Selection Framework（商业实验选择框架）

**Status:** Blueprint Completed

**Role:** Experiment Selection Layer（实验选择层）

**说明：** docs 认知规则层 — 连接 Market Intelligence → Opportunity Object → Experiment Object。定义选择标准、Experiment Priority Score（实验优先级评分）、Category 分配规则与失败学习规则。

**Framework:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md)

**上级文档:**

- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md)

**Responsibilities:**
- Opportunity → Experiment 转换规则
- Experiment Priority Score（与 Opportunity Score 隔离）
- Category A / B / C 选择规则
- Failure Learning 对 Cognition / Decision / Future Selection 的影响

**不负责:**
- 创建 Experiment Object 实例
- 触发 Content Factory 生产
- 修改 opportunity_scores 或运行时代码

**当前状态:** Framework v1 ✅ | 自动选择 Implementation ⏳ Pending

---

## Production Request Contract Layer（生产请求协议层）

**Status:** Blueprint Completed

**Role:** Production Request Contract Layer（生产请求协议层）

**说明：** docs 认知契约层 — 定义 **Experiment Object** 与 **Content Factory Runtime** 之间的标准生产请求协议。明确 Experiment（商业验证目标）→ Production Request（生产规格）→ Generated Product（实际资产）三层职责分离。

**Contract:** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md)

**上级文档:**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md)

**Responsibilities:**
- Production Request Object Schema v1（含 asset_requirements / quality_requirements）
- 生命周期：draft → approved → production → completed → failed → archived
- 模块权限：3_DECISION 生成、11_CONTENT_FACTORY 只读执行
- Experiment → Production Request → Product Asset 字段映射
- 未来 `production_requests` 表 Blueprint 映射

**不负责:**
- 创建 Production Request JSON 实例
- Content Factory 代码接入
- 数据库 DDL 执行
- 触发实际生产

**关联模块:**

| 模块 | 关系 |
|------|------|
| `3_DECISION` | 根据 Experiment 生成 / 批准 Production Request |
| `11_CONTENT_FACTORY` | 未来唯一合法生产入口 — 读取并执行 |
| `2_COGNITION` | 只提供 Opportunity — 不参与生产 |
| Commercial Experiment Layer | 上游 Experiment Object 来源 |

**当前状态:** Contract v1 ✅ | Runtime 连接 ⏳ Pending | DB `production_requests` ⏳ Pending | JSON 实例 ⏳ Pending

---

## Experiment Prepared Review Layer（实验准备审核层）

**Status:** Blueprint Completed

**Role:** Experiment Prepared Review Layer（实验准备审核层）

**说明：** docs 认知协议层 — 在 **Experiment Object** 与 **Production Request** 之间建立人工审核门槛。定义 Prepared Review Checklist、Experiment Review Object Schema、审核生命周期与模块权限边界。

**Protocol:** [docs/04_BLUEPRINT/protocol/AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md](../04_BLUEPRINT/protocol/AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md)

**上级文档:**

- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md)

**Responsibilities:**
- Prepared Review 四层 Checklist（Business / Product / Validation / Commercial）
- Experiment Review Object Schema v1
- 生命周期：draft → reviewing → prepared / rejected → archived
- Experiment `draft → prepared` 审核门禁
- 未来 `experiment_reviews` 表 Blueprint 映射

**不负责:**
- 创建 experiment_review JSON 实例
- 修改 Experiment / Opportunity 资产文件
- 创建 Production Request
- Content Factory 调用
- 数据库 DDL

**关联模块:**

| 模块 | 关系 |
|------|------|
| Human Reviewer | MVP Phase 1 唯一审核执行者 |
| `3_DECISION` | 未来 Review Policy — Implementation Pending |
| Production Request Contract Layer | 下游 — approve 后可创建 Production Request |
| `11_CONTENT_FACTORY` | 禁止参与审核 |
| `2_COGNITION` | 禁止参与审核 |

**当前状态:** Protocol v1 ✅ | Review JSON 实例 ⏳ Pending | DB `experiment_reviews` ⏳ Pending | Runtime ⏳ Pending

---

## Content Factory Integration Layer（Content Factory 集成层）

**Status:** Design Completed

**Role:** Content Factory Integration Layer（Content Factory 集成层）

**说明：** docs 认知集成层 — 定义 Production Request Object 如何进入 `11_CONTENT_FACTORY` 并产出 Product Asset Object 的 Input/Output Contract、Agent 映射、Feedback 链路与 Runtime 保护规则。

**Design:** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md)

**上级文档:**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md)
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)

**Responsibilities:**
- Integration Input Contract v1（Production Request → CF）
- Agent Mapping（Creator / Generator / Quality / Packaging — bypass MarketAgent）
- Product Asset Output Schema v1
- Feedback → Experiment Evaluation 连接
- Runtime Protection Rules（CF 可生产 / 不可选品）

**不负责:**
- 修改 `11_CONTENT_FACTORY` Python 代码
- 调用生产 Agent
- 生成实际产品
- Runtime 调度接入

**关联模块:**

| 模块 | 关系 |
|------|------|
| `11_CONTENT_FACTORY` | 生产执行目标 — Implementation Pending |
| Production Request Contract Layer | 上游 Input 来源 |
| Production Authorization Gate | Approval 门禁 |
| `0_START` | 未来调度 — Phase 5 Pending |

**当前状态:** Integration Design v1 ✅ | Adapter Code ⏳ Pending | Pilot Production ⏳ Pending | Runtime Connected ❌

---

## Content Factory Adapter Layer（Content Factory 适配器层）

**Status:** Plan Completed

**Role:** Content Factory Adapter Layer（Content Factory 适配器层）

**说明：** docs 认知实施规划层 — 在 Integration Design 基础上，规划 Production Request → Approval → Adapter → 11_CONTENT_FACTORY → Product Asset 的实施方案、文件结构、字段映射、Pilot 范围与风险控制。

**Plan:** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md)

**上级文档:**

- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md)
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md)

**Responsibilities:**
- Adapter 层定位与 Legacy Flow 分析
- Adapter 职责 / 禁止边界
- 未来文件结构规划（adapter/ contracts/ services/）
- Input / Output 字段映射
- Pilot 范围（preq_20260712_005 P0 only）
- 风险控制（Approval Gate / Single Pilot / Rollback / Legacy Protection）
- Implementation Roadmap Phase 2–3 Checklist

**不负责:**
- 创建 Adapter 代码或目录
- 修改 11_CONTENT_FACTORY Python
- Pilot 生产执行
- Runtime 调度

**当前状态:** Adapter Plan v1 ✅ | Code Implementation ✅ Completed | Pilot Execution ⏳ Pending

---

## Content Factory Adapter Runtime（Adapter 运行时层）

**Status:** Code Completed

**Role:** Content Factory Adapter Runtime（Adapter 运行时层）

**说明：** Production Request → Approval Gate → Input Mapper → `run_from_production_request()` → Output Mapper（Product Asset 草稿 dict，不写 commercial_assets）。

**路径:** `11_CONTENT_FACTORY/adapter/`

**Pipeline 扩展:** `ContentPipeline.run_from_production_request()` — Legacy `run(keyword)` 不变。

**Pilot Whitelist:** 仅 `preq_20260712_005`；默认 `dry_run=True`。

**当前状态:** Adapter Code v1 ✅ | Pilot Execution ⏳ Pending | product_assets JSON ⏳ Pending

**明确:** Adapter Completed ≠ Production Started；Code Completed ≠ Commercial Asset Created。

---

## Content Factory Adapter Architecture Audit（Adapter 架构审计层）

**Status:** Audit Completed

**Role:** Content Factory Adapter Architecture Audit（Adapter 架构审计层）

**说明：** 只读 Runtime 审计 — 在 Adapter Code Implementation 前分析 Legacy Pipeline、插入点、Output 映射与风险。

**Audit:** [docs/07_AUDIT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md](../07_AUDIT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md)

**审计结论:** CF 入口 `ContentPipeline.run(keyword)`；0_START/3_DECISION 无 CF 引用；推荐新增 `run_from_production_request()`；**可有条件进入 Adapter Code** — 须处理 Excel Pilot 的 PDF validation 门禁。

**当前状态:** Audit v1 ✅ | Adapter Code v1 ✅ | Pilot Execution ⏳ Pending

---

## Product Asset Contract Layer（产品资产契约层）

**Status:** Blueprint Completed

**Role:** Product Asset Contract Layer（产品资产契约层）

**说明：** docs 认知契约层 — 定义 Content Factory 生产完成后 **Product Asset Object** 的标准 Schema、生命周期（8 状态）、模块职责、CF Output 映射、Feedback 连接与未来 DB 映射。

**Contract:** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md)

**上级文档:**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md)
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)

**Responsibilities:**
- Product Asset Object Schema v1（含 artifact_information）
- 生命周期：generated → quality_checking → completed → published → testing → validated → archived / failed
- 模块边界：11_CONTENT_FACTORY 生成 / 3_DECISION 禁止生成 / 7_MEMORY 学习摘要
- CF Output → Product Asset 映射
- Feedback 四类连接（market / customer / sales / quality）
- 未来 `product_assets` 表 Blueprint

**不负责:**
- 创建 product_assets JSON 实例
- Content Factory 生产
- 数据库 DDL

**当前状态:** Contract v1 ✅ | JSON 实例 ⏳ Pending | DB ⏳ Pending | Runtime Connected ❌

---

## Product Asset Validation Gate Layer（产品资产验收门禁层）

**Status:** Blueprint Completed

**Role:** Product Asset Validation Gate Layer（产品资产验收门禁层）

**说明：** docs 认知契约层 — 定义 Content Factory Output 进入 `commercial_assets/product_assets/` 之前的验收门禁、`product_asset_validation` Object、四类 Checklist、决策规则与模块边界。

**Design:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PRODUCT_ASSET_VALIDATION_GATE.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_PRODUCT_ASSET_VALIDATION_GATE.md)

**上级文档:**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md)
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md)
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md)

**Responsibilities:**
- Validation Gate 层定位（≠ QualityAgent）
- product_asset_validation Object Schema v1
- Artifact / Contract / Quality / Commercial 四类 Checklist
- validation_status: passed / failed / pending_review
- 对象关系链：PR → Product Asset → Validation → Feedback
- Future Runtime Connection（Entry 033+）

**不负责:**
- Validation Gate Runtime 实现
- product_assets / validations JSON 实例创建
- Pilot 生产执行
- 修改 11_CONTENT_FACTORY Python

**当前状态:** Validation Gate Design v1 ✅ | Runtime v1 ✅ | product_assets ⏳ Pending

**明确:** Validation Gate Completed ≠ Production Started；Design Completed ≠ Runtime Connected。

---

## Product Asset Validation Runtime（产品资产验收 Runtime 层）

**Status:** Implementation Completed

**Role:** Product Asset Validation Runtime（产品资产验收 Runtime 层）

**说明：** Runtime 实现 — `ProductAssetValidator` 执行四类 Checklist，产出 `product_asset_validation` Object；只负责 check，不负责 create / write JSON / publish。

**路径:** `11_CONTENT_FACTORY/validation/product_asset_validator.py`

**Design 上级:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PRODUCT_ASSET_VALIDATION_GATE.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_PRODUCT_ASSET_VALIDATION_GATE.md)

**Responsibilities:**
- Artifact / Contract / Quality / Commercial 四类验收
- validation_status: passed / failed / pending_review
- product_asset_validation Object 产出（内存 dict）
- output_mapper `validation_context` 对接

**不负责:**
- 写入 commercial_assets/product_assets/
- Pilot 生产执行
- 修改 Legacy Pipeline / Agents

**当前状态:** Validation Runtime v1 ✅ | Pilot preq_005 ✅ | product_assets 1 条 ✅

**明确:** Validation Runtime Completed ≠ Production Started；Code Completed ≠ Product Created。

---

## Pilot Production Runtime Layer（Pilot 生产运行时层）

**Status:** Execution Completed

**Role:** Pilot Production Runtime Layer（Pilot 生产运行时层）

**说明:** Entry 033-B1 — 首次商业生产闭环：PR → Approval → Adapter → CF → Validation Gate → Product Asset。

**Pilot:** `preq_20260712_005` — Excel 考勤记录表 — **唯一允许**

**产物:**

- `commercial_assets/pilot_outputs/preq_20260712_005/`
- `commercial_assets/product_assets/product_assets_v1.json`
- `commercial_assets/product_asset_validations/product_asset_validations_v1.json`

**Product Asset ID:** `8523329941d4`

**当前状态:** Pilot Execution ✅ | product_assets 1 条 | Market Validation ⏳ Pending

**明确:** Production Completed ≠ Commercial Success；Validation Passed ≠ Market Validated；Single Pilot Only。

---

## Feedback & Experiment Evaluation Layer（反馈与实验评估层）

**Status:** Blueprint Completed

**Role:** Feedback & Experiment Evaluation Layer（反馈与实验评估层）

**说明:** Product Asset 生产后反馈采集、Experiment Evaluation、Learning Loop 与四类 Score 隔离。

**Contracts:**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md)

**Responsibilities:**
- Feedback Object Schema v1（五类 feedback_type）
- Experiment Evaluation Object Schema v1
- hypothesis_result / recommendation / learning_summary
- Score Isolation — 四者禁止混用
- Learning Loop → Selection Framework
- DB Blueprint：`feedback` / `experiment_evaluations`

**不负责:**
- Feedback / Evaluation JSON 实例
- 市场验证执行
- Runtime 修改

**当前状态:** Design v1 ✅ | Feedback 实例 ✅ 1 条 pending | Evaluation 实例 ✅ 1 条 pending

**明确:** Feedback Design ≠ Market Validation；Blueprint ≠ Implementation。

---

## Pilot Observation Protocol Layer（Pilot 商业观察协议层）

**Status:** Blueprint Completed

**Role:** Pilot Observation Protocol Layer（Pilot 商业观察协议层）

**说明:** 为 Product Asset `8523329941d4` 定义 Observation Protocol — 观察指标、观察期、成功/失败判据、数据治理与 Feedback/Evaluation 映射。

**Protocol:** [docs/04_BLUEPRINT/protocol/AI_FACTORY_OS_PILOT_OBSERVATION_PROTOCOL.md](../04_BLUEPRINT/protocol/AI_FACTORY_OS_PILOT_OBSERVATION_PROTOCOL.md)

**上级文档:**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md)

**Responsibilities:**
- Observation Layer 定位（Protocol ≠ Feedback）
- 四类 Observation Metric Schema（允许 null）
- observation_status: planned / running / completed
- Success / Failure Criteria + Data Governance
- Human Assisted SOP

**不负责:**
- 上架执行、Feedback/Evaluation 实例修改、Observation Agent 实现

**当前状态:** Protocol v1 ✅ | observation_status **planned** | 观察执行 ⏳ Pending

**明确:** Observation Protocol Design ≠ Observation Started；Protocol Completed ≠ Market Validation。

---

## Opportunity Candidate Registry（商业机会候选登记体系）

**Status:** Blueprint Completed

**Role:** Commercial Opportunity Asset Pool Layer（商业机会资产池层）

**说明：** docs 认知登记层 — AI Factory OS **第一层商业机会资产池**。管理 Opportunity Candidate（商业机会候选）的标准 Schema、生命周期与评估规则，连接 Market Intelligence → Opportunity Object → Experiment Selection。

**Registry:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md)

**Responsibilities:**
- Opportunity Candidate ≠ Opportunity Object 语义隔离
- Candidate Schema v1 与 5 状态生命周期
- Candidate Readiness 评估与进入 Selection 的前置规则
- 未来 Cognition Agent 自动生成 Candidate 的设计
- Commercial Intelligence Asset 治理归属

**不负责:**
- 创建 Candidate 实例或 JSON 台账
- 产出 Opportunity Object（属 2_COGNITION）
- 创建 Experiment Object（属 Selection + Registry）

**当前状态:** Registry v1 ✅ | Candidate 实例 ⏳ Pending | DB `opportunity_candidates` ⏳ Pending

---

## Opportunity Dataset Generation Rule（商业机会数据生成规则）

**Status:** Blueprint Completed

**Role:** Commercial Intelligence Dataset Generation Layer（商业智能数据生成层）

**说明：** docs 认知规范层 — 定义 Opportunity Candidate 数据资产**如何产生、如何质检、如何登记**的标准流程。为后续创建 Candidate 实例提供 SOP，不替代 Registry Schema 定义。

**Rule:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_DATASET_GENERATION_RULE.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_DATASET_GENERATION_RULE.md)

**上级文档:** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md)

**Responsibilities:**
- Data Sources（数据来源）定义 — 1_DATA / 人工 / 反馈 / 平台 / 竞争
- Candidate Quality Rules（四类证据质检）
- Candidate Readiness Score（与 Opportunity / Experiment Priority 隔离）
- Creation Template 与 Human Assisted Phase SOP
- Future Agent 自动生成规则与 Data Governance

**不负责:**
- 创建 Candidate 实例或 JSON 数据
- 修改 Python / 数据库
- 产出 Opportunity Object 或 Experiment Object

**当前状态:** Rule v1 ✅ | 首批 Candidate 数据 ⏳ Pending

---

## Asset Management Reference

**项目资产治理总规范：** [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](../04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)

| 文档 | 用途 |
|------|------|
| ASSET_LIFECYCLE_POLICY | 资产分级、归属、生命周期、清理策略 |
| ASSET_AUDIT | 审计规范与生命周期状态 |
| ASSET_SCAN_REPORT | 项目资产扫描现状 |
| ASSET_AUDIT_TEMPLATE | 单文件审计登记 |

---

## 相关文档

| 文档 | 路径 | 用途 |
|------|------|------|
| 工程进度 | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` | 当前真实建设状态 |
| 系统快照 | `docs/01_CURRENT_STATE/reference/system_snapshot.md` | 架构恢复说明 |
| 工作准则 | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` | 项目恢复与自描述原则 |
| 执行历史 | `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` | Cursor 重大修改记录 |
| Cognition 蓝图 | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` | 2_COGNITION Market Intelligence Layer 设计 |
| Database Schema 蓝图 | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` | 商业数据资产表结构设计 |
| Database Migration 计划 | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md` | Additive 演化路线与表映射 |
| Database Integration 设计 | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md` | 跨模块 Database Contract |
| Database Extension 实施计划 | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md` | Step 0–5 执行规范 |
| Asset Lifecycle Policy | `docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md` | 项目资产治理总规范 |
| Project Intelligence Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md` | Project Intelligence Layer 总架构 |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` | 商业智能 Object 契约 v1 |
| Cognition Agent Architecture | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md` | 2_COGNITION 五 Agent 架构 |
| Commercial MVP Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md` | 商业验证阶段 MVP 设计 v1 |
| Commercial Experiment System Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md` | 商业实验管理体系设计 v1 |
| Experiment Object Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` | 商业实验对象登记规范 v1 |
| Commercial Experiment Selection Framework | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md` | 商业实验选择规则层 v1 |
| Opportunity Candidate Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md` | 商业机会候选资产池登记 v1 |
| Opportunity Dataset Generation Rule | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_DATASET_GENERATION_RULE.md` | 商业机会数据生成规范 v1 |
