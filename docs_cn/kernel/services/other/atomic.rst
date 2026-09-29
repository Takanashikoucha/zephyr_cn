.. _atomic_v2:

原子服务
###############

:dfn:`原子变量`是可以被线程和 ISR 以不可中断方式读取和修改的变量。
在 32 位机器上它是 32 位变量，在 64 位机器上是 64 位变量。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的原子变量（仅受可用 RAM 限制）。

使用内核的原子 API 操作原子变量，
可以确保所需的操作正确执行，
即使更高优先级的上下文也在操作同一个变量。

内核还支持对原子变量数组中单个位的原子操作。

实现
**************

定义原子变量
===========================

原子变量使用 :c:type:`atomic_t` 类型的变量来定义。

默认情况下原子变量被初始化为零。不过，可以使用
:c:macro:`ATOMIC_INIT` 赋予它不同的值：

.. code-block:: c

    atomic_t flags = ATOMIC_INIT(0xFF);

操作原子变量
==============================

原子变量使用本节末尾列出的 API 进行操作。

下面的代码展示了如何使用原子变量来跟踪函数被调用的次数。
由于计数是原子递增的，即使调用该函数的线程被
同样调用该例程的更高优先级上下文中断，
也不存在计数在递增中途被损坏的风险。

.. code-block:: c

    atomic_t call_count;

    int call_counting_routine(void)
    {
        /* increment invocation counter */
        atomic_inc(&call_count);

        /* do rest of routine's processing */
        ...
    }

操作原子变量数组
=========================================

可以按照常规方式定义一个 32 位原子变量数组。
不过，也可以使用 :c:macro:`ATOMIC_DEFINE` 定义一个 N 位的原子变量数组。

原子变量数组中的单个位可以使用本节末尾以 :c:func:`_bit`
结尾的 API 进行操作。

下面的代码展示了如何使用原子变量数组实现一组 200 个标志位。

.. code-block:: c

    #define NUM_FLAG_BITS 200

    ATOMIC_DEFINE(flag_bits, NUM_FLAG_BITS);

    /* set specified flag bit & return its previous value */
    int set_flag_bit(int bit_position)
    {
        return (int)atomic_set_bit(flag_bits, bit_position);
    }

内存序
==================

为了一致性和正确性，所有 Zephyr 原子 API 都应当
在硬件需要处以包含一个完整内存屏障（例如 x86 上"序列化"
指令、ARM 上的"DMB"，或 C++ 内存模型所定义的
"顺序一致"操作），以保证跨上下文获得可靠的视图。
任何特定架构的实现都负责确保
这一行为。

建议用法
**************

使用原子变量来实现仅需操作单个 32 位值的关键区处理。

使用多个原子变量来实现对超过 32 位的位数组中
一组标志位的关键区处理。

.. note::
    与其他实现关键区的技术（如使用互斥锁
    或锁定中断）相比，使用原子变量通常高效得多。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_BUILTIN`
* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_ARCH`
* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_C`

API 参考
*************

.. important::
    所有原子服务 API 均可被线程和 ISR 使用。

.. doxygengroup:: atomic_apis
