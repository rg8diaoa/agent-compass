# 架构设计

> 分类: D | 层级: L2 | 编号: L2_D01
> 状态: ✅ 已锁定 | 目标读者: 设计审查
> 最后更新: 2026-06-10

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
│   ├── cli.py              — init/sync/audit/setup/hooks/gnhf
│   ├── mcp_server.py       — MCP Server（6 Tools）
│   ├── basic_audit.py      — 15 维 4-scope 自动化审计
│   ├── sync_graph.py       — 多语言 6 维扫描
│   ├── design_gate_check.py— 设计文档前置检查
│   ├── ripple_check.py     — 涟漪分析
│   ├── check_naming.py     — 命名规范检查
│   ├── gnhf_task.py        — gnhf 夜间任务模板生成
│   └── graph_to_mermaid.py — YAML → Mermaid
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
    ├──→ methodology/ → agentprecept/（方法论引用的审计/扫描脚本）
    ├──→ templates/（Agent 按设计先行原则读取模板并产出）
    └──→ docs/ → agentprecept/（自身文档调用审计和扫描脚本验证合规）

agentprecept/cli.py  ←→  agentprecept/mcp_server.py  ←→  agentprecept/
       │                         │
       ├── init: 6 阶段            ├── design_gate tool（Layer 1 软拦截）
       ├── hooks: git hook 安装   ├── audit_run (15 维)
       └── gnhf: 任务模板生成     └── query/diff/decision/handoff 4 个 tool

.git/hooks/pre-commit  ←  agentprecept hooks install（Layer 2）
.github/workflows/agentprecept-gate.yml  ←  agentprecept init --ci（Layer 3）
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

完整四模式（lite / normal / pro / max）六阶段发展路线见 **`docs/L1_C01_phased-plan_实施路线.md`**。

概要：

| 版本 | 阶段 | 核心交付 | 新增模式 |
|------|------|----------|:---:|
| v0.5.0 | normal 基础设施 | 模式系统 + 规则硬化 + pre-push hook | normal |
| v0.6.0 | 代理 + 技能 | 代理弹药库 + Skill 系统 | — |
| v0.7.0 | 沉淀与免疫 | compound + diagnose + 反模式库 | — |
| v0.8.0 | pro 模式 | 自检循环 + 宿主 hook + 跨会话债务 | pro |
| v0.9.0 | max 运行时 | serve + ap run + 工作流状态机 | max |
| v1.0.0 | 生产化 | 测试 + 文档 + PyPI 发布 | — |

## 关键设计决策

见 `docs/L4_O01_design-rationale_设计依据.md`（含 Auto-Pilot、设计先行、三层门禁、init 一键接入、gnhf 可选、checklist 粒度、15 维审计等）。