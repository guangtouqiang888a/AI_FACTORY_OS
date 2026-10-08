# HUMAN COMMERCIAL DECISION PACK
# Entry 048 | Pilot preq_20260712_005 / Product Asset 8523329941d4

生成时间：2026-08-29T15:00:00+08:00
系统状态：**READY FOR HUMAN DECISION**
发布状态：**PREPARED / NOT PUBLISHED**
观察状态：**NOT STARTED**

本文件是人工商业决策包。AI 给出的是建议，不是最终决定。

---

## Decision 1 — Distribution

Recommended: **taobao**
Alternative: **xianyu**
Why:
- Pilot 链路（opportunity.market / experiment.publish_channel_planned / PR / feedback.platform / pricing.platform）一致指向淘宝虚拟商品。
- 闲鱼在同批次其他 Category A 实验（PPT 类）出现更多，是可选对照渠道，但不是本 Pilot 主记录规划。
Evidence:
- opp_20260708_005.market = 国内淘宝虚拟商品
- exp_20260708_005.publish_channel_planned = taobao
- feedback.platform = taobao（观察未开始）
Why Not Yet Final:
- 无真实上架证据；AI 不得自行选定最终销售渠道。

Human must choose: taobao / xianyu / other / defer

---

## Decision 2 — Price

Recommended: **12.9 CNY**（Recommended Experimental Price）
Alternative: **9.9**（更低门槛） / **19.9**（CF 包装默认）
Why:
- 12.9 是本 Pilot 从 Opportunity→Experiment→PR→Evaluation 一贯假设价。
- 19.9 来自 Content Factory packaging 默认（Excel模板），不是本 Pilot 机会定价证据。
- 9.9 来自兄弟实验「家庭记账表」价位带，可作对照，非本 Pilot 主假设。
Evidence: 见 PRICE_REALITY_REPORT.md；无 VALIDATED 销量证据。
Risk:
- 12.9 可能偏高或偏低均未知；首轮目标是可解释可测试，不是最优定价。

Human must choose: 9.9 / 12.9 / 19.9 / other

---

## Decision 3 — Cover

Recommended: **Replace if low-cost image available; otherwise Keep Placeholder for first listing is acceptable**
Case: **B（轻微）** — placeholder 降低视觉吸引力，但不阻止数字商品第一轮测试。
Why:
- Reality 仅有 cover_placeholder.txt + cover_prompt.txt；ZIP 内无真实封面图。
- 最小方案：按 cover_prompt 生成一张 16:9 封面后替换；不做品牌重设计。

Human must choose: Keep Placeholder / Replace

---

## Decision 4 — Publish

READY / NOT READY: **READY FOR HUMAN DECISION**（材料与对账就绪；非已发布）
Required Human Approval:
1. 渠道最终选择
2. 价格最终选择
3. 封面 Keep/Replace
4. 明确授权「允许人工上架」
5. 上架后保存证据，另开 Observation Entry

AI 禁止：代发、代注册账户、代改真实售价、代买广告、代宣成功/失败。

---

## Conflict Summary

| Conflict | Impact | Recommended Resolution | Human Decision Required |
|----------|--------|------------------------|-------------------------|
| 9.9 vs 12.9 vs 19.9 | 上架价不清 | 首轮建议 12.9；9.9/19.9 作备选 | YES |
| planned taobao vs NOT YET SELECTED | 不能开始观察 | 人工确认渠道后再发布 | YES |
| CF default 19.9 vs Pilot hyp 12.9 | 包装价与实验价分叉 | 区分 DEFAULT vs HYPOTHESIS；上架用人工价 | YES |

---

## After You Decide

下一 Entry 建议：仅在人工决策完成后，执行授权发布与 Observation Start（需真实发布证据）。
