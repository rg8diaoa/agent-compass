# agent-compass 🧭

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

> **Agent 不会失忆的施工图。** 把项目关键信息写成你与 Agent 共同维护的数据文件——格式固定、可审计、跨会话不漂移。

---

## 为什么不是散文指令，也不是自动记忆

| 方式 | 问题 |
|------|------|
| 散文指令（"本项目用 FastAPI"） | Agent 读完就忘，下一轮重新遍历源码 |
| 自动记忆（Agent 自己记） | 自动但不可控，久了容易记不准 |

agent-compass 走第三条路：project-graph（30秒懂依赖关系）、设计依据（一行表记住为什么这样选）、会话交接（换班不丢进度）。文件是活的，项目长它也长。

---

## 解决什么问题

你用 ChatGPT/Claude/CodeWhale（下面统称 Agent）写代码，但每次新对话 Agent 都会：

- **失忆**："上一个 Agent 做到哪了？"
- **迷路**：不知道哪个模块改会影响到谁
- **推翻**：把团队试过但放弃的方案又提议一次
- **不一致**：今天叫 `priority_level`，明天叫 `importance`

agent-compass 不是让 Agent 更强——**是给 Agent 一份施工图，给用户一份验收单**。你在家装时不懂水电，也能对照 checklist 说"这里不对"。技术上同时给工程师完整的 14 维审计框架和 8 阶段生产就绪退出标准。

---

## 这个项目做了什么

| 比喻（小白友好） | 技术术语（工程师） |
|------|------|
| 施工图——哪面墙是承重不能拆 | **project-graph.yaml** — YAML 结构化数据，三层模型（结构/关系/演变）+ stability 字段（critical/stable/volatile） |
| 物业装修记录——上次改水电是哪年 | **L4_O01 设计依据** — 每决策一行表格（决策/来源/证据），从 git log 反推 |
| 工人交接班日志——白班干了什么 | **HANDOFF.md** — 5 状态标记（IN_PROGRESS/BLOCKED/NEEDS_HUMAN_REVIEW）+ 上下文用量评估 |
| 业主验收 checklist——水电通了？墙平了？ | **14-production-readiness** — 8 阶段退出标准 × 可自动化验证项（✅脚本/⚠️Agent自检/❌人类） |
| 装修特殊要求——不能用某种材料 | **MEMORY.md** — 跨版本持久偏好/项目约束/历史教训 |

---

## 三样拿手活

### 1. 结构化数据，不是散文指令

给 Agent 写一段话："本项目使用 FastAPI，数据库 PostgreSQL"。Agent 读一遍就忘了，下一轮重新遍历源码。

agent-compass 把项目结构写成**机器可消费的 YAML 图**（structure / relations / evolution）。Agent 每次新会话读 30 秒，不需遍历源码即可重建心智模型。`stability` 字段区分改模块的风险等级。

### 2. 不懂代码的人也能审 Agent 产出

Agent 提交了架构设计——你对照 4 项：
- □ 模块划分表有 > 3 个模块
- □ 每个模块有 1 行职责描述
- □ L4_O01 中有对应的技术选型依据
- □ project-graph 已经更新

4 项全 □ → 及格。少 1 项 → 告诉 Agent "补一下这里"。工程师可扩展到完整 14 维审计。

### 3. 教训驱动——每条规则踩过坑

三轮审计从 12 个问题收敛到 0 阻塞项。不是"你应该这样做"的道德说教，是"上次它炸了所以这次必须这样做"。`stability: critical` 规则来自真实线上事故：改 auth 模块不知道 admin 也依赖它。

---

## 核心文件

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | Agent 行为规则（硬规则 8 + 软建议 + 自动动作 + 探索/精确双模式） |
| `docs/project-graph.yaml` | 项目结构图——YAML 数据，Agent 30 秒读取 |
| `docs/L4_O01` | 设计决策追溯——决策/来源/证据 |
| `docs/HANDOFF.md` | 跨会话交接 + 5 状态标记 + 上下文用量 |
| `docs/MEMORY.md` | 持久偏好和项目约束 |

## 完整流程

```
研究 → 想法 → 设计 → 文档 → 开发 → 测试 → 审计 → 修复 → 维护 → (循环)
```

每阶段有退出标准（14-production-readiness），Agent 自检后才提交。

## 一行命令

```bash
pip install agent-compass
agent-compass init /your/project    # 一键生成核心文件
agent-compass sync                  # 从代码自动同步 project-graph
agent-compass audit                 # 快速审计（命名/断链/骨架）
agent-compass doctor                # 诊断缺什么
```

## 数字

- 15 篇方法论 + 35 个模板（16/16 分类全齐）+ 5 个 Skill
- Python 和 Node.js 双语言可运行示例
- 14 维审计框架 + 8 阶段生产就绪标准

---

## 三步开始

### 步骤一：安装（30 秒）

```bash
pip install agent-compass
agent-compass init /your/project
```

### 步骤二：发给 Agent

```
我正在用 agent-compass 方法初始化项目。
请读取 docs/project-graph.yaml — 告诉我当前项目结构。
如果 project-graph 是空的，用 tree 和 grep 自动生成。
```

### 步骤三：看 demo

```bash
make todo-api-test   # 4/4 测试全绿
```

已有项目接入 → `methodology/11-existing-project.md`（先搬 3 个文件，按需扩展）

---

## 效果

| 场景 | 没有 | 有 |
|------|------|------|
| 第一行代码 | Agent 不知道从哪开始 | 读 project-graph，30 秒 |
| 修了一个 bug | 可能引入新 bug | 读依赖图，知道影响的 2 个文件 |
| Agent 提方案 | "用 Session 吧" | 读 L4_O01——"去年已证明不行" |
| 换了 Agent | "做到哪了？" | 读 HANDOFF——从下一步继续 |
| 审 Agent 产出 | "看起来差不多" | 对照 4 项——"补一下这里" |

---

## 实战效果

在一个 41 份文档/46 个配置维度的大型多 Agent 协作项目中验证。三轮审计从 12 个问题收敛到 0 阻塞项。外部评审 9.0/10。

---

## 目录

```
agent-compass/
├── AGENTS.md          ← Agent 一看就用
├── SKILL.md           ← 一键加载 Skill
├── pyproject.toml     ← pip install agent-compass
│
├── agent_compass/     ← CLI（init/sync/audit/doctor）
├── scripts/           ← sync-graph/graph-to-mermaid/basic-audit/check-naming
├── skills/            ← 5 个核心 Skill（可加载能力包）
│
├── methodology/       ← 15 篇方法论（00循环 + 01-14专题）
├── templates/         ← 35 个模板（16分类全齐，🔥核心5个）
├── examples/          ← Python/Node 示例 + prompt 模板 + first-run
├── reference/         ← 审计案例/多维图/横向对比/速查卡片
├── docs/              ← 自身完整文档体系（吃自己的狗粮）
│
└── .github/           ← CI（audit.yml + test-examples.yml）
```

## 许可证

MIT
