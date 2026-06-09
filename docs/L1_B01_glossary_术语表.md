# 术语表

> 分类: B | 层级: L1 | 编号: L1_B01
> 状态: 📝 撰写中 | 目标读者: 全部

---

## 使用方式

本表记录项目中所有专用术语的定义和标准译法。在文档和代码注释中使用统一术语。

Agent 在生成内容前应参照本表确保用词一致。

---

## 核心术语

| 术语 | 英文 | 定义 | 首次出现于 |
|------|------|------|:--:|
| AgentPrecept | AgentPrecept | 一套 Agent 开发方法论，覆盖从想法到维护的完整循环（8 阶段），包含规范层、CLI/MCP 层、方法论层、模板层和示例层 | README |
| project-graph.yaml | project-graph.yaml | 项目依赖关系图配置文件，描述模块间引用关系、稳定性等级和 ADR 演进记录，是 agentprecept 的核心数据结构 | L2_D01 |
| HANDOFF.md | HANDOFF.md | 会话交接文件，记录 Agent 会话间的上下文传递，包含状态标记（🔥 活跃 / 📝 撰写中 / ✅ 锁定）和未完成事项 | L2_D01 |
| MEMORY.md | MEMORY.md | 持久偏好与项目约束文件，存储跨会话的 Agent 行为偏好、项目特定规则和长期记忆 | L2_D01 |
| L4_O01 | L4_O01 | 设计依据文档编号（层级 L4，分类 O，编号 01），记录项目关键设计决策及其理由和证据 | INDEX |
| 设计先行 | Design-First | agentprecept 核心原则之一：在编写代码之前先完成设计文档（project-graph.yaml + 设计依据），通过 design_gate 检查后才能进入实现阶段 | methodology/M1_A01 |
| Auto-Pilot | Auto-Pilot | agentprecept 的自动化工作流模式：Agent 在明确规范约束下自主完成 init → sync → audit 循环，无需人工干预 | methodology/M4_D02 |
| MCP Server | MCP Server | Model Context Protocol 服务端，agentprecept 提供 6 个 MCP tool（project_graph_query / decision_search / design_gate / sync_diff / audit_run / handoff_read）供外部 Agent 调用 | docs/mcp-tools |
| 涟漪分析 | Ripple Analysis | 修改影响范围分析：当变更一个模块时，通过 project-graph.yaml 的依赖图自动计算所有受影响的上下游模块 | methodology/M4_D00 |
| 4-scope 审计 | 4-Scope Audit | agentprecept 的四层审计体系：文档审计（命名/引用/术语/一致性）、工程审计（覆盖率/骨架/内容）、体验审计（用户旅程/可读性/定位）、健壮审计（复用性/社区就绪度） | L2_D01 |

---

## 缩写

| 缩写 | 全称 | 说明 |
|------|------|------|
| MCP | Model Context Protocol | 模型上下文协议，Agent 与外部工具/服务的标准化通信协议，agentprecept 基于此提供 6 个 tool |
| ADR | Architecture Decision Record | 架构决策记录，记录关键设计决策及其上下文、理由和后果，存储在 project-graph.yaml 的 evolution 字段中 |
| CLI | Command-Line Interface | 命令行界面，agentprecept 提供 init/sync/audit/setup/hooks/gnhf 六组命令 |
| CI | Continuous Integration | 持续集成，agentprecept 通过 GitHub Actions 运行 audit + test-examples 两条流水线 |
| YAML | YAML Ain't Markup Language | 一种人类可读的数据序列化格式，agentprecept 使用 YAML 编写 project-graph.yaml 项目图配置 |
