# AI_FACTORY_OS Asset Audit

> Project Asset Audit Layer — 项目资产审计规范 | 最后更新：2026-07-07

---

## Purpose

**目标：**

识别项目中的：

- **Production Assets** — 生产环境正在使用的核心资产
- **Experimental Assets** — 实验阶段产物与试探性代码
- **Temporary Files** — 运行时临时生成、可再生的输出
- **Deprecated Files** — 已废弃但保留历史参考价值
- **Archive Files** — 归档保存、不参与当前运行

**目的：** 避免历史文件影响未来 AI 判断。

未来 AI 恢复项目上下文时，必须结合本文档与 [AI_FACTORY_OS_ASSET_SCAN_REPORT.md](AI_FACTORY_OS_ASSET_SCAN_REPORT.md)，不得将临时输出或实验文件误判为正式生产资产。

---

# Asset Lifecycle Status

所有文件必须归类为以下生命周期状态之一：

## Active

当前系统正在使用。

**示例：**

- 核心代码（`0_START/`、`3_DECISION/`、`11_CONTENT_FACTORY/` 等）
- 配置文件（`8_CONFIG/config.py`、`7_MEMORY/runtime_policy.json`）
- 正式文档（`docs/`）
- 生产数据（`7_MEMORY/event_log.jsonl`、`data/ai_factory.db`）

---

## Experimental

实验阶段文件。

**示例：**

- 模型测试输出
- 新功能实验代码
- Demo 运行产物
- 早期未接入主链路的模块（如 `9_PRODUCT/` 冻结层代码）

---

## Temporary

临时生成文件。

**示例：**

- 测试输出（`output/*.json`）
- 临时图片 / 占位符（`cover_placeholder.txt`）
- 调试文件
- Python 编译缓存（`__pycache__/`、`*.pyc`）
- 运行日志（`logs/`）

---

## Deprecated

已经废弃，但保留历史价值。

**示例：**

- 未被代码引用的历史状态文件
- 旧版 Memory 快照（若已被新机制替代）
- 早期目录占位（空 Reserved 模块）

---

## Archive

归档保存。

**示例：**

- 已完成商业验证的产品 artifact 快照
- 历史实验批次输出（经审计后移入 archive 目录）
- 不再参与运行但需保留追溯的记录

---

# Audit Scope

本次重点审计目录：

| 目录 | 路径 | 审计重点 |
|------|------|----------|
| **output** | `output/` | 发布模拟输出，每次运行生成 |
| **data** | `data/` | SQLite 数据库与原始采集样本 |
| **logs** | `logs/` | 执行 hash、部署 trace、metrics |
| **artifacts** | `11_CONTENT_FACTORY/artifacts/` | 数字产品生产产物（无根级 `artifacts/`） |
| **Content Factory** | `11_CONTENT_FACTORY/` | 生产代码、storage、templates |
| **Memory** | `7_MEMORY/` | OS 运行时记忆与策略文件 |

### 检查项

对每个资产检查：

1. **文件用途** — 该文件在系统中扮演什么角色
2. **创建来源** — 由哪个模块 / Agent / 命令生成
3. **是否被代码引用** — 是否在 Python 配置或运行链中被读取
4. **是否影响生产流程** — 删除或移动是否破坏 CLI / API / Content Factory 流水线

---

# Audit Workflow

```
资产扫描 (Asset Scan)
    ↓
生命周期分类 (Lifecycle Status)
    ↓
登记模板填写 (ASSET_AUDIT_TEMPLATE)
    ↓
人工 Review
    ↓
Keep / Archive / Remove（须单独审批，本规范阶段仅识别不清理）
```

---

# Directory Classification Reference

| 目录 | 默认分类 | 说明 |
|------|----------|------|
| `0_START/` ~ `8_CONFIG/`（代码） | Active | 核心 OS 与配置 |
| `9_PRODUCT/` | Experimental / Frozen | 早期 SaaS 方向，未接入主链 |
| `10_DEPLOY/` | Active（Frozen 层） | HTTP 部署，禁止随意修改 |
| `11_CONTENT_FACTORY/`（代码） | Active | 数字商品生产层 |
| `11_CONTENT_FACTORY/artifacts/products/` | Active / Archive | 生产产物，可按 product_id 归档 |
| `11_CONTENT_FACTORY/storage/` | Active | Content Factory 产品记忆 |
| `output/` | Temporary | 由 `6_EXECUTION/publisher.py` 写入 |
| `logs/` | Temporary | 运行时日志，`.gitignore` 已排除 |
| `data/` | Active | `ai_factory.db` 为生产数据库 |
| `data/raw/` | Experimental | 早期采集样本 |
| `7_MEMORY/`（json/jsonl） | Active | OS 运行记忆 |
| `7_MEMORY/__pycache__/` | Temporary | Python 编译缓存 |
| `2_COGNITION/`、`4_PRODUCT/`、`5_CONTENT/` | Reserved | 空目录占位 |
| `docs/` | Active | 项目认知与自描述层 |

---

# Related Documents

| 文档 | 路径 | 用途 |
|------|------|------|
| 资产登记模板 | `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md` | 单文件审计登记表 |
| 资产扫描报告 | `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md` | 本次扫描结果 |
| 模块注册表 | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` | 模块状态与职责 |
| 工作准则 | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` | 资产生命周期管理原则 |
| Cursor 执行历史 | `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` | 审计层建设记录 |

---

# Audit Rules

1. **本阶段只识别，不清理** — 禁止未经审计直接删除文件
2. **不确定用途 → Keep** — 标记为 Review，等待人工确认
3. **Temporary ≠ 可立即删除** — 可能仍被调试或对比需要
4. **扫描报告随项目变化更新** — 重大目录变更后重新扫描并更新 `ASSET_SCAN_REPORT.md`
