# 08 — 工程化：CI/CD + 审计自动化 + 发布

> **AgentPrecept 落地**: CI gate 模板 + pre-commit hook + `agentprecept audit --gate`，详见文末。

> Agent 写的代码不只是跑在本地。要跑在生产环境。这一篇讲 agentprecept 怎么嵌入工程流水线。

---

## 问题

当前流程中，审计是"Agent 手动跑的"——但真实的工程环境中，审计应该是一段 CI 脚本，自动运行，不通过就阻断合并。

此外，版本发布（semver + changelog + tag）在 00-lifecycle 阶段 8 只提了一行，缺少具体操作步骤。

---

## 1. CI 审计自动化

### GitHub Actions 示例

```yaml
# .github/workflows/audit.yml
name: Docs Audit

on:
  pull_request:
    paths:
      - 'docs/**'
      - 'project-graph.yaml'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run agentprecept audit
        run: |
          # 15 维自动化审计
          agentprecept audit --gate > audit-report.md
          cat audit-report.md
      - name: Check for blocking issues
        run: |
          if grep -q "🔴" audit-report.md; then
            echo "::error::Audit found blocking issues"
            cat audit-report.md
            exit 1
          fi
```

### basic-audit.py 要检查什么（15 维参考）

```python
# agentprecept/basic_audit.py — Agent 可以生成这个脚本，也可以手动维护
import os, re, sys

def check_naming(docs_dir):
    """维度 1：文件名是否符合 L{L}_{CAT}{NN}_{Slug}_{Title}.md"""
    pattern = r'^L[1-4]_[A-P]\d{2}_[a-z0-9-]+_.+\.md$'
    violations = []
    for f in os.listdir(docs_dir):
        if f.startswith('L') and not re.match(pattern, f):
            violations.append(f)
    return violations

def check_broken_links(docs_dir):
    """维度 2：交叉引用断链"""
    # 扫描所有 .md 文件中的文件引用 → 验证目标存在
    pass

def check_todos(docs_dir):
    """维度 6：是否有超过 3 个月未处理的 TODO"""
    pass

# ... 其余维度
```

**关键原则**：审计脚本本身可以是 Agent 生成的。human 审查一次后纳入 CI。之后每次 PR，CI 自动跑——不通过就阻断。

---

## 2. 版本发布流程

不再是一行"打 tag"。是一个 Agent 可以执行的 checklist。

### 发布前

```
1. Agent 读取 L4_M01（变更日志）→ 确认本次发布包含的所有变更
2. Agent 读取 project-graph.yaml → 确认结构层没有未记录的变更
3. Agent 跑全量测试 → 确认全部绿
4. Agent 跑 CI 审计 → 确认 0 🔴
```

### 版本号规则（semver 映射）

| 变更类型 | semver | 示例 |
|---|---|---|
| bug 修复（不改变 API） | PATCH | 1.2.3 → 1.2.4 |
| 新增功能（向后兼容） | MINOR | 1.2.3 → 1.3.0 |
| 破坏性变更（API 不兼容） | MAJOR | 1.2.3 → 2.0.0 |

**Agent 怎么定版本号**：读取上次 release tag → 读取 L4_M01 本周期变更 → 按上表映射。

### 发布操作

```bash
# 1. 确认版本号
git tag v1.3.0

# 2. 生成 changelog（从 L4_M01 提取本周期条目）
# 从 L4_M01 提取本周期 changelog 条目

# 3. 发布
git push origin v1.3.0
gh release create v1.3.0 -F RELEASE.md
```

### 发布后

```
1. Agent 在 L4_M01 末尾追加 "## [1.3.0] — 2025-03-01"
2. Agent 在 project-graph.yaml evolution 中记录此版本
3. Agent 重写 HANDOFF.md：标记"新版本已发布，下一周期开始"
```

---

## 3. 预处理检查（pre-commit hook）

阻止 Agent 提交明显违反规范的代码。以下是建议的 `.pre-commit-config.yaml`：

```yaml
repos:
  - repo: local
    hooks:
      - id: check-naming
        name: 检查命名规范
        entry: python -m agentprecept.check_naming
        language: python
        files: \.py$
        stages: [pre-commit]

      - id: check-graph-sync
        name: 检查 project-graph 是否同步
        entry: agentprecept sync --check
        language: python
        files: project-graph.yaml
        stages: [pre-commit]
```

---

## 4. 异常处理工程规范

Agent 写代码时，异常处理需要统一约定。以下是一个通用模板（代码项目可直接使用）：

```python
# src/exceptions.py

class AppError(Exception):
    """应用级异常基类。所有自定义异常继承此。"""
    code: str    # 机器可读错误码，如 "AUTH_TOKEN_EXPIRED"
    status: int  # HTTP 状态码

class AuthError(AppError):
    """认证/授权异常"""
    status = 401

class NotFoundError(AppError):
    """资源不存在"""
    status = 404

class ConflictError(AppError):
    """并发冲突"""
    status = 409
```

**Agent 规则**：
- 创建新异常：继承 AppError → 定义 code + status
- 不可恢复的 → 抛出异常
- 可恢复的 → 返回 Result 或 (value, error) 二元组
- 不要 `except Exception` 裸吞——至少记录日志

---

## 5. Agent 并发安全

当多个 Agent 同时修改 `project-graph.yaml` 或 `L4_O01` 时：

```
Agent 修改共享文件前的流程：
1. git pull → 确认本地是最新
2. 修改文件
3. git add + commit + push
4. 如果 push 被拒绝（远程有更新）：
   → git pull --rebase
   → 手动解决冲突（YAML 冲突通常很简单）
   → 重新 push
```

**在 AGENTS.md 中的规则**（一行）：

> 修改 project-graph.yaml 或 L4_O01 前，先 `git pull`。push 被拒时，rebase 而非 force push。

---

## 一句话

**工程化不是另一套方法论。是把 agentprecept 的检查清单放进 CI 脚本里，让 Agent 每次提交前自动跑——不通过就阻断。**

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| CI 门禁 | GitHub Actions workflow 模板 | `agentprecept init` 自动生成 |
| pre-commit hook | 4 gates（分支/文档/粒度/确认） | `agentprecept init` 自动安装 |
| 审计自动化 | `agentprecept audit --gate` 15 维 | `agentprecept audit --gate` |
| 发布检查 | 审计 exit 0 才能 merge | CI gate 强制执行 |
