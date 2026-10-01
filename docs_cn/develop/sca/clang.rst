.. _clang:

Clang 静态分析器支持
#############################

Clang Static Analyzer 构建在 Clang 和 LLVM 之上。严格来说，分析器是 Clang 的一部分，因为 Clang 由一组可重用的 C++ 库组成，用于构建功能强大的源代码级工具。Clang Static Analyzer 使用的静态分析引擎是一个 Clang 库，能够在不同的上下文中、被不同的客户端复用。

LLVM 提供多种方法在代码库上运行分析器，包括通过一组专用工具（scan-build 和 analyze-build），或通过运行 clang 时的命令行参数（'--analyze'）。

- 'scan-build' 工具是最方便的方式，适用于使用简单 $CC makefile 变量的项目，因为它会包装并替换编译器调用来执行分析。

- 'analyze-build' 工具是 'scan-build' 的子工具，它仅依赖 'compile_commands.json' 数据库来执行分析。

- clang 选项 '--analyze' 会在构建过程中运行分析器，但不会生成目标文件，使得任何链接阶段都无法进行。在我们的场景中，第一个链接阶段会失败并停止分析。

由于其复杂的构建基础设施，使用 'analyze-build' 调用 clang 分析器是分析 Zephyr 项目最简单的方式。

`Clang 静态分析器文档 <https://clang.llvm.org/docs/ClangStaticAnalyzer.html>`__

安装 clang 分析器
*************************

'scan-build' 及其子工具 'analyze-build' 原生随 llvm 作为二进制文件的一部分提供。请确保二进制目录在你的 PATH 中可访问。

'scan-build' 也可作为独立的 python 包在 `pypi <https://pypi.org/project/scan-build/>`__ 上获得。

.. code-block:: shell

    pip install scan-build

运行 clang 静态分析器
*************************

.. note::

  分析器要求项目使用 LLVM 工具链构建，并生成 'compile_commands.json' 数据库。

要运行 clang 静态分析器，:ref:`west build <west-building>` 应使用 ``-DZEPHYR_SCA_VARIANT=clang`` 参数调用，连同 llvm 工具链参数，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/userspace/hello_world_user
   :board: qemu_x86
   :gen-args: -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=... -DZEPHYR_SCA_VARIANT=clang
   :goals: build
   :compact:

.. note::

  默认情况下，clang 静态分析器生成 html 报告，但可以通过选项（sarif、plist、html）选择其他输出格式。

配置 clang 静态分析器
*********************************

Clang 静态分析器可以使用特定选项进行控制。要获取可用选项的完整列表，请参考 'analyze-build' 辅助工具和 'scan-build' 辅助工具。

.. code-block:: shell

    analyze-build --help

默认已启用的选项：

* --analyze-headers : 同时分析 #include 文件中的函数。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``CLANG_SCA_OPTS``
     - 'analyze-build' 选项的分号分隔列表。

这些参数可以在命令行上传递，或作为环境变量设置。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=... -DZEPHYR_SCA_VARIANT=clang -DCLANG_SCA_OPTS="--sarif;--verbose"
   :goals: build
   :compact:
