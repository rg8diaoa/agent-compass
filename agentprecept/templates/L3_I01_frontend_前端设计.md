# 前端设计

> 分类: I | 层级: L3 | 编号: L3_I01
> 状态: ⏳ 待撰写 | 目标读者: 前端开发者
> 前置阅读: L2_D01_architecture_架构设计.md

---

## §1 技术栈

<!-- AGENT: 读取 L2_D01，列出前端技术选型 -->

| 层 | 选择 | 原因 |
|------|------|------|
| 框架 | _React / Vue / Svelte_ | _见 L4_O01_ |
| 状态管理 | | |
| 路由 | | |
| UI 库 | | |
| 构建工具 | | |

## §2 组件树

<!-- AGENT: 读取 L2_G01（数据结构）和 project-graph.yaml，生成组件树 -->
<!-- 两个维度：路由结构 + 组件层级 -->

```
App
├── Layout
│   ├── Header（导航 + 用户信息）
│   └── Sidebar
├── Pages
│   ├── LoginPage
│   ├── TaskListPage
│   └── TaskDetailPage
└── Shared
    ├── Button
    ├── Modal
    └── FormField
```

## §3 状态管理

<!-- AGENT: 列出全局状态、组件状态、缓存策略 -->

| 状态 | 类型 | 存储位置 |
|------|------|------|
| 用户认证 | 全局 | _localStorage + context_ |
| 任务列表 | 服务端 | _API + 内存缓存_ |

## §4 API 对接

<!-- AGENT: 读取 L2_G01（API 规范），生成前端 API 调用映射 -->

| 组件 | API 端点 | 触发时机 |
|------|------|------|
| TaskListPage | GET /tasks | 页面加载 |
| TaskDetailPage | PUT /tasks/{id} | 用户点击保存 |
