.. _threads_v2:

线程
#######

.. note::
   也支持有限度的 :ref:`nothread` 使用。

.. contents::
    :local:
    :depth: 2

本节描述用于创建、调度和删除独立可执行指令线程的内核服务。

:dfn:`线程`是一种内核对象，用于执行 ISR 无法完成的过长或过于复杂的应用处理。

应用程序可以定义任意数量的线程（仅受可用 RAM 限制）。每个线程通过在线程生成时分配的 :dfn:`线程 ID` 进行引用。

线程具有以下关键属性：

* 一个**栈区域**，即用于线程栈的内存区域。
  栈区域的**大小**可以调整以符合线程处理的实际需求。
  存在专门用于创建和操作栈内存区域的宏。

* 一个**线程控制块**，用于内核对线程元数据的私有簿记。
  这是 :c:struct:`k_thread` 类型的一个实例。

* 一个**入口点函数**，在线程启动时被调用。
  可以向该函数传递最多 3 个**参数值**。

* 一个**调度优先级**，指示内核调度器如何
  为线程分配 CPU 时间。（请参阅 :ref:`scheduling_v2`。）

* 一组**线程选项**，允许线程在特定情况下
  获得内核的特殊处理。
  （请参阅 :ref:`thread_options_v2`。）

* 一个**启动延迟**，指定内核在
  启动线程前应等待多长时间。

* 一个**执行模式**，可以是监督模式或用户模式。
  默认情况下，线程以监督模式运行，允许访问
  特权 CPU 指令、整个内存地址空间以及
  外设。用户模式线程具有缩减的特权集。
  这取决于 :kconfig:option:`CONFIG_USERSPACE` 选项。请参阅 :ref:`usermode_api`。

.. _lifecycle_v2:

生命周期
***********

.. _spawning_thread:

线程创建
==============

线程在使用前必须创建。内核初始化
线程控制块以及栈部分的一端。线程栈的其余
部分通常保持未初始化状态。

将启动延迟指定为 :c:macro:`K_NO_WAIT` 指示内核
立即启动线程执行。或者，可以通过指定超时
值指示内核延迟线程执行 -- 例如，允许线程使用的
设备硬件变得可用。

内核允许在线程开始
执行之前取消延迟启动。如果线程已经
启动，取消请求没有效果。成功取消延迟启动的线程
必须重新生成后才能使用。

启动线程
==================

以 :c:macro:`K_FOREVER` 作为启动延迟创建的线程
不会加入调度器的就绪队列，在显式启动之前
不会开始执行。:c:func:`k_thread_start` 函数启动这样的
非活动线程，使其有资格被调度。启动已经
启动的线程没有效果。

这在需要在一个时间点创建线程对象但
将其执行推迟到应用完成额外设置之后
时很有用。

线程终止
===================

线程启动后通常永远执行。然而，线程
可以通过从入口点函数返回来同步结束其执行。
这称为**终止**。

终止的线程负责在返回之前释放其
拥有的任何共享资源（如互斥锁和动态分配的内存），
因为内核*不会*自动回收它们。

在某些情况下，线程可能希望睡眠直到另一个线程终止。
这可以通过 :c:func:`k_thread_join` API 实现。
这将阻塞调用线程，直到超时到期、目标
线程自行退出，或目标线程中止（由于
:c:func:`k_thread_abort` 调用或触发致命错误）。

线程终止后，内核保证不会
使用该线程结构体。该结构体的内存
然后可以复用于任何目的，包括生成新线程。注意
线程必须完全终止，这存在竞态条件
线程自身逻辑发出的完成信号在
内核处理完成之前被另一个
线程看到。在正常
情况下，应用代码应使用 :c:func:`k_thread_join` 或
:c:func:`k_thread_abort` 来同步线程终止状态，
而不依赖应用逻辑内部的信号。

线程中止
==================

线程可以通过**中止**异步结束其执行。如果线程触发
致命错误条件（如解引用空指针），内核
会自动中止线程。

线程也可以通过另一个线程（或自身）
调用 :c:func:`k_thread_abort` 来中止。但通常
建议通知线程优雅地自行终止，而不是中止它。

与线程终止一样，内核不会回收
被中止线程拥有的共享资源。

.. note::
    内核目前不对应用程序
    重新生成被中止线程的能力做任何声明。

线程挂起
==================

线程可以因**挂起**而被阻止执行
无限长的时间。函数 :c:func:`k_thread_suspend`
可用于挂起任何线程，包括调用线程。
挂起已挂起的线程没有额外效果。

一旦挂起，线程在另一个线程调用
:c:func:`k_thread_resume` 移除挂起之前不能被调度。

.. note::
   线程可以使用 :c:func:`k_sleep` 阻止自身执行
   指定时间段。但这与挂起
   线程不同，因为睡眠线程在
   时间限制到达时会自动变为可执行。

.. _thread_states:

线程状态
*************

没有因素阻止其执行的线程被认为
处于**就绪**状态，有资格被选为当前线程。

有一个或多个因素阻止其执行的线程
被认为处于**未就绪**状态，不能被选为当前线程。

以下因素使线程未就绪：

* 线程尚未启动。
* 线程正在等待内核对象完成操作。
  （例如，线程正在获取不可用的信号量。）
* 线程正在等待超时发生。
* 线程已被挂起。
* 线程已终止或中止。

  .. image:: thread_states.svg
     :align: center

.. note::

   虽然上图可能暗示**就绪**和
   **运行**是不同的线程状态，但这不是正确
   的解释。**就绪**是线程状态，而**运行**是
   仅适用于**就绪**线程的
   调度状态。

线程栈对象
********************

每个线程都需要自己的栈缓冲区供 CPU 压入上下文。
根据配置，必须满足若干约束：

- 可能需要为内存管理
  结构额外保留内存
- 如果启用了基于保护页的栈溢出检测，一个小的写保护
  内存管理区域必须紧接在栈缓冲区之前
  以捕获溢出。
- 如果启用了用户空间，必须保留一个独立的固定大小提权栈
  作为处理系统调用的私有内核栈。
- 如果启用了用户空间，线程的栈缓冲区必须
  适当定尺寸和对齐，以便可以编程
  一个内存保护区域使其精确匹配。

对齐约束可能相当严格，例如某些 MPU
要求其区域大小为 2 的幂，且
按自身大小对齐。

因此，可移植代码不能简单地将任意字符缓冲区
传递给 :c:func:`k_thread_create`。存在专门用于静态实例化栈的宏，
前缀为 ``K_KERNEL_STACK`` 和 ``K_THREAD_STACK``。

此外，可以使用
:c:func:`k_thread_stack_alloc` 动态实例化栈，
随后使用
:c:func:`k_thread_stack_free` 释放。

仅内核栈
==================

如果已知线程永远不会以用户模式运行，或者
栈用于处理中断等特殊上下文，
最好使用 ``K_KERNEL_STACK`` 宏定义栈。

这些栈节省内存，因为永远不需要
编程 MPU 区域来覆盖栈缓冲区本身，内核也不需要
为提权栈或仅与用户模式线程相关的
内存管理数据结构额外保留空间。

从用户模式尝试使用以此方式声明的栈将导致
调用者致命错误。

如果未启用 ``CONFIG_USERSPACE``，``K_THREAD_STACK`` 宏
集与 ``K_KERNEL_STACK`` 宏的效果完全相同。

线程栈
=============

如果已知栈需要承载用户线程，或者
无法确定这一点，使用 ``K_THREAD_STACK`` 宏定义栈。
这可能使用更多内存，但栈对象适合承载
用户线程。

如果未启用 ``CONFIG_USERSPACE``，``K_THREAD_STACK`` 宏
集与 ``K_KERNEL_STACK`` 宏的效果完全相同。

.. _thread_priorities:

线程优先级
*****************

线程优先级是一个整数值，可以是负数或
非负数。
数值较低的优先级优先于数值较高的值。
例如，调度器赋予优先级 4 的线程 A 比
优先级 7 的线程 B *更高* 的优先级；同样，优先级 -2 的线程 C
的优先级高于线程 A 和线程 B。

调度器根据每个线程的优先级
区分两类线程。

* :dfn:`协同线程`具有负优先级值。
  一旦成为当前线程，协同线程保持
  当前线程状态，直到其执行使其未就绪的操作。

* :dfn:`可抢占线程`具有非负优先级值。
  一旦成为当前线程，可抢占线程可以在任何时候被替换，
  如果协同线程或优先级更高
  或相等的可抢占线程变为就绪。


线程的初始优先级值在线程
启动后可以向上或向下更改。因此，可抢占线程
可以通过更改优先级变为协同线程，反之亦然。

.. note::
    调度器不会做出启发式决策来重新调整线程优先级。
    线程优先级仅在应用请求时设置和更改。

内核支持几乎无限数量的线程优先级级别。
配置选项 :kconfig:option:`CONFIG_NUM_COOP_PRIORITIES` 和
:kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES` 指定每类线程的优先级
数量，产生以下可用优先级
范围：

* 协同线程：(-:kconfig:option:`CONFIG_NUM_COOP_PRIORITIES`) 到 -1
* 抢占式线程：0 到 (:kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES` - 1)

.. image:: priorities.svg
   :align: center

例如，配置 5 个协同优先级和 10 个抢占优先级
分别产生 -5 到 -1 和 0 到 9 的范围。

.. _metairq_priorities:

元中断（Meta-IRQ）优先级
==================

当启用时（请参阅 :kconfig:option:`CONFIG_NUM_METAIRQ_PRIORITIES`），在优先级空间的最高端（数值最低端）有一个特殊的协同优先级子类：元中断（meta-IRQ）线程。这些线程按正常优先级调度，但还具有特殊能力抢占所有优先级较低的其他线程（和其他元中断线程），即使那些线程是协同线程和/或已获取调度器锁。元中断线程仍然是线程，但仍可被任何硬件中断打断。

.. note::
   当被元中断线程抢占的协同（或调度锁定）线程在元中断线程完成后恢复执行时，它将在同一 CPU 上——假设其未被挂起或中止。这有助于确保这些线程在查询与自身 CPU 相关的属性期间不会被意外转移到另一个 CPU。

此行为使解除元中断线程阻塞的操作（通过任何手段，例如创建它、调用 k_sem_give() 等）由较低优先级线程执行时等同于同步系统调用，或由真正中断上下文执行时等同于 ARM 风格的"挂起 IRQ"。此功能的意图是用于在驱动程序子系统中实现中断"下半部"处理和/或"tasklet"特性。线程一旦被唤醒，将保证在当前 CPU 返回应用代码之前运行。

与其他操作系统中的类似特性不同，元中断线程是真正的线程，运行在自己的栈上（必须正常分配），而不是每 CPU 中断栈。启用在受支持架构上使用 IRQ 栈的设计工作正在进行中。

注意，由于这打破了 Zephyr API 对协同
线程做出的承诺（即操作系统不会在
当前线程主动阻塞之前调度其他
线程），因此应用代码应极其谨慎地使用。这些
不仅仅是非常高的优先级线程，不应如此使用。

.. _thread_options_v2:

线程选项
***************

内核支持一组 :dfn:`线程选项`，允许线程
在特定情况下获得特殊处理。与线程
关联的选项集在线程生成时指定。

不需要任何线程选项的线程选项值为零。
需要线程选项的线程通过名称指定，
需要多个选项时使用 :literal:`|` 字符作为分隔符
（即使用按位或运算符组合选项）。

支持以下线程选项。

:c:macro:`K_ESSENTIAL`
    此选项将线程标记为 :dfn:`基本线程`。这指示
    内核将线程的终止或中止视为致命
    系统错误。

    默认情况下，线程不被视为基本线程。

:c:macro:`K_SSE_REGS`
    此 x86 特定选项表示线程使用 CPU 的
    SSE 寄存器。另请参阅 :c:macro:`K_FP_REGS`。

    默认情况下，内核在调度线程时不尝试
    保存和恢复这些寄存器的内容。

:c:macro:`K_FP_REGS`
    此选项表示线程使用 CPU 的浮点
    寄存器。这指示内核采取额外步骤
    在调度线程时保存和恢复这些寄存器的内容。
    （更多信息请参阅 :ref:`float_v2`。）

    默认情况下，内核在调度线程时不尝试
    保存和恢复此寄存器的内容。

:c:macro:`K_USER`
    如果启用了 :kconfig:option:`CONFIG_USERSPACE`，此线程将以
    用户模式创建并具有缩减的特权。请参阅 :ref:`usermode_api`。否则
    此标志不起作用。

:c:macro:`K_INHERIT_PERMS`
    如果启用了 :kconfig:option:`CONFIG_USERSPACE`，此线程将继承父线程
    拥有的所有内核对象权限，但父线程
    对象除外。请参阅 :ref:`usermode_api`。


.. _custom_data_v2:

线程自定义数据
******************

每个线程都有一个 32 位 :dfn:`自定义数据` 区域，仅
线程自身可访问，应用可用于
其选择的任何目的。线程的默认自定义数据值为零。

.. note::
   ISR 无法使用自定义数据支持，因为它们在
   单个共享内核中断处理上下文中运行。

默认情况下，线程自定义数据支持被禁用。配置选项
:kconfig:option:`CONFIG_THREAD_CUSTOM_DATA` 可用于启用支持。

:c:func:`k_thread_custom_data_set` 和
:c:func:`k_thread_custom_data_get` 函数分别用于写入和读取
线程的自定义数据。线程只能访问自己的
自定义数据，不能访问其他线程的。

以下代码使用自定义数据功能记录每个线程
调用特定例程的次数。

.. note::
    显然，只有一个例程可以使用此技术，
    因为它独占使用自定义数据功能。

.. code-block:: c

    int call_tracking_routine(void)
    {
        uint32_t call_count;

        if (k_is_in_isr()) {
	    /* ignore any call made by an ISR */
        } else {
            call_count = (uint32_t)k_thread_custom_data_get();
            call_count++;
            k_thread_custom_data_set((void *)call_count);
	}

        /* do rest of routine's processing */
        ...
    }

使用线程自定义数据允许例程访问线程特定信息，
方法是将自定义数据用作指向线程拥有的
数据结构的指针。

.. _thread_name_v2:

线程名称
***********

当启用 :kconfig:option:`CONFIG_THREAD_NAME` 时，可以为每个
线程关联一个人类可读的名称。名称主要用于调试、
日志和 shell 内省辅助；内核不用于调度。

线程名称可以以两种方式分配：

* 静态方式，通过向 :c:macro:`K_THREAD_DEFINE` 传递名称。
* 运行时方式，使用 :c:func:`k_thread_name_set`。提供的字符串
  必须在线程生命周期内保持有效，因为只保留
  指向它的指针。

线程的名称可以通过 :c:func:`k_thread_name_get` 获取，返回
指向名称字符串的指针，或通过 :c:func:`k_thread_name_copy` 获取，
将名称复制到调用者提供的缓冲区中。复制变体是
用户模式下的安全选择，因为调用线程可能无法访问
另一个线程名称背后的内存。

如果未启用 :kconfig:option:`CONFIG_THREAD_NAME`，
:c:func:`k_thread_name_set` 返回错误，:c:func:`k_thread_name_get`
返回 ``NULL``。

线程内省
********************

内核提供多个接口用于在运行时检查线程。

**识别当前线程**
    :c:func:`k_current_get` 返回当前
    执行线程的线程 ID（:c:type:`k_tid_t`）。此 ID
    可以传递给其他线程 API 以
    操作调用线程。

**读取线程优先级**
    :c:func:`k_thread_priority_get` 返回线程的
    当前调度优先级。这反映了自线程创建以来
    的任何更改，例如由 :c:func:`k_thread_priority_set` 做出的更改。

**获取线程状态**
    :c:func:`k_thread_state_str` 将线程当前状态的
    人类可读表示（例如 ``pending``、``suspended`` 或
    ``ready``）写入调用者提供的缓冲区。这用于
    诊断输出，不应被程序解析。

**遍历所有线程**
    当启用 :kconfig:option:`CONFIG_THREAD_MONITOR` 时，
    :c:func:`k_thread_foreach` 为系统中的每个
    线程调用一次调用者提供的回调。它持有内部锁，
    在遍历期间阻止线程创建
    和终止，这保证了一致的线程列表快照，
    但可能引入与线程数量成比例的延迟。
    :c:func:`k_thread_foreach_unlocked`
    是较低延迟的变体，在每次回调周围释放锁，
    代价是较不严格一致的视图。

**查询栈使用情况**
    当启用 :kconfig:option:`CONFIG_INIT_STACKS` 和
    :kconfig:option:`CONFIG_THREAD_STACK_INFO` 时，
    :c:func:`k_thread_stack_space_get` 报告线程栈中
    剩余未使用的字节数，通过扫描栈的未使用
    （仍初始化的）区域计算得出。这补充了
    构建时栈分析工具和下面描述的
    运行时栈安全特性。

**查询挂起的超时**
    阻塞在带超时操作（如 :c:func:`k_sleep` 或
    带超时的内核对象操作）上的线程有一个挂起的超时。
    其剩余持续时间可以用
    :c:func:`k_thread_timeout_remaining_ticks` 以 tick 为单位查询，
    其到期的绝对系统 tick 可以用 :c:func:`k_thread_timeout_expires_ticks` 查询。
    如果线程没有挂起的超时，两者
    都返回零。

实现
**************

生成线程
==================

线程通过定义其栈区域和线程控制块
生成，然后调用 :c:func:`k_thread_create`。

栈区域可以使用
:c:macro:`K_THREAD_STACK_DEFINE` 或 :c:macro:`K_KERNEL_STACK_DEFINE` 静态分配
以确保其在内存中正确设置。

栈的大小参数必须是三个值之一：

- 最初传递给
  ``K_THREAD_STACK`` 或 ``K_KERNEL_STACK`` 系列栈实例化
  宏的请求栈大小。
- 对于使用 ``K_THREAD_STACK`` 系列
  宏定义的栈对象，该对象的
  :c:macro:`K_THREAD_STACK_SIZEOF()` 返回值。
- 对于使用 ``K_KERNEL_STACK`` 系列
  宏定义的栈对象，该对象的
  :c:macro:`K_KERNEL_STACK_SIZEOF()` 返回值。

或者，栈区域可以使用
:c:func:`k_thread_stack_alloc` 动态分配，
使用 :c:func:`k_thread_stack_free` 释放。

线程生成函数返回其线程 ID，可用于
引用线程。

以下代码生成一个立即启动的线程。

.. code-block:: c

    #define MY_STACK_SIZE 500
    #define MY_PRIORITY 5

    extern void my_entry_point(void *, void *, void *);

    K_THREAD_STACK_DEFINE(my_stack_area, MY_STACK_SIZE);
    struct k_thread my_thread_data;

    k_tid_t my_tid = k_thread_create(&my_thread_data, my_stack_area,
                                     K_THREAD_STACK_SIZEOF(my_stack_area),
                                     my_entry_point,
                                     NULL, NULL, NULL,
                                     MY_PRIORITY, 0, K_NO_WAIT);

或者，可以通过调用
:c:macro:`K_THREAD_DEFINE` 在编译时声明线程。注意
该宏自动定义
栈区域、控制块和线程 ID 变量。

以下代码与上面的代码段效果相同。

.. code-block:: c

    #define MY_STACK_SIZE 500
    #define MY_PRIORITY 5

    extern void my_entry_point(void *, void *, void *);

    K_THREAD_DEFINE(my_tid, MY_STACK_SIZE,
                    my_entry_point, NULL, NULL, NULL,
                    MY_PRIORITY, 0, 0);

.. note::
   :c:func:`k_thread_create` 的延迟参数是
   :c:type:`k_timeout_t` 值，因此 :c:macro:`K_NO_WAIT` 表示
   立即启动线程。:c:macro:`K_THREAD_DEFINE` 的
   对应参数是以整毫秒为单位的持续时间，因此
   等效参数为 0。

以下代码动态分配线程栈，等待线程
加入，然后释放动态分配的线程栈。

.. code-block:: c

    extern void my_entry_point(void *, void *, void *);

    k_tid_t my_tid;
    void *my_stack_area;

    my_stack_area = k_thread_stack_alloc(CONFIG_DYNAMIC_THREAD_STACK_SIZE);
    my_tid = k_thread_create(&my_thread_data, my_stack_area,
                              CONFIG_DYNAMIC_THREAD_STACK_SIZE,
                              my_entry_point,
                              NULL, NULL, NULL,
                              MY_PRIORITY, 0, K_NO_WAIT);
    k_thread_join(my_tid, K_FOREVER);
    k_thread_stack_free(my_stack_area);

用户模式约束
---------------------

本节仅在启用 :kconfig:option:`CONFIG_USERSPACE` 且用户
线程尝试创建新线程时适用。:c:func:`k_thread_create` API
仍在使用，但必须满足额外约束，否则
调用线程将被终止：

* 调用线程必须对子线程
  和栈参数都有权限；两者都由内核
  作为内核对象跟踪。

* 子线程和栈对象必须处于未初始化状态，
  即当前未运行且栈内存未使用。

* 传入的栈大小参数必须等于或小于
  栈对象声明时的边界。

* 必须使用 :c:macro:`K_USER` 选项，因为用户线程只能创建
  其他用户线程。

* 不得使用 :c:macro:`K_ESSENTIAL` 选项，用户线程不能
  被视为基本线程。

* 子线程的优先级必须是有效优先级值，且等于
  或低于父线程。

放弃权限
===================

如果启用 :kconfig:option:`CONFIG_USERSPACE`，以监督模式运行的线程
可以使用
:c:func:`k_thread_user_mode_enter` API 执行单向转换到用户模式。
这是一个单向操作，
将重置并清零线程的栈内存。线程将被标记
为非基本线程。

终止线程
===================

线程通过从入口点函数返回来终止自身。

以下代码说明线程终止的方式。

.. code-block:: c

    void my_entry_point(int unused1, int unused2, int unused3)
    {
        while (1) {
            ...
	    if (<some condition>) {
	        return; /* thread terminates from mid-entry point function */
	    }
	    ...
        }

        /* thread terminates at end of entry point function */
    }

如果启用 :kconfig:option:`CONFIG_USERSPACE`，中止线程还将
标记线程和栈对象为未初始化状态，以便它们可以被复用。

运行时统计
******************

如果启用 :kconfig:option:`CONFIG_THREAD_RUNTIME_STATS`，可以收集和获取
线程运行时统计信息，例如线程的
总执行周期数。

默认情况下，运行时统计使用默认内核
定时器收集。对于某些架构、SoC 或板，
有通过 timing 函数可用更高分辨率的定时器。
可以使用 :kconfig:option:`CONFIG_THREAD_RUNTIME_STATS_USE_TIMING_FUNCTIONS`
启用这些定时器的使用。

以下是一个示例：

.. code-block:: c

   k_thread_runtime_stats_t rt_stats_thread;

   k_thread_runtime_stats_get(k_current_get(), &rt_stats_thread);

   printk("Cycles: %llu\n", rt_stats_thread.execution_cycles);

系统中每个线程的组合统计信息可以通过
:c:func:`k_thread_runtime_stats_all_get` 获取，报告所有线程
（包括空闲线程）的总运行时
使用量。这对于
计算总体 CPU 利用率很有用。

当启用 :kconfig:option:`CONFIG_SCHED_THREAD_USAGE` 时，统计
收集可以在运行时按线程
使用
:c:func:`k_thread_runtime_stats_enable` 和
:c:func:`k_thread_runtime_stats_disable` 切换。线程当前
是否正在收集
可以通过 :c:func:`k_thread_runtime_stats_is_enabled` 检查。
对不需要测量的线程禁用收集减少了
每次上下文切换时产生的
簿记开销。

运行时栈安全
********************

当启用 :kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY` 时，内核
提供在运行时扫描线程栈以确定
多少栈空间仍未被使用的例程。如果未使用
栈空间量被发现
低于可配置的每线程阈值，将调用用户定义的
处理程序。

此特性旨在供监控软件使用。处理程序
例如可以记录警告、挂起或中止违规线程，
甚至重启
系统。它补充了构建时栈分析工具和
基于硬件的栈溢出检测，允许系统在
栈耗尽*之前*做出反应。

每个线程都有一个*未使用栈阈值*，以字节表示。当
栈安全检查发现线程的未使用栈空间
低于此阈值时，
调用提供的处理程序。阈值为 0 字节（默认值）
禁用该线程的检查。应用于
新创建线程的默认阈值派生自
:kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY_DEFAULT_UNUSED_THRESHOLD_PCT`，
将其表示为每个线程总栈大小的百分比。

单个线程的阈值可以在运行时设置或查询：

* :c:func:`k_thread_runtime_stack_unused_threshold_pct_set` 将阈值
  设置为线程总栈大小的百分比（0 到 99）。
* :c:func:`k_thread_runtime_stack_unused_threshold_set` 将阈值设置为
  绝对字节数。
* :c:func:`k_thread_runtime_stack_unused_threshold_get` 获取当前
  阈值（以字节为单位）。

两个例程执行实际检查。两者都接受一个指针，
返回时接收未使用栈空间量，以及
:c:type:`k_thread_stack_safety_handler_t` 处理程序（加用户参数），
在超过阈值时调用：

* :c:func:`k_thread_runtime_stack_safety_full_check` 扫描整个栈
  计算精确的未使用空间量。
* :c:func:`k_thread_runtime_stack_safety_threshold_check` 执行
  简化扫描，仅查找线程
  已越过其配置阈值的证据。这比
  完整检查更廉价，但不产生
  未使用空间的精确测量。

以下是一个示例，配置线程在其未使用
栈空间降至总栈大小的 10% 以下时调用
处理程序：

.. code-block:: c

   void stack_safety_handler(const struct k_thread *thread,
                             size_t unused_space, void *arg)
   {
           printk("Thread %p low on stack: %zu bytes unused\n",
                  thread, unused_space);
   }

   /* Trigger the handler once less than 10% of the stack remains unused */
   k_thread_runtime_stack_unused_threshold_pct_set(my_tid, 10);

   /* Periodically check the thread from a monitoring context */
   k_thread_runtime_stack_safety_full_check(my_tid, NULL,
                                            stack_safety_handler, NULL);

建议用途
**************

使用线程处理无法在 ISR 中处理的
处理。

使用独立的线程处理可以并行执行的
逻辑上不同的处理操作。


配置选项
**********************

相关配置选项：

* :kconfig:option:`CONFIG_MAIN_THREAD_PRIORITY`
* :kconfig:option:`CONFIG_MAIN_STACK_SIZE`
* :kconfig:option:`CONFIG_IDLE_STACK_SIZE`
* :kconfig:option:`CONFIG_THREAD_CUSTOM_DATA`
* :kconfig:option:`CONFIG_NUM_COOP_PRIORITIES`
* :kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES`
* :kconfig:option:`CONFIG_TIMESLICING`
* :kconfig:option:`CONFIG_TIMESLICE_SIZE`
* :kconfig:option:`CONFIG_TIMESLICE_PRIORITY`
* :kconfig:option:`CONFIG_USERSPACE`
* :kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY`
* :kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY_DEFAULT_UNUSED_THRESHOLD_PCT`



API 参考
**************

.. doxygengroup:: thread_apis

.. doxygengroup:: thread_stack_api
