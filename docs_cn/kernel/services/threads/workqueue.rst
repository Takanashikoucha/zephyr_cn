.. _workqueues_v2:

工作队列线程
#################

.. contents::
    :local:
    :depth: 1

:dfn:`工作队列`是一种内核对象，使用专用线程以先进先出方式
处理工作项。每个工作项通过调用工作项指定的
函数来处理。工作队列通常
由 ISR 或高优先级线程用于将非紧急处理
卸载到较低优先级线程，以便不影响时间敏感的处理。

可以定义任意数量的工作队列（仅受可用 RAM 限制）。每个
工作队列通过其内存地址引用。

工作队列具有以下关键属性：

* 一个**队列**，包含已添加但尚未处理的工作项。

* 一个处理队列中工作项的**线程**。该线程的
  优先级可配置，允许其根据需要
  为协同或抢占式。

无论工作队列线程优先级如何，工作队列线程
将在每个提交的工作项之间让出，
以防止协同工作队列使其他线程饥饿。

工作队列在使用前必须初始化。这将
其队列置为空并生成工作队列的线程。线程永远运行，
但没有可用工作项时睡眠。

工作项生命周期
********************

可以定义任意数量的**工作项**。每个工作项
通过其内存地址引用。

工作项被分配一个**处理函数**，即工作项
被处理时由工作队列线程
执行的函数。此函数接受单个参数，
即工作项本身的地址。工作项还
维护其状态信息。

工作项在使用前必须初始化。这将
记录工作项的处理函数并标记为
非挂起。

工作项可以由 ISR 或线程
通过将其提交到工作队列来**入队**（:c:enumerator:`K_WORK_QUEUED`）。
提交工作项将工作项
附加到工作队列的队列中。一旦工作队列线程
已处理其队列中所有前面的工作项，线程
将从队列中移除下一个工作
项并调用工作项的处理函数。根据
工作队列线程的调度优先级，以及
队列中其他项所需的工作量，已入队的工作项
可能快速处理，也可能
在队列中停留较长时间。

可延迟工作项可以被**调度**（:c:enumerator:`K_WORK_DELAYED`）到
工作队列；请参阅 `可延迟工作`_。

工作项在
工作队列上运行时为**运行中**（:c:enumerator:`K_WORK_RUNNING`），如果
在线程请求取消之前已开始运行，也可能
处于**取消中**（:c:enumerator:`K_WORK_CANCELING`）状态。

工作项可以处于多个状态；例如它可以：

* 在队列上运行；
* 被标记为取消中（因为线程使用了 :c:func:`k_work_cancel_sync()`
  等待工作项完成）；
* 被入队以在同一队列上再次运行；
* 被调度以提交到（可能不同的）队列

*同时处于所有状态*。处于这些状态中
任何状态的工作项都是**挂起**
（:c:func:`k_work_is_pending()`）或**忙**（:c:func:`k_work_busy_get()`）。

处理函数可以使用线程可用的任何内核 API。但是，
潜在阻塞的操作（例如获取信号量）必须
谨慎使用，因为工作队列
无法处理队列中后续的工作项
直到处理函数执行完毕。

传递给处理函数的单个参数在不需要时
可以忽略。如果处理函数需要关于
其将执行的工作的额外信息，工作项可以
嵌入在更大的数据
结构中。然后处理函数可以使用参数值
通过 :c:macro:`CONTAINER_OF` 计算
外围数据结构的地址，
从而获取其所需的额外信息。

工作项通常初始化一次，然后在需要
执行工作时提交到特定
工作队列。如果 ISR 或线程尝试
提交已入队的工作项，工作项不受影响；
工作项保持在
工作队列队列中的当前位置，
工作只执行一次。

处理函数被允许将其工作项参数
重新提交到工作队列，因为
此时工作项不再入队。
这允许处理程序分阶段执行工作，
而不会过度延迟
工作队列队列中其他工作项的处理。

.. important::
    挂起的工作项*不得*在
    工作队列线程处理该工作项之前被修改。
    这意味着工作项在忙时不得
    重新初始化。此外，工作项
    处理函数执行工作所需的任何额外信息
    不得在处理函数
    执行完毕之前被修改。

.. _k_delayable_work:

可延迟工作
**************

ISR 或线程可能需要调度一个
仅在指定时间段后才处理的工作项，
而不是立即处理。这可以通过
**调度**一个**可延迟工作项**
在未来时间提交到
工作队列来实现。

可延迟工作项包含一个标准工作项，但添加了
记录工作项应在何时何地提交的字段。

可延迟工作项以类似于标准工作项的方式
初始化和调度到工作队列，
但使用不同的内核 API。
发出调度请求时，内核启动一个超时机制，
在指定延迟经过后触发。超时发生后，
内核将工作项提交到指定工作队列，
在那里保持入队状态
直到按标准方式处理。

注意，用于可延迟工作的处理函数仍然接收
底层非可延迟工作结构的指针，
该结构从 :c:struct:`k_work_delayable` 公开不可访问。
要获取包含
可延迟工作对象的对象，使用此惯用法：

.. code-block:: c

   static void work_handler(struct k_work *work)
   {
           struct k_work_delayable *dwork = k_work_delayable_from_work(work);
           struct work_context *ctx = CONTAINER_OF(dwork, struct work_context,
	                                           timed_work);
           ...


触发式工作
**************

:c:func:`k_work_poll_submit` 接口根据**轮询事件**
（请参阅 :ref:`polling_v2`）调度触发式工作
项，在监控的资源变得可用
或轮询信号被触发，或
超时发生时调用用户定义的函数。
与 :c:func:`k_poll` 不同，触发式工作不需要
专用线程等待或主动轮询
轮询事件。

触发式工作项是一个标准工作项，具有
以下
添加的属性：

* 指向轮询事件数组的指针，该数组将
  触发工作项
  提交到工作队列

* 包含轮询事件的数组的大小。

触发式工作项以类似于标准工作项的方式
初始化和提交到工作队列，
但使用专门的内核 API。
发出提交请求时，内核开始
观察轮询事件指定的内核对象。一旦
至少一个被观察内核
对象的状态发生变化，工作项被提交到指定工作队列，
在那里保持入队状态
直到按标准方式处理。

.. important::
    触发式工作项以及引用的轮询事件数组
    必须有效且在整个触发式工作
    项生命周期（从提交到工作项
    执行或取消）期间不能被修改。

ISR 或线程可以**取消**其已提交的
触发式工作项，只要其仍在等待
轮询事件。在这种情况下，内核
停止等待关联的轮询事件，
指定的工作不执行。
否则无法执行取消。

系统工作队列
*****************

内核定义一个称为*系统工作队列*的工作队列，
可供任何需要工作队列支持的应用
或内核代码使用。
系统工作队列是可选的，只有当应用
使用它时才存在。

.. important::
    仅当无法向系统工作队列
    提交新工作项时才应定义额外的
    工作队列，因为每个新工作队列
    在内存占用上产生显著成本。
    如果其工作项无法与
    现有系统工作队列工作项共存
    且没有不可接受的影响，
    则可以证明新工作队列是合理的；
    例如，如果新工作项执行阻塞操作，
    会将其他系统工作队列处理
    延迟到不可接受的程度。

    另请注意：系统工作队列默认具有
    最低协同优先级。这意味着排空
    系统工作队列优先于
    *所有可抢占线程*。将系统工作队列的优先级
    配置为可抢占是有风险的，因为子系统和
    驱动程序可能隐式依赖
    工作项在协同上下文中执行。
    因此，较低优先级任务
    可能需要一个较低优先级的独立
    工作队列。

如何使用工作队列
*********************

定义和控制工作队列
====================================

工作队列使用 :c:struct:`k_work_q` 类型的变量定义。
工作队列通过定义其
线程使用的栈区域、初始化 :c:struct:`k_work_q`（将其
内存清零或调用 :c:func:`k_work_queue_init`），
然后调用
:c:func:`k_work_queue_start` 来初始化。栈区域必须
使用
:c:macro:`K_THREAD_STACK_DEFINE` 定义以确保
其在内存中正确设置。

以下代码定义并初始化一个工作队列：

.. code-block:: c

    #define MY_STACK_SIZE 512
    #define MY_PRIORITY 5

    K_THREAD_STACK_DEFINE(my_stack_area, MY_STACK_SIZE);

    struct k_work_q my_work_q;

    k_work_queue_init(&my_work_q);

    k_work_queue_start(&my_work_q, my_stack_area,
                       K_THREAD_STACK_SIZEOF(my_stack_area), MY_PRIORITY,
		       NULL);

此外，队列标识和与线程
重新调度相关的某些行为可以通过可选的
最后一个参数控制；详见
:c:func:`k_work_queue_start()`。

以下 API 可用于与工作队列交互：

* :c:func:`k_work_queue_drain()` 可用于阻塞调用者
  直到工作队列没有剩余项。
  工作队列线程重新提交的工作项
  在队列排空期间被接受，但
  来自任何其他线程或 ISR 的工作项
  被拒绝。
  提交更多工作的限制可以
  扩展到排空操作完成之后，
  以允许阻塞线程在队列"堵塞"期间
  执行额外工作。
  注意排空队列对调度或
  可延迟项的处理没有影响，但如果队列
  被堵塞且截止时间到期，
  该工作项将静默地提交失败。
* :c:func:`k_work_queue_unplug()` 移除
  之前排空操作导致的
  对队列提交的任何阻塞。

提交工作项
=====================

工作项使用 :c:struct:`k_work` 类型的变量定义。
必须
通过调用 :c:func:`k_work_init` 初始化，
除非使用 :c:macro:`K_WORK_DEFINE` 定义，
在这种情况下初始化在
编译时执行。

已初始化的工作项可以通过
调用 :c:func:`k_work_submit` 提交到系统工作队列，
或
通过调用 :c:func:`k_work_submit_to_queue` 提交到指定工作队列。

以下代码演示 ISR 如何将
错误消息的打印
卸载到系统工作队列。注意如果 ISR 尝试
在工作项仍入队时重新提交
该工作项，工作项保持不变，
关联的错误消息将不会打印。

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


以下 API 可用于检查工作项状态
或与之同步：

* :c:func:`k_work_busy_get()` 返回指示工作项
  状态的标志快照。
  零值表示工作未调度、未提交、未
  执行，或
  未被工作队列基础设施
  以其他方式引用。
* :c:func:`k_work_is_pending()` 是一个辅助函数，仅当
  工作被调度、入队或运行中时
  指示 ``true``。
* :c:func:`k_work_flush()` 可以从线程调用
  以阻塞直到工作
  项完成。如果工作未挂起则
  立即返回。
* :c:func:`k_work_cancel()` 尝试阻止
  工作项被
  执行。这可能成功也可能不成功。
  从 ISR 调用是安全的。
* :c:func:`k_work_cancel_sync()` 可以从线程调用
  以阻塞直到工作完成；
  如果取消成功或
  不需要（工作未提交或运行中）则
  立即返回。
  这可以在 :c:func:`k_work_cancel()`
  （从 ISR）调用后使用，
  以确认 ISR 发起的取消完成。

调度可延迟工作项
================================

可延迟工作项使用
:c:struct:`k_work_delayable` 类型的变量定义。
必须通过调用
:c:func:`k_work_init_delayable` 初始化。

对于延迟工作，有两种常见用例，
取决于如果新事件发生
截止时间是否应延长。
例如收集
异步到来的数据，例如
来自与键盘关联的 UART 的字符。
有两个 API 在延迟后提交工作：

* :c:func:`k_work_schedule()`（或 :c:func:`k_work_schedule_for_queue()`）
  调度工作以在特定时间或延迟后执行。
  在延迟完成前
  使用此 API 进一步
  调度同一工作项的尝试
  不会更改工作项
  被提交到其队列的时间。
  如果策略是
  持续收集数据
  直到自**第一个**未处理数据
  接收后指定延迟，
  则使用此 API；
* :c:func:`k_work_reschedule()`（或 :c:func:`k_work_reschedule_for_queue()`）
  无条件地设置工作的截止时间，
  替换任何之前
  未完成的延迟，
  必要时更改目标队列。
  如果策略是
  持续收集数据
  直到自**最后一个**未处理数据
  接收后指定延迟，
  则使用此 API。

如果工作项未被调度，两个 API 行为相同。
如果
指定 :c:macro:`K_NO_WAIT` 作为延迟，
行为等同于工作项
被立即直接提交到
目标队列，
无需等待
最小超时（除非使用 :c:func:`k_work_schedule()`
且之前的
延迟尚未完成）。

两者还有允许
控制用于提交的工作队列的变体。

辅助函数 :c:func:`k_work_delayable_from_work()` 可用于
从传递给工作处理函数
的 :c:struct:`k_work` 指针
获取指向包含
:c:struct:`k_work_delayable` 的指针。

以下额外 API 可用于检查工作项状态
或与之同步：

* :c:func:`k_work_delayable_busy_get()` 是可延迟
  工作对应的 :c:func:`k_work_busy_get()`
  等效函数。
* :c:func:`k_work_delayable_is_pending()` 是可延迟
  工作对应的
  :c:func:`k_work_is_pending()` 等效函数。
* :c:func:`k_work_flush_delayable()` 是可延迟
  工作对应的 :c:func:`k_work_flush()`
  等效函数。
* :c:func:`k_work_cancel_delayable()` 是可延迟
  工作对应的
  :c:func:`k_work_cancel()` 等效函数；
  :c:func:`k_work_cancel_delayable_sync()` 同理。

与工作项同步
=============================

虽然标准工作项和可延迟工作项的状态
都可以从任何上下文使用 :c:func:`k_work_busy_get()` 和
:c:func:`k_work_delayable_busy_get()` 确定，
但某些用例需要在
工作项提交后与之同步。
:c:func:`k_work_flush()`、
:c:func:`k_work_cancel_sync()` 和 :c:func:`k_work_cancel_delayable_sync()`
可以从线程上下文调用
以等待达到请求的状态。

这些 API 必须提供一个 :c:struct:`k_work_sync` 对象，
该对象没有应用可检查的组件，
但需要提供
同步对象。如果代码预期在
具有
:kconfig:option:`CONFIG_KERNEL_COHERENCE` 的架构上工作，
则不应在栈上分配这些对象。

工作队列最佳实践
************************

避免竞态条件
=====================

有时工作项必须处理的数据
自然是线程安全的，
例如当它被某个线程放入 :c:struct:`k_queue`
并在
工作线程中处理时。
更常见的是，
需要外部同步
来避免
数据竞态：
即工作线程可能检查或操作
被另一个线程或中断
访问的共享状态的情况。
这样的状态
可能是指示需要执行工作的标志，
或
由 ISR 或线程填充并由
工作处理程序读取的共享对象。

对于简单标志，:ref:`atomic_v2` 可能就足够了。
在其他情况下，
可以使用自旋
锁（:c:struct:`k_spinlock`）或线程感知锁（:c:struct:`k_sem`、
:c:struct:`k_mutex` 等）
来确保不发生数据竞态。

如果选定的锁机制可以 :ref:`api_term_sleep`，
那么允许
工作线程睡眠将使其他工作队列项
饥饿，
它们可能需要
推进
才能释放锁。
工作处理程序应
尝试通过其非等待路径
获取锁。
例如：

.. code-block:: c

   static void work_handler(struct work *work)
   {
           struct work_context *parent = CONTAINER_OF(work, struct work_context,
	                                              work_item);

           if (k_mutex_lock(&parent->lock, K_NO_WAIT) != 0) {
                   /* NB: Submit will fail if the work item is being cancelled. */
                   (void)k_work_submit(work);
		   return;
	   }

	   /* do stuff under lock */
	   k_mutex_unlock(&parent->lock);
	   /* do stuff without lock */
   }

注意，如果锁由优先级低于
工作队列的线程持有，
重新提交可能使
将释放锁的线程饥饿，
导致应用失败。
在需要上述惯用法的地方，
优先使用可延迟工作项，
工作应
以非零延迟
（重新）调度，
以允许
持有锁的线程推进。

注意，如果工作项已被
取消，
从工作处理程序提交可能失败。
通常这是可接受的，
因为取消将在
处理程序完成后完成。
如果不可接受，
上述代码必须
采取其他步骤
通知应用
工作未能执行。

单独的工作项是自锁的，
因此
你不需要持有外部锁
仅为了提交或调度它们。
即使你使用
由这样的锁保护的外部状态
来防止进一步重新提交，
只要你
确定
最终工作项将获取其锁
并检查
该状态以确定是否应执行任何操作，
执行
重新提交就是安全的。
在
可延迟工作项因
无法
获取锁
而
在其处理程序中
被重新调度的情况下，
需要
某些
其他自锁状态，
例如
应用/驱动
在
发起
取消时
设置的
原子标志，
用于
检测
取消并
避免
被取消的
工作项
在
截止时间
后
再次
被提交。

检查返回值
==================

所有工作 API 函数返回底层操作的状态，
在许多
情况下，
验证
获得
预期
结果
非常重要。

* 提交工作项（:c:func:`k_work_submit_to_queue`）
  可能
  失败，
  如果
  工作
  正在
  被
  取消
  或
  队列
  不
  接受
  新
  项。
  如果
  发生
  这种情况，
  工作
  将
  不
  被
  执行，
  这
  可能
  导致
  由
  工作
  处理程序
  活动
  驱动
  的
  子系统
  变得
  无
  响应。
* 异步
  取消
  （:c:func:`k_work_cancel`
  或
  :c:func:`k_work_cancel_delayable`）
  可能
  在
  工作
  项
  仍
  在
  被
  处理程序
  运行
  时
  完成。
  继续
  操作
  与
  工作
  处理程序
  共享
  的
  状态
  将
  导致
  数据
  竞态，
  可能
  导致
  故障。

Zephyr 代码中
许多
竞态
条件
一直
存在，
因为
未
检查
操作
的
结果。

可能有
充分
理由
相信
指示
操作
未
按
预期
完成
的
返回值
不
是
问题。
在
那些
情况下，
代码
应
清楚
地
记录
这一点，
通过
（1）
将
返回值
转换
为
``void``
以
指示
结果
被
有意
忽略，
（2）
记录
在
意外
情况下
发生
什么。
例如：

.. code-block:: c

   /* If this fails, the work handler will check pub->active and
    * exit without transmitting.
    */
   (void)k_work_cancel_delayable(&pub->timer);

然而
在
这样的
情况下，
以下
代码
仍
必须
避免
数据
竞态，
因为
它
无法
保证
工作
线程
不
在
访问
工作
相关
状态。

不要
过早
优化
==========================

工作队列
API
被
设计
为
从
多个
线程
和
中断
调用
时
安全。
尝试
外部
检查
工作
项
状态
并
基于
结果
做出
决策
很可能
创建
新
问题。

因此
当
新
工作
到来
时，
直接
提交
即可。
不要
尝试
通过
使用
:c:func:`k_work_is_pending`
或
:c:func:`k_work_busy_get`
检查
快照
状态
来
"优化"
检查
工作
项
是否
已
被
提交，
或
检查
:c:func:`k_work_delayable_remaining_get()`
的
非零
延迟。
这些
检查
是
脆弱的：
"忙"
指示
在
测试
返回
时
可能
已
过时，
"不忙"
指示
在
工作
从
多个
上下文
提交
时
也
可能
错误，
或
（对于
可
延迟
工作）
如果
截止
时间
已
完成
但
工作
仍
在
入队
或
运行
状态。

一般
最佳
实践
是
始终
在
共享
状态
中
维护
某个
条件，
处理程序
可以
检查
以
确认
是否
有
工作
需要
执行。
这样
你可以
将
工作
处理程序
用作
标准
清理
路径：
而
不
是
必须
在
工作
项
被
提交
的
位置
处理
取消
和
清理，
你
可能
能够
在
工作
处理程序
本身
中
完成
所有
操作。

可以
安全
使用
:c:func:`k_work_is_pending`
的
罕见
情况
是
作为
检查
以
避免
调用
:c:func:`k_work_flush`
或
:c:func:`k_work_cancel_sync`，
前提
是你
*确定*
在
你
检查
期间
没有
其他
东西
可能
提交
工作
（通常
因为
你
持有
一个
阻止
访问
用于
提交
的状态
的
锁）。

建议
用途
**************

使用
系统
工作
队列
将
复杂
的
中断
相关
处理
从
ISR
延迟
到
共享
线程。
这
允许
中断
相关
处理
及时
完成，
同时
不
损害
系统
响应
后续
中断
的
能力，
且
不
需要
应用
定义
和
管理
额外
线程
来
执行
处理。

配置
选项
**********************

相关
配置
选项：

* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_PRIORITY`
* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_NO_YIELD`

API
参考
**************

.. doxygengroup:: workqueue_apis
