# ENTRY 080-A — Xianyu P2-A Data Foundation Reality Audit

**Date:** 2026-09-05  
**Entry ID:** **080-A**  
**Project:** Xianyu Commercial Closed-Loop Project  
**Result:** `PASS_WITH_FINDINGS`  
**AI Cost:** **¥0**  
**DB Impact:** **NO DB WRITE**（read-only `file:...?mode=ro`）  
**Runtime Impact:** **NONE**

> Cursor Process Output ≠ Formal Audit ≠ Current State ≠ ChatGPT Closure Review.  
> P2-A = Reality Audit only. **P2 implementation = NOT STARTED.**

---

## Original Objective

建立真正能够跑通的闲鱼商业闭环：真实市场 → 采集 → 数据基础 → 分析 → 选品 → 定价 → 生产 → 质量门 → 中文发布包 → 人工发布 → 真实反馈 → 回写 → 学习 → 下一轮。

## Current Objective

在进入任何 P2 Data Foundation 实现之前，先用 **当前代码 + 当前 DB + 当前真实数据 + 当前资产** 回答：数据在哪、schema 是什么、20 条 observation 可用字段、view/want Reality、run/dedupe/provenance/keyword 缺口，以及 P2 该修什么 / 不该修什么。

## Scope

- READ-ONLY SQLite：`data/ai_factory.db`  
- Collector / Extension / importer / bridge / normalization（只读）  
- Historical page dumps & extension raw batches（对照，非 live 外部操作）  
- Formal Audit + Execution History + 必要 Continuity 指针  
- Git commit / push / remote verification  

## Out of Scope

修改 Python/JS/Extension；ALTER/INSERT/UPDATE/DELETE；migration；新建 schema；改 scoring/pricing/collection depth/keyword planner/publish；付费 AI；闲鱼外部操作；改 `a949d2e47cf1`；实施 P2-B；进入 P3。

## Reality Sources

| Source | Role |
|--------|------|
| `data/ai_factory.db`（ro） | Current DB Reality |
| `1_DATA/market_source_core.py` / `1_DATA/database.py` | Schema / insert / dedupe code |
| `1_DATA/browser_extension/xianyu/content.js` | Live collection parser（069 path） |
| `1_DATA/connectors/xianyu_market_observation_import_066.py` | Import gate |
| `1_DATA/connectors/xianyu_browser_connector.py` | Legacy browser path（非 20-obs 主链） |
| `1_DATA/_tests/xianyu_extension_065/raw/run_1788419997563.json` | Provenance raw for 20 REAL obs |
| `1_DATA/_tests/xianyu_search_session_063/page_dump_Excel*.html`（及 062 dumps） | Stored DOM Reality for search cards |
| Entry 069A / 069B / 078 | Prior Reality Audits |
| `99_ARCHIVE/database_history/` | Historical DB **对照 only** — **≠ Current Reality** |

---

## Database Schema Reality

**DB:** `D:\AI_FACTORY_OS\data\ai_factory.db`  
**PRAGMA foreign_keys:** **0**（未启用）  
**Declared FK（PRAGMA foreign_key_list）：** **全部表为空** — 仅有逻辑关联（如 `run_id` 字符串），无 enforced FK。  
**Table count:** **19**

| Table | Columns (summary) | PK | Declared FK | Row Count | Current Role |
|-------|-------------------|----|-------------|----------:|--------------|
| `market_observations` | id, observation_id, run_id, source_id, source, platform, source_type, source_item_id, source_url, title, category, price, currency, view_count, want_count, comment_count, share_count, seller_reference, published_at, observed_at, raw_reference, data_origin, verification_status, collector_version, normalizer_version, content_hash, dedupe_key, product_category, opportunity_product_type, notes, created_at | `id` + UNIQUE `observation_id` + UNIQUE(`source`,`dedupe_key`,`observed_at`) | none | **20** | **Current commercial observation store（唯一有 REAL 市场卡数据）** |
| `collection_runs` | run_id UNIQUE, source*, platform, collection_mode, counts, collection_query, acquisition_mode, raw_*, status, timestamps… | `id` | none | **14** | Run metadata；与 obs 逻辑关联 `run_id` |
| `collection_log` | task_date, platform_id, keyword, totals, status, timestamps | `id` | none | **14** | **Legacy** parallel log（多条仍 `running` / totals=0） |
| `keywords` | keyword UNIQUE, category, dates, flags | `id` | none | **0** | Table exists；**无真实 rows** |
| `platforms` | name UNIQUE | `id` | none | **2** | `xianyu`, `taobao` seed |
| `market_sources` | source_id, platform, modes, notes… | `id` | none | **4** | Source registry（xianyu enabled） |
| `market_signals` | signal_id, type, keyword, evidence_refs… | `id` | none | **6** | Downstream of 20 obs（073） |
| `selection_results` | selection_id, candidate_id, score, evidence_refs, payload… | `id` | none | **1** | Opp selection lineage |
| `products` | legacy listing-shaped columns incl. want/view | `id` | none | **0** | **Unused** for current closed-loop |
| `publish_queue` | product_asset_id, package_path, queue_status… | （schema as-is） | none | **2** | Legacy pilot / e2e queue（≠ a949） |
| `publish_evidence` | — | — | none | **0** | Closed-loop feedback empty |
| `market_events` | — | — | none | **0** | Closed-loop events empty |
| `collectors` | collector_id, source_id, mode, version… | `id` | none | （registry） | Collector registry |
| `scores` | product_id, hot/trend/… | `id` | none | **0** | Legacy scorer store unused |
| `acquisition_policy` / `acquisition_tasks` / `market_acquisition_policies` / `ai_cost_estimates` / `ai_execution_records` | policy/task/cost tables | — | none | small | Acquisition governance / cost gate |

**Not present as DB tables:** `opportunities`, `opportunity_candidates`, `product_definitions` — 商业对象主要在 JSON/filesystem / selection payload，而非独立表。

### Notable field Reality on `market_observations`

| Concern | Present? |
|---------|----------|
| timestamp (`observed_at` / `created_at`) | Yes |
| source / platform | Yes |
| keyword / query as column | **No**（query 在 `notes` JSON + `collection_runs.collection_query`） |
| product/item id | Yes `source_item_id`（20/20） |
| URL | Yes（20/20） |
| price | Yes（20/20） |
| want_count | Yes column；14/20 non-null |
| view_count | Yes column；**20/20 NULL** |
| title | Yes（20/20） |
| image | **No DB column**（raw batch 有 `image_url`；未入表） |
| position | **No DB column**（raw 有 `result_position`；未入表） |
| collection run ID | Yes `run_id` |
| provenance path | `raw_reference` + `notes` |
| confidence / evidence level | **Partial：** `data_origin` + `verification_status`；**无 formal evidence_level enum 列** |

---

## Observation Reality

**Total rows:** **20**  
**All** `data_origin=REAL` · `verification_status=MANUAL_VERIFIED`  
**Single run:** `crun_378745ca45e0`（query=`Excel模板`，acquisition_mode=`BROWSER_EXTENSION`）  
**Raw:** `1_DATA/_tests/xianyu_extension_065/raw/run_1788419997563.json`

### Completeness rates（Current DB）

| Field | Non-null rate | Notes |
|-------|--------------:|-------|
| title / price / URL / source_item_id / observed_at | **100%** | Commercial-usable identity + price |
| want_count | **70%**（14/20） | 6 NULL；**0 zeros** |
| view_count | **0%**（0/20） | Column reserved only |
| category / seller / comment / share / published_at | **0%** | Empty |
| image_url / result_position / want_count_status / query | **N/A as columns** | Present in raw/notes，非一等公民列 |

### Want values（non-null）

`2245, 1930, 1082, 660, 642, 436, 186, 26, 25, 14, 7, 3, 3, 1`  
（与 070 MATCH≥50 子集一致：2245…186）

### Duplicate rate（within current 20）

| Key | Unique | Dup groups |
|-----|-------:|----------:|
| source+source_item_id | 20 | 0 |
| source_url | 20 | 0 |
| title+price | 20 | 0 |
| observation_id | 20 | 0 |

### 20 条真实 observation **可用于商业分析的字段**

**可用（DB 一等字段）：**

- Identity：`source_item_id`, `source_url`, `title`, `price`, `currency`, `platform`, `source`
- Demand proxy：`want_count`（部分缺失）
- Time：`observed_at`
- Provenance soft：`data_origin`, `verification_status`, `run_id`, `raw_reference`, `collector_version`
- Dedupe：`dedupe_key`, `content_hash`

**可用但埋在 `notes` JSON（非列）：**

- `query`（Excel模板）, `want_count_status`, `result_origin=SEARCH_RESULT`, `session_id`

**Raw 有、DB 未落列：**

- `image_url`, `result_position`

**不可用 / 不可当作事实：**

- `view_count`（全 NULL）
- engagement 若用 view 合计 → 易伪 0（见 078）
- `products` 表（0 行）≠ 这些 observations

---

## View Count Investigation

### A–C. Search / card / detail（基于 **已保存 Reality**，本 Entry **未**做闲鱼外部 live 操作）

| Probe | Evidence | Result |
|-------|----------|--------|
| Search page DOM dumps（062/063 `page_dump_Excel*.html`） | `人想要` 出现多次；`浏览` / `浏览量` / `人看过` / `viewCount` / `views` = **0** | Search cards：**无稳定 view 文本** |
| Live extension batch `run_1788419997563.json` | 记录无 `view_count` 字段 | 未采集 |
| `content.js` | **无** view/浏览 parser；仅 `parseWant` | Parser gap + page 可能本身无字段 |
| Legacy `xianyu_browser_connector._safe_int_labeled(..., ("浏览","浏览量"))` | 代码存在；060 dump 中「浏览」仅出现在 **anti-bot「请使用正常浏览器」**，非 view metric | 不可当作已验证可得 |
| Detail page | 062 有 want detail probe；**无**已验证 view-on-detail 证据资产 | Detail view = **未证实** |

### D. Extension unused fields?

扩展 **未采集** view；raw 也无隐藏 view 字段可“漏解析”。

### E. Detail-page request?

若未来要 view：可能需详情页 — **仅记录设计风险**（成本、anti-bot、登录态、DOM 不稳定）；**本 Entry 不实施**。

### F. Risks（记录）

登录态 / anti-bot / dynamic class names（`feeds-item-wrap`、`text--*`）/ dump 过期 vs 今日 DOM — 均存在。

```text
VIEW_COUNT_STATUS = NOT_STABLELY_AVAILABLE
```

（语义：在 **当前主路径 = 搜索结果卡 + Extension** 下，基于存储 DOM + raw + 代码，view **不能**作为稳定可采集事实。详情页是否可得 = **未证实**，不得写成 `DETAIL_PAGE_AVAILABLE`。）

---

## Want Count Investigation

| Item | Reality |
|------|---------|
| Parser | Extension：`/(\d+)\s*人想要/`；browser connector 另有更宽 regex |
| DOM dumps | `人想要` **存在**（与 parser 一致） |
| DB | 14 non-null / 6 null / **0 个 0** |
| NULL | **合理** — `want_count_status=MISSING_ON_CARD`（存于 notes）；**NULL ≠ 0** |
| 0 | 当前真实 20 条中 **未出现**；代码允许真实 0（test fixtures） |
| 非数字 / 文案变化 | dumps 未见替代文案；若平台改文案则 MISSING 上升 — 风险记录 |
| 价格混淆 | price 来自 `number--`/`decimal--` 节点；want 来自全文 regex — 分离设计 |
| 错位 | 按 card 作用域解析；未见本批错位证据 |

**结论：** want 是当前 **主要可用 demand 字段**；缺失必须保留 NULL。

---

## Keyword Reality

| Question | Answer |
|----------|--------|
| `keywords` table exists? | **Yes** |
| Real rows? | **0** |
| Linked to observations? | **No FK / no join** |
| Query storage? | **String**：`collection_runs.collection_query` + obs `notes.query` + signals `keyword` |
| Seed vs discovered? | **Not modeled** |
| Hypothesis vs fact keyword? | **Not modeled** |
| AI Query Planner | **NOT IMPLEMENTED**（P3；本 Entry 不实现） |

---

## Collection Run Reality

1. **Run 定义：** `collection_runs.run_id`（如 `crun_378745ca45e0`）；含 mode、query、counts、raw_reference。  
2. **与 observations：** `market_observations.run_id` → 当前 **20/20** 指向同一 run。  
3. **Query：** run 列 `collection_query`；obs 无列，在 notes。  
4. **Page：** extension stats（pages/scroll）在 raw batch；**DB 无 page 列**。  
5. **Time：** run `started_at`/`finished_at`；obs `observed_at`。  
6. **maxRecords/maxPages：** 主要在 collector/extension **config**（如 maxRecords≤50 — 078）；**非** observation 表字段；run 不完整记录“为何采这么深”。  
7. **Adaptive depth：** **当前不支持**（缺重复率/信息增益/深度元数据契约）。  
8. **混杂：** 14 runs — 多条早期 BROWSER_EXTENSION 小 batch（手机壳等）`accepted_count>0`，但 **Current observations 仅保留 Excel 20 条**；`collection_log` 多条停在 `running`/totals=0 → **stale / incomplete log hygiene**。

---

## Dedup Reality

| Layer | Mechanism | Scope |
|-------|-----------|-------|
| Extension `globalSeen` | id → url → `title|price` hash | **单次 scrape session** |
| DB insert | `UNIQUE(source, dedupe_key, observed_at)` | **Exact same observed_at** = duplicate |
| `make_dedupe_key` | prefer `item:{source}:{id}` else url hash else title\|price hash | Insert-time |
| Index `idx_mobs_source_item` | **非 UNIQUE** | 允许同 item 多时间点 |

**跨时间同一商品：** 代码注释明确 — 不同 `observed_at` = **新行（历史）**，**不**被当作 duplicate。  
**风险：** 若时钟/observed_at 被错误复用，会误判 duplicate；反之反复采集会膨胀行数 — P4 相关，非本 Entry 修改。

---

## Provenance / Evidence Reality

| Capability | Current |
|------------|---------|
| TEST / SAMPLE / SIMULATION / REAL | `data_origin` 枚举支持；Current 20 = **REAL** |
| MANUAL_VERIFIED | `verification_status` |
| REAL_MARKET_STATISTICS / USER_BEHAVIOR / ORDER / PAYMENT | **MISSING_CAPABILITY**（无 formal evidence_level 列） |
| Formal evidence-level field | **MISSING_CAPABILITY** — **不要现在加字段**（P2-B 再决定） |

---

## Platform Neutrality

模型接近：`market_sources` → `collection_runs` → `market_observations`（source/platform 列）。  

但：

- want 语义（「人想要」）与 Xianyu DOM class **硬编码在 Extension**  
- legacy `products`/`keywords` 偏单平台 listing  
- **足够做“平台字段隔离”的起步，不足以称多平台成熟**

目标不是现在做多平台 — 仅记录。

---

## Historical Data Boundary

| Class | Objects | Treat as |
|-------|---------|----------|
| **当前可用** | 20 REAL obs + run `crun_378745ca45e0` + 6 signals + 1 selection + asset `a949` | Current closed-loop lineage |
| **历史参考** | 其它 collection_runs；publish_queue pilots；062/063 dumps | Reference only |
| **不可作为当前商业事实** | TEST/SAMPLE/SIMULATION；空 `keywords`/`products`；view_count NULL；legacy hypothesis prices；ARCHIVE_LOGICAL_ONLY assets（079-D） | Must not upgrade |

**本 Entry 未删除任何数据。**

---

## Capability Gap Matrix

| Capability | Current Reality | Evidence | P2 Required? | Priority | Safe Change |
|------------|-----------------|----------|--------------|----------|-------------|
| Observation storage | Working（20 REAL） | DB | Soft（harden contract） | P1 | Docs / optional additive cols later |
| Want count | Partial 70%；parser OK | DB+DOM+ext | Soft（status first-class?） | P1 | Prefer persist `want_count_status`；**不**把 NULL→0 |
| View count | Column empty；search **NOT_STABLELY_AVAILABLE** | dumps+ext+DB | **Yes（decide semantics）** | **P0** | Mark UNAVAILABLE in analytics；**勿假装已采集**；详情方案仅设计 |
| Keyword object | Table empty；query=string | DB | Soft | P2 | Populate/link later；**Planner = P3** |
| Provenance | origin+verification+raw_ref | DB | Soft | P1 | Document contract |
| Evidence level | MISSING_CAPABILITY | code/schema | Decide in P2-B | P2 | Additive only if needed |
| Collection run | Exists；depth metadata weak；log stale | DB | Soft | P1 | Hygiene + depth fields design |
| Deduplication | Session + DB triple-key | code | Soft（document） | P2 | No behavior change without P4 |
| Platform | Partial neutrality | schema | No multi-platform now | P3+ | Keep source/platform columns |
| Timestamp | OK | DB | No | — | — |
| Source | Registry + columns | DB | No | — | — |

---

## P2 Recommended Scope（给 P2-B 决策；本 Entry 不实施）

1. **Observation Field Contract** — 明确哪些字段是一等列 vs notes/raw。  
2. **View_count 政策** — 在 search 路径标记 `NOT_STABLELY_AVAILABLE`；engagement **禁止**把 NULL view 当 0 市场成功。  
3. **可选最小 schema（仅若 P2-B 授权）：** additive columns 如 `collection_query`, `want_count_status`, `image_url`, `result_position` — **无破坏性 migration**。  
4. **collection_log / orphan runs hygiene 设计**（只读评估 → 另授权清理）。  
5. **Keyword 表与 query 字符串对齐策略（无 AI Planner）。**

## Explicitly Not Recommended（P2 不做）

- 改 scorer / threshold / pricing / keyword planner  
- 改 collection depth / maxRecords 作为“伪 foundation”  
- 改 browser extension 大规模重写（除非专条授权 view 探测）  
- 改 publish pack / 生产新产品 / 发布 / 外部闲鱼操作  
- 把 Blueprint 当 schema；把 historical DB 当 Current  

---

## Findings

1. Current 商业数据核在 **`market_observations` 20 REAL**，非 `products`/`keywords`。  
2. **view_count：** schema 有、数据无、search DOM dumps 无稳定标签 → `NOT_STABLELY_AVAILABLE`。  
3. **want_count：** 真实可用但不完整；NULL 必须保留。  
4. Query/image/position/want_status **采集过但 DB 建模不完整**。  
5. `keywords=0`；Planner 未实现。  
6. Dual logging：`collection_runs` vs stale `collection_log`。  
7. Dedup 允许跨时间同 item 多行 — 正确历史语义，但未支撑 Adaptive Depth。  
8. Evidence-level 细分类 **MISSING_CAPABILITY**。  
9. Schema **不足以**无脑支撑 P3–P5 全部野心，但 **够**支撑在明确 view/want 语义下继续选品实验 — 前提是不误读 engagement。

## Decisions

- P2 **STARTED** at Audit layer only.  
- **P2 implementation NOT STARTED.**  
- No schema change in 080-A.  
- VIEW_COUNT_STATUS locked as above until new live DOM evidence Entry.

## Pending

- ChatGPT Closure Review  
- P2-B scope authorization  
- Optional live DOM re-probe Entry（另授权；≠本 Entry）

## Next Step

**STOP — 等待 ChatGPT 根据本 Audit 决定 P2-B。** 不实施 view_count，不扩采集，不进 P3。

## Stop Conditions

任何未经授权的 DB/Runtime 修改 → `FAIL_SCOPE`。

## AI Cost

**¥0**

## Runtime Impact

**NONE**

## DB Impact

**NO DB WRITE**

## Git Commit / Push / Remote Verification

| Field | Value |
|-------|-------|
| Git Commit | `066d2a5f70e897797abc0e8f3db049d57571db2c` |
| GitHub Push | **SUCCESS**（`47e24ec..066d2a5  main -> main`；无 force） |
| Remote Verification | **PASS**（local HEAD == origin/main `066d2a5…`；Audit 在 origin） |

---

## Final Completion Criteria

Audit 回答 §1 全部问题；Capability Gap 完整；推荐/禁止边界清晰；docs/git 同步；无实现副作用。
