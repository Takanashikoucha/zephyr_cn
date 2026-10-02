.. _bluetooth_mesh_blob:

BLOB Transfer models
####################

Binary Large Object（BLOB）Transfer model 实现 Bluetooth Mesh Binary Large Object Transfer Model 规范版本 1.0，并提供通过 Bluetooth Mesh 网络从单个源向多个 Target 节点发送大型二进制对象的功能。它是 :ref:`bluetooth_mesh_dfu` 的底层传输方式，但也可用于其他对象传输目的。该实现处于实验状态。

BLOB Transfer model 支持传输最大 4 GB（2 \ :sup:`32` 字节）的连续二进制对象。BLOB 传输协议内置数据包丢失恢复流程，并设置检查点，确保所有 target 在继续之前已接收全部数据。数据传输顺序不保证。

BLOB 传输受底层 mesh 网络的传输速度和可靠性限制。在理想条件下，BLOB 的传输速率最高可达 1 kbps，允许在 10 到 15 分钟内传输 100 kB 的 BLOB。然而，网络状况、传输能力和其他限制因素很容易使数据率降低若干数量级。根据应用程序和网络配置调整传输参数，并将其安排在网络流量较低的时段，将显著提升该协议的速度和可靠性。然而，在实际部署中，接近理想速率的传输速率不太可能实现。

有两个 BLOB Transfer model：

.. toctree::
   :maxdepth: 1

   blob_srv
   blob_cli

BLOB Transfer Client 在发送节点上实例化，BLOB Transfer Server 在接收节点上实例化。

Concepts
********

BLOB 传输协议引入了若干新概念以实现 BLOB 传输。


BLOBs
=====

BLOB 是最大 4 GB 的二进制对象，可包含应用程序希望通过 mesh 网络传输的任何数据。BLOB 是连续数据对象，被划分为 block 和 chunk，以使传输可靠且易于处理。BLOB 的内容或结构不受限制，应用程序可自由对数据本身定义任何编码或压缩。

BLOB 传输协议不提供任何内置的 BLOB 数据完整性检查、加密或认证。然而，Bluetooth Mesh 协议的底层加密通过网络层和应用层加密提供数据完整性检查，并保护 BLOB 内容免受第三方访问。

Blocks
------

二进制对象被划分为 block，通常从几百到几千字节大小。每个 block 单独传输，BLOB Transfer Client 确保所有 BLOB Transfer Server 在继续下一个 block 之前已接收完整 block。Block 大小由传输的 ``block_size_log`` 参数决定，传输中除最后一个 block 外所有 block 的大小都相同，最后一个 block 可能更小。对于存储在 flash 内存中的 BLOB，block 大小通常是 Target 设备 flash 页大小的倍数。

Chunks
------

每个 block 被划分为 chunk。Chunk 是 BLOB 传输中最小的数据单元，必须能容纳在单个 Bluetooth Mesh access 消息中（不包括 opcode，379 字节或更小）。传输 chunk 的机制取决于传输模式。

在 Push BLOB Transfer Mode 下运行时，chunk 作为未确认数据包从 BLOB Transfer Client 发送给所有目标 BLOB Transfer Server。当一个 block 中的所有 chunk 发送完毕后，BLOB Transfer Client 询问每个 BLOB Transfer Server 是否缺少任何 chunk，并重新发送它们。该过程重复进行，直到所有 BLOB Transfer Server 已接收所有 chunk，或者 BLOB Transfer Client 放弃。

在 Pull BLOB Transfer Mode 下运行时，BLOB Transfer Server 一次从 BLOB Transfer Client 请求少量 chunk，并等待 BLOB Transfer Client 发送它们，然后再请求更多 chunk。该过程重复进行，直到所有 chunk 已传输完毕，或者 BLOB Transfer Server 放弃。

有关传输模式的更多信息，参见 :ref:`bluetooth_mesh_blob_transfer_modes` 章节。

.. _bluetooth_mesh_blob_stream:

BLOB streams
============

在 BLOB Transfer model 的 API 中，BLOB 数据处理与高层传输处理相分离。这种分离允许不同应用程序复用不同的 BLOB 存储和传输策略。高层传输由应用程序直接控制，而 BLOB 数据本身通过 *BLOB stream* 访问。

BLOB stream 类似于标准库文件流。通过打开、关闭、读取和写入，BLOB Transfer model 可完全访问 BLOB 数据，无论它保存在 flash、RAM 还是外设上。BLOB stream 在使用前以访问模式（读取或写入）打开，BLOB Transfer model 以 block 和 chunk 为单位在 BLOB 数据中移动，并将 BLOB stream 用作接口。

Interaction
-----------

在读取或写入 BLOB 之前，通过调用其 :c:member:`open <bt_mesh_blob_io.open>` 回调打开 stream。与 BLOB Transfer Server 一起使用时，BLOB stream 始终以写入模式打开；与 BLOB Transfer Client 一起使用时，始终以读取模式打开。

对于 BLOB 中的每个 block，BLOB Transfer model 首先调用 :c:member:`block_start <bt_mesh_blob_io.block_start>`。随后，根据访问模式，重复调用 BLOB stream 的 :c:member:`wr <bt_mesh_blob_io.wr>` 或 :c:member:`rd <bt_mesh_blob_io.rd>` 回调，将数据移入或移出 BLOB。当 model 完成处理该 block 时，调用 :c:member:`block_end <bt_mesh_blob_io.block_end>`。当传输完成时，通过调用 :c:member:`close <bt_mesh_blob_io.close>` 关闭 BLOB stream。

Implementations
---------------

应用程序可以实现自己的 BLOB stream，或者使用 Zephyr 提供的实现：

.. toctree::
   :maxdepth: 2

   blob_flash


Transfer capabilities
=====================

每个 BLOB Transfer Server 可能具有不同的传输能力。每个设备的传输能力通过以下配置项控制：

* :kconfig:option:`CONFIG_BT_MESH_BLOB_SIZE_MAX`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_BLOCK_SIZE_MIN`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_BLOCK_SIZE_MAX`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_CHUNK_COUNT_MAX`

:kconfig:option:`CONFIG_BT_MESH_BLOB_CHUNK_COUNT_MAX` 选项也由 BLOB Transfer Client 使用，并影响 BLOB Transfer Client model 结构的内存消耗。

为确保传输可被尽可能多的 server 接收，BLOB Transfer Client 可在开始传输之前获取每个 BLOB Transfer Server 的能力。Client 将以尽可能高的 block 大小和 chunk 大小传输 BLOB。

.. _bluetooth_mesh_blob_transfer_modes:

Transfer modes
==============

BLOB 可使用两种传输模式传输：Push BLOB Transfer Mode 和 Pull BLOB Transfer Mode。在大多数情况下，应以 Push BLOB Transfer Mode 进行传输。

在 Push BLOB Transfer Mode 下，发送速率由 BLOB Transfer Client 控制，它会推送每个 block 的所有 chunk，而不进行任何高层流量控制。Push BLOB Transfer Mode 支持任意数量的 Target 节点，并且应是默认传输模式。

在 Pull BLOB Transfer Mode 下，BLOB Transfer Server 会以自身速率从 BLOB Transfer Client “拉取” chunk。Pull BLOB Transfer Mode 可与多个 Target 节点进行，并用于向充当 :ref:`bluetooth_mesh_lpn` 的 Target 节点传输 BLOB。在 Pull BLOB Transfer Mode 下运行时，BLOB Transfer Server 以小批量从 BLOB Transfer Client 请求 chunk，并等待它们全部到达后再请求更多 chunk。该过程重复进行，直到 BLOB Transfer Server 已接收 block 中的所有 chunk。随后，BLOB Transfer Client 开始下一个 block，BLOB Transfer Server 请求该 block 的所有 chunk。


.. _bluetooth_mesh_blob_timeout:

Transfer timeout
================

BLOB 传输的超时基于 Timeout Base 值。Client 和 server 使用相同的 Timeout Base 值，但计算超时的方式不同。

BLOB Transfer Server 使用以下公式计算 BLOB 传输超时::

  10 * (Timeout Base + 1) 秒


对于 BLOB Transfer Client，使用以下公式::

  (10000 * (Timeout Base + 2)) + (100 * TTL) 毫秒

其中 TTL 是传输中设置的 time to live 值。

API reference
*************

本节包含 BLOB Transfer model 共用的类型和定义。

.. doxygengroup:: bt_mesh_blob