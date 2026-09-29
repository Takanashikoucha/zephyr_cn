.. _icstat:

IAR
C-STAT
支持
##################

`IAR
C-STAT
<https://iar.com/cstat>`__
是
一
个
综合
的
C/C++
源
代码
静态
分析
工具。
它
可以
发现
错误
和
漏洞，
支持
MISRA
C、MISRA
C++、CERT
C/C++
和
CWE
等
一
系列
编码
标准。

安装
IAR
C-STAT
*********************

IAR
C-STAT
随
IAR
Build
Tools
和
IAR
Embedded
Workbench
预装。
参考
你
各自
产品
的
文档
获取
细节。

用
IAR
C-STAT
构建
************************

要
运行
IAR
C-STAT，
你
需要
CMake
4.1.0
或
更高
版本。
用
:ref:`west
build
<west-building>`
构建
时
追加
额外
参数
选择
IAR
C-STAT
``-DZEPHYR_SCA_VARIANT=iar_c_stat``，
例如

.. zephyr-app-commands::
   :zephyr-app:
   samples/basic/blinky
   :board:
   stm32f429ii_aca
   :gen-args:
   -DZEPHYR_SCA_VARIANT=iar_c_stat
   :goals:
   build
   :compact:

配置
IAR
C-STAT
***********************

IAR
C-STAT
接受
参数
自定义
分析。
以下
表格
列出
支持
的
选项。

.. list-table::
   :header-rows:
   1

   * - 参数
     - 描述
   * - ``CSTAT_RULESET``
     - 要
       使用
       的
       预定义
       规则集。
       （默认：
       ``stdchecks``，
       接受
       值：
       ``all,cert,misrac2004,misrac2012,misrac++2008,stdchecks,security``）
   * - ``CSTAT_ANALYZE_THREADS``
     - 分析
       中
       使用
       的
       线程
       数。
       （默认：
       <CPU
       数>）
   * - ``CSTAT_ANALYZE_OPTS``
     - 直接
       传递
       给
       ``analyze``
       命令
       的
       参数。
       （例如
       ``--timeout=900;--deterministic;--fpe``）
   * - ``CSTAT_DB``
     - 覆盖
       C-STAT
       SQLite
       数据库
       的
       默认
       位置。
       （例如
       ``/home/user/cstat.db``）
   * - ``CSTAT_CLEANUP``
     - 对
       C-STAT
       SQLite
       数据库
       执行
       清理。
       （例如
       ``true``）
