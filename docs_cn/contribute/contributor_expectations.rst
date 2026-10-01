.. _contributor-expectations:

贡献者期望
########################

Zephyr 项目鼓励 :ref:`贡献者 <contributor>`
以较小的 pull request 提交更改。
较小的 pull request（PR）具有以下好处：

- 审查更快、审查更彻底。
  审查者更容易多次抽出几分钟审查较小的更改，
  而不是分配大块时间审查一个大型 PR。

- 如果审查者或维护者拒绝更改的方向，浪费的工作更少。

- 更容易变基（rebase）和合并。
  较小的 PR 不太可能与树中的其他更改冲突。

- 如果 PR 破坏了功能，更容易回滚。

.. note::
   本页不适用于草稿 PR，草稿 PR 可以是任意大小、
   任意数量的 commit，以及任意组合的较小 PR
   用于测试和预览目的。
   草稿 PR 没有审查期望，
   从一开始就作为草稿创建的 PR 默认不会通知任何人。


定义较小的 PR
********************

- 较小的 PR 应包含一个自包含的逻辑更改。

- 添加新的大型功能或 API 时，PR 应只处理
  功能的一部分。在这种情况下，创建一个 :ref:`RFC 提案 <rfcs>`
  向审查者描述功能的其余部分。

- 在以下情况下，PR 应包含测试或示例：

   - 添加新功能或功能特性。

   - 修改功能，尤其是 API 行为契约变更。

   - 修复与硬件无关的 bug。
     测试应在未修复 bug 时失败，在应用修复后通过。

- PR 必须更新受功能性代码更改影响的所有文档。

- 如果引入新 API，PR 必须包含该 API 的使用示例。
  这为审查者提供上下文，并防止提交包含未使用 API 的 PR。


单个 PR 上的多个 Commit
*******************************

还鼓励贡献者将 PR 拆分为多个 commit。
请记住，PR 中的每个 commit 仍必须干净地构建
并通过所有 CI 测试。

例如，在引入 API 扩展时，
贡献者可以将 PR 拆分为多个 commit，
分别针对以下具体更改：

#. 引入新 API，包括共享的设备树绑定
#. 更新驱动实现 X，包含驱动特定的设备树绑定
#. 更新驱动实现 Y
#. 为新 API 添加测试
#. 添加使用该 API 的示例
#. 更新文档

大型更改
*************

对 Zephyr 项目的大型更改必须提交 :ref:`RFC 提案 <rfcs>`，
描述更改的完整范围和后续工作。
RFC 提案为审查者提供所需的上下文，
同时允许较小的、增量的 PR 获得审查并合并到项目中。
RFC 还应定义最小可行实现。

需要 RFC 提案的更改包括：

- 提交新功能。
- 提交新 API。
- :ref:`全树更改 <treewide-changes>`。
- 其他可从 RFC 提案流程中受益的大型更改。

维护者有权要求贡献者为过大或过于复杂的 PR 创建 RFC。

.. _pr_requirements:

PR 要求
***************

.. important::

   不符合以下质量期望的 pull request
   不太可能获得审查者的关注，
   审查者可能会在没有详细反馈的情况下
   要求修改此类 pull request。

   贡献者应自行审查其更改，确保在请求审查之前满足所有要求。

- PR 中的每个 commit 必须提供遵循 :ref:`commit-guidelines` 的 commit 消息。

- 不允许 fixup 或 merge commit，更多信息参见 :ref:`贡献工作流 <Contribution workflow>`。

- PR 描述必须包含更改摘要及其理由。

- PR 中的所有文件必须符合 :ref:`许可证要求<licensing_requirements>`。

- 代码必须遵循 Zephyr :ref:`编码风格 <coding_style>` 和 :ref:`编码指南 <coding_guidelines>`。

- PR 必须通过所有 CI 检查，如 :ref:`merge_criteria` 所述。
  贡献者可以将 PR 标记为草稿并明确请求审查者提供早期反馈，
  即使 CI 检查失败。

- pull request 中的 commit 应代表清晰、逻辑上的更改单元，
  便于审查并保持可二分查找性。
  以下指南对此原则进行展开：

   1. 不同的、逻辑上的更改单元

      每个 commit 应对应一个自包含的、有意义的更改。
      例如，添加功能、修复 bug 或重构现有代码应为单独的 commit。
      避免在同一 commit 中混合不同类型的更改
      （例如，功能实现和无关的重构）。

   2. 保持可二分查找性

      pull request 中的每个 commit 必须成功构建
      并通过所有相关测试。
      这确保可以有效地使用 git bisect
      来识别引入 bug 或问题的具体 commit。

   3. 压缩中间或非最终的开发历史

      在开发过程中，commit 可能包含中间更改
      （例如，部分实现、临时文件或调试代码）。
      在提交 pull request 之前，应压缩或重写这些 commit。
      移除非最终产物，例如：

      * 临时重命名文件，之后又被重新命名。
      * 在后续 commit 中被重写或大幅更改的代码。

   4. 提交前确保历史干净

      使用交互式变基（git rebase -i）
      在提交 pull request 之前清理 commit 历史。
      这有助于：

      * 将小的、不完整的 commit 压缩为单个连贯的 commit。
      * 确保每个 commit 保持可二分查找性。
      * 在提高清晰度的同时保持正确的作者署名。

   5. 重命名和代码重写

      如果在开发过程中后续 commit 重命名或重写了文件或代码，
      应压缩或重写较早的 commit 以反映最终结构。
      这确保：

      * 历史保持干净且易于跟踪。
      * 通过消除冗余的重命名或部分重写来保持可二分查找性。

   6. 作者署名

      在清理 commit 历史时，确保作者署名归属保持准确。

   7. 可读且可审查的历史

      最终的 commit 历史应便于未来的维护者理解。
      逻辑上的更改单元应分组为能讲述所做工作的
      清晰、连贯故事的 commit。

- 当添加主要新功能时，应将新功能的测试添加到自动化测试套件中。
  所有 API 函数都应有测试用例，
  并且应有 API 行为契约的测试。
  维护者和审查者有权判断所提供的测试是否充分。
  以下示例展示了如何有效测试 API 的最佳实践。

   - :zephyr_file:`内核定时器测试 <tests/kernel/timer/timer_behavior>` 为 :zephyr_file:`内核定时器 <kernel/timer.c>` 提供约 85% 的测试覆盖率（按代码行数衡量）。
   - 芯片外外设的模拟器是测试驱动 API 的有效方式。
     :zephyr_file:`电量计测试 <tests/drivers/fuel_gauge/sbs_gauge>`
     使用 :zephyr_file:`智能电池模拟器 <drivers/fuel_gauge/sbs_gauge/emul_sbs_gauge.c>`，
     为 :zephyr_file:`电量计 API <include/zephyr/drivers/fuel_gauge.h>`
     和 :zephyr_file:`智能电池驱动 <drivers/fuel_gauge/sbs_gauge/sbs_gauge.c>`
     提供测试覆盖。
   - Zephyr 项目的代码覆盖率报告可在 `Codecov`_ 上查看。

- 对 API 的不兼容更改还必须更新下一个版本的发布说明，
  详细说明该更改。
  标记为实验性的 API 不受此要求约束。

- 对 API 的更改必须根据 API 版本规则递增 API 版本号。

- 必须添加和/或更新文档以反映 PR 引入的代码更改。
  文档更改必须使用现有页面中已有的正确术语，
  并且必须用美式英语撰写。
  如果将图像作为文档的一部分，这些图像必须遵循 :ref:`doc_images` 中的规则。
  请参阅 :ref:`doc_guidelines` 获取更多信息。

- 在发布工程团队成员将 PR 合并到 zephyr 树之前，PR 还必须满足所有 :ref:`merge_criteria`。

维护者可以要求贡献者将 PR 拆分为较小的 PR，并可以要求他们创建 :ref:`RFC 提案 <rfcs>`。

.. _`Codecov`: https://app.codecov.io/gh/zephyrproject-rtos/zephyr

帮助审查者的工作流建议
========================================

- 除非作者完全按照审查者的建议操作，
  否则作者不得解决并隐藏评论，
  必须让最初的审查者来操作。
  Zephyr 项目不要求合并前解决所有评论。
  保留一些已完成的讨论有时有助于理解更大的全貌。

- 在"Files changed"视图中使用"Start Review"
  和"Add Review"绿色按钮回复评论。
  这允许回复多个评论并批量发布回复。
  这减少了发送给审查者的邮件数量。

- 由于 GitHub 未实现 |git range-diff|_，
  请尽量在审查过程中减少变基（rebase）。
  如果需要变基，将其作为单独的更新推送，
  不包含自上次推送 PR 以来的其他更改。
  仅推送变基时，在 PR 中添加评论指明哪个 commit 是变基。

.. |git range-diff| replace:: ``git range-diff``
.. _`git range-diff`: https://git-scm.com/docs/git-range-diff

让 PR 获得审查
==================

Zephyr 社区是多元化的群体，
具有不同水平的投入和优先级。
因此，审查者和维护者可能不会立即处理 PR。

- 在不活跃 1 周后，
  通过向 PR 添加评论来提醒（ping）
  PR 的受让人（Assignee）或审查者。

- 在不活跃 2 周后，
  在 Discord 的 `#pr-help`_ 频道发布消息
  并链接到该 PR。

.. _pr_technical_escalation:

PR 技术升级
=======================

在贡献者对审查者的更改请求提出异议的情况下，
Zephyr 定义了以下升级流程来解决技术分歧。

在升级技术分歧之前，请遵循以下步骤：

- 在 PR 中由受让人（Assignee）、维护者和审查者之间协商解决。

   - 如适用，由受让人担任主持人。

- 如果没有进展，受让人（维护者）有权驳回审查者
  提出的过时的、无关的或不相关的更改请求，
  给予审查者至少 1 个工作日的时间回应
  并重新审视其最初的更改请求，或启动升级流程。

   受让人有责任在 PR 中记录驳回任何审查的理由，
   并应通知审查者其审查已被驳回。

   为给审查者时间回应和升级，受让人应阻止 PR 被合并，
   方法是不批准 PR 或设置 *DNM* 标签。

参与审查过程的任何一方（受让人、审查者或更改的原始作者）均可按以下步骤触发升级：

- 通过在 PR 上添加"架构审查"（Architecture Review）标签
  升级到`架构工作组`_（Architecture Working Group）。
  除了每周处理此类升级的会议外，
  架构工作组在请求时应促进对升级的离线审查，
  特别是当任何一方无法参加会议时。

- 如果所有解决和升级途径均失败，
  受让人可以通过在 PR 上添加 *TSC* 标签升级到 TSC，
  并在 TSC 中获得有约束力的解决方案。

- 预期受让人确保升级的解决，
  并在 GitHub 上相关的 pull request 或 issue 中记录结果。

.. _#pr-help: https://discord.com/channels/720317445772017664/997527108844798012

.. _Architecture Project: https://github.com/zephyrproject-rtos/zephyr/projects/18

.. _Architecture Working Group: https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group
