.. _api_lifecycle:

API 生命周期
#############

使用 Zephyr API 的开发者需要知道一个给定的 API 在未来版本中不会发生变化的可信期限。
与此同时，负责维护和扩展 Zephyr API 的开发者需要能够引入尚未完全验证的新 API，
并在旧 API 不再最优或不再被底层平台支持时将其淘汰。


.. figure:: api_lifecycle.png
    :align: center
    :alt: API Life Cycle
    :figclass: align-center

    API Life Cycle

所有 API 及其成熟度的最新列表可在 :ref:`api_overview` 页面中查阅。


.. _api_lifecycle_experimental:

实验性
*************

实验性 API 表示该功能最近引入，可能在未来版本中发生变更或被移除。
请试用它，并通过 `Developer mailing list <https://lists.zephyrproject.org/g/devel>`_ 向社区提供反馈。

以下要求适用于所有新 API：

- API 的文档（用法说明），解释其设计和假设、如何使用、当前实现的局限性，
  以及（如适用）未来的潜力。
- API 的引入应伴随至少一个该 API 的实现（对于外设 API，这对应一个驱动）。
- 至少一个使用新 API 的示例（可能仅能在单块开发板上构建）。

在引入新的实验性 API 时，应在定义该 API 的头文件中标记 API 版本。
实验性 API 的版本号中，次版本号应不超过 1（0.1.z）。（参见 :ref:`api_overview`）

外设 API（硬件相关）
==================================

在为新外设或驱动子系统引入 API（带文档的公共头文件）时，
必须对 API 进行审查，该审查由来自不同厂商的代表组成的架构工作组推动。

当 API 在至少两个不同的硬件平台上拥有两个实现时，
应将其提升为 ``unstable``。

.. _api_lifecycle_unstable:

不稳定
********

API 正在趋于稳定，但尚未经过足够的实际测试以被视为稳定。
API 在性质上被认为是通用的，可以在不同的硬件平台上使用。

当 API 状态变更为不稳定 API 时，应在定义该 API 的头文件中标记 API 版本。
不稳定 API 的版本号中，次版本号应大于 1（0.y.z | y > 1）。（参见 :ref:`api_overview`）

.. note::

   变更将不会提前公告。

外设 API（硬件相关）
==================================

当 API 在至少两个不同的硬件平台上拥有两个实现时，
应将其从 ``experimental`` 提升为 ``unstable``。

硬件无关 API
=======================

对于硬件无关 API，需要多个应用程序在使用它之后，
才能将其从 ``experimental`` 提升为 ``unstable``。

.. _api_lifecycle_stable:

稳定
*******

API 已被证明令人满意，但底层代码的清理可能导致小的变更。
在合理的情况下，将保持向后兼容性。

API 在满足以下要求后可被声明为 ``stable``：

- 新 API 的测试用例，覆盖率 100%。
- 代码中的完整文档。所有公共接口都应被文档化并可在在线文档中查阅。
- API 已在使用中，并已在至少 2 个开发版本中可用。
- 稳定 API 可以随时获得向后兼容的更新、缺陷修复和安全修复。

为了将 API 声明为 ``stable``，需要遵循以下步骤：

#. 必须提交一个 Pull Request，更改 :ref:`api_overview` 表格中对应的条目。
#. 必须向 ``devel`` 邮件列表发送一封邮件，公告该 API 升级请求。
#. 该 Pull Request 必须提交到下一次 `Zephyr Architecture meeting`_ 讨论，
   若无异议，该 Pull Request 将被合并。

当 API 状态变更为稳定 API 时，应在定义该 API 的头文件中标记 API 版本。
稳定 API 的版本号中，主版本号应大于或等于 1（x.y.z | x >= 1）。（参见 :ref:`api_overview`）

.. _breaking_api_changes:

引入破坏性 API 变更
================================

如前所述，稳定 API 在其整个生命周期中力求保持向后兼容。
然而，在某些情况下，实现这一目标会阻碍技术进步，
或者在不给 API 及其实现的维护带来不合理负担的情况下根本不可行。

破坏性 API 变更被定义为：迫使用户修改现有代码以维持其应用程序当前行为的变更。
仅需要重新编译应用程序（而不修改应用程序本身）不被视为破坏性 API 变更。

为了限制和控制引入破坏向后兼容承诺的变更，
每当认为此类变更有必要时，必须遵循以下步骤才能被项目接受：

#. 必须在 GitHub 上打开一个 :ref:`RFC issue <rfcs>`，包含以下内容：

   .. code-block:: none

      Title:     RFC: Breaking API Change: <subsystem>
      Contents:  - Problem Description:
                   - Background information on why the change is required
                 - Proposed Change (detailed):
                   - Brief description of the API change
                 - Detailed RFC:
                   - Function call changes
                   - Device Tree changes (source and bindings)
                   - Kconfig option changes
                 - Dependencies:
                   - Impact to users of the API, including the steps required
                     to adapt out-of-tree users of the API to the change

   RFC issue 可以链接到一个包含这些代码形式变更的 Pull Request，
   以替代对变更的书面描述。
#. 该 RFC issue 必须被标记为 GitHub 的 ``Breaking API Change`` 标签。
#. 该 RFC issue 必须提交到下一次 `Zephyr Architecture meeting`_ 讨论。
#. 必须向 ``devel`` 邮件列表发送一封邮件，主题与 RFC issue 标题相同，
   并链接到该 RFC issue。

随后，该 RFC 将通过 issue 评论获得反馈，
并将在 Zephyr 架构会议上讨论，利益相关者和整个社区将有机会详细讨论。

最后，如果尚未在第一步中完成，必须在 GitHub 上提交一个 Pull Request。
由提出变更的人决定是同时引入 RFC 和 Pull Request，
还是等到 RFC 获得足够共识后再推进实施，
以确信该变更将被接受。
该 Pull Request 必须包含以下内容：

- 与 RFC issue 匹配的标题。
- 指向 RFC issue 的链接。
- 对 API 的实际变更：

  - API 头文件的变更
  - API 实现的变更
  - 相关 API 文档的变更
  - 设备树源文件和绑定的变更

- 将树内 API 用户适配到该变更所需的修改。
  根据该任务的范围，可能需要相应维护者的额外帮助。
- 在下一个即将发布的版本的发布说明的 "API Changes" 部分中添加条目。
- ``API``、``Breaking API Change`` 和 ``Release Notes`` 标签，
  以及其他适用的标签。
- 如果该 RFC 尚未在 `Zephyr Architecture meeting`_ 中讨论并达成一致，
  还需添加 ``Architecture Review`` 标签。

完成上述步骤后，提案的结果将取决于相应子系统维护者
对实际 Pull Request 的批准。与其他任何 Pull Request 一样，
作者可以请求在 `Zephyr TSC meeting`_ 中讨论，甚至最终进行投票。

如果该 Pull Request 被合并，则必须向 ``devel`` 和 ``user`` 邮件列表
发送邮件，通知他们该变更。

API 版本号应被更改以标记向后不兼容的变更。
这通过递增主版本号（X.y.z | X > 1）来实现。
它也可以包含次版本号和补丁级别的变更。
当主版本号递增时，补丁版本号和次版本号必须重置为 0。（参见 :ref:`api_overview`）

.. note::

   破坏性 API 变更将在迁移指南中列出并描述。

Deprecated
***********

.. note::

   不稳定 API 可以在任何时间不经弃用直接移除。
   API 的弃用和移除将在发布说明的 "API Changes" 部分中公告。

弃用现有 API 的以下要求：

- 弃用时间（稳定 API）：2 个发布版本。
  API 需要在至少两个完整版本中被标记为已弃用。
  例如，如果某个 API 在 4.0 版本中首次被弃用，
  那么它最早在 4.2 版本中可以被移除。
  可能存在特殊情形，由架构工作组决定提前弃用某个 API。
- 弃用时需要做的：

  - 标记为已弃用。这可以通过编译器本身实现
    （函数声明使用 ``__deprecated``，宏定义使用 ``__DEPRECATED_MACRO``），
    或者通过引入一个 Kconfig 选项（通常包含 ``DEPRECATED`` 字样）来实现，
    启用该选项可将 API 恢复为其先前的形式。
  - 记录该弃用。
  - 在下一个即将发布的版本的发布说明的 "API Changes" 部分中包含该弃用。
  - 使用已弃用 API 的代码需要被修改以移除对该 API 的使用。
  - 变更需要是原子的且可二分查找的。
  - 在相应版本的 `GitHub issue <https://github.com/zephyrproject-rtos/zephyr/labels/deprecation_tracker>`_
    中添加条目，跟踪已弃用 API 的移除。
    在此示例中，即对应 4.2 版本的那个。

在弃用等待期间，API 将处于 ``deprecated`` 状态。
Zephyr 维护者将在 ``docs.zephyrproject.org`` 上跟踪已弃用 API 的使用情况，
并支持开发者迁移其代码。Zephyr 将继续提供以下警告：

- API 文档将告知用户该 API 已弃用。
- 构建时尝试使用已弃用 API 将向控制台记录一条警告。


Retired
*******

在此阶段，API 被移除。

目标移除日期是弃用公告后 2 个发布版本。
Zephyr 维护者将决定何时实际移除该 API：
这将取决于多少开发者已成功从已弃用 API 迁移，
以及移除该 API 的紧迫程度。

如果移除该 API 是可行的，它将被移除。
维护者将移除对应的文档，并以通常的方式通知该移除：
发布说明、邮件列表、GitHub issues 和 pull-requests。

如果移除该 API 不可行，维护者将继续支持迁移，
并更新路线图，目标是移除该 API 在下一个发布版本中移除。

.. _`Zephyr TSC meeting`: https://github.com/zephyrproject-rtos/zephyr/wiki/Zephyr-Committee-and-Working-Group-Meetings#technical-steering-committee-tsc
.. _`Zephyr Architecture meeting`: https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group