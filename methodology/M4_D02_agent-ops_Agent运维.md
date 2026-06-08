# Agent 操作实战

> **AgentPrecept 落地**: gnhf 夜间同步 + git hook 四门拦截 + MEMORY 自动生长，详见文末。

> 编号: 15 | 层级: 操作手册 | 读者: Agent
> 状态: 📝 撰写中

Agent 在不同环境中执行任务时积累的操作经验。每条来自实战踩坑。

---

## 文件操作

### 批量文件创建

当需要创建超过 15 个文件时，分批交给子代理并行处理：
- 单个子代理会话 ≤ 15 个文件
- write_file 审批超时设 180 秒
- 总文件数 30+ 时分 2 批，每批 2-3 个子代理并行

依据：世界模拟器 37 文件迁移时，单子代理 230+ 秒超时；15 文件批在 180 秒安全线内。

### 只加不改原则

集成 agentprecept 或做架构迁移时，优先"新增 docs/ 层"而非修改现有 .py/.yaml。不碰代码降低风险，文档独立于逻辑。

---

## Git 操作

### index.lock 残留

```
fatal: Unable to create '.git/index.lock': File exists.
```
→ Windows: `del /f .git\index.lock`
→ Linux/macOS: `rm .git/index.lock`
→ 不要在 .git 目录外执行 git 命令

### Windows 分支命名

分支名避免含 `/`（如 `exp/compass-B`）。Windows 上 git 可能无法写入含斜杠的 reflog 文件。用 `exp-compass-B` 替代。

### commit 失败排查

1. `git status` 检查是否本地有未追踪冲突文件
2. `git log --oneline -3` 检查是否有相同提交已存在
3. 远程更新冲突 → `git pull --rebase` 然后重新 push

---

## 审计脚本

### GBK 编码问题

Windows PowerShell 终端 GBK 编码不兼容 emoji（✅❌⏳🔴）。所有脚本输出使用 ASCII 标记：`[PASS]` `[FAIL]` `[WARN]`。

### 子代理 vs 本地审计

- docs/ ≤ 10 文件 → 直接跑 basic-audit.py
- docs/ > 10 文件 → 子代理跑 basic-audit.py，结果回传

---

## 跨工具兼容

### run_verifiers 替代 exec_shell

当 CodeWhale 的 exec_shell 不可用时，`run_verifiers` 的 custom commands 可执行 shell 命令。缺点：stdout 不直接显示，需靠 exit code + 重定向到文件判断结果。

### CodeWhale Plan 模式

Plan 模式禁写。此时用 `update_plan` 输出完整变更方案，等用户切到 Agent/YOLO 模式再执行。

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| gnhf 夜间同步 | `agentprecept gnhf setup` | 可选，需 gnhf CLI |
| git hook 四门 | pre-commit 分支/文档/粒度/确认 | `agentprecept init` 自动安装 |
| MEMORY 自动生长 | AGENTS.md 规则 + 会话结束时追加 | Agent 自动执行 |
