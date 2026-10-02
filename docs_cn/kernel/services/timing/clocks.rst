.. _kernel_timing:

内核计时
#############

Zephyr 提供一个健壮且可扩展的计时框架，以启用从任意精度的硬件计时源报告和跟踪定时事件。

时间单位
==========

内核时间以用于不同目的的若干单位跟踪。

实时值（通常以毫秒或微秒指定）是向应用代码呈现时间的默认方式。它们具有通用可移植性和普遍可理解性的优势，尽管它们可能不完全匹配底层硬件的精度。

内核通过 :c:func:`k_cycle_get_32` 和 :c:func:`k_cycle_get_64` API 呈现"周期"计数。意图是此计数器表示操作系统能向用户呈现的最快周期计数器（例如 CPU 周期计数器）且读取操作非常快。预期非常敏感的应用代码可能以轮询方式使用它以获得最大精度。此计数器的频率可从 :c:func:`sys_clock_hw_cycles_per_sec` 获取。在大多数平台上，这是评估为 :kconfig:option:`CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC` 的运行时常量且对系统生命周期固定。在系统定时器频率不固定的平台上，:c:func:`sys_clock_hw_cycles_per_sec` 返回运行时值且应用代码不得假设单个不可变频率。

运行时系统定时器频率
------------------------------

某些平台需要系统定时器频率在运行时可用，要么因为定时器驱动程序从硬件发现时钟频率，要么因为定时器时钟频率可在启动后改变。

可在运行时改变活动系统定时器频率的平台必须启用 :kconfig:option:`CONFIG_SYSTEM_CLOCK_HW_CYCLES_PER_SEC_RUNTIME_UPDATE` 且：

* 在应用时钟更改后调用 :c:func:`z_sys_clock_hw_cycles_per_sec_update`。

* 如果系统定时器驱动程序缓存派生常量（如每 tick 周期数）或在时钟改变时需要重新编程硬件，提供 :c:func:`z_sys_clock_hw_cycles_per_sec_update` 的定时器驱动程序覆盖。

:c:func:`z_sys_clock_hw_cycles_per_sec_update` 的默认实现仅更新存储的频率值。

.. note::

  :kconfig:option:`CONFIG_SYSTEM_CLOCK_HW_CYCLES_PER_SEC_RUNTIME_UPDATE` 将系统定时器频率跟踪为单个**全局**值。它与每 CPU 频率缩放配置不兼容（不同 CPU 可能观察到不同系统定时器频率）。

  启用时，:c:func:`sys_clock_hw_cycles_per_sec` 和时间单位转换遵循当前运行时值。

对于异步计时，内核定义"tick"概念。"tick" 是内核执行所有内部运行时间和超时簿记的内部计数。预计中断在 tick 边界处传递（在可行范围内），且不跟踪分数 tick。tick 频率的选择可通过 :kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC` 配置。大多数硬件平台（支持设置任意中断超时的）的默认值预计在 10 kHz 范围内，软件仿真平台和传统驱动程序使用更传统的 100 Hz 值。

转换
----------

Zephyr 提供广泛枚举的转换库（带舍入控制）用于所有时间单位。任何"ms"（毫秒）、"us"（微秒）、"tick"或"cyc"单位可转换到任何其他单位。提供舍入控制，每个转换可用"floor"（向下舍入到最近输出单位）、"ceil"（向上舍入）和"near"（舍入到最近）。最后，输出精度可指定为 32 或 64 位。

例如：:c:func:`k_ms_to_ticks_ceil32` 将毫秒输入值转换为更高的 tick 数（返回截断到 32 位精度的结果）；:c:func:`k_cyc_to_us_floor64` 将测量的周期计数转换为完整 64 位精度的经过微秒数。参见参考文档了解转换例程的完整枚举。

在大多数平台上，各种计数器频率互为整数倍且输出适合单个字时，这些转换展开为 2-4 操作序列（仅在确实需要和请求时要求完整精度）。

.. _kernel_timing_uptime:

运行时间
======

内核代表应用跟踪系统运行时间计数。这始终可通过 :c:func:`k_uptime_get` 可用（提供系统启动以来的毫秒运行时间值）。预计这是大多数可移植应用代码使用的工具。

然而，内部跟踪是 tick 的 64 位整数计数。具有精确计时要求（愿意自己做转换到可移植实时单位）的应用可用 :c:func:`k_uptime_ticks` 访问此。

:c:func:`k_uptime_delta` 可用于获取参考和当前时间之间的经过时间。参考时间将更新到当前运行时间（以轻松计算下一个经过时间）。


超时
========

Zephyr 内核提供许多带"超时"参数的 API。概念上，这指示事件将发生的时间。例如：

* 内核阻塞操作（如 :c:func:`k_sem_take` 或 :c:func:`k_queue_get`）可提供超时（之后如果没有可用数据例程将返回错误代码）。

* 内核 :c:struct:`k_timer` 对象必须为其持续时间和周期指定延迟。

* 内核 :c:struct:`k_work_delayable` API 提供指示工作队列工作项何时被添加到系统队列的超时参数。

所有这些值用 :c:type:`k_timeout_t` 值指定。这是不透明结构体类型，必须用一系列内核超时宏之一初始化。最常见的 :c:macro:`K_MSEC` 定义当前时间后毫秒的时间。

相对超时的"当前时间"含义取决于上下文：

* 在超时回调内（如从传递给 :c:func:`k_timer_init` 的到期函数或传递给 :c:func:`k_work_init_delayable` 的工作处理函数）调度相对超时时，"当前时间"是当前触发的超时最初调度的精确时间（即使"真实时间"已前进）。这确保从另一个定时器的回调内调度的定时器始终与触发定时器以精确偏移计算。由此可以按固定间隔触发而不会随时间引入系统性时钟漂移。

* 从应用上下文调度超时时，"当前时间"意味着内核接收超时值时 :c:func:`k_uptime_ticks` 返回的值。

超时初始化的其他选项遵循上述单位约定：:c:macro:`K_NSEC()`、:c:macro:`K_USEC`、:c:macro:`K_TICKS` 和 :c:macro:`K_CYC()` 分别指定在指定纳秒、微秒、tick 和周期后到期的超时值。

:c:type:`k_timeout_t` 值的精度可配置，默认为 32 位。非 tick 单位中的大运行时间计数将经历复杂回绕语义，因此预计具有长运行时间的计时敏感应用将配置为使用 64 位超时类型。

最后，可将超时指定为自系统启动的绝对时间。用 :c:macro:`K_TIMEOUT_ABS_MS` 初始化的超时指示在系统运行时间达到指定值后到期的超时。类似地有纳秒、微秒、周期和 tick 变体的此 API。

计时内部
================

超时队列
-------------

所有用上述 API 指定的 Zephyr :c:type:`k_timeout_t` 事件在单个全局事件队列中管理。对事件采取的操作指定为请求事件的子系统提供的回调函数指针，连同预期嵌入子系统定义数据结构中的 :c:struct:`_timeout` 跟踪结构体（例如：:c:struct:`wait_q` 结构体或 :c:type:`k_tid_t` 线程结构体）。

注意通过 :c:type:`k_timeout_t` 传递的所有变体单位在插入队列时一次转换为 tick。内核内部无多次转换步骤，因此无论存在多少事件或超时可能多长，精度都保证在 tick 级别。

保存队列的数据结构在构建时通过 :kconfig:option:`CONFIG_TIMEOUT_BACKEND` 选择。仅前端在多个后端间共享（通告路径、SMP 重新进入处理和相对与绝对超时规则）；每个后端提供队列本身，因此集成者可匹配数据结构到工作负载而不触及通用代码。

默认 :kconfig:option:`CONFIG_TIMEOUT_BACKEND_DLIST` 将事件存储在按到期排序的双向链表中，每个保存从其前驱的 tick 差值计数。插入在挂起超时数量上是 O(N)：对典型系统挂起的少数几个不昂贵，但在许多未决时扩展性差。四个替代后端（目前全为实验性）用额外内存或行为换取大规模下更快插入：

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_MINHEAP` 将事件保存在以绝对到期为键的二进制最小堆中（插入和移除 O(log N)）。它需要 64 位 tick（:kconfig:option:`CONFIG_TIMEOUT_64BIT`）和固定容量堆（:kconfig:option:`CONFIG_TIMEOUT_HEAP_MAX_ENTRIES`，其溢出是致命的），且它不保留在同一 tick 到期的超时的触发顺序。

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_WHEEL` 是层次化定时器轮（近期 O(1) 插入和移除且之后排序溢出列表）。它有最大每事件和静态占用，不保留同 tick 触发顺序，且定期唤醒无 tick 空闲 CPU（因为其下次超时估计受轮周期限制（其他后端避免的功耗成本））。

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_BUCKET` 是单级分桶差值列表（定时器轮的更简单近亲）。它在可调近期窗口内提供 O(1) 插入（:kconfig:option:`CONFIG_TIMEOUT_BUCKET_LISTS`）且之后回退到排序溢出列表。它也需要 64 位 tick，但与定时器轮不同它保留同 tick 触发顺序且无空闲唤醒成本。

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_SKIPLIST` 是以绝对到期为键的 Pugh 跳表。预期插入和移除 O(log N) 且无容量限制，同 tick 触发顺序为先进先出。它需要 64 位 tick。每个事件保存 :kconfig:option:`CONFIG_TIMEOUT_SKIPLIST_MAX_LEVEL` 个前向指针，因此每事件 RAM 高于差值列表或最小堆。

非默认后端目标保持许多并发超时的系统（特别是聚集在近期的）。对大多数应用，差值列表仍是适当默认。

定时器驱动程序
-------------

内核计时在 tick 级别由定时器驱动程序驱动。该接口及其运行的锁在 :ref:`system_timer_drivers` 中描述。

时间分片
------------

计时子系统的辅助工作是向调度器提供 tick 计数器（允许实现线程的时间分片）。线程时间片不能是超时值（因为它不反映全局到期而是需要在 SMP 上下文中每个 CPU 独立跟踪的每 CPU 值）。

由于可能没有其他可用硬件驱动时间分片，Zephyr 复用现有定时器驱动程序。这意味着当时间分片线程当前被调度时，传递给 :c:func:`sys_clock_set_timeout` 的值可能被钳制到小于当前下次超时的值。

保持毫秒 API 的子系统
-------------------------------------

一般来说，此类代码将像应用代码一样移植。来自用户的毫秒值可由子系统以任何方式处理，然后在呈现给内核时用 :c:macro:`K_MSEC()` 转换为内核超时。

显然这以无法使用新特性（如更高精度超时构造函数或绝对超时）为代价。但对许多需求简单的子系统，这可能可接受。

一个复杂性是 :c:macro:`K_FOREVER`。可能过去已能接受此值到其毫秒 API 的子系统不再能（因为它不再是整数类型）。此类代码需要使用不同的整数值令牌表示"永远"。:c:macro:`K_NO_WAIT` 当然也有相同类型安全关注，但由于它（一直）只是数值零，它有自然移植路径。

使用 ``k_timeout_t`` 的子系统
--------------------------------

理想情况下，接受指定等待时间的"超时"参数的代码应尽可能使用内核原生抽象。但 :c:type:`k_timeout_t` 是不透明的，需要在应用检查前转换。

某些转换是简单的。需要测试 :c:macro:`K_FOREVER` 的代码可简单用 :c:macro:`K_TIMEOUT_EQ()` 宏测试不透明结构体的相等性并采取特殊行动。

更复杂的情况是子系统需要接受超时并循环（等待其完成同时执行可能需要底层内核代码上多个阻塞操作的处理）。例如，考虑此设计：

.. code-block:: c

    void my_wait_for_event(struct my_subsys *obj, int32_t timeout_in_ms)
    {
        while (true) {
            uint32_t start = k_uptime_get_32();

            if (is_event_complete(obj)) {
                return;
            }

            /* Wait for notification of state change */
            k_sem_take(obj->sem, timeout_in_ms);

            /* Subtract elapsed time */
            timeout_in_ms -= (k_uptime_get_32() - start);
        }
    }

此代码需要检查超时值（这不再可能）。对于此类情况，新 API 提供内部 :c:func:`sys_timepoint_calc` 和 :c:func:`sys_timepoint_timeout` 例程（将任意超时转换到和从基于其将到期的运行时间 tick 的时间点值）。因此此类循环可能如下：


.. code-block:: c

    void my_wait_for_event(struct my_subsys *obj, k_timeout_t timeout)
    {
        /* Compute the end time from the timeout */
        k_timepoint_t end = sys_timepoint_calc(timeout);

        do {
            if (is_event_complete(obj)) {
                return;
            }

            /* Update timeout with remaining time */
            timeout = sys_timepoint_timeout(end);

            /* Wait for notification of state change */
            k_sem_take(obj->sem, timeout);
        } while (!K_TIMEOUT_EQ(timeout, K_NO_WAIT));
    }

注意 :c:func:`sys_timepoint_calc` 接受特殊值 :c:macro:`K_FOREVER` 和 :c:macro:`K_NO_WAIT`（对绝对超时和常规超时行为相同）。相反，:c:func:`sys_timepoint_timeout` 如果这些用于创建时间点可能返回 :c:macro:`K_FOREVER` 或 :c:macro:`K_NO_WAIT`（后者在时间点现在在过去时也返回）。对简单情况，:c:func:`sys_timepoint_expired` 也可用。

但使用它们的子系统仍需要一些注意。注意差值超时需要相对于"当前时间"解释，显然该时间是调用 :c:func:`sys_timepoint_calc` 的时间。但用户预期时间是他们传递超时给你的时间。必须注意仅调用一次此函数（尽可能同步于用户代码中的超时创建）。它不应用于"存储"的超时值，且绝不应在循环中迭代调用。


API 参考
*************

.. doxygengroup:: clock_apis

