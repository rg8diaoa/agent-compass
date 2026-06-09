# 10 — 性能追踪：Agent 做性能优化时怎么做

> **AgentPrecept 落地**: 审计维度 15（体验审计）部分覆盖性能文档，详见文末。

> Agent 不是让代码"跑起来就行"。当性能成为问题时，Agent 需要一套流程——从测量到优化到验证，每一步有据可查。

---

## 性能优化的三个原则

1. **先测量，再优化**。不猜测瓶颈——用 profiler 数据说话
2. **一次改一个变量**。改多个东西后变快了，你永远不知道哪个是真正的原因
3. **优化决策进设计依据**。做了性能取舍后记录原因——下一个 Agent 不会推翻

---

## 性能优化流程

```
1. 测量 → 找到瓶颈
2. 记录基线 → 当前 QPS/延迟/内存基准
3. 提出方案 → 列出可选方案 + 预估收益
4. 实施优化 → 一次一个变量
5. 验证 → 对比基线，确认提升
6. 记录决策 → 追加 L4_O01
```

---

## 步骤详解

### 步骤 1：测量

```bash
# Python: cProfile
python -m cProfile -s cumulative src/main.py

# Node: clinic
clinic doctor -- node src/server.js

# 数据库: EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC;
```

### 步骤 2：记录基线

在 L4_O01 或性能日志中记录：

```markdown
| 指标 | 基线值 | 测量条件 |
|------|------|------|
| GET /tasks QPS | 850 | 100 并发, 100K 数据, 本地 |
| P99 延迟 | 320ms | 同上 |
| 内存占用 | 180MB | 空载 |
```

### 步骤 3-5：优化 + 验证

每次优化后对比基线：

```markdown
| 优化 | 改动 | 基线 QPS | 优化后 QPS | 提升 |
|------|------|:--:|:--:|:--:|
| 加索引 | CREATE INDEX ON tasks(user_id) | 850 | 3200 | 3.8× |
| 查询优化 | 去掉 SELECT * | 3200 | 4100 | 28% |
| 加缓存 | Redis 缓存列表结果 | 4100 | 12000 | 2.9× |
```

### 步骤 6：记录设计依据

```markdown
| 决策 | 来源 | 证据 |
|------|:--:|------|
| 为什么用 Redis 做缓存层而不是应用内存 | 性能测试 | 多实例部署时应用内存缓存不一致 |
| 为什么给 tasks.user_id 加索引而不是复合索引 | EXPLAIN 分析 | 所有查询都以 user_id 为首条件 |
| 为什么选择 LIMIT 20 而不是后端全量分页 | 压测数据 | 100K 数据下全量分页 P99 延迟 4.2s |
```

---

## 常见优化场景速查

| 症状 | 先检查 | 常见解法 |
|------|------|------|
| API 响应慢 | EXPLAIN → 是否全表扫描 | 加索引、优化查询、加缓存 |
| 高并发下崩溃 | 连接池配置 | 调大 pool_size、加排队机制 |
| 内存持续增长 | heap dump | 修复内存泄漏、对象复用 |
| 启动慢 | 初始化流程 | 懒加载、按需导入 |

---

## Agent 规则

1. 不要"我觉得慢"就优化 → 先拿 profiler 数据
2. 优化后必须跑全量测试 → 确认没有引入正确性 bug
3. 任何性能取舍（速度 vs 可读性 / 内存 vs CPU）→ 追加 L4_O01
4. 在 project-graph.yaml 中标记了性能敏感的模块：

```yaml
structure:
  src/api/tasks.py::list_tasks:
    type: endpoint
    perf_sensitive: true        # 标记性能关键
    baseline_qps: 850
    baseline_p99_ms: 320
```

---

## 一句话

**Agent 做性能优化和人一样——先测量，再改，改了记。记在 L4_O01 里，下一个 Agent 不会把索引删掉。**

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| 性能文档模板 | 体验审计（维度 15）部分覆盖 | `agentprecept audit --gate` |
| 基准记录 | L4_O01 模板支持性能决策行 | `agentprecept init` 自动复制模板 |
