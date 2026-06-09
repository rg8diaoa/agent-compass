# 配置管理规范

> 分类: E | 层级: L2 | 编号: L2_E03
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_F01_dev-env_开发环境.md

---

## §1 配置分层

三层配置体系。Agent 新增配置项时按此分层：

| 层 | 位置 | 内容 | 示例 |
|---|------|------|------|
| **环境变量** | `.env` | 密钥、数据库连接、第三方 API key | `DATABASE_URL`, `JWT_SECRET` |
| **配置文件** | `config/{profile}.yaml` | 非敏感运行参数 | `page_size`, `rate_limit`, `log_level` |
| **代码常量** | `src/config.py` | 不可变的业务常数 | `MAX_TASKS=100`, `ALLOWED_STATUSES` |

## §2 .env 规范

```
# .env.example（提交到 Git——不包含真实值）
DATABASE_URL=postgresql://localhost:5432/db
JWT_SECRET=your-secret-here
LOG_LEVEL=info
```

```bash
# .env（不提交到 Git——在 .gitignore 中）
DATABASE_URL=postgresql://prod-server:5432/db
JWT_SECRET=actual-secret-value
LOG_LEVEL=debug
```

## §3 配置文件格式

```yaml
# config/dev.yaml
app:
  page_size: 20
  max_page_size: 100
  rate_limit: 1000  # requests/minute

db:
  pool_size: 5
  timeout: 30s

auth:
  token_expiry: 24h
  refresh_expiry: 7d
```

## §4 Agent 规则

1. **新增配置项** → 先判断属于哪一层 → 放对应位置
2. **密钥/密码** → 只能放 `.env`，绝不硬编码在代码中
3. **新配置必须有默认值** → `config/defaults.yaml` 中记录
4. **配置变更** → 更新 `.env.example` 同步

## §5 Secrets 管理

开发环境用 `.env`。生产环境用平台密钥管理：

```
Python: os.getenv("KEY")
Node:   process.env.KEY
CI:     GitHub Secrets / GitLab Variables → 注入到环境变量
```

不将 `.env` 提交到 Git。在 `.gitignore` 中确认：

```
.env
*.local
```
