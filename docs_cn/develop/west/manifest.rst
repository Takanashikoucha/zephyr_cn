.. _west-manifests:

West Manifests（west manifest）
###############################

本页包含关于 west 的多仓库模型、manifest 文件以及 ``west manifest`` 命令的详细信息。
关于 ``west.manifest`` 模块的 API 文档，参见 :ref:`west-apis-manifest`。
关于更通用的介绍和命令概览，参见 :ref:`west-basics`。

.. only:: html

   .. contents::
      :depth: 3

.. _west-mr-model:

多仓库模型
*************************

West 对 :term:`west workspace` 中各仓库及其历史的看法，
如下图所示（不过本例中的一些部分特定于上游 Zephyr 对 west 的使用）：

.. figure:: west-mr-model.png
   :align: center
   :alt: West 多仓库历史
   :figclass: align-center

   West 多仓库历史

manifest 仓库的历史是"浮动"在灰色平面上方的那条 Git 提交链。
父提交用实线箭头指向子提交。下方的平面包含工作区中
各仓库的 Git 提交历史，每个项目仓库用一个矩形框起来。
每个仓库内部的父/子提交关系同样用实线箭头表示。

manifest 仓库中的每个提交（再次说明，对上游 Zephyr 而言
就是 zephyr 仓库本身）都带有一个 manifest 文件。
每个提交中的 manifest 文件指定了它在各项目仓库中
所期望的对应提交。这种关系在图中用虚线箭头表示。
每条虚线箭头都从 manifest 仓库中的某个提交
指向项目仓库中对应的提交。

请注意以下几个重要细节：

- 项目可以被添加（例如 ``P1`` 在 manifest 仓库提交
  ``D`` 和 ``E`` 之间被添加）也可以被移除
  （``P2`` 在同样的 manifest 仓库提交之间被移除）

- 项目仓库和 manifest 仓库的历史不必一起向前或向后移动：

  - ``P2`` 从 ``A → B`` 保持不变，``P1`` 和 ``P3`` 从 ``F →
    G`` 也保持不变。
  - ``P3`` 从 ``A → B`` 向前移动。
  - ``P3`` 从 ``C → D`` 向后移动。

  在项目历史中向后移动的一种用途，是通过回退到
  某个回归被引入之前的修订来"回退"该回归。

- 项目仓库的提交可以被"跳过"：``P3`` 从 ``B → C``
  在其历史中向前移动了多个提交。

- 在上面的图中，没有任何项目仓库同时拥有两个"同一时刻"的修订：
  每个 manifest 文件都精确地引用其所关心的项目中的
  一个提交。通过使用分支名作为 manifest 修订可以放宽这一限制，
  代价是无法再对 manifest 仓库历史进行二分查找。

.. _west-manifest-files:

Manifest 文件
**************

West manifest 是 YAML 文件。Manifest 有一个顶层的 ``manifest`` 节，
其中包含若干子节，形如：

.. code-block:: yaml

   manifest:
     remotes:
       # short names for project URLs
     projects:
       # a list of projects managed by west
     defaults:
       # default project attributes
     self:
       # configuration related to the manifest repository itself,
       # i.e. the repository containing west.yml
     version: "<schema-version>"
     group-filter:
       # a list of project groups to enable or disable

从 YAML 的角度说，manifest 文件包含一个带有 ``manifest`` 键的映射。
其他任何键及其内容都会被忽略（west v0.5 还要求有一个
``west`` 键，但从 v0.6 开始该键被忽略）。

manifest 包含 ``defaults``、``remotes``、``projects`` 和 ``self``
等子节。从 YAML 的角度说，``manifest`` 键的值
也是一个映射，以这些"子节"作为键。
从 west v0.10 起，所有这些"子节"键都是可选的。

``projects`` 的值是一个列表，包含 west 管理的仓库
以及相关的元数据。我们稍后会讨论它，
但首先描述 ``remotes`` 节，
它可以在 ``projects`` 列表中减少输入量。

远程仓库（Remotes）
===================

``remotes`` 子节包含一个序列，指定项目可以从其获取的
基础 URL。

每个 ``remotes`` 元素都有一个名称和一个"URL 基础"。
它们被用来为每个项目构造完整的 Git 获取 URL。
项目的获取 URL 可以通过在远程 URL 基础后追加
项目特定的路径来设置。（如下文所示，
项目也可以直接指定其完整的获取 URL。）

例如：

.. code-block:: yaml

   manifest:
     # ...
     remotes:
       - name: remote1
         url-base: https://git.example.com/base1
       - name: remote2
         url-base: https://git.example.com/base2

``remotes`` 的键及其用法见下表。

.. list-table:: remotes 键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 说明

   * - ``name``
     - 必填；远程仓库的唯一名称。

   * - ``url-base``
     - 一个前缀，会被前置到使用该远程仓库的
       每个项目的获取 URL 之前。

上面给出了两个远程仓库，名称分别为 ``remote1`` 和 ``remote2``。
它们的 URL 基础分别是 ``https://git.example.com/base1`` 和
``https://git.example.com/base2``。你也可以使用 SSH URL 基础；
例如，如果 ``remote1`` 也支持 Git over SSH，
你可以使用 ``git@example.com:base1``。
任何 Git 能接受的都可以。

.. _west-manifests-projects:

项目（Projects）
================

``projects`` 子节包含一个序列，描述 west 工作区中的
项目仓库。每个项目都有一个唯一的名称。
你可以指定克隆和获取项目时使用哪些 Git 远程 URL、
跟踪哪些修订，以及项目应存放在本地文件系统的哪个位置。
请注意，west 项目 :ref:`与模块是不同的 <modules-vs-projects>`。

下面是一个示例。我们假设使用上面给出的 ``remotes``。

.. Note: 如果你修改这个示例，请保持下方对应的 manifest 同步。

.. code-block:: yaml

   manifest:
     # [... same remotes as above...]
     projects:
       - name: proj1
         description: the first example project
         remote: remote1
         path: extra/project-1
       - name: proj2
         description: |
           A multi-line description of the second example
           project.
         repo-path: my-path
         remote: remote2
         revision: v1.3
       - name: proj3
         url: https://github.com/user/project-three
         revision: abcde413a111
       - name: proj4
         url: https://github.com/user/project-four
         revision: pull/69/head # GitHub Pull Request

在这个 manifest 中：

- ``proj1`` 使用远程仓库 ``remote1``，因此其 Git 获取 URL 为
  ``https://git.example.com/base1/proj1``。远程仓库的 ``url-base``
  后追加一个 ``/`` 和项目的 ``name`` 构成该 URL。

  本地，该项目会克隆到相对于 west 工作区根目录的
  ``extra/project-1`` 路径，因为它有一个显式的、
  取该值的 ``path`` 属性。

  由于该项目没有指定 ``revision``，默认使用 ``master``。
  当 west 下次更新该项目时，该分支的当前尖端
  会被获取并检出一个分离的 ``HEAD``。

- ``proj2`` 有 ``remote`` 和 ``repo-path``，因此其获取 URL 为
  ````https://git.example.com/base2/my-path````。
  如果存在 ``repo-path`` 属性，它在构造获取 URL 时
  覆盖默认的 ``name``。

  由于该项目没有 ``path`` 属性，默认使用其 ``name``。
  它会被克隆到一个名为 ``proj2`` 的目录中。
  当 west 更新该项目时，``v1.3`` 标签所指向的
  提交会被检出。

- ``proj3`` 有显式的 ``url``，因此会从
  ``https://github.com/user/project-three`` 获取。

  其本地路径默认为其名称 ``proj3``。
  提交 ``abcde413a111`` 会在其下次更新时被检出。

可用的项目键及其用法见下表。
有时我们会提到 ``defaults`` 子节；它将在下节描述。

.. list-table:: projects 元素键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 说明

   * - ``name``
     - 必填；项目的唯一名称。名称不能是保留值
       "west" 或 "manifest"。名称在 manifest 文件中必须唯一。

   * - ``description``
     - 可选，项目的信息性描述。west v1.2.0 添加。

   * - ``remote``、``url``
     - 必填（二者取其一，但不能同时使用）。

       如果项目有 ``remote``，则该远程仓库的 ``url-base``
       会与项目的 ``name``（如果有 ``repo-path`` 则用它）
       组合，构成获取 URL。

       如果项目有 ``url``，那就是远程 Git 仓库
       完整的获取 URL。

       如果两者都没有，``defaults`` 节必须指定一个
       ``remote``，它将被用作该项目的远程仓库。
       否则该 manifest 无效。

   * - ``repo-path``
     - 可选。如果给出，它会被拼接到远程仓库的
       ``url-base`` 之后（而不是项目的 ``name``）
       以构成其获取 URL。项目不能同时具有
       ``url`` 和 ``repo-path`` 属性。

   * - ``revision``
     - 可选。``west update`` 应检出的 Git 修订。
       默认以分离 HEAD 方式检出，
       以避免与本地分支名冲突。如果未给出，
       若 ``defaults`` 子节中存在 ``revision`` 值则使用它。

       项目修订可以是任何可获取的 git 引用：
       分支、标签、SHA、pull request 等。

       默认 ``revision`` 为 ``master``（如未另行指定）。

       使用 ``HEAD~0`` [#f1]_ 作为 ``revision``
       会使 west 保持项目的当前状态。

   * - ``path``
     - 可选。相对路径，指定在本地何处克隆该仓库，
       相对于 west 工作区的顶层目录。如果缺失，
       项目的 ``name`` 会被用作目录名。

   * - ``clone-depth``
     - 可选。如果给出，一个正整数，
       会在克隆的仓库中创建一个浅层历史，
       限制为给定的提交数。
       这只能在 ``revision`` 是分支或标签时使用。

   * - ``west-commands``
     - 可选。如果给出，一个指向项目内
       描述该项目提供的额外 west 命令的 YAML 文件的相对路径。
       按约定该文件命名为 :file:`west-commands.yml`。
       详情参见 :ref:`west-extensions`。

   * - ``import``
     - 可选。如果为 ``true``，从给定仓库中的
       manifest 文件导入项目到当前 manifest。
       详情参见 :ref:`west-manifest-import`。

   * - ``groups``
     - 可选，项目所属的组列表。
       详情参见 :ref:`west-manifest-groups`。

   * - ``submodules``
     - 可选。你可以用它让 ``west update`` 也更新
       项目中定义的 `Git 子模块`_。
       详情参见 :ref:`west-manifest-submodules`。

   * - ``userdata``
     - 可选。值是一个任意的 YAML 值。
       参见 :ref:`west-project-userdata`。

.. rubric:: 脚注

.. [#f1] 在 git 中，HEAD 是一个引用，而 HEAD~<n> 是一个有效的修订
         但不是引用。West 会获取引用（如 refs/heads/main 或
         HEAD）以及本地不可用的提交，但如果提交已经本地可用
         则不会获取。HEAD~0 会被解析为一个本地可用的特定提交，
         因此 west 只会检出该本地可用的提交（由 HEAD~0 标识）。

.. _Git 子模块: https://git-scm.com/book/en/v2/Git-Tools-Submodules

默认值（Defaults）
==================

``defaults`` 子节可以为项目属性提供默认值。
特别是，默认远程仓库名和修订可以在这里指定。
使用 ``defaults`` 编写我们到目前为止所描述的
同一个 manifest 的另一种方式是：

.. code-block:: yaml

   manifest:
     defaults:
       remote: remote1
       revision: v1.3

     remotes:
       - name: remote1
         url-base: https://git.example.com/base1
       - name: remote2
         url-base: https://git.example.com/base2

     projects:
       - name: proj1
         description: the first example project
         path: extra/project-1
         revision: master
       - name: proj2
         description: |
           A multi-line description of the second example
           project.
         repo-path: my-path
         remote: remote2
       - name: proj3
         url: https://github.com/user/project-three
         revision: abcde413a111

可用的 ``defaults`` 键及其用法见下表。

.. list-table:: defaults 键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 说明

   * - ``remote``
     - 可选。如果项目没有设置 ``url`` 或 ``remote`` 键，
       该值将用作项目的 ``remote``。

   * - ``revision``
     - 可选。如果项目没有设置 ``revision``，
       该值将用作项目的 ``revision``。如果未给出，
       默认为 ``master``。

自身（Self）
============

``self`` 子节可用于控制 manifest 仓库本身。

例如，考虑 zephyr 仓库 :file:`west.yml` 中的
这个片段：

.. code-block:: yaml

   manifest:
     # ...
     self:
       path: zephyr
       west-commands: scripts/west-commands.yml

这确保 zephyr 仓库被克隆到 ``zephyr`` 路径，
不过如上所述，即使从默认的 manifest URL
``https://github.com/zephyrproject-rtos/zephyr`` 克隆
也会发生这种情况。由于 zephyr 仓库确实包含
扩展命令，其 ``self`` 条目声明了相对于
仓库根目录的对应 :file:`west-commands.yml` 的位置。

可用的 ``self`` 键及其用法见下表。

.. list-table:: self 键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 说明

   * - ``path``
     - 可选。``west init`` 应克隆 manifest 仓库到的路径，
       相对于 west 工作区的 topdir。

       如果未给出，默认使用 manifest 仓库 URL 中
       路径组件的 basename。例如，如果 URL 是
       ``https://git.example.com/project-repo``，
       manifest 仓库会被克隆到 :file:`project-repo` 目录。

   * - ``west-commands``
     - 可选。这与项目序列元素中的同名键类似。

   * - ``import``
     - 可选。这也与 ``projects`` 键类似，
       但允许从 manifest 仓库中的其他文件导入项目。
       参见 :ref:`west-manifest-import`。

.. _west-manifest-schema-version:

版本（Version）
===============

``version`` 子节声明该 manifest 文件使用了
某个版本的 west 中引入的特性。
使用旧版本的 west 加载该 manifest 会失败，
并给出一个错误信息，说明所需的最低 west 版本。

下面是一个示例：

.. code-block:: yaml

   manifest:
     # Marks that this file uses version 0.10 of the west manifest
     # file format.
     #
     # An attempt to load this manifest file with west v0.8.0 will
     # fail with an error message saying that west v0.10.0 or
     # later is required.
     version: "0.10"

`west 源代码仓库`_ 中的 pykwalify schema :file:`manifest-schema.yml`
用于验证 manifest 节。

.. _west 源代码仓库:
   https://github.com/zephyrproject-rtos/west

下面是一个表格，列出有效的 ``version`` 值，
以及该版本中引入的 manifest 文件特性。

.. list-table::
   :header-rows: 1
   :widths: 1 4

   * - ``version``
     - 新特性

   * - ``"0.7"``
     - 对 ``version`` 特性的初始支持。本表中未另行提及的
       所有 manifest 文件特性都是在 west v0.7.0
       或更早版本中引入的。

   * - ``"0.8"``
     - 支持 ``import: path-prefix:``
       （:ref:`west-manifest-import-map`）

   * - ``"0.9"``
     - **不推荐使用 west v0.9.x**。

       提供该 schema 版本是为了让用户可以显式请求
       与 west :ref:`west_0_9_0` 兼容。
       然而，west :ref:`west_0_10_0` 及更高版本
       对 west v0.9.0 中引入的特性具有不兼容的行为。
       在可能的情况下，你应该忽略版本 "0.9"。

   * - ``"0.10"``

     - 支持：

       - ``projects:`` 中的 ``submodules:``
         （:ref:`west-manifest-submodules`）
       - ``manifest: group-filter:`` 以及
         ``projects:`` 中的 ``groups:``
         （:ref:`west-manifest-groups`）
       - ``import:`` 特性现在支持 ``allowlist:`` 和
         ``blocklist:``；它们分别被推荐作为旧名称的替代，
         作为 Zephyr 全项目包容性语言变更的一部分。
         旧键名出于向后兼容仍被支持。
         （:ref:`west-manifest-import`、
         :ref:`west-manifest-import-map`）

   * - ``"0.12"``
     - 支持 ``projects:`` 中的 ``userdata:``
       （:ref:`west-project-userdata`）

   * - ``"0.13"``
     - 支持 ``self: userdata:``
       （:ref:`west-project-userdata`）

   * - ``"1.0"``
     - 与 ``"0.13"`` 相同，但可供不希望使用
       ``"0.x"`` 版本字段的用户使用。

   * - ``"1.2"``
     - 支持 ``projects:`` 中的 ``description:``
       （:ref:`west-manifests-projects`）

.. note::

   没有在 manifest 文件格式中引入新特性的 west 版本
   不会改变有效 ``version`` 值的列表。
   例如，``version: "0.11"`` **不是** 有效的，
   因为 west v0.11.x 没有引入新的 manifest 文件格式特性。

如上所示对 ``version`` 值加引号，会强制 YAML 解析器
将其视为字符串。不加引号时，YAML 中的 ``0.10``
只是浮点值 ``0.1``。如果值转换为字符串后相同，
你可以省略引号，但最好加上。不确定时总是使用引号。

如果你的 manifest 不包含 ``version``，
west 的每个新版本都会假设它应该尝试使用
该版本中可用的特性来加载它。
如果该版本的 west 太旧而无法加载该 manifest，
这可能导致更难理解的错误信息。

组过滤器（Group-filter）
========================

参见 :ref:`west-manifest-groups`。

.. _west-active-inactive-projects:

活动与非活动项目
****************************

west manifest 中定义的项目可以是 *非活动的* 或 *活动的*。
区别在于非活动项目通常被 west 忽略。
例如，``west update`` 不会更新非活动项目，
``west list`` 默认不会打印关于它们的信息。
再例如，非活动项目中的任何 :ref:`west-manifest-import`
都会被 west 忽略。

有两种方法可以让项目变为非活动：

1. 使用 ``manifest.project-filter`` 配置选项。
   如果项目通过该选项被设为活动或非活动，
   则与使用 ``groups:`` 使项目非活动相关的规则
   会被忽略。也就是说，如果
   ``manifest.project-filter`` 中的某个正则表达式
   适用于某个项目，该项目的组
   对其活动或非活动状态没有影响。

   详情参见 :ref:`west-config-index` 中该选项的条目。

2. 否则，如果项目有组，且这些组全部被禁用，
   则该项目为非活动。

   详情参见下一节。

.. _west-manifest-groups:

项目组
**************

你可以使用 :ref:`上文 <west-manifest-files>` 简要描述的
``groups`` 和 ``group-filter`` 键将项目分组，
并启用或禁用组。

例如，这让你可以通过使用 ``west forall --group``
仅对组中的项目运行 ``west forall`` 命令。
这还可以让你使项目非活动；
关于非活动项目的更多信息参见上一节。

下一节介绍项目组。再下一节描述
:ref:`west-enabled-disabled-groups`。
:ref:`west-project-group-examples` 中有一些基本示例。
最后，:ref:`west-group-filter-imports`
提供了 ``group-filter`` 如何与
:ref:`west-manifest-import` 特性交互的简化概览。

项目组基础
==========

``groups:`` 和 ``group-filter:`` 键在 manifest 中
形如：

.. code-block:: yaml

   manifest:
     projects:
       - name: some-project
         groups: ...
     group-filter: ...

``groups`` 键的值是一个组名列表。组名是字符串。

你可以使用 ``group-filter`` 启用或禁用项目组。
组全部被禁用且未被 ``manifest.project-filter``
配置选项另行设为活动的项目，是非活动的。

例如，在这个 manifest 片段中：

.. code-block:: yaml

  manifest:
    projects:
      - name: project-1
        groups:
          - groupA
      - name: project-2
        groups:
          - groupB
          - groupC
      - name: project-3

这些项目属于以下组：

- ``project-1``：一个组，名为 ``groupA``
- ``project-2``：两个组，名为 ``groupB`` 和 ``groupC``
- ``project-3``：没有组

项目组的名称不得包含逗号 (,)、冒号 (:) 或空白。

组名不得以连字符 (-) 或加号 (+) 开头，
但可以在名称的其他位置包含这些字符。
例如，``foo-bar`` 和 ``foo+bar`` 是有效的组，
但 ``-foobar`` 和 ``+foobar`` 不是。

组名在其他方面是任意字符串。组名区分大小写。

作为一个限制，任何项目不得同时使用
``import:`` 和 ``groups:``。
（这是为了避免某些病态的边界情况。）

.. _west-enabled-disabled-groups:

启用与禁用的项目组
===================================

所有项目组默认启用。你可以在 manifest 文件
和 :ref:`west-config` 中启用或禁用组。

在 manifest 文件中，``manifest: group-filter:``
是一个 YAML 列表，列出要启用和禁用的组。

要启用一个组，在其名称前加加号 (+)。例如，
在这个 manifest 片段中 ``groupA`` 被启用：

.. code-block:: yaml

   manifest:
     group-filter: [+groupA]

虽然这对默认已启用的组来说是冗余的，
但它可以用来覆盖导入的 manifest 文件中的设置。
更多信息参见 :ref:`west-group-filter-imports`。

要禁用一个组，在其名称前加连字符 (-)。例如，
在这个 manifest 片段中 ``groupA`` 和 ``groupB`` 被禁用：

.. code-block:: yaml

   manifest:
     group-filter: [-groupA,-groupB]

.. note::

   由于 ``group-filter`` 是一个 YAML 列表，
   你可以将上面这个片段写成如下形式：

   .. code-block:: yaml

      manifest:
        group-filter:
          - -groupA
          - -groupB

   然而，这种语法可读性较差，因此不推荐。

除了 manifest 文件，你还可以使用
``manifest.group-filter`` 配置选项
控制哪些组被启用和禁用。
该选项是一个逗号分隔的列表，
列出要启用和/或禁用的组。

要启用一个组，将其名称加 ``+`` 前缀后添加到列表中。
要禁用一个组，将其名称加 ``-`` 前缀后添加到列表中。
例如，将 ``manifest.group-filter`` 设置为
``+groupA,-groupB`` 会启用 ``groupA`` 并禁用 ``groupB``。

配置选项的值覆盖 manifest 文件中的任何数据。
你可以这样理解：``manifest.group-filter`` 配置选项
被追加到 YAML 中的 ``manifest: group-filter:`` 列表之后，
遵循"最后一条生效"的语义。

实用示例：减少工作区下载量
-------------------------

默认情况下，``west update`` 会获取 manifest 中定义的
所有活动项目。大型工作区可能包含可选模块、
厂商 HAL、实验性组件，或并非每个工作流都需要的
平台特定依赖项和漏洞。

项目组可用于控制在 ``west`` 操作期间
哪些分组项目被视为活动。

例如，考虑以下 manifest 片段：

.. code-block:: yaml

  manifest:
    projects:
      - name: hal_nordic
        groups:
          - nordic
      - name: hal_stm32
        groups:
          - stm32
      - name: experimental_lib
        groups:
          - optional

面向 Nordic 设备的工作区可以在运行
``west update`` 之前禁用 ``stm32`` 和 ``optional`` 组：

.. code-block:: shell

   west config manifest.group-filter -- "-stm32,-optional"

配置完过滤器后，运行：

.. code-block:: shell

   west update

这会跳过仅属于被禁用组的项目。

.. note::

   项目组只影响在 manifest 中被显式分配到
   匹配组的项目。没有匹配组定义的项目
   无论配置的 ``manifest.group-filter`` 值如何
   都保持活动。

.. note::

   修改 ``manifest.group-filter`` 不会自动
   移除已克隆到工作区中的仓库。
   它影响的是在后续 ``west`` 操作期间
   项目是否被视为活动。

此工作流可以帮助减少不必要的下载，
并在大型多项目环境中简化工作区管理。

.. _west-project-group-examples:

项目组示例
==========

本节包含涉及项目组和活动项目的示例场景。
示例同时使用 ``manifest: group-filter:`` YAML 列表
和 ``manifest.group-filter`` 配置列表，
以展示它们如何协同工作。

请注意，以下 manifest 中的 ``defaults`` 和 ``remotes``
数据与示例无关，只是为了让示例完整自包含。

.. note::

   在以下所有示例中，假设
   ``manifest.project-filter`` 选项未设置。

示例 1：没有禁用的组
---------------------

整个 manifest 文件为：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB
       - name: baz

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项未设置
（你可以通过运行 ``west config -D manifest.group-filter``
来确保这一点）。

没有组被禁用，因为所有组默认启用。因此，
三个项目（``foo``、``bar`` 和 ``baz``）都是活动的。
请注意，没有办法使项目 ``baz`` 非活动，
因为它没有组。

示例 2：通过 manifest 禁用一个组
--------------------------------

整个 manifest 文件为：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     group-filter: [-groupA]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项未设置
（你可以通过运行 ``west config -D manifest.group-filter``
来确保这一点）。

由于 ``groupA`` 被禁用，项目 ``foo`` 是非活动的。
项目 ``bar`` 是活动的，因为 ``groupB`` 被启用。

示例 3：通过 manifest 禁用多个组
--------------------------------

整个 manifest 文件为：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     group-filter: [-groupA,-groupB]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项未设置
（你可以通过运行 ``west config -D manifest.group-filter``
来确保这一点）。

``foo`` 和 ``bar`` 都是非活动的，
因为它们的所有组都被禁用。

示例 4：通过配置禁用一个组
--------------------------

整个 manifest 文件为：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项被设置为 ``-groupA``
（你可以通过运行 ``west config manifest.group-filter -- -groupA``
来确保这一点；额外的 ``--`` 是必需的，
否则参数解析器会把 ``-groupA`` 当作
值为 ``roupA`` 的命令行选项 ``-g``）。

项目 ``foo`` 是非活动的，因为 ``groupA``
被 ``manifest.group-filter`` 配置选项禁用。
项目 ``bar`` 是活动的，因为 ``groupB`` 被启用。

Example 5: Overriding a disabled group via configuration
--------------------------------------------------------

整个 manifest 文件为：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     group-filter: [-groupA]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项被设置为 ``+groupA``
（你可以通过运行 ``west config manifest.group-filter +groupA``
来确保这一点）。

在这种情况下，``groupA`` 被启用：
``manifest.group-filter`` 配置选项的优先级高于
manifest 文件中的 ``manifest: group-filter: [-groupA]`` 内容。

因此，项目 ``foo`` 和 ``bar`` 都是活动的。

Example 6: Overriding multiple disabled groups via configuration
----------------------------------------------------------------

整个 manifest 文件为：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     group-filter: [-groupA,-groupB]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项被设置为
``+groupA,+groupB``（你可以通过运行
``west config manifest.group-filter "+groupA,+groupB"``
来确保这一点）。

在这种情况下，``groupA`` 和 ``groupB`` 都被启用，
因为配置值对两个组都覆盖了 manifest 文件。

因此，项目 ``foo`` 和 ``bar`` 都是活动的。

Example 7: Disabling multiple groups via configuration
------------------------------------------------------

整个 manifest 文件为：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

``manifest.group-filter`` 配置选项被设置为
``-groupA,-groupB``（你可以通过运行
``west config manifest.group-filter -- "-groupA,-groupB"``
来确保这一点）。

在这种情况下，``groupA`` 和 ``groupB`` 都被禁用。

因此，项目 ``foo`` 和 ``bar`` 都是非活动的。

.. _west-group-filter-imports:

组过滤器与导入（Group Filters and Imports）
=========================================

本节提供简化描述，说明 ``manifest: group-filter:``
值与 :ref:`west-manifest-import` 结合使用时的行为。
完整细节参见 :ref:`west-manifest-formal`。

.. warning::

   以下语义适用于 west v0.10.0 及更高版本。
   West v0.9.x 的语义不同，
   在 west v0.9.x 中将 ``group-filter`` 与 ``import``
   结合使用是不推荐的。

简而言之：

- 如果你只导入一个 manifest，它在其
  ``group-filter`` 中禁用的任何组
  在你的 manifest 中也会被禁用
- 你可以在 manifest 文件的
  ``manifest: group-filter:`` 值、
  工作区的 ``manifest.group-filter`` 配置选项
  或两者中覆盖这一点

下面是一些示例。

Example 1: no overrides
-----------------------

你正在使用这个 :file:`parent/west.yml` manifest：

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

而 :file:`child/west.yml` 包含：

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

在解析后的 manifest 中只有 ``child`` 和 ``project-2`` 是活动的。

``unstable`` 组在 :file:`child/west.yml` 中被禁用，
且在 :file:`parent/west.yml` 中未被覆盖。
因此，解析后 manifest 的最终 ``group-filter``
为 ``[-unstable]``。

由于 ``project-1`` 和 ``project-3`` 属于 ``unstable`` 组
且不属于任何其他组，它们是非活动的。

Example 2: overriding an imported ``group-filter`` via manifest
---------------------------------------------------------------

你正在使用这个 :file:`parent/west.yml` manifest：

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     group-filter: [+unstable,-optional]
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

而 :file:`child/west.yml` 包含：

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
         groups:
           - optional
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

只有 ``child``、``project-1`` 和 ``project-3`` 项目是活动的。

:file:`child/west.yml` 中的 ``[-unstable]`` 组过滤器
在 :file:`parent/west.yml` 中被覆盖，
因此 ``unstable`` 组被启用。
由于 ``project-1`` 和 ``project-3`` 属于 ``unstable`` 组，
它们是活动的。

同一个 :file:`parent/west.yml` 文件禁用了 ``optional`` 组，
因此 ``project-2`` 是非活动的。

:file:`parent/west.yml` 指定的最终组过滤器为
``[+unstable,-optional]``。

Example 3: overriding an imported ``group-filter`` via configuration
--------------------------------------------------------------------

你正在使用这个 :file:`parent/west.yml` manifest：

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

而 :file:`child/west.yml` 包含：

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
         groups:
           - optional
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

如果你运行：

.. code-block:: shell

   west config manifest.group-filter +unstable,-optional

则只有 ``child``、``project-1`` 和 ``project-3`` 项目是活动的。

:file:`child/west.yml` 中的 ``-unstable`` 组过滤器
在 ``manifest.group-filter`` 配置选项中被覆盖，
因此 ``unstable`` 组被启用。
由于 ``project-1`` 和 ``project-3`` 属于 ``unstable`` 组，
它们是活动的。

同一个配置选项禁用了 ``optional`` 组，
因此 ``project-2`` 是非活动的。

:file:`parent/west.yml` 和 ``manifest.group-filter``
配置选项指定的最终组过滤器为 ``[+unstable,-optional]``。

.. _west-manifest-submodules:

项目中的 Git 子模块
**************************

你可以使用 :ref:`上文 <west-manifest-files>` 简要描述的
``submodules`` 键，强制 ``west update`` 也处理
项目 git 仓库中配置的 `Git 子模块`_。
``submodules`` 键可以出现在 ``projects`` 内部，
形如：

.. code-block:: YAML

   manifest:
     projects:
       - name: some-project
         submodules: ...

``submodules`` 键可以是布尔值或映射列表。
我们按顺序描述它们。

Option 1: Boolean
=================

这是使用 ``submodules`` 最简单的方式。

如果 ``submodules`` 作为 ``projects`` 属性为 ``true``，
``west update`` 在更新项目本身时会递归更新
项目的 Git 子模块。如果为 ``false`` 或缺失，
则没有效果。

例如，假设你有一个源代码仓库 ``foo``，
它有一些子模块，你希望 ``west update``
保持它们全部同步，同时还有同一工作区中
另一个名为 ``bar`` 的项目。

你可以用这个 manifest 文件做到：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules: true
       - name: bar

这里，``west update`` 会初始化并更新 ``foo`` 中的
所有子模块。如果 ``bar`` 有任何子模块，
它们会被忽略，因为 ``bar`` 没有 ``submodules`` 值。

Option 2: List of mappings
==========================

``submodules`` 键可以是一个映射列表，
每个期望的子模块对应一个列表元素。
列出的每个子模块都会被递归更新。
你仍然可以用 ``git`` 命令手动跟踪和更新
未列出的子模块；无论存在与否，
``west`` 都会完全忽略它们。

``path`` 键必须精确匹配其父 west 项目中
某个子模块相对于父项目的路径，
如 ``git submodule status`` 的输出所示。
``name`` 键是可选的，目前 west 不使用它；
它也不会被传递给 ``git submodule`` 命令。
``name`` 键在 west 版本 0.9.0 中曾短暂必填，
但在 0.9.1 中变为可选。

例如，假设你有一个源代码仓库 ``foo``，
它有很多子模块，你希望 ``west update``
只保持其中一部分（而非全部）同步，
同时还有同一工作区中另一个名为 ``bar`` 的项目。

你可以用这个 manifest 文件做到：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules:
           - path: path/to/foo-first-sub
           - name: foo-second-sub
             path: path/to/foo-second-sub
       - name: bar

这里，``west update`` 会递归初始化并更新
``foo`` 中路径为 ``path/to/foo-first-sub`` 和
``path/to/foo-second-sub`` 的子模块。
``bar`` 中的任何子模块仍会被忽略。

.. _west-project-userdata:

仓库用户数据（Repository user data）
==================================

West v0.12 及更高版本支持项目中的可选 ``userdata`` 键。

West v0.13 及更高版本支持在
``manifest: self:`` 节中使用该键。

它供需要用户特定项目元数据的程序消费。
除了将其解析为 YAML 外，west 本身完全忽略其值。

该键的值是任意 YAML。West 解析该值，
并通过 :ref:`west-apis` 使其可被程序
作为对应 ``west.manifest.Project`` 对象的
``userdata`` 属性访问。

manifest 片段示例：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         userdata: a-string
       - name: baz
         userdata:
           key: value
     self:
       userdata: blub

Python 用法示例：

.. code-block:: python

   manifest = west.manifest.Manifest.from_file()

   foo, bar, baz = manifest.get_projects(['foo', 'bar', 'baz'])

   foo.userdata # None
   bar.userdata # 'a-string'
   baz.userdata # {'key': 'value'}
   manifest.userdata # 'blub'

.. _west-manifest-import:

Manifest 导入（Manifest Imports）
=================================

你可以使用上文简要描述的 ``import`` 键
在 :file:`west.yml` 中包含来自其他 manifest 文件的项目。
该键可以是 ``project`` 或 ``self`` 节的属性：

.. code-block:: yaml

   manifest:
     projects:
       - name: some-project
         import: ...
     self:
       import: ...

你可以使用 "self: import:" 从包含
:file:`west.yml` 的仓库加载额外文件。
你可以使用 "project: ... import:"
从该项目的 Git 历史中定义的额外文件加载。

West 按以下顺序从各个 manifest 文件解析
最终 manifest：

#. ``self`` 中导入的文件
#. 你的 :file:`west.yml` 文件
#. ``projects`` 中导入的文件

解析过程中，west 忽略已在其他文件中定义的项目。
例如，你的 :file:`west.yml` 中名为 ``foo`` 的项目
会使 west 忽略从你的 ``projects`` 列表导入的
其他名为 ``foo`` 的项目。

``import`` 键可以是布尔值、路径、映射或序列。
我们按顺序用示例描述它们：

- :ref:`布尔值 <west-manifest-import-bool>`

  - :ref:`west-manifest-ex1.1`
  - :ref:`west-manifest-ex1.2`
  - :ref:`west-manifest-ex1.3`

- :ref:`相对路径 <west-manifest-import-path>`

  - :ref:`west-manifest-ex2.1`
  - :ref:`west-manifest-ex2.2`
  - :ref:`west-manifest-ex2.3`

- :ref:`带额外配置的映射 <west-manifest-import-map>`

  - :ref:`west-manifest-ex3.1`
  - :ref:`west-manifest-ex3.2`
  - :ref:`west-manifest-ex3.3`
  - :ref:`west-manifest-ex3.4`

- :ref:`路径和映射的序列 <west-manifest-import-seq>`

  - :ref:`west-manifest-ex4.1`
  - :ref:`west-manifest-ex4.2`

最后，有一个更 :ref:`形式化的描述 <west-manifest-formal>`，
说明其工作原理，放在示例之后。

排障说明（Troubleshooting Note）
================================

如果你正在使用此特性并发现 west 的行为令人困惑，
尝试 :ref:`解析你的 manifest <west-manifest-resolve>`
以查看导入完成后的最终结果。

.. _west-manifest-import-bool:

Option 1: Boolean
=================

这是使用 ``import`` 最简单的方式。

如果 ``import`` 作为 ``projects`` 属性为 ``true``，
west 会从该项目根目录中的 :file:`west.yml` 文件
导入项目。如果为 ``false`` 或缺失，则没有效果。
例如，这个 manifest 会从 ``p1`` git 仓库
修订 ``v1.0`` 处导入 :file:`west.yml`：

.. code-block:: yaml

   manifest:
     # ...
     projects:
       - name: p1
         revision: v1.0
         import: true    # Import west.yml from p1's v1.0 git tag
       - name: p2
         import: false   # Nothing is imported from p2.
       - name: p3        # Nothing is imported from p3 either.

在 ``self`` 内部将 ``import`` 设置为
``true`` 或 ``false`` 都是错误的，
形如：

.. code-block:: yaml

   manifest:
     # ...
     self:
       import: true  # Error

.. _west-manifest-ex1.1:

Example 1.1: Downstream of a Zephyr release
-------------------------------------------

你有一个源代码仓库，想配合 Zephyr v1.14.1 LTS 使用。
你希望用 west 维护整个东西。
你不想修改任何主线仓库。

换句话说，你想要的 west 工作区看起来像这样：

.. code-block:: none

   my-downstream/
   ├── .west/                     # west directory
   ├── zephyr/                    # mainline zephyr repository
   │   └── west.yml               # the v1.14.1 version of this file is imported
   ├── modules/                   # modules from mainline zephyr
   │   ├── hal/
   │   └── [...other directories..]
   ├── [ ... other projects ...]  # other mainline repositories
   └── my-repo/                   # your downstream repository
       ├── west.yml               # main manifest importing zephyr/west.yml v1.14.1
       └── [...other files..]

你可以用以下 :file:`my-repo/west.yml` 做到：

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v1.14.1
         import: true

然后你可以在计算机上像这样创建工作区，
假设 ``my-repo`` 托管在 ``https://git.example.com/my-repo``：

.. code-block:: console

   west init -m https://git.example.com/my-repo my-downstream
   cd my-downstream
   west update

``west init`` 之后，:file:`my-downstream/my-repo` 会被克隆。

``west update`` 之后，``zephyr`` 仓库 :file:`west.yml`
在修订 ``v1.14.1`` 处定义的所有项目
也会被克隆到 :file:`my-downstream`。

此时你可以向 :file:`my-repo` 添加并提交任何代码，
包括你自己的 Zephyr 应用、驱动器等。
参见 :ref:`application`。

.. _west-manifest-ex1.2:

Example 1.2: "Rolling release" Zephyr downstream
------------------------------------------------

这与 :ref:`west-manifest-ex1.1` 类似，
只是我们对 zephyr 仓库使用 ``revision: main``：

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: main
         import: true

你可以用同样的方式创建工作区：

.. code-block:: console

   west init -m https://git.example.com/my-repo my-downstream
   cd my-downstream
   west update

这一次，每次你运行 ``west update``，
``zephyr`` 仓库中特殊的 :ref:`manifest-rev
<west-manifest-rev>` 分支都会更新为指向
从 URL https://github.com/zephyrproject-rtos/zephyr
新获取的 ``main`` 分支尖端。

然后会使用新 ``manifest-rev`` 处
:file:`zephyr/west.yml` 的内容
从 Zephyr 导入项目。这让你能够跟上
Zephyr 项目中的最新变更。代价是运行
``west update`` 不会产生可复现的结果，
因为远程 ``main`` 分支每次运行都可能变化。

理解这一点也很重要：west 在解析导入时
**完全忽略你工作树中的**
:file:`zephyr/west.yml`。West 在从项目导入时，
总是使用导入的 manifest 在最新
``manifest-rev`` 处提交时的内容。

只有当 manifest 位于你的 manifest 仓库工作树中时，
才能从文件系统导入 manifest。
示例参见 :ref:`west-manifest-ex2.2`。

.. _west-manifest-ex1.3:

Example 1.3: Downstream of a Zephyr release, with module fork
-------------------------------------------------------------

这个 manifest 与 :ref:`west-manifest-ex1.1` 中的类似，
只是它：

- 是 Zephyr 2.0 的下游
- 包含该发布中包含的 :file:`modules/hal/nordic`
  :ref:`模块 <modules>` 的下游 fork

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
       - name: my-remote
         url-base: https://git.example.com
     projects:
       - name: hal_nordic         # higher precedence
         remote: my-remote
         revision: my-sha
         path: modules/hal/nordic
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.0.0
         import: true             # imported projects have lower precedence

   # subset of zephyr/west.yml contents at v2.0.0:
   manifest:
     defaults:
       remote: zephyrproject-rtos
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
     # ...
     - name: hal_nordic           # lower precedence, values ignored
       path: modules/hal/nordic
       revision: another-sha

使用这个 manifest 文件，名为 ``hal_nordic`` 的项目：

- 从 ``https://git.example.com/hal_nordic`` 克隆，
  而不是从 ``https://github.com/zephyrproject-rtos/hal_nordic``。
- 被 ``west update`` 更新到提交 ``my-sha``，
  而不是主线提交 ``another-sha``

换句话说，当你的顶层 manifest 定义了一个项目
（如 ``hal_nordic``）时，west 会忽略
解析导入时随后找到的任何其他定义。

这意味着你必须在 :file:`my-repo/west.yml` 中
定义 ``hal_nordic`` 时，把
``path: modules/hal/nordic`` 值复制进去。
:file:`zephyr/west.yml` 中的值会被完全忽略。
如果实际操作中这令人困惑，
排障建议参见 :ref:`west-manifest-resolve`。

当你运行 ``west update`` 时，west 会：

- 将 zephyr 的 ``manifest-rev`` 更新为指向 ``v2.0.0`` 标签
- 导入该 ``manifest-rev`` 处的 :file:`zephyr/west.yml`
- 本地检出除 ``hal_nordic`` 外所有 zephyr 项目的
  ``v2.0.0`` 修订
- 将 ``hal_nordic`` 更新到 ``my-sha``，
  而不是 ``another-sha``

.. _west-manifest-import-path:

Option 2: Relative path
=======================

``import`` 的值也可以是一个指向 manifest 文件或
包含 manifest 文件的目录的相对路径。
该路径相对于 ``import`` 键所在的
``projects`` 或 ``self`` 仓库的根目录。

下面是一个示例：

.. code-block:: yaml

   manifest:
     projects:
       - name: project-1
         revision: v1.0
         import: west.yml
       - name: project-2
         revision: main
         import: p2-manifests
     self:
       import: submanifests

这会导入以下内容：

- :file:`project-1/west.yml` 的内容（位于 ``manifest-rev``，
  在运行 ``west update`` 后指向标签 ``v1.0``）
- 目录树 :file:`project-2/p2-manifests` 中的任何 YAML 文件
  （位于 ``main`` 分支的最新提交处，
  由 ``west update`` 获取），按文件名排序
- 你的 manifest 仓库中 :file:`submanifests` 里的
  YAML 文件（按其在文件系统上的呈现），
  按文件名排序

请注意 ``projects`` 导入通过 ``manifest-rev``
从 Git 获取数据，而 ``self`` 导入
从你的文件系统获取数据。
这是因为通常，west 将你的 manifest 仓库的
版本控制交由你自己处理。

.. _west-manifest-ex2.1:

Example 2.1: Downstream of a Zephyr release with explicit path
--------------------------------------------------------------

这是以显式方式编写与 :ref:`west-manifest-ex1.1`
中等价 manifest 的方法。

.. code-block:: yaml

   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v1.14.1
         import: west.yml

``import: west.yml`` 的设置意味着使用
``zephyr`` 项目内部的 :file:`west.yml` 文件。
这个示例是人为构造的，但展示了这个思路。

这在实践中可能有用，
当你想导入的 manifest 文件名称
不是 :file:`west.yml` 时。

.. _west-manifest-ex2.2:

Example 2.2: Downstream with directory of manifest files
--------------------------------------------------------

你的 Zephyr 下游有很多额外的仓库。
多到你想把它们拆分到多个 manifest 文件中，
但要在单个 manifest 仓库中跟踪它们全部，
形如：

.. code-block:: none

   my-repo/
   ├── submanifests
   │   ├── 01-libraries.yml
   │   ├── 02-vendor-hals.yml
   │   └── 03-applications.yml
   └── west.yml

你想把 :file:`my-repo/submanifests` 中的所有文件
添加到主 manifest 文件 :file:`my-repo/west.yml`，
除了 :file:`zephyr/west.yml` 中的项目外。
你想跟踪 Zephyr 仓库 ``main`` 分支中的
最新开发代码，而不是使用固定修订。

方法如下：

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: main
         import: true
     self:
       import: submanifests

解析期间，manifest 文件按以下顺序导入：

#. :file:`my-repo/submanifests/01-libraries.yml`
#. :file:`my-repo/submanifests/02-vendor-hals.yml`
#. :file:`my-repo/submanifests/03-applications.yml`
#. :file:`my-repo/west.yml`
#. :file:`zephyr/west.yml`

.. note::

   本例中 :file:`.yml` 文件名前缀加了数字，
   以确保它们按指定顺序导入。

   你可以选择任意名称。West 在导入前
   会按名称对目录中的文件排序。

请注意 :file:`submanifests` 中的 manifest
是在 :file:`my-repo/west.yml` 和
:file:`zephyr/west.yml` *之前* 导入的。
通常，``self`` 节中的 ``import``
先于 ``projects`` 中的 manifest 文件
和主 manifest 文件处理。

这意味着 :file:`my-repo/submanifests` 中定义的项目
具有最高优先级。例如，如果 :file:`01-libraries.yml`
定义了 ``hal_nordic``，:file:`zephyr/west.yml` 中
同名的项目会被简单地忽略。
通常，排障建议参见 :ref:`west-manifest-resolve`。

这看起来可能奇怪，但它允许你"事后"重新定义项目，
如下一个示例所示。

.. _west-manifest-ex2.3:

Example 2.3: Continuous Integration overrides
---------------------------------------------

你的持续集成系统需要从开发者的 fork 而不是
主线开发树中获取并测试 west 工作区中的
多个仓库，以查看这些变更是否协同工作良好。

从 :ref:`west-manifest-ex2.2` 开始，CI 脚本在
:file:`my-repo/submanifests` 中添加一个
:file:`00-ci.yml` 文件，内容如下：

.. code-block:: yaml

   # my-repo/submanifests/00-ci.yml:
   manifest:
     projects:
       - name: a-vendor-hal
         url: https://github.com/a-developer/hal
         revision: a-pull-request-branch
       - name: an-application
         url: https://github.com/a-developer/application
         revision: another-pull-request-branch

CI 脚本在 :file:`my-repo/submanifests` 中
生成该文件后运行 ``west update``。
:file:`00-ci.yml` 中定义的项目
优先级高于 :file:`my-repo/submanifests` 中的
其他定义，因为文件名 :file:`00-ci.yml`
排在其他文件名之前。

因此，``west update`` 总是会检出
名为 ``a-vendor-hal`` 和 ``an-application``
的项目中开发者的分支，
即使这些项目也在其他地方被定义。

.. _west-manifest-import-map:

Option 3: Mapping
=================

``import`` 键还可以包含一个映射，
带有以下键：

- ``file``：可选。要导入的 manifest 文件或目录的名称。
  如果不存在，默认为 :file:`west.yml`。
- ``name-allowlist``：可选。如果存在，
  要包含的项目名称或名称序列。
- ``path-allowlist``：可选。如果存在，
  要匹配的项目路径或路径序列。
  这是一个 shell 风格的 glob 模式，
  目前使用 `pathlib`_ 实现。
  注意这意味着大小写敏感性
  因平台而异。
- ``name-blocklist``：可选。类似 ``name-allowlist``，
  但包含要排除的项目名称而非包含的。
- ``path-blocklist``：可选。类似 ``path-allowlist``，
  但包含要排除的项目路径而非包含的。
- ``path-prefix``：可选（v0.8.0 新增）。如果给出，
  它会被前置到工作区中项目的路径，
  以及任何导入项目的路径。
  这可用于将这些项目放到工作区的子目录中。

.. _re: https://docs.python.org/3/library/re.html
.. _pathlib:
   https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.match

如果两者都给出，allowlist 覆盖 blocklist。
例如，如果一个项目被路径阻止但被名称允许，
它仍会被导入。

.. _west-manifest-ex3.1:

Example 3.1: Downstream with name allowlist
-------------------------------------------

这里是一对 manifest 文件，代表主线和下游。
然而下游不想使用主线的所有项目。
我们假设主线 :file:`west.yml` 托管在
``https://git.example.com/mainline/manifest``。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     projects:
       - name: mainline-app                # included
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib
         path: libraries/lib
         url: https://git.example.com/mainline/lib
       - name: lib2                        # included
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           name-allowlist:
             - mainline-app
             - lib2
       - name: downstream-app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

单文件中等价的 manifest 为：

.. code-block:: yaml

   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
       - name: downstream-app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3
       - name: mainline-app                   # imported
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib2                           # imported
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2

如果没有使用 allowlist，主线 manifest 中的
``lib`` 项目会被导入。

.. _west-manifest-ex3.2:

Example 3.2: Downstream with path allowlist
-------------------------------------------

下面是一个示例，展示如何使用
``path-allowlist`` 只允许主线的库。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     projects:
       - name: app
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib
         path: libraries/lib                  # included
         url: https://git.example.com/mainline/lib
       - name: lib2
         path: libraries/lib2                 # included
         url: https://git.example.com/mainline/lib2

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           path-allowlist: libraries/*
       - name: app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

单文件中等价的 manifest 为：

.. code-block:: yaml

   manifest:
     projects:
       - name: lib                          # imported
         path: libraries/lib
         url: https://git.example.com/mainline/lib
       - name: lib2                         # imported
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2
       - name: mainline
         url: https://git.example.com/mainline/manifest
       - name: app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

.. _west-manifest-ex3.3:

Example 3.3: Downstream with path blocklist
-------------------------------------------

下面是一个示例，展示如何按工作区中的
公共路径前缀阻止主线的所有厂商 HAL，
为你目标芯片添加自己的版本，
并保留其他所有内容。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     defaults:
       remote: mainline
     remotes:
       - name: mainline
         url-base: https://git.example.com/mainline
     projects:
       - name: app
       - name: lib
         path: libraries/lib
       - name: lib2
         path: libraries/lib2
       - name: hal_foo
         path: modules/hals/foo     # excluded
       - name: hal_bar
         path: modules/hals/bar     # excluded
       - name: hal_baz
         path: modules/hals/baz     # excluded

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           path-blocklist: modules/hals/*
       - name: hal_foo
         path: modules/hals/foo
         url: https://git.example.com/downstream/hal_foo

单文件中等价的 manifest 为：

.. code-block:: yaml

   manifest:
     defaults:
       remote: mainline
     remotes:
       - name: mainline
         url-base: https://git.example.com/mainline
     projects:
       - name: app                  # imported
       - name: lib                  # imported
         path: libraries/lib
       - name: lib2                 # imported
         path: libraries/lib2
       - name: mainline
         repo-path: https://git.example.com/mainline/manifest
       - name: hal_foo
         path: modules/hals/foo
         url: https://git.example.com/downstream/hal_foo

.. _west-manifest-ex3.4:

Example 3.4: Import into a subdirectory
---------------------------------------

你想导入一个 manifest 及其项目，
将一切都放到你的 :term:`west workspace` 的一个
子目录中。

例如，假设你想从项目 ``foo`` 导入这个 manifest，
将该项目及其项目 ``bar`` 和 ``baz`` 添加到你的工作区：

.. code-block:: yaml

   # foo/west.yml:
   manifest:
     defaults:
       remote: example
     remotes:
       - name: example
         url-base: https://git.example.com
     projects:
       - name: bar
       - name: baz

你不想把它们导入到顶层工作区，
而是想把所有三个项目仓库放到一个
:file:`external-code` 子目录中，形如：

.. code-block:: none

   workspace/
   └── external-code/
       ├── foo/
       ├── bar/
       └── baz/

你可以用这个 manifest 做到：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         url: https://git.example.com/foo
         import:
           path-prefix: external-code

单文件中等价的 manifest 为：

.. code-block:: yaml

   # foo/west.yml:
   manifest:
     defaults:
       remote: example
     remotes:
       - name: example
         url-base: https://git.example.com
     projects:
       - name: foo
         path: external-code/foo
       - name: bar
         path: external-code/bar
       - name: baz
         path: external-code/baz

.. _west-manifest-import-seq:

Option 4: Sequence
==================

``import`` 键还可以包含文件、目录和映射的序列。

.. _west-manifest-ex4.1:

Example 4.1: Downstream with sequence of manifest files
-------------------------------------------------------

这个示例 manifest 与 :ref:`west-manifest-ex2.2` 中的 manifest
等价，使用显式命名的文件序列。

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     projects:
       - name: zephyr
         url: https://github.com/zephyrproject-rtos/zephyr
         import: west.yml
     self:
       import:
         - submanifests/01-libraries.yml
         - submanifests/02-vendor-hals.yml
         - submanifests/03-applications.yml

.. _west-manifest-ex4.2:

Example 4.2: Import order illustration
--------------------------------------

这个更复杂的示例展示了 west 导入 manifest 文件的顺序：

.. code-block:: yaml

   # my-repo/west.yml
   manifest:
     # ...
     projects:
       - name: my-library
       - name: my-app
       - name: zephyr
         import: true
       - name: another-manifest-repo
         import: submanifests
     self:
       import:
         - submanifests/libraries.yml
         - submanifests/vendor-hals.yml
         - submanifests/applications.yml
     defaults:
       remote: my-remote

对于这个示例，west 按以下顺序解析导入：

#. :file:`my-repo/submanifests` 中列出的文件最先，
   按出现顺序（例如 :file:`libraries.yml`
   在 :file:`applications.yml` 之前，
   因为这是一个文件序列），
   因为 ``self: import:`` 总是最先导入
#. 接着是 :file:`my-repo/west.yml`
   （只要项目 ``my-library`` 等
   尚未在 :file:`submanifests` 中的某处定义）
#. 之后是 :file:`zephyr/west.yml`，
   因为它是 :file:`my-repo/west.yml`
   ``projects`` 列表中第一个 ``import`` 键
#. 最后是 :file:`another-manifest-repo/submanifests`
   中的文件（按文件名排序），
   因为它是最后一个项目 ``import``

.. _west-manifest-formal:

Manifest 导入细节（Manifest Import Details）
==========================================

本节以更形式化的方式描述 west 如何解析
使用 ``import`` 的 manifest 文件。

概述（Overview）
----------------

``import`` 键可以出现在 west manifest 的
``projects`` 和 ``self`` 节中。
一般情况形如：

.. code-block:: yaml

   # Top-level manifest file.
   manifest:
     projects:
       - name: foo
         import:
           ... # import-1
       - name: bar
         import:
           ... # import-2
       # ...
       - name: baz
         import:
           ... # import-N
     self:
       import:
         ... # self-import

Import 键是可选的。如果 ``import-1, ..., import-N``
中有任何缺失，west 不会从该项目导入额外的
manifest 数据。如果 ``self-import`` 缺失，
则不会导入 manifest 仓库中的额外文件
（除顶层文件外）。

解析 manifest 导入的最终结果是：

- 一个 ``projects`` 列表，由顶层文件中定义的
  ``projects`` 与导入文件中定义的 ``projects``
  组合产生

- 一组扩展命令，取自顶层文件和任何导入文件中
  的 ``west-commands`` 键

- 一个 ``group-filter`` 列表，由顶层和任何
  导入的过滤器组合产生

导入按以下顺序进行：

#. 先导入 ``self-import`` 的 manifest。
#. 接着处理顶层 manifest 文件的定义。
#. 按顺序导入 ``import-1``、...、``import-N``
   的 manifest。

当单个 ``import`` 键引用多个 manifest 文件时，
它们按以下顺序处理：

- 如果值是命名一个目录的相对路径
  （或 ``file`` 是目录的映射），
  其中包含的 manifest 文件按字典序处理
  —— 即按文件名排序。
- 如果值是序列，其元素按出现顺序递归导入。

必要时该过程会递归。例如，如果 ``import-1``
产生一个包含 ``import`` 键的 manifest 文件，
它会先按相同规则递归解析，
然后才进一步处理其内容。

以下各节描述这些结果。

项目（Projects）
----------------

本节描述最终的 ``projects`` 列表如何创建。

项目按名称标识。如果同一名称出现在多个 manifest 中，
使用第一个定义，后续定义被忽略。
例如，如果 ``import-1`` 包含一个名为 ``bar`` 的项目，
它会被忽略，因为顶层 :file:`west.yml`
已经定义了同名项目。

``import-1`` 到 ``import-N`` 所命名文件的内容
从 Git 中以其项目中最新的 ``manifest-rev``
修订导入。这些修订可以通过运行
``west update`` 更新为 ``rev-1`` 到 ``rev-N``
的值。如果任何 ``manifest-rev`` 引用缺失或过期，
``west update`` 还会从远程获取 URL 获取项目数据
并更新该引用。

还要注意，为了让 west 更新 ``P`` 本身，
从根 manifest 到定义项目 ``P`` 的仓库的
所有导入的 manifest 都必须保持最新。
例如，这意味着如果 :file:`baz/west.yml`
定义了 ``P``，``west update P`` 会更新
``baz`` 项目中的 ``manifest-rev``，
同时更新本地 ``P`` git 克隆中的
``manifest-rev`` 分支。令人困惑的是，
更新 ``baz`` 可能导致 :file:`baz/west.yml`
中移除 ``P``，而按道理这应该使
``west update P`` 因无法识别的项目而失败！

因此，如果 ``P`` 定义在导入的 manifest 中，
就不可能运行 ``west update P``；
你必须用普通的 ``west update``
连同所有其他项目一起更新该项目。

默认情况下，如果项目的修订是本地已可用的
SHA 或标签，west 不会通过网络获取任何项目数据，
因此更新额外项目除非确实需要，
否则不应花费太多时间。
更多信息参见
:ref:`update.fetch <west-config-index>` 配置选项
的文档。

扩展命令（Extensions）
----------------------

处理导入过程中发现的、使用 ``west-commands`` 键
定义的所有扩展命令，在解析后的 manifest 中都可用。

如果导入的 manifest 文件在其 ``self:`` 节中
有 ``west-commands:`` 定义，
在那里定义的扩展命令会在 manifest
被导入时添加到可用扩展集合中。
因此，它们会优先于之后添加的
同名扩展命令。

组过滤器（Group filters）
-------------------------

解析后的 manifest 有一个 ``group-filter`` 值，
它是顶层 manifest 和任何导入的 manifest 中
``group-filter`` 值拼接的结果。

在导入顺序中靠前的 manifest 文件
优先级更高，因此被拼接到最终
``group-filter`` 的更后面。

换句话说，设：

- 从 ``self-import`` 解析的子 manifest 的
  组过滤器为 ``self-filter``
- 顶层 manifest 文件的组过滤器为 ``top-filter``
- 从 ``import-1`` 到 ``import-N`` 解析的
  子 manifest 的组过滤器分别为
  ``filter-1`` 到 ``filter-N``

则最终解析的 ``group-filter`` 值为
``filterN + ... + filter-2 + filter-1 +
top-filter + self-filter``，
其中 ``+`` 指列表拼接。

.. important::

   上面列表中过滤器出现的顺序很重要。

   最终拼接列表中最后一个过滤器元素"胜出"，
   决定组是启用还是禁用。

例如，在 ``[-foo] + [+foo]`` 中，组 ``foo`` 是 *启用的*。
然而，在 ``[+foo] + [-foo]`` 中，组 ``foo`` 是 *禁用的*。

为简洁起见，west 和本文档可能省略
按这些规则冗余的拼接组过滤器元素。
例如，``[+foo] + [-foo]`` 可以更简单地
写成 ``[-foo]``，原因如上所述。
再例如，``[-foo] + [+foo]`` 可以写成
空列表 ``[]``，因为所有组默认启用。

.. _west-manifest-cmd:

Manifest 命令（Manifest Command）
==================================

``west manifest`` 命令可用于操作 manifest 文件。
它接受一个动作和动作特定的参数。

以下各节描述每个动作，
并为简单用法提供基本签名。
运行 ``west manifest --help``
获取所有选项的完整细节。

.. _west-manifest-resolve:

解析 Manifest（Resolving Manifests）
====================================

``--resolve`` 动作输出一个与你的当前 manifest
及其所有 :ref:`导入的 manifest <west-manifest-import>`
等价的单个 manifest 文件：

.. code-block:: none

   west manifest --resolve [-o outfile]

该动作的主要用途是查看执行任何 ``import``
之后的"最终" manifest 内容。

要打印关于每个导入的 manifest 文件的详细信息
以及 manifest 解析过程中项目如何处理，
使用 ``-v`` 设置最高详细级别：

.. code-block:: console

   west -v manifest --resolve

冻结 Manifest（Freezing Manifests）
===================================

``--freeze`` 动作输出一个冻结的 manifest：

.. code-block:: none

   west manifest --freeze [-o outfile]

"冻结"的 manifest 是一个每个项目的修订
都是 SHA 的 manifest 文件。
你可以使用 ``--freeze`` 生成一个
与当前 manifest 文件等价的冻结 manifest。
``-o`` 选项指定输出文件；如果未给出，
使用标准输出。

验证 Manifest（Validating Manifests）
=====================================

``--validate`` 动作在当前 manifest 文件有效时
成功，否则以错误失败：

.. code-block:: none

   west manifest --validate

错误信息有助于诊断错误。

这里"无效"指 manifest 文件的语法
不符合本页文档中记录的规则。

如果你的 manifest 有效但行为不符合你的预期，
用 ``-v`` 提高详细级别是获取
west 对你的 manifest 做出哪些决策
以及原因之详细信息的好方法：

.. code-block:: none

   west -v manifest --validate

.. _west-manifest-path:

获取 manifest 路径（Get the manifest path）
===========================================

``--path`` 动作打印顶层 manifest 文件的路径：

.. code-block:: none

   west manifest --path

输出类似于 ``/path/to/workspace/west.yml``。
路径格式取决于你的操作系统。
