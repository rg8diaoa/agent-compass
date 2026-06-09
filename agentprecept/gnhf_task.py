"""gnHF 任务模板生成器

用法: python agentprecept/gnhf_task.py [output_path]

读取当前 project-graph 状态 + git diff 摘要,
渲染为 gnhf --goal 可消费的 markdown 任务模板。
"""
import sys
import subprocess
from pathlib import Path


def git_diff_summary() -> str:
    """获取自上次 sync 以来的代码变更摘要"""
    try:
        result = subprocess.run(
            ["git", "diff", "--stat", "HEAD"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() or "(无变更)"
    except Exception:
        return "(无法获取 git diff)"


def current_graph_state() -> str:
    """读取 project-graph 的概要统计"""
    graph_path = Path("docs/project-graph.yaml")
    if not graph_path.exists():
        return "project-graph.yaml 不存在——首次同步"

    import yaml
    doc = yaml.safe_load(graph_path.read_text(encoding="utf-8")) or {}
    structure = doc.get("structure", {})
    relations = doc.get("relations", [])
    evolution = doc.get("evolution", [])

    from collections import Counter
    type_counts = Counter(r.get("type") for r in relations)

    return f"""structure: {len(structure)} 个包/模块
relations: {len(relations)} 条依赖
  types: {', '.join(f'{t}:{c}' for t, c in sorted(type_counts.items()))}
evolution: {len(evolution)} 条 ADR"""


def render_template(output_path: str = ".gnhf/sync-task.md") -> str:
    """生成 gnhf 任务模板"""
    diff = git_diff_summary()
    state = current_graph_state()

    template = f"""# agentprecept: Auto-Sync Task

## 目标
根据最新代码结构更新 `docs/project-graph.yaml`。

## 当前知识库状态
{state}

## 代码变更摘要
```
{diff}
```

## 执行规则
1. 运行 `python -m agentprecept.sync_graph src docs/project-graph.yaml`
2. 同步完成后运行 `python -m agentprecept audit docs/`
3. 如果 audit 无 FAIL: 任务完成
4. 如果 audit 有 FAIL: 修复对应问题后重新 audit
5. structure 中的 stability 和 description 字段必须保留
6. relations 全量替换——代码 import 是唯一真实来源
7. evolution 追加新的 ADR，不动已有的

## 期望输出
- `docs/project-graph.yaml` 已更新
- `python -m agentprecept audit docs/` exit 0
- 提交信息: `auto-sync: update project-graph ({len(diff.splitlines())} files changed)`
"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template, encoding="utf-8")
    return template


def main():
    output = sys.argv[1] if len(sys.argv) > 1 else ".gnhf/sync-task.md"
    template = render_template(output)
    print(f"[gnhf] 任务模板已生成: {output}")
    print(f"[gnhf] 使用方法: gnhf --agent claude --goal {output} --verify 'python -m agentprecept audit docs/'")


if __name__ == "__main__":
    main()