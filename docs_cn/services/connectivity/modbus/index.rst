.. _modbus:

Modbus
######

Modbus 是一种工业消息协议。该协议针对不同类型的网络或总线进行了规范。Zephyr OS
实现支持通过串行线路通信，可搭配 RS485 或 RS232 等不同物理接口使用。
TCP 支持未直接实现，但提供了辅助函数以便按应用需求实现 TCP 支持。

Modbus 通信基于客户端/服务器模型。
总线上只允许存在一个客户端。客户端可与多个
服务器设备通信。服务器设备本身是被动的，不得发送
请求或未经请求的响应。
客户端请求的服务由功能码（FCxx）指定，
可在规范或下文 API 文档中找到。

Zephyr RTOS 实现同时支持客户端和服务器角色。

有关 Modbus 和 Modbus RTU 的更多信息，可在网站
`MODBUS Protocol Specifications`_ 上找到。

示例
*******

* :zephyr:code-sample:`modbus-rtu-server` 和 :zephyr:code-sample:`modbus-rtu-client` 示例提供了
  使用评估板试用 RTU 服务器和 RTU 客户端实现的可能性。
* :zephyr:code-sample:`modbus-tcp-server` 示例是一个简单的 Modbus TCP 服务器。
* :zephyr:code-sample:`modbus-gateway` 示例展示了如何使用 Zephyr OS
  构建 TCP 到串行线路的网关。

API 参考
*************

.. doxygengroup:: modbus

.. _`MODBUS Protocol Specifications`: https://www.modbus.org/specs.php
