.. _bluetooth_mesh_blob_flash:

BLOB Flash
##########

BLOB Flash Readers 和 Writers 实现从 :ref:`flash map <flash_map_api>` 中定义的 flash partitions 读取和写入 BLOB data。


BLOB Flash Reader
*****************

BLOB Flash Reader 与 BLOB Transfer Client 交互以直接从 flash 读取 BLOB data。在传递给 BLOB Transfer Client 前须通过调用 :c:func:`bt_mesh_blob_flash_rd_init` 初始化。每个 BLOB Flash Reader 一次仅支持一个 transfer。


BLOB Flash Writer
*****************

BLOB Flash Writer 与 BLOB Transfer Server 交互以直接写入 flash 的 BLOB data。在传递给 BLOB Transfer Server 前须通过调用 :c:func:`bt_mesh_blob_flash_rd_init` 初始化。每个 BLOB Flash Writer 一次仅支持一个 transfer（且要求为 flash page size 倍数的 block size。若以低于 flash page size 的 block size 开始 transfer（transfer 将被拒绝。

BLOB Flash Writer 将 chunk data 复制到 buffer 以容纳与 flash write block size 未对齐的 chunks。若 chunk 的起始或长度未对齐（buffer data 用 ``0xff`` 填充。

API Reference
*************

.. doxygengroup:: bt_mesh_blob_io_flash
