.. SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
.. SPDX-FileCopyrightText: Copyright (c) 2026 Philipp Steiner
.. SPDX-License-Identifier: Apache-2.0

.. _precision_timing:

精密定时
################

精密定时子系统为 PTP、gPTP 以及其他控制高分辨率时钟的用户
提供一组小型的可复用机制。
通过 :kconfig:option:`CONFIG_PRECISION_TIMING` 启用。

.. note::

    该 API 处于 :ref:`实验性 <api_lifecycle_experimental>` 成熟度阶段，
    仍可能发生变化。协议使用本子系统不会改变其成熟度。

本子系统有意不实现同步策略。PTP 和 gPTP 继续拥有各自的协议状态机、
时钟选择、阶跃阈值、采样接受、锁定检测、信源丢失处理以及诊断功能。

精密时间
**************

:c:type:`precision_time_t` 是一个有符号 64 位纳秒值。
带检查的加法和减法辅助函数会报告溢出。
该类型不标识时间域或时间尺度；
对 TAI、UTC、PHC、单调时间以及协议关系的建模不在本 API 范围内。

精密时钟
***************

:c:struct:`precision_clock` 分发四个必需的时钟操作：

* 读取当前时间；
* 设置绝对时间；
* 应用相位调整；以及
* 以百万分比设置相对于标称频率的速率偏移，
  并带有 16 位二进制小数部分。

所有操作都必须由时钟适配器实现。
调整范围和其他硬件约束仍由底层时钟实现负责。

:c:struct:`precision_clock_ptp_adapter` 通过该接口
暴露现有的 Zephyr PTP 时钟设备。
它在 :c:struct:`net_ptp_time` 与 :c:type:`precision_time_t`
之间执行必要的转换；不增加能力发现或同步状态。

PI 控制器
*************

:c:struct:`precision_pi` 是基于实例的比例积分（PI）控制器。
每个实例保存自己的增益和积分项。
对于每个误差采样，更新等价于：

.. code-block:: c

    integral += ki * error;
    output = kp * error + integral;

控制器不决定某个误差是否应该阶跃、拒绝或用于速率调整。
它也不跟踪同步、捕获、锁定、保持、信源超时或时钟故障。
调用方负责这些决策，并在其策略要求时
重置累积的积分项。

PTP 和 gPTP 集成从
:kconfig:option:`CONFIG_PRECISION_TIMING_PI_KP` 和
:kconfig:option:`CONFIG_PRECISION_TIMING_PI_KI` 初始化其控制器。
整数值以千分比表示增益。
:c:func:`precision_pi_init` 的直接用户
可以为每个控制器实例提供不同的增益。

协议集成
********************

PTP 和 gPTP 的默认时钟更新路径各自保留现有的策略，
并使用 :c:struct:`precision_pi` 进行共享计算。
它们初始化一次 PTP 时钟适配器，
并使用 :c:struct:`precision_clock` 操作访问 PHC。

示例
******

:zephyr:code-sample:`precision_timing` 示例演示了带检查的时间算术、
基于软件的精密时钟以及 PI 驱动的速率调整。

API 参考
*************

.. doxygengroup:: precision_timing

.. doxygengroup:: precision_time

.. doxygengroup:: precision_clock

.. doxygengroup:: precision_clock_ptp

.. doxygengroup:: precision_pi
