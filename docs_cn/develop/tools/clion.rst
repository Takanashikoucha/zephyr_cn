.. _clion_ide:

CLion
#####

.. note::

   本指南描述如何用 CLion 的 CMake 集成设置、构建和调试 Zephyr 的示例应用。这种方式不再最优。

   CLion 现在有 `原生 Zephyr West 集成`_，提供更简单、更直观的方式打开、构建和运行/调试 Zephyr 项目。本指南将很快更新，但如果你偏好使用 CMake，它仍然有效。

CLion_ 是一款跨平台的 C/C++ IDE，支持多线程 RTOS 调试。

本指南描述在 CLion 中设置、构建和调试 Zephyr 的 :zephyr:code-sample:`multi-thread-blinky` 示例的过程。

说明已在 Windows 上测试。在 CLion 工作流方面，步骤对 macOS 和 Linux 相同，但确保选择正确的环境文件并调整路径。

获取 CLion
*********

`下载 CLion`_ 并安装它。

初始化新工作区
**************************

本指南给出如何构建和调试 :zephyr:code-sample:`multi-thread-blinky` 示例应用的细节，但说明对任何 Zephyr 项目和 :ref:`工作区布局 <west-workspaces>` 类似。

开始前，确保你有一个可用的 Zephyr 开发环境，按照 :ref:`getting_started` 中的说明。

在 CLion 中打开项目
**************************

#. 在 CLion 中，在欢迎屏幕上点击 :guilabel:`Open` 或从主菜单选择 :menuselection:`File --> Open`。

#. 导航到你的 Zephyr 工作区（即如果你遵循了入门说明，则为主目录中的 :file:`zephyrproject` 文件夹），然后选择 :file:`zephyr/samples/basic/threads` 或其他示例项目文件夹。

   点击 :guilabel:`OK`。

#. 如果提示，点击 :guilabel:`Trust Project`。

   更多项目安全信息见 CLion 在线帮助的 `项目安全`_ 章节。

配置工具链和 CMake 配置档
*****************************************

CLion 将打开带有 CMake 配置档设置的 :guilabel:`Open Project Wizard`。如果未出现，转到 :menuselection:`Settings --> Build, Execution, Deployment --> CMake`。

#. 点击 :guilabel:`Toolchain` 字段旁的 :guilabel:`Manage Toolchains`。这将打开 :guilabel:`Toolchain` 设置对话框。

#. 我们推荐在 Windows 上用默认设置的 :guilabel:`Bundled MinGW` 工具链，或在 Unix 机器上用 :guilabel:`System`（默认）工具链。

#. 点击 :menuselection:`Add environment --> From file` 并选择 ``..\.venv\Scripts\activate.bat``。

   .. figure:: img/clion_toolchain_mingw.webp
      :width: 600px
      :align: center
      :alt: MinGW toolchain with environment script

   点击 :guilabel:`Apply` 保存更改。

#. 回到 CMake 配置档设置对话框，在 :guilabel:`CMake options` 字段中指定你的开发板。例如：

   .. code-block::

      -DBOARD=nrf52840dk/nrf52840

   .. figure:: img/clion_cmakeprofile.webp
      :width: 600px
      :align: center
      :alt: CMake profile

#. 点击 :guilabel:`Apply` 保存更改。

   CMake 加载应该成功完成。

为调试配置 Zephyr 参数
*************************************

#. 在右上角的配置切换器中，选择 :guilabel:`guiconfig` 并点击锤子图标。

#. 用 GUI 应用设置以下标志：

   .. code-block::

      DEBUG_THREAD_INFO
      THREAD_RUNTIME_STATS
      DEBUG_OPTIMIZATIONS

构建项目
*****************

在配置切换器中，选择 **zephyr_final** 并点击锤子图标。

注意其他 CMake 目标（如 ``puncover`` 或 ``hardenconfig``）也可以在此时调用。

启用 RTOS 集成
***********************

#. 转到 :menuselection:`Settings --> Build, Execution, Deployment --> Embedded Development --> RTOS Integration`。

#. 设置 :guilabel:`Enable RTOS Integration` 复选框。

   此选项在调试期间启用 Zephyr 任务视图。更多信息见 CLion 在线帮助的 `多线程 RTOS 调试`_。

   你可以将选项保持为 :guilabel:`Auto`。CLion 将自动检测 Zephyr。

创建嵌入式 GDB Server 配置
*******************************************

要在 CLion 中调试 Zephyr 应用，你需要从嵌入式 GDB Server 模板创建一个运行/调试配置。

以下说明展示 Nordic Semiconductor 开发板和 Segger J-Link 调试探针的情况。如果你的设置不同，确保相应调整配置设置。

#. 从主菜单选择 :menuselection:`Run --> New Embedded Configuration`。

#. 配置设置：

    .. list-table::
        :header-rows: 1

        * - 选项
          - 值

        * - :guilabel:`Name`（可选）
          - Zephyr-threads

        * - :guilabel:`GDB Server Type`
          - Segger JLink

        * - :guilabel:`Location`
          - Windows 上 ``JLinkGDBServerCL.exe`` 的路径或 macOS/Linux 上 ``JLinkGDBServer`` 二进制文件。

        * - :guilabel:`Debugger`
          - Bundled GDB

            .. note:: 对非 ARM 和非 x86 架构，用 Zephyr SDK 的 GDB 可执行文件。确保选择带 Python 支持的版本（例如 **riscv64-zephyr-elf-gdb-py**）并检查系统 ``PATH`` 中是否有 Python。

        * - :guilabel:`Target`
          - zephyr-final

        * - :guilabel:`Executable binary`
          - zephyr-final

        * - :guilabel:`Download binary`
          - Always

        * - :guilabel:`TCP/IP port`
          - Auto

    .. figure:: img/clion_gdbserverconfig.webp
       :width: 500px
       :align: center
       :alt: Embedded GDB server configuration

#. 点击 :guilabel:`Next` 设置 Segger J-Link 参数。

    .. figure:: img/clion_segger_settings.webp
       :width: 500px
       :align: center
       :alt: Segger J-Link parameters

#. 准备好时点击 :guilabel:`Create`。

开始调试
***************

#. 点击代码行旁左侧槽中的位置设置断点。

#. 确保配置切换器中选择了 **Zephyr-threads** 并点击 bug 图标或按 :kbd:`Ctrl+D`。

#. 当断点被命中时，CLion 打开 Debug 工具窗口。

   Zephyr 任务列在 :guilabel:`Threads & Variables` 窗格中。你可以在它们之间切换并检查每个任务的变量。

    .. figure:: img/clion_debug_threads.webp
       :width: 800px
       :align: center
       :alt: Viewing Zephyr tasks during a debug session

   参考 `CLion 在线帮助`_ 获取 IDE 调试能力的详细描述。

.. _native Zephyr West integration: https://jb.gg/cl_zephyr_doc
.. _CLion: https://www.jetbrains.com/clion/
.. _Download CLion: https://www.jetbrains.com/clion/download
.. _Project security: https://www.jetbrains.com/help/clion/project-security.html#projects_security
.. _Multi-threaded RTOS debug: https://www.jetbrains.com/help/clion/rtos-debug.html
.. _CLion web help: https://www.jetbrains.com/help/clion/debugging-code.html
