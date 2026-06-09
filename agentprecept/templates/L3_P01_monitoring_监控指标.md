# 监控指标规范

> 分类: P | 层级: L3 | 编号: L3_P01
> 状态: 📝 撰写中 | 目标读者: 开发者/运维
> 前置阅读: L2_F05_logging_日志规范.md

---

## §1 黄金信号（Four Golden Signals）

每个服务至少暴露这四类指标：

| 信号 | 含义 | 示例指标 |
|------|------|------|
| **延迟** | 请求耗时分布 | `http_request_duration_seconds`（P50/P90/P99） |
| **流量** | 请求量 | `http_requests_total` |
| **错误** | 失败率 | `http_requests_failed_total` |
| **饱和度** | 资源使用 | `db_connections_active`, `queue_depth` |

## §2 Prometheus 指标命名

```
格式: {namespace}_{subsystem}_{name}_{unit}
示例: todoapi_http_requests_total
      todoapi_db_connections_active
      todoapi_task_operations_duration_seconds
```

## §3 Agent 规则

1. 每个新模块 → 定义至少 2 个指标（请求计数 + 延迟）
2. 指标在代码中显式注册（不自动生成）
3. 关键业务操作（登录、创建任务、支付）→ 额外定义成功率指标

```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "todoapi_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_DURATION = Histogram(
    "todoapi_http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"]
)
```

## §4 告警约定

| 条件 | 级别 | 动作 |
|------|:--:|------|
| 错误率 > 5% 持续 5 分钟 | P1 | 通知 + 自动回滚 |
| P99 延迟 > 基线 × 3 | P2 | 通知 + 排查 |
| 磁盘/内存 > 80% | P2 | 通知 + 扩容 |

## §5 在 project-graph 中标记

```yaml
structure:
  src/api/tasks.py:
    type: endpoint
    metrics:
      - todoapi_task_operations_total
      - todoapi_task_operation_duration_seconds
```
