# EVIDENCE & LEARNING

## 1. Evidence 的目的
回答：
> 现实中究竟发生了什么？

Evidence 必须可追溯、可复核，并明确支持哪个 Claim / Acceptance Criterion / Decision。

## 2. 四层信息
CLAIM：声明、观点或待验证判断。
OBSERVATION：观察到的现象或记录。
EVIDENCE：可复核证据，如 Test、CI、Commit、Runtime Log、User Feedback、Metric、Business Result、Migration Result。
CONCLUSION：根据 Evidence 得出的结论。

## 3. 禁止混淆
HYPOTHESIS ≠ FACT
AI 推测 ≠ Evidence
Cursor PASS ≠ Acceptance
单次异常 ≠ 已验证规律

## 4. Evidence 最少包含
Evidence ID / Source / Timestamp / Related Task / Related Claim or Acceptance / Observation / Evidence / Conclusion / Verification Status

## 5. Learning
Learning 不是每个 Task 的强制终态。

Evidence → Analysis → Learning

Learning 可能更新：
- Product
- Architecture
- Engineering Rules
- Governance
- Future Tasks

## 6. 知识生命周期
OBSERVATION → HYPOTHESIS → VALIDATION → DECISION → VALIDATED RULE → RETIRED

未经验证的内容不能直接升级为 Validated Rule。
