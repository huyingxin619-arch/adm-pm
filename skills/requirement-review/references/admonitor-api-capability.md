# API 能力范围清单

> AdMonitor 知识参考材料，用于需求审核粗判。标记"知识参考，非最终判断"。

## 产品线与Base URL

| 产品 | Base URL | 说明 |
|------|----------|------|
| ADM | `https://api.cn.miaozhen.com` | PC+Mobile广告监测 |
| TVM | `https://api-tvmonitor.cn.miaozhen.com` | OTT电视广告监测 |
| M+任务定制 | `http://admtaskapi.cn.miaozhen.com/mplus/task/submit` | 跨活动排重/重叠/独占 |
| 多维查询 | `https://intra-api.miaozhen.com` | 多维钻取API（异步任务） |

## ADM API 能拉到的数据

### 基础数据报告（/admonitor/v1/reports/basic/show）
- ✅ Imp / Click / UV / Clicker（累计/单天/日均/分小时）
- ✅ 按活动/媒体/点位/关键词维度
- ✅ 按地域（全球省级/地级市）
- ✅ net / totalnet 过滤
- ✅ PC / Mobile / PM 平台

### 实时数据报告（/admonitor/v1/reports/realtime/show）
- ✅ 当天实时Imp/Click（约15min更新）
- ✅ 分小时数据
- ⚠️ 仅overall，无stable/target
- ⚠️ 未经GIVT过滤

### 到达人群报告（/admonitor/v1/reports/reach/show）
- ✅ GRP / iGRP
- ✅ 1+~10+ 到达人数
- ✅ 相交样本量
- ✅ 累计Imp

### SIVT异常流量报告（/admonitor/v1/reports/sivt/show）
- ✅ 当天异常曝光/点击数
- ⚠️ 仅day指标，无acc
- ⚠️ 仅overall，不支持by_audience
- ⚠️ 未开通SIVT分地域的活动只返回全球维度

## ADM API 拉不到的数据（仅界面）

| 数据 | 说明 |
|------|------|
| Demography（人群属性） | 性别/年龄/教育/收入分布，仅界面可查 |
| 个性分析 | App/操作系统/联网方式/终端类型，仅Mobile |
| 地域分析详细数据 | 界面有UV/UV%/Index等，API仅基础指标 |
| 转化效果 | MiniSite转化数据 |
| Reach%-UG（User-Graph版本） | 仅界面 |
| Est.Imp / Est.Click（排期预估） | 仅界面 |
| Cost / Days / CMK | 仅界面 |
| SDK签名校验数据 | KA专属，仅界面 |

## TVM API 与ADM的差异

| 差异点 | ADM | TVM |
|--------|-----|-----|
| Token | 需client_id+client_secret | 只需username+password |
| 活动列表分页 | limit=M,N（M=偏移量） | pageSize+pageNo（pageNo从1开始） |
| programs/list分页 | — | limit=M,N但M=页码不是偏移量 |
| 点击数据 | 有 | 无（OTT无点击） |
| by_audience | overall/stable/target | overall/people/target/targetdevice |
| 默认limit | 0,500 | 0,300 |
| filtration_type | net/totalnet | net/totalNet（大写N） |
| 点位信息 | /cms/v1/campaigns/list_spots | /monitortv/v1/spot/list |

## M+任务定制 API 能力

| 能力 | 说明 |
|------|------|
| 跨活动排重 | 多个活动UV去重 |
| 重叠分析 | 多个活动交集 |
| 独占分析 | 某活动相对于其他活动的差集 |
| 自定义维度分组 | 29个字段可选，最多5个 |
| 分频次UV/Clicker | 1+~N+（Maxreach控制，默认10+） |
| 可见曝光数据 | 需权限，无点击数据 |

## 多维查询 API 能力

| 能力 | 说明 |
|------|------|
| ADM固定模板 | 按活动/网站/广告位 |
| ADM自定义模板 | 多维钻取（维度自由组合） |
| TVM固定模板 | 按活动/网站/广告位 |
| 异步任务 | 提交→排队→下载 |

## 分页已知坑

| 接口 | 默认 | 翻页方式 |
|------|------|----------|
| ADM列表类 | limit=0,500 | 500,500 → 1000,500（M=偏移量） |
| TVM campaigns/list | pageSize=15,pageNo=1 | pageNo递增 |
| TVM programs/list | limit=M,N | M=页码不是偏移量（与ADM语义不同！） |
| ADM报表 | limit=0,500 | 同列表类 |

## 数据时效

| 数据类型 | 完成时间 |
|----------|----------|
| ADM/TVM基础数据（Net） | 次日10:00 |
| ADM/TVM Verify数据（IVT） | 次日12:00 |
| ADM/TVM分地域数据 | 次日20:00 |
| ADM/TVM Total Net数据 | 次日20:00 |
| 实时数据 | 约15分钟更新 |
| M+任务 | 异步，需轮询查询状态 |

## 限流

| 接口 | 用户级 | 全局 |
|------|--------|------|
| TVM创建任务 | 2次/秒 | 20次/秒 |
| ADM固定模板创建 | 2次/秒 | 20次/秒 |
| ADM自定义模板创建 | 10次/分钟 | 20次/秒 |
| 下载报表 | 单任务5次/分+用户30次/分 | 50次/秒 |
| 批量查询状态 | 10次/秒 | 200次/秒 |

## 错误码速查

| error_code | 含义 |
|------------|------|
| 0 | 正常 |
| 2005 | 活动暂时没有数据 |
| 404 | 接口拼写错误 |
| 40101 | token无效 |
| 40301 | 无权限 |
| 40302 | 指标/维度/平台权限不足 |
| 40305/40312 | 任务数据量过大 |
| 40901 | 任务未完成 |
| 42901 | 触发限流 |
