# MCP Tools 参考

agentprecept 通过 MCP Server 暴露 6 个 tool，供任何支持 MCP 的 Agent 调用。

## 启动

```bash
compass-mcp
# 或
python -m agentprecept.mcp_server
```

前置条件：`pip install fastmcp`

## Tool 列表

> **Tool vs Resource**：agentprecept 当前仅提供 MCP Tools（可调用的函数），不提供 MCP Resources（只读数据资源）。两者区别：Tool 是模型主动调用的 RPC 操作（如审计、查询），Resource 是模型被动读取的数据（如文件内容）。未来版本可能为 HANDOFF、project-graph 等高频读取数据追加 Resource 支持。

### 1. project_graph_query

查询项目图信息。

```json
// 请求
{
  "module": "src/services",
  "query_type": "relations"
}

// 响应
{
  "relations": [
    {"from": "src/services/diary_service.py", "to": "src.models.diary.DiaryEntry", "type": "depends_on"},
    ...
  ],
  "count": 15
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| module | string | 模块名（留空=全部），如 "src/services" |
| query_type | string | "structure" / "relations" / "evolution" / "all" |

### 2. audit_run

运行 15 维自动化审计（--gate 模式）。默认 8 维，--gate 追加维度 9-15。

```json
// 请求
{
  "docs_dir": "docs"
}

// 响应
{
  "results": [
    {"dimension": "命名一致性", "status": "PASS", "findings": []},
    ...
  ],
  "summary": {"FAIL": 0, "WARN": 1, "PASS": 7}
}
```

| 参数 | 类型 | 默认 |
|------|------|------|
| docs_dir | string | "docs" |

### 3. sync_diff

dry-run 同步——不写文件，返回待变更清单。

```json
// 请求
{
  "src_dir": "src"
}

// 响应
{
  "structure": {"added": ["src/new_module"], "removed": []},
  "relations": {"added": 5, "removed": 1, "total_new": 84},
  "type_counts": {"depends_on": 76, "maps_to": 5, "calls": 2, "mounts": 1},
  "needs_sync": true
}
```

### 4. decision_search

搜索设计依据。

```json
// 请求
{
  "query": "Peewee"
}

// 响应
[
  "| 为什么选择 Peewee 而非 SQLAlchemy | ORM 选型 | 项目规模小（5 model），Peewee 更轻量；未来如有复杂查询需求再迁移 |"
]
```

### 5. handoff_read

读取会话交接状态。

```json
// 请求
{}

// 响应
{
  "status": "[IN_PROGRESS]",
  "next_step": "1. 完成 MCP Server 验证 2. 切到 gnhf 集成分支",
  "file_exists": true
}
```

### 6. design_gate

Agent 准备修改代码前调用。返回模块的前置设计文档状态。

```json
// design_gate(module="src/services", operation="modify")
{
  "status": "BLOCKED",
  "gates": [
    {
      "type": "design_document",
      "name": "L2_D01",
      "status": "missing",
      "action": "create_first",
      "template": "templates/L2_D01*.md"
    },
    {
      "type": "design_document",
      "name": "L4_O01_design-rationale.md",
      "status": "skeleton",
      "action": "fill_content",
      "path": "docs/L4_O01_design-rationale.md"
    }
  ],
  "message": "module src/services: design docs need creation or filling"
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| module | string | 模块路径，如 "src/services" |
| operation | string | "modify" / "create" |

**返回值：**

| 字段 | 说明 |
|------|------|
| status | "CLEAR" / "WARN" / "BLOCKED" |
| gates | 每个前置文档的状态（exists/missing/skeleton）和动作（none/create_first/fill_content） |
| message | 人类可读的摘要 |

---

## 在 Code Agent 中配置

### Claude Code

```json
// .mcp.json
{
  "mcpServers": {
    "agentprecept": {
      "command": "python",
      "args": ["-m", "agentprecept.mcp_server"]
    }
  }
}
```

### CodeWhale

编辑 `~/.deepseek/mcp.json`（或通过 `codewhale mcp add` 命令）：

```json
{
  "mcpServers": {
    "agentprecept": {
      "command": "python",
      "args": ["-m", "agentprecept.mcp_server"],
      "cwd": "/path/to/agentprecept",
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1"
      }
    }
  }
}
```

> **Windows 注意**：`PYTHONIOENCODING=utf-8` 和 `PYTHONUTF8=1` 可防止 GBK 编码损坏 MCP 握手消息。

### Cursor / OpenCode

```json
{
  "mcpServers": {
    "agentprecept": {
      "command": "python",
      "args": ["-m", "agentprecept.mcp_server"]
    }
  }
}
```
