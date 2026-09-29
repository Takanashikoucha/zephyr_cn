# 中文翻译进度管理

## 总体进度

| 批次 | 目录 | 文件数 | 状态 | 完成日期 |
|---|---|---|---|---|
| 1 | introduction | 1 | 已完成 | 2026-09-29 |
| 2 | kernel | 65 | 已完成 | 2026-09-29 |
| 3 | build | 94 | 待开始 | - |
| 4a | develop (前 70) | 70 | 待开始 | - |
| 4b | develop (后 68) | 68 | 待开始 | - |
| 5a | hardware (前 62) | 62 | 待开始 | - |
| 5b | hardware (后 61) | 61 | 待开始 | - |
| 6a | services (前 60) | 60 | 待开始 | - |
| 6b | services (61-120) | 60 | 待开始 | - |
| 6c | services (121-180) | 60 | 待开始 | - |
| 6d | services (181-240) | 60 | 待开始 | - |
| 6e | services (241-300) | 60 | 待开始 | - |
| 6f | services (301-359) | 59 | 待开始 | - |
| 7 | releases | 43 | 待开始 | - |
| 8 | security+contribute+project+safety | 60 | 待开始 | - |

## 已完成

- [x] 基础设施（conf.py + 荧枝主题 + Actions workflow）
- [x] introduction 核心文件（index + 部分子页）
- [x] kernel 全部 65 个文件（data_structures + memory_management + services + usermode + timing_functions + util）
- [x] develop 框架（index）
- [x] build 框架（index）
- [x] hardware 框架（index）
- [x] 源码阅读指南（7 篇）
- [ ] Pages 部署问题：自定义域名 blog.kouchalab.win 的 _static 文件 404，CNAME 文件修改未生效，需用户手动在 Settings 删除自定义域名

## 翻译规范

- 源文件：`doc/` 目录下的 `.rst` 文件
- 目标文件：`docs_cn/` 对应路径
- 语言：简体中文，技术术语保留英文原文
- 格式：保持 rst 结构不变，仅翻译正文
- 验证：每批翻译后运行 `sphinx-build` 确认无错误
