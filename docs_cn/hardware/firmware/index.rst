固件
########

概述
********

这类驱动程序提供支持，用于与各种提供服务的固件（例如时钟管理、电源管理、引脚控制等）进行交互。Zephyr 当前支持的固件列表总结如下：

.. list-table::
   :align: center

   * - 名称
     - 供应商
     - 描述
     - 文档

   * - SCMI
     - ARM
     - 系统控制与管理接口
     - `链接 <https://developer.arm.com/documentation/den0056/latest/>`__

   * - TISCI
     - TI
     - TI 系统控制器接口
     - `链接 <https://software-dl.ti.com/tisci/esd/latest/index.html>`__

   * - QEMU FWCFG
     - QEMU
     - QEMU 固件配置
     - `链接 <https://www.qemu.org/docs/master/specs/fw_cfg.html>`__

   * - RPI FIRMWARE
     - Raspberry Pi
     - Raspberry Pi VideoCore 固件接口
     - `链接 <https://github.com/raspberrypi/firmware/wiki>`__

API 参考
*************

通常，固件驱动程序旨在为其他类别的驱动程序提供功能。此外，不同固件的目的和功能可能各不相同。因此，这类驱动程序不实现供最终用户使用的标准 API。

示例
*******

参见 :zephyr:code-sample-category:`firmware`。

资源
*********

.. toctree::
   :maxdepth: 1

   arm-scmi
