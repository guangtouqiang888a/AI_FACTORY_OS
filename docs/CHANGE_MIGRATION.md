# CHANGE & MIGRATION

## 1. 目的
保证系统能够持续演化，而不是“冻结旧系统→全部重建”。

## 2. Change 类型
- Bug：修复错误行为
- Product Decision：产品方向变化
- API Change：接口变化，需要 Compatibility
- DB Change：数据结构变化，需要 Migration
- Architecture Change：系统结构变化，需要 Impact Analysis 和 Migration Plan
- Security / External Action：高风险或真实世界不可逆动作，需要严格授权

## 3. 标准流程
Problem → Impact Analysis → Options → Decision → Migration/Compatibility Plan → Implementation → Validation → Release → Observation → Legacy Retirement

## 4. Compatibility
必要时允许：
Old + New → Migration → Validation → Remove Legacy

## 5. 禁止
不能因为代码不漂亮、AI 不喜欢旧代码、新模型出现或新架构更先进，就直接删除旧系统。

删除必须有明确退出条件和证据。
