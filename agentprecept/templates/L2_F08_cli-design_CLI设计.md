# CLI 设计

> 分类: F | 层级: L2 | 编号: L2_F08
> 状态: 📝 撰写中 | 目标读者: 开发者
> 前置阅读: L2_F01_dev-env_开发环境.md

---

## §1 命令结构

```
{program} {command} {subcommand} [options] [arguments]
```

| 元素 | 示例 |
|------|------|
| program | `todo` |
| command | `todo task` |
| subcommand | `todo task create` |
| options | `--priority P1` |
| arguments | `"Buy milk"` |

## §2 通用约定

```bash
# 帮助
todo --help
todo task --help

# 版本
todo --version

# 子命令分组：名词在前，动词在后
todo task create     # ✅
todo create-task     # ❌
```

## §3 退出码

| 码 | 含义 |
|:--:|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 参数错误 |
| 3 | 认证失败 |
| 4 | 资源不存在 |
| 5 | 冲突（并发/重复） |

## §4 参数命名

| 格式 | 用途 | 示例 |
|------|------|------|
| `--flag` | 布尔开关 | `--verbose` |
| `--option VALUE` | 带值 | `--priority P1` |
| `ARG` | 位置参数 | `todo task delete TASK_ID` |

## §5 Agent 规则

1. 新增命令 → 遵循 `{名词} {动词}` 格式
2. 新增参数 → 全局选项（`--verbose`）放在子命令前面
3. 退出码 → 使用 §3 约定，不发明新码
4. 错误输出 → 写到 stderr，正常输出 → stdout
