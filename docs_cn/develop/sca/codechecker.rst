.. _codechecker:

CodeChecker
支持
###################

`CodeChecker
<https://codechecker.readthedocs.io/>`__
是
一个
静态
分析
基础设施。
它
执行
构建
系统
上
可用
的
分析
工具，
如
`Clang-Tidy
<https://clang.llvm.org/extra/clang-tidy/>`__、
`Clang
Static
Analyzer
<https://clang-analyzer.llvm.org/>`__
和
`Cppcheck
<https://cppcheck.sourceforge.io/>`__。
参考
分析器
的
网站
获取
安装
说明。

安装
CodeChecker
**********************

CodeChecker
本身
是
一个
在
`pypi
<https://pypi.org/project/codechecker/>`__
上
可用
的
python
包。

.. code-block:: shell

   pip
   install
   codechecker

用
CodeChecker
构建
*************************

要
运行
CodeChecker，
:ref:`west
build
<west-building>`
应该
被
调用
带
``-DZEPHYR_SCA_VARIANT=codechecker``
参数，
例如

.. code-block:: shell

   west
   build
   -b
   mimxrt1064_evk
   samples/basic/blinky
   --
   -DZEPHYR_SCA_VARIANT=codechecker


配置
CodeChecker
***********************

CodeChecker
使用
不同
的
命令
步骤，
每个
带
其
各自
的
配置
参数。
以下
表格
列出
所有
这些
选项。

.. list-table::
   :header-rows:
   1

   * - 参数
     - 描述
   * - ``CODECHECKER_ANALYZE_JOBS``
     - 分析
       中
       使用
       的
       线程
       数。
       （默认：
       <CPU
       数>）
   * - ``CODECHECKER_ANALYZE_OPTS``
     - 直接
       传递
       给
       ``analyze``
       命令
       的
       参数。
       （例如
       ``--timeout;360``）
   * - ``CODECHECKER_CLEANUP``
     - 解析/存储
       后
       执行
       清理。
       这
       将
       删除
       所有
       ``plist``
       文件。
   * - ``CODECHECKER_CONFIG_FILE``
     - 带
       配置
       选项
       的
       JSON
       或
       YAML
       文件，
       传递
       给
       所有
       命令。
   * - ``CODECHECKER_EXPORT``
     - 逗号
       分隔
       的
       报告
       类型
       列表。
       允许
       的
       类型
       是：
       ``html,json,codeclimate,gerrit,baseline``。
   * - ``CODECHECKER_NAME``
     - CodeChecker
       运行
       元数据
       名称。
       （默认：
       ``zephyr``）
   * - ``CODECHECKER_PARSE_EXIT_STATUS``
     - 默认
       情况
       下，
       CodeChecker
       识别
       的
       问题
       不
       会
       使
       构建
       失败，
       设置
       这个
       选项
       在
       分析
       期间
       失败。
   * - ``CODECHECKER_PARSE_OPTS``
     - 直接
       传递
       给
       ``parse``
       命令
       的
       参数。
