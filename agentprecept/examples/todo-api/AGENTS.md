# AGENTS.md — Todo API 项目指令

## 项目文档结构

本项目采用 AgentPrecept 的四层文档分层。文档位于 `docs/` 目录。

| 层次 | 文件 | 内容 | 何时读 |
|---|---|---|---|
| L1 | `docs/L1_A01_quickstart.md` | 怎么跑起来 | 每次开始 |
| L1 | `docs/L1_A02_naming-convention.md` | 命名规则 | 每次开始 |
| L2 | `docs/L2_D01_architecture.md` | 架构设计 | 技术决策时 |
| L4 | `docs/L4_O01_design-rationale.md` | 为什么这样设计 | 修改核心逻辑前 |

## 文档命名格式

```
L{Level}_{Category}{NN}_{Slug}_{Title}.md
```

## Agent 操作规则

1. 每次会话开始时：读取 INDEX.md 和 L1_A02（命名规范）
2. 做技术决策前：查看 L4_O01（设计依据）
3. 会话结束时：重写 HANDOFF.md
4. 新增模块时：更新 `project-graph.yaml`
