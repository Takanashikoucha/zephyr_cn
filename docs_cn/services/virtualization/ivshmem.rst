.. _ivshmem_driver:

Inter-VM Shared Memory
######################

.. contents::
   :local:
   :depth: 2

Overview
********

Zephyr 已支持作为客户操作系统运行在 Qemu 和 `ACRN <https://projectacrn.github.io/latest/tutorials/using_zephyr_as_uos.html>`_ 上，因此可能需要让虚拟机彼此感知，或感知宿主机。这通过名为 ivshmem（inter-VM Shared Memory，虚拟机间共享内存）的特性实现，它向各参与方暴露一块共享内存。

支持两种类型：纯共享内存（ivshmem-plain），或具备让一个虚拟机向另一个虚拟机产生中断、从而自身也能被中断能力的共享内存（ivshmem-doorbell）。

更多信息请参阅官方 `Qemu ivshmem 文档 <https://www.qemu.org/docs/master/system/devices/ivshmem.html>`_。

Support
*******

Zephyr 同时支持 plain 和 doorbell 两个版本。启用 :kconfig:option:`CONFIG_IVSHMEM` 即可构建 ivshmem 驱动。默认情况下，这将暴露 plain 版本。需要启用 :kconfig:option:`CONFIG_IVSHMEM_DOORBELL` 才能获得 doorbell 版本。

由于 doorbell 版本使用 MSI-X 向量支持通知向量，必须将 :kconfig:option:`CONFIG_IVSHMEM_MSI_X_VECTORS` 调整为所需的向量数量。

请注意，可以通过启用 :kconfig:option:`CONFIG_IVSHMEM_SHELL` 暴露一个小型 shell 模块来测试 ivshmem 功能。

ivshmem-v2
**********

Zephyr 还支持 ivshmem-v2：

https://github.com/siemens/jailhouse/blob/master/Documentation/ivshmem-v2-specification.md

它主要用于 Jailhouse 虚拟化器的 IPC（例如 :zephyr:code-sample:`eth-ivshmem`）。也可以在不使用 Jailhouse 的情况下使用 ivshmem-v2，方法是构建 Siemens 的 QEMU fork 并修改 QEMU 启动参数：

https://github.com/siemens/qemu/tree/wip/ivshmem2

API Reference
*************

.. doxygengroup:: ivshmem
