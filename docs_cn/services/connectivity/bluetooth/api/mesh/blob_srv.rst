.. _bluetooth_mesh_blob_srv:

BLOB Transfer Server
####################

Binary Large Object（BLOB）Transfer Server model 实现大型二进制对象的可靠接收。它作为 :ref:`bluetooth_mesh_dfu_srv` 的后端，但也可用于接收其他二进制镜像。

BLOBs
*****

如 :ref:`bluetooth_mesh_blob` 中所述，BLOB Transfer model 传输的二进制对象被划分为 block，block 又被划分为 chunk。由于传输由 BLOB Transfer Client model 控制，BLOB Transfer Server 必须允许 block 以任何顺序到达。Block 内的 chunk 也可以以任何顺序到达，但在开始下一个 block 之前必须接收完该 block 中的所有 chunk。

BLOB Transfer Server 跟踪已接收的 block 和 chunk，并且只处理每个 block 和 chunk 一次。BLOB Transfer Server 还确保任何缺失的 chunk 由 BLOB Transfer Client 重新发送。

Usage
*****

BLOB Transfer Server 在 element 上实例化，并带有一组事件处理回调：

.. code-block:: C

   static const struct bt_mesh_blob_srv_cb blob_cb = {
       /* Callbacks */
   };

   static struct bt_mesh_blob_srv blob_srv = {
       .cb = &blob_cb,
   };

   static const struct bt_mesh_model models[] = {
       BT_MESH_MODEL_BLOB_SRV(&blob_srv),
   };

BLOB Transfer Server 一次能够接收一个 BLOB 传输。在 BLOB Transfer Server 能够接收传输之前，必须由用户进行准备。传输 ID 必须在 BLOB Transfer Client 启动传输之前，通过 :c:func:`bt_mesh_blob_srv_recv` 函数传递给 BLOB Transfer Server。该 ID 必须通过某个更高层流程在 BLOB Transfer Client 和 BLOB Transfer Server 之间共享，例如厂商特定的传输管理 model。

一旦 BLOB Transfer Server 上设置好传输，它即可接收 BLOB。应用程序通过事件处理回调获知传输进度，BLOB 数据被发送到 BLOB stream。

BLOB Transfer Server、BLOB stream 和应用程序之间的交互如下所示：

.. figure:: images/blob_srv.svg
   :align: center
   :alt: BLOB Transfer Server model interaction

   BLOB Transfer Server model interaction

Transfer suspension
*******************

BLOB Transfer Server 在传输期间维护一个运行计时器，每当收到消息时都会重置。如果 BLOB Transfer Client 在传输计时器到期前未发送消息，BLOB Transfer Server 将暂停该传输。

BLOB Transfer Server 通过调用 :c:member:`suspended <bt_mesh_blob_srv_cb.suspended>` 回调通知用户暂停。如果 BLOB Transfer Server 正在接收某个 block 的中间，该 block 将被丢弃。

BLOB Transfer Client 可通过启动新的 block 传输来恢复已暂停的传输。BLOB Transfer Server 通过调用 :c:member:`resume <bt_mesh_blob_srv_cb.resume>` 回调通知用户。

Transfer recovery
*****************

BLOB 传输的状态被持久化存储。如果发生重启，BLOB Transfer Server 将尝试恢复传输。当 Bluetooth Mesh 子系统启动时（例如通过调用 :c:func:`bt_mesh_init`），BLOB Transfer Server 会检查被中止的传输，如果存在则调用 :c:member:`recover <bt_mesh_blob_srv_cb.recover>` 回调。在 recover 回调中，用户必须提供一个 BLOB stream 用于传输的剩余部分。如果 recover 回调未成功返回或未提供 BLOB stream，传输将被放弃。如果未实现 recover 回调，重启后的传输总是被放弃。

传输成功恢复后，BLOB Transfer Server 进入挂起状态。它将保持挂起，直到 BLOB Transfer Client 恢复传输或用户取消它。

.. note::
   发送该传输的 BLOB Transfer Client 必须支持传输恢复，传输才能完成。如果 BLOB Transfer Client 已放弃该传输，BLOB Transfer Server 将保持挂起，直到应用程序调用 :c:func:`bt_mesh_blob_srv_cancel`。

API reference
*************

.. doxygengroup:: bt_mesh_blob_srv