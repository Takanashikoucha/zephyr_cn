.. _cs_trace_defmt:

ARM Coresight Trace Deformatter
###############################

Formatter 是一种将多个跟踪流（trace stream，由 7 位 ID 指定）封装为
单个输出流的方法。Formatter 使用 16 字节帧（frame），每帧封装最多 15 字节的
数据。例如，ETR（Embedded Trace Router，嵌入式跟踪路由器）就使用了它，ETR 是一个环形 RAM
缓冲区，可以存储来自各种跟踪流的数据。通常跟踪数据
由主机（host）离线解码，但 deformatter 可以在芯片上（on-chip）使用，在
应用程序运行期间解码数据。

用法
*****

Deformatter 通过用户回调函数初始化。数据使用
:c:func:`cs_trace_defmt_process` 以 16 字节块为单位进行解码。每当流发生变化或
到达块末尾时都会调用回调函数。回调函数包含流 ID 和
数据。

API 文档
*****************

.. doxygengroup:: cs_trace_defmt
