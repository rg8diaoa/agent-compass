# API 版本管理规范

> 分类: G | 层级: L2 | 编号: L2_G02
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_D01_architecture_架构设计.md

---

## §1 何时需要新版本

| 变更类型 | 需要新版本？ | 操作 |
|------|:--:|------|
| 新增可选字段 | 否 | 直接加 |
| 新增必填字段 | 是 | 新版本或默认值 |
| 删除字段 | 是 | 先标记 deprecated，一个版本后再删 |
| 修改字段类型 | 是 | 新版本 |
| 修改端点行为 | 是 | 新版本 |

## §2 版本策略

**URL 路径版本**（推荐）：

```
GET /v1/tasks
GET /v2/tasks
```

**为什么不用 Header 版本**：URL 版本对 Agent 和人类都更可见。Agent 修改端点时可以立即知道涉及哪个版本。

## §3 废弃流程

```
v1 API
  → 阶段 1: 在响应头中加 Deprecation: true + Sunset: date
  → 阶段 2: 文档中标注 @deprecated
  → 阶段 3: 一个版本周期后删除 v1
```

```python
@app.get("/v1/tasks")
@deprecated(sunset="2025-06-01")
async def list_tasks_v1():
    ...
```

## §4 Agent 规则

1. **新增端点** → 使用当前最新版本号
2. **破坏性变更** → 创建新版本端点，保留旧版本至少一个版本周期
3. **废弃旧端点** → 在 L4_M01（变更日志）中记录废弃日期
4. **版本号记录在 project-graph.yaml**：

```yaml
structure:
  src/api/v1/:
    type: package
    status: deprecated
    sunset: "2025-06-01"
  src/api/v2/:
    type: package
    status: active
```

## §5 文档同步

每次新增/废弃 API 版本 → 更新 `L2_G01`（API 规范文档）：

```markdown
## v2 Endpoints

| Method | Path | 描述 | 认证 |
|------|------|------|:--:|
| GET | /v2/tasks | 获取任务列表（支持游标分页） | ✅ |
| POST | /v2/tasks | 创建任务 | ✅ |

## v1 Endpoints（@deprecated, sunset: 2025-06-01）
```
