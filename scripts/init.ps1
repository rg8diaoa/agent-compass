# agent-compass 初始化脚本 (Windows PowerShell)
# 用法: .\init.ps1 C:\path\to\your-project

param([string]$Project = ".")

Write-Host "agent-compass 初始化 → $Project"

Copy-Item "AGENTS.md" "$Project/"
New-Item -ItemType Directory -Force -Path "$Project\docs" | Out-Null
Copy-Item "templates\project-graph.yaml" "$Project\docs\"
Copy-Item "templates\HANDOFF.md" "$Project\docs\"
Copy-Item "templates\L4_O01_design-rationale_设计依据.md" "$Project\docs\"

Write-Host "✅ 核心文件已复制:"
Write-Host "   $Project\AGENTS.md"
Write-Host "   $Project\docs\project-graph.yaml"
Write-Host "   $Project\docs\HANDOFF.md"
Write-Host "   $Project\docs\L4_O01_design-rationale_设计依据.md"
Write-Host ""
Write-Host "下一步: 复制 examples\first-run.md 中的 prompt 发给 Agent 自动初始化 project-graph"
