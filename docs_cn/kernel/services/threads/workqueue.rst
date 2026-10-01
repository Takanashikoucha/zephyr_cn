.. _workqueues_v2:

工作队列线程
#################

.. contents::
    :local:
    :depth: 1

:dfn:`工作队列` 是一种使用专用线程以先进先出方式处理工作项的内核对象。每个工作项通过调用该工作项指定的函数来处理。工作队列通常由中断服务例程（ISR）或高优先级线程使用，将非紧急处理卸载到低优先级线程，以避免影响对时间敏感的处理。

可以定义任意数量的工作队列（仅受可用 RAM 限制）。每个工作队列由其内存地址引用。

工作队列具有以下关键属性：

* 一个**队列**，包含已添加但尚未处理的工作项。

* 一个处理队列中工作项的**线程**。该线程的优先级可配置，允许根据需要设为协同或抢占式。

无论工作队列线程的优先级如何，工作队列线程将在每个提交的工作项之间让出，以防止协同工作队列饿死其他线程。

工作队列在使用之前必须被初始化。这将其队列设置为空并生成工作队列的线程。该线程永远运行，但在没有工作项可用时睡眠。

工作项生命周期
********************

可以定义任意数量的**工作项**。每个工作项由其内存地址引用。

工作项被分配一个**处理函数**，即工作项被处理时由工作队列线程执行的函数。该函数接受单个参数，即工作项本身的地址。工作项还维护关于其状态的信息。

工作项在使用之前必须被初始化。这记录工作项的处理函数并将其标记为未挂起。

工作项可由 ISR 或线程通过将其提交到工作队列来**入队**（:c:enumerator:`K_WORK_QUEUED`）。提交工作项将其追加到工作队列的队列。一旦工作队列线程处理完队列中所有先前工作项，线程将从队列移除下一个工作项并调用其处理函数。根据工作队列线程的调度优先级和队列中其他工作项所需的工作量，已入队的工作项可能很快被处理，也可能在队列中保持较长时间。

可延迟工作项可被**调度**（:c:enumerator:`K_WORK_DELAYED`）到工作队列；参见 `可延迟工作`_。

工作项在某个工作队列上运行时为**运行中**（:c:enumerator:`K_WORK_RUNNING`），如果它在某线程请求取消前已开始运行，则也可能处于**取消中**（:c:enumerator:`K_WORK_CANCELING`）状态。

工作项可处于多个状态；例如它可以：

* 在某个队列上运行；

* 被标记为取消中（因为某线程使用 :c:func:`k_work_cancel_sync()` 等待直到工作项完成）；

* 被入队以在同一队列上再次运行；

* 被调度以提交到（可能不同的）队列

*全部同时*。处于这些状态中任何状态的工作项是**挂起**（:c:func:`k_work_is_pending()`）或**忙**（:c:func:`k_work_busy_get()`）。

处理函数可以使用线程可用的任何内核 API。然而，潜在阻塞的操作（如获取信号量）必须谨慎使用，因为处理函数完成执行前工作队列无法处理队列中后续工作项。

传递给处理函数的单个参数如不需要可忽略。如果处理函数需要关于其要执行的工作的额外信息，工作项可嵌入在更大的数据结构中。然后处理函数可用 :c:macro:`CONTAINER_OF` 用参数值计算包含数据结构的地址，从而获得所需额外信息的访问。

工作项通常初始化一次，然后每当需要执行工作时提交到特定工作队列。如果 ISR 或线程尝试提交已入队的工作项，工作项不受影响；工作项保持在工作队列队列中的当前位置，工作仅执行一次。

处理函数被允许将其工作项参数重新提交到工作队列，因为那时工作项不再入队。这允许处理函数分阶段执行工作，而不会不当延迟工作队列队列中其他工作项的处理。

.. important::

    挂起的工作项*不得*在工作队列线程处理前被修改。这意味着工作项在忙时不得重新初始化。此外，工作项处理函数执行其工作所需的任何额外信息在处理函数完成执行前不得被修改。

.. _k_delayable_work:

可延迟工作
**************

ISR 或线程可能需要调度一个仅在指定时间段后才处理的工作项（而非立即处理）。这可通过**调度**一个**可延迟工作项**在未来时间提交到工作队列完成。

可延迟工作项包含一个标准工作项，但添加了记录何时何地应提交该工作项的字段。

可延迟工作项的初始化和调度到工作队列的方式类似标准工作项，尽管使用不同的内核 API。当发出调度请求时，内核启动一个在指定延迟过后触发的超时机制。一旦超时发生，内核将工作项提交到指定工作队列，在那里保持入队直到以标准方式处理。

注意用于可延迟工作的处理函数仍接收指向底层非可延迟工作结构的指针，该指针无法从 :c:struct:`k_work_delayable` 公开访问。要访问包含可延迟工作对象的对象，使用此惯用法：

.. code-block:: c

    static void work_handler(struct k_work *work)
    {
            struct k_work_delayable *dwork = k_work_delayable_from_work(work);
            struct work_context *ctx = CONTAINER_OF(dwork, struct work_context,
 	                                           timed_work);

            ...


触发工作
**************

:c:func:`k_work_poll_submit` 接口响应**轮询事件**（参见 :ref:`polling_v2`）调度一个触发工作项，当被监视资源变得可用或轮询信号被提升或超时发生时调用用户定义的函数。与 :c:func:`k_poll` 不同，触发工作不需要专用线程等待或主动轮询以等待轮询事件。

触发工作项是具有以下额外属性的标准工作项：

* 一个指向将触发工作项提交到工作队列的轮询事件数组的指针。

* 包含轮询事件的数组的大小。

触发工作项的初始化和提交到工作队列的方式类似标准工作项，尽管使用专用的内核 API。当发出提交请求时，内核开始观察由轮询事件指定的内核对象。一旦至少一个被观察的内核对象改变状态，工作项被提交到指定工作队列，在那里保持入队直到以标准方式处理。

.. important::

    触发工作项以及引用的轮询事件数组必须有效且在整个触发工作项生命周期（从提交到工作项执行或取消）中不可修改。

ISR 或线程可**取消**它已提交的触发工作项，只要它仍在等待轮询事件。在这种情况下，内核停止等待附加的轮询事件且指定工作不执行。否则无法执行取消。

系统工作队列
*****************

内核定义一个称为*系统工作队列*的工作队列，可用于任何需要工作队列支持的应用或内核代码。系统工作队列是可选的，仅在应用使用它时存在。

.. important::

    仅当无法向系统工作队列提交新工作项时才应定义额外工作队列，因为每个新工作队列在内存占用上产生显著成本。如果其工作项无法与现有系统工作队列工作项共存而不产生不可接受的影响，则可证明新工作队列合理；例如，如果新工作项执行将其他系统工作队列处理延迟到不可接受程度的阻塞操作。

    还要注意：系统工作队列默认具有最低协同优先级。这意味着排空系统工作队列优先于*所有可抢占线程*。将系统工作队列的优先级配置为抢占式有风险，因为子系统和驱动程序可能隐式依赖工作项在协同上下文中执行。因此，较低优先级的单独工作队列可能适合低优先级任务。

如何使用工作队列
*********************

定义和控制工作队列
===================================

工作队列使用 :c:struct:`k_work_q` 类型的变量来定义。工作队列通过定义其线程使用的栈区域、初始化 :c:struct:`k_work_q`（将其内存清零或调用 :c:func:`k_work_queue_init`）然后调用 :c:func:`k_work_queue_start` 来初始化。栈区域必须使用 :c:macro:`K_THREAD_STACK_DEFINE` 定义以确保在内存中正确设置。

下面的代码定义并初始化一个工作队列：

.. code-block:: c

    #define MY_STACK_SIZE 512
    #define MY_PRIORITY 5

    K_THREAD_STACK_DEFINE(my_stack_area, MY_STACK_SIZE);

    struct k_work_q my_work_q;

    k_work_queue_init(&my_work_q);

    k_work_queue_start(&my_work_q, my_stack_area,
                       K_THREAD_STACK_SIZEOF(my_stack_area), MY_PRIORITY,
 		       NULL);

此外，队列标识和与线程重新调度相关的某些行为可通过可选的最后参数控制；参见 :c:func:`k_work_queue_start()` 了解细节。

以下 API 可用于与工作队列交互：

* :c:func:`k_work_queue_drain()` 可用于阻塞调用者直到工作队列无剩余工作项。队列正在排空时接受从工作队列线程重新提交的工作项，但拒绝来自任何其他线程或 ISR 的工作项。提交更多工作的限制可延长到排空操作完成之后，以便允许阻塞线程在队列"堵塞"时执行额外工作。注意排空队列对可延迟工作项的调度或处理无效果，但如果队列堵塞且截止期过期，工作项将静默提交失败。

* :c:func:`k_work_queue_unplug()` 移除先前排空操作导致的对队列提交的任何先前阻塞。

提交工作项
======================

工作项使用 :c:struct:`k_work` 类型的变量来定义。必须通过调用 :c:func:`k_work_init` 初始化，除非使用 :c:macro:`K_WORK_DEFINE` 定义（此时初始化在编译时执行）。

已初始化的工作项可通过调用 :c:func:`k_work_submit` 提交到系统工作队列，或通过调用 :c:func:`k_work_submit_to_queue` 提交到指定工作队列。

下面的代码演示 ISR 如何将其错误消息的打印卸载到系统工作队列。注意如果 ISR 尝试在工作项仍入队时重新提交，工作项保持不变且关联错误消息不打印。

.. code-block:: c

    struct device_info {
        struct k_work work;
        char name[16]
    } my_device;

    void my_isr(void *arg)
    {

        ...
        if (error detected) {
            k_work_submit(&my_device.work);
	}

	...
    }

    void print_error(struct k_work *item)
    {
        struct device_info *the_device =
            CONTAINER_OF(item, struct device_info, work);
        printk("Got error on device %s\n", the_device->name);
    }

    /* initialize name info for a device */
    strcpy(my_device.name, "FOO_dev");

    /* initialize work item for printing device's error messages */
    k_work_init(&my_device.work, print_error);

    /* install my_isr() as interrupt handler for the device (not shown) */

    ...


以下 API 可用于检查工作项的状态或与其同步：

* :c:func:`k_work_busy_get()` 返回指示工作项状态的标志快照。零值表示工作未被调度、提交、正在执行或以其他方式仍被工作队列基础设施引用。

* :c:func:`k_work_is_pending()` 是一个辅助函数，当且仅当工作被调度、入队或运行中时返回 ``true``。

* :c:func:`k_work_flush()` 可从线程调用以阻塞直到工作项完成。如果工作未挂起则立即返回。

* :c:func:`k_work_cancel()` 尝试防止工作项被执行。这可能成功也可能不成功。从 ISR 调用是安全的。

* :c:func:`k_work_cancel_sync()` 可从线程调用以阻塞直到工作完成；如果取消成功或不需要（工作未提交或运行中）则立即返回。这可用于 :c:func:`k_work_cancel()`（从 ISR）调用后确认 ISR 发起的取消完成。

调度可延迟工作项
================

可延迟工作项使用 :c:struct:`k_work_delayable` 类型的变量来定义。必须通过调用 :c:func:`k_work_init_delayable` 初始化。

对于延迟工作有两个常见用例，取决于新事件发生时是否应延长截止期。示例是收集异步到达的数据（如与键盘关联的 UART 的字符）。有两个在延迟后提交工作的 API：

* :c:func:`k_work_schedule()`（或 :c:func:`k_work_schedule_for_queue()`）调度工作在特定时间或延迟后执行。在延迟完成前用此 API 进一步尝试调度相同工作项不会改变工作项被提交到其队列的时间。如果策略是在收到**第一个**未处理数据后指定延迟内继续收集数据则使用此。

* :c:func:`k_work_reschedule()`（或 :c:func:`k_work_reschedule_for_queue()`）无条件设置工作的截止期，替换任何先前未完成延迟并在必要时更改目标队列。如果策略是在收到**最后一个**未处理数据后指定延迟内继续收集数据则使用此。

如果工作项未调度，两个 API 行为相同。如果指定 :c:macro:`K_NO_WAIT` 作为延迟，行为如同工作项被直接立即提交到目标队列（不等待最小超时，除非使用 :c:func:`k_work_schedule()` 且先前延迟未完成）。

两者都有允许控制用于提交的队列的变体。

辅助函数 :c:func:`k_work_delayable_from_work()` 可用于从传递给工作处理函数的 :c:struct:`k_work` 指针获取指向包含 :c:struct:`k_work_delayable` 的指针。

以下额外 API 可用于检查工作项的状态或与其同步：

* :c:func:`k_work_delayable_busy_get()` 是 :c:func:`k_work_busy_get()` 的可延迟工作对应物。

* :c:func:`k_work_delayable_is_pending()` 是 :c:func:`k_work_is_pending()` 的可延迟工作对应物。

* :c:func:`k_work_flush_delayable()` 是 :c:func:`k_work_flush()` 的可延迟工作对应物。

* :c:func:`k_work_cancel_delayable()` 是 :c:func:`k_work_cancel()` 的可延迟工作对应物；类似地 :c:func:`k_work_cancel_delayable_sync()`。

与工作项同步
=============================

虽然常规和可延迟工作项的状态都可用 :c:func:`k_work_busy_get()` 和 :c:func:`k_work_delayable_busy_get()` 从任何上下文确定，但某些用例需要在工作项提交后与其同步。:c:func:`k_work_flush()`、:c:func:`k_work_cancel_sync()` 和 :c:func:`k_work_cancel_delayable_sync()` 可从线程上下文调用以等待直到达到请求状态。

这些 API 必须提供一个 :c:struct:`k_work_sync` 对象，该对象无应用可检查的组件但提供同步对象所需。如果代码预期在具有 :kconfig:option:`CONFIG_KERNEL_COHERENCE` 的架构上工作，则这些对象不应在栈上分配。

工作队列最佳实践
************************

避免竞态条件
=====================

有时工作项必须处理的数据自然线程安全，例如当它由某线程放入 :c:struct:`k_queue` 并在工作线程中处理时。更常见的是需要外部同步以避免数据竞态：工作线程可能检查或操纵由另一线程或中断访问的共享状态的情况。此类状态可能是指示需要执行工作的标志，或由 ISR 或线程填充并由工作处理函数读取的共享对象。

对于简单标志 :ref:`atomic_v2` 可能足够。在其他情况下可使用自旋锁（:c:struct:`k_spinlock`）或线程感知锁（:c:struct:`k_sem`、:c:struct:`k_mutex`、...）确保不发生数据竞态。

如果选定的锁机制可 :ref:`api_term_sleep`，则允许工作线程睡眠会饿死其他工作队列工作项（它们可能需要进展以释放锁）。工作处理函数应尝试用其无等待路径获取锁。例如：

.. code-block:: c

    static void work_handler(struct work *work)
    {
            struct work_context *parent = CONTAINER_OF(work, struct work_context,
 	                                              work_item);

            if (k_mutex_lock(&parent->lock, K_NO_WAIT) != 0) {
                    /* NB: 如果工作项正在被取消则提交将失败。 */
                    (void)k_work_submit(work);
 		   return;

 	   }

 	   /* 在锁下做事 */

 	   k_mutex_unlock(&parent->lock);

 	   /* 在无锁下做事 */
    }

注意如果锁被优先级低于工作队列的线程持有，重新提交可能饿死将释放锁的线程，导致应用失败。上述惯用法必需时，首选可延迟工作项，且工作应以非零延迟重新调度，以允许持有锁的线程取得进展。

注意从工作处理函数提交如果工作项已被取消可能失败。通常这可接受，因为处理函数完成后取消将完成。如果不可接受，上述代码必须采取其他步骤通知应用工作无法执行。

单独隔离的工作项是自锁定的，因此你无需仅为了提交或调度它们而持有外部锁。即使你用由此类锁保护的外部状态防止进一步重新提交，只要你确定最终工作项将获取其锁并检查状态以确定是否应做任何事，重新提交就是安全的。如果可延迟工作项在其处理函数中因无法获取锁而重新调度，则需要某些其他自锁定状态（如应用/驱动程序在取消发起时设置的原子标志）来检测取消并避免被取消的工作项在截止期后被再次提交。

检查返回值
==================

所有工作 API 函数返回底层操作的状态，在许多情况下验证获得预期结果很重要。

* 提交工作项（:c:func:`k_work_submit_to_queue`）如果工作正在被取消或队列不接受新工作项可能失败。如果发生，工作不执行，这可能导致由工作处理函数活动驱动的子系统变得无响应。

* 异步取消（:c:func:`k_work_cancel` 或 :c:func:`k_work_cancel_delayable`）可能在工作项仍被处理函数运行时完成。继续操纵与工作处理函数共享的状态将导致可能导致失败的数据竞态。

Zephyr 代码中已存在许多竞态条件，因为未检查操作的结果。

可能有充分理由相信指示操作未按预期完成的返回值不是问题。在这些情况下，代码应清楚记录这一点，通过（1）将返回值强制转换为 ``void`` 表示故意忽略结果，（2）记录意外情况下发生什么。例如：

.. code-block:: c

    /* 如果这失败，工作处理函数将检查 pub->active 并
     * 不传输就退出。

     */
    (void)k_work_cancel_delayable(&pub->timer);

然而在这种情况下，以下代码仍必须避免数据竞态，因为它无法保证工作线程未访问工作相关状态。

不要过早优化
==========================

工作队列 API 设计为从多个线程和中断调用时安全。尝试外部检查工作项的状态并基于结果做决策很可能创建新问题。

因此当新工作到来时，直接提交它。不要尝试通过用 :c:func:`k_work_is_pending` 或 :c:func:`k_work_busy_get` 检查快照状态或从 :c:func:`k_work_delayable_remaining_get()` 检查非零延迟来"优化"以检查工作项是否已提交。这些检查是脆弱的："忙"指示可能在测试返回时已过时，"不忙"指示如果工作从多个上下文提交也可能是错的（或（对于可延迟工作）截止期已完成但工作仍处于入队或运行中状态）。

通用最佳实践是始终在共享状态中维护某些可由处理函数检查以确认是否有工作要做的条件。这样你可以将工作处理函数用作标准清理路径：无需在提交工作项的点处理取消和清理，你可能能在工作处理函数本身完成所有事情。

你可安全使用 :c:func:`k_work_is_pending` 的罕见情况是作为避免调用 :c:func:`k_work_flush` 或 :c:func:`k_work_cancel_sync` 的检查，如果你*确定*在你检查时没有其他东西可能提交工作（通常因为你持有防止访问用于提交的状态的锁）。

建议用法
**************

使用系统工作队列将复杂中断相关处理从 ISR 延迟到共享线程。这允许中断相关处理及时完成（不损害系统响应后续中断的能力）且不需要应用定义和管理额外线程做处理。

配置选项
**********************

相关配置选项：

* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`

* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_PRIORITY`

* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_NO_YIELD`

API 参考
**************

.. doxygengroup:: workqueue_apis









































