# AI_FACTORY_OS State Migration Rollback Plan

> Entry 039-D | Rollback Strategy（未来执行迁移时适用）  
> **本 Entry 不执行备份或迁移**

---

## 1. Preconditions（任何迁移 Entry 之前）

| Step | Action |
|------|--------|
| 1 | 读取本 Rollback Plan + Historical Snapshot（039-D） |
| 2 | **Backup** `commercial_assets/` 全目录（zip 或 git commit） |
| 3 | 记录 `migration_id`、时间、操作者、目标 Wave |
| 4 | Dry-run：输出拟改 diff，**零写入** |
| 5 | Human approve dry-run |

---

## 2. Backup

| 项 | 要求 |
|----|------|
| **Scope** | 至少：product_assets, production_requests, experiments, feedback, evaluations, opportunities, candidates, reviews |
| **Pilot 强制** | 单独副本含 `8523329941d4` / `preq_20260712_005` / `exp_20260708_005` |
| **Location** | 建议 `backups/commercial_assets/<migration_id>/`（未来创建；非本 Entry） |
| **Integrity** | checksum（sha256）写入 audit |

---

## 3. Version

| 机制 | 说明 |
|------|------|
| dataset_version | JSON 顶层 version +1 |
| migration_id | e.g. `mig_039E_waveB_pilot` |
| schema_ref | 指向 Field Standard 文档版本 |
| dual-write period | 旧字段保留 ≥1 个验证 Entry |

---

## 4. Audit Record

每条字段变更记录：

```
migration_id, object_type, object_id,
field_before, value_before,
field_after, value_after,
auto_or_human, operator, timestamp, reason
```

建议落盘：`docs/migration_audit/` 或 `commercial_assets/_migration_audit/`（未来 Entry 创建）。

---

## 5. Restore

| 场景 | 动作 |
|------|------|
| 迁移失败 / 校验失败 | 用 backup zip **整目录还原** commercial_assets |
| 单对象回滚 | 从 audit + backup 恢复该 JSON 对象块 |
| Pilot 损坏 | 优先恢复 PA / PR / Experiment 三件套 |
| 禁止 | 凭记忆手改 ID；从 CF product_memory 覆盖 SoT |

**Restore 验证：** ID 链 cand→…→fbk 与 Snapshot 一致；generation_status/validation_status 与文件存在性抽检。

---

## 6. Stop Conditions

- Product Asset ID 变化  
- Artifact 路径丢失  
- hypothesis_result 被自动改写  
- dry-run 未审批却写入  

→ **立即 Rollback**
