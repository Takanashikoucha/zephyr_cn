.. _vscode_ide:

Visual Studio Code
##################

`Visual Studio Code`_（简称 VS Code）是一款流行的跨平台 IDE，支持 C 项目，
并拥有丰富的扩展集合。

本指南介绍如何在 VS Code 中为 Zephyr 的 :zephyr:code-sample:`blinky` 示例
配置 VS Code 的过程。

本指南中的步骤已在 Linux 上测试通过，macOS 和 Windows 上的步骤应该相同，
只需在必要时调整路径即可。

获取 VS Code
***********

`下载 VS Code`_ 并安装。

通过左侧面板中的 :guilabel:`Extensions` 市场安装所需的扩展。
搜索 `C/C++ Extension Pack`_ 并安装。

初始化新的工作区
**************************

本指南详细介绍了如何配置 :zephyr:code-sample:`blinky` 示例应用，
但对于任何 Zephyr 项目和 :ref:`工作区布局 <west-workspaces>`，步骤都是类似的。

开始之前，请确保你拥有一个可用的 Zephyr 开发环境，
参见 :ref:`getting_started` 中的说明。

在 VS Code 中打开项目
***************************

#. 在 VS Code 中，从主菜单选择 :menuselection:`File --> Open Folder`。

#. 导航到你的 Zephyr 工作区并选中它（即如果你按照入门说明操作，
   就是主目录（HOME）中的 :file:`zephyrproject` 文件夹）。

#. 如果系统提示，请启用工作区信任（workspace trust）。

生成编译命令
*************************

为了支持代码导航和代码检查（linting）功能，你必须先编译一次项目，
以生成 :file:`compile_commands.json` 文件，该文件将为 C/C++ 扩展提供
所需的信息（例如包含（include）路径）。你可以在 VS Code 内置终端中完成；
从顶部菜单选择 :menuselection:`Terminal --> New Terminal`，
或通过命令面板（:kbd:`Ctrl+Shift+P`）打开，然后输入：

.. code-block:: console

   $ cd zephyr
   $ west build -p always -b native_sim/native/64 samples/basic/blinky


配置 C/C++ 扩展
*****************************

现在你需要将指向生成的 :file:`compile_commands.json` 文件，
以在 VS Code 中启用代码检查和代码导航。

#. 转到 VS Code 顶部菜单的 :menuselection:`File --> Preferences --> Settings`。

#. 搜索参数 :guilabel:`C_Cpp > Default: Compile Commands`，并将其值设置为：
   ``zephyr/build/compile_commands.json``。

   代码中的代码检查（linting）错误现在应该已解决，你也能在代码中正常导航了。

其他资源
********************

还有许多其他扩展在 Zephyr 与 VS Code 的开发中会很有用。
本指南目前尚未涵盖它们，你可以参阅它们的文档进行配置：

贡献工具
====================

- `Checkpatch 扩展`_
- `EditorConfig 扩展`_

文档语言扩展
==================================

- `reStructuredText 扩展包`_

IDE 扩展
==============

- `CMake 扩展文档`_
- `nRF Kconfig 扩展`_
- `nRF DeviceTree 扩展`_
- `GNU 链接器映射文件扩展`_

其他指南
================

- `如何使用现代化的可视化 IDE 开发 Zephyr 应用`_

.. note::

   请注意，这些扩展的质量和维护水平可能并不相同。

.. _Visual Studio Code: https://code.visualstudio.com/
.. _Download VS Code: https://code.visualstudio.com/Download
.. _VS Code documentation: https://code.visualstudio.com/docs
.. _C/C++ Extension Pack: https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-extension-pack
.. _C/C++ Extension documentation: https://code.visualstudio.com/docs/languages/cpp
.. _CMake Extension documentation: https://code.visualstudio.com/docs/cpp/cmake-linux

.. _Checkpatch Extension: https://marketplace.visualstudio.com/items?itemName=idanp.checkpatch
.. _EditorConfig Extension: https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig

.. _reStructuredText Extension Pack: https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext-pack

.. _nRF Kconfig Extension: https://marketplace.visualstudio.com/items?itemName=nordic-semiconductor.nrf-kconfig
.. _nRF DeviceTree Extension: https://marketplace.visualstudio.com/items?itemName=nordic-semiconductor.nrf-devicetree
.. _GNU Linker Map files Extension: https://marketplace.visualstudio.com/items?itemName=trond-snekvik.gnu-mapfiles

.. _How to Develop Zephyr Apps with a Modern, Visual IDE: https://github.com/beriberikix/zephyr-vscode-example
