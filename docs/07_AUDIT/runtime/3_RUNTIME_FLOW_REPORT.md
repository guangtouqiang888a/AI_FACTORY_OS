# Runtime Flow Map

> Entry 038-A | Python import 与调用链分析（代码事实）

---

## Flow A — Core OS Pipeline（0_START 主链）

```
入口: 0_START/main.py 或 10_DEPLOY/api.py POST /run
↓
模块: 0_START/controller.py — SystemController.run(task)
↓
函数: SelfEvolutionEngine.evolve(policy)
↓
输出: evolution patch dict
↓
模块: 0_START/planner.py — Planner.plan()
↓
函数: _build_dag() → nodes: data → scoring → decision → execution
↓
输出: dag + complexity
↓
模块: 0_START/policy_engine.py — PolicyEngine.evaluate_pipeline() / apply_dag_policies()
↓
输出: approved dag + per-node policy (executor: rule|deepseek|gpt)
↓
模块: 0_START/execution_runtime.py — ExecutionRuntime.execute_dag()
↓
函数: execute_node() × 4（topological order）
↓
```

### Node: data

```
模块: 1_DATA/collector.py — DataAgent.execute()
↓
函数: XianyuCollector.collect(keyword)
↓
调用: 1_DATA/database.py — upsert_keyword, insert_product, get_products_by_keyword
↓
输出: {keyword, products[], data_result, product_count}
```

### Node: scoring

```
模块: 3_DECISION/scoring_agent.py — ScoringAgent.execute()
↓
函数: scorer.score_product() × N products
↓
调用: 1_DATA/database.save_score()
↓
输出: {keyword, products[] with scores, count}
```

### Node: decision

```
模块: 3_DECISION/decision_agent.py — DecisionAgent.execute()
↓
函数: decision_engine.decide_scored()
↓
调用: 3_DECISION/risk_engine.assess_risk(); 7_MEMORY/memory_core.load_runtime_policy()
↓
输出: {action: publish|observe|skip, reason, candidates, best}
```

### Node: execution

```
模块: 6_EXECUTION/execution_agent.py — ExecutionAgent.execute()
↓
函数: publisher.publish(decision)
↓
输出: {status: skipped|published_local, path?} → output/*.json
```

### Post-pipeline Memory

```
模块: 7_MEMORY/memory_core.py
↓
函数: extract_pattern(ctx) → update_strategy(pattern) → write_event()
↓
输出: pattern dict, strategy rules, event_log.jsonl append
```

---

## Flow B — Content Factory Legacy Pipeline（keyword）

```
入口: python 11_CONTENT_FACTORY/pipeline/content_pipeline.py [keyword]
↓
模块: ContentPipeline.run(keyword, platform="xianyu")
↓
函数: MarketAgent.execute()
↓
输出: {category, market_score, competition, recommendation}
↓
函数: CreatorAgent.execute()
↓
输出: DigitalProduct dict + artifact scaffold
↓
函数: ProductGeneratorAgent.execute()
↓
调用: excel_generator / ppt_generator / word_generator / pdf_generator / cover_generator
↓
输出: artifact_path, artifact_files[]
↓
函数: validate_artifacts()
↓
函数: QualityAgent.execute()
↓
输出: quality_score, commercial_score, status
↓
函数: PackagingAgent.execute()
↓
输出: zip_path, publish_package files
↓
函数: ReleaseGateAgent.execute()
↓
输出: release_status
↓
函数: ContentPipeline._save_product()
↓
输出: 11_CONTENT_FACTORY/storage/product_memory.json append
```

---

## Flow C — Content Factory Adapter Pipeline（Production Request）

```
入口: python 11_CONTENT_FACTORY/adapter/adapter_runner.py --preq <id> [--execute]
↓
模块: adapter_runner.run_adapter()
↓
函数: ProductionRequestLoader.load_input_package()
↓
读取: commercial_assets/production_requests/production_requests_v1.json
       commercial_assets/production_request_reviews/production_request_reviews_v1.json
↓
函数: ApprovalGate.validate() — pilot whitelist: preq_20260712_005 only
↓
函数: input_mapper.map_production_request_to_input()
↓
函数: ContentPipeline.run_from_production_request(input_package, dry_run=not --execute)
↓
  [MarketAgent SKIPPED — trace step status=skipped]
↓
  CreatorAgent → ProductGeneratorAgent → validate_artifacts_experiment()
  → QualityAgent → PackagingAgent → ReleaseGateAgent → _save_product()
↓
函数: output_mapper.map_pipeline_result_to_product_asset()
↓
输出: product_asset_draft dict（**不写 commercial_assets/**）
```

**注意：** `ProductAssetValidator` **不在 adapter_runner 调用链中**；Validation Gate 为独立 CLI/测试路径。

---

## Agent Registry 对照

| Agent 名称 | 框架 | 注册位置 | 是否在主链运行 |
|------------|------|----------|----------------|
| DataAgent | OS BaseAgent | 0_START/agent_runtime | ✅ OS DAG |
| ScoringAgent | OS BaseAgent | 0_START/agent_runtime | ✅ OS DAG |
| DecisionAgent | OS BaseAgent | 0_START/agent_runtime | ✅ OS DAG |
| ExecutionAgent | OS BaseAgent | 0_START/agent_runtime | ✅ OS DAG |
| MarketAgent | ContentAgent | ContentPipeline.__init__ | ✅ CF Legacy only |
| CreatorAgent | ContentAgent | ContentPipeline | ✅ CF |
| ProductGeneratorAgent | ContentAgent | ContentPipeline | ✅ CF |
| QualityAgent | ContentAgent | ContentPipeline | ✅ CF |
| PackagingAgent | ContentAgent | ContentPipeline | ✅ CF |
| ReleaseGateAgent | ContentAgent | ContentPipeline | ✅ CF |
| FeedbackAgent | ContentAgent | agents/__init__ export | ❌ 未接入 pipeline |
| PublishAssistantAgent | ContentAgent | agents/__init__ export | ❌ 未接入 pipeline |

---

## 跨链连接（已确认 / 未确认）

| 连接 | 状态 | 证据 |
|------|------|------|
| 0_START → 11_CONTENT_FACTORY | ❌ 未连接 | 全 repo 无 import |
| 0_START → commercial_assets | ❌ 未连接 | 无 Python 读取 |
| 3_DECISION → commercial_assets | ❌ 未连接 | decision_engine 仅读 SQLite |
| 11 adapter → commercial_assets | ✅ 只读 | production_request_loader.py |
| 11 adapter → product_assets JSON 写入 | ❌ 未连接 | output_mapper 注释明确不写 |
| 1_DATA → 11_CONTENT_FACTORY | ❌ 未连接 | 无共享数据流 |

---

## Broken / Unreachable Entry Points

| 入口 | 问题 |
|------|------|
| `9_PRODUCT/api_server.py` | `from 0_START.controller` — SyntaxError |
| `0_START/self_healing_engine.py` | `from 7_MEMORY.memory_core import write_memory` — SyntaxError + API 不存在 |

---

## Planner / Policy / Execution 关系

```
Planner: 仅构建 DAG 结构，不做策略决策
↓
PolicyEngine: 评估 pipeline 是否 approved；为每 node 分配 executor
↓
ExecutionRuntime: 唯一执行入口；deterministic mode 强制 rule executor
↓
ModelBridge: 仅当 policy executor ≠ rule 且 budget 允许时附加 llm_insight
```

**当前 DETERMINISTIC_MODE=True**（config.py）→ 所有 node 实际以 **rule executor** 运行。
