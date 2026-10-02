.. _west-history:

历史与动机
##########

West 被加入 Zephyr 项目，是为了满足两个基本需求：

* 能够同时操作多个 Git 仓库
* 能够为 Zephyr 的基础工作流提供一个可扩展且易于使用的命令行接口

在 west 的开发过程中，我们识别出了一组 :ref:`west-design-constraints`，
以避免此类工具的常见陷阱。

需求
****

尽管将 Zephyr 代码库拆分为多个仓库的动机不在本页的讨论范围之内，
但基本需求本身，以及"不使用现有工具而是开发一个新工具"这一选择的明确理由，
则属于本页的内容。

基本需求如下：

* **R1**：将外部维护的代码保存在主 zephyr 仓库之外、独立维护的仓库中，
  且不需要用户手动克隆每一个外部仓库
* **R2**：提供一个工具，使 Zephyr 用户和发行版维护者都能从中受益并进行扩展
* **R3**：允许用户和下游发行版在不修改 zephyr 仓库的情况下覆盖或删除仓库
* **R4**：同时支持持续跟踪和基于提交（可二分）的项目更新

自研工具的理由
**************

west 的部分功能与 `Git Submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_
和 Google 的 `repo <https://gerrit.googlesource.com/git-repo/>`_ 提供的功能类似。

在 west 的初期设计与开发过程中，我们考虑过现有的工具。
但没有一种适合 Zephyr 的需求。特别是，我们详细考察了以下工具：

* Google repo

  - 无法干净地支持将 zephyr 用作 manifest 仓库（**R4**）
  - 仅支持 Python 2
  - 与 Windows 的兼容性不佳
  - 假定代码评审使用 Gerrit

* Git submodules

  - 无法完全支持 **R1**，因为外部维护的仓库仍然必须位于主 zephyr Git 树内
  - 无法支持 **R3**，因为下游副本必须删除或替换 submodule 定义
  - 无法持续跟踪外部仓库中最新的 ``HEAD``（**R4**）
  - 需要硬编码外部仓库的路径/位置

多个 Git 仓库
*************

Zephyr 致力于提供部署复杂物联网应用所需的全部构件。
这意味着 Zephyr 项目远不止是一个 RTOS 内核，
而是一组协同工作的组件的集合。

在此背景下，项目中以标准化方式操作多个 Git 仓库有以下几个原因：

* 清晰地区分 Zephyr 原始代码与导入的项目和库
* 避免原始代码与导入代码之间的许可证不兼容
* 缩小核心 Zephyr 代码库的规模和范围，
  可选组件放在额外的仓库中，而不是直接导入树中
* 安全与安全性认证
* 强制组件的模块化
* 基于受支持的板卡和 SoC 子集进行树外开发

关于 west 工作区如何管理多个 git 仓库的信息，请参见 :ref:`west-basics`。

.. _west-design-constraints:

设计约束
********

West 的特性是：

- **可选**：始终*可以*退回到"原始"命令行工具，
  即在不使用 west 的情况下使用 Zephyr
  （尽管 west 本身可能需要被安装并可被构建系统访问）。
  不过这样做并不总是*方便*。
  （如果 west 的所有功能都已经很方便地可用，就没有开发它的理由了。）

- **与 CMake 兼容**：构建、烧录和调试，以及模拟器支持，
  将始终保持与直接使用 CMake 兼容。

- **跨平台**：West 使用 Python 3 编写，可在 Zephyr 支持的所有平台上工作。

- **可作为库使用**：只要可能，west 的功能都实现为库，
  可以在其他程序中独立使用，并配有包装它们的独立命令行接口。
  West 本身是一个名为 ``west`` 的 Python 包；它的库实现为子包。

- **对功能持保守态度**：没有强烈而有说服力的动机，就不会接受任何功能。

- **明确规范**：West 在包装其他命令时的行为有明确的规定和文档说明。
  这使得与第三方工具的互操作成为可能，
  也意味着 Zephyr 开发者在使用 west 时总能了解"底层"正在发生什么。

更多细节和讨论，参见 :github:`Zephyr issue #6205 <6205>`。

.. _west-update-detached-heads:

``west update`` 的分离 HEAD
****************************

:ref:`update
procedure <west-update-procedure>` 中记录的分离 git ``HEAD`` 修订版的使用方式，
让一些用户感到困惑甚至沮丧。

具体而言，用户经常询问为什么 ``west update`` 默认不保持现有的本地分支处于检出状态。

本节解释 ``west update`` 为什么默认表现出这样的行为，
并介绍一些管理本地修改项目的其他选项。

``west update`` 的两个核心需求是：

#. 安全性：该命令不应丢失用户的任何工作
#. 确定性：两个用户在同一个 manifest 上运行 ``west update``，
   应得到完全相同的 :ref:`workspace <west-basics>` 内容

使用分离 HEAD 有助于保持安全性。
如更新流程中所述，对更新后的项目使用 ``git checkout --detach``
以获得分离的 ``HEAD`` 是一项通常安全的操作，不会丢失用户的工作：

- 如果你的工作都已安全地提交在本地 git 分支中，该分支将保持原样
  （详见 ``git help checkout`` 的输出）

- 如果你有未提交的工作，只要可能，git 会将其安全地保留在你的工作树中

- 如果不可能，整个命令将失败，
  你可以在重新运行 ``west update`` 之前决定如何处理你的工作

分离 HEAD 也有助于确保确定性：

- 精确检出 manifest 文件中指定的项目修订版，
  是确保工作区文件与主 manifest 中指定内容一致的必要条件。
  如果 west 默认不检出 manifest 修订版，你的工作区可能会与你根据
  工作副本中 manifest 文件内容所期望的有所不同，且这种差异不可见。
  更糟糕的是，差异的具体方式将取决于你运行 ``west update`` 之前分支中的具体内容。

- 与 :ref:`west-manifest-import` 存在微妙的交互。
  如果你的项目本身有一个或多个被 ``west update`` 导入的 manifest 文件，
  west 就需要将这些文件检出到工作树中，才能解析完整的导入 manifest。
  如果 ``west update`` 在你的项目中保持某个分支处于检出状态，
  你工作树中的 manifest 文件可能已经过时。
  如果 west 随后使用这些过时的文件完成导入，
  流程可能会意外失败，或产生其他不确定性的结果。

West 不会直接检出 :ref:`manifest-rev <west-manifest-rev>` 分支，
原因在该分支的文档中有说明。

这一默认行为是很久以前选定的，现在已太迟无法更改，因为用户已经依赖它。
不过，如果这一默认行为不适合你，还有其他运行 ``west update`` 的方式。
要了解更多信息，运行 ``west
help update`` 并阅读 ``checked out branch behavior`` 选项组的说明文本。例如：

- 如果你正在项目中积极编写代码，并希望在上游 manifest 可能发生变化后保持其最新状态，
  使用 ``west update --rebase``

- 如果你有一些本地代码希望保留，只要你的项目的上游修订版没有前进到更新的版本，
  使用 ``west update --keep-descendants``

如果你想为这些命令之一设置更短的输入方式，可以使用 :ref:`west-aliases`。
你也可以通过向以下地址发送 pull request 为该选项组贡献新选项：

https://github.com/zephyrproject-rtos/west
