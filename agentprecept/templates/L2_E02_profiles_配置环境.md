# 配置环境管理

> 分类: E | 层级: L2 | 编号: L2_E02
> 状态: 📝 撰写中 | 目标读者: 开发者/运维
> 前置阅读: L2_E03_config_配置管理.md

---

## §1 环境分层

| 环境 | 用途 | 配置来源 | 谁在用 |
|------|------|------|------|
| **dev** | 本地开发 | `.env` + `config/dev.yaml` | 开发者 |
| **staging** | 预发布验证 | CI 注入环境变量 + `config/staging.yaml` | CI + QA |
| **prod** | 生产环境 | 平台密钥管理 + `config/prod.yaml` | 运维 |

## §2 配置切换

```python
# config.py
import os

PROFILE = os.getenv("APP_PROFILE", "dev")
config = load_yaml(f"config/{PROFILE}.yaml")
```

```bash
# 启动时指定环境
APP_PROFILE=staging uvicorn src.main:app
APP_PROFILE=prod gunicorn src.main:app
```

## §3 环境间差异

| 配置项 | dev | staging | prod |
|------|-----|---------|------|
| `LOG_LEVEL` | debug | info | warning |
| `DB_POOL_SIZE` | 5 | 20 | 50 |
| `DEBUG_MODE` | true | false | false |
| `CORS_ORIGINS` | `*` | `*.staging.example.com` | `*.example.com` |

## §4 Docker / CI 注入

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - APP_PROFILE=prod
      - DATABASE_URL=${DATABASE_URL}
```

```yaml
# .github/workflows/deploy.yml
env:
  APP_PROFILE: staging
  DATABASE_URL: ${{ secrets.STAGING_DB_URL }}
```

## §5 Agent 规则

1. 新增配置项 → 在所有环境的 config/{profile}.yaml 中同步添加
2. 环境间差异 → 在 L4_O01 中记录原因
3. 敏感配置不可出现在 config/*.yaml → 放环境变量
