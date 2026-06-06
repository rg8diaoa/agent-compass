# AGENTS.md — agent-compass

> 复制到项目根目录。Agent 每次会话自动读取。

## 会话启动（50 秒）

1. 读 `docs/project-graph.yaml` → 项目结构
2. 读 `docs/HANDOFF.md` → 做到哪了
3. 读 `docs/MEMORY.md` → 人类偏好

## 工作模式

- [EXPLORE] 默认：直接出 MVP，标注假设。明显歧义才问。适用于快速原型
- [PRECISE] 用户说"精确模式"/"重构"/"修 bug"→ 严格遵循硬规则。适用于生产级变动

## 目标驱动执行（Karpathy 原则）

```
不是 "加验证"     → "写测试覆盖非法输入，然后让它们通过"
不是 "修复 bug"   → "写测试复现 → 测试通过 → 修复完成"
每个任务 = 可验证目标 + 验证方法。循环直到验证通过。
```

## 防偷懒（Anti-Laziness）

- 审计时：必须实际运行 `agent-compass audit`。不许凭记忆说"之前确认过"
- 验证时：必须读回写入的文件内容。不许假设"写成功了"
- 跨文件引用时：必须 `grep` 验证路径存在。不许凭记忆说"应该有"
- 工具失败时：报告中标注 [无法验证]。不许跳过也不许造假

## 全局自动动作

| 触发 | 动作 |
|------|------|
| 每次代码变更 | `agent-compass sync`（更新 project-graph） |
| 做了设计决策 | 追加 L4_O01：决策 / 来源 / 证据 |
| 会话结束 | 全量重写 HANDOFF（状态+上下文+下一步） |
| 提交前 | 对照 14-production-readiness 退出标准 |
| 上下文 > 60% | HANDOFF 加 [CLOSING]，提醒切新会话 |
| 同一问题 3 轮无进展 | 停 → HANDOFF [BLOCKED] |

## 用户口头禅映射

| 用户说 | Agent 加载 |
|------|------|
| "初始化"/"init" | examples/first-run.md |
| "加功能"/"新端点" | L2_D01 + L3_J02 |
| "修 bug"/"fix" | 00-lifecycle §阶段7 + L3_J02 |
| "审计"/"audit" | methodology/04 + `agent-compass audit` |
| "发布"/"release" | 14-production-readiness §阶段8 |
| "交接"/"handoff" | 重写 docs/HANDOFF |

## 核心模板（Agent 主动加载）

| 模板 | 触发条件 |
|------|------|
| project-graph.yaml | 每次代码变更 |
| L4_O01 设计依据 | 做技术决策时 |
| HANDOFF | 会话结束 |
| L3_J02 测试用例 | 新增 API 端点 |
| L2_D01 架构设计 | 项目初始化 / 架构变更 |

## 人类审 Agent（4 项及格线）

□ 模块 > 3 □ 有职责描述 □ L4_O01 有依据 □ 图已更新

## 状态标记

[IN_PROGRESS] / [NEEDS_HUMAN_REVIEW] / [NEEDS_HUMAN_DECISION] / [BLOCKED] / [CLOSING]

## 完整方法论

速查卡: `reference/cheatsheet.md` | 方法论导航: `methodology/INDEX.md`
