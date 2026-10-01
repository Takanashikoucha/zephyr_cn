.. _modules:

模块（外部项目）
##################

Zephyr 依赖多个外部维护项目的源代码，以避免重复造轮子，并在有意义时尽可能多地复用成熟的、久经考验的代码。在 Zephyr 构建系统的语境中，这些项目被称为*模块*。这些模块必须与 Zephyr 构建系统集成，如本页其他章节更详细地描述的那样。

要被归类为纳入默认模块列表的候选者，外部项目必须拥有 Zephyr 项目之外的独立生命周期，即位于自己的仓库中，并拥有自己的贡献和维护工作流以及发布流程。Zephyr 模块不应包含专为 Zephyr 编写的代码。相反，这类代码应贡献到 zephyr 主树。

要纳入 Zephyr 项目默认清单的模块，需要提供经项目技术指导委员会（TSC）认可并批准的功能或特性，并且应符合 :ref:`模块许可要求 <modules_licensing>` 和 :ref:`贡献指南 <modules_contributing>`。它们还应有一位致力于维护该模块代码库的 Zephyr 开发者。

Zephyr 依赖多个类别的模块，包括但不限于：

- 调试器集成
- 芯片厂商的硬件抽象层（HAL）
- 加密库
- 文件系统
- 进程间通信（IPC）库

此外，在某些情况下，模块（尤其是厂商 HAL）可以包含对可选 :ref:`二进制 blob <bin-blobs>` 的引用。

本页汇总了一系列策略和最佳实践，旨在更好地组织 Zephyr 模块中的工作流。

.. _modules-vs-projects:

模块与 west 项目
******************

本页描述的 Zephyr 模块与 :ref:`west 项目 <west-workspace>` 不是同一个概念。事实上，模块 :ref:`根本不需要 west <modules_without_west>`。然而，当 :ref:`与 west 一起使用 <modules_using_west>` 模块时，构建系统会使用 west 来查找模块。

概括来说：

模块是包含 :file:`zephyr/module.yml` 文件的仓库，这样 Zephyr 构建系统就可以从仓库中拉取源代码。
:ref:`west 项目 <west-manifests-projects>` 是 :file:`west.yml` 清单文件中 ``projects:`` 部分的条目。
west 项目通常也是模块，但并非总是如此。有些 west 项目不包含在最终固件镜像中（例如工具），因此不需要是模块。
Zephyr 构建系统通过 :ref:`west 本身 <modules_using_west>` 或 :ref:`ZEPHYR_MODULES CMake 变量 <modules_without_west>` 来查找模块。

本页的内容仅适用于模块，而不适用于一般的 west 项目（除非它们本身是模块）。

模块仓库
***********

* 默认清单中包含的所有模块都应托管在 zephyrproject-rtos GitHub 组织下的仓库中。

* 模块仓库的代码库应在仓库根目录的 :file:`zephyr/` 文件夹中包含一个 *module.yml* 文件。

* 模块仓库名称应遵循使用小写字母和短横线（而非下划线）的约定。该规则适用于所有新的模块仓库，但直接跟踪外部项目（托管在 Git 仓库中）的仓库除外；此类模块可以以其外部项目对应物的名称命名。

  .. note::

     不符合上述约定的现有模块仓库无需重命名以符合该约定。

* 模块仓库名称应在 :file:`zephyr/module.yml` 文件中显式设置。

* 模块应使用 "zephyr" 作为仓库主分支的默认名称。用于特定目的的分支，例如某个 LTS Zephyr 版本的模块分支，其名称应以 'zephyr\_' 前缀开头。

* 如果模块拥有外部（上游）项目仓库，模块仓库应保留上游仓库的文件夹结构。

  .. note::

     模块仓库中不需要维护一个镜像外部仓库 master 分支的 'master' 分支。不建议这样做，因为这可能会围绕模块的主分支（应为 'zephyr'）造成混淆。

* 模块应以以模块名称开头的包含路径公开其提供的所有头文件。（例如，mcuboot 应将其 ``bootutil/bootutil.h`` 公开为 "mcuboot/bootutil/bootutil.h"。）

.. _modules_synchronization:

与上游同步
==========

建议将模块仓库与对应外部项目的最新稳定版本同步。但是，如果需要获取模块代码库中的重要更新，则允许使用最新开发分支的尖端来更新 Zephyr 模块仓库。将模块与上游同步时，必须记录执行该特定更新的理由。

允许实践的要求
----------------------------------

对模块仓库主分支的更改（包括与上游代码库的同步）只能通过拉取请求（pull request）应用。这些拉取请求必须能够由 Zephyr CI *验证* 且可*合并*（例如使用 Github UI 的 *Rebase and merge* 或 *Create a merge commit* 选项）。这确保传入的更改始终**可审查**，且 *下游* 模块仓库的历史是增量的（即现有的提交、标签等始终被保留）。该策略还允许直接在对将引入模块仓库的一组更改上运行 Zephyr CI、git lint、身份和许可检查。

.. note::

     不允许向模块的主分支强制推送（force-push）。

允许的实践
-----------------

以下实践符合上述要求，应在所有模块仓库中遵循。由模块代码负责人选择首选的同步实践，但要求所选实践在相应模块仓库中始终被一致遵循。

**使用来自上游的 diff 更新模块：**
上游更改作为单个 *snapshot* 提交（手动 diff）通过针对模块主分支的拉取请求引入，可使用 *Rebase & merge* 操作合并。该方法简单，应适用于所有模块，缺点是在模块仓库中压制了上游历史。

  .. note::

     对于外部项目未托管在上游 Git 仓库中的模块，上述实践是唯一允许的实践。

提交信息应指明上游项目 URL、模块更新到的版本（上游版本、标签、提交 SHA，如适用等），以及执行更新的原因。

**通过合并上游分支更新模块：**
通过执行目标上游分支（例如主分支、最新 release 分支等）的 Git 合并引入上游更改，将结果通过针对模块主分支的拉取请求提交，并使用 *Create a merge commit* 操作合并该拉取请求。
该方法适用于拥有上游项目 Git 仓库的模块。该方法的主要优势是上游仓库历史（即原始提交 SHA）在模块仓库中被保留。该方法的缺点是在下游主分支中生成两个额外的合并提交。


向 Zephyr 模块贡献代码
******************************

.. _modules_contributing:


个人角色与职责
===================================

为便于管理 Zephyr 模块仓库，定义了以下个人角色。

**管理员（Administrator）：** 每个 Zephyr 模块应有一位管理员，负责管理对模块仓库的访问权限，例如应模块负责人的要求在仓库中添加个人作为协作者。模块管理员是管理员（Administrators）团队的成员，该团队是由对模块 GitHub 仓库拥有管理员权限的项目成员组成的组。

**模块负责人（Module owner）：** 每个模块应有一位模块代码负责人。模块负责人对 Zephyr 模块仓库的内容承担总体责任。具体而言，模块负责人将：

* 协调模块仓库中的代码审查
* 成为针对仓库主分支的拉取请求的默认指派人
* 视情况请求向仓库添加更多协作者
* 遵循 :ref:`modules_synchronization` 中描述的策略，定期将模块仓库与其上游对应物同步
* 关注外部项目中的安全漏洞问题，并在上游代码库中可用安全修复后尽快更新模块仓库以包含这些修复
* 在 Zephyr 发布说明中列出模块代码库中存在的任何已知安全漏洞问题。


  .. note::

     模块负责人不必是 Zephyr :ref:`维护者 <project_roles>`。

**合并者（Merger）：** Zephyr 发布工程团队有权并有责任合并模块仓库主分支中已批准的拉取请求。


维护模块代码库
===============================

zephyr 主树中的更新，例如公共 Zephyr API 的更新，可能需要修补模块的代码库。保持模块代码库最新的责任由此类更新的 Zephyr **贡献者**和模块**负责人**共同承担。具体而言：

* 原始更改在 Zephyr 中的贡献者有义务提交模块仓库中所需的相应更改，以确保包含原始更改的拉取请求上的 Zephyr CI 以及模块集成测试都能成功。

* 模块负责人对将模块代码库与 zephyr 主树同步和测试承担总体责任。这包括在 Zephyr CI 执行的测试之外偶尔对模块代码库进行高级测试。模块负责人必须修复 Zephyr 拉取请求 CI 运行未能捕获的模块代码库中的问题。


.. _modules_changes:

向模块贡献更改
===============================

直接向模块代码库提交和合并更改（即在相应外部项目仓库中合并之前）应仅限于：

* 因 zephyr 主树更新而必需的更改
* 不应等待先在外部项目中合并的紧急更改，例如安全漏洞的修复。

如果模块拥有上游项目仓库，则应不鼓励对模块代码库进行非平凡的更改，包括模块设计或功能方面的更改。在这种情况下，此类更改应直接提交到上游项目。

:ref:`向模块提交更改 <submitting_new_modules>` 详细描述了向模块仓库贡献更改的流程。

贡献指南
-----------------------

向 Zephyr 模块贡献代码应遵循项目通用的 :ref:`贡献指南 <contribute_guidelines>`。

**拉取请求：** 至少需要 2 个批准（包括 PR 指派人的批准）才能合并。此外，模块仓库中的拉取请求只有在其引入的更改使用 Zephyr CI 工具验证后才能合并，如本页其他章节更详细地描述的那样。

模块仓库主分支中拉取请求的合并必须与 zephyr 主树中相应的清单文件更新相配套。

**问题报告：** `GitHub issues`_ 在模块仓库中被有意禁用，以支持集中式的问题报告策略。涉及例如模块中的 bug 或增强功能的问题单应在 zephyr 主仓库中打开。应使用与每个模块对应的 GitHub 标签对问题进行适当标注（如适用）。

  .. note::

     允许为 zephyr 模块提交 bug 报告以跟踪相应的上游项目 bug。这些 bug 报告不应影响 :ref:`发布质量标准 <release_quality_criteria>`。


.. _modules_licensing:

许可要求与策略
***********************************

模块代码库中的所有源文件都应包含许可头，除非模块仓库有一个覆盖未包含许可头的源文件的**主许可文件**。

主许可文件应由 Zephyr 开发者添加到模块代码库中，仅当它们作为外部项目的一部分存在且包含宽松的 OSI 兼容许可时。主许可文件最好包含完整的许可文本，而不是包含 SPDX 许可标识符。如果存在多个主许可文件，应明确哪个许可适用于模块代码库中的每个源文件。

模块源文件中的单独许可头优先于主许可。

任何要添加到模块仓库的新内容都需要有许可覆盖。

  .. note::

     Zephyr 建议通过单独许可头和主许可文件来传达模块许可。这不是硬性要求；如果外部项目有自己的实践来传达许可如何适用于模块代码库（例如通过一个或多个主许可文件），只要满足许可要求（例如 OSI 兼容性），该实践可被 Zephyr 模块接受并在其中引用。

许可策略
================

创建模块仓库时，开发者应：

* 导入主许可文件（如果它们在外部项目中存在）
* 记录（例如在模块 README 或 .yml 文件中）覆盖模块代码库的默认许可。

许可检查
------------------

许可检查（通过 CI 工具）应在每个向模块仓库添加新内容的拉取请求上启用。


文档要求
**************************

所有 Zephyr 模块仓库都应包含一个 .rst 文件，记录：

* 模块的范围和目的
* 模块如何与 Zephyr 集成
* 模块仓库的负责人
* 与外部项目的同步信息（提交、SHA、版本等）
* 如 :ref:`modules_licensing` 中描述的许可信息。

该文件是模块纳入的必要条件，其中包含的信息应保持最新。


测试要求
********************

所有 Zephyr 模块应提供一定程度的**集成**测试，确保与 Zephyr 的集成正确工作。集成测试：

* 可以是以位于 zephyr 主树中的最小示例和测试集的形式
* 应验证与 Zephyr 集成的模块基本使用（配置、功能 API 等）
* 应在引入模块仓库更改的拉取请求的 twister 运行中作为一部分被构建和执行（例如在 QEMU 中）

  .. note::

     作为纳入 Zephyr 默认清单候选者的新模块应提供一定程度的集成测试。

  .. note::

     厂商 HAL 通过构建或执行在目标平台上的 Zephyr 测试得到隐式测试，因此不需要提供集成测试。

集成测试的目的不是为模块提供功能验证；这应是外部项目测试框架的一部分。

某些外部项目提供位于上游测试基础设施中但明确为 Zephyr 编写的测试套件。这些测试可以（但并非必须）成为 Zephyr 测试框架的一部分。

弃用和移除模块
*********************************

模块可能因以下原因（包括但不限于）被弃用：

* 模块缺乏维护
* 外部项目中的许可变更
* 代码库变得过时

模块信息应指示某个模块是否已弃用，构建系统应在尝试使用已弃用的模块构建 Zephyr 时发出警告。

已弃用的模块可在 2 个 Zephyr 版本发布后从 Zephyr 默认清单中移除。

  .. note::

     已移除模块的仓库应通过其原始 URL 保持可访问，因为它们被较旧的 Zephyr 版本所依赖。


在 Zephyr 构建系统中集成模块
****************************************

构建系统变量 :makevar:`ZEPHYR_MODULES` 是包含 Zephyr 模块的目录绝对路径的 `CMake 列表`_。这些模块包含 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件，分别描述如何构建和配置它们。模块的 :file:`CMakeLists.txt` 文件通过 CMake 的 `add_subdirectory()`_ 命令添加到构建中，:file:`Kconfig` 文件被包含在构建的 Kconfig 菜单树中。

如果你安装了 :ref:`west <west>`，除非你在添加新模块，否则不需要担心该变量如何定义。构建系统知道如何使用 west 来设置 :makevar:`ZEPHYR_MODULES`。你可以通过设置 :makevar:`EXTRA_ZEPHYR_MODULES` CMake 变量或在 ``.zephyrrc`` 中添加一行 :makevar:`EXTRA_ZEPHYR_MODULES` 来向该列表添加额外模块（参见 :ref:`env_vars` 章节了解更多细节）。如果你想保留用 west 找到的模块列表同时也添加自己的模块，这会有用。如果 :makevar:`EXTRA_ZEPHYR_MODULES` 在多个地方被设置，例如既作为环境变量又作为 CMake 变量，最终的额外模块列表将是所有来源的合并结果。

.. note::
    如果模块 ``FOO`` 由 :ref:`west <west>` 提供但同时也通过 ``-DEXTRA_ZEPHYR_MODULES=/<path>/foo`` 给出，则命令行变量 :makevar:`EXTRA_ZEPHYR_MODULES` 给出的模块将优先。这允许你在构建时使用 ``FOO`` 的自定义版本，同时仍使用 :ref:`west <west>` 提供的其他 Zephyr 模块。例如这对特殊测试目的会很有用。

如果你想永久地将模块添加到 zephyr 工作区且使用 zephyr 作为你的清单仓库，你还可以将一个 west 清单文件添加到 :zephyr_file:`submanifests` 目录中。参见 :zephyr_file:`submanifests/README.txt` 了解更多细节。

参见 :ref:`west-basics` 了解更多关于 west 工作区的内容。

最后，你还可以通过各种方式自己指定模块列表，或者如果你的应用不需要模块则完全不使用模块。

.. _module-yml:

模块 yaml 文件描述
****************************

模块可以使用名为 :file:`zephyr/module.yml` 的文件来描述。:file:`zephyr/module.yml` 的格式描述如下：

模块名称
===========

每个 Zephyr 模块都被赋予一个名称，可以在构建系统中引用它。

名称应在 :file:`zephyr/module.yml` 文件中指定。这将确保模块名称不能通过用户定义的目录名或 ``west`` 清单文件被更改：

.. code-block:: yaml

    name: <name>

在 CMake 中，Zephyr 模块的位置随后可以使用 CMake 变量 ``ZEPHYR_<MODULE_NAME>_MODULE_DIR`` 引用，变量 ``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 保存包含模块 :file:`CMakeLists.txt` 文件的目录的位置。

.. note::
    当用于 CMake 和 Kconfig 变量时，模块名称中的所有字母都转换为大写，所有非字母数字字符都转换为下划线 (_)。
    例如，模块 ``foo-bar`` 在 CMake 和 Kconfig 中必须被引用为 ``ZEPHYR_FOO_BAR_MODULE_DIR``。

以下是 Zephyr 模块 ``foo`` 的一个示例：

.. code-block:: yaml

    name: foo

.. note::
    如果未指定 ``name`` 字段，则 Zephyr 模块名称将被设置为模块文件夹的名称。
    例如，位于 :file:`<workspace>/modules/bar` 的 Zephyr 模块如果在 :file:`zephyr/module.yml` 中未指定任何内容，将使用 ``bar`` 作为其模块名称。

模块集成文件（模块内）
====================================

构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 的包含可以描述为：

.. code-block:: yaml

    build:
      cmake: <cmake-directory>
      kconfig: <directory>/Kconfig

``cmake: <cmake-directory>`` 部分指定 :file:`<cmake-directory>` 包含要使用的 :file:`CMakeLists.txt`。``kconfig: <directory>/Kconfig`` 部分指定要使用的 Kconfig 文件。两者都不是必需的：``cmake`` 默认为 ``zephyr``，``kconfig`` 默认为 ``zephyr/Kconfig``。

以下是一个示例 :file:`module.yml` 文件，引用模块根目录中的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件：

.. code-block:: yaml

    build:
      cmake: .
      kconfig: Kconfig

.. _sysbuild_module_integration:

Sysbuild 集成
==================

:ref:`Sysbuild <sysbuild>` 是 Zephyr 构建系统，允许作为单个应用的一部分构建多个镜像，sysbuild 构建过程可以按需通过模块从外部扩展，例如添加自定义构建步骤或向构建添加额外目标。sysbuild 特定的构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 的包含可以描述为：

.. code-block:: yaml

    build:
      sysbuild-cmake: <cmake-directory>
      sysbuild-kconfig: <directory>/Kconfig

``sysbuild-cmake: <cmake-directory>`` 部分指定 :file:`<cmake-directory>` 包含要使用的 :file:`CMakeLists.txt`。``sysbuild-kconfig: <directory>/Kconfig`` 部分指定要使用的 Kconfig 文件。

以下是一个示例 :file:`module.yml` 文件，引用模块 ``sysbuild`` 目录中的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件：

.. code-block:: yaml

    build:
      sysbuild-cmake: sysbuild
      sysbuild-kconfig: sysbuild/Kconfig

模块描述文件 :file:`zephyr/module.yml` 还可以用于指定构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 位于 :ref:`modules_module_ext_root` 中。

位于 ``MODULE_EXT_ROOT`` 中的构建文件可以描述为：

.. code-block:: yaml

    build:
      sysbuild-cmake-ext: True
      sysbuild-kconfig-ext: True

这允许在 Zephyr 模块外部描述构建包含的控制。

.. _modules-vulnerability-monitoring:

漏洞监控
========================

模块描述文件 :file:`zephyr/module.yml` 可用于改进漏洞监控。

如果你的模块需要使用外部引用跟踪漏洞（例如你的模块是从另一个仓库 fork 的），你可以使用 ``security`` 部分。它包含字段 ``external-references``，其中包含需要为你的模块监控的引用列表。支持的格式为：

- CPE（通用平台枚举，Common Platform Enumeration）
- PURL（包 URL，Package URL）

.. code-block:: yaml

    security:
      external-references:
        - <module-related-cpe>
        - <an-other-module-related-cpe>
        - <module-related-purl>

Mbed TLS 模块的一个实际示例可能如下：

.. code-block:: yaml

    security:
      external-references:
        - cpe:2.3:a:arm:mbed_tls:3.5.2:*:*:*:*:*:*:*
        - pkg:github/Mbed-TLS/mbedtls@V3.5.2

.. note::
    CPE 字段必须遵循 `NVD <https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/cpe>`_ 提供的 CPE 2.3 模式。
    PURL 字段必须遵循 `Github <https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst>`_ 提供的 PURL 规范。


构建系统集成
========================

当模块拥有 :file:`module.yml` 文件时，它将被自动纳入 Zephyr 构建系统。模块的路径随后可以通过 Kconfig 和 CMake 变量访问。

Zephyr 模块
----------------

在 Kconfig 和 CMake 中，变量 ``ZEPHYR_<MODULE_NAME>_MODULE_DIR`` 包含模块的绝对路径。

此外，``ZEPHYR_<MODULE_NAME>_MODULE`` 和 ``ZEPHYR_<MODULE_NAME>_MODULE_BLOBS``（在模块声明 blob 的情况下）符号会自动为可用模块生成。这些可用于例如声明来自依赖该模块或模块中 blob 的其他 Kconfig 符号的依赖关系。为了满足在模块不存在时构建 Zephyr 时的合规性检查，建议模块在其位于 Zephyr 主树 ``modules/`` 下的相应 Kconfig 文件中为这些符号提供默认定义。

在 CMake 中，``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 包含包含被纳入 CMake 构建系统的 :file:`CMakeLists.txt` 文件的目录的绝对路径。如果 module.yml 文件未指定 CMakeLists.txt，则该变量的值为空。

要读取 Zephyr 模块 ``foo`` 的这些变量：

- 在 CMake 中：使用 ``${ZEPHYR_FOO_MODULE_DIR}`` 表示模块的顶级目录，使用 ``${ZEPHYR_FOO_CMAKE_DIR}`` 表示包含其 :file:`CMakeLists.txt` 的目录
- 在 Kconfig 中：使用 ``$(ZEPHYR_FOO_MODULE_DIR)`` 表示模块的顶级目录

注意小写模块名 ``foo`` 在 CMake 和 Kconfig 中都转换为大写 ``FOO``。

这些变量还可以用于测试某个给定模块是否存在。例如，要验证 ``foo`` 是 Zephyr 模块的名称：

.. code-block:: cmake

    if(ZEPHYR_FOO_MODULE_DIR)
        # Do something if FOO exists.
    endif()

在 Kconfig 中，该变量可用于查找要包含的额外文件。例如，要包含模块 ``foo`` 中的文件 :file:`some/Kconfig`：

.. code-block:: kconfig

    source "$(ZEPHYR_FOO_MODULE_DIR)/some/Kconfig"

在处理每个 Zephyr 模块的 CMake 过程中，以下变量也可用：

- 当前模块的名称：``${ZEPHYR_CURRENT_MODULE_NAME}``
- 当前模块的顶级目录：``${ZEPHYR_CURRENT_MODULE_DIR}``
- 当前模块的 :file:`CMakeLists.txt` 目录：``${ZEPHYR_CURRENT_CMAKE_DIR}``

这消除了 Zephyr 模块在 CMake 处理过程中需要知道自身名称的需求。模块可以使用这些 ``CURRENT`` 变量来 source 额外的 CMake 文件。例如：

.. code-block:: cmake

    include(${ZEPHYR_CURRENT_MODULE_DIR}/cmake/code.cmake)

可以从模块的第一个 CMakeLists.txt 文件向 Zephyr `CMake 列表`_ 变量追加值。
为此，将值追加到列表，然后在 CMakeLists.txt 文件的 PARENT_SCOPE 中设置该列表。例如，要在 Zephyr CMakeLists.txt 作用域中向 ``FOO_LIST`` 变量追加 ``bar``：

.. code-block:: cmake

    list(APPEND FOO_LIST bar)
    set(FOO_LIST ${FOO_LIST} PARENT_SCOPE)

一个 Zephyr 列表的有用示例是向 ``SYSCALL_INCLUDE_DIRS`` 列表添加额外目录。

Sysbuild 模块
----------------

在 Kconfig 和 CMake 中，变量 ``SYSBUILD_CURRENT_MODULE_DIR`` 包含 sysbuild 模块的绝对路径。在 CMake 中，``SYSBUILD_CURRENT_CMAKE_DIR`` 包含包含被纳入 CMake 构建系统的 :file:`CMakeLists.txt` 文件的目录的绝对路径。如果 module.yml 文件未指定 CMakeLists.txt，则该变量的值为空。

要读取 sysbuild 模块的这些变量：

- 在 CMake 中：使用 ``${SYSBUILD_CURRENT_MODULE_DIR}`` 表示模块的顶级目录，使用 ``${SYSBUILD_CURRENT_CMAKE_DIR}`` 表示包含其 :file:`CMakeLists.txt` 的目录
- 在 Kconfig 中：使用 ``$(SYSBUILD_CURRENT_MODULE_DIR)`` 表示模块的顶级目录

在 Kconfig 中，该变量可用于查找要包含的额外文件。例如，要包含文件 :file:`some/Kconfig`：

.. code-block:: kconfig

    source "$(SYSBUILD_CURRENT_MODULE_DIR)/some/Kconfig"

模块可以使用这些变量来 source 额外的 CMake 文件。例如：

.. code-block:: cmake

    include(${SYSBUILD_CURRENT_MODULE_DIR}/cmake/code.cmake)

可以从模块的第一个 CMakeLists.txt 文件向 Zephyr `CMake 列表`_ 变量追加值。
为此，将值追加到列表，然后在 CMakeLists.txt 文件的 PARENT_SCOPE 中设置该列表。例如，要在 Zephyr CMakeLists.txt 作用域中向 ``FOO_LIST`` 变量追加 ``bar``：

.. code-block:: cmake

    list(APPEND FOO_LIST bar)
    set(FOO_LIST ${FOO_LIST} PARENT_SCOPE)

Sysbuild 模块钩子
----------------------

Sysbuild 提供了一种基础设施，允许 sysbuild 模块定义一个函数，该函数将由 sysbuild 在 CMake 流程中预定义的点调用。

由 sysbuild 调用的函数：

- ``<module-name>_pre_cmake(IMAGES <images>)``：此函数在为所有镜像调用 CMake configure 之前，为每个 sysbuild 模块调用。
- ``<module-name>_post_cmake(IMAGES <images>)``：此函数在为所有镜像完成 CMake configure 之后，为每个 sysbuild 模块调用。
- ``<module-name>_pre_domains(IMAGES <images>)``：此函数在 sysbuild 创建 domains yaml 之前，为每个 sysbuild 模块调用。
- ``<module-name>_post_domains(IMAGES <images>)``：此函数在 sysbuild 创建 domains yaml 之后，为每个 sysbuild 模块调用。

从 sysbuild 传递给模块定义的函数的参数：

- ``<images>`` 是构建系统将创建的 Zephyr 镜像列表。

如果模块 ``foo`` 想提供一个 post CMake configure 函数，则该模块的 sysbuild :file:`CMakeLists.txt` 文件必须定义函数 ``foo_post_cmake()``。

为便于函数命名，模块名称在加载模块的 sysbuild :file:`CMakeLists.txt` 文件时由 sysbuild CMake 通过 ``SYSBUILD_CURRENT_MODULE_NAME`` CMake 变量提供。

``foo`` sysbuild 模块如何定义 ``foo_post_cmake()`` 的示例：

.. code-block:: cmake

    function(${SYSBUILD_CURRENT_MODULE_NAME}_post_cmake)
        cmake_parse_arguments(POST_CMAKE "" "" "IMAGES" ${ARGN})

        message("Invoking ${CMAKE_CURRENT_FUNCTION}. Images: ${POST_CMAKE_IMAGES}")
    endfunction()

Zephyr 模块依赖
==========================

Zephyr 模块可能依赖于其他 Zephyr 模块的存在才能正确工作。或者，某个 Zephyr 模块可能由于某些 CMake 目标的依赖关系必须在另一个 Zephyr 模块之后处理。

这样的依赖关系可以使用 ``depends`` 字段描述。

.. code-block:: yaml

    build:
      depends:
        - <module>

以下是 Zephyr 模块 ``foo`` 依赖于 Zephyr 模块 ``bar`` 存在于构建系统中的示例：

.. code-block:: yaml

    name: foo
    build:
      depends:
        - bar

该示例将确保 ``foo`` 被纳入构建系统时 ``bar`` 存在，并且确保 ``bar`` 在 ``foo`` 之前被处理。

.. _modules_module_ext_root:

模块集成文件（外部）
====================================

模块集成文件可以位于 Zephyr 模块本身之外。``MODULE_EXT_ROOT`` 变量保存一个根列表，其中包含位于 Zephyr 模块外部的集成文件。

Zephyr 中的模块集成文件
----------------------------------

Zephyr 仓库包含某些已知 Zephyr 模块的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 构建文件。

这些文件位于

.. code-block:: none

    <ZEPHYR_BASE>
    └── modules
        └── <module_name>
            ├── CMakeLists.txt
            └── Kconfig

自定义位置中的模块集成文件
---------------------------------------------

你可以为额外模块创建类似的 ``MODULE_EXT_ROOT``，并使这些模块被 Zephyr 构建系统知晓。

创建具有以下结构的 ``MODULE_EXT_ROOT``

.. code-block:: none

    <MODULE_EXT_ROOT>
    └── modules
        ├── modules.cmake
        └── <module_name>
            ├── CMakeLists.txt
            └── Kconfig

然后通过向 CMake 构建系统指定 ``-DMODULE_EXT_ROOT`` 参数来构建你的应用。``MODULE_EXT_ROOT`` 接受 `CMake 列表`_ 形式的根作为参数。

Zephyr 模块可以使用模块描述文件 :file:`zephyr/module.yml` 自动添加到 ``MODULE_EXT_ROOT`` 列表中，参见 :ref:`modules_build_settings`。

.. note::

    ``ZEPHYR_BASE`` 始终作为具有最低优先级的 ``MODULE_EXT_ROOT`` 被添加。
    这允许你用你自己 ``MODULE_EXT_ROOT`` 中的实现覆盖 ``<ZEPHYR_BASE>/modules/<module_name>`` 下的任何集成文件。

:file:`modules.cmake` 文件必须包含通过特定命名的 CMake 变量指定 Zephyr 模块集成文件的逻辑。

要包含模块的 CMake 文件，将变量 ``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 设置为包含 CMake 文件的路径。

要包含模块的 Kconfig 文件，将变量 ``ZEPHYR_<MODULE_NAME>_KCONFIG`` 设置为 Kconfig 文件的路径。

以下是如何添加对 ``FOO`` 模块支持的一个示例。

创建以下结构

.. code-block:: none

    <MODULE_EXT_ROOT>
    └── modules
        ├── modules.cmake
        └── foo
            ├── CMakeLists.txt
            └── Kconfig

并在 :file:`modules.cmake` 文件内部添加以下内容

.. code-block:: cmake

    set(ZEPHYR_FOO_CMAKE_DIR ${CMAKE_CURRENT_LIST_DIR}/foo)
    set(ZEPHYR_FOO_KCONFIG   ${CMAKE_CURRENT_LIST_DIR}/foo/Kconfig)

模块集成文件（zephyr/module.yml）
--------------------------------------------

模块描述文件 :file:`zephyr/module.yml` 可用于指定构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 位于 :ref:`modules_module_ext_root` 中。

位于 ``MODULE_EXT_ROOT`` 中的构建文件可以描述为：

.. code-block:: yaml

    build:
      cmake-ext: True
      kconfig-ext: True

这允许在 Zephyr 模块外部描述构建包含的控制。

Zephyr 仓库本身始终被添加为 Zephyr 模块 ext root。

.. _modules_build_settings:

构建设置
==============

可以指定在将模块纳入构建系统时必须使用的额外构建设置。

所有 ``root`` 设置相对于模块的根。

:file:`module.yml` 文件中支持的构建设置为：

- ``board_root``：包含构建系统可用的额外开发板。额外开发板必须位于 :file:`<board_root>/boards` 文件夹中。
- ``dts_root``：包含与架构/SoC 家族相关的额外 dts 文件。额外 dts 文件必须位于 :file:`<dts_root>/dts` 文件夹中。
- ``snippet_root``：包含可供使用的额外代码片段。这些片段必须定义在 :file:`<snippet_root>/snippets` 文件夹下的 :file:`snippet.yml` 文件中。例如，如果你有 ``snippet_root: foo``，则应将模块的 :file:`snippet.yml` 文件放在 :file:`<your-module>/foo/snippets` 或任何嵌套子目录中。
- ``soc_root``：包含构建系统可用的额外 SoC。额外 SoC 必须位于 :file:`<soc_root>/soc` 文件夹中。
- ``arch_root``：包含构建系统可用的额外架构。额外架构必须位于 :file:`<arch_root>/arch` 文件夹中。
- ``module_ext_root``：包含 Zephyr 模块的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件，另见 :ref:`modules_module_ext_root`。
- ``sca_root``：包含构建系统可用的额外 :ref:`SCA <sca>` 工具实现。每个工具必须位于 :file:`<sca_root>/sca/<tool>` 文件夹中。该文件夹必须包含 :file:`sca.cmake`。

包含额外 root 的 :file:`module.yaml` 文件示例，以及相应的文件系统布局。

.. code-block:: yaml

    build:
      settings:
        board_root: .
        dts_root: .
        soc_root: .
        arch_root: .
        module_ext_root: .


需要以下文件夹结构：

.. code-block:: none

    <zephyr-module-root>
    ├── arch
    ├── boards
    ├── dts
    ├── modules
    └── soc

测试运行器（Twister）集成
=================================

要执行模块中可用的测试和示例，应将 Zephyr 测试运行器（twister）指向包含这些示例和测试的目录。这可以通过在 :file:`zephyr/module.yml` 文件中指定示例和测试的路径来完成。此外，如果模块定义了树外开发板，模块文件可以指向 twister 到模块中维护这些文件的路径。例如：

.. code-block:: yaml

    build:
      cmake: .
    samples:
      - samples
    tests:
      - tests
    boards:
      - boards

:file:`zephyr/module.yml` 文件中定义的测试和示例不会被 twister 自动检测。要让 twister 知晓模块中定义的测试和示例，必须在执行 twister 时将那些测试和示例的路径添加到命令行，例如：

.. code-block:: shell

    ./scripts/zephyr_module.py --twister-out module_tests.args
    if [ -s module_tests.args ]; then
        west twister +module_tests.args --outdir module_tests ...
    fi


.. _modules-bin-blobs:

二进制 Blob
=============

Zephyr 支持获取和使用 :ref:`二进制 blob <bin-blobs>`，其元数据完全包含在 :file:`zephyr/module.yml` 中。这是因为二进制 blob 必须始终与 Zephyr 模块相关联，因此 blob 元数据属于模块的描述本身。

二进制 blob 使用 :ref:`west blobs <west-blobs>` 获取。如果 :ref:`未使用 <modules_without_west>` ``west``，则必须手动下载和验证。

:file:`zephyr/module.yml` 中的 ``blobs`` 部分由一系列映射组成，每个映射具有以下条目：

- ``path``：二进制 blob 的路径，相对于模块仓库中的 :file:`zephyr/blobs/` 文件夹
- ``sha256``：二进制 blob 文件的 `SHA-256 <https://en.wikipedia.org/wiki/SHA-2>`_ 校验和
- ``type``：:ref:`二进制 blob 的类型 <bin-blobs-types>`。目前仅限于 ``img`` 或 ``lib``
- ``version``：版本字符串
- ``license-path``：该 blob 许可文件的路径，相对于模块仓库的根
- ``url``：标识 blob 将被从中获取的位置以及要使用的获取方案的 URL。如果包含的是列表而非单个字符串，每个 URL 都将被视为获取同一 blob 的回退。
- ``description``：二进制 blob 的可读描述
- ``doc-url``：指向该 blob 官方文档位置的 URL

以下条目也可能存在：

- ``click-through``：布尔值，指示是否必须接受 click-through 许可才能下载该 blob
- ``size``：blob 的字节大小。某些获取器可能需要
- ``fetcher``：用于下载 blob 的方法。如果未设置，方法从 URL 推断

包管理器依赖
===========================

Zephyr 模块可以描述来自包管理器的依赖，目前仅支持 ``pip``。

west 扩展命令 ``west packages <manager>`` 可用于列出 Zephyr 的依赖并展示在其 ``module.yml`` 文件中利用此功能的模块。
运行 ``west help packages`` 了解更多细节。

Python pip
----------

调用 ``west packages pip`` 列出 Zephyr 和模块的 `requirement 文件`_。传入 ``--install`` 时，如果有活动的虚拟环境则安装这些文件。

以下示例演示了一个 ``zephyr/module.yml`` 文件，其中模块 ``scripts`` 目录中有一些 requirement 文件。


.. code-block:: yaml

    package-managers:
      pip:
        requirement-files:
          - scripts/requirements-build.txt
          - scripts/requirements-doc.txt


.. _modules-runners:

外部运行器
================

如果模块有需要自定义 :ref:`运行器 <west-runner>` 的树外开发板，则可以向其 ``zephyr/module.yml`` 文件添加一个列表，例如：


.. code-block:: yaml

    runners:
      - file: scripts/my-runner.py


每个文件条目在执行 ``west flash`` 或 ``west debug`` 时被导入，``ZephyrBinaryRunner`` 的子类被注册使用。

模块纳入
================

.. _modules_using_west:

使用 West
----------

如果安装了 west 且 :makevar:`ZEPHYR_MODULES` 尚未设置，构建系统会在你的 :term:`west 安装` 中找到所有模块并使用它们。它通过运行 :ref:`west list <west-built-in-misc>` 获取安装中所有项目的路径，然后过滤结果以仅保留具有必要模块元数据文件的项目。

``west list`` 输出中的每个项目都按如下方式测试：

- 如果项目包含名为 :file:`zephyr/module.yml` 的文件，则该文件的内容将用于确定应将哪些文件添加到构建中，如前一节所述。

- 否则（即如果项目没有 :file:`zephyr/module.yml`），构建系统会在项目中查找 :file:`zephyr/CMakeLists.txt` 和 :file:`zephyr/Kconfig` 文件。如果两者都存在，该项目被视为模块，这些文件将被添加到构建中。

- 如果这两项检查都未成功，该项目不被视为模块，也不会被添加到 :makevar:`ZEPHYR_MODULES`。

.. _modules_without_west:

不使用 West
------------

如果你没有安装 west 或不想让构建系统使用它来查找 Zephyr 模块，你可以使用以下选项之一自己设置 :makevar:`ZEPHYR_MODULES`。列表中的每个目录必须包含 :file:`zephyr/module.yml` 文件或 :file:`zephyr/CMakeLists.txt` 和 :file:`Kconfig` 文件，如前一节所述。

#. 在 CMake 命令行上，如下所示：

   .. code-block:: console

      cmake -DZEPHYR_MODULES=<path-to-module1>[;<path-to-module2>[...]] ...

#. 在你的应用顶级 :file:`CMakeLists.txt` 的顶部，如下所示：

   .. code-block:: cmake

      set(ZEPHYR_MODULES <path-to-module1> <path-to-module2> [...])
      find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

   如果你选择此选项，确保在调用 ``find_package(Zephyr ...)`` **之前**设置该变量，如上所示。

#. 在一个单独预加载以填充 CMake 缓存的 CMake 脚本中，如下所示：

   .. code-block:: cmake

      # Put this in a file with a name like "zephyr-modules.cmake"
      set(ZEPHYR_MODULES <path-to-module1> <path-to-module2>
        CACHE STRING "pre-cached modules")

   你可以通过在 CMake 命令行中添加 ``-C zephyr-modules.cmake`` 来告诉构建系统使用该文件。

不使用模块
-----------------

如果你没有安装 west 且没有自己指定 :makevar:`ZEPHYR_MODULES`，则不会向构建中添加额外模块。你仍然能够构建任何不需要外部仓库中定义的代码或 Kconfig 选项的应用。

向模块提交更改
******************************

提交新模块或对现有模块进行更改时，主仓库 Zephyr 需要对更改有引用才能验证这些更改。在主树中，这通过修订（revision）完成。对于已合并并成为树一部分的代码，我们使用提交哈希、标签或分支名。然而对于拉取请求，我们要求在 revision 字段中指定拉取请求编号，以便能够使用提交到模块的更改构建 zephyr 主树。

为避免将包含拉取请求信息的更改合并到 master，拉取请求应被标记为 ``DNM``（Do Not Merge，不要合并）或最好是草稿拉取请求，以确保它不会意外合并，并允许模块先被合并并被分配永久的提交哈希。草稿通过在被标记为 "Ready for review" 之前不自动通知任何人来减少噪音。
模块合并后，revision 需要由提交者或维护者更改为反映该更改的模块提交哈希。

注意，对不同模块的多个相互依赖的更改可以使用完全相同的流程提交。在这种情况下，你将更改所有对其有拉取请求的模块的多个条目。

.. _submitting_new_modules:

提交新模块的流程
===================================

请遵循 :ref:`external-src-process` 中的流程并获得 TSC 批准，将外部源代码作为模块集成

如果请求被批准，项目团队将创建一个新的仓库并用允许按照项目贡献指南向模块项目提交代码的基本信息进行初始化。

如果模块作为 GitHub 上另一个项目的 fork 维护，与上游相关的 Zephyr 模块相关文件及更改需要在名为 ``zephyr`` 的特殊分支中维护。

Zephyr 项目的维护者将创建该仓库并初始化它。你将被添加为新仓库的协作者。按照 :ref:`此处 <modules_using_west>` 描述的指南将模块内容（代码）提交到新仓库，然后在 :zephyr_file:`west.yml` 中添加一个新条目，包含以下信息：

   .. code-block:: console

      - name: <name of repository>
        path: <path to where the repository should be cloned>
        revision: <ref pointer to module pull request>


例如，要将 *my_module* 添加到清单：

.. code-block:: console

    - name: my_module
      path: modules/lib/my_module
      revision: pull/23/head


其中上述示例中的 23 表示提交到 *my_module* 仓库的拉取请求编号。模块更改被审查和合并后，revision 需要更改为来自模块仓库的提交哈希。

.. _changes_to_existing_module:

向现有模块提交更改的流程
================================================

#. 遵循 :ref:`贡献指南 <contribute_guidelines>` 和 :ref:`期望 <contributor-expectations>`，使用拉取请求向现有仓库提交更改。
#. 提交一个拉取请求，更改主 Zephyr 树的 :zephyr_file:`west.yml` 中引用该模块的条目，包含以下信息：

   .. code-block:: console

      - name: <name of repository>
        path: <path to where the repository should be cloned>
        revision: <ref pointer to module pull request>


例如，要将 *my_module* 添加到清单：

.. code-block:: console

    - name: my_module
      path: modules/lib/my_module
      revision: pull/23/head

其中上述示例中的 23 表示提交到 *my_module* 仓库的拉取请求编号。模块更改被审查和合并后，revision 需要更改为来自模块仓库的提交哈希。


.. _CMake list: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _add_subdirectory(): https://cmake.org/cmake/help/latest/command/add_subdirectory.html
.. _GitHub issues: https://github.com/zephyrproject-rtos/zephyr/issues
.. _requirement files: https://pip.pypa.io/en/stable/reference/requirements-file-format/
