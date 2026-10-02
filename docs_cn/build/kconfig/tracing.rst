.. _kconfig_traceconfig:

跟踪值到其来源
##############################

保存到 :file:`zephyr/.config` 的合并配置包含将用户配置文件应用到整个 Kconfig
文件树的结果。这个过程可能很难跟踪，特别是当不可见符号从树的任何地方被隐式
选择时。为帮助这，``traceconfig`` 目标可以用于在构建目录中生成一个详细说明每个
符号如何得到其最终值的文件。

按通常方式构建 Zephyr 项目后，可以使用以下命令之一生成 Kconfig 跟踪：

   .. code-block:: bash

      west build -t traceconfig

   .. code-block:: bash

      ninja traceconfig

.. note::
   生成的信息只在干净构建上有用，因为否则 ``.config`` 文件"固定"所有设置到
   特定值（如 :ref:`卡住的符号 <stuck_symbols>` 中所述）。因此，推荐在生成
   跟踪前运行 :ref:`干净构建 <west-building-pristine>`。

输出将在构建目录中的 :file:`zephyr/kconfig-trace.md` 文件中。这个文件最好在
IDE 中查看以利用 Markdown 元素（表格、高亮、可点击链接），但即使直接用任何
文本编辑器打开也容易理解。

报告分为三个部分：

#. 可见符号（visible symbols）
#. 不可见符号（invisible symbols）
#. 未设置符号（unset symbols）

对于第 1 和 2 部分，呈现一个表格，其中每个符号显示其类型、名称和当前值。第四
列详细说明导致值被应用的语句类型，可以是以下之一：

 - *assigned*，当从配置文件读取显式赋值，形式为 ``CONFIG_xxx=y``；

 - *default*，当没有用户赋值，但从 Kconfig 树读取适用的默认值；

 - *selected* 或 *implied*，当来自单独符号的 ``select`` 或 ``imply`` 语句导致
   符号被设置。

第五列详细说明源语句的位置。对于前两种语句类型，提供精确位置（文件名和行号）；
在后两种情况下，它包含导致符号被设置的表达式。

最后，第 3 部分简单列出所有未定义符号。这些没有附加信息，因为它们从未通过
上述任何方式接收值。
