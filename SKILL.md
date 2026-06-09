# agentprecept

## Description

让多个 Agent 在同一项目上协作不踩脚。核心机制：project-graph（秒懂结构）+ L4_O01（不推翻决策）+ HANDOFF（无缝交接）+ MCP Server（Code Agent 原生集成）+ gnhf（夜间自动同步）。Agent 按需读取模板，按指令自动产出。

## Instructions

### Auto-Pilot 模式（默认开启）

加载本 Skill 后，以下流程自动执行，无需用户提醒。除非用户在当前对话中明确说"停"/"跳过"/"不用"，或修改 AGENTS.md 变更规则。

- 代码变更后 → `agentprecept sync`；若 CLI 不可用 → 手动编辑 project-graph
- 设计决策后 → 立即追加 L4_O01（适配性修改也算决策）
- 会话结束信号 → 全量重写 HANDOFF（用户说"结束/交接/handoff/compact"、全部 checklist 完成且 2 轮无新任务、> 15 轮）
- git commit 前 → 对照 14-production-readiness
- 默认行为：完成任一模块后 → 追加测试任务到 checklist（每项 1-3 commit 粒度）；每 5 轮自问"缺设计文档吗？有该写没写的 MEMORY 教训吗？"；发现偏好/约束/教训 → grep 后追加 MEMORY.md（可更新旧行不可重复，追加后读回验证）；MCP 未配 → 提示配置；Hook/CI 未装 → 提示安装；缺模板 → 从 agentprecept templates/ 取
- 反馈提示：HANDOFF 状态为 [CLOSING] 时，Agent 应提示："如果这次体验有用，花 2 分钟在 GitHub 填反馈模板"
- 分支纪律：涉及架构/重命名/多文件（>10 文件）的变更必须在独立分支上执行
- 自选维度检查：每 5 轮对话检查自选维度是否退化
- 版本规则：严格 semver，PATCH 修 bug 累积 3+ 发版，MINOR 每个功能独立发版，MAJOR 破坏性变更
- 发版铁律：发布到 GitHub/PyPI 前必须 audit --gate FAIL 0 + 展示结果给用户 + 等用户确认（"发/发布/publish"）。严禁未经确认私自打 tag/push/twine upload，高于任何自动化
- ⏳ 待补检测：会话首次启动时，若 docs/ 中 ⏳ 待撰写状态的文档超过 3 份，Agent 应主动提醒"有 N 份文档待补充，要我填充吗？"
- 狗粮检查：agentprecept 自身项目必须通过自检：① L2_D01 反映当前架构 ② init 脚本引用的 templates/ 文件全部存在 ③ project-graph relations 不为空 ④ AGENTS/SKILL/instructions 关键规则一致
- 批量创建文件 > 15 个时 → 分子代理并行（单个子代理 ≤ 15 文件，超时 180s。依据：世界模拟器 37 文件迁移时 230s 超时）
- 模板外脑：docs/ 只有核心 8 文件。需要更多模板时从 agentprecept templates/（37 个）和 methodology/（16 篇）按需取用
- MCP Server：`python -m agentprecept.mcp_server`，6 个 tool（query/audit/diff/decision/handoff/design_gate），配置见 docs/mcp-tools.md
- audit：`agentprecept audit --gate` 15 维自动化 + 4 维自选清单提示
- 首次安装 → `agentprecept setup` 一键完成初始化 + MCP 配置指南

Agent 不得等待提醒、不得跳过、不得事后补做。Auto-Pilot 优先级高于工作模式（EXPLORE/PRECISE）。

### 设计先行原则

写代码前必须先有设计文档。新项目→架构设计(L2_D01)，新模块→模块设计(L2_F07)，数据变更→数据结构(L2_G01)，API 变更→API 契约(L2_G03)，技术选型→设计依据(L4_O01)。不满足→先出草稿→标注[NEEDS_HUMAN_REVIEW]→等确认("确认/可以/go/OK/开始")→确认前不得写代码。EXPLORE 下内容可简化但确认步骤不可跳过；PRECISE 下必须达模板完成标准。

### 新项目初始化检测

用户表达"写一个/搭一个/建一个XX"等意图时→Agent 识别为新项目创建→先跑 init.ps1/sh（AGENTS.md+7文档）→出架构设计草稿→人类确认→才能写代码。骨架不可跳过，即使用户说"直接做"。

### 讨论阶段拦截

用户提功能建议/讨论方案时→先整理要点→标注[NEEDS_HUMAN_REVIEW]→等确认→再进设计阶段。即使用户说"先试试"也必须先出方案要点。纯技术细节(命名/结构)由 Agent 自行决定，多方案选型/UX变更/外部信息必须问用户。

### 目标驱动执行（Karpathy 原则）

```
不是 "加验证"     → "写测试覆盖非法输入，然后让它们通过"
不是 "修复 bug"   → "写测试复现 → 测试通过 → 修复完成"
每个任务 = 可验证目标 + 验证方法。循环直到验证通过。
```

### 防偷懒（Anti-Laziness）

- 审计时：必须实际运行 `agentprecept audit`；若 CLI 不可用则运行 `python -m agentprecept.basic_audit`。不许凭记忆说"之前确认过"
- 验证时：必须读回写入的文件内容。不许假设"写成功了"
- 跨文件引用时：必须 `grep` 验证路径存在。不许凭记忆说"应该有"
- 工具失败时：报告中标注 [无法验证]。不许跳过也不许造假
- **审计缓存陷阱**：MCP tool 返回 TOOL_RESULT_REF（缓存引用）时，必须重新获取实际结果——不许把缓存引用当成"已审计"。审计结论必须来自本会话的工具实际输出
- 完成任一模块公开函数后：在 checklist 末尾追加对应测试任务
- git 操作异常时：index.lock 残留 → `del /f .git\index.lock` (Windows) 或 `rm .git/index.lock`；commit 失败 → 检查未追踪冲突文件

### 并行安全

- 修改共享模块前 → 检查 HANDOFF 并行状态
- 如果 locked → 等待或选其他模块
- 如果 free → HANDOFF 加 [LOCKED] 条目
- `project-graph.yaml` 可选字段：`locked_by` / `locked_until`

### 首次邂逅检测（Auto-Pilot）

当 Agent 检测到用户 clone/发送 agentprecept 仓库链接时，必须立即主动询问安装方式：

> 检测到 agentprecept。安装方式？
> [A] 当前项目安装（推荐，全工具通用） | [B] CodeWhale 全局 Skill | [C] 暂不安装

用户回答后立即执行：

- **A — 当前项目安装**：运行 `scripts/init.ps1`（Windows）或 `scripts/init.sh`（Linux/macOS）→ `pip install fastmcp -q`。复制 AGENTS.md 到项目根目录——Claude Code / Cursor / CodeWhale / OpenCode / Copilot / Windsurf 全部自动读取
- **B — CodeWhale 全局 Skill**：复制 `SKILL.md` 到 `~/.deepseek/skills/agentprecept/`
- **C — 暂不安装**：跳过，不追问

**A/B 安装后 Agent 必须立即执行 MCP 自动配置（同一 turn）**：
1. 检测当前工具：CodeWhale → `~/.deepseek/mcp.json` / Claude Code → `.mcp.json` / Cursor → `.cursor/mcp.json`
2. 若配置文件不存在 → 创建；若存在且无 agentprecept 条目 → 追加
3. MCP 条目（cwd 为 agentprecept 仓库绝对路径，Windows 必须 `PYTHONIOENCODING=utf-8`）：
   `{"mcpServers":{"agentprecept":{"command":"python","args":["-m","agentprecept.mcp_server"],"cwd":"<路径>","env":{"PYTHONIOENCODING":"utf-8","PYTHONUTF8":"1"}}}}`
4. 提示 git init

---

### Auto-Pilot 自动动作（不可跳过）

| 触发 | 动作 | 时机 |
|------|------|:--:|
| 代码变更 | `agentprecept sync` | 同一 turn |
| 技术决策 | 追加 L4_O01（决策/来源/证据） | 同一 turn |
| 会话结束 | 全量重写 HANDOFF | 结束前 |
| > 15 轮 | HANDOFF 加 [CLOSING] | 发现时立即 |
| 3 轮无进展 | HANDOFF 加 [BLOCKED] | 第 3 轮结束时 |

**会话结束信号**：用户说结束/交接/handoff/compact、全部 checklist 完成且 2 轮无新任务、> 15 轮。

**技术决策定义**（满足任一）：架构/库/框架选型、适配性修改、平台限制放弃特性、第三方依赖替换、数据 schema 变更、安全策略变更。适配性修改也算决策。

### 用户口头禅映射

| 用户说 | Agent 加载 |
|------|------|
| 初始化/init | examples/first-run.md |
| 修 bug/fix | 00-lifecycle §阶段7 + L3_J02 |
| 审计/audit | methodology/M4_D00 + `agentprecept audit` |
| 发布/release | 14-production-readiness §阶段8 |

### 核心模板

| 模板 | 触发 |
|------|------|
| project-graph.yaml | 每次代码变更 |
| L4_O01 | 做技术决策时 |
| HANDOFF | 会话结束信号 |
| L3_J02 | 新增公开函数/端点/命令 |

### 人类审 Agent（4 项）

- □ 模块 > 3: `project-graph.yaml` structure 键 ≥ 4
- □ 有职责描述: 每个模块 `description` 字段非空
- □ L4_O01 有依据: 文件行数 ≥ 5 + 最近一条 7 天内
- □ 图已更新: `evolution` 最新条目同比

### 状态标记

[IN_PROGRESS] / [NEEDS_HUMAN_REVIEW] / [NEEDS_HUMAN_DECISION] / [BLOCKED] / [CLOSING]

### 完整方法论

速查卡: `reference/cheatsheet.md` | 方法论导航: `methodology/INDEX.md`

### 文档体系搭建

当在新项目中初始化文档体系时：

1. **第一步**：复制 `templates/INDEX.md` 到 `docs/INDEX.md`，根据项目类型选择初始文档列表
2. **第二步**：复制 `templates/L1_A02_naming-convention_命名规范.md`，作为命名宪法
3. **第三步**：复制 `templates/HANDOFF.md`，每次会话结束前更新
4. **第四步**：在项目成长过程中，按需从 templates/ 中扩展其他文档

### 文档分层

本项目使用四层文档体系。创建新文档时，根据内容选择合适的层级和分类：

- **L1 蓝图**（A/B/C 类）：项目是什么、怎么跑起来、命名规则、术语。Agent 每次会话开始时读取
- **L2 核心**（D/E/F/G 类）：架构设计、配置规范、开发手册、API 契约。Agent 做技术决策时读取
- **L3 实施**（H/I/J/K/L 类）：集成方案、前端设计、测试策略、验收标准、用户手册。Agent 写代码时读取
- **L4 追溯**（M/N/O/P 类）：变更日志、迁移方案、设计依据、运维手册。Agent 维护和迁移时读取

### 命名格式

```
L{Level}_{Category}{NN}_{Slug}_{Title}.md
```

分类码 A-P。详见 methodology/M3_C00_naming_命名即导航.md。

**弹性条款**：项目多版本共存、外部生成文件允许偏离格式，偏离时在 HANDOFF 中标注原因。

### 文档状态

每个文档头部标注状态：⏳待撰写 / 📝撰写中 / 🔍审查中 / ✅已锁定 / ❌已废弃。Agent 只引用 ✅ 或 🔍 状态的文档作为可靠依据。

### 一等公民

四份文档在任何项目中不可缺：INDEX.md（目录） / 命名规范 / 术语表 / HANDOFF.md（交接）。

### 项目图

为项目维护 `project-graph.yaml`，三层结构：

- **结构层**：包/模块/文件的层级关系
- **关系层**：依赖、调用、引用、关联 issue
- **演变层**：设计决策（ADR）、关键 commit、发布版本

Agent 在修改核心模块前应查询项目图确定影响范围。

### 审计

文档体系应定期进行审计（`agentprecept audit --gate`，15 维自动化 + 自选清单）。Agent 可执行审计并输出结构化报告。

### 会话交接

每次会话结束时，Agent 应全量重写 HANDOFF.md：

- 当前状态（完成/进行中/阻塞）
- 本会话具体完成事项
- 下一步（具体一步，非方向描述）
- 关键决策

### 设计依据

做技术决策前，先查设计依据文档（L4_O01）。做完决策后，追加一行记录：决策 / 来源 / 证据。

### 适用场景

- **代码项目**：后端服务、前端应用、CLI、微服务、SDK
- **知识库**：技术文档、内部 wiki、课程体系
- **项目管理**：需求文档、设计文档、团队协作
- **配置管理**：30+ 独立配置项的复杂系统
