# 07 — 开发工作流：agentprecept 怎么帮你写代码

> **AgentPrecept 落地**: `agentprecept init/sync/audit` + pre-commit 4 gates + CI gate，详见文末。

> 前面 6 篇讲的是"建体系"。这一篇讲的是"用体系"——修 bug、加功能、重构时，这套东西怎么让 Agent 更可靠。

---

## 三个场景，三个流程

### 场景 1：修 bug

```
出 bug 了：login 接口偶发返回 500，日志显示 token 过期判断异常。
```

**没有 agentprecept**：Agent 读代码 → 发现 `refresh_token()` 逻辑复杂 → 不知道改了会影响谁 → 可能引入新 bug → 修完不知道有没有违反之前的设计。

**有 agentprecept**：

1. Agent 查 `project-graph.yaml`：
   ```
   relations:
     - from: src/auth/login.py::authenticate
       to: src/models/user.py::UserModel
       type: calls
     - from: src/auth/login.py
       to: src/lib/crypto.py
       type: depends_on
   ```
   知道 `refresh_token()` 被 `login.py` 调用，`login.py` 依赖 `crypto.py`。修改影响面：2 个文件。

2. Agent 查 `L4_O01_design-rationale.md`：
   ```
   | 为什么用 JWT 而不是 API Key | 2025-01 安全评估 | JWT 无状态... |
   ```
   知道 refresh token 的设计前提是无状态 JWT——不能引入服务端 session 检查。约束明确。

3. Agent 修复代码。

4. Agent 在 HANDOFF.md 记录：
   ```
   ## 阻塞项
   - login 偶发 500：根因是 refresh_token 中 datetime.utcnow() 和数据库时间不一致。
     修复：统一使用 db.func.now()。见 commit a4c2d1。
   ```

5. 如果是架构级修复（如"改变 token 过期判断策略"），追加一行到设计依据。

**效果**：Agent 修 bug 不会引入新 bug，因为它在动手前知道了影响面和约束。

---

### 场景 2：加新功能

```
需求：给 Task 加一个"优先级"字段（P0-P3），按优先级排序。
```

**没有 agentprecept**：Agent 在 `tasks.py` 加字段 → 命名叫 `priority_level` → 前端拿到的是 `priorityLevel` → 一个月后另一个 Agent 加类似字段叫 `importance` → 术语混乱。

**有 agentprecept**：

1. Agent 查命名规范 → 字段命名：`priority`（snake_case），不是 `priority_level`。

2. Agent 查术语表 → 如果已有"优先度"定义，复用。没有则加一行：
   ```
   | 优先级 | Priority | Task 的执行优先级，P0（紧急）到 P3（低） | L2_G01 |
   ```

3. Agent 加字段、写迁移、写测试。

4. Agent 更新 `project-graph.yaml`：
   ```yaml
   relations:
     - from: src/api/tasks.py::list_tasks
       to: src/models/task.py::Task.priority
       type: reads
   ```

5. 如果在实现中做了一个设计决策（如"排序在数据库层做而不是应用层"），追加设计依据。

**效果**：新功能上线后，三个月后另一个 Agent 加功能时发现术语表已有 `priority`，不会发明 `importance`。图的依赖关系让后续修改有据可查。

---

### 场景 3：大重构

```
任务：把 auth 模块从手写 JWT 改成 OAuth2 库。
```

**没有 agentprecept**：Agent 改 `auth/` → 发现 `crypto.py` 也被其他模块用 → 不知道怎么改 → 改完跑了测试没报错 → 上线后 `admin.py` 的 token 验证逻辑悄悄坏了（因为 admin 的测试覆盖率不够）。

**有 agentprecept**：

1. Agent 查 `project-graph.yaml` → 发现 `auth/` 被以下模块依赖：
   ```
   login.py → 调用 → authenticate()
   middleware.py → 调用 → verify_token()
   admin.py → 调用 → verify_token()   ← 重点：admin 测试覆盖率 15%
   ```

2. Agent 查设计依据 → 确认 JWT 的约束是无状态。OAuth2 仍然无状态，约束兼容。

3. Agent 制定重构计划，优先给 `admin.py` 补测试（因为影响面中它的覆盖率最低）。

4. 重构执行。

5. Agent 全量更新 `project-graph.yaml`（auth 模块的依赖关系全部变了）。

6. Agent 追加设计依据：
   ```
   | 为什么从手写 JWT 迁移到 OAuth2 库 | 2025-06 重构 | 减少自定义加密代码，降低安全审计成本 |
   ```

7. HANDOFF.md 记录重构概要。

**效果**：Agent 不会漏掉 `admin.py`，因为有图在。设计依据记录了"为什么迁移"，未来有人质疑为什么用 OAuth2 时有答案。

---

## 最小可行配置

不是每个项目都需要完整 4 层文档体系。根据项目规模选择：

| 项目规模 | 需要什么 |
|---|---|
| **小**（<5 模块，1 人） | `AGENTS.md` + `project-graph.yaml` |
| **中**（5-20 模块，2-5 人+Agent） | 上面 + L1_A02 命名规范 + L4_O01 设计依据 + HANDOFF.md |
| **大**（20+ 模块，多 Agent） | 完整四层文档体系 |

---

## 一句话

**agentprecept 不是让你写更多文档。是让 Agent 在写代码前多花 30 秒查三样东西——图、设计依据、命名规范——然后少花 3 小时修引入的 bug。**

---

## 双分支实验模式

当项目面临重大架构变更、技术选型替换、或两种互斥实现方案时，
不做"在 main 上试错"的赌博。双分支让你同时看到两种选择的**完整差异**——
不只是代码，还包括文档、测试、审计结果。

### 流程

1. **切两个实验分支**：
   ```bash
   git checkout -b exp/方案A  main
   git checkout -b exp/方案B  main
   ```

2. **两个分支独立实施，不交叉**。
   - 代码变更：按 agentprecept 标准流程（设计先行 → 确认 → 代码 → 测试）
   - 每次代码变更后自动 sync project-graph
   - 每个决策追加 L4_O01

3. **全链路审计**（不在 main 上执行）：
   ```bash
   # 文档审计（--gate 开启全部 15 维）
   python scripts/basic-audit.py docs/ --gate

   # 代码 lint（按项目工具链适配）
   ruff check src/ 2>/dev/null || pylint src/ 2>/dev/null

   # 测试
   pytest tests/ -q 2>/dev/null || python -m pytest tests/ -q
   ```
   至少跑文档审计 + 测试。Agent 不只是用来写文档的——审计不能只审 docs/。

4. **对比后选优合并**：
   ```bash
   git checkout main
   git merge exp/方案A   # 选择方案 A
   git branch -d exp/方案B
   ```

5. **合并 project-graph**（两条分支各自产出不同的图）：
   - 优先保留 merge 目标分支（方案 A）的 project-graph
   - 如果方案 B 有 A 没有的 relations，手动补充
   - 合并后立即跑 sync 确认无冲突

6. **原始 main 备份**：
   ```bash
   git branch main-backup main~1   # 保留合并前状态 30 天
   ```

7. **确认稳定后删除备份**：
   ```bash
   git branch -d main-backup
   ```

### 为什么不是 feature 分支

feature 分支只有一条路径。双分支同时验证两种选择，
成本是 2 倍实现时间，收益是避免合并后推倒重来的风险。

### 适用场景

- 架构重构（新老结构全链路对比）
- 技术选型替换（如 Peewee → SQLAlchemy，对比 model 定义/迁移/测试）
- agentprecept 集成（方案 A 纯文档 / 方案 B 文档+代码提升）

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| 项目接入 | `agentprecept init` 6 阶段 | `agentprecept init /project` |
| 代码同步 | `agentprecept sync` | `agentprecept sync` |
| 审计 | `agentprecept audit --gate` 15 维 | `agentprecept audit --gate` |
| 提交门禁 | pre-commit 4 gates | git commit 自动触发 |
| CI 门禁 | GitHub Actions PR 审计 | `agentprecept audit --gate` |
