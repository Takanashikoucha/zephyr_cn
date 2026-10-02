.. _disk_virtio_blk:

VirtIO 块设备
############

VirtIO 是一种标准化接口，用于向客户机暴露虚拟设备，通常运行在 QEMU 等 hypervisor 之下。``virtio,blk`` 驱动将 VirtIO 块设备呈现为一个 Zephyr 磁盘：它可通过 :ref:`Disk Access API <disk_access_api>` 访问，并经由该接口进一步被 :ref:`File System API <file_system_api>` 使用。

该驱动与传输层无关，在 Zephyr 支持的两种 VirtIO 传输（PCI 和 MMIO，参见 :ref:`VirtIO <virtio>`）上无需任何修改即可运行。每个启用的 ``virtio,blk`` 设备树节点都会创建一个实例。

驱动设计
*************

驱动位于 :zephyr_file:`drivers/disk/virtio_blk.c`，构建在通用 VirtIO API 之上。``virtio,blk`` 节点是 VirtIO 传输设备（``DT_INST_PARENT``）的子节点，因此同一段代码无需修改即可服务于 PCI 或 MMIO 设备。

单个在途请求
========================

``disk_access`` 读写 API 是同步且阻塞的。驱动还通过互斥锁对调用方进行串行化，因此每个设备始终只保持一个在途请求：它向请求 virtqueue 添加一条描述符链，通知设备，然后阻塞在一个信号量上，该信号量由完成回调从中断上下文发出信号。

由于没有请求流水线化，整个 virtqueue 都用于单个请求的散列-聚集（scatter-gather）链。面向用户的配置项是每个请求的最大数据段数
（:kconfig:option:`CONFIG_DISK_VIRTIO_BLK_MAX_SEGMENTS`）；驱动通过将 ``MAX_SEGMENTS + 2`` 向上取整为 2 的幂来确定 virtqueue 大小，为请求头和状态字节预留空间。

块大小
==========

VirtIO 块协议始终以固定的 512 字节扇区为单位对设备寻址，并以该单位报告设备容量。暴露给 ``disk_access`` 的逻辑块大小可能与之不同：

* 当设备提供 ``VIRTIO_BLK_F_BLK_SIZE`` 时，驱动会协商该特性并暴露设备通告的 ``blk_size``。
* 否则回退到
  :kconfig:option:`CONFIG_DISK_VIRTIO_BLK_SECTOR_SIZE`。

所有寻址在内部都会转换为 512 字节的 VirtIO 扇区。块大小必须是 512 的倍数，并且在 :kconfig:option:`CONFIG_MMU` 下不得超过 MMU 页大小；不支持的值会在初始化时被拒绝。

零拷贝传输
===================

调用方缓冲区直接交给设备，不使用中转缓冲区（bounce buffer）。在
:kconfig:option:`CONFIG_MMU` 下，缓冲区可能位于内核线性 RAM 映射之外（例如 ``f_mkfs()`` 向下传递的线程栈工作区），且无需物理连续。驱动通过 ``arch_page_phys_get()`` 逐页遍历此类缓冲区，将物理上相邻的区间合并为散列-聚集段，并且当传输的碎片化程度超出段预算时，将其拆分到多个设备请求中。

特性协商
===================

除了 ``VIRTIO_BLK_F_BLK_SIZE`` 之外，驱动还会协商：

* ``VIRTIO_BLK_F_RO`` — 只读设备被报告为
  ``DISK_STATUS_WR_PROTECT``，写请求以 ``-EROFS`` 拒绝。
* ``VIRTIO_BLK_F_FLUSH`` — ``DISK_IOCTL_CTRL_SYNC`` 向设备发起 flush。
  当设备未提供 ``FLUSH`` 时没有回写缓存需要刷新，
  因此该 ioctl 是成功的空操作（no-op）而非错误。

状态字节不为 ``OK`` 的已完成请求会被记录日志并映射到 errno：不支持的请求变为 ``-ENOTSUP``，I/O 错误变为 ``-EIO``。

VirtIO 块设备配置
**************************

DTS
===

``virtio,blk`` 节点放置在其 VirtIO 传输父节点之下，需要一个供 ``disk_access`` API 使用的 ``disk-name``。在 PCI 传输下：

.. code-block:: devicetree

    #include <zephyr/dt-bindings/pcie/pcie.h>

    / {
        pcie0 {
            virtio-blk-pci {
                compatible = "virtio,pci";
                vendor-id = <0x1af4>;
                device-id = <0x1001>;
                interrupts = <0xb 0x0 0x0>;
                interrupt-parent = <&intc>;
                status = "okay";

                virtio_blk: virtio-blk {
                    compatible = "virtio,blk";
                    disk-name = "VIRTIOBLK0";
                    status = "okay";
                };
            };
        };
    };

在 MMIO 传输下，节点是现有 ``virtio,mmio`` 总线的子节点：

.. code-block:: devicetree

    &virtio_mmio4 {
        status = "okay";

        virtio_blk: virtio-blk {
            compatible = "virtio,blk";
            disk-name = "VIRTIOBLK0";
            status = "okay";
        };
    };

选项
-------

* :kconfig:option:`CONFIG_DISK_DRIVER_VIRTIO_BLK`
* :kconfig:option:`CONFIG_DISK_VIRTIO_BLK_MAX_SEGMENTS`
* :kconfig:option:`CONFIG_DISK_VIRTIO_BLK_SECTOR_SIZE`

QEMU 选项
--------------

当 :kconfig:option:`CONFIG_DISK_DRIVER_VIRTIO_BLK` 在 QEMU 板级上启用时，
仿真层会创建一个原始（raw）后端镜像并将其挂接到仿真的 virtio-blk 设备。PCI 传输由通用的 QEMU 仿真代码挂接；``qemu_cortex_a53`` 板级将 MMIO ``virtio-blk-device`` 挂接到 ``virtio-mmio-bus.4``。

* :kconfig:option:`CONFIG_QEMU_VIRTIO_BLK_LOGICAL_BLOCK_SIZE`
* :kconfig:option:`CONFIG_QEMU_VIRTIO_BLK_DISK_SIZE`

限制
***********

* 同一时刻只有一个请求在途。这与同步的
  ``disk_access`` 契约一致，因此不会让该消费方损失吞吐量，但驱动不提供请求流水线化。
* 与 Zephyr VirtIO 子系统的其余部分一样，驱动假设 DMA 一致性，不对描述符、环或数据缓冲区执行任何缓存维护。
* 在 MMU 下，逻辑块大小不得超过 MMU 页大小。
