.. _getting_started:

入门指南
########

按照本指南，你可以：

- 在 Ubuntu、macOS 或 Windows 上搭建命令行 Zephyr 开发环境
  （其他 Linux 发行版的说明在 :ref:`installation_linux` 中讨论）
- 获取源代码
- 构建、烧录并运行一个示例应用

.. _host_setup:

选择并更新操作系统
******************

点击你正在使用的操作系统。

.. tabs::

   .. group-tab:: Ubuntu

      本指南涵盖 Ubuntu 24.04 LTS 及更高版本。
      如果你使用的是其他 Linux 发行版，请参见 :ref:`installation_linux`。

      .. code-block:: bash

         sudo apt update
         sudo apt upgrade

   .. group-tab:: macOS

      选择 :menuselection:`系统设置 --> 通用 --> 软件更新`，
      并安装所有可用的更新。更多细节见 `Apple 支持主题
      <https://support.apple.com/en-us/HT201541>`_。

      .. note::

         不支持 x86-64 macOS。

   .. group-tab:: Windows

      选择 :menuselection:`开始 --> 设置 --> 更新和安全 --> Windows Update`。
      点击 :guilabel:`检查更新`，并安装所有可用的更新。

.. _install-required-tools:

安装依赖
********

接下来，安装 Zephyr 配置和构建应用所需的主机工具。
下面的说明使用每个操作系统推荐的包管理器，
以便这些工具在终端中可用。

当前主要依赖项的最低要求版本如下：

.. list-table::
   :header-rows: 1

   * - 工具
     - 最低版本

   * - `CMake <https://cmake.org/>`_
     - 3.28.0

   * - `Python <https://www.python.org/>`_
     - 3.12

   * - `Devicetree 编译器 <https://www.devicetree.org/>`_
     - 1.4.6

.. note::

   强烈推荐使用 Python 3.12。在某些系统上使用更新的 Python 版本可能会失败，
   例如在 Windows 上安装所需软件包时。

.. tabs::

   .. group-tab:: Ubuntu

      .. _install_dependencies_ubuntu:

      #. 使用 ``apt`` 安装所需的依赖项：

         .. code-block:: bash

            sudo apt install --no-install-recommends git cmake ninja-build gperf \
              ccache dfu-util device-tree-compiler wget python3-dev python3-venv python3-tk \
              xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

         .. note::

            由于 ``gcc-multilib`` 和 ``g++-multilib`` 在 AArch64（ARM64）
            系统上不可用，你可能需要从待安装的软件包列表中省略它们。

      #. 输入以下命令，验证系统上安装的主要依赖项的版本：

         .. code-block:: bash

            cmake --version
            python3 --version
            dtc --version

         对照本节开头表格中的版本进行检查。
         关于手动更新依赖项的更多信息，请参见 :ref:`installation_linux` 页面。

   .. group-tab:: macOS

      .. _install_dependencies_macos:

      #. 安装 `Homebrew <https://brew.sh/>`_：

         .. code-block:: bash

            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

      #. Homebrew 安装脚本完成后，按照屏幕上的说明
         将 Homebrew 安装路径添加到 PATH。

         .. code-block:: bash

            (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile
            source ~/.zprofile

      #. 使用 ``brew`` 安装所需的依赖项：

         .. code-block:: bash

            brew install cmake ninja gperf python3 python-tk ccache qemu dtc libmagic wget openocd

      #. 将 Homebrew 的 Python 目录添加到 PATH，
         以便你可以像使用 ``python3`` 和 ``pip3`` 一样执行 ``python`` 和 ``pip``。

            .. code-block:: bash

               (echo; echo 'export PATH="'$(brew --prefix)'/opt/python/libexec/bin:$PATH"') >> ~/.zprofile
               source ~/.zprofile

   .. group-tab:: Windows

      .. note::

         这些说明针对原生 Windows 环境。
         你也可以按照本指南中的 Ubuntu 说明，
         使用 `Windows 子系统 Linux（WSL）
         <https://learn.microsoft.com/windows/wsl/install>`_。
         在这种情况下请注意：从 WSL 内部烧录和调试硬件，
         需要先将 USB 设备对 WSL 可见，
         例如使用 `usbipd-win <https://github.com/dorssel/usbipd-win>`_。

      在较新的 Windows 版本（10 及更高版本）上，
      从 Microsoft Store 安装 Windows Terminal。
      下面的说明在 ``cmd.exe`` 或 PowerShell 中均可使用。

      这些说明使用 Windows 的官方包管理器 `winget`_。
      如果无法使用 winget，请从各软件包对应的网站安装依赖项，
      并确保其命令行工具位于你的 :envvar:`PATH` :ref:`环境变量 <env_vars>` 中。

      |p|

      .. _install_dependencies_windows:

      #. 在较新的 Windows 版本中，winget 默认已预装。
         你可以在终端窗口中输入 ``winget`` 来验证这一点。
         如果失败，你可以 `安装 winget`_。

      #. 打开命令提示符（``cmd.exe``）或 PowerShell 终端窗口。
         操作方法是：按下 Windows 键，输入 ``cmd.exe`` 或 PowerShell，
         然后点击搜索结果。

      #. 使用 ``winget`` 安装所需的依赖项：

         .. code-block:: bat

            winget install Kitware.CMake Ninja-build.Ninja oss-winget.gperf Python.Python.3.12 Git.Git oss-winget.dtc wget 7zip.7zip

      #. 关闭终端窗口。

      .. note::

         你可能需要将 7zip 的安装目录添加到 ``PATH``。


.. _winget: https://learn.microsoft.com/en-us/windows/package-manager/
.. _install winget: https://aka.ms/getwinget

.. _get_the_code:
.. _clone-zephyr:
.. _install_py_requirements:
.. _gs_python_deps:

获取 Zephyr 并安装 Python 依赖
******************************

接下来，使用 :ref:`west <west>` 创建一个工作区，
并获取 Zephyr 及其 :ref:`模块 <modules>`。

这些命令使用 :file:`zephyrproject` 作为工作区名称；
你可以选择其他名称和位置。
你还会在 `Python 虚拟环境`_ 中安装 Zephyr 的 Python 依赖项，
以便它们与系统 Python 安装保持分离。

.. _Python virtual environment: https://docs.python.org/3/library/venv.html

#. 创建一个新的虚拟环境：

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            python3 -m venv ~/zephyrproject/.venv

      .. group-tab:: macOS

         .. code-block:: bash

            python3 -m venv ~/zephyrproject/.venv

      .. group-tab:: Windows

         以 **普通用户** 身份打开 ``cmd.exe`` 或 PowerShell 终端窗口。

         .. tabs::

            .. code-tab:: bat

               cd %HOMEPATH%
               py -3.12 -m venv zephyrproject\.venv

            .. code-tab:: powershell

               cd $Env:HOMEPATH
               py -3.12 -m venv zephyrproject\.venv

#. 激活虚拟环境：

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            source ~/zephyrproject/.venv/bin/activate

      .. group-tab:: macOS

         .. code-block:: bash

            source ~/zephyrproject/.venv/bin/activate

      .. group-tab:: Windows

         .. note::

            在 PowerShell 中激活 Python 虚拟环境需要运行一个脚本，
            因此需要先允许运行脚本。

            .. code-block:: powershell

               Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

         .. tabs::

            .. code-tab:: bat

               zephyrproject\.venv\Scripts\activate.bat

            .. code-tab:: powershell

               zephyrproject\.venv\Scripts\Activate.ps1

   激活后，你的 shell 提示符前会出现 ``(.venv)`` 前缀。
   随时可以通过运行 ``deactivate`` 来取消激活虚拟环境。

   .. note::

      请记住：每次开始新的终端会话后，在使用 Zephyr 之前都要激活虚拟环境。
      否则，像 ``west`` 这样的命令将找不到，
      或者可能针对另一个 Python 环境运行，导致难以理解的错误。

#. 安装 west：

   west 是 Zephyr 的工作区管理器；下面的命令用它来创建和更新工作区。

   .. code-block:: shell

      pip install west

#. 获取 Zephyr 源代码：

   ``west init`` 会创建一个 :term:`west 工作区`，
   并克隆 ``https://github.com/zephyrproject-rtos/zephyr``
   作为其 :term:`清单仓库 <west manifest repository>`。

   然后 ``west update`` 会获取 Zephyr :term:`west 清单`
   中列出的各个 :term:`west 项目 <west project>`（模块）
   （硬件抽象层（HAL）、库等）。

   .. tabs::

      .. group-tab:: Ubuntu

         .. only:: not release

            .. code-block:: bash

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject
               cd ~/zephyrproject
               west update

         .. only:: release

            .. We need to use a parsed-literal here because substitutions do not work in code
               blocks. This means users can't copy-paste these lines as easily as other blocks but
               should be good enough still :)

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject --mr v |zephyr-version-ltrim|
               cd ~/zephyrproject
               west update

      .. group-tab:: macOS

         .. only:: not release

            .. code-block:: bash

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject
               cd ~/zephyrproject
               west update

         .. only:: release

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject --mr v |zephyr-version-ltrim|
               cd ~/zephyrproject
               west update

      .. group-tab:: Windows

         .. only:: not release

            .. code-block:: bat

               west init -m https://github.com/zephyrproject-rtos/zephyr zephyrproject
               cd zephyrproject
               west update

         .. only:: release

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr zephyrproject --mr v |zephyr-version-ltrim|
               cd zephyrproject
               west update

   .. tip::

      为了减少磁盘空间占用，并避免在设置期间下载不必要的模块或厂商 HAL，
      你可以在运行 ``west update`` 之前配置 :ref:`west-manifest-groups`。

#. 安装 Zephyr 的 Python 依赖项：

   ``west packages`` 会从检出的 Zephyr 工作区（包括其模块）
   读取 Python 依赖需求，因此安装的软件包与你获取的 Zephyr 版本相匹配。

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            west packages pip --install

      .. group-tab:: macOS

         .. code-block:: bash

            west packages pip --install

      .. group-tab:: Windows

         .. tabs::

            .. code-tab:: bat

               cmd /c zephyr\scripts\utils\west-packages-pip-install.cmd

            .. code-tab:: powershell

               python -m pip install @((west packages pip) -split ' ')

   .. note::

      安装这些依赖项可能会降级或升级 west 本身。

#. 导出 :ref:`Zephyr CMake 包 <cmake_pkg>`。
   这会将你当前的 Zephyr 检出注册到 CMake 的用户包注册表中，
   以便在构建应用时 ``find_package(Zephyr)`` 能够自动找到它。

   .. code-block:: shell

      west zephyr-export

安装 Zephyr SDK
***************

:ref:`Zephyr 软件开发套件（SDK） <toolchain_zephyr_sdk>`
包含 Zephyr 所支持的每种架构的工具链。
这些工具链包括编译器、汇编器、链接器，
以及为目标硬件构建 Zephyr 应用所需的其他程序。

它还包含额外的主机工具，例如用于仿真、烧录和调试
Zephyr 应用的定制 QEMU 和 OpenOCD 构建。

从 Zephyr 仓库使用 ``west sdk install`` 安装 Zephyr SDK：

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west sdk install

   .. group-tab:: macOS

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west sdk install

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            cd %HOMEPATH%\zephyrproject\zephyr
            west sdk install

         .. code-tab:: powershell

            cd $Env:HOMEPATH\zephyrproject\zephyr
            west sdk install

.. tip::

   使用命令选项来选择 SDK 安装位置，
   或仅安装所选架构的工具链。
   详情见 ``west sdk install --help``。

.. note::

    如果你想在不使用 ``west sdk`` 命令的情况下安装 Zephyr SDK，
    请参见 :ref:`toolchain_zephyr_sdk_install`。

.. _getting_started_run_sample:

构建 Blinky 示例
*****************

.. note::

   :zephyr:code-sample:`blinky` 与大多数（但不是所有）:ref:`开发板` 兼容。
   如果你的开发板不满足 Blinky 的 :ref:`blinky-sample-requirements`，
   那么 :zephyr:code-sample:`hello_world` 是一个很好的替代选择。

   如果你不确定 west 为你的开发板使用的名称，
   使用 ``west boards`` 列出 Zephyr 支持的所有开发板。
   你的开发板的 :zephyr:board-catalog:`文档页面`
   也会显示要传递给 ``west build`` 的精确开发板目标名称。

使用 :ref:`west build <west-building>` 构建 :zephyr:code-sample:`blinky`。
将 ``<your-board-name>`` 替换为你的开发板名称：

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west build -p always -b <your-board-name> samples/basic/blinky

   .. group-tab:: macOS

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west build -p always -b <your-board-name> samples/basic/blinky

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            cd %HOMEPATH%\zephyrproject\zephyr
            west build -p always -b <your-board-name> samples\basic\blinky

         .. code-tab:: powershell

            cd $Env:HOMEPATH\zephyrproject\zephyr
            west build -p always -b <your-board-name> samples\basic\blinky

``-p always`` 选项强制进行全新构建（pristine build），
它会删除之前任何配置产生的构建输出。
这可以避免入门时出现过期文件。
之后，你可以使用 ``-p auto``，
让 ``west build`` 的启发式规则决定何时可能需要全新构建。
详情见 ``west build -h``。

.. note::

   一块开发板可能包含一个或多个 SoC，
   每个 SoC 可能包含一个或多个 CPU 簇。
   为这类开发板构建时，必须指定要为哪个 SoC 或 CPU 簇构建示例。
   例如，要为 :zephyr:board:`nrf5340dk` 的 ``cpuapp`` 核心
   构建 :zephyr:code-sample:`blinky`，开发板必须指定为：
   ``nrf5340dk/nrf5340/cpuapp``。
   更多细节请参见 :ref:`board_terminology`。

烧录示例
********

连接你的开发板（通常通过 USB），
如果有电源开关则将其打开。
如果不确定该怎么做，请查看 :ref:`开发板` 中你的开发板页面，
因为有些开发板烧录时需要特定的设置或操作。

使用 :ref:`west flash <west-flashing>` 烧录示例。
这会将你刚刚构建的应用程序写入所连接的开发板：

.. code-block:: shell

   west flash

.. note::

    你可能需要安装你的开发板所需的额外 :ref:`主机工具 <flash-debug-host-tools>`。
    如果缺少任何必需的依赖项，``west flash`` 命令会打印错误。

.. note::

    在 Linux 上，首次使用调试探针烧录之前，
    你可能需要先配置 udev 规则。请参见 :ref:`setting-udev-rules`。

如果你使用的是 blinky，LED 将开始闪烁，如本图所示：

.. figure:: img/ReelBoard-Blinky.webp
   :width: 400px
   :name: reelboard-blinky

   Phytec :zephyr:board:`reel_board <reel_board>` 运行 blinky

下一步
******

以下是探索 Zephyr 的一些后续步骤：

* 尝试其他 :zephyr:code-sample-category:`示例`
* 了解 :ref:`应用` 和 :ref:`west <west>` 工具
* 了解 west 的 :ref:`烧录和调试 <west-build-flash-debug>` 功能，
  或更一般地了解 :ref:`flashing_and_debugging`
* 查看 :ref:`beyond-GSG`，了解其他设置方案和思路
* 探索 :ref:`project-resources`，从 Zephyr 社区获取帮助

.. _help:

寻求帮助
********

在寻求帮助之前，请搜索本文档、Zephyr 项目的 GitHub 讨论和 issue，
以及 Discord 聊天记录。你的问题可能在那里已经有答案了。
你还可以询问本文档每个页面都提供的 :ref:`聊天机器人 <kapa_ai>`。

* **邮件列表**：users@lists.zephyrproject.org 通常是寻求帮助的正确列表。
  `搜索存档并在此注册`_。
* **GitHub**：使用 `GitHub 讨论`_ 提问，
  使用 `GitHub issues`_ 报告 bug 和功能请求。
* **Discord**：你可以使用这个 `Discord 邀请`_ 加入。

寻求帮助时，请包含：

#. 你想做什么
#. 你尝试了什么，包括你运行的命令
#. 发生了什么，包括完整的文本输出

复制粘贴文本，而不是分享截图。
在 Discord 或 GitHub 上，如果终端输出、源代码或日志超过 5 行，
请使用三个反引号创建一个代码片段。

.. _Search archives and sign up here: https://lists.zephyrproject.org/g/users
.. _GitHub discussions: https://github.com/zephyrproject-rtos/zephyr/discussions
.. _Discord invite: https://chat.zephyrproject.org
.. _GitHub issues: https://github.com/zephyrproject-rtos/zephyr/issues
