#!/usr/bin/env python3
"""将 guide/ 目录下的 Markdown 文件转换为 HTML。

输出到 guide_html/ 目录，供 GitHub Pages 部署。
"""
import os
import re
from pathlib import Path

try:
    import markdown
except ImportError:
    raise SystemExit("请先安装 markdown 库: pip install markdown")

GUIDE_DIR = Path(__file__).parent.parent / "guide"
OUTPUT_DIR = Path(__file__).parent.parent / "guide_html"

# 荧枝风格 CSS（内联到每个 HTML 页面）
LUMINOUS_CSS = """
:root {
  --night1: #05070b; --night2: #081018;
  --bone: #7cc4ff; --bone2: #a9dcff; --bone-dim: rgba(124,196,255,.30);
  --thread: #5eead4; --red: #ff4d63; --purple: #c9a3ff;
  --txt: #e6eef6; --sub: #93a6bd; --dim: #5f7288;
  --line: rgba(124,196,255,.20); --panel: rgba(4,9,16,.82);
}
body {
  font-family: 'JetBrains Mono', 'Sarasa Mono SC', 'Noto Sans Mono CJK SC', monospace;
  background: var(--night1); color: var(--sub);
  font-size: 14px; line-height: 1.6; margin: 0; padding: 0;
}
.container { max-width: 900px; margin: 0 auto; padding: 32px 24px; }
h1, h2, h3, h4 { color: var(--txt); font-weight: 800; margin-top: 28px; margin-bottom: 14px; }
h1 { font-size: 28px; letter-spacing: 1px; border-bottom: 1px solid var(--line); padding-bottom: 10px; }
h2 { font-size: 21px; letter-spacing: 3px; color: #fff;
     text-shadow: 0 2px 10px rgba(8,16,28,.95), 0 0 22px rgba(124,196,255,.6); }
h3 { font-size: 17px; color: var(--bone2); filter: drop-shadow(0 0 8px rgba(124,196,255,.3)); }
p { margin: 12px 0; }
strong { color: var(--bone2); }
a { color: var(--bone); text-decoration: none; border-bottom: 1px solid transparent; transition: all .2s; }
a:hover { color: var(--bone2); border-bottom-color: var(--bone-dim); }
code { background: rgba(124,196,255,.08); color: var(--bone2); padding: 2px 6px;
       border-radius: 4px; border: 1px solid rgba(124,196,255,.13); }
pre { background: rgba(4,9,16,.9); border: 1px solid var(--line); border-radius: 10px;
      padding: 16px 18px; overflow-x: auto; margin: 16px 0;
      box-shadow: inset 0 0 20px rgba(0,0,0,.4); }
pre code { background: transparent; border: none; padding: 0; color: var(--sub); }
table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 16px 0; }
th { font-size: 10.5px; letter-spacing: 2px; color: var(--dim); text-transform: uppercase;
    text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--line); }
td { padding: 11px 12px; border-bottom: 1px solid rgba(124,196,255,.08); }
tr:hover td { background: rgba(124,196,255,.04); }
ul, ol { margin: 12px 0; padding-left: 24px; }
li { margin: 6px 0; }
li::marker { color: var(--thread); }
blockquote { border-left: 3px solid var(--red); background: rgba(255,77,99,.05);
             padding: 14px 18px; margin: 16px 0; border-radius: 0 10px 10px 0; }
"""


def convert_md_to_html(md_text: str, title: str) -> str:
    """将 Markdown 文本转换为带荧枝风格的 HTML 页面。"""
    # 提取标题（第一个 # 开头行）
    first_line = md_text.split("\n")[0].strip()
    if first_line.startswith("# "):
        title = first_line[2:].strip()

    # 转换 Markdown 为 HTML 片段
    body_html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "codehilite"],
    )

    # 包装为完整 HTML 页面
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Zephyr 源码阅读指南</title>
  <style>{LUMINOUS_CSS}</style>
</head>
<body>
  <div class="container">
    {body_html}
    <hr>
    <p style="font-size:12px;color:var(--dim);letter-spacing:1.5px;">
      theme: zephyr luminous branch · Zephyr 源码阅读指南
    </p>
  </div>
</body>
</html>"""


def main():
    if not GUIDE_DIR.exists():
        raise SystemExit(f"指南目录不存在: {GUIDE_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(GUIDE_DIR.glob("*.md"))
    if not md_files:
        raise SystemExit(f"指南目录中没有 Markdown 文件: {GUIDE_DIR}")

    print(f"找到 {len(md_files)} 个指南文件")

    for md_file in md_files:
        print(f"  转换: {md_file.name}")
        md_text = md_file.read_text(encoding="utf-8")
        html = convert_md_to_html(md_text, md_file.stem)
        out_file = OUTPUT_DIR / f"{md_file.stem}.html"
        out_file.write_text(html, encoding="utf-8")

    # 生成指南索引页
    index_items = []
    for md_file in md_files:
        title = md_file.stem
        # 提取描述（第一个非标题行）
        lines = md_file.read_text(encoding="utf-8").split("\n")
        desc = ""
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith(">"):
                desc = line[:60]
                break
        index_items.append(f'<li><a href="{title}.html">{title}</a> - {desc}</li>')

    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Zephyr 源码阅读指南</title>
  <style>{LUMINOUS_CSS}</style>
</head>
<body>
  <div class="container">
    <h1>Zephyr 源码阅读指南</h1>
    <p>系统化的 Zephyr RTOS 源码导读，从整体架构到关键子系统。</p>
    <h2>指南目录</h2>
    <ul>
      {''.join(index_items)}
    </ul>
    <hr>
    <p style="font-size:12px;color:var(--dim);letter-spacing:1.5px;">
      theme: zephyr luminous branch
    </p>
  </div>
</body>
</html>"""
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"指南索引已生成: {OUTPUT_DIR / 'index.html'}")
    print("完成")


if __name__ == "__main__":
    main()
