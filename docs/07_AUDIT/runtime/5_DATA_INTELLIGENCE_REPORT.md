# Data Intelligence Flow Report

> Entry 038-A | 数据流审计

---

## 数据流总览

```
[数据来源 A — 市场 Excel]
data/raw/xianyu/*.xlsx
  ↓ pandas read (需安装 pandas)
1_DATA/collector.py — XianyuCollector.collect_from_excel()
  ↓ normalize_row()
1_DATA/database.py — insert_product(), upsert_keyword()
  ↓
data/ai_factory.db — products, keywords, collection_log
  ↓
3_DECISION/scoring_agent.py — score_product()
  ↓
data/ai_factory.db — scores
  ↓
3_DECISION/decision_engine.py — decide_scored()
  ↓
6_EXECUTION/publisher.py — local output/*.json
  ↓
7_MEMORY/memory_core.py — pattern/strategy learning


[数据来源 B — 商业 JSON]  ← 与 A 无 Python 连接
commercial_assets/opportunity_candidates/
commercial_assets/opportunities/
commercial_assets/experiments/
commercial_assets/production_requests/
  ↓ 人工辅助 + ID 引用
11_CONTENT_FACTORY/adapter/ — 仅读取 PR + Approval
  ↓
11_CONTENT_FACTORY/artifacts/
commercial_assets/product_assets/  ← 人工登记
```

---

## 必答问题

### 当前是否存在数据采集模块？

**✅ 是 — 有限实现**

| 项 | 详情 |
|----|------|
| 模块 | `1_DATA/collector.py` — `DataAgent` / `XianyuCollector` |
| 数据源 | `data/raw/xianyu/` 下 `.xlsx` 文件 |
| 触发 | OS DAG `data` node（task 作为 keyword） |
| 限制 | 无爬虫/API；无 pandas 时返回 error；Excel 不存在时 fallback 读 DB 已有数据 |
| 证据 | `collector.py` L28–88 |

---

### 当前是否存在市场数据输入？

**✅ 部分存在 — 两套独立输入**

| 输入类型 | 位置 | 用途 |
|----------|------|------|
| SQLite 商品数据 | `data/ai_factory.db` products 表（**61 rows**） | OS 评分/决策 |
| Excel 原始数据 | `data/raw/xianyu/`（审计时 glob 不可见，可能 gitignore） | 采集入库 |
| commercial_assets | opportunities/experiments JSON | 商业实验设计 |
| CF MarketAgent | keyword 启发式 | CF Legacy pipeline only |

**❌ 不存在：** 实时市场 API、淘宝/闲鱼 live 抓取、Observation 反馈回写 DB

---

### 当前是否存在评分系统？

**✅ 是 — 两套评分语义**

| 系统 | 位置 | 维度 | 范围 |
|------|------|------|------|
| OS Scorer | `3_DECISION/scorer.py` | hot, trend, comp, profit, difficulty | 0–100 total → SQLite scores（**519 rows**） |
| CF QualityAgent | `11_CONTENT_FACTORY/agents/quality_agent.py` | quality, commercial, content, usability, market, selling | 0–100 → product dict |
| Commercial Selection | JSON `selection_score` in opportunity_candidates | 人工/规则登记 | 文档层 |

**无统一评分 Source of Truth**

---

### 当前是否存在决策系统？

**✅ 是 — OS Decision 存在；Commercial Decision 为 JSON 人工流程**

| 决策 | 实现 | 输入 |
|------|------|------|
| OS Decision | `3_DECISION/decision_engine.py` | SQLite scored products |
| Experiment Selection | JSON `experiment_selection_records_v1.json` | 人工 assisted |
| Experiment Review | JSON `experiment_reviews_v1.json` | human_assisted approve/reject |
| PR Approval | JSON `production_request_reviews_v1.json` | human_assisted |
| CF Release Gate | `release_gate.py` | product quality/packaging |

---

### 当前是否存在内容生产连接？

**⚠️ 部分 — CF 独立；与 OS 数据链未连接**

| 连接 | 状态 |
|------|------|
| OS Decision → CF Production | ❌ |
| SQLite market data → CF input | ❌ |
| commercial_assets PR → CF Adapter | ✅ Pilot only |
| CF output → commercial_assets Product Asset | ❌ 自动（人工 Entry 写入） |
| CF output → SQLite | ❌ |

---

## Database 数据流（Operational Data）

| 表 | 行数 | 写入模块 | 读取模块 |
|----|------|----------|----------|
| platforms | 1 | database.ensure_schema | collector |
| products | 61 | collector → insert_product | scoring_agent, decision |
| keywords | 6 | upsert_keyword | collector |
| collection_log | 29 | start/finish_collection_log | — |
| scores | 519 | save_score | decision_engine, get_top_scored |
| trends | 0 | **无 Python 写入** | — |
| audit_log | 1 | **无 Python 写入** | — |

**Schema 漂移：** `trends`、`audit_log` 表存在于 DB，但 `database.py ensure_schema()` **未定义**；`platforms` 实际列（base_url, status）与 ensure_schema 定义（id, name）不一致。

---

## 2_COGNITION 数据流

**❌ 不存在** — 目录为空；Blueprint 规划的 TrendAgent/DemandAgent 等 **零代码**。

市场理解实际发生在：
1. `1_DATA` — 历史商品数据
2. `11_CONTENT_FACTORY/market_agent.py` — keyword 规则（Legacy path）

---

## 结论

| 能力 | 存在 | 连接 OS | 连接 CF | 连接 Commercial JSON |
|------|------|---------|---------|---------------------|
| 数据采集 | ✅ 有限 | ✅ | ❌ | ❌ |
| 市场数据 | ✅ SQLite | ✅ | ❌ | 文档 only |
| 评分 | ✅ 双系统 | ✅ OS | ✅ CF | JSON selection_score |
| 决策 | ✅ OS + JSON | ✅ OS | ❌ | 人工 JSON |
| 内容生产 | ✅ CF | ❌ | ✅ | Adapter 只读 PR |

**核心缺口：** Data Intelligence（1+3）与 Content Factory（11）及 Commercial Assets **三条数据流平行，无 Runtime 汇聚点**。
