.. _west-build-flash-debug:

构建、烧录与调试
################################

Zephyr 提供了多个 :ref:`West 扩展命令 <west-extensions>`，用于构建、烧录以及与运行在开发板上的 Zephyr 程序交互：``build``、``flash``、``debug``、``debugserver``、``rtt`` 和 ``attach``。

关于为烧录和调试命令添加开发板支持的信息，见板级移植指南中的 :ref:`flash-and-debug-support`。

.. Add a per-page contents at the top of the page. This page is nested
   deeply enough that it doesn't have any subheadings in the main nav.

.. only:: html

   .. contents::
      :local:

.. _west-building:

构建：``west build``
************************

.. tip:: 运行 ``west build -h`` 可快速了解概况。

``build`` 命令帮助你从源码构建 Zephyr 应用。你可以使用 :ref:`west config <west-config-cmd>` 配置其行为。

它的默认行为会尝试"做你想做的事"：

- 如果当前工作目录中存在名为 :file:`build` 的 Zephyr 构建目录，则会对其进行增量重编译。从 Zephyr 构建目录中运行 ``west build`` 时也是如此。

- 否则，如果你从 Zephyr 应用的源码目录运行 ``west build`` 且未找到构建目录，则会创建一个新的构建目录并在其中编译该应用。

基础用法
======

使用 ``west build`` 最简单的方法是进入应用的根目录（即包含应用 :file:`CMakeLists.txt` 的文件夹），然后运行::

  west build -b <BOARD>

其中 ``<BOARD>`` 是你想要构建的目标开发板名称。这与直接调用 CMake 时提供的名称完全相同：
``cmake -DBOARD=<BOARD>``。

.. tip::

   你可以使用 :ref:`west boards <west-boards>` 命令列出所有受支持的开发板。

将会创建一个名为 :file:`build` 的构建目录，``west build`` 运行 CMake 在该目录中生成构建系统后，应用将在其中编译。如果 ``west build`` 发现已存在构建目录，则在其中增量重编译应用，而不再次运行 CMake。你可以使用 ``--cmake`` 强制重新运行 CMake。

如果已有现成的构建目录，则无需使用 ``--board`` 选项；``west build`` 可以从 CMake 缓存中推断出开发板。对于新构建，会按顺序检查 ``--board`` 选项、:envvar:`BOARD` 环境变量或 ``build.board`` 配置选项。

.. _west-multi-domain-builds:

Sysbuild（多域构建）
==============================

:ref:`sysbuild` 可用于创建多域构建系统，将单个或多个开发板的多个镜像组合在一起。

使用 ``--sysbuild`` 在 ``west build`` 中选择 :ref:`sysbuild` 构建基础设施来构建多个域。

关于 sysbuild 用法的更详细信息，可参见 :ref:`sysbuild` 指南。

.. tip::

   可以启用 ``build.sysbuild`` 配置选项，使 ``west build`` 默认使用 sysbuild 构建。
   可以使用 ``--no-sysbuild`` 为某次特定构建禁用 sysbuild。

``west build`` 会通过 sysbuild 所指定各域的顶层构建文件夹构建所有域。

多域项目中的单个域可以通过 ``--domain`` 参数来构建。

示例
========

下面是一些 ``west build`` 的用法示例，按主题分组。

强制重新运行 CMake
--------------------------

要强制重新运行 CMake，使用 ``--cmake``（或 ``-c``）选项::

  west build -c

设置默认开发板
-----------------------

要配置 ``west build`` 默认构建 ``reel_board``::

  west config build.board reel_board

（这里可以使用 Zephyr 支持的任何其他开发板；不一定是 ``reel_board``。）

.. _west-building-dirs:

设置源码目录与构建目录
------------------------------------

要显式设置应用源码目录，将其路径作为位置参数提供::

  west build -b <BOARD> path/to/source/directory

要显式设置构建目录，使用 ``--build-dir``（或 ``-d``）::

  west build -b <BOARD> --build-dir path/to/build/directory

要将默认构建目录从 :file:`build` 改为其他名称，使用
``build.dir-fmt`` 配置选项。该选项允许使用格式字符串来命名构建
目录，例如::

  west config build.dir-fmt "build/{board}/{app}"

使用上述配置后，运行 ``west build -b reel_board samples/hello_world`` 将
使用构建目录 :file:`build/reel_board/hello_world`。关于该选项的更多细节，
见 :ref:`west-building-config`。

设置构建系统目标
-------------------------------

要指定要运行的构建系统目标，使用 ``--target``（或 ``-t``）。

例如，在带有 QEMU 的主机平台上，可以使用 ``run`` 目标
在一条命令中构建并运行 :zephyr:code-sample:`hello_world` 示例（针对模拟的
:zephyr:board:`qemu_x86 <qemu_x86>` 开发板）::

  west build -b qemu_x86 -t run samples/hello_world

另一个示例，使用 ``-t`` 列出所有构建系统目标::

  west build -t help

最后一个示例，使用 ``-t`` 运行 ``pristine`` 目标，该目标会删除
构建目录中的所有文件::

  west build -t pristine

.. _west-building-pristine:

Pristine（全新）构建
---------------

*pristine*（全新）构建目录本质上就是一个新的构建目录。
之前构建产生的所有中间产物都已被移除。

要强制 ``west build`` 在重新运行 CMake 生成构建系统之前
将构建目录变为 pristine，使用 ``--pristine=always``（或
``-p=always``）选项。

不带值地给出 ``--pristine`` 或 ``-p``，效果与给出值 ``always`` 相同。
例如，以下两条命令等价::

  west build -p -b reel_board samples/hello_world
  west build -p=always -b reel_board samples/hello_world

默认情况下，``west build`` 不会尝试判断构建目录
是否需要变为 pristine。如果你做了类似的事情——
比如试图复用某个构建目录来配合不同的 ``--board``——就可能导致错误。

使用 ``--pristine=auto`` 可使 ``west build`` 检测这些情况中的一部分，
并在尝试构建之前将构建目录变为 pristine。

.. tip::

   可以运行 ``west config build.pristine always`` 始终执行 pristine
   构建，或 ``west config build.pristine never`` 禁用该启发式判断。
   细节见 ``west build`` 的 :ref:`west-building-config`。

.. _west-building-verbose:

详细（Verbose）构建
------------------

要打印 ``west build`` 运行的 CMake 和编译器命令，使用 west 的全局
详细级别选项 ``-v``::

  west -v build -b reel_board samples/hello_world

.. _west-building-generator:
.. _west-building-cmake-args:

一次性 CMake 参数
------------------------

要向 ``west
build`` 执行的 CMake 调用传递额外参数，将它们放在命令行末尾的 ``--`` 之后。

.. important::

   像这样传递额外的 CMake 参数会强制 ``west build`` 重新运行
   CMake 构建配置步骤，即使构建系统已经生成。
   这会使增量构建变慢（但仍比从头构建快得多）。

   使用 ``--`` 生成构建目录一次之后，后续运行请使用 ``west build -d
   <build-dir>`` 做增量构建。

   或者，按下一节所述将 CMake 参数设为永久；
   这样不会拖慢增量构建。

例如，要使用 Unix Makefiles CMake 生成器而不是 Ninja（
``west build`` 的默认选择），运行::

  west build -b reel_board -- -G'Unix Makefiles'

要使用 Unix Makefiles 并将 `CMAKE_VERBOSE_MAKEFILE`_ 设为 ``ON``::

  west build -b reel_board -- -G'Unix Makefiles' -DCMAKE_VERBOSE_MAKEFILE=ON

注意 ``--`` 只出现一次，即使给出了多个 CMake 参数。
``west build`` 命令行中 ``--`` 之后的所有参数都会传给 CMake。

.. _west-building-dtc-overlay-file:

要将 :ref:`DTC_OVERLAY_FILE <important-build-vars>` 设为
:file:`enable-modem.overlay`，将该文件用作
:ref:`设备树 overlay <dt-guide>`::

  west build -b reel_board -- -DDTC_OVERLAY_FILE=enable-modem.overlay

要将 :file:`file.conf` Kconfig 片段合并到构建的
:file:`.config` 中::

  west build -- -DEXTRA_CONF_FILE=file.conf

.. _west-building-cmake-config:

永久 CMake 参数
-------------------------

上一节介绍的是为单次 ``west
build`` 命令添加 CMake 参数。如果想保存 CMake 参数供 ``west build``
每次生成新构建系统时使用，则应使用
``build.cmake-args`` 配置选项。每当 ``west build`` 运行 CMake
生成构建系统时，它会按 shell 规则拆分该选项的值，
并将结果包含在 ``cmake`` 命令行中。

请记住，默认情况下，如果构建目录中已存在构建系统，``west build`` **会尽量避免生成新的
构建系统**。因此，设置 ``build.cmake-args`` 之后，
你需要删除所有已存在的构建目录，或执行一次 :ref:`pristine 构建
<west-building-pristine>`，以确保该选项生效。

例如，要始终启用 :makevar:`CMAKE_EXPORT_COMPILE_COMMANDS`，可以
运行::

  west config build.cmake-args -- -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

（额外的 ``--`` 用于强制命令的其余部分被当作位置参数处理。
不加它的话，:ref:`west config <west-config-cmd>` 会把
``-DVAR=VAL`` 语法当作其 ``-D`` 选项的使用。）

要启用 :makevar:`CMAKE_VERBOSE_MAKEFILE`，使 CMake 始终生成详细的
构建系统::

  west config build.cmake-args -- -DCMAKE_VERBOSE_MAKEFILE=ON

要在 ``build.cmake-args`` 中保存多个参数，使用一个字符串，
其值可以拆分为不同的参数（``west build`` 内部使用
Python 函数 `shlex.split()`_ 拆分该值）。

.. _shlex.split(): https://docs.python.org/3/library/shlex.html#shlex.split

例如，要同时启用 :makevar:`CMAKE_EXPORT_COMPILE_COMMANDS` 和
:makevar:`CMAKE_VERBOSE_MAKEFILE`::

  west config build.cmake-args -- "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_VERBOSE_MAKEFILE=ON"

如果想把 CMake 参数保存在单独的文件中，可以把 CMake 的 ``-C <initial-cache>`` 选项与 ``build.cmake-args`` 组合。
例如，设置上一节示例所用选项的另一种方式是
创建一个名为 :file:`~/my-cache.cmake` 的文件，内容如下：

.. code-block:: cmake

   set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE BOOL "")
   set(CMAKE_VERBOSE_MAKEFILE ON CACHE BOOL "")

然后运行::

  west config build.cmake-args "-C ~/my-cache.cmake"

更多细节见 `cmake(1) 手册页`_ 和 `set() 命令`_ 文档。

.. _cmake(1) manual page:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _set() command:
   https://cmake.org/cmake/help/latest/command/set.html

构建工具参数
--------------------

使用 ``-o`` 向底层构建工具传递选项。

这对基于 ``ninja``（:ref:`默认 <west-building-generator>`）
和基于 ``make`` 的构建系统都适用。

例如，向 ``ninja`` 传递 ``-dexplain``::

  west build -o=-dexplain

另一个示例，向 ``make`` 传递 ``--keep-going``::

  west build -o=--keep-going

注意必须使用 ``-o=--foo`` 而不是 ``-o --foo``，
否则 ``--foo`` 会被当作 ``west build`` 的选项。

构建并行度
-----------------

默认情况下，``ninja`` 使用所有核心构建，而 ``make`` 只使用
一个。你可以用两个工具都支持的 ``-j`` 选项显式控制这一点。

例如，用 4 个核心构建::

  west build -o=-j4

``-o`` 选项在上一节有进一步说明。

构建单个域
---------------------

在 :zephyr:code-sample:`hello_world` 与 `MCUboot`_ 的多域构建中，可以使用
``--domain hello_world`` 只构建该域::

  west build --sysbuild --domain hello_world

``--domain`` 参数可以与 ``--target`` 参数组合，
为指定域构建特定目标，例如::

  west build --sysbuild --domain hello_world --target help

使用 snippet
-------------

见 :ref:`using-snippets`。

.. _west-building-config:

配置选项
=====================

你可以使用这些选项 :ref:`配置 <west-config-cmd>` ``west build``。

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - ``build.board``
     - 字符串。若给出，当未提供 ``--board`` 且环境中
       未设置 ``BOARD`` 时，:ref:`west build
       <west-building>` 使用该开发板。
   * - ``build.board_warn``
     - 布尔值，默认 ``true``。若为 ``false``，当
       ``west build`` 无法确定目标开发板时禁用警告。
   * - ``build.cmake-args``
     - 字符串。若存在，其值将按 shell 规则拆分，
       并在每次生成新构建系统时传给 CMake。见
       :ref:`west-building-cmake-config`。
   * - ``build.dir-fmt``
     - 字符串，默认 ``build``。构建文件夹格式字符串，
       west 在需要创建或定位构建文件夹时使用。
       当前可用的参数有：

         - ``west_topdir``：west 工作区的绝对路径，
           即 ``west_topdir`` 命令的返回值
         - ``board``：开发板名称
         - ``source_dir``：相对于当前工作目录的
           CMake 源码目录路径。如果当前工作目录
           位于源码目录内部，则为空字符串（
           在 Windows 上，位于另一驱动器上的源码目录
           相对当前目录无路径时也是如此）。如果未
           指定源码目录，则默认为当前工作目录。
           例如，从 ``<west_topdir>/app1`` 运行 ``west build ../app`` 时，
           ``source_dir`` 解析为 ``../app``（即
           相对于当前工作目录的路径）。
         - ``source_dir_workspace``：相对于
           ``west_topdir`` 的源码目录路径（如果位于工作区内部）。
           否则，相对于文件系统根目录（Unix 上为 ``/``，
           Windows 上为 ``C:/``）。
           例如，从 ``<west_topdir>/app1`` 运行 ``west build ../app`` 时，
           ``source_dir`` 解析为 ``app``（即
           相对于 west 工作区目录的路径）。
         - ``app``：源码目录的名称。
   * - ``build.generator``
     - 字符串，默认 ``Ninja``。用于创建
       构建系统的 `CMake 生成器`_。（为单次构建设置生成器，
       见 :ref:`上面的示例 <west-building-generator>`）
   * - ``build.guess-dir``
     - 字符串，指示 west 在使用 ``build.dir-fmt`` 且信息不足以
       解析构建文件夹名称时，是否尝试猜测要使用的构建文件夹。
       可取以下值：

         - ``never``（默认）：从不尝试猜测，而是退出并要求
           用户通过 ``-d`` 提供构建文件夹。
         - ``runners``：使用任何 "runner" 命令时尝试猜测
           文件夹。这些通常是所有调用外部工具的命令，
           如 ``flash`` 和 ``debug``。
   * - ``build.pristine``
     - 字符串。控制 ``west build`` 在构建前
       清理构建文件夹的方式。可取以下值：

         - ``never``（默认）：从不自动将构建文件夹
           变为 pristine。
         - ``auto``：如果存在构建系统且否则构建
           会失败（例如用户指定的开发板或应用
           与之前用于创建构建目录的不同），
           ``west build`` 会在构建前自动将构建文件夹
           变为 pristine。
         - ``always``：如果存在构建系统，
           构建前始终将构建文件夹变为 pristine。
   * - ``build.sysbuild``
     - 布尔值，默认 ``false``。若为 ``true``，
       使用 sysbuild 基础设施构建应用。

.. _west-flashing:

烧录：``west flash``
************************

.. tip:: 运行 ``west flash -h`` 获取额外帮助。

基础用法
======

从 Zephyr 构建目录中，重新构建二进制文件并烧录到
你的开发板::

  west flash

要指定构建目录，使用 ``--build-dir``（或 ``-d``）::

  west flash --build-dir path/to/build/directory

如果不指定构建目录，``west flash`` 会先在
:file:`build` 中查找，然后查找当前工作目录。如果你设置了
``build.dir-fmt`` 配置选项（见 :ref:`west-building-dirs`），``west
flash`` 会在那里查找而不是 :file:`build`。

选择 Runner
================

如果你的开发板的 Zephyr 集成支持多种程序
进行烧录，可以使用 ``--runner``（或
``-r``）选项指定使用哪一种。例如，如果 West 默认
使用 ``nrfjprog`` 烧录你的开发板，但同时也支持 JLink，
你可以用以下命令覆盖默认设置::

  west flash --runner jlink

你可以在构建时通过 CMake 变量 ``BOARD_FLASH_RUNNER``
覆盖默认烧录 runner，通过 ``BOARD_DEBUG_RUNNER``
覆盖调试 runner。

例如::

  # 将默认 runner 设为 "jlink"，覆盖开发板的
  # 通常默认值。
  west build [...] -- -DBOARD_FLASH_RUNNER=jlink

关于设置 CMake 参数的更多信息，
见 :ref:`west-building-cmake-args` 和 :ref:`west-building-cmake-config`。

关于 West 使用的 ``runner`` 库的更多信息，
见下文 :ref:`west-runner`。支持烧录的 runner 列表
可通过 ``west flash -H`` 获取；如果从构建目录运行
或使用 ``--build-dir``，会打印关于你的开发板可用
runner 的额外信息。

配置覆盖
======================

CMake 缓存包含 West 烧录时使用的默认值，例如
开发板目录在文件系统上的位置、要烧录的
zephyr 二进制文件（多种格式）的路径等。你可以在
运行时通过额外选项覆盖其中任何配置。

例如，要覆盖要烧录的（包含 Zephyr 镜像的）HEX 文件
（假设你的 runner 期望 HEX 文件），但保持其他
烧录配置为默认值::

  west flash --hex-file path/to/some/other.hex

``west flash -h`` 的输出包含所有 runner 支持的
覆盖选项的完整列表。

Runner 专属覆盖
=========================

每个 runner 可能支持额外的与烧录相关的选项。
例如，某些 runner 支持 ``--erase`` 标志，
在烧录 Zephyr 镜像之前对开发板上的 flash 存储
进行整片擦除。

要查看你的开发板支持的 runner 的所有可用选项
及其用法信息，使用 ``--context``（或
``-H``）::

  west flash --context

.. important::

   注意短选项名中的大写 H。这会重新运行构建，
   以确保显示的信息是最新的！

在构建目录之外运行 West 时，``west flash -H`` 只
打印 runner 列表。你可以使用 ``west flash -H -r
<runner-name>`` 打印某个 runner 支持的选项的用法信息。

例如，打印 ``jlink`` runner 的用法信息::

  west flash -H -r jlink

.. _west-multi-domain-flashing:

多域烧录
=====================

当检测到 :ref:`west-multi-domain-builds` 文件夹时，``west flash``
会按 sysbuild 定义的顺序烧录所有域。

多域项目中的单个域镜像可以通过 ``--domain`` 来烧录。

例如，在 :zephyr:code-sample:`hello_world` 与
`MCUboot`_ 的多域构建中，可以使用 ``--domain hello_world`` 只烧录
该域的镜像::

  west flash --domain hello_world

.. _west-debugging:

配置选项
=====================

你可以使用这些选项 :ref:`配置 <west-config-cmd>` ``west flash``。

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - ``flash.rebuild``
     - 布尔值，默认 ``true``。若为 ``false``，west flash 时不重新构建。

调试：``west debug``、``west debugserver``
***********************************************

.. tip::

   运行 ``west debug -h`` 或 ``west debugserver -h`` 获取额外帮助。

基础用法
======

从 Zephyr 构建目录中，为开发板附加调试器并
打开调试控制台（例如 GDB 会话）::

  west debug

为开发板附加调试器并打开一个本地网络端口，
供调试器连接（例如 IDE 调试器）::

  west debugserver

要指定构建目录，使用 ``--build-dir``（或 ``-d``）::

  west debug --build-dir path/to/build/directory
  west debugserver --build-dir path/to/build/directory

如果不指定构建目录，这些命令会先在
:file:`build` 中查找，然后查找当前工作目录。如果你设置了
``build.dir-fmt`` 配置选项（见 :ref:`west-building-dirs`），``west
debug`` 会在那里查找而不是 :file:`build`。

选择 Runner
================

如果你的开发板的 Zephyr 集成支持多种程序
进行调试，可以使用 ``--runner``（或
``-r``）选项指定使用哪一种。例如，如果 West 默认
使用 ``pyocd-gdbserver`` 调试你的开发板，但同时也支持 JLink，
你可以用以下命令覆盖默认设置::

  west debug --runner jlink
  west debugserver --runner jlink

关于 West 使用的 ``runner`` 库的更多信息，
见下文 :ref:`west-runner`。支持调试的 runner 列表
可通过 ``west debug -H`` 获取；如果从构建目录运行
或使用 ``--build-dir``，会打印关于你的开发板可用
runner 的额外信息。

配置覆盖
======================

CMake 缓存包含 West 调试时使用的默认值，例如
开发板目录在文件系统上的位置、包含符号表的
zephyr 二进制文件的路径等。你可以在
运行时通过额外选项覆盖其中任何配置。

例如，要覆盖包含 Zephyr 二进制文件和
符号表的 ELF 文件（假设你的 runner 期望 ELF 文件），但保持
其他调试配置为默认值::

  west debug --elf-file path/to/some/other.elf
  west debugserver --elf-file path/to/some/other.elf

``west debug -h`` 的输出包含所有 runner 支持的
覆盖选项的完整列表。

Runner 专属覆盖
=========================

每个 runner 可能支持额外的与调试相关的选项。
例如，某些 runner 支持用于设置调试服务器
所用网络端口的标志。

要查看你的开发板支持的 runner 的所有可用选项
及其用法信息，使用 ``--context``（或
``-H``）::

  west debug --context

（命令 ``west debugserver --context`` 会打印相同的输出。）

.. important::

   注意短选项名中的大写 H。这会重新运行构建，
   以确保显示的信息是最新的！

在构建目录之外运行 West 时，``west debug -H`` 只
打印 runner 列表。你可以使用 ``west debug -H -r
<runner-name>`` 打印某个 runner 支持的选项的用法信息。

例如，打印 ``jlink`` runner 的用法信息::

  west debug -H -r jlink

.. _west-multi-domain-debugging:

多域调试
=====================

``west debug`` 一次只能调试单个域。当检测到
:ref:`west-multi-domain-builds` 文件夹时，``west debug``
会调试 sysbuild 指定的 ``default`` 域。

默认域就是作为源码目录给出的应用。
见以下示例::

  west build --sysbuild path/to/source/directory

例如，使用 sysbuild 构建 ``hello_world`` 与 `MCUboot`_ 时，
``hello_world`` 成为默认域::

  west build --sysbuild samples/hello_world

因此要调试 ``hello_world``，可以执行::

  west debug

或::

  west debug --domain hello_world

如果要调试 MCUboot，必须显式指定 MCUboot 为要调试的域::

  west debug --domain mcuboot

.. _west-runner:

配置选项
=====================

你可以使用这些选项 :ref:`配置 <west-config-cmd>` ``west debug``，
以及 :ref:`配置 <west-config-cmd>` ``west debugserver``。

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - ``debug.rebuild``
     - 布尔值，默认 ``true``。若为 ``false``，west debug 时不重新构建。
   * - ``debugserver.rebuild``
     - 布尔值，默认 ``true``。若为 ``false``，west debugserver 时不重新构建。

烧录与调试 runner
***********************

烧录和调试命令使用对各种
:ref:`flash-debug-host-tools` 的 Python 封装。这些封装全部定义在
:zephyr_file:`scripts/west_commands/runners` 处的一个 Python
库中。每个封装称为一个 *runner*。Runner 可以烧录和/或调试
Zephyr 程序。

该库中的核心抽象是 ``ZephyrBinaryRunner``，
一个表示 runner 的抽象类。可用 runner 的集合
由导入的 ``ZephyrBinaryRunner`` 子类决定。
``ZephyrBinaryRunner`` 位于 ``runners.core`` 模块中；
各个 runner 实现在其他子模块中，如 ``runners.nrfjprog``、
``runners.openocd`` 等。

运行 Robot Framework 测试：``west robot``
*********************************************

.. tip:: 运行 ``west robot -h`` 获取额外帮助。

基础用法
======

目前该命令只支持一个使用 ``renode-test`` 的 runner
（本质上是在 Renode 中运行 Robot 测试的封装），但可以通过
添加其他 runner 轻松扩展。

从 Zephyr 构建目录中，运行一个 Robot 测试套件::

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot

这将运行 testsuite.robot 中的所有测试，并打印
Robot Framework 提供的输出。

要向 Renode 传递额外参数，使用 ``--renode-robot-args`` 开关。
例如，要在 Robot Framework 输出之外显示 Renode 日志：

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot --renode-robot-arg="--show-log"

Runner 专属覆盖
=========================

要查看你的开发板支持的 Robot runner 的所有可用选项
及其用法信息，使用 ``--context``（或
``-H``）::

  west robot --runner=renode-robot --context


要查看 "renode-test" runner 支持的所有可用选项，使用::

  west robot --runner=renode-robot --renode-robot-help

模拟开发板：``west simulate``
******************************************

基础用法
======

目前该命令只支持一个使用 Renode 的 runner，
但可以通过添加其他 runner 轻松扩展。

从 Zephyr 构建目录中，运行已构建的二进制文件::

  west simulate --runner=renode

这将启动 Renode，并基于当前平台的默认 ``.resc`` 脚本
配置模拟（默认加载 zephyr.elf 文件）。之后可以在
Renode 的 Monitor 中输入 "start" 或 "s" 启动模拟。
也可以通过向 Renode 传递命令实现这一点，使用 runner 提供的参数：

  west simulate --runner=renode --renode-command start

要向 Renode 本身传递参数，例如以控制台模式
而不是独立窗口启动 Renode：

  west simulate --runner=renode --renode-arg="--console"

从这一点开始，Renode 可以在控制台和窗口模式下正常使用。
关于使用 Renode 的详情，见 `Renode - 文档`_。

.. _Renode - documentation:
   https://docs.renode.io

Runner 专属覆盖
=========================

要查看所有 runner 支持的所有可用选项
及其用法信息，使用 ``--context``（或 ``-H``）::

  west simulate --runner=renode --context

要查看 Renode 支持的所有可用选项，使用::

  west simulate --runner=renode --renode-help

树外（Out of tree）runner
*******************

:ref:`Zephyr 模块 <modules>` 可以通过在其
:ref:`module.yml <modules-runners>` 中添加 python
文件来被发现外部 runner。通过继承
``ZephyrBinaryRunner`` 并实现所有抽象方法来创建外部 runner 类。

.. note::

   对自定义树外 runner 的支持使 ``runners.core`` 模块成为
   公共 API 的一部分，不向后兼容的更改需要经历
   :ref:`弃用流程 <breaking_api_changes>`。

Hacking（二次开发）
*******

本节记录烧录和调试命令使用的 ``runners.core`` 模块。
这是实现这些功能支持所用的核心抽象。

开发者可以通过实现额外的 runner 来为 Zephyr 程序
添加新的烧录和调试方式。要让该支持进入上游 Zephyr，
应将该 runner 添加到新的或已有的 ``runners`` 模块中，
并从 :file:`runners/__init__.py` 导入。

.. note::

   :zephyr_file:`scripts/west_commands/tests` 中的测试用例
   为 runners 包和各个 runner 类添加单元测试
   覆盖。

   添加新 runner 时请尽量添加测试。注意如果
   你的更改破坏了现有测试用例，上游拉取请求的
   CI 测试将会失败。

.. automodule:: runners.core
   :members:

手动操作
****************

如果你不想使用 West 烧录或调试开发板，只需
检查构建目录中由构建系统输出的二进制文件。
这些文件通常命名为 ``zephyr/zephyr.elf``、
``zephyr/zephyr.hex`` 等，具体取决于你的开发板的构建系统
集成。这些二进制文件可以用你选择的替代工具
烧录到开发板，或按需用于调试，
例如作为符号表的来源。

默认情况下，这些 West 命令在烧录和调试前
会重新构建二进制文件。当然，这也可以通过
Zephyr 构建系统提供的常规目标实现（事实上，
这些命令就是这么做的）。

.. _cmake(1):
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _CMAKE_VERBOSE_MAKEFILE:
   https://cmake.org/cmake/help/latest/variable/CMAKE_VERBOSE_MAKEFILE.html

.. _CMake Generator:
   https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html

.. _MCUboot: https://mcuboot.com/
