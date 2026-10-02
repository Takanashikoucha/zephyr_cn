.. _flash_map_api:

Flash 分区图（flash map）
#########

``<zephyr/storage/flash_map.h>`` API 允许通过 :c:struct:`flash_area` 结构体访问设备 flash 分区的信息。

每个 :c:struct:`flash_area` 描述一个 flash 分区。该 API 提供对 "flash map" 的访问，其中包含可通过全局唯一 ID 号访问的预定义 flash 区域。该 map 由 DTS 文件中 "fixed-partitions" 和 "zephyr,mapped-partition" 兼容项创建。用户也可以在运行时创建 :c:struct:`flash_area` 对象，用于特定于应用的目的。

本文档在引用单个 "fixed-partitions" 或 "zephyr,mapped-partition" 实体时使用 "flash area"（flash 区域）。

:c:struct:`flash_area` 包含一个指向 :c:struct:`device` 的指针，可借助 :ref:`flash API <flash_api>` 直接访问该区域所在的 flash 设备。每个 flash 区域由其所放置的设备、相对于设备起始位置的偏移量以及设备上的大小来表征。:c:func:`flash_area_open` 函数使用一个额外的标识符参数在 flash map 中查找 flash 区域。

flash_map.h API 提供操作 :c:struct:`flash_area` 的函数。主要示例是 :c:func:`flash_area_read` 和 :c:func:`flash_area_write`。这些函数本质上是对 flash API 的封装，附带额外的偏移量和大小检查，将 flash 操作限制在预定义区域内。

大多数 ``<zephyr/storage/flash_map.h>`` API 函数需要一个 :c:struct:`flash_area` 对象指针，表征将要操作的 flash 区域。获取该指针有两种可能的方法：

 * 使用 :c:func:`flash_area_open` 获取；

 * 定义一个 :c:struct:`flash_area` 类型的对象，这需要提供一个有效的 :c:struct:`device` 对象指针以及该区域在 flash 设备内的偏移量和大小。

:c:func:`flash_area_open` 使用数字标识符在 flash map 中搜索 :c:struct:`flash_area` 对象，如果找到，则返回一个指向代表该 ID 区域的对象的指针。flash 区域的 ID 号可以通过 :c:macro:`PARTITION_ID()` 从 "fixed-partitions" 或 "zephyr,mapped-partition" DTS 节点标签获取；这些标签按如下所述从设备树获取。

与设备树的关系
****************************

flash_map.h API 使用由 :ref:`devicetree_api` 生成的数据，特别是其 :ref:`devicetree-flash-api`。Zephyr 还有一些分区约定，用于通过 MCUboot 引导加载器进行 :ref:`dfu`，以及定义可供 :ref:`file systems <file_system_api>` 或其他非易失性 :ref:`storage <storage_services>` 使用的分区。

下面是一个设备树片段示例，同时为 MCUboot 和存储分区使用固定 flash 分区。为清晰起见省略了一些细节。

.. literalinclude:: example_fragment.dts
   :language: DTS
   :start-after: start-after-here

分区偏移量应相对于该分区所属 flash 内存的起始地址表示。

``boot_partition``、``slot0_partition``、``slot1_partition`` 和 ``scratch_partition`` 节点标签是为 MCUboot 定义的，尽管并非所有 MCUboot 配置都需要定义它们全部。更多细节参见 `MCUboot 文档`_。

``storage_partition`` 节点是为文件系统或其他非易失性存储 API 使用而定义的。

.. _MCUboot documentation: https://docs.mcuboot.com

数字 flash 区域 ID 通过向 :c:macro:`PARTITION_ID()` 传入 DTS 节点标签获得；例如要获取 ``slot0_partition`` 的 ID 号，用户调用 ``PARTITION_ID(slot0_partition)``。

所有 :code:`PARTITION_*` 宏都以 DTS 节点标签作为分区标识符。

如果某区域在 DTS 文件中已定义，用户无需使用 :c:func:`flash_map_open` 获取 :c:struct:`flash_area` 对象指针即可了解 flash 区域的大小、偏移量或设备。知道一个区域的 DTS 节点标签后，用户可以分别使用 :c:macro:`PARTITION_OFFSET()`、:c:macro:`PARTITION_SIZE()` 或 :c:macro:`PARTITION_DEVICE()` 直接从 DTS 节点定义获取这些信息。例如要获取 ``storage_partition`` 的偏移量，只需调用 ``PARTITION_OFFSET(storage_partition)``。

下面的示例展示了如何使用 :c:func:`flash_area_open` 和 DTS 节点标签获取 :c:struct:`flash_area` 对象指针：

.. code-block:: c

   const struct flash_area *my_area;
   int err = flash_area_open(PARTITION_ID(slot0_partition), &my_area);

   if (err != 0) {
   	handle_the_error(err);
   } else {
   	flash_area_read(my_area, ...);
   }

API 参考
*************

.. doxygengroup:: flash_area_api
