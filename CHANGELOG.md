# 变更日志

## [0.1.0] — 2026-06-06

### 核心机制

- **结构化项目图**（project-graph.yaml）：三层模型 + stability 字段（critical/stable/volatile）
- **设计依据**（L4_O01）：每决策一行表格，从 git log 反推
- **会话交接**（HANDOFF）：5 状态标记 + 上下文用量 + Agent 自我判断
- **AGENTS.md**：硬规则 8 条 + 软建议 + 自动动作 + 渐进加载

### 方法论（15 篇）

- 00 完整循环（8 阶段）
- 01-14 专题：文档/命名/设计依据/审计/交接/图/工作流/工程化/安全/性能/接入/人机协作/自我管理/生产就绪
- 14 维审计（8 维自动）框架（含狗粮/用户旅程/体验/定位/复用/社区）

### 模板（35 个，16/16 分类全齐）

- 31 编号模板 + 4 工具文件
- 🔥 核心 5 个：project-graph / L4_O01 / HANDOFF / 测试用例 / 架构设计
- 6 个模板深挖为 Agent 可执行指令

### 可执行物

- `scripts/`：init.sh / init.ps1 / basic-audit.py / sync-graph.py / graph-to-mermaid.py / check-naming.py
- `skills/`：5 个核心 skill（project-graph/design-rationale/session-handoff/test-cases/architecture-design）
- `templates/MEMORY.md`：跨会话持久记忆模板
- `Makefile`：make init / make audit / make todo-api-test
- `.github/workflows/`：audit.yml + test-examples.yml
- `examples/todo-api/`：可运行的 FastAPI demo（4 测试全绿）

### 参考与对比

- 审计收敛历程 + 多维图案例
- 横向对比（vs AGENTS.md / CLAUDE.md / Cursor Rules / CrewAI / CodeWhale Skill / ECC / Karpathy Skills）
- Agent 自身评估（deepseek-v4-pro 真实看法）
- 速查卡片（cheatsheet.md）

### 开源元文件

LICENSE (MIT) / CONTRIBUTING / CODE_OF_CONDUCT / README / SKILL / .gitignore
