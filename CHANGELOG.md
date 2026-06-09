# 变更日志

## [0.4.3] — 2026-06-09

### 修复

- **MCP audit 路径推导错误**：`check_dogfood`/`check_readme_claims`/`check_terminology` 改用 `_find_project_root(docs_dir)` 向上查找项目根目录（以 `.git` 为边界），不再依赖 CWD。修复传入 `docs_dir="world-simulator/docs"` 时狗粮维度 3 项假阳性
- **CLI GBK 编码崩溃**：`main()` 入口添加 `sys.stdout.reconfigure(encoding='utf-8')`，防止 Windows GBK 终端无法编码 emoji
- **包入口缺失**：新增 `agentprecept/__main__.py`，支持 `python -m agentprecept`
- **`__version__` 缺失**：`__init__.py` 导出 `__version__`，从 `importlib.metadata` 读取

### 恢复

- 恢复 7 个被误删的模板文件（`Path.replace()` 移动而非复制的 bug 仍待修复）

---

## [0.4.0] — 2026-06-09

### project-graph 全量重建

- **100% 覆盖率**：27 条 relations，覆盖 agentprecept/ ↔ scripts/ ↔ docs/ ↔ templates/ ↔ methodology/
- **ripple_check.py**：涟漪分析脚本，DIRECT / INDIRECT / SAME_PKG 三级影响分析

### 审计深度升级

- **basic-audit.py 4-scope 重构**：docs / code / git / config 四个维度独立审计 + `--scope` flag
- **狗粮维度重写**：4 项存在性检查 → 自治健康度多维评估
- **自选维度恢复**：从遗忘恢复 → 审计报告清单提示

### 设计文档补全

- **L4_O01**：追加 ADR-008 ~ ADR-019（12 条设计决策，含重命名/init 升级/三层拦截/gnhf 可选/CI 交互/checklist 粒度/审计扩展/涟漪分析）
- **L2_D01**：九层架构 + 任务拆分粒度 + 强制拦截三层体系完整文档

### 规则与体验优化

- **版本规则**：严格 semver（主版本.次版本.修订号）
- **反馈提示**：HANDOFF [CLOSING] 时提醒填写反馈模板
- **模板扩展**：36 → 37（新增 MEMORY.md 为一等公民）

---

## [0.3.0] — 2026-06-08

### init 能力接入器（文档复制器 → 6 阶段全自动接入）

- **init 6 阶段**：骨架 / Git / Pre-commit Hook / gnhf / CI Gate / MCP —— 一键运行，全部就位
- **hooks 子命令**：`agentprecept hooks install/uninstall/status`
- **gnhf 子命令**：`agentprecept gnhf setup/task/status`
- **CI Gate 模板**：`agentprecept init` 检测已有 CI 后询问是否追加 PR 门禁
- **接入状态报告**：`agentprecept init --status` 输出完整能力矩阵
- **Flag 支持**：`--yes / --dry-run / --status / --ci / --no-ci / --no-gnhf`

### 强制拦截三层体系

- **Layer 1 — MCP design_gate**：第 6 个 MCP tool，Agent 写代码前调用，返回模块的前置设计文档状态（CLEAR/BLOCKED）
- **Layer 2 — Git Pre-commit Hook**：init 自动安装，代码变更时检查核心设计文档是否存在（`git commit --no-verify` 跳过）
- **Layer 3 — CI Pipeline Gate**：`agentprecept audit --gate`（10 维），PR 不通过无法 merge

### 审计升级：8 维 → 10 维

- **维度 9 — README 声明校验**：README 中的数字声明 vs 实际代码/目录数量
- **维度 10 — 设计覆盖检查**：project-graph 的 `design_docs` 字段 vs 实际存在的设计文档
- **--gate flag**：`agentprecept audit --gate` 或 `python scripts/basic-audit.py docs/ --gate`

### project-graph 扩展

- `design_docs` 字段：structure 条目可声明所需的前置设计文档类型
- `sync-graph.py` 支持扫描代码中的 `# design_docs:` 注释标记

### 规则骨

- **checklist 粒度规则**：每项 1-3 commit，架构边界即任务边界（L2_D01 + AGENTS.md + SKILL.md + MEMORY.md 四文件同步）
- **重大设计变更走分支**：MEMORY.md 追加教训 → AGENTS.md 规则层融入
- **反馈提示**：HANDOFF [CLOSING] 时 Agent 自动提示填写反馈模板

### 社区基础设施

- `templates/FEEDBACK.md`：2 分钟反馈模板
- `L2_D01`：重写为九层结构 + 任务拆分粒度 + 强制拦截体系
- `L4_O01`：追加 ADR-008 ~ ADR-014（重命名/init升级/三层拦截/gnhf可选/CI交互/checklist粒度/审计扩展）
- `mcp-tools.md`：追加 design_gate tool 文档

---

## [0.2.1] — 2026-06-08

### 项目重命名：agent-compass → AgentPrecept

- **命名变更**：agent-compass → AgentPrecept（避免与 Future AGI "Agent Compass" 商业产品混淆）
- **Python 模块**：`agent_compass/` → `agentprecept/`，所有 import 路径同步更新
- **CLI 命令**：`agent-compass` → `agentprecept`，`compass-mcp` → `agentprecept-mcp`
- **MCP Server**：注册名 `"agent-compass"` → `"agentprecept"`
- **PyPI 包**：旧 `agent-compass` 包将标记 deprecated，新包 `agentprecept` 发布
- **全局替换**：~86 文件中 ~220 处引用更新（Python/文档/模板/方法论/CI/脚本）
- **README 新增**：名称区分声明块 + 横向定位对比表

### 规则加固

- **重大设计变更走分支**：MEMORY.md 追加教训——涉及架构/重命名/多文件（>10 文件）变更必须在独立分支执行

---

## [0.2.0] — 2026-06-07

### MCP Server 上线

- **MCP Server**：FastMCP 实现，注册 5 个 Tool（project_graph_query / audit_run / sync_diff / decision_search / handoff_read）
- **MCP 自动配置**：首次邂逅检测自动配置 mcp.json（含 cwd + PYTHONIOENCODING Windows 兼容）
- **双向 MCP 检测**：全局 instructions 检测"MCP 可用+项目未 init"→提示初始化；项目 AGENTS 检测"有规则+无 MCP"→提示配置
- **mcp-tools.md**：完整 Tool API 参考文档，CodeWhale 配置示例从 TOML 改为 mcp.json

### MEMORY 机制重新设计

- **自动生长**：MEMORY.md 从静态填空模板改为引导型模板，Agent 在对话中自动追加偏好/约束/教训
- **全局偏好分离**：agentprecept 自身 MEMORY 瘦身为纯项目约束，用户全局偏好移至 CodeWhale note
- **init 脚本升级**：一等公民 4→5（新增 MEMORY.md），init.ps1 和 init.sh 双平台同步

### 项目图补全

- **project-graph relations**：从空列表补全为 14 条边（import/reference/read/write），覆盖 agentprecept/↔scripts/↔docs/
- **structure 修复**：agentprecept/ 去重 + 补 mcp_server.py；新增 scripts/ 包；docs/ 补 mcp-tools.md
- **templates 补文件**：创建 templates/HANDOFF.md 和 templates/L4_O01_design-rationale_设计依据.md（init 脚本引用的空白模板）

### 规则加固

- **"go" 语义钉死**：确认的是上一轮的设计草稿，不是讨论；两步确认不可合并
- **狗粮自检 4 项**：L2_D01 架构 + init 模板完整性 + project-graph relations + 规则一致性
- **审计缓存陷阱**：MCP tool 返回 TOOL_RESULT_REF 必须重新获取实际结果
- **讨论阶段拦截强化**：agentprecept 自身变更不豁免设计先行
- **模板外脑**：Agent 知道 templates/（37 个）和 methodology/（16 篇）按需取用

### 全维度审计

- 8 维自动化审计全 PASS
- 修复 12+ 处过时引用：methodology/ 和根目录文件中 14-dim→8 维自动、audit.py→basic-audit.py、gen-changelog.py→注释化
- INDEX.md 数字修正：14 维审计→8 自动+6 按需、35+→44+ ADR、35→36 模板、15→16 方法论
- methodology/ 和根目录 GitHub 文档全部交叉引用验证

### README 全面同步

- 安装方式双路线（Agent 自动装 / 手动装）
- 数字同步：核心文档 7→8、方法论 15→16、模板 35→36
- 去重 docs/ 目录树行
- 审计描述：14 维中能自动化→8 维自动+6 维按需
- 核心文件表补 mcp-tools.md
- MEMORY 描述加"Agent 自动生长"

---

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