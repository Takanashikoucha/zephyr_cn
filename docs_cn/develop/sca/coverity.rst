.. _coverity:

Coverity
#########

Coverity
Scan
是
Black
Duck
提供
的
一
个
服务，
将
开源
编码
项目
的
分析
结果
提供
给
在
Coverity
Scan
注册
了
其
产品
的
开源
代码
开发者。

这个
集成
只
在
scan.coverity.com
和
通过
这个
服务
可用
的
工具
分发
上
测试
过。

生成
构建
数据
文件
***************************

要
使用
这个
集成，
coverity
工具
分发
必须
在
你
的
:envvar:`PATH`
环境
中
找到，
并且
:ref:`west
build
<west-building>`
应该
被
调用
带
``-DZEPHYR_SCA_VARIANT=coverity``
参数，
例如

.. code-block:: shell

   west
   build
   -b
   qemu_cortex_m3
   samples/hello_world
   --
   -DZEPHYR_SCA_VARIANT=coverity


扫描
结果
将
被
生成
为
:file:`build/sca/coverity`。

你
也
可以
设置
:envvar:`COVERITY_OUTPUT_DIR`
作为
多个
和
增量
扫描
结果
的
目标。

结果
分析
****************

遵循
https://scan.coverity.com
上
的
说明
上传
结果。
