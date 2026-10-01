.. _contribute_guidelines:

贡献指南
#######################

作为一个开源项目，我们欢迎并鼓励社区直接向项目提交补丁。在我们的协作开源环境中，提交变更的标准和方法有助于减少活跃开发社区可能导致的混乱。

本文档解释了如何参与项目讨论、记录 bug 和增强请求，以及向项目提交补丁，使你的补丁能够快速被代码库接受。


前提条件
*************

.. _Zephyr Project website: https://zephyrproject.org

作为贡献者，你需要熟悉 Zephyr 项目，如何配置、安装和使用它（如 `Zephyr 项目网站`_ 中所述），以及如何设置你的开发环境（如 Zephyr :ref:`getting_started` 中介绍的）。

你应该熟悉常见的开发者工具，如 Git 和 CMake，以及 GitHub 等平台。

如果你还没有这样做，你需要在 https://github.com 上创建一个（免费的）GitHub 账户，并在你的开发系统上准备好 Git 工具。

.. note::
    Zephyr 开发工作流支持所有 3 个主要操作系统（Linux、macOS 和 Windows），但下面各节中使用的一些工具仅在 Linux 和 macOS 上可用。在 Windows 上，而不是自己运行这些工具，你需要依赖使用 Github Actions 的持续集成（CI）服务，该服务在你提交 Pull Request（PR）时在 GitHub 上自动运行。你可以在 PR 对话列表末尾附近的 workflow 详情链接中查看任何失败结果。有关更多信息，参见 `持续集成`_


.. _licensing_requirements:

许可证
*********

许可证对开源项目非常重要。它有助于确保软件继续按照作者期望的条款可用。

.. _Apache 2.0 license:
    https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _GitHub repo: https://github.com/zephyrproject-rtos/zephyr

Zephyr 使用 `Apache 2.0 许可证`_（如项目 `GitHub 仓库`_ 中的 LICENSE 文件所示）来在开放贡献和允许你按自己的意愿使用软件之间取得平衡。Apache 2.0 许可证是一种宽松的开源许可证，允许你自由使用、修改、分发和销售包含 Apache 2.0 许可软件的你自己的产品。（有关此的更多信息，请查看 `为什么选择 Apache 2.0 许可证`_ 和 `Apache 许可证十大问题解答`_ 等文章）。

.. _Why choose Apache 2.0 licensing:
    https://www.zephyrproject.org/faqs/#1571346989065-9216c551-f523

.. _Top 10 Apache License Questions Answered:
    https://www.whitesourcesoftware.com/whitesource-blog/top-10-apache-license-questions-answered/

许可证告诉你作为开发者拥有哪些权利，由版权持有者提供。重要的是贡献者完全理解许可权利并同意它们。有时版权持有者不是贡献者，例如当贡献者代表公司工作时。

使用其他许可证的组件
===============================

Zephyr 项目中有一些导入或复用的组件使用其他许可，如 :ref:`Zephyr_Licensing` 中所述。

从使用 Apache 2.0 许可证以外的许可证的其他项目中导入代码到 Zephyr OS 需要完全理解上下文并由 Zephyr 治理委员会批准。

通过仔细审查潜在的贡献，同时对贡献的代码执行 :ref:`DCO`，我们可以确保 Zephyr 社区能够使用 Zephyr 项目开发产品，而无需担心专利或版权问题。

有关导入组件的此贡献和审查流程的更多信息，参见 :ref:`external-contributions`。

.. only:: latex

    .. toctree::
       :maxdepth: 1

       ../LICENSING.rst

.. _copyrights:

版权和许可证声明
=============================

Zephyr 遵循 SPDX/REUSE 风格的文件头。在每个文件的顶部添加机器可读的版权声明和许可证标识符，以便工具可以检测它们（例如 :ref:`west spdx <west-spdx>`，它使用 `REUSE 工具`_）。

Zephyr 项目遵循 Linux 基金会的 `社区最佳实践`_ 版权声明，因此我们建议使用以下版权声明：

.. code-block:: none

    SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors

在旁边包含许可证标识符：

.. code-block:: none

    SPDX-License-Identifier: Apache-2.0

实用指南：

- 将这两行放在文件的最顶部，使用文件的原生注释语法。
- 如果你创作了实质性的原创内容，你*可以*为自己或你的组织添加额外的一行。

.. _Community Best Practice:
    https://www.linuxfoundation.org/blog/copyright-notices-in-open-source-software-projects/

.. _REUSE tool:
    https://github.com/fsfe/reuse-tool

.. _DCO:

开发者起源证明（DCO）
***************************************

为了善意地确保满足许可标准，Zephyr 项目要求遵循开发者起源证明（DCO）流程。

DCO 是附加在每个开发者所做的每个贡献上的证明。在贡献的 commit message 中（本文档后面更完整地描述），开发者只需添加一个 ``Signed-off-by`` 声明，从而同意 DCO。

当开发者提交一个补丁时，这是贡献者有权按许可证提交补丁的承诺。DCO 协议如下所示，也在 https://developercertificate.org/ 上。

.. code-block:: none

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the
        best of my knowledge, is covered under an appropriate open
        source license and I have the right under that license to
        submit that work with modifications, whether created in whole
        or in part by me, under the same open source license (unless
        I am permitted to submit under a different license), as
        Indicated in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including
        all personal information I submit with it, including my
        sign-off) is maintained indefinitely and may be redistributed
        consistent with this project or the open source license(s)
        involved.

DCO 签署
=============

DCO 中的"签署"是每个 commit 日志消息中的"Signed-off-by:"行。Signed-off-by: 行必须是以下格式::

   Signed-off-by: Your Name <your.email@example.com>

对于你的 commit，替换：

- ``Your Name`` 为你的法定姓名（不允许化名、黑客代号和团体名称）

- ``your.email@example.com`` 为你用于创建 commit 的真实电子邮件地址。不允许伪或匿名电子邮件，如 ``you-id+your-username@users.noreply.github.com``。电子邮件必须与你用于创建 commit 的电子邮件匹配（如果不匹配，CI 将失败）。

你可以使用 ``git commit -s`` 自动将 Signed-off-by: 行添加到你的 commit 正文中。使用 zephyr git 历史中的其他 commit 作为示例。参见 :ref:`git_setup` 了解如何配置 Git 中的用户和电子邮件设置。

额外要求：

- 如果你在修改某人创建的一个现有 commit，你必须添加你的 Signed-off-by: 行而不删除现有的行。

.. _ai_coding_assistants:

AI 编码助手
********************

本节为使用 AI 工具和助手向 Zephyr 项目贡献的贡献者提供指导。

许可证和法律要求
================

所有贡献必须符合项目的许可证要求，并与 Zephyr 的许可证兼容（例如 Apache-2.0，参见 :ref:`licensing_requirements` 了解更多细节）。

Signed-off-by 和开发者起源证明
===============================

AI 代理**不得**添加 ``Signed-off-by`` 标签。只有人类才能合法证明 :ref:`DCO`。人类提交者负责：

- 审查所有 AI 生成的代码。
- 确保符合许可证要求。
- 添加自己的 Signed-off-by 标签以证明 DCO。
- 对贡献承担全部责任。

使用披露和署名
================

当使用 AI 工具帮助编写贡献时，适当的署名有助于跟踪 AI 在开发过程中不断变化的角色。贡献应包含以下格式的 ``Assisted-by:`` 标签：

.. code-block:: none

   Assisted-by: [Agent Name]:[Model Version] [Tool1] [Tool2]

其中：

- ``[Agent Name]`` 是 AI 工具或框架的名称。
- ``[Model Version]`` 是使用的特定模型版本。
- ``[Tool1] [Tool2]`` 是可选的专用分析工具。

基本开发工具（git、gcc、make、编辑器）不应列出。

示例：

.. code-block:: none

   Assisted-by: Claude:claude-opus-4.6 coccinelle

.. _source_tree_v2:

源代码树结构
*********************

要克隆主 Zephyr 项目仓库，使用 :ref:`get_the_code` 中的说明。

本节描述主仓库的源代码树。除了 Zephyr 内核本身，你还会找到技术文档、示例代码、支持的开发板配置和一组子系统测试的源代码。所有这些都可以供开发者贡献和增强。

理解 Zephyr 源代码树有助于定位与特定 Zephyr 功能相关的代码。

在树的顶部，几个文件很重要：

:file:`CMakeLists.txt`
    CMake 构建系统的顶层文件，包含构建 Zephyr 所需的大量逻辑。

:file:`Kconfig`
    顶层 Kconfig 文件，引用同样位于顶层目录中的 :file:`Kconfig.zephyr` 文件。

    参见 :ref:`手册中的 Kconfig 章节 <kconfig>` 了解详细的 Kconfig 文档。

:file:`west.yml`
    :ref:`west` 清单，列出由 west 命令行工具管理的外部仓库。

Zephyr 源代码树还包含以下顶层目录，每个目录可能有一个或多个未在此描述的额外子目录级别。

:file:`arch`
    特定于架构的内核和片上系统（SoC）代码。每个支持的架构（例如 x86 和 ARM）有自己的子目录，其中包含以下领域的额外子目录：

    * 特定于架构的内核源文件
    * 特定于架构的内核包含文件，用于私有 API

:file:`soc`
    SoC 相关代码和配置文件。

:file:`boards`
    开发板相关代码和配置文件。

:file:`doc`
    Zephyr 技术文档源文件和用于生成 https://docs.zephyrproject.org web 内容的工具。

:file:`drivers`
    设备驱动代码。

:file:`dts`
    :ref:`devicetree <dt-guide>` 源文件，用于描述不可发现的开发板特定硬件细节。

:file:`include`
    所有公共 API 的包含文件，除了 :file:`lib` 下定义的。

:file:`kernel`
    与架构无关的内核代码。

:file:`lib`
    库代码，包括最小标准 C 库。

:file:`misc`
    不属于其他任何顶层目录的杂项代码。

:file:`samples`
    演示 Zephyr 功能使用的示例应用程序。

:file:`scripts`
    用于构建和测试 Zephyr 应用程序的各种程序和其他文件。

:file:`cmake`
    构建 Zephyr 所需的额外构建脚本。

:file:`subsys`
    Zephyr 子系统，包括：

    * USB 设备栈代码
    * 网络代码，包括蓝牙栈和网络栈
    * 文件系统代码
    * 蓝牙主机和控制器

:file:`tests`
    Zephyr 功能的测试代码和基准测试。

:file:`share`
    额外的与架构无关的数据。它目前包含 Zephyr 的 CMake 包。

Pull Request 和 Issue
************************

.. _Zephyr Project Issues: https://github.com/zephyrproject-rtos/zephyr/issues

.. _open pull requests: https://github.com/zephyrproject-rtos/zephyr/pulls

.. _Zephyr devel mailing list: https://lists.zephyrproject.org/g/devel

.. _Zephyr Discord Server: https://chat.zephyrproject.org

在开始编写补丁之前，首先在我们的 issue `Zephyr 项目 Issues`_ 系统中查看你希望处理的 issue 上报告了什么。在 `Zephyr devel 邮件列表`_（或 `Zephyr Discord 服务器`_）上进行对话，看看其他人对你的 issue（和提议的解决方案）的看法。你可能会发现其他人也遇到了你发现的问题，或者有类似的变更或添加想法。向 `Zephyr devel 邮件列表`_ 发送消息，向开发社区介绍并讨论你的想法。

在提交自己的 issue 之前搜索现有或相关的 issue 总是一个好的做法。当你提交一个 issue（bug 或功能请求）时，分诊团队将审查并评论提交，通常在工作日内几天内。

你可以在 GitHub 上找到所有 `打开的 pull request`_，在 Github issues 中打开 `Zephyr 项目 Issues`_。

.. _git_setup:

Git 设置
*********

我们需要知道你是谁，以及如何联系你。要将此信息添加到你的 Git 安装中，将 Git 配置变量 ``user.name`` 设置为你的全名，``user.email`` 设置为你的电子邮件地址。

例如，如果你的名字是 ``Zephyr Developer``，你的电子邮件地址是 ``z.developer@example.com``：

.. code-block:: console

   git config --global user.name "Zephyr Developer"
   git config --global user.email "z.developer@example.com"

.. note::
    ``user.name`` 必须是你的全名（至少包含名和姓），而不是化名或黑客代号。你在 Git 配置中使用的电子邮件地址必须与你用于签署 commit 的电子邮件地址匹配。如果不匹配，CI 系统将使你的 pull request 失败。

    如果你打算使用 Github.com UI 编辑 commit，确保你的 github profile ``email address`` 和 profile ``name`` 也与你 git 配置中使用的匹配（``user.name`` & ``user.email``）。

Pull Request 指南
***********************
在打开新的 Pull Request 时，遵循以下指南以确保符合 Zephyr 标准并促进审查过程。

如有疑问，建议探索 Zephyr 仓库中现有的 Pull Request。使用搜索过滤器和标签定位与你提议的变更相关的 PR。

.. note::
    GitHub 的默认代码 UI 使用 4 字符制表符。然而，Zephyr 遵循 `Linux 内核编码风格`_，使用 8 字符制表符。

    为确保你对代码的视图与其他开发者一致，请前往你的 `GitHub 用户偏好设置`_ 并将制表符宽度更改为 8 个空格。

.. _Linux kernel coding style:
    https://kernel.org/doc/html/latest/process/coding-style.html#indentation

.. _user preferences on GitHub:
    https://github.com/settings/appearance

.. _commit-guidelines:

Commit Message 指南
=========================

变更作为 Git commit 提交。每个 commit 都有一个 *commit message* 描述变更。可接受的 commit message 如下所示：

.. code-block:: none

    [area]: [summary of change]

    [Commit message body (must be non-empty)]

    Signed-off-by: [Your Full Name] <[your.email@address]>

你需要将上面方括号中的文本（``[like this]``）更改为适合你的 commit。

这里是一个好的 commit message 示例。

.. code-block:: none

    drivers: sensor: abcd1234: fix bus I/O error handling

    abcd1234 传感器驱动未能检查设备响应数据包中的 flags 字段，该字段指示发生了错误。这可能导致从响应缓冲区读取无效数据。通过检查该标志并添加错误路径来修复。

    Signed-off-by: Zephyr Developer <z.developer@example.com>

[area]: [summary of change]
---------------------------

这一行称为 commit 的*标题*。标题必须：

* 一行
* 少于 72 个字符
* 后面跟一个完全空行

[area]
  ``[area]`` 前缀通常标识正在变更的代码区域。如果多个区域受到影响，它也可以标识变更的更广泛上下文。

  这里是一些示例：

  * ``doc: ...`` 用于文档变更
  * ``drivers: foo:`` 用于 ``foo`` 驱动变更
  * ``Bluetooth: Shell:`` 用于蓝牙 shell 变更
  * ``net: ethernet:`` 用于以太网相关的网络变更
  * ``dts:`` 用于全树 devicetree 变更
  * ``style:`` 用于代码风格变更

  如果你不确定使用什么，尝试运行 ``git log FILE``，其中 ``FILE`` 是你正在更改的文件，并使用更改同一文件的先前 commit 作为灵感。

[summary of change]
  ``[summary of change]`` 部分应该是你做了什么的一个快速描述。这里是一些示例：

  * ``doc: update wiki references to new site``
  * ``drivers: sensor: sensor_shell: fix channel name collision``

Commit Message 正文
-------------------

.. warning::

    不允许空的 commit message 正文。即使是琐碎的变更，也请包含描述性的 commit message 正文。如果不这样做，你的 pull request 将不通过 CI 检查。

commit 的这部分应该解释你的变更做了什么，以及为什么需要它。要具体。说"修复了一些东西"的正文将被拒绝。确保在相关时包含以下内容：

* **做了什么** 变更做了什么，
* **为什么** 你选择了该方法，
* **假设了什么** 假设了什么，以及
* **如何** 你知道它有效——例如，你运行了哪些测试。

你的 commit message 中的每一行通常应为 75 个字符或更少。使用换行符换行更长的行。例外包括包含长 URL、电子邮件地址等的行。

有关已接受的 commit message 示例，你可以参考 Zephyr GitHub `变更日志 <https://github.com/zephyrproject-rtos/zephyr/commits/main>`__。


Signed-off-by: ...
------------------

.. tip::

    你应该已经设置了 :ref:`git_setup`。使用 ``git commit -s`` 创建你的 commit，以自动使用此信息添加 Signed-off-by: 行。

出于开源许可证原因，你的 commit 必须包含一个如下所示的 Signed-off-by: 行：

.. code-block:: none

    Signed-off-by: [Your Full Name] <[your.email@address]>

例如，如果你的全名是 ``Zephyr Developer``，你的电子邮件地址是 ``z.developer@example.com``：

.. code-block:: none

    Signed-off-by: Zephyr Developer <z.developer@example.com>

这意味着你已亲自确保你的变更符合 :ref:`DCO`。因此，你必须使用你的法定姓名。不允许化名或"黑客别名"。

你的姓名和你使用的电子邮件地址必须与 Git commit 的 ``Author:`` 字段中的姓名和电子邮件匹配。

参见 :ref:`contributor-expectations` 了解对贡献者和审查者期望的更完整讨论。

添加链接
------------

.. _GitHub references:
    https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls

如果你的变更处理了特定的 GitHub issue，使用以下格式在 pull request 描述中包含引用：

.. code-block:: none

    Fixes zephyrproject-rtos/zephyr#[issue number]

仅对于 Zephyr 项目的 pull request，也可以使用短形式，例如：

.. code-block:: none

    Fixes #[issue number]

将 [issue number] 替换为相关的 GitHub issue 编号。例如：

.. code-block:: none

    Fixes zephyrproject-rtos/zephyr#1234

此语法确保在 pull request 合并时自动关闭 issue。始终指定完整的仓库路径（zephyrproject-rtos/zephyr）以避免歧义，特别是在跨多个仓库工作时。

相同的格式也可以用于 commit message。

对于链接到额外外部资源——如相关 issue、数据手册或技术参考手册——使用 ``Link:`` 标签：

.. code-block:: none

    Link: https://github.com/zephyrproject-rtos/zephyr/issues/<issue number>

.. _Continuous Integration:

持续集成（CI）
===========================

Zephyr 项目运行一个持续集成（CI）系统，该系统在每个 Pull Request（PR）上运行，以验证 PR 的多个方面：

* Git commit 格式
* 编码风格
* 多个架构和开发板的 Twister 构建
* 文档构建以验证任何文档变更

CI 在 Github Actions 上运行，它使用 `CI 测试`_ 节中描述的相同工具。在 Pull Request 可以合并之前，CI 结果必须为绿色，显示"所有检查均已通过"。在 PR 创建时运行 CI，并在每次用 commit 修改 PR 时再次运行。

CI 运行的当前状态始终可以在 GitHub PR 页面的底部找到，在审查状态下方。根据运行的成功或失败，你将看到：

* "所有检查均已通过"
* "所有检查均已失败"

在失败的情况下，你可以点击失败消息下方显示的"详细信息"链接以导航到 ``Github Actions`` 并检查结果。点击链接后，你将被带到 ``Github actions`` 摘要结果页面，其中将显示一个包含所有不同构建的表格。要查看哪个构建或测试失败，点击包含失败（即非绿色）构建的行。

.. _CI Tests:

本地运行 CI 测试
========================

.. _check_compliance_py:

check_compliance.py
-------------------

:zephyr_file:`scripts/ci/check_compliance.py` 脚本是评估代码是否符合 Zephyr 既定指南和最佳实践的有价值工具。该脚本充当一组执行各种检查（包括 linter 和 formatter）的工具的包装器。

鼓励开发者在打开新的 Pull Request 之前本地运行该脚本来验证他们的变更：

.. code-block:: bash

    ./scripts/ci/check_compliance.py -c <commit range>

检查并行运行，每个 CPU 使用一个工作进程。传入 ``-p N`` 将工作进程数限制为 ``N``，或 ``-p 1`` 顺序运行检查。

.. code-block:: bash

    ./scripts/ci/check_compliance.py -p 1 -c <commit range>

.. note::
    在 Windows 上，如果 .pl 扩展名尚未与应用程序关联，则第一次在不指定解释器的情况下运行 .pl 文件时，Windows 将询问使用什么应用程序打开 Perl 文件。将默认应用程序设置为 Strawberry Perl。默认情况下，可执行文件安装在 ``C:\Strawberry\perl\bin\perl.exe``。

KeepSorted 检查
^^^^^^^^^^^^^^^^

KeepSorted 检查确保指定的代码、配置或文档块保持排序顺序。

要使用 KeepSorted 检查，将排序内容包装在包含开始和停止标记的专用行之间，通常使用注释：

.. code-block:: c

    // zephyr-keep-sorted-start
    option_a
    option_b
    option_c
    // zephyr-keep-sorted-stop

KeepSorted 标记选项
"""""""""""""""""""""""""""

每个块的排序行为可以以几种方式自定义。为此，可以在与开始标记本身相同的行上添加以下一个或多个参数：

**re(regex_pattern)**
    启用正则表达式模式，其中仅检查匹配指定正则表达式的行的排序。其他行被忽略。

    检查 yaml 文件中排序属性的示例：

    .. code-block:: yaml

      # zephyr-keep-sorted-start re(^\s+\- name:)
      projects:
        - name: application
          revision: main
        - name: library1
          revision: feature-branch
        - name: library2
          revision: main
      # zephyr-keep-sorted-stop

**strip(characters)**
    在执行排序比较之前从行中删除指定字符。当行有应在排序期间忽略的可选前缀或后缀时，这很有用。

    从 yaml 字典键中删除引号的示例：

    .. code-block:: yaml

      # zephyr-keep-sorted-start strip(":)
      ACPI:
        status: odd fixes
      "West project: acpica":
        status: odd fixes
      # zephyr-keep-sorted-stop

**nofold**
    禁用行折叠。默认情况下，主行之后的缩进行被连接（折叠）在一起以进行排序比较。``nofold`` 选项禁用此行为并忽略缩进行。

**ignorecase**
    使用 Python 的 `str.casefold`_ 启用不区分大小写的排序。这允许在排序块中混合大写和小写项目而不会导致排序顺序违规。如果省略，默认为 Python 的字符串排序。

.. _str.casefold: https://docs.python.org/3/library/stdtypes.html#str.casefold

可以在同一标记行上组合多个选项：

.. code-block:: rst

    .. zephyr-keep-sorted-start re(^\* \w) ignorecase
    * Shell
      关于 shell 的重要消息。

    * STM32
      该供应商的更新。
    .. zephyr-keep-sorted-stop

twister
-------

.. note::
    twister 仅在 Linux 上完全支持；在 Windows 和 MacOS 上，测试的执行不支持所有目标设备。

如果你认为你的变更可能破坏某些测试，你可以将你的 PR 作为草稿提交，让项目 CI 自动为你运行 :ref:`twister_script`。

如果测试失败，你可以从 CI 运行日志中查看如何在本地重新运行它，例如：

.. code-block:: bash

    west twister -p native_sim -s tests/drivers/build_all/sensor/drivers.sensor.generic_test

.. _static_analysis:

静态代码分析
********************

Coverity Scan 是开源项目静态代码分析的一项免费服务。它基于 Coverity 的商业产品，能够分析 C、C++ 和 Java 代码。

Coverity 的静态代码分析不运行代码。相反，它使用抽象解释来获取关于代码控制流和数据流的信息。它能够跟踪程序可能采取的所有可能代码路径。例如，分析器理解 malloc() 返回的内存之后必须用 free() 释放。它跟踪所有分支和函数调用，以查看所有可能的组合是否释放内存。分析器能够检测各种各样的问题，如资源泄漏（内存、文件描述符）、NULL 解引用、释放后使用、未检查的返回值、死代码、缓冲区溢出、整数溢出、未初始化变量，等等。

结果可在 `Coverity Scan <https://scan.coverity.com/projects/zephyr>`_ 网站上查看。要访问结果，你必须自己创建一个账户。从 Zephyr 项目页面，你可以选择"将我添加到项目"以被添加到项目中。新成员必须经管理员批准。

Zephyr 代码库的静态分析每两周进行一次。静态分析工具检测到的任何问题都会自动创建 GitHub issue。这些 issue 将具有工具最初定义的相同（或等效）优先级。

为确保问责制和高效的 issue 解决，它们被分配给负责受影响代码的相应维护者。

一个专门的团队，由具有静态分析、代码质量和软件安全专业知识的成员组成，确保静态分析过程的有效性，并验证已识别的 issue 得到适当分类和及时解决。

工作流
========

如果在分析 Coverity 报告后得出结论认为是误报，请将分类设置为"False positive"或"Intentional"，操作设置为"Ignore"，所有者设置为你自己的账户，并添加一条评论说明为什么该 issue 被认为是误报或故意的。

使用详情更新 zephyr 项目中相关的 Github issue，并仅在在 scan 服务网站上完成上述步骤后关闭它。任何未修复或未在 scan 服务中忽略条目的 issue，如果该 issue 继续存在于代码中，将被自动重新打开。

.. _Contribution workflow:

贡献工作流
*********************

我们鼓励的一个普遍做法是进行小的、受控的变更。这种做法简化了审查，使合并和变基更容易，并保持变更历史清晰和干净。

在向 Zephyr 项目贡献时，你还必须尽可能多地提供关于你的变更的信息，更新适当的文档，并在提交前彻底测试你的变更。

Zephyr 开发者使用的一般 GitHub 工作流使用命令行 Git 命令和与 GitHub 的浏览器交互的组合。与 Git 一样，完成任务有多种方式。我们将在下面描述一个典型的工作流：

.. _Create a Fork of Zephyr:
    https://github.com/zephyrproject-rtos/zephyr#fork-destination-box

#. 在你的个人 GitHub 账户上 `Create a Fork of Zephyr`_。（点击 GitHub 上 Zephyr 项目仓库页面右上角的 fork 按钮。）

#. 在你的开发计算机上，进入你 :ref:`obtained the code <get_the_code>` 时创建的 :file:`zephyr` 文件夹::

     cd zephyrproject/zephyr

    将指向 `upstream repository <https://github.com/zephyrproject-rtos/zephyr>`_ 的默认远程从 ``origin`` 重命名为 ``upstream``::

     git remote rename origin upstream

    让 Git 知道你刚刚创建的 fork，将其命名为 ``origin``::

     git remote add origin https://github.com/<your github id>/zephyr

    并验证远程仓库::

     git remote -v

    输出应类似于::

     origin   https://github.com/<your github id>/zephyr (fetch)
     origin   https://github.com/<your github id>/zephyr (push)
     upstream https://github.com/zephyrproject-rtos/zephyr (fetch)
     upstream https://github.com/zephyrproject-rtos/zephyr (push)

#. 为你的工作创建一个主题分支（基于 ``main``）（如果你正在处理一个 issue，我们建议在分支名中包含 issue 编号）::

     git switch main
     git switch -c fix_comment_typo

    一些 Zephyr 子系统在 ``main`` 之外的单独分支上进行开发工作，因此你可能需要在你的 checkout 中指示这一点::

     git switch -c fix_out_of_date_patch origin/net

#. 进行变更，本地测试，变更，测试，再测试，……（也查看前面关于 `twister`_ 的章节）。

#. 当一切看起来良好时，通过添加你更改的文件开始 pull request 流程::

     git add [file(s) that changed, add -p if you want to be more specific]

    你可以使用以下命令查看尚未暂存的文件::

     git status

#. 验证要提交的变更看起来符合你的预期::

     git diff --cached

#. 将你的变更提交到你的本地仓库::

     git commit -s

    ``-s`` 选项自动将你的 ``Signed-off-by:`` 添加到你的 commit 消息中。没有这个表明你同意 :ref:`DCO` 的行，你的 commit 将被拒绝。参见 :ref:`commit-guidelines` 节了解编写 commit 消息的具体指南。

#. 将你的主题分支（包含你的变更）推送到你个人 GitHub 账户中的 fork::

     git push origin fix_comment_typo

#. 在你的 web 浏览器中，转到你 fork 的仓库，点击你刚工作的分支的 ``Compare & pull request`` 按钮，你想用它打开一个 pull request。

#. 审查 pull request 变更，验证你正在为 ``main`` 分支打开一个 pull request。你 commit 消息中的标题和消息也应该出现。

#. 一个 bot 将分配一个或多个建议的审查者（基于仓库中的 MAINTAINERS 文件）。如果你是项目成员，你现在也可以选择额外的审查者。

#. 点击提交按钮，你的 pull request 被发送并等待审查。当审查评论被做出时会发送电子邮件，或者你可以到 https://github.com/zephyrproject-rtos/zephyr/pulls 查看你的 pull request。

#. 在等待你的 pull request 被接受和合并的同时，你可以创建另一个分支来处理另一个 issue。（确保你的新分支基于 ``main`` 而不是之前的分支。）::

     git switch main
     git switch -c fix_another_issue

    并使用上面描述的相同过程在这个新的主题分支上工作。

#. 如果审查者要求对你的补丁进行更改，你可以交互式变基 commit 以修复审查问题。在你的开发仓库中::

     git rebase -i <offending-commit-id>^

    在交互式变基编辑器中，将 ``pick`` 替换为 ``edit`` 以选择特定的 commit（如果你的 pull request 中有多个），或删除该行以完全删除一个 commit。然后编辑文件以修复审查中的问题。

    如前所述，检查并测试你的变更。准备好后，继续补丁提交::

     git add [file(s)]
     git rebase --continue

    如需要更新 commit 注释，并继续::

     git push --force origin fix_comment_typo

    通过强制推送你的更新，你原来的 pull request 将用你的变更更新，因此你不需要重新提交 pull request。

#. 在推送请求的变更之后，在 PR 页面上检查是否存在合并冲突。如果有，变基你的本地分支::

      git fetch --all
      git rebase --ignore-whitespace upstream/main

    ``--ignore-whitespace`` 选项阻止 ``git apply``（由 rebase 调用）更改任何空白。解决冲突并再次推送::

      git push --force origin fix_comment_typo

    .. note:: 虽然修改 commit 和强制推送是 GitHub 之外常见的审查模型，也是 Zephyr 推荐的模型，但它不是 GitHub 支持的主要模型。强制推送可能导致意外行为，例如无法使用"查看变更"按钮（最后一个除外）——GitHub 抱怨找不到较旧的 commit。你也不总是能够比较最新审查版本与最新提交版本。在重写历史时，GitHub 仅保证访问最新版本。

#. 如果 CI 运行失败，你需要对代码进行更改以修复问题，并按上述描述通过变基修改你的 commit。有关 CI 系统的更多信息可在 `持续集成`_ 中找到。

.. _contribution_tips:

贡献技巧
================

以下是改进和加速 Pull Request 审查流程的提示列表。如果你遵循它们，你的 pull request 很可能得到所需的关注，并更快准备好合并：

.. _git-rebase:
    https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt---keep-base

#. 推送后续变更时，使用 `git-rebase`_ 的 ``--keep-base`` 选项

#. 在 PR 页面上检查变更是否仍可以无合并冲突地合并

#. 确保 PR 标题解释了正在修复或添加什么

#. 确保你的 PR 有一个正文，包含关于你提交内容的更多细节

#. 确保你在 PR 正文中引用你正在修复的 issue

#. 提交后立即关注早期 CI 结果，并在发现问题时修复

#. 在 1-2 小时后重新查看 PR，查看所有 CI 检查的状态，确保一切为绿色

#. 如果你收到变更请求并提交变更以处理它们，确保你点击 GitHub UI 上的"重新请求审查"按钮以通知请求变更的人

识别贡献来源
===============================

向树中添加新文件时，重要的是在文件中详细说明来源、提供署名并详细说明预期用途。在文件是 Zephyr 原创的情况下，commit 消息应包含以下内容（如果没有 Origin 标签，则假设"Original"）::

      Origin: Original

在文件 :ref:`imported from an external project <external-contributions>` 的情况下，commit 消息应包含关于原始项目、项目位置、文件来源 commit 的 SHA-id 和预期用途的详细信息。

例如，本地维护的导入的副本::

      Origin: Contiki OS
      License: BSD 3-Clause
      URL: https://www.contiki-os.org/
      commit: 853207acfdc6549b10eb3e44504b1a75ae1ad63a
      Purpose: 引入网络栈。

例如，模块仓库中外部维护的导入的副本::

      Origin: Tiny Crypt
      License: BSD 3-Clause
      URL: https://github.com/01org/tinycrypt
      commit: 08ded7f21529c39e5133688ffb93a9d0c94e5c6e
      Purpose: 引入 TinyCrypt

对外部模块的贡献
**********************************

遵循 :ref:`modules` 节中的指南，贡献 :ref:`new modules <submitting_new_modules>` 和提交对 :ref:`existing modules <changes_to_existing_module>` 的变更。

.. _treewide-changes:

全树变更
****************

本节描述全树变更的贡献以及一些适用于它们的额外相关要求。这些要求的存在是为了试图由于此类变更的重大影响而给予它们更多的审查和用户可见性。

定义和决策
=============================

*全树变更* 定义为对 Zephyr API、编码实践或其他开发要求的任何变更，该变更意味着需要在 zephyr 源代码仓库中进行所需的变更，或者可以合理预期对广泛的外部 Zephyr 基础源代码也是如此。

这个定义必然是非正式的。这是因为关于任何特定变更是否为全树变更的决定可能是主观的，并且可能取决于额外的上下文。

项目维护者在决定提议的变更何时为全树变更时应使用良好判断并优先考虑 Zephyr 开发者体验。旷日持久的分歧可以由 Zephyr 项目的技术指导委员会（TSC）解决，但请避免过早升级至 TSC。

全树变更的要求
=================================

- zephyr 仓库必须对任何全树变更的 issue 或 pull request 应用'treewide' GitHub 标签

- 提议全树变更的人必须在任何与变更相关的 pull request 可以合并之前，创建一个 `RFC 议题 <https://github.com/zephyrproject-rtos/zephyr/issues/new?assignees=&labels=RFC&template=003_rfc-proposal.yml>`_ 描述变更、其理由和影响等

- 项目的 `架构工作组 (WG) <https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group>`_ 必须在议程中包含该 issue，并在任何与变更相关的 pull request 可以合并之前讨论项目将接受还是拒绝该变更（如果 WG 未达成共识则升级至 TSC）

- Architecture WG 必须指定与每个单独全树变更相关的任何 PR 的合并程序，包括影响特定子系统的 pull request 所需的任何批准或额外审查时间要求

- 提议全树变更的人必须在任何与变更相关的 pull request 可以合并之前，如果 RFC 被 Architecture WG 接受，向 devel@lists.zephyrproject.org 发送关于该 RFC 的电子邮件

示例
========

一些过去的全树变更示例是：

- 弃用 :ref:`Logging API <logging_api>` 的版本 1 而支持版本 2（参见 commit `262cc55609 <https://github.com/zephyrproject-rtos/zephyr/commit/262cc55609b73ea61b5f999c6c6daaba20bc5240>`_）
- 移除对旧 :ref:`dt-bindings` 语法的支持（`6bf761fc0a <https://github.com/zephyrproject-rtos/zephyr/commit/6bf761fc0a2811b037abec0c963d60b00c452acb>`_）

注意，添加广泛使用的 API 的新版本同时保持对旧版本的支持不是全树变更。然而，此类 API 的弃用和移除是全树变更。

专用驱动要求
*******************************

独立设备的驱动应该在可能的情况下使用 Zephyr 总线 API（SPI、I2C...），以便设备可以与任何实现了兼容总线的任何供应商的任何 SoC 一起使用。

如果由于特定 SoC 系列中的专用加速器而在技术上无法使用 Zephyr API 实现完整性能，可以通过为该 SoC 系列提供专用路径来扩展对外部设备的支持。然而，驱动必须仍为所有其他 SoC 提供常规路径（通过 Zephyr API）。每个例外必须由 Architecture WG 批准才能被验证并可能被学习/改进。
