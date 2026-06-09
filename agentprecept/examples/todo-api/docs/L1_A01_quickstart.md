# 快速开始

> 分类: A | 层级: L1 | 编号: L1_A01
> 状态: 📝 撰写中 | 目标读者: 开发者

---

## 环境要求

- Python 3.10+
- PostgreSQL 15+

## 安装

```bash
git clone https://github.com/example/todo-api
cd todo-api
pip install -r requirements.txt
```

## 配置

```bash
cp .env.example .env
# 编辑 .env：设置 DATABASE_URL 和 JWT_SECRET
```

## 运行

```bash
uvicorn src.main:app --reload
```

## 验证

```bash
pytest tests/ -v
```

## 常见问题

### Q: 数据库连接失败？
A: 检查 PostgreSQL 是否运行，确认 .env 中 DATABASE_URL 正确。
