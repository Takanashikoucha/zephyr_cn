.. _system_timer_drivers:

系统定时器驱动
####################

此页描述内核的节拍（tick）计时与产生这些节拍的硬件驱动之间的接口。
该计时的内核侧以及应用程序所看到的一切，在 :ref:`kernel_timing` 中描述。

定时器驱动
=============

内核在节拍层面的计时由一个具有相对简单 API 的定时器驱动来驱动。

* 驱动应能通过 :c:func:`sys_clock_announce` 调用向内核"通告"新的节拍，
  该调用传递自上次通告调用（或系统启动）以来经过的整数节拍数。
  这些调用可以在任何时间发生，但驱动应尽力（在受中断延迟交互影响、
  实际可行的范围内）确保它们发生在节拍边界附近（即不在某个节拍的
  "中间"），并且最重要的是，它们随时间推移必须正确，且相对于其他
  计数器和真实世界时间的偏斜最小。

* 驱动应向内核提供 :c:func:`sys_clock_set_timeout` 调用，
  指示在内核必须收到通告调用以触发已注册的超时之前，
  最多可以经过多少节拍。在该时刻之前通告新的节拍是合法的
  （尽管节拍数必须正确），但在那之后延迟会导致事件被错过。
  注意此处传递的超时值是相对于当前时间的差值，但这并不免除驱动
  随时间以稳定速率提供节拍的要求。此函数的简单实现容易出现
  分数节拍被错误"重置"从而导致时钟偏斜的缺陷。

* 驱动应提供 :c:func:`sys_clock_elapsed` 调用，
  给出自上次 :c:func:`sys_clock_announce` 调用以来已经过了多少节拍
  （与真实世界的时钟相比）的当前指示，内核需要用它来检查
  新到达的超时是否已到期。

* 驱动可选地提供 :c:func:`sys_clock_no_timeout` 调用。
  当没有超时时（即超时队列为空）且启用了
  :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE` 时，
  内核用它代替 :c:func:`sys_clock_set_timeout` 进行调用。

  此时不会有节拍通告到来，系统也不关心精确的运行时间（uptime）统计，
  因此驱动可以做一些事情来节省资源。下一次 :c:func:`sys_clock_set_timeout`
  调用时恢复正常操作；与 :c:func:`sys_clock_disable` 不同，这不是拆除（teardown）。

  定时器的*计数器*不得停止。:c:func:`sys_clock_cycle_get_32`
  和 :c:func:`sys_clock_cycle_get_64` 必须像该调用从未发生一样继续向上计数。

  .. note::

     即使超时队列为空，CPU 仍会继续运行，例如就绪队列中仍有线程，
     或者有中断触发。这些线程和中断服务程序（ISR）可能调用
     :c:func:`k_cycle_get_32` 或 :c:func:`k_busy_wait`。
     这限制了实现可以做些什么：屏蔽定时器中断是安全的，
     而门控（gating）定时器的时钟很可能不安全。具体哪些操作是安全的取决于硬件。

  该钩子是可选的。没有它时，:c:func:`sys_clock_set_timeout` 会被要求表达
  它能表达的最长等待时间，即 ``UINT32_MAX`` 个节拍。这在数值上就是此处
  ``K_TICKS_FOREVER`` 的含义——长期以来的"无截止时刻"信号——
  因此尚未改造的驱动仍可继续工作。

* 驱动可选地提供 :c:func:`sys_clock_idle_enter` 调用，
  电源管理路径在 CPU 即将进入低功耗空闲时使用它代替
  :c:func:`sys_clock_set_timeout`。它接收距下一次预期唤醒的节拍数；
  如果没有唤醒、且运行时间统计允许漂移，则接收 ``SYS_CLOCK_IDLE_FOREVER``。

  向低功耗唤醒定时器移交、或以其他方式重新配置自身以进入睡眠的驱动，
  在此处完成这些操作。收到 ``SYS_CLOCK_IDLE_FOREVER`` 时，它还可以停止其
  时间基准——这是 :c:func:`sys_clock_no_timeout` 不允许的，因为 CPU 正在退出，
  而 :c:func:`sys_clock_idle_exit` 保证在返回时运行。只有发起调用的 CPU 会进入空闲，
  因此时间基准在多个 CPU 之间共享的驱动必须确保只有最后一个进入空闲的 CPU 停止时钟。

  该钩子是可选的。没有它时，:c:func:`sys_clock_set_timeout` 会以已弃用的
  ``idle`` 参数设为 ``true`` 的方式被调用，因此仍依赖该参数来控制低功耗处理的
  驱动仍可继续工作。

最后三个入口点划分了系统可能处于的四种状态：

.. list-table::
   :header-rows: 1
   :widths: 15 45 40

   * -
     - 无待处理事项
     - 有待处理事项
   * - **运行中**
     - ``sys_clock_no_timeout()``
     - ``sys_clock_set_timeout(ticks)``
   * - **空闲**
     - ``sys_clock_idle_enter(SYS_CLOCK_IDLE_FOREVER)``
     - ``sys_clock_idle_enter(ticks)``

没有 :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE` 时，左列永远不会出现：
内核保持一个合成的截止时刻处于就绪状态，使运行时间保持精确，
驱动只会看到右列。

定时器驱动加锁
====================

内核通过 :c:func:`sys_clock_lock` 和 :c:func:`sys_clock_unlock`
暴露一个统一的定时器锁。此锁同时保护内核内部的节拍计时
（``curr_tick``、超时队列）以及必须与其保持一致的任何驱动私有状态
（例如硬件周期计数器基线）。

维护内部状态的定时器驱动应在其 ISR 开始时获取此锁，更新其硬件状态，
然后将锁密钥传递给 :c:func:`sys_clock_announce_locked` 由其消费。
这确保驱动的周期计数器基线与内核的 ``curr_tick`` 始终在同一把锁下更新，
消除了在 SMP 系统上（或较少见的、高优先级 ISR 需要一致实时参考的 UP 系统上）
使用两把分离锁时可能出现的竞争条件。

驱动提供的回调 :c:func:`sys_clock_set_timeout` 和 :c:func:`sys_clock_elapsed`
始终由内核在此锁已持有的状态下调用。

为向后兼容，:c:func:`sys_clock_announce` 仍然可用，并在内部获取锁。
新驱动和已迁移的驱动应优先采用 :c:func:`sys_clock_lock` /
:c:func:`sys_clock_announce_locked` 模式。

注意，此 API 的自然实现会得到一个"无节拍"（tickless）内核：
它只为已注册的事件接收并处理定时器中断，依赖可编程的硬件计数器
提供不规则的中断。但传统的"有节拍"（ticked）或"简单"（dumb）
计数器驱动也可以简单地实现：

* 驱动可以按与操作系统节拍速率对应的固定速率接收中断，
  每次调用 :c:func:`sys_clock_announce` 并传入参数 1。

* 驱动可以忽略 :c:func:`sys_clock_set_timeout` 调用，
  因为无论超时状态如何，每个节拍都会被通告。

* 驱动可以对每次 :c:func:`sys_clock_elapsed` 调用返回零，
  因为最多只能检测到一个节拍已经过（否则就会收到中断）。

SMP 细节
==========

一般而言，上述定时器 API 在多处理器环境中运行时不会改变。
内核会在内部对所有访问进行适当的同步，并确保所有临界区都小而精简。
但以下几点值得注意：

* Zephyr 不关心由哪个 CPU 处理定时器中断。让所有定时器中断都在单个
  处理器上处理并不违规（尽管在某些情况下可能不太理想）。
  现有的 SMP 架构实现的是对称的定时器驱动。

* 预期 :c:func:`sys_clock_announce` 调用在驱动层面是全局同步的。
  内核不做任何每 CPU 跟踪，并预期如果两个定时器中断几乎同时触发，
  只有一个会向计时子系统提供当前节拍计数。如果没有节拍经过，
  另一个可以合法地提供零节拍计数。它不应因时间片（timeslicing）要求
  而"跳过"通告调用（参见 :ref:`kernel_timing` 中的时间片说明）。

* 某些 SMP 硬件使用单个全局定时器设备，其他则使用每 CPU 计数器。
  这里的复杂性（例如确保 CPU 之间的计数器同步）预期由驱动而非内核来管理。

* 通过 :c:func:`sys_clock_set_timeout` 传回驱动的下一个超时值，
  对每个 CPU 都完全相同地给出。因此默认情况下，每个 CPU 都会对每个事件
  看到同时发生的定时器中断，尽管按定义只有一个应对 :c:func:`sys_clock_announce`
  看到非零的节拍参数。对计时敏感的应用程序来说，这很可能是一个正确的
  默认值（因为它最小化了某个出错的 ISR 或中断锁延迟超时的可能性），
  但在某些情况下可能是性能问题。当前设计预期任何此类优化
  都是定时器驱动的责任。

通用无节拍核心
=====================

上述工作——周期到节拍的转换、通告基线、节拍对齐的截止时刻计算，
以及计数器回绕和范围处理——在几乎每个无节拍驱动中都大同小异，
而手写变体是反复出现的定时器缺陷来源。
:zephyr_file:`drivers/timer/system_timer_generic.h` 将该逻辑集中承载一次。

它是一个实现头文件，而非声明头文件：包含它即*定义*
:c:func:`sys_clock_set_timeout`、:c:func:`sys_clock_elapsed` 和
:c:func:`sys_clock_cycle_get_32` / :c:func:`sys_clock_cycle_get_64`。
任意数量的驱动都可以基于它构建；每个驱动在提供下述宏和原语后
包含它一次。一次构建只编译一个系统定时器驱动，因此这些定义只会落地一次。
驱动此后只以周期（cycles）为单位工作；节拍域归核心（core）所有。

核心会发出两个周期读取函数，64 位的那个无论计数器宽度如何都会发出：
通告基线是 64 位的，链接器会丢弃没有任何调用的那个读取函数。

驱动是否同时选择 :kconfig:option:`CONFIG_TIMER_HAS_64BIT_CYCLE_COUNTER`
仍由其自己决定。该选项表示 64 位读取是廉价的，或者至少不比 32 位读取贵，
因此偏好较窄的读取函数没有任何收益。使用 ``TIMER_CORE_COUNTER_NONATOMIC`` 时，
两者都通过时钟锁，上述结论成立；对于宽度小于 64 位的原子计数器，
只有 64 位读取函数会获取锁，32 位的那个保持无锁读取。

需要两个原语：``timer_driver_cycle_get()`` 读取硬件周期计数器，
以及一个装载（arming）函数——根据后端是 ``timer_driver_set_compare()``
还是 ``timer_driver_set_reload()``。驱动的 ISR 在确认（acknowledge）硬件后
调用 ``timer_core_announce()``；其初始化在连接 IRQ 后调用 ``timer_core_init()``；
在 SMP 上，其 ``smp_timer_init()`` 调用 ``timer_core_smp_prime()``。

后端选择
-----------------

以下宏恰好有一个，用于说明硬件是什么：

``TIMER_CORE_BACKEND_COMPARE_ORDERED``
    绝对比较器，有序匹配：计数器达到或超过编程值时中断触发一次，
    因此已经在过去的截止时刻会立即触发。可用范围是计数器宽度的一半。

``TIMER_CORE_BACKEND_COMPARE_EXACT``
    绝对比较器，相等匹配：计数器经过某值之后再写入该值，
    会在整个计数器周期内被错过。核心通过一个验证（verify）循环写入比较器，
    因此驱动无需自己设置最小延迟下限。

``TIMER_CORE_BACKEND_RELOAD``
    相对延迟：递减计数器（down-counter）和比较匹配复位
    （compare-match-reset）的周期定时器。假定会自动重载（auto-reload），
    因此有节拍（ticked）内核会从初始化时设置的值自由运行（free-run）。

可选宏
---------------

每个宏仅在下述默认值不适用时才定义：

``TIMER_CORE_CYCLES_PER_SEC``
    计数器速率，以 Hz 为单位。默认为内核系统时钟速率。当计数器经过
    预分频或按自身固定速率运行时，需设置此宏。核心从中派生
    ``TIMER_CORE_CYC_PER_TICK``，驱动可以读取它用于自身的硬件设置
    （通常是初始化时编程的一个节拍周期），但绝不应自行定义它。

``TIMER_CORE_CYCLES_PER_SEC_RUNTIME``
    上述速率是一个变量而非构建时常量，因为它从时钟控制器读取
    或在初始化时计算。核心会预计算每节拍的周期数一次，
    而不是依赖除法折叠（division folding）。
    该变量必须在调用 ``timer_core_init()`` 之前保持其最终值。

``TIMER_CORE_COUNTER_WIDTH``
    ``timer_driver_cycle_get()`` 返回的计数的宽度（以位为单位，最多 64 位）。
    默认为原生寄存器宽度。宽度不同的计数器必须声明其自身的宽度：
    32 位 CPU 上真正的 64 位计数器否则会继承一个 32 位掩码，
    从而丢失超过 2^32 个周期的任何跨度。核心会把每个差值掩码到该宽度，
    因此窄计数器按原样读取，驱动永远不需要在软件中扩展计数。

``TIMER_CORE_COUNTER_NONMONOTONIC``
    计数器可能短暂地读出一个比已观察值更小的值，
    就像 QEMU SMP 下的全局定时器那样。核心将向后的读取视为"无经过"，
    而非一次巨大的跳跃。

``TIMER_CORE_COUNTER_NONATOMIC``
    ``timer_driver_cycle_get()`` 不是单次原子读取，
    而是由 ISR 也会触及的状态合成的值。核心会改为在时钟锁下读取它。

``TIMER_CORE_HAVE_CYCLE_GET_32``、``TIMER_CORE_HAVE_CYCLE_GET_64``
    驱动自行定义该入口点，核心则不定义。用于需要缩放的计数器。
    include 后可用的 ``timer_core_cycle_get()`` 以计数器自身的域
    给出全宽计数，供缩放使用。

    设置了 ``TIMER_CORE_CYCLES_PER_SEC`` 的驱动必须提供 32 位的那个，
    因为按自身速率运行的计数器是内核无法直接读取的。
    此时核心也不会发出 64 位读取函数，因为它处于驱动刚刚声明为外部的域中。
    如果希望核心也发出 64 位读取函数，请同时提供它。

``TIMER_CORE_ALARM_MAX_CYCLES``
    装载原语能表达的最大值，仅此而已。默认为 ``TIMER_CORE_COUNTER_WIDTH``
    的完整跨度，因为闹钟（alarm）和计数器通常是一体化的硬件。
    当装载范围由其他因素决定时，需设置此宏：例如窄于计数器的
    比较或重载寄存器，或者独立的设备。

    它声明的是硬件容量，因此不包含安全余量。核心从
    ``TIMER_CORE_COUNTER_WIDTH`` 派生自己的上限：它不会把装载时刻安排在
    比上次通告超前超过计数器跨度的一半（使用
    ``TIMER_CORE_COUNTER_NONMONOTONIC`` 时为四分之一）的位置，
    从而保证迟到的通告仍能产生掩码可解析的差值。两个上限中先触及的那个生效。

``TIMER_CORE_ALARM_MIN_CYCLES``
    重载下限，以周期为单位，仅 ``TIMER_CORE_BACKEND_RELOAD`` 使用。默认为 1。

``TIMER_CORE_ALARM_LEAD_CYCLES``
    比较器必须超前计数器多少周期才能捕捉到匹配，
    仅 ``TIMER_CORE_BACKEND_COMPARE_EXACT`` 使用。默认为 1，
    即计数器仍低于写入值时比较器触发。对于必须先把写入传递到
    计数器的时钟域、且对距离更近的匹配会错过的硬件，请调大此值。

新的无节拍驱动应基于此头文件构建，而不是重新实现节拍计时。
该头文件完整记录了每个宏和原语。
