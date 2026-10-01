.. _polling_v2:

轮询 API
###########

轮询 API 用于并发地等待多个条件中的任意一个得到满足。

.. contents::
    :local:
    :depth: 2

概念
********

轮询 API 的主要函数是 :c:func:`k_poll`，其概念与 POSIX 的 :c:func:`poll` 函数非常相似，区别在于它操作的是内核对象而非文件描述符。

轮询 API 允许单个线程并发地等待一个或多个条件得到满足，
而无需逐一主动查看每个条件。

这类条件有一个有限的集合：

- 信号量变为可用
- 内核 FIFO 中有可取出的数据
- 内核 LIFO 中有可取出的数据
- 内核消息队列中有可取出的数据
- 内核管道中有可取出的数据
- 轮询信号被触发

想要等待多个条件的线程必须定义一个
**轮询事件**数组，每个条件对应一个。

数组中的所有事件在数组被轮询之前
都必须完成初始化。

每个事件必须指定必须满足哪种**类型**的条件，
才能将其状态改变，以指示所请求的条件已满足。

每个事件必须指定它希望条件在哪个**内核对象**上
得到满足。

每个事件必须指定条件满足时使用哪种**模式**运行。

每个事件可以可选地指定一个**标签**（tag），
由用户自行决定将多个事件分组在一起。

除内核对象外，还有一种**轮询信号**伪对象
类型，可以直接被触发。

:c:func:`k_poll` 函数在它等待的任一条件得到满足时
立即返回。:c:func:`k_poll` 返回时，可能有不止一个
条件已满足——如果它们在调用 :c:func:`k_poll` 之前
就已满足，或者由于内核抢占式多线程特性所致。
调用者必须查看数组中所有轮询事件的状态，
才能弄清楚哪些条件已满足以及应采取什么操作。

目前只有一种可用的运行模式：对象不被获取（acquire）。
举例来说，这意味着当 :c:func:`k_poll` 返回且
轮询事件状态表明信号量可用时，
:c:func:`k_poll()` 的调用者必须接着调用
:c:func:`k_sem_take` 来获取
该信号量的所有权。如果该信号量存在竞争，
调用 :c:func:`k_sem_take` 时它是否仍可用
并不保证。

实现
**************

使用 k_poll()
=============

主要 API 是 :c:func:`k_poll`，它操作一个
:c:struct:`k_poll_event` 类型的轮询事件数组。
数组中的每个条目代表一个带条件的
事件，调用 :c:func:`k_poll` 时将等待其
得到满足。

轮询事件可以使用运行时初始化器
:c:macro:`K_POLL_EVENT_INITIALIZER()` 或 :c:func:`k_poll_event_init`，
或静态初始化器 :c:macro:`K_POLL_EVENT_STATIC_INITIALIZER()` 进行初始化。
必须向初始化器传递一个与所指定**类型**匹配的对象。
**模式** *必须* 设置为 :c:enumerator:`K_POLL_MODE_NOTIFY_ONLY`。
状态 *必须* 设置为 :c:macro:`K_POLL_STATE_NOT_READY`（初始化器
会负责这一点）。用户**标签**是可选的，对 API 完全
不透明：它的作用
是帮助用户将相似的事件分组在一起。由于是可选的，
出于性能考虑，它被传递给静态初始化器，
但不传递给运行时初始化器。如果使用运行时初始化器，
用户必须在 :c:struct:`k_poll_event` 数据结构中
单独设置它。如果要忽略数组中的某个事件
（很可能只是暂时忽略），
可将其类型设置为 :c:macro:`K_POLL_TYPE_IGNORE`。

.. code-block:: c

    struct k_poll_event events[4] = {
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_SEM_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_sem, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_fifo, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_MSGQ_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_msgq, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_PIPE_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_pipe, 0),
    };

或在运行时：

.. code-block:: c

    struct k_poll_event events[4];
    void some_init(void)
    {
        k_poll_event_init(&events[0],
                          K_POLL_TYPE_SEM_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_sem);

        k_poll_event_init(&events[1],
                          K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_fifo);

        k_poll_event_init(&events[2],
                          K_POLL_TYPE_MSGQ_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_msgq);

        k_poll_event_init(&events[3],
                          K_POLL_TYPE_PIPE_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_pipe);

        // tags are left uninitialized if unused
    }


事件初始化完成后，数组即可传递给
:c:func:`k_poll`。可以指定一个超时时间
只等待指定时长，或使用特殊值 :c:macro:`K_NO_WAIT` 和
:c:macro:`K_FOREVER`，分别表示不等待，或一直等到
事件条件满足为止（不会更早返回）。

每个信号量或 FIFO 上都会提供一个轮询者（poller）列表，
应用希望多少事件在其中等待都可以。
注意，等待者按先到先得（first-come-first-serve）的顺序
获得服务，而不是按优先级顺序。

成功时，:c:func:`k_poll` 返回 0。超时则返回
-:c:macro:`EAGAIN`。

.. code-block:: c

    // assume there is no contention on this semaphore and FIFO
    // -EADDRINUSE will not occur; the semaphore and/or data will be available

    void do_stuff(void)
    {
        rc = k_poll(events, ARRAY_SIZE(events), K_MSEC(1000));
        if (rc == 0) {
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, 0);
            } else if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, 0);
                // handle data
            } else if (events[2].state == K_POLL_STATE_MSGQ_DATA_AVAILABLE) {
                ret = k_msgq_get(events[2].msgq, buf, K_NO_WAIT);
                // handle data
            } else if (events[3].state == K_POLL_STATE_PIPE_DATA_AVAILABLE) {
                bytes_read = k_pipe_read(events[3].pipe, buf, bytes_to_read, K_NO_WAIT);
                // handle data
            }
        } else {
            // handle timeout
        }
    }

在循环中调用 :c:func:`k_poll` 时，
用户必须将事件状态重置为
:c:macro:`K_POLL_STATE_NOT_READY`。

.. code-block:: c

    void do_stuff(void)
    {
        for(;;) {
            rc = k_poll(events, ARRAY_SIZE(events), K_FOREVER);
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, 0);
            }
            if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, 0);
                // handle data
            }
            if (events[2].state == K_POLL_STATE_MSGQ_DATA_AVAILABLE) {
                ret = k_msgq_get(events[2].msgq, buf, K_NO_WAIT);
                // handle data
            }
            if (events[3].state == K_POLL_STATE_PIPE_DATA_AVAILABLE) {
                bytes_read = k_pipe_read(events[3].pipe, buf, bytes_to_read, K_NO_WAIT);
                // handle data
            }
            events[0].state = K_POLL_STATE_NOT_READY;
            events[1].state = K_POLL_STATE_NOT_READY;
            events[2].state = K_POLL_STATE_NOT_READY;
            events[3].state = K_POLL_STATE_NOT_READY;
        }
    }

使用 k_poll_signal_raise()
===========================

事件类型之一是 :c:macro:`K_POLL_TYPE_SIGNAL`：
这是对轮询事件的"直接"触发。
可以将其视为一个轻量级的二进制信号量，
只有一个线程能等待它。

轮询信号是一个独立的 :c:struct:`k_poll_signal` 类型对象，
必须附加到一个 k_poll_event 上，类似于信号量或 FIFO。
它必须先用 :c:macro:`K_POLL_SIGNAL_INITIALIZER()` 或
:c:func:`k_poll_signal_init` 进行初始化。

.. code-block:: c

    struct k_poll_signal signal;
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);
    }

通过 :c:func:`k_poll_signal_raise` 函数触发该信号。
该函数接收一个用户**结果**（result）参数，
对 API 不透明，可用于
向等待该事件的线程传递额外信息。

.. code-block:: c

    struct k_poll_signal signal;

    // thread A
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);

        struct k_poll_event events[1] = {
            K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
                                     K_POLL_MODE_NOTIFY_ONLY,
                                     &signal),
        };

        k_poll(events, 1, K_FOREVER);

        int signaled, result;

        k_poll_signal_check(&signal, &signaled, &result);

        if (signaled && (result == 0x1337)) {
            // A-OK!
        } else {
            // weird error
        }
    }

    // thread B
    void signal_do_stuff(void)
    {
        k_poll_signal_raise(&signal, 0x1337);
    }

如果信号要在循环中被轮询，*每次*迭代中
都必须将其事件状态重置为
:c:macro:`K_POLL_STATE_NOT_READY`，*并且*
如果它已被触发，还必须使用 :c:func:`k_poll_signal_reset()`
将其 ``result`` 重置。

.. code-block:: c

    struct k_poll_signal signal;
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);

        struct k_poll_event events[1] = {
            K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
                                     K_POLL_MODE_NOTIFY_ONLY,
                                     &signal),
        };

        for (;;) {
            k_poll(events, 1, K_FOREVER);

            int signaled, result;

            k_poll_signal_check(&signal, &signaled, &result);

            if (signaled && (result == 0x1337)) {
                // A-OK!
            } else {
                // weird error
            }

            k_poll_signal_reset(&signal);
            events[0].state = K_POLL_STATE_NOT_READY;
        }
    }

注意，轮询信号在内部没有同步。接收
信号后，传入该信号的 :c:func:`k_poll` 调用
会在系统任何代码调用 :c:func:`k_poll_signal_raise()`
之后返回。但如果信号由外部
管理并通过 :c:func:`k_poll_signal_init()` 重置，
那么等到应用检查时，事件状态
可能已不再等于 :c:macro:`K_POLL_STATE_SIGNALED`，
（简单的）应用就会错过事件。
最佳实践是始终只从调用 :c:func:`k_poll`
循环的线程内部重置信号，
或者改用某种跟踪事件计数的其他事件类型：
从这个意义上说，信号量和 FIFO 更不容易出错，
因为它们在架构上不会"错过"
事件。

建议用法
**************

使用 :c:func:`k_poll` 将多个原本会各自
挂起在单个对象上的线程合并为一个，
从而可能节省大量栈空间。

如果只有一个线程挂起在轮询信号上，
可将其作为轻量级二进制信号量使用。

.. note::
    只有当没有其他线程在等待对象变为可用时，
    对象才会被触发，且只有一个线程
    能轮询某个特定对象，因此轮询
    最适合用于对象不受多个线程竞争的场景，
    基本上是一个单一线程作为多个对象的
    主"服务器"或"分发器"，
    并且是唯一尝试获取这些对象的线程。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_POLL`

API 参考
*************

.. doxygengroup:: poll_apis
