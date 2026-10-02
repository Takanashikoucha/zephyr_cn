.. _bluetooth_mesh_blob_cli:

BLOB Transfer Client
####################

Binary Large Object（BLOB）Transfer Client 是 BLOB 传输的发送方。它支持以 Push BLOB Transfer Mode 和 Pull BLOB Transfer Mode 两种方式，将任意大小的 BLOB 发送给任意数量的 Target 节点。

Usage
*****

Initialization
=============

BLOB Transfer Client 在 element 上实例化，并带有一组事件处理回调：

.. code-block:: C

   static const struct bt_mesh_blob_cli_cb blob_cb = {
         /* Callbacks */
   };

   static struct bt_mesh_blob_cli blob_cli = {
         .cb = &blob_cb,
   };

   static const struct bt_mesh_model models[] = {
         BT_MESH_MODEL_BLOB_CLI(&blob_cli),
   };

Transfer context
================

获取传输能力流程和 BLOB 传输都会使用一个 :c:struct:`bt_mesh_blob_cli_inputs` 实例来确定如何执行传输。BLOB Transfer Client Inputs 结构体至少必须初始化一个 target 列表、一个应用密钥和一个 time to live（TTL）值，然后才能用于某个流程：

.. code-block:: c

   static struct bt_mesh_blob_target targets[3] = {
           { .addr = 0x0001 },
           { .addr = 0x0002 },
           { .addr = 0x0003 },
   };
   static struct bt_mesh_blob_cli_inputs inputs = {
           .app_idx = MY_APP_IDX,
           .ttl = BT_MESH_TTL_DEFAULT,
   };

   sys_slist_init(&inputs.targets);
   sys_slist_append(&inputs.targets, &targets[0].n);
   sys_slist_append(&inputs.targets, &targets[1].n);
   sys_slist_append(&inputs.targets, &targets[2].n);

注意传输中的所有 BLOB Transfer Server 都必须绑定到所选应用密钥。


Group address
-------------

应用程序还可以额外在上下文结构体中指定一个组地址。如果该组不是 :c:macro:`BT_MESH_ADDR_UNASSIGNED`，传输中的消息将发往该组地址，而不是单独发送给每个 Target 节点。Mesh Manager 必须确保所有拥有 BLOB Transfer Server model 的 Target 节点都订阅了该组地址。

通常，使用组地址传输 BLOB 可以提高传输速度，因为 BLOB Transfer Client 会同时将每条消息发送给所有 Target 节点。然而，在 Bluetooth Mesh 中向组地址发送大型分片消息，通常不如向单播地址发送可靠，因为组没有传输层确认机制。这可能导致每个 block 末尾出现更长的恢复期，并增加丢失 Target 节点的风险。只有当 Target 节点列表较长时，使用组地址进行 BLOB 传输通常才会带来收益，并且每种寻址策略的有效性会因不同部署和 chunk 大小差异很大。

Transfer timeout
----------------

如果 Target 节点未能在 BLOB Transfer Client 的时间限制内响应已确认消息，该 Target 节点将从传输中移除。应用程序可以通过上下文结构体为 BLOB Transfer Client 提供额外时间来降低这种情况发生的可能性。除 20 秒基础时间外，额外时间可按 10 秒递增设置，最多可达 182 小时。等待时间会随传输 TTL 自动缩放。

注意 BLOB Transfer Client 仅在以下情况下继续传输：

* 所有 Target 节点都已响应。
* 某个节点已从 Target 节点列表中移除。
* BLOB Transfer Client 超时。

增加等待时间会增加该延迟。

BLOB transfer capabilities retrieval
===================================

通常建议在开始传输之前获取 BLOB 传输能力。该流程会从所有 Target 节点获取传输能力，并使用允许所有 Target 节点参与传输的最宽松参数集。未能响应或返回不兼容传输参数的 Target 节点将被移除。

Target 节点按照其在 Target 节点列表中的顺序优先排序。如果某个 Target 节点与任何先前的 Target 节点不兼容，例如报告了不重叠的 block 大小范围，它将被移除。丢失的 Target 节点将通过 :c:member:`lost_target <bt_mesh_blob_cli_cb.lost_target>` 回调报告。

流程结束通过 :c:member:`caps <bt_mesh_blob_cli_cb.caps>` 回调发出信号，所得能力可用于确定 BLOB 传输所需的 block 大小和 chunk 大小。

BLOB transfer
=============

BLOB 传输通过调用 :c:func:`bt_mesh_blob_cli_send` 函数启动，除前述传输输入外，还需要一组传输参数和一个 BLOB stream 实例。传输参数包括 64 位 BLOB ID、BLOB 大小、传输模式、以对数形式表示的 block 大小和 chunk 大小。BLOB ID 由应用程序定义，但必须与 BLOB Transfer Server 启动时使用的 BLOB ID 匹配。

传输会持续运行，直到至少对一个 Target 节点成功完成，或者被取消。传输结束通过 :c:member:`end <bt_mesh_blob_cli_cb.end>` 回调通知应用程序。丢失的 Target 节点将通过 :c:member:`lost_target <bt_mesh_blob_cli_cb.lost_target>` 回调报告。

API reference
*************

.. doxygengroup:: bt_mesh_blob_cli