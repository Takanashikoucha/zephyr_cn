.. _mipi_stp_decoder:

MIPI STP Decoder
################

MIPI 系统跟踪协议（MIPI System Trace Protocol，MIPI STP）被开发为一种通用基础协议，
可以由多个应用特定的跟踪协议共享。它充当一个封装协议（wrapper protocol），
用于合并通常包含来自不同
跟踪源（trace source）的不同跟踪协议的多个流（stream）。流由操作码（opcode，最短为 4 位）后跟可选的数据和
可选的时间戳（timestamp）组成。存在用于数据（8、16、32、64 位数据，标记/未标记，带
或不带时间戳）的操作码，用于流识别（主设备（master）和
通道（channel）），用于同步（ASYNC 操作码）以及
其他用途。

使用该协议的一个示例是 ARM Coresight STM（System Trace Macrocell，系统跟踪宏单元），其中
写入 Stimulus Port 寄存器的数据直接映射到 STP 流。

该模块可用于在芯片上（on-chip）对数据流进行解码。使用 STP v2。

用法
*****

解码器（Decoder）通过回调函数初始化。每解码一个操作码都会调用回调函数。
解码器具有内部状态，因为操作码之间存在依赖关系（例如时间戳可
为相对值）。解码器可以处于同步或未同步状态。初始状态可配置。
如果解码器未与流同步，则它会逐个解码每个半字节（nibble），以寻找 ASYNC 操作码。
可以调用
:c:func:`mipi_stp_decoder_sync_loss` 向解码器指示
同步丢失。:c:func:`mipi_stp_decoder_decode` 用于解码数据。

限制
***********

存在以下限制：

* 解码器仅支持小端（little endian）架构。
* 解码半字节时，如果核心支持非对齐内存访问，则效率更高。
  实现支持带非对齐内存访问的优化版本和通用版本。
  优化版本用于 ARM Cortex-M（M0 除外）。
* 仅实现了最常见操作码的有限集合。

API 文档
*****************

.. doxygengroup:: mipi_stp_decoder_apis
