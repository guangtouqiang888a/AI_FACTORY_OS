# AI_FACTORY_OS Engineering Constitution

## 1. 系统定义
AI_FACTORY_OS 是一个持续演化的工程系统，而不是单纯的 AI 开发流程。

核心目标：
> 让 AI 能够持续、可控、可验证地参与软件演化，并让错误能够被发现、定位、修复、迁移和学习，而不必因为一次错误推倒整个系统。

## 2. 最终权威
Human Owner 是最终 Owner。

AI 可以推理、提议、规划、实现、测试、分析、Review、总结。
AI 不可以自行成为最终业务权威、把推测升级为事实、绕过自动化护栏、在需要人工授权的高风险动作上自行授权，或用自身 PASS 替代系统 Acceptance。

## 3. 四类角色
Human：目标、方向、价值判断、重大风险、最终授权。
ChatGPT：架构、推理、规划、方案比较、审查、Closure Review、学习。
Cursor：本地代码实现、文件修改、测试、调试、Git 技术操作。
GitHub + Automation：长期事实载体、历史、代码、决策、证据和机械约束。

## 4. 核心对象
GOVERNANCE / CURRENT STATE / PRODUCT / TASK
Evidence、Learning、Change/Migration、Engineering 围绕它们运行。

## 5. Task 原则
Task 是最小受控工程变化单元。必须有 WHY、WHAT、ACCEPTANCE、RISK、CHANGE、EVIDENCE、DECISION、OUTCOME。

## 6. 完成定义
Cursor 完成 ≠ VALIDATING 完成 ≠ ACCEPTED ≠ RELEASED ≠ CLOSED。
Task 只有在规定证据、Review、授权和真实结果条件满足后才能关闭。

## 7. Evidence 原则
必须区分 CLAIM、OBSERVATION、EVIDENCE、CONCLUSION。推测不能伪装成事实。

## 8. 风险原则
权限由 RISK × ACTION × REVERSIBILITY × EVIDENCE × AUTHORIZATION 共同决定。
R0：极低风险；R1：普通工程；R2：高影响工程；R3：高风险/不可逆/真实世界动作。

## 9. 自动化优先
能够机械检查的规则，不依赖 AI 记忆。测试失败、Required Check 失败、关键结构不满足时必须停止推进。

## 10. 架构演化
架构变化经过：
Problem → Impact Analysis → Decision → Migration/Compatibility → Implementation → Validation → Release → Legacy Retirement
禁止把重建当作默认架构治理方式。

## 11. AI 可替换
系统不得把核心规则绑定到某个模型、供应商或 Agent。AI 是可替换工程组件，不是系统权威。

## 12. 长期连续性
ChatGPT 上下文是临时的；GitHub 是长期事实载体。项目必须能够在上下文丢失、模型更换、Cursor 更换、人员或电脑变化后继续运行。

## 13. Core 文件纪律
Core 文件必须长期稳定、系统级、跨 Task 有效且不适合放在更具体的位置。“重要”不等于“Core”。

## 14. 停止条件
关键事实缺失、Evidence 不足、风险未知、Acceptance 不清楚、架构影响未知或授权不足时，系统必须停止推进，而不是让 AI 猜测继续。
