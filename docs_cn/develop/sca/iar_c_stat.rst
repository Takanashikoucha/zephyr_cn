.. _icstat:

IAR C-STAT 支持
##################

`IAR C-STAT <https://iar.com/cstat>`__ 是一款面向 C/C++ 源代码的综合静态分析工具。
它可以发现错误和漏洞，支持多种编码标准，
如 MISRA C、MISRA C++、CERT C/C++ 和 CWE。

安装 IAR C-STAT
*********************

IAR C-STAT 随 IAR 构建工具和 IAR 嵌入式工作台预装提供。
请参阅相应产品的文档了解细节。

使用 IAR C-STAT 构建
************************

要运行 IAR C-STAT，需要 CMake 4.1.0 或更高版本。
使用 :ref:`west build <west-building>` 构建时，
添加参数 ``-DZEPHYR_SCA_VARIANT=iar_c_stat`` 以选择 IAR C-STAT，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/blinky
   :board: stm32f429ii_aca
   :gen-args: -DZEPHYR_SCA_VARIANT=iar_c_stat
   :goals: build
   :compact:

配置 IAR C-STAT
***********************

IAR C-STAT 接受用于定制分析的参数。
下表列出了支持的选项。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``CSTAT_RULESET``
     - 要使用的预定义规则集。（默认：``stdchecks``，接受值：``all,cert,misrac2004,misrac2012,misrac++2008,stdchecks,security``）
   * - ``CSTAT_ANALYZE_THREADS``
     - 分析中使用的线程数。（默认：<CPU 数量>）
   * - ``CSTAT_ANALYZE_OPTS``
     - 直接传递给 ``analyze`` 命令的参数。（例如 ``--timeout=900;--deterministic;--fpe``）
   * - ``CSTAT_DB``
     - 覆盖 C-STAT SQLite 数据库的默认位置。（例如 ``/home/user/cstat.db``）
   * - ``CSTAT_CLEANUP``
     - 对 C-STAT SQLite 数据库执行清理。（例如 ``true``）

这些参数可以在命令行上传递，也可以作为环境变量设置。
下面是一个按需启用并组合非标准规则集的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/blinky
   :board: stm32f429ii_aca
   :gen-args: -DZEPHYR_SCA_VARIANT=iar_c_stat -DCSTAT_RULESET=misrac2012,cert
   :goals: build
