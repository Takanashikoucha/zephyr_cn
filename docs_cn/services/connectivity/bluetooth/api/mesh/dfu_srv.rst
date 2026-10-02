.. _bluetooth_mesh_dfu_srv:

固件更新服务器
######################

固件更新服务器模型实现 :ref:`bluetooth_mesh_dfu` 子系统中的 Target 节点功能。它扩展 :ref:`bluetooth_mesh_blob_srv`，用于从 Distributor 节点接收固件镜像二进制文件。

与扩展的 BLOB 传输服务器模型一起，固件更新服务器模型实现了通过 Mesh 网络接收固件更新所需的所有功能，但不提供保存、应用或验证镜像的任何功能。

固件镜像
***************

固件更新服务器保存设备上所有可更新固件镜像的列表。完整列表应通过 :c:macro:`BT_MESH_DFU_SRV_INIT` 中的 ``_imgs`` 参数传递给服务器，并且必须在蓝牙 Mesh 子系统启动前填充。镜像列表中的每个固件镜像都必须可独立更新，并且应有自己的固件 ID。

例如，一台具有可升级引导加载程序、应用以及具有固件更新能力的外围芯片的设备，其固件镜像列表中可以有三个条目，每个条目都有各自独立的固件 ID。

接收传输
*******************

固件更新服务器模型使用同一元素上的 BLOB 传输服务器模型来传输二进制镜像。固件更新服务器、BLOB 传输服务器与应用之间的交互如下所述：

.. figure:: images/dfu_srv.svg
   :align: center
   :alt: 蓝牙 Mesh 固件更新服务器传输

   蓝牙 Mesh 固件更新服务器传输

传输检查
=============

传输检查是应用可对入站固件镜像元数据执行的可选传输前检查。固件更新服务器通过调用 :c:member:`check <bt_mesh_dfu_srv_cb.check>` 回调来执行传输检查。

传输检查的结果是成功/失败状态返回值以及预期的 :c:enum:`bt_mesh_dfu_effect`。DFU 效果返回参数将被传回 Distributor，并应指示固件更新将对设备的 Mesh 状态产生什么影响。

.. _bluetooth_mesh_dfu_srv_comp_data_and_models_metadata:

Composition Data 和 Models Metadata
------------------------------------

如果传输将导致设备更改其 Composition Data 或变为未配置状态，应通过元数据检查的效果参数传达这一点。

当传输将导致 Composition Data 发生变化，且支持 :ref:`bluetooth_mesh_models_rpr_srv` 时，新固件镜像的 Composition Data 将由 Composition Data Pages 128、129 和 130 表示。新固件镜像的 Models Metadata 将由 Models Metadata Page 128 表示。Composition Data Pages 0、1 和 2，以及 Models Metadata Page 0，将表示旧固件镜像的 Composition Data 和 Models Metadata，直到设备使用 :ref:`bluetooth_mesh_models_rpr_cli` 通过节点配置协议接口（NPPI）过程重新配置。

应用必须调用 :c:func:`bt_mesh_comp_change_prepare` 和 :c:func:`bt_mesh_models_metadata_change_prepare` 函数，以在启动到具有更新后 Composition Data 和 Models Metadata 的固件之前保存现有的 Composition Data 和 Models Metadata 页。然后，旧的 Composition Data 将加载到 Composition Data Pages 0、1 和 2，而新固件中的 Composition Data 将加载到 Composition Data Pages 128、129 和 130。旧镜像的 Models Metadata 将加载到 Models Metadata Page 0，新镜像的 Models Metadata 将加载到 Models Metadata Page 128。

限制：

* 应用新固件镜像后，无法更改设备的 Composition Data 并让设备保持已配置状态且继续运行旧固件。

启动
=====

启动过程为应用准备接收入站传输。它将包含关于正在更新哪个镜像的信息，以及更新元数据。

固件更新服务器的 :c:member:`start <bt_mesh_dfu_srv_cb.start>` 回调必须返回一个 BLOB Writer 指针，BLOB 传输服务器将把 BLOB 发送到该 BLOB Writer。

BLOB 传输
=============

在设置阶段之后，固件更新服务器为入站传输准备 BLOB 传输服务器。整个固件镜像被传输到 BLOB 传输服务器，后者将镜像传递给其分配的 BLOB Writer。

在 BLOB 传输结束时，固件更新服务器调用其 :c:member:`end <bt_mesh_dfu_srv_cb.end>` 回调。

镜像验证
==================

BLOB 传输完成后，应用应尽可能以任意方式验证镜像，以确保其已准备好被应用。一旦镜像已验证，应用调用 :c:func:`bt_mesh_dfu_srv_verified`。

如果镜像无法验证，应用调用 :c:func:`bt_mesh_dfu_srv_rejected`。

应用镜像
==================

最后，如果镜像已验证，Distributor 可以指示固件更新服务器应用该传输。这通过 :c:member:`apply <bt_mesh_dfu_srv_cb.apply>` 回调传达给应用。应用应交换镜像并开始运行新固件。固件镜像表应更新以反映更新后镜像的新固件 ID。

当传输应用于 Mesh 应用本身时，设备可能需要在交换过程中重启。该重启可以在 apply 回调内部执行，也可以异步执行。使用新固件启动后，应在蓝牙 Mesh 子系统启动前更新固件镜像表。

Distributor 将读出固件镜像表以确认传输已成功应用。如果元数据检查表明设备将变为未配置状态，则 Target 节点无需响应此检查。

API 参考
*************

.. doxygengroup:: bt_mesh_dfu_srv
