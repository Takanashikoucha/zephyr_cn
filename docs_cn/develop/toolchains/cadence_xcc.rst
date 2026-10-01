.. _toolchain_cadence_xcc:

Cadence Tensilica Xtensa C/C++ 编译器（XCC）
#############################################

#. 获取针对特定 SoC 的 Tensilica 软件开发工具包。这通常包含两个部分：

   * Xtensa Xplorer，包含必要的可执行文件和库。

   * 一个 SoC 特定的附加组件，安装在 Xtensa Xplorer 之上。

     * 该附加组件允许编译器为手头 SoC 生成代码。

#. 安装 Xtensa Xplorer，然后安装 SoC 附加组件。

   * 按照 Cadence 的说明安装 SDK。

   * 根据 SDK 的不同，有两组编译器：

     * 基于 GCC 的编译器：``xt-xcc`` 及其相关工具。

     * 基于 Clang 的编译器：``xt-clang`` 及其相关工具。

#. 确保已获取使用 SDK 的许可证，或能够访问远程许可证服务器。

#. :ref:`设置以下环境变量 <env_vars>`：

   * 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``xcc`` 或 ``xt-clang``。
   * 将 :envvar:`XTENSA_TOOLCHAIN_PATH` 设置为工具链安装目录。

   * 有两种方式指定要使用的 SoC ID 和 SDK 版本，它们互斥，不能同时使用。

     #. 为单个 SoC 构建时：

        * 将 :envvar:`XTENSA_CORE` 设置为应用目标 SoC 的 ID。
        * 将 :envvar:`TOOLCHAIN_VER` 设置为 Xtensa SDK 版本。

     #. 为多个 SoC 构建时，对每个 SoC 和板级组合：

        * 将 :envvar:`XTENSA_CORE_{normalized_board_target}`
          设置为应用目标 SoC 的 ID。
        * 将 :envvar:`TOOLCHAIN_VAR_{normalized_board_target}`
          设置为 Xtensa SDK 版本。

#. 例如，假设 SDK 安装在 ``/opt/xtensa``，使用 SDK 在 ``intel_adsp/ace15_mtpm`` 上进行应用开发，用上述两种方式设置环境：

   #. 单个 SoC：

      .. code-block:: console

         # Linux
         export ZEPHYR_TOOLCHAIN_VARIANT=xt-clang
         export XTENSA_TOOLCHAIN_PATH=/opt/xtensa/XtDevTools/install/tools/
         export XTENSA_CORE=ace10_LX7HiFi4_2022_10
         export TOOLCHAIN_VER=RI-2022.10-linux

   #. 多个 SoC：

      .. code-block:: console

         # Linux
         export ZEPHYR_TOOLCHAIN_VARIANT=xt-clang
         export XTENSA_TOOLCHAIN_PATH=/opt/xtensa/XtDevTools/install/tools/
         export TOOLCHAIN_VER_intel_adsp_ace15_mtpm=RI-2022.10-linux
         export XTENSA_CORE_intel_adsp_ace15_mtpm=ace10_LX7HiFi4_2022_10

#. 要使用基于 Clang 的编译器：

   * 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``xt-clang``。

   * 注意基于 Clang 的编译器可能包含一个旧的 LLVM 缺陷，导致以下错误：

     .. code-block:: console

        /tmp/file.s: Assembler messages:
        /tmp/file.s:20: Error: file number 1 already allocated
        clang-3.9: error: Xtensa-as command failed with exit code 1

     如果发生这种情况，将 :envvar:`XCC_NO_G_FLAG` 设置为 ``1``。

     * 例如：

       .. code-block:: console

          # Linux
          export XCC_NO_G_FLAG=1
