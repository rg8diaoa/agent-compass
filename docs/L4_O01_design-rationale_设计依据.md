# 设计依据

> 分类: O | 层级: L4 | 编号: L4_O01
> 状态: 📝 撰写中 | 目标读者: 设计审查

| 决策 | 来源 | 证据 |
|------|:--:|------|
| 为什么用 MIT 许可证 | 开源策略 | 最大化传播——零使用门槛，最广泛的兼容性 |
| 为什么方法论用 00-10 编号而非 L 格式 | 可读性 | methodology/ 是教学材料，需保持线性阅读顺序；L 格式是给项目文档的 |
| 为什么 AGENTS.md 和 SKILL.md 并存 | 工具兼容 | AGENTS.md 覆盖 Claude Code/Cursor/OpenCode/CodeWhale/Copilot；SKILL.md 给支持 Skill 机制的工具一键安装 |
| 为什么模板状态默认 ⏳ 而非 📝 | 设计策略 | 模板是骨架——内容应由用户填入。命名规范/设计依据等通用性极高者设为 📝 |
| 为什么模板文件名必须有中文标题 | 人类可读 | L 格式的 slug 给 Agent grep，中文标题给人类浏览——双重索引 |
| 为什么分类覆盖 16/16 全齐 | 完整性 | 避免用户遇到"分类表有但从没找到模板"的落差 |
| 为什么三层图不是六层图 | 通用性 | 三层覆盖 90% 项目；六层是特定领域扩展（见 reference/） |
| 为什么脚本输出用 ASCII 标记代替 emoji | 跨平台 | Windows GBK 终端不兼容 emoji（UnicodeEncodeError）；[PASS]/[FAIL]/FAIL 在全部终端可正常输出。MEMORY.md 已记录此教训 |
| 为什么引入 Auto-Pilot 模式 | 执行纪律 | AGENTS.md 的"全局自动动作"在 Agent 会话中未被自动触发——Agent 将其当作参考知识而非必须执行的挂钩。Auto-Pilot 声明明确：无人打断时无例外执行，Agent 不得等待提醒或事后补做 |
| 为什么开发者元信息（HANDOFF/MEMORY/AUDIT_REPORT）不发布 | 发布清洁 | 这些文件是 agentprecept 项目自身的开发过程记录和偏好，用户 clone 后不需要知道"上次修了什么 bug"或"开发者回答风格偏好"。模板（templates/）中已有对应空白副本供用户使用 |
| 为什么加入首次邂逅检测 | 自举体验 | Agent clone agentprecept 后主动三选一（当前项目/全局 Skill/暂不），把安装决策从"需要先读文档"变成"Agent 主动问"。当前项目安装为推荐默认——AGENTS.md 是行业标准，Claude Code/Cursor/CodeWhale/OpenCode/Copilot/Windsurf 全自动读取 |
| 为什么模板 project-graph.yaml 初始值用 {} / [] / [] 而非空字段 | 空值安全 | YAML 空字段（`structure:` 后无值）被解析为 None，导致 sync-graph.py 在 `k not in None` 处抛 TypeError。显式写空集合阻断此路径。sync-graph.py 同步加固 `.get("key") or default` |
| 为什么 sync-graph.py 的 relations 保留完整子模块路径 | 粒度正确 | 旧代码 `imp.split(".")[0]` 把 `test_ac.services` 砍成 `test_ac`——5 条模块间依赖全部丢失。修复后 `to` 保留原文，`from` 和 `to` 精确到子模块 |
| 为什么标准库排除列表用集合而非列表 | 可维护性 | 提取为 `STDLIB_ROOTS` 模块级常量，扩展时只加一行。覆盖了 dataclasses/enum/abc 等旧代码遗漏的标准库 |
| 为什么 relations 全量替换而非追加 | 清洁性 | 旧代码"只追加不清洗"导致历史错误关系永久残留。代码 import 是唯一真实来源——每次 sync 直接覆盖 |
| 为什么 relations 精确到符号级（from X import Y → X.Y） | 信息密度 | 模块级 `services.py → test_ac.models` 只知道"依赖 models"。符号级 `services.py → test_ac.models.Task` 知道"依赖 Task 这个类"——改一个类就知道影响范围。实现：正则在 `import` 后捕获逗号分隔的符号名 |
| 为什么 init 脚本必须产出 7 个文件而非 4 个 | 一等公民完整性 | 旧 init.ps1/sh 只复制 AGENTS.md + project-graph + HANDOFF + L4_O01，遗漏 INDEX.md + 命名规范 + 术语表——导致初始化后的项目缺少一等公民文档。修复后产出 7 文件：4 一等公民 + 3 核心支撑 |
| 为什么加入设计先行原则 | 工程质量 | Agent 容易跳过设计直接写代码（test-ac 即为案例——sync 后直接编码，架构和接口全在脑子里未落文档）。原则强制"设计文档 → 人类确认 → 写代码"的顺序，覆盖 L2_D01/L2_F07/L2_G01/L2_G03/L4_O01 五种前置设计 |
| 为什么 Auto-Pilot 需要降级路径 | 跨平台可靠性 | 声明式规则假设 CLI/shell 始终可用——但 Plan 模式禁 shell、非 Python 环境无 CLI。降级路径（手动编辑 project-graph、对照 memory 中的方法论）确保规则在任何 Agent 环境下不落空 |
| 为什么用可检测信号替代模糊触发 | Agent 可观测性 | "会话即将结束""上下文>60%"对 Agent 不可观测。改为显式信号（用户说关键词、轮数>15、checklist 完成+2轮无任务）让 Agent 能自主判断 |
| 为什么划分默认行为层 | 执行完整性 | 有些规则不需要触发条件（测试追加、文档自检），但当前建模为触发型。默认行为层覆盖"每次会话都该做的事"，不依赖特定事件 |
| 为什么人类确认需要明确信号约定 | 防止跳过确认 | EXPLORE 下"可简化"被 Agent 理解为连确认都可以跳。明确信号列表（"确认/可以/go/OK/开始"）+ 确认前禁止 write_file/edit_file/commit——堵住逃逸口 |
| 为什么需要新项目初始化检测 | 补三选一盲区 | 三选一检测"agentprecept 仓库出现"，但不检测"用户说建新项目"。mindstream 案例：用户说"建一个日记应用"，Agent 直接开始写代码——因为既不是 clone agentprecept，也不是说"安装"。新规则用意图识别替代关键词匹配 |
| 为什么需要讨论阶段拦截 | 防止跳跃设计 | Agent 在讨论新功能时容易直接开始写代码（"好的，加一下"），跳过方案对齐。讨论→方案要点→确认的拦截层确保方向对再动手 |
| 为什么需要 Agent 决策权划分 | 减少无效追问 | 没有决策权划分时 Agent 要么事事都问（烦），要么事事不问（危险）。必须问的（选型/UX/外部信息）vs 自己拍的（命名/结构/日志）明确边界 |
| 为什么 basic-audit 扩展到 8 维 | 审计覆盖面 | 方法论定义 14 维，原脚本只跑了 3 维。扩展到编号连续性/骨架⏳残留/图格式/设计追溯/狗粮审计/覆盖率共 8 维自动化——术语/内容/体验/定位/社区维需人工审计 |
| 为什么 sync-graph.py 扩展到多语言 + 盲区检测 | 通用性 | 原只扫 Python import。新增 JS/TS import 扫描、语言分布检测、框架推断、盲区报告——让 Agent 知道哪些语言/框架有扫描器覆盖、哪些需要手动维护。参考 CodeToFlow 的语言驱动思路 |
| 为什么命名规范允许弹性偏离 | 规范服务项目 | 世界模拟器 _V2 后缀与纯编号命名共存——多版本场景下版本标识比格式一致性更有信息量。偏离时在 HANDOFF 标注，audit 报 FAIL 为预期行为 |
| 为什么需要 Agent 操作手册 | 操作知识沉淀 | 子代理超时、git 锁、Windows 分支命名、GBK 编码——这些都是实战踩坑但 agentprecept 没有文档化的 Agent 操作经验。新设 methodology/15-agent-ops.md |
| 为什么 README 声明外挂层不侵入 | 降低集成门槛 | 世界模拟器集成验证了 agentprecept 的最大优势——全部新增在 docs/ 层，零代码侵入。这是区别于其他框架的核心卖点 |
| 为什么用 gnhf 替代自建 worktree | 不重复造轮子 | gnhf 已解决 git worktree 隔离 + 原子提交 + agent 后端兼容的全部工程细节（1900+ stars）。agentprecept 只需生成 gnhf --goal 模板，安全执行层完全外包 |
| 为什么 tests/ 暂不建 | 当前阶段偏差 | agentprecept 是方法论仓库——核心产出是文档和规则，不是运行时服务。sync/audit 脚本已有 mindstream 和 test-ac 两个真实项目验证。正式测试在 PyPI 发布前补 |
| 为什么加 compass setup 命令 | 零配置体验 | 当前用户 pip install 后需手动 init+配 MCP+跑 doctor——三步断裂。setup 一键完成所有，输出可直接粘贴的 MCP 配置 JSON |
| 为什么首次邂逅要自动配 MCP | 全自动闭环 | 用户发 GitHub 链接→Agent 三选一→安装完后自动检测当前工具(CodeWhale/Claude/Cursor)→创建或追加 MCP 配置文件。用户从发链接到全部可用只需选一个字母 |
| 为什么 L2_D01 必须反映当前架构 | 狗粮自指 | 本次架构变更方案中 Agent 跳过了更新 L2_D01——因为 L2_D01 本身已过时（只画了 4 层，实际 8 层）。修复：L2_D01 重写为当前全貌 + 设计先行表加自指规则 + 默认行为层加狗粮检查 |
| 为什么用 MCP Server 暴露 agentprecept 功能 | Code Agent 原生集成 | 当前 Agent 靠读 YAML/MD 文件获取项目知识，MCP Server 把 sync/audit/query/decision/handoff 变为结构化 API——Agent 通过 MCP 协议直接调用，不需遍历文件系统。FastMCP 一行装饰器暴露现有函数 |
| 为什么 MCP Server 需要 PYTHONIOENCODING=utf-8 | Windows 兼容 | MCP Server 在 CodeWhale 中 5 个 tool 全部未注册。诊断排除 Python/fastmcp/包/配置后，发现 mcp-stderr.log 为非 UTF-8 编码。Windows GBK 终端下 Python stderr 输出中文导致 MCP 握手消息损坏→Server 注册失败。修复：mcp.json 中 agentprecept 条目加 env.PYTHONIOENCODING=utf-8 + env.PYTHONUTF8=1；备选方案 cmd 包装 + 完整路径 |
| 为什么 mcp-tools.md 需要重构而非自动修复 | 编码修复 | 原始文件 UTF-16-LE 编码（无 BOM），Git 提交时已损坏——字节中多处 3f（ASCII ?）替代了合法 UTF-8 续字节，无法自动恢复。基于 Git 可见内容重构全文为 UTF-8，audit_run 恢复为 8 维全 PASS。教训：agentprecept 自身文档必须用 UTF-8 保存，basic-audit.py 未做编码容错 |
| 为什么 mcp-tools.md 的 CodeWhale 配置段使用 mcp.json 而非 TOML | 配置正确性 | 原文档用了 `[mcp_servers]` TOML 格式，但 CodeWhale 实际读取 `~/.deepseek/mcp.json`（JSON 格式）。错误的配置示例会误导用户。修正为正确的 mcp.json 格式 + 补充 `cwd`/`env`/`PYTHONIOENCODING` 的 Windows 注意事项 |
| 为什么 MCP Resources 暂不实现 | 兼容性优先 | agentprecept 宣称支持 Claude Code/Cursor/CodeWhale/OpenCode/Copilot/Windsurf。MCP Tools 是所有工具的最大公约数（全支持），Resources 仅 Claude/CodeWhale 明确支持。加 Resource 时保留 Tool 作为 fallback——计划未来版本实现 |
| 为什么 L2_D01 要加入 MCP Server 层 | 狗粮自指 | 本次会话修改 mcp-tools.md 后触发了狗粮检查——L2_D01 的 CLI 层描述只有 cli.py 四命令，遗漏了 mcp_server.py 和 5 个 MCP tools。修正：CLI 层 → CLI+MCP 层，数据流加入 MCP 通道 |
| 为什么 MEMORY.md 要从填空模板改为自动生长 | 记忆机制 | 旧 MEMORY.md 是静态填空模板，依赖用户手动维护；同时 agentprecept 自身 MEMORY.md 混了全局偏好（"回复风格"等）和项目约束。设计：agentprecept 自身 MEMORY 瘦身为纯项目级；templates/MEMORY.md 改为引导型模板（含 Agent 注释），配合 AGENTS.md 自动生长规则；init 脚本补复制 MEMORY.md（5/5 一等公民）。用户全局偏好移至 CodeWhale note |
| 为什么需要双向 MCP 发现检测 | 安装闭环 | 全局 instructions 检测到"MCP 可用 + 项目未 init"→ 提示 init；项目 AGENTS.md 检测到"有 AGENTS.md + 无 MCP"→ 提示配置 MCP。两者对称，确保无论从哪条路径进入，缺失的部分都会被提醒补全 |
| 为什么 init 脚本要从 4 一等公民扩展到 5 | 记忆就绪 | 新增 MEMORY.md 为一等公民。之前只有 INDEX/命名规范/术语表/HANDOFF，缺少 MEMORY 导致新项目无法使用自动生长机制。init.ps1 和 init.sh 同步更新 |
| 为什么从 agent-compass 改名为 AgentPrecept | 品牌区分 | 外部评价指出搜索 "Agent Compass" 70% 指向 Future AGI 商业产品。precept（戒律）比 compass（指南针）更精确覆盖"设计先行+强制拦截"。多候选池对比（AION/Stela/Knot/Herm/DevCompass）后选 AgentPrecept，基于小白+Agent 双群体口述传播测试 |
| 为什么 init 从文档复制器升级为能力接入器 | 一键接入 | 当前 init 只复制文件，用户需手动 git init/配 MCP/装 hook/配 CI——每一步都是流失点。改为 6 阶段自动检测+配置 |
| 为什么强制拦截分三层而非一层 | 可达节点 | AgentPrecept 无法拦截 Agent 工具的 write_file 操作。三层分别在可达节点插入：MCP tool 调用（软）、git commit（硬可跳过）、CI PR merge（硬不可跳过） |
| 为什么 gnhf 作为可选阶段而非强制 | 外部依赖 | gnhf 是外部工具（git worktree 沙盒），不是 AgentPrecept 的运行时依赖。不捆绑不 vendoring，init 检测后询问 |
| 为什么 CI Gate 询问用户而非自动追加 | 已有配置保护 | 项目可能已有复杂 CI 配置，自动追加可能破坏已有配置。init 检测后展示 Gate 说明并询问 |
| 为什么 checklist 项必须对齐 commit 粒度 | 实战教训 | 粗粒度 checklist（"完成用户认证模块"）导致 item 停留过久，commit 过大不可独立 revert。标准：1-3 commit/item |
| 为什么审计从 8 维扩展为 10 维 | 狗粮升级 | 外部评价指出"README 宣称与实现之间有落差"。新增维度 9（README 声明校验）+ 维度 10（设计覆盖检查） |
| 为什么分支检查要有工程化保障 | 规则空洞 | MEMORY.md 记录了"重大变更走分支"但 pre-commit hook 不检查。升级 hook 追加 Gate 1（>10 文件 on main → 阻止）+ CI 侧新增维度 11（分支策略检查）。规则不能只靠 Agent 自觉 |
| 为什么 commit 粒度和 NEEDS_HUMAN_REVIEW 要进 hook | 最后两道防线 | 单 commit >15 代码文件（Gate 3）+ staged 含 NEEDS_HUMAN_REVIEW（Gate 4）——这两项在 hook 层可自动化检测。CI 侧维度 12 补冗余告警。语义判断（"真的需要 15 文件一起改？"）仍是 Agent 自觉，但极端异常已被拦截 |
