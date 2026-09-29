.. _cpptest:

Parasoft
C/C++test
支持
##########################

Parasoft
`C/C++test
<https://www.parasoft.com/products/parasoft-c-ctest/>`__
是
C
和
C++
的
软件
测试
和
静态
分析
工具。
它
是
商业
软件
你
必须
获取
商业
许可
才能
使用
它。

C/C++test
的
文档
可以
找到
在
https://docs.parasoft.com/。
请参考
文档
了解
如何
使用
它。

生成
Build
Data
Files
***************************

要
使用
C/C++test，
``cpptestscan``
必须
在
你
的
:envvar:`PATH`
环境
变量
中
找到。
并且
:ref:`west
build
<west-building>`
应该
带
``-DZEPHYR_SCA_VARIANT=cpptest``
参数
调用，
例如

.. code-block:: shell

   west
   build
   -b
   qemu_cortex_m3
   zephyr/samples/hello_world
   --
   -DZEPHYR_SCA_VARIANT=cpptest

``.bdf``
文件
将
被
生成
为
:file:`build/sca/cpptest/cpptestscan.bdf`。

生成
报告
文件
************************

请参考
Parasoft
C/C++test
文档
获取
更多
细节。

要
导入
并
生成
报告
文件，
类似
以下
的
东西
应该
工作。

.. code-block:: shell

   cpptestcli
   -data
   out
   -localsettings
   local.conf
   -bdf
   build/sca/cpptest/cpptestscan.bdf
   -config
   "builtin://Recommended
   Rules"
   -report
   out/report

你
可能
需要
将
``bdf.import.c.compiler.exec``、
``bdf.import.cpp.compiler.exec``
和
``bdf.import.linker.exec``
设置
为
工具链
:ref:`west
build
<west-building>`
使用
的
那
个。
