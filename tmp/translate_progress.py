#!/usr/bin/env python3
import os
SRC = "/home/koucha/RTOS/doc"
DST = "/home/koucha/RTOS/docs_cn"
batches = {
    "批次 1 introduction": ["introduction"],
    "批次 2 kernel": ["kernel"],
    "批次 3 build": ["build"],
    "批次 4 develop": ["develop"],
    "批次 5 hardware": ["hardware"],
    "批次 6 services": ["services"],
    "批次 7 releases": ["releases"],
    "批次 8 security+contribute+project+safety": ["security", "contribute", "project", "safety"],
}
src_files = set()
for root, dirs, files in os.walk(SRC):
    for f in files:
        if f.endswith(".rst"):
            src_files.add(os.path.relpath(os.path.join(root, f), SRC))
dst_files = set()
for root, dirs, files in os.walk(DST):
    for f in files:
        if f.endswith(".rst"):
            dst_files.add(os.path.relpath(os.path.join(root, f), DST))
print("=== 翻译进度总览 ===")
print(f"源文件总数: {len(src_files)}")
print(f"已翻译: {len(dst_files & src_files)}")
print(f"未翻译: {len(src_files - dst_files)}")
print(f"完成率: {len(dst_files & src_files)/len(src_files)*100:.1f}%")
print()
print("=== 按批次 ===")
for batch_name, dirs in batches.items():
    total = 0; done = 0
    for d in dirs:
        for f in src_files:
            if f.startswith(d + "/"):
                total += 1
                if f in dst_files: done += 1
    if total > 0:
        print(f"{batch_name}: {done}/{total} ({done/total*100:.1f}%)")
missing = sorted(src_files - dst_files)
if missing:
    print(f"\n=== 未翻译文件清单 ({len(missing)}) ===")
    for i, f in enumerate(missing, 1): print(f"{i}. {f}")
extra = sorted(dst_files - src_files)
if extra:
    print(f"\n=== 异常: docs_cn 有但 doc 没有的文件 ({len(extra)}) ===")
    for f in extra: print(f"  {f}")
