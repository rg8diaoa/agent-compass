# agent-compass 初始化脚本 (Windows PowerShell)
# 用法: .\init.ps1 C:\path\to\your-project

param([string]$Project = ".")

Write-Host "agent-compass 初始化 → $Project"

if (Test-Path "$Project\AGENTS.md") {
    Write-Host "⚠ AGENTS.md 已存在，跳过覆盖。如需更新请手动替换。"
} else {
    Copy-Item "AGENTS.md" "$Project/"
}
New-Item -ItemType Directory -Force -Path "$Project\docs" | Out-Null

# 一等公民（4 份，不可缺）
Copy-Item "templates\INDEX.md" "$Project\docs\"
Copy-Item "templates\L1_A02_naming-convention_命名规范.md" "$Project\docs\"
Copy-Item "templates\L1_B01_glossary_术语表.md" "$Project\docs\"
Copy-Item "templates\HANDOFF.md" "$Project\docs\"
# 核心支撑
Copy-Item "templates\project-graph.yaml" "$Project\docs\"
Copy-Item "templates\L4_O01_design-rationale_设计依据.md" "$Project\docs\"

Write-Host "✅ 一等公民文档（4/4）:"
Write-Host "   $Project\docs\INDEX.md              — 文档目录"
Write-Host "   $Project\docs\L1_A02_*.md           — 命名规范"
Write-Host "   $Project\docs\L1_B01_*.md           — 术语表"
Write-Host "   $Project\docs\HANDOFF.md            — 会话交接"
Write-Host ""
Write-Host "✅ 核心支撑:"
Write-Host "   $Project\AGENTS.md                  — Agent 入口"
Write-Host "   $Project\docs\project-graph.yaml    — 项目图"
Write-Host "   $Project\docs\L4_O01_*.md           — 设计依据"
Write-Host ""
Write-Host ""
Write-Host "可选: 初始化 git 仓库？(y/n)"
$gitAnswer = Read-Host
if ($gitAnswer -eq 'y') {
    git init $Project 2>$null
    Write-Host "   git init done"
}
Write-Host ""
Write-Host "下一步: 1) 运行 agent-compass setup 获取 MCP 配置"
Write-Host "      2) 将 MCP 配置加入 Claude Code(.mcp.json) 或 CodeWhale(~/.deepseek/mcp.json)"
Write-Host "      3) 重启 Agent, MCP tools 自动可用"
Write-Host "      4) 或: 复制 examples\first-run.md 中的 prompt 发给 Agent 自动初始化 project-graph"
