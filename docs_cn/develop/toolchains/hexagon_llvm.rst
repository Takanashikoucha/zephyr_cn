.. _toolchain_hexagon:

Qualcomm Hexagon LLVM 工具链
###############################

#. 从 `toolchain_for_hexagon 发布页面
   <https://github.com/quic/toolchain_for_hexagon/releases>`_ 下载预构建的
   Hexagon LLVM 交叉工具链并解压，例如解压到 ``/opt/hexagon-toolchain``。
   安装目录就是包含 ``bin/clang`` 的那个目录。

   请使用基于 LLVM 23 或更高版本构建的发布版本。更早的发布版本会错误编译
   ``~BIT(n)``。修复已在
   `#205489 <https://github.com/llvm/llvm-project/pull/205489>`_ 中合入。

#. 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``hexagon``，
   将 :envvar:`HEXAGON_TOOLCHAIN_PATH` 设置为该目录：

   .. code-block:: bash

      export ZEPHYR_TOOLCHAIN_VARIANT=hexagon
      export HEXAGON_TOOLCHAIN_PATH=/opt/hexagon-toolchain

.. envvar:: HEXAGON_TOOLCHAIN_PATH

   Hexagon LLVM 交叉工具链的安装目录。

该工具链是一个普通的 LLVM 安装，因此该变体就是 :ref:`host_toolchains`
的 ``llvm`` 变体驱动一个不同的编译器。它拥有自己独立的路径变量，
因为 Hexagon 版 clang 只注册 Hexagon 目标，无法构建主机编译的目标
（例如 :zephyr:board:`native_sim`）；需要同时覆盖两者的环境必须
分别独立指定两个 LLVM 安装的路径，正如 Zephyr 的 CI 在单次 Twister
运行同时跨这两类平台时所做的那样。

使用 ``ZEPHYR_TOOLCHAIN_VARIANT=host/llvm`` 和
:envvar:`LLVM_TOOLCHAIN_PATH` 来构建 Hexagon 目标是等价的，且仍然受支持，
只要该变量所指向的安装就是 Hexagon 的那个安装。
