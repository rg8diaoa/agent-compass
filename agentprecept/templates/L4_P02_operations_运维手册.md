# 运维手册

> 分类: P | 层级: L4 | 编号: L4_P02
> 状态: 📝 撰写中 | 目标读者: 运维/开发者
> 前置阅读: L3_P01_monitoring_监控指标.md

---

## §1 部署架构

<!-- AGENT: 读取 L2_D01 + project-graph.yaml，生成部署架构 -->

```
[在此插入部署图：服务器、数据库、缓存、负载均衡]
```

## §2 部署步骤

```bash
# 1. 拉取代码
git checkout v1.3.0

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
alembic upgrade head

# 4. 重启服务
systemctl restart todo-api
```

## §3 备份策略

| 备份对象 | 频率 | 保留 | 恢复验证 |
|------|:--:|:--:|:--:|
| 数据库 | 每日 | 30 天 | 每周恢复测试 |
| 配置文件 | 每次变更 | 永久 | git 即备份 |
| 用户上传文件 | 每日 | 90 天 | 每月抽查 |

```bash
# 数据库备份
pg_dump todo_db > backup_$(date +%Y%m%d).sql
```

## §4 健康检查

```
GET /health → 200 OK
{
  "status": "ok",
  "db": "connected",
  "cache": "connected",
  "uptime": "72h"
}
```

| 检查项 | 端点 | 期望 |
|------|------|------|
| 服务存活 | `GET /health` | 200 |
| 数据库 | 健康检查中的 db 字段 | connected |
| 缓存 | 健康检查中的 cache 字段 | connected |

## §5 故障恢复

| 故障 | 检测 | 恢复步骤 |
|------|------|------|
| 服务不响应 | `/health` 超时 | 1. 检查进程 `systemctl status` → 2. 重启 → 3. 查日志 |
| 数据库不可用 | 健康检查 db=disconnected | 1. 检查 PG 进程 → 2. 重启 PG → 3. 恢复备份 |
| 磁盘满 | 监控告警 | 1. 清理日志 → 2. 扩容 |
| 内存泄漏 | 监控指标持续上升 | 1. 重启服务 → 2. 生成 heap dump → 3. 修复代码 |

## §6 Agent 规则

1. 首次部署 → 在项目内创建并填充本模板
2. 部署架构变更 → 同步更新 §1 + project-graph.yaml
3. 每次故障 → 在 §5 追加一条记录
