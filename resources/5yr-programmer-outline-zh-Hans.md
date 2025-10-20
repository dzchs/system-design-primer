# 五年经验工程师核心能力大纲（基于本项目）

说明：本大纲基于本仓库的系统设计与实践内容，按照五年左右从业经验的工程师在工作中应重点掌握与持续精进的领域进行整理。每一条均尽量给出对应的学习入口，优先指向本仓库中文资料。

---

## 1. 系统设计基础认知与方法论

- 概念与权衡
  - 性能与可扩展性：理解二者差异、常见瓶颈与扩展手段
    - 参考：README-zh-Hans.md 中的 [性能与可扩展性](../README-zh-Hans.md#性能与可扩展性)
  - 延迟与吞吐量：如何在可接受延迟下最大化吞吐
    - 参考： [延迟与吞吐量](../README-zh-Hans.md#延迟与吞吐量)
  - 可用性与一致性（CAP）：CP/AP 取舍与分区容错
    - 参考： [CAP 理论](../README-zh-Hans.md#cap-理论)、[一致性模式](../README-zh-Hans.md#一致性模式)、[可用性模式](../README-zh-Hans.md#可用性模式)
- 设计流程（实战通用）
  - 明确用例、约束与假设 → 高层设计 → 核心组件细化 → 扩展与瓶颈处理 → 预估计算
    - 参考： [如何处理一个系统设计的面试题](../README-zh-Hans.md#如何处理一个系统设计的面试题)
  - 粗略估算能力（Back-of-the-envelope）：容量、QPS、存储、网络带宽
    - 参考： [2 的次方表](../README-zh-Hans.md#2-的次方表)、[每个程序员都应该知道的延迟数](../README-zh-Hans.md#每个程序员都应该知道的延迟数)

## 2. 核心基础设施与平台能力

- 网络与边缘
  - DNS：解析、TTL 策略、权威/递归
    - 参考： [域名系统](../README-zh-Hans.md#域名系统)
  - CDN：Push/Pull 策略、缓存层级、命中率优化
    - 参考： [内容分发网络 CDN](../README-zh-Hans.md#内容分发网络cdn)
  - 负载均衡：四层/七层、Active-Active/Active-Passive、会话保持
    - 参考： [负载均衡器](../README-zh-Hans.md#负载均衡器)
  - 反向代理/Web Server：静态/动态分离、TLS 终止、限流
    - 参考： [反向代理（web 服务器）](../README-zh-Hans.md#反向代理web-服务器)
- 应用层架构
  - 单体到微服务演进、领域边界、服务发现、接口契约
    - 参考： [应用层](../README-zh-Hans.md#应用层)、[微服务](../README-zh-Hans.md#微服务)、[服务发现](../README-zh-Hans.md#服务发现)
- 存储系统
  - 关系型数据库（RDBMS）：主从/主主复制、联合（分库分表/联邦）、分片、反规范化、SQL 调优
    - 参考： [关系型数据库管理系统](../README-zh-Hans.md#关系型数据库管理系统rdbms)、[主从复制](../README-zh-Hans.md#主从复制)、[主主复制](../README-zh-Hans.md#主主复制)、[联合](../README-zh-Hans.md#联合)、[分片](../README-zh-Hans.md#分片)、[非规范化](../README-zh-Hans.md#非规范化)、[SQL 调优](../README-zh-Hans.md#sql-调优)
  - NoSQL：KV/文档/宽列/图存储选型与场景，索引、数据模型
    - 参考： [NoSQL](../README-zh-Hans.md#nosql)、[键-值存储](../README-zh-Hans.md#键-值存储)、[文档类型存储](../README-zh-Hans.md#文档类型存储)、[列型存储](../README-zh-Hans.md#列型存储)、[图数据库](../README-zh-Hans.md#图数据库)、[SQL 还是 NoSQL](../README-zh-Hans.md#sql-还是-nosql)
  - 缓存体系：多级缓存、缓存粒度（查询级/对象级）、一致性与失效策略
    - 参考： [缓存](../README-zh-Hans.md#缓存)、[数据库查询级别的缓存](../README-zh-Hans.md#数据库查询级别的缓存)、[对象级别的缓存](../README-zh-Hans.md#对象级别的缓存)、[何时更新缓存](../README-zh-Hans.md#何时更新缓存)、[直写/回写/刷新](../README-zh-Hans.md#直写模式)
- 异步与解耦
  - 消息队列/任务队列：一次性/至少一次/至多一次投递，重试与幂等，死信队列
    - 参考： [消息队列](../README-zh-Hans.md#消息队列)、[任务队列](../README-zh-Hans.md#任务队列)、[背压](../README-zh-Hans.md#背压)
- 通讯协议与 API 设计
  - TCP/UDP、RPC（同步/异步）、REST（资源建模）、API 版本化、节流与配额
    - 参考： [通讯](../README-zh-Hans.md#通讯)、[RPC](../README-zh-Hans.md#远程过程调用协议rpc)、[REST](../README-zh-Hans.md#表述性状态转移rest)
- 安全基线
  - 传输与存储加密、鉴权鉴别（Token/OAuth/JWT）、最小权限、输入校验、审计
    - 参考： [安全](../README-zh-Hans.md#安全)

## 3. 可靠性工程与高可用设计

- 可用性模式与冗余
  - 故障切换（主备/主主）、多 AZ/多 Region、读写分离
    - 参考： [可用性模式](../README-zh-Hans.md#可用性模式)、[主从复制](../README-zh-Hans.md#主从复制)、[主主复制](../README-zh-Hans.md#主主复制)
- 一致性策略
  - 强/最终/弱一致性选择，读写路径设计，数据回放与修复
    - 参考： [一致性模式](../README-zh-Hans.md#一致性模式)
- 弹性与容错
  - 限流、熔断、降级、重试与退避、超时、幂等性设计
  - 热点与分片倾斜处理，流量隔离与灰度发布
- 灾备与恢复
  - RTO/RPO 目标、备份/演练、跨区域容灾

## 4. 可观测性与性能工程

- 监控与告警（Metrics/Logs/Tracing）
  - 主机与应用指标：CPU/内存/IO/GC/队列积压/错误率/尾延迟
  - 日志与链路追踪：结构化日志、采样、相关性 ID
  - 告警策略：阈值/异常检测、分级与值班响应
  - 参考：在 AWS 扩展案例中的监控清单（CloudWatch、statsd、graphite、Sentry、Splunk、Pingdom 等）
    - 入口： [在 AWS 上设计百万级系统 → 监控](../solutions/system_design/scaling_aws/README-zh-Hans.md)
- 压测与容量规划
  - 基准测试、压测模型（恒定/阶梯/峰值）、极限与烧机测试
  - 容量计算与成本优化（按需/预留/自动伸缩）
  - 参考： [延迟数字](../README-zh-Hans.md#每个程序员都应该知道的延迟数)

## 5. 典型系统设计实战（案例导向）

- 短链接/Paste 服务：高 QPS 读、多级缓存、哈希与碰撞、数据模型
  - 入口： [Pastebin 设计](../solutions/system_design/pastebin/README-zh-Hans.md)
- 社交时间线与搜索：写扩散/读放大、Fan-out、搜索索引、反垃圾
  - 入口： [Twitter 时间线与搜索](../solutions/system_design/twitter/README-zh-Hans.md)
- 爬虫系统：URL 去重、队列调度、反爬、分布式抓取与解析
  - 入口： [Web 爬虫](../solutions/system_design/web_crawler/README-zh-Hans.md)
- 理财聚合：第三方集成、数据采集与清洗、隐私与合规
  - 入口： [Mint.com](../solutions/system_design/mint/README-zh-Hans.md)
- 社交图数据结构：图模型、邻接查询、推荐与共同好友
  - 入口： [Social Graph](../solutions/system_design/social_graph/README-zh-Hans.md)
- 搜索引擎 KV 存储：热点键、分片与一致性哈希、SLA 保障
  - 入口： [Query Cache](../solutions/system_design/query_cache/README-zh-Hans.md)
- 分类销售排名：流式/批处理、MapReduce、近实时聚合
  - 入口： [Sales Rank](../solutions/system_design/sales_rank/README-zh-Hans.md)
- 云上扩展范式：从单机到高可用、到读写分离、到自动伸缩、多级缓存、异步化
  - 入口： [在 AWS 上扩展到千万用户](../solutions/system_design/scaling_aws/README-zh-Hans.md)

## 6. 工程实践与代码质量

- API 与契约
  - 领域建模、稳定契约与向后兼容、版本化、速率限制与配额
- 代码质量
  - 可读性与模块边界、错误处理、日志与度量内聚、测试金字塔（单测/集成/端到端）
- 数据与变化管理
  - 数据迁移、在线变更（双写/影子表/灰度）、回滚策略
- 交付与运维（DevOps）
  - CI/CD、基础设施即代码、容器化与编排、发布策略（蓝绿/金丝雀）
- 安全工程
  - 威胁建模、密钥管理、最小权限/零信任、审计与合规（如 GDPR）

## 7. 软技能与协作能力

- 需求澄清与范围控制：明确边界、识别约束、达成共识
- 沟通与文档：设计提案（ADR/设计文档）、变更说明、RCA（故障复盘）
- 估算与优先级：成本—收益分析、排期策略、技术债管理
- 带队与评审：Code Review 原则、Mentoring、跨团队协作

## 8. 学习路径与资源（结合本仓库）

- 按阶段学习
  - 广度优先：快速过一遍 [系统设计主题索引](../README-zh-Hans.md#系统设计主题的索引)
  - 深度优先：选择 2–3 个案例做端到端设计与实现演练（见第 5 部分）
- 强化记忆
  - 使用抽认卡： [系统设计卡片](../resources/flash_cards/System%20Design.apkg)、[练习卡片](../resources/flash_cards/System%20Design%20Exercises.apkg)
- 参考真实世界
  - 阅读： [真实架构](../README-zh-Hans.md#真实架构)、[公司工程博客](../README-zh-Hans.md#公司工程博客)
- 面试与表达
  - 复盘： [如何处理系统设计题](../README-zh-Hans.md#如何处理一个系统设计的面试题)

## 9. 能力分级自检清单

- 必会（上线保真）
  - 能基于需求完成高层设计，识别核心瓶颈
  - 熟悉 RDBMS/缓存/队列/负载均衡的基本用法与常见坑
  - 实施基本告警与监控，能定位 90% 常见问题
- 进阶（规模化）
  - 能设计并落地读写分离、主从复制、水平扩展与多级缓存
  - 掌握一致性/幂等/限流/熔断/降级等可靠性手段
  - 能进行容量规划与成本优化，推动自动化与 CI/CD
- 专家（复杂度治理）
  - 跨地域高可用、灾备、数据治理与安全合规方案设计
  - 架构演进路线图制定（单体 → 微服务/模块化单体/平台化）
  - 以度量驱动的性能与稳定性持续改进

---

## 附：面向对象设计与基础能力补强

- 高频 OOD 练习（巩固抽象与边界）
  - Hash Map、LRU 缓存、呼叫中心、纸牌、停车场、聊天服务
  - 入口：solutions/object_oriented_design 下对应笔记本
- 计算机基础与数据结构
  - 复杂度分析、并发基础、常见数据结构与算法在系统设计中的应用

---

如果你希望将以上大纲用于团队培养或自学计划：

1) 先广度浏览第 1–3 部分，建立系统观；
2) 选择第 5 部分的 2–3 个案例做端到端设计与回顾；
3) 在实际工作中持续将第 4、6、7 部分固化为工程标准；
4) 每季度按第 9 部分进行自检与目标复盘。
