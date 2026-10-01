.. _dma_api:

直接内存访问（DMA）
##########################

概述
********

直接内存访问（控制器）是一种常见的协处理器类型，通常可以卸载外设与内存之间的数据传输。

DMA API 不是可移植的 API，实际上也无法做到可移植，因为每个 DMA 都有独特的内存要求、外设交互方式和特性。该 API 实际上提供了驱动在代码树中所需要的全部有用 DMA 功能的并集。对于 DMA IP 可能非常相似但存在细微差异的厂商的外设设备，它仍然可以是一个良好的抽象（需谨慎使用）。

DMA 驱动通常不处理缓存一致性；这留给开发者处理，因为需求因应用不同而差异巨大。参见 :ref:`cache_guide` 了解 Zephyr 中缓存管理的概述。

驱动实现期望
**********************************

同步与所有权
++++++++++++++++++++++++++++++

从 API 的角度看，DMA 通道是单所有者对象，意味着驱动不应尝试用互斥锁或信号量等内核同步原语来包装通道。如果 DMA 通道需要修改共享寄存器，那些寄存器更新应包裹在自旋锁中。

这使得整个 API 开销极低且可从任何调用上下文调用，包括中断服务程序，在其中启动/停止/挂起/恢复/重载通道传输可能非常有用。

传输描述符内存管理
+++++++++++++++++++++++++++++++++++++

驱动不应尝试使用任何形式的堆分配。如果传输描述符需要对象池，则应以不破坏"可从中断服务程序调用"这一承诺的方式设置。许多驱动选择为每个通道创建简单的静态描述符数组，描述符数组的大小可通过 Kconfig 调整。

通道状态机期望
++++++++++++++++++++++++++++++++++

DMA 通道应被视为状态机，DMA API 以 API 调用的形式提供状态转换事件。每个驱动都应维护自己的通道状态跟踪。通道的忙碌状态应随时可通过 :c:func:`dma_get_status()` 检查。

下面提供一张图表，展示预期的可能状态转换及其对应的 API 调用，供参考。

.. graphviz::
   :caption: DMA 状态有限状态机

   digraph {
       node [style=rounded];
       edge [fontname=Courier];
       init [shape=point];

       CONFIGURED [label=Configured,shape=box];
       RUNNING [label=Running,shape=box];
       SUSPENDED [label=Suspended,shape=box];

       init -> CONFIGURED [label=dma_config];

       CONFIGURED -> RUNNING [label=dma_start];
       CONFIGURED -> CONFIGURED [label=dma_stop, headport=c, tailport=e];
       CONFIGURED -> CONFIGURED [label=dma_config, headport=c, tailport=w];

       RUNNING -> CONFIGURED [label=dma_stop];
       RUNNING -> RUNNING [label=dma_start];
       RUNNING -> RUNNING [label=dma_resume, headport=w];
       RUNNING -> SUSPENDED [label=dma_suspend];

       SUSPENDED -> SUSPENDED [label=dma_suspend];
       SUSPENDED -> RUNNING [label=dma_resume];
       SUSPENDED -> CONFIGURED [label=dma_stop];
   }

API 参考
*************

.. doxygengroup:: dma_interface
