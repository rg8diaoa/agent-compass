"""命名规范检查脚本

用法: python scripts/check-naming.py docs/
检查 docs/ 下所有 L 开头的文件是否遵循命名规范。
"""

import os, re, sys


def main():
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    pattern = r'^L[1-4]_[A-P]\d{2}_[a-z0-9-]+_.+\.md$'
    violations = 0

    for fname in sorted(os.listdir(docs_dir)):
        if not fname.startswith("L"):
            continue
        if not re.match(pattern, fname):
            print(f"❌ {fname}")
            violations += 1

    if violations == 0:
        print(f"✅ 所有 L 开头文件命名合规 ({docs_dir}/)")
        exit(0)
    else:
        print(f"\n{violations} 个文件命名不符合规范")
        exit(1)


if __name__ == "__main__":
    main()
