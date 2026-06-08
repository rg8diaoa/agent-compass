"""AgentPrecept CLI — 项目初始化(6阶段) / 同步 / 审计(10维) / 诊断 / setup / hooks / gnhf"""

import sys
import subprocess
import json
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent / "scripts"
ROOT = Path(__file__).parent.parent

# ===== init (6 阶段) =====

def _check_git(project):
    git_dir = Path(project) / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init", project], capture_output=True)
        return True, "git init done"
    return False, "Git already initialized"


def _install_hook(project):
    hook_path = Path(project) / ".git" / "hooks" / "pre-commit"
    hook_content = """#!/bin/bash
# AgentPrecept pre-commit gate
# Skip: git commit --no-verify

# --- Gate 1: branch policy ---
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
CHANGED_COUNT=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    if [ "$CHANGED_COUNT" -gt 10 ] 2>/dev/null; then
        echo ""
        echo "[AgentPrecept] WARNING: $CHANGED_COUNT files on $BRANCH branch"
        echo "[AgentPrecept] Major changes should use feature branches."
        echo "[AgentPrecept] Create: git checkout -b feature/your-change"
        echo "[AgentPrecept] Skip:  git commit --no-verify"
        exit 1
    fi
fi

# --- Gate 2: design docs ---
DESIGN_DOCS=("docs/L2_D01" "docs/L4_O01" "docs/project-graph.yaml")
CHANGED_CODE=$(git diff --cached --name-only | grep -v '^docs/\\|\\.md$\\|\\.ya\\?ml$\\|\\.json$')
[ -z "$CHANGED_CODE" ] && exit 0

for doc in "${DESIGN_DOCS[@]}"; do
    if ! compgen -G "$doc*" >/dev/null && [ ! -f "$doc" ]; then
        echo ""
        echo "[AgentPrecept] missing core design doc: $doc"
        echo "[AgentPrecept] skip: git commit --no-verify"
        exit 1
    fi
done

# --- Gate 3: commit size ---
CHANGED_CODE_FILES=$(git diff --cached --name-only | grep -Ev '^docs/|\\.md$|\\.ya?ml$|\\.json$|\\.cfg$|\\.toml$' | wc -l | tr -d ' ')
if [ "$CHANGED_CODE_FILES" -gt 15 ] 2>/dev/null; then
    echo ""
    echo "[AgentPrecept] WARNING: $CHANGED_CODE_FILES code files in one commit"
    echo "[AgentPrecept] Consider splitting into smaller commits (1-3 files each)"
    echo "[AgentPrecept] Skip: git commit --no-verify"
    exit 1
fi

# --- Gate 4: NEEDS_HUMAN_REVIEW ---
REVIEW_TAGGED=$(git diff --cached --name-only | xargs grep -l '\[NEEDS_HUMAN_REVIEW\]' 2>/dev/null)
if [ -n "$REVIEW_TAGGED" ]; then
    echo ""
    echo "[AgentPrecept] WARNING: staged files contain [NEEDS_HUMAN_REVIEW]"
    echo "[AgentPrecept] Confirm design docs first, then remove NEEDS_HUMAN_REVIEW."
    echo "[AgentPrecept] Skip: git commit --no-verify"
    exit 1
fi

exit 0
"""
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    hook_path.write_text(hook_content)
    # Unix: chmod +x
    try:
        hook_path.chmod(0o755)
    except Exception:
        pass
    return True


def _check_gnhf():
    try:
        result = subprocess.run(["gnhf", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False


def _setup_gnhf():
    from agentprecept.gnhf_task import render_template
    render_template()
    return True


def _check_ci(project):
    workflows = Path(project) / ".github" / "workflows"
    return workflows.exists() and any(workflows.glob("*.yml"))


def _generate_ci_gate(project):
    workflows = Path(project) / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    gate_yml = workflows / "agentprecept-gate.yml"
    content = """# AgentPrecept CI Gate — PR merge 前自动运行 10 维审计
name: AgentPrecept Gate
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  audit-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install agentprecept
      - run: agentprecept audit --gate
"""
    gate_yml.write_text(content)
    return True


def _mcp_config():
    config = {
        "mcpServers": {
            "agentprecept": {
                "command": "python",
                "args": ["-m", "agentprecept.mcp_server"],
                "env": {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
            }
        }
    }
    return json.dumps(config, indent=2)


def cmd_init(project=".", yes=False, dry_run=False, status_only=False,
             ci=None, gnhf_opt=None):
    """6 阶段项目接入"""
    project = Path(project).resolve()

    if status_only:
        print_status(project)
        return

    if dry_run:
        print(f"[dry-run] would init: {project}")
        return

    project.mkdir(parents=True, exist_ok=True)
    docs = project / "docs"
    docs.mkdir(exist_ok=True)

    report = {}

    # Phase 1: 骨架
    if not (project / "AGENTS.md").exists() or yes:
        (ROOT / "AGENTS.md").replace(project / "AGENTS.md")
    for tmpl in ["INDEX.md", "L1_A02_naming-convention_命名规范.md",
                 "L1_B01_glossary_术语表.md", "HANDOFF.md",
                 "MEMORY.md", "project-graph.yaml",
                 "L4_O01_design-rationale_设计依据.md"]:
        src = ROOT / "templates" / tmpl
        dst = docs / tmpl
        if src.exists() and not dst.exists():
            src.replace(dst)
    report["AGENTS.md"] = True
    report["docs/ skeleton"] = True

    # Phase 2: Git
    report["Git"] = _check_git(project)[0]

    # Phase 3: Git Hook
    if report["Git"]:
        report["Pre-commit Hook"] = _install_hook(project)

    # Phase 3.5: gnhf
    if report.get("Git") and gnhf_opt is not False:
        if _check_gnhf():
            if gnhf_opt or yes:
                _setup_gnhf()
                report["gnhf"] = "enabled"
            else:
                report["gnhf"] = "skipped (run: agentprecept gnhf setup)"
        else:
            report["gnhf"] = "not installed (pip install gnhf && agentprecept gnhf setup)"

    # Phase 4: CI Gate
    has_ci = _check_ci(project)
    if has_ci and ci is not False:
        if ci or yes:
            _generate_ci_gate(project)
            report["CI Gate"] = True
        else:
            report["CI Gate"] = "skipped (run: agentprecept init --ci)"
    else:
        report["CI Gate"] = "no CI detected"

    # Phase 5: MCP
    report["MCP"] = _mcp_config()

    # Phase 6: 状态报告
    print_status(project, report)


def print_status(project, report=None):
    """输出 AgentPrecept 接入状态"""
    project = Path(project)
    if report is None:
        report = {}

    print("AgentPrecept 接入状态")
    print("-" * 44)

    def line(icon, name, detail=""):
        print(f"  {icon} {name:<20} {detail}")

    ag = (project / "AGENTS.md").exists()
    idx = (project / "docs" / "INDEX.md").exists()
    git = (project / ".git").exists()
    hook = (project / ".git" / "hooks" / "pre-commit").exists()
    ci_gate = (project / ".github" / "workflows" / "agentprecept-gate.yml").exists()

    line("✅" if ag else "❌", "AGENTS.md", "Agent 行为规则" if ag else "缺失")
    line("✅" if idx else "❌", "docs/ skeleton", "7 核心文档" if idx else "缺失")
    line("✅" if git else "⚠", "Git", "已初始化" if git else "运行: git init")
    line("✅" if hook else "⚠", "Pre-commit Hook", "设计文档门禁" if hook else "需 git init")
    if g := report.get("gnhf", ""):
        status = "✅" if g == "enabled" else "⚠"
        line(status, "gnhf", g)
    if ci := report.get("CI Gate", ""):
        line("✅" if ci is True else "⚠", "CI Gate", ci if isinstance(ci, str) else "PR merge 强制审计")
    line("✅" if ag else "⚠", "MCP", "6 tools 可用" if ag else "需 AGENTS.md")

    print("-" * 44)
    total = sum(1 for v in [ag, idx, git, hook] if v)
    print(f"  {total}/4 核心能力已接入")


# ===== hooks =====

def cmd_hooks(action="status", project="."):
    """Git hook 管理"""
    hook_path = Path(project) / ".git" / "hooks" / "pre-commit"

    if action == "install":
        if not (Path(project) / ".git").exists():
            print("error: git 未初始化")
            return
        _install_hook(project)
        print("pre-commit hook installed")
    elif action == "uninstall":
        if hook_path.exists():
            hook_path.unlink()
            print("pre-commit hook removed")
    elif action == "status":
        if hook_path.exists():
            print("pre-commit hook: installed")
        else:
            print("pre-commit hook: not installed")


# ===== gnhf =====

def cmd_gnhf(action="status"):
    """gnhf 集成"""
    if action == "setup":
        if _check_gnhf():
            _setup_gnhf()
            print("[gnhf] task template generated: .gnhf/sync-task.md")
            print("[gnhf] run: gnhf --goal .gnhf/sync-task.md --verify 'agentprecept audit'")
        else:
            print("gnhf CLI not found. Install: pip install gnhf")
    elif action == "task":
        _setup_gnhf()
        print("[gnhf] task template regenerated")
    elif action == "status":
        task_file = Path(".gnhf/sync-task.md")
        if _check_gnhf():
            print("gnhf CLI: available")
            print(f"task template: {'exists' if task_file.exists() else 'missing'}")
        else:
            print("gnhf CLI: not installed")


# ===== sync / audit / doctor / setup =====

def cmd_sync(src="src", graph="docs/project-graph.yaml"):
    subprocess.run([sys.executable, str(SCRIPTS / "sync-graph.py"), src, graph])


def cmd_audit(docs="docs", gate=False):
    args = [sys.executable, str(SCRIPTS / "basic-audit.py"), docs]
    if gate:
        args.append("--gate")
    subprocess.run(args)


def cmd_doctor():
    root = Path.cwd()
    checks = {
        "AGENTS.md": root / "AGENTS.md",
        "docs/INDEX.md": root / "docs" / "INDEX.md",
        "docs/project-graph.yaml": root / "docs" / "project-graph.yaml",
        "docs/HANDOFF.md": root / "docs" / "HANDOFF.md",
        "docs/L4_O01": root / "docs" / "L4_O01_design-rationale_设计依据.md",
    }
    ok = 0
    for name, path in checks.items():
        status = "OK" if path.exists() else "MISSING"
        if path.exists():
            ok += 1
        print(f"  {status}  {name}")
    print(f"\n{ok}/{len(checks)} 项通过")
    if ok < len(checks):
        print("运行 agentprecept init . 修复缺失文件")


def cmd_setup():
    print("=== agentprecept setup ===\n")
    print("[1/3] 初始化项目文档...")
    cmd_init(".", yes=True)
    print()
    print("[2/3] MCP Server 配置")
    print(f"  {_mcp_config()}")
    print("  重启 Agent 后即可使用 MCP tools: query/audit/diff/decision/handoff/design_gate\n")
    print("[3/3] 诊断环境...")
    cmd_doctor()


# ===== main =====

USAGE = """agentprecept — AI coding agent governance toolkit

用法: agentprecept <command> [options]

命令:
  init [project]      一键接入（6 阶段: 骨架/Git/Hook/gnhf/CI/MCP）
    --yes              全部 yes（非交互）
    --dry-run          预览模式
    --status           仅查看接入状态
    --ci               追加 CI Gate
    --no-ci            跳过 CI Gate
    --no-gnhf          跳过 gnhf
  sync [src]          从代码同步 project-graph
  audit [docs]         8 维审计（--gate 开启 10 维）
  doctor              诊断缺失文件
  setup               一键安装（init + MCP + doctor）
  hooks <action>      Git hook 管理 (install/uninstall/status)
  gnhf <action>       gnhf 集成 (setup/task/status)
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "init":
        project = args[0] if args else "."
        yes = "--yes" in args
        dry_run = "--dry-run" in args
        status_only = "--status" in args
        ci = False if "--no-ci" in args else (True if "--ci" in args else None)
        gnhf_opt = False if "--no-gnhf" in args else None
        cmd_init(project, yes=yes, dry_run=dry_run, status_only=status_only,
                 ci=ci, gnhf_opt=gnhf_opt)

    elif cmd == "sync":
        cmd_sync(*(args[:2] if args else ["src", "docs/project-graph.yaml"]))

    elif cmd == "audit":
        gate = "--gate" in args
        docs = next((a for a in args if a != "--gate"), "docs")
        cmd_audit(docs=docs, gate=gate)

    elif cmd == "doctor":
        cmd_doctor()

    elif cmd == "setup":
        cmd_setup()

    elif cmd == "hooks":
        action = args[0] if args else "status"
        project = args[1] if len(args) > 1 else "."
        cmd_hooks(action, project)

    elif cmd == "gnhf":
        action = args[0] if args else "status"
        cmd_gnhf(action)

    else:
        print(USAGE)


if __name__ == "__main__":
    main()