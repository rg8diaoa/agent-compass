# 架构设计

> 分类: D | 层级: L2 | 编号: L2_D01
> 状态: ⏳ 待撰写 | 目标读者: 开发者

---

## 三层架构

```
src/
├── api/          ← 路由层：接收 HTTP 请求，参数验证，调用 service
├── services/     ← 业务逻辑层：核心逻辑，与数据模型交互
├── models/       ← 数据模型层：ORM 定义，数据库交互
├── schemas/      ← 请求/响应 Schema 定义
└── db/           ← 数据库连接和迁移
```

## 数据流

```
Client → api/tasks.py → services/task_service.py → models/task.py → PostgreSQL
                ↑                    ↑                    ↑
           参数验证            业务逻辑              ORM 查询
```

## 模块职责

| 模块 | 职责 | 不负责 |
|------|------|--------|
| `api/` | HTTP 请求/响应处理 | 业务逻辑、数据库查询 |
| `services/` | 核心业务逻辑 | HTTP 处理 |
| `models/` | 数据持久化 | 业务规则 |
| `schemas/` | 输入输出验证 | 数据库操作 |
