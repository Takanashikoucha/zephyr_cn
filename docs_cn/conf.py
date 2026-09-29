# Zephyr 中文文档构建配置
# 独立于上游 doc/conf.py，使用荧枝风格主题
import os
import sys
from pathlib import Path

# 路径设置
DOCS_CN = Path(__file__).resolve().parent
ZEPHYR_BASE = DOCS_CN.parent

# 复用上游 Sphinx 扩展
sys.path.insert(0, str(ZEPHYR_BASE / "doc" / "_extensions"))

# -- 项目元数据 --------------------------------------------------------------

project = "Zephyr 中文文档"
copyright = "2026 Zephyr 中文文档项目"
author = "Zephyr 中文文档贡献者"
language = "zh_CN"

# 版本（从上游 VERSION 文件读取）
try:
    with open(ZEPHYR_BASE / "VERSION") as f:
        import re
        m = re.match(
            r"^VERSION_MAJOR\s*=\s*(\d+)$\n"
            r"^VERSION_MINOR\s*=\s*(\d+)$\n"
            r"^PATCHLEVEL\s*=\s*(\d+)$\n"
            r"^VERSION_TWEAK\s*=\s*\d+$\n"
            r"^EXTRAVERSION\s*=\s*(.*)$",
            f.read(),
            re.MULTILINE,
        )
        if m:
            major, minor, patch, extra = m.groups(1)
            version = ".".join((major, minor, patch))
            if extra:
                version += "-" + extra
        else:
            version = "dev"
except Exception:
    version = "dev"

release = version

# -- Sphinx 扩展 -------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.extlinks",
    "sphinx_design",
]

# 复用上游 zephyr 扩展（提供 Kconfig 指令、设备树角色等）
# 注意：部分扩展依赖外部数据（manifest、boards 等），
# 中文文档构建时可能不可用，故采用 try/except 逐个加载
_zephyr_extensions = [
    "zephyr.build_timer",
    "zephyr.kconfig",
    "zephyr.dtcompatible-role",
    "zephyr.link-roles",
    "zephyr.domain",
    "zephyr.api_overview",
]
for _ext in _zephyr_extensions:
    try:
        import importlib
        importlib.import_module(_ext)
        extensions.append(_ext)
    except ImportError:
        pass

# -- 主题 --------------------------------------------------------------------

# 荧枝风格自定义主题
html_theme = "luminous_branch"
html_theme_path = [str(DOCS_CN / "_themes")]

# 主题选项
html_theme_options = {
    "fiber_seed": 7,
    "fiber_red_bias": 0.0,
}

# -- 静态资源 ----------------------------------------------------------------

html_static_path = ["_static"]
html_extra_path = []

# -- 输出 --------------------------------------------------------------------

html_output = "html"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- 交叉引用 ----------------------------------------------------------------

# 链接到上游英文文档（便于对照）
intersphinx_mapping = {
    "zephyr": ("https://docs.zephyrproject.org/latest/", None),
}

# -- 其他 --------------------------------------------------------------------

# 代码块高亮
highlight_language = "c"

# 复制按钮
html_copy_source = True

# 页脚
html_show_sphinx = True
html_show_copyright = True

# 侧边栏
html_sidebars = {
    "**": ["globaltoc.html", "searchbox.html"],
}

# 全局 toctree
globaltoc_includehidden = True

# 排除 API 文档（中文文档不含 Doxygen 生成内容）
exclude_patterns += ["_doxygen", "_api"]
