# agent-compass 🧭

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

> **你用自然语言指挥 Agent，项目自己记住结构和决策。**
>
> 像一个建筑工地的施工图——工人（Agent）换了一批又一批，图纸让新工人 30 秒知道哪面墙不能拆。

---

## 解决什么问题

你用 ChatGPT/Claude/CodeWhale（下面统称 Agent）写代码，但每次新对话 Agent 都会：

- **失忆**："上一个 Agent 做到哪了？"
- **迷路**：不知道哪个模块改会影响到谁
- **推翻**：把团队试过但放弃的方案又提议一次
- **不一致**：今天叫 `priority_level`，明天叫 `importance`

agent-compass 不是让 Agent 更强——**是给 Agent 一份施工图，给用户一份验收单**。你在家装时不懂水电，也能对照 checklist 说"这里不对"。

---

## 这个项目做了什么

| 现实生活中 | agent-compass |
|------|------|
| 建筑工地的施工图——哪面墙是承重不能拆 | **project-graph.yaml**（告诉 Agent 改了哪儿会塌） |
| 物业的装修记录——上次改水电是2024年，改的哪根管 | **L4_O01 设计依据**（去年为什么用JWT而不是Session） |
| 工人的交接班日志——白班干了什么，夜班从哪接 | **HANDOFF.md**（Agent A → Agent B 无缝接手） |
| 业主验收 checklist——水电通了？墙平了？ | **14-production-readiness**（你审 Agent 的 4 项及格线） |
| 你家装修的特殊要求——不能用某种材料、偏爱某种颜色 | **MEMORY.md**（不用 React，只用 Vue） |

---

## 三样拿手活

### 1. 给 Agent 写"施工图"，不是写"说明书"

别人给 Agent 写的是散文指令："本项目使用 FastAPI 框架，数据库是 PostgreSQL"。Agent 读完就忘了。

agent-compass 把项目结构写成**数据文件**——一份 YAML 图。Agent 每次打开项目读 30 秒，就知道：
- 有哪些模块（结构）
- 谁依赖谁（关系）
- 哪些改的时候要小心（稳定性）

### 2. 给不懂代码的人写"验收单"

Agent 写完代码你怎么知道好不好？8 个阶段每步有退出标准，4 项及格线。看到 □ 就打勾，少一个就让 Agent 补。

### 3. 每条规则背后都有"为什么"——踩过坑才写的

三轮审计从 12 个问题收敛到 0，不是"觉得应该这样"——是验证过的。

---

## 项目功能

### 核心文件

| 文件 | 功能 | 给谁用 |
|------|------|------|
| `AGENTS.md` | Agent 操作指令 | Agent 每次打开项目先读 |
| `docs/project-graph.yaml` | 项目结构图（数据文件） | Agent 写代码前 30 秒读 |
| `docs/L4_O01` | 每一条设计决策的来源和证据 | Agent 做技术决策前读 |
| `docs/HANDOFF.md` | 会话交接，做到哪了 + 下一步 | Agent 每次结束时写，下一个先读 |
| `docs/MEMORY.md` | 你的偏好（不用React、用中文注释等） | Agent 每次会话开始读 |

### 完整流程

```
研究（有没有人做过了？）→ 想法 → 设计 → 写文档 → 开发 → 测试 → 审计 →
修复 → 长期维护 → （循环）
```

### 一行命令完成

```bash
pip install agent-compass
agent-compass init /your/project    # 一键生成核心文件
agent-compass sync                  # 自动从代码更新项目图
agent-compass audit                 # 快速检查文档有没有坏链接
agent-compass doctor                # 检查缺了什么文件
```

### 数字

- 15 篇方法论
- 35 个可直接使用的模板（覆盖 16 个分类）
- 5 个 Skill（Agent 可加载的能力包）
- Python 和 Node.js 双语言示例

---

## 三步开始

### 步骤一：安装（30 秒）

```bash
pip install agent-compass
agent-compass init /your/project
```

### 步骤二：发给 Agent

复制下面这段话发给 Agent：

```
我正在用 agent-compass 方法初始化项目。
请读取 docs/project-graph.yaml — 告诉我当前项目结构。
如果 project-graph 是空的，请用 tree 和 grep 命令自动生成。
```

### 步骤三：看 demo

```bash
make todo-api-test   # 4 个测试全过
```

### 已有项目接入

你的项目已经写了一段时间了？不要全搬 35 个模板。见 `methodology/11-existing-project.md`——先搬 3 个文件就够了。

---

## 效果对比

| 场景 | 没有 | 有 |
|------|------|------|
| 第一行代码 | Agent 不知道从哪开始 | 读 project-graph，30 秒 |
| 修了一个 bug | 可能引入新 bug（不知道影响谁） | 读依赖图，知道影响的 2 个文件 |
| Agent 提方案 | "用 Session 吧" | 读历史决策——"去年已证明不行" |
| 换了 Agent | "做到哪了？" | 读交接——从下一步继续 |
| 审 Agent 产出 | "看起来差不多" | 对照 4 项——"补一下这里" |

---

## 实战效果

在一个 41 份文档、46 个配置维度的大型 Agent 协作项目中验证过。三轮审查从 12 个问题收到 0 个阻塞项。外部评分 9.0/10。

---

## 目录

```
agent-compass/
├── AGENTS.md          ← Agent 一看就用
├── SKILL.md           ← 一键加载
│
├── agent_compass/     ← 命令行工具
├── scripts/           ← 辅助脚本
├── skills/            ← 5 个可加载 Skill
│
├── methodology/       ← 15 篇方法论
├── templates/         ← 35 个模板（直接改就能用）
├── examples/          ← Python/Node 示例
├── reference/         ← 案例和对比
├── docs/              ← 自身文档（吃自己的狗粮）
│
└── .github/           ← 自动化检查
```

## 许可证

MIT
