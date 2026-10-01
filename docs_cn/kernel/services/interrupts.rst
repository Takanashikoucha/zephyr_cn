.. _interrupts_v2:

中断
##########

:dfn:`中断服务程序`（ISR）是一个响应硬件或软件中断而异步执行的函数。ISR 通常会抢占当前线程的执行，使响应能够以极低的延迟发生。只有当所有 ISR 工作完成后，线程执行才会恢复。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的 ISR（仅受可用 RAM 限制），前提是受底层硬件施加的约束。

ISR 具有以下关键属性：

* 一个触发 ISR 的**中断请求（IRQ）信号**。
* 与该 IRQ 关联的**优先级级别**。
* 一个被调用以处理中断的**中断服务程序**。
* 一个传递给该函数的**参数值**。

:abbr:`IDT (中断描述符表)` 或向量表用于将特定的中断源与特定的 ISR 关联。在任何给定时刻，只能有一个 ISR 与特定 IRQ 关联。

多个 ISR 可以使用同一个函数来处理中断，允许单个函数服务一个产生多种类型中断的设备，或服务于多个设备（通常为同一类型）。传递给 ISR 函数的参数值使该函数能够判断哪个中断被触发。

内核为所有未使用的 IDT 条目提供默认 ISR。如果触发了意外的中断，该 ISR 将生成致命系统错误。

内核支持**中断嵌套**。如果触发了更高优先级的中断，ISR 可以在执行过程中被抢占。较低优先级的 ISR 在较高优先级 ISR 完成处理后恢复执行。

ISR 在内核的**中断上下文**中执行。该上下文拥有自己专用的栈区域（或在某些架构上有多个栈区域）。中断上下文栈的大小必须能够处理多个并发 ISR 的执行（如果启用了中断嵌套支持）。

.. important::
    许多内核 API 只能被线程使用，而不能被 ISR 使用。在例程可能同时被线程和 ISR 调用的情况下，内核提供 :c:func:`k_is_in_isr` API，允许例程根据其是作为线程的一部分还是作为 ISR 的一部分执行来改变其行为。

.. _multi_level_interrupts:

多级中断处理
==============================

硬件平台可以通过使用一个或多个嵌套中断控制器来支持比原生提供的更多的中断线。硬件中断源被合并到一条中断线，然后路由到父控制器。

如果支持嵌套中断控制器，应启用 :kconfig:option:`CONFIG_MULTI_LEVEL_INTERRUPTS`，并根据硬件架构配置 :kconfig:option:`CONFIG_2ND_LEVEL_INTERRUPTS` 和 :kconfig:option:`CONFIG_3RD_LEVEL_INTERRUPTS`。

为每个硬件中断分配一个唯一的 32 位中断号，其中嵌入用于选择和调用正确中断服务程序（ISR）的信息。每个中断级别在该 32 位号中占用一个字节，使用该架构最多支持四个中断级别，如下图所示并说明：

.. code-block:: none

              9                           2       0
    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │   │   │ ╷ │   │   │   │   │ A │   │ ╷ │   │   │               (LEVEL 1)
    └───┴───┴─│─┴───┴───┴───┴───┴───┴───┴─│─┴───┴───┘
              └─────────────────┐         └─────────────────────┐
          5                     v                               v
    ┌───┬───┬───┬───┬───┬───┬───┐   ┌───┬───┬───┬───┬───┬───┬───┐
    │   │ ╷ │   │ C │   │   │   │   │   │   │   │   │ B │   │   │   (LEVEL 2)
    └───┴─│─┴───┴───┴───┴───┴───┘   └───┴───┴───┴───┴───┴───┴───┘
          └─────────────────────┐
                                v
    ┌───┬───┬───┬───┬───┬───┬───┐
    │   │   │   │   │ D │   │   │                                   (LEVEL 3)
    └───┴───┴───┴───┴───┴───┴───┘

这里展示了三个中断级别。

* 一个单元格代表一条中断线，编号从 0（最右侧）开始。
* LEVEL 1 有 12 条中断线，其中两条线（2 和 9）连接到嵌套控制器，第 4 线上有一个设备 'A'。
* 一个 LEVEL 2 控制器的中断线 5 连接到一个 LEVEL 3 嵌套控制器，第 3 线上有一个设备 'C'。
* 另一个 LEVEL 2 控制器没有嵌套控制器，但第 2 线上有一个设备 'B'。
* LEVEL 3 控制器的第 2 线上有一个设备 'D'。

以下是如何为每个硬件中断生成唯一中断号。让我们考虑上面显示的四个中断 A、B、C 和 D：

.. code-block:: none

   A -> 0x00000004
   B -> 0x00000302
   C -> 0x00000409
   D -> 0x00030609

.. note::
   LEVEL 2 及更高级别的位位置偏移 1，因为 0 表示该级别不存在中断号。在我们的示例中，LEVEL 3 控制器的设备 D 在第 2 线上，连接到 LEVEL 2 控制器的第 5 线，该线又连接到 LEVEL 1 控制器的第 9 线（2 -> 5 -> 9）。由于 LEVEL 2 及更高级别的编码偏移，设备 D 被分配编号 0x00030609。

防止中断
=========================

在某些情况下，当前线程可能需要防止 ISR 在其执行时间敏感或关键区段操作期间执行。

线程可以使用 **IRQ 锁**临时阻止系统中的所有 IRQ 处理。即使该锁已生效，也可以再次施加该锁，因此例程可以在不知道其是否已生效的情况下使用它。在线程运行期间，内核要再次处理中断之前，线程必须与加锁次数相同地解锁其 IRQ 锁。

.. important::
    线程在持有 IRQ 锁时不允许 :ref:`睡眠 <thread_sleeping>`；只能调用 :ref:`isr-ok <api_term_isr-ok>` 函数。

或者，线程可以临时**禁用**指定 IRQ，使关联的 ISR 在该 IRQ 被触发时不执行。之后必须**启用**该 IRQ 以允许 ISR 执行。

.. important::
    禁用 IRQ 会阻止系统中*所有*线程被关联 ISR 抢占，而不仅仅是禁用了该 IRQ 的线程。

.. _zlis:

零延迟中断
-----------------------

通过施加 IRQ 锁来防止中断可能会增加观测到的中断延迟。然而，较高的中断延迟对于某些低延迟用例可能不可接受。

内核通过允许具有关键延迟约束的中断在无法被中断锁阻止的优先级级别上执行来处理此类用例。

这些中断被定义为*零延迟中断*。

零延迟中断的支持需要启用 :kconfig:option:`CONFIG_ZERO_LATENCY_IRQS`。

配置为零延迟的任何中断还必须声明为 :ref:`直接 ISR <direct_isrs>`（且不得使用 :c:macro:`ISR_DIRECT_PM`），因为常规 ISR 与内核交互。

此外，必须将标志 :c:macro:`IRQ_ZERO_LATENCY` 传递给 :c:macro:`IRQ_DIRECT_CONNECT` 宏，以将特定中断配置为零延迟。

在某些架构上，可以将零延迟中断 ISR 声明为同时为直接和动态的，请参阅 :ref:`direct_isrs`。

零延迟中断预期用于直接管理硬件事件，而不是与内核代码交互。它们应将所有内核 API 视为未定义行为（即，在零延迟中断上下文中使用 API 的应用程序负责直接验证正确行为）。零延迟中断不得修改任何由从常规 Zephyr 上下文调用的内核 API 检查的数据，也不得生成需要同步处理的异常（例如内核 panic）。

当系统电源管理在 PM 恢复期间保持中断锁定时，零延迟中断在锁定-恢复顺序之外，可能在 PM 挂起/恢复逻辑期间被分派，早于 PM 恢复簿记和 SoC/设备硬件恢复完成。

此类 ISR 必须是 PM-唤醒安全的，或者在系统状态不允许 ISR 执行时，必须屏蔽或禁用该中断源。

请参阅 :ref:`设备电源策略约束 <pm-device-constraint>`，了解在可能产生零延迟中断的设备路径处于活动状态时，将不安全状态排除在策略选择之外的一种方式。

.. important::
    零延迟中断按架构特定方式支持。该功能当前在 ARM Cortex-M 架构变体中实现。

.. tip::
    为缓解 flash 访问延迟，考虑将 ISR 和所有相关符号重定位到 RAM。

卸载 ISR 工作
==================

ISR 应快速执行以确保系统运行可预测。如果需要耗时较长的处理，ISR 应将部分或全部处理卸载到线程，从而恢复内核响应其他中断的能力。

内核支持多种将中断相关处理卸载到线程的机制。

* ISR 可以使用内核对象（如 FIFO、LIFO 或信号量）通知辅助线程执行中断相关处理。
* ISR 可以指示系统工作队列线程执行一个工作项。（请参阅 :ref:`workqueues_v2`。）

当 ISR 将工作卸载到线程时，通常在 ISR 完成时有一次上下文切换到该线程，使中断相关处理几乎可以立即继续。然而，根据处理卸载的线程优先级，当前正在执行的协同线程或其他更高优先级的线程可能在处理卸载的线程被调度之前执行。

共享中断线
======================

在某些硬件平台中，不同的 IP 可能使用相同的中断线。例如，中断 17 可能被 DMA 控制器使用来通知数据传输已完成，或被 DAI 控制器用来通知传输 FIFO 已达到水位线。要实现这一点，要么采用一些特殊逻辑，要么寻找变通方案（例如，使用 shared_irq 中断控制器），但这扩展性不太好。

为了解决这个问题，可以使用共享中断，通过 :kconfig:option:`CONFIG_SHARED_INTERRUPTS` 启用。

每当尝试在同一中断线上注册第二个 ISR/参数对时（使用 :c:macro:`IRQ_CONNECT` 或 :c:func:`irq_connect_dynamic`），该中断线将变为共享，意味着两个 ISR/参数对（之前注册的和刚刚注册的）将在每次中断触发时被调用。

在共享中断上下文中使用中断线的实体称为客户端。

一个中断允许的最大客户端数量由 :kconfig:option:`CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS` 控制。

中断共享对用户是透明的。因此，用户可以像往常一样使用 :c:macro:`IRQ_CONNECT` 和 :c:func:`irq_connect_dynamic` 注册中断。中断共享在幕后自动处理。

启用共享中断支持和动态中断支持后，用户可以动态断开 ISR，使用 :c:func:`irq_disconnect_dynamic`。ISR 断开后，每当其注册的中断线被触发时，该 ISR 将不再被调用。

请注意，启用 :kconfig:option:`CONFIG_SHARED_INTERRUPTS` 将导致二进制文件大小有不可忽视的增加。请谨慎使用。

实现
**************

定义常规 ISR
====================

ISR 在运行时通过调用 :c:macro:`IRQ_CONNECT` 定义。之后必须通过调用 :c:func:`irq_enable` 启用。

.. note::
    无前缀的中断控制 API（如 :c:func:`irq_enable` 和 :c:func:`irq_lock`）是旧拼写。新代码应使用其命名空间等效形式，如 :c:func:`k_irq_enable`、:c:func:`k_irq_lock` 等。无前缀的名称仍完全支持。

.. important::
    IRQ_CONNECT() 不是 C 函数，在幕后执行一些内联汇编操作。其所有参数必须在构建时已知。有多个实例的驱动程序可能需要定义每实例配置函数来配置每个中断实例。

以下代码定义并启用一个 ISR。

.. code-block:: c

    #define MY_DEV_IRQ  24       /* device uses IRQ 24 */
    #define MY_DEV_PRIO  2       /* device uses interrupt priority 2 */
    /* argument passed to my_isr(), in this case a pointer to the device */
    #define MY_ISR_ARG  DEVICE_GET(my_device)
    #define MY_IRQ_FLAGS 0       /* IRQ flags */

    void my_isr(void *arg)
    {
       ... /* ISR code */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_ISR_ARG, MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

由于 :c:macro:`IRQ_CONNECT` 宏要求所有参数在构建时已知，在某些情况下这可能不可接受。也可以使用 :c:func:`irq_connect_dynamic` 在运行时安装中断。其用法与 :c:macro:`IRQ_CONNECT` 完全相同：

.. code-block:: c

    void my_isr_installer(void)
    {
       ...
       irq_connect_dynamic(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_ISR_ARG,
                           MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

动态中断需要启用 :kconfig:option:`CONFIG_DYNAMIC_INTERRUPTS` 选项。目前不支持移除或重新配置动态中断。

.. _direct_isrs:

定义'直接' ISR
=====================

常规 Zephyr 中断引入一些开销，对于某些低延迟用例可能不可接受。具体包括：

* ISR 的参数被检索并传递给 ISR
* 如果启用了电源管理且系统处于空闲状态，在执行 ISR 之前所有硬件都将从低功耗状态恢复，这可能非常耗时
* 虽然某些架构在硬件中完成此操作，但其他架构需要在代码中切换到中断栈
* 中断服务完成后，操作系统执行一些逻辑以潜在地做出调度决策
* :ref:`zlis` 必须始终声明为直接 ISR，因为常规 ISR 与内核交互

Zephyr 支持所谓的'直接'中断，通过 :c:macro:`IRQ_DIRECT_CONNECT` 安装，其处理程序使用 :c:macro:`ISR_DIRECT_DECLARE` 声明。这些直接中断有一些特殊实现要求和缩减的功能集；详见 :c:macro:`IRQ_DIRECT_CONNECT` 和 :c:macro:`ISR_DIRECT_DECLARE` 的定义。

直接中断仅在选择了 :kconfig:option:`CONFIG_ARCH_HAS_DIRECT_INTERRUPTS` 的架构上可用。在其他架构上使用 :c:macro:`IRQ_DIRECT_CONNECT` 或 :c:macro:`ISR_DIRECT_DECLARE` 将导致构建失败。

以下代码演示了一个直接 ISR：

.. code-block:: c

    #define MY_DEV_IRQ  24       /* device uses IRQ 24 */
    #define MY_DEV_PRIO  2       /* device uses interrupt priority 2 */
    #define MY_IRQ_FLAGS 0       /* IRQ flags */

    ISR_DIRECT_DECLARE(my_isr)
    {
       do_stuff();
       /* PM done after servicing interrupt for best latency. This cannot be
       used for zero-latency IRQs because it accesses kernel data. */
       ISR_DIRECT_PM();
       /* Ask the kernel to check if scheduling decision should be made. If the
       ISR is for a zero-latency IRQ then the return value must always be 0. */
       return 1;
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_DIRECT_CONNECT(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

动态直接中断的安装按架构特定方式支持。该功能当前在 Arm Cortex-M 架构变体中通过宏 :c:macro:`ARM_IRQ_DIRECT_DYNAMIC_CONNECT` 实现，可用于声明直接且动态的中断。

基于 RAM 的 ISR 执行
======================

为了超低延迟，可以将 ISR 和向量表重定位到 RAM 以消除 flash 访问延迟。

可以通过启用 :kconfig:option:`CONFIG_SRAM_VECTOR_TABLE` 和 :kconfig:option:`CONFIG_SRAM_SW_ISR_TABLE` 选项实现，这将使向量表放置在 RAM 中。

然后，可以使用 Zephyr :ref:`代码和数据重定位 <code_data_relocation>` 将 ISR 代码和所有相关符号也重定位到 RAM。

共享中断线
=========================

以下代码使用相同的中断号定义两个 ISR。

.. code-block:: c

    #define MY_DEV_IRQ 24		/* device uses INTID 24 */
    #define MY_DEV_IRQ_PRIO 2		/* device uses interrupt priority 2 */
    /*  this argument may be anything */
    #define MY_FST_ISR_ARG INT_TO_POINTER(1)
    /*  this argument may be anything */
    #define MY_SND_ISR_ARG INT_TO_POINTER(2)
    #define MY_IRQ_FLAGS 0		/* IRQ flags */

    void my_first_isr(void *arg)
    {
       ... /* some magic happens here */
    }

    void my_second_isr(void *arg)
    {
       ... /* even more magic happens here */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_second_isr, MY_SND_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

`定义常规 ISR`_ 中描述的关于 :c:macro:`IRQ_CONNECT` 的相同限制在此同样适用。如果禁用了 :kconfig:option:`CONFIG_SHARED_INTERRUPTS`，上述代码将生成构建错误。否则，上述代码将导致两个 ISR 在每次中断 24 被触发时被调用。

如果 :kconfig:option:`CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS` 设置为低于 2（当前客户端数量）的值，将生成构建错误。

如果启用了动态中断，:c:func:`irq_connect_dynamic` 将允许在运行时共享中断。超出配置的最大允许客户端数量将导致断言失败。

动态断开 ISR
================================

以下代码使用相同的中断号定义两个 ISR。第二个 ISR 在运行时被断开。

.. code-block:: c

    #define MY_DEV_IRQ 24		/* device uses INTID 24 */
    #define MY_DEV_IRQ_PRIO 2		/* device uses interrupt priority 2 */
    /*  this argument may be anything */
    #define MY_FST_ISR_ARG INT_TO_POINTER(1)
    /*  this argument may be anything */
    #define MY_SND_ISR_ARG INT_TO_POINTER(2)
    #define MY_IRQ_FLAGS 0		/* IRQ flags */

    void my_first_isr(void *arg)
    {
       ... /* some magic happens here */
    }

    void my_second_isr(void *arg)
    {
       ... /* even more magic happens here */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_second_isr, MY_SND_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

    void my_isr_uninstaller(void)
    {
       ...
       irq_disconnect_dynamic(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

:c:func:`irq_disconnect_dynamic` 调用将使中断 24 变为非共享，意味着系统将表现得好像第一个 :c:macro:`IRQ_CONNECT` 调用从未发生过。此行为仅在启用 :kconfig:option:`CONFIG_DYNAMIC_INTERRUPTS` 时允许，否则将生成链接器错误。

实现细节
=====================

中断表在构建时通过一些特殊构建工具设置。这里列出的细节适用于除 x86 之外的所有架构，x86 在下面的 `x86 细节`_ 部分中介绍。

调用 :c:macro:`IRQ_CONNECT` 将声明一个 struct _isr_list 实例，放置在特殊的 .intList 段中。该段仅在预编译阶段放置在编译代码中。它供 Zephyr 脚本生成中断表使用，并在最终构建中移除。该脚本实现不同的解析器来处理 .intList 段中的数据并生成所需的输出。

默认解析器生成 C 数组，其中填充参数和中断处理程序，以地址形式直接从 .intList 段条目中获取。它适用于所有架构和编译器（除上述例外）。该解析器的限制在于数组生成后代码不应再重定位。此阶段的任何重定位都可能导致中断数组中的条目不再指向预期的函数。这意味着该解析器虽然兼容性更好，但限制了使用链接时优化。

本地 ISR 声明解析器使用不同的方法在二进制层面构建相同的数组。

所有数组条目都在本地声明和定义，直接在使用 :c:macro:`IRQ_CONNECT` 的文件中。

它们放置在具有唯一合成名称的段中。

该段的名称随后放置在 .intList 段中，用于生成链接器脚本片段，将条目放置在正确地址。

该解析器目前限于受支持的架构和工具链，但作为回报，它保留了关于对象关系的信息供链接器使用，从而启用链接时优化。

使用 C 数组实现
-----------------------------

这是所有 Zephyr 支持架构的默认配置。

任何 :c:macro:`IRQ_CONNECT` 调用都将声明一个 struct _isr_list 实例，放置在特殊的 .intList 段中：

.. code-block:: c

    struct _isr_list {
        /** IRQ line number */
        int32_t irq;
        /** Flags for this IRQ, see ISR_FLAG_* definitions */
        int32_t flags;
        /** ISR to call */
        void *func;
        /** Parameter for non-direct IRQs */
        void *param;
    };

Zephyr 分两个阶段构建；构建的第一阶段产生 ``${ZEPHYR_PREBUILT_EXECUTABLE}``.elf，其中包含 .intList 段中的所有条目，前面有一个头：

.. code-block:: c

    struct {
        void *spurious_irq_handler;
        void *sw_irq_handler;
        uint32_t num_isrs;
        uint32_t num_vectors;
        struct _isr_list isrs[];  <- of size num_isrs
    };

``${ZEPHYR_PREBUILT_EXECUTABLE}``.elf 中由头和 struct _isr_list 实例组成的数据随后由 gen_isr_tables.py 脚本使用，生成一个 C 文件，定义向量表和软件 ISR 表，然后编译并链接到最终应用程序中。

任何中断的优先级级别不编码在这些表中，而是 :c:macro:`IRQ_CONNECT` 还有一个运行时组件，将中断所需的优先级级别编程到中断控制器。某些架构不支持中断优先级的概念，在这种情况下优先级参数被忽略。

向量表
~~~~~~~~~~~~
当启用 :kconfig:option:`CONFIG_GEN_IRQ_VECTOR_TABLE` 时生成向量表。该数据结构由 CPU 原生使用，简单地是一个函数指针数组，其中每个元素 n 对应 IRQ 线 n 的 IRQ 处理程序，函数指针为：

#. 对于使用 :c:macro:`IRQ_DIRECT_CONNECT` 声明的'直接'中断，处理程序函数将放置在此处。
#. 对于使用 :c:macro:`IRQ_CONNECT` 声明的常规中断，通用软件 IRQ 处理程序的地址放置在此处。此代码执行通用内核中断簿记，并从软件 ISR 表中查找 ISR 和参数。
#. 对于完全未配置的中断线，虚假 IRQ 处理程序的地址将放置在此处。虚假 IRQ 处理程序在遇到时导致系统致命错误。

某些架构对所有中断有公共入口点，不支持向量表，在这种情况下应禁用 :kconfig:option:`CONFIG_GEN_IRQ_VECTOR_TABLE` 选项。

某些架构可能为系统异常保留一些初始向量，并在别处的表中声明，在这种情况下需要将 CONFIG_GEN_IRQ_START_VECTOR 设置为正确偏移表中的索引。

软件 ISR 表
~~~~~~~~~~~~
这是一个 struct _isr_table_entry 数组：

.. code-block:: c

    struct _isr_table_entry {
        void *arg;
        void (*isr)(void *);
    };

通用软件 IRQ 处理程序使用此表查找 ISR 及其参数并执行它。活动的 IRQ 线在中断控制器寄存器中查找，用于索引此表。

共享软件 ISR 表
~~~~~~~~~~~~~~~~~~~

这是一个 struct z_shared_isr_table_entry 数组：

.. code-block:: c

    struct z_shared_isr_table_entry {
        struct _isr_table_entry clients[CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS];
        size_t client_num;
    };

此表跟踪每条中断线注册的客户端。每当中断线变为共享时，:c:func:`z_shared_isr` 将替换 _sw_isr_table 中当前注册的 ISR。此特殊 ISR 将遍历已注册客户端列表并调用各 ISR。

使用链接器脚本实现
----------------------------------

这种准备和解析 .isrList 段以实现中断向量数组的方式称为本地 ISR 声明。名称来源于所有创建中断向量的数组条目都在 :c:macro:`IRQ_CONNECT` 宏调用处本地创建的事实。然后使用自动生成的链接器脚本将其放置在内存中的正确位置。

此选项需要通过选择 :kconfig:option:`CONFIG_ISR_TABLES_LOCAL_DECLARATION` 启用。如果所用架构和工具链支持此配置，则设置 :kconfig:option:`CONFIG_ISR_TABLES_LOCAL_DECLARATION_SUPPORTED`。有关当前支持的配置信息，请参阅此选项的详情。

任何 :c:macro:`IRQ_CONNECT` 或 :c:macro:`IRQ_DIRECT_CONNECT` 调用都将声明一个 ``struct _isr_list_sname`` 实例，放置在特殊的 .intList 段中：

.. code-block:: c

    struct _isr_list_sname {
        /** IRQ line number */
        int32_t irq;
        /** Flags for this IRQ, see ISR_FLAG_* definitions */
        int32_t flags;
        /** The section name */
        const char sname[];
    };

注意段名放置在柔性数组成员中。这意味着初始化结构的大小将随结构名称长度变化。整个条目在应用程序构建期间由脚本使用，包含正确放置中断所需的所有信息。

除 _isr_list_sname 外，:c:macro:`IRQ_CONNECT` 宏还生成一个条目，该条目将成为中断数组的一部分：

.. code-block:: c

    struct _isr_table_entry {
        const void *arg;
        void (*isr)(const void *);
    };

此数组放置在名称保存在 _isr_list_sname 结构中的段中。

:c:macro:`IRQ_DIRECT_CONNECT` 宏创建的值取决于架构。它可以更改为指向中断处理程序的变量：

.. code-block:: c

    static uintptr_t <unique name> = ((uintptr_t)func);

或者实现跳转到中断处理程序的裸函数：

.. code-block:: c

    static void <unique name>(void)
    {
        __asm(ARCH_IRQ_VECTOR_JUMP_CODE(func));
    }

与 :c:macro:`IRQ_CONNECT` 类似，创建的变量或函数放置在 _isr_list_sname 段中保存的段中。

脚本生成的文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

中断表生成脚本创建 3 个文件：:file:`isr_tables.c`、:file:`isr_tables_swi.ld` 和 :file:`isr_tables_vt.ld`。

:file:`isr_tables.c` 将包含所有中断、直接中断和共享中断（如果启用）的结构。此文件仅实现应用程序未实现的所有结构，在找不到未在此处实现的中断处留下注释。

然后使用两个链接器文件。:file:`isr_tables_vt.ld` 文件包含在所选架构需要放置中断向量的位置。:file:`isr_tables_swi.ld` 文件描述软件中断表元素的放置。使用单独的文件是因为它可能放置在可写或不可写段中，取决于当前配置。

x86 细节
-----------

x86 架构有一种特殊类型的向量表，称为中断描述符表（IDT），必须按照 x86 处理器文档以特定方式布局。

它本质上仍是一个向量表，:ref:`gen_idt.py` 工具使用 .intList 段创建它。

然而，在基于 APIC 的系统中，向量表中的索引不对应 IRQ 线。

前 32 个向量保留给 CPU 异常，所有剩余向量（直到索引 255）对应优先级级别，每 16 个一组。

在此方案中，优先级级别 0 的中断将放置在向量 32-47，级别 1 48-63，依此类推。

当 :ref:`gen_idt.py` 工具构建 IDT 时，配置中断时将在请求优先级级别的适当范围内查找空闲向量并在那里设置处理程序。

在 x86 上，当 CPU 执行中断或异常向量时，没有万无一失的方法来确定哪个向量被触发，因此不使用以 IRQ 线为索引的软件 ISR 表。

相反，:c:macro:`IRQ_CONNECT` 调用创建一个小的汇编语言函数，该函数以 ISR 和参数为参数调用 :c:func:`_interrupt_enter` 中的通用中断代码。

是此汇编中断存根的地址被放置在 IDT 中。

对于使用 :c:macro:`IRQ_DIRECT_CONNECT` 声明的中断，无参数的 ISR 直接放置在 IDT 中。

在向量表中的位置对应中断优先级级别的系统中，中断控制器需要在运行时知道 IRQ 线关联的向量。:ref:`gen_idt.py` 额外创建一个 _irq_to_interrupt_vector 数组，将 IRQ 线映射到其在 IDT 中配置的向量。这在运行时由 :c:macro:`IRQ_CONNECT` 使用，用于在中断控制器中编程 IRQ 到向量的关联。

对于动态中断，构建必须生成一些 4 字节动态中断存根，每个使用的动态中断一个存根。存根数量由 :kconfig:option:`CONFIG_X86_DYNAMIC_IRQ_STUBS` 选项控制。每个存根压入一个唯一标识符，然后用于从表中获取相应的处理程序函数和参数，该表在动态中断连接时被填充。

超出默认支持的中断数量
-------------------------------------------------------

在多级配置中生成中断时，每级别 8 位是确定给定中断码属于哪个级别时使用的默认掩码。

当处理支持单个聚合器超过 255 个中断的 CPU 时，这可能成为问题。

在这种情况下，可能需要覆盖这些默认值并使用自定义的每级别位数。

无论每级使用多少位，所有级别使用的总位数之和必须小于或等于 32 位，以适应单个 32 位整数。

要修改每级总位数，在 :file:`Kconfig.multilevel` 中覆盖默认值 8，为第一级设置 :kconfig:option:`CONFIG_1ST_LEVEL_INTERRUPT_BITS`，为第二级设置 :kconfig:option:`CONFIG_2ND_LEVEL_INTERRUPT_BITS`，为第三级设置 :kconfig:option:`CONFIG_3RD_LEVEL_INTERRUPT_BITS`。

这些掩码控制位掩码长度以及生成中断值、检查中断级别和将中断转换为不同级别时应用的移位。

控制此逻辑的代码可在 :file:`irq_multilevel.h` 中找到。

建议用途
**************

使用常规或直接 ISR 执行需要非常快速响应且能快速完成而不阻塞的中断处理。

.. note::
    耗时的中断处理，或涉及阻塞的处理，应交给线程。请参阅 `卸载 ISR 工作`_ 了解应用程序中可用的各种技术描述。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_ISR_STACK_SIZE`

还存在额外的架构特定和设备特定配置选项。

API 参考
*************

.. doxygengroup:: isr_apis
