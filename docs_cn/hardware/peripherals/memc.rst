.. _memc_api:

内存控制器（MEMC）
########################

概述
********

MEMC API 提供访问 PSRAM 和 NOR flash 等外部内存设备的通用接口。它支持两种访问模式：

- **内存映射（Memory-mapped）：** 控制器通过 CPU 可直接访问的地址窗口暴露设备。驱动可以实现 :c:member:`memc_driver_api.get_mem_base` 以通告映射的基地址，使 :c:func:`memc_read` 和 :c:func:`memc_write` 自动使用 ``memcpy``。或者，如果硬件透明映射内存，驱动可以不提供任何运行时 API——在这种情况下，上层使用平台特定的基地址直接访问设备。

- **总线事务（Bus transaction）：** 控制器为每次传输发出显式总线命令（例如 MSPI）。驱动实现 :c:member:`memc_driver_api.read` 和 :c:member:`memc_driver_api.write`。用于控制器上不存在内存映射地址空间的情况。

:c:func:`memc_read` 和 :c:func:`memc_write` 在可用时自动选择内存映射路径，否则回退到总线事务。

为设备内省提供额外的可选 API：:c:func:`memc_get_size` 返回设备容量，:c:func:`memc_read_id` 返回设备识别字节。

旧式（仅初始化）驱动
**************************

向 ``DEVICE_DT_INST_DEFINE`` 传递 ``NULL`` 作为 API 指针的现有 memc 驱动不受此 API 影响。调用者应使用 :c:macro:`DEVICE_API_IS` 在调用任何 memc 函数前测试设备是否实现了 memc 接口：

.. code-block:: c

   if (DEVICE_API_IS(memc, dev)) {
      memc_read(dev, offset, buf, sizeof(buf));
   } else {
      /* Legacy init-only driver - device is memory-mapped.
       * Access via platform-specific base address.
       */
      memcpy(buf, (const uint8_t *)MEMC_BASE + offset, sizeof(buf));
   }

对未实现 memc API 的设备调用 :c:func:`memc_read` 或 :c:func:`memc_write` 返回 ``-ENOTSUP``。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_MEMC`
* :kconfig:option:`CONFIG_MEMC_INIT_PRIORITY`

API 参考
*************

.. doxygengroup:: memc_interface
