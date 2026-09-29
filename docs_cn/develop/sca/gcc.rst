.. _gcc:

GCC
静态
分析
支持
###########################

静态
分析
在
`GCC
<https://gcc.gnu.org/>`__
10
中
引入
并
用
选项
``-fanalyzer``
启用。
这个
选项
执行
比
传统
警告
更
昂贵
和
彻底
的
代码
分析。

运行
GCC
静态
分析
***********************

要
运行
GCC
静态
分析，
:ref:`west
build
<west-building>`
应该
被
调用
带
``-DZEPHYR_SCA_VARIANT=gcc``
参数，
例如

.. zephyr-app-commands::
   :zephyr-app:
   samples/userspace/hello_world_user
   :board:
   qemu_x86
   :gen-args:
   -DZEPHYR_SCA_VARIANT=gcc
   :goals:
   build
   :compact:

配置
GCC
静态
分析器
*******************************

GCC
静态
分析器
可以
用
特定
选项
控制。

* `控制
  分析器
  的
  选项
  <https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html>`__
* `控制
  诊断
  消息
  格式
  的
  选项
  <https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Message-Formatting-Options.html>`__

.. list-table::
   :header-rows:
   1

   * - 参数
     - 描述
   * - ``GCC_SCA_OPTS``
     - 分号
       分隔
       的
       GCC
       分析器
       选项
       列表。

这些
参数
可以
在
命令行
传递，
或
设置
为
环境变量。

.. zephyr-app-commands::
   :zephyr-app:
   samples/hello_world
   :board:
   stm32h573i_dk
   :gen-args:
   -DZEPHYR_SCA_VARIANT=gcc
   -DGCC_SCA_OPTS="-fdiagnostics-format=json;-fanalyzer-verbosity=3"
   :goals:
   build
   :compact:

.. note::

   GCC
   静态
   分析器
   正在
   积极
   开发
   中，
   每
   个
   新
   版本
   带
   新
   选项。
   这
   `页
   <https://gcc.gnu.org/wiki/StaticAnalyzer>`__
   给出
   每
   个
   新
   版本
   引入
   的
   选项
   和
   修复
   的
   概览。


分析器
最新
版本
******************************

由于
Zephyr
工具链
可能
不
包括
GCC
静态
分析器
的
最新
版本，
你
可能
需要
安装
一个
较
新
的
GCC
版本
来
获取
最新
的
分析器
选项。
