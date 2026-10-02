.. _disk_nvme:

NVMe
####

NVMe 是 PCIe 总线上的标准化逻辑设备接口，用于暴露存储设备。

支持 NVMe 控制器和磁盘。磁盘可以通过它们暴露的
:ref:`Disk Access API <disk_access_api>` 访问，
从而通过 :ref:`File System API <file_system_api>` 使用。

驱动程序设计
*************

驱动程序分为 3 个主要部分：

- NVMe 控制器：:zephyr_file:`drivers/disk/nvme/nvme_controller.c`
- NVMe 命令：:zephyr_file:`drivers/disk/nvme/nvme_cmd.c`
- NVMe 命名空间：:zephyr_file:`drivers/disk/nvme/nvme_namespace.c`

其中 NVMe 控制器是设备驱动程序的根。它是获取设备驱动程序实例的部分。
注意这仅仅是 DTS 描述的 NVMe 控制器，
而不包括其任何命名空间（磁盘）。
NVMe 命令是用于与控制器及其暴露的命名空间通信的通用逻辑。
最后，NVMe 命名空间是专门用于处理实际命名空间的部分，
进而使应用程序能够通过磁盘访问 API 访问每个命名空间
:zephyr_file:`drivers/disk/nvme/nvme_disk.c`。

如果一个控制器暴露多个命名空间（磁盘），
可以通过调整配置选项 CONFIG_NVME_MAX_NAMESPACES
来增加内置命名空间支持数量（见下文）。

每个暴露的磁盘通过其相关的 disk_info 结构体，
由其从相关命名空间继承的名称来区分。因此，磁盘名称遵循 NVMe 命名规范，
即 nvme<k>n<n>，其中 k 是控制器编号，
n 是命名空间编号。大多数情况下，如果系统中只插入一个 NVMe 磁盘，
会看到 'nvme0n0' 作为暴露的磁盘。

NVMe 配置
******************

DTS
===

任何暴露 NVMe 磁盘的板都应提供 DTS overlay 以启用其在 Zephyr 中的使用

.. code-block:: devicetree

    #include <zephyr/dt-bindings/pcie/pcie.h>
    / {
        pcie0 {
            nvme0: nvme0 {
                compatible = "nvme-controller";
                vendor-id = <VENDOR_ID>;
                device-id = <DEVICE_ID>;
                status = "okay";
            };
        };
    };

其中 VENDOR_ID 和 DEVICE_ID 是暴露的 NVMe 控制器的值。

选项
=======

* :kconfig:option:`CONFIG_NVME`

请注意，NVME 需要目标支持 PCIe 多向量 MSI-X 才能正常工作。

* :kconfig:option:`CONFIG_NVME_MAX_NAMESPACES`

重要注意事项
************************

NVMe 规范强制要求数据缓冲区放置在双字（4 字节）对齐的地址。
虽然这对于管理用户进程下方虚拟内存和动态分配的先进操作系统
不是问题，但在 Zephyr 中，只要缓冲区地址
直接映射到物理内存，这可能成为一个问题。

因此，在此阶段，用户需要确保提供给
:c:func:`disk_access_read` 和 :c:func:`disk_access_write` 的缓冲区地址
是双字对齐的。
