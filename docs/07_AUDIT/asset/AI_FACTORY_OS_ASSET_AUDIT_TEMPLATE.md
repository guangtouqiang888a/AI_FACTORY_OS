# AI_FACTORY_OS Asset Audit Template

> 单文件资产登记模板 | 复制本模板用于逐项审计

---

## 使用说明

对每个待审计文件或目录复制一份下方模板，填写完整后纳入资产台账。

**Action 取值：**

| Action | 含义 |
|--------|------|
| **Keep** | 保留，当前或未来仍需要 |
| **Archive** | 移入归档区，不参与运行 |
| **Remove** | 建议删除（须人工审批后执行） |

---

## Template

```markdown
### Asset Entry

**File Path:**

**File Type:**

**Created By:**

**Purpose:**

**Lifecycle Status:**

Active / Experimental / Temporary / Deprecated / Archive

**Referenced By:**

**Action:**

Keep / Archive / Remove

**Notes:**

（可选）审计备注、Review 日期、审批人
```

---

## 示例

### Asset Entry — output/publish_*.json

**File Path:** `output/publish_虚拟资料_20260707_155141.json`

**File Type:** JSON — 本地模拟发布记录

**Created By:** `6_EXECUTION/publisher.py`（经 `config.OUTPUT_DIR`）

**Purpose:** 记录 Decision → Publish 环节的本地模拟分发结果

**Lifecycle Status:** Temporary

**Referenced By:** `8_CONFIG/config.py`（OUTPUT_DIR）；`.gitignore`（已排除版本控制）

**Action:** Keep（运行期）/ Archive（历史批次审计后）

**Notes:** 每次 CLI/API 运行可能新增；不影响 Content Factory artifact 生产链

---

### Asset Entry — 7_MEMORY/core_state.json

**File Path:** `7_MEMORY/core_state.json`

**File Type:** JSON — 历史状态快照

**Created By:** 早期 Memory 实验（来源未在当前代码链中确认）

**Purpose:** 未知 — 当前无代码引用

**Lifecycle Status:** Deprecated

**Referenced By:** （无 Python 引用）

**Action:** Review — 确认后可 Archive 或 Remove

**Notes:** 删除前须备份；不影响 `event_log.jsonl` / `pattern_memory.json` 主链

---

## Batch Audit Table（可选）

| File Path | Lifecycle Status | Referenced By | Action | Review Date |
|-----------|------------------|---------------|--------|-------------|
| | | | Keep / Archive / Remove | |
