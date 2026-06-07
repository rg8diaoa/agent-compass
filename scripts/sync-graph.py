"""从代码自动同步 project-graph.yaml 的结构层和关系层

用法: python scripts/sync-graph.py src/ docs/project-graph.yaml

用 tree 生成结构层（不覆盖 stability 和 description），
多维度扫描生成关系层（全量替换 relations）：
  - depends_on: Python import（符号级）
  - maps_to:    ORM model → DB table
  - exposes:    模块 → API 端点 / 页面挂载
  - routes:     页面 → 页面导航
  - calls:      函数 → 外部服务
不覆盖 evolution 层和人类手动修改的条目。
"""
import os, re, sys, yaml
from pathlib import Path

# 标准库 + 常见第三方库首段（被排除，不记录为项目依赖）
STDLIB_ROOTS = {
    # Python 标准库
    "os", "sys", "re", "json", "logging", "datetime",
    "typing", "pathlib", "collections", "functools",
    "dataclasses", "enum", "abc", "contextlib", "itertools",
    "math", "random", "hashlib", "uuid", "io", "time",
    "threading", "subprocess", "shutil", "tempfile", "atexit",
    "copy", "textwrap", "argparse", "traceback", "warnings",
    "unittest", "doctest", "pdb",
    # 常见第三方
    "fastapi", "uvicorn", "pytest", "sqlalchemy",
    "pydantic", "flask", "django", "asyncio", "peewee",
}

# 外部服务调用模式（函数调用 → 外部服务标注）
EXTERNAL_PATTERNS = [
    (r'OpenAI\(', "openai:chat.completions"),
    (r'openai\.([a-zA-Z.]+)\s*\(', None),  # 动态捕获: openai.chat.completions.create()
    (r'requests\.(get|post|put|delete|patch)\s*\(', None),
    (r'Fernet\(', "cryptography:fernet"),
    (r'boto3\.client\s*\(\s*["\'](\w+)["\']', None),
    (r'httpx\.(get|post|put|delete)\s*\(', None),
]


def build_structure(src_dir: str) -> dict:
    """从目录树生成结构层"""
    structure = {}
    src = Path(src_dir)
    if not src.exists():
        return structure

    for d in sorted(src.glob("**/")):
        if d.name.startswith(".") or d.name.startswith("_"):
            continue
        rel = str(d.relative_to(src.parent))
        children = [f.name for f in sorted(d.glob("*.py")) if not f.name.startswith("_")]
        if children or d == src:
            structure[rel] = {
                "type": "package",
                "stability": "stable",
                "children": children,
            }
    return structure


def _prep_imports(content: str) -> str:
    """续行符/括号内换行 → 单行"""
    content = re.sub(r'\\\s*\n\s*', ' ', content)
    content = re.sub(r'\(\s*\n\s*', '(', content)
    content = re.sub(r'\n\s*\)', ')', content)
    return content


def build_relations(src_dir: str) -> list:
    """维度 1: Python import（符号级）"""
    from_import_re = re.compile(r'^from\s+(\S+)\s+import\s+(.+?)$', re.MULTILINE)
    import_re = re.compile(r'^import\s+(.+?)$', re.MULTILINE)
    src = Path(src_dir)
    relations = []
    seen = set()

    for f_py in sorted(src.glob("**/*.py")):
        if f_py.name.startswith("_") or f_py.name.startswith("test"):
            continue
        content = _prep_imports(f_py.read_text(encoding="utf-8"))
        rel = str(f_py.relative_to(src.parent)).replace("\\", "/")

        for m in from_import_re.finditer(content):
            module = m.group(1)
            root = module.split(".")[0]
            if root in STDLIB_ROOTS:
                continue
            for sym in m.group(2).split(","):
                sym = sym.strip()
                if not sym or sym == "*":
                    continue
                key = (rel, f"{module}.{sym}", "depends_on")
                if key not in seen:
                    seen.add(key)
                    relations.append({
                        "from": rel,
                        "to": f"{module}.{sym}",
                        "type": "depends_on",
                    })

        for m in import_re.finditer(content):
            for module in m.group(1).split(","):
                module = module.strip()
                if not module:
                    continue
                root = module.split(".")[0]
                if root in STDLIB_ROOTS:
                    continue
                key = (rel, module, "depends_on")
                if key not in seen:
                    seen.add(key)
                    relations.append({
                        "from": rel,
                        "to": module,
                        "type": "depends_on",
                    })

    return relations


def build_db_relations(src_dir: str) -> list:
    """维度 2: ORM model → DB table（Peewee / SQLAlchemy）"""
    # class X(Model): 或 class X(BaseModel):
    model_re = re.compile(r'^class\s+(\w+)\s*\(\s*(?:\w+\.)?(?:Model|BaseModel)\s*\)\s*:', re.MULTILINE)
    # class Meta: / table_name = 'xxx' / __tablename__ = 'xxx'
    table_re = re.compile(r"(?:table_name|__tablename__)\s*=\s*['\"](\w+)['\"]")
    fk_re = re.compile(r'(?:ForeignKeyField|ForeignKey)\s*\(\s*[\'"]?(\w+)\.(\w+)[\'"]?')
    src = Path(src_dir)
    relations = []
    seen = set()

    for f_py in sorted(src.glob("**/*.py")):
        if f_py.name.startswith("_") or f_py.name.startswith("test"):
            continue
        content = f_py.read_text(encoding="utf-8")
        rel = str(f_py.relative_to(src.parent)).replace("\\", "/")

        for m in model_re.finditer(content):
            model_name = m.group(1)
            model_pos = m.end()

            # 在这个 model 定义后面的内容里找 table_name
            tail = content[model_pos:model_pos + 2000]  # 只搜 2000 字，够用
            table_match = table_re.search(tail)
            table_name = table_match.group(1) if table_match else model_name.lower() + "s"

            # model → table
            key = (f"{rel}:{model_name}", table_name, "maps_to")
            if key not in seen:
                seen.add(key)
                relations.append({
                    "from": f"{rel}:{model_name}",
                    "to": table_name,
                    "type": "maps_to",
                })

            # 外键: model → 其他 model
            for fk in fk_re.finditer(tail):
                ref_model = fk.group(1)  # Tag → DiaryTag
                key = (f"{rel}:{model_name}", f"{rel}:{ref_model}", "maps_to")
                if key not in seen:
                    seen.add(key)
                    relations.append({
                        "from": f"{rel}:{model_name}",
                        "to": f"{rel}:{ref_model}",
                        "type": "maps_to",
                    })

    return relations


def build_api_relations(src_dir: str) -> list:
    """维度 3: 模块 → API 端点 / 页面挂载"""
    # FastAPI: @app.get("/path")
    fastapi_re = re.compile(r'@\w+\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']')
    # Flet: page.add(X) / page.controls.append(X)
    flet_re = re.compile(r'(?:page|self)\.(?:add|controls\.append)\s*\(\s*(\w+)')
    # view.push() / go()
    view_re = re.compile(r'(?:page\.go|view\.push)\s*\(\s*["\']([^"\']+)["\']')
    src = Path(src_dir)
    relations = []
    seen = set()

    for f_py in sorted(src.glob("**/*.py")):
        if f_py.name.startswith("_") or f_py.name.startswith("test"):
            continue
        content = f_py.read_text(encoding="utf-8")
        rel = str(f_py.relative_to(src.parent)).replace("\\", "/")

        # FastAPI 端点
        for m in fastapi_re.finditer(content):
            method, path = m.group(1).upper(), m.group(2)
            key = (rel, f"{method} {path}", "exposes")
            if key not in seen:
                seen.add(key)
                relations.append({
                    "from": rel,
                    "to": f"{method} {path}",
                    "type": "exposes",
                })

        # Flet 页面挂载
        for m in flet_re.finditer(content):
            widget = m.group(1)
            key = (rel, f"widget:{widget}", "mounts")
            if key not in seen:
                seen.add(key)
                relations.append({
                    "from": rel,
                    "to": f"widget:{widget}",
                    "type": "mounts",
                })

        # 页面路由（GoRouter / Flet 路由）
        for m in view_re.finditer(content):
            route = m.group(1)
            key = (rel, route, "routes")
            if key not in seen:
                seen.add(key)
                relations.append({
                    "from": rel,
                    "to": route,
                    "type": "routes",
                })

    return relations


def build_frontend_relations(src_dir: str) -> list:
    """维度 4: 前端导航（NavigationBar → pages）"""
    # Flet NavigationBar destination label → UI 文件
    nav_re = re.compile(r'NavigationBarDestination\s*\([^)]*?label\s*=\s*["\']([^"\']+)["\']', re.DOTALL)
    # on_change 回调中的条件分发（index → 页面构建）
    route_re = re.compile(r'if\s+.*?(?:index|e\.control\.selected_index)\s*==\s*(\d+)\s*:')
    src = Path(src_dir)
    relations = []
    seen = set()
    nav_labels = []

    for f_py in sorted(src.glob("**/*.py")):
        if f_py.name.startswith("_") or f_py.name.startswith("test"):
            continue
        content = f_py.read_text(encoding="utf-8")
        rel = str(f_py.relative_to(src.parent)).replace("\\", "/")

        # 收集所有导航标签
        for m in nav_re.finditer(content):
            nav_labels.append((rel, m.group(1)))

        # 路由分发
        for m in route_re.finditer(content):
            idx = int(m.group(1))
            if idx < len(nav_labels):
                nav_rel, label = nav_labels[idx]
                key = (nav_rel, label, "routes")
                if key not in seen:
                    seen.add(key)
                    relations.append({
                        "from": nav_rel,
                        "to": label,
                        "type": "routes",
                    })

    return relations


def build_external_relations(src_dir: str) -> list:
    """维度 5: 函数 → 外部服务"""
    func_re = re.compile(r'^def\s+(\w+)\s*\(', re.MULTILINE)
    src = Path(src_dir)
    relations = []
    seen = set()

    for f_py in sorted(src.glob("**/*.py")):
        if f_py.name.startswith("_") or f_py.name.startswith("test"):
            continue
        content = f_py.read_text(encoding="utf-8")
        rel = str(f_py.relative_to(src.parent)).replace("\\", "/")

        # 找到每个函数定义，然后在其后续内容中搜索外部调用
        for func_m in func_re.finditer(content):
            func_name = func_m.group(1)
            func_start = func_m.end()
            tail = content[func_start:func_start + 3000]

            for pat, static_to in EXTERNAL_PATTERNS:
                for call_m in re.finditer(pat, tail):
                    if static_to:
                        to_val = static_to
                    elif call_m.lastindex and call_m.lastindex >= 1:
                        to_val = call_m.group(0).split("(")[0].strip()
                    else:
                        to_val = call_m.group(0).split("(")[0].strip()

                    key = (f"{rel}:{func_name}", to_val, "calls")
                    if key not in seen:
                        seen.add(key)
                        relations.append({
                            "from": f"{rel}:{func_name}",
                            "to": to_val,
                            "type": "calls",
                        })

    return relations


def main():
    src_dir = sys.argv[1] if len(sys.argv) > 1 else "src"
    graph_path = sys.argv[2] if len(sys.argv) > 2 else "docs/project-graph.yaml"

    graph_file = Path(graph_path)
    if graph_file.exists():
        existing = yaml.safe_load(graph_file.read_text(encoding="utf-8")) or {}
    else:
        existing = {}

    new_structure = build_structure(src_dir)
    old_structure = existing.get("structure") or {}
    for k, v in new_structure.items():
        if k not in old_structure:
            old_structure[k] = v
        else:
            old_structure[k].update(
                {kk: vv for kk, vv in v.items()
                 if kk not in old_structure[k]}
            )

    # 全量替换——代码是唯一真实来源
    all_relations = []
    all_relations.extend(build_relations(src_dir))
    all_relations.extend(build_db_relations(src_dir))
    all_relations.extend(build_api_relations(src_dir))
    all_relations.extend(build_frontend_relations(src_dir))
    all_relations.extend(build_external_relations(src_dir))

    existing["relations"] = all_relations
    existing["structure"] = old_structure
    existing.setdefault("evolution", [])

    graph_file.write_text(yaml.dump(existing, allow_unicode=True, sort_keys=False, default_flow_style=False),
                          encoding="utf-8")

    # 统计各 type 数量
    type_counts = {}
    for r in all_relations:
        t = r["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    type_summary = " / ".join(f"{t}:{c}" for t, c in sorted(type_counts.items()))

    print(f"[OK] project-graph synced: {len(old_structure)} structure / {len(all_relations)} relations / {len(existing['evolution'])} evolution")
    print(f"     types: {type_summary}")


if __name__ == "__main__":
    main()
