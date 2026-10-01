.. _toolchain_zephyr_sdk:

Zephyr SDK
##########

Zephyr 软件开发套件（SDK）包含 Zephyr 支持的每种架构的 GNU 和 LLVM 工具链。它还包含额外的主机工具，如自定义 QEMU 和 OpenOCD。

强烈建议使用 Zephyr SDK，在某些条件下甚至可能必需（例如为某些架构在 QEMU 中运行测试）。

支持的架构
***************

Zephyr SDK 支持以下目标架构：

* ARC（32 位和 64 位；ARCv1、ARCv2、ARCv3）
* ARM（32 位和 64 位；ARMv6、ARMv7、ARMv8；A/R/M 配置）
* Microblaze（32 位）
* MIPS（32 位和 64 位）
* RISC-V（32 位和 64 位；RV32I、RV32E、RV64I）
* RX
* SPARC（32 位和 64 位；SPARC V8、SPARC V9）
* x86（32 位和 64 位）
* Xtensa

.. _toolchain_zephyr_sdk_bundle_variables:

安装捆绑包和变量
*********************************

Zephyr SDK 捆绑包支持所有主要操作系统（Linux、macOS 和 Windows），以压缩文件形式分发。

为便于分发，SDK 预打包为三种不同变体供下载：

.. list-table:: SDK 捆绑包变体
   :widths: 20 20 60
   :header-rows: 1

   * - 变体
     - 主机工具
     - 包含的工具链
   * - ``gnu``
     - 是
     - 所有支持架构的 GNU（Binutils、GCC 和 GDB）
   * - ``llvm``
     - 是
     - LLVM/Clang
   * - ``minimal``
     - 是
     - 无

安装过程包括解压下载的捆绑包文件并运行包含的安装脚本。

无论下载哪个捆绑包，安装过程中会提示你想安装哪些工具链，如果未在安装脚本执行的本地目录中找到，将在安装期间下载。也可以将 GNU 和 LLVM SDK 捆绑包都下载并解压到同一目录树中，从而无需在安装脚本执行期间下载即可安装两者。

额外的操作系统特定说明在下面的章节中描述。

如果未选择工具链，构建系统会查找 Zephyr SDK 并使用其中的工具链。你可以通过将环境变量 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``zephyr`` 来强制这样做。

如果你在任何默认位置（列在下面操作系统特定说明中）之外安装 Zephyr SDK 并希望自动发现 Zephyr SDK，则必须通过运行安装脚本在 CMake 包注册表中注册 Zephyr SDK。如果你决定不在 CMake 注册表中注册 Zephyr SDK，则可以用 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 指向 Zephyr SDK 安装目录。

你也可以将 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 设置为包含多个 Zephyr SDK 的目录，允许自动选择工具链。例如，你可以将 ``ZEPHYR_SDK_INSTALL_DIR`` 设置为 ``/company/tools``，其中 ``company/tools`` 文件夹包含以下子文件夹：

* ``/company/tools/zephyr-sdk-0.13.2``
* ``/company/tools/zephyr-sdk-a.b.c``
* ``/company/tools/zephyr-sdk-x.y.z``

这允许 Zephyr 构建系统选择正确版本的 SDK，同时允许多个 Zephyr SDK 在特定路径下分组。

.. _toolchain_zephyr_sdk_compatibility:

Zephyr SDK 版本兼容性
********************************

一般来说，本页引用的 Zephyr SDK 版本应被视为对应 Zephyr 版本的推荐版本。

完整的兼容 Zephyr 和 Zephyr SDK 版本列表，请参考 `Zephyr SDK 版本兼容性矩阵`_。

.. _toolchain_zephyr_sdk_install:

Zephyr SDK 安装
***********************

.. toolchain_zephyr_sdk_install_start

.. note:: 如需，你可以在下面的说明中将 |sdk-version-literal| 更改为另一版本；`Zephyr SDK 发行版`_ 页面包含所有可用的 SDK 发行版。

.. note:: 下面的说明用于使用 Zephyr GNU SDK 捆绑包安装，它包含所有支持架构的 GNU 工具链和主机工具。要使用 Zephyr LLVM SDK 捆绑包安装，将 SDK 捆绑包文件名中的 ``_gnu`` 后缀替换为 ``_llvm``。

.. note:: 如果你想卸载 SDK，只需删除你安装它的目录即可。

.. tabs::

   .. group-tab:: Linux

      .. _linux_zephyr_sdk:

      #. 下载并验证 `Zephyr SDK 捆绑包`_：

         .. parsed-literal::

            cd ~
            wget |sdk-url-linux|
            wget -O - |sdk-url-linux-sha| | shasum --check --ignore-missing

         如果你的主机架构是 64 位 ARM（例如 Raspberry Pi），将 ``x86_64`` 替换为 ``aarch64`` 以下载 64 位 ARM Linux SDK。

      #. 解压 Zephyr SDK 捆绑包归档：

         .. parsed-literal::

            tar xvf zephyr-sdk- |sdk-version-trim| _linux-x86_64_gnu.tar.xz

         .. note::
            建议在以下位置之一解压 Zephyr SDK 捆绑包：

            * ``$HOME``
            * ``$HOME/.local``
            * ``$HOME/.local/opt``
            * ``$HOME/bin``
            * ``/opt``
            * ``/usr/local``

            Zephyr SDK 捆绑包归档包含 ``zephyr-sdk-<version>`` 目录，当在 ``$HOME`` 下解压时，结果安装路径将是 ``$HOME/zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 捆绑包安装脚本：

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            ./setup.sh

         .. note::
            你只需在解压 Zephyr SDK 捆绑包后运行一次安装脚本。

            如果你在初始安装后移动 Zephyr SDK 捆绑包目录，必须重新运行安装脚本。

      #. 安装 `udev <https://en.wikipedia.org/wiki/Udev>`_ 规则，允许你作为普通用户烧录大多数 Zephyr 开发板：

         .. parsed-literal::

            sudo cp ~/zephyr-sdk- |sdk-version-trim| /hosttools/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
            sudo udevadm control --reload

   .. group-tab:: macOS

      .. _macos_zephyr_sdk:

      #. 下载并验证 `Zephyr SDK 捆绑包`_：

         .. parsed-literal::

            cd ~
            curl -L -O |sdk-url-macos|
            curl -L |sdk-url-macos-sha| | shasum --check --ignore-missing

      #. 解压 Zephyr SDK 捆绑包归档：

         .. parsed-literal::

            tar xvf zephyr-sdk- |sdk-version-trim| _macos-aarch64_gnu.tar.xz

         .. note::
            建议在以下位置之一解压 Zephyr SDK 捆绑包：

            * ``$HOME``
            * ``$HOME/.local``
            * ``$HOME/.local/opt``
            * ``$HOME/bin``
            * ``/opt``
            * ``/usr/local``

            Zephyr SDK 捆绑包归档包含 ``zephyr-sdk-<version>`` 目录，当在 ``$HOME`` 下解压时，结果安装路径将是 ``$HOME/zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 捆绑包安装脚本：

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            ./setup.sh

         .. note::
            你只需在解压 Zephyr SDK 捆绑包后运行一次安装脚本。

            如果你在初始安装后移动 Zephyr SDK 捆绑包目录，必须重新运行安装脚本。

   .. group-tab:: Windows

      .. _windows_zephyr_sdk:

      #. 以**普通用户**身份打开 ``cmd.exe`` 终端窗口

      #. 下载 `Zephyr SDK 捆绑包`_：

         .. parsed-literal::

            cd %HOMEPATH%
            wget |sdk-url-windows|

      #. 解压 Zephyr SDK 捆绑包归档：

         .. parsed-literal::

            7z x zephyr-sdk- |sdk-version-trim| _windows-x86_64_gnu.7z

         .. note::
            建议在以下位置之一解压 Zephyr SDK 捆绑包：

            * ``%HOMEPATH%``
            * ``%PROGRAMFILES%``

            Zephyr SDK 捆绑包归档包含 ``zephyr-sdk-<version>`` 目录，当在 ``%HOMEPATH%`` 下解压时，结果安装路径将是 ``%HOMEPATH%\zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 捆绑包安装脚本：

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            setup.cmd

         .. note::
            你只需在解压 Zephyr SDK 捆绑包后运行一次安装脚本。

            如果你在初始安装后移动 Zephyr SDK 捆绑包目录，必须重新运行安装脚本。

.. _Zephyr SDK Releases: https://github.com/zephyrproject-rtos/sdk-ng/tags
.. _Zephyr SDK Version Compatibility Matrix: https://github.com/zephyrproject-rtos/sdk-ng/wiki/Zephyr-Version-Compatibility#zephyr-sdk-version-compatibility-matrix

.. toolchain_zephyr_sdk_install_end
