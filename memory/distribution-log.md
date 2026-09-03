# PRD 分发记录

格式：PRD编号 | 标题 | 分发日期 | 接收人 | 状态 | 备注

> **2026-09-02 起规则更新**：备注中必须包含「提需人：XXX；通知渠道：{chat_id}」。
> 通知渠道 = 需求提出时的聊天通道，DM 和群聊都通知。格式：DM:{uid} 或 群:{group_no}。
> 提需人 = @我提需求的那个人。
> 2026-09-02 之前建的 issue 没有通知渠道字段，轮询跳过通知，仅更新状态。

---

## 2026-08-24

| PRD编号 | 标题 | 分发日期 | 接收人 | 状态 | 备注 |
|---------|------|----------|--------|------|------|
| ADM-8 | 活动2510519 自动日报未发送（汉高施华蔻） | 2026-08-24 | Loop adm-pm助手专家 | 已闭环（小胡手动处理） | 后续补 task ID 4348956 和截图；分发原则更新：自动任务/发送类问题默认只分后端，不同时 @ 大数据侧 |
| ADM-15 | [TVM] 监测代码OTT媒体列表添加媒体：银河新电视 | 2026-08-27 | Loop adm-pm助手专家 | 已闭环 | 提需人：关甜甜；映射 Babel stid: 000000020000000000436821；9/2 11:51 in_review→done 已闭环 |
| ADM-16 | [TVM] ott-givt 分规则统计需求（活动4144746） | 2026-08-27 | Loop adm-pm助手专家（兜底，坤城不在Loop workspace） | 已闭环 | 提需人：王心宇；活动4144746/点位32KiJ/日期20260826；labels: type/investigate+tech/data-tvm+svc/tv-query；9/3 15:37 in_review→done 已闭环 |
| ADM-18 | [TVM] OTT-GIVT统计需求测试：20260826大盘整体分规则统计 | 2026-08-27 | Loop adm-pm助手专家 | 已闭环 | 提需人：王心宇；大盘整体/日期20260826；labels: type/investigate+tech/data-tvm+svc/tv-query；9/3 15:36 in_progress→done 已闭环；9/3 15:37 updated（当前done） |
| ADM-23 | [TVM] OTT-GIVT分规则统计测试需求：260801-260826大盘by day | 2026-08-27 | Loop adm-pm助手专家 | todo | 提需人：王心宇；大盘/区间260801-260826；①GIVT整体过滤量级by day ②各子规则by day变化；labels: type/investigate+tech/data-tvm+svc/tv-query |

## 2026-08-28

| PRD编号 | 标题 | 分发日期 | 接收人 | 状态 | 备注 |
|---------|------|----------|--------|------|------|
| ADM-24 | ADM M+ & TVM 数据中心 API 接口开发 | 2026-08-28 | Loop adm-pm助手专家（→吕金果二次分配） | 开发中 | 提需人：胡映昕；优先级high；期望2周完成；含2张截图附件；issue ID: 5e4c50ef-6039-4289-836c-a0c8ae1379bc；⚠️老issue无通知渠道，跳过通知；子任务ADM-26：9/2 14:34 指派人变更+新评论（技术负责人审核反馈：mplus配置前缀应使用admonitor、prod环境redis配置需修正）；9/2 14:47 指派人变更+新评论（配置修改已完成：mplus配置前缀统一到admonitor命名空间，从mz.mplus.*迁移到mz.admonitor.mplus.*）；9/2 14:47 新评论（确认合并）；9/2 14:56 指派人变更+新评论（OCTO-LOOP合并指令：技术负责人确认合并，请将feat/ADM-26-mplus-api合并到feature/260831-mplus-api并push）；9/3 14:51 指派人变更（4f356f9a→38aeb0d2）+新评论（技术负责人要求：M+ list接口需补充ES查询能力，与admonitor web端保持一致，参考intra-api多维查询）；9/3 15:25 指派人变更（38aeb0d2→4f356f9a）+新评论（M+ list接口ES/MzSearch查询能力已补充完成，参考AdQueryTaskListServiceImpl实现，接入ES主路径+MySQL透明降级）；9/3 15:51 指派人变更（4f356f9a→38aeb0d2）+新评论（OCTO-LOOP启动报错修复：mz.admonitor.mplus.list.es.base-url is required when mz.admonitor.mplus.list.es.enabled=true，M+ list ES不应启用）；9/3 16:06 指派人变更（38aeb0d2→4f356f9a）+新评论（启动报错修复：M+ list ES 复用 ADM MzSearch 集群配置，已按技术负责人要求修复启动报错，M+ list ES 现在直接复用 AdMonitor query/list 集群配置）；9/3 16:10 指派人变更（38aeb0d2→4f356f9a）+新评论（补充说明：16:06的修复已覆盖dispatcher派发要求，commit f86d63a已push到feature/260831-mplus-api：已删除独立MplusMzSearchClientConfig.java不重复建RestC）；9/3 16:13 新评论（🤖 OCTO-LOOP 启动报错已修复 commit f86d63a 已push到feature/260831-mplus-api：1.删除独立MplusMzSearchClientConfig不再重复建RestClient/校验base-url 2.ES） |
| ADM-27 | M+ 任务下载字段错列排查（任务481039/481041） | 2026-08-28 | Loop adm-pm助手专家 | 开发中 | 提需人：胡映昕；反馈人：慕程琳；优先级high；任务ID 481039/481041；活动2510032；字段ti/NS/IP/tr/ipTp错列；含2张截图+1个zip附件；issue ID: ae7727f0-c42f-4c10-87c0-a2b812d6e789；子任务ADM-28（CSV字段逗号未转义修复）：9/2 15:43 状态 todo→in_progress；9/2 15:43 新评论（ns字段回传多ip导致M+取值异常，ns只适配单个ip，多ip违背设计）；⚠️老issue无通知渠道，跳过通知 |

## 2026-09-02

| PRD编号 | 标题 | 分发日期 | 接收人 | 状态 | 备注 |
|---------|------|----------|--------|------|------|
| ADM-37 | [TVM] SIVT线上举证条数限制（新增设备规则） | 2026-09-02 | Loop adm-pm助手专家（→吴坤城） | in_review | 提需人：王心宇；通知渠道：DM:03b1da44f59b437b8edb0be6800288cf；优先级P1/high；期望本周(9/5前)；新增设备规则全量→限50条按uuid升序；非白名单已无量不改；labels: type/feature+tech/sivt-tvm+svc/tv-api；issue ID: 3c9bb261-02ba-4c3e-afe4-fb9655125197；9/2 11:33 状态变更 in_progress→in_review（请验收）；9/2 14:21 指派人变更（adm-pm助手→d5ca704c） |
| ADM-38 | [TVM] OTT GIVT举证开发需求 | 2026-09-02 | Loop adm-pm助手专家（目标承接：吴坤城，坤城不在Loop workspace无法直派） | todo | 提需人：王心宇；通知渠道：DM:03b1da44f59b437b8edb0be6800288cf；优先级high；参照OTV以SFTP形式支持举证；举证规则/字段/存储要求见企微文档（链接在issue内）；labels: type/feature+tech/data-tvm+svc/tv-api；issue ID: 1450ab52-62a3-4e51-b8b8-e616afa89cb7；9/2 15:13 指派人变更（adm-pm助手→7bcc9ad4）+新评论（需求审核报告：复述需求内容，确认提需人王心宇，目标承接人待定）；9/2 16:00 指派人变更（7bcc9ad4→d5ca704c） |

## 2026-09-01

| PRD编号 | 标题 | 分发日期 | 接收人 | 状态 | 备注 |
|---------|------|----------|--------|------|------|
| ADM-33 | [TVM] 多维自动报告异常（任务1106395/1106394） | 2026-09-01 | Loop adm-pm助手专家 | todo | 提需人：邢思源；优先级high；子任务1106405计算失败+8/29报告未生成；issue ID: 270ad7ff-34d8-4830-978f-016d10b65e66；9/2 11:38 状态 in_progress→todo（格式审核未通过：缺svc服务标签，无法自动派发）+指派人变更+新评论（格式审核未通过反馈）；9/2 11:46 指派人变更+新评论（OCTO-LOOP：svc/ui-report无对应dev agent，无法自动派工排查）；9/2 11:49 状态 todo→blocked（有阻塞）；9/2 14:03 状态 blocked→todo + 指派人变更 + 新评论（OCTO-LOOP流程纠正：之前误判涉及svc/ui-report导致阻塞，实际标签为svc/tv-web+svc/tv-query，由tv cloud web worker统一处理，不涉及ui-report）；9/2 14:03 新评论（等待三个探索agent完成代码分析，开始搜索/home/mlclaw/miaozhen/api代码库中auto-report功能）；9/2 16:28 指派人变更（取消指派）；9/2 16:28 指派人变更（→4f356f9a，重新指派）；9/2 16:31 指派人变更（4f356f9a→1c537bb8）；9/2 16:52 指派人变更（1c537bb8→4f356f9a，重新指派）；9/2 17:05 指派人变更（4f356f9a→1c537bb8）；9/2 17:05 新评论（OCTO-LOOP根因已确认，请出修复方案：技术负责人黄春波已通过生产日志确认真实根因，与代码静态分析有差异，请基于确认的根因出修复方案）；9/2 17:05 新评论（修复方案：①st_email表email字段VARCHAR(30)太短导致收件人邮箱被截断 ②子任务计算失败修复方案）；9/2 17:13 指派人变更（1c537bb8→4f356f9a，重新指派）；9/2 17:16 新评论（agent自身评论：issue被重新指派回来，可能因@黄春波触发）；9/2 17:26 新评论（agent自身评论：No new comments, waiting for 黄春波's confirmation. The repeated triggers appear to be from the system re-assigning to me after my own comments post. Not…）；9/2 17:33 状态 todo→done 已闭环；9/2 17:53 状态 done→in_review（请验收）；9/3 10:18 状态 in_review→todo（退回待处理）；9/3 10:27 指派人变更（4f356f9a→1c537bb8）；9/3 10:28 指派人变更（1c537bb8→4f356f9a，重新指派）；9/3 10:32 新评论（方案问题：1，st_query_task_tv.mail字段长度本来就是500，不需要变更。2，同意 3，error日志，但不阻塞流程 4，不需要数据修复）；⚠️老issue无通知渠道，跳过通知 |
| ADM-35 | [ADM] 统计caid版本信息（2026年7月日志） | 2026-09-01 | 于长亮 | in_progress | 提需人：邢思源；优先级high；日志7/1-7/30；m14a优先m14兜底；剔除CAID默认值；by day输出非朋友圈大盘+朋友圈整体流量；issue ID: daef2a20-4eab-4b0f-afbc-1655a4a719a0；9/2 15:42 状态 todo→in_progress；⚠️老issue无通知渠道，跳过通知 |
| ADM-36 | [ADM] 监测点信息导出extInfo字段异常（批量导出错位+新建活动字段空值） | 2026-09-01 | Loop adm-pm助手专家 | 开发中 | 提需人：吴济；优先级high；历史活动2512416正常/新活动2513757异常；extInfo_md5FormatType批量导出左移+新建活动空值；extInfo_budgetInput被copy；issue ID: 9bab8061-fb2a-42a0-9e15-0e735be6096c；⚠️漏记通知渠道，9/1建issue时未补；9/1 21:15 指派人变更+新评论（extInfo列位置是运行时扫描表头fieldName→列号映射，要求提供日志格式去服务器查看细节）；9/2 14:20 指派人变更+新评论（extInfo列索引扫描相关日志说明：现有日志仅2行在SpotsInfoServiceImpl.java的findExtInfoIndexFromExcel()方法内）；9/2 14:20 新评论（排查结论：根因是导入模板版本不一致导致列索引错位，非代码bug，8/25上线后有人用旧模板导入）；9/2 15:03 新评论（8.25和9.1的上线涉及到adm的模板了吗？没涉及到也会影响这个问题是不是 @huangchunbo）；9/2 15:03 新评论（@吴济：每次上线重启后会拿业务导入的模版进行索引设置，所以导致了这个问题）；9/2 15:03 新评论（@huangchunbo：业务找到这两波活动的导入模板，表头一致，没有新旧之分）；9/2 15:03 新评论（@吴济：上线后第一个导入的模版读取完就缓存了，后面的都不会重新扫描）；9/3 16:15 指派人变更（cab5ac70→4f356f9a）；9/3 16:16 状态变更 todo→in_progress + 指派人变更（4f356f9a→d0ff2b22）；9/3 16:16 新评论（🤖 OCTO-LOOP 修复任务通知：技术负责人黄春波已确认修复方案——启动时读取模板获取列索引，不再缓存第一个导入模板的列映射）；⚠️漏记通知渠道，9/1建issue时未补 |

## 2026-09-03

| PRD编号 | 标题 | 分发日期 | 接收人 | 状态 | 备注 |
|---------|------|----------|--------|------|------|
| ADM-39 | [ADM] 监测点信息导出模板与存储表结构对应优化 | 2026-09-03 | Loop adm-pm助手专家 | cancelled | 提需人：吴济；通知渠道：群:9f78c49daf00466a8eb58ede140f52b6；优先级high；优化整个监测点信息导出模板匹配逻辑（单活动/批量/多维钻取）；关联ADM-36；issue ID: 3c650d05-e7ff-4698-a19a-77b2fedcb3c1；labels: type/feature+tech/backend+svc/admonitor+svc/ui-report；9/3 16:00 状态 todo→cancelled（已取消）；9/3 16:03 updated（当前cancelled） |
| ADM-40 | [TVM] OTT-GIVT统计：2026年8月各子规则(keyword) by day表现 | 2026-09-03 | wkc 小分队（squad） | in_review | 提需人：王心宇；通知渠道：群:9f78c49daf00466a8eb58ede140f52b6；优先级high；大盘整体；2026-08-01~08-31 by day；各子规则keyword；issue ID: 4bebe45c-ceac-4bdc-addb-3fd09cc5997c；labels: type/investigate+tech/data-tvm+svc/tv-api+svc/tv-query；原指派adm-pm助手专家，心宇要求指派坤城，转指派wkc小分队（leader: wkc-指挥官）；9/3 15:03 in_progress→in_review（请验收） |

---

_每次分发后即时更新。_
