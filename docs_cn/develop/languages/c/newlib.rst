.. _c_library_newlib:

Newlib
######

`Newlib`_ 是一个为嵌入式系统编写的
完整 C 库实现。它是一个独立的开源项目，
并不以源代码形式包含在 Zephyr 中。
相反，:ref:`toolchain_zephyr_sdk` 为每个受支持的架构
包含一个预编译库（:file:`libc.a` 和
:file:`libm.a`）。

.. note::
   其他第三方工具链（例如 :ref:`toolchain_gnuarmemb`）
   也捆绑了 Newlib 的预编译库。

Zephyr 实现了被 Newlib 中的
C 标准库函数调用的 "API hook" 函数。
这些钩子函数在 :file:`lib/libc/newlib/libc-hooks.c`
中实现，并将库内部的系统调用
转换为等价的 Zephyr API 调用。

Newlib 类型
***************

:ref:`toolchain_zephyr_sdk` 中包含的 Newlib
有两个版本：'full' 和 'nano' 变体。

Full Newlib
===========

Newlib full 变体（:file:`libc.a` 和 :file:`libm.a`）
是 Zephyr SDK 中可用的功能最完整的
Newlib 变体，支持几乎所有标准 C 库功能。
它针对性能进行了优化（性能优先于代码大小），
其占用空间显著大于 nano 变体。

该变体可以通过在应用配置文件中
选择 :kconfig:option:`CONFIG_NEWLIB_LIBC`
并取消选择 :kconfig:option:`CONFIG_NEWLIB_LIBC_NANO`
来启用。

Nano Newlib
===========

Newlib nano 变体（:file:`libc_nano.a` 和
:file:`libm_nano.a`）是 Newlib 的大小优化版本，
支持 full 变体支持的所有功能，
但不支持 C99 引入的新格式说明符，
例如 ``char`` 和 ``long long`` 类型的
格式说明符（即 ``%hhX`` 和 ``%llX``）。

该变体可以通过在应用配置文件中
选择 :kconfig:option:`CONFIG_NEWLIB_LIBC`
和 :kconfig:option:`CONFIG_NEWLIB_LIBC_NANO`
来启用。

请注意，Newlib nano 变体并非对所有架构都可用。
nano 变体的可用性由
:kconfig:option:`CONFIG_HAS_NEWLIB_LIBC_NANO` 指定。

.. _`Newlib`: https://sourceware.org/newlib/

格式化输出
****************

Newlib 支持所有标准 C 格式化输入和输出函数，
包括 ``printf``、``fprintf``、``sprintf`` 和 ``sscanf``。

Newlib 的格式化输入和输出函数实现
支持 C 标准定义的所有格式说明符，
但有以下例外：

* 浮点格式说明符（例如 ``%f``）需要启用
  :kconfig:option:`CONFIG_NEWLIB_LIBC_FLOAT_PRINTF` 和
  :kconfig:option:`CONFIG_NEWLIB_LIBC_FLOAT_SCANF`。
* C99 格式说明符不被 Newlib nano 变体支持
  （即 ``char`` 的 ``%hhX``、``long long`` 的 ``%llX``、
  ``intmax_t`` 的 ``%jX``、``size_t`` 的 ``%zX``、
  ``ptrdiff_t`` 的 ``%tX``）。

动态内存管理
*************************

Newlib 实现了一个内部堆分配器，
用于管理标准动态内存管理接口函数
（例如 :c:func:`malloc` 和 :c:func:`free`）
所使用的内存块。

Newlib 实现的内部堆分配器
可能因所使用的 Newlib 类型不同而有所差异。
例如，Zephyr SDK 的 Full Newlib
（:file:`libc.a` 和 :file:`libm.a`）中实现的
堆分配器会向操作系统请求更大的内存块，
与 Nano Newlib（:file:`libc_nano.a` 和
:file:`libm_nano.a`）相比，
其最小内存需求显著更高。

Newlib 动态内存管理函数与
Zephyr 侧 libc 钩子之间唯一的接口
是 :c:func:`sbrk` 函数，
Newlib 用它来管理为其内部堆分配器
保留的内存池的大小。

在 :file:`libc-hooks.c` 中实现的
:c:func:`_sbrk` 钩子函数
处理来自 Newlib 的内存池大小变更请求，
并在系统内存不足时返回错误，
从而确保 Newlib 内部堆分配器的
内存池大小不超过可用内存空间的数量。

当启用用户空间时，
Newlib 内部堆分配器的内存池
被放置在一个名为 ``z_malloc_partition`` 的
专用内存分区中，该分区可以被用户模式线程访问。

Newlib 堆可用的内存空间数量
取决于系统配置：

* 当启用 MMU（选择了 :kconfig:option:`CONFIG_MMU`）时，
  为 Newlib 堆保留的内存空间数量
  由 :c:func:`k_mem_free_get` 函数返回的
  空闲内存空间大小或
  :kconfig:option:`CONFIG_NEWLIB_LIBC_MAX_MAPPED_REGION_SIZE`
  决定，取其中最小者。

* 当启用 MPU 且 MPU 需要 2 的幂次方的
  分区大小和地址对齐
  （:kconfig:option:`CONFIG_NEWLIB_LIBC_ALIGNED_HEAP_SIZE`
  被设置为非零值）时，
  为 Newlib 堆保留的内存空间数量
  由 :kconfig:option:`CONFIG_NEWLIB_LIBC_ALIGNED_HEAP_SIZE` 决定。

* 否则，为 Newlib 堆保留的内存空间数量
  等于 SRAM 区域中空闲（未分配）内存的数量。

Newlib 实现的标准动态内存管理接口函数
是线程安全的，可以被多个线程同时调用。
