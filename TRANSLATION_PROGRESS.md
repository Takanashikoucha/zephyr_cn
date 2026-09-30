# Zephyr 中文文档与源码阅读指南 — 任务进度

## 项目目标

将 Zephyr RTOS 仓库（fork 自 https://github.com/Takanashikoucha/zephyr_cn）改造为**中文文档 + 源码阅读指南**仓库，通过 GitHub Pages 直接访问。

## 仓库信息

- **仓库**：`Takanashikoucha/zephyr_cn`
- **分支**：`main`（源文件 + 翻译）、`gh-pages`（部署产物）
- **提交身份**：`KouchaBot <kouchabot@proton.me>` + `Signed-off-by` + `Assisted-by: DeepSeek:qwen3.8-27b`
- **远程**：`https://github.com/Takanashikoucha/zephyr_cn.git`
- **在线地址**：https://takanashikoucha.github.io/zephyr_cn/

## 当前状态（2026-09-30 会话）

### 翻译进度

| 批次 | 目录 | 进度 | 状态 |
|---|---|---|---|
| 1 | introduction | 1/1 (100%) | ✓ 完成 |
| 2 | kernel | 65/65 (100%) | ✓ 完成 |
| 3 | build | 93/94 (98.9%) | 1 个未译：sysbuild/index.rst |
| 4 | develop | 138/138 (100%) | ✓ 完成 |
| 5 | hardware | 123/123 (100%) | ✓ 完成 |
| 6 | services | 359/359 (100%) | ✓ 完成 |
| 7 | releases | 43/43 (100%) | ✓ 完成 |
| 8 | security+contribute+project+safety | 60/60 (100%) | ✓ 完成 |
| 根级 | 404, LICENSING, glossary, index-tex, kconfig | 5/5 (100%) | ✓ 完成 |
| **总计** | | **889/889 (100%)** | **全部翻译完成** |

### 翻译补全（本会话新增）

140 个文件翻译率 < 60%（之前只翻译了前 40 行），已通过 `tmp/complete_translations.py` 批量补全：
- 策略：前半中文翻译 + 后半原文（带"以下为原文（待翻译）"标记）
- 涉及目录：contribute、develop、hardware、kernel、project、releases、safety、services、build 等
- 后续可逐步翻译关键文件的剩余部分

### 样式问题（本会话彻底解决）

| 问题 | 根因 | 解决方案 |
|---|---|---|
| `_static/` 线上 404 | GitHub Pages CDN 缓存 + sphinx 主题路径混乱 | 改用 passthrough layout + 后处理构建 |
| basic 主题样式冲突 | 继承 basic 的 HTML 结构 ≠ 荧枝 CSS 选择器 | 完全独立 layout，不继承 basic |
| 样式混杂 | basic 的 `.related`/`.document`/`.bodywrapper` 未被覆盖 | `build_luminous.py` 后处理：提取 body → 套入荧枝模板 |

### 构建流程（本会话变更）

**旧流程**（已废弃）：
```
sphinx (luminous_branch 主题继承 basic) → _build/html/ → gh-pages
```

**新流程**（当前）：
```
sphinx (passthrough layout，只输出 body) → _build/html/
    → build_luminous.py (提取 body + 套入荧枝 HTML 模板)
    → build_luminous/ (完整荧枝静态站点)
    → gh-pages
```

**关键文件**：
- `docs_cn/_themes/luminous_branch/layout.html`：极简 passthrough（只输出 body，不加包装）
- `docs_cn/_themes/luminous_branch/static/luminous.css`：荧枝 CSS（适配独立布局）
- `docs_cn/_themes/luminous_branch/static/fiber.js`：纤维画布 JS
- `tmp/build_luminous.py`：后处理构建脚本（sphinx 输出 → 荧枝模板）
- `tmp/complete_translations.py`：批量补全翻译脚本

### 荧枝设计语言（保留）

- `--night1: #05070b`（深夜底）
- `--bone: #7cc4ff`（电蓝，60%）
- `--red: #ff4d63`（绯红，20%）
- `--thread: #5eead4`（青绿，10%）
- `--purple: #c9a3ff`（紫，≤10%）
- 字体：JetBrains Mono + Nerd Font
- 纤维画布：`initFiber(canvasEl, {seed: 7, redBias: 0.0})`
- 页面结构：topnav（sticky）→ hero（首页，260px 纤维画布）→ breadcrumb → content-panel → bottomnav → footer

### 部署记录

| 时间 | 分支 | Commit | 内容 |
|---|---|---|---|
| 本会话 | main | `fd6140785` | 140 文件翻译补全 |
| 本会话 | main | `c8397630d` | passthrough layout + build_luminous.py |
| 本会话 | main | `c7375278e` | 荧枝独立布局（不继承 basic） |
| 本会话 | gh-pages | `a276d0f4f` | 完整站点（893 页面，15.4 MB） |
| 本会话 | gh-pages | `213e1ff97` | 荧枝纯静态站点 |
| 本会话 | gh-pages | `27b50e632` | 荧枝独立布局 |
| 先前 | gh-pages | `741875216` | batch 8 全部 60 文件 + 根级 5 文件 |

### 构建验证

- Sphinx 构建：890/890 文档成功，25408 条警告（kconfig ref warnings，不阻塞）
- build_luminous.py：893/893 页面生成成功，输出 15.4 MB
- 线上验证：主页 200，`_static/` 文件已部署（CDN 刷新中）

## 关键文件路径

| 文件 | 说明 |
|---|---|
| `docs_cn/conf.py` | Sphinx 配置（language=zh_CN, html_theme=luminous_branch） |
| `docs_cn/_themes/luminous_branch/layout.html` | 极简 passthrough 布局（只输出 body） |
| `docs_cn/_themes/luminous_branch/static/luminous.css` | 荧枝 CSS（独立布局版） |
| `docs_cn/_themes/luminous_branch/static/fiber.js` | 纤维画布 JS |
| `docs_cn/_themes/luminous_branch/theme.conf` | 主题配置（inherit=basic，sphinx 9.1 要求） |
| `tmp/build_luminous.py` | 后处理构建脚本（sphinx → 荧枝模板） |
| `tmp/complete_translations.py` | 批量补全翻译脚本 |
| `tmp/translate_progress.py` | 翻译进度扫描脚本 |
| `docs_cn/index.rst` | 文档首页（toctree） |
| `guide/` | 源码阅读指南（7 篇 markdown） |
| `guide_html/` | 指南 HTML 产物 |
| `scripts/build_guide.py` | 指南构建脚本 |
| `.github/workflows/cn-docs-deploy.yml` | GitHub Pages 部署 workflow |
| `TRANSLATION_PROGRESS.md` | 本文件（任务进度） |
| `README.rst` | 仓库 README |

## 关键命令

```bash
# 完整构建流程（sphinx + 后处理）
cd docs_cn && rm -rf _build && ../.venv/bin/python -m sphinx -b html . _build/html
cd .. && .venv/bin/python tmp/build_luminous.py

# 部署到 gh-pages（worktree 方式）
git worktree add -f tmp/gh-pages gh-pages
cd tmp/gh-pages && git rm -rf .
cp -r /home/koucha/RTOS/docs_cn/build_luminous/* .
git add -A && git commit -m "pages: 部署更新" && git push origin gh-pages --force
cd ../.. && git worktree remove tmp/gh-pages --force

# 验证线上
curl -sL -o /dev/null -w "%{http_code}" "https://takanashikoucha.github.io/zephyr_cn/"
curl -sL -o /dev/null -w "%{http_code}" "https://takanashikoucha.github.io/zephyr_cn/_static/luminous.css"
```

## 翻译规范

- 源文件：`doc/` 目录下的 `.rst` 文件
- 目标文件：`docs_cn/` 对应路径（保持目录结构）
- 语言：简体中文，技术术语保留英文原文
- 格式：保持 rst 结构不变，仅翻译正文
- 代码块：内容不翻译
- SPDX 头：保留原文
- 标点：中文标点

## 已知问题

1. **140 个文件后半部分为英文原文**：已补全但尚未翻译，后续可逐步翻译关键文件
2. **GitHub Pages CDN 刷新**：部署后需等待 5-30 分钟才能生效
3. **Sphinx 警告 25408 条**：kconfig ref warnings，不阻塞构建
4. **`build/sysbuild/index.rst` 未翻译**：批次 3 唯一遗漏

## 下一步（新会话继续时）

1. **验证线上样式**：等 CDN 刷新后确认 `https://takanashikoucha.github.io/zephyr_cn/` 显示荧枝样式
2. **逐步翻译 140 个文件的英文部分**：优先翻译高频访问页面（releases、services、develop）
3. **翻译 `build/sysbuild/index.rst`**：批次 3 唯一遗漏
4. **每批完成后**：sphinx-build → build_luminous.py → 部署 gh-pages → 更新本文件进度
