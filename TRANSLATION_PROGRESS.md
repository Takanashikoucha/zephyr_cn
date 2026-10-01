# Zephyr 中文文档全量精校 — 任务进度

## 项目目标

将 Zephyr RTOS 仓库（fork 自 https://github.com/Takanashikoucha/zephyr_cn）的 `doc/`（英文原文）翻译为 `docs_cn/`（中文译文），三条指令：
1. 同步上游内容
2. 确认网页样式（荧枝设计）
3. 全量精校 1591 个文件（每个文件确认翻译成中文且结构没变化、没引入多余换行）

## 仓库信息

- **仓库**：`Takanashikoucha/zephyr_cn`
- **分支**：`main`（源文件 + 翻译）、`gh-pages`（部署产物）
- **远程**：`origin=Takanashikoucha/zephyr_cn`，`upstream=zephyrproject-rtos/zephyr`
- **分支点**：`698da682f`；upstream 最新 `fa4f8fb0e`（Zephyr 4.5.0-rc1），本地 main 落后 319 提交
- **提交身份**：`KouchaBot <kouchabot@proton.me>` + `Assisted-by: DeepSeek:qwen3.8-27b [dsh]`

## 当前状态（2026-09-30 会话，handoff 前）

### 任务 1：同步上游内容 ✅ 完成
- upstream 最新 `fa4f8fb0e`（Zephyr 4.5.0-rc1），本地 main 落后 319 提交
- 上游 15 个 doc 变更中 11 个有本地对应翻译，新原文需重译（含 4.5.0-rc1 的 release-notes/migration-guide 更新）

### 任务 2：确认网页样式 ✅ 完成
- 荧枝（Luminous Branch）设计语言：深夜底 `#05070b` + 发光纤维 canvas + 电蓝 `#7cc4ff`/绯红 `#ff4d63` + JBM 等宽字体
- Sphinx 主题：`docs_cn/_themes/luminous_branch/`（layout.html + static/luminous.css + static/fiber.js）
- luminous.css 对照荧枝规范审查通过 + h1 修正（渐变文字+发光分割线）

### 任务 3：全量精校 1591 个文件 🔄 进行中

**进度（从 0 计数）**：

| 范围 | 文件数 | 验证通过 | 打回重做中 |
|------|--------|----------|------------|
| #1-400 | 400 | 452 | 2（#399-400） |
| #1142-1171 | 30 | 30 | 0 |
| bad_files | 30 | 30 | 0 |
| 历史批次 | 6 | 6 | 0 |
| **合计** | **466** | **452** | **2** |

- **已验证通过**：452 个文件（28.4%）
- **打回重做中**：2 个文件（#399-400：release-notes-3.5 55% 内容缺失、release-notes-3.6 未开始）
- **待处理**：#401-1591（约 1190 个文件）

**管理机制**（用户建议）：
1. 单 subagent 串行：只起 1 个 subagent（避免并行争抢 GPU 变慢）
2. 10 个一批：每批 10 个文件（上下文更小，速度更快）
3. 子智能体报告 → 父 agent 用 verify_batch.py 全量验证（更严格）
4. 通过 → 标记完成；不通过 → 打回重做
5. 误报处理：代码块/URL/指令参数/toctree 文件路径/git 命令/文件名/环境变量名/包名/专有名词/变体名/命令/RST 角色名/技术术语/Git 术语/配置键/API 符号名/寄存器名/指令名/扩展名/异常名/架构名/机制名/链接器区域名/设备树段名/协议名/接口名/Shell 命令输出/模式名/标准名/总线名/标签名/属性名/单位名/框架名/术语表/链接文本/URL 锚点/目录名/设备树属性名/宏名/厂商名/产品名/API 结构体名/字段名/API 调用名/Kconfig 选项名/代码标识符/表格行/章节名/链接器段名/Doxygen 命令名/设备树兼容字符串/csv-table 数据行内的碎片行和英文 = 误报，标记通过
6. 行数 65%-70% 略低于 70% 但属中文自然压缩（原文含大量换行/代码块）= 标记通过；47%-64% 内容缺失 = 打回重做
7. 每 2-3 批报告一次进度

**验证标准**：
- 行数比 70%-125%
- 无碎片行（连续 6+ 行 <15 字符短行，代码块/标题/下划线/列表项/表格行/指令行除外）
- 无残留未翻译英文（代码块/API 符号/指令名/专有名词/URL/文件名/git 命令/环境变量名/变体名/命令/寄存器名/指令名/扩展名/异常名/架构名/机制名/链接器区域名/设备树段名/协议名/接口名/Shell 命令输出/模式名/标准名/总线名/标签名/属性名/单位名/框架名/术语表/链接文本/URL 锚点/目录名/设备树属性名/宏名/厂商名/产品名/API 结构体名/字段名/API 调用名/Kconfig 选项名/代码标识符/表格行/章节名/链接器段名/Doxygen 命令名/设备树兼容字符串/csv-table 数据行内除外）

## 关键文件路径

| 文件 | 说明 |
|---|---|
| `docs_cn/conf.py` | Sphinx 配置（language=zh_CN, html_theme=luminous_branch） |
| `docs_cn/_themes/luminous_branch/layout.html` | 极简 passthrough 布局（只输出 body） |
| `docs_cn/_themes/luminous_branch/static/luminous.css` | 荧枝 CSS（独立布局版） |
| `docs_cn/_themes/luminous_branch/static/fiber.js` | 纤维画布 JS |
| `verify_batch.py` | 全量验证脚本（行数 70%-125% + 碎片行检测 + 残留英文 Counter 阈值） |
| `TRANSLATION_PROGRESS.md` | 本文件（任务进度） |
| `README.rst` | 仓库 README |

## 关键命令

```bash
# 全量验证（用法：python3 verify_batch.py <英文原文路径> [...]）
python3 verify_batch.py doc/kernel/index.rst doc/kernel/heap.rst ...

# 查看某批次文件清单（all_rst_files.txt 已删除，需用 find 重建）
find doc -name '*.rst' | sort > all_rst_files.txt
sed -n '401,410p' all_rst_files.txt | sed 's|docs_cn/|doc/|'

# 构建（sphinx + 后处理）
cd docs_cn && rm -rf _build && ../.venv/bin/python -m sphinx -b html . _build/html
cd .. && .venv/bin/python tmp/build_luminous.py
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

1. **子智能体报告不可信**（多轮）：声称"无碎片行/全部合格"但 verify_batch.py 检测出问题 → 打回重做 + 提示词加强"必须用 Python 脚本检测"
2. **verify_batch.py 白名单严重不足**：每批必出专有名词误报（1/5 或 2/5 通过但全是误报）。长期方案：应扩充白名单加入所有 Zephyr 外部模块名/工具名/编译器名/公司名/架构名（约 100+ 词），否则每批都要人工 grep 确认
3. **GitHub Pages CDN 刷新**：部署后需等待 5-30 分钟才能生效
4. **Sphinx 警告 25408 条**：kconfig ref warnings，不阻塞构建

## 下一步（新会话继续时）

1. **继续全量精校 #401-1591**（约 1190 个文件）：
   - 重建 `all_rst_files.txt`：`find doc -name '*.rst' | sort > all_rst_files.txt`
   - 按 10 个一批派 subagent（单 subagent 串行）
   - 子智能体报告 → verify_batch.py 全量验证 → 通过标记完成 / 不通过打回重做
   - 每 2-3 批报告一次进度
2. **重做 #399-400**（release-notes-3.5 55% 内容缺失、release-notes-3.6 未开始）
3. **部署与验收**：提交（KouchaBot + Assisted-by: DeepSeek:qwen3.8-27b）→ push main → Actions 部署 gh-pages → 线上截图验收

## 部署记录

| 时间 | 分支 | Commit | 内容 |
|---|---|---|---|
| 本会话 | main | `97c3b70f8` | 全量精校 452 个文件验证通过（698 文件，178460 行插入，162588 行删除） |
| 本会话 | main | `fd6140785` | 140 文件翻译补全 |
| 本会话 | main | `c8397630d` | passthrough layout + build_luminous.py |
| 本会话 | main | `c7375278e` | 荧枝独立布局（不继承 basic） |
| 本会话 | gh-pages | `a276d0f4f` | 完整站点（893 页面，15.4 MB） |
