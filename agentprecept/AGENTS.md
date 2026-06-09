# AGENTS.md — agentprecept

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
- **checklist 粒度**：每项 checklist 必须在 1-3 个 commit 内完成。若某项预估需 5+ commit，Agent 必须拆成多个 checklist item。粒度标准：人类 review ≤ 5 分钟。架构边界（project-graph structure 的模块划分）即 checklist 的天然切割线
- **每 5 轮对话**：自问两件事——"有没有该写但还没写的设计文档？"+"有没有该追加到 MEMORY.md 的教训但还没写？"
- **项目首次初始化后**：提醒创建 `docs/HANDOFF.md` 和 `docs/MEMORY.md` 空模板
- **⏳ 待补检测**：会话首次启动时，若 docs/ 中 ⏳ 待撰写状态的文档超过 3 份，Agent 应主动提醒"有 N 份文档待补充，要我填充吗？"。用户确认后按设计先行原则逐份填充——先出草稿→标注[NEEDS_HUMAN_REVIEW]→等确认→再写
- **狗粮检查**：agentprecept 自身项目必须通过以下自检，否则先修再继续：① L2_D01 反映当前架构 ② init 脚本引用的 templates/ 文件全部存在 ③ project-graph relations 不为空（有代码时）④ AGENTS/SKILL/instructions 关键规则一致。agentprecept 自身必须吃自己的狗粮
- **记忆自动生长**：Agent 在对话中发现新的用户偏好、项目约束、踩坑教训时，**同一 turn 内立即追加**到 `docs/MEMORY.md` 对应小节。追加前先 grep 确认无相似条目（不凭记忆判断）；已有条目可更新（替换旧行），不可重复追加。追加后读回验证格式正确。用户说"记住"→立即追加。会话结束前回顾确认全部已写入。模板注释（`<!-- ... -->`）仅第一次追加时删除
- **MCP 缺失检测**：当项目已有 AGENTS.md 但 `mcp_agentprecept_*` tools 不可用时，Agent 应提示用户配置 MCP（`agentprecept setup` 或手动编辑 mcp.json）
- **Hook/CI 检测**：每次会话启动时检查 `.git/hooks/pre-commit` 和 `.github/workflows/` 是否存在。缺失 → 提示 `agentprecept hooks install` 或 `agentprecept init --ci`。CI gate 是唯一不可跳过的硬拦截——没装等于没有防线
- **模板外脑**：docs/ 只有核心 8 文件。需要 API 契约、测试策略、部署方案等模板时，Agent 应知道从 agentprecept 仓库的 `templates/`（37 个）和 `methodology/`（16 篇）按需取用
- **反馈提示**：HANDOFF 状态为 [CLOSING] 时，Agent 应提示："如果这次体验有用，花 2 分钟在 GitHub 填反馈模板"
- **分支纪律**：涉及架构/重命名/多文件（>10 文件）的变更必须在独立分支上执行。pre-commit hook 强制拦截 main/master 分支上 >10 文件的 commit（可 `--no-verify` 跳过）；CI gate 维度 11 不可跳过
- **自选维度检查**：每 5 轮对话检查自选维度（用户旅程/定位审计/复用/社区就绪度）是否退化。`agentprecept audit --gate` 报告末尾有自选清单
- **版本规则**：严格 semver。PATCH（v0.4.1）修 bug 不增删功能——累积 3+ 修复或 1 个关键修复后发布；MINOR（v0.5.0）新增向后兼容功能，每个功能独立发版不等累积；MAJOR（v1.0.0）破坏性变更。升级方式：全量（`pip install -U agentprecept`），11KB wheel 不搞增量
- **发版铁律**：任何版本发布到 GitHub/PyPI 前，必须完成 audit --gate FAIL 0 验证 + 将验证结果展示给用户 + 等待用户明确确认（"发"/"发布"/"publish"/"go ahead"）。Agent 严禁未经用户确认私自打 tag、push、或 twine upload。这条规则高于任何自动化——即使 Auto-Pilot 也不得跳过
- **批量创建文件**：> 15 个文件时 → 分子代理并行（单个子代理 ≤ 15 文件，超时 180s。依据：世界模拟器 37 文件迁移时 230s 超时）

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
| **agentprecept 自身架构变更** | **更新 docs/L2_D01 + 追加 L4_O01** | **自身 L2_D01** |

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

> **"go" 的语义**：用户说 "go" 表示确认的是 Agent **上一轮输出的设计草稿**。如果上一轮没有设计草稿只有讨论，Agent 必须先输出草稿再等确认——不得把讨论中的 "go" 当成跳过设计的通行证。

> **agentprecept 自身变更也适用**：即使是修改 AGENTS.md、SKILL.md、instructions.md 或 init 脚本，也属于"架构决策"，必须先出 L4_O01 条目草稿，标注 [NEEDS_HUMAN_REVIEW]，等确认后再改代码。

EXPLORE 下设计文档**内容**可简化（标题 + 3 行要点即可），但 [NEEDS_HUMAN_REVIEW] 标记和等待确认的步骤不可跳过。
PRECISE 下设计文档必须达到对应模板的"完成标准"才放行。

### 讨论阶段拦截

用户提出功能建议、改进方向、或讨论方案时，Agent 不得在讨论中直接写代码。流程：

```
讨论 → 整理方案要点 → [NEEDS_HUMAN_REVIEW] → 确认 → 设计文档 → 确认 → 写代码
       ↑ 方案没对齐不许进入设计阶段
```

即使用户说"先试试"或"做个原型"，Agent 也必须先整理方案要点（3-5 条），标注假设和待确认项，等用户回应后再动手。

> **重要**：讨论阶段中用户说 "go"/"可以"/"OK" 仅表示认可方案方向，不等于跳过设计文档。流程仍然是两步确认：方案要点确认 → 设计文档确认 → 写代码。agentprecept 自身开发不得豁免。

### Agent 决策权

在设计阶段，Agent 必须区分两类事项：

**必须问用户**：
- 多方案选型（列出对比 + 推荐一个）
- 影响用户体验的行为变更
- 需要外部提供的信息（密钥、配置值、API 地址等）
- 数据格式/存储方案的选择

**Agent 自行决定**（不追问）：
- 变量命名、代码结构、文件组织
- 纯技术实现细节（算法选择、库版本等）
- 错误处理策略、日志格式
- 默认值（标注原因，用户可后续修改）

---

## 首次邂逅检测（Auto-Pilot）

当 Agent 在当前会话中检测到以下任一信号：
- 用户发送了 agentprecept 仓库链接（GitHub/Gitee/本地路径）
- 用户要求 clone/fetch/下载 agentprecept
- agentprecept 目录刚出现在工作区中
- 用户说"安装 agentprecept"或类似表述

Agent 必须立即（同一 turn 内）主动询问，不得跳过：

> 检测到 agentprecept。安装方式？
> **[A] 当前项目安装（推荐）** — 复制 AGENTS.md 到项目根目录。Claude Code / Cursor / CodeWhale / OpenCode / Copilot / Windsurf 全支持——它们都自动读取项目根目录的 AGENTS.md
> **[B] CodeWhale 全局 Skill** — 复制 SKILL.md 到 `~/.deepseek/skills/`，所有项目可用（仅 CodeWhale 用户有意义）
> **[C] 暂不安装** — 跳过，以后再说

用户选择后立即执行：

**A — 当前项目安装（全工具通用）**：
```powershell
.\init.ps1 .
pip install fastmcp -q
Write-Host "[agentprecept] AGENTS.md + 7 核心文档已就位。"
```

**安装后 Agent 必须立即执行 MCP 自动配置（同一 turn）**：
1. 检测当前工具：CodeWhale → `~/.deepseek/mcp.json` / Claude Code → `.mcp.json` / Cursor → `.cursor/mcp.json`
2. 若配置文件不存在 → 创建；若存在且无 agentprecept 条目 → 追加
3. MCP 条目（含 cwd 和编码兼容）：
   - `cwd` 设为 agentprecept 仓库的绝对路径
   - `env.PYTHONIOENCODING=utf-8` + `env.PYTHONUTF8=1`（Windows 必需，防止 GBK 编码损坏 MCP 握手消息）
   - 完整 JSON：`{"mcpServers":{"agentprecept":{"command":"python","args":["-m","agentprecept.mcp_server"],"cwd":"<agentprecept绝对路径>","env":{"PYTHONIOENCODING":"utf-8","PYTHONUTF8":"1"}}}}`
4. 输出：`[agentprecept] MCP 已自动配置。重启后 6 tools 可用。`
5. 提示 git init

**B — CodeWhale 全局 Skill**：
```powershell
mkdir -Force ~/.deepseek/skills/agentprecept
Copy-Item SKILL.md ~/.deepseek/skills/agentprecept/
Write-Host "[agentprecept] CodeWhale Skill 安装完成。"
```
安装后同样执行 MCP 自动配置（步骤 A 的 1-4）。

**C — 暂不安装**：跳过，不追问。

---

## 新项目初始化检测

当用户在对话中表达创建新项目/新工具/新应用的意图时——无论措辞如何（"帮我写一个日记应用""搭一个 API 服务""建一个爬虫""我需要一个任务管理工具"）——Agent 必须识别为**新项目创建意图**，不得跳过以下步骤：

1. **骨架初始化**：运行 `init.ps1 .`（Windows）或 `init.sh .`（Linux/macOS），产出 AGENTS.md + docs/ 下 7 个核心文档
2. **版本控制**：提示用户是否 git init
3. **默认 checklist**：按 commit 粒度生成初始 checklist。第一项集合不得合并为"项目初始化"一个 item——必须拆为：
   - git init（1 commit）
   - docs/ 7 核心文档补全（1 commit）
   - L2_D01 架构设计草稿（1 commit，需 [NEEDS_HUMAN_REVIEW]）
   - project-graph 初始生成（1 commit，`agentprecept sync`）
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

### 命名规范弹性条款

L{Level}_{CAT}{NN}_{Slug}_{Title}.md 是推荐格式，以下情况允许偏离：
- 项目多版本共存（`_V2`、`_legacy` 后缀保留）
- 外部生成文件（CI 配置、OpenAPI 自动生成 spec）
- 偏离时在 HANDOFF 中标注原因。basic-audit.py 的命名检查对偏离文件产生 WARN/FAIL 是预期行为——Agent 应在审计报告中查阅 HANDOFF 判断是否为合理豁免

规范服务项目，不是反过来。

## 目标驱动执行（Karpathy 原则）

```
不是 "加验证"     → "写测试覆盖非法输入，然后让它们通过"
不是 "修复 bug"   → "写测试复现 → 测试通过 → 修复完成"
每个任务 = 可验证目标 + 验证方法。循环直到验证通过。
```

## 防偷懒（Anti-Laziness）

- 审计时：必须实际运行 `agentprecept audit`；若 CLI 不可用则运行 `python -m agentprecept.basic_audit`。不许凭记忆说"之前确认过"
- 验证时：必须读回写入的文件内容。不许假设"写成功了"
- 跨文件引用时：必须 `grep` 验证路径存在。不许凭记忆说"应该有"
- 工具失败时：报告中标注 [无法验证]。不许跳过也不许造假
- **审计缓存陷阱**：MCP tool 返回 TOOL_RESULT_REF（缓存引用）时，必须重新获取实际结果——不许把缓存引用当成"已审计"。审计结论必须来自本会话的工具实际输出
- 完成任一模块公开函数后：在 checklist 末尾追加对应测试任务。来不及写时在 HANDOFF 标注原因
- **git 操作异常时**：index.lock 残留 → `del /f .git\index.lock` (Windows) 或 `rm .git/index.lock`；分支名避免含 `/`（Windows 路径兼容）；commit 失败 → 检查是否有未追踪冲突文件

## 并行安全

- 修改共享模块前 → 检查 HANDOFF 并行状态
- 如果 locked → 等待或选其他模块
- 如果 free → HANDOFF 加 [LOCKED] 条目
- `project-graph.yaml` 可选字段：`locked_by` / `locked_until`

## Auto-Pilot 自动动作（不可跳过）

以下动作在触发条件满足时自动执行，与任务是否"完成"无关。Agent 不得将其视为"可选"或"事后补做"。

| 触发 | 动作 | 降级（工具不可用时） | 执行时机 |
|------|------|---------------------|----------|
| 每次代码变更（edit_file / write_file / apply_patch） | `agentprecept sync` 更新 project-graph | 手动编辑 project-graph.yaml，追加 structure/relations/evolution | 同一 turn 内立即执行 |
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
| "审计"/"audit" | methodology/M4_D00 + `agentprecept audit` |
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
