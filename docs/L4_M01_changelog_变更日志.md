# 变更日志

> 分类: M | 层级: L4 | 编号: L4_M01
> 状态: 📝 撰写中 | 目标读者: 维护者

---

## [0.1.0] — 2026-06-06

### 新增

- 完整循环方法论（00-lifecycle）：8 阶段 Agent 工作流
- 11 篇专题方法论 + 人机协作 + 自我管理
- 36 个模板（31 编号 + 5 工具，16/16 分类全齐）
- Prompt 模板集（5 个）+ first-run 初始化工单
- 双语言示例（Python + Node.js）
- 自身完整文档体系（docs/）
- 14 维审计框架
- 仓库自身：project-graph / HANDOFF / 设计依据
- AGENTS.md / SKILL.md 双入口 + 规则分层 + 硬约束
- README 差异化对比表

## [0.2.0] — 2026-06-07

### 规则引擎升级
- Auto-Pilot 模式：降级路径（shell 不可用→手动编辑 YAML）
- 默认行为层：⏳ 待补检测 / 狗粮检查 / 测试追加
- 设计先行原则：讨论阶段拦截 + Agent 决策权划分 + 人类确认信号明确化
- 首次邂逅检测 + 新项目初始化检测（意图识别）
- 命名规范弹性条款 + 人类审 Agent 4 项可验证化
- 防偷懒：git 异常处理（index.lock/分支命名/commit 排查）

### sync-graph.py 四次大修
- 粒度修复 → 符号级解析 → 5 维扫描 → 多语言 + 盲区检测
- JS/TS import 扫描 + 语言分布检测（17 种语言）+ 框架推断（12 种框架）

### basic-audit.py：3 维 → 8 维
- 命名/引用/编号/骨架/图格式/设计追溯/覆盖率/狗粮
- GBK emoji 修复

### init 脚本
- 4 文件 → 7 文件（补 INDEX/命名规范/术语表）
- git init 可选步骤 + AGENTS.md 覆盖保护

### MCP Server + gnhf 集成
- MCP Server：5 tools（query/audit/diff/decision/handoff），FastMCP 一行装饰器
- gnhf 集成：任务模板生成器 + 安全 worktree 外包

### 文档体系
- L2_D01：4 层 → 8 层架构 + 数据流图
- methodology/07-dev-workflow：双分支实验模式
- methodology/15-agent-ops.md：新建 Agent 操作手册
- README：四样 → 五样拿手活 + 不侵入代码声明
- ACKNOWLEDGMENTS：+gnhf 致谢
- L4_O01：累计 44+ 条决策

### MCP Server 上线
- MCP Server 正式可用：5 tools（query/audit/diff/decision/handoff）
- 首次邂逅检测自动配置 mcp.json（含 cwd + PYTHONIOENCODING）
- 双向 MCP 检测：全局 + 项目两个方向互相补全
- mcp-tools.md 完整 API 文档

### MEMORY 机制重新设计
- 自动生长：Agent 自动追加偏好/约束/教训
- 全局与项目分离：agent-compass 自身 MEMORY 瘦身
- init 脚本支持：一等公民 4→5（新增 MEMORY.md），双平台同步

### 项目图补全
- relations：空列表 → 14 条边（import/reference/read/write）
- structure 修复：agent_compass 去重 + scripts/ 新增包

### 规则加固
- go 语义钉死：两步确认不可合并
- 狗粮自检 4 项：架构/模板/图/规则一致性
- 审计缓存陷阱规则
- 讨论阶段 agent-compass 自身不豁免
- 模板外脑规则：Agent 知道按需取用

### 全维度审计
- 8 维自动化全 PASS
- 修复 12+ 处过时引用（methodology/ + 根目录）
- INDEX/README/CHANGELOG 数字全面同步
- 创建缺失模板：templates/HANDOFF.md + L4_O01
- methodology/ 全部交叉引用验证

### 环境部署
- init.ps1/sh 双平台同步 + CodeWhale instructions 同步
