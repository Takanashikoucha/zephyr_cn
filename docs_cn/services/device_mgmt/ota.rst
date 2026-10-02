.. _ota:

Over-the-Air Update
###################

概述
********

空中下载（OTA）升级是一种通过网络连接向远程
设备交付固件更新的方法。虽然名称暗示
无线
连接，但通过有线连接（如以太网）接收的
更新仍通常被称为 OTA 升级。此方法需要
服务器
基础设施来托管固件二进制文件，并实现一种在
更新可用时发出信号的方法。安全性是 OTA 升级的
关注点；固件
二进制文件应被
加密签名并在升级前验证。

:ref:`dfu` 章节讨论使用 MCUboot 升级
Zephyr 固件。相同的方法可作为
OTA 的一部分使用。二进制文件首先被
下载到未占用的代码分区（通常命名为 ``slot1_partition``），然后
使用 :ref:`mcuboot` 流程升级。

OTA 示例
***************

Golioth
=======

`Golioth`_ 是一个包含 OTA 升级的 IoT 管理平台。设备
被配置为观察 Golioth Cloud 上可用的固件修订版本。
当有新版本可用时，设备下载并烧录
二进制文件。在
此实现中，云与设备之间的连接使用
TLS/DTLS 保护，且
签名的固件二进制文件在升级发生前由
MCUboot 确认。

1. 一个可用的示例可在 `Golioth Firmware SDK 仓库`_ 找到
2. `Golioth OTA 文档`_ 包含关于
版本管理流程的完整信息

普通 HTTP 下载
==================

:ref:`fota_http` 库从任何 HTTP 服务器获取
签名映像，
写入次要槽并请求交换。无需管理
协议或专用升级服务器。MCUboot 在
升级发生前验证映像
签名。

Zephyr
:zephyr:code-sample-category:`mgmt` 章节包含
:zephyr:code-sample:`fota-http` 示例。

Eclipse hawkBit™
================

`Eclipse hawkBit™`_ 是一个使用
轮询 REST API 来检测固件更新的升级服务器框架。检测
到新更新时，二进制文件
被下载并安装。MCUboot 可用于
在升级固件前验证
签名。

Zephyr
:zephyr:code-sample-category:`mgmt` 章节包含
:zephyr:code-sample:`hawkbit-api` 示例。

UpdateHub
=========

`UpdateHub`_ 是一个远程更新
嵌入式设备的平台。更新可
手动触发或通过轮询监控。检测
到新更新时，二进制文件
被下载并安装。MCUboot 可用于
在升级固件前验证
签名。

Zephyr
:zephyr:code-sample-category:`mgmt` 章节包含
:zephyr:code-sample:`updatehub-fota` 示例。

SMP 服务器
==========

简单管理协议（SMP）服务器可用于通过
Bluetooth Low Energy（LE）或 UDP 更新
固件。:ref:`mcu_mgr` 用于向
远程设备发送
签名
固件二进制文件，其在升级发生前由
MCUboot 验证。

Zephyr
:zephyr:code-sample-category:`mgmt` 章节包含
:zephyr:code-sample:`smp-svr` 示例。

轻量级 M2M（LwM2M）
======================

:ref:`lwm2m_interface` 协议包含
:kconfig:option:`CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT` 的固件升级支持。设备
使用 DTLS 安全连接到
LwM2M 服务器。有一个
:zephyr:code-sample:`lwm2m-client` 示例，但
其不演示固件升级功能。

mender-mcu
==========

`mender-mcu`_ 通过
与 Zephyr 集成，使
资源受限设备上的健壮固件升级成为可能。其实现
Update Module 接口，并提供
一个与 MCUboot 集成的默认 Update Module，以提供
A/B 升级。
这允许微控制器（MCU）执行原子、
防故障的 OTA
升级，失败时自动回滚。

集成细节和示例参见 :ref:`external_module_mender_mcu`。

Memfault 和由 Memfault 驱动的 nRF Cloud
==========================================

`Memfault`_ 是一个包含
OTA 管理的 IoT 可观测性平台。设备
周期性向
Memfault 的服务检查以获取 OTA 升级，且
升级可用时，下载并
安装
二进制文件。

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
