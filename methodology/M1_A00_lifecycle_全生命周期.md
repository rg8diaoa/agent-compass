# 00 — 完整循环：Agent 开发方法论全景

> **AgentPrecept 落地**: 8 阶段中 init/sync/audit/handoff 4 阶段有 CLI 支持，详见文末落地表。

> agentprecept 不是"写文档的方法"。是从想法到维护，Agent 在每个阶段该做什么、查什么、产出什么的完整工作流。

---

## 循环总览

```
            ┌─────────────────────────────────────────┐
            │              agentprecept              │
            │          Agent 开发完整循环              │
            └─────────────────────────────────────────┘

   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
   │  1.想法  │ ──→ │  2.设计  │ ──→ │ 3.文档   │ ──→ │ 4.开发   │
   │  Idea    │     │  Design  │     │  Docs    │     │  Code    │
   └──────────┘     └──────────┘     └──────────┘     └────┬─────┘
        ↑                                                  │
        │                    ┌──────────────────────────────┘
        │                    ↓
   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ 8.维护   │ ←── │  7.修复  │ ←── │ 6.审计   │ ←── │ 5.测试   │
   │ Maintain │     │   Fix    │     │  Audit   │     │   Test   │
   └──────────┘     └──────────┘     └──────────┘     └──────────┘
        │                                                  ↑
        └──────────────────────────────────────────────────┘
                          循环往复
```

**贯穿全循环的三条线**：

| 贯穿物 | 作用 | 谁维护 |
|---|---|---|
| **project-graph.yaml** | 项目结构地图——Agent 任何时候都知道"改了 X 会影响谁" | Agent 在每个阶段更新 |
| **L4_O01 设计依据** | 每个关键决策的来源和理由——防止 Agent 推翻已验证的方案 | Agent 做决策时追加 |
| **HANDOFF.md** | 会话间交接——下一个 Agent 知道从哪开始 | Agent 每次会话结束时重写 |

---

## 阶段 0：研究 → 查是否重复造轮子（5-10 分钟）

**做新东西前，先看有没有人已经做过了。**

| | Agent 做什么 |
|---|---|
| **查什么** | web_search + GitHub search |
| **做什么** | 搜索 3 个类似项目，对比功能 |
| **产出** | 一句话：为什么还要做？与竞品差在哪？ |
| **跳过** | 内部工具 / 已有明确需求文档 / 个人项目 → 直接跳阶段 1 |

---

## 阶段 1：想法 → 需求

**你有一句话需求："做一个 Todo API，支持用户登录"。**

| | Agent 做什么 |
|---|---|
| **查什么** | 无——这是起点 |
| **做什么** | 将一句话需求展开为结构化需求列表 |
| **产出** | `docs/L1_C01_phased-plan_实施路线.md`（模板在 templates/，功能列表、用户故事、验收条件） |
| **更新图** | 不需要（还没有代码） |

```markdown
# 需求定义

## 用户故事
- 作为用户，我可以注册/登录
- 作为用户，我可以创建、查看、编辑、删除自己的 Task
- 作为用户，我可以给 Task 加标签和优先级

## 验收条件
- 登录后获取 JWT token，有效期 24h
- Task CRUD 全部需要认证
- 用户只能操作自己的 Task
```

---

## 阶段 2：设计 → 架构

**从需求推导技术方案。**

| | Agent 做什么 |
|---|---|
| **查什么** | 需求定义（L1_C01） |
| **做什么** | 技术选型、模块划分、数据模型设计 |
| **产出** | `docs/L2_D01_architecture_架构设计.md`、`docs/L2_G01_data-schema_数据结构.md`（模板在 templates/，按需取用） |
| **更新图** | 创建 `project-graph.yaml` 结构层——列出所有计划中的模块 |
| **更新依据** | 每做一个技术选型，追加一行到 L4_O01（为什么选 X 而不是 Y） |

```yaml
# project-graph.yaml 初始版本（设计阶段产物）
structure:
  src/api/:
    type: package
    children: [tasks.py, auth.py]
  src/services/:
    type: package
    children: [task_service.py, auth_service.py]
  src/models/:
    type: package
    children: [task.py, user.py]
```

```markdown
# L4_O01 设计依据（设计阶段追加）
| 决策 | 来源 | 证据 |
|------|:--:|------|
| 三层架构 api/services/models | 设计评审 | 两层导致 api 混入业务逻辑 |
| JWT 而不是 Session | 需求分析 | 无状态，未来分布式部署无需改造 |
```

---

## 阶段 3：文档体系初始化

**在写第一行代码前，搭好文档骨架。**

| | Agent 做什么 |
|---|---|
| **查什么** | agentprecept templates/ |
| **做什么** | 从 templates/ 复制文档骨架到 docs/，初始化术语表 |
| **产出** | INDEX.md、L1_A02 命名规范、L1_B01 术语表、HANDOFF.md |
| **更新图** | 不需要 |
| **更新依据** | 不需要 |

```
docs/
├── INDEX.md                    ← 文档导航
├── L1_A01_quickstart.md        ← 怎么跑起来
├── L1_A02_naming-convention.md ← 命名宪法
├── L1_B01_glossary.md          ← 术语定义
├── L1_C01_phased-plan.md       ← 需求（阶段 1 产出）
├── L2_D01_architecture.md      ← 架构（阶段 2 产出）
├── L2_G01_data-schema.md       ← 数据结构（阶段 2 产出，模板）
├── L4_O01_design-rationale.md  ← 设计依据（阶段 2 产出）
├── HANDOFF.md                  ← 会话交接
└── project-graph.yaml          ← 项目图（阶段 2 产出）
```

---

## 阶段 4：开发 → 写代码

**开始实现。这是循环中最频繁的阶段。**

| | Agent 做什么 |
|---|---|
| **查什么** | project-graph.yaml（影响范围）→ L4_O01（架构约束）→ L1_A02（命名）→ L1_B01（术语） |
| **做什么** | 按架构设计实现模块 |
| **产出** | 代码 |
| **更新图** | 每新建/删除模块 → 更新 structure；每新增依赖 → 更新 relations |
| **更新依据** | 如果实现中做了新的设计决策 → 追加 L4_O01 |

**这是 agentprecept 最核心的价值时刻**——Agent 在写 `authenticate()` 之前，花 30 秒查图知道它依赖 `crypto.py`，查依据知道不能引入 session。30 秒避免 3 小时的连锁 bug。

详细流程见：[07-dev-workflow.md](07-dev-workflow.md)

---

## 阶段 5：测试 → 验证

**Agent 不仅要写代码，还要验证代码。**

| | Agent 做什么 |
|---|---|
| **查什么** | L2_D01（架构）→ L2_G01（数据 Schema）→ 需求定义（验收条件） |
| **做什么** | 写测试、跑测试、收集覆盖率 |
| **产出** | 测试文件、测试报告 |
| **更新图** | 在 relations 中添加 `type: tests` 边 |
| **更新依据** | 如果测试覆盖策略发生变化 → 追加 L4_O01 |

```yaml
# project-graph.yaml 测试关系
relations:
  - from: tests/test_auth.py
    to: src/api/auth.py
    type: tests
  - from: tests/test_tasks.py
    to: src/api/tasks.py
    type: tests
```

**Agent 测试规则**：

1. 每个新模块必须创建对应测试文件
2. 修改影响范围内的模块 → 先跑已有测试确认没有回归
3. 覆盖率低于 80% → 标记在 HANDOFF.md 中
4. 测试发现架构级 bug → 追加设计依据，记录为什么原来的设计不够

---

## 阶段 6：审计 → 质量检查

**不是人工审查——Agent 自己跑审计。**

| | Agent 做什么 |
|---|---|
| **查什么** | docs/ 全部文档、project-graph.yaml |
| **做什么** | 运行 agentprecept audit --gate 逐维度扫描（15 维自动化 + 自选清单） |
| **产出** | 审计报告（`AUDIT_REPORT.md`） |
| **更新图** | 如果发现图不一致 → 修正 project-graph.yaml |
| **更新依据** | 通常不需要 |

审计维度：

| 维度 | 具体检查 |
|:--:|------|
| 命名一致性 | 文件名是否符合 `L{Level}_{CAT}{NN}_{Slug}_{Title}.md` |
| 交叉引用 | 文档中引用的路径是否真实存在 |
| 术语一致性 | 同一概念是否在所有文档中用同一词 |
| 设计追溯 | L4_O01 是否有空白记录 |
| 覆盖率 | 计划文档是否已完成 |
| 骨架残留 | TODO/TBD/FIXME 是否过期 |
| 内容一致性 | 跨文档是否有矛盾 |

详细见：[04-audit-framework.md](04-audit-framework.md)

---

## 阶段 7：修复 → bug 处理

**出了 bug——不只是修，是系统化处理。**

| | Agent 做什么 |
|---|---|
| **查什么** | project-graph.yaml（影响范围）→ L4_O01（约束）→ HANDOFF.md（上一个人排查到哪） |
| **做什么** | 定位根因 → 修复 → 验证影响范围内没有回归 |
| **产出** | 修复代码 + 根因记录 |
| **更新图** | 如果修复改变了依赖关系 → 更新 relations |
| **更新依据** | 如果修复涉及架构级变更 → 追加 L4_O01 |
| **更新交接** | 如果根因复杂且未完全解决 → 记录到 HANDOFF.md |

**修复后必须回答**：这是一个点状 bug（改一行就好）还是系统性 bug（设计缺陷）？如果是后者，追加 L4_O01：

```markdown
| 为什么把 token 过期判断从应用层移到数据库层 | 2025-03 bug 修复 | login 偶发 500——应用层 datetime 和数据库时间不一致。统一用 db.func.now() |
```

详细见：[07-dev-workflow.md](07-dev-workflow.md) 场景 1

---

## 阶段 8：维护 → 长期演进

**项目上线后。Agent 负责的不只是修 bug——是让它可持续。**

| 维护动作 | Agent 做什么 | 更新什么 |
|---|---|---|
| **依赖升级** | 查 project-graph → 确定影响范围 → 升级 → 全量测试 | project-graph（如有新依赖） |
| **技术债务处理** | 从 HANDOFF 和设计依据中识别累积债务 | 追加 L4_O01 记录债务清理决策 |
| **架构迁移** | 查 project-graph → 全量影响分析 → 按重构流程（阶段 4） | project-graph 全量更新 + L4_O01 |
| **版本发布** | 按下方发布流程执行 | project-graph evolution + L4_M01 |
| **知识传递** | 重写 HANDOFF.md | HANDOFF.md |

### 版本发布完整流程

不再是一行"打 tag"。是一个 Agent 可执行的 checklist：

**发布前**：
```
1. 读 L4_M01（变更日志）→ 确认本周期所有变更
2. 读 project-graph.yaml → 确认结构无未记录变更
3. 跑全量测试 → 全部绿
4. 跑 CI 审计（阶段 6）→ 0 🔴
```

**定版本号**（semver）：
- bug 修复、API 不变 → PATCH（1.2.3→1.2.4）
- 新功能、向后兼容 → MINOR（1.2.3→1.3.0）
- 破坏性变更 → MAJOR（1.2.3→2.0.0）

**发布操作**：
```bash
git tag v1.3.0
# 从 L4_M01 提取本周期 changelog 条目
git push origin v1.3.0
gh release create v1.3.0 -F RELEASE.md
```

**发布后**：
```
1. 在 L4_M01 追加 "## [1.3.0] — YYYY-MM-DD"
2. 在 project-graph.yaml evolution 记录此版本
3. 重写 HANDOFF.md → "新版本已发布，下一周期开始"
```

详细见：[08-engineering.md](08-engineering.md)

### 维护核心原则

Agent 不应该"重写第一个版本已经解决的问题"。每次维护动作前，先查 L4_O01——如果这个问题在项目早期已被讨论过，适用当时的决策。

---

## 各阶段进入/退出条件

| 阶段 | 进入条件 | 退出标准 | Agent 自检 |
|------|----------|----------|-----------|
| 0.研究 | 收到新需求 | 找到 3 个类似项目 + 对比功能 | web_search 返回 ≥3 结果 |
| 1.想法 | 研究完成 | 输出 3-5 条需求要点 | 人类确认 |
| 2.设计 | 想法确认 | L2_D01 草稿完成 | [NEEDS_HUMAN_REVIEW] 已标注 |
| 3.文档 | 设计确认 | project-graph.yaml 覆盖新模块 | agentprecept sync 通过 |
| 4.开发 | 文档就绪 | checklist 全 completed | pre-commit 4 gates 通过 |
| 5.测试 | 开发完成 | checklist 测试项全完成 | run_tests 通过 |
| 6.审计 | 测试通过 | agentprecept audit --gate 0 FAIL | exit code 0 |
| 7.修复 | 审计有 FAIL | 所有 FAIL → 0 | 重新 run audit |
| 8.维护 | 修复完成 | HANDOFF 重写 + MEMORY 更新 | HANDOFF [CLOSING] |

---

## 最小启动：30 分钟从零到完整循环

不需要一次做到 8 个阶段。项目初期只需 3 步：

```
第 1 步（10 分钟）：复制 AGENTS.md → Agent 自动遵循循环规则
第 2 步（15 分钟）：创建 project-graph.yaml（结构层 + 初始设计依据）
第 3 步（5 分钟） ：创建 HANDOFF.md（空模板）
```

后续每个阶段**按需**扩展——加新功能时自然进入阶段 4，出 bug 时进入阶段 7，上线后进入阶段 8。

---

## 循环的节奏

| 阶段 | 触发频率 | 每次耗时 |
|---|---|---|
| 1. 想法 | 项目启动 / 大版本 | 1-2 小时 |
| 2. 设计 | 项目启动 / 大版本 | 2-4 小时 |
| 3. 文档初始化 | 项目启动 | 30 分钟 |
| **4. 开发** | **每天多次** | **Agent 花 30 秒查 + 正常写代码** |
| **5. 测试** | **每次提交前** | **分钟级** |
| 6. 审计 | 每轮重大变更后 | 10 分钟 |
| **7. 修复** | **出 bug 时** | **Agent 花 30 秒查 + 正常修 bug** |
| 8. 维护 | 持续 | 按需 |

加粗的三项占日常工作的 90%+。agentprecept 在这三项中为 Agent 节省的时间——每次查图/查依据/查命名 30 秒——是这套体系最直接的回报。

---

## 一句话

**agentprecept 是一个循环，不是一份文档。Agent 从阶段 1 走到阶段 8，每走一圈，项目就更有序。**

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| 项目初始化 | `agentprecept init` 6 阶段一键接入 | `agentprecept init /project` |
| 代码→图同步 | `agentprecept sync` + `sync-graph.py` | `agentprecept sync` |
| 审计 | `agentprecept audit --gate` 15 维自动化 | `agentprecept audit --gate` |
| 会话交接 | `HANDOFF.md` 模板 + `handoff_read` MCP tool | `handoff_read()` |
| gnhf 夜间同步 | `agentprecept gnhf setup` | 可选，需 gnhf CLI |
