.. _cbor_api:

CBOR
####

`CBOR <https://cbor.io/>`_（Concise Binary Object Representation，简洁二进制对象表示）是一种数据格式，其设计目标包括极小的代码尺寸可能性、相当小的消息尺寸，以及无需版本协商即可扩展。

Zephyr 通过 `zcbor`_ 库提供对 CBOR 的支持，该库作为 West 模块引入。

配置
*************

要启用 CBOR 支持，请启用 :kconfig:option:`CONFIG_ZCBOR` Kconfig 选项。

API 参考
*************

zcbor 库提供自己的 API 文档，请参考它获取更多信息。

.. _`zcbor`: https://github.com/zephyrproject-rtos/zcbor
