.. _can_isotp:

ISO-TP Transport Protocol
#########################

.. contents::
    :local:
    :depth: 2

Overview
********

ISO-TP 是 ISO-Standard ISO15765-2 Road vehicles - Diagnostic communication over Controller Area Network（DoCAN）Part2: Transport protocol and network layer services 中定义的 transport protocol。如其名称已暗示（其最初设计为道路车辆诊断 over Controller Area Networks 使用（且仍如此使用。然而（其不限于道路车辆或 automotive domain 的应用。

此 transport protocol 将 classical CAN（8 bytes）和 CAN FD（64 bytes）的有限 payload data size 扩展为理论上的四 gigabytes。此外（其添加 flow control 机制以影响 sender 行为。ISO-TP 按 CAN frame 的 payload size 将 packets 分割为小 fragments。这些 segments 的 header 称为 Protocol Control Information（PCI）。

Classical CAN 上小于或等于 7 bytes 的 packets 称为 single-frames（SF）。它们无需 fragment 且无任何 flow-control。

大于该值的 packets 被分割为 first-frame（FF）和所需数量的 consecutive-frames（CF）。FF 包含关于整个 payload data 长度的信息（此外还有 payload data 的前几个 bytes。接收 peer 发回 flow-control-frame（FC）以拒绝、推迟或接受后续 consecutive frames。FC 还定义发送条件（即 block-size（BS）和 frames 之间的最小 separation time（STmin）。Block size 定义 sender 在必须等待另一 FC 前允许发送多少 CF。

.. image:: isotp_sequence.svg
   :width: 20%
   :align: center
   :alt: ISO-TP Sequence

API Reference
*************

.. doxygengroup:: can_isotp
