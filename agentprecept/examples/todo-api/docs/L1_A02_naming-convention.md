# 命名规范

> 分类: A | 层级: L1 | 编号: L1_A02
> 状态: 📝 撰写中 | 目标读者: 全部

---

## §1 文件命名

遵循 AgentPrecept 标准：

```
L{Level}_{Category}{NN}_{Slug}_{Title}.md
```

## §2 代码命名

| 类型 | 规则 | 示例 |
|---|---|---|
| 文件 | snake_case | `task_service.py` |
| 类 | PascalCase | `TaskService` |
| 函数 | snake_case | `create_task()` |
| 常量 | UPPER_SNAKE_CASE | `MAX_TASKS` |
| 私有 | _前缀 | `_validate_input()` |

## §3 API 端点

```
GET    /tasks           # 列表
POST   /tasks           # 创建
GET    /tasks/{id}      # 详情
PUT    /tasks/{id}      # 更新
DELETE /tasks/{id}      # 删除
```

## §4 数据库表

表名：snake_case 复数（`tasks`、`task_tags`）
列名：snake_case（`created_at`、`updated_at`）
