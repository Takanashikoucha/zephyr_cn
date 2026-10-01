.. _stacks_v2:

栈
######

:dfn:`栈`（stack）是一种内核对象，用于实现传统的后进先出（LIFO）队列，允许线程和 ISR 添加和移除有限数量的整数数据值。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的栈（仅受可用 RAM 限制）。每个栈都通过其内存地址来引用。

栈具有以下关键属性：

* 一个**队列**，包含已添加但尚未移除的整数数据值。该队列使用 ``stack_data_t`` 值的数组实现，且必须按原生字边界对齐。``stack_data_t`` 类型对应原生字大小，即根据 CPU 架构和编译模式为 32 位或 64 位。

* 数组中可以入队的**最大数量**数据值。

栈在使用前必须初始化，初始化会将其队列置为空。

线程或 ISR 可以将数据值**添加**到栈中：如果存在等待线程，该值会直接交给等待线程；否则该值被添加到 LIFO 的队列中。

.. note::
    如果启用了 :kconfig:option:`CONFIG_NO_RUNTIME_CHECKS`，内核将*不会*检测并阻止向已达到最大入队数量的栈添加数据值的尝试。向已满的栈添加数据值将导致数组溢出，并引发不可预测的行为。

线程可以将数据值从栈中**移除**。如果栈的队列为空，线程可以选择等待数据值被提供。任意数量的线程可以同时等待一个空栈。当数据值被添加时，它会交给等待时间最长的最高优先级线程。

.. note::
    内核允许 ISR 从栈中移除数据项，但如果栈为空，ISR 不得尝试等待。

实现
**************

定义栈
================

栈使用类型为 :c:struct:`k_stack` 的变量来定义，之后必须通过调用 :c:func:`k_stack_init` 或 :c:func:`k_stack_alloc_init` 进行初始化。在后一种情况下，不提供缓冲区，而是从调用线程的资源池中进行分配。

以下代码定义并初始化一个空栈，可容纳最多十个字大小的数据值。

.. code-block:: c

    #define MAX_ITEMS 10

    stack_data_t my_stack_array[MAX_ITEMS];
    struct k_stack my_stack;

    k_stack_init(&my_stack, my_stack_array, MAX_ITEMS);

或者，可以通过调用 :c:macro:`K_STACK_DEFINE` 在编译时定义并初始化一个栈。

以下代码与上面代码段的效果相同，注意该宏同时定义了栈及其数据值数组。

.. code-block:: c

    K_STACK_DEFINE(my_stack, MAX_ITEMS);

向栈中压入
==================

通过调用 :c:func:`k_stack_push` 将数据项添加到栈中。

以下代码基于上面的示例，展示线程如何通过将数据结构的内存地址保存到栈中，来创建一个数据结构池。

.. code-block:: c

    /* define array of data structures */
    struct my_buffer_type {
        int field1;
        ...
	};
    struct my_buffer_type my_buffers[MAX_ITEMS];

    /* save address of each data structure in a stack */
    for (int i = 0; i < MAX_ITEMS; i++) {
        k_stack_push(&my_stack, (stack_data_t)&my_buffers[i]);
    }

从栈中弹出
==================

通过调用 :c:func:`k_stack_pop` 从栈中取出数据项。

以下代码基于上面的示例，展示线程如何动态分配一个未使用的数据结构。当不再需要该数据结构时，线程必须将其地址重新压回栈中，以便该数据结构可以被复用。

.. code-block:: c

    struct my_buffer_type *new_buffer;

    k_stack_pop(&buffer_stack, (stack_data_t *)&new_buffer, K_FOREVER);
    new_buffer->field1 = ...

建议使用
**************

在已知最大存储项数的情况下，使用栈以"后进先出"方式存储和检索整数数据值。

配置选项
*********************

相关配置选项：

* 无。

API 参考
*************

.. doxygengroup:: stack_apis
