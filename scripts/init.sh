#!/bin/bash
# agent-compass 初始化脚本
# 用法: bash init.sh /path/to/your-project

PROJECT="${1:-.}"

echo "agent-compass 初始化 → $PROJECT"

cp AGENTS.md "$PROJECT/"
mkdir -p "$PROJECT/docs"

# 一等公民（4 份，不可缺）
cp templates/INDEX.md "$PROJECT/docs/"
cp templates/L1_A02_naming-convention_命名规范.md "$PROJECT/docs/"
cp templates/L1_B01_glossary_术语表.md "$PROJECT/docs/"
cp templates/HANDOFF.md "$PROJECT/docs/"
# 核心支撑
cp templates/project-graph.yaml "$PROJECT/docs/"
cp templates/L4_O01_design-rationale_设计依据.md "$PROJECT/docs/"

echo "✅ 一等公民文档（4/4）:"
echo "   $PROJECT/docs/INDEX.md              — 文档目录"
echo "   $PROJECT/docs/L1_A02_*.md           — 命名规范"
echo "   $PROJECT/docs/L1_B01_*.md           — 术语表"
echo "   $PROJECT/docs/HANDOFF.md            — 会话交接"
echo ""
echo "✅ 核心支撑:"
echo "   $PROJECT/AGENTS.md                  — Agent 入口"
echo "   $PROJECT/docs/project-graph.yaml    — 项目图"
echo "   $PROJECT/docs/L4_O01_*.md           — 设计依据"
echo ""
echo "下一步: 复制 examples/first-run.md 中的 prompt 发给 Agent 自动初始化 project-graph"
