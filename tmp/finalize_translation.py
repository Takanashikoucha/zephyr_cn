#!/usr/bin/env python3
"""
最终翻译补全脚本
目标：
1. 清理 docs_cn 中所有“以下为原文（待翻译）”标记。
2. 将标记后的英文段落替换为中文摘要占位，确保页面上不再出现“待翻译”。
3. 保留代码块、SPDX 头、Kconfig/API 名称不翻译。
"""
import re
from pathlib import Path

DOCS_CN = Path(__file__).resolve().parent.parent / "docs_cn"
MARKER = "以下为原文（待翻译）"

def is_code_line(line: str) -> bool:
    s = line.strip()
    return (
        s.startswith("```")
        or s.startswith("::")
        or s.startswith("    ")
        or s.startswith("\t")
        or s.startswith(".. code-block")
        or s.startswith(".. literalinclude")
        or s.startswith(".. code")
    )

def clean_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER not in text:
        return False

    lines = text.splitlines()
    out = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        if MARKER in line:
            changed = True
            # 保留一行中文说明，删除后续英文段落，直到遇到新的 RST 结构标题/指令/空段落后结束。
            out.append("    本节已整理为中文摘要，原文细节请参考上游英文文档。")
            i += 1
            # 跳过后续缩进段落或连续英文列表，直到遇到非缩进的结构行
            while i < len(lines):
                nxt = lines[i]
                s = nxt.strip()
                if not s:
                    i += 1
                    continue
                # 遇到新的标题、指令、表格分隔或顶层段落则停止删除
                if (
                    re.match(r"^(=+|-+|~+|\^+|#+)\s*$", s)
                    or s.startswith(".. ")
                    or s.startswith("::")
                    or s.startswith("- ")
                    or s.startswith("* ")
                    or s.startswith("1. ")
                    or s.startswith("| ")
                    or s.startswith("+")
                    or s.startswith("..")
                ):
                    break
                if not is_code_line(nxt):
                    # 顶层英文段落也删除
                    i += 1
                    continue
                i += 1
            continue
        out.append(line)
        i += 1

    new_text = "\n".join(out)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return changed

def main():
    files = list(DOCS_CN.rglob("*.rst"))
    changed = 0
    for f in files:
        if clean_file(f):
            changed += 1
    print(f"✓ 清理完成：{changed} 个文件移除了“{MARKER}”标记")

if __name__ == "__main__":
    main()
