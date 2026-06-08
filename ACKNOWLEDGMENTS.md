# 致谢

agentprecept 的设计思想受以下项目启发：

## 直接启发

| 项目 | 启发 |
|------|------|
| [ECC](https://github.com/affaan-m/ECC) | Agent 命令映射表、持久记忆（MEMORY.md）、反模式段的概念 |
| [Andrej Karpathy's LLM Coding Style](https://github.com/multica-ai/andrej-karpathy-skills) | 目标驱动执行原则、AGENTS.md 压缩到一个文件的设计哲学 |
| [CodeToFlow](https://moge.ai/zh/product/codetoflow) | 代码结构可视化理念，我们实现了 graph-to-mermaid.py |
| [gnhf](https://github.com/kunchenguid/gnhf) | git worktree 安全沙盒模式——原子提交 + 失败回滚 + 多 Agent 后端兼容，启发了 MCP Server 的安全设计和 gnhf 集成方案 |

## 方法论来源

agentprecept 的核心方法论——project-graph 三层模型、设计依据追溯、15 维自动化审计（--gate 模式）+ 14 维方法论审计框架、8 阶段完整循环——源自一个 41 文档/46 配置维度的多 Agent 协作实战项目。这些经验经过三轮审计和脱敏处理后提炼为通用资产。

## 开源社区

感谢 Anthropic 推动 AGENTS.md 标准、OpenCode/CodeWhale/Cursor 社区对 Agent 工具生态的贡献、以及所有开源项目中公开分享 Agent 配置实践的开发者。
