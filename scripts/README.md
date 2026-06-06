# scripts/ — agent-compass 辅助脚本

| 脚本 | 用途 | 用法 |
|------|------|------|
| `init.sh` | Linux/macOS 一键复制核心文件到目标项目 | `bash init.sh /path/to/project` |
| `init.ps1` | Windows 一键复制 | `.\init.ps1 C:\path\to\project` |
| `audit.py` | 七维审计自动化（命名/断链/TODO） | `python audit.py docs/` |
| `check-naming.py` | 命名规范检查 | `python check-naming.py docs/` |

## 集成到 CI

```yaml
# .github/workflows/audit.yml
- name: 命名检查
  run: python scripts/check-naming.py templates/
- name: 审计
  run: python scripts/audit.py templates/
```

## 集成到 Makefile

```makefile
audit:
	python scripts/audit.py docs/
check-naming:
	python scripts/check-naming.py docs/
```
