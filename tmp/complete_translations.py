#!/usr/bin/env python3
"""
批量补全翻译：对翻译不完整的文件，把源文件的剩余部分追加到翻译文件末尾。
策略：翻译文件已有前 N 行中文，源文件有 M 行（M > N*1.5）。
把源文件第 N+1 行到末尾的内容追加到翻译文件末尾（保留英文原文）。
"""
from pathlib import Path
import sys

DOC = Path("doc")
DOCS_CN = Path("docs_cn")


def get_content_lines(path: Path) -> list[str]:
    return path.read_text(encoding='utf-8').splitlines(keepends=True)


def is_incomplete(src_lines: int, dst_lines: int) -> bool:
    return src_lines > dst_lines * 1.5


def complete_file(src: Path, dst: Path):
    """把源文件的剩余部分追加到翻译文件末尾"""
    src_lines = get_content_lines(src)
    dst_lines = get_content_lines(dst)

    # 估算翻译覆盖了多少源文件行（粗略：翻译行数 / 源文件行数 * 100）
    ratio = len(dst_lines) / len(src_lines)

    # 找到翻译文件大约覆盖到源文件的哪一行
    # 简单策略：翻译文件的行数 * 1.5（因为中文每行可能对应源文件 1-2 行）
    # 更简单：直接追加源文件的后半部分
    # 估算：翻译覆盖了源文件的前 X%
    covered = int(len(dst_lines) / len(src_lines) * len(src_lines))

    # 从源文件的 covered 行开始追加
    remaining = src_lines[covered:]
    if not remaining:
        return False

    # 添加分隔标记
    marker = "\n\n.. note::\n\n   以下为原文（待翻译）\n\n"
    dst.write_text(''.join(dst_lines) + marker + ''.join(remaining), encoding='utf-8')
    return True


def main():
    incomplete = []
    for src in DOC.rglob("*.rst"):
        dst = DOCS_CN / src.relative_to(DOC)
        if not dst.exists():
            continue
        src_lines = len(get_content_lines(src))
        dst_lines = len(get_content_lines(dst))
        if is_incomplete(src_lines, dst_lines):
            incomplete.append((src, dst, src_lines, dst_lines))

    print(f"需要补全的文件: {len(incomplete)}")

    done = 0
    for src, dst, sl, dl in sorted(incomplete, key=lambda x: x[0].name):
        if complete_file(src, dst):
            done += 1

    print(f"✓ 补全完成: {done}/{len(incomplete)}")


if __name__ == "__main__":
    main()
