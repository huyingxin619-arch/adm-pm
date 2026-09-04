# 踩坑日记

格式：编号 | 日期 | 现象 | 根因 | 解法 | 状态

---

## P001 | 2026-08-19 | 点位恢复时给了 Spid 没给 SpotsPlanId，研发要来回确认

**现象**：毕晓艺反馈活动 2509914 点位被误删，提供了 Spid `95zDC`。建 issue 时只记了 Spid。黄春波实际操作需要 SpotsPlanId（十进制），得另外找小胡确认。

**根因**：AdMonitor 有两套 ID——Spid 是 base62 编码的短 ID（`95zDC`），SpotsPlanId 是十进制的内部 ID（`134413966`）。建 issue 时不知道研发需要哪个，只记了用户给的。

**解法**：base62 字符集 `0-9A-Za-z`（0-9=0-9, A-Z=10-35, a-z=36-61），逐字符查 index 乘以 62 的幂次求和。拿到 Spid 后直接转成 SpotsPlanId 一起给研发。

**状态**：已解决

---

## P002 | 2026-08-24 | 建 Loop issue 时没读图、没附图、指派错专家

**现象**：小胡让把活动 2510519 自动日报未发送的问题提到 Loop。第一版 issue 描述里没写报表 task ID（图里明确是 4348956、0/0），也没附图；指派时错指给了 `hcb-admonitor-fullstack`，被指纠正才改指 Loop 里的 adm-pm助手。

**根因**：
1. 建 issue 前没用 image 工具读截图，漏掉了关键定位信息（task ID、0/0 异常）
2. 不柴清 Loop 里专家身份——小胡说的“那个专家 bot”指的就是 Loop 里的 adm-pm助手，不是别的 agent
3. 对 Loop issue 描述的共-noticed 要求没养成习惯：Loop 那边的专家不继承对话上下文，必须把信息都写进 issue

**解法（已固化为 AGENTS.md Loop 铁律）**：
1. 反馈内容含图片 → 必须先用 image 工具读图，提取 task ID/错误日志/配置截图等关键信息
2. 有图片的 issue 必须附图（`--attachment`）
3. issue 描述必须自足，不能假设 Loop 那边的我知道对话上下文
4. 默认指派给 adm-pm助手专家（agent_id: c8ae294f-2048-437f-aa87-f3dd76565f4e）
5. 遇到“专家 bot”这种叫法，默认是 Loop 里的自己，不用问

**状态**：已解决，规则已入 AGENTS.md + Loop 专家 instructions

---

## P003 | 2026-09-04 | 群聊回复偶尔被端上渲染成“此消息不支持查看”占位图

**现象**：小胡在群里反馈，我发出的部分消息他们端上看不到，只看到“此消息不支持查看，请至手机端查看详情()”占位图。手机端也同样看不到。纯文本消息可以看到。触发样本：17:01 我创建 ADM-43 后的回复（含 `**ADM-43**` 加粗 + `@[uid:姓名]` mention + issue URL 链接）。

**根因**：未知格式化消息被 octo 客户端识别为未知类型 / 解析失败。候选嫌疑犯：
1. 同一条消息中叠加多种富文本元素（加粗 + mention + URL）
2. `@[uid:姓名]` 这种 mention 语法在某些端上不能反序列化
3. 消息中混了某些特殊字符（typography quotes、emoji、反斜括号转义等）
4. 消息被转成某种特殊 payload.type（不是 1），碰上不支持渲染的客户端

**解法（临时）**：
- 群聊回复默认纯文本
- 少用反引号 / 加粗 / 表格，不堆多种富文本元素在一条消息里
- @mention 必须用时才用，不要在一条消息里同时加粗+链接+@人
- issue URL 单独一行发，不要跟加粗/链接砌进一段

**后续验证**：之后再发“复杂格式”的消息后，主动问小胡能不能看到；如果出现新样本，对比找共性。

**状态**：未闭环（根因未明）

**补充验证（2026-09-04 17:10）**：小胡截图确认，16:58 那条包含 mention + 加粗 + URL 的消息正常显示，17:01 那条是占位图。所以根因不在 mention/加粗/URL叠加。17:01 左右我在跑多个 exec 命令（label add），输出结果很长。假设：某些消息被渲染成了非标准 payload.type（如卡片消息 type=17），但 bot 没有卡片权限，客户端显示占位图。待验证。

---

## P003 | 2026-09-04 | 直接派 work agent 被退回（团规：非团长/所有者不接活）

**现象**：ADM-44 子任务我直接指派给 hcb-admonitor-fullstack（work agent），被黄春波退回，反馈：派发人不是团长（octo-issue-dispatcher）也不是 worker 所有者（黄春波），按团规不接活。

**根因**：work agent 有派发权限管控——只接受团长（octo-issue-dispatcher）或 worker 所有者（黄春波）的派发，adm-pm助手作为创建者直接派给 work agent 会被退回。

**解法**：admonitor web 端任务不直接派给 work agent，派给 agent: dispatcher 或人员 member，由他们二次分配。已更新 prd-knowledge.md 分发规则。

**状态**：已解决，规则已入 prd-knowledge.md

---

_每次踩坑当场记录，不等整理。_
