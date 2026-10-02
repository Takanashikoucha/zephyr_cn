.. _language_c:

C 语言支持
##################

C 是一种通用的低级编程语言，
广泛用于编写嵌入式系统的代码。

Zephyr 主要使用 C 语言编写，
并原生支持使用 C 语言编写的应用。
所有 Zephyr API 函数和宏都用 C 实现，
并作为 :file:`include` 目录下 C 头文件的一部分提供，
因此使用 C 语言编写 Zephyr 应用
可以让开发者访问最多的功能。

``main()`` 函数的返回类型必须是 ``int``，
因为 Zephyr 应用运行在 C 标准定义的
"hosted"（宿主）环境中。
应用必须从 main 返回零（0）。
所有非零返回值均被保留。

.. _c_standards:

语言标准
******************

Zephyr 并不针对 C 标准的某个特定版本；
不过，Zephyr 代码库大量使用了
1999 年发布的 ISO C 标准
（ISO/IEC 9899:1999，后文简称 C99）
中新引入的特性，例如以下所列，
这实际上要求使用支持 C99 标准及更高标准的
编译器工具链：

* 内联函数
* 标准布尔类型（``<stdbool.h>`` 中的 ``bool``）
* 固定宽度整数类型（``<stdint.h>`` 中的 ``[u]intN_t``）
* 指定初始化器
* 可变参数宏
* ``restrict`` 限定符

此外，某些组件或其部分使用了
标准 C11 和 C17 版本
（分别为 ISO/IEC 9899:2011 和 9899:2018）
中引入的特性：

* ``_Generic`` 关键字
* ``_Static_assert`` 关键字

总之，推荐使用至少支持 C17 标准的编译器工具链来开发 Zephyr。
不过需要注意，某些可选的 Zephyr 组件和外部模块
可能使用了标准较新版本中引入的 C 语言特性，
在这种情况下就需要使用更新的、支持这些标准的编译器工具链。

.. _c_library:

标准库
****************

`C 标准库`_ 是任何 C 程序不可或缺的组成部分，
Zephyr 提供了对多个不同 C 库的支持供应用选择，
具体取决于用于构建应用的编译器工具链。

.. toctree::
   :maxdepth: 2

   common_libc.rst
   minimal_libc.rst
   newlib.rst
   picolibc.rst

.. _`C 标准库`: https://en.wikipedia.org/wiki/C_standard_library

.. _c_library_formatted_output:

格式化输出
****************

C 定义了标准格式化输出函数，
例如 ``printf`` 和 ``sprintf``，
这些函数由 C 标准库实现。

每个 C 标准库都有自己的一套要求和配置，
用于选择格式化输出的模式与能力。
更多细节请参考各 C 标准库的文档。

.. _c_library_dynamic_mem:

动态内存管理
*************************

C 定义了标准动态内存管理接口
（例如 :c:func:`malloc` 和 :c:func:`free`），
这些函数由 C 标准库实现。

尽管动态内存管理实现的细节在不同 C 标准库之间各不相同，
但所有受支持的库都必须遵循以下约定。
每个受支持的 C 标准库都应当：

* 自行管理其内存堆，无论是内部管理
  还是通过调用在 :file:`libc-hooks.c` 中实现的
  钩子函数（例如 :c:func:`sbrk`）。

* 维护针对标准动态内存分配接口
  （例如 :c:func:`malloc`）所分配的内存块的
  架构相关和内存区域相关的对齐要求。

* 在启用用户空间时，
  在 ``z_malloc_partition`` 内存分区内分配内存块。
  参见 :ref:`memory_domain_predefined_partitions`。

关于 C 标准库特定内存管理实现的更多细节，
请参考各 C 标准库的文档。

.. note::
   原生 Zephyr 应用应当使用 Zephyr 内核支持的
   :ref:`内存管理 API <memory_management_api>`，
   例如 :c:func:`k_malloc`，
   以便利用其提供的高级功能。

   例如 :c:func:`malloc` 这样的
   C 标准动态内存管理接口函数
   只应由面向多个操作系统的
   可移植应用和库使用。
