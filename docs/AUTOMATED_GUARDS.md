# AUTOMATED GUARDS

## 1. 目标
把可以机械验证的规则交给机器执行，而不是依赖 AI 记忆。

## 2. Framework Integrity
自动检查：
- 必要 Core 文件存在
- Task 状态枚举合法
- 核心循环定义存在
- 角色边界没有缺失
- Foundation 文档结构没有损坏

## 3. Task Integrity
逐步检查：
- Task 必填字段
- 状态转换合法
- Acceptance Criteria 存在
- Risk 存在
- Evidence 与 Acceptance 有关联

## 4. Engineering Integrity
逐步检查：
- Schema Change → Migration
- API Breaking Change → Compatibility
- Required Tests → PASS
- Required CI → PASS
- 核心依赖删除 → Impact Analysis

## 5. Release Integrity
逐步检查：
- Acceptance PASS
- Required Review PASS
- Required Authorization PASS
- Evidence 完整
- Release 条件满足

## 6. Guard 失败原则
Guard FAIL → 停止推进。

不得靠解释绕过、AI 自行覆盖或修改结果让检查“看起来通过”。

规则本身错误时，通过 Change 修改规则。

## 7. 自动化原则
第一阶段只建立不会阻碍真实工程的基础检查，随后逐步增加。
