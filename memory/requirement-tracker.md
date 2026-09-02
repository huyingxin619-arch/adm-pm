# 需求跟踪

格式：需求编号 | 标题 | 状态 | 负责人 | 最后更新 | 备注

状态枚举：梳理中 | 待分发 | 已分发 | 开发中 | 已完成 | 已搁置

---

| 需求编号 | 标题 | 状态 | 负责人 | 最后更新 | 备注 |
|-----------|------|------|--------|----------|------|
| ADM-33 | [TVM] 多维自动报告异常（任务1106395/1106394） | 已分发 | Loop adm-pm助手专家 | 2026-09-02 14:03 | 提需人：邢思源；优先级high；9/2 14:03 状态 blocked→todo + 指派人变更 + 新评论（OCTO-LOOP流程纠正：误判涉及svc/ui-report导致阻塞，实际标签svc/tv-web+svc/tv-query，由tv cloud web worker统一处理）；9/2 14:03 新评论（等待三个探索agent完成代码分析，搜索api代码库auto-report功能）；无来源群group_id跳过通知 |
| ADM-35 | [ADM] 统计caid版本信息（2026年7月日志） | 已分发 | 于长亮 | 2026-09-01 | 提需人：邢思源；优先级high |
| ADM-36 | [ADM] 监测点信息导出extInfo字段异常 | 开发中 | Loop adm-pm助手专家 | 2026-09-02 14:20 | 提需人：吴济；优先级high；9/1 21:15 新评论（extInfo列位置是运行时扫描表头fieldName→列号映射，要求提供日志格式去服务器查看）；9/2 14:20 指派人变更+新评论（extInfo列索引扫描相关日志说明：现有日志仅2行在SpotsInfoServiceImpl.java的findExtInfoIndexFromExcel()方法内）；无来源群group_id跳过通知 |
| ADM-26 | ADM M+ 任务定制 API 接口开发（ADM-24子任务） | 开发中 | Loop adm-pm助手专家 | 2026-09-02 11:38 | 提需人：胡映昕；父需求ADM-24；9/2 11:38 指派人变更+新评论（OCTO-LOOP审核修改完成：已移除7个文件中"异常流量任务"措辞，纯文档/注释变更无业务逻辑，fix commit 8d646e2已push并合并总开发分支fea）；老issue无来源群，跳过通知 |
| ADM-37 | [TVM] SIVT线上举证条数限制（新增设备规则） | in_review | Loop adm-pm助手专家 | 2026-09-02 14:21 | 提需人：王心宇；优先级P1/high；期望本周(9/5前)；9/2 11:33 状态 in_progress→in_review（请验收）；9/2 14:21 指派人变更（adm-pm助手→d5ca704c）；来源群无group_id跳过通知 |
| ADM-12 | [BUG] TvMonitor：无布点计算权限用户新建活动时，布点计算字段未设默认值 | 已闭环 | Loop adm-pm助手专家 | 2026-09-02 11:51 | 9/2 11:51 in_review→done 已闭环；老issue无来源群记录 |
| ADM-15 | [TVM] 监测代码OTT媒体列表添加媒体：银河新电视 | 已闭环 | Loop adm-pm助手专家 | 2026-09-02 11:51 | 提需人：关甜甜；9/2 11:51 in_review→done 已闭环；老issue无来源群group_id跳过通知 |

---

_每次状态变更即时更新。_
