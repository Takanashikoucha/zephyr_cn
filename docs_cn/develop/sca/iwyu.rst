.. _iwyu:

include-what-you-use
（IWYU）
支持
###################################

`include-what-you-use
<https://include-what-you-use.org/>`__
（IWYU）
是
一
个
构建
在
Clang
和
LLVM
之上
的
工具，
分析
C
和
C++
源
文件
中
的
``#include``
指令。
对
每个
翻译
单元
它
报告
被
包含
但
未
使用
的
头
文件，
以及
被
使用
但
其
定义
头
文件
只
被
传递
包含
的
符号。
遵循
其
建议
保持
包含
集
最
小
且
显式。

安装
include-what-you-use
*******************************

``include-what-you-use``
由
大多数
Linux
发行版
分发，
在
ubuntu
上：

.. code-block:: shell

   sudo
   apt-get
   install
   iwyu

确保
``include-what-you-use``
二进制
文件
在
你
的
:envvar:`PATH`
中
可用。

运行
include-what-you-use
************************

.. note::

   IWYU
   构建
   在
   Clang
   上，
   因此
   用
   LLVM
   工具链
   构建
   产生
   最
   准确
   的
   结果。

要
运行
include-what-you-use，
:ref:`west
build
<west-building>`
应该
被
调用
带
``-DZEPHYR_SCA_VARIANT=iwyu``
参数，
例如

.. zephyr-app-commands::
   :zephyr-app:
   samples/hello_world
   :board:
   native_sim
   :gen-args:
   -DZEPHYR_SCA_VARIANT=iwyu
   :goals:
   build
   :compact:

分析
与
每个
源
文件
的
编译
同时
运行，
建议
的
包含
更改
被
打印
到
构建
输出
（stderr）。

配置
include-what-you-use
********************************

include-what-you-use
可以
用
特定
选项
控制。
参考
`IWYU
documentation
<https://github.com/include-what-you-use/include-what-you-use/blob/master/README.md>`__
获取
完整
的
选项
列表。
