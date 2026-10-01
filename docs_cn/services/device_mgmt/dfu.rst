.. _dfu:

Device Firmware Upgrade
#######################

Overview
********

Device Firmware Upgrade subsystem 提供
runtime 升级 Zephyr-based application image 所需 frameworks。其当前
由两个不同 modules 组成：

* :zephyr_file:`subsys/dfu/boot/`: 与 bootloaders 的 interface code
* :zephyr_file:`subsys/dfu/img_util/`: Image management code

DFU subsystem 处理 image management（但不处理将 image 发送到
target
device 所需的 transport 或 management protocols 本身。关于这些 protocols 和 frameworks 的信息参见
:ref:`device_mgmt` section。

.. _flash_img_api:

Flash Image
===========

Flash image API 作为 Device Firmware Upgrade (DFU) subsystem
的一部分（在 Flash Stream 之上提供抽象（以简化
firmware
image chunks 写入 flash。

API Reference
-------------

.. doxygengroup:: flash_img_api

.. _mcuboot_api:

MCUBoot API
===========

MCUBoot API 提供获取
application images 的 version 信息和 boot status。其允许选择
下一 boot 的 application image 和 boot type。

API Reference
-------------

.. doxygengroup:: mcuboot_api

Bootloaders
***********

.. _mcuboot:

MCUBoot
=======

Zephyr 与开源、跨 RTOS 的
`MCUboot boot loader`_ 直接兼容。其与 MCUboot 交互（并
知晓其所需的 image
format（因此当 MCUboot
为与 Zephyr 一起使用的 boot loader 时 Device Firmware Upgrade 可用。Source code 本身托管在
`MCUboot GitHub Project`_ page。

要用 MCUboot 与 Zephyr（须考虑以下：

1. 须定义 MCUboot 所需的 flash partitions；细节
   参见 :ref:`flash_map_api`。
2. 须将 flash partition 指定为 chosen code partition

.. code-block:: devicetree

   / {
      chosen {
         zephyr,code-partition = &slot0_partition;
      };
   };

3. Application 的 :file:`.conf` file 须启用
   :kconfig:option:`CONFIG_BOOTLOADER_MCUBOOT` Kconfig option（使 Zephyr
   以 MCUboot-compatible 方式构建
4. 须构建并将 MCUboot 本身刷入 device
5. 可能须采取措施避免 mass erase flash（且
   在正确 offset（bootloader 正后方）刷入
   Zephyr application image

关于 MCUboot 与 Zephyr 使用的更详细信息
可
在 MCUboot 网站的 `MCUboot with Zephyr`_ documentation page 找到。

.. _MCUboot boot loader: https://mcuboot.com/
.. _MCUboot with Zephyr: https://docs.mcuboot.com/readme-zephyr
.. _MCUboot GitHub Project: https://github.com/runtimeco/mcuboot
