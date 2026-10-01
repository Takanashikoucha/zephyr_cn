.. _mipi_stp_decoder:

MIPI STP Decoder
################

MIPI System Trace Protocol (MIPI STP) 开发为可
由多个 application-specific trace protocols 共享的通用 base protocol。其作为 wrapper protocol
（合并通常包含来自不同
trace sources 的不同 trace protocols 的 disparate streams。Stream 由 opcode（最短 4 bit 长）后跟可选 data 和
可选 timestamp 组成。有 data (8、16、32、64 bit data marked/not marked（有或
无 timestamp) 的 opcodes（stream recognition (master 和
channel)（synchronization (ASYNC opcode) 和
其他。

使用此 protocol 的一个示例为 ARM Coresight STM (System Trace Macrocell)（其中
写入 Stimulus Port registers 的 data 直接映射到 STP stream。

此 module 可用于对 data stream 进行 on-chip 解码。使用 STP v2。

Usage
*****

Decoder 用 callback 初始化。每个解码的 opcode 调用 callback。
Decoder 有内部 state（因为 opcodes 间有依赖（如 timestamp 可
为 relative。Decoder 可处于同步或未同步状态。初始 state 可配置。
若 decoder 未与 stream 同步（则其解码每个 nibble 以寻找 ASYNC opcode。
可调用
:c:func:`mipi_stp_decoder_sync_loss` 向 decoder 指示
同步丢失。:c:func:`mipi_stp_decoder_decode` 用于解码 data。

Limitations
***********

有以下 limitations：

* Decoder 仅支持 little endian architectures。
* 解码 nibbles 时（core 支持 unaligned memory access 时更高效。
  实现支持带 unaligned memory access 的优化版本和通用版本。
  优化版本用于 ARM Cortex-M（M0 除外。
* 仅实现最常见 opcodes 的有限集合。

API documentation
*****************

.. doxygengroup:: mipi_stp_decoder_apis
