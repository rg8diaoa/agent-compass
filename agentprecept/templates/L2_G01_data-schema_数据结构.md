# 数据结构

> 分类: G | 层级: L2 | 编号: L2_G01
> 状态: ⏳ 待撰写 | 目标读者: 开发者
> 前置阅读: L2_D01_architecture_架构设计.md

---

## AGENT: 填充流程

```
1. 扫描以下文件提取数据模型:
   - Python: grep -rn "class.*Model\|class.*Schema\|Table(" src/
   - Node: grep -rn "mongoose.model\|new Schema\|@Entity" src/
   - Prisma: 直接读 schema.prisma
2. 提取每个模型的字段名、类型、约束(not null/max/default)
3. 生成 §1 表格: 模型 | 字段 | 类型 | 约束
4. 从 project-graph relations 中提取实体间调用关系 → 生成 §2 ASCII ER 图
5. 从项目代码中找 API Schema 定义 → 填 §3
```

---

## §1 数据模型

<!-- AGENT: 执行上方流程 1-3 -->

| 模型 | 字段 | 类型 | 约束 |
|------|------|------|------|
| _示例_ | _name_ | _string_ | _not null, max 255_ |

## §2 关系图

<!-- AGENT: 执行上方流程 4 -->

```
[在此插入 ASCII ER 图]
```

## §3 API Schema

<!-- AGENT: 执行上方流程 5 -->

```json
{
  "id": "uuid",
  "name": "string"
}
```

## §4 数据库迁移

每次数据模型变更 → 创建迁移文件。

## Agent 规则

1. 新增字段 → 同步更新本模板 §1
2. 修改关系 → 同步更新 §2 + project-graph.yaml relations
3. API 变更 → 同步更新 §3 + L2_G02（版本管理）
