# Git 工作流

> 分类: F | 层级: L2 | 编号: L2_F03
> 状态: 📝 撰写中 | 目标读者: 开发者

---

## §1 分支策略

```
main          ← 生产就绪代码，只通过 PR 合并
├── develop    ← 集成分支（可选）
├── feature/*  ← 新功能
├── fix/*      ← bug 修复
└── release/*  ← 发布准备
```

## §2 Commit 格式

```
{type}: {简短描述}

{详细说明（可选）}
```

| type | 含义 |
|------|------|
| `feat` | 新功能 |
| `fix` | bug 修复 |
| `refactor` | 重构（不改变行为） |
| `docs` | 文档变更 |
| `test` | 测试变更 |
| `chore` | 构建/依赖/工具 |

示例：`fix: token 过期判断改用 db.func.now()`

## §3 Agent 规则

1. **新建分支** → `feature/{描述}` 或 `fix/{描述}`
2. **Commit** → 做完一个逻辑单元就 commit，不攒一堆
3. **修改共享文件前** → 先 `git pull`（见 AGENTS.md 并发安全）
4. **Push 被拒** → `git pull --rebase`，不 force push
5. **合并到 main** → 通过 PR + CI 通过

## §4 .gitignore 基线

```
# 环境变量（含密钥）
.env
*.local

# 依赖
node_modules/
__pycache__/
.venv/

# IDE
.vscode/
.idea/

# 构建产物
dist/
build/
*.pyc
```
