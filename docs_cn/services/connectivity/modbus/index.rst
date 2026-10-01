.. _modbus:

Modbus
######

Modbus 是工业 messaging protocol。该 protocol 为不同类型的 networks 或 buses 指定。Zephyr OS 实现支持通过 serial line 通信（可用于不同 physical interfaces（如 RS485 或 RS232。TCP support 未直接实现（但有 helper functions 按 application 需求实现 TCP support。

Modbus 通信基于 client/server model。总线上仅可存在一个 client。Client 可与多个 server devices 通信。Server devices 本身为 passive（且不得发送 requests 或 unsolicited responses。Client 请求的 services 由 function codes（FCxx）指定（可在 specification 或以下 API 文档中找到。

Zephyr RTOS 实现支持 client 和 server 两种 roles。

在 `MODBUS Protocol Specifications`_ 网站可找到更多关于 Modbus 和 Modbus RTU 的信息。

Samples
*******

* :zephyr:code-sample:`modbus-rtu-server` 和 :zephyr:code-sample:`modbus-rtu-client` samples 提供用 evaluation board 试用 RTU server 和 RTU client 实现的可能性。
* :zephyr:code-sample:`modbus-tcp-server` sample 为简单 Modbus TCP server。
* :zephyr:code-sample:`modbus-gateway` sample 展示如何用 Zephyr OS 构建 TCP 到 serial line 的 gateway。

API Reference
*************

.. doxygengroup:: modbus

.. _`MODBUS Protocol Specifications`: https://www.modbus.org/specs.php
