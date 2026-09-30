.. _application:

应用
开发
#######################

.. note::

   在
   本文档
   中，
   我们
   假设：

   - 你的
     **应用
     目录**，
     :file:`<app>`，
     是
     类似
     :file:`<home>/zephyrproject/app`
     的
     东西
   - 其
     **构建
     目录**
     是
     :file:`<app>/build`

   这些
   术语
   在
   下面
   定义。
   在
   Linux/macOS
   上，
   <home>
   等价
   于
   ``~``。
   在
   Windows
   上，
   它
   是
   ``%userprofile%``。

   将
   你的
   应用
   保持
   在
   工作区
   （:file:`<home>/zephyrproject`）
   内
   使
   使用
   ``west
   build``
   和
   其他
   命令
   配合
   它
   更
   容易。
   （你
   可以
   把
   应用
   放
   在
   任何
   地方
   只要
   :ref:`ZEPHYR_BASE
   <important-build-vars>`
   被
   适当
   设置，
   尽管
   这样。）

概览
********

Zephyr
的
构建
系统
基于
`CMake`_。

构建
系统
是
应用
中心
的，
并
要求
基于
Zephyr
的
应用
发起
构建
Zephyr
源
代码。
应用
构建
控制
应用
和
Zephyr
本身
两者
的
配置
和
构建
过程，
将
它们
编译
成
单个
二进制
文件。

主
zephyr
仓库
包含
Zephyr
的
源
代码、
配置
文件
和
构建
系统。
你
也
很可能
安装
了
各种
:ref:`模块`
与
zephyr
仓库
一起，
它们
提供
第三方
源
代码
集成。

**应用
目录**
中
的
文件
将
Zephyr
和
任何
模块
与
应用
链接。
这个
目录
包含
所有
应用
特定
文件，
如
应用
特定
配置
文件
和
源
代码。

这里
是
简单
Zephyr
应用
中
的
文件：

.. code-block:: none

   <app>
   ├──
   CMakeLists.txt
   ├──
   app.overlay
   ├──
   prj.conf
   ├──
   VERSION
   └──
   src
       └──
       main.c

这些
内容
是：

* **CMakeLists.txt**：
  这个
  文件
  告诉
  构建
  系统
  哪里
  找到
  其他
  应用
  文件，
  并
  将
  应用
  目录
  与
  Zephyr
  的
  CMake
  构建
  系统
  链接。
  这个
  链接
  提供
  Zephyr
  构建
  系统
  支持
  的
  功能，
  如
  开发板
  特定
  配置
  文件、
  在
  真实
  或
  仿真
  硬件
  上
  运行
  和
  调试
  编译
  后
  二进制
  文件
  的
  能力
  等。

* **app.overlay**：
  这
  是
  一个
  设备树
  覆盖
  文件，
  指定
  应该
  应用
  到
  你
  构建
  目标
  的
  任何
  开发板
  基础
  设备树
  的
  应用
  特定
  更改。
  设备树
  覆盖
  的
  目的
  通常
  是
  配置
  应用
  使用
  的
  硬件
  的
  某些
  东西。

  构建
  系统
  默认
  查找
  :file:`app.overlay`，
  但
  你
  可以
  添加
  更多
  设备树
  覆盖，
  其他
  默认
  文件
  也
  被
  搜索。

  关于
  设备树
  的
  更多
  信息
  见
  :ref:`devicetree`。

* **prj.conf**：
  这
  是
  一个
  Kconfig
  片段，
  指定
  一个
  或多个
  Kconfig
  选项
  的
  应用
  特定
  值。
  这些
  应用
  设置
  与
  其他
  设置
  合并
  以
  产生
  最终
  配置。
  Kconfig
  片段
  的
  目的
  通常
  是
  配置
  应用
  使用
  的
  软件
  功能。

  构建
  系统
  默认
  查找
  :file:`prj.conf`，
  但
  你
  可以
  添加
  更多
  Kconfig
  片段，
  其他
  默认
  文件
  也
  被
  搜索。

  关于
  这个
  文件
  和
  如何
  使用
  它
  的
  更多
  信息
  见
  :ref:`app-version-details`。

* **VERSION**：
  一个
  包含
  几个
  版本
  信息
  字段
  的
  文本
  文件。
  这些
  字段
  让
  你
  管理
  应用
  的
  生命周期
  并
  在
  签名
  应用
  镜像
  时
  自动
  提供
  应用
  版本。

  关于
  这个
  文件
  和
  如何
  使用
  它
  的
  更多
  信息
  见
  :ref:`app-version-details`。

* **main.c**：
  一个
  源
  代码
  文件。
  应用
  通常
  包含
  用
  C、
  C++
  或
  汇编
  语言
  编写
  的
  源
  文件。
  Zephyr
  约定
  是
  将
  它们
  放
  在
  :file:`<app>`
  中
  名为
  :file:`src`
  的
  子
  目录
  中。

一旦
应用
被
定义，
构建
系统
就
可以
构建
它。
应用
构建
控制
应用
和
Zephyr
本身
两者
的
配置
和
构建
过程。

构建
应用
****************

构建
应用
的
首选
方式
是
使用
:ref:`west
build
<west-building>`
命令。
它
接受
开发板
名称
和
应用
目录
作为
参数：

.. code-block:: console

   west
   build
   -b
   <board>
   <app>

构建
系统
将
应用
配置
与
Zephyr
配置
合并
并
构建
所有
源
代码
成
单个
二进制
文件。

构建
过程
产生
几个
输出
文件
在
构建
目录
中：

.. code-block:: none

   <app>/build
   ├──
   zephyr
   │   ├──
   │   zephyr.elf
   │   ├──
   │   zephyr.bin
   │   ├──
   │   zephyr.hex
   │   └──
   │   zephyr.map
   └──
   ...

.. _application-kconfig:

Kconfig
配置
****************

应用
可以
有
一个
或多个
Kconfig
片段
文件
来
配置
Zephyr
的
软件
功能。
默认
的
Kconfig
片段
文件
是
:file:`prj.conf`。

Kconfig
片段
是
普通
文本
文件，
包含
一个
或多个
Kconfig
选项
赋值。
每个
赋值
是
一行，
格式
为：

.. code-block:: cfg

   CONFIG_<option
   name>=<value>

例如，
启用
日志
的
Kconfig
片段
可能
像
这样：

.. code-block:: cfg

   CONFIG_LOG=y
   CONFIG_LOG_DEFAULT_LEVEL=3

构建
系统
将
应用
Kconfig
片段
与
开发板
默认
配置
和
其他
设置
合并
以
产生
最终
Kconfig
配置。
最终
配置
保存
到
构建
目录
中
的
:file:`zephyr/.config`
文件。

可以
用
``west
build
--
-DCONF_FILE=<file>``
指定
额外
的
Kconfig
片段
文件。

.. _application-devicetree:

设备树
配置
****************

应用
可以
有
一个
或多个
设备树
覆盖
文件
来
配置
硬件。
默认
的
设备树
覆盖
文件
是
:file:`app.overlay`。

设备树
覆盖
是
普通
文本
文件，
包含
一个
或多个
设备树
节点
或
属性
赋值。
构建
系统
将
应用
设备树
覆盖
与
开发板
基础
设备树
合并
以
产生
最终
设备树。

可以
用
``west
build
--
-DEXTRA_DTC_OVERLAY_FILE=<file>``
指定
额外
的
设备树
覆盖
文件。

设备树
源
通过
C
预
处理器
传递，
因此
你
可以
包含
可以
位于
``DTS_ROOT``
目录
中
的
文件。
按
约定
设备树
包含
文件
有
``.dtsi``
扩展名。

你
也
可以
用
预
处理器
控制
设备树
文件
的
内容，
通过
``DTS_EXTRA_CPPFLAGS``
CMake
Cache
变量
指定
指令：

.. zephyr-app-commands::
   :tool:
   all
   :board:
   <board
   name>
   :gen-args:
   -DDTS_EXTRA_CPPFLAGS=-DTEST_ENABLE_FEATURE
   :goals:
   build
   :compact:

.. _CMake:
   https://www.cmake.org
.. _CMake
   介绍:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html#description
.. _CMake
   列表:
   https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _示例
   应用:
   https://github.com/zephyrproject-rtos/example-application


.. note::

   以下为原文（待翻译）

      :tool: all
      :cd-into:
      :board: <board>
      :goals: build

   If desired, you can build the application using the configuration settings
   specified in an alternate :file:`.conf` file using the :code:`CONF_FILE`
   parameter. These settings will override the settings in the application's
   :file:`.config` file or its default :file:`.conf` file. For example:

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :gen-args: -DCONF_FILE=prj.alternate.conf
      :goals: build
      :compact:

   As described in the previous section, you can instead choose to permanently
   set the board and configuration settings by either exporting :makevar:`BOARD`
   and :makevar:`CONF_FILE` environment variables or by setting their values
   in your :file:`CMakeLists.txt` using ``set()`` statements.
   Additionally, ``west`` allows you to :ref:`set a default board
   <west-building-config>`.

.. _build-directory-contents:

Build Directory Contents
========================

When using the Ninja generator a build directory looks like this:

.. code-block:: none

   <app>/build
   ├── build.ninja
   ├── CMakeCache.txt
   ├── CMakeFiles
   ├── cmake_install.cmake
   ├── rules.ninja
   └── zephyr

The most notable files in the build directory are:

* :file:`build.ninja`, which can be invoked to build the application.

* A :file:`zephyr` directory, which is the working directory of the
  generated build system, and where most generated files are created and
  stored.

After running ``ninja``, the following build output files will be written to
the :file:`zephyr` sub-directory of the build directory. (This is **not the
Zephyr base directory**, which contains the Zephyr source code etc. and is
described above.)

* :file:`.config`, which contains the configuration settings
  used to build the application.

  .. note::

     The previous version of :file:`.config` is saved to :file:`.config.old`
     whenever the configuration is updated. This is for convenience, as
     comparing the old and new versions can be handy.

* Various object files (:file:`.o` files and :file:`.a` files) containing
  compiled kernel and application code.

* :file:`zephyr.elf`, which contains the final combined application and
  kernel binary. Other binary output formats, such as :file:`.hex` and
  :file:`.bin`, are also supported.

.. _application_rebuild:

Rebuilding an Application
=========================

Application development is usually fastest when changes are continually tested.
Frequently rebuilding your application makes debugging less painful
as the application becomes more complex. It's usually a good idea to
rebuild and test after any major changes to the application's source files,
CMakeLists.txt files, or configuration settings.

.. important::

    The Zephyr build system rebuilds only the parts of the application image
    potentially affected by the changes. Consequently, rebuilding an application
    is often significantly faster than building it the first time.

Sometimes the build system doesn't rebuild the application correctly
because it fails to recompile one or more necessary files. You can force
the build system to rebuild the entire application from scratch with the
following procedure:

#. Open a terminal console on your host computer, and navigate to the
   build directory :file:`<app>/build`.

#. Enter one of the following commands, depending on whether you want to use
   ``west`` or ``cmake`` directly to delete the application's generated
   files, except for the :file:`.config` file that contains the
   application's current configuration information.

   .. code-block:: console

       west build -t clean

   or

   .. code-block:: console

       ninja clean

   Alternatively, enter one of the following commands to delete *all*
   generated files, including the :file:`.config` files that contain
   the application's current configuration information for those board
   types.

   .. code-block:: console

       west build -t pristine

   or

   .. code-block:: console

       ninja pristine

   If you use west, you can take advantage of its capability to automatically
   :ref:`make the build folder pristine <west-building-config>` whenever it is
   required.

#. Rebuild the application normally following the steps specified
   in :ref:`build_an_application` above.

.. _application_board_version:

Building for a board revision
=============================

The Zephyr build system has support for specifying multiple hardware revisions
of a single board with small variations. Using revisions allows the board
support files to make minor adjustments to a board configuration without
duplicating all the files described in :ref:`create-your-board-directory` for
each revision.

To build for a particular revision, use ``<board>@<revision>`` or
``<board>@<revision>/<qualifiers>`` instead of plain ``<board>`` or
``<board>/<qualifiers>``. For example:

.. zephyr-app-commands::
   :tool: all
   :cd-into:
   :board: nrf9160dk@0.14.0/nrf9160/ns
   :goals: build
   :compact:

Check your board's documentation for details on whether it has multiple
revisions, and what revisions are supported.

When targeting a board revision, the active revision will be printed at CMake
configure time, like this:

.. code-block:: console

   -- Board: plank, Revision: 1.5.0

.. _application_run:

Run an Application
******************

An application image can be run on a real board or emulated hardware.

.. _application_run_board:

Running on a Board
==================

Most boards supported by Zephyr let you flash a compiled binary using
``west flash`` to copy the binary to the board and run it.
Follow these instructions to flash and run an application on real
hardware:

#. Build your application, as described in :ref:`build_an_application`.

#. Make sure your board is attached to your host computer. Usually, you'll do
   this via USB.

#. Run this console command from the build directory,
   :file:`<app>/build`, to flash the compiled Zephyr image and run it on
   your board:

   .. code-block:: console

      west flash

The Zephyr build system integrates with the board support files to
use hardware-specific tools to flash the Zephyr binary to your
hardware, then run it.

Each time you run the flash command, your application is rebuilt and flashed
again.

In cases where board support is incomplete, flashing via the Zephyr build
system may not be supported. If you receive an error message about flash
support being unavailable, consult :ref:`your board's documentation <boards>`
for additional information on how to flash your board.

.. note:: When developing on Linux, it's common to need to install
          board-specific udev rules to enable USB device access to
          your board as a non-root user. If flashing fails,
          consult your board's documentation to see if this is
          necessary.

.. _application_run_qemu:

Running in an Emulator
======================

Zephyr has built-in emulator support for QEMU.
It allows you to run and test an application virtually, before
(or in lieu of) loading and running it on actual target hardware.

Check out :ref:`beyond-GSG` for additional steps needed on Windows.

Follow these instructions to run an application via QEMU:

#. Build your application for one of the QEMU boards, as described in
   :ref:`build_an_application`.

   For example, you could set ``BOARD`` to:

   - ``qemu_x86`` to emulate running on an x86-based board
   - ``qemu_cortex_m3`` to emulate running on an ARM Cortex M3-based board

#. Run one of these console commands from the build directory,
   :file:`<app>/build`, to run the Zephyr binary in QEMU:

   .. code-block:: console

      west build -t run

   or

   .. code-block:: console

      ninja run

#. Press :kbd:`Ctrl A, X` to stop the application from running
   in QEMU.

   The application stops running and the terminal console prompt
   redisplays.

Each time you execute the run command, your application is rebuilt and run
again.


.. note::

   If the :ref:`Zephyr SDK <toolchain_zephyr_sdk>` is installed, the ``run``
   target will use the SDK's QEMU binary by default. To use another version of
   QEMU, :ref:`set the environment variable <env_vars>` ``QEMU_BIN_PATH``
   to the path of the QEMU binary you want to use instead.

.. note::

   You can choose a specific emulator by appending ``_<emulator>`` to your
   target name, for example ``west build -t run_qemu`` or ``ninja run_qemu``
   for QEMU.

.. _custom_board_definition:

Custom Board, Devicetree and SOC Definitions
********************************************

In cases where the board or platform you are developing for is not yet
supported by Zephyr, you can add board, Devicetree and SOC definitions
to your application without having to add them to the Zephyr tree.

The structure needed to support out-of-tree board and SOC development
is similar to how boards and SOCs are maintained in the Zephyr tree. By using
this structure, it will be much easier to upstream your platform related work into
the Zephyr tree after your initial development is done.

Add the custom board to your application or a dedicated repository using the
following structure:

.. code-block:: console

   boards/
   soc/
   CMakeLists.txt
   prj.conf
   README.rst
   src/

where the ``boards`` directory hosts the board you are building for:

.. code-block:: console

   .
   ├── boards
   │   └── vendor
   │       └── my_custom_board
   │           ├── doc
   │           │   └── img
   │           └── support
   └── src

and the ``soc`` directory hosts any SOC code. You can also have boards that are
supported by a SOC that is available in the Zephyr tree.

Boards
======

Use the vendor name as the folder name (which must match the vendor prefix in
:zephyr_file:`dts/bindings/vendor-prefixes.txt` if submitting upstream to Zephyr, or be
``others`` if it is not a vendor board) under ``boards`` for ``my_custom_board``.

Documentation (under ``doc/``) and support files (under ``support/``) are optional, but
will be needed when submitting to Zephyr.

The contents of ``my_custom_board`` should follow the same guidelines for any
Zephyr board, and provide the following files::

    board.yml
    my_custom_board_defconfig
    my_custom_board.dts
    my_custom_board.yaml
    board.cmake
    board.h
    CMakeLists.txt
    doc/
    Kconfig.my_custom_board
    Kconfig.defconfig
    support/


Once the board structure is in place, you can build your application
targeting this board by specifying the location of your custom board
information with the ``-DBOARD_ROOT`` parameter to the CMake
build system:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

This will use your custom board configuration and will generate the
Zephyr binary into your application directory.

You can also define the ``BOARD_ROOT`` variable in the application
:file:`CMakeLists.txt` file. Make sure to do so **before** pulling in the Zephyr
boilerplate with ``find_package(Zephyr ...)``.

.. note::

   When specifying ``BOARD_ROOT`` in a CMakeLists.txt, then an absolute path must
   be provided, for example ``list(APPEND BOARD_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-board-root>)``.
   When using ``-DBOARD_ROOT=<board-root>`` both absolute and relative paths can
   be used. Relative paths are treated relatively to the application directory.

.. note::

   When using sysbuild, then ``BOARD_ROOT`` must defined in a module or in the sysbuild
   ``CMakeLists.txt`` file, see :ref:`sysbuild_var_override` for details.

SOC Definitions
===============

Similar to board support, the structure is similar to how SOCs are maintained in
the Zephyr tree, for example:

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── common
                └── stm32l0x


The file :zephyr_file:`soc/Kconfig` will create the top-level
``SoC/CPU/Configuration Selection`` menu in Kconfig.

Out of tree SoC definitions can be added to this menu using the ``SOC_ROOT``
CMake variable. This variable contains a semicolon-separated list of directories
which contain SoC support files.

Following the structure above, the following files can be added to load
more SoCs into the menu.

.. code-block:: none

        soc
        └── st
            └── stm32
                └── stm32l0x
                    ├── Kconfig
                    ├── Kconfig.soc
                    └── Kconfig.defconfig

The Kconfig files above may describe the SoC or load additional SoC Kconfig files.

An example of loading ``stm32l0`` specific Kconfig files in this structure:

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── Kconfig.soc
                └── stm32l0x
                    └── Kconfig.soc

can be done with the following content in ``st/stm32/Kconfig.soc``:

.. code-block:: kconfig

   rsource "*/Kconfig.soc"

Once the SOC structure is in place, you can build your application
targeting this platform by specifying the location of your custom platform
information with the ``-DSOC_ROOT`` parameter to the CMake
build system:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DSOC_ROOT=<path to soc> -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

This will use your custom platform configurations and will generate the
Zephyr binary into your application directory.

See :ref:`modules_build_settings` for information on setting SOC_ROOT in a module's
:file:`zephyr/module.yml` file.

Or you can define the ``SOC_ROOT`` variable in the application
:file:`CMakeLists.txt` file. Make sure to do so **before** pulling in the
Zephyr boilerplate with ``find_package(Zephyr ...)``.

.. note::

   When specifying ``SOC_ROOT`` in a CMakeLists.txt, then an absolute path must
   be provided, for example ``list(APPEND SOC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-soc-root>``.
   When using ``-DSOC_ROOT=<soc-root>`` both absolute and relative paths can be
   used. Relative paths are treated relatively to the application directory.

.. _dts_root:

Devicetree Definitions
======================

Devicetree directory trees are found in ``APPLICATION_SOURCE_DIR``,
``BOARD_DIR``, and ``ZEPHYR_BASE``, but additional trees, or DTS_ROOTs,
can be added by creating this directory tree::

    include/
    dts/common/
    dts/arm/
    dts/
    dts/bindings/

Where 'arm' is changed to the appropriate architecture. Each directory
is optional. The binding directory contains bindings and the other
directories contain files that can be included from DT sources.

Once the directory structure is in place, you can use it by specifying
its location through the ``DTS_ROOT`` CMake Cache variable:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_ROOT=<path to dts root>
   :goals: build
   :compact:

You can also define the variable in the application :file:`CMakeLists.txt`
file. Make sure to do so **before** pulling in the Zephyr boilerplate with
``find_package(Zephyr ...)``.

.. note::

   When specifying ``DTS_ROOT`` in a CMakeLists.txt, then an absolute path must
   be provided, for example ``list(APPEND DTS_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-dts-root>``.
   When using ``-DDTS_ROOT=<dts-root>`` both absolute and relative paths can be
   used. Relative paths are treated relatively to the application directory.

Devicetree source are passed through the C preprocessor, so you can
include files that can be located in a ``DTS_ROOT`` directory.  By
convention devicetree include files have a ``.dtsi`` extension.

You can also use the preprocessor to control the content of a devicetree
file, by specifying directives through the ``DTS_EXTRA_CPPFLAGS`` CMake
Cache variable:

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_EXTRA_CPPFLAGS=-DTEST_ENABLE_FEATURE
   :goals: build
   :compact:

.. _CMake: https://www.cmake.org
.. _CMake introduction: https://cmake.org/cmake/help/latest/manual/cmake.1.html#description
.. _CMake list: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _example-application: https://github.com/zephyrproject-rtos/example-application
