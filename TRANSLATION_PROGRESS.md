# Zephyr 中文文档与源码阅读指南 — 任务进度

## 项目目标

将 Zephyr RTOS 仓库（fork 自 https://github.com/Takanashikoucha/zephyr_cn）改造为**中文文档 + 源码阅读指南**仓库，通过 GitHub Pages 直接访问。

## 仓库信息

- **仓库**：`Takanashikoucha/zephyr_cn`
- **Token**：见 remote URL（已嵌入）或环境变量 `GITHUB_TOKEN`（repo + pages + workflow scope）
- **分支**：`main`（源文件 + 翻译）、`gh-pages`（部署产物）
- **提交身份**：`KouchaBot <kouchabot@proton.me>` + `Signed-off-by` trailer
- **远程**：`https://github.com/Takanashikoucha/zephyr_cn.git`

## 当前状态（2026-09-29 会话结束时）

### 已完成

| 任务 | 状态 | 说明 |
|---|---|---|
| 仓库 fork + shallow clone | ✓ | `--depth 1`，68,532 个文件 |
| 中文文档框架（docs_cn/） | ✓ | conf.py + 荧枝主题 + 目录结构 |
| 荧枝主题（luminous_branch） | ✓ | 继承 basic，luminous.css + fiber.js |
| 源码阅读指南（7 篇） | ✓ | guide/ + guide_html/（build_guide.py 生成） |
| README 修改 | ✓ | 顶部添加中文文档说明卡片（commit c74afbbf9） |
| 上游 workflow 清理 | ✓ | 删除 42 个上游 CI workflow，只保留 cn-docs-deploy.yml |
| 自定义域名解除 | ✓ | 用户已删除 Takanashikoucha.github.io 的 blog.kouchalab.win 绑定 |
| 批次 1：introduction | ✓ | 1 个文件 |
| 批次 2：kernel | ✓ | 65 个文件全部翻译完成 |
| 批次 3：build（部分） | 进行中 | 32 个文件已翻译（subagent 完成），62 个待翻译 |
| 荧枝 CSS 部署修复 | 进行中 | 发现 luminous.css/fiber.js 在 static/css/ 和 static/js/ 子目录中，Sphinx 不递归复制；已复制到 static/ 根目录并更新 layout.html 路径，本地构建验证通过，但线上仍 404（GitHub Pages 缓存/构建延迟） |

### 进行中 / 待解决

1. **荧枝主题线上渲染未确认**
   - 根因：`luminous.css` 和 `fiber.js` 原在 `static/css/` 和 `static/js/` 子目录，Sphinx 只复制 `static/` 直接子文件到 `_static/`
   - 已修复：将两个文件复制到 `static/` 根目录，更新 `layout.html` 引用路径（`_static/css/luminous.css` → `_static/luminous.css`）
   - 本地构建验证：`_build/html/_static/` 中已包含 `luminous.css` 和 `fiber.js` ✓
   - 已部署到 gh-pages（commit 1efd65e3e）
   - **待验证**：线上 `https://Takanashikoucha.github.io/zephyr_cn/_static/luminous.css` 是否 200（之前多次 404，可能是 GitHub Pages 构建延迟或缓存）
   - **验证命令**：`curl -sI "https://Takanashikoucha.github.io/zephyr_cn/_static/luminous.css?cb=$(date +%s)" | grep -E "^HTTP|content-type"`
   - 期望：`HTTP/2 200` + `content-type: text/css`

2. **批次 3：build 剩余 62 个文件待翻译**
   - 已完成 32 个（cmake/index + cmake-ref/index + cmake-ref/module/ 16 个 + prop_tgt/ 1 个 + variable/ 13 个）
   - 待翻译 62 个：cmake-ref/variable/ 剩余 19 个 + dts/ 12 个 + flashing/ 2 个 + kconfig/ 7 个 + signing/ 1 个 + snippets/ 4 个 + sysbuild/ 2 个 + version/ 1 个 + zephyr_cmake_package.rst
   - 文件列表：`/tmp/build_files.txt`（94 行，前 32 个已翻译）

3. **docs_cn/index.rst toctree 更新**
   - 当前只包含 5 个顶层条目（introduction/kernel/develop/build/hardware）
   - 需添加：services/releases/security/contribute/project/safety 等（随后续批次翻译完成逐步添加）

4. **hero 区未渲染**
   - `layout.html` 的 `body` 块被 Sphinx basic 主题覆盖（basic 主题的 body 块优先级更高）
   - 导致 hero-section 纤维画布不显示
   - 可选修复：改用 `html_body_scrollable` 或自定义 `body` 块继承方式

### 待办（后续批次）

| 批次 | 目录 | 文件数 | 状态 |
|---|---|---|---|
| 3（续） | build 剩余 | 62 | 待开始 |
| 4a | develop 前 70 | 70 | 待开始 |
| 4b | develop 后 68 | 68 | 待开始 |
| 5a | hardware 前 62 | 62 | 待开始 |
| 5b | hardware 后 61 | 61 | 待开始 |
| 6a | services 前 60 | 60 | 待开始 |
| 6b | services 61-120 | 60 | 待开始 |
| 6c | services 121-180 | 60 | 待开始 |
| 6d | services 181-240 | 60 | 待开始 |
| 6e | services 241-300 | 60 | 待开始 |
| 6f | services 301-359 | 59 | 待开始 |
| 7 | releases | 43 | 待开始 |
| 8 | security+contribute+project+safety | 60 | 待开始 |

**总计**：约 980 个 rst 文件（`doc/` 目录 889 个 + 子目录）

## 关键文件路径

| 文件 | 说明 |
|---|---|
| `docs_cn/conf.py` | Sphinx 配置（language=zh_CN, html_theme=luminous_branch） |
| `docs_cn/_themes/luminous_branch/layout.html` | 荧枝主题布局模板 |
| `docs_cn/_themes/luminous_branch/static/luminous.css` | 荧枝 CSS（已从 css/ 子目录复制到根目录） |
| `docs_cn/_themes/luminous_branch/static/fiber.js` | 纤维画布 JS（已从 js/ 子目录复制到根目录） |
| `docs_cn/index.rst` | 文档首页（toctree） |
| `docs_cn/kernel/` | kernel 翻译（65 文件完成） |
| `docs_cn/build/` | build 翻译（32/94 完成） |
| `guide/` | 源码阅读指南（7 篇 markdown） |
| `guide_html/` | 指南 HTML 产物 |
| `scripts/build_guide.py` | 指南构建脚本（markdown → HTML，内联荧枝 CSS） |
| `.github/workflows/cn-docs-deploy.yml` | GitHub Pages 部署 workflow |
| `TRANSLATION_PROGRESS.md` | 本文件（任务进度） |
| `README.rst` | 仓库 README（顶部有中文文档说明卡片） |

## 关键命令

```bash
# Sphinx 构建（在 docs_cn/ 目录）
cd docs_cn && rm -rf _build && ../.venv/bin/python -m sphinx -b html . _build/html

# 指南构建
.venv/bin/python scripts/build_guide.py

# 部署到 gh-pages（worktree 方式）
git worktree add -f /tmp/gh-pages gh-pages
cd /tmp/gh-pages && git rm -rf .
cp -r /home/koucha/RTOS/docs_cn/_build/html/* .
mkdir -p guide && cp -r /home/koucha/RTOS/guide_html/* guide/
git add -A && git commit -m "pages: 部署更新" && git push origin gh-pages --force

# 验证线上 CSS
curl -sI "https://Takanashikoucha.github.io/zephyr_cn/_static/luminous.css?cb=$(date +%s)" | grep -E "^HTTP|content-type"

# 验证线上页面渲染（Playwright）
python3 tmp/verify_style.py
```

## 翻译规范

- 源文件：`doc/` 目录下的 `.rst` 文件
- 目标文件：`docs_cn/` 对应路径（保持目录结构）
- 语言：简体中文，技术术语保留英文原文（Kconfig、CMake、devicetree、Sphinx、west 等）
- 格式：保持 rst 结构不变（标题层级、目录树、代码块、引用标记），仅翻译正文
- 代码块：内容不翻译
- SPDX 头：保留原文
- 标点：中文标点
- 验证：每批翻译后运行 `sphinx-build` 确认无错误（glossary 警告非阻塞）

## 荧枝设计语言

- `--night1: #05070b`（深夜底）
- `--bone: #7cc4ff`（电蓝，60%）
- `--red: #ff4d63`（绯红，20%）
- `--thread: #5eead4`（纤维线）
- 字体：JetBrains Mono + Sarasa Mono SC + Noto Sans Mono
- 纤维画布：`initFiber(canvasEl, {seed, redBias})`

## 已知问题

1. **hero 区不渲染**：basic 主题 body 块覆盖自定义 layout body 块
2. **glossary 警告**：构建时 50-766 条警告（glossary `term` 缺失），非阻塞
3. **GitHub Pages 缓存**：部署后需等待 5-30 分钟才能生效
4. **zephyr.domain 扩展**：conf.py 中使用 `zephyr.domain`（非 `zephyr.domains`），通过 try/except importlib 加载

## 下一步（新会话继续时）

1. **验证荧枝主题线上渲染**：`curl -sI "https://Takanashikoucha.github.io/zephyr_cn/_static/luminous.css"` 确认 200 + text/css
2. **如仍 404**：检查 gh-pages 分支 `_static/` 目录是否包含 luminous.css（`curl -s "https://api.github.com/repos/Takanashikoucha/zephyr_cn/contents/_static?ref=gh-pages" | python3 -c "import sys,json; [print(i['name']) for i in json.load(sys.stdin)]"`）
3. **继续批次 3**：翻译 build 剩余 62 个文件（参考 `/tmp/build_files.txt` 第 33-94 行）
4. **每批完成后**：sphinx-build 验证 → 提交推送 main → 部署 gh-pages → 更新本文件进度
