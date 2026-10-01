.. _condvar:

条件变量
###################

:dfn:`条件变量` 是一种同步原语，允许线程等待直到某个特定条件发生。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的条件变量（仅受可用 RAM 限制）。每个条件变量由其内存地址引用。

要等待某个条件变为真，线程可以使用条件变量。

条件变量本质上是一个线程队列：当某个执行状态（即某个条件）不符合预期时（通过等待该条件），线程可以将自己放入该队列。函数 :c:func:`k_condvar_wait` 原子地执行以下步骤：

#. 释放最后获取的互斥锁。
#. 将当前线程放入条件变量队列。

其他线程在改变该状态时，可以通过 :c:func:`k_condvar_signal` 或 :c:func:`k_condvar_broadcast` 对条件发出信号，从而唤醒其中一个（或多个）等待线程并允许它们继续；此时该线程：

#. 重新获取先前释放的互斥锁。
#. 从 :c:func:`k_condvar_wait` 返回。

无论等待因何完成——线程被发出信号、提供的超时时间已过、还是等待被请求为非阻塞——:c:func:`k_condvar_wait` 总是由调用线程重新锁定关联的互斥锁后返回。

条件变量在使用之前必须被初始化。


实现
**************

定义条件变量
=============================

条件变量使用 :c:struct:`k_condvar` 类型的变量来定义。然后必须通过调用 :c:func:`k_condvar_init` 进行初始化。

下面的代码定义一个条件变量：

.. code-block:: c

    struct k_condvar my_condvar;

    k_condvar_init(&my_condvar);

或者，可以通过调用 :c:macro:`K_CONDVAR_DEFINE` 在编译时定义并初始化条件变量。

下面的代码与上面代码段效果相同。

.. code-block:: c

    K_CONDVAR_DEFINE(my_condvar);

等待条件变量
===============================

线程可以通过调用 :c:func:`k_condvar_wait` 等待某个条件。

下面的代码等待条件变量。


.. code-block:: c

    K_MUTEX_DEFINE(mutex);
    K_CONDVAR_DEFINE(condvar)

    int main(void)
    {
        k_mutex_lock(&mutex, K_FOREVER);

        /* block this thread until another thread signals cond. While
         * blocked, the mutex is released, then re-acquired before this
         * thread is woken up and the call returns.
         */
        k_condvar_wait(&condvar, &mutex, K_FOREVER);
        ...
        k_mutex_unlock(&mutex);
    }

发出条件变量信号
===============================

通过调用 :c:func:`k_condvar_signal` 为单个线程发出信号，或调用 :c:func:`k_condvar_broadcast` 为多个线程发出信号，即可对条件变量发出信号。

下面的代码基于上面的示例。

.. code-block:: c

    void worker_thread(void)
    {
        k_mutex_lock(&mutex, K_FOREVER);

        /*
         * Do some work and fulfill the condition
         */
        ...
        ...
        k_condvar_signal(&condvar);
        k_mutex_unlock(&mutex);
    }

建议用法
**************

将条件变量与互斥锁配合使用，用于将一个线程中的状态（条件）变化信号给另一个线程。条件变量本身不是条件，也不是事件。条件包含在周围的编程逻辑中。

单独的互斥锁并非设计用作通知/同步机制。它们的用途仅为提供对共享资源的互斥访问。

配置选项
*********************

相关配置选项：

* 无。

API 参考
**************

.. doxygengroup:: condvar_apis
