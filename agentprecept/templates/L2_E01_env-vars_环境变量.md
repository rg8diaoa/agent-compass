# 环境变量规范

> 分类: E | 层级: L2 | 编号: L2_E01
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_E03_config_配置管理.md

---

## §1 命名约定

```
{NAMESPACE}_{COMPONENT}_{KEY}
```

| 示例 | 含义 |
|------|------|
| `APP_PORT` | 应用端口 |
| `DB_HOST` | 数据库主机 |
| `REDIS_URL` | Redis 连接串 |
| `JWT_SECRET` | JWT 签名密钥 |
| `LOG_LEVEL` | 日志级别 |

- 全大写，下划线分隔
- 用命名空间前缀区分不同服务（`DB_`、`REDIS_`、`AWS_`）

## §2 默认值策略

```python
# config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/dev")
JWT_SECRET = os.getenv("JWT_SECRET")  # 无默认值——必须显式设置
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
```

- 开发环境可用默认值
- 密钥/密码 → 无默认值（启动时就报错，防止遗忘）

## §3 .env.example 模板

```bash
# === 必需 ===
DATABASE_URL=postgresql://localhost:5432/db
JWT_SECRET=change-me-to-a-random-string

# === 可选 ===
LOG_LEVEL=info
PORT=8000
REDIS_URL=redis://localhost:6379

# === 第三方 ===
SENDGRID_API_KEY=
```

## §4 Agent 规则

1. 新增环境变量 → 同步更新 `.env.example`
2. 密钥类变量 → 无默认值，不提交到 Git
3. 非保密配置 → 优先放配置文件而非环境变量（见 L2_E03）
