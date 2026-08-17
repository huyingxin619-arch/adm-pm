# 指标定义清单

> AdMonitor 知识参考材料，用于需求审核粗判。标记"知识参考，非最终判断"。

## 基础指标

| 指标 | 定义 | 计算逻辑 | 注意事项 |
|------|------|----------|----------|
| Imp（曝光） | 广告展示次数 | 收到曝光监测代码请求即计1次 | 实时数据未过滤，基础数据经过GIVT过滤 |
| Click（点击） | 广告点击次数 | 收到点击监测代码请求即计1次 | OTT端无点击 |
| UV（独立访问者） | 不重复用户数 | 对UUID去重后，用打通算法跨端合并 | 不能跨时间段简单加总 |
| Clicker（点击者） | 有点击行为的UV | 同UV逻辑，仅限有点击行为的用户 | OTT端无点击者 |
| CTR（点击到达率） | 点击占曝光比例 | Click / Imp | 需自行计算，API不直接返回 |

## 到达/频次指标

| 指标 | 定义 | 注意事项 |
|------|------|----------|
| Reach（到达人数） | 看过广告N次及以上的不重复用户 | 基于打通后UV计算 |
| Reach%（到达率） | Reach / Universe × 100% | 可能超过100%，原因见已知约束 |
| GRP（毛评点） | Imp / Universe × 100 | 传统广告指标在互联网的映射 |
| iGRP（互联网GRP） | 同GRP，互联网语境 | — |
| Frequency（频次） | 总曝光 / UV | 平均曝光频次 |
| 1+~10+ 到达 | 看过1次/2次/.../10次及以上的UV | API返回 rch_acc_p01~rch_acc_p10 |
| 相交样本量 | 稳定人群与Panel库相交的ID数 | <300时数据不可参考（统计学置信度不足） |

## 人群指标

| 指标 | 定义 | 注意事项 |
|------|------|----------|
| TA（目标人群） | 基于稳定人群与Panel相交样本推算的TA占比 | 仅stable人群维度有 |
| Universe（总体网民数） | CNNIC+华通人调研推算 | 半年更新一次，仅stable维度有 |
| Demography（人群属性） | 性别/年龄/教育/收入分布 | 仅界面可查，API拉不到 |
| Index（集中度指数） | 目标人群在某维度占比 / 该人群在全网占比 × 100 | >100表示高于平均水平 |

## 指标维度组合限制

| 组合 | 是否可用 | 说明 |
|------|----------|------|
| by_audience=target + metrics=day | ❌ 无效 | day维度指标返回0或null |
| by_audience=overall + 关键词数据 | ✅ | 仅overall可查关键词 |
| 实时报告 + stable/target | ❌ | 实时仅overall |
| OTT + 点击/Clicker | ❌ | OTT设备无点击行为 |
| overall + Universe | ❌ | Universe仅stable维度有 |

## metrics参数与返回字段对照

| metrics值 | 返回字段 | 说明 |
|-----------|---------|------|
| acc | imp_acc, clk_acc, uim_acc, ucl_acc | 累计值（活动开始到date） |
| day | imp_day, clk_day, uim_day, ucl_day | 单天值（date当天） |
| avg_day | imp_avg_day等 | 日均值 |
| acc_hrs | imp_acc_h00~h23, clk_acc_h00~h23 | 分小时累计 |
| all | 以上全部 | — |

## by_audience各值含义

| 值 | 含义 | 适用 |
|----|------|------|
| overall | 所有网民 | ADM + TVM |
| stable | 稳定人群（移动端全部；PC端24h后再监测到的MZID） | 仅ADM |
| target | 目标人群（TA） | ADM + TVM |
| targetdevice | 目标人群（设备维度） | 仅TVM |
| people | 屏前人数（OTT一台电视可能多人观看） | 仅TVM |

## 平台类型（仅ADM）

| 值 | 含义 |
|----|------|
| pc | PC端 |
| mb | Mobile端 |
| pm | PC+Mobile打通（日常报告用这个） |
