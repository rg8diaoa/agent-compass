# AGENTS.md — Todo API (Node.js)

## 写代码前：先看三样

| 查什么 | 文件 | 得到什么 |
|---|---|---|
| 项目长什么样 | `docs/project-graph.yaml` | 模块依赖图 |
| 以前怎么决策的 | `docs/L4_O01_design-rationale.md` | 为什么不那样做 |
| 怎么命名 | `docs/L1_A02_naming-convention.md` | 命名格式 |

## 开发流程

```
写代码前：
  1. 读 project-graph.yaml → 影响范围
  2. 读 L4_O01 → 架构约束
  3. 读 L1_A02 → 命名格式

写代码后：
  4. 新建/删模块 → 更新 project-graph.yaml
  5. 新增依赖 → 更新 project-graph.yaml relations
  6. 做新决策 → 追加 L4_O01
```

## 项目图

```yaml
# docs/project-graph.yaml
structure:
  src/routes/:
    type: package
    children: [tasks.js, auth.js]
  src/services/:
    type: package
    children: [taskService.js, authService.js]
  src/models/:
    type: package
    children: [Task.js, User.js]

relations:
  - from: src/routes/tasks.js::createTask
    to: src/services/taskService.js::create
    type: calls
  - from: src/services/authService.js::authenticate
    to: src/models/User.js
    type: calls
  - from: src/routes/tasks.js
    to: src/middleware/auth.js
    type: depends_on

evolution:
  - id: ADR-001
    topic: 三层架构（routes/services/models）
    decision: 三层分离
    date: 2025-01-15
  - id: ADR-002
    topic: JWT vs Session
    decision: JWT（无状态）
    date: 2025-01-20
```

## 命名规范（Node.js）

| 类型 | 规则 | 示例 |
|---|---|---|
| 文件 | kebab-case 或 camelCase | `task-service.js` |
| 类 | PascalCase | `TaskService` |
| 函数 | camelCase | `createTask()` |
| 常量 | UPPER_SNAKE_CASE | `MAX_TASKS` |
