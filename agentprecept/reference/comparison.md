# AgentPrecept 横向对比

> AgentPrecept 不取代任何现有工具——它填补一个空白。

---

## 市场上的 Agent 规范/工具分类

| 类别 | 代表 | 解决什么问题 | AgentPrecept 的关系 |
|------|------|------|------|
| **单页 Agent 指令** | `AGENTS.md` / `CLAUDE.md` / `.cursorrules` | 给 Agent 一段项目背景描述 | AgentPrecept 的 AGENTS.md 属于此类。但它比纯散文多了"硬规则/软建议/自动动作"分层 |
| **项目上下文注入** | OpenCode `.opencode/instructions` | 自动加载项目特定指令 | 兼容——AgentPrecept 的 AGENTS.md 可放任意工具的项目根目录 |
| **Skill 机制** | CodeWhale Skill / OpenCode Skill | 领域技能包（如 PDF/SQL/前端组件） | 互补——AgentPrecept 本身是一个 Skill 包（有 SKILL.md） |
| **多 Agent 编排** | CrewAI / AutoGen | 定义不同 Agent 角色和任务流程 | 不同层面——AgentPrecept 不编排 Agent，它让每个 Agent 在项目中不迷路 |
| **分布式工作流** | OpenClaw / Hermes | 多个 Agent 并行工作的调度 | 互补——这些工具调度 Agent，AgentPrecept 让 Agent 在项目中知道从哪开始 |

---

## AgentPrecept 的不可替代点

### 1. 结构化交接——不是散文，是数据

```
别人的 AGENTS.md:           AgentPrecept:
                            
"项目使用 FastAPI，           project-graph.yaml:
 数据库是 PostgreSQL"         结构层: auth/ → login.py (critical)
                             关系层: login.py → UserModel (calls)
                             L4_O01: JWT | 安全评审 | 无状态
                             HANDOFF: [NEEDS_HUMAN_REVIEW] | 上下文 42%
```

散文 Agent 读一次就忘了。结构化数据每次新会话重新读，30 秒重建项目心智模型。**市面上没有任何项目提供这个。**

### 2. 人类审 Agent 的及格线

所有 Agent 工具都在强化 Agent 的能力。AgentPrecept 花了同样精力在"用户不懂架构时怎么审 Agent"：

```
Agent 提交架构设计 → 对照 4 项:
  □ 模块划分表 > 3 模块
  □ 每个模块 1 行职责描述
  □ L4_O01 有技术选型依据
  □ project-graph 已更新
```

**14-production-readiness 的 8 阶段退出标准也是独一份。**

### 3. 教训驱动，不是原则驱动

大部分 AGENTS 指南是"你应该这样做"的道德说教。AgentPrecept 每条规则背后有实际踩过的坑。

---

## 适用 vs 不适用

| 你属于... | 结论 |
|------|------|
| 单人 + < 5 模块 + 不用 Agent | 太重——AGENTS.md 一段话够了 |
| 单人 + < 5 模块 + 用 Agent | project-graph 值得建，其他的按需 |
| 多人 + 多 Agent + 有人不太懂代码 | AgentPrecept 的核心价值在这里 |
| 开源项目接受外部贡献 | project-graph 让新贡献者的 Agent 30 秒入戏 |
| 你要的不是写文档的方法 | project-graph + L4_O01 + HANDOFF 就够了，跳过模板和方法论 |

---

## 致谢

AgentPrecept 的设计思想受以下项目启发：

- [ECC](https://github.com/affaan-m/ECC) — Claude Code 增强系统，启发了 Agent 命令映射、持久记忆和反模式
- [Andrej Karpathy's LLM Coding Style](https://github.com/multica-ai/andrej-karpathy-skills) — 启发了目标驱动执行和单文件设计哲学
- [CodeToFlow](https://moge.ai/zh/product/codetoflow) — 启发了 project-graph 可视化，我们实现了 graph-to-mermaid.py
