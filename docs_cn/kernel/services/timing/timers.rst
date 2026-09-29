.. _timers_v2:

定时器
######

:dfn:`定时器`是一种内核对象，使用内核的系统时钟
测量时间的流逝。当定时器的指定时间限制
到达时，它可以执行应用定义的动作，
或者它只是记录到期并等待应用
读取其状态。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的定时器（仅受可用 RAM 限制）。每个定时器
通过其内存地址引用。

定时器具有以下关键属性：

* 一个**持续时间**，指定定时器
  首次到期前的时间间隔。
  这是 :c:type:`k_timeout_t` 值，
  可以通过不同单位初始化。

* 一个**周期**，指定首次之后
  所有定时器
  到期之间的时间间隔，也是 :c:type:`k_timeout_t`。它必须
  非负。周期为 ``K_NO_WAIT``（即零）或
  ``K_FOREVER`` 意味着定时器是一次性定时器，
  在单次到期后停止。（例如，如果定时器
  以持续时间 200 和周期 75 启动，
  它将在 200 ms 后首次到期，
  然后在那之后每 75 ms 到期。）

* 一个**到期函数**，在定时器每次到期时
  执行。该函数由系统时钟中断处理程序
  执行。
  如果不需要到期函数，可以指定 ``NULL`` 函数。

* 一个**停止函数**，在定时器运行期间
  被提前停止时执行。该函数由停止定时器的
  线程执行。
  如果不需要停止函数，可以指定 ``NULL`` 函数。

* 一个**状态**值，指示定时器自状态值
  上次被读取以来已到期多少次。

定时器在使用前必须初始化。这指定其
  到期函数和停止函数值，将定时器状态设为零，
  并将定时器置于**停止**状态。

定时器通过指定持续时间和周期来**启动**。
  定时器状态重置为零，然后定时器进入
  **运行**状态并开始倒计时至到期。

.. note::

   定时器的持续时间是相对于定时器
   启动时间的**最小**延迟。定时器的周期是相对于
   定时器"应该"上次到期的
   **最小**延迟。这意味着周期性定时器
   不会相对于系统定时器漂移，且其周期性延迟
   可能短于或长于指定周期。

   为确保定时器到期前的最小延迟，
   在**到期函数**内部或定时器到期后
   重新启动定时器。

   延迟的变化性源于系统变量，如中断
   处理延迟和前面定时器处理程序的
   执行时间。

当运行中的定时器到期时，其状态递增
  且定时器执行其到期函数（如果存在）；
  如果线程正在等待定时器，它被解除阻塞。
  如果定时器周期为零，定时器进入停止状态；
  否则，定时器以新持续时间重新开始，
  等于定时器"应该"到期时间
  与其周期之间的差值。

如果需要，运行中的定时器可以在
  倒计时中途停止。
  定时器状态保持不变，然后定时器进入停止状态
  并执行其停止函数（如果存在）。
  如果线程正在等待定时器，它被解除阻塞。
  尝试停止非运行定时器是被允许的，
  但由于定时器已经停止，
  对定时器没有效果。

如果需要，运行中的定时器可以在
  倒计时中途重新启动。
  定时器状态重置为零，然后定时器
  使用调用者指定的新持续时间和周期值
  开始倒计时。
  如果线程正在等待定时器，它继续等待。

可以随时直接读取定时器状态
  以确定定时器自其状态
  上次被读取以来已到期多少次。
  读取定时器状态将其值重置为零。
  定时器到期前剩余的时间量也可以读取；
  值为零表示定时器已停止。

线程可以通过与定时器
  **同步**间接读取定时器状态。
  这阻塞线程直到定时器状态非零
  （指示其至少到期一次）或定时器停止；
  如果定时器状态已经非零或定时器已经停止，
  线程不等待继续。同步操作
  返回定时器状态并将其重置为零。

.. note::
    由于读取状态（直接或
    间接）会改变其值，
    因此任何给定定时器
    应只有一个用户检查其状态。
    类似地，每次
    应只有一个线程
    与给定定时器同步。ISR 不允许
    与定时器同步，
    因为 ISR 不允许阻塞。

定时器观察者
***************

当启用 :kconfig:option:`CONFIG_TIMER_OBSERVER` 时，代码可以注册
:dfn:`定时器观察者`，
被通知系统中所有定时器的生命周期事件。
观察者是
一组可选回调，
在定时器初始化、启动、停止或到期时
调用。
这允许外部模块
-- 例如跟踪、性能分析或电源管理代码 --
在不修改内核内部或各个定时器的情况下
对定时器活动做出反应。

观察者使用 :c:macro:`K_TIMER_OBSERVER_DEFINE` 静态定义，
接受指向 ``on_init``、``on_start``、``on_stop`` 和 ``on_expiry``
回调的指针；
任何不需要的回调
可以
作为 ``NULL``
传递。
由于
到期
回调
在
中断
上下文
中
运行，
它
必须
保持
简短
且
非
阻塞。

实现
**************

定义定时器
================

定时器使用 :c:struct:`k_timer` 类型的变量定义。
之后必须通过调用 :c:func:`k_timer_init` 初始化。

以下代码定义并初始化一个定时器。

.. code-block:: c

    struct k_timer my_timer;
    extern void my_expiry_function(struct k_timer *timer_id);

    k_timer_init(&my_timer, my_expiry_function, NULL);

或者，可以通过调用 :c:macro:`K_TIMER_DEFINE`
在编译时定义并初始化定时器。

以下代码与上面的代码段效果相同。

.. code-block:: c

    K_TIMER_DEFINE(my_timer, my_expiry_function, NULL);

使用定时器到期函数
=============================

以下代码使用定时器周期性执行非平凡动作。
由于所需的工作无法在中断级别完成，
定时器的到期函数将工作项提交到
:ref:`系统工作队列 <workqueues_v2>`，
其线程执行该工作。

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
====================

以下代码直接读取定时器状态
以确定定时器是否已到期。

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
==================================

以下代码执行定时器状态同步，
允许线程
做有用的工作，
同时确保
一对协议操作
之间
间隔
指定
的
时间
间隔。

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
    如果线程没有其他工作要做，
    它
    可以
    简单
    在
    两个
    协议
    操作
    之间
    睡眠，
    而
    不
    使用
    定时器。

建议用途
**************

使用定时器在指定
时间
后
发起
异步
操作。

使用定时器确定
指定
的
时间
量
是否
已经
经过。
特别是，
当
需要
比
更
简单
的
:c:func:`k_sleep`
和
:c:func:`k_usleep`
调用
提供
的
更高
精度
和/或
单位
控制
时，
应
使用
定时器。

使用定时器
在
执行
涉及
时间
限制
的
操作
时
执行
其他
工作。

.. note::
   如果
   线程
   需要
   测量
   执行
   操作
   所需
   的
   时间，
   它
   可以
   直接
   读取
   :ref:`系统时钟或硬件时钟 <kernel_timing>`
   ，
   而
   不
   使用
   定时器。

配置选项
*********************

相关配置选项：

* 无

API 参考
*************

.. doxygengroup:: timer_apis
