.. _workbench_for_zephyr:

Zephyr 工作台
#########################################

Zephyr 工作台（Workbench for Zephyr）是一个 Visual Studio Code（VS Code）扩展，为 Zephyr 开发提供支持，包括 **SDK 管理**、**项目创建向导**、**构建/烧录** 和 **调试**。

查看 `入门教程`_ 了解逐步操作说明。

主要功能
************

- 安装本机主机工具（Python、CMake 等）
- 安装并分配工具链（Zephyr SDK、IAR 等）
- 导入 West 工作区
- 创建和导入 Zephyr 应用
- 构建和烧录应用
- 调试应用
- 自动安装运行器
- 执行内存和静态分析

兼容性
*************

- Windows 10-11
- Linux（x86_64）

  - Ubuntu
  - Debian
  - Fedora
  - 其他发行版也可能可用（未测试）

- macOS

快速上手
***************

#. 安装扩展

   从 VS Code Marketplace 安装 `Workbench for Zephyr`_。

#. 打开 Workbench for Zephyr 扩展

   在操作栏（Activity Bar）中，点击 :guilabel:`Workbench for Zephyr` 图标。

#. 安装主机工具

   点击 :guilabel:`Install Host Tools` 下载并安装本机工具（通常安装到 ``${HOME}/.zinstaller``）。

   .. figure:: img/workbench_for_zephyr_install_host_tools.webp
      :align: center
      :alt: 在 Workbench for Zephyr 中安装主机工具

   .. note::

      某些主机工具可能需要管理员权限。
      在 Windows 上，安装 7z 时需要管理员权限。
      在 Linux 上，使用包管理器安装工具时需要管理员权限，
      例如运行 :command:`apt install` 时。

#. 导入工具链

   点击 :guilabel:`Import Toolchain`，选择工具链，并选择目标文件夹。

   工具链提供构建和调试 Zephyr 应用所需的编译器和调试器。
   Zephyr SDK 是推荐选项，可以安装为完整包或针对特定目标的最小版本。
   Workbench 也支持其他工具链，例如 IAR。

#. 初始化 / 导入 West 工作区

   点击 :guilabel:`Initialize workspace` 并填写工作区信息。

   .. figure:: img/workbench_for_zephyr_west_workspace.webp
      :align: center
      :width: 600px
      :alt: 在 Workbench for Zephyr 中初始化 West 工作区

   Workbench 将创建工作区并解析 west 清单以配置项目。

#. 创建新应用

   在 Workbench for Zephyr 中，新项目基于 Zephyr 源码中的示例。

   - 点击 :guilabel:`Create New Application`。
   - 选择要关联的 :guilabel:`West Workspace`（West 工作区）。
   - 选择要使用的 :guilabel:`Zephyr SDK`。
   - 选择目标 :guilabel:`Board`（开发板），例如 ``ST STM32F4 Discovery``。
   - 选择要基于的 :guilabel:`Sample`（示例）项目，例如 ``hello_world``。
   - 输入项目名称。
   - 输入项目位置。

   .. figure:: img/workbench_for_zephyr_application.webp
      :align: center
      :width: 600px
      :alt: 在 Workbench for Zephyr 中从示例创建新应用

#. 构建应用

   点击状态栏中的 :guilabel:`Build`（构建），或选择应用文件夹进行构建。
   构建输出显示在集成终端中。

#. 配置并运行调试会话

   使用 :guilabel:`Debug Manager`（调试管理器）生成或更新调试配置
   （:file:`.vscode/launch.json`）：

   - 生成的 ELF 文件（程序路径）
   - SVD 文件（可选）
   - GDB/端口/地址（如需要）
   - 调试服务器/运行器（OpenOCD、J-Link、LinkServer、pyOCD 等）

   .. figure:: img/workbench_for_zephyr_debug_manager.webp
      :align: center
      :width: 600px
      :alt: Workbench for Zephyr 中的调试管理器

   然后通过 :guilabel:`Run and Debug`（运行和调试）正常启动调试。

安装运行器
***************

Workbench for Zephyr 可以为某些运行器（例如 OpenOCD 和 STM32CubeProgrammer）提供安装程序。使用 :guilabel:`Install Runners` 查看支持的工具并安装它们（或打开供应商网站）。

有用链接
************

- 浏览 `扩展仓库`_
- 了解更多详情，查看 `完整文档`_

.. _Extension repository: https://github.com/Ac6Embedded/vscode-zephyr-workbench
.. _Full documentation: https://z-workbench.com/
.. _Workbench for Zephyr: https://marketplace.visualstudio.com/items?itemName=Ac6.zephyr-workbench
.. _Getting started tutorial: https://youtu.be/1RB0GI6rJk0?si=_D2AA3KurzCwLtRv
