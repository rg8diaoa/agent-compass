"""agentprecept 审计脚本 — 10 维自动化审计

用法: python scripts/basic-audit.py docs/
      python scripts/basic-audit.py docs/ --gate  # 开启维度 9+10
输出: 十维审计报告（markdown）
"""
import os, re, sys
from pathlib import Path


def check_naming(docs_dir: str) -> list[dict]:
    """维度 1: 文件名是否符合 L{Level}_{CAT}{NN}_{Slug}_{Title}.md"""
    pattern = r'^L[1-4]_[A-P]\d{2}_[a-z0-9-]+_.+\.md$'
    findings = []
    for f in Path(docs_dir).glob("*.md"):
        if not f.name.startswith("L"):
            continue
        if not re.match(pattern, f.name):
            findings.append({"file": f.name, "issue": "命名不符合规范", "severity": "FAIL"})
    return findings


def check_broken_links(docs_dir: str) -> list[dict]:
    """维度 2: 交叉引用断链"""
    findings = []
    for f in Path(docs_dir).glob("*.md"):
        content = f.read_text(encoding="utf-8")
        refs = re.findall(r'\(([^)]+\.md)\)', content)
        for ref in refs:
            target = (f.parent / ref.split("#")[0]).resolve()
            if not target.exists():
                findings.append({
                    "file": f.name,
                    "issue": f"引用不存在: {ref}",
                    "severity": "FAIL"
                })
    return findings


def check_numbering(docs_dir: str) -> list[dict]:
    """维度 3: 编号连续性 — 分类内 NN 是否从 01 连续无跳跃"""
    pattern = re.compile(r'^L([1-4])_([A-P])(\d{2})_')
    findings = []
    groups = {}

    for f in Path(docs_dir).glob("L*.md"):
        m = pattern.match(f.name)
        if not m:
            continue
        level, cat, nn = m.group(1), m.group(2), int(m.group(3))
        key = (level, cat)
        groups.setdefault(key, []).append(nn)

    for (level, cat), nns in sorted(groups.items()):
        nns.sort()
        if nns[0] != 1:
            findings.append({
                "file": f"L{level}_{cat}*",
                "issue": f"编号从 {nns[0]:02d} 开始（应从 01 开始）",
                "severity": "WARN"
            })
        for i in range(len(nns) - 1):
            gap = nns[i+1] - nns[i]
            if gap > 1:
                findings.append({
                    "file": f"L{level}_{cat}*",
                    "issue": f"编号跳跃: {nns[i]:02d} -> {nns[i+1]:02d}（缺 {gap-1} 个编号）",
                    "severity": "WARN"
                })
    return findings


def check_skeleton(docs_dir: str) -> list[dict]:
    """维度 4: 骨架残留 — placeholder / TODO / FIXME / TBD"""
    findings = []
    for f in Path(docs_dir).glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if "placeholder" in content:
            findings.append({
                "file": f.name,
                "issue": "含 placeholder 待撰写标记",
                "severity": "WARN"
            })
        else:
            for marker in ["TODO:", "TODO ", "FIXME:", "FIXME ", "TBD:", "TBD "]:
                if marker in content:
                    findings.append({
                        "file": f.name,
                        "issue": f"含 {marker.strip()}",
                        "severity": "WARN"
                    })
                    break
    return findings


def check_graph_schema(docs_dir: str) -> list[dict]:
    """维度 5: project-graph.yaml 格式校验"""
    graph_path = Path(docs_dir) / "project-graph.yaml"
    findings = []

    if not graph_path.exists():
        findings.append({
            "file": "project-graph.yaml",
            "issue": "文件不存在",
            "severity": "FAIL"
        })
        return findings

    try:
        import yaml
    except ImportError:
        findings.append({
            "file": "project-graph.yaml",
            "issue": "PyYAML 未安装，无法校验格式",
            "severity": "WARN"
        })
        return findings

    try:
        doc = yaml.safe_load(graph_path.read_text(encoding="utf-8"))
    except Exception as e:
        findings.append({
            "file": "project-graph.yaml",
            "issue": f"YAML 解析失败: {e}",
            "severity": "FAIL"
        })
        return findings

    if doc is None:
        findings.append({
            "file": "project-graph.yaml",
            "issue": "文件为空或全为注释",
            "severity": "FAIL"
        })
        return findings

    valid_top_keys = {"structure", "relations", "evolution"}
    actual_keys = set(doc.keys())
    extra_keys = actual_keys - valid_top_keys
    if extra_keys:
        findings.append({
            "file": "project-graph.yaml",
            "issue": f"top-level 含非标准键: {extra_keys}（标准: structure/relations/evolution）",
            "severity": "FAIL"
        })

    structure = doc.get("structure")
    if structure is None:
        findings.append({
            "file": "project-graph.yaml",
            "issue": "structure 字段为空（应为 {}）",
            "severity": "FAIL"
        })
    elif isinstance(structure, dict):
        for path, meta in structure.items():
            if not isinstance(meta, dict):
                findings.append({
                    "file": "project-graph.yaml",
                    "issue": f"structure.{path} 不是字典",
                    "severity": "FAIL"
                })
                continue
            if "type" not in meta:
                findings.append({
                    "file": "project-graph.yaml",
                    "issue": f"structure.{path} 缺 type 字段",
                    "severity": "FAIL"
                })
            if "description" not in meta and "children" not in meta:
                findings.append({
                    "file": "project-graph.yaml",
                    "issue": f"structure.{path} 既无 description 也无 children",
                    "severity": "WARN"
                })

    relations = doc.get("relations")
    if relations is None:
        findings.append({
            "file": "project-graph.yaml",
            "issue": "relations 字段为空（应为 []）",
            "severity": "WARN"
        })
    elif isinstance(relations, list):
        valid_types = {"depends_on", "references", "indexes", "extends", "demonstrates", "tests",
                       "maps_to", "exposes", "calls", "routes", "mounts", "validates",
                       "import", "reference", "read", "write"}
        for i, rel in enumerate(relations):
            if not isinstance(rel, dict):
                findings.append({
                    "file": "project-graph.yaml",
                    "issue": f"relations[{i}] 不是字典",
                    "severity": "FAIL"
                })
                continue
            for field in ["from", "to", "type"]:
                if field not in rel:
                    findings.append({
                        "file": "project-graph.yaml",
                        "issue": f"relations[{i}] 缺 {field} 字段",
                        "severity": "FAIL"
                    })
            if rel.get("type") and rel["type"] not in valid_types:
                findings.append({
                    "file": "project-graph.yaml",
                    "issue": f"relations[{i}].type='{rel['type']}' 不在标准值中 ({valid_types})",
                    "severity": "WARN"
                })
            to_val = rel.get("to")
            if isinstance(to_val, list):
                findings.append({
                    "file": "project-graph.yaml",
                    "issue": f"relations[{i}].to 是列表（应为字符串），标准格式不支持 to: [...]",
                    "severity": "FAIL"
                })

    return findings


def check_design_trace(docs_dir: str) -> list[dict]:
    """维度 6: 设计追溯 — L4_O01 是否存在 + 是否有足够内容"""
    findings = []
    l4_path = Path(docs_dir) / "L4_O01_design-rationale_设计依据.md"

    if not l4_path.exists():
        findings.append({
            "file": "L4_O01_设计依据.md",
            "issue": "文件不存在",
            "severity": "FAIL"
        })
        return findings

    content = l4_path.read_text(encoding="utf-8")
    lines = [l for l in content.split("\n") if l.strip() and not l.strip().startswith("#") and not l.strip().startswith(">") and not l.strip().startswith("<!--")]
    if len(lines) < 5:
        findings.append({
            "file": "L4_O01_设计依据.md",
            "issue": f"有效内容行数 {len(lines)} < 5（可能为空模板）",
            "severity": "WARN"
        })

    decision_rows = [l for l in content.split("\n") if l.strip().startswith("|") and "来源" not in l and "---" not in l]
    if len(decision_rows) < 1:
        findings.append({
            "file": "L4_O01_设计依据.md",
            "issue": "无设计决策行（表格为空）",
            "severity": "WARN"
        })

    return findings


def check_coverage(docs_dir: str) -> list[dict]:
    """维度 7: 覆盖率 — INDEX.md 引用的文档 vs 实际存在的文件"""
    findings = []
    index_path = Path(docs_dir) / "INDEX.md"

    if not index_path.exists():
        findings.append({
            "file": "INDEX.md",
            "issue": "文件不存在（无法检查覆盖率）",
            "severity": "FAIL"
        })
        return findings

    content = index_path.read_text(encoding="utf-8")
    refs = re.findall(r'`(L[1-4]_[A-P]\d{2}_.+?\.md)`', content)
    actual_files = {f.name for f in Path(docs_dir).glob("L*.md")}

    for ref in refs:
        if ref not in actual_files:
            findings.append({
                "file": "INDEX.md",
                "issue": f"引用文件不存在: {ref}",
                "severity": "FAIL"
            })
    extra = actual_files - set(refs)
    if extra:
        tool_files = {"HANDOFF.md", "AUDIT_REPORT.md", "MEMORY.md"}
        extra -= tool_files
        for fname in sorted(extra):
            findings.append({
                "file": fname,
                "issue": "文件存在但未在 INDEX.md 中引用",
                "severity": "WARN"
            })

    return findings


def check_dogfood(docs_dir: str) -> list[dict]:
    """维度 8: 狗粮审计 — 项目自身是否遵循 agentprecept 方法论"""
    findings = []
    required = {
        "INDEX.md": "文档索引",
        "project-graph.yaml": "项目图",
        "HANDOFF.md": "会话交接",
        "L4_O01_design-rationale_设计依据.md": "设计依据",
    }
    for fname, desc in required.items():
        if not (Path(docs_dir) / fname).exists():
            findings.append({
                "file": fname,
                "issue": f"一等公民文档缺失: {desc}",
                "severity": "FAIL"
            })
    return findings


def check_readme_claims(docs_dir: str) -> list[dict]:
    """维度 9: README 数字声明 vs 实际数量"""
    findings = []
    readme = Path("README.md")
    if not readme.exists():
        findings.append({"file": "README.md", "issue": "文件不存在", "severity": "FAIL"})
        return findings

    content = readme.read_text(encoding="utf-8")

    claims = [
        ("10 维审计", r"(\d+)\s*维审计[^框架]", "scripts/basic-audit.py", "regex", r"def check_", 10),
        ("6 个 MCP tool", r"(\d+)\s*个\s*MCP\s*tool", "agentprecept/mcp_server.py", "regex", r"@mcp\.tool", 6),
        ("5 维代码扫描", r"(\d+)\s*维代码扫描", "scripts/sync-graph.py", "regex", r"def build_.*_relations", 5),
        ("16 篇方法论", r"(\d+)\s*篇方法论", "methodology/", "glob", "[01][0-9]-*.md", 16),
        ("36 个模板", r"(\d+)\s*个模板", "templates/", "glob", "*.md", 36),
        ("5 个 Skill", r"(\d+)\s*个\s*Skill", "skills/", "glob", "*.md", 5),
    ]

    for name, claim_re, path, method, pattern, expected in claims:
        m = re.search(claim_re, content)
        if not m:
            continue
        claimed = int(m.group(1))
        p = Path(path)
        if method == "glob":
            actual = len(list(p.rglob(pattern))) if p.is_dir() else -1
        else:
            actual = len(re.findall(pattern, p.read_text(encoding="utf-8"), re.MULTILINE)) if p.is_file() else -1
        if actual >= 0 and actual != claimed:
            findings.append({
                "file": "README.md",
                "issue": f"{name}: 声明 {claimed}，实际 {actual}",
                "severity": "FAIL" if actual < claimed else "WARN"
            })

    return findings


def check_branch_policy(docs_dir: str) -> list[dict]:
    """维度 11: 分支策略——是否有直接 push 到 main 的大变更"""
    findings = []
    # CI 侧检查：如果当前在 main 分支且 commit 变更 >10 文件，发出警告
    import subprocess as sp
    try:
        branch = sp.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        capture_output=True, text=True, timeout=5).stdout.strip()
        if branch in ("main", "master"):
            # 检查当前 commit 的变更文件数
            changed = sp.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                            capture_output=True, text=True, timeout=5).stdout.strip()
            changed_files = [f for f in changed.split("\n") if f]
            if len(changed_files) > 10:
                findings.append({
                    "file": "branch policy",
                    "issue": f"直接 push {len(changed_files)} 文件到 {branch} 分支。重大变更应走 feature 分支 + PR",
                    "severity": "WARN"
                })
    except Exception:
        pass
    return findings


def check_commit_size(docs_dir: str) -> list[dict]:
    """维度 12: commit 粒度——单 commit 是否过大"""
    findings = []
    import subprocess as sp
    try:
        changed = sp.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                        capture_output=True, text=True, timeout=5).stdout.strip()
        code_files = [f for f in changed.split("\n") if f and not f.startswith("docs/")
                       and not f.endswith(".md") and not f.endswith(".yaml")
                       and not f.endswith(".yml") and not f.endswith(".json")
                       and not f.endswith(".cfg") and not f.endswith(".toml")]
        if len(code_files) > 15:
            findings.append({
                "file": "commit size",
                "issue": f"单 commit 含 {len(code_files)} 个代码文件（建议 ≤15）",
                "severity": "WARN"
            })
    except Exception:
        pass
    return findings


def check_design_coverage(docs_dir: str) -> list[dict]:
    """维度 10: 代码模块是否有对应的设计文档"""
    findings = []
    graph_path = Path(docs_dir) / "project-graph.yaml"
    if not graph_path.exists():
        return findings

    try:
        import yaml
        doc = yaml.safe_load(graph_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return findings

    structure = doc.get("structure") or {}
    for module_path, meta in structure.items():
        if not isinstance(meta, dict):
            continue
        design_docs = meta.get("design_docs", [])
        for dd in design_docs:
            matches = list(Path(docs_dir).glob(f"{dd}*.md"))
            if not matches:
                findings.append({
                    "file": module_path,
                    "issue": f"design_docs 声明 {dd} 但文件不存在",
                    "severity": "FAIL"
                })
                continue
            for mf in matches:
                content = mf.read_text(encoding="utf-8")
                if "placeholder" in content or "TODO:" in content or "TBD:" in content:
                    findings.append({
                        "file": module_path,
                        "issue": f"design_doc {mf.name} 含骨架残留",
                        "severity": "WARN"
                    })

    return findings


def _safe(s: str) -> str:
    """Windows GBK 终端兼容——替换不可编码字符"""
    return s.encode("gbk", errors="replace").decode("gbk")


def main():
    gate_mode = "--gate" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--gate"]
    docs_dir = args[0] if args else "docs"
    results = []

    checks = [
        (check_naming, "命名一致性"),
        (check_broken_links, "交叉引用完整性"),
        (check_numbering, "编号连续性"),
        (check_skeleton, "骨架残留"),
        (check_graph_schema, "项目图格式"),
        (check_design_trace, "设计追溯"),
        (check_coverage, "覆盖率"),
        (check_dogfood, "狗粮审计"),
    ]
    if gate_mode:
        checks.append((check_readme_claims, "README声明校验"))
        checks.append((check_design_coverage, "设计覆盖检查"))
        checks.append((check_branch_policy, "分支策略检查"))
        checks.append((check_commit_size, "commit粒度检查"))

    for check, name in checks:
        findings = check(docs_dir)
        has_fail = any(item["severity"] == "FAIL" for item in findings)
        status = "PASS" if not findings else "FAIL" if has_fail else "WARN"
        results.append((name, status, findings))

    print("# 审计报告\n")
    print(f"审计范围: {docs_dir}/")
    for name, status, findings in results:
        print(f"## [{status}] {name}")
        if findings:
            for f_item in findings:
                print(_safe(f"- [{f_item['severity']}] {f_item['file']}: {f_item['issue']}"))
        else:
            print("无问题")
        print()

    total_fail = sum(1 for _, s, _ in results if s == "FAIL")
    total_warn = sum(1 for _, s, _ in results if s == "WARN")
    print(f"---\nFAIL {total_fail}  WARN {total_warn}")
    exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()