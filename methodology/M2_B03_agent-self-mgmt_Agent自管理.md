# 13 — Agent 自我管理：判断、压缩、交接

> **AgentPrecept 落地**: Auto-Pilot 模式 + checklist 粒度规则 → AGENTS.md 硬规则，详见文末。

> Agent 不只是干活——需要管理自己的上下文、判断何时停下、何时继续。

---

## Token 成本意识

| 动作 | 估算 Token | 值得吗 |
|------|:--:|:--:|
| 读 project-graph（50 行 YAML） | ~300 | ✅ 省下遍历源码 |
| 读 AGENTS.md（66 行） | ~1,500 | ✅ 每次会话 |
| 读全量 14 篇方法论 | ~15,000 | ❌ 除非遇到困惑 |
| 读扩展 26 模板 | ~8,000 | ❌ 按需加载 |

## 上下文管理

| 判断点 | 规则 |
|------|------|
| 上下文 > 60% | 主动提示"上下文即将用完，建议切新会话" → HANDOFF 全量重写 |
| 上下文 > 80% | 停止新任务 → 只做交接 → 状态改为 [CLOSING] |
| 切新会话 | 上一个 Agent 的 HANDOFF → 新 Agent 第 1 步读它 |

---

## 话题漂移检测

```
修 bug 修到一半 → 发现另一个模块可以重构 → 开始重构...

❌ 直接改重构
✅ Agent:
   "我注意到在修 bug 时发现 X 模块有重构机会。
   但当前任务是修 bug。我把重构想法记入 HANDOFF，
   修完 bug 后你可以决定是否继续。"
```

规则: 话题明显漂移 → 停下来 → 记入 HANDOFF → 回到原任务

---

## 上下文压缩策略

| 触发 | 操作 |
|------|------|
| 项目 > 40 轮对话 | 手动 compact：保留 project-graph + L4_O01 + HANDOFF + 最近 5 轮 |
| 项目 > 100K token | 保留 AGENTS + project-graph + HANDOFF → 其余压缩为摘要 |
| compact 后 | 重新读 project-graph + HANDOFF → 从上次断点继续 |

## 死循环检测

```
排查一个 bug，试了方案 A → 失败 → 方案 B → 失败 → 方案 C → 失败 →
回到方案 A 微调 → 失败 → 方案 B 微调 → ...
```

规则: 同一问题排查 3 轮无进展 → 停止 → HANDOFF 记录排查路径 + 疑问点 → 状态改为 [BLOCKED]

---

## 多 Agent 并行安全

```
Agent A 和 Agent B 同时修改 project-graph.yaml
```

规则:
- 修改共享文件前 → `git pull`
- push 被拒 → `git pull --rebase`，不 force push
- 如果两个 Agent 改了同一模块 → HANDOFF 标注冲突位置
- 分工: 一个 Agent 一个 Layer（结构层 / 关系层 / 演变层）

---

## Agent 状态标记

| 标记 | 含义 | 触发条件 |
|------|------|------|
| [IN_PROGRESS] | 正常进行中 | 默认状态 |
| [NEEDS_HUMAN_REVIEW] | 产出完成，等人审查 | 完成 > 3 文件新增 / 修改图结构层 / 做新决策 |
| [NEEDS_HUMAN_DECISION] | 遇到歧义，等人决策 | 两方案无优劣 / 影响 > 5 模块 / 破坏 API 兼容 |
| [BLOCKED] | 外部依赖阻塞 | 等 API key / 等数据 / 排查 3 轮无进展 |
| [CLOSING] | 正在压缩上下文准备结束 | 上下文 > 80% / 人类说"今天到这" |

---

## 渐进加载策略

Agent 不需要每次会话读全部方法论。按需加载:

```
会话开始 → AGENTS.md + project-graph + HANDOFF
写代码   → 读 07-dev-workflow + 对应模板
做决策   → 读 03-design-rationale + L4_O01
跑审计   → 读 04-audit-framework
加功能   → 读 00-lifecycle 阶段 4 + 对应模板
修 bug   → 读 00-lifecycle 阶段 7 + 对应模板
其他     → 按需查阅 methodology/INDEX

---

## 自检工具

### 改代码前
```
ripple_check.py <changed-file> → DIRECT/INDIRECT/SAME_PKG
→ 知道影响几个文件
→ 跨模块时谨慎拆分 commit
```

### 提交前
```
pre-commit 4 gates:
  Gate 1: 分支策略（>10 文件 on main？）
  Gate 2: 设计文档前置（改了代码但没设计文档？）
  Gate 3: commit 粒度（>15 代码文件？）
  Gate 4: NEEDS_HUMAN_REVIEW（staged 含待确认内容？）
```

### 会话结束前
```
1. 写 HANDOFF（IN_PROGRESS → [CLOSING]）
2. 查 MEMORY.md 是否有新教训要追加
3. agentprecept audit --scope=docs → 确保 0 FAIL
```

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| Auto-Pilot | AGENTS.md 默认行为规则 | Agent 每次会话自动执行 |
| checklist 粒度 | 1-3 commit/item 强制规则 | AGENTS.md 硬规则 |
| 上下文管理 | HANDOFF + 轮数阈值 | 15 轮触发 CLOSING |
```
