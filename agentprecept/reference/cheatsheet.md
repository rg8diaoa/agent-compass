# AgentPrecept 速查卡片

> Agent 和人类共享的单页参考。

## Agent 每次会话（50 秒）

1. 读 project-graph → 项目结构
2. 读 HANDOFF → 做到哪了
3. 读 MEMORY → 人类偏好

## Agent 写代码前

- 涉及 > 2 文件 → 先列影响范围
- 涉及 stability:critical → 先列影响 + 等确认
- 不确定 → "我理解的是 X，对吗？"（不许猜）

## Agent 写代码后

- `agentprecept sync` — 同步 project-graph
- 追加 L4_O01 — 决策 / 来源 / 证据
- 更新 HANDOFF — 状态 / 上下文 / 下一步

## 目标驱动执行

```
不是 "加验证"                  → "写测试覆盖非法输入，然后让它们通过"
不是 "修复 bug"                → "写测试复现 → 测试通过 → 修复完成"
每个任务 = 可验证目标 + 验证方法
```

## 人类审 Agent（4 项及格线）

□ 模块 > 3 □ 有职责描述 □ L4_O01 有依据 □ 图已更新

## 常用命令

```
agentprecept init     # 初始化项目
agentprecept sync     # 同步 project-graph
agentprecept audit    # 快速审计
agentprecept doctor   # 检查缺什么
```

## 状态标记

[IN_PROGRESS] / [NEEDS_HUMAN_REVIEW] / [NEEDS_HUMAN_DECISION] / [BLOCKED] / [CLOSING]
