# 架构设计

> 分类: D | 层级: L2 | 编号: L2_D01
> 状态: ✅ 已锁定 | 目标读者: 设计审查
> 最后更新: 2026-06-09

---

## 九层结构

```text
AgentPrecept/
│
├── 规范层: AGENTS.md + SKILL.md         ← Agent 行为规则引擎
│   ├── Auto-Pilot 模式（自动动作 + 降级路径）
│   ├── 设计先行原则（设计→确认→代码）
│   ├── 任务拆分粒度规则（1-3 commit/item）
│   ├── 讨论拦截 + Agent 决策权
│   ├── 首次邂逅检测 + 新项目初始化检测
│   └── 默认行为层（无条件执行）
│
├── CLI + MCP 层 (agentprecept/)          ← 用户和 Agent 的命令入口
│   ├── cli.py              — init(6阶段)/sync/audit(15维)/setup/hooks/gnhf
│   └── mcp_server.py       — MCP Server（6 个 Tool: query/audit/diff/decision/handoff/design_gate）
│
├── 脚本层 (scripts/)                     ← 核心引擎
│   ├── sync-graph.py       — 多语言 6 维扫描 + design_docs 注释
│   ├── basic-audit.py      — 15 维 4-scope 自动化审计（--gate）
│   ├── ripple_check.py     — 涟漪分析（DIRECT/INDIRECT/SAME_PKG）
│   ├── design_gate_check.py— 设计文档前置检查（MCP + hook 共享）
│   ├── graph-to-mermaid.py — YAML → Mermaid 可视化
│   ├── check-naming.py
│   ├── init.ps1 / init.sh  — 项目骨架生成
│   └── README.md
│
├── 方法论层 (methodology/)               ← 给人类和 Agent 的原理文档
│   └── 18 篇 M{1-4}_{A-D}{NN} 体系（四板块：入门/协作/工程/运维）
│
├── 模板层 (templates/)                  ← 可拷贝的文档骨架
│   └── 37 个（16/16 分类全齐），含 INDEX/HANDOFF/AUDIT_REPORT/project-graph/FEEDBACK
│
├── 示例层 (examples/)                   ← 给用户的 onboarding
│
├── 参考层 (reference/)                  ← 证明方法论有效
│
├── 狗粮层 (docs/)                       ← AgentPrecept 自身吃狗粮
│   ├── INDEX.md / project-graph.yaml / HANDOFF.md / MEMORY.md
│   ├── L2_D01（本文件） / L4_O01 / L4_M01 / L1_A01 / mcp-tools.md
│
└── gnhf 桥接层 (agentprecept/gnhf_task.py) ← 外部工具集成（可选）
    └── 生成 .gnhf/sync-task.md 任务模板
```

## 任务拆分与提交粒度

> 实战经验固化。Agent 做任务拆分时，每一项必须精确对应一个 commit。

### 一个 commit = 一个可独立 revert 的变更

正例：
- commit: 添加 User model（1 文件）
- commit: 添加 auth_service 中间件（1 文件）
- commit: 添加 POST /login 端点（2 文件）
→ 每个都可独立 revert

反例：
- commit: 完成用户认证模块（15 文件，无法独立 revert）

### checklist → commit 映射

| checklist 粒度 | 对应 | 判断标准 |
|----------------|------|----------|
| 合理 | 1-3 个 commit | 人类 review ≤ 5 分钟 |
| 太粗 | 5+ 个 commit | 拆成多个 checklist item |

### 架构边界即任务边界

project-graph.yaml 的 structure 中每个模块 = checklist 的天然切割线。
跨模块变更：先稳定接口 → 再各自实现 → `agentprecept audit` 验证。

## 模块依赖

```text
AGENTS.md ────→ agentprecept/cli.py（Agent 执行规则时调用 CLI 命令）
    │
    ├──→ methodology/ → scripts/（方法论引用的脚本）
    ├──→ templates/（Agent 按设计先行原则读取模板并产出）
    └──→ docs/ → scripts/（自身文档调用审计和扫描脚本验证合规）

agentprecept/cli.py  ←→  agentprecept/mcp_server.py  ←→  scripts/
       │                         │
       ├── init: 6 阶段            ├── design_gate tool（Layer 1 软拦截）
       ├── hooks: git hook 安装   ├── audit_run (15 维)
       └── gnhf: 任务模板生成     └── query/diff/decision/handoff 4 个 tool

.git/hooks/pre-commit  ←  init 自动安装（Layer 2）
.github/workflows/agentprecept-gate.yml  ←  init 自动生成（Layer 3）
```

## 数据流

```text
用户项目源码
    │
    │  sync-graph.py（扫描，含 design_docs 注释）
    ▼
project-graph.yaml ←── basic-audit.py（15 维审计，含 --gate 模式）
    │                       │
    ├── Agent 直接读取        ├── 结构化报告
    ├── MCP design_gate ─────┤
    └── CI gate ─────────────┘

gnhf（可选）:
  gnhf_task.py → .gnhf/sync-task.md → gnhf CLI → 夜间自动 sync + audit
```

## 强制拦截三层体系

| 层级 | 触发点 | 机制 | 可否跳过 |
|------|--------|------|:---:|
| Layer 1 | MCP design_gate tool | Agent 主动调用 | ✅（软拦截） |
| Layer 2 | Git pre-commit hook | init 自动安装 | `git commit --no-verify` |
| Layer 3 | CI Pipeline Gate | init 自动生成配置 | ❌（硬拦截） |

## 路线图

### ✅ v0.4.2 — 方法论升级（已完成）
- 全量重命名为 M 体系，18 篇四板块
- 新增 M1_A02 自然语言编程 + M2_B02 非技术审产出
- 5 项深化：生命周期进入退出条件 / 文档先行反模式 / Agent 特有安全 / 已有项目渐进路线 / Agent 自管理自检工具
- AGENTS.md + Hook/CI 检测默认行为
- audit --gate FAIL 0 ✅

### v0.5.0 — Agent 自主生长（MINOR）
- C: 任务级思维框架（AGENTS.md +1 规则）
- A: Git hook 自动记忆生长（memory-grow.py + gnhf 扩展）

### v0.6.0 — 方法论模式（MINOR）
- B: `agentprecept init --mode agile|waterfall`

## 关键设计决策

见 `docs/L4_O01_design-rationale_设计依据.md`（含 Auto-Pilot、设计先行、三层门禁、init 一键接入、gnhf 可选、checklist 粒度、15 维审计等）。