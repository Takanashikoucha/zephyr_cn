.. _nvs_api:

非易失性存储（NVS）
##########################

以 id-数据对表示的元素使用由 FIFO 管理的循环缓冲区存储在 flash 中。flash 区域被划分为扇区。元素被追加到某个扇区，直到该扇区的存储空间耗尽。然后 flash 区域中的一个新扇区被准备使用（擦除）。擦除扇区之前，会检查标识符-数据对是否已存在于正在使用的扇区中；如果不存在，则将该 id-数据对拷贝过去。

id 是一个 16 位无符号数。NVS 确保对于每个已使用的 id，任何时刻 flash 中都至少存储有一个 id-数据对。

NVS 允许存储二进制块（binary blob）、字符串、整型、长整型以及它们的任意组合。

每个元素在 flash 中存储为元数据（8 字节）和数据。元数据被写入一个从 nvs 扇区末尾开始的表中，数据从扇区起始位置开始一个接一个地写入。元数据由以下字段组成：id、扇区内数据偏移量、数据长度、part（未使用）以及一个 CRC。该 CRC 仅对元数据计算，只确保一次写入已完成。元素的实际数据可以由另一个（可选的）CRC-32 保护。使用 :kconfig:option:`CONFIG_NVS_DATA_CRC` 配置项启用数据部分的 CRC。

.. note:: 数据 CRC 仅在读取元素的完整数据时才会被检查。
   由于数据 CRC 存储在元素数据区域的末尾，部分读取时不会检查数据 CRC。

.. note:: 对之前已存在且没有数据 CRC 的 NVS 内容启用数据 CRC 特性，
   将使所有现有数据失效。

向 nvs 写入数据时，始终先写入数据，然后写入元数据。在 flash 中写入但没有元数据的数据在初始化期间会被忽略。

初始化期间，NVS 会验证存储在 flash 中的数据；如果它遇到错误，将忽略任何元数据缺失/不正确 的数据。

NVS 在向 flash 写入数据之前会检查 id-数据对。如果 id-数据对没有变化，则不执行对 flash 的写入。

为保护 flash 区域免受频繁擦除，有足够的空闲空间非常重要。NVS 具有一个保护机制，避免在空闲空间有限时陷入 flash 页擦除的无限循环。检测到这样的循环时，NVS 返回没有更多可用空间。

对 NVS 而言，文件系统声明如下：

.. code-block:: c

	static struct nvs_fs fs = {
	.flash_device = NVS_FLASH_DEVICE,
	.sector_size = NVS_SECTOR_SIZE,
	.sector_count = NVS_SECTOR_COUNT,
	.offset = NVS_STORAGE_OFFSET,
	};

其中：

- ``NVS_FLASH_DEVICE`` 是对将被使用的 flash 设备的引用。
  该设备必须处于可工作状态。
- ``NVS_SECTOR_SIZE`` 是扇区大小，它必须是 flash 擦除页大小的倍数且为 2 的幂。
- ``NVS_SECTOR_COUNT`` 是扇区数量，至少为 2，
  始终保留一个扇区为空，以便拷贝现有数据。
- ``NVS_STORAGE_OFFSET`` 是存储区域在 flash 中的偏移量。


Flash 磨损
**********

向 flash 写入数据时，研究 flash 磨损非常重要。flash 的寿命有限，由 flash 可被擦除的次数决定。flash 一次擦除一页，页大小由硬件决定。例如，nRF51822 设备的页大小为 1024 字节，每页大约可擦除 20,000 次。

计算预期设备寿命
====================================

假设我们使用一个 4 字节的状态变量，它每分钟变化一次，
并且需要在重启后恢复。NVS 被定义为 sector_size 等于页大小（1024 字节），并定义了 2 个扇区。

每次写入状态变量需要 12 字节的 flash 存储：8 字节用于元数据，4 字节用于数据。存储数据时，
第一个扇区在 1024/12 = 85.33 分钟后被填满。再过 85.33 分钟，
第二个扇区被填满。当这种情况发生时，由于我们只使用两个扇区，
第一个扇区将被用于存储，并将在 171 分钟系统时间后被擦除。
以设备预期寿命 20,000 次写入、两个扇区每 171 分钟写入一次计算，
设备应可持续约 171 * 20,000 分钟，即约 6.5 年。

更一般地，设

- ``NS`` 为每分钟存储请求数，
- ``DS`` 为数据大小（字节），
- ``SECTOR_SIZE`` 为扇区大小（字节），
- ``PAGE_ERASES`` 为页可被擦除的次数，

则预期设备寿命（分钟）可计算为::

   SECTOR_COUNT * SECTOR_SIZE * PAGE_ERASES / (NS * (DS+8)) 分钟

从这个公式还可以看出，如果预期寿命太短该怎么做：增加 ``SECTOR_COUNT`` 或 ``SECTOR_SIZE``。

Flash 写块大小迁移
********************************
在 DFU 过程中，NVS 使用的 flash 驱动可能会改变其支持的最小写块大小。
除非物理 ATE 大小发生变化，NVS 的 flash 内镜像将保持兼容。
特别是，允许在 1、2、4、8 字节的写块大小之间迁移。

示例
******

NVS 的使用示例提供在 ``samples/subsys/kvss/nvs`` 中。

故障排除
***************

使用 NVS 时出现 MPU 故障，或返回 ``-ETIMEDOUT`` 错误
   NVS 可以使用 SoC 的内部 flash。 在 MPU 启用时，
   flash 驱动需要通过 :kconfig:option:`CONFIG_MPU_ALLOW_FLASH_WRITE` 配置的
   对 flash 内存的 MPU RWX 访问权限。 如果该选项被禁用，
   NVS 应用引用内部 SoC flash 且是唯一运行的线程时，将出现 MPU 故障。 在
   多线程应用中，另一个线程可能截获该故障，
   此时 NVS API 将返回 ``-ETIMEDOUT`` 错误。


API 参考
*************

NVS 子系统的 API 由 ``nvs.h`` 提供：

.. doxygengroup:: nvs_data_structures

.. doxygengroup:: nvs_high_level_api

.. comment
   不做文档化
   .. doxygengroup:: nvs
