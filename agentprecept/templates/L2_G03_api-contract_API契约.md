# API 契约

> 分类: G | 层级: L2 | 编号: L2_G03
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_G02_api-versioning_API版本管理.md

---

## §1 OpenAPI 注解规范

每个 API 端点必须包含完整的 OpenAPI 注解。以下为 FastAPI 示例：

```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/tasks", tags=["tasks"])

class CreateTaskRequest(BaseModel):
    title: str
    priority: str = "P2"

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(req: CreateTaskRequest):
    """创建新任务。

    - 需要认证
    - 同一用户最多 100 个未完成任务
    """
    ...
```

| 注解项 | 必填 | 说明 |
|:--:|:--:|------|
| `tags` | ✅ | 按资源分组 |
| `response_model` | ✅ | 响应类型 |
| `status_code` | ✅ | HTTP 状态码 |
| docstring | ✅ | 功能说明 + 认证要求 + 业务限制 |

## §2 文档生成

```bash
# FastAPI 自动生成
uvicorn src.main:app  # → http://localhost:8000/docs

# Express / NestJS
npm run swagger:generate
```

## §3 响应格式统一

```json
// 成功
{
  "data": { "id": "abc", "title": "Buy milk" },
  "meta": { "request_id": "req_123" }
}

// 错误
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task abc not found"
  },
  "meta": { "request_id": "req_123" }
}
```

## §4 分页约定

```json
// 请求
GET /tasks?page=1&page_size=20

// 响应
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 145,
    "total_pages": 8
  }
}
```

- `page` 从 1 开始
- `page_size` 默认 20，最大 100

## §5 Agent 规则

1. 新增端点 → 必须包含完整的 OpenAPI 注解
2. 响应格式 → 遵循 §3 统一格式
3. 分页 → 遵循 §4 约定
4. 端点变更 → 同步更新本文档 + L2_G02（版本管理）
