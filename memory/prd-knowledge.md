# PRD 知识库

## AdMonitor 产品全景

### 定位
秒针广告监测产品，做第三方独立监测——广告投了没、多少人看到、效果如何、有没有无效流量。
两条产品线：
- ADM（AdMonitor）：互联网广告监测，覆盖 PC/移动/OTT
- TVM（TVMonitor）：电视广告监测，覆盖有线电视/IPTV/OTT电视

### 核心架构：三个环节
1. **收数**：广告位部署监测代码（JS/API），用户看到广告时触发曝光/点击事件，秒针服务器收到原始日志（rawlog）
2. **清洗**：rawlog → dmlog → tnlog。过滤无效流量（IVT）、去重、地域解析、设备识别。数据质量核心环节
3. **出数**：清洗后日志做聚合计算，按活动/点位/媒体等维度聚合，算出 Imp/Click/UV/Reach/TA 等指标，生成报表

### 功能模块

**活动管理层：**
- CMS 管理广告活动、点位、监测代码
- 活动状态流转：创建→审核→生效→结束

**数据洞察层（产品界面）：**
- Dashboard 总览
- 实时数据
- 基础数据（Imp/Click/UV 等核心指标）
- 到达效果
- 地域分析
- 人群分析（TA、Demography）
- 异常流量（GIVT+SIVT+风险流量+SDK签名校验）
- 转化效果

**高级功能：**
- 多维钻取（按 OS、平台、地域等交叉分析）
- M+任务定制（定制化报表）
- SNAP 监拍（模拟设备截屏验证广告真实露出）

### 核心概念

**监测代码类型：**
- C2S（客户端直发秒针）
- S2S（媒体服务器转发）

**数据口径：**
- acc（从活动开始累计） vs day（单日）
- net（过滤IVT后） vs totalnet（包含部分过滤前）
- by_audience 分 overall/stable/target 三种人群维度

**核心指标：**
- Imp（曝光）
- Click（点击）
- UV（独立曝光用户）
- Clicker（独立点击用户）
- CTR = Click/Imp
- Reach = 接触UV/Universe
- TA = 目标人群占比

### 接口文档
- 官方API文档：https://docs.cn.miaozhen.com/api-docs/index.html
- 三大板块：AdMonitor API、TV Monitor API、多维查询API
- ⚠️ SPA页面，需浏览器打开，爬不到内容

### 已知坑类别
- API分页：很多接口默认只返回500条（TVM 300条），不翻页会丢数据
- 数据时效：当天数据不是最终值，要等清洗跑完
- 参数大小写敏感
- ADM和TVM分页参数语义不同，不能套用
- M+任务定制参数多，坑也多

### 当前在做的
- 多维API刚上线，核心接口已通
- 布点项目（监测代码部署测试）
- 批量创建点位
- 几个KA客户专属项目在进行

---

## PRD 标准模板

（待填充——第一个 PRD 落地时建立模板）

## 分发规则

### 分发判断逻辑
1. 根据需求涉及的产品线（ADM/TVM）和技术方向（前端/后端/大数据/端侧/SDK）匹配对应研发
2. 大数据需求不确定归属时，ADM/TVM 大数据都先指给张成
3. 前端/后端需求指给吕金果，由他二次分配
4. 多个方向同时涉及的需求，分别@对应负责人

### 问题排查类分发原则
- **自动性任务/发送类问题**（如自动日报未发送、任务状态异常）：**默认只分后端**（吕金果），不同时 @ 大数据侧。后端先查发送/调度链路，如果定位到是数据生成问题再升级到大数据侧。不要上来就 @ 所有人。
- 避免不必要的跨方向同步排查，减少干扰。

### 特定方向直派规则（产品指定）
- **OTT-GIVT 相关统计需求** → **吴坤城**（TVM大数据研发，负责TVA数据计算/SIVT）。产品（王心宇）2026-08-28 明确要求，后续此类需求跳过兑底直接指派坤城。

### 分发格式参考
- @对应研发 + PRD链接/文件
- 简述需求要点和优先级
- 明确验收标准和期望完成时间

## 研发对应关系

### 前端/后端（ADM/TVM）
| 研发 | 职责 | 下游指派 |
|------|------|----------|
| 吕金果 | ADM/TVM 前端和后端技术负责人 | 根据需求指派给黄春波、李晴晴 |
| 黄春波 | 前端研发（吕金果指派） | — |
| 李晴晴 | 前端研发（吕金果指派） | — |

### 端侧 / SNAP
| 研发 | 职责 |
|------|------|
| 周康平 | 端侧研发，实验室相关工作，SNAP 采集/云手机侧开发 |
| 囡囡（贾囡囡） | SNAP 计算（吕金果团队）；（uid 待补，Space 搜不到”贾囡囡“，可能不是本名）|

### 大数据（ADM/TVM）
| 研发 | 职责 |
|------|------|
| 张成 | ADM/TVM 大数据技术负责人（**兑底指派**：不确定的大数据需求都可指给他） |
| 董文菁 | ADM 大数据研发，Terran 收数处理 |
| 于长亮 | ADM 大数据研发，实时数据/ETL/DM/宝洁朋友圈/宝洁日志传输/总局iptv项目 |
| 陈龙 | ADM 大数据研发，CT |
| 杨春雪 | ADM 大数据研发，SIVT/dr2pg |
| 陈鹏 | ADM 大数据研发，DR及panel研发制作，universe/panel相关问题指给他 |
| 吴坤城 | TVM 大数据研发，TVA 大数据侧数据计算/PMO计算/SIVT |

### MCP/lite/海外
| 研发 | 职责 |
|------|------|
| 赵思捷 | ADM MCP维护，lite产品维护，海外ADM产品维护 |

### SDK
| 研发 | 职责 |
|------|------|
| 张乾 | Android 秒针 SDK 研发 |
| 王立涛 | iOS 秒针 SDK 研发 |

### 分工动态学习机制

**原则**：分工表只需要增长，不需要完美。新出现方向永远有兑底，被学习吸收后毕业务成指派。
- **兑底指派**：
  - 前端/后端问题→ 吕金果（filter）
  - 大数据问题→ 张成（filter）
- **动态学习路径**：吕金果/张成收到 issue 后转指派给谁 → 谁接了活，谁就是该方向的 owner → 下次同类 case 直接指派具体人
- **学习信号来源**：issue reassignment、issue comment 中被 @ 的研发、issue conversation 中出现“由 XX 接手”
- **学习时机**：当场发现当场学习，不等周回顾；同步到本文件 + Loop 专家 instructions

---

## Issue 状态流转规范（2026-08-24 建立）

Loop 原生 7 个状态：`backlog` / `todo` / `in_progress` / `in_review` / `done` / `blocked` / `cancelled`。使用边界：

| 状态 | 含义 | 进入条件 | 谁动 |
|------|------|---------|------|
| `backlog` | 未确认要不要做 | 产品还没想清楚、未跟干系人对齐 | 建 issue 时可选 |
| `todo` | 确认要做、还没人动起来 | 明确了需求/问题，未进入处理 | 建 issue 默认 |
| `in_progress` | 有人在干活 | 研发/专家开始处理 | 研发或 Loop 专家 |
| `in_review` | 研发做完了、等产品验收 | 研发认为问题解决/需求交付 | 研发推进 |
| `done` | 产品验收通过、真正闭环 | 产品验证后点验收 | 产品 |
| `blocked` | 现阶段没有想到明确使用场景 | （暂不用） | — |
| `cancelled` | 重复/误建/不再需要做 | 发现与别的 issue 重复、或明确不需要做 | 任何人，但必须加关闭原因 |

### 要点
- **backlog vs todo**：backlog = 产品还没想清楚；todo = 确认了要做但没启动
- **in_review = 产品验收阶段**：研发推进到这里后，产品验收过了才进 done
- **cancelled 必须加原因**：写明重复对象 / 为什么不需要做，后来者能查到上下文
- **blocked 暂不用**：等出现场景再说

### 重复 issue 处理原则
同一问题被重复建了 issue（主 issue 重复 / 子 issue 重复）：
1. 保留信息量最全、遵循最新分发规范的那个
2. 重复的一律 cancelled，评论里说明重复对象和后续跟进位置
3. 不保留“留着看”心态，避免状态不同步

---

## Label 体系（2026-08-24 建立）

### 维度说明
- **Project**：粗粒归属，一个 issue 只属于一个 project。当前保持现状 `adm 需求指派`，不新增
- **Label**：细粒属性，一个 issue 可同时打多个

### type/*（工作性质，必选其一）
| label | 含义 | 什么时候用 |
|-------|------|-----------|
| `type/feature` | 新功能/增强 | 要新开发 |
| `type/bug` | 确认的产品缺陷 | 数据和预期不符且是产品问题 |
| `type/investigate` | 排查中，未定 bug | 现象有了，原因未知（初始默认）|
| `type/operation` | 运营/配置/权限类 | 不需要写代码，但要操作 |
| `type/consult` | 咨询/答疑 | 不需要动手，要解释 |

**重要**：`type/bug` 与 `type/feature` 不是二选一。初期都打 `type/investigate`，定位后再改。

### tech/*（技术方向，决定分发对象）
| label | 分发对象 |
|-------|---------|
| `tech/frontend` | 吕金果→黄春波/李晴晴 |
| `tech/backend` | 吕金果 |
| `tech/data-adm` | 张成 |
| `tech/data-tvm` | 张成→吴坤城 |
| `tech/sivt-adm` | 杨春雪 |
| `tech/sivt-tvm` | 吴坤城 |
| `tech/ivt` | 周康平 |
| `tech/snap-collect` | 周康平 |
| `tech/snap-compute` | 囡囡（贾囡囡、金果团队；uid 待补；先兑底吕金果转派）|
| `tech/sdk-android` | 张乾 |
| `tech/sdk-ios` | 王立涛 |

### 客户标识
| label | 含义 |
|-------|------|
| `ka/pg` | 宝洁专属，其他客户不算 KA |

### svc/*（保留现有 7 个，服务定位补充）
`svc/admonitor`、`svc/intra-api`、`svc/tv-api`、`svc/tv-query`、`svc/tv-web`、`svc/ui-report`、`svc/verify-api`

### 交叉使用示例
| 场景 | Label 组合 |
|------|-----------|
| 宝洁客户提了 SIVT 数据异常 | `ka/pg` + `type/investigate` + `tech/sivt-adm` |
| 自动日报没发送，初期排查 | `type/investigate` + `tech/backend` |
| SNAP 监拍异常 | `type/investigate` + `tech/ivt` |
| SNAP 计算异常 | `type/investigate` + `tech/snap-compute` |
| 客户要 SNAP 采集异常 | `type/investigate` + `tech/snap-collect` |
| ADM 数据对不上 | `type/investigate` + `tech/data-adm` |
| 确认是产品 bug | 改 `type/bug`，定位到具体 `tech/*` |

---

_每次 PRD 相关工作完成后，更新此文件。_
