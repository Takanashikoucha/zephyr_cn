.. _c_library_picolibc:

Picolibc
########

`Picolibc`_ 是一个为嵌入式系统编写的
完整 C 库实现，
目标是 `C17 (ISO/IEC 9899:2018)`_ 和
`POSIX 2018 (IEEE Std 1003.1-2017)`_ 标准。
Picolibc 是一个外部开源项目，
作为模块提供给 Zephyr，
并以预编译形式作为 :ref:`toolchain_zephyr_sdk`
的一部分包含，
覆盖每个受支持的架构（:file:`libc.a`）。

.. note::
   Picolibc 也对其他第三方工具链可用，
   例如 :ref:`toolchain_gnuarmemb`。

Zephyr 实现了被 Picolibc 中的
C 标准库函数调用的 "API hook" 函数。
这些钩子函数在 :zephyr_file:`lib/libc/picolibc/`
中实现，并将库内部的系统调用
转换为等价的 Zephyr API 调用。

.. _`Picolibc`: https://github.com/picolibc/picolibc
.. _`C17 (ISO/IEC 9899:2018)`: https://www.iso.org/standard/74528.html
.. _`POSIX 2018 (IEEE Std 1003.1-2017)`: https://pubs.opengroup.org/onlinepubs/9699919799/functions/printf.html

.. _c_library_picolibc_module:

Picolibc 模块
===============

当作为 Zephyr 模块构建时，有几个配置项可用于调整库中的功能集，在库所支持的功能与最终函数的代码大小之间取得平衡。由于标准 C++ 库必须针对目标 C 库编译，Picolibc 模块不能与使用标准 C++ 库的应用一起使用。构建 Picolibc 模块会增加编译应用所需的时间。

Picolibc 模块可以通过在应用配置文件中
选择 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`
来启用。

当把 Picolibc 模块更新到新版本时，
:ref:`Zephyr SDK 中工具链捆绑的 Picolibc
<c_library_picolibc_toolchain>`
也必须更新到相同版本。

.. _c_library_picolibc_toolchain:

工具链 Picolibc
==================

从版本 0.16 开始，Zephyr SDK
包含每个目标架构的 Picolibc 预编译版本，
以及 libstdc++ 的预编译版本。

工具链版本的 Picolibc
可以通过在应用配置文件中
取消选择 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`
来启用。

对于 Zephyr 的每个版本发布，
在使用 :ref:`推荐版本的 Zephyr SDK <toolchain_zephyr_sdk_compatibility>`
时，工具链捆绑的 Picolibc 和
:ref:`Picolibc 模块 <c_library_picolibc_module>`
保证保持同步。

不使用工具链捆绑 Picolibc 构建
-------------------------------------------

对于没有捆绑 Picolibc 的工具链，
仍然可以通过从源代码构建来使用 Picolibc。
请注意，:ref:`c_library_picolibc_module`
中提到的任何限制仍然适用。

要不使用工具链捆绑的 Picolibc 构建，
工具链必须启用 :kconfig:option:`CONFIG_PICOLIBC_SUPPORTED`。
例如，这需要添加到工具链 Kconfig 文件：

.. code-block:: kconfig

   config TOOLCHAIN_<name>_PICOLIBC_SUPPORTED
     def_bool y
     select PICOLIBC_SUPPORTED

通过启用 :kconfig:option:`CONFIG_PICOLIBC_SUPPORTED`，
当没有工具链捆绑的 Picolibc 时，
构建系统会自动通过其模块
从源代码构建 Picolibc。

格式化输出
****************

Picolibc 支持所有标准 C 格式化输入和输出函数，
包括 :c:func:`printf`、:c:func:`fprintf`、
:c:func:`sprintf` 和 :c:func:`sscanf`。

Picolibc 的格式化输入和输出函数实现
支持 C17 和 POSIX 2018 标准定义的
所有格式说明符，但有以下例外：

* 浮点格式说明符（例如 ``%f``）需要
  :kconfig:option:`CONFIG_PICOLIBC_IO_FLOAT`。

* long long 格式说明符（例如 ``%lld``）需要
  :kconfig:option:`CONFIG_PICOLIBC_IO_LONG_LONG`。
  该选项会随 :kconfig:option:`CONFIG_PICOLIBC_IO_FLOAT`
  自动启用。

Printk、cbprintf 及相关函数
****************************

使用 Picolibc 时，Zephyr 格式化输出函数通过 stdio 调用来实现。这包括：

 * printk、snprintk 和 vsnprintk
 * cbprintf 和 cbvprintf
 * fprintfcb、vfprintfcb、printfcb、vprintfcb、
   snprintfcb 和 vsnprintfcb

当使用带标签参数（:kconfig:option:`CONFIG_CBPRINTF_PACKAGE_SUPPORT_TAGGED_ARGUMENTS` 和 :c:macro:`CBPRINTF_PACKAGE_ARGS_ARE_TAGGED`）时，对 cbpprintf 的调用不会使用 Picolibc，因此使用这些代码格式化输出的结果会与 Picolibc 的结果不同，因为 cbprintf 函数并不完全符合 C/POSIX 标准。

数学函数
**************

Picolibc 为 float、double 和 long double
数学运算提供完整的
C17/`IEEE STD 754-2019`_ 支持，
但不包括 Bessel 函数的 long double 版本。

.. _`IEEE STD 754-2019`: https://ieeexplore.ieee.org/document/8766229

线程本地存储
********************

Picolibc 使用线程本地存储（TLS）
（在受支持时）来存放
应当保持为每个线程局部的数据，
例如 :c:macro:`errno`。
这意味着使用 Picolibc 时
TLS 支持会被启用。
由于所有 TLS 变量都从线程栈区域分配，
这可能会使栈大小需求增加几个字节。

C 库本地变量
*************************

Picolibc 使用几个内部变量
来处理堆管理之类的事情。
这些变量被收集在一个名为
:c:var:`z_libc_partition` 的专用内存分区中。
使用 :kconfig:option:`CONFIG_USERSPACE`
和内存域的应用必须确保
该分区被包含在
Picolibc 调用期间活跃的任何域中。

动态内存管理
*************************

Picolibc 使用 :ref:`通用 C 库 <c_library_common>`
提供的 malloc API 系列实现，
后者本身构建在
:ref:`内核内存堆 API <heap_v2>` 之上。
