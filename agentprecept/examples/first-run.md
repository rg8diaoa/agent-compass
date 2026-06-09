# agentprecept 初始化向导

> 复制下面这段 prompt 发给 Agent，Agent 会自动走完初始化 6 阶段。

---

```
我正在用 agentprecept 方法论初始化这个项目。

请按以下步骤执行：

## 第 1 步：生成项目图
读 templates/project-graph.yaml 中的 AGENT 指令，用 tree + grep 生成初始版本。

## 第 2 步：反推设计依据
读 templates/L4_O01_design-rationale_设计依据.md 中的 AGENT 指令，从 git log 反推设计决策。

## 第 3 步：生成架构图
读 templates/L2_D01_architecture_架构设计.md 中的 AGENT 指令，从 project-graph 生成 ASCII 架构图。

## 第 4 步：检查术语表
读 templates/L1_B01_glossary_术语表.md。扫描代码中的术语，如有新术语则补充。

每步输出完成后告诉我进度，进行下一步。
```

---

## 人类评判 Agent 产出（4 项及格线）

```
Agent 提交了架构设计 → 你对照:
  □ 模块划分表有 > 3 个模块
  □ 每个模块有 1 行职责描述
  □ L4_O01 中有对应的技术选型依据
  □ project-graph 已经更新

4 项全 □ → 及格。少 1 项 → 告诉 Agent "补一下 X"
```


---

## 如果你已经有 project-graph（非首次）

```
读 docs/project-graph.yaml → 告诉我当前结构
读 docs/HANDOFF.md → 告诉我上次做到哪了
告诉我下一步应该做什么
```

---

## 快速修复：Agent 改代码前查影响范围

```
读 docs/project-graph.yaml 的 relations 层
告诉我 [你要改的模块] 被哪些模块依赖
```
