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
| 为什么开发者元信息（HANDOFF/MEMORY/AUDIT_REPORT）不发布 | 发布清洁 | 这些文件是 agent-compass 项目自身的开发过程记录和偏好，用户 clone 后不需要知道"上次修了什么 bug"或"开发者回答风格偏好"。模板（templates/）中已有对应空白副本供用户使用 |
| 为什么加入首次邂逅检测 | 自举体验 | Agent clone agent-compass 后主动三选一（当前项目/全局 Skill/暂不），把安装决策从"需要先读文档"变成"Agent 主动问"。当前项目安装为推荐默认——AGENTS.md 是行业标准，Claude Code/Cursor/CodeWhale/OpenCode/Copilot/Windsurf 全自动读取 |
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
| 为什么需要新项目初始化检测 | 补三选一盲区 | 三选一检测"agent-compass 仓库出现"，但不检测"用户说建新项目"。mindstream 案例：用户说"建一个日记应用"，Agent 直接开始写代码——因为既不是 clone agent-compass，也不是说"安装"。新规则用意图识别替代关键词匹配 |
| 为什么 00-lifecycle 作为入口 | 认知顺序 | 先见森林（循环），再见树木（各阶段细节） |
