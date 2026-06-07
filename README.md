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

你用 code agent（下面统称 Agent）写代码，但每次新对话 Agent 都会：

- **失忆**："上一个 Agent 做到哪了？"
- **迷路**：不知道哪个模块改会影响到谁
- **推翻**：把团队试过但放弃的方案又提议一次
- **不一致**：今天叫 `priority_level`，明天叫 `importance`
- **裸写**：拿到需求跳过设计直接写代码，架构全在脑子里没落文档

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
| 设计图纸——承重墙在哪、管线怎么走 | **L2_D01 架构设计** — 模块划分 + 职责描述 + 数据流 + 接口约定（设计先行原则强制前置） |
| 监理检查工具——8 维自动化巡检 | **basic-audit.py** — 命名/引用/编号/残留/图格式/追溯/覆盖率/狗粮，一行命令全跑 |

---

## 五样拿手活

### 1. 结构化数据，不是散文指令

给 Agent 写一段话："本项目使用 FastAPI，数据库 PostgreSQL"。Agent 读一遍就忘了，下一轮重新遍历源码。

agent-compass 把项目结构写成**机器可消费的 YAML 图**（structure / relations / evolution）。Agent 每次新会话读 30 秒，不需遍历源码即可重建心智模型。`stability` 字段区分改模块的风险等级。

### 2. 不懂代码的人也能审 Agent 产出 + 自动化审计

Agent 提交了架构设计——你对照 4 项：
- □ 模块 > 3（`project-graph.yaml` structure 键数 ≥ 4）
- □ 有职责描述（每个模块 `description` 非空）
- □ L4_O01 有依据（行数 ≥ 5 + 最近一条 7 天内）
- □ 图已更新（`evolution` 最新条目与最后一次变更同会话）

4 项全 □ → 及格。少 1 项 → 告诉 Agent "补一下这里"。

**8 维自动化审计**：`python scripts/basic-audit.py docs/` 一行命令跑完命名一致性、交叉引用完整性、编号连续性、骨架残留、项目图格式、设计追溯、覆盖率、狗粮审计。方法论 14 维中能自动化的全部就位。

### 3. 教训驱动——每条规则踩过坑

三轮审计从 12 个问题收敛到 0 阻塞项。不是"你应该这样做"的道德说教，是"上次它炸了所以这次必须这样做"。`stability: critical` 规则来自真实线上事故：改 auth 模块不知道 admin 也依赖它。

### 4. 设计先行 + 讨论拦截——方案没对齐不动手

Agent 拿到需求容易跳过设计直接写代码——或者在讨论中就顺手改了。agent-compass 强制三道拦截：

```
讨论新功能 → 整理方案要点 → [NEEDS_HUMAN_REVIEW] → 确认
         → 设计文档草稿 → 确认("go/OK/开始") → 写代码
```

新项目必须出架构设计（L2_D01），新模块必须有模块设计（L2_F07），API 变更必须先写契约（L2_G03）。确认信号明确了——"确认/可以/go/OK/开始/执行"或"不用审/直接做"。EXPLORE 下内容可简化但确认步骤不可跳过。

### 5. 新项目自举——说"建一个XX"就自动初始化

用户说"帮我写一个日记应用"、"搭一个 API 服务"——Agent 识别为新项目创建意图，自动：运行 `init.ps1`（AGENTS.md + 7 核心文档）→ 提示 git init → 出架构设计草稿 → 等确认 → 才能写代码。骨架不可跳过，即使用户说"直接做"。

---

## 核心文件

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | Agent 行为规则（Auto-Pilot + 设计先行 + 讨论拦截 + 降级路径 + 双模式） |
| `docs/project-graph.yaml` | 项目结构图——YAML 数据，Agent 30 秒读取 |
| `docs/L2_D01` | 架构设计 — 模块划分 + 职责 + 数据流 + 接口（设计先行） |
| `docs/L2_G01` | 数据结构设计 — 实体关系 + 约束 |
| `docs/L2_G03` | API 契约 — 端点 + 请求/响应格式 |
| `docs/L4_O01` | 设计决策追溯——决策/来源/证据 |
| `docs/HANDOFF.md` | 跨会话交接 + 5 状态标记 + 上下文用量 |
| `docs/MEMORY.md` | 持久偏好和项目约束 |

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
pip install agent-compass
agent-compass init /your/project    # 一键生成核心文件
agent-compass sync                  # 从代码自动同步 project-graph
agent-compass audit                 # 8 维自动化审计（命名/引用/编号/残留/格式/追溯/覆盖/狗粮）
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
| Agent 想写新模块 | 直接开始写 | 先出模块设计草稿，确认后再动工 |
| 讨论新功能 | "好的，加一下"直接改 | 先整理方案要点，确认后再进设计 |
| 建一个新项目 | 直接开始写代码 | init 骨架 + 架构草稿 → 确认 → 动工 |

---

## 实战效果

在一个 41 份文档/46 个配置维度的多 Agent 协作项目中验证。三轮审计从 12 个问题收敛到 0 阻塞项。外部评审 9.0/10。

---

## 目录

```
agent-compass/
├── AGENTS.md          ← Agent 一看就用
├── SKILL.md           ← 一键加载 Skill
├── pyproject.toml     ← pip install agent-compass
│
├── agent_compass/     ← CLI（init/sync/audit/doctor）
├── scripts/           ← sync-graph(符号级)/graph-to-mermaid/basic-audit(8维)/check-naming
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

## 灵感来源

- **ECC** — Agent 命令映射与持久记忆模式
- **Andrej Karpathy's LLM Coding Style** — 目标驱动执行、"一个文件改善 Agent 行为"
- **CodeToFlow** — 代码结构可视化理念

核心方法论源自本人的一个 41 文档/46 配置维度的多 Agent 协作实战项目。

## 许可证

MIT
