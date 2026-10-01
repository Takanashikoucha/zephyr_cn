.. _memory_domain:

内存保护设计
########################

Zephyr 的内存保护设计面向具有 MPU（Memory Protection Unit，内存保护单元）硬件的微控制器。
我们也支持某些具有分页 MMU（Memory Management Unit，内存管理单元）的架构（例如 x86），
但在那种情况下，MMU 是像 MPU 一样使用的，配合一个恒等（identity）页表。

以下所有讨论都将使用 MPU 术语；
具有 MMU 的系统可以被视为拥有一个数量无限制的可编程区域的 MPU。

当启用 Zephyr 的内存保护特性时，内存访问的配置有若干不同的级别，
下面逐一描述：

启动时内存配置
******************************

这是内核启动之后 MPU 的配置。它应包含以下内容：

- 任何需要特殊缓存（caching）或写回（write-back）策略
  以支持基本硬件和驱动功能的内存区域配置。
  注意大多数 MPU 都有默认内存访问策略映射的概念，
  它可以作为"背景"映射启用，覆盖任何没有被 MPU 区域配置到的内存区域。
  强烈建议使用该机制，以最大化可供最终用户使用的 MPU 区域数量。
  在 ARMv7-M/ARMv8-M 上这被称为系统地址映射（System Address Map），
  其他 CPU 可能有类似能力。有关如何在设备树中标注系统映射的信息，
  参见 :ref:`mem_mgmt_api`。

- 一个（或几个）只读、可执行区域，用于程序文本（text）和只读数据（ro-data），
  且用户模式可访问。它可以进一步细分为 ro-data 的只读区域
  和 text 的只读可执行区域，但这需要额外的 MPU 区域。
  这是必需的，以便运行在用户模式的线程能够读取 ro-data 并取指（fetch 指令）。

- 根据配置，支持 GCOV、HEP 等额外特性的用户可访问读写区域。

假设存在一个允许超级用户模式访问其所需任何内存的背景映射，
并且定义了授予用户模式 text/ro-data 访问权限的区域，
这就足以满足启动时的配置。

硬件栈溢出
***********************

:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 是一个可选特性，
在系统运行于超级用户模式时检测栈缓冲区溢出。
它捕获的是整个栈缓冲区溢出的问题，而不是单个栈帧溢出——
后者请使用编译器辅助的 :kconfig:option:`CONFIG_STACK_CANARIES`。

与超级用户模式中的任何崩溃一样，
超级用户模式栈溢出之后无法对系统的整体健康状况做出任何保证，
任何此类情况都应被视为严重错误。
然而，知道这些溢出何时发生仍然非常有价值，
因为如果没有稳健的检测逻辑，
栈缓冲区溢出会导致系统以神秘的方式崩溃，或以未定义的方式运行。

某些系统通过运行时创建一个"保护"（guard）MPU 区域来实现此特性，
该区域被设置为只读，位于超级用户模式栈缓冲区的开头或紧接其前。
如果栈发生溢出，将产生一个异常。

此特性是可选的，捕获用户模式栈溢出并不需要它；
禁用它可能根据 MPU 设计释放 1-2 个 MPU 区域。

其他系统可能有专用的 CPU 支持来捕获栈溢出，不需要额外的 MPU 区域。

线程栈
************

任何运行在用户模式的线程都需要访问自己的栈缓冲区。
在上下文切换到用户模式线程时，
会用栈缓冲区的边界来配置一个专用的 MPU 区域或 MMU 页表项。
超出其栈缓冲区的线程将开始向它无权访问的内存推送数据，
从而产生一个内存访问违例异常。

注意，用户线程可以访问同一内存域中其他用户线程的栈。
这是架构支持内存域所需的最小要求。
架构可以进一步限制栈访问，使每个用户线程只能访问自己的栈——
前提是此类架构通过
:kconfig:option:`CONFIG_ARCH_MEM_DOMAIN_SUPPORTS_ISOLATED_STACKS` 声明了该能力。
如果支持，此行为默认启用；
如果架构支持两种运行模式，
可以通过 :kconfig:option:`CONFIG_MEM_DOMAIN_ISOLATED_STACKS` 选择性地禁用它。
然而，某些架构可能决定始终启用此行为，因此该选项无法禁用。
无论这些 Kconfig 如何设置，
用户线程都不能访问其内存域之外其他用户线程的栈。

线程资源池
*********************

一小部分作为系统调用调用的内核 API 需要堆内存分配。
这些内存仅供内核使用，用户模式不能直接访问。
要使用这些系统调用，调用线程必须把自己分配给一个资源池，
即一个 :c:struct:`k_heap` 对象。
内存通过 :c:func:`z_thread_malloc` 从线程的资源池中取出，
并用 :c:func:`k_free` 释放。

使用资源池的 API 如下，
为不想在应用程序中做堆分配的用户注明了替代方案：

 - :c:func:`k_stack_alloc_init` 设置一个 k_stack，
   其存储缓冲区从资源池分配，而不是使用用户提供的缓冲区。
   替代方案是用 :c:macro:`K_STACK_DEFINE()` 声明在启动时自动初始化的 k_stack，
   或在超级用户模式下用 :c:func:`k_stack_init` 初始化 k_stack。

 - :c:func:`k_msgq_alloc_init` 设置一个 k_msgq 对象，
   其存储缓冲区从资源池分配，而不是使用用户提供的缓冲区。
   替代方案是用 :c:macro:`K_MSGQ_DEFINE()` 声明在启动时自动初始化的 k_msgq，
   或在超级用户模式下用 :c:func:`k_msgq_init` 初始化 k_msgq。

 - :c:func:`k_poll` 从用户模式调用时，
   在等待事件期间需要制作所提供事件数组的一份内核侧副本。
   该副本在 :c:func:`k_poll` 因任何原因返回时被释放。

 - :c:func:`k_queue_alloc_prepend` 和 :c:func:`k_queue_alloc_append`
   会分配一个容器结构体来放置数据，
   因为定义队列的内部簿记（bookkeeping）信息不能放在用户提供的内存中。

 - :c:func:`k_object_alloc` 允许在运行时动态分配整个内核对象，
   并向调用者返回一个可用的指针。

相关的 API 是 :c:func:`k_thread_heap_assign`，
它为目标线程分配一个 k_heap，从这些分配中取出内存。

如果启用了系统堆，可以用 :c:func:`k_thread_system_pool_assign` 使用系统堆，
但最好让在系统上运行的不同逻辑应用程序拥有各自的池。

内存域
**************

内核确保任何用户线程都能访问自己的栈缓冲区，
以及程序文本和只读数据。
内存域 API 是向用户线程授予额外内存块访问权限的方式。

概念上，一个内存域是一组内存分区的集合。
一个域中内存分区的最大数量受可用 MPU 区域数量的限制。
这就是为什么把启动时 MPU 区域数量最小化很重要。

内存域*不*用于控制超级用户模式对内存的访问。
在某些情况下这可能不可避免；
例如，某些架构不允许定义"用户模式只读、但超级用户模式可读写"的区域。
操作此类区域时必须非常小心，避免无意中导致内核在访问该区域时崩溃。
任何试图用内存域 API 控制超级用户模式访问的行为，充其量是未定义行为；
超级用户模式的访问策略只应通过启动时内存区域来控制。

内存域 API 只对超级用户模式可用。
用户模式对内存域的唯一控制是：
任何用户线程的子线程会自动成为父线程所在域的成员。

所有线程都是某个内存域的成员，包括超级用户线程
（尽管这对其内存访问没有影响）。
有一个默认域 ``k_mem_domain_default``，
如果线程没有被明确分配到某个域，或者没有从父线程继承内存域成员资格，
就会被分配到该默认域。主线程作为默认域的成员开始运行。

内存分区
================

每个内存分区由一个内存地址、一个大小和一组访问属性组成。
内存分区用于控制对系统内存的访问。定义内存分区受以下约束：

- 分区必须表示底层内存管理硬件可编程的一个内存区域，
  并符合底层硬件的任何约束。
  例如，许多基于 MPU 的系统要求分区大小取 2 的幂，并对齐到其自身大小。
  对于基于 MMU 的系统，分区必须对齐到页，且大小是页大小的整数倍。

- 同一内存域中的分区不得相互重叠。
  内存域中的分区之间没有优先级的概念。
  内存域中的分区假定具有比任何启动时内存区域更高的优先级，
  但内存域分区能否与启动时内存区域重叠，则取决于架构。

- 同一个分区可以指定在多个内存域中。
  例如，可能存在一个共享内存区域，多个域都授予对其的访问。

- 确定要在分区中暴露哪些内存时必须小心。
  向包含内核私有数据的任何内存提供直接的用户模式访问是不恰当的。

- 内存域分区用于控制对系统 RAM 的访问。
  不对应于 RAM 的内存分区配置可能不被架构支持；
  对于基于 MMU 的系统，情况确实如此。

有两种方式定义内存分区：手动或自动。

手动内存分区
------------------------

以下代码声明了一个全局数组 ``buf``，
然后为它声明了一个读写分区，该分区可以被添加到某个域中：

.. code-block:: c

    uint8_t __aligned(32) buf[32];

    K_MEM_PARTITION_DEFINE(my_partition, buf, sizeof(buf),
                           K_MEM_PARTITION_P_RW_U_RW);

当我们试图把分散在若干 C 文件中的多个对象容纳进单个分区时，
这种方式的扩展性不太好。

自动内存分区
---------------------------

自动内存分区由构建系统创建。
所有需要放入某个分区的全局变量都以其目标分区进行标记。
构建系统随后把这些数据合并为一个单一的连续内存块，
在启动时清零所有 BSS 变量，
并定义一个具有适当基地址和大小的内存分区，包含所有被标记的数据。

.. figure:: auto_mem_domain.png
   :alt: 自动内存域构建流程
   :align: center

   自动内存域构建流程

自动内存分区只配置为读写区域。
它们用 :c:macro:`K_APPMEM_PARTITION_DEFINE()` 定义。
全局变量随后通过 :c:macro:`K_APP_DMEM()`（用于已初始化数据）
和 :c:macro:`K_APP_BMEM()`（用于 BSS）路由到该分区。

.. code-block:: c

    #include <zephyr/app_memory/app_memdomain.h>

    /* Declare a k_mem_partition "my_partition" that is read-write to
     * user mode. Note that we do not specify a base address or size.
     */
    K_APPMEM_PARTITION_DEFINE(my_partition);

    /* The global variable var1 will be inside the bounds of my_partition
     * and be initialized with 37 at boot.
     */
    K_APP_DMEM(my_partition) int var1 = 37;

    /* The global variable var2 will be inside the bounds of my_partition
     * and be zeroed at boot size K_APP_BMEM() was used, indicating a BSS
     * variable.
     */
    K_APP_BMEM(my_partition) int var2;

构建系统会确保 ``my_partition`` 的基地址正确对齐，
且区域的总大小符合内存管理硬件的要求，必要时添加填充（padding）。

如果创建多个分区，可以使用 ``app_macro_support.h`` 中提供的可变参数预处理器宏：

.. code-block:: c

    FOR_EACH(K_APPMEM_PARTITION_DEFINE, part0, part1, part2);

静态库全局变量的自动分区
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

用于设置自动内存分区的构建时逻辑在 ``scripts/build/gen_app_partitions.py`` 中。
如果一个静态库被链接进 Zephyr，
可以用 ``--library`` 参数将该库中所有全局变量路由到某个特定的内存分区。

例如，如果启用了 Newlib C 库，Newlib 的所有全局变量都需要放在 ``z_libc_partition`` 中。
顶层 ``CMakeLists.txt`` 中对脚本的调用添加了以下内容：

.. code-block:: none

    gen_app_partitions.py ... --library libc.a z_libc_partition ..

对于预编译的库，项目级配置或构建文件中没有支持表达这一点的方式；
必须编辑顶层 ``CMakeLists.txt``。

对于使用 ``zephyr_library`` 或 ``zephyr_library_named`` 创建的 Zephyr 库，
可以使用 ``zephyr_library_app_memory`` 函数
指定该库中所有全局变量应放入的内存分区。

.. _memory_domain_predefined_partitions:

预定义内存分区
-----------------------------

有若干由系统预定义的内存分区：

 - ``z_malloc_partition`` - 该分区包含 libc malloc() 使用的系统级内存池。
   由于可能存在资源饥饿（starvation）问题，
   不建议从全局池中取堆内存；更好的做法是定义各种 sys_heap 对象
   并将它们分配给特定的内存域。

 - ``z_libc_partition`` - 包含 C 库和运行时所需的全局变量。
   使用 Minimal C 库或 Newlib C 库时必需。
   启用 :kconfig:option:`CONFIG_STACK_CANARIES` 时必需。

库专属的分区列在 :zephyr_file:`include/zephyr/app_memory/partitions.h` 中。
例如，要从用户模式使用 MBEDTLS 库，必须把 ``k_mbedtls_partition`` 添加到该域中。

内存域使用
==================

创建内存域
----------------------

内存域使用 :c:struct:`k_mem_domain` 类型的变量定义。
之后必须通过调用 :c:func:`k_mem_domain_init` 初始化。

以下代码定义并初始化一个空的内存域。

.. code-block:: c

    struct k_mem_domain app0_domain;

    k_mem_domain_init(&app0_domain, 0, NULL);

向内存域添加内存分区
------------------------------------------

有两种方式向内存域添加内存分区。

第一个代码示例展示如何在创建内存域时添加内存分区。

.. code-block:: c

    /* the start address of the MPU region needs to align with its size */
    uint8_t __aligned(32) app0_buf[32];
    uint8_t __aligned(32) app1_buf[32];

    K_MEM_PARTITION_DEFINE(app0_part0, app0_buf, sizeof(app0_buf),
                           K_MEM_PARTITION_P_RW_U_RW);

    K_MEM_PARTITION_DEFINE(app0_part1, app1_buf, sizeof(app1_buf),
                           K_MEM_PARTITION_P_RW_U_RO);

    struct k_mem_partition *app0_parts[] = {
        app0_part0,
        app0_part1
    };

    k_mem_domain_init(&app0_domain, ARRAY_SIZE(app0_parts), app0_parts);

第二个代码示例展示如何逐个向已初始化的内存域添加内存分区。

.. code-block:: c

    /* the start address of the MPU region needs to align with its size */
    uint8_t __aligned(32) app0_buf[32];
    uint8_t __aligned(32) app1_buf[32];

    K_MEM_PARTITION_DEFINE(app0_part0, app0_buf, sizeof(app0_buf),
                           K_MEM_PARTITION_P_RW_U_RW);

    K_MEM_PARTITION_DEFINE(app0_part1, app1_buf, sizeof(app1_buf),
                           K_MEM_PARTITION_P_RW_U_RO);

    k_mem_domain_add_partition(&app0_domain, &app0_part0);
    k_mem_domain_add_partition(&app0_domain, &app0_part1);

.. note::
    内存分区的最大数量受 MPU 区域最大数量或 MMU 表最大数量的限制。

内存域分配
------------------------

任何线程都可以加入一个内存域，任何内存域也可以有多个线程被分配到它。
线程通过一个 API 调用被分配到内存域：

.. code-block:: c

    k_mem_domain_add_thread(&app0_domain, app_thread_id);

如果该线程已经是其他某个域（包括默认域）的成员，
它将从原域中移除，转而加入新域。

此外，如果一个线程是某个内存域的成员，并且它创建了一个子线程，
该子线程也将属于该域。

从内存域中移除内存分区
----------------------------------------------

以下代码展示如何从内存域中移除一个内存分区。

.. code-block:: c

    k_mem_domain_remove_partition(&app0_domain, &app0_part1);

k_mem_domain_remove_partition() API 会查找与给定参数匹配的内存分区，
并从内存域中移除该分区。

可用的分区属性
------------------------------

定义分区时，需要为该分区设置访问权限属性。
由于内存分区的访问控制依赖 MPU 或 MMU，可用的分区属性因架构而异。

某个特定架构的可用分区属性完整列表，
可在架构专属的 include 文件 ``include/zephyr/arch/<arch name>/arch.h`` 中找到
（例如 :zephyr_file:`include/zephyr/arch/arm/arch.h`）。
分区属性的若干示例：

.. code-block:: c

    /* Denote partition is privileged read/write, unprivileged read/write */
    K_MEM_PARTITION_P_RW_U_RW
    /* Denote partition is privileged read/write, unprivileged read-only */
    K_MEM_PARTITION_P_RW_U_RO

在几乎所有情况下，``K_MEM_PARTITION_P_RW_U_RW`` 都是正确的选择。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_MAX_DOMAIN_PARTITIONS`

API 参考
*************

以下内存域 API 由 :zephyr_file:`include/zephyr/kernel.h` 提供：

.. doxygengroup:: mem_domain_apis
