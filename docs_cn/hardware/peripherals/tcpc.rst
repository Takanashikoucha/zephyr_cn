.. _tcpc_api:

USB Type-C 端口控制器（TCPC）
#############################

概述
********

`TCPC <tcpc-specification_>`_（USB Type-C 端口控制器）
TCPC 是一种用于简化 USB-C 系统实现的设备，它提供以下三个功能：

* VBUS 和 VCONN 控制 `USB Type-C <usb-type-c-specification_>`_：
  TCPC 可为 Source（电源输出方）设备提供控制 VBUS 输出的机制，为 Sink（电源接收方）设备提供控制 VBUS 接收的机制。类似机制也用于 VCONN 控制。

* CC 控制与检测：
  TCPC 实现了控制 CC 引脚上拉和下拉电阻的逻辑。它还提供了检测并报告 CC 引脚上存在哪些电阻的方法。

* 电源传输（Power Delivery）消息的接收与发送 `USB Power Delivery <usb-pd-specification_>`_：
  TCPC 发送和接收由 TCPM 构建的消息，并将其放到 CC 线路上。

.. _tcpc-api:

TCPC API
========

TCPC 设备驱动程序充当 TCPC 设备与应用软件之间的中间层；这通过设备驱动程序提供的 Zephyr API 实现，该 API 用于与 TCPC 设备通信并控制它。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_USBC_TCPC_DRIVER`

API 参考
*************

.. doxygengroup:: usb_type_c
.. doxygengroup:: usb_type_c_port_controller_api
.. doxygengroup:: usb_power_delivery

.. _tcpc-specification:
   https://www.usb.org/document-library/usb-type-cr-port-controller-interface-specification

.. _usb-type-c-specification:
   https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-revision-21

.. _usb-pd-specification:
   https://www.usb.org/document-library/usb-power-delivery
