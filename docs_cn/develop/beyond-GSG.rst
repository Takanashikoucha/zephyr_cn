.. _beyond-gsg:

超越入门指南
################################

:ref:`getting_started` 提供了一条直接的路径，
用于设置你的 Linux、macOS 或 Windows 环境
以进行 Zephyr 开发。
在本文档中，我们将深入探讨 Zephyr 开发环境设置
相关问题及替代方案。

.. _python-pip:

Python 和 pip
**************

Python 3 及其包管理器 pip\ [#pip]_ 被 Zephyr 广泛使用，
用于安装和运行编译及运行 Zephyr 应用所需的脚本、
设置和维护 Zephyr 开发环境、
以及构建项目文档。

根据你的操作系统，
安装新包时你可能需要向 ``pip3`` 命令
提供 ``--user`` 标志。
这一点在说明中均有记录。
有关 pip\ [#pip]_ 的更多信息，
包括 `关于 -\-user 的信息`_，
请参阅 Python 打包用户指南中的 `安装包`_。

- 在 Linux 上，确保 ``~/.local/bin``
  位于 :envvar:`PATH` :ref:`环境变量 <env_vars>` 的开头，
  否则用 ``--user`` 安装的程序将无法被找到。
  使用 ``--user`` 安装可避免 pip 与系统包管理器之间的冲突，
  也是基于 Debian 的发行版的默认行为。

- 在 macOS 上，`Homebrew 禁用 -\--user`_。

- 在 Windows 上，如果你需要使用该选项，
  请参阅 `安装包`_ 中关于 ``--user`` 的信息。

在所有操作系统上，
pip 的 ``-U`` 标志会在包已本地安装
但有更新版本可用时安装或更新该包。
如果需要包的最新版本，
使用该标志是良好实践。
（检查 :zephyr_file:`scripts/requirements.txt` 文件，
查看是否期望特定的 Python 包版本。）

高级平台设置
***********************

以下是针对受支持开发平台的
更高级平台设置配置的一些替代说明：

.. toctree::
   :maxdepth: 1

   Linux 设置替代方案 <getting_started/installation_linux.rst>
   macOS 设置替代方案 <getting_started/installation_mac.rst>
   Windows 设置替代方案 <getting_started/installation_win.rst>

.. _gs_toolchain:

安装工具链
*******************

Zephyr 二进制文件由 *工具链* 编译和链接，
它由交叉编译器及相关工具组成，
与用于开发在主机操作系统上
本地运行的软件的编译器和工具不同。

你可以安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`
以获取所有受支持架构的工具链，
或安装由 SoC 厂商或特定开发板推荐的
:ref:`替代工具链 <toolchains>`
（查看你的特定 :ref:`开发板级文档 <boards>`）。

你可以通过设置 :ref:`环境变量 <env_vars>`
（例如将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT <{TOOLCHAIN}_TOOLCHAIN_PATH>`
设置为受支持的值），
连同工具链变体特定的额外变量，
来配置 Zephyr 构建系统使用特定工具链。

.. _gs_toolchain_update:

更新 Zephyr SDK 工具链
***************************

更新 Zephyr SDK 时，
检查 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 或
:envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量
是否已经设置。

* 如果变量未设置，
  默认将选择最新兼容版本的 Zephyr SDK。
  不做任何更改，继续下一步。

* 如果 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 已设置，
  构建时将选择对应的工具链。
  Zephyr SDK 由值 ``zephyr`` 标识。
  如果 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 环境变量
  不是 ``zephyr``，
  则取消设置它或将其值更改为 ``zephyr``，
  以确保选择 Zephyr SDK。

* 如果 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量已设置，
  它将覆盖 Zephyr SDK 的默认查找位置。
  如果你将 Zephyr SDK 安装到
  :ref:`推荐位置 <toolchain_zephyr_sdk_bundle_variables>` 之一，
  可以取消设置该变量。
  否则，将其设置为你选择的安装位置。

有关 Zephyr 中这些环境变量的更多信息，
请参阅 :ref:`env_vars_important`。

克隆 Zephyr 仓库
*******************************

Zephyr 项目源代码维护在
`GitHub zephyr 仓库 <https://github.com/zephyrproject-rtos/zephyr>`_ 中。
Zephyr 使用的外部模块位于
父 `GitHub Zephyr 项目 <https://github.com/zephyrproject-rtos/>`_ 中。
由于这些依赖关系，
使用 Zephyr 创建的 :ref:`west <west>` 工具
来获取和管理 Zephyr 及外部模块源代码非常方便。
有关更多详情，请参阅 :ref:`west-basics`。

安装开发工具后，
使用 :ref:`west` 创建、初始化
并从 zephyr 和外部模块仓库下载源代码。
我们将使用名称 ``zephyrproject``，
但你可以选择任何路径中不包含空格的名称。

.. code-block:: console

   west init zephyrproject
   cd zephyrproject
   west update

``west update`` 命令获取并保持
:ref:`模块` 在 :file:`zephyrproject` 文件夹中
与本地 zephyr 仓库中的代码同步。

.. warning::

   每当 :file:`zephyr/west.yml` 更改时，
   你必须运行 ``west update``。
   例如，当你拉取 :file:`zephyr` 仓库、
   在其中切换分支、
   或在其中执行 ``git bisect`` 时。

保持 Zephyr 更新
=====================

要更新 Zephyr 项目源代码，
你需要通过 ``git`` 获取最新更改。
之后，如前一段所述运行 ``west update``。
此外，检查更新或新增的 Python 依赖。

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         # 将 zephyrproject 替换为你给 west init 的路径
         cd zephyrproject/zephyr
         git pull
         west update
         west packages pip --install

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            :: 将 zephyrproject 替换为你给 west init 的路径
            cd zephyrproject\zephyr
            git pull
            west update
            cmd /c scripts\utils\west-packages-pip-install.cmd

         .. code-tab:: powershell

            # 将 zephyrproject 替换为你给 west init 的路径
            cd zephyrproject\zephyr
            git pull
            west update
            python -m pip install @((west packages pip) -split ' ')

导出 Zephyr CMake 包
***************************

如果尚未作为 :ref:`getting_started` 的一部分完成，
:ref:`cmake_pkg` 可以被导出到
CMake 的用户包注册表中。

.. _gs-board-aliases:

开发板别名
*************

与多个开发板协作的开发者
可能觉得显式开发板名称繁琐，
并希望为常用目标使用别名。
这可以通过一个 CMake 文件实现，内容如下：

.. code-block:: cmake

   # 变量 foo_BOARD_ALIAS=bar 将 BOARD=foo 替换为 BOARD=bar，
   # 并在 CMake 缓存中设置 BOARD_ALIAS=foo。
   set(pca10028_BOARD_ALIAS nrf51dk/nrf51822)
   set(pca10056_BOARD_ALIAS nrf52840dk/nrf52840)
   set(k64f_BOARD_ALIAS frdm_k64f)
   set(sltb004a_BOARD_ALIAS efr32mg_sltb004a)

并在 :envvar:`ZEPHYR_BOARD_ALIASES` 中指定其位置。
这允许在 ``cmake -DBOARD=pca10028``
和 ``west -b pca10028`` 这样的上下文中
使用别名 ``pca10028``。

构建和运行应用
****************************

你可以在真实硬件上使用受支持的主机系统构建、烧录和运行 Zephyr 应用。
根据你的操作系统，你还可以用 QEMU 在仿真中运行它，
或用 :zephyr:board:`native_sim <native_sim>` 作为本地应用运行。
有关构建应用的更多信息，
请参阅 :ref:`build_an_application` 章节。

构建 Blinky
=============

让我们构建 :zephyr:code-sample:`blinky` 示例应用。

Zephyr 应用被构建为在特定硬件上运行，
称为"开发板"\ [#board_misnomer]_。
我们这里使用 Phytec
:zephyr:board:`reel_board<reel_board>`，
但如果你有不同的开发板，
可以将 ``reel_board`` 构建目标更改为其他值。
有关受支持开发板的列表，
请参阅 :ref:`boards`
或在 ``zephyrproject`` 目录内任何位置
运行 ``west boards``。

#. 进入 zephyr 仓库：

   .. code-block:: console

      cd zephyrproject/zephyr

#. 为 ``reel_board`` 构建 blinky 示例：

   .. zephyr-app-commands::
      :zephyr-app: samples/basic/blinky
      :board: reel_board
      :goals: build

主要构建产物位于 :file:`build/zephyr`；
:file:`build/zephyr/zephyr.elf`
是 ELF 格式的 blinky 应用二进制文件。
根据你的开发板，
可能还存在其他二进制格式、反汇编和 map 文件。

:zephyr_file:`samples` 文件夹中的
其他示例应用记录在
:zephyr:code-sample-category:`samples` 中。

.. note:: 如果你想为其他开发板或应用
   重用现有构建目录，
   需要向 ``west build`` 添加参数 ``-p=auto``
   以清理之前构建的设置和产物。

通过烧录到开发板运行应用
==========================================

Zephyr 支持的大多数硬件开发板
都可以通过运行 ``west flash`` 烧录。
这可能需要安装和配置开发板特定工具
才能正常工作。

有关更多详情，
请参阅 :ref:`application_run`
和 :ref:`boards` 中你的特定开发板的文档。

.. _setting-udev-rules:

设置 udev 规则
==================

烧录开发板需要直接访问开发板硬件的权限，
通常由烧录工具的安装来管理。
在 Linux 系统上，
如果 ``west flash`` 命令失败，
你很可能需要定义 udev 规则
来授予所需的访问权限。

Udev 是 Linux 内核的设备管理器，
udev 守护程序处理硬件设备添加（或移除）到系统时引发的所有用户空间事件。
我们可以添加一个规则文件，
授予非 root 用户对某些 USB 连接设备的访问权限。

OpenOCD（On-Chip Debugger）项目
提供了一个规则文件，
为大多数 Zephyr 支持的基于 arm 的开发板
定义了开发板特定规则，
因此我们推荐安装该规则文件：
从他们的 sourceforge 仓库下载，
或者如果你安装了 Zephyr SDK，
SDK 文件夹中就有该规则文件的副本：

* 下载 OpenOCD 规则文件并复制到正确位置::

     wget -O 60-openocd.rules https://sf.net/p/openocd/code/ci/master/tree/contrib/60-openocd.rules?format=raw
     sudo cp 60-openocd.rules /etc/udev/rules.d

* 或从 Zephyr SDK 文件夹复制规则文件::

     sudo cp ${ZEPHYR_SDK_INSTALL_DIR}/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d

然后，无论哪种情况，
都要求 udev 守护程序重新加载这些规则::

   sudo udevadm control --reload

拔下再插上到开发板的 USB 连接，
你就应该有权限访问开发板硬件进行烧录了。
如需更多信息，
查看你的开发板特定文档（:ref:`boards`）。

在 QEMU 中运行应用
===========================

当目标为 x86 或 ARM Cortex-M3 架构时，
你可以使用 `QEMU <https://www.qemu.org/>`_
在主机系统上通过仿真运行 Zephyr 应用。
QEMU 包含在 Zephyr SDK 中。

如果使用手动安装的 QEMU，
确保它在系统 ``PATH`` 环境变量中可用。

``QEMU_BIN_PATH`` 可以作为可选覆盖使用，
指定 Twister 使用的 QEMU 二进制文件位置。
提供时，Twister 会验证指定路径存在。
否则，Twister 依赖 SDK 或其他 QEMU 发现机制。

例如，你可以使用 x86 仿真开发板配置
（``qemu_x86``）构建并运行
:zephyr:code-sample:`hello_world` 示例：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: qemu_x86
   :goals: build run

要退出 QEMU，按 :kbd:`Ctrl-a`，然后按 :kbd:`x`。

使用 ``qemu_cortex_m3``
以目标为仿真的 Arm Cortex-M3 示例。

.. _gs_native:

本地运行示例应用（Linux）
=========================================

你可以将某些示例编译为
在 Linux 上运行的主机程序。
有关更多信息，请参阅 :zephyr:board:`native_sim`。
在 64 位主机操作系统上，
你需要安装 32 位 C 库，
或目标为 :ref:`native_sim/native/64<native_sim32_64>` 构建。

首先，为 ``native_sim`` 构建 Hello World。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: native_sim
   :goals: build

接下来，运行应用。

.. code-block:: console

   west build -t run
   # 或直接运行 zephyr.exe：
   ./build/zephyr/zephyr.exe

按 :kbd:`Ctrl-C` 退出。

你可以运行 ``./build/zephyr/zephyr.exe --help``
获取可用选项列表。

该可执行文件可以使用标准工具
（如 gdb 或 valgrind）进行插桩。

.. rubric:: 脚注

.. [#pip]

   pip 是 Python 的包安装器。
   其 ``install`` 命令首先尝试
   重用已安装在电脑上的包和包依赖。
   如果不可能，``pip install``
   会从互联网上的 Python 包索引（PyPI）下载它们。

   Zephyr 的 :file:`requirements.txt`
   请求的包版本可能与系统上的其他要求冲突，
   在这种情况下你可能想为 Zephyr 开发
   设置一个 virtualenv。

.. [#board_misnomer]

   这随时间推移变得有些名不副实。
   尽管目标可以（且经常是）运行在其自己专用硬件开发板上的微处理器，
   Zephyr 也支持使用 QEMU 在仿真中运行
   为其他架构构建的目标、
   产生实现 Zephyr 驱动接口的本地主机系统二进制文件的目标，
   甚至在同一物理芯片上不同架构的 CPU 核心上
   运行不同的 Zephyr 基础二进制文件。
   每个这些硬件配置都称为"开发板"，
   尽管在上下文中这不总是完全合理。

.. _关于 -\--user 的信息:
 https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site
.. _Homebrew 禁用 -\--user:
 https://docs.brew.sh/Homebrew-and-Python#note-on-pip-install---user
.. _安装包:
 https://packaging.python.org/tutorials/installing-packages/
