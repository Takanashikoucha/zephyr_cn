.. _architecture_porting_guide:

体系结构移植指南
##########################

当 Zephyr 需要运行在尚未支持的 :abbr:`ISA (指令集体系结构)` 或 :abbr:`ABI (应用二进制接口)` 上时，就需要进行体系结构移植。

以下是 Zephyr 支持的指令集体系结构和 ABI 示例：

* x86_32 指令集体系结构，配 System V ABI
* ARMv7-M 指令集体系结构，配 Thumb2 指令集和 ARM 嵌入式 ABI（aeabi）
* ARCv2 指令集体系结构

关于 Kconfig 配置的信息，参见 :ref:`setting_configuration_values`。体系结构使用的 Kconfig 配置方案与板卡类似。

体系结构移植可分为若干部分；大多数是必需的，某些是可选的：

* **早期启动序列**：每个体系结构在 CPU 从复位状态恢复时必须采取不同的步骤（必需）。

* **中断与异常处理**：每个体系结构以特定方式处理异步的、未被请求的事件（必需）。

* **线程上下文切换**：Zephyr 的上下文切换依赖于 ABI，每个指令集体系结构需要保存的寄存器集合各不相同（必需）。

* **线程创建与终止**：线程的初始栈帧取决于 ABI 和体系结构，线程中止（abort）可能也是如此（必需）。

* **设备驱动程序**：大多数情况下，系统时钟定时器与中断控制器和体系结构绑定（部分必需，部分可选）。

* **工具库**：某些常用内核 API 出于性能原因依赖于体系结构特定的实现（必需）。

* **CPU 空闲/电源管理**：大多数体系结构提供了让 CPU 进入睡眠的指令（部分可选，但很可能非常需要）。

* **故障管理**：用于实现体系结构特定的调试辅助以及线程中致命错误的处理（部分可选）。

* **链接器脚本与工具链**：构建系统与镜像链接时很可能需要体系结构特定的细节（必需）。

* **内存管理与内存映射**：用于支持内存管理与内存映射的体系结构特定细节。

* **栈对象**：用于栈对象相关的内存保护硬件的体系结构特定细节。

* **用户模式线程**：用于支持用户模式下的线程。

* **GDB 桩**：用于支持 GDB 桩以启用远程调试。

早期启动序列
*******************

早期启动序列的目标是将系统从复位后的状态带到可以运行 C 代码（从而运行通用内核初始化序列）的状态。大多数时候只需很少的步骤，而某些体系结构需要执行更多工作。

所有体系结构的通用步骤：

* 建立初始栈。
* 如果运行 :abbr:`XIP (eXecute-In-Place，就地执行)` 内核，将已初始化的数据从 ROM 复制到 RAM。
* 如果不使用 ELF 加载器，清零 BSS 段。
* 跳转到 :code:`z_cstart()`，即早期内核初始化

  * :code:`z_cstart()` 负责从启动时运行的假上下文
    切换出去，切换到主线程。

某些必须采取的体系结构特定步骤示例：

* 如果在 x86_32 上以实模式（real mode）获得控制权，切换到 32 位保护模式。
* 在 x86_32 上设置段寄存器，以处理将段寄存器留在未知或损坏状态的引导加载程序。
* 在 Cortex-M3/4 上初始化板卡特定的看门狗。
* 在 Cortex-M 上将栈从 MSP 切换到 PSP。
* 在 Cortex-M 上使用不同于调用 z_swap() 的方法，以防止竞态条件。
* 在 ARCv2 上设置 FIRQ 和常规 IRQ 处理。

早期启动序列钩子
=========================

Zephyr 暴露了若干钩子（描述于 :zephyr_file:`include/zephyr/platform/hooks.h`），允许在启动过程的精确时刻执行 SoC 或板卡特定的代码。

内核负责从与体系结构无关的代码中调用大多数钩子。然而，某些钩子必须在早期启动序列期间调用；由于该序列在体系结构特定的代码中实现，对钩子的调用也必须在那里完成。以下给出了早期启动序列的大致概述，以及体系结构特定代码应在何时调用钩子：

#. 执行从与体系结构特定的入口点开始，其名称与 :kconfig:option:`CONFIG_KERNEL_ENTRY` 匹配。

#. 体系结构特定状态立即被重新初始化（如果启用了 :kconfig:option:`CONFIG_INIT_ARCH_HW_AT_BOOT`）。

#. 调用 :c:func:`soc_early_reset_hook`。

   .. note::
    在调用此钩子之前无需建立有效的栈。
    但是，钩子在返回前允许覆盖栈指针。
    体系结构特定的代码不得期望 :c:func:`soc_early_reset_hook` 调用期间栈指针寄存器的值被保留。

    在具有多个栈指针的体系结构上，通常有一个可直接访问的*"主"*栈指针
    和若干*"次"*栈指针寄存器。
    :c:func:`soc_early_reset_hook` 的实现可以覆盖*"主"*栈指针，
    但**不得**读取或修改任何*"次"*栈指针的值。
    （这使得体系结构特定代码可以在调用 :c:func:`soc_early_reset_hook` 之前
    设置其想要的任何*"次"*栈指针）

    例如，ARM Cortex-A 体系结构定义了若干执行模式，
    每个都有自己的栈指针寄存器 :samp:`sp_{mode}`。
    当处理器在模式 :samp:`{X}` 中执行时，涉及 ``sp`` 通用寄存器的操作
    作用于 :samp:`sp_{X}`。
    在此体系结构上，假设调用 :c:func:`soc_early_reset_hook` 时
    处理器在模式 :samp:`{M}` 中执行，
    该钩子允许覆盖 :samp:`sp_{M}`（通过 ``sp`` 可访问），
    但**不得**读取或覆盖任何其他 :samp:`sp_{mode}`
    （其中 :samp:`{mode} != {M}`）。

    :c:func:`soc_early_reset_hook` 的实现允许不将执行返回到
    体系结构特定的代码，此时它们"接管"系统。
    此类钩子不受上述规则约束，可以读取或覆盖任何栈指针。
    但是，当提供此类实现时，早期启动序列的其余部分显然不会执行。

#. 为早期启动序列的后续步骤建立初始栈。

#. 执行体系结构特定的*"从休眠到 RAM（suspend-to-RAM）恢复"*逻辑

   .. note::
    参见 :kconfig:option:`CONFIG_PM_S2RAM` 和体系结构特定实现
    以获取更多细节，但注意：如果此逻辑判定正在退出
    休眠到 RAM 状态，则早期启动序列的其余部分不会执行。

#. 调用 :c:func:`soc_reset_hook`。

#. *在此执行体系结构特定的操作（汇编）...*

#. 调用 :c:func:`z_prep_c`。此体系结构特定函数用 C 实现。

#. :c:func:`z_prep_c` 立即调用 :c:func:`soc_prep_hook`。

#. *在此执行体系结构特定的操作（C）...*

#. 调用 :c:func:`z_cstart`。与体系结构无关的代码开始执行。

中断与异常处理
********************************

每个体系结构以不同方式定义中断与异常处理。

当设备想向处理器发出信号表示有工作要代其完成时，它触发一个中断。
当线程执行了软件串行流程本身不处理的操作时，它触发一个异常。
中断和异常都将控制权交给处理程序。
就中断而言，该处理程序称为 :abbr:`ISR (中断服务例程)`。
处理程序执行异常或中断所需的工作。
对于中断，该工作是设备特定的。
对于异常，取决于异常类型，
但大多数情况下由内核本身负责提供处理程序。

内核必须在处理程序自身执行的工作之外执行一些工作。例如：

* 在将控制权交给处理程序之前：

  * 保存当前正在执行的上下文。
  * 可能退出省电模式，
    包括唤醒设备。
  * 如果退出无滴答空闲模式，更新内核运行时间。

* 在从处理程序收回控制权之后：

  * 决定是否执行上下文切换。
  * 在执行上下文切换时，
    恢复被切换进来的上下文。

此工作在各体系结构间概念上相同，但细节完全不同：

* 要保存和恢复的寄存器。
* 执行工作的处理器指令。
* 异常的编号。
* 等等。

因此需要一个体系结构特定的实现，称为中断/异常桩（stub）。

另一个问题是内核将 ISR 的签名定义为：

.. code-block:: C

    void (*isr)(void *parameter)

各体系结构没有一致或原生的方式来处理 ISR 的参数。因此有两种常用的参数处理方法。

* 利用某种体系结构定义的机制，在桩中强制传入参数值。这在 X86 系体系结构中常见。

* 通过单独的表插入并跟踪 ISR 的参数，需要体系结构在运行时确定当前执行的是哪个中断。为真实中断向量表的所有条目安装一个通用的中断处理分发器（demuxer），然后从单独的表中获取设备的 ISR 和参数。此方法在 ARC 和 ARM 体系结构中通过 :kconfig:option:`CONFIG_GEN_ISR_TABLES` 实现中常见。可以通过查看 x86 的 :code:`_interrupt_enter()`、ARM 的 :code:`_isr_wrapper()`，或 :zephyr_file:`arch/arc/core/isr_wrapper.S` 中 ARC 的完整实现描述来找到桩的示例。

每个体系结构还必须实现中断控制原语：

* 锁定中断：:c:macro:`irq_lock()`、:c:macro:`irq_unlock()`。
* 注册中断：:c:macro:`IRQ_CONNECT()`。
* 如可能，编程设置优先级 :c:func:`irq_priority_set`。
* 启用/禁用中断：:c:macro:`irq_enable()`、:c:macro:`irq_disable()`。

.. note::

  :c:macro:`IRQ_CONNECT` 是一个利用汇编和/或链接器脚本技巧
  在构建时连接中断的宏，可节省启动时间和代码段大小。

向量表应包含针对每个可能发生的中断和异常的处理程序。
处理程序可以简单到一个自旋循环。
但我们强烈建议处理程序至少打印一些调试信息。
这些信息有助于弄清楚出了什么问题——
无论是遇到属于故障（fault）的异常（如除零或非法内存访问），
还是遇到非预期的中断（:dfn:`虚假中断`）。
参见 :zephyr_file:`arch/arm/core/cortex_m/fault.c` 中的 ARM 实现作为示例。

线程上下文切换
************************

多线程是拥有内核的基本目的。Zephyr 支持两种类型的线程：可抢占（preemptible）和协作（cooperative）。确定下一个要调度的线程的规则由内核处理。然而，上下文切换本身的方法由体系结构移植来实现。

Zephyr 提供两个互斥的上下文切换接口。
首选使用的接口是 :code:`arch_switch`，
在启用 :kconfig:option:`CONFIG_USE_SWITCH` 时选用。
替代接口是 :code:`arch_swap`——
在禁用 :kconfig:option:`CONFIG_USE_SWITCH` 时选用。
移植到新体系结构时只需实现其中一个；
但对于 SMP 平台，必须是 :code:`arch_switch`。

上下文切换可能在若干情况下发生：

* 当线程执行阻塞操作时，例如获取当前不可用的信号量。

* 当一个可抢占线程通过释放其阻塞的对象，解锁了更高优先级的线程。

* 当一个中断解锁了比当前执行线程更高优先级的线程，且当前执行线程是可抢占的。

* 当一个线程运行完毕。

* 当一个线程导致致命异常并被从运行线程中移除。例如引用了非法内存。

因此，上下文切换必须能够处理所有这些情况。

有两种类型的上下文切换：:dfn:`协作式`和 :dfn:`抢占式`。

* *协作式*上下文切换发生在线程自愿将控制权交给另一个线程时。有两种情况会发生

  * 当线程显式让出（yield）。
  * 当线程尝试获取当前不可用的对象
    并愿意等待该对象可用。

* *抢占式*上下文切换发生是因为一个 ISR 或线程触发了一个操作，该操作调度了比当前运行线程更高优先级的线程（前提是当前运行线程是可抢占的）。此类操作的一个示例是释放了更高优先级线程正在等待的对象。

.. note::

  当某个协作式线程是正在运行的线程时，永远不会从它手中夺走控制权。

协作式上下文切换总是通过线程调用内核内部例程 :code:`z_swap`（或其变体）来完成。
这进而调用 :code:`arch_switch` 或 :code:`arch_swap`（视情况而定）。
当这些被调用时，不会执行任何检查来判断上下文切换是否应该发生——
上下文切换必须发生。

.. note::

  在 32 位 x86 上，:code:`arch_swap` 足够通用且体系结构足够灵活，
  可以在退出中断时调用它来触发上下文切换。
  不应将此视为规则，因为 ARM Cortex-M 和 ARCv2 的移植都不这样做。

由于 :code:`z_swap` 是协作式的，ABI 中由调用方保存的寄存器已经在栈上。无需在 k_thread 结构中保存它们。

上下文切换也可以以抢占式执行。这发生在退出 ISR 时，在内核的中断退出桩中：

* x86 上处理程序调用后的 :code:`_interrupt_enter`。
* ARM 上的 :code:`z_arm_exc_exit` 和 :code:`z_arm_int_exit`。
* ARCv2 上的 :code:`_firq_exit` 和 :code:`_rirq_exit`。

调用上下文切换的决策逻辑很简单，仅在退出非嵌套中断时执行：

当启用 :kconfig:option:`CONFIG_USE_SWITCH` 时 ...

* 中断退出代码应调用 :c:func:`z_get_next_switch_handle`，并返回由返回的切换句柄（switch handle）标识的线程上下文

当未启用 :kconfig:option:`CONFIG_USE_SWITCH` 时 ...

* 中断退出代码应从就绪队列获取缓存的线程，并：

  * 如果缓存的线程不是当前线程，则调用上下文切换。
  * 否则不调用。

这很简单，但至关重要：如果未正确实现，内核将不按预期工作并出现奇怪的崩溃，大多由栈损坏引起。

线程创建与终止
*******************************

要启动新线程，必须构建一个栈帧，使上下文切换可以像弹出被切换出线程的栈帧一样弹出它。这要在体系结构特定的 :code:`_new_thread` 内部例程中实现。

线程入口点也不应被直接调用，
即不应将其设置为新线程的 :abbr:`PC (程序计数器)`。
相反，它必须用 :code:`_thread_entry` 包装。
这意味着栈帧中的 PC 应设置为 :code:`_thread_entry`，
线程入口点应作为第一个参数传递给 :code:`_thread_entry`。
具体细节取决于 ABI。

是否需要体系结构特定的线程终止实现取决于体系结构。存在一个通用实现，但它可能对某个体系结构不起作用。

遇到的一种需要体系结构特定线程终止实现的原因是：
中止线程的方式可能因中止原因不同而不同——是优雅退出还是异常。
ARM Cortex-M 就是这种情况：
如果线程触发了致命异常，CPU 必须被从处理程序模式（handler mode）中取出；
但如果线程优雅地退出了其入口点函数，则不需要。

这意味着要实现 :c:func:`k_thread_abort` 的体系结构特定版本，
并根据需要为该体系结构设置 Kconfig 选项
:kconfig:option:`CONFIG_ARCH_HAS_THREAD_ABORT`
（例如参见 :zephyr_file:`arch/arm/core/cortex_m/Kconfig`）。

线程本地存储
********************

要在新体系结构上启用线程本地存储（TLS）：

#. 实现 :c:func:`arch_tls_stack_setup`，在栈中建立 TLS 存储区域。参见工具链文档了解存储区域需要如何组织。可以使用某些辅助函数：

   * 函数 :c:func:`z_tls_data_size` 返回线程本地变量所需的尺寸（不包括工具链和体系结构所需的任何额外数据）。
   * 函数 :c:func:`z_tls_copy` 为线程本地变量准备 TLS 存储区域。它只复制变量本身，不处理体系结构和/或工具链特定的数据。

#. 在上下文切换时，获取新线程的 ``struct k_thread`` 中的 ``tls`` 字段，并将其放入适当的寄存器（或其他变量）中，以访问 TLS 存储区域。参见工具链和体系结构文档了解应使用哪些寄存器。
#. 在 Kconfig 中，向与新体系结构相关的 Kconfig 项添加 ``select ARCH_HAS_THREAD_LOCAL_STORAGE``。
#. 运行 ``tests/kernel/threads/tls`` 测试，确保新代码工作正常。

设备驱动程序
**************

内核只需要很少的硬件设备即可运行。
理论上，唯一必需的设备是中断控制器，
因为内核可以在没有系统时钟的情况下运行。
实际上，为了能够访问大部分（如果不是全部）健全性检查测试套件，
还需要系统时钟。
由于这两者通常与体系结构绑定，它们是体系结构移植的一部分。

中断控制器
=====================

不同体系结构之间的中断控制器和中断概念可能有显著差异。

例如，x86 有 :abbr:`IDT (中断描述符表)` 和不同中断控制器的概念。中断在 IDT 中的位置决定其优先级。

另一方面，ARM Cortex-M 将 :abbr:`NVIC (嵌套向量中断控制器)` 作为体系结构定义的一部分。无需独立于 NVIC 向量表的 IDT 类表。表中的位置与 IRQ 的优先级无关：优先级可按条目编程。

ARCv2 将其中断单元作为体系结构定义的一部分，与 NVIC 有些类似。
然而，ARC 将中断定义为异常编号与中断编号之间的一对一映射
（即异常 1 是 IRQ1，设备 IRQ 从 16 开始），
而 ARM 中 IRQ0 等价于异常 16
（奇怪的是，异常 1 可被视为 IRQ-15）。

所有这些差异意味着，就中断控制器而言，各体系结构之间几乎（如果有的话）无法共享任何东西。

系统时钟
=============

x86 将 APIC 定时器和 HPET 作为其体系结构定义的一部分。ARM Cortex-M 有 SYSTICK 异常。最后，ARCv2 有 timer0/1 设备。

内核超时在系统时钟定时器驱动程序的中断处理程序上下文中处理。


通过串口使用控制台
========================

还有另一个对体系结构移植几乎是必需的设备，因为它对调试非常有用。它是一个简单的轮询式、仅输出的串口驱动程序，用于发送控制台（:code:`printk`、:code:`printf`）输出。

它不是必需的，可以使用 RAM 控制台（:kconfig:option:`CONFIG_RAM_CONSOLE`）将所有输出发送到可由调试器读取的循环缓冲区。

工具库
*****************

内核依赖一些函数，这些函数可以用很少的指令或现代处理器中的无锁方式实现。因此预计它们作为体系结构移植的一部分来实现。

* 原子操作。

  * 如果某体系结构存在相应指令，
    实现通过 :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_ARCH`
    Kconfig 选项配置。

  * 如果某体系结构不存在相应指令，
    则存在一个通用版本，用 :c:func:`irq_lock` 或
    :c:func:`irq_unlock` 包装非原子操作。
    它通过 :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_C`
    Kconfig 选项配置。

* 查找最低有效置位（find-least-significant-bit-set）和查找最高有效置位（find-most-significant-bit-set）。

  * 如果某体系结构不存在相应指令，
    总是可以将这些函数实现为通用 C 函数。

可以用编译器内建函数（built-ins）来实现这些，但注意它们必须使用所需的编译器屏障（barrier）。

CPU 空闲/电源管理
***************************

内核通过两个函数提供 CPU 电源管理支持：:c:func:`arch_cpu_idle` 和 :c:func:`arch_cpu_atomic_idle`。

:c:func:`arch_cpu_idle` 可以简单到
在中断未锁定时调用该体系结构的省电指令，
例如 x86 上的 :code:`hlt`、
ARM 上的 :code:`wfi` 或 :code:`wfe`、
ARC 上的 :code:`sleep`。
此函数可以在一个不关心睡眠前是否会被中断打断的上下文中循环调用。
基本上有两种情况使用此函数是正确的：

* 在单线程系统中，在初始化后不用于做实际工作的唯一线程中，即它在整个应用期间坐在循环中什么都不做。

* 在空闲线程（idle thread）中。

而 :c:func:`arch_cpu_atomic_idle` 必须能够原子地重新启用中断并调用省电指令。因此它可以用于真实的应用代码，同样用于单线程系统。

通常，CPU 空闲应留给空闲线程，但在某些非常特殊的场景中，应用可以使用这些 API。

两个函数必须对给定体系结构都存在。但是，如需要，实现可以简单地是以下步骤：

#. 解锁中断
#. NOP（空操作）

不过，强烈建议提供真实实现。

故障管理
****************

在发生未处理的 CPU 异常时，
体系结构代码必须调用 :c:func:`z_fatal_error`。
此函数输出与体系结构无关的信息，
并通过调用 :c:func:`k_sys_fatal_error` 做出下一步的策略决策。
此函数可以被覆盖以实现应用特定的策略，
可能包括锁定中断并永远自旋（默认实现），
甚至关闭系统（如果支持）。

工具链与链接
*********************

必须向构建系统添加工具链支持。

需要在 :zephyr_file:`include/zephyr/toolchain/gcc.h` 中定义某些体系结构特定的定义。参见该文件中当前支持的体系结构的内容。

每个体系结构还需要自己的链接器脚本，即使大多数段可以从其他体系结构的链接器脚本派生。某些段可能特定于新体系结构，例如 ARM 上的 SCB 段和 x86 上的 IDT 段。

内存管理与内存映射
************************************

如果目标平台启用分页（paging）并要求驱动程序对其 I/O 区域进行内存映射，需要启用 :kconfig:option:`CONFIG_MMU` 并实现以下 API：

- :c:func:`arch_mem_map`
- :c:func:`arch_mem_unmap`
- :c:func:`arch_page_phys_get`

栈对象
*************

内存保护硬件的存在影响栈对象的创建方式。
所有体系结构移植必须指定栈指针所需的对齐，
它是 CPU 和 ABI 要求的某种组合。
这在体系结构头文件中用 :c:macro:`ARCH_STACK_PTR_ALIGN` 定义，
通常是 4、8 或 16 字节这样的小值。

存在两种类型的线程栈：

- "内核"栈，用 :c:macro:`K_KERNEL_STACK_DEFINE()` 和相关 API 定义，
  可以托管运行在监督模式（supervisor mode）的内核线程，
  或用作中断/异常处理的栈。
  这些的对齐要求显著放宽，且使用的保留数据更少。
  不为权限提升栈（privilege elevation stacks）保留内存。

- "线程"栈通常使用更多内存，但能够托管运行在用户模式的线程，以及内核栈的任何用例。

如果未启用 :kconfig:option:`CONFIG_USERSPACE`，"线程"栈和"内核"栈等价。

体系结构层可能定义额外的宏，以指定栈对象基部的对齐、栈对象内不用于线程栈缓冲区的保留数据，以及如何向上取整栈尺寸以支持用户模式线程。在没有定义的情况下，假设某些默认值：

- :c:macro:`ARCH_KERNEL_STACK_RESERVED`：默认无保留空间
- :c:macro:`ARCH_THREAD_STACK_RESERVED`：默认无保留空间
- :c:macro:`ARCH_KERNEL_STACK_OBJ_ALIGN`：默认对齐到 :c:macro:`ARCH_STACK_PTR_ALIGN`
- :c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN`：默认对齐到 :c:macro:`ARCH_STACK_PTR_ALIGN`
- :c:macro:`ARCH_THREAD_STACK_SIZE_ALIGN`：默认向上取整到 :c:macro:`ARCH_STACK_PTR_ALIGN`

所有栈创建宏都基于这些来定义。

所有栈对象都有以下布局，某些区域根据配置可能为零大小。始终有两个主要部分：开头的保留内存，然后是栈缓冲区本身。某些区域的边界只能在关联线程对象的上下文中于运行时确定。其他区域在构建时完全可计算。

某些体系结构可能需要从栈缓冲区中在运行时切出（carve-out）保留内存，
而不是在构建时无条件保留它，
或补充一个现有的保留区域（ARM FPU 就是这种情况）。
此类切出始终在 ``thread.stack_info.start`` 中跟踪。
``thread.stack_info.start`` 和 ``thread.stack_info.size`` 指定的区域
始终完全可被用户模式线程访问。
``thread.stack_info.delta`` 表示一个偏移，
可用于从栈对象的末端计算初始栈指针，
同时考虑 TLS 和 ASLR 随机偏移的存储。

.. code-block:: none

   +---------------------+ <- thread.stack_obj
   | Reserved Memory     | } K_(THREAD|KERNEL)_STACK_RESERVED
   +---------------------+
   | Carved-out memory   |
   |.....................| <- thread.stack_info.start
   | Unused stack buffer |
   |                     |
   |.....................| <- 线程当前的栈指针
   | Used stack buffer   |
   |                     |
   |.....................| <- 初始栈指针。可用
   | ASLR Random offset  |      thread.stack_info.delta 计算
   +---------------------| <- thread.userspace_local_data
   | Thread-local data   |
   +---------------------+ <- thread.stack_info.start + thread.stack_info.size


目前，Zephyr 不支持向上增长的栈。

无内存保护
====================

如果不使用内存保护，则默认值足够。

基于硬件的栈溢出检测
=================================

此选项使用硬件特性，在监督模式线程溢出其栈时生成致命错误。这对调试有用，但由于几个原因，在此发生后无法可靠地对系统状态做出任何断言：

* 溢出发生时内核可能正处于临界区（critical section）中，将重要全局数据结构留在损坏状态。

* 对于用保护（guard）内存区域实现栈保护的系统，在硬件检测到此情况之前，可能超出保护区域并损坏相邻数据结构。

要启用 :kconfig:option:`CONFIG_HW_STACK_PROTECTION` 特性，
系统必须提供某种基于硬件的栈溢出保护，
并启用 :kconfig:option:`CONFIG_ARCH_HAS_STACK_PROTECTION` 选项。

支持两种基于硬件的栈溢出检测形式：用于此目的的专用 CPU 特性，或紧邻栈缓冲区之前的特殊只读保护区域。

:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仅捕获监督线程的栈溢出。捕获用户线程的栈溢出不需要；:kconfig:option:`CONFIG_USERSPACE` 与之是正交的。

此特性仅检测监督模式栈溢出，包括处理系统调用时的栈溢出。它不保证内核未被损坏。监督模式中的任何栈溢出都应视为致命错误，无法对整体系统完整性做出任何断言。

用户模式中的栈溢出是可恢复的（从内核的角度），且不需要特殊配置；:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仅适用于捕获 CPU 处于监督模式时的溢出。

基于 CPU 的栈溢出检测
----------------------------------

如果通过特殊 CPU 寄存器（如 ARM 的 SPLIM）检测监督模式中的栈溢出，则默认值足够。



基于保护区域的栈溢出检测
------------------------------------

通过紧邻栈缓冲区之前的特殊内存保护区域检测监督模式栈溢出，该区域在写入时生成异常。保留内存将用于保护区域。

:c:macro:`ARCH_KERNEL_STACK_RESERVED` 应定义为内存保护区域的最小尺寸。
在大多数 ARM CPU 上这是 32 字节。
:c:macro:`ARCH_KERNEL_STACK_OBJ_ALIGN` 也应设置为该区域所需的对齐。

基于 MMU 的系统不应为保护区域保留 RAM，而应简单地在每个栈映射到地址空间时，在其下方留下一个不存在的（non-present）虚拟页。栈对象仍需正确对齐和按页粒度确定大小。

.. code-block:: none

   +-----------------------------+ <- thread.stack_obj
   | Guard reserved memory       | } K_KERNEL_STACK_RESERVED
   +-----------------------------+
   | Guard carve-out             |
   |.............................| <- thread.stack_info.start
   | Stack buffer                |
   .                             .

内核栈的保护区域切出（guard carve-out）不常见，应尽可能避免。它们往往在两种情况下需要：

* 同一个栈可能被重新用于托管用户线程，此时保护区域不需要，也不应无条件保留。当权限提升栈不在栈对象内部时就是这种情况。

* 所需的保护区域大小可变且取决于上下文。例如，某些 ARM CPU 在异常期间有惰性浮点栈（lazy floating point stacking），可能不写入任何东西就将栈指针减少大量值，完全超出最小尺寸的保护区域并损坏相邻内存。与其无条件保留更大的保护区域，不如在线程使用浮点时切出额外内存。

启用用户模式
================

启用用户模式激活两个新要求：

* 必须分配一个单独的、固定大小的权限模式栈（由 :kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE` 指定），用户线程不能访问它。内核在处理系统调用时将其用作栈。如果实现了栈保护区域，必须能在其之前放置栈保护区域，如需要则支持切出。

* 内存保护硬件必须能够编程一个恰好覆盖线程栈缓冲区的区域（在 ``thread.stack_info`` 中跟踪）。这意味着 :c:macro:`ARCH_THREAD_STACK_SIZE_ADJUST()` 需要向上取整请求的栈尺寸，以便一个区域可以覆盖它，且 :c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN()` 也应按内存保护硬件的粒度指定。

如果内存保护硬件要求所有内存区域的大小为其自身大小的 2 的幂，
并对齐到其自身大小，情况会更复杂。
这在较旧的 MPU 上常见，
用 :kconfig:option:`CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` 标识。

``thread.stack_info`` 始终跟踪栈对象中用户可访问的部分，用其内存储的范围来编程一个允许用户访问的内存保护区域必须始终正确。

非 2 的幂内存区域要求
-------------------------------------------

在没有 2 的幂区域要求的系统上，:c:macro:`K_THREAD_STACK_RESERVED` 定义的线程栈保留内存区域可用于包含权限模式栈。布局可能类似：

.. code-block:: none

   +------------------------------+ <- thread.stack_obj
   | Other platform data          |
   +------------------------------+
   | Guard region (if enabled)    |
   +------------------------------+
   | Guard carve-out (if needed)  |
   |..............................|
   | Privilege elevation stack    |
   +------------------------------| <- thread.stack_obj +
   | Stack buffer                 |      K_THREAD_STACK_RESERVED =
   .                              .      thread.stack_info.start

保护区域和任何切出（如需要）在线程创建时配置为只读区域。

* 如果线程是监督线程，权限提升区域只是额外的栈内存。溢出最终会崩溃到保护区域。

* 如果线程在用户模式运行，将配置一个内存保护区域，允许用户线程访问栈缓冲区，但不允许其前后。用户模式中的溢出会崩溃到权限提升栈，用户线程无法访问它。处理系统调用时的溢出会崩溃到保护区域。

在 MMU 系统上不应有物理保护区域；权限模式栈将映射到内核内存，栈缓冲区在内存的用户部分，各自在其下方有不存在的虚拟保护页，以捕获运行时栈溢出。

其他平台数据可能存储在保护区域之前，但如果此类数据可以存储在 ``thread.arch`` 某处，则强烈不推荐这样做。

:c:macro:`ARCH_THREAD_STACK_RESERVED` 需要定义为包含平台数据、权限提升栈和保护区域的保留区域的尺寸。它必须尺寸适当，使得授予用户模式访问栈缓冲区的 MPU 区域可以紧接其后放置。

2 的幂内存区域要求
---------------------------------------

线程栈对象必须按相同的 2 的幂确定尺寸和对齐，且不保留任何保留内存，以允许在内存中高效打包。因此，线程栈中的任何保护区域必须被完全切出，权限提升栈必须在其他地方分配。

:c:macro:`ARCH_THREAD_STACK_SIZE_ADJUST()` 和
:c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN()`
都应定义为 :c:macro:`Z_POW2_CEIL()`。
:c:macro:`K_THREAD_STACK_RESERVED` 必须为 0。

对于权限栈，必须启用 :kconfig:option:`CONFIG_GEN_PRIV_STACKS`。
对系统中找到的每个线程栈，
生成一个对应的、固定大小的内核栈，用于处理系统调用。
权限栈的地址可以用 :c:func:`z_priv_stack_find()`
基于线程栈地址在运行时快速查找。
这些栈的布局与其他仅内核用的栈相同。

.. code-block:: none

   +-----------------------------+ <- z_priv_stack_find(thread.stack_obj)
   | Reserved memory             | } K_KERNEL_STACK_RESERVED
   +-----------------------------+
   | Guard carve-out (if needed) |
   |.............................|
   | Privilege elevation stack   |
   |                             |
   +-----------------------------+ <- z_priv_stack_find(thread.stack_obj) +
                                         K_KERNEL_STACK_RESERVED +
                                         CONFIG_PRIVILEGED_STACK_SIZE

   +-----------------------------+ <- thread.stack_obj
   | MPU guard carve-out         |
   | (supervisor mode only)      |
   |.............................| <- thread.stack_info.start
   | Stack buffer                |
   .                             .

线程栈对象中的保护区域切出仅在线程运行于监督模式时使用。如果线程降到用户模式，则没有保护区域，整个对象用作栈缓冲区，关联的用户模式线程拥有完全访问权限，``thread.stack_info`` 相应更新。

用户模式线程
*****************

要支持用户模式线程，需要实现若干内核到体系结构（kernel-to-arch）API，且系统必须启用 :kconfig:option:`CONFIG_ARCH_HAS_USERSPACE` 选项。请参见每个函数的文档获取更多细节：

* :c:func:`arch_buffer_validate`，测试当前线程是否对特定内存区域有访问权限

* :c:func:`arch_user_mode_enter`，不可逆地将监督线程降到用户模式权限。栈必须被擦除。

* :c:func:`arch_syscall_oops`，在系统调用参数无法验证时生成内核 oops，使得 oops 看起来来自用户线程中调用系统调用的位置

* :c:func:`arch_syscall_invoke0` 到 :c:func:`arch_syscall_invoke6`，以适当数量的参数调用系统调用，所有参数必须通过寄存器在权限提升期间传入。

* :c:func:`arch_is_user_context`，如果 CPU 当前运行在用户模式则返回非零

* :c:func:`arch_mem_domain_max_partitions_get`，指示内存域（memory domain）的最大区域数。MMU 系统有无限数量，MPU 系统对此有限制。

某些体系结构可能在调用内存域 API 时需要更新软件内存管理结构，
或在另一个 CPU 上修改硬件寄存器。
如果是，体系结构必须选择
:kconfig:option:`CONFIG_ARCH_MEM_DOMAIN_SYNCHRONOUS_API`，
且必须实现若干额外 API。
这在 MMU 系统上常见，在 MPU 系统上不常见：

* :c:func:`arch_mem_domain_thread_add`

* :c:func:`arch_mem_domain_thread_remove`

* :c:func:`arch_mem_domain_partition_add`

* :c:func:`arch_mem_domain_partition_remove`

请参见这些 API 的 doxygen 文档了解细节。

除实现这些 API 外，还有一些其他任务：

* :c:func:`_new_thread` 需要在用户模式下用 :c:macro:`K_USER` 生成线程

* 在上下文切换时，应通过内存管理硬件中适当的配置更改，将传出线程的栈内存标记为用户模式不可访问。传入线程的栈内存同样应标记为可访问。这确保线程不能干扰其他线程的栈。

* 在上下文切换时，系统需要在传入和传出线程的内存域之间切换。

* 线程栈区域必须包含一个内核栈区域。它对用户线程应始终不可访问。此栈在发起系统调用时使用。它对所有线程应为固定大小，且必须足够大以处理任何系统调用。

* 需要建立软件中断或某种权限提升机制。这与 _arch_syscall_invoke 宏的实现紧密相关。在系统调用时，需要在 _k_syscall_table 中查找适当的处理函数。非法的系统调用 ID 应跳转到 :c:enum:`K_SYSCALL_BAD` 处理程序。在系统调用完成时，必须注意不将任何寄存器状态泄漏回用户模式。

GDB 桩
********

要在新体系结构上启用 GDB 桩以进行远程调试：

#. 在适当的体系结构 include 目录（:file:`include/zephyr/arch/<arch>/gdbstub.h`）下创建新的 ``gdbstub.h`` 头文件。

   * 创建新的结构体 ``struct gdb_ctx`` 作为 GDB 上下文。

     * 必须定义一个名为 ``exception`` 的 ``unsigned int`` 类型成员，用于存储 GDB 异常原因。此值需要在进入 :c:func:`z_gdb_main_loop` 之前设置。

     * 体系结构可以定义 GDB 桩运行所需的任意数量成员。

     * 此结构体的指针需要传递给 :c:func:`z_gdb_main_loop`，该指针将传递给其他 GDB 桩函数。

#. 进入和退出 GDB 桩主循环的函数。

   * 如果体系结构依赖中断来服务断点（breakpoint），需要实现中断服务例程（ISR），它作为 GDB 桩主循环的入口点。

   * 这些函数需要保存和恢复上下文，以便代码执行可以像未遇到断点一样继续。

   * 这些函数需要在保存执行上下文后调用 :c:func:`z_gdb_main_loop`，进入 GDB 桩主循环以接收来自 GDB 的命令。

   * 在调用 :c:func:`z_gdb_main_loop` 之前，必须设置 :c:member:`gdb_ctx.exception` 以指定异常原因。

#. 实现支持 GDB 桩功能所需的函数：

   * :c:func:`arch_gdb_init`

     * 这需要初始化支持 GDB 桩功能所需的各项，例如建立 GDB 上下文和连接调试中断。

     * 这必须通过体系结构特定的方法停止代码执行（例如触发调试中断）。这允许 GDB 在启动期间连接。

   * :c:func:`arch_gdb_continue`

     * 当 GDB 发送 ``c`` 或 ``continue`` 命令继续代码执行时调用此函数。

   * :c:func:`arch_gdb_step`

     * 当 GDB 发送 ``si`` 或 ``stepi`` 命令执行一条机器指令后返回 GDB 提示符时调用此函数。

   * 硬件寄存器读/写函数：

     * 由于 GDB 桩运行在目标上，对硬件寄存器的操作需要缓存，以避免影响 GDB 桩的执行。将其视为上下文切换，其中执行上下文更改为 GDB 桩。因此上下文切换前运行线程的寄存器值需要存储。寄存器值的操作仅对此缓存副本执行。更新的值然后在切换回之前运行的线程前写入硬件寄存器。

     * :c:func:`arch_gdb_reg_readall`

       * 这收集将出现在发回 GDB 的 ``g``/``G`` 数据包中的所有硬件寄存器值。G 数据包的格式是体系结构特定的。参考 GDB 文档了解预期内容。

       * 注意，对于大多数体系结构，必须返回并发送一个有效的 G 数据包给 GDB。如果向 GDB 发送长度不正确的数据包，GDB 将中止调试会话。

     * :c:func:`arch_gdb_reg_writeall`

       * 这接受 GDB 发送的 G 数据包，并用数据包中的值填充硬件寄存器。

     * :c:func:`arch_gdb_reg_readone`

       * 这读取一个硬件寄存器的值并将结果发送到 GDB。

     * :c:func:`arch_gdb_reg_writeone`

       * 这将 GDB 接收的一个硬件寄存器的值写入该寄存器。

   * 断点：

     * :c:func:`arch_gdb_add_breakpoint` 和 :c:func:`arch_gdb_remove_breakpoint`

     * GDB 可能决定使用软件断点，它修改断点位置的内存，用软件断点或陷阱（trap）指令替换指令。GDB 然后在执行到达断点时恢复内存内容。GDB 默认支持此，通常无需在体系结构代码中处理软件断点（断点类型为 ``0``）。

     * 如果代码在无法在运行时修改的 ROM 或 flash 中，则需要硬件断点（类型 ``1``）。参考体系结构数据手册了解如何启用硬件断点。

     * 如果体系结构不支持硬件断点，则无需在体系结构代码中实现这些。GDB 将依赖软件断点。

#. 对于某些内存区域不可访问的体系结构，需要定义一个名为 :c:var:`gdb_mem_region_array` 的 :c:struct:`gdb_mem_region` 类型数组，以指定可访问的区域。对每个数组项：

   * :c:member:`gdb_mem_region.start` 指定内存区域的起始。

   * :c:member:`gdb_mem_region.end` 指定内存区域的结束。

   * :c:member:`gdb_mem_region.attributes` 指定内存区域的权限。

     * :c:macro:`GDB_MEM_REGION_RO`：区域只读。

     * :c:macro:`GDB_MEM_REGION_RW`：区域可读可写。

   * :c:member:`gdb_mem_region.alignment` 指定内存区域的读/写对齐。如果无对齐要求且读/写可逐字节进行，则使用 ``0``。

API 参考
*************

时序
======

.. doxygengroup:: arch-timing

线程
=======

.. doxygengroup:: arch-threads

.. doxygengroup:: arch-tls

电源管理
================

.. doxygengroup:: arch-pm

对称多处理
==========================

.. doxygengroup:: arch-smp

中断
==========

.. doxygengroup:: arch-irq

用户空间
=========

.. doxygengroup:: arch-userspace

内存管理
=================

.. doxygengroup:: arch-mmu

其他体系结构 API
===============================

.. doxygengroup:: arch-misc

GDB 桩 API
=============

.. doxygengroup:: arch-gdbstub
