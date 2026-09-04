# 需求跟踪

格式：需求编号 | 标题 | 状态 | 负责人 | 最后更新 | 备注

状态枚举：梳理中 | 待分发 | 已分发 | 开发中 | 已完成 | 已搁置

---

| 需求编号 | 标题 | 状态 | 负责人 | 最后更新 | 备注 |
|-----------|------|------|--------|----------|------|
| ADM-33 | [TVM] 多维自动报告异常（任务1106395/1106394） | 开发中 | Loop adm-pm助手专家 | 2026-09-03 17:54 | 提需人：邢思源；优先级high；9/3 17:54 状态变更 todo→in_progress；无通知渠道跳过通知 |
| ADM-35 | [ADM] 统计caid版本信息（2026年7月日志） | 开发中 | 于长亮 | 2026-09-02 15:42 | 提需人：邢思源；优先级high；9/2 15:42 状态 todo→in_progress；无来源群group_id跳过通知 |
| ADM-36 | [ADM] 监测点信息导出extInfo字段异常 | in_review | Loop adm-pm助手专家 | 2026-09-04 13:02 | 提需人：吴济；优先级high；9/4 11:16 in_progress→in_review（请验收）；9/4 11:18 in_review→in_progress + 指派人变更（4f356f9a→cab5ac70）+ 新评论（提测通知：已修复并合并到测试分支develop分支，请验收）；9/4 13:02 in_progress→in_review（请验收）+新评论（测试反馈：问题活动2513757和2512416单活动/批量导出信息均对齐；批量导入新建活动2514111导出信息均对齐；没有旧模板无法测试；手动建空活动后单活动模板导入不成功找不到原因）；无通知渠道跳过通知 |
| ADM-26 | ADM M+ 任务定制 API 接口开发（ADM-24子任务） | 开发中 | Loop adm-pm助手专家 | 2026-09-03 16:06 | 提需人：胡映昕；父需求ADM-24；9/2 14:34 指派人变更+新评论（技术负责人审核反馈：mplus配置前缀应使用admonitor、prod环境redis配置需修正）；9/2 14:47 指派人变更+新评论（配置修改已完成：mplus配置前缀统一到admonitor命名空间，从mz.mplus.*迁移到mz.admonitor.mplus.*）；9/2 14:47 新评论（确认合并）；9/2 14:56 指派人变更+新评论（OCTO-LOOP合并指令：技术负责人确认合并，请将feat/ADM-26-mplus-api合并到feature/260831-mplus-api并push）；9/3 14:51 指派人变更（4f356f9a→38aeb0d2）+新评论（技术负责人要求：M+ list接口需补充ES查询能力，与admonitor web端保持一致，参考intra-api多维查询）；9/3 15:25 指派人变更（38aeb0d2→4f356f9a）+新评论（M+ list接口ES/MzSearch查询能力已补充完成，参考AdQueryTaskListServiceImpl实现，接入ES主路径+MySQL透明降级）；9/3 15:51 指派人变更（4f356f9a→38aeb0d2）+新评论（OCTO-LOOP启动报错修复：mz.admonitor.mplus.list.es.base-url is required when mz.admonitor.mplus.list.es.enabled=true，M+ list ES不应启用）；9/3 16:06 指派人变更（38aeb0d2→4f356f9a）+新评论（启动报错修复：M+ list ES 复用 ADM MzSearch 集群配置，已按技术负责人要求修复启动报错，M+ list ES 现在直接复用 AdMonitor query/list 集群配置）；9/3 16:10 指派人变更（38aeb0d2→4f356f9a）+新评论（补充说明：16:06的修复已覆盖dispatcher派发要求，commit f86d63a已push到feature/260831-mplus-api：已删除独立MplusMzSearchClientConfig.java不重复建RestC）；9/3 16:13 新评论（🤖 OCTO-LOOP 启动报错已修复 commit f86d63a 已push到feature/260831-mplus-api：1.删除独立MplusMzSearchClientConfig不再重复建RestClient/校验base-url 2.ES）；老issue无通知渠道，跳过通知 |
| ADM-38 | [TVM] OTT GIVT举证开发需求 | 已分发 | Loop adm-pm助手专家 | 2026-09-02 16:00 | 提需人：王心宇；优先级high；9/2 15:13 指派人变更（adm-pm助手→7bcc9ad4）+新评论（需求审核报告：复述需求内容，确认提需人王心宇，目标承接人待定）；9/2 16:00 指派人变更（7bcc9ad4→d5ca704c）；来源群无group_id跳过通知 |
| ADM-37 | [TVM] SIVT线上举证条数限制（新增设备规则） | in_review | Loop adm-pm助手专家 | 2026-09-02 14:21 | 提需人：王心宇；优先级P1/high；期望本周(9/5前)；9/2 11:33 状态 in_progress→in_review（请验收）；9/2 14:21 指派人变更（adm-pm助手→d5ca704c）；来源群无group_id跳过通知 |
| ADM-28 | M+ 任务下载 CSV 字段错列 — 导出逻辑修复（ns字段逗号未转义）（ADM-27子任务） | 开发中 | Loop adm-pm助手专家 | 2026-09-02 15:43 | 提需人：胡映昕；父需求ADM-27；9/2 15:43 状态 todo→in_progress；9/2 15:43 新评论（ns字段回传多ip导致M+取值异常，ns只适配单个ip，多ip违背设计）；老issue无来源群跳过通知 |
| ADM-12 | [BUG] TvMonitor：无布点计算权限用户新建活动时，布点计算字段未设默认值 | 已闭环 | Loop adm-pm助手专家 | 2026-09-02 11:51 | 9/2 11:51 in_review→done 已闭环；老issue无来源群记录 |
| ADM-17 | [bug] tvmonitor 活动管理：自定义人群发布TA重算失败 + 活动列表空指针 | 已闭环 | Loop adm-pm助手专家 | 2026-09-03 16:48 | 老issue无通知渠道；9/3 10:49 in_review→done 已闭环；子任务ADM-22（自定义人群发布TA重算时未传布点计算参数）9/3 14:39 in_review→done 已闭环；子任务ADM-21（活动列表/campaign/list空指针NPE修复）9/3 16:48 in_review→done 已闭环 |
| ADM-15 | [TVM] 监测代码OTT媒体列表添加媒体：银河新电视 | 已闭环 | Loop adm-pm助手专家 | 2026-09-02 11:51 | 提需人：关甜甜；9/2 11:51 in_review→done 已闭环；老issue无来源群group_id跳过通知 |
| ADM-18 | [TVM] OTT-GIVT统计需求测试：20260826大盘整体分规则统计 | 已闭环 | Loop adm-pm助手专家 | 2026-09-03 15:37 | 提需人：王心宇；9/3 15:36 in_progress→done 已闭环；9/3 15:37 updated（当前done）；老issue无通知渠道跳过通知 |
| ADM-16 | [TVM] ott-givt 分规则统计需求（活动4144746） | 已闭环 | Loop adm-pm助手专家 | 2026-09-03 15:37 | 提需人：王心宇；9/3 15:37 in_review→done 已闭环；老issue无通知渠道跳过通知 |
| ADM-19 | [GIVT查询] 20260826 大盘整体 OTT-GIVT 分规则统计（ADM-18子任务） | 已闭环 | Loop adm-pm助手专家 | 2026-09-03 15:35 | 提需人：王心宇；父需求ADM-18；9/3 15:35 in_review→done 已闭环；老issue无通知渠道跳过通知 |
| ADM-39 | [ADM] 监测点信息导出模板与存储表结构对应优化 | 已搁置 | Loop adm-pm助手专家 | 2026-09-03 16:03 | 提需人：吴济；优先级high；9/3 16:00 状态 todo→cancelled（已取消）；9/3 16:03 updated（当前cancelled）；关联ADM-36；已通知群聊@吴济 |
| ADM-40 | [TVM] OTT-GIVT统计：2026年8月各子规则(keyword) by day表现 | in_review | wkc 小分队 | 2026-09-03 15:03 | 提需人：王心宇；优先级high；9/3 15:03 in_progress→in_review（请验收） |
| ADM-41 | [ADM] DR报告与数据定制模块操作系统数据不一致排查（活动2495707） | 开发中 | Loop adm-pm助手专家 | 2026-09-03 20:26 | 提需人：邢思源；优先级high；9/3 20:22 状态变更 todo→in_progress；9/3 20:26 拆分新子任务 ADM-42；已通知群聊@邢思源 |
| ADM-42 | [ADM] DR报告与数据定制模块OS数据不一致排查 — 数据侧（活动2495707） | 已分发 | Loop adm-pm助手专家 | 2026-09-03 20:26 | 提需人：邢思源（继承父需求ADM-41）；优先级high；父需求ADM-41；9/3 20:26 新建子任务；已通知群聊@邢思源 |
| ADM-43 | [ADM] 多维钻取API地域字典不完整（OpenAPI /cms/v1/regions/list 缺86个地级市） | in_review | Loop adm-pm助手专家 | 2026-09-04 17:04 | 提需人：胡映昕；优先级high；issue ID: 8087a516-9d11-4b1c-9273-165c6780613e；9/4 16:58 状态变更 todo→in_progress；9/4 17:04 状态变更 in_progress→in_review（请验收）+新评论（需求审核与分发完成：OpenAPI返回251个地级市，多维钻取全量337个，缺86个，已拆分后端子任务ADM-44）+拆分新子任务ADM-44；已通知群聊@胡映昕 |

| ADM-44 | [后端] 修复 OpenAPI /cms/v1/regions/list 地域字典缺失86个地级市（ADM-43子任务） | 开发中 | Loop adm-pm助手专家 | 2026-09-04 17:05 | 提需人：胡映昕（继承父需求ADM-43）；父需求ADM-43；9/4 17:05 状态变更 todo→in_progress + 指派人变更（4f356f9a→d0ff2b22）；已通知群聊@胡映昕 |

---
