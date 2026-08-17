# 字段清单（核心）

> AdMonitor 知识参考材料，用于需求审核粗判。标记"知识参考，非最终判断"。
> 完整字段注册表见 memory/admonitor-field-registry.md（🔒 不对外暴露）。

## 监测代码基础字段

| 字段 | 含义 | 来源 |
|------|------|------|
| k | 活动ID | 秒针生成 |
| p | 点位ID | 秒针生成 |
| m | 媒体ID | 秒针生成 |
| rt | 返回类型，rt=2返回1×1像素 | — |
| ns | 媒体回传的IP | 媒体回传 |
| ni | 媒体IES订单ID | 媒体回传 |
| v | 广告位所在页 | 媒体回传 |
| tr | 媒体唯一请求ID | 媒体回传 |
| o | 点击落地页地址 | — |
| nt | S2S日志实际发生时间 | — |

## 设备ID字段（m0~m14系列）

| 字段 | 含义 | 采集方式 |
|------|------|----------|
| m0 | OpenUDID（iOS6以下） | 媒体/SDK |
| m0a | Windows Phone DUID | 媒体/SDK |
| m1 | AndroidID原始值 | 媒体/SDK |
| m1a | AndroidID MD5 | 媒体/SDK |
| m2 | IMEI MD5 | 媒体/SDK |
| m3 | IMEI原始值 | 媒体/SDK |
| m4 | 海外AAID | 媒体回传 |
| m5 | IDFA原始值 | 媒体/SDK |
| m5b | IDFA MD5 | 媒体/SDK |
| m6 | MAC（保留冒号）MD5 | 媒体/SDK |
| m6a | MAC（去除冒号）MD5 | 媒体/SDK |
| m6b | OTT有线MAC MD5 | 媒体/SDK |
| m6c | OTT无线MAC MD5 | 媒体/SDK |
| m6d | OTT蓝牙MAC MD5 | 媒体/SDK |
| m11 | OAID原始值 | 媒体/SDK |
| m11a | OAID MD5 | 媒体/SDK |
| m14 | CAID原始值 | 媒体/SDK |
| m14a | CAID MD5 | 媒体/SDK |

## UUID取值优先级（OTV 22级）

```
m5b → m5 → m11a → m11 → m2 → m3 → m14 → m14a → m1a → m1 → m0 → m0a → m6 → m6a → ai → na → bd → m9(IP+UA合成) → a(MZID cookie)
```

## UUID取值优先级（OTT 9级）

```
m6b → m6c → m6d → m6a → m6 → m1a → m1 → m9 → a
```

## 媒体专属ID

| 字段 | 含义 | 来源 |
|------|------|------|
| ai | 阿里Uni ID | 阿里EAR |
| bd | 字节bdid | 字节系媒体 |
| re | 小红书ID | 小红书 |
| jd | 京东ID | 京东 |
| na | 腾讯DAR ID / Yahoo IDFA | 腾讯/Yahoo |

## 剧目监测字段

| 字段 | 含义 |
|------|------|
| nd | 剧目ID |
| np | 剧目顺位 |
| nn | APP名称/平台判断 |
| nc | 剧目vid |
| nf | 一级频道名称 |
| ne | 二级频道名称 |
| ng | 剧目所在URL |

## 可见曝光字段

| 字段 | 含义 |
|------|------|
| vx | 0=普通曝光/1=可见曝光/2=加载/3=可测量/4=不可见 |
| vi | 可见曝光持续时间 |
| vh | 可见像素占比 |
| vb | 视频广告时长 |
| vc | 中点监测（mid/end） |

## ETL生成字段（核心）

| 字段 | 含义 | 说明 |
|------|------|------|
| uuid | 最终用户唯一标识 | 由优先级决定 |
| idfrom | uuid的判定来源 | — |
| plt | 平台标识 | pc=0/mobile=1/OTT=3 |
| os | 操作系统 | A/i/WP |
| reg | 地域（TOP100 IP库） | 8=中国大陆 |
| rel | 地域（CITY337 IP库） | — |
| rex | 地域（国标码） | — |
| rawip | 秒针收到的原始IP | — |
| ip | 最终参与计算的IP | — |
| ipv | IP类型 | v4/v6 |

## 常见字段陷阱

| 陷阱 | 说明 |
|------|------|
| nx出现2次 | 原TV和PC/MB不同team导致，一个宏参数多个含义 |
| ag/md/mn出现2次 | terran生成与SDK采集同含义 |
| MZID(stable)判定 | PC端24h后再被监测到才算stable |
| m9 | IP+UA合成的指纹信息，精度最低，S2S不回传设备ID时才用 |
