.. _ota:

Over-the-Air Update
###################

Overview
********

Over-the-Air (OTA) Update 为用
network connection 向 remote
devices 交付 firmware updates 的方法。虽然名称暗示
wireless
connection（通过 wired connection（如 Ethernet）接收的
updates 仍通常被称为 OTA updates。此方法需
server
infrastructure 来 host firmware binary 并实现
update 可用时的 signaling 方法。Security 是 OTA updates 的
concern；firmware
binaries 应被
cryptographically signed 并在升级前验证。

:ref:`dfu` section 讨论用 MCUboot 升级
Zephyr firmware。相同方法可作为
OTA 的一部分使用。Binary 首先被
下载到未占用的 code partition（通常命名为 ``slot1_partition``）（然后
用 :ref:`mcuboot` process 升级。

Examples of OTA
***************

Golioth
=======

`Golioth`_ 为包含 OTA updates 的 IoT management platform。Devices
配置为观察 Golioth Cloud 上可用的 firmware revisions。
有新 version 可用时（device 下载并 flash
binary。此
implementation 中（cloud 与 device 间的 connection 用
TLS/DTLS 保护（且
signed firmware binary 在升级发生前由
MCUboot 确认。

1. 可用的 sample 可在 `Golioth Firmware SDK repository`_ 找到
2. `Golioth OTA documentation`_ 包含关于
   versioning process 的完整 information

Plain HTTP download
===================

:ref:`fota_http` library 从任何 HTTP server 获取
signed image（
写入 secondary slot 并请求 swap。无需 management
protocol 或专用 update server。MCUboot 在
升级发生前验证 image
signature。

Zephyr
:zephyr:code-sample-category:`mgmt` section 包含
:zephyr:code-sample:`fota-http` sample。

Eclipse hawkBit™
================

`Eclipse hawkBit™`_ 为用
polling 检测 firmware updates 的 REST api 的 update server framework。检测
到新 update 时（binary
被下载并安装。MCUboot 可用于
升级 firmware 前验证
signature。

Zephyr
:zephyr:code-sample-category:`mgmt` section 包含
:zephyr:code-sample:`hawkbit-api` sample。

UpdateHub
=========

`UpdateHub`_ 为远程更新
embedded devices 的 platform。Updates 可
手动触发或通过 polling 监控。检测
到新 update 时（binary
被下载并安装。MCUboot 可用于
升级 firmware 前验证
signature。

Zephyr
:zephyr:code-sample-category:`mgmt` section 包含
:zephyr:code-sample:`updatehub-fota` sample。

SMP Server
==========

Simple Management Protocol (SMP) server 可用于通过
Bluetooth Low Energy (LE) 或 UDP 更新
firmware。:ref:`mcu_mgr` 用于向
remote device 发送
signed
firmware binary（其在升级发生前由
MCUboot 验证。

Zephyr
:zephyr:code-sample-category:`mgmt` section 包含
:zephyr:code-sample:`smp-svr` sample。

Lightweight M2M (LwM2M)
=======================

:ref:`lwm2m_interface` protocol 包含
:kconfig:option:`CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT` 的 firmware update 支持。Devices
用 DTLS 安全连接到
LwM2M server。有
:zephyr:code-sample:`lwm2m-client` sample（但
其不演示 firmware update feature。

mender-mcu
==========

`mender-mcu`_ 通过
与 Zephyr 集成（使
resource-constrained devices 上的 robust firmware updates 成为可能。其实现
Update Module interface（并提供
与 MCUboot 集成的默认 Update Module（以提供
A/B updates。
这允许 microcontroller units (MCUs) 执行原子、
fail-safe 的 OTA
updates（失败时自动 rollback。

集成细节和示例参见 :ref:`external_module_mender_mcu`。

Memfault and nRF Cloud powered by Memfault
==========================================

`Memfault`_ 为包含
OTA management 的 IoT observability platform。Devices
周期性向
Memfault 的 service check-in 以获取 OTA update（且
update 可用时（下载并
install
binary。

总体集成细节和
示例参见 :ref:`external_module_memfault_firmware_sdk`。

.. _MCUboot bootloader: https://mcuboot.com/
.. _Golioth: https://golioth.io/
.. _Golioth Firmware SDK repository: https://github.com/golioth/golioth-firmware-sdk/tree/main/examples/zephyr/fw_update
.. _Golioth OTA documentation: https://docs.golioth.io/device-management/ota
.. _Eclipse hawkBit™: https://www.eclipse.org/hawkbit/
.. _UpdateHub: https://updatehub.io/
.. _mender-mcu: https://github.com/mendersoftware/mender-mcu
.. _Memfault: https://memfault.com/
