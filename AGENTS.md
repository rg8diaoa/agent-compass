# AGENTS.md — agent-compass

> 复制到项目根目录。Agent 每次会话自动读取。

## Auto-Pilot 模式（默认开启）

以下全部流程自动执行，除非用户在当前对话中明确：
- 说"停"/"跳过"/"不用"中断当前动作
- 修改本文件（AGENTS.md）变更流程规则
- 要求暂停或切换模式

无人打断 = 无例外执行。Agent 不得等待提醒、不得跳过、不得事后补做。Auto-Pilot 高于 EXPLORE/PRECISE 模式——即使 EXPLORE 模式下也不得跳过自动动作。

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
Write-Host "[agent-compass] 安装完成。AGENTS.md + 4 核心文档已就位。Claude Code/Cursor/CodeWhale/OpenCode/Copilot/Windsurf 均可自动读取。"
```

**B — CodeWhale 全局 Skill**：
```powershell
mkdir -Force ~/.deepseek/skills/agent-compass
Copy-Item SKILL.md ~/.deepseek/skills/agent-compass/
Write-Host "[agent-compass] CodeWhale Skill 安装完成。重启会话后 `/skill agent-compass` 可用。"
```

**C — 暂不安装**：跳过，不追问。

安装完成后，若用户选了 A，Agent 应主动提示下一步："要我运行首次初始化吗？（生成 project-graph、反推设计依据、生成架构图）"

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

- 审计时：必须实际运行 `agent-compass audit`。不许凭记忆说"之前确认过"
- 验证时：必须读回写入的文件内容。不许假设"写成功了"
- 跨文件引用时：必须 `grep` 验证路径存在。不许凭记忆说"应该有"
- 工具失败时：报告中标注 [无法验证]。不许跳过也不许造假

## 并行安全

- 修改共享模块前 → 检查 HANDOFF 并行状态
- 如果 locked → 等待或选其他模块
- 如果 free → HANDOFF 加 [LOCKED] 条目
- `project-graph.yaml` 可选字段：`locked_by` / `locked_until`

## Auto-Pilot 自动动作（不可跳过）

以下动作在触发条件满足时自动执行，与任务是否"完成"无关。Agent 不得将其视为"可选"或"事后补做"。

| 触发 | 动作 | 执行时机 |
|------|------|----------|
| 每次代码变更（edit_file / write_file / apply_patch） | `agent-compass sync`（更新 project-graph） | 同一 turn 内立即执行 |
| 做了技术决策 | 追加 L4_O01：决策 / 来源 / 证据 | 同一 turn 内立即追加 |
| 会话即将结束 | 全量重写 HANDOFF（状态+上下文+具体下一步） | 结束前最后一轮 |
| git commit 之前 | 对照 14-production-readiness 退出标准 | commit 前 |
| 上下文 > 60% | HANDOFF 加 [CLOSING]，提醒用户切新会话 | 发现时立即 |
| 同一问题 3 轮无进展 | 停 → HANDOFF 加 [BLOCKED] | 第 3 轮结束时 |

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
| HANDOFF | 会话结束 |
| L3_J02 测试用例 | 新增 API 端点 |
| L2_D01 架构设计 | 项目初始化 / 架构变更 |

## 人类审 Agent（4 项及格线）

□ 模块 > 3 □ 有职责描述 □ L4_O01 有依据 □ 图已更新

## 状态标记

[IN_PROGRESS] / [NEEDS_HUMAN_REVIEW] / [NEEDS_HUMAN_DECISION] / [BLOCKED] / [CLOSING]

## 完整方法论

速查卡: `reference/cheatsheet.md` | 方法论导航: `methodology/INDEX.md`
