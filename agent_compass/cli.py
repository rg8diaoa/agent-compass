"""agent-compass CLI — 项目初始化 / 同步 / 审计 / 诊断 / setup"""

import sys
import subprocess
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent / "scripts"
ROOT = Path(__file__).parent.parent


def cmd_init(project: str = "."):
    """复制 AGENTS.md + 7 文档到目标项目"""
    project = Path(project)
    project.mkdir(parents=True, exist_ok=True)
    docs = project / "docs"
    docs.mkdir(exist_ok=True)

    # 入口
    (ROOT / "AGENTS.md").replace(project / "AGENTS.md")
    # 一等公民
    (ROOT / "templates" / "INDEX.md").replace(docs / "INDEX.md")
    (ROOT / "templates" / "L1_A02_naming-convention_命名规范.md").replace(
        docs / "L1_A02_naming-convention_命名规范.md")
    (ROOT / "templates" / "L1_B01_glossary_术语表.md").replace(
        docs / "L1_B01_glossary_术语表.md")
    (ROOT / "templates" / "HANDOFF.md").replace(docs / "HANDOFF.md")
    # 核心支撑
    (ROOT / "templates" / "project-graph.yaml").replace(docs / "project-graph.yaml")
    (ROOT / "templates" / "L4_O01_design-rationale_设计依据.md").replace(
        docs / "L4_O01_design-rationale_设计依据.md")

    print(f"[OK] agent-compass 初始化完成 -> {project}")
    print(f"   一等公民: INDEX / 命名规范 / 术语表 / HANDOFF")
    print(f"   核心支撑: AGENTS.md / project-graph / L4_O01")


def cmd_sync(src: str = "src", graph: str = "docs/project-graph.yaml"):
    """从代码自动同步 project-graph"""
    subprocess.run([sys.executable, str(SCRIPTS / "sync-graph.py"), src, graph])


def cmd_audit(docs: str = "docs"):
    """8 维审计"""
    subprocess.run([sys.executable, str(SCRIPTS / "basic-audit.py"), docs])


def cmd_doctor():
    """诊断：检查项目缺少哪些文件"""
    root = Path.cwd()
    checks = {
        "AGENTS.md": root / "AGENTS.md",
        "docs/INDEX.md": root / "docs" / "INDEX.md",
        "docs/project-graph.yaml": root / "docs" / "project-graph.yaml",
        "docs/HANDOFF.md": root / "docs" / "HANDOFF.md",
        "docs/L4_O01": root / "docs" / "L4_O01_design-rationale_设计依据.md",
        "docs/L1_A02 命名规范": root / "docs" / "L1_A02_naming-convention_命名规范.md",
        "docs/L1_B01 术语表": root / "docs" / "L1_B01_glossary_术语表.md",
    }

    ok = 0
    for name, path in checks.items():
        status = "OK" if path.exists() else "MISSING"
        if path.exists():
            ok += 1
        print(f"  {status}  {name}")
    print(f"\n{ok}/{len(checks)} 项通过")

    if ok < len(checks):
        print("运行 agent-compass init . 修复缺失文件")


def cmd_setup():
    """一键安装：init + MCP 配置指南 + 诊断"""
    print("=== agent-compass setup ===\n")

    # 1. init
    print("[1/3] 初始化项目文档...")
    cmd_init(".")
    print()

    # 2. MCP 配置
    print("[2/3] MCP Server 配置")
    mcp_config = {
        "mcpServers": {
            "agent-compass": {
                "command": "compass-mcp",
            }
        }
    }
    import json
    print(f"""  将以下内容加入你的 Agent 工具的 MCP 配置文件：

  Claude Code  → .mcp.json:
{json.dumps(mcp_config, indent=2)}

  CodeWhale    → ~/.deepseek/mcp.json:
{json.dumps(mcp_config, indent=2)}

  Cursor       → .cursor/mcp.json:
{json.dumps(mcp_config, indent=2)}

  重启 Agent 后即可使用 MCP tools: query / audit / diff / decision / handoff
""")

    # 3. doctor
    print("[3/3] 诊断环境...")
    cmd_doctor()


COMMANDS = {
    "init": cmd_init,
    "sync": cmd_sync,
    "audit": cmd_audit,
    "doctor": cmd_doctor,
    "setup": cmd_setup,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("agent-compass — Agent 协作不踩脚")
        print(f"用法: agent-compass {{{'|'.join(COMMANDS)}}}")
        print()
        print("  首次使用: agent-compass setup    # 一键初始化 + MCP 配置 + 诊断")
        print("  日常使用: agent-compass sync     # 代码变更后同步项目图")
        print("          agent-compass audit     # 8 维文档审计")
        return

    cmd = COMMANDS[sys.argv[1]]
    cmd(*sys.argv[2:])


if __name__ == "__main__":
    main()
