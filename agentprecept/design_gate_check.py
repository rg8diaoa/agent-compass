"""design_gate check — MCP tool 和 git hook 共享的检查逻辑

用法:
  python -m agentprecept.design_gate_check --files src/a.py src/b.py    # git hook 调用
  python -m agentprecept.design_gate_check --module src/services        # MCP tool 调用

exit 0: 全部通过
exit 1: 有缺失——设计文档需创建
exit 2: project-graph.yaml 不存在

--json: 输出 JSON 格式
"""
import sys
import json
from pathlib import Path

GRAPH_PATH = Path("docs/project-graph.yaml")


def load_graph():
    if not GRAPH_PATH.exists():
        return None
    import yaml
    return yaml.safe_load(GRAPH_PATH.read_text(encoding="utf-8")) or {}


def find_module(graph, file_path):
    """根据文件路径查找所属模块的 structure 条目"""
    structure = graph.get("structure", {})
    # 精确匹配
    if file_path in structure:
        return file_path, structure[file_path]
    # 前缀匹配（取最长匹配）
    best = None
    best_key = None
    for key in structure:
        if file_path.startswith(key.rstrip("/")) and (best is None or len(key) > len(best_key)):
            best = structure[key]
            best_key = key
    if best and isinstance(best, dict):
        return best_key, best
    return None, {}


def check_design_docs(graph, targets):
    """检查目标文件所需的设计文档"""
    results = []
    for target in targets:
        mod_key, mod_meta = find_module(graph, target)
        design_docs = mod_meta.get("design_docs", []) if isinstance(mod_meta, dict) else []

        if not design_docs:
            continue

        for dd in design_docs:
            matches = list(Path("docs").glob(f"{dd}*.md"))
            if not matches:
                results.append({
                    "target": target,
                    "module": mod_key or "(unknown)",
                    "design_doc": dd,
                    "status": "missing",
                    "action": "create_first"
                })
            else:
                for mf in matches:
                    content = mf.read_text(encoding="utf-8")
                    skeleton = "placeholder" in content or "TODO:" in content
                    if skeleton:
                        results.append({
                            "target": target,
                            "module": mod_key or "(unknown)",
                            "design_doc": mf.name,
                            "status": "skeleton",
                            "action": "fill_content"
                        })
    return results


def main():
    json_mode = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    graph = load_graph()
    if graph is None:
        if json_mode:
            print(json.dumps({"status": "WARN", "gates": [], "message": "project-graph.yaml not found"}))
        else:
            print("[design_gate] WARN: project-graph.yaml not found")
        sys.exit(2)

    # 解析输入
    targets = []
    module_mode = False
    for i, arg in enumerate(args):
        if arg == "--files":
            targets.extend(args[i+1:])
            break
        elif arg == "--module":
            module_mode = True
            targets.append(args[i+1])
            break

    results = check_design_docs(graph, targets)

    if not results:
        if json_mode:
            print(json.dumps({"status": "CLEAR", "gates": [], "message": "all design docs ready"}))
        sys.exit(0)

    if json_mode:
        blocked = any(r["status"] in ("missing", "skeleton") for r in results)
        output = {
            "status": "BLOCKED" if blocked else "CLEAR",
            "gates": results,
            "message": f"{len(results)} design doc(s) need attention"
        }
        print(json.dumps(output))
    else:
        for r in results:
            print(f"[design_gate] {r['target']} -> {r['design_doc']}: {r['status']} ({r['action']})")

    sys.exit(1 if any(r["status"] == "missing" for r in results) else 0)


if __name__ == "__main__":
    main()