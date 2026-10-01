.. _toolchain_atfe:

Arm Toolchain for Embedded (ATfE)
#################################


Arm Toolchain for Embedded（ATfE）是 Arm 提供的 C 和 C++ 工具链，基于免费开源的 LLVM 编译器基础设施和用于裸机（baremetal）目标的 Picolib C 库。

ATfE 经过精心调优，特别关注较新 ARM 产品（2024 年之后）的性能，例如 64 位 Arm 架构（AArch64），或 M-Profile 向量扩展（MVE，一种 32 位 Armv8.1-M 扩展）。

安装
************

#. 下载并安装适用于你的操作系统的 `Arm toolchain for embedded`_ 构建包，并将其解压到文件系统中。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``host/llvm``。
   - 将 :envvar:`LLVM_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. 要检查你是否在当前环境中正确设置了这些变量，请按照以下示例 shell 会话操作（:envvar:`LLVM_TOOLCHAIN_PATH` 的值在你的系统上可能不同）：

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            echo $ZEPHYR_TOOLCHAIN_VARIANT
            host/llvm
            echo $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab:: macOS

         .. code-block:: bash

            echo $ZEPHYR_TOOLCHAIN_VARIANT
            host/llvm
            echo $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab:: Windows

         .. code-block:: powershell

            > echo %ZEPHYR_TOOLCHAIN_VARIANT%
            host/llvm
            > echo %LLVM_TOOLCHAIN_PATH%
            C:\ATfE

   .. _toolchain_env_var:

#. 你也可以在生成 Zephyr 应用的构建系统时，将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 和 ``LLVM_TOOLCHAIN_PATH`` 设置为 CMake 变量，如下所示：

   .. code-block:: console

      west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=...

工具链设置
******************

由于 LLVM 与 GNU 工具具有广泛的兼容性，使用任何 LLVM 工具链构建时，你必须指定一些设置，让编译器知道使用哪些工具：

链接器
   * 设置 :envvar:`CONFIG_LLVM_USE_LLD=y` 以使用 LLVM 链接器。
   * 设置 :envvar:`CONFIG_LLVM_USE_LD=y` 以使用 GNU LD 链接器。

运行时库
   * 设置 :envvar:`CONFIG_COMPILER_RT_RTLIB=y` 以使用 LLVM 运行时库。
   * 设置 :envvar:`CONFIG_LIBGCC_RTLIB=y` 以使用 LibGCC 运行时库。

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=... -DCONFIG_LLVM_USE_LLD=y -DCONFIG_COMPILER_RT_RTLIB=y

.. _Arm Toolchain for Embedded: https://developer.arm.com/Tools%20and%20Software/Arm%20Toolchain%20for%20Embedded
