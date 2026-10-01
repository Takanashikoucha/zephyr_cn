.. _contribute_to_zephyr:

贡献 Zephyr
######################

来自社区的贡献是项目的骨干。无论是提交代码、改进文档
还是提议新功能，你的努力都备受赞赏。本页列出了
有用的资源和指南，帮助你在贡献之旅中前行。

通用指南
==================

.. toctree::
   :maxdepth: 1
   :hidden:

   guidelines.rst
   contributor_expectations.rst
   reviewer_expectations.rst
   coding_guidelines/index.rst
   style/index.rst
   proposals_and_rfcs.rst
   modifying_contributions.rst
   pr_lifecycle_policy.rst


:ref:`contribute_guidelines`
   了解向 Zephyr 项目贡献的整体流程和指南。

   本页是首次贡献者的必读内容，因为它包含如何确保
   你的贡献可以被考虑纳入项目并可能合并的重要信息。

:ref:`contributor-expectations`
   本文档是另一份必读内容，描述了项目*所有*
   贡献者的预期行为。

:ref:`reviewer-expectations`
   本文档是另一份必读内容，描述了审查项目贡献时
   的预期行为。

:ref:`coding_guidelines`
   代码贡献应遵循一套编码指南以确保代码库的
   一致性和可读性。

:ref:`coding_style`
   代码贡献应遵循一套风格指南以确保代码库的
   一致性和可读性。

:ref:`rfcs`
   了解何时以及如何为新功能和项目更改
   提交 RFC（征求评论）。

:ref:`modifying_contributions`
   修改其他开发者贡献的指南以及如何对待
   过时的 pull request。

:ref:`pr_lifecycle_policy`
   保持开放 pull request 专注于正在积极进行
   且可能合并的工作的策略。

文档
=============

Zephyr 项目依靠良好的文档蓬勃发展。无论是作为
代码贡献的一部分还是作为独立工作，贡献文档
对项目特别有价值。

.. toctree::
   :maxdepth: 1
   :hidden:

   documentation/guidelines.rst
   documentation/generation.rst

:ref:`doc_guidelines`
   本页提供了使用 reStructuredText（reST）标记语言
   和 Sphinx 文档生成器编写文档的一些简单指南。

:ref:`zephyr_doc`
   在编写文档时，查看渲染后的效果可能很有帮助。

   本页描述如何在本地构建 Zephyr 文档。


处理外部组件
==================

.. toctree::
   :maxdepth: 1
   :hidden:

   external.rst
   bin_blobs.rst

:ref:`external-contributions`
   对 Zephyr 有用的基础功能或特性可能已在其他
   开源项目中现成可用，建议并鼓励重用此类代码。
   本页更详细地描述何时以及如何将外部源代码
   导入 Zephyr。

:ref:`external-tooling`
   类似地，编译、代码分析、测试或仿真期间使用的
   外部工具可能有益，并在本节中涵盖。

:ref:`bin-blobs`
   由于某些功能可能仅通过以二进制形式分发的
   可执行代码才能提供，本页描述向项目
   :ref:`贡献二进制 blob <blobs-process>`
   的流程和指南。

需要沿途的帮助？
==================

如果你有与贡献流程相关的问题，Zephyr 社区在这里帮助你。
你可以加入我们的 `Discord`_ 频道或使用 `开发者邮件列表`_。


.. _Discord: https://chat.zephyrproject.org
.. _开发者邮件列表: https://lists.zephyrproject.org/g/devel
