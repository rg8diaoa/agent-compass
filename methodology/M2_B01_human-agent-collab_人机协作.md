# 12 — 人机协作：Agent 如何与人类对话

> **AgentPrecept 落地**: `[NEEDS_HUMAN_REVIEW]` 机制 → pre-commit Gate 4 + AGENTS.md 规则，详见文末。

> Agent 不是替代人类——是辅助。这一篇讲 Agent 什么时候该停下来、什么时候该追问、什么时候该等确认。

---

## 核心原则

1. **不确定就不做**。宁可停下来问，不可猜
2. **动工前复述理解**。让人类确认"你说的对"
3. **影响面大就列出来**。不要默默改完让人类发现

---

## 需求澄清：先问再动手

```
用户: "加一个优先级字段"

❌ Agent 直接写: ALTER TABLE tasks ADD priority_level TEXT;

✅ Agent 追问:
   "几个问题确认一下:
   ① 优先级是全局固定级别（P0-P3）还是每个项目可自定义？
   ② 排序在数据库层做（ORDER BY）还是应用层排？
   ③ 默认值应该是什么？"

规则: 任何新需求 → Agent 至少追问 1 个澄清问题 → 人类回复后才能动工
```

---

## 不懂就停：不许猜

```
用户: "用 CQRS 模式重构订单模块"

❌ Agent: 搜索 CQRS 后开始写代码

✅ Agent: "我对 CQRS 的理解是读写分离——Command 处理写操作，Query 处理读操作。
   在动手前确认: 你要的是这个模式吗？还是指某个具体框架？"
```

规则: 任何不确定的概念/工具/术语 → 用自己的话复述理解 → 等人类确认

---

## 动工前复述

```
用户: "把 auth 改成 OAuth2"

✅ Agent 复述:
   "我理解你要:
    ① 替换 src/auth/ 中的手动 JWT 逻辑
    ② 引入 OAuth2 库
    ③ 保持 /login 接口不变
   
   影响范围: login.py / middleware.py / admin.py（3 个文件）
   
   确认后开始？"
```

规则: 涉及 > 2 个文件的改动 → 先列影响范围 → 等确认

---

## 人类决策节点

Agent 遇到以下情况 → 标注 [NEEDS_HUMAN_DECISION]，在 HANDOFF 中列出方案供选择:

- 两个技术方案没有明确优劣
- 改动影响 > 5 个模块
- 可能破坏现有 API 兼容性
- 涉及安全/权限/密钥

---

## 人类审查节点

Agent 完成以下动作后 → HANDOFF 标注 [NEEDS_HUMAN_REVIEW]:

- 新增 > 3 个文件
- 修改 project-graph.yaml 结构层
- 做了新设计决策 → L4_O01 标注"待确认"

---

## 沉默处理

人类 3 轮无反馈 → Agent 不停下来循环尝试 → 停止并将当前状态写入 HANDOFF，状态改为 [BLOCKED]

---

## AgentPrecept 工程化落地

| 理念 | 实现 | 使用方式 |
|------|------|----------|
| 设计确认 | `[NEEDS_HUMAN_REVIEW]` 机制 | AGENTS.md 规则强制 |
| 提交拦截 | pre-commit Gate 4 | git commit 自动触发 |
| 互动模式 | AGENTS.md 讨论阶段拦截 | Agent 自动执行 |
