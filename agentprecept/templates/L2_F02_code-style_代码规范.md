# 代码规范

> 分类: F | 层级: L2 | 编号: L2_F02
> 状态: 📝 撰写中 | 目标读者: 开发者

---

## §1 命名约定

| 类型 | 规则 | 示例 |
|---|---|---|
| 文件 | snake_case | `task_service.py` |
| 类 | PascalCase | `TaskService` |
| 函数/方法 | snake_case | `create_task()` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| 私有成员 | `_` 前缀 | `_validate_input()` |

## §2 导入顺序

```
1. 标准库
2. 第三方库
3. 本项目模块
```

## §3 类型注解

- 所有公共函数的参数和返回值必须注解
- 类 `__init__` 参数必须注解

## §4 模块结构

每个模块导出 `__all__` 明确公共 API。模块内部函数用 `_` 前缀标记私有。

## §5 Lint 配置

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

## §6 Agent 规则

1. 新建文件 → 遵循命名约定
2. 公共函数 → 必须有类型注解
3. 导入 → 按顺序分组
