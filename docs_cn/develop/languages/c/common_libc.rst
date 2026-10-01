.. _c_library_common:

通用 C 库代码
#####################

Zephyr 提供一些 C 库函数，设计用于与多个 C 库配合使用。
这些函数要么提供多个 C 库中不可用的功能，要么用更适合在 Zephyr 环境中使用的代码替换 C 库中的功能。

时间函数
*************

它提供了标准 C 函数 :c:func:`time` 的实现，依赖 Zephyr 函数 :c:func:`sys_clock_gettime`。这个函数可以通过选择 :kconfig:option:`COMMON_LIBC_TIME` 启用。

动态内存管理
*************************

通用动态内存管理实现可以通过在应用配置文件中选择 :kconfig:option:`CONFIG_COMMON_LIBC_MALLOC` 来启用。

通用 C 库内部使用 :ref:`内核内存堆 API <heap_v2>` 来管理内存堆，
该堆被 :c:func:`malloc` 和 :c:func:`free` 等标准动态内存管理接口函数使用。

内部内存堆通常位于 ``.bss`` 段中。不过，当启用用户空间时，
它被放置在一个名为 ``z_malloc_partition`` 的专用内存分区中，该分区可以被用户模式线程访问。
内部内存堆的大小由 :kconfig:option:`CONFIG_COMMON_LIBC_MALLOC_ARENA_SIZE` 指定。

使用通用 C 库的应用的默认堆大小为零（无堆）。
对于其他 C 库用户，如果存在 MMU，则默认堆为 16kB。否则，堆使用所有可用内存。

另外还有独立的控制选项来选择 :c:func:`calloc`（:kconfig:option:`COMMON_LIBC_CALLOC`）
和 :c:func:`reallocarray`（:kconfig:option:`COMMON_LIBC_REALLOCARRAY`）。
这两者默认均启用，因为在不使用它们的应用中启用并不影响内存占用。

通用 C 库实现的标准动态内存管理接口函数是线程安全的，可以被多个线程同时调用。
这些函数实现在 :file:`lib/libc/common/source/stdlib/malloc.c` 中。
