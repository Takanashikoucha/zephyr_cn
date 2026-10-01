.. _arm_scmi:

ARM 系统控制与管理接口
###############################

概述
********

系统控制与管理接口（SCMI）是 ARM 制定的一项规范，描述了一组与操作系统无关的软件接口，用于执行系统管理（例如：时钟控制、pinctrl 等等）。在此上下文中，Zephyr 充当一个 SCMI 代理。

.. note::

    Zephyr 的实现可能仅包含本文档中提到的部分功能或特性。

标准协议
******************

支持的**标准** [#]_ 协议集合总结如下：

.. list-table::
    :align: center

    * - ID
      - 名称
      - 支持的版本

    * - 0x10
      - 基础协议
      - 2.1

    * - 0x11
      - 电源域管理协议
      - 3.1

    * - 0x12
      - 系统电源管理协议
      - 2.1

    * - 0x14
      - 时钟管理协议
      - 3.0

    * - 0x19
      - 引脚控制协议
      - 1.0

传输层
**********

支持的传输层总结如下：

.. list-table::
    :align: center

    * - 名称
      - 说明
      - 兼容值

    * - MBOX
      - 基于 mailbox 门铃的共享内存
      - :dtcompatible:`arm,scmi`

    * - SMC
      - 基于 SMC 门铃的共享内存
      - :dtcompatible:`arm,scmi-smc`

厂商扩展
*****************

SCMI 规范允许厂商引入额外的协议，并针对某些情况下平台固件的行为方式提供一定的自由度。在本文档的上下文中，这些内容统称为**厂商扩展**。

NXP
===

NXP 提供了一个符合 SCMI 的平台固件，称为 **System Manager (SM)**。其文档可 `在此 <https://github.com/nxp-imx/imx-sm>`__ 找到。

支持的 NXP 专属协议总结如下：

.. list-table::
    :align: center

    * - ID
      - 名称
      - 支持的版本

    * - 0x82
      - CPU
      - 1.0

支持的 NXP 专属特殊处理（quirk）总结如下：

#. 根据平台固件的配置方式不同，共享内存中的消息可能包含一个由固件在每次接收消息时进行校验的 CRC 字段。参见 :kconfig:option:`CONFIG_ARM_SCMI_NXP_VENDOR_EXTENSIONS`。

.. rubric:: 脚注

.. [#] 指 SCMI 规范所涵盖的协议。
