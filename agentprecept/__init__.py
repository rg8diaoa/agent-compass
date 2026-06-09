"""AgentPrecept — AI 编码 Agent 方法论治理工具集"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("agentprecept")
except PackageNotFoundError:
    __version__ = "0.0.0"  # 未安装时回退
