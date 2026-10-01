.. _toolchain_eld:

嵌入式链接器（ELD）
#####################

`ELD`_ 是 Qualcomm 的开源、基于 LLVM 的、GNU 兼容链接器。
它可以在用 LLVM 工具链构建 Zephyr 时作为 LLD 或 GNU ld 的替代
（例如 :ref:`Arm 嵌入式工具链 <toolchain_atfe>` 或主机 clang）。
参见 `ELD 用户指南`_ 获取 ELD 本身的详细信息。

ELD 只是一个链接器（``ld.eld``）；
仍然需要一个单独的 C/C++ 工具链来编译源代码。

安装
************

有三种方式获取 ELD：

#. **每日二进制发布。** 预构建的 ``ld.eld`` 二进制文件发布在
   `ELD 发布页`_ 上。

#. **从源码构建。** 按 `ELD README`_ 中描述的，
   针对一个 LLVM 代码树构建 ELD；
   集成的 ``llvm-project`` 构建在构建树的 ``bin/`` 目录下产生 ``ld.eld``。

#. **通过 cpullvm 的完整工具链。** `cpullvm`_ 工具链是一个用于
   Arm、AArch64 和 RISC-V 嵌入式目标的完整 LLVM 工具链，
   打包了 ``ld.eld`` 和 ``ld.lld`` 连同 clang、运行时库和头文件。
   预构建的 cpullvm 压缩包发布在其 `cpullvm 发布页`_ 上
   用于 Linux 和 Windows，
   cpullvm 22.1.1 已在 ELD CI 中与 Zephyr 测试过。

选项 1 和 2 只提供 ``ld.eld``；
仍然需要一个单独的 LLVM 工具链（clang、运行时库和头文件）来构建 Zephyr。

验证安装：

.. code-block:: console

   $ ld.eld --version
   eld 22.0 (GNU Compatible linker)

需要 ELD 22.0 或更高版本。

使用
*****

ELD 通过 ``host/llvm`` 工具链变体选择。
将 :envvar:`LLVM_TOOLCHAIN_PATH` 指向 LLVM 工具链
（例如 cpullvm 安装，或 ``bin/`` 目录或 :envvar:`PATH` 上有 ``ld.eld`` 的另一个工具链），
然后通过将 :kconfig:option:`CONFIG_LLVM_USE_ELD` 设置为 ``y`` 启用 ELD。

例如：

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm \
                     -DLLVM_TOOLCHAIN_PATH=<path-to-llvm-toolchain> \
                     -DCONFIG_LLVM_USE_ELD=y

参见 :ref:`toolchain_atfe` 或 :ref:`toolchain_zephyr_sdk` 获取
配置 LLVM 工具链的更多信息。

.. _ELD: https://github.com/qualcomm/eld
.. _ELD 用户指南: https://qualcomm.github.io/eld/
.. _ELD 发布页: https://github.com/qualcomm/eld/releases
.. _ELD README: https://github.com/qualcomm/eld#building-eld-and-running-tests
.. _cpullvm: https://github.com/qualcomm/cpullvm-toolchain
.. _cpullvm 发布页: https://github.com/qualcomm/cpullvm-toolchain/releases
