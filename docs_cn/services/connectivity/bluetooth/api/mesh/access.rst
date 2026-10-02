.. _bluetooth_mesh_access:

Access 层
############

Access 层是应用程序访问 Bluetooth Mesh 网络的接口。Access 层提供机制，将节点行为划分为 element 和 model，并由应用程序实现这些 element 和 model。

Mesh models
***********

Mesh 节点的功能由 model 表示。每个 model 实现节点所支持的单一行为，例如作为灯、传感器或恒温器。Mesh model 被分组到 *element* 中。每个 element 都被分配一个单播地址，并且每种类型的 model 只能包含一个。按照惯例，每个 element 表示 Mesh 节点行为的单一方面。例如，一个包含传感器、两个灯和一个电源插座的节点，会将这些功能分布在四个 element 中，每个 element 实例化实现所支持行为单一方面所需的全部 model。

节点的 element 和 model 结构在节点组合数据中指定，并在初始化时传递给 :c:func:`bt_mesh_init`。Bluetooth SIG 已定义一组基础 model（参见 :ref:`bluetooth_mesh_models`），并在 `Bluetooth Mesh Model Specification <https://www.bluetooth.com/specifications/mesh-specifications/>`_ 中定义了一组用于实现常见行为的 model。所有未由 Bluetooth SIG 指定的 model 都是厂商 model，必须绑定到 Company ID。

Mesh model 具有若干参数，可通过初始化 mesh 协议栈或使用 :ref:`bluetooth_mesh_models_cfg_srv` 进行配置：

Opcode list
===========

Opcode 列表包含 model 可接收的所有消息 opcode，以及最小可接受的有效载荷长度和用于传递这些消息的回调。Model 可以支持任意数量的 opcode，但每个 opcode 在每个 element 中只能由一个 model 列出。

完整的 opcode 列表必须传递给组合数据中的 model 结构体，且不能在运行时更改。Opcode 列表的结尾由特殊条目 :c:macro:`BT_MESH_MODEL_OP_END` 决定。除非列表为空，否则该条目必须始终出现在 opcode 列表中。如果列表为空，则应使用 :c:macro:`BT_MESH_MODEL_NO_OPS` 代替正式的 opcode 列表定义。

AppKey list
===========

AppKey 列表包含 model 可接收消息的所有应用密钥。只有使用 AppKey 列表中的应用密钥加密的消息才会传递给该 model。

每个 model 可持有的最大应用密钥数量由配置项 :kconfig:option:`CONFIG_BT_MESH_MODEL_KEY_COUNT` 配置。AppKey 列表的内容由 :ref:`bluetooth_mesh_models_cfg_srv` 管理。

Subscription list
=================

Model 会处理所有发往其 element 单播地址的消息（前提是所用应用密钥存在于 AppKey 列表中）。此外，model 还会处理发往其订阅列表中任意组地址或虚拟地址的数据包。这使得节点能够通过单条消息寻址整个 mesh 网络中的多个节点。

每个 model 可持有的订阅列表中的最大地址数量由配置项 :kconfig:option:`CONFIG_BT_MESH_MODEL_GROUP_COUNT` 配置。订阅列表的内容由 :ref:`bluetooth_mesh_models_cfg_srv` 管理。

Model publication
=================

Model 可以通过两种方式发送消息：

* 在 :c:struct:`bt_mesh_msg_ctx` 中指定一组消息参数，并调用 :c:func:`bt_mesh_model_send`。
* 设置 :c:struct:`bt_mesh_model_pub` 结构体并调用 :c:func:`bt_mesh_model_publish`。

使用 :c:func:`bt_mesh_model_publish` 发布消息时，model 会使用由 :ref:`bluetooth_mesh_models_cfg_srv` 配置的发布参数。这是发送主动 model 消息的推荐方式，因为它将选择消息参数的责任交给网络管理员，而网络管理员通常比单个节点更了解 mesh 网络。

为了支持使用发布参数进行发布，model 必须为发布分配一个数据包缓冲区，并将其传递给 :c:member:`bt_mesh_model_pub.msg`。Config Server 还可为发布消息设置周期性发布。为了支持此功能，model 必须填充 :c:member:`bt_mesh_model_pub.update` 回调。:c:member:`bt_mesh_model_pub.update` 回调会在消息发布前立即调用，使 model 能够修改有效载荷以反映其当前状态。

通过将 :c:member:`bt_mesh_model_pub.retr_update` 设置为 1，model 可以配置 :c:member:`bt_mesh_model_pub.update` 回调在每次重传时触发。例如，使用 Delay 参数的 model 可以利用这一点，因为该参数可以在每次重传时调整。:c:func:`bt_mesh_model_pub_is_retransmission` 函数可用于区分首次发布和重传。:c:macro:`BT_MESH_PUB_MSG_TOTAL` 和 :c:macro:`BT_MESH_PUB_MSG_NUM` 宏可用于返回一个发布间隔内的总传输次数和重传序号。

Extended models
===============

Bluetooth Mesh 规范允许 mesh model 相互扩展。当一个 model 扩展另一个 model 时，它会继承被扩展 model 的功能，并且扩展可用于从简单 model 构建复杂 model，利用现有 model 功能以避免定义新 opcode。Model 可以从任意 element 扩展任意数量的 model。当一个 model 在同一 element 中扩展另一个 model 时，两个 model 将共享订阅列表。Mesh 协议栈通过将两个 model 的订阅列表合并为一个来实现此功能，并组合这两个 model 总共可拥有的订阅数量。Model 可以扩展其他正在扩展的 model，从而形成“扩展树”。扩展树中的所有 model 在其跨度的每个 element 中共享一个订阅列表。

Model 扩展通过在初始化期间调用 :c:func:`bt_mesh_model_extend` 完成。一个 model 只能被另一个 model 扩展，且扩展不能形成循环。注意，节点状态绑定以及 model 之间的其他关系必须由 model 实现定义。

Model 扩展概念会增加 Access 层数据包处理的一些开销，并且必须通过 :kconfig:option:`CONFIG_BT_MESH_MODEL_EXTENSIONS` 显式启用才会生效。

Model data storage
==================

Mesh model 可能具有与每个 model 实例关联的数据，需要持久化存储。Access API 提供一种机制来存储这些数据，利用内部 model 实例编码方案。Model 可以通过调用 :c:func:`bt_mesh_model_data_store` 为每个实例存储一个用户定义的数据项。为了在设备下次重启时能够读出数据，model 的 :c:member:`bt_mesh_model_cb.settings_set` 回调必须被填充。当在持久化存储中找到 model 特定数据时，会调用该回调。Model 可以通过调用作为参数传递给该回调的 ``read_cb`` 来获取数据。详细信息参见 :ref:`settings_api` 模块文档。

当 model 数据频繁变化时，每次变化都存储可能导致 flash 磨损增加。为减少磨损，model 可以通过调用 :c:func:`bt_mesh_model_data_store_schedule` 推迟数据存储。协议栈将安排一个工作项，其延迟由 :kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义。当工作项运行时，协议栈会为每个已请求存储数据的 model 调用 :c:member:`bt_mesh_model_cb.pending_store` 回调。Model 随后可以调用 :c:func:`bt_mesh_model_data_store` 存储数据。

如果启用 :kconfig:option:`CONFIG_BT_MESH_SETTINGS_WORKQ`，:c:member:`bt_mesh_model_cb.pending_store` 回调将从专用线程调用。这允许协议栈在 model 数据存储期间处理其他传入和传出消息。当需要存储大量数据时，建议使用该选项和 :c:func:`bt_mesh_model_data_store_schedule` 函数。

Composition Data
================

Composition Data 提供关于 mesh 设备的信息。设备的 Composition Data 保存关于设备上 element、所支持 model 以及其他功能的信息。Composition Data 被划分为不同页面，每个页面包含关于设备的特定功能信息。为了访问这些信息，用户可以使用 :ref:`bluetooth_mesh_models_cfg_srv` model，或者（如果支持）使用 :ref:`bluetooth_mesh_lcd_srv` model。

Composition Data Page 0
-----------------------

Composition Data Page 0 提供设备的基本信息，是所有 mesh 设备的必选项。它包含 element 和 model 组合、所支持的功能以及制造商信息。

Composition Data Page 1
-----------------------

Composition Data Page 1 提供关于 model 之间关系的信息，是所有 mesh 设备的必选项。一个 model 可以扩展和/或对应一个或多个 model。Model 可以通过调用 :c:func:`bt_mesh_model_extend` 扩展另一个 model，或者通过调用 :c:func:`bt_mesh_model_correspond` 对应另一个 model。:kconfig:option:`CONFIG_BT_MESH_MODEL_EXTENSION_LIST_SIZE` 指定设备上组合中可存储多少 model 关系，该数量应反映 :c:func:`bt_mesh_model_extend` 和 :c:func:`bt_mesh_model_correspond` 调用的数量。

Composition Data Page 2
-----------------------

Composition Data Page 2 提供关于所支持 mesh profile 的信息。Mesh profile 规范为希望支持特定 Bluetooth SIG 定义 profile 的设备定义产品要求。当前支持的 profile 可在 `Bluetooth SIG Assigned Numbers <https://www.bluetooth.com/specifications/assigned-numbers/uri-scheme-name-string-mapping/>`_ 的 3.12 节中找到。Composition Data Page 2 仅对声称支持一个或多个 mesh profile 的设备为必选项。

Composition Data Pages 128, 129 and 130
---------------------------------------

Composition Data Pages 128、129 和 130 分别镜像 Composition Data Pages 0、1 和 2。它们用于在固件更新后 Composition Data 将发生变化时，表示被镜像页面的新内容。详细信息参见 :ref:`bluetooth_mesh_dfu_srv_comp_data_and_models_metadata`。

Delayable messages
==================

Delayable message 功能通过 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_ACCESS_DELAYABLE_MSG` 启用。这是一个可选功能，实现规范对由 model 响应所接收消息而发送的消息（也称为响应消息）的建议。

响应消息应使用以下随机延迟发送：

* 如果所接收消息发往单播地址，则在 20 到 50 毫秒之间
* 如果所接收消息发往组地址或虚拟地址，则在 20 到 500 毫秒之间

当 :c:member:`bt_mesh_msg_ctx.rnd_delay` 标志被设置时，会触发 delayable message 功能。Delayable message 功能会将消息存储在本地内存中，直到随机延迟到期。

如果随机延迟到期时传输层没有足够内存立即发送消息，则该消息将再推迟 10 毫秒。如果传输层因其他任何原因无法发送消息，delayable message 功能会携带传输层错误码触发 :c:member:`bt_mesh_send_cb.start` 回调。

如果 delayable message 功能找不到足够空闲内存来存储传入消息，它会发送延迟接近到期的消息以释放内存。

当 mesh 协议栈挂起或重置时，尚未发送的消息会被移除，并携带错误码触发 :c:member:`bt_mesh_send_cb.start` 回调。

.. note::
   当 model 连续发送多条消息时，这些消息可能不会按传递给 Access 层的顺序发送。这是因为某些消息可能被延迟的时间比其他消息更长。

   当同一 model 产生的一组消息需要按特定顺序发送时，通过将 :c:member:`bt_mesh_msg_ctx.rnd_delay` 设置为 ``false`` 可禁用随机化。

Delayable publications
======================

Delayable publication 功能实现规范对以下情况中消息发布延迟的建议：

* 当 Bluetooth Mesh 协议栈启动或发布由 :c:func:`bt_mesh_model_publish` 函数触发时，在 20 到 500 毫秒之间
* 对于周期性发布的消息，在 20 到 50 毫秒之间

该功能是可选的，并通过 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_DELAYABLE_PUBLICATION` 启用。启用后，每个 model 可通过将 :c:member:`bt_mesh_model_pub.delayable` 位域分别设置为 ``1`` 或 ``0`` 来启用或禁用 delayable publication。该位域可随时更改。

API reference
*************

.. doxygengroup:: bt_mesh_access