.. _other_x_compilers:

其他交叉编译器
###############

这种工具链变体借鉴自 Linux 内核构建系统的机制：使用 ``CROSS_COMPILE`` 环境变量来配置基于 GNU 的交叉工具链。

此类"其他交叉编译器"的例子包括：你的 Linux 发行版打包的交叉工具链、你自己编译的、或从网上下载的。与 :ref:`toolchains` 中明确列出的工具链不同，Zephyr 构建系统可能未针对这些工具链进行过测试，也不官方支持它们。（尽管如此，工具链配置机制本身是受支持的。）

按照以下步骤使用其中一种工具链。

#. 安装适合你的主机和目标系统的交叉编译器。

   例如，你可以在基于 Debian 的 Linux 系统上安装 ``gcc-arm-none-eabi`` 包，或在 Fedora 或 Red Hat 上安装 ``arm-none-eabi-newlib``：

   .. code-block:: console

      # On Debian or Ubuntu
      sudo apt-get install gcc-arm-none-eabi
      # On Fedora or Red Hat
      sudo dnf install arm-none-eabi-newlib

#. :ref:`设置这些环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``cross-compile``。
   - 将 ``CROSS_COMPILE`` 设置为你的工具链二进制文件的共同路径前缀，例如包含编译器二进制文件的目录路径加上目标三元组和尾随连字符。

#. 要检查你是否在当前环境中正确设置了这些变量，请参照以下示例 shell 会话（``CROSS_COMPILE`` 的值在你的系统上可能不同）：

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      cross-compile
      $ echo $CROSS_COMPILE
      /usr/bin/arm-none-eabi-

   你也可以将 ``CROSS_COMPILE`` 设置为 CMake 变量。

使用此选项时，你的所有工具链二进制文件必须位于同一目录中，并具有共同的文件名前缀。``CROSS_COMPILE`` 变量设置为目录与文件名前缀的拼接。

在上面 Debian 示例中，``gcc-arm-none-eabi`` 包在 ``/usr/bin/`` 目录中安装 ``arm-none-eabi-gcc`` 和 ``arm-none-eabi-ld`` 等二进制文件，因此共同前缀是 ``/usr/bin/arm-none-eabi-``（包括尾随连字符 ``-``）。

如果你的工具链安装在 ``/opt/mytoolchain/bin`` 且二进制文件名称基于目标三元组 ``myarch-none-elf``，``CROSS_COMPILE`` 将设置为 ``/opt/mytoolchain/bin/myarch-none-elf-``。
