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
| 为什么 00-lifecycle 作为入口 | 认知顺序 | 先见森林（循环），再见树木（各阶段细节） |
