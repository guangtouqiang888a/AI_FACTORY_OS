# AI_FACTORY_OS Reality Architecture Alignment Report

> **现实架构对齐审计报告** | Entry **041-A**  
> **Date:** 2026-07-15  
> **Type:** Reality Audit（现实状态审计）— Docs + Code **Read Only**  
> **原则：** Reality > Documentation · Blueprint ≠ Production · Design ≠ Runtime

**约束回执：** 未修改 Python / Database / commercial_assets / Runtime；仅新增本审计报告，并同步 Current State / CURSOR_EXECUTION_HISTORY（Entry 完成记录）。

---

## 执行摘要

| 问题 | 结论 |
|------|------|
| Core OS 与 Content Factory 是否仍双轨？ | **是 — 仍属情况 B（两套独立 Runtime）** |
| 双轨是合理模块拆分还是历史偏移？ | **二者兼有：** 目录上 CF 已标注为「Execution Layer 子系统 / Isolated」属**有意识隔离交付**；但 **Runtime 零连接**使「统一 AI_FACTORY_OS」尚未成立，属**未收敛的架构缺口**（非误建第二公司，亦非已完成模块内拆分） |
| 代码/DB/资产是否符合设计架构？ | **部分符合目标蓝图叙述，Runtime 与商业状态字段严重滞后于文档「完成」话术** |
| 未来是否需要架构调整？ | **需要治理下的明确抉择（永久双轨 vs 授权 Runtime 桥接）**；**不自动开工**；先现实诚实同步再融合 |

**双轨判定标签：** `DUAL_TRACK_CONFIRMED`（情况 B）

---

# 第一部分：当前真实系统结构图

## 1.1 目录 Reality（根目录）

```
AI_FACTORY_OS/
├── 0_START/              Core OS 编排入口（Planner / Policy / Runtime）
├── 1_DATA/               数据采集 + SQLite（database.py）
├── 2_COGNITION/          【空目录】Planned — 0 业务文件
├── 3_DECISION/           评分 / 决策（OS 域）
├── 4_PRODUCT/            【空目录】Planned
├── 5_CONTENT/            【空目录】Planned
├── 6_EXECUTION/          OS 发布执行（本地 JSON 输出）
├── 7_MEMORY/             OS 运行记忆
├── 8_CONFIG/             配置；ACTIVE_MODULES 不含 CF
├── 9_PRODUCT/            Frozen 残留（含损坏 api_server.py）
├── 10_DEPLOY/            FastAPI → SystemController.run()（有效 HTTP）
├── 11_CONTENT_FACTORY/   数字商品生产线 + Adapter（独立入口）
├── commercial_assets/    商业对象 JSON SoT
├── data/ai_factory.db    OS Operational SQLite
├── docs/                 治理 + 蓝图 + 审计
├── output/ · logs/
```

## 1.2 真实运行结构（非设计愿景）

```
【Track A — Core OS Runtime】
  入口: python 0_START/main.py
        或 10_DEPLOY/api.py → SystemController.run(task)
       ↓
  Planner → PolicyEngine → ExecutionRuntime(DAG)
       ↓
  data(1_DATA/SQLite) → scoring → decision → execution(本地 publish)
       ↓
  7_MEMORY 学习更新
  ✗ 不调用 11_CONTENT_FACTORY
  ✗ 不读写 commercial_assets

【Track B — Content Factory + Commercial（Isolated）】
  入口: python 11_CONTENT_FACTORY/adapter/adapter_runner.py --preq <id>
       ↓
  commercial_assets PR/Approval JSON（只读加载）
       ↓
  ApprovalGate → map → ContentPipeline → 产物 / Product Asset 草稿
       ↓
  ✗ 不进入 0_START DAG
  ✗ ProductAssetValidator 未接入 adapter_runner 主链
```

**不是情况 A：** 不存在「OS 主程序内嵌调用 Content Factory 模块」的 Runtime 关系。  
**是情况 B：** 同一仓库、两套入口、两套数据面、两套决策语义。

---

# 第二部分：双轨性质判定

| 维度 | 观察 | 解释 |
|------|------|------|
| 代码边界 | `0_START` / `10_DEPLOY` grep **无** `11_CONTENT_FACTORY`、`commercial_assets` | Runtime 零连接 |
| 配置 | `ACTIVE_MODULES = (0_START, 1_DATA, 3_DECISION, 6_EXECUTION, 7_MEMORY, 8_CONFIG)` | CF 未注册 |
| 数据面 | OS→SQLite products；Commercial→JSON 对象链 | 双 SoT |
| 文档定位 | MODULE_REGISTRY：`11_CONTENT_FACTORY` = Active Isolated；Runtime Integration ❌ | **有意识隔离**（设计已承认） |
| 统一蓝图 | UNIFIED_ARCHITECTURE Phase C = 未来授权融合 | 双轨是**过渡态目标**，非终态宣称 |

### 结论（必须保留）

1. **仍属双轨（情况 B）** — 与 Entry 038-A ISSUE-P0-001 一致，**2026-07-15 复查仍成立**。  
2. **不是「偶然复制粘贴出两个无关项目」** — CF 已通过 Adapter 对接 `commercial_assets`，定位为仓库内隔离生产线。  
3. **也不是「已经完成的合理模块拆分」** — 合理拆分应有明确 Orchestrator/桥接契约的 Runtime；目前只有 **人工 + 文档** 串起商业链与 OS 链。  
4. **性质标签：** `Intentional Isolation + Unfinished Convergence`（有意隔离 + 收敛未完成）。

---

# 第三部分：Python / Runtime Reality

| 入口 | 路径 | 调用什么 | 是否连 CF |
|------|------|----------|-----------|
| CLI OS | `0_START/main.py` | `SystemController` | **否** |
| HTTP | `10_DEPLOY/api.py` | `run_task` → Controller | **否** |
| CF Adapter | `11_CONTENT_FACTORY/adapter/adapter_runner.py` | Pipeline + commercial_assets 读 | **独立** |
| CF Pipeline 直调 | `content_pipeline.py` | 工厂内部 | **独立** |
| 损坏入口 | `9_PRODUCT/api_server.py`、`0_START/self_healing_engine.py` | 非法/错误 import | 不可用 |

**Agent 注册（OS）：** DataAgent / ScoringAgent / DecisionAgent / ExecutionAgent — 均来自 1_DATA / 3_DECISION / 6_EXECUTION，无 CF Agent。

**Validator：** `product_asset_validator.py` 存在；**未**被 `adapter_runner.py` import（Gate≠接主链）。

---

# 第四部分：Database Reality

| 项 | Reality（2026-07-15 探测） |
|----|---------------------------|
| 文件 | `data/ai_factory.db` 存在（约 81920 bytes） |
| 表 | `platforms`, `products`(61), `keywords`(6), `collection_log`(29), `scores`(519), **`trends`(0)**, **`audit_log`(1)** |
| `ensure_schema()` 定义 | 仅 platforms/products/keywords/collection_log/scores；**不建** trends/audit_log |
| platforms 列 | DB 含 `base_url`, `status`；代码 CREATE 仅 `id`,`name` |

**Schema Drift：仍存在（SD-001 类）** — 与 039-A Schema Drift Report 一致。  

**对统一架构影响：**  
- 阻碍「干净新环境 = 现网能力」的可重复部署；  
- **不单独造成** Core↔CF 双轨（双轨主因是无 Runtime 桥）；  
- 未来若 Commercial 写入 SQLite，须先做 Reality Alignment Entry。

---

# 第五部分：commercial_assets Reality

| 对象 | 现实状态（节选） | 与文档叙事冲突 |
|------|------------------|----------------|
| Experiments（4） | 全部 `status=draft`（含 exp_005） | Pilot 生产完成但仍 draft |
| Production Requests（3） | 全部 `status=draft`（含 preq_005） | Approval/生产完成叙事 vs draft |
| Product Asset `8523329941d4` | `generation_status=completed`, `validation_status=passed` | 与生产完成一致 |
| Opportunities（5） | `status=human_assisted` | 创建方法语义≠生命周期（已知） |
| Feedback `fbk_…001` | `feedback_status=pending`, observation `not_started` | 与 Current State 一致 |
| Evaluation | `hypothesis_result=pending` | 观察未开始 |

**结论：** 设计生命周期 / 迁移策略已写，**JSON 同步仍未执行**；Asset Reality 证明「人辅 Pilot 生产发生过」，不等于 Experiment/PR lifecycle 字段已对齐。

---

# 第六部分：MODULE_REGISTRY 对齐

| 模块 | Registry 声称 | Reality | 对齐？ |
|------|---------------|---------|--------|
| 0_START / 1_DATA / 3_DECISION / 6_EXECUTION / 7_MEMORY | Active | Active | ✅ |
| 2_COGNITION | Planned — Not Implemented | **空目录** | ✅（宣称正确） |
| 4_PRODUCT / 5_CONTENT | Planned | **空** | ✅ |
| 9_PRODUCT | Frozen | 残留文件 + 损坏 api_server | ⚠️ 残留风险 |
| 10_DEPLOY | **Frozen** | **可运行 FastAPI，主 HTTP 入口** | ❌ **误导（旧 DC-005）** |
| 11_CONTENT_FACTORY | Active — Isolated；Runtime ❌ | Active Isolated；零连接 | ✅ |
| 蓝图目标流 `1_DATA→…→CF→DEPLOY` | 目标架构 | **Runtime 未实现** | ⚠️ 易被读成已通 |

---

# 第七部分：与 Core Governance / 设计架构对照

| 设计主张 | Reality | 判定 |
|----------|---------|------|
| Unified Architecture 目标统一分层 | 蓝图存在；Runtime 双轨 | Design ≠ Runtime ✅ 原则成立 |
| CF = Execution 子系统 | 仓库内目录成立；主 DAG 未注册 | **半符合** |
| commercial_assets = Commercial SoT | JSON 确为商业链数据面 | ✅ |
| OS SQLite = Operational | products/scores 有数据 | ✅ |
| Governance Before Expansion | 040 系列已建 | ✅（docs） |
| Pilot 可追溯 | preq_005 / PA 8523329941d4 仍在 | ✅ |

---

# 第八部分：未来是否需要架构调整？

## 8.1 选项（仅分析，不实施）

| 选项 | 含义 | 适用 |
|------|------|------|
| **A. 永久双轨 + 显式编排人辅** | OS 负责采集/决策原型；CF+JSON 负责商品验证；文档全部改称 Dual-Track Operating Model | 短期商业验证优先、融合成本高 |
| **B. 授权 Runtime 桥接（Phase C）** | DAG 可选节点或 Orchestrator 调 Adapter；保持 Pilot 可追溯 | 中长期统一 OS |
| **C. 仅状态/文档诚实化** | 先修 Registry Deploy 状态、JSON lifecycle（授权 Entry）；不触融合 | **推进前最低成本必做** |

## 8.2 建议次序（Reality-first）

1. **先 C：** MODULE_REGISTRY `10_DEPLOY` 状态校正；商业 JSON 人辅同步（另开 Entry，Human Assisted）。  
2. **再决策 A 或 B：** 用 DEC 明确「近两年是否 Runtime 融合」；禁止聊天默认假设已统一。  
3. **并行：** Schema drift 对齐（另开 DB Entry）；Broken entries 归档/标注。  
4. **禁止：** 无授权的大融合重构；禁止把本报告写成「已统一」。

## 8.3 推进前门槛（Gate）

进入「项目推进 / Reality Execution」前建议满足：

- [ ] 双轨性质已写入 Current State（本 Entry）  
- [ ] 用户选择临时策略 A 或明确 B 的时间窗（DEC）  
- [ ] 商业状态同步或明确「继续 draft 旁注」  
- [ ] Deploy 模块状态与 Reality 一致  

---

# 第九部分：证据索引

| 证据 | 位置 |
|------|------|
| ACTIVE_MODULES | `8_CONFIG/config.py` L89 |
| OS 入口 | `0_START/main.py`, `0_START/controller.py` |
| CF 入口 | `11_CONTENT_FACTORY/adapter/adapter_runner.py` |
| Deploy | `10_DEPLOY/api.py` |
| ensure_schema | `1_DATA/database.py` |
| 历史双轨审计 | `docs/07_AUDIT/runtime/3_RUNTIME_FLOW_REPORT.md`, `10_KNOWN_ISSUES.md` P0-001 |
| Schema drift | `docs/07_AUDIT/database/AI_FACTORY_OS_SCHEMA_DRIFT_REPORT.md` |

---

## 约束与同步

| 项 | 结果 |
|----|------|
| Python 修改 | **No** |
| Database 修改 | **No** |
| commercial_assets 修改 | **No** |
| Runtime 修改 | **No** |
| 本报告 | **Created** |

---

**Report status:** COMPLETED — Dual Track Confirmed (Case B)  
**Architecture adjustment required:** **Decision required (A or B); honesty/sync (C) recommended before expansion**  
**Entry 041-A:** Reality Architecture Alignment Audit done.
