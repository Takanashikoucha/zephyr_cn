.. _bluetooth_mesh_blob_flash:

BLOB Flash
##########

BLOB Flash Reader 和 Writer 实现从 :ref:`flash map <flash_map_api>` 中定义的 flash 分区读取和写入 BLOB 数据。


BLOB Flash Reader
*****************

BLOB Flash Reader 与 BLOB Transfer Client 交互，以直接从 flash 读取 BLOB 数据。在传递给 BLOB Transfer Client 之前，必须通过调用 :c:func:`bt_mesh_blob_flash_rd_init` 初始化。每个 BLOB Flash Reader 一次仅支持一个传输。


BLOB Flash Writer
*****************

BLOB Flash Writer 与 BLOB Transfer Server 交互，以将 BLOB 数据直接写入 flash。在传递给 BLOB Transfer Server 之前，必须通过调用 :c:func:`bt_mesh_blob_flash_rd_init` 初始化。每个 BLOB Flash Writer 一次仅支持一个传输，并且要求 block 大小是 flash 页大小的倍数。如果以低于 flash 页大小的 block 大小启动传输，该传输将被拒绝。

BLOB Flash Writer 将 chunk 数据复制到缓冲区，以容纳与 flash 写入 block 大小未对齐的 chunk。如果 chunk 的起始位置或长度未对齐，缓冲区数据将用 ``0xff`` 填充。

API Reference
*************

.. doxygengroup:: bt_mesh_blob_io_flash