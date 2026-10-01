.. _env_vars:

环境变量
=====================

本文档中的各种页面引用设置 Zephyr 特定环境变量。本页描述如何做。

设置变量
*****************

选项 1：只一次
-------------------

要将环境变量 ``MY_VARIABLE`` 设置为 ``foo`` 用于当前终端窗口的生命周期：

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         export MY_VARIABLE=foo

   .. group-tab:: Windows

      .. code-block:: console

         set MY_VARIABLE=foo

.. warning::

   这最适合实验。如果你关闭终端窗口、使用另一个终端窗口或标签、重启电脑等，这个设置将永远丢失。

   如果你想继续使用设置，推荐使用选项 2 或 3。

选项 2：在所有终端中
--------------------------

.. tabs::

   .. group-tab:: Linux/macOS

      将 ``export MY_VARIABLE=foo`` 行添加到你主目录中你 shell 的启动脚本。对于 Bash，这通常是 Linux 上的 :file:`~/.bashrc` 或 macOS 上的 :file:`~/.bash_profile`。这些启动脚本中的更改不影响已启动的 shell 实例；尝试打开新终端窗口获取新设置。

   .. group-tab:: Windows

      你可以在 ``cmd.exe`` 中使用 ``setx`` 程序或第三方 RapidEE 程序。

      要使用 ``setx``，键入这个命令，然后关闭终端窗口。任何新 ``cmd.exe`` 窗口将有 ``MY_VARIABLE`` 设置为 ``foo``。

      .. code-block:: console

         setx MY_VARIABLE foo

      要安装 RapidEE，一个免费图形环境变量编辑器，`使用 Chocolatey`_ 在管理员命令提示符中：

      .. code-block:: console

         choco install rapidee

      然后你可以从终端运行 ``rapidee`` 启动程序并设置环境变量。确保使用 "User" 环境变量区域 -- 否则，你必须以管理员身份运行 RapidEE。退出前确保通过点击左上角的 Save 按钮保存你的更改。你在 RapidEE 中做的设置在你打开新终端窗口时将可用。

.. _env_vars_zephyrrc:

选项 3：使用 ``zephyrrc`` 文件
----------------------------------

如果你不想让变量的设置对你的所有终端可用，但仍想保存值用于使用 Zephyr 时加载到你的环境中，选择这个选项。

.. tabs::

   .. group-tab:: Linux/macOS

      Zephyr 支持 :file:`zephyrrc` 文件的多个位置，在可能时遵循 XDG Base Directory Specification。在以下位置之一创建 zephyrrc 文件（它们将按顺序检查）：

      #. :file:`$XDG_CONFIG_HOME/zephyr/zephyrrc`
      #. :file:`$HOME/.config/zephyr/zephyrrc`
      #. :file:`$HOME/.zephyrrc`

      将这行添加到你偏好位置的文件：

      .. code-block:: console

         export MY_VARIABLE=foo

      要将这个值取回你的当前终端环境，**你必须运行** ``source zephyr-env.sh`` 从主 ``zephyr`` 仓库。除其他事情外，这个脚本会加载你的 :file:`zephyrrc`（它从上面位置列表找到的第一个）。

      如果你关闭窗口等，值将丢失；重新运行 ``source zephyr-env.sh`` 取回它。

   .. group-tab:: Windows

      用记事本这样的文本编辑器将 ``set MY_VARIABLE=foo`` 行添加到文件 :file:`%userprofile%\\zephyrrc.cmd` 保存值。

      要将这个值取回你的当前终端环境，**你必须运行** ``zephyr-env.cmd`` 在 ``cmd.exe`` 窗口中在更改目录到主 ``zephyr`` 仓库之后。除其他事情外，这个脚本运行 :file:`%userprofile%\\zephyrrc.cmd`。

      如果你关闭窗口等，值将丢失；重新运行 ``zephyr-env.cmd`` 取回它。

      这些脚本：

      - 将 :envvar:`ZEPHYR_BASE` 设置为 zephyr 仓库的位置
      - 向你的 :envvar:`PATH` 环境变量添加某些 Zephyr 特定位置（如 zephyr 的 :file:`scripts` 目录）
      - 加载上面 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件中的任何设置。

      因此你可以在你需要任何这些设置的任何时候使用它们。

.. _zephyr-env:

Zephyr 环境脚本
**************************

你可以使用 zephyr 仓库脚本 ``zephyr-env.sh``（用于 macOS 和 Linux）和 ``zephyr-env.cmd``（用于 Windows）将 Zephyr 特定设置加载到当前终端的环境中。要做到这，从 zephyr 仓库运行这个命令：

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         source zephyr-env.sh

   .. group-tab:: Windows

      .. code-block:: console

         zephyr-env.cmd

这些脚本：

- 将 :envvar:`ZEPHYR_BASE` 设置为 zephyr 仓库的位置
- 向你的 ``PATH`` 环境变量添加某些 Zephyr 特定位置（如 zephyr 的 :file:`scripts` 目录）
- 加载上面 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件中的任何设置。

因此你可以在你需要任何这些设置的任何时候使用它们。

.. _env_vars_important:

重要环境变量
*******************************

一些 :ref:`important-build-vars` 也可以在环境中设置。这里是一些这些重要环境变量的描述。这不是全面的列表。

.. envvar:: BOARD

   见 :ref:`important-build-vars`。

.. envvar:: CONF_FILE

   见 :ref:`important-build-vars`。

.. envvar:: SHIELD

   见 :ref:`shields`。

.. envvar:: ZEPHYR_BASE

   见 :ref:`important-build-vars`。

.. envvar:: EXTRA_ZEPHYR_MODULES

   见 :ref:`important-build-vars`。

.. envvar:: ZEPHYR_MODULES

   见 :ref:`important-build-vars`。

.. envvar:: ZEPHYR_BOARD_ALIASES

   见 :ref:`gs-board-aliases`

以下额外环境变量在配置用于构建 Zephyr 应用的 :ref:`工具链 <gs_toolchain>` 时重要。

.. envvar:: ZEPHYR_SDK_INSTALL_DIR

   Zephyr SDK 安装的路径。

.. envvar:: ZEPHYR_TOOLCHAIN_VARIANT

   要使用的工具链的名称。

.. envvar:: {TOOLCHAIN}_TOOLCHAIN_PATH

   :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 指定的工具链的路径。例如，如果 ``ZEPHYR_TOOLCHAIN_VARIANT=host/llvm``，使用 ``LLVM_TOOLCHAIN_PATH``。（注意形成环境变量名称时的大写小写。）

你可能在 :ref:`更新 Zephyr SDK 工具链 <gs_toolchain_update>` 时需要更新这些变量中的某些。

仿真器和开发板可能也依赖额外的程序。构建系统将尝试自动定位这些程序，但可能依赖额外的 CMake 或环境变量来做到。请查阅你的仿真器或开发板的文档获取更多信息。以下环境变量在这种情况下可能有用：

.. envvar:: PATH

   ``PATH`` 是在 Unix 类或 Microsoft Windows 操作系统上使用的环境变量，用于指定可执行程序位于的一组目录。

.. _使用 Chocolatey: https://chocolatey.org/packages/RapidEE
