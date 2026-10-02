.. _dfu:

Device Firmware Upgrade
#######################

概述
********

设备固件升级（Device Firmware Upgrade）子系统提供了在运行时升级基于 Zephyr 的应用程序映像所需的框架。它目前由两个不同的模块组成：

* :zephyr_file:`subsys/dfu/boot/`：与引导加载程序的接口代码
* :zephyr_file:`subsys/dfu/img_util/`：映像管理代码

DFU 子系统处理映像管理，但不处理将映像发送到目标设备所需的传输协议或管理协议本身。关于这些协议和框架的信息，请参阅
:ref:`device_mgmt` 章节。

.. _flash_img_api:

Flash Image
===========

Flash 映像 API 是设备固件升级（DFU）子系统的一部分，
它在 Flash Stream 之上提供一层抽象，以简化将固件
映像块写入 flash 的操作。

API 参考
-------------

.. doxygengroup:: flash_img_api

.. _mcuboot_api:

MCUBoot API
===========

MCUBoot API 用于获取应用程序映像的版本信息和引导状态。
它允许为下一次引导选择应用程序映像和引导类型。

API 参考
-------------

.. doxygengroup:: mcuboot_api

引导加载程序
***********

.. _mcuboot:

MCUBoot
=======

Zephyr 与开源、跨 RTOS 的
`MCUboot 引导加载程序`_ 直接兼容。它与 MCUboot 进行交互，
并了解其所需的映像格式，因此当使用 MCUboot
作为 Zephyr 的引导加载程序时，设备固件升级功能可用。其源代码本身托管在
`MCUboot GitHub 项目`_ 页面。

要在 Zephyr 上使用 MCUboot，需要考虑以下几点：

1. 需要定义 MCUboot 所需的 flash 分区；详见
   :ref:`flash_map_api`。
2. 需要指定你的 flash 分区为所选的代码分区

.. code-block:: devicetree

   / {
      chosen {
         zephyr,code-partition = &slot0_partition;
      };
   };

3. 你的应用程序的 :file:`.conf` 文件需要启用
   :kconfig:option:`CONFIG_BOOTLOADER_MCUBOOT` Kconfig 选项，以便 Zephyr
   以 MCUboot 兼容的方式构建
4. 需要构建并将 MCUboot 本身刷入你的设备
5. 可能需要采取措施避免批量擦除 flash，并且
   在正确的偏移处（紧跟在
   引导加载程序之后）刷入
   Zephyr 应用程序映像

关于在 Zephyr 上使用 MCUboot 的更详细信息
可以在 MCUboot 网站上的 `MCUboot with Zephyr`_ 文档页面找到。

.. _MCUboot boot loader: https://mcuboot.com/
.. _MCUboot with Zephyr: https://docs.mcuboot.com/readme-zephyr
.. _MCUboot GitHub Project: https://github.com/runtimeco/mcuboot
