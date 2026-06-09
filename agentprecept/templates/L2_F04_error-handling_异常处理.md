# 异常处理规范

> 分类: F | 层级: L2 | 编号: L2_F04
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_F02_code-style_代码规范.md

---

## §1 异常层次

所有自定义异常继承项目基类：

```python
class {Project}Error(Exception):
    """所有自定义异常的基类"""
    code: str    # 机器可读错误码
    status: int  # HTTP 状态码（如适用）

class AuthError({Project}Error):
    """认证/授权异常"""
    status = 401

class NotFoundError({Project}Error):
    """资源不存在"""
    status = 404

class ConflictError({Project}Error):
    """并发冲突"""
    status = 409

class ValidationError({Project}Error):
    """输入验证失败"""
    status = 422

class ExternalServiceError({Project}Error):
    """外部服务调用失败"""
    status = 502
```

## §2 错误码约定

```
格式: {DOMAIN}_{REASON}
示例: AUTH_TOKEN_EXPIRED / TASK_NOT_FOUND / RATE_LIMIT_EXCEEDED
```

每个异常定义唯一 `code`，用于日志检索和监控告警。

## §3 抛出 vs 返回

- 不可恢复的错误 → 抛出异常
- 可恢复的状态 → 返回 Result 或 (value, error) 二元组
- 警告 → 日志记录 + 不影响主流程

## §4 日志记录

```python
import logging
logger = logging.getLogger(__name__)

try:
    result = external_service.call()
except ExternalServiceError as e:
    logger.error("external_failed", extra={
        "service": "payment",
        "error_code": e.code,
        "retry_count": retries
    })
    raise
```

## §5 重试与降级

| 场景 | 策略 | 参数 |
|------|------|------|
| 网络超时 | 指数退避重试 | max_retries=3, base_delay=1s |
| 外部服务 5xx | 有限重试 + 降级 | max_retries=2, fallback=缓存 |
| 数据冲突 | 乐观锁重试 | max_retries=3, 从数据库重新读取后重试 |
| 参数验证 | 不重试 | 直接返回 422 |

## §6 Agent 规则

1. 创建新异常 → 继承 `{Project}Error` → 定义 code + status
2. 不要 `except Exception` 裸吞异常——至少记录日志
3. 在 L4_O01 中记录"为什么这个模块选择了重试/降级策略"
