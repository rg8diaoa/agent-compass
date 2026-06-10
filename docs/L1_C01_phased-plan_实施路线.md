# 实施路线

> 分类: C | 层级: L1 | 编号: L1_C01
> 状态: 🔍 审查中 | 目标读者: 开发者
> 前置阅读: L2_D01_architecture_架构设计.md
> 最后更新: 2026-06-09

---

## §0 模式概览

AgentPrecept 提供四级治理深度，用户按需选择：

```text
lite           normal（默认）      pro                max
基础治理  ──→  深度约束    ──→   极致协议     ──→   运行时引擎
```

| 模式 | 定位 | 核心机制 | 适合场景 |
|------|------|----------|----------|
| **lite** | 基础治理 | 描述性规则 + 一次性 CLI + 6 MCP 只读 tool | 已有项目渐进接入、不想改变工作流 |
| **normal** | 深度约束 | 禁止性规则 + 自动检查点 + 代理弹药库 + Skill 系统 | 新项目从头搭建（默认安装） |
| **pro** | 极致协议 | 自检循环 + 跨会话债务追踪 + 宿主 hook 脚本生成 | 生产级团队、需要强制合规 |
| **max** | 运行时引擎 | 常驻 MCP Server + ap run 实际执行 + 代理调度 + 实时进度 | 全自动开发、无人值守 |

```text
normal = lite + 规则硬化 + 自动检查点 + 代理弹药库 + Skill 查询
pro    = normal + 自检循环 + 跨会话债务强制执行 + 宿主 hook 生成
max    = pro + 常驻服务 + ap run 执行引擎 + 工作流状态机 + 代理调度
```

安装时选择：
```bash
agentprecept init                 # 默认 normal
agentprecept init --mode lite
agentprecept init --mode pro
agentprecept init --mode max

agentprecept mode switch pro      # 已有项目升级
agentprecept mode show            # 查看当前模式
```

---

## §1 Phase 0：当前基准（v0.4.0+）— 对应 lite 模式

### 已交付

| 模块 | 能力 |
|------|------|
| CLI | `init`（6阶段）/ `sync`（6维扫描）/ `audit`（15维4-scope）/ `setup` / `hooks` / `gnhf` |
| MCP | 6 个 tool（query / audit / diff / decision / handoff / design_gate） |
| 脚本 | agentprecept/ 包内（sync_graph/basic_audit/design_gate/check_naming/ripple_check/graph_to_mermaid） |
| 规则 | AGENTS.md（284行，Auto-Pilot + 设计先行 + 讨论拦截 + 首次邂逅 + 新项目检测） |
| 文档 | 方法论 18 篇 / 模板 37 个 / 狗粮层 12 个文件 |
| 门禁 | 三层强制拦截（L1 MCP / L2 pre-commit hook / L3 CI gate） |

### 已知限制

- 规则为描述性措辞，Agent 可以"忘"
- 设计门禁靠 Agent 自愿调用 MCP——无强制触发
- skills/ 下 5 个文件无程序化加载路径
- 无代理调用指导
- 无错误模式库
- MEMORY.md 自动生长依赖 Agent 自觉

### lite 模式将长期保留

lite 是所有能力的子集。任何模式可降级到 lite（`ap mode switch lite`），降级后 AGENTS.md 恢复为描述性规则。已有项目初次接入时默认 lite 体验不变。

---

## §2 Phase 1：normal 模式基础设施（v0.5.0）

### 目标

交付 normal 模式核心基建：规则硬化 + 自动检查点 + 模式系统。

### 范围

| 模块 | 说明 | 验收 |
|------|------|:---:|
| AGENTS.md 分拆 | `core/` 目录：loop.md + design-gate.md + anti-lazy.md + normal.md | 编译为单文件 |
| 模式编译引擎 | `init` 时根据 mode 将 core/ 文件编译进 AGENTS.md | 单文件无占位符残留 |
| 禁止性规则 | normal 规则集："禁止未经 design_gate 的写入"等 | normal init 后规则生效 |
| 检查点协议 | sync 后自动 audit --scope code；commit 频率约束 | AGENTS.md 明确描述 |
| pre-push hook | `ap hooks install` 扩展 pre-push → audit --gate | push 被 audit 拦截 |
| HANDOFF 扩展 | 新增 `workflow_phase` / `debt_log` 字段 | `ap status` 可读 |
| `ap status` | 展示当前模式、阶段、债务 | CLI 结构化输出 |
| `ap mode` | show / switch 子命令 | 模式切换后 AGENTS.md 重新编译 |
| 模板更新 | 新增 L1_C01 到 templates/ + init 脚本更新 | 新项目包含路线图 |

### 门禁

```text
Phase 1 通过标准:
  □ ap init（默认 normal）在新项目跑通
  □ ap status 展示 mode=normal + phase
  □ ap mode switch lite/normal 来回切换 AGENTS.md 正确编译
  □ pre-push hook 在 audit fail 时阻断 push
  □ normal 模式 AGENTS.md 含"禁止"措辞的规则 ≥ 5 条
  □ audit --gate FAIL 0
```

### 不做

- 代理弹药库（v0.6.0）
- Skill 系统 CLI/MCP（v0.6.0）
- 自检循环协议（v0.8.0 pro）
- 运行时服务（v0.9.0 max）

---

## §3 Phase 2：代理弹药库 + Skill 系统（v0.6.0）

### 目标

交付代理提示词模板和 Skill 查询系统。normal 及以上可用。

### 范围

| 模块 | 说明 | 验收 |
|------|------|:---:|
| agents/ 目录 | 9 个代理提示词模板（planner / architect / coder / security_reviewer / performance_analyst / style_guardian / e2e_tester / refactor_cleaner / debugger） | 每个文件 ≥ 50 行，可独立复制到 sub-agent |
| AGENTS.md 代理调用规则 | normal+ 规则集：何时调哪个代理 | "修改 auth 模块→先调 security_reviewer" |
| `ap review` 命令 | L1 跑 audit + L2 输出代理审查提示词 | 输出可直接粘贴到 sub-agent prompt |
| MCP `review_run` tool | ap review 的 MCP 版本 | 结构化 JSON 输出 |
| skills/ 重构 | 按 domain / workflow / governance 分类，统一 YAML frontmatter | 所有 Skill 可通过 CLI 查询 |
| `ap skill list/show/search` | CLI 查询命令 | `ap skill search "新增模块"` 返回匹配 |
| MCP `skill_search` / `skill_list` | MCP 查询 tool | Agent 按任务关键词搜索 |
| 当前 5 个 Skill 迁移 | governance/ 下分类存放 | 旧路径保留兼容 |

### 门禁

```text
Phase 2 通过标准:
  □ ap review --type security 输出 ≥ 3 条审查点
  □ ap skill search "python" 返回 python-patterns
  □ agents/ 下 9 个模板文件全部存在
  □ normal 模式 AGENTS.md 含代理调用规则章节
```

---

## §4 Phase 3：沉淀与免疫（v0.7.0）

### 目标

交付 compound 沉淀命令和错误免疫基础。normal 及以上可用。

### 范围

| 模块 | 说明 | 验收 |
|------|------|:---:|
| `ap compound` | 分析 git diff → 识别新增模块/API/配置 → 建议 MEMORY.md 条目 | 输出 3-5 条 pattern/lesson 建议 |
| MEMORY.md 格式升级 | 支持 `## Pattern:` / `## Lesson:` 区块 | compound 输出可直接追加 |
| `ap diagnose` | 读取 .errors/ → 匹配已知反模式 → 输出修复建议 | 已知错误类型自动识别 |
| `ap check --patterns` | 扫描代码中的已知反模式（SQL 注入、循环内 DB 调用等） | 扫描 agentprecept 自身 ≥ 5 条命中 |
| `.errors/` 格式定义 | `latest.json` schema + 捕获规则（AGENTS.md normal+） | Agent 遭遇错误时写入 |
| 反模式库 v1 | 10-15 条初始反模式（来自 agentprecept 自身 MEMORY.md 教训） | ap check 可检测 |

### 门禁

```text
Phase 3 通过标准:
  □ ap compound 在示例项目上输出 ≥ 3 条建议
  □ ap diagnose 在已知错误上输出正确匹配
  □ ap check --patterns 扫描 agentprecept 自身命中 ≥ 5 条
  □ .errors/latest.json schema 被 AGENTS.md 规则引用
```

---

## §5 Phase 4：pro 模式 — 自检循环 + 宿主 hook（v0.8.0）

### 目标

交付 pro 模式专属能力：自检循环协议 + 跨会话债务强制执行 + 宿主 hook 脚本生成。

### 范围

| 模块 | 说明 | 验收 |
|------|------|:---:|
| core/pro.md | pro 自检循环规则：每轮结束自问 4 题 | 编译进 AGENTS.md |
| 自检循环协议 | ①本轮是否违反约束？②有无该写未写 MEMORY？③有无新增 .errors/？④checklist 与 commit 频率是否健康？ | pro init 后 AGENTS.md 含完整协议 |
| `ap generate-hook` | 为目标宿主生成 hook 脚本：claude-code / codewhale | 产出可执行 hook 文件 |
| Claude Code hook 模板 | PreToolUse 检查脚本（调用 agentprecept design-gate） | 复制后 claude 自动执行 |
| CodeWhale plugin 模板 | plugin 骨架 + activation notes | 复制后可加载 |
| 跨会话债务强制执行 | HANDOFF debt_log → 会话启动时 AGENTS.md pro 规则：先清债务 | 遗留债务场景拦截验证 |
| `ap resume` | 读取 HANDOFF → 恢复中断位置 | 中断后 resume 输出"下一步" |

### 自检循环协议（pro 核心）

```markdown
## 思维循环协议（pro 模式）

每轮对话结束前，Agent 必须自问并回答：

1. **约束检查**：本轮是否执行了 write_file / edit_file / apply_patch？
   → 若是：是否已通过 design_gate 检查？未通过 → 下一轮必须先输出设计文档草稿

2. **记忆检查**：本轮是否发现了新的模式/教训/偏好？
   → 若是：是否已追加到 MEMORY.md？未追加 → 下一轮第一件事：grep + 追加

3. **错误检查**：本轮是否遭遇了工具/命令失败？
   → 若是：是否已写入 .errors/latest.json？未写入 → 下一轮第一件事：写入

4. **进度检查**：当前 checklist 是否有 item 超过 3 个 commit 未完成？
   → 若是：是否需要拆分为更小 item？是否需要 HANDOFF 加 [BLOCKED]？
```

### 门禁

```text
Phase 4 通过标准:
  □ ap generate-hook --target claude-code 产出可执行 hook 文件
  □ pro 模式 init 后 AGENTS.md 含自检循环协议
  □ 遗留债务场景：新会话被 HANDOFF debt_log 拦截
  □ ap resume 在中断后正确恢复状态
  □ audit --gate FAIL 0
```

---

## §6 Phase 5：max 模式 — 运行时引擎（v0.9.0）

### 目标

交付 max 模式专属能力：常驻 MCP Server + ap run 执行引擎 + 代理调度。

> **这是 AgentPrecept 首次引入运行时组件。** max 模式下的 `agentprecept serve` 启动一个增强型 MCP Server 后台进程，维护工作流状态机，通过 MCP 协议与 Agent 交互——驱动完整的工作流闭环。

### 范围

| 模块 | 说明 | 验收 |
|------|------|:---:|
| `agentprecept serve` | 启动增强型 MCP Server（后台常驻） | 进程启动，MCP 握手成功 |
| 工作流状态机 | 内存中维护 WorkflowState（IDEA→PLAN→WORK→REVIEW→COMPOUND），持久化到 HANDOFF.md | 状态转移正确，持久化一致 |
| `ap run "需求"` | 通过 MCP 协议串联完整工作流：plan→work→review→compound | 一条命令走完闭环 |
| MCP `workflow_next` tool | 返回当前阶段 + 下一步指令（Agent 调用的核心 tool） | Agent 每轮调用，获得行为指引 |
| MCP `workflow_transition` tool | 推进工作流阶段 + 触发门禁检查 | 阶段转移前自动跑 design_gate |
| MCP `agent_dispatch` tool | 返回当前任务应调用的代理提示词 | 输出可直接粘贴到 sub-agent |
| `ap status --live` | 查询运行中的工作流实时进度 | 展示当前阶段、任务进度、耗时 |
| `ap resume`（增强） | 恢复中断的 ap run，从 HANDOFF 读取状态 | 断点续传 |
| 代理调度（顺序） | ap run 内按 plan→code→review 顺序分发代理提示词 | 每个阶段输出对应代理 prompt |
| 代理调度（并行） | review 阶段并行输出 security + performance 审查提示词 | 一次输出多份 |

### max 模式运行时架构

```text
┌─────────────────────────────────────────────┐
│                agentprecept serve             │
│  ┌───────────┐  ┌───────────┐  ┌─────────┐  │
│  │ 工作流     │  │ 门禁引擎   │  │ 代理    │  │
│  │ 状态机     │  │ (audit)   │  │ 调度器   │  │
│  └─────┬─────┘  └─────┬─────┘  └────┬────┘  │
│        │              │             │        │
│  ┌─────┴──────────────┴─────────────┴────┐   │
│  │          增强 MCP Server               │   │
│  │  workflow_next / workflow_transition  │   │
│  │  agent_dispatch / review_run          │   │
│  │  + 全部 lite 6 tool                   │   │
│  └────────────────┬──────────────────────┘   │
└───────────────────┼──────────────────────────┘
                    │ MCP 协议
                    ▼
              ┌──────────┐
              │  Agent   │ ← 每轮调用 workflow_next，获得下一步指令
              └──────────┘
```

### ap run 执行流程（max 模式）

```bash
$ ap run "实现用户登录功能，支持 JWT"

# serve 进程内部：
# ┌──────────────────────────────────────────────────────┐
# │ [状态机] IDEA → PLAN                                  │
# │ [门禁] design_gate 检查 → CLEAR                       │
# │ [Agent 调用 workflow_next]                            │
# │   → 返回："当前阶段 PLAN。请读取 project-graph.yaml   │
# │            确定影响范围，生成 tasks/plan.md。"         │
# │                                                      │
# │ [Agent 执行规划，写入 tasks/plan.md]                   │
# │ [Agent 调用 workflow_transition --to WORK]            │
# │ [状态机] PLAN → WORK                                  │
# │                                                      │
# │ [Agent 调用 workflow_next]                            │
# │   → 返回："当前阶段 WORK。任务 1/6: 创建 JWT 工具类。  │
# │            请调用 agent_dispatch 获取 coder prompt。"  │
# │                                                      │
# │ ... (Agent 逐任务执行，每完成一个调用 workflow_next)   │
# │                                                      │
# │ [状态机] WORK → REVIEW                                │
# │ [Agent 调用 workflow_next]                            │
# │   → 返回："当前阶段 REVIEW。                            │
# │            请并行调用 review_run (security+perf)。"    │
# │                                                      │
# │ [Agent 执行审查，输出修复建议]                         │
# │                                                      │
# │ [状态机] REVIEW → COMPOUND                            │
# │ [Agent 调用 workflow_next]                            │
# │   → 返回："当前阶段 COMPOUND。请运行 ap compound。"    │
# └──────────────────────────────────────────────────────┘
```

### 门禁

```text
Phase 5 通过标准:
  □ agentprecept serve 启动后 MCP 握手成功
  □ ap run "实现 echo 端点" 走完 IDEA→PLAN→WORK→REVIEW→COMPOUND
  □ ap status --live 实时展示进度
  □ 中断 serve 进程后 ap resume 恢复
  □ review 阶段并行输出 security + performance 两份审查提示词
  □ ap run 的 PLAN→WORK 转移触发 design_gate（设计文档缺失时阻止转移）
```

---

## §7 Phase 6：生产化（v1.0.0）

### 目标

测试覆盖、文档补全、打包发布。

| 模块 | 说明 |
|------|------|
| 测试 | CLI 命令集成测试 + core/ 编译测试 + MCP tool 单元测试 + serve 进程测试 |
| 文档 | 用户手册（L3_L01）+ 迁移指南（v0.4→v1.0）+ API 参考 + mcp-tools.md 更新 |
| 性能 | MCP tool 响应时间 < 1s（audit_run 除外）；serve 内存占用 < 100MB |
| 示例项目 | todo-api 的 lite / normal / pro / max 四模式版本 |
| 发布 | PyPI v1.0.0 |

---

## §8 版本映射

| 版本 | 类型 | 对应阶段 | 核心交付 | 可用模式 |
|------|------|----------|----------|----------|
| v0.5.0 | MINOR | Phase 1 | 模式系统 + 规则硬化 + pre-push hook | lite / normal（新增） |
| v0.6.0 | MINOR | Phase 2 | 代理弹药库 + Skill 系统 | lite / normal |
| v0.7.0 | MINOR | Phase 3 | compound + diagnose + 反模式库 | lite / normal |
| v0.8.0 | MINOR | Phase 4 | pro 模式 + 自检循环 + 宿主 hook | lite / normal / pro（新增） |
| v0.9.0 | MINOR | Phase 5 | max 模式 + serve + ap run | lite / normal / pro / max（新增） |
| v1.0.0 | MAJOR | Phase 6 | 测试 + 文档 + PyPI 发布 | 全模式 |

---

## §9 模式能力矩阵

| 能力 | lite | normal | pro | max |
|------|:---:|:---:|:---:|:---:|
| 文档骨架（init） | ✅ | ✅ | ✅ | ✅ |
| 项目图（sync） | ✅ | ✅ | ✅ | ✅ |
| 审计（audit --gate） | ✅ | ✅ | ✅ | ✅ |
| MCP 6 tool | ✅ | ✅ | ✅ | ✅ |
| 三层门禁 | ✅ | ✅ | ✅ | ✅ |
| 禁止性规则 | — | ✅ | ✅ | ✅ |
| 自动检查点 | — | ✅ | ✅ | ✅ |
| pre-push hook | — | ✅ | ✅ | ✅ |
| ap status | — | ✅ | ✅ | ✅ |
| 代理弹药库 | — | ✅ | ✅ | ✅ |
| Skill 查询 | — | ✅ | ✅ | ✅ |
| ap review | — | ✅ | ✅ | ✅ |
| ap compound | — | ✅ | ✅ | ✅ |
| ap diagnose | — | ✅ | ✅ | ✅ |
| ap check | — | ✅ | ✅ | ✅ |
| 自检循环协议 | — | — | ✅ | ✅ |
| 跨会话债务强制执行 | — | — | ✅ | ✅ |
| 宿主 hook 生成 | — | — | ✅ | ✅ |
| ap resume | — | — | ✅ | ✅ |
| agentprecept serve | — | — | — | ✅ |
| ap run | — | — | — | ✅ |
| 工作流状态机 | — | — | — | ✅ |
| 代理调度 | — | — | — | ✅ |
| ap status --live | — | — | — | ✅ |

---

## §10 不纳入（明确不做）

| 项 | 原因 |
|----|------|
| 直接拦截 Agent 工具调用（write_file 等） | AgentPrecept 不在工具调用链上——这是宿主工具的领地。max 模式通过 MCP 引导 Agent 行为，但不能物理拦截 |
| 跨平台桌面通知 | 依赖过多，各宿主工具已有通知机制 |
| PreCompact 上下文注入 | AgentPrecept 感知不到宿主工具的压缩事件 |
| 内置 LLM 调用 | 不绑模型——AgentPrecept 是治理层，不是执行层 |
| gnhf 内置 | 保持可选阶段——gnhf 是独立工具，不 vendoring |

---

## §11 配套变更清单（全阶段汇总）

| 阶段 | 新建文件 | 修改文件 |
|------|----------|----------|
| Phase 1 | `core/loop.md` / `core/design-gate.md` / `core/anti-lazy.md` / `core/normal.md` / `docs/L1_C01_phased-plan_实施路线.md` | `AGENTS.md` / `SKILL.md` / `cli.py`（mode + status） / `init.ps1` / `init.sh` / `docs/INDEX.md` / `docs/L2_D01` / `docs/project-graph.yaml` / `templates/L1_C01` |
| Phase 2 | `agents/` 目录（9 文件）/ `skills/domain/` / `skills/workflow/` / `skills/governance/` / `skills/index.md` / `core/normal.md`（更新） | `cli.py`（review + skill） / `mcp_server.py`（review_run + skill_search） |
| Phase 3 | `core/normal.md`（更新）| `cli.py`（compound + diagnose + check） / `mcp_server.py`（compound tool） |
| Phase 4 | `core/pro.md` | `cli.py`（generate-hook + resume） / `AGENTS.md`（编译引擎支持 pro）|
| Phase 5 | `agentprecept/serve.py` / `agentprecept/workflow.py` / `core/max.md` | `cli.py`（serve + run） / `mcp_server.py`（workflow_next + workflow_transition + agent_dispatch）|
| Phase 6 | `tests/` | `CHANGELOG.md` / `README.md` / `pyproject.toml` |