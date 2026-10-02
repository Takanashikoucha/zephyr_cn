.. _bluetooth_mesh_dfu:

设备固件更新（DFU）
############################

蓝牙 Mesh 支持在 Mesh 网络中分发固件镜像。蓝牙 Mesh DFU 子系统实现了蓝牙 Mesh 设备固件更新模型规范版本 1.0。

蓝牙 Mesh DFU 实现了固件镜像的分发机制，不对镜像的大小、格式或用途做任何限制。该子系统的主要设计目标是提供蓝牙 Mesh DFU 规范中可落地的部分，并将使用、固件验证和部署留给应用。

DFU 规范在 Zephyr 蓝牙 Mesh DFU 子系统中实现为三个独立模型：

.. toctree::
   :maxdepth: 1

   dfu_srv
   dfu_cli
   dfd_srv

概述
********

DFU 角色
=========

蓝牙 Mesh DFU 子系统定义了 Mesh 节点在固件镜像分发过程中必须承担的三种不同角色：

Target 节点
   Target 节点是被传输固件镜像的接收者和使用者。其所有功能由 :ref:`bluetooth_mesh_dfu_srv` 模型实现。一次传输可以针对任意数量的 Target 节点，它们会同时被更新。

Distributor
   Distributor 角色在 DFU 过程中有两个用途。首先，它在上传固件过程中作为 Target 节点，然后作为 Distributor 将已上传的镜像分发给其他 Target 节点。Distributor 不选择传输参数，而是依赖 Initiator 提供 Target 节点列表和传输参数。Distributor 功能由两个模型实现，:ref:`bluetooth_mesh_dfd_srv` 和 :ref:`bluetooth_mesh_dfu_cli`。:ref:`bluetooth_mesh_dfd_srv` 负责与 Initiator 通信，:ref:`bluetooth_mesh_dfu_cli` 负责将镜像分发给 Target 节点。

Initiator
   Initiator 角色通常由实现蓝牙 Mesh :ref:`Provisioner <bluetooth_mesh_provisioning>` 和 :ref:`Configurator <bluetooth_mesh_models_cfg_cli>` 角色的同一设备实现。Initiator 需要完整了解潜在 Target 节点及其固件，并控制（并发起）所有固件更新。Initiator 角色未在 Zephyr 蓝牙 Mesh DFU 子系统中实现。

.. figure:: images/dfu_roles_mesh.svg
   :align: center
   :alt: 图形概述 DFU 角色，即 Mesh 节点在镜像分发过程中可承担的角色

   DFU 角色及相关蓝牙 Mesh 模型

蓝牙 Mesh 应用可以按任意方式组合 DFU 角色，甚至通过在独立元素上实例化模型来承担同一角色的多个实例。例如，可以通过在 Initiator 节点上实例化 :ref:`bluetooth_mesh_dfu_cli` 并直接调用其 API，来组合 Distributor 和 Initiator 角色。

也可以将 Initiator 和 Distributor 设备合并为单个设备，并用专有机制替换固件分发服务器模型，直接访问固件更新客户端模型，例如通过串行协议。

.. note::
   所有 DFU 模型都实例化一个或多个 :ref:`bluetooth_mesh_blob`，并且某些角色组合可能需要分布在多个元素上。

阶段
======

蓝牙 Mesh DFU 过程被设计为在三个阶段中执行：

上传阶段
   首先，外部实体（如手机或网关，即 Initiator）将镜像上传到 Mesh 网络中的 Distributor。在上传阶段，Initiator 将固件镜像及其所有元数据传输到 Mesh 网络内部的 Distributor 节点。Distributor 持久保存固件镜像及其元数据，并等待 Initiator 的进一步指令。完成上传过程所需的时间取决于镜像大小。上传完成后，Initiator 可以在耗时更长的分发阶段期间断开与网络的连接。一旦固件已上传到 Distributor，Initiator 可以随时触发分发阶段。

固件能力检查阶段（可选）
   在开始分发阶段之前，Initiator 可选择检查 Target 节点是否能接受新固件。未响应的节点，或响应表示无法接收新固件的节点，会被排除在固件分发过程之外。

分发阶段
   在固件镜像可以分发之前，Initiator 将 Target 节点列表及其指定的固件镜像索引传输到 Distributor。接下来，它通知 Distributor 开始固件分发过程，该过程在后台运行，同时 Initiator 和 Mesh 网络执行其他任务。一旦固件镜像已传输到 Target 节点，Distributor 可以请求它们立即应用固件镜像，并报告其状态和新的固件 ID。

固件镜像
===============

Mesh 节点固件中所有可更新部分都应表示为固件镜像。每个 Target 节点持有一份固件镜像列表，其中每个镜像都应可独立更新和识别。

固件镜像表示为一个 BLOB（固件本身），并附带以下附加信息：

固件 ID
   固件 ID 用于识别固件镜像。Initiator 节点可以请求 Target 节点提供其当前固件 ID 列表，以确定是否有更新版本的固件可用。固件 ID 的格式是厂商特定的，但通常，它应包含足够信息，使了解该格式的 Initiator 节点能够确定镜像类型及其版本。固件 ID 是可选的，其最大长度由 :kconfig:option:`CONFIG_BT_MESH_DFU_FWID_MAXLEN` 决定。

固件元数据
   固件元数据由 Target 节点用于确定是否应接受入站固件更新，以及该更新会产生什么效果。元数据格式是厂商特定的，应包含 Target 节点验证镜像所需的所有信息，以及 Target 节点在应用镜像前必须做的任何准备。典型的元数据信息包括镜像签名、节点 Composition Data 的变化，以及 BLOB 的格式。Target 节点可以在接受入站传输之前执行元数据检查，以确定是否应开始传输。固件元数据可以在元数据检查之后被 Target 节点丢弃，因为其他节点永远不会从 Target 节点请求元数据。固件元数据是可选的，其最大长度由 :kconfig:option:`CONFIG_BT_MESH_DFU_METADATA_MAXLEN` 决定。

   Zephyr 中的蓝牙 Mesh DFU 子系统提供了自己的元数据格式（:c:struct:`bt_mesh_dfu_metadata`）以及一组相关函数，可供终端产品使用。通过 :kconfig:option:`CONFIG_BT_MESH_DFU_METADATA` 选项启用对该格式的支持。元数据格式在下表中列出。

+------------------------+--------------+----------------------------------------+
| Field                  | Size (Bytes) | Description                            |
+========================+==============+========================================+
| 新固件版本             | 8 B          | 1 B：主版本                             |
|                        |              | 1 B：次版本                             |
|                        |              | 2 B：修订号                             |
|                        |              | 4 B：构建号                             |
+------------------------+--------------+----------------------------------------+
| 新固件大小             | 3 B          | 新固件的字节大小                       |
+------------------------+--------------+----------------------------------------+
| 新固件核心类型         | 1 B          | 位域：                                  |
|                        |              | 位 0：应用核心                          |
|                        |              | 位 1：网络核心                          |
|                        |              | 位 2：应用特定 BLOB。                  |
|                        |              | 其他位：RFU                             |
+------------------------+--------------+----------------------------------------+
| 入站 composition       | 4 B          | AES-CMAC 的低 4 个八位组               |
| data 的哈希值          | (Optional)   | (app-specific-key, composition data)。 |
|                        |              | 如果 New firmware core type 字段       |
|                        |              | 中设置了位 0，则存在该字段。           |
+------------------------+--------------+----------------------------------------+
| 新元素数量             | 2 B          | 应用固件后节点上的元素数量             |
|                        | (Optional)   | 如果 New firmware core type 字段       |
|                        |              | 中设置了位 0，则存在该字段。           |
+------------------------+--------------+----------------------------------------+
| 新固件的应用特定       | <variable>   | 应用特定数据，使应用能够在             |
| data                   | (Optional)   | 响应状态消息之前，使用这些数据         |
|                        |              | 执行某些厂商特定行为。                 |
+------------------------+--------------+----------------------------------------+

  .. note::

      AES-CMAC 算法在蓝牙 Mesh DFU 元数据中作为固定密钥的哈希函数使用，不用于加密。由于密钥是已知的，因此生成的哈希值不安全。

固件 URI
   固件 URI 为 Initiator 提供关于何处可以找到该镜像固件更新的信息。URI 指向一个在线资源，Initiator 可以与该资源交互以获取固件的新版本。这允许 Initiator 通过与 URI 指向的 Web 服务器交互，为 Mesh 网络中的任意节点执行更新。URI 必须使用 ``http`` 或 ``https`` 方案指向资源，且目标 Web 服务器必须按照规范定义的 Firmware Check Over HTTPS 过程运行。固件 URI 是可选的，其最大长度由 :kconfig:option:`CONFIG_BT_MESH_DFU_URI_MAXLEN` 决定。

   .. note::

      不支持带外分发机制。

.. _bluetooth_mesh_dfu_firmware_effect:

固件效果
---------------

新镜像的 Composition Data Page 0 可能与 Target 节点上分配的 Composition Data Page 0 不同。这可能影响节点的配置数据以及 Distributor 如何完成 DFU。根据旧镜像和新镜像上远程配置服务器模型的可用性，设备在应用新固件后可能以未配置状态启动，或需要重新配置。完整可用选项列表在 :c:enum:`bt_mesh_dfu_effect` 中定义：

:c:enumerator:`BT_MESH_DFU_EFFECT_NONE`
   新固件编程后，设备保持已配置状态。如果新固件的 composition data 没有变化，则选择该效果。
:c:enumerator:`BT_MESH_DFU_EFFECT_COMP_CHANGE_NO_RPR`
   当 composition data 发生变化且设备不支持远程配置时，选择该效果。新 composition data 仅在重新配置后生效。
:c:enumerator:`BT_MESH_DFU_EFFECT_COMP_CHANGE`
   当 composition data 发生变化且设备支持远程配置时，选择该效果。在这种情况下，设备保持已配置状态，新 composition data 在使用远程配置模型重新配置后生效。
:c:enumerator:`BT_MESH_DFU_EFFECT_UNPROV`
   如果新固件中的 composition data 发生变化、设备不支持远程配置，且新 composition data 在应用固件后生效，则选择该效果。如果因应用特定原因需要取消设备配置，也可以选择该效果。

当 Target 节点收到 Firmware Update Firmware Metadata Check 消息时，Firmware Update Server 模型调用 :c:member:`bt_mesh_dfu_srv_cb.check` 回调，应用随后可以处理元数据并提供效果值。如果效果是 :c:enumerator:`BT_MESH_DFU_EFFECT_COMP_CHANGE`，应用必须调用 :c:func:`bt_mesh_comp_change_prepare` 和 :c:func:`bt_mesh_models_metadata_change_prepare` 函数，以在应用新固件镜像之前准备 Composition Data Page 和 Models Metadata Page 内容。更多信息见 :ref:`bluetooth_mesh_dfu_srv_comp_data_and_models_metadata`。


DFU 过程
**************

DFU 协议实现为一组必须按特定顺序执行的过程。

Initiator 控制 DFU 协议的上传阶段，上传子过程的所有 Distributor 端处理均由 :ref:`bluetooth_mesh_dfd_srv` 实现。

分发阶段由 :ref:`bluetooth_mesh_dfu_cli` 实现的 Distributor 控制。Target 节点在 :ref:`bluetooth_mesh_dfu_srv` 中实现所有这些过程的处理，并通过一组回调通知应用。

.. figure:: images/dfu_stages_procedures_mesh.svg
   :align: center
   :alt: DFU 阶段和过程概述

   从 Distributor 视角看到的 DFU 阶段和过程

上传固件
======================

上传固件过程使用 :ref:`bluetooth_mesh_blob` 将固件镜像从 Initiator 传输到 Distributor。上传固件过程分两步执行：

1. Initiator 生成 BLOB ID，并将其与固件信息及其他 BLOB 传输输入参数一起发送到 Distributor 的固件分发服务器。固件分发服务器保存这些信息，并在响应状态消息给 Initiator 之前，为其 BLOB 传输服务器准备好接收传输。
#. Initiator 的 BLOB 传输客户端模型将固件镜像传输到 Distributor 的 BLOB 传输服务器，后者将镜像存储在预定的闪存分区中。

当 BLOB 传输完成时，固件镜像即可用于分发。Initiator 可以向 Distributor 上传多个固件镜像，并要求其按任意顺序或在任意时间分发。另有附加过程可用于查询和删除 Distributor 中的固件镜像。

以下与固件镜像相关的 Distributor 能力可通过配置选项设置：

* :kconfig:option:`CONFIG_BT_MESH_DFU_SLOT_CNT`：设备上可用的镜像槽数量。
* :kconfig:option:`CONFIG_BT_MESH_DFD_SRV_SLOT_MAX_SIZE`：每个镜像允许的最大大小。
* :kconfig:option:`CONFIG_BT_MESH_DFD_SRV_SLOT_SPACE`：所有镜像的可用空间。

填充 Distributor 的接收者列表
===========================================

在 Distributor 可以开始分发固件镜像之前，它需要一个 Target 节点列表以确定向哪些节点发送镜像。Initiator 通过直接查询潜在目标或通过某个外部权威机构获取完整的 Target 节点列表。Initiator 使用这些信息填充 Distributor 的接收者列表，其中包含每个 Target 节点的地址及相关固件镜像索引。Initiator 可以发送一条或多条 Firmware Distribution Receivers Add 消息来构建 Distributor 的接收者列表，并发送一条 Firmware Distribution Receivers Delete All 消息来清空该列表。

可以添加到 Distributor 的最大接收者数量通过 :kconfig:option:`CONFIG_BT_MESH_DFD_SRV_TARGETS_MAX` 配置选项设置。

发起分发
===========================

一旦 Distributor 已保存固件镜像并收到 Target 节点列表，Initiator 即可发起分发过程。用于分发的 BLOB 传输参数与更新策略一起传递给 Distributor。更新策略决定 Distributor 是否应请求在 Target 节点上应用固件。Distributor 保存传输参数，并开始将固件镜像分发给其 Target 节点列表。

固件分发
---------------------

Distributor 的 Firmware Update Client 模型使用其 BLOB 传输客户端模型的广播子系统与所有 Target 节点通信。固件分发按以下步骤执行：

1. Distributor 的 Firmware Update Client 模型生成 BLOB ID，并将其与其他 BLOB 传输参数、Target 节点固件镜像索引和固件镜像元数据一起发送到每个 Target 节点的 Firmware Update Server 模型。每个 Target 节点执行元数据检查，并为其 BLOB 传输服务器模型准备好传输，然后向 Firmware Update Client 发送状态响应，指示固件更新是否会影响该节点的蓝牙 Mesh 状态。
#. Distributor 的 BLOB 传输客户端模型将固件镜像传输到所有 Target 节点。
#. 一旦收到 BLOB 传输，Target 节点的应用通过对照镜像元数据执行签名验证或镜像校验和等检查，来验证固件是否有效。
#. Distributor 的 Firmware Update Client 模型查询所有 Target 节点，以确保它们都已验证固件镜像。

如果分发过程至少有一个 Target 节点报告已接收并验证镜像，则认为分发过程成功。

.. note::
   只有当*所有* Target 节点都丢失时，固件分发过程才会失败。Initiator 负责从 Distributor 请求失败的 Target 节点列表，并在当前尝试结束后发起额外尝试来更新丢失的 Target 节点。

暂停分发
---------------------------

Initiator 还可以请求 Distributor 暂停固件分发。在这种情况下，Distributor 将停止向 Target 节点发送任何消息。当固件分发恢复时，Distributor 将从最后一个成功传输的块继续发送固件。

应用固件镜像
===========================

如果 Initiator 提出请求，Distributor 可以针对所有成功接收并验证固件镜像的 Target 节点发起 Apply Firmware on Target Node 过程。Apply Firmware on Target Node 过程不接收参数，为避免歧义，它应在新传输发起之前执行。Apply Firmware on Target Node 过程包括以下步骤：

1. Distributor 的 Firmware Update Client 模型指示所有已验证固件镜像的 Target 节点应用该镜像。Target 节点的 Firmware Update Server 模型在调用应用 ``apply`` 回调之前，先响应一条状态消息。
#. Target 节点的应用执行应用传输前所需的任何准备工作，例如保存 Composition Data 快照或清除其配置。
#. Target 节点的应用将当前固件与新镜像交换，并用新的固件 ID 更新其固件镜像列表。
#. Distributor 的 Firmware Update Client 模型请求每个 Target 节点的完整固件镜像列表，并扫描该列表，确保新的固件 ID 已替换旧的。

.. note::
   在分发过程的元数据检查中，Target 节点可能报告在应用固件镜像后它将变为未配置状态。在这种情况下，Distributor 的 Firmware Update Client 模型将发送完整固件镜像列表请求，并预期没有响应。

取消分发
===========================

Initiator 可以在任意时间取消固件分发。在这种情况下，Distributor 通过向所有 Target 节点发送取消消息来启动取消过程。Distributor 等待所有 Target 节点的响应。一旦所有 Target 节点都已回复，或请求超时，分发过程即被取消。此后，可以从 ``Firmware distribution`` 部分重新开始分发过程。


API 参考
*************

本节列出设备固件更新 Mesh 模型共用的类型。

.. doxygengroup:: bt_mesh_dfd

.. doxygengroup:: bt_mesh_dfu

.. doxygengroup:: bt_mesh_dfu_metadata
