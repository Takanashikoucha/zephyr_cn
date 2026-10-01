.. _ide_for_zephyr_vscode_ext:

IDE for Zephyr（VS Code 扩展）
##################################

`IDE for Zephyr`_ 是一个用于 Zephyr RTOS 开发的 Visual Studio Code（VS Code）扩展。
它支持**主机工具管理**、**west 工作区设置**、**SDK 管理**、**项目创建**、**构建/烧录**和**调试**。

.. figure:: img/ide-for-zephyr_main_vscode_ext.webp
   :align: center
   :alt: IDE for Zephyr 主页面，展示带内存报告的界面

关键功能
************

- 通过内置的 ``zephyr-ide-cortex`` 和 ``zephyr-ide-west`` 调试器类型与 Cortex-Debug 集成，
  支持 ST-Link、J-Link、OpenOCD、Black Magic Probe 及其他探针，并自动解析 ELF、GDB 和 runner 路径
- 与 clangd 或 C/C++ 集成以提供 IntelliSense
- 从构建仪表板（Build Dashboard）查看内存使用情况、Kconfig 和设备树；
  无需离开 VS Code 即可用旭日图（sunburst chart）查看 ROM 和 RAM
- 使用内置编辑器交互式编辑 Kconfig 选项
- 从项目面板添加、运行和重新配置 Twister 测试
- 在 Linux、macOS 和 Windows 上自动安装本机（native）主机工具（CMake、Python 3、Ninja、DTC、GCC 等）
- 安装和管理 Zephyr SDK 版本及各体系结构的工具链
- 从现有应用程序或 Zephyr 示例添加项目，支持多个构建以及按构建覆盖开发板和配置
- 将项目配置存储在可版本控制的 :file:`.vscode/zephyr-ide.json` 中，
  该文件可以指定 SDK、软件包和二进制资源（blob）

兼容性
*************

- Windows
- Linux
- macOS

快速入门
***************

#. 安装扩展

   从 `VS Code Marketplace`_ 或 `Open VSX Registry`_ 安装 IDE for Zephyr。

   另有一个捆绑了 Cortex-Debug、C/C++、Serial Monitor、Devicetree LSP 和 CMake 支持的扩展包，
   可在 `VS Code Marketplace (Extension Pack)`_ 和 `Open VSX Registry (Extension Pack)`_ 获取。

#. 打开概览页面并安装主机工具

   点击 :guilabel:`Host Tools` 卡片。扩展会验证所需的构建依赖
   （CMake、Python 3、Ninja、DTC、GCC 等）是否在 PATH 中，并可自动安装任何缺失的工具。

#. 配置 west 工作区

   点击 :guilabel:`Workspace` 卡片并选择一种设置方法：

   - **IDE for Zephyr Workspace from Git** — 克隆一个已包含预配置 IDE for Zephyr 工作区的仓库。
   - **West Workspace from Git** — 克隆一个基于 west 的现有 Zephyr 仓库。
   - **Standard Workspace** — 创建一个全新的工作区，包含 Python 虚拟环境、west 安装和 Zephyr 仓库初始化。
   - **Open Current Directory** — 采用现有的 :file:`.west` 文件夹，或通过 :envvar:`ZEPHYR_BASE`
     链接到外部的 Zephyr 安装。

   此步骤还会在需要时提示你安装 Zephyr SDK。之后你可以从概览页面的 :guilabel:`Zephyr SDK` 卡片管理 SDK。

   .. figure:: img/ide_for_zephyr_workspace_setup_vscode_ext.webp
      :align: center
      :alt: IDE for Zephyr 中的工作区设置选项

#. 添加项目和构建

   在项目面板中，点击 :guilabel:`Add Project` 添加一个现有应用程序，
   或复制一个 Zephyr 示例作为起点。

   添加项目后，点击 :guilabel:`Add Build` 创建一个构建配置。
   选择目标开发板，可选地再选择一个 runner 配置文件。每个项目可以有多个构建，
   分别针对不同开发板或配置。

#. 构建并烧录应用程序

   使用状态栏按钮或 :guilabel:`Project Build` 面板来构建、烧录，
   或运行一次全新的构建（pristine build）。构建输出显示在集成终端中。

#. 配置并运行调试会话

   IDE for Zephyr 自带内置的 ``zephyr-ide-west`` 调试器类型，
   它从当前激活的构建中读取 :file:`runners.yaml`，并自动将其转换为一个 Cortex-Debug 会话。
   无需在 :file:`.vscode/launch.json` 中配置条目即可开始使用。
   ``zephyr-ide-west`` 提供程序接受你本应传递给 ``west debugserver`` 的参数，
   而 ``zephyr-ide-cortex`` 提供程序则接受你直接传递给 ``cortex-debug`` 的参数。
   你还可以设置自己的启动（launch）配置并将其绑定到某个构建，
   扩展提供了可在启动时解析的命令。

   要手动添加启动配置，使用最小形式：

   .. code-block:: json

      {
        "name": "Zephyr IDE: Debug",
        "type": "zephyr-ide-west",
        "request": "launch"
      }

   内置提供程序会从 :file:`runners.yaml` 中选择 runner，解析 ELF 和 GDB 路径，
   并将会话转发给 Cortex-Debug。

共享项目配置
*****************************

项目设置、构建、runner 配置文件、Kconfig 叠加层（overlay）、设备树叠加层，
以及按构建划分的 west 和 CMake 参数都存储在 :file:`.vscode/zephyr-ide.json` 中。
该文件人类可读，可以提交到版本控制，使团队成员共享相同的工作区配置。

有用链接
************

- 浏览`扩展仓库`_
- 阅读`完整文档`_
- 试用`示例项目`_

.. _IDE for Zephyr:
   https://marketplace.visualstudio.com/items?itemName=mylonics.zephyr-ide
.. _VS Code Marketplace:
   https://marketplace.visualstudio.com/items?itemName=mylonics.zephyr-ide
.. _Open VSX Registry:
   https://open-vsx.org/extension/mylonics/zephyr-ide
.. _VS Code Marketplace (Extension Pack):
   https://marketplace.visualstudio.com/items?itemName=mylonics.zephyr-ide-extension-pack
.. _Open VSX Registry (Extension Pack):
   https://open-vsx.org/extension/mylonics/zephyr-ide-extension-pack
.. _Extension repository: https://github.com/mylonics/zephyr-ide
.. _Full documentation: https://zephyr-ide.mylonics.com/
.. _Getting started video: https://www.youtube.com/watch?v=Asfolnh9kqM
.. _Sample project: https://github.com/mylonics/zephyr-ide-sample-project
