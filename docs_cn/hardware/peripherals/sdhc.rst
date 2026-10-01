.. _sdhc_api:

安全数字（SD 卡）接口
###################################

Zephyr 可以通过系统的原生 SD 卡接口，或者通过 SPI（串行外设接口）与所连接的 SD 卡进行通信。某些设备还可以与 MMC（多媒体卡）设备进行通信。

应用程序可以使用 Zephyr 的 :ref:`磁盘访问 API <disk_access_api>` 将 SD 卡用作存储设备，也可以使用 Zephyr 的 SD 卡子系统直接对卡进行读写。

SD 主机控制器（SDHC）
*************************

SD 主机控制器（SDHC）是一种能够向 SD 卡发送命令的设备。这些命令可以通过系统的原生 SD 卡接口发送，也可以通过 SPI 发送。

应用程序通常不应直接使用 SD 主机控制器 API，而应使用 Zephyr 的 SD 卡子系统。

请求
========

SD 主机控制器（SDHC）API 的核心是 :c:func:`sdhc_request` API。请求包含一个 :c:struct:`sdhc_command` 命令结构和一个可选的 :c:struct:`sdhc_data` 数据结构。调用方可以检查返回码，或检查 SD 命令结构的 ``response`` 字段，以判断 SDHC 请求是否成功。数据结构允许调用方指定要传输的块数，以及用于读取或写入这些块的缓冲区位置。所提供的缓冲区是用于发送数据还是读取数据，取决于所提供的命令操作码（opcode）。

主机控制器 I/O
===================

:c:func:`sdhc_set_io` API 允许用户更改 SD 主机控制器的 I/O 设置，例如时钟频率、I/O 电压和卡供电。并非所有控制器都支持应用所有 I/O 设置。例如，SPI 模式控制器通常无法切换 SD 卡的供电。

相关配置选项：

* :kconfig:option:`CONFIG_SDHC`

API 参考
*************

.. doxygengroup:: sdhc_interface
