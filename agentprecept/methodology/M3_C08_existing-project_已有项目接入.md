# 11 — 已有项目接入：不从头开始

> **AgentPrecept 落地**: `agentprecept init` 支持已有项目渐进接入，详见文末。

> agentprecept 不要求你从零建文档体系。可以在已有项目上渐进接入。

---

## 不要一次全搬

最常犯的错误：clone agentprecept 后把 templates/ 全复制到项目里，然后看着 22 个 ⏳ 模板不知道从哪开始。

**正确做法**：只搬你当前需要的，按需扩展。

---

## 接入路线图

### 第 1 天：Agent 知道怎么干活（5 分钟）

1. 复制 `AGENTS.md` 到项目根目录
2. 修改 AGENTS.md 中的文件路径：如果你的项目文档在 `docs/`，保持不变；如果在别处，调整路径

Agent 读到 AGENTS.md 后，会自动在写代码前查 project-graph + 设计依据 + 命名规范。

### 第 1 周：建图（15 分钟）

1. 从 `templates/project-graph.yaml` 复制骨架到 `docs/project-graph.yaml`
2. 用以下 prompt 让 Agent 帮你填充：

```
读取 src/ 目录结构，按 agentprecept 的三层图格式填充 docs/project-graph.yaml 的结构层。只列主要模块（不大于 10 个包），不要列到函数级别。
```

3. 让 Agent 补充关系层：

```
读取 src/ 中所有 import 语句，补充 project-graph.yaml 的关系层。格式：from → to → type（calls/depends_on/tests）。
```

### 第 2 周：建设计依据（10 分钟）

1. 复制 `templates/L4_O01_design-rationale_设计依据.md` 到 `docs/`
2. 用以下 prompt：

```
回顾最近 3 个月的技术决策（从 git log 和 PR 讨论中提取），补充到 docs/L4_O01 中。格式：决策 | 来源 | 证据。至少 5 条。
```

### 第 3 周：建命名规范和术语表（10 分钟）

1. 复制模板到 docs/
2. 让 Agent 扫描已有代码提取命名规律：

```
扫描 src/ 中的文件名、类名、函数名，总结当前的命名规律，填入 L1_A02 命名规范。如果发现不一致的地方，标注出来。
```

### 之后：按需扩展

当以下情况发生时，追加对应模板：
- 新增了外部服务集成 → L3_H01
- 团队增加了前端开发者 → L3_I01
- 准备上线 → L3_P01 + 阶段 8 发布流程
- 做了大重构 → L4_N01

---

## 接入检查清单

```
□ 第 1 天：AGENTS.md 已放到项目根目录
□ 第 1 周：project-graph.yaml 结构与实际代码一致（用 Agent 生成，人工验证）
□ 第 2 周：L4_O01 有至少 5 条历史决策记录
□ 第 3 周：L1_A02 + L1_B01 到位，无命名/术语冲突
□ 按需：H/I/J/K/L/M/N/P 模板在需要时追加
```

---

## 常见坑

| 坑 | 避免方法 |
|------|------|
| 一次搬太多模板，看不过来 | 只搬 AGENTS.md + project-graph + L4_O01 三样，之后按需 |
| project-graph 太大（200+ 行） | 控制在 50 行以内——只列主要模块和关键依赖 |
| Agent 生成的命名规范与实际不一致 | 人工审查后锁定为 ✅ |
| 设计依据空白 | 从最近的 git log 和 PR 描述中反推 |

---

## 渐进路线图

### 第一天（30 分钟）
- 复制 AGENTS.md 到项目根 → Agent 获得设计先行规则
- 复制 templates/project-graph.yaml 模板
- 手动填充结构层（只列主要模块，3-5 个即可）

### 第一周（半天）
- 运行 agentprecept sync → 自动完善 project-graph
- 创建 docs/HANDOFF.md → 第一次交接
- 安装 pre-commit hook → agentprecept hooks install
- 跑 agentprecept audit --scope=docs → 看文档层差距

### 第一个月
- 全量 15 维审计 → agentprecept audit --gate
- CI gate 接入 → .github/workflows/agentprecept-gate.yml
- 团队习惯固化：每次会话结束写 HANDOFF，每次决策追 L4_O01

### 反模式
| 做法 | 问题 |
|------|------|
| 一次性全部文档就位 | 1 周后全部过时，没人维护 |
| 跳过 project-graph | 没有图就没有涟漪分析、没有审计 |
| 只装 hook 不装 CI | hook 可 --no-verify 跳过，CI 才是硬拦截 |

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| 渐进接入 | `agentprecept init` 已有项目安全初始化 | `agentprecept init /project` |
| 最小接入 | 只需 AGENTS.md + project-graph + L4_O01 | `agentprecept init` 自动生成 |
