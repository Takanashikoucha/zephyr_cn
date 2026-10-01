.. _smbus_api:

系统管理总线（SMBus）
#############################

.. contents::
    :local:
    :depth: 2

概述
********

系统管理总线（SMBus）派生自 I2C，用于与主板上的设备通信。系统可以使用 SMBus 与主板上的外设通信而无需使用专用控制线。SMBus 外设可以提供各种制造商信息、报告错误、接受控制参数等。

总线上的设备可以以三种角色操作：作为控制器（发起事务并控制时钟）、外设（响应事务命令）或主机（一种专用控制器，为系统 CPU 提供主接口）。Zephyr 提供了控制器角色的 API。

SMBus 外设设备可以用两种方法与控制器发起通信：

* **主机通知协议**：支持主机通知协议的外设设备表现得像控制器来执行通知。它向特殊地址"SMBus 主机（0x08）"写入三字节消息，包含自身地址和两字节相关数据。
* **SMBALERT# 信号**：外设设备用特殊信号 SMBALERT# 向控制器请求注意。控制器需要从特殊"SMBus 警报响应地址（ARA）（0x0c）"读取一个字节。外设设备用包含自身地址的数据字节响应。

目前，API 基于 `SMBus 规范`_ 版本 2.0

.. note::
    参见 :ref:`coding_guideline_inclusive_language` 了解此 API 中使用的术语信息。

.. _smbus-controller-api:

SMBus 控制器 API
********************

当 SMBus 设备控制总线（特别是起始和停止条件以及时钟）时使用 Zephyr 的 SMBus 控制器 API。这是与 SMBus 外设交互最常用的模式。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_SMBUS`

API 参考
*************

.. doxygengroup:: smbus_interface

.. _SMBus Specification: https://smbus.org/specs/smbus20.pdf
