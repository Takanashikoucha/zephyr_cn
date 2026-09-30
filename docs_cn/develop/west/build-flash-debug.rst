.. _west-build-flash-debug:

构建、
烧录
和
调试
################################

Zephyr
提供
多
个
:ref:`west
extension
commands
<west-extensions>`
用于
构建、
烧录
和
与
运行
在
board
上
的
Zephyr
程序
交互：
``build``、
``flash``、
``debug``、
``debugserver``、
``rtt``
和
``attach``。

对
添加
board
支持
给
烧录
和
调试
命令
的
信息，
参考
:ref:`flash-and-debug-support`
在
board
移植
指南
中。

.. Add
   a
   per-page
   contents
   at
   the
   top
   of
   the
   page.
   This
   page
   is
   nested
   deeply
   enough
   that
   it
   doesn't
   have
   any
   subheadings
   in
   the
   main
   nav.

.. only::
   html

   .. contents::
      :local:

.. _west-building:

构建：
``west
build``
************************

.. tip::
   运行
   ``west
   build
   -h``
   获取
   快速
   概览。

``build``
命令
帮助
你
从
源
构建
Zephyr
应用。
你
可以
用
:ref:`west
config
<west-config-cmd>`
配置
其
行为。

其
默认
行为
尝试
"做
你
意思
的"：

- 如果
  当前
  工作
  目录
  中
  有
  命名
  为
  :file:`build`
  的
  Zephyr
  构建
  目录，
  它
  被
  增量
  重新
  编译。
  如果
  你
  从
  Zephyr
  构建
  目录
  运行
  ``west
  build``
  同样
  为
  真。

- 否则，
  如果
  你
  从
  Zephyr
  应用
  的
  源
  目录
  运行
  ``west
  build``
  且
  没
  有
  找到
  构建
  目录，
  新
  的
  被
  创建
  且
  应用
  在
  它
  中
  被
  编译。


.. note::

   以下为原文（待翻译）


Verbose Builds
--------------

To print the CMake and compiler commands run by ``west build``, use the global
west verbosity option, ``-v``::

  west -v build -b reel_board samples/hello_world

.. _west-building-generator:
.. _west-building-cmake-args:

One-Time CMake Arguments
------------------------

To pass additional arguments to the CMake invocation performed by ``west
build``, pass them after a ``--`` at the end of the command line.

.. important::

   Passing additional CMake arguments like this forces ``west build`` to re-run
   the CMake build configuration step, even if a build system has already been
   generated.  This will make incremental builds slower (but still much faster
   than building from scratch).

   After using ``--`` once to generate the build directory, use ``west build -d
   <build-dir>`` on subsequent runs to do incremental builds.

   Alternatively, make your CMake arguments permanent as described in the next
   section; it will not slow down incremental builds.

For example, to use the Unix Makefiles CMake generator instead of Ninja (which
``west build`` uses by default), run::

  west build -b reel_board -- -G'Unix Makefiles'

To use Unix Makefiles and set `CMAKE_VERBOSE_MAKEFILE`_ to ``ON``::

  west build -b reel_board -- -G'Unix Makefiles' -DCMAKE_VERBOSE_MAKEFILE=ON

Notice how the ``--`` only appears once, even though multiple CMake arguments
are given. All command-line arguments to ``west build`` after a ``--`` are
passed to CMake.

.. _west-building-dtc-overlay-file:

To set :ref:`DTC_OVERLAY_FILE <important-build-vars>` to
:file:`enable-modem.overlay`, using that file as a
:ref:`devicetree overlay <dt-guide>`::

  west build -b reel_board -- -DDTC_OVERLAY_FILE=enable-modem.overlay

To merge the :file:`file.conf` Kconfig fragment into your build's
:file:`.config`::

  west build -- -DEXTRA_CONF_FILE=file.conf

.. _west-building-cmake-config:

Permanent CMake Arguments
-------------------------

The previous section describes how to add CMake arguments for a single ``west
build`` command. If you want to save CMake arguments for ``west build`` to use
every time it generates a new build system instead, you should use the
``build.cmake-args`` configuration option. Whenever ``west build`` runs CMake
to generate a build system, it splits this option's value according to shell
rules and includes the results in the ``cmake`` command line.

Remember that, by default, ``west build`` **tries to avoid generating a new
build system if one is present** in your build directory. Therefore, you need
to either delete any existing build directories or do a :ref:`pristine build
<west-building-pristine>` after setting ``build.cmake-args`` to make sure it
will take effect.

For example, to always enable :makevar:`CMAKE_EXPORT_COMPILE_COMMANDS`, you can
run::

  west config build.cmake-args -- -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

(The extra ``--`` is used to force the rest of the command to be treated as a
positional argument. Without it, :ref:`west config <west-config-cmd>` would
treat the ``-DVAR=VAL`` syntax as a use of its ``-D`` option.)

To enable :makevar:`CMAKE_VERBOSE_MAKEFILE`, so CMake always produces a verbose
build system::

  west config build.cmake-args -- -DCMAKE_VERBOSE_MAKEFILE=ON

To save more than one argument in ``build.cmake-args``, use a single string
whose value can be split into distinct arguments (``west build`` uses the
Python function `shlex.split()`_ internally to split the value).

.. _shlex.split(): https://docs.python.org/3/library/shlex.html#shlex.split

For example, to enable both :makevar:`CMAKE_EXPORT_COMPILE_COMMANDS` and
:makevar:`CMAKE_VERBOSE_MAKEFILE`::

  west config build.cmake-args -- "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_VERBOSE_MAKEFILE=ON"

If you want to save your CMake arguments in a separate file instead, you can
combine CMake's ``-C <initial-cache>`` option with ``build.cmake-args``. For
instance, another way to set the options used in the previous example is to
create a file named :file:`~/my-cache.cmake` with the following contents:

.. code-block:: cmake

   set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE BOOL "")
   set(CMAKE_VERBOSE_MAKEFILE ON CACHE BOOL "")

Then run::

  west config build.cmake-args "-C ~/my-cache.cmake"

See the `cmake(1) manual page`_ and the `set() command`_ documentation for
more details.

.. _cmake(1) manual page:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _set() command:
   https://cmake.org/cmake/help/latest/command/set.html

Build tool arguments
--------------------

Use ``-o`` to pass options to the underlying build tool.

This works with both ``ninja`` (:ref:`the default <west-building-generator>`)
and ``make`` based build systems.

For example, to pass ``-dexplain`` to ``ninja``::

  west build -o=-dexplain

As another example, to pass ``--keep-going`` to ``make``::

  west build -o=--keep-going

Note that using ``-o=--foo`` instead of ``-o --foo`` is required to prevent
``--foo`` from being treated as a ``west build`` option.

Build parallelism
-----------------

By default, ``ninja`` uses all of your cores to build, while ``make`` uses only
one. You can control this explicitly with the ``-j`` option supported by both
tools.

For example, to build with 4 cores::

  west build -o=-j4

The ``-o`` option is described further in the previous section.

Build a single domain
---------------------

In a multi-domain build with :zephyr:code-sample:`hello_world` and `MCUboot`_, you can use
``--domain hello_world`` to only build this domain::

  west build --sysbuild --domain hello_world

The ``--domain`` argument can be combined with the ``--target`` argument to
build the specific target for the target, for example::

  west build --sysbuild --domain hello_world --target help

Use a snippet
-------------

See :ref:`using-snippets`.

.. _west-building-config:

Configuration Options
=====================

You can :ref:`configure <west-config-cmd>` ``west build`` using these options.

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - Option
     - Description
   * - ``build.board``
     - String. If given, this the board used by :ref:`west build
       <west-building>` when ``--board`` is not given and ``BOARD``
       is unset in the environment.
   * - ``build.board_warn``
     - Boolean, default ``true``. If ``false``, disables warnings when
       ``west build`` can't figure out the target board.
   * - ``build.cmake-args``
     - String. If present, the value will be split according to shell rules and
       passed to CMake whenever a new build system is generated. See
       :ref:`west-building-cmake-config`.
   * - ``build.dir-fmt``
     - String, default ``build``. The build folder format string, used by
       west whenever it needs to create or locate a build folder. The currently
       available arguments are:

         - ``west_topdir``: The absolute path to the west workspace, as
           returned by the ``west_topdir`` command
         - ``board``: The board name
         - ``source_dir``: Path to the CMake source directory, relative to the
           current working directory. If the current working directory is
           inside the source directory, this is an empty string, as it is on
           Windows for a source directory on another drive, which has no
           relative path to the current one. If no source directory is
           specified, it defaults to current working directory.
           E.g. if ``west build ../app`` is run from ``<west_topdir>/app1``,
           ``source_dir`` resolves to ``../app`` (which is the relative path
           to the current working dir).
         - ``source_dir_workspace``: Path to the source directory, relative to
           ``west_topdir`` (if it is inside the workspace). Otherwise, it is
           relative to the filesystem root (``/`` on Unix, respectively
           ``C:/`` on Windows).
           E.g. if ``west build ../app`` is run from ``<west_topdir>/app1``,
           ``source_dir`` resolves to ``app`` (which is the relative path to
           the west workspace dir).
         - ``app``: The name of the source directory.
   * - ``build.generator``
     - String, default ``Ninja``. The `CMake Generator`_ to use to create a
       build system. (To set a generator for a single build, see the
       :ref:`above example <west-building-generator>`)
   * - ``build.guess-dir``
     - String, instructs west whether to try to guess what build folder to use
       when ``build.dir-fmt`` is in use and not enough information is available
       to resolve the build folder name. Can take these values:

         - ``never`` (default): Never try to guess, bail out instead and
           require the user to provide a build folder with ``-d``.
         - ``runners``: Try to guess the folder when using any of the 'runner'
           commands.  These are typically all commands that invoke an external
           tool, such as ``flash`` and ``debug``.
   * - ``build.pristine``
     - String. Controls the way in which ``west build`` may clean the build
       folder before building. Can take the following values:

         - ``never`` (default): Never automatically make the build folder
           pristine.
         - ``auto``:  ``west build`` will automatically make the build folder
           pristine before building, if a build system is present and the build
           would fail otherwise (e.g. the user has specified a different board
           or application from the one previously used to make the build
           directory).
         - ``always``: Always make the build folder pristine before building, if
           a build system is present.
   * - ``build.sysbuild``
     - Boolean, default ``false``. If ``true``, build application using the
       sysbuild infrastructure.

.. _west-flashing:

Flashing: ``west flash``
************************

.. tip:: Run ``west flash -h`` for additional help.

Basics
======

From a Zephyr build directory, re-build the binary and flash it to
your board::

  west flash

To specify the build directory, use ``--build-dir`` (or ``-d``)::

  west flash --build-dir path/to/build/directory

If you don't specify the build directory, ``west flash`` searches for one in
:file:`build`, then the current working directory. If you set the
``build.dir-fmt`` configuration option (see :ref:`west-building-dirs`), ``west
flash`` searches there instead of :file:`build`.

Choosing a Runner
=================

If your board's Zephyr integration supports flashing with multiple
programs, you can specify which one to use using the ``--runner`` (or
``-r``) option. For example, if West flashes your board with
``nrfjprog`` by default, but it also supports JLink, you can override
the default with::

  west flash --runner jlink

You can override the default flash runner at build time by using the
``BOARD_FLASH_RUNNER`` CMake variable, and the debug runner with
``BOARD_DEBUG_RUNNER``.

For example::

  # Set the default runner to "jlink", overriding the board's
  # usual default.
  west build [...] -- -DBOARD_FLASH_RUNNER=jlink

See :ref:`west-building-cmake-args` and :ref:`west-building-cmake-config` for
more information on setting CMake arguments.

See :ref:`west-runner` below for more information on the ``runner``
library used by West. The list of runners which support flashing can
be obtained with ``west flash -H``; if run from a build directory or
with ``--build-dir``, this will print additional information on
available runners for your board.

Configuration Overrides
=======================

The CMake cache contains default values West uses while flashing, such
as where the board directory is on the file system, the path to the
zephyr binaries to flash in several formats, and more. You can
override any of this configuration at runtime with additional options.

For example, to override the HEX file containing the Zephyr image to
flash (assuming your runner expects a HEX file), but keep other
flash configuration at default values::

  west flash --hex-file path/to/some/other.hex

The ``west flash -h`` output includes a complete list of overrides
supported by all runners.

Runner-Specific Overrides
=========================

Each runner may support additional options related to flashing. For
example, some runners support an ``--erase`` flag, which mass-erases
the flash storage on your board before flashing the Zephyr image.

To view all of the available options for the runners your board
supports, as well as their usage information, use ``--context`` (or
``-H``)::

  west flash --context

.. important::

   Note the capital H in the short option name. This re-runs the build
   in order to ensure the information displayed is up to date!

When running West outside of a build directory, ``west flash -H`` just
prints a list of runners. You can use ``west flash -H -r
<runner-name>`` to print usage information for options supported by
that runner.

For example, to print usage information about the ``jlink`` runner::

  west flash -H -r jlink

.. _west-multi-domain-flashing:

Multi-domain flashing
=====================

When a :ref:`west-multi-domain-builds` folder is detected, then ``west flash``
will flash all domains in the order defined by sysbuild.

It is possible to flash the image from a single domain in a multi-domain project
by using ``--domain``.

For example, in a multi-domain build with :zephyr:code-sample:`hello_world` and
`MCUboot`_, you can use the ``--domain hello_world`` domain to only flash
only the image from this domain::

  west flash --domain hello_world

.. _west-debugging:

Configuration Options
=====================

You can :ref:`configure <west-config-cmd>` ``west flash`` using these options.

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - Option
     - Description
   * - ``flash.rebuild``
     - Boolean, default ``true``. If ``false``, do not rebuild on west flash.

Debugging: ``west debug``, ``west debugserver``
***********************************************

.. tip::

   Run ``west debug -h`` or ``west debugserver -h`` for additional help.

Basics
======

From a Zephyr build directory, to attach a debugger to your board and
open up a debug console (e.g. a GDB session)::

  west debug

To attach a debugger to your board and open up a local network port
you can connect a debugger to (e.g. an IDE debugger)::

  west debugserver

To specify the build directory, use ``--build-dir`` (or ``-d``)::

  west debug --build-dir path/to/build/directory
  west debugserver --build-dir path/to/build/directory

If you don't specify the build directory, these commands search for one in
:file:`build`, then the current working directory. If you set the
``build.dir-fmt`` configuration option (see :ref:`west-building-dirs`), ``west
debug`` searches there instead of :file:`build`.

Choosing a Runner
=================

If your board's Zephyr integration supports debugging with multiple
programs, you can specify which one to use using the ``--runner`` (or
``-r``) option. For example, if West debugs your board with
``pyocd-gdbserver`` by default, but it also supports JLink, you can
override the default with::

  west debug --runner jlink
  west debugserver --runner jlink

See :ref:`west-runner` below for more information on the ``runner``
library used by West. The list of runners which support debugging can
be obtained with ``west debug -H``; if run from a build directory or
with ``--build-dir``, this will print additional information on
available runners for your board.

Configuration Overrides
=======================

The CMake cache contains default values West uses for debugging, such
as where the board directory is on the file system, the path to the
zephyr binaries containing symbol tables, and more. You can override
any of this configuration at runtime with additional options.

For example, to override the ELF file containing the Zephyr binary and
symbol tables (assuming your runner expects an ELF file), but keep
other debug configuration at default values::

  west debug --elf-file path/to/some/other.elf
  west debugserver --elf-file path/to/some/other.elf

The ``west debug -h`` output includes a complete list of overrides
supported by all runners.

Runner-Specific Overrides
=========================

Each runner may support additional options related to debugging. For
example, some runners support flags which allow you to set the network
ports used by debug servers.

To view all of the available options for the runners your board
supports, as well as their usage information, use ``--context`` (or
``-H``)::

  west debug --context

(The command ``west debugserver --context`` will print the same output.)

.. important::

   Note the capital H in the short option name. This re-runs the build
   in order to ensure the information displayed is up to date!

When running West outside of a build directory, ``west debug -H`` just
prints a list of runners. You can use ``west debug -H -r
<runner-name>`` to print usage information for options supported by
that runner.

For example, to print usage information about the ``jlink`` runner::

  west debug -H -r jlink

.. _west-multi-domain-debugging:

Multi-domain debugging
======================

``west debug`` can only debug a single domain at a time. When a
:ref:`west-multi-domain-builds` folder is detected, ``west debug``
will debug the ``default`` domain specified by sysbuild.

The default domain will be the application given as the source directory.
See the following example::

  west build --sysbuild path/to/source/directory

For example, when building ``hello_world`` with `MCUboot`_ using sysbuild,
``hello_world`` becomes the default domain::

  west build --sysbuild samples/hello_world

So to debug ``hello_world`` you can do::

  west debug

or::

  west debug --domain hello_world

If you wish to debug MCUboot, you must explicitly specify MCUboot as the domain
to debug::

  west debug --domain mcuboot

.. _west-runner:

Configuration Options
=====================

You can :ref:`configure <west-config-cmd>` ``west debug`` and
:ref:`configure <west-config-cmd>` ``west debugserver`` using these options.

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - Option
     - Description
   * - ``debug.rebuild``
     - Boolean, default ``true``. If ``false``, do not rebuild on west debug.
   * - ``debugserver.rebuild``
     - Boolean, default ``true``. If ``false``, do not rebuild on west debugserver.

Flash and debug runners
***********************

The flash and debug commands use Python wrappers around various
:ref:`flash-debug-host-tools`. These wrappers are all defined in a Python
library at :zephyr_file:`scripts/west_commands/runners`. Each wrapper is
called a *runner*. Runners can flash and/or debug Zephyr programs.

The central abstraction within this library is ``ZephyrBinaryRunner``, an
abstract class which represents runners. The set of available runners is
determined by the imported subclasses of ``ZephyrBinaryRunner``.
``ZephyrBinaryRunner`` is available in the ``runners.core`` module; individual
runner implementations are in other submodules, such as ``runners.nrfjprog``,
``runners.openocd``, etc.

Running Robot Framework tests: ``west robot``
*********************************************

.. tip:: Run ``west robot -h`` for additional help.

Basics
======

Currently the command supports only one runner which is using ``renode-test``,
(essentially a wrapper for running Robot tests in Renode), but can be
easily extended by adding other runners.

From a Zephyr build directory, to run a Robot test suite::

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot

This will run all tests from testsuite.robot and print output provided
by Robot Framework.

To pass additional parameters to Renode use ``--renode-robot-args`` switch.
For example to show Renode logs in addition to Robot Framework's output:

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot --renode-robot-arg="--show-log"

Runner-Specific Overrides
=========================

To view all of the available options for the Robot runners your board
supports, as well as their usage information, use ``--context`` (or
``-H``)::

  west robot --runner=renode-robot --context


To view all available options "renode-test" runner supports, use::

  west robot --runner=renode-robot --renode-robot-help

Simulating a board with: ``west simulate``
******************************************

Basics
======

Currently the command supports only one runner which is using Renode,
but can be easily extended by adding other runners.

From a Zephyr build directory, to run the built binary::

  west simulate --runner=renode

This will start Renode and configure simulation based on a default ``.resc`` script
for the current platform with the zephyr.elf file loaded by default. The simulation
then can be started by typing "start" or "s" in Renode's Monitor. This can also be
done by passing a command to Renode, using an argument provided by the runner:

  west simulate --runner=renode --renode-command start

To pass an argument to Renode itself, for example to start Renode in console mode
instead of a separate window:

  west simulate --runner=renode --renode-arg="--console"

From that point on Renode can be used normally in both console and window modes.
For details on using Renode see `Renode - documentation`_.

.. _Renode - documentation:
   https://docs.renode.io

Runner-Specific Overrides
=========================

To view all of the available options supported by the runners, as well
as their usage information, use ``--context`` (or ``-H``)::

  west simulate --runner=renode --context

To view all available options Renode supports, use::

  west simulate --runner=renode --renode-help

Out of tree runners
*******************

:ref:`Zephyr modules <modules>` can have external runners discovered by adding python
files in their :ref:`module.yml <modules-runners>`. Create an external runner class by
inheriting from ``ZephyrBinaryRunner`` and implement all abstract methods.

.. note::

   Support for custom out-of-tree runners makes the ``runners.core`` module part of
   the public API and backwards incompatible changes need to undergo the
   :ref:`deprecation process <breaking_api_changes>`.

Hacking
*******

This section documents the ``runners.core`` module used by the
flash and debug commands. This is the core abstraction used to implement
support for these features.

Developers can add support for new ways to flash and debug Zephyr programs by
implementing additional runners. To get this support into upstream Zephyr, the
runner should be added into a new or existing ``runners`` module, and imported
from :file:`runners/__init__.py`.

.. note::

   The test cases in :zephyr_file:`scripts/west_commands/tests` add unit test
   coverage for the runners package and individual runner classes.

   Please try to add tests when adding new runners. Note that if your
   changes break existing test cases, CI testing on upstream pull
   requests will fail.

.. automodule:: runners.core
   :members:

Doing it By Hand
****************

If you prefer not to use West to flash or debug your board, simply
inspect the build directory for the binaries output by the build
system. These will be named something like ``zephyr/zephyr.elf``,
``zephyr/zephyr.hex``, etc., depending on your board's build system
integration. These binaries may be flashed to a board using
alternative tools of your choice, or used for debugging as needed,
e.g. as a source of symbol tables.

By default, these West commands rebuild binaries before flashing and
debugging. This can of course also be accomplished using the usual
targets provided by Zephyr's build system (in fact, that's how these
commands do it).

.. _cmake(1):
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _CMAKE_VERBOSE_MAKEFILE:
   https://cmake.org/cmake/help/latest/variable/CMAKE_VERBOSE_MAKEFILE.html

.. _CMake Generator:
   https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html

.. _MCUboot: https://mcuboot.com/
