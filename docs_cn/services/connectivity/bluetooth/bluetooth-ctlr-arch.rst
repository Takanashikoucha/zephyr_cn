.. _bluetooth-ctlr-arch:

LE Controller
#############

概述
********

.. image:: img/ctlr_overview.png

#. HCI

   * 主机控制器接口，蓝牙标准
   * 提供 Zephyr 蓝牙 HCI 驱动

#. HAL

   * 硬件抽象层
   * 厂商专属，并使用 Zephyr 驱动

#. Ticker

   * 软实时射频/资源调度

#. LL_SW

   * 基于软件的链路层实现
   * 状态与角色、控制流程、数据包控制器

#. Util

   * 裸机内存池管理
   * 可变数量的队列，无锁使用
   * 固定数量的 FIFO，无锁使用
   * 基于 Mayfly 概念的延迟 ISR 执行


架构
************

执行概览
==================

.. image:: img/ctlr_exec_overview.png


架构概览
=====================

.. image:: img/ctlr_arch_overview.png


调度
**********

.. image:: img/ctlr_sched.png


Ticker
======

.. image:: img/ctlr_sched_ticker.png


上层链路层与下层链路层
=====================================

.. image:: img/ctlr_sched_ull_lll.png


调度变体
===================

.. image:: img/ctlr_sched_variant.png


ULL 与 LLL 时序
==================

.. image:: img/ctlr_sched_ull_lll_timing.png


事件处理
**************

.. image:: img/ctlr_sched_event_handling.png


调度间隔紧密的事件
===============================

.. image:: img/ctlr_sched_msc_close_events.png


中止活动事件
=====================

.. image:: img/ctlr_sched_msc_event_abort.png


取消挂起事件
========================

.. image:: img/ctlr_sched_msc_event_cancel.png


抢占活动事件
===========================

.. image:: img/ctlr_sched_msc_event_preempt.png


数据流
*********

发送数据流
==================

.. image:: img/ctlr_dataflow_tx.png


接收数据流
=================

.. image:: img/ctlr_dataflow_rx.png


执行优先级
********************

.. image:: img/ctlr_exec_prio.png

- 事件处理（0、1）< 事件准备（2、3）< 事件/接收完成（4）< 发送
  请求（5）< 角色管理（6）< Host（7）。

- LLL 是厂商 ISR，ULL 是 Mayfly ISR 概念，Host 是内核线程。

链路层控制流程
*****************************

以下简要介绍 ULL 中控制流程处理实现的主要概念。

三个主要执行上下文
=============================

- HCI/LLCP API
   * 杂项流程发起 API
   * 通过 ull_llcp.c::ull_cp_<proc>() 发起本地流程
   * 与运行中流程（本地和远程）的接口

- lll_prepare 上下文驱动 ull_cp_run()
   * LLCP 主状态机入口/时钟
   * 通过 ull_peripheral.c/ull_central.c::ticker_cb 经由 ull_conn_llcp() 调用

- rx_demux 上下文驱动 ull_cp_tx_ack() 和 ull_cp_rx()
   * LLCP 发送确认处理和 PDU 接收
   * 来自 ull_conn.c::ull_conn_rx()
   * 处理将 PDU 传递给运行中流程，以及可能发起远程流程

数据结构与 PDU 辅助
==============================

- struct llcp_struct
   * 主要 LLCP 数据存储
   * 定义在 ull_conn_types.h 中，作为 struct ll_conn 的一部分声明
   * 保存本地和远程流程请求队列以及连接专属的 LLCP 数据
   * 基本的连接级抽象

- struct proc_ctx
   * 通用流程上下文数据，包含杂项流程数据和状态，以及用于入队的 sys_snode_t
   * 定义在 ull_llcp_internal.h 中，通过 ull_llcp.c::create_procedure() 声明/实例化
   * 还保存 tx_ack 中使用的节点引用以及 rx_node 保留机制

- struct llcp_mem_pool
   * 用于实现流程上下文资源的内存池——本地和远程版本各实例化一个
   * 通过 ull_llcp.c::create_procedure() 使用

- 杂项 PDU 操作
   * 控制 PDU 的编码和解码由 ull_llcp_pdu.c::llcp_pdu_encode/decode_<PDU>() 完成
   * 杂项 PDU 验证由 ull_llcp.c::pdu_validate_<PDU>() 经由 ull_llcp.c::pdu_is_valid() 处理

LLCP 本地与远程请求/流程状态机
=====================================================

- ull_llcp_local.c
   * 处理本地发起流程的状态机
   * 命名概念：lr _<...> => 本地请求机
   * 本地流程队列处理
   * 本地 run/rx/tx_ack 开关

- ull_llcp_remote.c
   * 上述各项的远程版本
   * 命名概念：rr_<...> => 远程请求机
   * 还处理由 llcp_rx_new() 发起的远程流程
   * 杂项流程冲突处理（在 rr_st_idle() 中）

- ull_llcp_common/conn_upd/phy/enc/cc/chmu.c
   * 各个流程的实现（ull_llcp_common.c 收集较简单的流程）
   * 命名概念：lp_<...> => 本地发起流程，rp_<...> => 远程发起流程
   * 处理流程从发起（可能经过 instant）到完成以及（如适用）Host 通知的流动

杂项概念
=====================

- 流程冲突处理
   * 解释参见 BT 规范
   * 基本上某些流程可以并行存在，某些则不行——例如一次只能有一个 instant 基础流程
   * 规范规定了发生冲突时如何处理的规则

- 终止处理
   * 关于终止如何处理有特定规则。
   * 由于存在关于流程上下文的资源处理，且 terminate 必须始终可用，这作为特殊情况处理
   * 另请注意——存在杂项情况，对端行为无效时会触发连接终止

- 新远程流程处理
   * 表 new_proc_lut[] 将 LLCP PDU 映射到 llcp_rr_new() 中使用的流程/角色
   * 注意——对于任何给定连接，远程流程队列中永远只能有一个远程流程

- 杂项小项
   * 暂停/恢复概念——有两个（详见规范）
   * 流程执行可被加密流程暂停
   * 数据发送可被 PHY、DLE 和 ENC 流程暂停
   * RX 节点保留——确保需要用于通知时无需等待 RX 节点分配


杂项单元测试概念
================================

- 每个流程一个单独的 ZTEST 单元测试
   * zephyr/tests/bluetooth/controller/ctrl_<proc>

- RX 节点处理被模拟
   * 不同配置由单独的 conf 文件处理（例如参见 ctrl_conn_update）
   * ZTEST(periph_rem_no_param_req, test_conn_update_periph_rem_accept_no_param_req)

- 单元测试中使用的 rx_demux/prepare 上下文的模拟版本——仅测试流程 PDU 流动
   * 模拟 LLL prepare/done 流程的 event_prepare()/event_done() 辅助函数
   * 'lower tester' 模拟 rx/tx 的 lt_rx()/lt_tx()
   * 'upper tester' 模拟通知流程处理的 ut_rx_node()
   * 一组生成和解析 PDU 的辅助函数，以及杂项模拟的 ull_stuff()




下层链路层
****************

LLL 执行
=============

.. image:: img/ctlr_exec_lll.png


LLL 恢复
----------

.. image:: img/ctlr_exec_lll_resume_top.png

.. image:: img/ctlr_exec_lll_resume_bottom.png


裸机工具
********************

内存 FIFO 与内存队列
============================

.. image:: img/ctlr_mfifo_memq.png

Mayfly
======

.. image:: img/ctlr_mayfly.png


* Mayfly 是多实例可扩展的 ISR 执行上下文
* 正如 Work 之于 Thread，Mayfly 之于 ISR
* 在 ISR 中执行的函数列表
* 执行优先级映射到 IRQ 优先级
* 便于跨执行上下文调度
* Race-to-idle 执行
* 无锁、裸机

遗留 Controller
*****************

.. image:: img/ctlr_legacy.png

蓝牙低功耗 Controller——厂商专属细节
*********************************************************

硬件要求
=====================

Nordic Semiconductor
--------------------

Nordic Semiconductor 蓝牙低功耗 Controller 实现
需要以下硬件外设。

.. list-table:: SoC Peripheral Use
   :header-rows: 1
   :widths: 15 15 15 10 50

   * - 资源
     - nRF 外设
     - 实例数
     - Zephyr 驱动可访问
     - 描述
   * - 时钟
     - NRF_CLOCK
     - 1
     - 是
     - * 一个低频时钟（LFCLOCK）或休眠时钟，用于蓝牙射频事件间的低功耗
       * 一个高频时钟（HFCLOCK）或活动时钟，用于高精度
         数据包定时和基于软件的收发器状态切换，包括蓝牙射频事件内的帧间间隔（tIFS）定时
   * - RTC [a]_
     - NRF_RTC0
     - 1
     - **否**
     - * 使用 2 个捕获/比较寄存器
   * - 定时器
     - NRF_TIMER0 或 NRF_TIMER4 [1]_，以及 NRF_TIMER1 [0]_
     - 2 或 1 [1]_
     - **否**
     - * 2 个实例，分别用于数据包定时和 tIFS 软件切换
       * 第一个实例有 7 个捕获/比较寄存器（3 个必需，1 个可选用于 ISR 分析，
         4 个用于单定时器 tIFS 切换）
       * 如果未使用单 tIFS 定时器，第二个实例有 4 个捕获/比较寄存器。
   * - PPI [b]_
     - NRF_PPI
     - 21 个通道（20 个 [2]_），以及 2 个通道组 [3]_
     - 是 [4]_
     - * 用于射频模式切换以实现 tIFS 定时，用于 PA/LNA
       控制
   * - DPPI [c]_
     - NRF_DPPI
     -  20 个通道，以及 2 个通道组 [3]_
     - 是 [4]_
     - * 用于射频模式切换以实现 tIFS 定时，用于 PA/LNA
       控制
   * - SWI [d]_
     - NRF_SWI4 和 NRF_SWI5，或 NRF_SWI2 和 NRF_SWI3 [5]_
     - 2
     - **否**
     - * 2 个实例，用于下层链路层和上层链路层低优先级
       执行上下文
   * - 射频
     - NRF_RADIO
     - 1
     - **否**
     - * 2.4 GHz 射频收发器，支持多种射频标准，如 1 Mbps、
       2 Mbps 以及 Coded PHY S2/S8 长距离蓝牙低功耗技术
   * - RNG [e]_
     - NRF_RNG
     - 1
     - 是
     -
   * - ECB [f]_
     - NRF_ECB
     - 1
     - **否**
     -
   * - CBC-CCM [g]_
     - NRF_CCM
     - 1
     - **否**
     -
   * - AAR [h]_
     - NRF_AAR
     - 1
     - **否**
     -
   * - GPIO [i]_
     - NRF_GPIO
     - 用于 PA 和 LNA 的 2 个 GPIO 引脚，各 1 个
     - 是
     - * 另外，10 个调试 GPIO 引脚（可选）
   * - GPIOTE [j]_
     - NRF_GPIOTE
     - 1
     - 是
     - * 用于 PA/LNA
   * - TEMP [k]_
     - NRF_TEMP
     - 1
     - 是
     - * 用于 RC 来源 LFCLOCK 校准
   * - UART [l]_
     - NRF_UART0
     - 1
     - 是
     - * 用于仅 Controller 构建中的 HCI 接口
   * - IPC [m]_
     - NRF_IPC [5]_
     - 1
     - 是
     - * 用于仅 Controller 构建中的 HCI 接口


.. [a] 实时计数器（RTC）
.. [b] 可编程外设互连（PPI）
.. [c] 分布式可编程外设互连（DPPI）
.. [d] 软件中断（SWI）
.. [e] 随机数发生器（RNG）
.. [f] AES 电子密码本模式加密（ECB）
.. [g] 密码块链（CBC）——计数器模式消息认证码
       加密（CCM）
.. [h] 加速地址解析器（AAR）
.. [i] 通用输入输出（GPIO）
.. [j] GPIO 任务与事件（GPIOTE）
.. [k] 温度传感器（TEMP）
.. [l] 通用异步收发器（UART）
.. [m] 进程间通信外设（IPC）


.. [0] :kconfig:option:`CONFIG_BT_CTLR_TIFS_HW` ``=n``
.. [1] :kconfig:option:`CONFIG_BT_CTLR_SW_SWITCH_SINGLE_TIMER` ``=y``
.. [2] 当未使用预定义 PPI 通道时
.. [3] 用于基于软件的 tIFS 切换
.. [4] 使用 nRFx 接口的驱动
.. [5] 用于 nRF53x 系列
