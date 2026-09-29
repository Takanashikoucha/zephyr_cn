Firmware
########

Overview
********

这
类
drivers
提供
与
各种
service
提供
（例如
clock
management、
power
management、
pinctrl
等）
firmware
交互
的
支持。
Zephyr
当前
支持
的
firmware
列表
在
下面
总结：

.. list-table::
   :align:
   center

   * - Name
     - Vendor
     - Description
     - Documentation

   * - SCMI
     - ARM
     - System
       Control
       and
       Management
       Interface
     - `Link
       <https://developer.arm.com/documentation/den0056/latest/>`__

   * - TISCI
     - TI
     - TI
       System
       Controller
       Interface
     - `Link
       <https://software-dl.ti.com/tisci/esd/latest/index.html>`__

   * - QEMU
     FWCFG
     - QEMU
     - QEMU
       Firmware
       Configuration
     - `Link
       <https://www.qemu.org/docs/master/specs/fw_cfg.html>`__

   * - RPI
     FIRMWARE
     - Raspberry
       Pi
     - Raspberry
       Pi
       VideoCore
       Firmware
       Interface
     - `Link
       <https://github.com/raspberrypi/firmware/wiki>`__

API
Reference
*************
