.. _net_timeout_interface:

Network Timeout
###############

.. contents::
    :local:
    :depth: 2

Overview
********

Zephyr 的 network infrastructure 主要用毫秒分辨率的 uptime clock 跟踪 timeouts（deadlines 和 durations 均用 32-bit unsigned values 测量。32-bit value 在 49 天 17 小时 2 分钟 47.296 秒时回绕。

Timeout 处理常受 latency 影响（因此检查 timeout 的时间可能在其应过期后一段时间。正确正确处理此（无最大 latency 的任意期望（要求可直接表示的最大 delay 为 31-bit non-negative number（``INT32_MAX``）（其在 24 天 20 小时 31 分钟 23.648 秒时溢出。

大多数 network timeouts 短于 delay 回绕（但少数 protocols 允许表示为以秒计数的 unsigned 32-bit values 的 delays（对应 42-bit 毫秒 count。

Net_timeout API 提供 generic timeout mechanism 以正确跟踪这些 extended-duration timeouts 的剩余时间。

Use
***

此 API 最简单的使用为：

#. 用 :c:func:`net_timeout_set()` 配置 network timeout。
#. 用 :c:func:`net_timeout_evaluate()` 确定距 timeout 发生还有多久。调度 timeout 在此 delay 后发生。
#. 当 timeout callback 调用时（再次用 :c:func:`net_timeout_evaluate()` 确定 timeout 是否完成（或是否还有额外时间剩余。若后者（重新调度 callback。
#. 当 timeout 运行时（用 :c:func:`net_timeout_remaining` 获取距 timeout 过期还有多少秒。这可显式更新 timeout（应通过取消任何 pending callback（并从 step 1 用新 timeout 重新开始完成。

:c:struct:`net_timeout` 包含 ``sys_snode_t``（允许多个 timeout instances 聚合以共享单个 kernel timer element。Application 须对所有 instances 使用 :c:func:`net_timeout_evaluate()` 以确定下一个发生的 timeout event。

:c:func:`net_timeout_deadline()` 可用于重建 timeout 的全精度 deadline。其主要用于测试（但可能对某些 applications 有用（其确实允许毫秒分辨率的剩余时间计算。

API Reference
*************

.. doxygengroup:: net_timeout
