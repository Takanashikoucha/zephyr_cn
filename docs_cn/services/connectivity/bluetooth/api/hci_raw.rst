.. _bt_hci_raw:


HCI RAW channel
###############

Overview
********

HCI RAW channel API 旨在将 HCI interface 暴露给 remote entity。Local Bluetooth controller 由 remote entity 拥有（且 host Bluetooth stack 不使用。RAW API 提供对 Bluetooth HCI driver 发送和接收的 packets 的直接访问。

API Reference
*************

.. doxygengroup:: hci_raw
