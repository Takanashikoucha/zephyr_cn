.. _dtdoctor:

设备树诊断（``dtdoctor``）
#####################################

``dtdoctor`` 是一个帮助诊断 Devicetree 相关构建错误的静态分析工具。

它拦截来自编译器和链接器的错误消息，当它们指到未解析的 Devicetree 设备符号（例如 ``__device_dts_ord_*``）时，提供关于什么可能导致错误以及如何修复的详细信息。

使用 dtdoctor
**************

要启用 ``dtdoctor``，用 ``-DZEPHYR_SCA_VARIANT=dtdoctor`` 构建。

例如：

.. code-block:: shell

   west build -b reel_board samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=dtdoctor
