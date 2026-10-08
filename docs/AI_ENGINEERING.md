# AI ENGINEERING MODEL

## 1. 双 AI 工作层
ChatGPT ↔ Cursor

### ChatGPT
Architecture / Reasoning / Planning / Task Definition / Risk Analysis / Review / Closure Review / Learning

### Cursor
Local Implementation / File Operations / Code / Tests / Debugging / Git Technical Operations

## 2. 标准工作循环
ChatGPT：Task Definition → Implementation Plan → Acceptance Criteria
Cursor：Implement → Test → Report Evidence
Automation：Verify
ChatGPT：Review → Closure Decision
Human：必要时 Final Authorization
GitHub：Persist Facts

## 3. 重要边界
Cursor 不能自行宣布整个 Task CLOSED。
ChatGPT 也不能跳过实际验证凭空宣布成功。
任何 AI 结论都必须回到 Evidence。

## 4. AI Provider 可替换
系统不得依赖某一个模型。Provider、模型和 Agent 都是可替换执行组件。

## 5. AI 停止条件
以下任一情况应停止并要求进一步决策：
- 关键事实缺失
- Evidence 不足
- 风险未知
- Acceptance 不清楚
- 架构影响未知
- 所需授权不存在
- 自动化护栏失败
