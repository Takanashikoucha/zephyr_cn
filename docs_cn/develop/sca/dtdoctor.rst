.. _dtdoctor:

Devicetree
诊断
（``dtdoctor``）
#####################################

``dtdoctor``
是
一
个
静态
分析
工具，
帮助
诊断
与
Devicetree
相关
的
构建
错误。

它
拦截
编译器
和
链接器
的
错误
消息，
当
它们
引用
未
解析
的
Devicetree
设备
符号
（例如
``__device_dts_ord_*``）
时，
提供
关于
可能
导致
错误
的
原因
和
如何
修复
的
详细
信息。

使用
dtdoctor
**************

要
启用
``dtdoctor``，
用
``-DZEPHYR_SCA_VARIANT=dtdoctor``
构建。

例如：

.. code-block:: shell

   west
   build
   -b
   reel_board
   samples/basic/blinky
   --
   -DZEPHYR_SCA_VARIANT=dtdoctor
