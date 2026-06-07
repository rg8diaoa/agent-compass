# gnhf 集成模板

agent-compass 与 [gnhf](https://github.com/kunchenguid/gnhf) 集成，
让 AI Agent 在安全的 git worktree 中自动维护 `project-graph.yaml`。

## 快速开始

```bash
# 1. 生成 gnhf 任务模板
python agent_compass/gnhf_task.py

# 2. 使用 gnhf 安全执行
gnhf --agent claude \
     --goal .gnhf/sync-task.md \
     --verify "python scripts/basic-audit.py docs/" \
     --max-iterations 1

# 3. 查看结果
git log --oneline -3
cat docs/HANDOFF.md
```

## 工作流

```
gnhf_task.py                    gnhf                        agent-compass
─────────────                   ────                        ─────────────
读取 project-graph 状态    →    创建 worktree
读取 git diff 摘要         →    --goal 传给 Agent       →   运行 sync-graph.py
渲染任务模板               →                             →   运行 basic-audit.py
                            →    --verify 验证            →   exit 0/1
                            →    通过→合并 commit
                            →    失败→丢弃 worktree
```

## gnHF 配置示例

```toml
# .gnhf/config.toml
[project]
name = "my-project"

[agent]
provider = "claude"
model = "claude-sonnet-4-20250514"

[verify]
command = "python scripts/basic-audit.py docs/"
on-failure = "discard"

[runtime]
max-iterations = 3
max-tokens = 100000
```

## 扩展方向

- **git hook 触发**：post-commit hook 中自动运行 `gnhf_task.py` → 检测到变更时提示
- **CI 集成**：PR 流水线中 `gnhf --verify-only` 检查 project-graph 是否过期
- **夜间自动**：cron 定时运行 gnhf，第二天醒来知识库已同步
