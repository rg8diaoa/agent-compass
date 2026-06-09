# 测试策略

> 分类: J | 层级: L3 | 编号: L3_J01
> 状态: ⏳ 待撰写 | 目标读者: QA / 开发者

---

## §1 测试金字塔

| 层级 | 覆盖范围 | 目标覆盖率 | 工具 |
|------|------|:--:|------|
| **单元测试** | 函数/方法级别 | ≥ 80% | _pytest / jest_ |
| **集成测试** | 模块间交互 | ≥ 60% | _pytest + testcontainers_ |
| **端到端测试** | 关键用户流程 | 核心路径全覆盖 | _playwright / cypress_ |
<!-- AGENT: 根据项目实际技术栈选择测试工具，删除不适用的行 -->

## §2 Agent 规则

1. 新模块必须创建对应测试文件
2. 修改已有模块 → 先跑已有测试确认无回归
3. 覆盖率不达标 → 标记到 HANDOFF.md
4. 测试发现架构级问题 → 追加 L4_O01

## §3 测试文件命名

```
tests/
├── test_{module_name}.py
├── conftest.py              ← 共享 fixture
└── factories/               ← 测试数据工厂
```

## §4 CI 集成

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: pytest --cov --cov-report=term --cov-fail-under=80
```
