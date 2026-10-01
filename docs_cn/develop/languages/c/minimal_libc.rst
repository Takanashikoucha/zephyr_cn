.. _c_library_minimal:

最小 libc
############

最基础的 C 库名为 "minimal libc"，
它是 Zephyr 代码库的一部分，
提供满足 Zephyr 及其子系统需求所需的
标准 C 库最小子集，
主要涉及字符串操作和显示领域。

它的占用空间非常小，适合不依赖 ISO C 标准库中较少使用部分的项目。它也可以与多种不同的工具链配合使用。

最小 libc 的实现位于
主 Zephyr 代码树的 :file:`lib/libc/minimal` 中。

函数
*********

最小 libc 实现了满足 Zephyr 内核需求所需的
ISO/IEC 9899:2011 标准 C 库函数的最小子集，
该最小子集由 :ref:`编码指南规则 A.4
<coding_guideline_libc_usage_restrictions_in_zephyr_kernel>` 定义。

格式化输出
****************

最小 libc 不实现自己的格式化输出处理器；
相反，它将 ``printf`` 和 ``sprintf`` 等
C 标准格式化输出函数
映射到 :c:func:`cbprintf` 函数，
后者是 Zephyr 自己的
C99 兼容格式化输出实现。

更多细节，请参考 :ref:`格式化输出 <formatted_output>`
操作系统服务文档。

动态内存管理
*************************

最小 libc 使用 :ref:`通用 C 库 <c_library_common>`
提供的 malloc API 系列实现，
后者本身构建在
:ref:`内核内存堆 API <heap_v2>` 之上。

错误号
*************

错误号在 Zephyr API 中广泛使用，
作为函数的返回值来指示错误条件。
它们通常以本节定义的
整数字面量的负值形式返回，
并在 :file:`errno.h` 头文件中定义。

`POSIX errno.h 规范`_ 和其他事实标准来源中
定义的一部分错误号
已被添加到最小 libc 中。

Zephyr 会有意识地保持最小 libc
错误号的值与 Zephyr 支持的
各 C 标准库实现中的值保持一致。
最小 libc 的 :file:`errno.h` 会对照
:ref:`Newlib <c_library_newlib>` 的相应文件进行检查，
以确保错误号保持对齐。

下面是错误号定义的列表。
实际数值请参考 `errno.h`_。

.. doxygengroup:: system_errno

.. _`POSIX errno.h 规范`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/errno.h.html
.. _`errno.h`: https://github.com/zephyrproject-rtos/zephyr/blob/main/lib/libc/minimal/include/errno.h
