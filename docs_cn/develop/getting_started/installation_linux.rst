.. _installation_linux:

安装 Linux 主机依赖
###############################

以下 Linux 发行版有可用的文档：

* Ubuntu
* Fedora
* Clear Linux
* Arch Linux

对于非滚动发布（rolling release）的发行版，
你的包管理器可能无法满足部分要求和依赖项。
在这种情况下，请按照提供的额外说明，
从包管理器以外的来源查找软件。

.. note:: 如果你在企业防火墙后面工作，你可能需要配置代理来访问互联网
   （如果你还没有这样做的话）。虽然一些工具使用环境变量
   ``http_proxy`` 和 ``https_proxy`` 获取代理设置，
   但一些工具使用自己的配置文件，最典型的是 ``apt`` 和 ``git``。

更新你的操作系统
****************

确保你的主机系统是最新的。

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: console

         sudo apt-get update
         sudo apt-get upgrade

   .. group-tab:: Fedora

      .. code-block:: console

         sudo dnf upgrade

   .. group-tab:: Clear Linux

      .. code-block:: console

         sudo swupd update

   .. group-tab:: Arch Linux

      .. code-block:: console

         sudo pacman -Syu

.. _linux_requirements:

安装要求和依赖
*************************************

.. NOTE FOR DOCS AUTHORS: DO NOT PUT DOCUMENTATION BUILD DEPENDENCIES HERE.

   本节针对构建 Zephyr 二进制文件所需的依赖项，*不是*
   本文档的依赖。如果你需要添加一个仅构建文档才需要的依赖项，
   请将其添加到 doc/README.rst。（此更改是在文档引入 LaTeX->PDF
   支持之后做出的，因为 texlive 的占用量非常大，
   而不构建 PDF 文档的用户并不需要它。）

注意，下面的说明会同时安装 Ninja 和 Make；你只需要其中一个。

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: console

         sudo apt-get install --no-install-recommends git cmake ninja-build gperf \
           ccache dfu-util device-tree-compiler wget \
           python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
           make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

   .. group-tab:: Fedora

      .. code-block:: console

         sudo dnf group install development-tools c-development
         sudo dnf install cmake ninja-build gperf dfu-util dtc wget which \
           python3-pip python3-tkinter xz file python3-devel SDL2-devel \
           libusb1-devel

   .. group-tab:: Clear Linux

      .. code-block:: console

         sudo swupd bundle-add c-basic dev-utils dfu-util dtc \
           os-core-dev python-basic python3-basic python3-tcl

      Clear Linux 的侧重点是 *原生* 性能和安全，而不是交叉编译。
      因此，它独特地默认向所有用户的 :ref:`环境 <env_vars>`
      导出一组编译器和链接器标志。
      Zephyr 的 CMake 构建系统会因此发出警告甚至失败。
      要清除这些标志中的 C/C++ 标志并修复 Zephyr 构建，
      请以 root 身份运行以下命令，然后注销并重新登录：

      .. code-block:: console

         echo 'unset CFLAGS CXXFLAGS' >> /etc/profile.d/unset_cflags.sh

      注意，该命令会为 *系统上的所有用户* 取消设置 C/C++ 标志。
      每个 Linux 发行版都有一组独特的、相对复杂的、
      且可能不断演变的 bash 初始化文件，它们相互 source，
      Clear Linux 也不例外。如果你需要更灵活的解决方案，
      可以从查看 ``/usr/share/defaults/etc/profile`` 中的逻辑入手。

   .. group-tab:: Arch Linux

      .. code-block:: console

         sudo pacman -S git cmake ninja gperf ccache dfu-util dtc wget \
             python-pip python-setuptools python-wheel tk xz file make which

CMake
=====

需要一个 :ref:`较新的 CMake 版本 <install-required-tools>`。
使用 ``cmake --version`` 检查你当前的版本。
如果你使用的是较旧的版本，有几种方式可以获得更新的版本：

* 在 Ubuntu 上，你可以按照添加
  `kitware 第三方 apt 仓库 <https://apt.kitware.com/>`_
  的说明，使用 apt 获取更新版本的 cmake。

* 从 CMake 项目网站下载并安装打包好的 cmake。
  （注意：这不会卸载之前版本的 cmake。）

  .. code-block:: console

     cd ~
     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh
     chmod +x cmake-3.21.1-Linux-x86_64.sh
     sudo ./cmake-3.21.1-Linux-x86_64.sh --skip-license --prefix=/usr/local
     hash -r

  如果安装脚本把 cmake 放到了你 PATH 中的新位置，
  可能就需要执行 ``hash -r`` 命令。

* 从 CMake 项目自己在 `CMake Downloads`_ 页面提供的
  预构建二进制文件中下载并安装。
  例如，要在 :file:`~/bin/cmake` 安装 3.21.1 版本：

  .. code-block:: console

     mkdir $HOME/bin/cmake && cd $HOME/bin/cmake
     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh
     yes | sh cmake-3.21.1-Linux-x86_64.sh | cat
     echo "export PATH=$PWD/cmake-3.21.1-Linux-x86_64/bin:\$PATH" >> $HOME/.zephyrrc

* 使用 ``pip3``：

  .. code-block:: console

     pip3 install --user cmake

  注意：这不会卸载之前版本的 cmake，
  并且会把新的 cmake 安装到你的 ~/.local/bin 目录，
  因此你需要将 ~/.local/bin 添加到 PATH。
  （详情见 :ref:`python-pip`。）

* 检查你的发行版的 beta 或 unstable 发布软件包库中是否有更新。

* 在 Ubuntu 上，你还可以使用 snap 获取当前可用的最新版本：

  .. code-block:: console

     sudo snap install cmake

更新 cmake 后，使用 ``cmake --version``
验证新安装的 cmake 能够被找到。
你可能还想卸载包管理器提供的 CMake，以避免冲突。
（使用 ``whereis cmake`` 查找其他已安装的版本。）

DTC（Device Tree Compiler，设备树编译器）
=========================

需要一个 :ref:`较新的 DTC 版本 <install-required-tools>`。
使用 ``dtc --version`` 检查你当前的版本。
如果你使用的是较旧的版本，
可以通过从源码构建来安装一个更新的版本，
或者安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` 中捆绑的那个。

Python
======

需要一个 :ref:`较新的 Python 3 版本 <install-required-tools>`。
使用 ``python3 --version`` 检查你当前的版本。

如果你使用的是较旧的版本，就需要安装一个更新的 Python 3。
你可以从源码构建，
或者（如果可用）使用你发行版软件包渠道中的 backport。
建议将该 Python 隔离在虚拟环境中，以避免干扰系统 Python。

.. _pyenv: https://github.com/pyenv/pyenv

安装 Zephyr 软件开发套件（SDK）
*************************************************

Zephyr 软件开发套件（SDK）包含 Zephyr 所支持的每种架构的工具链。
它还包括额外的主机工具，例如定制 QEMU 和 OpenOCD。

强烈推荐使用 Zephyr SDK，
在某些条件下它甚至是必需的
（例如，在 QEMU 中运行某些架构的测试）。

要安装 SDK，请按照 :ref:`Zephyr SDK 安装指南 <linux_zephyr_sdk>`
中的 Linux 步骤操作。

.. _sdkless_builds:

在 Linux 上不使用 Zephyr SDK 构建
****************************************

Zephyr SDK 是为了方便和易用而提供的。
它为所有 Zephyr 目标架构提供工具链，
构建应用或运行测试时不需要任何额外标志。
除了交叉编译器，Zephyr SDK 还提供预构建的主机工具。
不过，使用 :ref:`工具链` 一节中描述的其他工具链，
不使用 SDK 的工具链进行构建也是可行的。

如上所述，SDK 还包括预构建的主机工具。
要使用 SDK 的预构建主机工具配合来自其他来源的工具链，
你必须将 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量
设置为 Zephyr SDK 安装目录。
要不使用 Zephyr SDK 的预构建主机工具进行构建，
:envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量必须处于未设置状态。

要确保该变量处于未设置状态，运行：

.. code-block:: console

   unset ZEPHYR_SDK_INSTALL_DIR

.. _Zephyr SDK Releases: https://github.com/zephyrproject-rtos/sdk-ng/tags
.. _CMake Downloads: https://cmake.org/download
