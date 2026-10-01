.. _memory_management_api_virtual_memory:

虚拟内存
##############

Zephyr 中的虚拟内存（VM）为开发者提供了精细调整内存访问的能力。
要利用虚拟内存，平台必须支持
内存管理单元（MMU），并且必须在构建中启用它。
由于 Zephyr 的目标主要是嵌入式系统，
Zephyr 中的虚拟内存支持与传统操作系统中的
略有不同：

内核映像映射
   默认情况下，如果未启用按需分页，
则对内核映像（包括代码和数据）
在物理内存和虚拟内存地址空间之间
进行 1:1 映射。偏离这一做法
需要仔细操作链接器脚本。

二级存储
   基本的虚拟内存支持不使用二级存储
来扩展可用内存。最大可用内存
与物理内存相同。

   * :ref:`memory_management_api_demand_paging` 启用
     将二级存储用作虚拟内存的后备存储，
     从而允许比可用物理内存更大的可用内存。
     注意按需分页需要显式启用。

   * 虽然虚拟内存空间可以大于物理
     内存空间，但不启用按需分页时，
     所有虚拟映射的内存都必须
     由物理内存来支持。


Kconfig 选项
********

必需
========

以下是内核支持虚拟内存
需要启用或定义的 Kconfig 选项。

* :kconfig:option:`CONFIG_MMU`：必须在
  内核中启用以支持虚拟内存。

* :kconfig:option:`CONFIG_MMU_PAGE_SIZE`：内存页的大小。默认值为 4KB。

* :kconfig:option:`CONFIG_KERNEL_VM_BASE`：虚拟地址空间的基地址。

* :kconfig:option:`CONFIG_KERNEL_VM_SIZE`：虚拟地址空间的大小。
  默认值为 8MB。

* :kconfig:option:`CONFIG_KERNEL_VM_OFFSET`：内核映像
  从此偏移开始（相对于 :kconfig:option:`CONFIG_KERNEL_VM_BASE`）。

可选
========

* :kconfig:option:`CONFIG_KERNEL_DIRECT_MAP`：允许
  虚拟地址和物理地址之间的 1:1 映射，
  而不是由内核在虚拟地址空间内选择地址。
  这对于映射设备 MMIO 区域
  以实现更精确的访问控制非常有用。


内存映射概述
*******************

这是虚拟内存地址空间内存映射的概述。
注意，代码中使用的 ``Z_*`` 宏
可能根据架构和 Kconfig 选项
具有不同的含义，下面将对此进行解释。

.. code-block:: none
   :emphasize-lines: 1, 3, 9, 22, 24

   +--------------+ <- K_MEM_VIRT_RAM_START
   | Undefined VM | <- architecture specific reserved area
   +--------------+ <- K_MEM_KERNEL_VIRT_START
   | Mapping for  |
   | main kernel  |
   | image        |
   |              |
   |              |
   +--------------+ <- K_MEM_VM_FREE_START
   |              |
   | Unused,      |
   | Available VM |
   |              |
   |..............| <- grows downward as more mappings are made
   | Mapping      |
   +--------------+
   | Mapping      |
   +--------------+
   | ...          |
   +--------------+
   | Mapping      |
   +--------------+ <- memory mappings start here
   | Reserved     | <- special purpose virtual page(s) of size K_MEM_VM_RESERVED
   +--------------+ <- K_MEM_VIRT_RAM_END

* ``K_MEM_VIRT_RAM_START`` 是虚拟内存地址空间的开始。
  这需要页对齐。目前，它与
  :kconfig:option:`CONFIG_KERNEL_VM_BASE` 相同。

* ``K_MEM_VIRT_RAM_SIZE`` 是虚拟内存地址空间的大小。
  这需要页对齐。目前，它与
  :kconfig:option:`CONFIG_KERNEL_VM_SIZE` 相同。

* ``K_MEM_VIRT_RAM_END`` 简单地等于（``K_MEM_VIRT_RAM_START`` + ``K_MEM_VIRT_RAM_SIZE``）。

* ``K_MEM_KERNEL_VIRT_START`` 与链接器
  脚本中指定的 ``z_mapped_start`` 相同。
  这是启动时内核映像开始的虚拟地址。

* ``K_MEM_KERNEL_VIRT_END`` 与链接器
  脚本中指定的 ``z_mapped_end`` 相同。
  这是启动时内核映像结束的虚拟地址。

* ``K_MEM_VM_FREE_START`` 是可以为
  内存映射分配地址的虚拟地址空间的开始。
  这取决于
  :kconfig:option:`CONFIG_ARCH_MAPS_ALL_RAM` 是否启用。

   * 如果启用，意味着所有物理内存
     都映射在虚拟内存地址空间中，
     并且它等于
     （:c:macro:`DT_CHOSEN_SRAM_ADDR` + :c:macro:`DT_CHOSEN_SRAM_SIZE`）。

   * 如果禁用，``K_MEM_VM_FREE_START``
     与 ``K_MEM_KERNEL_VIRT_END`` 相同，
     即内核映像的结束位置。

* ``K_MEM_VM_RESERVED`` 是一个保留区域，
  用于支持内核功能。例如，
  保留某些地址以支持按需分页。


虚拟内存映射
***********************

在启动时设置映射
===========================

一般来说，大多数支持的架构在启动时
设置内存映射如下：

* ``.text`` 段是只读且可执行的。
  它在内核模式和用户模式下都可访问。

* ``.rodata`` 段是只读且不可执行的。
  它在内核模式和用户模式下都可访问。

* 其他内核段，如 ``.data``、``.bss`` 和 ``.noinit``，是可读写且不可执行的。它们仅在内核模式下可访问。

   * 用户模式线程的栈在线程创建时会自动授予其对应的用户模式线程可读写访问权限。

   * 全局变量默认情况下对用户模式线程不可访问。
     请参阅 :ref:`Memory Domains and Partitions<memory_domain>`
     了解如何在用户模式线程中使用全局变量，
     以及如何在用户模式线程之间共享数据。

这些映射的缓存模式因架构而异。
它们可以是无缓存、写回或直写。

注意，SoC 有自己启动所需的额外映射，
这些映射在它们自己的 SoC 配置下定义。
这些映射通常包括
设置硬件所需的设备 MMIO 区域。


映射匿名内存
========================

未使用的物理内存可以按需
映射到虚拟地址空间中。
这在概念上类似于从堆分配内存，
但这些映射必须按页大小对齐，
并且具有更精细的访问控制。

* :c:func:`k_mem_map` 可用于
  映射未使用的物理内存：

   * 请求的大小必须是页大小的倍数。

   * 返回的地址位于
     ``K_MEM_VM_FREE_START`` 和
     ``K_MEM_VIRT_RAM_END`` 之间的
     虚拟地址空间内。

   * 映射的区域不保证
     在内存中物理连续。

   * 映射虚拟区域紧邻之前和之后
     的守护页会自动分配，
     以捕获由于缓冲区下溢
     或上溢导致的访问问题。

* 映射的区域可以通过
  :c:func:`k_mem_unmap` 解除映射
  （即释放）：

   * 必须谨慎确保向
     :c:func:`k_mem_map` 和
     :c:func:`k_mem_unmap` 传递
     相同的区域大小。
     解除映射函数在解除映射前
     不检查其是否为有效的映射区域。


API 参考
*************

.. doxygengroup:: kernel_memory_management
