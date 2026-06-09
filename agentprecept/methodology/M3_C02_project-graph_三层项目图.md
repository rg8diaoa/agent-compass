# 06 — 三层项目图：Agent 的认知模型

> **AgentPrecept 落地**: `project-graph.yaml` + `agentprecept sync` + `project_graph_query` MCP tool + 审计维度 5/10，详见文末。

> 文档是地图。图是 Agent 理解项目"长什么样"的方式。

---

## 为什么需要图

文件系统是扁平的。`src/models/user.py` 和 `src/services/auth.py` 在磁盘上相邻，但它们之间的关系——谁依赖谁、谁调用谁、谁引用了同一个概念——对 Agent 完全不可见。

图把不可见的关系变成可查询的结构。

---

## 三层图模型

```

                    ┌──────────────┐
                    │  演变层 (E)   │  ← 历史：谁在什么时候做了什么
                    │  Evolution   │
                    └──────┬───────┘
                           │ 随时间展开
                    ┌──────┴───────┐
                    │  关系层 (R)   │  ← 联系：谁依赖谁、谁引用谁
                    │  Relation    │
                    └──────┬───────┘
                           │ 连接
                    ┌──────┴───────┐
                    │  结构层 (S)   │  ← 骨架：有什么、在哪里
                    │  Structure   │
                    └──────────────┘
```

---

## 代码项目映射（优先场景）

用于后端服务、前端应用、CLI 工具、微服务、库等。

| 层 | 节点类型 | 边类型 |
|---|---|---|
| **结构层 S** | 包→模块→类→函数 | 包含关系 |
| **关系层 R** | 模块、接口、数据模型、配置、issue | 导入、调用、继承、依赖、关联 issue |
| **演变层 E** | commit、PR、ADR、发布版本 | 修改来源、决策依据、版本标记 |

**示例**（一个 API 服务）：

```
S: src/ → auth/ → login.py → authenticate()
R: authenticate() → 调用 → UserModel.find_by_email()
    UserModel → 被引用 → login.py / register.py / admin.py
    模块 auth/ → 依赖 → 模块 crypto/（哈希库）
E: authenticate() 最后修改 → commit a3f2b1 → "修复 token 过期判断"
    ADR-003：为什么用 JWT 而不是 session → 设计依据链接
```

Agent 要改 `authenticate()` 时，从图中查询：谁调用它？哪些模型会被影响？上次改是什么原因？

---

## 文档/知识库项目映射

用于技术文档、内部 wiki、课程体系、知识管理平台等。

| 层 | 节点类型 | 边类型 |
|---|---|---|
| **结构层 S** | 目录→文档→段落 | 包含关系 |
| **关系层 R** | 术语、引用、示例、外部资源 | 引用、示例关联、版本对照、外部链接 |
| **演变层 E** | 修订、翻译、归档版本 | 修订来源、翻译映射 |

**示例**（一份技术文档库）：

```
S: docs/ → api/ → auth.md → "获取 token" 段落
R: "认证令牌" 术语 → 被引用于 auth.md / sdk.md / faq.md
    auth.md 代码示例 → 引用 repos/todo-api/src/auth/
E: auth.md 修订于 2025-03 → 原因：API v2 升级
```

Agent 要改 `auth.md` 中关于 token 的描述时，从图中查询：哪些文档引用了"认证令牌"这个术语？修改会波及多少地方？

---

## 项目管理映射

用于需求文档、设计文档、项目计划、团队协作场景。

| 层 | 节点类型 | 边类型 |
|---|---|---|
| **结构层 S** | 项目→里程碑→任务 | 包含关系 |
| **关系层 R** | 任务、负责人、文档、决策 | 分配、依赖、阻塞、引用 |
| **演变层 E** | 周报、复盘、决策记录、变更请求 | 状态变更、决策来源 |

---

## 如何构建项目图

不是手动画。是让 Agent 在项目文档体系中维护一个 `project-graph.yaml`：

```yaml
# 代码项目 project-graph.yaml 示例
structure:
  src/auth/:
    type: package
    children: [login.py, middleware.py, permissions.py]
  src/models/:
    type: package
    children: [user.py, session.py, task.py]

relations:
  - from: src/auth/login.py::authenticate
    to: src/models/user.py::UserModel
    type: calls
  - from: src/auth/login.py
    to: src/lib/crypto.py
    type: depends_on
  - from: src/models/user.py
    to: src/schemas/user.py
    type: validates_against

evolution:
  - id: ADR-003
    topic: 认证方案选择（JWT vs Session）
    decision: JWT
    date: 2025-02-10
    rationale_ref: docs/L4_O01_design-rationale_设计依据.md#auth-jwt
  - id: COMMIT-a3f2b1
    topic: 修复 token 过期判断
    affected: [src/auth/login.py::refresh_token]
    date: 2025-03-01
```

这份 YAML 是 Agent 可以查询和更新的数据结构。不需要完整——从核心模块开始，按需扩展。

---

## 图不是替代文档

| | 文档 | 图 |
|---|---|---|
| **读什么** | 行为、设计、原因 | 关系、影响面、结构 |
| **怎么问** | "权限系统怎么设计？" | "改 UserModel 会影响哪些文件？" |
| **谁维护** | 人类 + Agent | Agent 从代码中推导 |

文档描述**意图**。图描述**结构**。两者互补。

---

## 渐进原则

不需要一开始就构建完整图。三层从简到繁：

1. **结构层**（最小）——先有骨架。一个项目有哪些目录、哪些主要模块
2. **关系层**（需要时）——当 Agent 不确定"改了这里会影响哪里"时开始建立
3. **演变层**（有历史时）——当项目积累了 ADR 和重要 commit 后填充

---

## 一句话

**Agent 不会在文件系统里迷路——它会在关系里迷路。图是 Agent 的关系地图。**

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| 三层模型 | `project-graph.yaml` structure/relations/evolution | `agentprecept sync` 自动扫描 |
| 图查询 | `project_graph_query` MCP tool | `project_graph_query(module)` |
| 图审计 | 审计维度 5（格式）+ 维度 10（覆盖） | `agentprecept audit --gate` |
