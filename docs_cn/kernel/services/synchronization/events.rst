.. _events:

事件
######

:dfn:`事件对象` 是一种实现传统事件的内核对象。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的事件对象（仅受可用 RAM 限制）。每个事件对象由其内存地址引用。一个或多个线程可以等待某个事件对象，直到所需的事件集被投递到该事件对象。当新事件被投递到事件对象时，所有等待条件已满足的线程同时变为就绪。

事件对象具有以下关键属性：

* 一个 32 位值，跟踪哪些事件已被投递到它。

事件对象在使用之前必须被初始化。

事件可以由线程或 ISR **投递**。投递事件时，事件可以覆盖现有事件集，或以按位方式添加到现有事件集。覆盖现有事件集被称为设置（setting）；以按位方式添加到现有事件集被称为发布（posting）。发布和设置事件都有可能满足多个等待在该事件对象上的线程的匹配条件。所有匹配条件已满足的线程同时被激活。

线程可以等待一个或多个事件。它们可以等待所有请求的事件，或其中任意一个。此外，发出等待请求的线程可以选择在等待之前重置事件对象当前跟踪的事件集。当多个线程等待同一个事件对象时，必须谨慎使用此选项。

.. note::
    内核确实允许 ISR 查询事件对象，但 ISR 不得尝试等待事件。

实现
**************

定义事件对象
=========================

事件对象使用 :c:struct:`k_event` 类型的变量来定义。然后必须通过调用 :c:func:`k_event_init` 进行初始化。

下面的代码定义一个事件对象。

.. code-block:: c

    struct k_event my_event;

    k_event_init(&my_event);

或者，可以通过调用 :c:macro:`K_EVENT_DEFINE` 在编译时定义并初始化事件对象。

下面的代码与上面代码段效果相同。

.. code-block:: c

    K_EVENT_DEFINE(my_event);

设置事件
=============================

事件对象中的事件通过调用 :c:func:`k_event_set` 来设置。

下面的代码基于上面的示例，将事件对象跟踪的事件设置为 0x001。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        /* notify threads that data is available */

        k_event_set(&my_event, 0x001);

        ...
    }

发布事件
=============================

事件通过调用 :c:func:`k_event_post` 发布到事件对象。

下面的代码基于上面的示例，向事件对象发布一组事件。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        ...

        /* notify threads that more data is available */

        k_event_post(&my_event, 0x120);

        ...
    }

等待事件（不移除）
===================================

线程通过调用 :c:func:`k_event_wait` 等待事件。

下面的代码基于上面的示例，最多等待 50 毫秒，等待指定的任意事件被发布。如果没有任何事件按时被发布，则发出警告。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("No input devices are available!");
        } else {
            /* Access the desired input device(s) */
            ...
        }
        ...
    }

或者，消费者线程可能希望使用 :c:func:`k_event_wait_all` 等待所有事件后再继续。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("At least one input device is not available!");
        } else {
            /* Access the desired input devices */
            ...
        }
        ...
    }

等待事件（带移除）
===============================

线程通过调用 :c:func:`k_event_wait_safe` 等待事件（接收时原子移除）。

下面的代码基于上面的示例，最多等待 50 毫秒，等待指定的任意事件被发布。如果没有任何事件按时被发布，则发出警告。

如果事件按时收到，则在下一次事件被设置或发布之前，它们将不存在于事件对象中。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_safe(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("No input devices are available!");
        } else {
            /* Access the desired input device(s) */
            ...
        }
        ...
    }

或者，消费者线程可能希望使用 :c:func:`k_event_wait_all_safe` 等待所有事件（接收时原子移除）后再继续。

如果所有事件按时收到，则在下一次事件被设置或发布之前，它们将不存在于事件对象中。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all_safe(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("At least one input device is not available!");
        } else {
            /* Access the desired input devices */
            ...
        }
        ...
    }

建议用法
**************

使用事件指示一组条件已经发生。

使用事件同时向多个线程传递少量数据。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_EVENTS`

API 参考
**************

.. doxygengroup:: event_apis
