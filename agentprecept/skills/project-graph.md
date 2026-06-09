# project-graph skill — Agent 项目图自动维护

加载此 skill 后，Agent 在每次代码变更时自动同步 project-graph.yaml。

## 自动动作

1. `agentprecept sync` 或 `python -m agentprecept.sync_graph src/ docs/project-graph.yaml`
2. stability 字段默认 stable（标记"Agent 自动推断"）
3. 如检测到认证/核心逻辑模块 → stability=critical

## 手动初始化

```bash
agentprecept sync
```

## 输出规范

见 `templates/project-graph.yaml` 的 AGENT 注释区。
