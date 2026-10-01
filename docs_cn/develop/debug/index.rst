.. _develop_debug:

调试
#########

.. _application_debugging:

应用调试
*********************

本节是一个快速实践参考，
用于开始使用 QEMU 调试你的应用。
本节的大多数内容
已经在 `QEMU`_ 和 `GNU_Debugger`_ 参考手册中覆盖。

.. _QEMU: https://wiki.qemu.org/Main_Page

.. _GNU_Debugger: https://www.gnu.org/software/gdb

在这个快速参考中，
你将找到快捷方式、特定环境变量和参数，
它们可以帮助你快速设置调试环境。

调试在 QEMU 中运行的应用的最简单方式是
使用 GNU Debugger，
并在你的开发系统中通过 QEMU
设置一个本地 GDB 服务器。

调试需要一个 :abbr:`ELF (Executable and Linkable Format)`
二进制镜像。
构建系统会在构建目录中生成该镜像。
默认情况下，内核二进制文件名为 :file:`zephyr.elf`。
可以使用 :kconfig:option:`CONFIG_KERNEL_BIN_NAME` 更改该名称。

GDB 服务器
==========

我们将使用标准 1234 TCP 端口
打开一个 :abbr:`GDB (GNU Debugger)` 服务器实例。
该端口号可以更改为最适合开发环境的端口。
有多种方式实现这一点。
每种方式都会启动一个 QEMU 实例，
处理器在启动时停止，
并有一个 GDB 服务器实例在监听连接。

直接运行 QEMU
~~~~~~~~~~~~~~~~~~~~~

你可以运行 QEMU，
在它开始执行任何代码之前
监听 "gdb 连接" 以进行调试。

.. code-block:: bash

   qemu -s -S <image>

这将设置 Qemu 监听端口 1234
并等待 GDB 连接。

上面使用的选项含义如下：

* ``-S`` 不在启动时启动 CPU；
  相反，你必须在 monitor 中键入 'c'。
* ``-s`` :literal:`-gdb tcp::1234` 的简写：
  在 TCP 端口 1234 上打开一个 GDB 服务器。


用 :command:`ninja` 运行 QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在应用的构建目录内运行以下命令：

.. code-block:: console

   ninja debugserver

QEMU 会将控制台输出写到
通过 CMake 指定的 :makevar:`${QEMU_PIPE}` 路径，
通常是构建目录内的 :file:`qemu-fifo`。
你可以在运行期间
用 :command:`tail -f qemu-fifo` 监控该文件。

用 :command:`west` 运行 QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

从你的项目根目录运行以下命令：

.. code-block:: console

   west build -t debugserver_qemu

QEMU 会将控制台输出写到
你调用 :command:`west` 的终端。

配置 :command:`gdbserver` 监听设备
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kconfig 选项 :kconfig:option:`CONFIG_QEMU_GDBSERVER_LISTEN_DEV`
控制监听设备，
它可以是 TCP 端口号或字符设备的路径。
GDB 9.0 及之后的版本
也支持 Unix 域套接字。

如果该选项未设置，
那么 QEMU 调用将缺少 ``-s`` 或 ``-gdb`` 参数。
然后你可以使用 :envvar:`QEMU_EXTRA_FLAGS`
shell 环境变量传入你自己的监听设备配置。

GDB 客户端
==========

通过运行 :command:`gdb`
并给出以下命令来连接到服务器：

.. code-block:: bash

   $ path/to/gdb path/to/zephyr.elf
   (gdb) target remote localhost:1234
   (gdb) dir ZEPHYR_BASE

.. note::

   用你系统正确的
   :ref:`ZEPHYR_BASE <important-build-vars>` 替换。

你可以使用本地 GDB 配置 :file:`.gdbinit`
在每次运行时初始化你的 GDB 实例。
你的主目录是典型位置，
但你可以配置 GDB 从其他位置加载，
包括你调用 :command:`gdb` 的目录。
这个示例文件执行与上面相同的配置：

.. code-block:: none

   target remote localhost:1234
   dir ZEPHYR_BASE

替代接口
~~~~~~~~~~~~~~~~~~

GDB 提供一个基于 curses 的接口，
在终端中运行。
在调用 :command:`gdb` 时传入 ``--tui`` 选项，
或在 :command:`gdb` 内给出 ``tui enable`` 命令。

.. note::

   你开发系统上的 GDB 版本
   可能不支持 ``--tui`` 选项。
   请确保你使用与用于构建二进制的工具链对应的
   SDK 中的 GDB 二进制文件。

最后，下面的命令使用
:abbr:`DDD (Data Display Debugger)`
（GDB 的图形前端）连接到 GDB 服务器。
该命令从 ELF 二进制文件加载符号表，
在本例中为 :file:`zephyr.elf`。

.. code-block:: bash

   ddd --gdb --debugger "gdb zephyr.elf"

两条命令都执行 :command:`gdb`。
命令名可能根据你使用的工具链
和交叉开发工具而变化。

:command:`ddd` 可能不在你的开发系统中默认安装。
按照你的系统说明安装它。
例如，在 Ubuntu 系统上使用
:command:`sudo apt-get install ddd`。

调试
=========

按上述配置，当你连接 GDB 客户端时，应用将在系统启动时停止。
你可以设置断点、单步执行代码等，
就像直接在 :command:`gdb` 内运行应用一样。

.. note::

   :command:`gdb` 不会在应用运行时
   打印系统控制台输出，
   这与你直接在 GDB 中运行本地应用时不同。
   如果你在连接客户端后只是 :command:`continue`，
   应用将运行，但看起来什么都不发生。
   按上述描述检查控制台输出。

用 Eclipse 调试
******************

概览
========

CMake 支持生成项目描述文件，
可以导入到 Eclipse 集成开发环境（IDE）
并用于图形调试。

`GNU MCU Eclipse plug-ins`_
提供了一个机制，
在 Eclipse 中用 pyOCD、Segger J-Link
和 OpenOCD 调试工具调试 ARM 项目。

下面的教程演示如何在 Windows 中
用 pyOCD 在 Eclipse 中调试 Zephyr 应用。
假设你已经安装了 GCC ARM Embedded 工具链和 pyOCD。

设置 Eclipse 开发环境
==========================================

#. 下载并安装 `Eclipse IDE for C/C++ Developers`_。

#. 在 Eclipse 中，通过打开菜单
   ``Window->Eclipse Marketplace...``，
   搜索 ``GNU MCU Eclipse``，
   并点击匹配结果的 ``Install``
   安装 `GNU MCU Eclipse plug-ins`_。

#. 通过打开菜单 ``Window->Preferences``，
   导航到 ``MCU``，
   并设置 ``Global pyOCD Path``
   来配置 pyOCD GDB 服务器路径。

生成并导入 Eclipse 项目
=====================================

#. 按 :ref:`toolchain_gnuarmemb` 中描述的
   设置 GNU Arm Embedded 工具链。

#. 导航到 Zephyr 树之外的文件夹
   来构建你的应用。

   .. code-block:: console

      # On Windows
      cd %userprofile%

   .. note::
      如果构建目录是源目录的子目录，
      如在 Zephyr 中通常所做，
      CMake 将警告：

      "The build directory is a subdirectory of the source directory.

      This is not supported well by Eclipse.  It is strongly recommended to use
      a build directory which is a sibling of the source directory."

#. 用 CMake 配置你的应用并用 ninja 构建它。
   注意由 ``-G"Eclipse CDT4 - Ninja"`` 参数
   指定的不同 CMake 生成器。
   这将生成一个 Eclipse 项目描述文件 :file:`.project`，
   除了通常的 ninja 构建文件。

   .. zephyr-app-commands::
      :tool: all
      :zephyr-app: samples/synchronization
      :host-os: win
      :board: frdm_k64f
      :gen-args: -G"Eclipse CDT4 - Ninja"
      :goals: build
      :compact:

#. 在 Eclipse 中，通过打开菜单
   ``File->Import...``
   并选择选项 ``Existing Projects into Workspace``
   导入你生成的项目。
   在选项 ``Select root directory:`` 中
   浏览到你的应用构建目录。
   在找到的项目列表中勾选你的项目的复选框
   并点击 ``Finish`` 按钮。

创建调试器配置
===============================

#. 打开菜单 ``Run->Debug Configurations...``。

#. 选择 ``GDB PyOCD Debugging``，
   点击 ``New`` 按钮，
   并配置以下选项：

   - 在 Main 标签中：

     - Project: ``my_zephyr_app@build``
     - C/C++ Application: :file:`zephyr/zephyr.elf`

   - 在 Debugger 标签中：

     - pyOCD Setup

       - Executable path: :file:`${pyocd_path}\\${pyocd_executable}`
       - 取消勾选 "Allocate console for semihosting"

     - Board Setup

       - Bus speed: 8000000 Hz
       - 取消勾选 "Enable semihosting"

     - GDB Client Setup

       - Executable path 示例（使用你的 ``GNUARMEMB_TOOLCHAIN_PATH``）：
         :file:`C:\\gcc-arm-none-eabi-6_2017-q2-update\\bin\\arm-none-eabi-gdb.exe`

   - 在 SVD Path 标签中：

     - File path: :file:`<workspace
       top>\\modules\\hal\\nxp\\mcux\\devices\\MK64F12\\MK64F12.xml`

     .. note::
        这是可选的。
        它向调试器提供 SoC 的
        内存映射寄存器地址和位域。

#. 点击 ``Debug`` 按钮开始调试。

RTOS 感知
=============

对 Zephyr RTOS 感知的支持
在 `pyOCD v0.11.0`_ 及之后实现。
它与 Eclipse 中的 GDB PyOCD Debugging 兼容，
但你必须在应用中启用 CONFIG_DEBUG_THREAD_INFO=y。

调试 I2C 通信
***************************

可以记录应用执行的所有或
部分 I2C 事务。
该功能由 Kconfig 选项
:kconfig:option:`CONFIG_I2C_DUMP_MESSAGES` 启用，
但它使用 :c:macro:`LOG_DBG` 函数打印内容，
因此 :kconfig:option:`CONFIG_I2C_LOG_LEVEL_DBG`
选项也必须启用。

转储的示例输出如下::

   D: I2C msg: io_i2c_ctrl7_port0, addr=50
   D:    W      len=01: 00
   D:    R Sr P len=08:
   D: contents:
   D: 43 42 41 00 00 00 00 00 |CBA.....

第一行指示 I2C 控制器
和事务的目标地址。
在上面示例中，I2C 控制器名为 ``io_i2c_ctrl7_port0``，
目标设备地址是 ``0x50``

.. note::

   地址、长度和内容的值都是十六进制，
   但缺少 ``0x`` 前缀

接下来的行包含消息，包括发送和接收的。
写消息的内容总是显示，
而读消息的内容由 ``i2c_dump_msgs_rw`` 函数的参数控制。
该函数可供用户使用，
但也被 ``i2c_transfer`` API 函数内部调用，启用读内容转储。
在长度参数之前，
使用缩写打印消息的头部：

  - W - 写消息
  - R - 读消息
  - Sr - 重启位
  - P - 停止位

上面示例显示一个写消息，
字节 ``0x00`` 表示从 I2C 目标读取的寄存器地址。
之后日志显示接收消息的长度，
接着是从目标读取的字节 ``43 42 41 00 00 00 00 00``。
内容转储包含十六进制和 ASCII 表示。

过滤 I2C 通信转储
===================================

默认情况下，
所有 I2C 控制器和 I2C 目标之间的
所有 I2C 通信都被记录。
这可能用无关设备污染日志，
使有效调试与感兴趣设备的通信变得困难。

启用 Kconfig 选项
:kconfig:option:`CONFIG_I2C_DUMP_MESSAGES_ALLOWLIST`
以创建要记录的 I2C 目标允许列表。
设备允许列表使用 devicetree 配置，
例如::

  / {
      i2c {
          display0: some-display@a {
              ...
          };
          sensor3: some-sensor@b {
              ...
          };
      };

      i2c-dump-allowlist {
          compatible = "zephyr,i2c-dump-allowlist";
          devices = <&display0>, <&sensor3>;
      };
  };

过滤器节点由具有
``zephyr,i2c-dump-allowlist`` 值的
compatible 字符串标识。
设备使用具有 I2C 总线上设备 phandle 的
``devices`` 属性选择。

在上面示例中，
与设备 ``display0`` 和 ``sensor3`` 的通信
将显示在日志中。


.. _Eclipse IDE for C/C++ Developers: https://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/oxygen2
.. _GNU MCU Eclipse plug-ins: https://gnu-mcu-eclipse.github.io/plugins/install/
.. _pyOCD v0.11.0: https://github.com/pyocd/pyOCD/releases/tag/v0.11.0
