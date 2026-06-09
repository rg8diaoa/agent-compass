# session-handoff skill — 会话交接自动化

加载此 skill 后，Agent 在每次会话结束时全量重写 HANDOFF。

## 自动动作

1. `git diff --stat origin/main..HEAD` → 代码变更
2. `git log --since="上次更新" --oneline` → 本会话内容
3. 评估上下文用量
4. 更新状态标记

## 状态标记

[IN_PROGRESS] / [NEEDS_HUMAN_REVIEW] / [NEEDS_HUMAN_DECISION] / [BLOCKED] / [CLOSING]

详见 `templates/HANDOFF.md` 的 AGENT 指令区。
