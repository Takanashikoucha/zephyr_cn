.. _iwyu:

include-what-you-use（IWYU）支持
###################################

`include-what-you-use <https://include-what-you-use.org/>`__（IWYU）
是一款构建在 Clang 和 LLVM 之上的工具，
用于分析 C 和 C++ 源文件中的 ``#include`` 指令。
对每个翻译单元，它报告被包含但未使用的头文件，
以及被使用但其定义头文件仅被传递性包含的符号。
按其建议操作可保持包含集最小且显式。

安装 include-what-you-use
*******************************

``include-what-you-use`` 由大多数 Linux 发行版分发，
在 Ubuntu 上：

.. code-block:: shell

    sudo apt-get install iwyu

确保 ``include-what-you-use`` 二进制文件在你的 :envvar:`PATH` 中可用。

运行 include-what-you-use
************************

.. note::

   IWYU 构建在 Clang 之上，因此使用 LLVM 工具链构建可产生最准确的结果。

要运行 include-what-you-use，
:ref:`west build <west-building>` 应带上 ``-DZEPHYR_SCA_VARIANT=iwyu`` 参数调用，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: native_sim
   :gen-args: -DZEPHYR_SCA_VARIANT=iwyu
   :goals: build
   :compact:

分析在每个源文件编译过程中运行，
建议的包含变更会打印到构建输出（stderr）。

配置 include-what-you-use
********************************

include-what-you-use 可以通过特定选项进行控制。
完整的选项列表参见
`IWYU 文档 <https://github.com/include-what-you-use/include-what-you-use/blob/master/README.md>`__。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``IWYU_OPTS``
     - include-what-you-use 选项的分号分隔列表。
       每个选项会自动加上所需的 ``-Xiwyu`` 前缀后转发给工具。

这些参数可以在命令行上传递，也可以作为环境变量设置。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: native_sim
   :gen-args: -DZEPHYR_SCA_VARIANT=iwyu -DIWYU_OPTS="--no_comments;--verbose=3"
   :goals: build
   :compact:
