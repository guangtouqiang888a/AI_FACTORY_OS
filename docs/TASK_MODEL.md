# TASK MODEL

## 1. 定义
Task 是 AI_FACTORY_OS 的最小受控工程变化单元。

## 2. 生命周期
IDEA → BACKLOG → READY → IN_PROGRESS → VALIDATING → REVIEW → ACCEPTED → RELEASED → OBSERVING → CLOSED

异常：BLOCKED / REJECTED / SUPERSEDED / RETIRED

## 3. 状态含义
IDEA：想法，尚未承诺执行。
BACKLOG：值得保留。
READY：目标、范围、Acceptance、风险、依赖明确，可以开始。
IN_PROGRESS：工程执行中。
VALIDATING：实现完成，正在验证和收集证据。
REVIEW：等待 Review / 授权。
ACCEPTED：Acceptance Criteria、Required Review 和授权满足。
RELEASED：按规定发布。
OBSERVING：进入真实世界，等待实际结果。
CLOSED：结果已记录，生命周期完成。

BLOCKED：外部条件或决策不足。
REJECTED：当前方案不接受。
SUPERSEDED：被新的 Task/Decision 替代。
RETIRED：对应能力或方案正式退出。

## 4. 状态变化
必须遵守：
PROPOSE → VERIFY → AUTHORIZE → STATE CHANGE

## 5. Task 必备字段
ID / Title / Type / Why / What / Scope / Acceptance Criteria / Risk / Dependencies / Change Impact / Implementation / Validation / Evidence / Decision / Release / Observation / Outcome

## 6. 完成定义
Cursor 提交代码只是 Implementation 完成。

Task Acceptance 还必须满足：
- 自动验证通过
- Acceptance Criteria 全部满足
- Required Review 完成
- 所需授权完成
- Evidence 已记录

Task Closed 还需要：
- Release/实际结果已记录
- Outcome 已明确
- 若产生 Learning，已转化为知识或新 Task
