.. _mem_mgmt_api:

内存属性
#################

可以在设备树（devicetree）中使用 ``zephyr,memory-attr`` 属性为内存区域标记属性。然后可以在运行时利用提供的辅助库（
helper library）检索该属性和相关的内存区域。

可以在该属性中指定的一组通用属性，其定义和说明在 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr.h` 中。

例如，要在设备树中将一个内存区域标记为不可掉电（non-volatile）、可缓存（cacheable）、乱序（out-of-order）：

.. code-block:: devicetree

   mem: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-attr = <(DT_MEM_NON_VOLATILE | DT_MEM_CACHEABLE | DT_MEM_OOO)>;
   };

.. note::

   使用 ``zephyr,memory-attr`` 不会实际创建任何内存区域。当需要从设备树定义的内存区域创建一个实际的段（
   section）时，可以使用兼容属性 :dtcompatible:`zephyr,memory-region`，它会产生（仅在架构支持时）一个新的链接器段（linker section）和区域。

``zephyr,memory-attr`` 属性还可以用于设置架构特定的和软件特定的自定义属性，这些属性可以在运行时被解释。除其他用途外，这被用于从设备树定义的内存区域创建 MPU 区域，例如：

.. code-block:: devicetree

   mem: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-region = "NOCACHE_REGION";
       zephyr,memory-attr = <DT_MEM_ARM_MPU_RAM_NOCACHE>;
   };

关于 MPU 用法的更多详情，参见 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-arm.h`
 以及 :ref:`arm_cortex_m_developer_guide` 中的 :ref:`arm_cortex_m_mpu_considerations`。关于 Zephyr 如何处理缓存的详情，参见 :ref:`cache_guide`。

处理和管理标记了属性的内存区域的传统且推荐的方式，是启用 :kconfig:option:`CONFIG_MEM_ATTR` 使用提供的 ``mem-attr`` 辅助库。
启用该选项后，内存区域列表及其属性被编译进一个用户可访问的数组，并提供一组函数，可用于查询、探测以及对区域和属性采取行动（更多详情参见下一节）。

.. note::

   ``zephyr,memory-attr`` 属性只是相关内存区域能力的描述性属性，不会导致任何实际的内存设置。打算使用这些信息做一些工作（例如从该属性创建 MPU 区域）的用户、代码或子系统，必须使用提供的 ``mem-attr`` 库或常规的设备树辅助函数来执行所需的工作/设置。注意，不过，对于某些架构（如 ARM 和 ARM64），MPU 驱动使用该信息在启动时正确初始化缓存。参见 :kconfig:option:`CONFIG_ARM_MPU`、:kconfig:option:`CONFIG_RISCV_PMP` 等。

``mem-attr`` 库及其用法的测试位于 ``tests/subsys/mem_mgmt/mem_attr/``。

内存属性堆分配器
********************************

可以利用内存属性 ``zephyr,memory-attr`` 来定义并创建一组内存堆（heap），用户可以从这些堆中以特定属性/能力动态分配内存。

当设置了 :kconfig:option:`CONFIG_MEM_ATTR_HEAP` 时，每个被标记为 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-sw.h` 中列出的某个内存属性的区域，都会被添加到一个内存堆池（pool）中，用于以特定属性动态分配内存缓冲区。

以下是可能的属性（非穷举）列表：

.. code-block:: none

   DT_MEM_SW_ALLOC_CACHE
   DT_MEM_SW_ALLOC_NON_CACHE
   DT_MEM_SW_ALLOC_DMA

例如，我们可以定义几个具有不同属性的内存区域，并使用相应的属性来指示可以从这些区域动态分配内存：

.. code-block:: devicetree

   mem_cacheable: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-attr = <(DT_MEM_CACHEABLE | DT_MEM_SW_ALLOC_CACHE)>;
   };

   mem_non_cacheable: memory@20000000 {
       compatible = "mmio-sram";
       reg = <0x20000000 0x1000>;
       zephyr,memory-attr = <(DT_MEM_NON_CACHEABLE | ATTR_SW_ALLOC_NON_CACHE)>;
   };

   mem_cacheable_big: memory@30000000 {
       compatible = "mmio-sram";
       reg = <0x30000000 0x10000>;
       zephyr,memory-attr = <(DT_MEM_CACHEABLE | DT_MEM_OOO | DT_MEM_SW_ALLOC_CACHE)>;
   };

   mem_cacheable_dma: memory@40000000 {
       compatible = "mmio-sram";
       reg = <0x40000000 0x10000>;
       zephyr,memory-attr = <(DT_MEM_CACHEABLE      | DT_MEM_DMA |
                              DT_MEM_SW_ALLOC_CACHE | DT_MEM_SW_ALLOC_DMA)>;
   };

然后用户可以使用提供的函数从这些区域中动态划分（carve）内存，库会根据提供的属性和大小，负责从正确的堆分配内存：

.. code-block:: c

   // 初始化池
   mem_attr_heap_pool_init();

   // 从 `mem_cacheable` 分配 0x100 字节可缓存内存
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE, 0x100);

   // 从 `mem_non_cacheable` 分配 0x200 字节对齐到 32 字节的不可缓存内存
   block = mem_attr_heap_aligned_alloc(ATTR_SW_ALLOC_NON_CACHE, 0x100, 32);

   // 从 `mem_cacheable_dma` 分配 0x100 字节可缓存且可 DMA 的内存
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE | DT_MEM_SW_ALLOC_DMA, 0x100);

当多个区域被标记为相同属性时，内存的分配方式为：

1. 从 ``zephyr,memory-attr`` 属性具有所请求属性（或属性组合）的区域分配。

2. 在第 1 点中的区域之间，如果存在剩余未分配空间可满足所请求的大小，则从最小的区域分配。

3. 如果没有足够空间，则从能够容纳所请求大小的下一个更大区域分配。

下面的示例展示了第 3 点：

.. code-block:: c

   // 该内存从 `mem_non_cacheable` 分配
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_NON_CACHE, 0x100);

   // 该内存从 `mem_cacheable_big` 分配
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE, 0x5000);

.. note::

    该框架假设用于创建堆的内存区域可被代码使用，且在初始化时可用。用户在调用 :c:func:`mem_attr_heap_pool_init` 之前必须负责初始化和配置该内存区域。

    这意味着该区域必须在 MPU/MMU 方面（如需要）被正确配置，并且可以从中创建一个实际的堆，例如利用 ``zephyr,memory-region`` 属性创建一个合适的链接器段来容纳该堆。

API 参考
*************

.. doxygengroup:: memory_attr_interface
.. doxygengroup:: memory_attr_heap
