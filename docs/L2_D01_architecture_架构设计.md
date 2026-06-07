# 架构设计

> 分类: D | 层级: L2 | 编号: L2_D01
> 状态: ✅ 已锁定 | 目标读者: 设计审查
> 最后更新: 2026-06-07

---

## 八层结构

```
agent-compass/
│
├── 规范层: AGENTS.md + SKILL.md     ← Agent 行为规则引擎
│   ├── Auto-Pilot 模式（自动动作 + 降级路径）
│   ├── 设计先行原则（设计→确认→代码）
│   ├── 讨论拦截 + Agent 决策权
│   ├── 首次邂逅检测 + 新项目初始化检测
│   └── 默认行为层（无条件执行）
│
├── CLI 层 (agent_compass/)           ← 用户和 Agent 的命令入口
│   └── cli.py（init / sync / audit / doctor 四个命令）
│
├── 脚本层 (scripts/)                 ← 核心引擎（CLI 的底层实现）
│   ├── sync-graph.py   — 多语言 5 维扫描 + 盲区检测
│   ├── basic-audit.py  — 8 维自动化审计
│   ├── graph-to-mermaid.py — YAML → Mermaid 可视化
│   ├── check-naming.py — 命名规范校验
│   ├── init.ps1 / init.sh — 项目骨架生成
│   └── README.md
│
├── 方法论层 (methodology/)           ← 给人类和 Agent 的原理文档
│   └── 16 篇：00-lifecycle + 01-14 + 15-agent-ops + INDEX
│
├── 模板层 (templates/)              ← 可拷贝的文档骨架
│   └── 35 个（16/16 分类全齐），含 INDEX/HANDOFF/AUDIT_REPORT/project-graph
│
├── 示例层 (examples/)               ← 给用户的 onboarding
│   └── Python todo-api + Node todo-api + Prompt 模板 + first-run
│
├── 参考层 (reference/)              ← 证明方法论有效
│   └── 审计收敛案例 + 多维图 + 横向对比 + 速查卡片
│
└── 狗粮层 (docs/)                   ← agent-compass 自身吃狗粮
    ├── INDEX.md              — 文档索引
    ├── project-graph.yaml    — 自身项目图
    ├── L2_D01（本文件）       — 架构设计
    ├── L4_O01                — 设计依据（30+ 条决策）
    ├── L4_M01                — 变更日志
    └── L1_A01                — 快速开始
```

## 模块依赖

```
AGENTS.md ────→ agent_compass/cli.py（Agent 执行规则时调用 CLI 命令）
    │
    ├──→ methodology/ → scripts/（方法论引用的脚本）
    │
    ├──→ templates/（Agent 按设计先行原则读取模板并产出）
    │
    └──→ docs/ → scripts/（自身文档调用审计和扫描脚本验证合规）

scripts/sync-graph.py  ←→  scripts/basic-audit.py（sync 后建议跑 audit）
    │                          │
    └──→ docs/project-graph.yaml    ← 输出目标
                               ← 审计输入
```

## 数据流

```
用户项目源码
    │
    │  sync-graph.py（扫描）
    ▼
project-graph.yaml  ←──── basic-audit.py（审计）
    │                       │
    │  Agent 读取             │  结构化报告
    ▼                       ▼
L4_O01 / HANDOFF / MEMORY  docs/ 完整性状态
```

## 关键设计决策

见 `docs/L4_O01_design-rationale_设计依据.md`（30+ 条决策，包含 Auto-Pilot、设计先行、降级路径、符号级 sync、多语言扫描、8 维审计等）。
