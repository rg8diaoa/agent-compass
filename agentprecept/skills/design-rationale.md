# design-rationale skill — 设计依据自动追溯

加载此 skill 后，Agent 在每次做技术决策时自动追加到 L4_O01。

## 自动动作

1. 从 git log 反推决策（`git log --grep="选择\|改用\|why"`）
2. 如 git 不可用 → 检查 CHANGELOG / PR 描述
3. 格式: 决策 | 来源 | 证据

## 触发条件

- 新引入了外部库
- 改变了模块架构
- 修复了系统级 bug

详见 `templates/L4_O01_design-rationale_设计依据.md`。
