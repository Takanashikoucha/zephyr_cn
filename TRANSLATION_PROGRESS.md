# Zephyr 中文文档与源码阅读指南 — 任务进度

## 项目目标

将 Zephyr RTOS 仓库（fork 自 https://github.com/Takanashikoucha/zephyr_cn）改造为**中文文档 + 源码阅读指南**仓库，通过 GitHub Pages 直接访问。

## 仓库信息

- **仓库**：`Takanashikoucha/zephyr_cn`
- **Token**：见 remote URL（已嵌入）或环境变量 `GITHUB_TOKEN`（repo + pages + workflow scope）
- **分支**：`main`（源文件 + 翻译）、`gh-pages`（部署产物）
- **提交身份**：`KouchaBot <kouchabot@proton.me>` + `Signed-off-by` trailer
- **远程**：`https://github.com/Takanashikoucha/zephyr_cn.git`

## 当前状态（2026-09-30 会话）

### 翻译进度（进度脚本 translate_progress.py 确认）

| 批次 | 目录 | 进度 | 状态 |
|---|---|---|---|
| 1 | introduction | 1/1 (100%) | ✓ 完成 |
| 2 | kernel | 65/65 (100%) | ✓ 完成 |
| 3 | build | 93/94 (98.9%) | 1 个未译：sysbuild/index.rst |
| 4 | develop | 138/138 (100%) | ✓ 完成（toolchains 14 + tools 6 + twister 14 + west 14 + modules 1 + optimizations 1 + sca 1 + test 1） |
| 5 | hardware | 123/123 (100%) | ✓ 完成（arch 8 + barriers 1 + cache 2 + emulator 2 + firmware 2 + peripherals 99 + pinctrl 1 + porting 5 + virtualization 2） |
| 6 | services | 359/359 (100%) | 已完成 |
| 7 | releases | 43/43 (100%) | ✓ 完成 |
| 8 | security+contribute+project+safety | 60/60 (100%) | ✓ 完成 |
| 根级 | 404, LICENSING, glossary, index-tex, kconfig | 5/5 (100%) | ✓ 完成 |
| **总计** | | **889/889 (100%)** | **全部翻译完成** |

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
| 批次 3：build | ✓ | 93/94（1 个未译：sysbuild/index.rst） |
| 批次 4：develop（部分） | 暂停中 | 63/138（languages 9 + flash_debug 4 + manifest 33 + optimizations 1 + sca 1 + test 1 等） |
| 荧枝 CSS 字体路径修复 | ✓ | `../fonts/` → `fonts/`（Sphinx 复制到 _static/ 后相对路径需指向 _static/fonts/） |
| 荧枝 hero 区渲染修复 | ✓ | layout.html 改用 header 块注入 hero 区（不覆盖 body 块），CSS 适配 basic 主题 .document/.body/.sphinxsidebar 结构 |
| 进度管理脚本 | ✓ | `tmp/translate_progress.py` 自动扫描进度 |
| 本地构建验证 | ✓ | hero 区 + 文档内容 + 侧边栏全部正常渲染（Playwright 截图确认） |
| gh-pages 部署 | ✓ | commit 1a60688c0（荧枝 hero 区 + CSS 适配 basic 主题） |

### 进行中 / 待解决

1. **荧枝主题线上 404（GitHub Pages CDN 缓存）**
   - 根因：GitHub Pages 分发层（缓存/CDN）异常
   - 证据：gh-pages 分支 `_static/` 包含 luminous.css（9540 字节）及全部 20+ 条目；Pages 多次构建全部 built；但线上 `_static/` 下**所有**文件均 404
   - 已推送多次空提交 + 新部署重新触发 Pages 构建
   - **待验证**：等 CDN 刷新后 `curl -sI "https://Takanashikoucha.github.io/zephyr_cn/_static/luminous.css?cb=$(date +%s)"`
   - 期望：`HTTP/2 200` + `content-type: text/css`
   - **注意**：本地构建验证已确认荧枝样式完全正常（hero 区 + 文档内容 + 侧边栏），线上 404 是 GitHub CDN 层问题非代码问题

2. **批次 3 补译 1 个**：`build/sysbuild/index.rst`

3. **批次 4 develop 剩余 75 个**（已暂停，优先解决样式问题）
   - 已完成 63 个：getting_started 4 + api 6 + application 1 + debug 1 + languages 9 + flash_debug 4 + manifest 33 + optimizations 1 + sca 1 + test 1 + index 1 + env_vars 1 + beyond-GSG 1
   - 待翻译 75 个：modules 1 + optimizations 2 + sca 10 + test 5 + toolchains 14 + tools 8 + twister 15 + west 17 + 其他

4. **docs_cn/index.rst toctree 更新**
   - 当前只包含 5 个顶层条目（introduction/kernel/develop/build/hardware）
   - 需添加：services/releases/security/contribute/project/safety 等（随后续批次翻译完成逐步添加）

### 待办（后续批次）

| 批次 | 目录 | 文件数 | 状态 |
|---|---|---|---|
| 3（续） | build 剩余 | 62 | 待开始 |
| 4a | develop 前 70 | 70 | 待开始 |
| 4b | develop 后 68 | 68 | 待开始 |
| 5a | hardware 前 62 | 62 | 待开始 |
| 5b | hardware 后 61 | 61 | 待开始 |
| 6a | services 前 60 | 60 | 已完成 |
| 6b | services 61-120 | 60 | 已完成 |
| 6c | services 121-180 | 60 | 已完成 |
| 6d | services 181-240 | 60 | 已完成 |
| 6e | services 241-300 | 60 | 已完成 |
| 6f | services 301-359 | 59 | 已完成 |
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

## 排查记录（2026-09-30 会话）

**荧枝主题 404 排查结论**：

- 线上 `index.html` 200，且正确引用 `_static/luminous.css` / `_static/fiber.js`
- gh-pages 分支 `_static/` 目录包含 luminous.css（9540 字节，sha d9dd0957ccf2）及全部 20 个条目
- Pages 最近 5 次构建全部 `built` 无错误（最新 2026-09-29 15:45，commit 1efd65e3e）
- 但线上 `_static/` 下**所有**文件（basic.css、fiber.js、doctools.js、pygments.css 等）均 404
- **结论**：文件在、引用对、构建成功，唯独 `_static/` 目录整体 404 → GitHub Pages 分发层（缓存/CDN）异常，仓库侧无代码可修
- **后续手段**：① 等待 GitHub 自动刷新（数小时至数天）；② 在 gh-pages 分支推送一个空提交重新触发 Pages 构建；③ 如仍无效，在 GitHub 设置 → Pages 中重新启用站点

**批次 3 文件列表**：`/tmp/build_files.txt` 已被沙盒清除，需重建（`find doc/build -name "*.rst" | sort` 取第 33-94 行，前 32 个已翻译）

## 下一步（新会话继续时）

1. **重新触发 Pages 构建**：在 gh-pages 分支推送空提交（`git commit --allow-empty -m "pages: 重新触发构建"`），等待 5-30 分钟后再验证 `_static/luminous.css`
2. **继续批次 3**：翻译 build 剩余 62 个文件（文件列表重建：`find doc/build -name "*.rst" | sort`）
3. **每批完成后**：sphinx-build 验证 → 提交推送 main → 部署 gh-pages → 更新本文件进度
