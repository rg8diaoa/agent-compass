# 模块设计

> 分类: F | 层级: L2 | 编号: L2_F07
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_D01_architecture_架构设计.md

---

## §1 无循环依赖

```
依赖方向：Application → Domain → Infrastructure → 外部
            ↑            ↑           ↑
         编排层      业务核心      技术实现

❌ Domain → Application（反向）
❌ Infrastructure → Domain → Infrastructure（循环）
```

**Agent 规则**：新建模块时，确认它依赖的模块不会反向依赖它。用 `madge` 或 `import-linter` 自动检测。

## §2 依赖注入

```python
# ✅ 构造器注入
class TaskService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache

# ❌ 全局单例
class TaskService:
    db = GlobalDB.get_instance()
```

- 不在模块内部创建依赖实例——从外部传入
- 使用接口（Protocol / ABC）而非具体类，方便测试时 mock

## §3 模块公有接口

每个模块通过 `__all__` 明确公有 API：

```python
# src/services/task_service.py
__all__ = ["TaskService", "CreateTaskDTO", "TaskNotFoundError"]

class TaskService:
    ...

class CreateTaskDTO:
    ...

class TaskNotFoundError(Exception):
    ...
```

模块私有函数用 `_` 前缀。

## §4 模块拆分原则

| 信号 | 说明 | 操作 |
|------|------|------|
| 单文件 > 400 行 | 职责太多 | 拆分子模块 |
| 相同前缀的函数 > 8 个 | 隐含新模块 | 提取为独立模块 |
| 跨层调用（api 直接调 db） | 违规依赖 | 插入 service 层 |
| 两个模块总是一起改动 | 耦合过高 | 考虑合并 |

## §5 Agent 规则

1. 新建模块 → 用构造器注入，不创建全局实例
2. 新建模块 → 定义 `__all__`
3. 文件超过 400 行 → 询问是否拆分
4. 发现循环依赖 → 在 L4_O01 中记录并提 PR 修复
