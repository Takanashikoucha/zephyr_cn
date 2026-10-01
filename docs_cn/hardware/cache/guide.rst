.. _cache_guide:

缓存基础
##############

本节讨论缓存一致性的基础知识，以及用户在什么情况下需要显式处理缓存问题。有关 Zephyr 缓存工具的更详细信息，
请参见 :ref:`cache_config` 了解 Zephyr Kconfig 选项，或参见 :ref:`cache_api` 了解 API 参考。
本节主要关注数据缓存，尽管对于支持缓存的系统通常还存在指令缓存。

.. note::

  这里的信息假设已启用架构特定的 MPU 支持。详情请参见架构特定的文档。

.. note::

  虽然缓存一致性可能是 SMP 核心之间共享数据时需要关注的问题，但 Zephyr 通常会确保从多个核心观察内存时处于一致状态。
  大多数应用只需要使用缓存 API 与外部硬件交互，例如 DMA 控制器，或运行不同操作系统镜像的外部 CPU。
  有关 SMP 核心之间缓存一致性的更多信息，请参见 :kconfig:option:`CONFIG_KERNEL_COHERENCE`。

当处理处理器核心与其他总线主之间共享的内存时，需要考虑缓存一致性。通常处理器缓存会尽可能靠近每个处理器核心，
以最大化性能收益。正因如此，DMA 引擎移入和移出内存的数据在处理器缓存中会是过时的，从而出现看似损坏的数据。
如果你正在使用 DMA 移动数据，而处理器看不到你期望的数据，那么缓存一致性问题可能就是原因。

有多种方法可以确保处理器核心和外设看到的数据是一致的。最简单的方法就是直接禁用缓存，
但这违背了设置硬件缓存的初衷，并会带来显著的性能损失。许多架构提供了仅为内存的一部分禁用缓存的方法。
当缓存一致性比性能更重要时（例如使用 SPI 配合 DMA 时），这种方法会很有用。
最后，还有在运行时对内存区域执行缓存刷新（flush）或缓存无效化（invalidate）的选项。

全局禁用数据缓存
---------------------------------

如上所述，全局禁用数据缓存可能会有显著的性能影响，但对调试可能很有用。

要求：

* :kconfig:option:`CONFIG_DCACHE`：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT`：启用缓存 API。

* 调用 :c:func:`sys_cache_data_disable()` 全局禁用数据缓存。

为内存区域禁用缓存
-------------------------------------

如果非缓存（uncached）内存上的性能对应用并不关键，那么仅为内存的一部分禁用缓存可以是很好的性能折衷方案。
如果应用需要许多小于缓存行（cache line）的小的、互不相关的缓冲区，这是一个不错的选择。

要求：

* :kconfig:option:`CONFIG_DCACHE`：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_MEM_ATTR`：启用 ``mem-attr`` 库，用于处理设备树中的内存属性。

* 按照 :ref:`mem_mgmt_api` 为你的设备树添加注释。

假设 MPU 驱动已启用，它会在内核初始化期间根据指定的内存属性配置相应的区域。
当使用专用的非缓存内存区域时，需要指示链接器将缓冲区放入该区域。
这可以通过使用 ``Z_GENERIC_SECTION`` 显式指定内存区域来实现：

.. code-block:: c

  /* SRAM4 marked as uncached in device tree */
  uint8_t buffer[BUF_SIZE] Z_GENERIC_SECTION("SRAM4");

.. note::

  为具有单独缓存规则的独立内存区域进行配置，需要使用 MPU 区域，而在某些架构上 MPU 区域可能是有限资源。
  其他内存保护特性（如 :ref:`userspace <mpu_userspace>`、:ref:`stack protection <mpu_stack_objects>`
  或 :ref:`memory domains<memory_domain>`）也可能需要 MPU 区域。

按变量自动禁用缓存
-------------------------------------------

Zephyr 能够自动定义内存中的一个非缓存区域，并使用 ``__nocache`` 将变量分配到其中。
任何用此属性标记的变量都会被放入内存中一个特殊的 ``nocache`` 链接器区域。
该区域会在初始化期间由 MPU 驱动配置为非缓存。与显式声明某内存区域为非缓存相比，这是一种更简单的方案，
但对这些变量的放置控制较少，因为链接器可能将该区域分配在 RAM 的任意位置。

要求：

* :kconfig:option:`CONFIG_DCACHE`：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_NOCACHE_MEMORY`：启用 ``nocache`` 链接器区域的分配，并将其配置为非缓存。

* 在任何非缓存缓冲区定义的末尾添加 ``__nocache`` 属性：

.. code-block:: c

  uint8_t buffer[BUF_SIZE] __nocache;

.. note::

  参见上文关于 MPU 区域可能受限的说明。尽管 ``nocache`` 区域是由 Zephyr 自动创建而非由用户显式定义，
  它仍然是一个独立的 MPU 区域。

运行时缓存控制
---------------------

性能最高但最复杂的选项是在运行时控制数据缓存。在这种情况下，最相关的两个缓存操作是**刷新（flushing）**
和**无效化（invalidating）**。这两个操作都作用于可缓存内存的最小单位——缓存行。
数据缓存行通常为 16 到 128 字节。参见 :kconfig:option:`CONFIG_DCACHE_LINE_SIZE`。
缓存行大小通常在硬件中固定且不可配置，但 Zephyr 需要知道缓存行的大小，才能正确且高效地管理缓存。
如果相关缓冲区小于数据缓存行大小，将它们放在非缓存区域可能更高效，
因为打包进同一缓存行的无关数据在无效化时可能被破坏。

刷新缓存涉及将指定区域中所有被修改过的缓存行写回共享内存。
在处理器向某缓冲区写入之后、远程总线主从该区域读取之前，应刷新与该缓冲区关联的缓存。

.. note::

  某些架构支持一种称为**直写（write-through）**的缓存配置，其中处理器核心的数据写入会直接传播到共享内存。
  虽然这解决了 CPU 写入的缓存一致性问题，但也会导致到主内存的流量增加，可能造成性能下降。

无效化缓存的工作方式类似，但方向相反。它会将指定区域中的缓存行标记为过时，
确保处理器下次从指定区域读取时，缓存行会从主内存重新加载。
在读取某外设写入过的缓冲区之前，应先无效化该缓冲区的数据缓存。

在某些情况下，同一缓冲区可能被重复用于例如 DMA 读取和 DMA 写入。
在这种情况下，可以先刷新与该缓冲区关联的缓存，然后再将其无效化，
从而确保下次处理器从该缓冲区读取时缓存会被刷新。

要求：

* :kconfig:option:`CONFIG_DCACHE`：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT`：启用缓存 API。

* 调用 :c:func:`sys_cache_data_flush_range()` 刷新内存区域。

* 调用 :c:func:`sys_cache_data_invd_range()` 无效化内存区域。

* 调用 :c:func:`sys_cache_data_flush_and_invd_range()` 刷新并无效化。

对齐
---------

正如 :c:func:`sys_cache_data_invd_range()` 及相关函数中所述，缓冲区应对齐到缓存行大小。
这可以通过使用 ``__aligned`` 实现：

.. code-block:: c

  uint8_t buffer[BUF_SIZE] __aligned(CONFIG_DCACHE_LINE_SIZE);
