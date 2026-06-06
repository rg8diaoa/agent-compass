#!/bin/bash
# agent-compass 初始化脚本
# 用法: bash init.sh /path/to/your-project

PROJECT="${1:-.}"

echo "agent-compass 初始化 → $PROJECT"

# 核心文件
cp AGENTS.md "$PROJECT/"
mkdir -p "$PROJECT/docs"
cp templates/project-graph.yaml "$PROJECT/docs/"
cp templates/HANDOFF.md "$PROJECT/docs/"
cp templates/L4_O01_design-rationale_设计依据.md "$PROJECT/docs/"

echo "✅ 核心文件已复制:"
echo "   $PROJECT/AGENTS.md"
echo "   $PROJECT/docs/project-graph.yaml"
echo "   $PROJECT/docs/HANDOFF.md"
echo "   $PROJECT/docs/L4_O01_design-rationale_设计依据.md"
echo ""
echo "下一步: 复制 examples/first-run.md 中的 prompt 发给 Agent 自动初始化 project-graph"
