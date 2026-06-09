# architecture-design skill — 架构设计图自动生成

加载此 skill 后，Agent 从 project-graph 自动生成架构图。

## 自动动作

1. 读 project-graph structure 层
2. 生成 Mermaid 图（`python -m agentprecept.graph_to_mermaid`）
3. 按 api/services/models 分组标注
4. critical 模块红色标注

## 完成标准

□ 图包含 ≥ 3 个模块
□ 每个模块有职责描述
□ L4_O01 有对应依据

详见 `templates/L2_D01_architecture_架构设计.md`。
