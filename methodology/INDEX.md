# 方法论索引

> 方法论体系: `M{层级}_{类别}{NN}_{Slug}_{Title}.md`
> 18 篇，四板块。物理编号不可变，逻辑组织由本索引定义。

---

## 入门篇 M1 — 开始用 AgentPrecept 之前

| 编号 | 标题 | 解决什么问题 |
|------|------|-------------|
| M1_A00 | [全生命周期](M1_A00_lifecycle_全生命周期.md) | Agent 开发从想法到维护的 8 阶段全景 |
| M1_A01 | [为什么文档先行](M1_A01_why-docs-first_为什么文档先行.md) | 散文指令 vs 结构化数据——为什么让 Agent 读文件比读 prompt 可靠 |
| M1_A02 | [自然语言编程指南](M1_A02_natural-lang_自然语言编程.md) | 不会写代码的人怎么用自然语言让 Agent 干活 |

## 协作篇 M2 — 人与 Agent 如何配合

| 编号 | 标题 | 解决什么问题 |
|------|------|-------------|
| M2_B00 | [交接模式](M2_B00_handoff_交接模式.md) | Agent 换班不丢进度——HANDOFF.md 怎么写 |
| M2_B01 | [人-Agent 协作](M2_B01_human-agent-collab_人机协作.md) | Agent 什么时候停、什么时候问、什么时候等确认 |
| M2_B02 | [非技术审 Agent 产出](M2_B02_non-tech-review_非技术审产出.md) | 不懂代码怎么看 Agent 做得好不好 |
| M2_B03 | [Agent 自管理](M2_B03_agent-self-mgmt_Agent自管理.md) | Agent 提交前的自检清单——ripple_check + pre-commit + audit |

## 工程篇 M3 — 代码治理

| 编号 | 标题 | 解决什么问题 |
|------|------|-------------|
| M3_C00 | [命名即导航](M3_C00_naming_命名即导航.md) | 文件命名就是第一个设计决策——L{Level}_{CAT}{NN} 体系 |
| M3_C01 | [设计依据](M3_C01_design-rationale_设计依据.md) | 每次技术决策记一行——"为什么选这个"防止 Agent 推倒重来 |
| M3_C02 | [三层项目图](M3_C02_project-graph_三层项目图.md) | project-graph.yaml 让 Agent 30 秒读懂项目结构 |
| M3_C03 | [开发工作流](M3_C03_dev-workflow_开发工作流.md) | 修 bug、加功能、重构——三场景下 agentprecept 怎么介入 |
| M3_C04 | [工程化实践](M3_C04_engineering_工程化实践.md) | CI/CD、pre-commit、多环境管理的 agentprecept 配置 |
| M3_C05 | [安全实践](M3_C05_security_安全实践.md) | Agent 写代码时的最低安全门槛 + Prompt 注入防护 |
| M3_C06 | [性能优化](M3_C06_performance_性能优化.md) | 性能审计与 project-graph 的关联 |
| M3_C08 | [已有项目接入](M3_C08_existing-project_已有项目接入.md) | 不是新项目——已有代码怎么渐进式引入 agentprecept |

## 运维篇 M4 — 质量与审查

| 编号 | 标题 | 解决什么问题 |
|------|------|-------------|
| M4_D00 | [审计框架](M4_D00_audit-framework_审计框架.md) | 15 维 4-scope 审计——查什么、怎么自动化、怎么读报告 |
| M4_D01 | [生产就绪](M4_D01_production-readiness_生产就绪.md) | 每个阶段做到什么程度才算合格——8 阶段退出标准 |
| M4_D02 | [Agent 运维](M4_D02_agent-ops_Agent运维.md) | Agent 常见故障：超时、锁文件、分支冲突——怎么处理 |

---

## 命名体系说明

方法论使用独立命名体系 `M{层级}_{类别}{NN}_{Slug}_{Title}.md`：

| 字段 | 含义 | 当前取值 |
|------|------|---------|
| M | 方法论标识 | 固定 |
| 层级 | 1-4 难度递进 | 1 入门 / 2 协作 / 3 工程 / 4 运维 |
| 类别 | A-D 主题分类 | A 流程 / B 设计 / C 开发 / D 审计 |
| NN | 类别内编号 | 00+，新篇末尾追加，不引发涟漪 |
| Slug | 英文短标识 | 小写连字符 |
| Title | 中文标题 | 面向人类读者 |

与 `docs/` 的 L{1-4}_{A-P}{NN} 体系独立——两棵树，一条引用。详见 `docs/L1_A02_命名规范.md`。
