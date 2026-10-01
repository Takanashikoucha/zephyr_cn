.. _pulse_io_api:

脉冲 IO
########

概述
********

脉冲 IO 子系统为在单个 GPIO 线上
生成和捕获定时数字边沿的硬件
提供厂商无关的 API。若干 MCU
系列以不同名称提供用于此目的的
专用外设。脉冲 IO 抽象该硬件类，
使客户端驱动程序（如可寻址 LED
灯带、红外发射和接收、步进脉冲
生成、频率和占空比测量，以及
单线风格协议）可以绑定一次并
在任何提供后端的 SoC 上运行。

相关配置选项：

* :kconfig:option:`CONFIG_PULSE_IO`

提交模式
****************

通道在配置时锁定到一种提交模式，
从后端通过其能力通告的模式中选择。

``PULSE_IO_MODE_SYMBOL``
   应用提交 :c:struct:`pulse_symbol` 数组，
   每个携带显式电平和以配置的分辨率
   的节拍为时长的持续时间。连续符号
   可以有任意、无关的持续时间。用于
   边沿长度在一个流内变化的协议，
   如红外遥控器、单线和步进加速斜坡。

``PULSE_IO_MODE_CELL``
   应用提交 :c:struct:`pulse_cell` 数组。
   每个单元有相同期，在通道配置中
   设置一次，每个单元携带该周期内的
   电平或占空比值。用于自然周期性流，
   其中只有每周期的电平或占空比变化，
   如可寻址 LED 位整形或可变占空比 PWM。
   对于这些情况，单元比符号更节省内存。

后端在 :c:struct:`pulse_io_caps` 中通告
支持的模式。请求不支持的模式导致
:c:func:`pulse_io_channel_configure`
返回 ``-ENOTSUP``。

配置
*************

客户端在探测时查询
:c:func:`pulse_io_get_capabilities`
以决定使用哪种模式和特性集，
用 :c:func:`pulse_io_channel_get` 保留通道，
并在任何传输前用
:c:func:`pulse_io_channel_configure` 配置它。
阻塞传输使用 :c:func:`pulse_io_transmit_sync`
和 :c:func:`pulse_io_receive_sync`；
异步和流式传输使用 RTIO 路径。

字节到符号辅助函数
:c:func:`pulse_io_encode_bytes` 及其逆函数
:c:func:`pulse_io_decode_bytes`
用每比特模板在协议字节流和
脉冲符号之间转换。

RTIO
****

后端可以可选地与 :ref:`rtio` 集成，
暴露 iodev 提交路径以及通过
:c:func:`pulse_io_get_encoder` 和
:c:func:`pulse_io_get_decoder` 获取的
编码器和解码器虚表。用 RTIO，
客户端将载荷编码到符号缓冲区，
通过 RTIO 队列提交，并解码任何
捕获的回复，获得排队和链式传输、
流式接收，以及 RTIO 框架提供的
用户空间路径。RTIO 操作是可选的；
未实现它们的后端将对应驱动程序
API 成员留为 ``NULL``，
访问器返回 ``-ENOSYS``。

API 参考
*************

.. doxygengroup:: pulse_io_interface