# 11_CONTENT_FACTORY — 数字商品生产车间

AI Factory OS 的**业务生产层**，独立于核心 OS 执行链。

## 第一生产线

**教育资料 + 办公效率模板**

支持产品：PDF资料 · PPT模板 · Excel模板 · Word模板 · 学习计划 · AI办公模板

## 生产流水线

```
market → creator → artifact → quality → packaging → publish_assistant → memory
```

## 目录结构

```
11_CONTENT_FACTORY/
├── agents/              # 生产 Agent
├── artifacts/           # Artifact Layer
│   ├── artifact_manager.py
│   └── products/        # 产品产物目录（运行时生成）
├── schemas/             # DigitalProduct 数据模型
├── pipeline/            # content_pipeline.py 测试入口
├── storage/             # product_memory.json
├── templates/
└── llm_adapter.py       # LLM 接口预留（禁止直接调用 API）
```

## 产品目录结构

```
artifacts/products/{product_id}/
├── source/
├── documents/
├── templates/
├── images/
├── package/
│   ├── publish_package/     # title.txt, description.txt, keywords.txt, pricing.json, cover_prompt.txt
│   └── publish_assistant/   # 人工发布辅助
└── metadata.json
```

## 快速测试

```powershell
python 11_CONTENT_FACTORY/pipeline/content_pipeline.py "办公PPT模板"
python 0_START/main.py
```

## 架构边界

- **不修改** 0_START ~ 10_DEPLOY 核心层
- **LLM** 未来经 PolicyEngine → ModelBridge 接入
- **发布** 半自动辅助，禁止自动刷平台
