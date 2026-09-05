# Entry 078 — Xianyu Commercial Closed-Loop Reality Audit

**Date:** 2026-09-05  
**Mode:** READ-ONLY / NO Runtime·DB·Asset mutation during investigation  
**Result:** `PASS_WITH_FINDINGS`  
**Cursor PASS ≠ ChatGPT Closure Review**  
**Paid AI used in this Entry:** `0`（static analysis + SQLite read-only）

---

## 1. Original Objective

建立一个真正能够在闲鱼跑通的商业闭环：真实市场采集 → 沉淀 → 选品 → 生产 → 人工发布 → 真实反馈回写 → 商业学习 → 下一轮采集。

## 2. Current Objective

在任何结构性修改之前，完整确认当前 AI_FACTORY_OS 闲鱼商业闭环 Reality（采集 / 数据 / 选品 / 定价 / 产品 / 发布 / 反馈 / 学习 / AI 成本）。

## 3. Scope

阅读、查询、统计、静态分析、DB 只读、文件盘点、provenance 验证、Formal Audit、必要 docs 同步、Git。

## 4. Out of Scope

修改采集器 / DB migration / 删除数据或产品 / 改评分定价 / 生产发布 / 付费 AI / 外部平台动作 / 进入 Entry 079。

---

## 5. Executive Reality Summary

当前系统**已具备半条真实链路**：

> Browser Extension（人工打开搜索页）→ Bridge TEST sink → Human-verified Import（069B）→ Current DB `market_observations=20` → Filter（070，`min_want_count=50` 为 **IMPLEMENTATION_DEFAULT**）→ 7 MATCH → 6 deterministic Signals（073，**无 AI**）→ 1 keyword-group Opportunity（075）→ Product Definition draft（076）→ Product Asset `a949d2e47cf1`（077，质量 PASS）→ Human Publish Pack（**NOT_PUBLISHED**）。

闭环在 **Human Publish 之后全部断开**：

| 缺口 | Reality |
|------|---------|
| 真实发布 / 曝光 / 浏览 / 想要 / 咨询 / 订单 / 支付 / 收入 | **NOT_STARTED** |
| `publish_evidence` / `market_events` | **0 rows** |
| Commercial Learning（生产路径） | **NOT_STARTED**（API scaffold 存在） |
| `view_count` 采集 | **COLLECTION GAP**（扩展不解析；DB 列全 NULL） |
| AI Query Planner / 自动关键词 | **NOT IMPLEMENTED** |
| `maxRecords≤50` / `maxPages≤5` | **IMPLEMENTATION_LIMIT ≠ BUSINESS_THRESHOLD** |
| `min_want_count=50` | **IMPLEMENTATION_DEFAULT ≠ validated business threshold** |
| PM/Gantt 具体商品 | **HYPOTHESIS**；上游仅证明 Excel模板市场类 |
| `a949` Publish Pack | **PARTIAL**（可人工参考发布，但相对 queue schema 缺 FAQ/delivery；未入 publish_queue；价格 9.9 vs CF 19.9 冲突） |

**Verdict：** 商业闭环 **未跑通**。已跑通的是「真实观察 → 假设产品资产」前半段；后半段反馈学习缺失。不得把 production/quality PASS 当作 commercial success。

---

## 6. Current Closed Loop Diagram

```text
Collection .......... IMPLEMENTED (Extension) + HUMAN_REQUIRED (open search / Start)
    → Data .......... PARTIAL (Bridge default TEST sink; DB only via 066 human gate)
    → Keyword ....... HUMAN_REQUIRED / NOT_STARTED (no AI Query Planner; query from page/URL/task)
    → Depth ......... IMPLEMENTATION_LIMIT (maxRecords≤50, maxPages≤5; scroll aids in-page load)
    → Intelligence .. PARTIAL (deterministic signals; engagement=0 when views missing)
    → Selection ..... PARTIAL (heuristic scorer; keyword-group → 1 opportunity)
    → Pricing ....... PARTIAL (CF defaults + hypothesis; Paid Price absent)
    → Production .... IMPLEMENTED (077 deterministic Excel; AI=0)
    → Quality ....... IMPLEMENTED (SELLABLE_QUALITY_FLOOR PASS for a949)
    → Publish Pack .. PARTIAL (a949 usable MD; incomplete vs queue required files)
    → Human Publish . HUMAN_REQUIRED / NOT_STARTED (no listing published)
    → Feedback ...... NOT_STARTED (0 evidence, 0 market_events)
    → Learning ...... NOT_STARTED (commercial path unused; scaffold exists)
```

---

## 7. Detailed Reality Matrix

| Capability | Current Implementation | Evidence | Decision Maker | Current Threshold / Formula | Trustworthiness | AI Needed | Paid Cost | Action |
| ---------- | ---------------------- | -------- | -------------- | --------------------------- | --------------- | --------- | --------- | ------ |
| Extension collect | content.js card scrape | `1_DATA/browser_extension/xianyu/` | Human Start + DOM | maxRecords≤50, maxPages≤5 | MEDIUM（UI fragile） | No | 0 | KEEP |
| Keyword source | URL/search box / task param | content.js `readQueryFromPage`; engine `select_query` | Human | N/A | HIGH for “manual” | Optional future | 0 now | INVESTIGATE |
| AI Query Planner | Comment only | acquisition_engine L527 | N/A | N/A | N/A | Yes later | Potential | INVESTIGATE |
| want_count parse | `/(\d+)\s*人想要/` | content.js `parseWant` | Extension | NULL if missing | HIGH when VISIBLE | No | 0 | KEEP |
| view_count collect | Not parsed | content.js no view; DB 20/20 NULL | N/A | N/A | **GAP** | No | 0 | REDESIGN |
| Bridge ingest | TEST_MODE default | bridge_065 | Policy | test sink | HIGH | No | 0 | KEEP |
| DB import | Human verified 066 | import_066 + 069B | Human gate | REAL+MANUAL_VERIFIED | HIGH | No | 0 | KEEP |
| Filter 20→7 | acquisition_engine filter | entry_068 DEFAULT + 070 JSON | Code default | min_want=50 | HEURISTIC | No | 0 | INVESTIGATE |
| Signals 7→6 | market_signal_core deterministic | DB 6 signals | Rules | 6 types | MEDIUM（engagement distorted） | No | 0 | INVESTIGATE |
| Opp 6→1 | group by keyword | opportunity_discovery_075 | Rules | 1 keyword group | HIGH for mechanism | No | 0 | KEEP |
| Product Def | opportunity_to_product_076 | prod_a0638789fc2b draft | Rules+human lineage | evidence-first | HIGH for draft | No | 0 | KEEP |
| Specific SKU | PM/Gantt hypothesis | experiments JSON | Human hypothesis | HYPOTHESIS | LOW as market fact | Optional | 0 | KEEP |
| Scorer | hot/trend/comp/profit/diff | scorer.py + SCORE_WEIGHTS | Heuristic | weights 0.31/0.25/0.19/0.15/0.10; threshold 40 | HEURISTIC | No | 0 | REDESIGN |
| Pricing | CF hardcodes + PI ontology | creator_agent / price_intelligence | Defaults | 19.9/29.9/…; a949 9.9 hyp | HEURISTIC≠MARKET | No on path | 0 | INVESTIGATE |
| Product Asset | CF adapter + openpyxl | a949d2e47cf1 | Authorized PR | Quality floor | HIGH as asset | No | 0 | KEEP |
| Publish pack | MD + partial package | e2e_outputs/a949 | Human | Human gate | PARTIAL | No | 0 | REPLACE |
| Feedback writeback | market_event_core API | rows=0 | Human evidence | REAL+verified | Scaffold only | No | 0 | INVESTIGATE |
| Commercial learning | memory_core gates | unused | Event router | commercial_outcome required | NOT_STARTED live | Optional | Potential | INVESTIGATE |
| ModelBridge LLM | DeepSeek/OpenAI HTTP | 0_START/model_bridge.py | Policy | budget ceiling | Idle on 069–077 | Yes if routed | **Yes if used** | KEEP |

Action vocabulary: KEEP / REPLACE / REDESIGN / REMOVE / INVESTIGATE only（本 Entry 不执行）。

---

## 8. Collection Reality

### Extension files

`1_DATA/browser_extension/xianyu/{manifest.json,popup.html,popup.js,content.js,README.md}` — MV3；host `*.goofish.com` + localhost bridge。

### Keyword source

| Question | Reality |
|----------|---------|
| From URL? | **Yes** — query params `q` / `keyword` / `searchWord` |
| From search box? | **Yes** — fallback `input[type=search]` / placeholder 搜索 |
| Program auto-type keyword? | **No** |
| Auto switch keywords? | **No** |
| Auto generate next keywords? | **No** |
| AI Query Planner? | **NOT IMPLEMENTED**（`select_query` = task parameter；comment “future”） |

### Volume limits

| Param | UI default | Hard clamp | Classification |
|-------|------------|------------|----------------|
| maxRecords | 20 | **≤50** | `IMPLEMENTATION_LIMIT ≠ BUSINESS_THRESHOLD` |
| maxPages | 1 | **≤5** | same |
| scroll | step 400 / interval 300 / maxScrollRounds | Helps load cards in page | Technical, not market sample size proof |

050 不得解释为「市场认为 50 足够」。

### Field capability matrix

| Field | Status |
|-------|--------|
| source / platform | 实际可采集（常量 goofish/xianyu） |
| source_item_id / source_url | 实际可采集 |
| title / price / currency | 实际可采集 |
| want_count / want_count_status | 实际可采集（可见→int；缺失→null + MISSING_ON_CARD） |
| view_count | **当前不可采集**（代码未解析；DB 列预留全 NULL） |
| result_origin / observed_at / query / session_id / collector_version / result_position | 实际可采集 |
| image_url | 实际可采集（卡片 img） |
| seller / comments / shares / publish_time / sales info | **当前不可采集**（sales_platform 恒 null） |

### want_count Reality

- Parse: `(\d+)\s*人想要`
- NULL ≠ 0：**遵守**（MISSING → null；069B null=6 zero=0）
- Filter：NULL → UNKNOWN（**不删除**行；分类）
- Low want：BELOW_THRESHOLD（保留分类，不物理删除）

### Pagination Reality

- Next control: `[class*="search-pagination-page-box"]` digits / `>` / `下一页`
- Cross-page: yes if maxPages>1
- Dedupe: globalSeen by `id:` / `url:` / title|price hash
- Fragility: class-name selectors — UI change → **易失效**

### Collection chain (Runtime vs Test)

```text
Extension → Bridge(test_mode=True default) → 1_DATA/_tests/xianyu_extension_065/
→ [HUMAN] import_066 → data/ai_factory.db.market_observations
→ filter (068/engine) → in-memory candidates (not a table)
→ market_signal_core → market_signals
```

HISTORICAL / alternate: browser_connector 060, interactive 061, targeted 062, search_session 063 — mostly test sinks / CDP；Live API = NOT_AVAILABLE。

---

## 9. Keyword Reality

- Live commercial lineage keyword: **`Excel模板`**（人工搜索页 + Extension）
- `keywords` table: **0 rows** — not used as planner store
- Auto keyword generation: **NOT IMPLEMENTED**
- Adaptive depth / learning→acquisition: **PROPOSED / NOT_BUILT**

---

## 10. Want/View Reality

| Metric | Collection | DB (20 REAL) | Used in 070 | Used in 073 |
|--------|------------|--------------|-------------|-------------|
| want_count | Yes | 14 non-null / 6 null | Yes（threshold 50） | demand/trend |
| view_count | **No** | **20/20 NULL** | No | engagement falls back to 0.0 when total_view=0 |

**FINDING：** `engagement_signal=0.0`（unit `want_per_view`）在 view 全缺失时表现为“零互动”，易被误读为市场事实。实为 **DATA GAP ARTIFACT**。

MATCH want_counts（070）: 2245, 1930, 1082, 660, 642, 436, 186（均 ≥50）。

---

## 11. Data / DB Reality

**Current DB:** `data/ai_factory.db`（282624 bytes）  
**Legacy DB:** `99_ARCHIVE/database_history/ai_factory_legacy_simulation_20260830.db` — **isolated**（SAMPLE history；不参与当前推理）

### Table Reality

| 表 | 当前用途 | 行数 | REAL | TEST | SAMPLE | 是否参与当前推理 | 问题 |
| - | ---- | -: | ---: | ---: | -----: | -------- | -- |
| market_observations | 069B 真观察 | 20 | 20 | 0 | 0 | **Yes** | view/seller/comment/share/published 全空 |
| market_signals | 073 信号 | 6 | 6（derived） | 0 | 0 | **Yes** | engagement 失真；growth UNAVAILABLE |
| selection_results | 075 选中 | 1 | 1 | 0 | 0 | **Yes** | soft dedupe cosmetic gaps historical |
| products | 旧产品路径 | 0 | 0 | 0 | 0 | No | 空；与 observation 路径分离 |
| scores | 产品评分落库 | 0 | 0 | 0 | 0 | No | 空 |
| keywords | 关键词库 | 0 | 0 | 0 | 0 | No | 未使用 |
| platforms | 平台字典 | 2 | — | — | — | Partial | xianyu + taobao 名存在≠能力 |
| market_events | 反馈事件 | 0 | 0 | 0 | 0 | No | 闭环缺口 |
| publish_evidence | 发布证据 | 0 | 0 | 0 | 0 | No | 无人记录 |
| publish_queue | 人工发布队列 | 2 | legacy/auto | — | — | Partial | **无 a949**；仅 8523 + f2f8 |
| collection_runs | 采集运行 | 14 | mix | mix | 0 | Partial | 含手机壳等非 069B |
| collection_log | 旧日志 | 14 | ? | ? | ? | Low | 并行旧结构 |
| collectors / market_sources / acquisition_* | 能力/任务 | small | — | — | — | Ops | — |
| ai_cost_estimates | 成本估计 | 16 | — | — | — | Audit | estimates |
| ai_execution_records | 执行记录 | 4 | — | — | — | Audit | paid_invocation=**0** all |
| market_acquisition_policies | 策略 | 24 | — | — | — | Low | — |

Foreign keys: **none declared**（schema 松耦合）。

### Future extensibility（报告缺口 only）

| Concept | Present? |
|---------|----------|
| Platform / Source / Observation | Yes（tables） |
| Product / Product Asset | Product table empty；assets in JSON/`commercial_assets` |
| Listing | JSON handoff；queue fields |
| Event / Feedback | market_events schema yes；0 rows |
| Order / Revenue / Cost | event types scaffold；no dedicated order table |
| Experiment / Provenance | mostly `commercial_assets` JSON + observation provenance fields |
| Short-video / novel platform adapters | **Not present** as first-class — schema partially platform-agnostic but product-type/runtime not ready |

**SCHEMA REDESIGN REQUIRED?** Not mandatory for 闲鱼 pilot； for multi-platform closed-loop feedback, **INVESTIGATE** unification of Asset/Listing/Order/Cost（本 Entry 不 migration）。

---

## 12. 069B→077 Provenance Reality

```text
069B: 20 REAL/MANUAL_VERIFIED observations (query=Excel模板, run crun_378745ca45e0)
  → 070: 20 → 7 MATCH + 7 BELOW + 6 UNKNOWN (min_want_count=50; classify only; AI=0)
  → 073: 7 MATCH → 6 deterministic signals (AI=0)
  → 075: 6 signals → 1 opportunity aoc_19399677b7ba via keyword group Excel模板 (AI=0)
       selection sel_53e7c414624f score=68.92
  → 076: Product Definition prod_a0638789fc2b draft; market class Excel模板=DIRECT_EVIDENCE;
         specific subtype UNKNOWN; AI=0
  → Hypothesis prep: PM/Gantt = HYPOTHESIS/DERIVED (≠ DIRECT_EVIDENCE)
  → 077: preq_20260904_pmgantt → Asset a949d2e47cf1; Quality PASS; AI=0; NOT_PUBLISHED
```

### Why “6 Signals → 1 Opportunity”

**规则聚合，非 AI、非人工挑选多个机会。**  
所有 6 个 signal 共享 keyword=`Excel模板` → `_group_signals_by_keyword` → 1 candidate。

### Why PM/Gantt

**非 076 自动输出。** 076 只固化市场类 Excel模板 draft。PM/Gantt 为后续商业假设（观察标题中存在工作计划/甘特类 listing 的**弱启发** + 人工设计），明确标记 HYPOTHESIS。

### a949 Reality checklist

- REAL Product Asset on disk: **Yes**
- SELLABLE_QUALITY_FLOOR PASS: **Yes**
- Human-publishable materials: **Partial Yes**
- Published: **No**
- Real sales data: **No**

---

## 13. Selection Reality

### Metrics & formula（原样）

From `3_DECISION/scorer.py` + `8_CONFIG/config.py`:

```
hot        = clamp(want * 2 + view_contrib)
trend      = clamp(hot * 0.85 + 10)
comp       = clamp(100 - min(want / 5, 80))
profit     = clamp(price * 3 + want * 0.5)
difficulty = clamp(50 - min(want, 40))
total      = hot*0.31 + trend*0.25 + comp*0.19 + profit*0.15 + difficulty*0.10
```

- `view_contrib`: if view NULL → 0.01（product path null_as_zero）或 0.0（observation path）
- Observation path: want NULL → **score None**（NULL≠0）
- Weights: **HEURISTIC / IMPLEMENTATION_DEFAULT**
- `PUBLISH_SCORE_THRESHOLD = 40`（candidate_selector default；也可 60 注释历史）— **not validated WTP**
- `top_n = 5` default — **IMPLEMENTATION_DEFAULT**
- Risk: sensitive keyword block + price≤0 low — **HEURISTIC**

**MODEL REBUILD REQUIRED**（若目标为真实转化/利润学习）— 本 Entry 不改公式。

---

## 14. Pricing Reality

| Class | Examples | Role |
|-------|----------|------|
| A. True market Paid Price | **None** | N/A |
| B. Listing Price (platform) | Not published | N/A |
| C. Paid Price | None | N/A |
| D. AI Recommended Price | Entry 057 ontology / experimental rec | Heuristic labeled AI_RECOMMENDED；**not LLM** on 077 |
| E. Pipeline Default | Excel 19.9 / PPT 29.9 / Word 12.9 / PDF 15.9 / digital_template 19.9 / 学习计划 9.9 / AI办公 24.9 | `creator_agent._suggest_price` **HEURISTIC** |
| F. Historical/Test | Legacy pilot 12.9；products 路径历史 99.9 listing avg（diversity LOW） | HISTORICAL / MARKET_REFERENCE≠Paid |
| Hypothesis | a949 **¥9.9** PRICE_HYPOTHESIS | Not market fact |

**禁止：** DEFAULT → MARKET FACT；99.9 → validated price。

**FINDING：** a949 pack 写 9.9，而 CF `pricing.json` 仍可能带 19.9 default — **price inconsistency for human publish**.

---

## 15. Product Reality

| Asset | Class | Notes |
|-------|-------|-------|
| a949d2e47cf1 | **KEEP** REAL Entry 077 | Hypothesis SKU；NOT_PUBLISHED |
| f2f8bab97df8 | **KEEP** historical E2E | Full pack；queue awaiting human；≠ 077 lineage |
| 8523329941d4 | **ARCHIVE/KEEP as legacy pilot** | Attendance；isolated |
| e601c17c6977 | **ARCHIVE** early CF | Incomplete package |
| 75f2feac9b04 / 10ff21f1efee / 3d323bf0de83 / 5f4719b47909 | **INVALIDATE** orphan shells | Empty/incomplete；not reasoning input |

Provenance link Asset→PD→Opp→Signals→Obs：**Yes for a949**.

---

## 16. Publish Reality

### a949d2e47cf1

| Item | Present? |
|------|----------|
| Final product xlsx/zip | Yes（artifact root） |
| 中文标题/描述/卖点 | Yes（HUMAN_PUBLISH_PACK.md） |
| 图片 | Placeholder only |
| price | 9.9 hypothesis（冲突风险） |
| delivery / FAQ / version files | **Missing** vs publish_queue required set |
| publish checklist | Thin |
| internal IDs | Present in pack（内部可接受；对外文案需人工剥离） |
| In publish_queue | **No** |

**Can user publish to 闲鱼?** 技术上可用 zip + 文案草稿人工上架；**正式 package gate 不完整** → **HUMAN_REQUIRED + REPLACE pack completeness**.

### f2f8bab97df8

Fuller package + FAQ/delivery；仍 HUMAN_REQUIRED；cover placeholder；AWAITING_HUMAN_ACTION；evidence 0。

### e601 / 8523 e2e_outputs

e601/8523 **not** under e2e_outputs（8523 在 artifacts + queue）。

---

## 17. Feedback Reality

| Question | Answer |
|----------|--------|
| 真实发布？ | **No** |
| 真实曝光/浏览/想要/咨询/订单/支付/收入/退款？ | **No** |
| 写回 DB？ | **No**（publish_evidence=0；market_events=0） |
| 用于下一轮选品？ | **No** |

APIs exist（`record_publish_evidence`, `market_event_core`, learning router）但 **live unused**.

**NOT IMPLEMENTED as closed loop / NOT STARTED / HUMAN ACTION REQUIRED.**

---

## 18. Learning Reality

- Execution/pattern memory: separate lane exists ≠ commercial success
- Commercial learning: gated ingest **IMPLEMENTED**；production use **NOT_STARTED**
- Feedback_agent CF: stub
- Self-evolution may tweak weights within policy — **not** driven by 闲鱼成交

---

## 19. AI / Cost Matrix

| 阶段 | AI 是否需要 | 当前是否实际调用 AI | AI 用途 | 可否规则替代 | 预计成本 | 是否可能产生付费 API 成本 |
| -- | ------- | ----------- | ----- | ------ | ---: | --------------- |
| 1 采集 | No | No | — | Yes | 0 | No |
| 2 清洗 | No | No | — | Yes | 0 | No |
| 3 关键词发现 | Optional | No | 语义扩展 | Partial | 0 now | **Yes if Planner built+LLM** |
| 4 采集深度 | No | No | — | Yes | 0 | No |
| 5 市场分析 | Optional | No（deterministic signals） | 语义解释 | Mostly yes | 0 | Potential |
| 6 选品 | Optional | No（heuristic） | 复杂判断辅助 | Partial | 0 | Potential |
| 7 定价 | Optional | No（hardcode/heuristic） | WTP 辅助 | Partial | 0 | Potential |
| 8 产品生产 | Optional | No（077 deterministic） | 内容创意 | Yes for Excel templates | 0 | Yes if LLM path |
| 9 质量检查 | No | No | — | Yes | 0 | No |
| 10 发布包 | Optional | No | 文案润色 | Yes | 0 | Potential |
| 11 发布 | No | No | — | Human | 0 | No |
| 12 数据回写 | No | No | — | Yes | 0 | No |
| 13 商业学习 | Optional | No | 异常解释 | Partial | 0 | Potential |

**069B→077 paid AI cost Reality: ¥0.**  
**Paid capability exists** in `0_START/model_bridge.py` + `execution_runtime.py`（DeepSeek/OpenAI）；Current DB `paid_invocation=0`.

---

## 20. Reality Purification Inventory

| Item | Class | Notes |
|------|-------|-------|
| 20 REAL observations + 6 signals + sel + prod + a949 | **KEEP** | Current reasoning + evidence |
| Entry audits 069B–077 + History | **KEEP** | Historical Evidence |
| `_tests/xianyu_entry_*` | **KEEP** | Evidence；≠ live input unless re-imported |
| Legacy archived DB | **ARCHIVE** | Isolated SAMPLE |
| f2f8 / 8523 assets | **KEEP/ARCHIVE** | Not 077 SKU；queue clutter |
| Orphan product dirs 3d32/5f47/10ff/75f2 | **INVALIDATE** | Do not use as reasoning；**DELETE deferred**（禁止本 Entry 删历史证据/未授权删） |
| Bridge test sinks | **KEEP** as test | Not Current DB |
| Scorer weights / min_want=50 / maxRecords=50 | **INVESTIGATE** | Defaults ≠ business truth |
| engagement_signal 0.0 with null views | **INVALIDATE as market fact** | Recompute after view capability |
| 99.9 / 19.9 defaults as “market validated” | **INVALIDATE claim** | Keep numbers as labeled heuristics |
| CF LLM adapter unconfigured | **KEEP** | Prevents accidental paid calls on CF path |

**禁止删除** Entry audit / provenance / execution history / historical evidence。

---

## 21. Critical Findings

1. **闭环未闭合：** Publish 后反馈/学习 **NOT_STARTED**；0 evidence / 0 events。  
2. **view_count COLLECTION GAP：** 扩展不采集；DB 全 NULL；engagement=0.0 易误导。  
3. **IMPLEMENTATION_LIMIT：** maxRecords 50 / maxPages 5 ≠ 商业阈值。  
4. **IMPLEMENTATION_DEFAULT：** min_want_count=50 ≠ 验证阈值；仅分类不过滤删除。  
5. **Keyword：** 人工；AI Query Planner **NOT IMPLEMENTED**。  
6. **6→1 Opportunity：** keyword 聚合规则，非智能选品多样性。  
7. **PM/Gantt：** HYPOTHESIS；不得当 DIRECT_EVIDENCE。  
8. **Scorer：** 启发式权重；**MODEL REBUILD REQUIRED**（未来）— 未改。  
9. **Pricing：** 硬编码默认 + 假设价；**无 Paid Price**；a949 9.9 vs 19.9 冲突。  
10. **a949 Publish Pack PARTIAL：** 可人工参考，但缺 FAQ/delivery、无 queue、封面占位。  
11. **Orphan shells** 污染 artifacts 目录（INVALIDATE）。  
12. **Paid LLM surface idle** but real if Core OS ModelBridge routed。

---

## 22. Recommended Rebuild Order

（建议顺序 only — **本 Entry 不执行**）

1. Human publish a949 + record publish_evidence（商业结果优先）  
2. Define feedback capture path（inquiry/order/revenue）→ market_events  
3. view_count collection redesign（若页面可得）或明确 UNAVAILABLE 语义  
4. Publish pack completeness for a949 + queue entry  
5. Keyword / depth policy as **business-reviewed** params（勿 silently raise 50）  
6. Selection/pricing model rebuild **after** real outcomes exist  
7. Cleanup INVALIDATE orphans（授权删除 Entry）  
8. Multi-platform schema only when needed

---

## 23. STOP / GO Decision

| Decision | Value |
|----------|-------|
| Entry 078 Audit | **GO complete**（READ-ONLY done） |
| Enter structural rebuild now | **STOP** until ChatGPT prioritizes next Entry |
| Claim closed loop complete | **STOP / FAIL claim** — loop open after publish |
| Auto-publish / paid AI for next step | **STOP** without explicit authorization |

**GO for：** Human External Publish using existing Asset + pack（with known gaps）.  
**STOP for：** silent threshold changes, scorer rewrite, DB migration, Entry 079 without instruction.

---

## 24. Evidence List

| Evidence | Path |
|----------|------|
| Extension | `1_DATA/browser_extension/xianyu/content.js`（maxRecords/parseWant/no view） |
| Bridge | `1_DATA/connectors/xianyu_extension_bridge_065.py` |
| Filter default | `1_DATA/connectors/xianyu_entry_068_pipeline.py` DEFAULT_FILTER |
| Filter engine | `1_DATA/acquisition_engine.py` FILTER_* |
| 070 result | `1_DATA/_tests/xianyu_entry_070/filter_candidate_result.json` |
| Signals | `1_DATA/market_signal_core.py`；DB `market_signals` |
| Opportunity | `3_DECISION/opportunity_discovery.py` |
| Scorer/weights | `3_DECISION/scorer.py`；`8_CONFIG/config.py` |
| Pricing | `11_CONTENT_FACTORY/agents/creator_agent.py`；`3_DECISION/price_intelligence.py` |
| DB | `data/ai_factory.db` read-only counts/NULLs |
| Legacy DB | `99_ARCHIVE/database_history/ai_factory_legacy_simulation_20260830.db` |
| Product Asset | `11_CONTENT_FACTORY/artifacts/products/a949d2e47cf1/` |
| Publish pack | `commercial_assets/e2e_outputs/a949d2e47cf1/` |
| Prior audits | `docs/07_AUDIT/ENTRY_069B…` … `ENTRY_076…`；`AI_FACTORY_OS_FIRST_REAL_XIANYU_PRODUCT_PRODUCTION_2026-09-05.md` |

---

## Acceptance Checklist

- [x] Extension / Keyword / maxRecords·Pages / want / view  
- [x] DB Reality  
- [x] 069B→077 provenance  
- [x] Selection / Pricing / Product / Publish / Feedback / Learning / AI cost  
- [x] Cleanup inventory KEEP/ARCHIVE/INVALIDATE/DELETE（DELETE deferred）  
- [x] No Runtime/DB/Asset mutation in investigation  
- [x] Audit written  
- [ ] Execution History / necessary Current State / Git — completed in closeout steps  

**Status: PASS_WITH_FINDINGS**
