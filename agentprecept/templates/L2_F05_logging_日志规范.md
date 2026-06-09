# 日志规范

> 分类: F | 层级: L2 | 编号: L2_F05
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_F02_code-style_代码规范.md

---

## §1 日志级别

| 级别 | 含义 | Agent 何时使用 |
|------|------|------|
| **ERROR** | 需要人工介入的故障 | 外部服务不可用、数据库连接失败 |
| **WARNING** | 可自动恢复的异常 | 重试成功、降级触发、接近限流阈值 |
| **INFO** | 关键业务流程 | 用户登录、任务创建、配置变更 |
| **DEBUG** | 开发调试信息 | 函数入参出参、SQL 语句 |

Agent 不要用 `print()`——用结构化日志。

## §2 结构化格式

```python
import logging
logger = logging.getLogger(__name__)

logger.info("task_created", extra={
    "task_id": task.id,
    "user_id": current_user.id,
    "priority": task.priority
})
```

输出（JSON Lines）：

```json
{"level": "INFO", "event": "task_created", "task_id": "abc123", "user_id": "user_42", "priority": "P1"}
```

## §3 不记录的内容

| 不记录 | 原因 |
|------|------|
| 密码/密钥/Token | 安全——日志可能被非授权访问 |
| 完整请求体（含敏感字段） | 脱敏后记录 |
| 个人身份信息（PII） | 合规——GDPR 等法规要求 |

## §4 每模块日志话题

每个模块定义自己的日志话题，用于检索和告警：

```python
# src/services/auth_service.py
logger.info("login_success", extra={"user_id": user.id})
logger.warning("login_failed", extra={"reason": "invalid_password"})

# src/services/task_service.py
logger.info("task_created", extra={"task_id": task.id})
logger.error("task_creation_failed", extra={"reason": str(e)})
```

## §5 Agent 规则

1. 每个新模块 → 在模块顶部定义 `logger = logging.getLogger(__name__)`
2. 关键操作（创建/删除/权限变更）→ INFO 级别
3. 异常处理 → ERROR 级别 + `extra={"error_code": e.code}`
4. 记录结构化字段而非 `f-string` 拼接消息
