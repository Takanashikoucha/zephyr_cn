.. _lora_api:
.. _lorawan_api:

LoRa and LoRaWAN
################

Overview
********

LoRa（Long Range 缩写）是 `Semtech Corporation`_ 开发的专有低功耗无线 communication protocol。

LoRa 基于 chirp spread spectrum（CSS）modulation 技术作为 physical layer（PHY）。

LoRaWAN（Long Range Wide Area Network）在 LoRa PHY 上定义 networking layer。

Zephyr 提供 LoRa APIs 以直接通过 wireless interface 发送 raw data packets（以及 LoRaWAN APIs 以通过 gateway 将 end device 连接到 internet。

Zephyr 提供两个 LoRaWAN backend 实现：

* **LoRaMac-node**（默认）：基于 Semtech 的 `LoRaMac-node library`_（包含为 Zephyr module。支持 LoRaWAN specification 定义的所有 regions。用 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_LORAMAC_NODE` 选择。

* **Native**：Zephyr-idiomatic 的 LoRaWAN 1.0.x Class A 实现（直接与 LoRa radio driver 通信而无外部依赖。当前支持 EU868 region。用 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE` 选择。

.. note::

        Semtech 已弃用 ``LoRaMac-node`` 以改用 `LoRa Basics Modem`_。将 Zephyr APIs 移植为使用 ``LoRa Basics Modem`` 作为 backend 正在进行中。

        当前（仅 SX1261、SX1262、SX1272 和 SX1276 chipsets 通过 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_LORA_BASICS_MODEM` 支持基础 LoRa API。


LoRaWAN specification 由 `LoRa Alliance`_ 发布。

.. _`Semtech Corporation`: https://www.semtech.com/

.. _`LoRaMac-node library`: https://github.com/Lora-net/LoRaMac-node

.. _`LoRa Basics Modem`: https://github.com/Lora-net/SWL2001

.. _`LoRa Alliance`: https://lora-alliance.org/

Configuration Options
*********************

LoRa PHY
========

相关 configuration options 可在 :zephyr_file:`drivers/lora/Kconfig` 下找到。

* :kconfig:option:`CONFIG_LORA`

* :kconfig:option:`CONFIG_LORA_SHELL`

* :kconfig:option:`CONFIG_LORA_INIT_PRIORITY`

LoRaWAN
=======

相关 configuration options 可在 :zephyr_file:`subsys/lorawan/Kconfig` 下找到。

* :kconfig:option:`CONFIG_LORAWAN`

* :kconfig:option:`CONFIG_LORAWAN_SYSTEM_MAX_RX_ERROR`

* :kconfig:option:`CONFIG_LORAWAN_REGION_AS923`

* :kconfig:option:`CONFIG_LORAWAN_REGION_AU915`

* :kconfig:option:`CONFIG_LORAWAN_REGION_CN470`

* :kconfig:option:`CONFIG_LORAWAN_REGION_CN779`

* :kconfig:option:`CONFIG_LORAWAN_REGION_EU433`

* :kconfig:option:`CONFIG_LORAWAN_REGION_EU868`

* :kconfig:option:`CONFIG_LORAWAN_REGION_KR920`

* :kconfig:option:`CONFIG_LORAWAN_REGION_IN865`

* :kconfig:option:`CONFIG_LORAWAN_REGION_US915`

* :kconfig:option:`CONFIG_LORAWAN_REGION_RU864`

Native Backend
--------------

Native backend 用 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE` 选择（且 :zephyr_file:`subsys/lorawan/native/Kconfig` 下有额外 options：

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_ENGINE_STACK_SIZE`

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_ENGINE_PRIORITY`

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_PUBLIC_NETWORK`

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_DUTY_CYCLE`

API Reference
*************

LoRa PHY
========

.. doxygengroup:: lora_interface

LoRaWAN
=======

.. doxygengroup:: lorawan_api
