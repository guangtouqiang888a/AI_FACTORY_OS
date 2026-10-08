# Constitution

Highest-layer stable principles of AI_FACTORY_OS.

This document is not an operations manual and not a claim that supporting mechanisms already exist.

## 1. System Identity

> AI_FACTORY_OS is an AI-native, human-owned, evidence-driven, continuously evolving software engineering system.

含义：

- **AI-native**：系统设计默认假设 AI 会参与工程协作，而不是事后外挂。
- **human-owned**：人类始终拥有最终主权。
- **evidence-driven**：关键判断应尽量建立在可追溯事实之上。
- **continuously evolving**：系统被设计为可持续演化，而不是一次性写死。

## 2. Human Ownership

人类始终拥有：

- 最终目标定义
- 重大决策
- 风险承担
- 最终授权

AI 可以建议与执行，但不能取代 Owner 的最终责任。

## 3. AI Is Replaceable

AI 不应成为系统的不可替换单点依赖。

具体协作角色边界见 [AGENTS.md](../AGENTS.md)。

## 4. Facts Must Be Traceable

关键工程事实必须能够追溯到至少一类可靠来源，例如：

- 原始来源
- 具体变更
- 验证结果
- Git 历史
- 或未来建立的 Evidence 记录

“AI 说过”本身不是工程事实。

## 5. Validation Is Mandatory

实现与验证必须区分：

```text
Implementation
↓
Validation
↓
Review
↓
Acceptance
```

本地执行完成、模型自述完成，或聊天中的“看起来对”，都不等于验收通过。

## 6. Architecture Must Evolve

架构可以改变。

禁止：

- 把当前架构永久冻结
- 因为局部问题就整体推倒重来

当前结构说明见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 7. Controlled Change

不同类型的变化未来应拥有不同控制深度，例如：

```text
Ordinary Code Change
Database Change
API Change
Architecture Change
Product Direction Change
External / High-Risk Action
```

本 Constitution 只确立原则：变化必须受控。  
具体控制文件与流程不在本阶段建立。

## 8. Mechanical Guardrails

凡是能被机器客观验证的规则，最终应尽可能由机器验证，而不是依赖 AI 自觉。

本阶段不创建 Automated Guards。

## 9. System of Record

```text
ChatGPT  = reasoning / design / review
Cursor   = local execution
GitHub   = durable project facts
```

聊天上下文可以辅助协作，但不能替代仓库中的长期事实。

## 10. No Governance by File Accumulation

信息重要，不等于必须成为核心文件。

核心文件必须同时具备：

- 长期稳定价值
- 跨任务价值
- 系统机制价值

禁止用文件堆积伪装成治理完成。

## 11. Core Principle

> 先定义机制，再定义文件；先定义事实流，再定义目录。

目录与文件是机制的载体，不是机制本身。
