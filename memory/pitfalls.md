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

_每次踩坑当场记录，不等整理。_
