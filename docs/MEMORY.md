# 项目持久记忆

> agent-compass 自身的持久偏好和约束。

## 人类偏好

- 回答风格: 简短
- 代码注释语言: 中文
- 优先测试框架: pytest
- 优先包管理: pip

## 项目约束

- 不引入非 Python 运行时依赖（保持跨平台）
- 模板中所有代码示例 Python/Node 双语言

## 历史教训

- Windows GBK 终端不兼容 emoji → 全部脚本用 ASCII 标记
- egg-info 构建产物会污染 Git → .gitignore 排除
- 模板文件必须有中文标题 → L4_O01 ADR-005
