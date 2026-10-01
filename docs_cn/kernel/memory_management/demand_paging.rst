.. _memory_management_api_demand_paging:

按需分页
#############

按需分页提供了一种机制，数据仅在当前执行上下文需要时
才被调入物理内存。物理内存概念上被划分为页大小的
页框（page frame）区域，用于存放数据。

Zephyr 内核镜像本身始终驻留在物理内存中，
且从不成为驱逐（eviction）的候选对象。按需分页仅适用于：

* 运行时通过 :c:func:`k_mem_map()` 创建的匿名内存映射，以及
* 当 :kconfig:option:`CONFIG_LINKER_USE_ONDEMAND_SECTION` 启用时，
  通过 ``__ondemand_func`` / ``__ondemand_rodata`` 属性放置在
  显式按需链接器段中的内存。

这是所有主要操作系统使用的相同模型：异常或中断的分发路径
从不在可分页的页上，因此在故障处理期间发生故障
在结构上是不可能的。添加到 ``__ondemand_*`` 段中的代码或数据
是贡献者显式选择使该区域可分页，并承担确保其不会被
页故障处理程序自身执行路径触及的责任。

.. note::

   Zephyr 的早期版本还支持一种基于 ``__pinned_*`` 链接器属性的
   选择性固定（pinning）方案，该方案仅保持被标记的内核镜像子集
   驻留，并对其余部分进行按需分页。该模型被发现既不安全
   和/或非常侵入性：CPU 异常分发可能目标为线程位于
   可驱逐页上的特权栈，如果该页已被驱逐，在 x86 上会升级为
   双重故障（double fault），在 ARM64 上会升级为嵌套中止
   （nested abort）；而且"故障处理程序可达表面（调度器、
   驱动、libc、锁原语）上的每个字节都必须详尽标记"这一契约
   一旦建立就不切实际，之后也无法维护。``__pinned_*`` 属性族、
   对应的 Kconfig 选项（``LINKER_USE_PINNED_SECTION`` /
   ``LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT``）以及
   ``K_*_PINNED_STACK_*`` 栈宏已在 Zephyr 4.4 中移除。
   参见 :github:`108773` 了解完整分析。

* 当处理器尝试访问数据且数据页存在于某个页框中时，
  执行继续，无任何中断。

* 当处理器尝试访问不存在于任何页框中的数据页时，
  发生页故障。随后分页代码如果有空闲页框，
  就从后备存储（backing store）将对应的数据页调入物理内存。
  如果没有更多空闲页框，则调用驱逐算法
  选择一个要换出的数据页，从而为新的数据页调入
  释放一个页框。如果该数据页在首次调入后被修改过，
  数据将被写回后备存储。如果没有被修改
  或者在写回后备存储之后，该数据页即被视为已换出，
  对应的页框随即空闲。然后分页代码调用后备存储，
  将对应于所请求数据位置的数据页调入。
  后备存储将该数据页复制到空闲页框中。
  现在数据页已在物理内存中，执行可以继续。

有函数可以手动调用页调入和换出，
使用 :c:func:`k_mem_page_in()` 和 :c:func:`k_mem_page_out()`。
:c:func:`k_mem_page_in()` 可用于提前调入预期近期需要的数据页。
这用于最小化页故障数量，因为这些数据页已在物理内存中，
从而最小化延迟。:c:func:`k_mem_page_out()` 可用于
换出那些在相当长一段时间内不会再被访问的数据页。
这释放了页框，使得下一次页调入可以更快执行，
因为分页代码无需调用驱逐算法。

数据区域也可以用 :c:func:`k_mem_pin()` **固定**在物理内存中。
这会在必要时将该区域调入，并标记其页框，
使得驱逐算法永远不会选择它们，从而保证该区域保持驻留，
且对其访问永远不会故障。这是 :c:func:`k_mem_page_in()` 的
更强形式，适用于必须始终可用的延迟敏感或安全关键数据。
固定的区域之后用 :c:func:`k_mem_unpin()` 释放，
它会将页框重新标记为可驱逐；解除固定本身并不会驱逐该区域，
因此如果需要立即驱逐，可以随后调用 :c:func:`k_mem_page_out()`。

术语
***********

数据页（Data Page）
   数据页是页大小的数据区域。它可能存在于页框中，
   也可能被换出到某个后备存储。其位置总是可以
   通过虚拟地址在 CPU 的页表（或等价物）中查找。
   数据类型总是 ``void *``，或在某些情况下做指针运算时为
   ``uint8_t *``。

页框（Page Frame）
   页框是 RAM 中页大小的物理内存区域。
   它是可放置数据页的容器。它总是通过物理地址引用。
   Zephyr 有使用 ``uintptr_t`` 表示物理地址的约定。
   对每个页框，都会实例化一个 ``struct k_mem_page_frame``
   以保存元数据。每个页框的标志如下：

   * ``K_MEM_PAGE_FRAME_FREE`` 表示页框未使用，
     且在空闲页框列表中。设置此标志时，其他标志无意义，
     且不得修改。

   * ``K_MEM_PAGE_FRAME_PINNED`` 表示页框被固定在内存中，
     且不应被换出。

   * ``K_MEM_PAGE_FRAME_RESERVED`` 表示硬件保留的物理页，
     不应被使用。

   * ``K_MEM_PAGE_FRAME_MAPPED`` 在物理页被映射到
     虚拟内存地址时设置。

   * ``K_MEM_PAGE_FRAME_BUSY`` 表示页框当前正参与
     页调入/换出操作。

   * ``K_MEM_PAGE_FRAME_BACKED`` 表示页框在后备存储中
     有一份干净的副本。

K_MEM_SCRATCH_PAGE
   提供给后备存储的一个特殊页的虚拟地址，用于：
   * 将数据页从 ``K_MEM_SCRATCH_PAGE`` 复制到指定位置；或，
   * 将数据页从指定位置复制到 ``K_MEM_SCRATCH_PAGE``。
   它用作页调入/换出操作的中间页。此暂存页
   需要映射为可读/写，以便后备存储代码访问。
   然而数据页本身在虚拟地址空间中可能仅映射为只读。
   如果此页原样提供给后备存储，数据页必须被重新映射为
   可读/写，这对安全有影响，因为数据页对其他应用部分
   不再只读。

分页统计
*****************

当 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS`
启用时，可通过各种函数调用获取分页统计：

* 总体统计通过 :c:func:`k_mem_paging_stats_get()`

* 每线程统计通过 :c:func:`k_mem_paging_thread_stats_get()`
  （如果 :kconfig:option:`CONFIG_DEMAND_PAGING_THREAD_STATS` 启用）

* 执行时间直方图在 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM`
  启用且 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS`
  已定义时可获取。注意计时高度依赖于架构、SoC 或开发板。
  强烈建议为特定应用定义
  ``k_mem_paging_eviction_histogram_bounds[]`` 和
  ``k_mem_paging_backing_store_histogram_bounds[]``。

  * 驱逐算法的执行时间直方图通过
    :c:func:`k_mem_paging_histogram_eviction_get()`

  * 后备存储执行页调入的执行时间直方图通过
    :c:func:`k_mem_paging_histogram_backing_store_page_in_get()`

  * 后备存储执行页换出的执行时间直方图通过
    :c:func:`k_mem_paging_histogram_backing_store_page_out_get()`

驱逐算法
******************

驱逐算法用于确定哪个数据页及其对应页框可以被换出，
以为下一次页调入操作释放页框。有四个函数
由内核分页代码调用：

* :c:func:`k_mem_paging_eviction_init()` 被调用来初始化
  驱逐算法。这在 ``POST_KERNEL`` 阶段调用。

* :c:func:`k_mem_paging_eviction_add()` 在每次数据页成为
  未来驱逐候选时调用。

* :c:func:`k_mem_paging_eviction_remove()` 在数据页不再适合
  被驱逐时调用。这可能发生在给定数据页被固定、
  被解除映射或即将被驱逐时。

* :c:func:`k_mem_paging_eviction_select()` 被调用来选择
  要驱逐的数据页。函数参数 ``dirty`` 被写入，
  以向调用者指示所选数据页自首次调入后是否被修改过。
  如果 ``dirty`` 位返回为已设置，分页代码向后备存储
  发出信号，将数据页写回存储（从而更新其内容）。
  函数返回指向所选数据页对应页框的指针。

还有一个额外函数，由架构的内存管理代码在数据页触发
访问故障时调用以标记它们：
:c:func:`k_mem_paging_eviction_accessed()`。这用于 LRU 算法
重新排队"已使用"的页。

目前有两种可用的驱逐算法：

* 已作为示例实现了一种 NRU（Not-Recently-Used，非最近使用）
  驱逐算法。这是一个非常简单的算法，根据数据页
  是否被访问和修改来排序。选择基于此排序。

* 也可用 LRU（Least-Recently-Used，最近最少使用）驱逐算法。
  它基于数据页的排序队列。LRU 代码比 NRU 代码更复杂，
  但也明显更高效。推荐用于生产环境。

要实现新的驱逐算法，必须实现
:c:func:`k_mem_paging_eviction_init()` 和
:c:func:`k_mem_paging_eviction_select()`。
如果为某个算法启用了 :kconfig:option:`CONFIG_EVICTION_TRACKING`，
还必须实现这些额外函数：
:c:func:`k_mem_paging_eviction_add()`、
:c:func:`k_mem_paging_eviction_remove()`、
:c:func:`k_mem_paging_eviction_accessed()`。

后备存储
*************

后备存储负责在数据页的对应页框和存储之间
进行页调入/换出。以下是必须实现的函数：

* :c:func:`k_mem_paging_backing_store_init()` 被调用来
  在 ``POST_KERNEL`` 阶段初始化后备存储。

* :c:func:`k_mem_paging_backing_store_location_get()` 被调用来
  保留一个后备存储位置，以便数据页可以被换出。
  此 ``location`` 令牌传递给
  :c:func:`k_mem_paging_backing_store_page_out()`
  以执行实际的换出操作。

* :c:func:`k_mem_paging_backing_store_location_free()` 被调用来
  释放一个后备存储位置（``location`` 令牌），
  之后可用于后续的换出操作。

* :c:func:`k_mem_paging_backing_store_location_query()` 被调用来
  获取对应于要虚拟映射并按需调入的存储内容的
  ``location`` 令牌。与 :kconfig:option:`CONFIG_DEMAND_MAPPING`
  一起使用时最有用。

* :c:func:`k_mem_paging_backing_store_page_in()` 将数据页
  从与所提供的 ``location`` 令牌关联的后备存储位置
  复制到 ``K_MEM_SCRATCH_PAGE`` 指向的页。

* :c:func:`k_mem_paging_backing_store_page_out()` 将数据页
  从 ``K_MEM_SCRATCH_PAGE`` 复制到与所提供的 ``location``
  令牌关联的后备存储位置。

* :c:func:`k_mem_paging_backing_store_page_finalize()` 在
  :c:func:`k_mem_paging_backing_store_page_in()` 之后调用，
  以便可以更新页框结构体用于内部记账。这可以是空操作。

要实现新的后备存储，必须实现上述提到的函数。
:c:func:`k_mem_paging_backing_store_page_finalize()`
如果需要，可以是空函数。

API 参考
*************

.. doxygengroup:: mem-demand-paging

驱逐算法 API
=======================

.. doxygengroup:: mem-demand-paging-eviction

后备存储 API
==================

.. doxygengroup:: mem-demand-paging-backing-store
