.. _polyspace:

Polyspace 支持
#################

`Polyspace® <https://mathworks.com/products/polyspace.html>`__ 是 MathWorks 的一款商业静态代码分析工具，已获认证可用于最高安全等级的场景。它可以检查对 MISRA C 和 CERT C 等编码规范的合规性，发现 CWE，检测缺陷并计算代码复杂度度量。可选地，它还可以运行形式化证明来验证不存在数组越界访问、溢出、竞态条件等运行时错误，从而帮助实现内存安全。

安装
**********

Polyspace 工具必须已安装，并在操作系统或容器的 PATH 变量中可用。具体来说，路径 ``<polyspace_root>/polyspace/bin`` 必须在列表中。

安装说明参见 `此处 <https://mathworks.com/help/bugfinder/install-polyspace.html>`__。要使用形式化验证（证明缺陷的*不存在*），你还必须额外安装 `这个组件 <https://mathworks.com/help/codeprover/install-polyspace.html>`__。

安装目录中必须有一个许可证文件。要申请试用许可证，请访问 `此页面 <https://www.mathworks.com/campaigns/products/trials.html>`__。

运行
*******

可以通过 ``west`` 命令触发代码分析，方法是向构建添加选项 ``-DZEPHYR_SCA_VARIANT=polyspace``，例如：

.. code-block:: shell

   west build -b qemu_x86 samples/hello_world -- -DZEPHYR_SCA_VARIANT=polyspace

审查结果
*****************

识别出的问题会在构建末尾汇总并打印到控制台窗口中，同时给出包含详细结果的文件夹路径。

为了高效审查，应在 `Polyspace 用户界面 <https://mathworks.com/help/bugfinder/review-results-1.html>`__ 中打开该文件夹，或将其 `上传到 Web 界面 <https://mathworks.com/help/bugfinder/gs/run-bug-finder-on-server.html>`__ 并在那里审查。

要程序化地访问结果（例如在 CI 流水线中），各个问题还会以 CSV 文件的形式记录在结果文件夹中。

配置
*************

默认情况下，Polyspace 会扫描所有 C 和 C++ 源代码中的典型编程缺陷。以下选项可用于自定义默认行为：

.. list-table::
   :widths: 20 40 30
   :header-rows: 1

   * - 选项
     - 效果
     - 示例
   * - ``POLYSPACE_ONLY_APP``
     - 如果设置，只分析用户代码并忽略 Zephyr 源文件。
     - ``-DPOLYSPACE_ONLY_APP=1``
   * - ``POLYSPACE_OPTIONS``
     - 提供额外的命令行标志，例如用于选择编码规则。选项及其值之间用分号分隔。选项列表参见 `此处 <https://mathworks.com/help/bugfinder/referencelist.html?type=analysisopt&s_tid=CRUX_topnav>`__。
     - ``-DPOLYSPACE_OPTIONS="-misra3;mandatory-required;-checkers;all"``
   * - ``POLYSPACE_OPTIONS_FILE``
     - 命令行标志也可以放在一个文本文件中逐行提供。请提供该文件的绝对路径。
     - ``-DPOLYSPACE_OPTIONS_FILE=/workdir/zephyr/myoptions.txt``
   * - ``POLYSPACE_MODE``
     - 在缺陷查找（bugfinding）和证明（proving）模式之间切换。默认为缺陷查找。更多细节参见 `此处 <https://mathworks.com/help/bugfinder/gs/use-bug-finder-and-code-prover.html>`__。
     - ``-DPOLYSPACE_MODE=prove``
   * - ``POLYSPACE_PROG_NAME``
     - 覆盖被分析应用的名称。默认为开发板和应用名称。
     - ``-DPOLYSPACE_PROG_NAME=myapp``
   * - ``POLYSPACE_PROG_VERSION``
     - 覆盖被分析应用的版本。默认取自 git-describe。
     - ``-DPOLYSPACE_PROG_VERSION=v1.0b-28f023``
