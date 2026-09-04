# AI_FACTORY_OS 核心记忆系统（稳定中文版本）

# =========================
# 一、系统定义
# =========================
AI_FACTORY_OS 是一个由“系统控制器”统一调度的人工智能自动化操作系统。

系统目标包括：
- 自动获取数据
- 自动分析与决策
- 自动生成产品或内容
- 自动执行任务
- 自动记录记忆
- 自动优化系统行为

---

# =========================
# 二、系统整体结构
# =========================
系统唯一运行流程：

数据 → 决策 → 执行 → 记忆

唯一控制中心：
0_START/controller.py（系统控制器）

---

# =========================
# 三、系统模块说明
# =========================

1_DATA：负责数据获取与整理  
2_COGNITION：负责数据分析与理解  
3_DECISION：负责决策与评分  
4_PRODUCT：负责产品生成  
5_CONTENT：负责内容生成  
6_EXECUTION：负责执行与发布  
7_MEMORY：负责记录与读取系统记忆  
8_CONFIG：负责系统配置管理  

---

# =========================
# 四、核心规则
# =========================
- 系统控制器是唯一执行中心
- 所有模块必须受控制器调度
- 模块之间禁止直接调用
- 所有记忆必须统一写入
- 禁止创建第二套控制系统

---

# =========================
# 五、记忆系统结构
# =========================

系统记忆分为三层：

（一）短期记忆
- 当前任务内容
- 当前执行上下文

（二）中期记忆
- 运行日志
- 执行记录（event_log.jsonl）

（三）长期记忆
- 本文件（PROJECT_CORE_MEMORY.md）

---

# =========================
# 六、系统状态
# =========================
当前状态：
- 控制器：运行中
- 执行流程：稳定
- 记忆系统：统一
- 系统模式：生产环境

---

# =========================
# 七、系统进化记录
# =========================
- 系统初始化完成
- 控制器结构统一完成
- 记忆系统标准化完成
- 模块结构稳定

---

# =========================
# 八、重要警告
# =========================
任何修改必须遵守：

- 不允许破坏系统控制器
- 不允许新增调度系统
- 不允许绕过记忆系统
- 所有变化必须可追踪

[MEMORY_ENTRY]
time: auto
module: system
source: chatgpt
content: AI_FACTORY_OS 已重新进行模块级拆分，系统被划分为8个可独立测试模块，并定义标准执行顺序：7_MEMORY → 0_START → 1_DATA → 3_DECISION → 6_EXECUTION → 5_CONTENT → 4_PRODUCT → 2_COGNITION。所有模块必须支持单元测试能力，并可独立运行后再接入SystemController统一调度。
[/MEMORY_ENTRY]

[MEMORY_ENTRY]
time: auto
module: system
source: chatgpt
content: AI_FACTORY_OS 已完成自愈内核系统（Self-Healing Engine v1.0）。系统整合测试系统、修复系统、优化系统与记忆同步系统，实现模块级自动检测、错误修复建议生成、健康评分计算及记忆自动写入，形成完整“测试→修复→优化→记忆”闭环能力。
[/MEMORY_ENTRY]
[MEMORY_ENTRY]
time: 2026-07-06 14:16:59
module: 0_START
source: system
content: AI Factory OS v2 启动: controller.boot()
[/MEMORY_ENTRY]

[MEMORY_ENTRY]
time: 2026-07-06 14:17:00
module: 1_DATA
source: system
content: [Agent:DataAgent] keyword=虚拟资料, valid=2, products=-
[/MEMORY_ENTRY]

[MEMORY_ENTRY]
time: 2026-07-06 14:17:00
module: 3_DECISION
source: system
content: [Agent:DecisionAgent] action=publish, reason=最高分 82.91 — PPT模板打包
[/MEMORY_ENTRY]

[MEMORY_ENTRY]
time: 2026-07-06 14:17:00
module: 6_EXECUTION
source: system
content: [Agent:ExecutionAgent] status=published_local
[/MEMORY_ENTRY]

[MEMORY_ENTRY]
time: 2026-07-06 14:17:00
module: 7_MEMORY
source: system
content: 闭环完成 v2: 虚拟资料 → pattern=success → rules=2
[/MEMORY_ENTRY]
