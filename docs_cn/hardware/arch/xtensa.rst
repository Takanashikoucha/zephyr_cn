.. _xtensa_developer_guide:

Xtensa 开发者指南
######################

概述
********

本页面包含有关为基于 Xtensa 的平台进行开发时某些方面的信息。

HiFi 音频引擎 DSP
*********************

内核允许线程在支持这些寄存器的板卡上使用 HiFi 音频引擎 DSP 寄存器。
内核仅支持线程使用 HiFi 寄存器，不支持中断服务程序（ISR）。

.. note::
    目前，只有 Intel ADSP ACE 硬件平台默认配置为支持 HiFi。

概念
========

可以将内核配置为让应用程序利用 Xtensa HiFi 音频引擎 DSP 提供的服务。
支持三种工作模式，描述如下。

无 HiFi 寄存器模式
----------------------

当应用程序没有任何使用 HiFi 寄存器的线程时，使用该模式。
这是内核的默认 HiFi 服务模式。

非共享 HiFi 寄存器模式
----------------------------

当应用程序只有单个线程使用 HiFi 寄存器时，使用该模式。
每当发生上下文切换时，HiFi 寄存器保持原样不变。

.. note::
    如果有两个或更多线程尝试使用 HiFi 寄存器，则行为未定义，
    因为内核不尝试检测（也不阻止）多个线程使用这些寄存器。

共享 HiFi 寄存器模式
--------------------------

当应用程序有两个或更多线程使用 HiFi 寄存器时，使用该模式。
启用后，内核自动允许所有线程使用 HiFi 寄存器。
从概念上讲，它可以细分为两个子模式——急切模式（eager）和惰性模式（lazy）。
两者都会保存和恢复 HiFi 寄存器，但区别在于何时保存和恢复这些寄存器，
以及保存到何处、从何处恢复。

在急切共享模型中，无论线程是否使用过这些寄存器，
HiFi 寄存器都会在每次线程上下文切换时保存和恢复。
每个线程可能需要额外的栈空间来容纳必须保存的额外寄存器。
这是两种模型中的默认模型。

在惰性共享模型中，内核跟踪“拥有”协处理器的线程。
如果“拥有”该协处理器的线程被切换出去，HiFi 寄存器将不会被保存，
直到有新线程尝试使用 HiFi；此后，该新线程成为新的所有者，
并加载其 HiFi 寄存器。

.. note::
    如果 SMP 系统检测到即将成为所有者的线程在另一颗 CPU 上仍为所有者，
    则会向该 CPU 发送 IPI（处理器间中断），以启动将其 HiFi 寄存器保存到内存的操作。
    当前处理器随后将自旋等待，直到 HiFi 寄存器被保存。
    这种自旋可能导致偶发的较长延迟。
    为获得最佳性能，建议将使用 HiFi 的线程绑定到单个 CPU。

配置选项
=====================

当配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING` 被禁用，
而配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI3` 和/或 :kconfig:option:`CONFIG_XTENSA_HIFI4` 被启用时，
选择非共享 HiFi 寄存器模式。

当配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING` 与配置选项
:kconfig:option:`CONFIG_XTENSA_HIFI3` 和/或 :kconfig:option:`CONFIG_XTENSA_HIFI4` 同时被启用时，
选择共享 HiFi 寄存器模式。
如上文所述，线程必须具有足够的栈空间，以便在上下文切换期间保存 HiFi 寄存器的值。

急切和惰性 HiFi 共享模式都需要启用配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING`。
虽然急切 HiFi 共享是默认模式，但可以通过启用配置选项 :kconfig:option:`CONFIG_XTENSA_EAGER_HIFI_SHARING` 显式选择它。
若要改为选择惰性 HiFi 共享，请启用配置选项 :kconfig:option:`CONFIG_XTENSA_LAZY_HIFI_SHARING`。
