.. _disk_access_api:

磁盘访问
###########

概述
********

磁盘访问 API 提供对存储设备的访问。

初始化磁盘
******************

由于许多磁盘设备（如 SD 卡）是可热插拔的，磁盘访问
API 提供用于初始化和反初始化磁盘的 IOCTL。它们
如下：

* :c:macro:`DISK_IOCTL_CTRL_INIT`：初始化磁盘。必须在
  磁盘设备上可以执行其他 I/O 操作之前调用。
  等效于调用旧函数 :c:func:`disk_access_init`。

* :c:macro:`DISK_IOCTL_CTRL_DEINIT`：反初始化磁盘。一旦发出此 IOCTL，
  在磁盘可用于其他 I/O 操作之前，
  必须先发出 :c:macro:`DISK_IOCTL_CTRL_INIT`。

初始化/反初始化 IOCTL 调用是配对的，因此磁盘不会反初始化，
直到发出的反初始化 IOCTL 数量与初始化 IOCTL 数量相同。

也可以通过向
:macro:`DISK_IOCTL_CTRL_DEINIT` IOCTL 传递一个设置为 ``true`` 的布尔值指针
来强制反初始化磁盘。这是一个不安全操作，
每个磁盘驱动程序可能以不同方式处理，但它始终返回
表示成功的值。

请注意，反初始化磁盘是低级操作——通常
反初始化和初始化调用应留给文件系统
实现，用户应用程序不需要手动
反初始化磁盘，而可以调用 :c:func:`fs_unmount`

SD 卡支持
***************

Zephyr 支持一些 SD 卡控制器，并支持通过 SPI
连接 SD 卡。这些驱动程序使用磁盘驱动程序接口，文件系统
可以通过磁盘访问 API 访问 SD 卡。
同时支持标准 SD 卡和高容量 SD 卡。

.. note:: FAT 文件系统不是电源安全的，如果丢失电源
   或在未卸载文件系统的情况下移除卡，文件系统可能
   损坏

SD 存储卡子系统
========================

Zephyr 通过磁盘驱动程序 API 或 SDMMC
子系统支持 SD 存储卡。该子系统可以通过磁盘驱动程序 API 透明使用，
但也支持对卡进行直接块级访问。SDMMC 子系统
与 :ref:`sd host controller api <sdhc_api>` 交互，以
与连接的 SD 卡通信。


通过 SPI 支持 SD 卡
=======================

下面的设备树片段示例展示了如何将 SD 卡节点添加到 ``spi1``
接口。示例使用引脚 ``PA27`` 作为片选，并在 SD 卡
初始化后以 24 MHz 运行 SPI 总线：

.. code-block:: devicetree

    &spi1 {
            status = "okay";
            cs-gpios = <&porta 27 GPIO_ACTIVE_LOW>;

            sdhc0: sdhc@0 {
		    compatible = "zephyr,sdhc-spi-slot";
                    reg = <0>;
                    status = "okay";
		    mmc {
			compatible = "zephyr,sdmmc-disk";
                        disk-name = "SD";
			status = "okay";
		    };
                    spi-max-frequency = <24000000>;
            };
    };

SD 卡会在板启动时由
文件系统驱动程序自动检测和初始化。

要读写文件和目录，请参见 :zephyr_file:`include/zephyr/fs/fs.h` 中的 :ref:`file_system_api`，
例如 :c:func:`fs_open()`、
:c:func:`fs_read()` 和 :c:func:`fs_write()`。

eMMC 设备支持
*******************

Zephyr 还支持使用磁盘访问 API 的 eMMC 设备。
Zephyr 中的 MMC 使用 SD 子系统实现，因为 MMC 总线
与 SD 总线有很多相似之处。MMC 控制器也使用
SDHC 设备驱动程序 API。

闪存分区上的模拟块设备支持
************************************************

Zephyr flashdisk 驱动程序允许将闪存内存分区用作
块设备。flashdisk 实例在设备树中定义：

.. code-block:: devicetree

    / {
        msc_disk0 {
            compatible = "zephyr,flash-disk";
            partition = <&storage_partition>;
            disk-name = "NAND";
            cache-size = <4096>;
        };
    };

:dtcompatible:`zephyr,flash-disk` 节点中指定的缓存大小应
等于后备分区的最小可擦除块大小。

NVMe 磁盘支持
================

也支持 NVMe 磁盘

.. toctree::
    :maxdepth: 1

    nvme.rst

VirtIO 块设备支持
***************************

也支持 VirtIO 块设备

.. toctree::
    :maxdepth: 1

    virtio_blk.rst


磁盘访问 API 配置选项
*************************************

相关配置选项：

* :kconfig:option:`CONFIG_DISK_ACCESS`

API 参考
*************

.. doxygengroup:: disk_access_interface

磁盘驱动程序配置选项
*********************************

相关驱动程序配置选项：

* :kconfig:option:`CONFIG_DISK_DRIVERS`

磁盘驱动程序接口
*********************

.. doxygengroup:: disk_driver_interface
