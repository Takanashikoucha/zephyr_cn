.. _timers_v2:

定时器
######

:dfn:`timer`（定时器）是一种内核对象，使用内核的系统时钟测量时间的流逝。
当定时器的指定时限到达时，它可以执行一个应用程序定义的操作，
也可以只是记录这次到期并等待应用程序读取其状态。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的定时器（仅受可用 RAM 限制）。每个定时器都通过其内存地址来引用。

定时器具有以下关键属性：

* 一个**持续时间**（duration），指定定时器首次到期前的时间间隔。
  这是一个 :c:type:`k_timeout_t` 值，可以用不同的单位初始化。

* 一个**周期**（period），指定首次到期之后所有到期之间的时间间隔，
  同样是一个 :c:type:`k_timeout_t`。它必须非负。周期为 ``K_NO_WAIT``（即零）
  或 ``K_FOREVER`` 表示该定时器是一次性（one-shot）定时器，在单次到期后停止。
  （例如，如果一个定时器以持续时间 200、周期 75 启动，
  它将在 200 ms 后首次到期，此后每隔 75 ms 到期一次。）

* 一个**到期函数**（expiry function），在定时器每次到期时执行。
  该函数由系统时钟中断处理程序执行。如果不需要到期函数，可以指定 ``NULL`` 函数。

* 一个**停止函数**（stop function），在定时器运行中被提前停止时执行。
  该函数由停止定时器的线程执行。如果不需要停止函数，可以指定 ``NULL`` 函数。

* 一个**状态**（status）值，指示自状态值上次被读取以来定时器已经到期了多少次。

定时器在使用前必须初始化。初始化指定其到期函数和停止函数的值，
将定时器状态置零，并把定时器置入**已停止**（stopped）状态。

通过指定持续时间和周期来**启动**（start）定时器。
定时器的状态被重置为零，然后定时器进入**运行中**（running）状态
并开始向到期时刻倒计时。

.. note::

    定时器的持续时间是相对于定时器启动时刻的**最小**延迟。
    定时器的周期是相对于定时器最后"应该"到期时刻的**最小**延迟。
    这意味着周期性定时器不会相对于系统定时器产生漂移，
    其周期性延迟可能短于或长于指定的周期。

    若要确保定时器到期前的最小延迟，应在**到期函数**内部
    或在定时器到期之后重启该定时器。

    延迟的变化性源于系统中断处理延迟
    和先前定时器处理程序的执行时间等系统变量。

运行中的定时器到期时，其状态递增，定时器执行其到期函数（如果存在）；
如果有线程在等待该定时器，该线程被解除阻塞。
如果定时器的周期为零，定时器进入已停止状态；
否则，定时器以一个新的持续时间重启，
该持续时间等于定时器"应该"到期的时刻与其周期之间的差值。

运行中的定时器可以在倒计时中途被停止（如果需要）。
定时器的状态保持不变，然后定时器进入已停止状态并执行其停止函数（如果存在）。
如果有线程在等待该定时器，该线程被解除阻塞。
尝试停止一个非运行中的定时器是允许的，
但由于定时器已经停止，这不会对其产生任何影响。

运行中的定时器可以在倒计时中途被重启（如果需要）。
定时器的状态被重置为零，然后定时器开始使用调用者指定的
新持续时间和周期值进行倒计时。如果有线程在等待该定时器，该线程继续等待。

可以随时直接读取定时器的状态，
以确定自其状态上次被读取以来定时器已经到期了多少次。
读取定时器的状态会将其值重置为零。
定时器到期前的剩余时间也可以读取；值为零表示定时器已停止。

线程可以通过与定时器**同步**（synchronizing）来间接读取定时器的状态。
这会阻塞线程，直到定时器状态非零（表示它至少已经到期一次）或定时器被停止；
如果定时器状态已经非零或定时器已经停止，线程则继续执行而不等待。
同步操作返回定时器的状态并将其重置为零。

.. note::
    任何给定定时器只应由单个使用者检查其状态，
    因为读取状态（直接或间接）会改变其值。
    类似地，一次只应有一个线程与给定定时器同步。
    中断服务程序（ISR）不允许与定时器同步，因为 ISR 不允许阻塞。

定时器观察者
***************

启用 :kconfig:option:`CONFIG_TIMER_OBSERVER` 后，代码可以注册
:dfn:`timer observers`（定时器观察者），
它们会收到系统中所有定时器生命周期事件的通告。
观察者是一组可选的回调，在定时器被初始化、启动、停止或到期时被调用。
这使得外部模块——例如跟踪（tracing）、性能分析（profiling）或电源管理代码——
能够在不修改内核内部或各个定时器的情况下对定时器活动做出反应。

观察者使用 :c:macro:`K_TIMER_OBSERVER_DEFINE` 静态定义，
它接受指向 ``on_init``、``on_start``、``on_stop`` 和 ``on_expiry`` 回调的指针；
任何不需要的回调都可以传 ``NULL``。
由于到期回调在中断上下文中运行，它必须保持简短且非阻塞。

实现
**************

定义定时器
================

定时器使用 :c:struct:`k_timer` 类型的变量来定义。
之后必须通过调用 :c:func:`k_timer_init` 进行初始化。

以下代码定义并初始化一个定时器。

.. code-block:: c

    struct k_timer my_timer;
    extern void my_expiry_function(struct k_timer *timer_id);

    k_timer_init(&my_timer, my_expiry_function, NULL);

或者，可以通过调用 :c:macro:`K_TIMER_DEFINE` 在编译时定义并初始化定时器。

以下代码与上面的代码段效果相同。

.. code-block:: c

    K_TIMER_DEFINE(my_timer, my_expiry_function, NULL);

使用定时器到期函数
=============================

以下代码使用定时器周期性地执行一个非平凡操作。
由于所需的工作无法在中断级别完成，
定时器的到期函数向 :ref:`系统工作队列 <workqueues_v2>` 提交一个工作项，
由工作队列的线程执行该工作。

.. code-block:: c

    void my_work_handler(struct k_work *work)
    {
        /* do the processing that needs to be done periodically */
        ...
    }

    K_WORK_DEFINE(my_work, my_work_handler);

    void my_timer_handler(struct k_timer *dummy)
    {
        k_work_submit(&my_work);
    }

    K_TIMER_DEFINE(my_timer, my_timer_handler, NULL);

    ...

    /* start a periodic timer that expires once every second */
    k_timer_start(&my_timer, K_SECONDS(1), K_SECONDS(1));

读取定时器状态
==================

以下代码直接读取定时器状态，以确定定时器是否已经到期。

.. code-block:: c

    K_TIMER_DEFINE(my_status_timer, NULL, NULL);

    ...

    /* start a one-shot timer that expires after 200 ms */
    k_timer_start(&my_status_timer, K_MSEC(200), K_NO_WAIT);

    /* do work */
    ...

    /* check timer status */
    if (k_timer_status_get(&my_status_timer) > 0) {
        /* timer has expired */
    } else if (k_timer_remaining_get(&my_status_timer) == 0) {
        /* timer was stopped (by someone else) before expiring */
    } else {
        /* timer is still running */
    }

使用定时器状态同步
=================================

以下代码执行定时器状态同步，使线程能够做有用的工作，
同时确保一对协议操作之间由指定的时间间隔隔开。

.. code-block:: c

    K_TIMER_DEFINE(my_sync_timer, NULL, NULL);

    ...

    /* do first protocol operation */
    ...

    /* start a one-shot timer that expires after 500 ms */
    k_timer_start(&my_sync_timer, K_MSEC(500), K_NO_WAIT);

    /* do other work */
    ...

    /* ensure timer has expired (waiting for expiry, if necessary) */
    k_timer_status_sync(&my_sync_timer);

    /* do second protocol operation */
    ...

.. note::
    如果线程没有其他工作可做，它可以简单地在两个协议操作之间睡眠，
    而无需使用定时器。

建议用法
**************

使用定时器在指定时间之后发起一个异步操作。

使用定时器判断指定时间是否已经过。特别是，
当需要比简单的 :c:func:`k_sleep` 和 :c:func:`k_usleep` 调用
所能提供的更高精度和/或更细的单位控制时，应使用定时器。

使用定时器，在执行涉及时限的操作的同时执行其他工作。

.. note::
    如果线程需要测量执行某操作所需的时间，
    可以直接读取 :ref:`系统时钟或硬件时钟 <kernel_timing>`，
    而无需使用定时器。

配置选项
*********************

相关配置选项：

* 无

API 参考
*************

.. doxygengroup:: timer_apis
