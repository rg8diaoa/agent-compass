# 快速开始

> 分类: A | 层级: L1 | 编号: L1_A01
> 状态: 📝 撰写中 | 目标读者: 开发者

---

## 这是什么

agent-compass 是一套 Agent 开发方法论。本文档是 agent-compass 自身的快速开始——如何贡献、修改、扩展这套方法论。

## 项目结构

```
agent-compass/
├── AGENTS.md + SKILL.md   ← 规范层（Agent 行为规则引擎）
├── agent_compass/         ← CLI + MCP 层（init/sync/audit/doctor + MCP Server 5 tools）
├── scripts/               ← 脚本层（sync-graph 5维/basic-audit 8维/init/check-naming）
├── methodology/           ← 方法论层（16 篇：00-14 + 15-agent-ops）
├── templates/             ← 模板层（36 个，16/16 分类全齐，init 核心 8 个）
├── examples/              ← 示例层（Python/Node todo-api）
├── reference/             ← 参考层（案例/速查）
├── docs/                  ← 狗粮层（project-graph/HANDOFF/MEMORY/L4_O01/mcp-tools）
└── .github/               ← CI（audit + test-examples）
```

详见 `docs/L2_D01_architecture_架构设计.md`。

## 如何贡献

1. Fork → 修改 → PR
2. 新增方法论文档：遵循 `methodology/` 中的编号规则
3. 新增模板：遵循 `L{Level}_{CAT}{NN}_{Slug}_{Title}.md` 格式
4. 更新 `docs/INDEX.md` 和 `templates/INDEX.md` 同步

## 如何修改方法论

1. 如果修改已锁定文档（✅）→ 同步更新 `docs/L4_M01_changelog_变更日志.md`
2. 如果新增方法论 → `NN` 编号追加到现有末尾
3. 修改后跑 `methodology/04-audit-framework.md` 中的审计清单
