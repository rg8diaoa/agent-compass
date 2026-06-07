# AGENTS.md — agent-compass

> 复制到项目根目录。Agent 每次会话自动读取。

## Auto-Pilot 模式（默认开启）

以下全部流程自动执行，除非用户在当前对话中明确：
- 说"停"/"跳过"/"不用"中断当前动作
- 修改本文件（AGENTS.md）变更流程规则
- 要求暂停或切换模式

无人打断 = 无例外执行。Agent 不得等待提醒、不得跳过、不得事后补做。Auto-Pilot 高于 EXPLORE/PRECISE 模式——即使 EXPLORE 模式下也不得跳过自动动作。

---

## 默认行为（无条件执行）

以下行为不需要触发条件，每个会话默认执行。Agent 不得跳过：

- **会话首次启动**：读 `docs/project-graph.yaml` → `docs/HANDOFF.md` → `docs/MEMORY.md`
- **完成任一模块后**：检查 checklist 中是否有对应测试任务，没有则追加
- **每 5 轮对话**：自问"有没有该写但还没写的设计文档？"
- **项目首次初始化后**：提醒创建 `docs/HANDOFF.md` 和 `docs/MEMORY.md` 空模板

---

## 设计先行原则

Agent 不是码农——是工程师。工程师动工前必有图纸。

在 write_file / edit_file / apply_patch 之前，Agent 必须先确认对应设计文档就位且已读：

| 变更类型 | 前置设计文档 | 模板 |
|---------|-------------|------|
| 新项目 | 架构设计（模块划分 + 职责描述 + 数据流 + 接口约定） | L2_D01 |
| 新模块 | 模块设计（职责 + 对外接口 + 内部结构） | L2_F07 |
| 数据库/数据模型变更 | 数据结构设计（实体关系 + 约束 + 迁移方案） | L2_G01 |
| API 新增/变更 | API 契约（端点 + 请求/响应格式 + 错误码） | L2_G03 |
| 架构/技术选型决策 | 设计依据（为什么选这个方案 + 对比过的替代方案） | L4_O01 |

不满足前置条件时，Agent 必须：
1. 输出对应设计文档草稿
2. 标注 [NEEDS_HUMAN_REVIEW]
3. 等待人类确认（以下任一信号视为确认："确认"/"可以"/"go"/"OK"/"开始"/"执行"；"不用审"/"直接做"也视为确认放行）
   **在收到确认信号前，Agent 不得执行 write_file / edit_file / apply_patch / git commit。**
4. 确认后 → 再写代码

```
完整流程: 设计文档 → 人类确认 → 写代码 → 测试 → 审计
          ↑ 不许跳               ↑ 设计没确认不许动工
```

EXPLORE 下设计文档**内容**可简化（标题 + 3 行要点即可），但 [NEEDS_HUMAN_REVIEW] 标记和等待确认的步骤不可跳过。
PRECISE 下设计文档必须达到对应模板的"完成标准"才放行。

---

## 首次邂逅检测（Auto-Pilot）

当 Agent 在当前会话中检测到以下任一信号：
- 用户发送了 agent-compass 仓库链接（GitHub/Gitee/本地路径）
- 用户要求 clone/fetch/下载 agent-compass
- agent-compass 目录刚出现在工作区中
- 用户说"安装 agent-compass"或类似表述

Agent 必须立即（同一 turn 内）主动询问，不得跳过：

> 检测到 agent-compass。安装方式？
> **[A] 当前项目安装（推荐）** — 复制 AGENTS.md 到项目根目录。Claude Code / Cursor / CodeWhale / OpenCode / Copilot / Windsurf 全支持——它们都自动读取项目根目录的 AGENTS.md
> **[B] CodeWhale 全局 Skill** — 复制 SKILL.md 到 `~/.deepseek/skills/`，所有项目可用（仅 CodeWhale 用户有意义）
> **[C] 暂不安装** — 跳过，以后再说

用户选择后立即执行：

**A — 当前项目安装（全工具通用）**：
```powershell
.\scripts\init.ps1 .
# Linux/macOS: bash scripts/init.sh .
Write-Host "[agent-compass] 安装完成。AGENTS.md + 7 核心文档已就位。Claude Code/Cursor/CodeWhale/OpenCode/Copilot/Windsurf 均可自动读取。"
Write-Host "要我初始化 git 仓库吗？"
```

**B — CodeWhale 全局 Skill**：
```powershell
mkdir -Force ~/.deepseek/skills/agent-compass
Copy-Item SKILL.md ~/.deepseek/skills/agent-compass/
Write-Host "[agent-compass] CodeWhale Skill 安装完成。重启会话后 `/skill agent-compass` 可用。"
```

**C — 暂不安装**：跳过，不追问。

安装完成后，若用户选了 A，Agent 应主动提示：
> 要我运行首次初始化吗？（git init、生成 project-graph、反推设计依据、生成架构图）

---

## 新项目初始化检测

当用户在对话中表达创建新项目/新工具/新应用的意图时——无论措辞如何（"帮我写一个日记应用""搭一个 API 服务""建一个爬虫""我需要一个任务管理工具"）——Agent 必须识别为**新项目创建意图**，不得跳过以下步骤：

1. **骨架初始化**：运行 `scripts/init.ps1 .`（Windows）或 `scripts/init.sh .`（Linux/macOS），产出 AGENTS.md + docs/ 下 7 个核心文档
2. **版本控制**：提示用户是否 git init
3. **默认 checklist**：生成初始 checklist，第一项必须包含 git init + 文档补全 + 架构设计 + project-graph 生成
4. **设计先行**：按设计先行原则，先出架构设计草稿（L2_D01），标注 [NEEDS_HUMAN_REVIEW]，等确认后才能写代码

> 初始化完成前不得写实现代码。即使用户说"直接做"，Agent 也必须先完成骨架 + 架构设计草稿，否则就是裸写。

EXPLORE 下骨架不可跳过（必须执行 init），设计文档可简化（标题 + 3 行要点）。
PRECISE 下 design 文档必须达到模板完成标准。

---

## 会话启动（Auto-Pilot 自动）

1. 读 `docs/project-graph.yaml` → 项目结构
2. 读 `docs/HANDOFF.md` → 做到哪了
3. 读 `docs/MEMORY.md` → 人类偏好

## 工作模式

- [EXPLORE] 默认：直接出 MVP，标注假设。明显歧义才问。适用于快速原型
- [PRECISE] 用户说"精确模式"/"重构"/"修 bug"→ 严格遵循硬规则。适用于生产级变动

## 目标驱动执行（Karpathy 原则）

```
不是 "加验证"     → "写测试覆盖非法输入，然后让它们通过"
不是 "修复 bug"   → "写测试复现 → 测试通过 → 修复完成"
每个任务 = 可验证目标 + 验证方法。循环直到验证通过。
```

## 防偷懒（Anti-Laziness）

- 审计时：必须实际运行 `agent-compass audit`；若 CLI 不可用则运行 `python scripts/basic-audit.py`。不许凭记忆说"之前确认过"
- 验证时：必须读回写入的文件内容。不许假设"写成功了"
- 跨文件引用时：必须 `grep` 验证路径存在。不许凭记忆说"应该有"
- 工具失败时：报告中标注 [无法验证]。不许跳过也不许造假
- 完成任一模块公开函数后：在 checklist 末尾追加对应测试任务。来不及写时在 HANDOFF 标注原因

## 并行安全

- 修改共享模块前 → 检查 HANDOFF 并行状态
- 如果 locked → 等待或选其他模块
- 如果 free → HANDOFF 加 [LOCKED] 条目
- `project-graph.yaml` 可选字段：`locked_by` / `locked_until`

## Auto-Pilot 自动动作（不可跳过）

以下动作在触发条件满足时自动执行，与任务是否"完成"无关。Agent 不得将其视为"可选"或"事后补做"。

| 触发 | 动作 | 降级（工具不可用时） | 执行时机 |
|------|------|---------------------|----------|
| 每次代码变更（edit_file / write_file / apply_patch） | `agent-compass sync` 更新 project-graph | 手动编辑 project-graph.yaml，追加 structure/relations/evolution | 同一 turn 内立即执行 |
| 做了技术决策 | 追加 L4_O01：决策 / 来源 / 证据 | 无降级——编辑 .md 文件始终可行 | 同一 turn 内立即追加 |
| 会话结束信号（见下方列表） | 全量重写 HANDOFF（状态+上下文+具体下一步） | 同上 | 结束前最后一轮 |
| git commit 之前 | 对照 14-production-readiness 退出标准 | 对照方法论 memory（已读过 14-production-readiness.md） | commit 前 |
| 对话轮数 > 15 | HANDOFF 加 [CLOSING]，提醒用户切新会话 | — | 发现时立即 |
| 同一问题 3 轮无进展 | 停 → HANDOFF 加 [BLOCKED] | — | 第 3 轮结束时 |

### 会话结束信号（任一发生即触发 HANDOFF 重写）

- 用户说"结束"/"交接"/"handoff"/"compact"
- 用户说"下一个会话"/"换模型"
- 全部 checklist 项 completed + 用户连续 2 轮未发新任务
- 对话轮数 > 15（Agent 数自己回复次数）

### "技术决策"定义（满足任一即触发 L4_O01 追加）

技术决策包括但不限于：
- 架构/库/框架选型（"选 X 而不是 Y"）
- 因框架/库版本不兼容被迫改变 API 调用方式（适配性修改）
- 因平台限制放弃设计特性（"X 平台不支持 Y，改用 Z"）
- 第三方依赖替换或版本锁定
- 数据结构 schema 变更
- 安全策略变更

**适配性修改也算决策。** 不是只有"选 A 还是选 B"才算——被迫改调用方式同样需要记录为什么。

## 用户口头禅映射

| 用户说 | Agent 加载 |
|------|------|
| "初始化"/"init" | examples/first-run.md |
| "加功能"/"新端点" | L2_D01 + L3_J02 |
| "修 bug"/"fix" | 00-lifecycle §阶段7 + L3_J02 |
| "审计"/"audit" | methodology/04 + `python scripts/basic-audit.py docs/` |
| "发布"/"release" | 14-production-readiness §阶段8 |
| "交接"/"handoff" | 重写 docs/HANDOFF |

## 核心模板（Agent 主动加载）

| 模板 | 触发条件 |
|------|------|
| project-graph.yaml | 每次代码变更 |
| L4_O01 设计依据 | 做技术决策时 |
| HANDOFF | 会话结束信号 |
| L3_J02 测试用例 | 新增模块公开函数 / API 端点 / CLI 命令 |
| L2_D01 架构设计 | 项目初始化 / 架构变更 |

## 人类审 Agent（4 项及格线 → 可验证）

| 检查项 | 可验证方式 |
|--------|-----------|
| □ 模块 > 3 | `project-graph.yaml` 的 structure 键 ≥ 4 |
| □ 有职责描述 | 每个模块 `description` 字段非空 |
| □ L4_O01 有依据 | 文件行数 ≥ 5 + 最近一条日期在 7 天内 |
| □ 图已更新 | `evolution` 最新条目与最后代码变更为同一会话 |

## 状态标记

[IN_PROGRESS] / [NEEDS_HUMAN_REVIEW] / [NEEDS_HUMAN_DECISION] / [BLOCKED] / [CLOSING]

## 完整方法论

速查卡: `reference/cheatsheet.md` | 方法论导航: `methodology/INDEX.md`
