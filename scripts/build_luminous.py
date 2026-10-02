#!/usr/bin/env python3
"""
荧枝静态站点构建器
从 sphinx 生成的 HTML 中提取 body 内容，套入荧枝 HTML 模板。
"""
import os
import re
import sys
import shutil
from pathlib import Path
from html.parser import HTMLParser

# ── 路径 ──
DOCS_CN = Path(__file__).resolve().parent.parent / "docs_cn"
SPHINX_OUT = DOCS_CN / "_build" / "html"
OUT_DIR = DOCS_CN / "build_luminous"

# ── 荧枝 HTML 模板 ──
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Zephyr 中文文档</title>
  <link rel="stylesheet" href="{base}_static/pygments.css" />
  <link rel="stylesheet" href="{base}_static/luminous.css" />
  <link rel="stylesheet" href="{base}_static/sphinx-design.min.css" />
  <script src="{base}_static/fiber.js" defer></script>
  <script src="{base}_static/doctools.js"></script>
  <script src="{base}_static/sphinx_highlight.js"></script>
</head>
<body>

<nav class="topnav">
  <div class="topnav-inner">
    <a class="topnav-brand" href="{base}index.html">
      <span class="brand-dot"></span>
      <span class="brand-text">ZEPHYR</span>
      <span class="brand-sub">中文文档</span>
    </a>
    <div class="topnav-links">
      <a href="{base}index.html">首页</a>
      <a href="{base}genindex.html">索引</a>
      <a href="{base}search.html">搜索</a>
    </div>
  </div>
</nav>

{hero}

{breadcrumb}

<main class="main-content">
  <div class="content-panel">
    {body}
  </div>
</main>

<div class="bottomnav">
  {prev_btn}
  <a class="nav-home" href="{base}index.html">
    <span class="home-dot"></span>
  </a>
  {next_btn}
</div>

<footer class="site-footer">
  <span class="footer-brand">⚡ theme: zephyr luminous branch</span>
  <span class="footer-ver">v{version}</span>
  <span class="footer-copy">© 2026 Zephyr 中文文档项目</span>
</footer>

<script>
document.addEventListener('DOMContentLoaded', function() {{
  var canvas = document.getElementById('fiber-canvas');
  if (canvas && typeof initFiber === 'function') {{
    initFiber(canvas, {{ seed: 7, redBias: 0.0 }});
  }}
}});
</script>

</body>
</html>"""

HERO = """<div class="hero-section">
  <canvas id="fiber-canvas" class="fiber-bg"></canvas>
  <div class="hero-content">
    <div class="eyebrow">ZEPHYR 中文文档</div>
    <h1 class="hero-title">Zephyr 中文文档</h1>
    <p class="tagline">实时操作系统 · 中文技术文档与源码导读</p>
  </div>
</div>"""


class BodyExtractor(HTMLParser):
    """提取 <body> 标签内的内容"""
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.body_parts = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
            self.depth = 1
        elif self.in_body:
            self.depth += 1
            self.body_parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag == 'body' and self.in_body:
            self.in_body = False
        elif self.in_body:
            self.depth -= 1
            self.body_parts.append(f'</{tag}>')

    def handle_data(self, data):
        if self.in_body:
            self.body_parts.append(data)

    def handle_startendtag(self, tag, attrs):
        if self.in_body:
            self.body_parts.append(self.get_starttag_text())

    def handle_comment(self, data):
        if self.in_body:
            self.body_parts.append(f'<!--{data}-->')

    def handle_decl(self, decl):
        if self.in_body:
            self.body_parts.append(f'<!{decl}>')

    def get_body(self):
        return ''.join(self.body_parts)


def extract_body(html_path: Path) -> str:
    """从 HTML 文件中提取 body 内容，去掉旧 layout 元素"""
    content = html_path.read_text(encoding='utf-8')
    parser = BodyExtractor()
    parser.feed(content)
    body = parser.get_body()
    # 去掉旧 layout 的 topnav
    body = re.sub(r'<nav class="topnav">.*?</nav>', '', body, flags=re.DOTALL)
    # 去掉旧 layout 的 hero-section
    body = re.sub(r'<div class="hero-section">.*?</div>\s*(?=<main|<div class="breadcrumb")', '', body, flags=re.DOTALL)
    # 更精确：去掉包含 fiber-canvas 的 hero-section（贪婪匹配到对应的闭合 div）
    body = re.sub(r'<div class="hero-section">\s*<canvas.*?</div>\s*</div>', '', body, flags=re.DOTALL)
    # 去掉旧 layout 的 bottomnav
    body = re.sub(r'<div class="bottomnav">.*?</div>\s*(?=<footer)', '', body, flags=re.DOTALL)
    # 去掉旧 layout 的 site-footer
    body = re.sub(r'<footer class="site-footer">.*?</footer>', '', body, flags=re.DOTALL)
    # 去掉旧 layout 的 fiber 初始化 script
    body = re.sub(r'<script>\s*document\.addEventListener.*?</script>', '', body, flags=re.DOTALL)
    # 清理多余空白
    body = re.sub(r'\n\s*\n', '\n', body)
    return body.strip()


def get_title(html_content: str) -> str:
    """提取 <title> 内容"""
    m = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return "Zephyr 中文文档"


def get_breadcrumb(body: str) -> str:
    """从 body 中提取或生成面包屑（简化：用 h1 标题）"""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if title:
            return f'<div class="breadcrumb"><span class="bc-current">{title}</span></div>'
    return ""


def get_prev_next(html_content: str):
    """提取 prev/next 链接"""
    prev_html = re.search(r'<link rel="prev" title="([^"]+)" href="([^"]+)"', html_content)
    next_html = re.search(r'<link rel="next" title="([^"]+)" href="([^"]+)"', html_content)

    prev_btn = '<span class="nav-btn nav-placeholder"></span>'
    if prev_html:
        prev_btn = f'<a class="nav-btn nav-prev" href="{prev_html.group(2)}"><span class="nav-arrow">←</span><span class="nav-label">{prev_html.group(1)}</span></a>'

    next_btn = '<span class="nav-btn nav-placeholder"></span>'
    if next_html:
        next_btn = f'<a class="nav-btn nav-next" href="{next_html.group(2)}"><span class="nav-label">{next_html.group(1)}</span><span class="nav-arrow">→</span></a>'

    return prev_btn, next_btn


def build():
    if not SPHINX_OUT.exists():
        print(f"错误：sphinx 输出目录不存在：{SPHINX_OUT}")
        print("请先运行 sphinx 构建")
        sys.exit(1)

    # 清理输出目录
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    # 复制 _static 目录
    static_src = SPHINX_OUT / "_static"
    static_dst = OUT_DIR / "_static"
    if static_src.exists():
        shutil.copytree(static_src, static_dst)
    print(f"✓ 复制 _static/ → {static_dst}")

    # 复制 guide 目录
    guide_src = DOCS_CN.parent / "guide_html"
    guide_dst = OUT_DIR / "guide"
    if guide_src.exists():
        shutil.copytree(guide_src, guide_dst)
        print(f"✓ 复制 guide_html/ → {guide_dst}")

    # 处理所有 HTML 文件
    html_files = list(SPHINX_OUT.rglob("*.html"))
    total = len(html_files)
    ok = 0
    errors = []

    for i, html_file in enumerate(html_files):
        rel = html_file.relative_to(SPHINX_OUT)
        out_file = OUT_DIR / rel

        # 跳过 _static 内的 html
        if "_static" in rel.parts:
            continue

        try:
            content = html_file.read_text(encoding='utf-8')
            title = get_title(content)
            body = extract_body(html_file)
            prev_btn, next_btn = get_prev_next(content)

            # 计算 base 路径（回到根目录的相对路径）
            depth = len(rel.parts) - 1  # 不含文件名
            base = "../" * depth if depth > 0 else ""

            # 首页（index.html）显示 hero
            is_home = (rel == Path("index.html"))
            hero = HERO if is_home else ""

            # 非首页显示面包屑
            breadcrumb = get_breadcrumb(body) if not is_home else ""

            # 渲染模板
            page = TEMPLATE.format(
                title=title,
                base=base,
                hero=hero,
                breadcrumb=breadcrumb,
                body=body,
                prev_btn=prev_btn,
                next_btn=next_btn,
                version="4.4.99",
            )

            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(page, encoding='utf-8')
            ok += 1

        except Exception as e:
            errors.append(f"{rel}: {e}")

        if (i + 1) % 100 == 0:
            print(f"  进度: {i+1}/{total}")

    print(f"\n✓ 构建完成: {ok}/{total} 页面")
    if errors:
        print(f"⚠ {len(errors)} 个错误:")
        for e in errors[:10]:
            print(f"  {e}")

    # 统计输出大小
    total_size = sum(f.stat().st_size for f in OUT_DIR.rglob("*") if f.is_file())
    print(f"✓ 输出目录: {OUT_DIR} ({total_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    build()
