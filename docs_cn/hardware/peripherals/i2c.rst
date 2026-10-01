.. _i2c_api:

I2C（Inter-Integrated Circuit，集成电路总线）
##################################

概述
********

.. note::

   Zephyr I2C API 中使用的术语遵循
   `NXP I2C 总线规范 Rev 7.0 <i2c-specification_>`_。
   自 2021 年 10 月 1 日该版本发布起，术语与之前修订版有所不同。

`I2C`_（Inter-Integrated Circuit，发音为“eye squared see”）
是一种常用的双信号共享外设接口总线。许多片上系统（SoC）方案提供
可在 I2C 总线上通信的控制器。总线上的设备可以扮演两种角色：
作为发起事务并控制时钟的“控制器”，
或作为响应事务命令的“目标”。
给定 SoC 上的 I2C 控制器通常支持控制器角色，
有些还支持目标模式。Zephyr 为两种角色都提供了 API。

.. _i2c-controller-api:

I2C 控制器 API
==================

当 I2C 外设控制总线（特别是起始和停止条件以及时钟）时，
使用 Zephyr 的 I2C 控制器 API。
这是最常用的模式，用于与传感器和串行存储器等 I2C 设备交互。

该 API 受所有树内 I2C 外设驱动支持，并被视为稳定。

.. _i2c-target-api:

I2C 目标 API
==============

当 I2C 外设响应由总线上另一个控制器发起的事务时，
使用 Zephyr 的 I2C 目标 API。
它可用于由另一设备（如主机处理器）控制传感器角色的 Zephyr 应用。

该 API 仅受极少数树内 I2C 外设驱动支持。
它被视为实验性 API，因为它与以控制器模式支持的所有 I2C 外设的能力不兼容。


配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_I2C`
* :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`

传输超时
================

I2C 子系统提供两种互补机制，用于控制驱动在返回 ``-ETIMEDOUT`` 之前
等待传输完成的时间。

应用级默认值（Kconfig）
-----------------------------------

:kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS` 为所有通过选择
``I2C_TRANSFER_TIMEOUT_SUPPORTED`` 加入的 I2C 控制器设置默认超时（以毫秒为单位）。
值 ``0`` 表示永远等待（``K_FOREVER``）。
不允许无限超时的驱动（例如直接将值写入硬件寄存器的驱动）
使用 :c:macro:`BUILD_ASSERT_INVALID_I2C_TRANSFER_TIMEOUT`
在构建时强制非零值。

按控制器的设备树覆盖
---------------------------

单个控制器可以通过 ``dts/bindings/i2c/i2c-controller.yaml``
中定义的 ``zephyr,transfer-timeout-ms`` 设备树属性覆盖应用级默认值。
当该属性不存在时，驱动回退到 :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`。

示例板级 overlay::

    &i2c1 {
        /* Fast sensor bus - fail quickly on a hung device */
        zephyr,transfer-timeout-ms = <50>;
    };

    &i2c2 {
        /* EEPROM bus - allow for long internal write cycles */
        zephyr,transfer-timeout-ms = <2000>;
    };

支持按实例超时的驱动使用
:c:macro:`I2C_DT_INST_TRANSFER_TIMEOUT`
（或 :c:macro:`I2C_DT_INST_TRANSFER_TIMEOUT_MS` 用于原始整数用途），
它按以下优先级解析超时：

1. 控制器节点上的 ``zephyr,transfer-timeout-ms`` 设备树属性
2. :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`
3. 当解析值为 ``0`` 时的 ``K_FOREVER``

API 参考
*************

.. doxygengroup:: i2c_interface

.. _i2c-specification:
   https://www.nxp.com/docs/en/user-guide/UM10204.pdf

.. _I2C: i2c-specification_
