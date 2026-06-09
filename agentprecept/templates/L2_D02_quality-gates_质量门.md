# 质量门

> 分类: D | 层级: L2 | 编号: L2_D02
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_D01_architecture_架构设计.md

---

## §1 概述

质量门在 Agent 提交代码前自动执行。不同于审计（文档级检查）——质量门是**代码级**检查。不通过 → 不提交。

## §2 代码级门禁

| 门 | 检查什么 | 阈值 | 纯代码/需语义 |
|:--:|------|:--:|:--:|
| **圈复杂度** | 单函数分支路径数 | ≤ 10 | 纯代码 |
| **函数行数** | 单函数最大行数（含注释） | ≤ 50 | 纯代码 |
| **文件行数** | 单文件最大行数 | ≤ 400 | 纯代码 |
| **依赖方向** | 是否出现循环依赖 | 0 循环 | 纯代码 |

```bash
# ruff / eslint 内置检查
ruff check --select=C90    # 圈复杂度
eslint --rule 'max-lines-per-function' --rule 'max-lines'
```

## §3 架构级门禁

| 门 | 检查什么 | 谁执行 |
|:--:|------|:--:|
| **无循环依赖** | import 图是否出现环 | `import-linter` / `madge` |
| **Layer 方向** | api → services → models 方向不逆 | 手动 + Agent 审查 |
| **公开接口变更** | 修改 `__all__` 导出内容 → 触发审查 | pre-commit hook |

```bash
# 检测循环依赖
pip install import-linter
lint-imports
```

## §4 Agent 规则

1. 提交前自动跑代码级门禁（ruff/eslint）
2. 新增模块后跑依赖方向检查（`madge --circular`）
3. 门禁失败 → 修好再提交，不加 `# noqa` 绕过
4. 如果确实需要跳过某条门禁 → 在 L4_O01 中记录原因

## §5 门禁不替代审计

| | 质量门（本文档） | 审计（见 AUDIT_REPORT.md） |
|---|---|---|
| 检查面 | 代码级 | 文档级 |
| 频率 | 每次提交 | 重大变更后 |
| 执行者 | pre-commit / CI | Agent 手动或 CI |
