# AgentPrecept ![version](https://img.shields.io/badge/version-v0.4.7-blue)

> **AgentPrecept（原 agent-compass）与 Future AGI 的 "Agent Compass" 商业产品无关。**
> 本项目的定位是 AI 编码 Agent 的方法论治理工具集——不是 LLM 可观测性平台。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

> **Agent 不会失忆的施工图。** 结构化数据文件 + MCP 原生集成——格式固定、可审计、跨会话不漂移。

---

## 为什么不是散文指令，也不是自动记忆

| 方式 | 问题 |
|------|------|
| 散文指令（"本项目用 FastAPI"） | Agent 读完就忘，下一轮重新遍历源码 |
| 自动记忆（Agent 自己记） | 自动但不可控，久了容易记不准 |

agentprecept 走第三条路：project-graph（30秒懂依赖关系）、设计依据（一行表记住为什么这样选）、会话交接（换班不丢进度）。文件是活的，项目长它也长。

### 不侵入代码——全部新增在外挂层

agentprecept 的集成方式是"外挂层"——不修改任何现有源码文件，全部产出在 AGENTS.md + docs/ + .git/hooks/ + .github/workflows/ 下。适合已有项目的渐进式引入，也适合新项目的零风险冷启动。

---

## 解决什么问题

你用 code agent（下面统称 Agent）写代码，但每次新对话 Agent 都会：

- **失忆**："上一个 Agent 做到哪了？"
- **迷路**：不知道哪个模块改会影响到谁
- **推翻**：把团队试过但放弃的方案又提议一次
- **不一致**：今天叫 `priority_level`，明天叫 `importance`
- **裸写**：拿到需求跳过设计直接写代码，架构全在脑子里没落文档

agentprecept 不是让 Agent 更强——**是给 Agent 一份施工图，给用户一份验收单**。你在家装时不懂水电，也能对照 checklist 说"这里不对"。技术上同时给工程师完整的 15 维审计框架和 8 阶段生产就绪退出标准。

---

## 这个项目做了什么

| 比喻（小白友好） | 技术术语（工程师） |
|------|------|
| 施工图——哪面墙是承重不能拆 | **project-graph.yaml** — YAML 结构化数据，三层模型（结构/关系/演变）+ stability 字段（critical/stable/volatile） |
| 物业装修记录——上次改水电是哪年 | **L4_O01 设计依据** — 每决策一行表格（决策/来源/证据），从 git log 反推 |
| 工人交接班日志——白班干了什么 | **HANDOFF.md** — 5 状态标记（IN_PROGRESS/BLOCKED/NEEDS_HUMAN_REVIEW）+ 上下文用量评估 |
| 业主验收 checklist——水电通了？墙平了？ | **14-production-readiness** — 8 阶段退出标准 × 可自动化验证项（✅脚本/⚠️Agent自检/❌人类） |
| 装修特殊要求——不能用某种材料 | **MEMORY.md** — 跨版本持久偏好/项目约束/历史教训 |
| 设计图纸——承重墙在哪、管线怎么走 | **L2_D01 架构设计** — 模块划分 + 职责描述 + 数据流 + 接口约定（设计先行原则强制前置） |
| 改一面墙——旁边哪些会被牵连 | **ripple_check.py** — 涟漪分析（DIRECT/INDIRECT/SAME_PKG），基于 project-graph 显式依赖计算影响半径 |
| 三道安检——进场前、施工中、验收时 | **三层门禁体系** — ① MCP design_gate（Agent 自助）→ ② pre-commit hook（--no-verify 可跳过）→ ③ CI gate 15 维审计（不可跳过） |
| 监理检查工具——15 维自动化巡检 | **basic-audit.py** — 命名/引用/编号/残留/图格式/追溯/覆盖率/狗粮/声明校验/设计覆盖/分支策略/commit粒度/术语一致/内容一致/体验审计，一行命令全跑（--gate 模式） |

---

## 五样拿手活

### 1. 结构化数据，不是散文指令

给 Agent 写一段话："本项目使用 FastAPI，数据库 PostgreSQL"。Agent 读一遍就忘了，下一轮重新遍历源码。

agentprecept 把项目结构写成**机器可消费的 YAML 图**（structure / relations / evolution）。Agent 每次新会话读取后快速定位模块关系，大幅减少遍历源码的需求。`stability` 字段区分改模块的风险等级。

### 2. 不懂代码的人也能审 Agent 产出 + 自动化审计

Agent 提交了架构设计——你对照 4 项：
- □ 模块 > 3（`project-graph.yaml` structure 键数 ≥ 4）
- □ 有职责描述（每个模块 `description` 非空）
- □ L4_O01 有依据（行数 ≥ 5 + 最近一条 7 天内）
- □ 图已更新（`evolution` 最新条目与最后一次变更同会话）

4 项全 □ → 及格。少 1 项 → 告诉 Agent "补一下这里"。

**15 维审计**：`agentprecept audit --gate` 一行命令跑完 15 维 4-scope（docs/code/git/config）。+ 4 维自选清单在报告末尾提示。

**三层门禁体系**：理想路径过三道检查——① MCP `design_gate` Agent 自助检查设计文档就位 ② pre-commit hook 四道检查（分支/粒度/设计/确认）③ CI gate 15 维审计兜底。实际生效取决于配置了哪几层。

### 3. 教训驱动——每条规则踩过坑

三轮审计从 12 个问题收敛到 0 阻塞项。不是"你应该这样做"的道德说教，是"上次它炸了所以这次必须这样做"。`stability: critical` 规则来自真实线上事故：改 auth 模块不知道 admin 也依赖它。

### 4. 设计先行 + 讨论拦截——方案没对齐不动手

Agent 拿到需求容易跳过设计直接写代码——或者在讨论中就顺手改了。agentprecept 定义了设计流程三道检查：

```
讨论新功能 → 整理方案要点 → [NEEDS_HUMAN_REVIEW] → 确认
         → 设计文档草稿 → 确认("go/OK/开始") → 写代码
```

新项目必须出架构设计（L2_D01），新模块必须有模块设计（L2_F07），API 变更必须先写契约（L2_G03）。确认信号明确了——"确认/可以/go/OK/开始/执行"或"不用审/直接做"。EXPLORE 下内容可简化但确认步骤不可跳过。

### 5. 新项目自举——说"建一个XX"就自动初始化

用户说"帮我写一个日记应用"、"搭一个 API 服务"——Agent 识别为新项目创建意图，自动：运行 `init.ps1`（AGENTS.md + templates/ 下全部文档，含 MEMORY 自动生长）→ 提示 git init → 出架构设计草稿 → 等确认 → 才能写代码。骨架不可跳过，即使用户说"直接做"。

---

## 核心文件

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | Agent 行为规则引擎 |
| `docs/project-graph.yaml` | 项目结构图，Agent 30 秒读取 |
| `docs/L2_D01` | 架构设计（模块划分 + 职责 + 数据流） |
| `docs/L4_O01` | 设计决策追溯（决策/来源/证据） |
| `docs/HANDOFF.md` | 跨会话交接 + 状态标记 |
| `docs/MEMORY.md` | 持久偏好与历史教训（Agent 自动生长） |
| `docs/mcp-tools.md` | MCP Server 6 个 tool 参考 |

## 完整流程

```
研究 → 想法 → 设计 ────→ 人类确认 ────→ 开发 → 测试 → 审计 → 修复 → 维护 → (循环)
               ↑                      ↑
          设计先行原则              设计没确认不许动工
         (L2_D01/F07/G01/G03)      [NEEDS_HUMAN_REVIEW]
```

每阶段有退出标准（14-production-readiness），Agent 自检后才提交。

## 一行命令

```bash
pip install agentprecept
agentprecept init /your/project     # 6 阶段骨架一键生成
agentprecept sync                   # 6 维代码扫描，自动同步 project-graph
agentprecept audit --gate           # 15 维 4-scope 自动化审计
agentprecept setup                  # 诊断 + MCP 配置指南
python -m agentprecept.mcp_server   # 启动 MCP Server（6 tools）
```

## 数字

- 18 篇方法论 + 37 个模板（16/16 分类全齐）+ 5 个 Skill
- Python 和 Node.js 双语言可运行示例
- 15 维审计框架 + 8 阶段生产就绪标准

---

## 安装

两条路，选一条：

| 方式 | 适合 | 怎么做 |
|------|------|--------|
| 🤖 **Agent 自动装**（推荐） | 零配置，Agent 搞定一切 | 把本仓库 GitHub 链接发给 Agent，说"帮我装" |
| 🛠️ **手动装** | 自己控制每一步 | `pip install agentprecept` → `agentprecept setup` |

### 🤖 Agent 自动装（30 秒）

把链接发给 Claude Code / CodeWhale / Cursor / OpenCode / Copilot / Windsurf，说"帮我装 agentprecept"。Agent 自动完成：

1. 运行 init → AGENTS.md + templates/ 下全部文档就位（含 MEMORY 自动生长）
2. `pip install fastmcp` → MCP 依赖就绪
3. 检测你的工具 → 自动配置 MCP（含 Windows 编码兼容）
4. 提示 git init

### 🛠️ 手动装

```bash
pip install agentprecept
cd your-project && agentprecept setup   # 一键初始化 + MCP 配置指南 + 诊断
```

> **升级**：先卸载再安装，不要用 `--force-reinstall`（避免残留旧脚本导致 `ModuleNotFoundError`）：
> ```bash
> pip uninstall agentprecept -y && pip install -U agentprecept
> ```

将 `setup` 输出的 JSON 复制到 Agent 工具配置文件（Claude Code → `.mcp.json` / CodeWhale → `~/.deepseek/mcp.json` / Cursor → `.cursor/mcp.json`），重启即用。

### 开写

Agent 自动读取 AGENTS.md，按 Auto-Pilot 规则运行。MCP tools 在 Agent 会话中可被直接调用。

已有项目接入 → `methodology/M3_C08_existing-project_已有项目接入.md`

---

## 效果

| 场景 | 没有 | 有 |
|------|------|------|
| 第一行代码 | Agent 不知道从哪开始 | 读 project-graph，30 秒 |
| 修了一个 bug | 可能引入新 bug | 读依赖图，追踪显式依赖的关联文件 |
| Agent 提方案 | "用 Session 吧" | 读 L4_O01——"去年已证明不行" |
| 换了 Agent | "做到哪了？" | 读 HANDOFF——从下一步继续 |
| 审 Agent 产出 | "看起来差不多" | 对照 4 项——"补一下这里" |
| Agent 想写新模块 | 直接开始写 | 先出模块设计草稿，确认后再动工 |
| 讨论新功能 | "好的，加一下"直接改 | 先整理方案要点，确认后再进设计 |
| 建一个新项目 | 直接开始写代码 | init 骨架 + 架构草稿 → 确认 → 动工 |

---

## 实战效果

agentprecept 自身使用 agentprecept 管理——本文档体系即 `agentprecept init` + `agentprecept audit --gate` 的产出。15 维自动化审计 FAIL 0，pre-commit 4 gates 全部在线。

---

## 已知限制

- **涟漪分析**：基于 project-graph 显式依赖，覆盖不了动态反射（`getattr`）、
  猴子补丁和微服务间 HTTP/gRPC 调用。分布式项目建议配合 OpenTelemetry。
- **设计门禁**：检查设计文档是否存在，不校验内容质量。质量把控依赖
  [NEEDS_HUMAN_REVIEW] 人工确认步骤。
- **安全审计**：15 维不含 SAST、secret scanning 和 Prompt 注入检测。
  AgentPrecept 是方法论文档治理工具，不是安全扫描器。
- **多语言支持**：sync-graph 自动扫描 Python/JS/TS，其他语言需手动维护 project-graph。

## 和类似工具的区别

| | AgentPrecept | Cursor Rules | ROADMAP.md | CrewAI |
|--|-------------|-------------|------------|--------|
| 性质 | 方法论+工具集 | IDE 规则片段 | 单文件规划 | Agent 编排框架 |
| 设计规范 | ✅ 定义三步流程 | ❌ | ❌ | ❌ |
| 项目结构图 | ✅ YAML 3层+自动扫描 | ❌ | ❌ | ❌ |
| 脚本化审计 | ✅ 15 维 | ❌ | ❌ | ❌ |
| 会话交接 | ✅ HANDOFF | ❌ | ❌ | ❌ |
| 一键接入 | ✅ `agentprecept init` | ❌ | ❌ | ❌ |
| 侵入代码 | 零（外挂层） | 零 | 零 | 有 |

---

## 目录

```
agentprecept/
├── AGENTS.md          ← Agent 一看就用
├── SKILL.md           ← 一键加载 Skill
├── pyproject.toml     ← pip install agentprecept
├── build-data.ps1      ← 构建辅助（wheel 打包前复制数据文件）
├── docs/
│ ├── project-graph.yaml  ← 项目结构图
│ ├── HANDOFF.md          ← 会话交接
│ ├── MEMORY.md           ← 持久记忆（自动生长）
│ ├── L4_O01              ← 设计依据（44+ ADR）
│ └── mcp-tools.md        ← MCP 6 tool API
├── skills/            ← 5 个核心 Skill
├── methodology/       ← 18 篇方法论（M{1-4}_{A-D}{NN} 四板块体系）
├── templates/         ← 37 个模板（16分类全齐，init 核心 8 个）
├── examples/          ← Python/Node 示例 + prompt 模板 + first-run
├── reference/         ← 审计案例/多维图/横向对比/速查卡片
└── .github/           ← CI（audit.yml + test-examples.yml）
```

## 灵感来源

- **ECC** — Agent 命令映射与持久记忆模式
- **Andrej Karpathy's LLM Coding Style** — 目标驱动执行、"一个文件改善 Agent 行为"
- **CodeToFlow** — 代码结构可视化理念
- **gnhf** — git worktree 安全沙盒 + 原子提交模式，启发了 agentprecept 的安全设计

核心方法论源自本人的“世界模拟器”多 Agent 协作实战项目。

## 许可证

MIT