.. _usbc_vbus_api:

USB-C VBUS
##########

概述
********

USB-C VBUS 是 USB Type-C 连接中从供电端（Source）向受电端（Sink）设备输送电力的线路。

.. _usbc-vbus-api:

USB-C VBUS 接口
===============

USB-C VBUS 设备驱动程序提供了一组用于控制和测量 VBUS 的接口（API）。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_USBC_VBUS_DRIVER`

接口参考
*************

.. doxygengroup:: usbc_vbus_api