.. _gcc:

GCC 静态分析支持
###########################

静态分析是在 `GCC <https://gcc.gnu.org/>`__ 10 中引入的，
通过选项 ``-fanalyzer`` 启用。
该选项执行的代码分析比传统警告昂贵得多，也更彻底。

运行 GCC 静态分析
***********************

要运行 GCC 静态分析，
:ref:`west build <west-building>` 应带上 ``-DZEPHYR_SCA_VARIANT=gcc`` 参数调用，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/userspace/hello_world_user
   :board: qemu_x86
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc
   :goals: build
   :compact:

配置 GCC 静态分析器
*******************************

GCC 静态分析器可以通过特定选项进行控制。

* `控制分析器的选项 <https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html>`__

* `控制诊断消息格式的选项 <https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Message-Formatting-Options.html>`__

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``GCC_SCA_OPTS``
     - GCC 分析器选项的分号分隔列表。

这些参数可以在命令行上传递，也可以作为环境变量设置。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc -DGCC_SCA_OPTS="-fdiagnostics-format=json;-fanalyzer-verbosity=3"
   :goals: build
   :compact:

.. note::

   GCC 静态分析器正处于活跃开发中，每个新版本都会引入新的选项。
   这个`页面 <https://gcc.gnu.org/wiki/StaticAnalyzer>`__
   概述了分析器每个新版本引入的选项和修复。

分析器的最新版本
******************************

由于 Zephyr 工具链可能不包含最新版本的 GCC 静态分析器，
GCC 静态分析也可以使用更新的
`GNU Arm 嵌入式工具链 <https://docs.zephyrproject.org/latest/develop/toolchains/gnu_arm_embedded.html>`__
来运行，以利用最新的分析器版本。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc -DZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb -DGNUARMEMB_TOOLCHAIN_PATH=...
   :goals: build
   :compact:
