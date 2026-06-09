# scripts/ — AgentPrecept 辅助脚本

**依赖**: Python 3.10+ + PyYAML (`pip install pyyaml`)

CLI 入口: `pip install -e .` → `agentprecept init|sync|audit|setup|hooks|gnhf`

---

| 脚本 | 用途 | 用法 |
|------|------|------|
| `init.ps1` | Windows 一键生成核心文档骨架 | `.\init.ps1 C:\path\to\project` |
| `init.sh` | Linux/macOS 一键生成核心文档骨架 | `bash init.sh /path/to/project` |
| `sync-graph.py` | 6 维代码扫描，自动同步 project-graph | `python sync-graph.py src/ docs/project-graph.yaml` |
| `basic-audit.py` | 15 维 4-scope 自动化审计（--gate 模式） | `python basic-audit.py docs/ --scope all` |
| `ripple_check.py` | 涟漪分析：修改一个文件影响哪些文件 | `python ripple_check.py docs/project-graph.yaml <changed-file>` |
| `design_gate_check.py` | 代码修改前设计文档前置检查（MCP + hook 共享单源码） | `python design_gate_check.py docs/ <changed-files>` |
| `check-naming.py` | 命名规范检查 | `python check-naming.py docs/` |
| `graph-to-mermaid.py` | project-graph → Mermaid 可视化 | `python graph-to-mermaid.py docs/project-graph.yaml` |

## 审计

`basic-audit.py` 执行 15 维 4-scope 自动化审计：

| scope | 覆盖 | 维度数 |
|-------|------|:--:|
| `docs` | 命名/引用/编号/骨架/图格式/设计追溯/覆盖率/狗粮/声明校验/设计覆盖 | 10 |
| `code` | 一致性 + 逻辑内核 | 2 |
| `git` | 分支策略 + commit 粒度 | 2 |
| `config` | 工具链配置 | 1 |

`--gate` 模式零 FAIL 才算通过。`--scope docs` 只看文档层。

4 维自选清单（用户旅程/定位审计/复用/社区就绪度）在报告末尾提示，需人工判定。

## 涟漪分析

`ripple_check.py` 读取 project-graph 的 relations，分析修改一个文件后的影响范围：

```
DIRECT    — 直接依赖被改文件
INDIRECT  — 通过 DIRECT 传递
SAME_PKG  — 同目录下，建议检查
```

## 设计门禁

`design_gate_check.py` 在代码修改前检查是否已有对应设计文档就位。同一份源码被 MCP `design_gate` tool 和 pre-commit hook Gate 2 共享调用——两个入口，一个实现，不漂移。

## 集成到 CI

```yaml
- name: 15维审计
  run: agentprecept audit --gate
- name: 命名检查
  run: python scripts/check-naming.py docs/
```
