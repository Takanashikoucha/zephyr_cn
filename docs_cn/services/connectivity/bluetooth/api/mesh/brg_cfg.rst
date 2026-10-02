.. _bluetooth_mesh_brg_cfg:

Subnet Bridge
#############

随着 Bluetooth Mesh Protocol Specification 版本 1.1 的发布，引入了 Bluetooth Mesh Subnet Bridge 功能。
该功能允许 mesh 网络使用子网进行区域隔离，同时允许不同相邻子网中的特定设备之间进行通信，而不损害安全性。

Bluetooth Mesh Subnet Bridge 功能使网络中选定的节点能够充当 Subnet Bridge，通过在相邻子网中的节点之间中继消息实现受控通信。

Subnet Bridge 功能包含两个 model：

- :ref:`bluetooth_mesh_models_brg_cfg_srv`
- :ref:`bluetooth_mesh_models_brg_cfg_cli`

Bridge Configuration Server model 是支持 Subnet Bridge 功能的必选项。
Bridge Configuration Client model 是可选项，允许节点配置其他节点上的 Subnet Bridge。
这些 model 定义了配置和管理 Subnet Bridge 功能所需的必要状态、消息和行为。

Subnet Bridge 功能的配置和管理通过 Bridge Configuration Server 和 Client model 处理。
实现 Bridge Configuration Client model 的节点可以充当 Subnet Bridge 功能的 *Configuration Manager*。

Concepts
********

为了更好地理解 Subnet Bridge 功能及其能力，需要概述几个概念。

Subnet
======

子网是 mesh 网络中共享一个公共网络密钥的一组节点，使它们能够在网络层安全通信。
每个子网独立运行，节点仅在该组内交换消息。
一个节点可同时属于多个子网。

Subnet Bridge node
==================

Subnet Bridge 节点是 Bluetooth Mesh 网络中属于多个子网并启用 Subnet Bridge 功能的节点。只有此类节点可以执行子网桥接。Subnet Bridge 节点连接子网，并通过在子网组之间中继消息允许它们之间通信。

Subnet Bridge 节点有一个主 subnet，基于主 NetKey，负责处理 IV Update 流程，并将更新传播到其他子网。
在其上中继消息的次级子网被称为 *bridged subnets*。

Bridging Table
==============

Bridging Table 包含该节点桥接的子网条目，并由 Bridge Configuration Server model 管理。

Bridging Table 中条目的最大数量由 :kconfig:option:`CONFIG_BT_MESH_BRG_TABLE_ITEMS_MAX` 选项定义，默认值为最小值 16，最大可能大小为 255。

Enabling or disabling the Subnet Bridge feature
***********************************************

Bridge Configuration Client（或 Configuration Manager）可通过向目标节点上的 Bridge Configuration Server model 发送 **Subnet Bridge Set** 消息来启用或禁用节点上的 Subnet Bridge 功能，使用 :c:func:`bt_mesh_brg_cfg_cli_set` 函数。

Adding or removing subnets
**************************

Bridge Configuration Client 可通过向目标节点上的 Bridge Configuration Server model 发送 **Bridging Table Add** 或 **Bridging Table Remove** 消息，调用 :c:func:`bt_mesh_brg_cfg_cli_table_add` 或 :c:func:`bt_mesh_brg_cfg_cli_table_remove` 函数，从 Bridging Table 中添加或删除条目。

.. _bluetooth_mesh_brg_cfg_states:

Subnet Bridge states
********************

Subnet Bridge 具有以下状态：

- *Subnet Bridge*：该状态指示节点上的 Subnet Bridge 功能是启用还是禁用。
  Bridge Configuration Client 可通过向 Bridge Configuration Server 发送 **Subnet Bridge Get** 消息并使用 :c:func:`bt_mesh_brg_cfg_cli_get` 函数获取此信息。

- *Bridging Table*：该状态保存 bridging table。Client 可通过向目标节点发送 **Bridging Table Get** 消息并使用 :c:func:`bt_mesh_brg_cfg_cli_table_get` 函数，请求 Bridging Table 中的条目列表。

  Client 可通过调用 :c:func:`bt_mesh_brg_cfg_cli_subnets_get` 函数向目标 Server 发送 **Bridged Subnets Get** 消息，获取当前由 Subnet Bridge 桥接的子网列表。

- *Bridging Table Size*：该状态报告 Bridging Table 可存储的最大条目数。Client 可通过发送 **Bridging Table Size Get** 消息并使用 :c:func:`bt_mesh_brg_cfg_cli_table_size_get` 函数获取此信息。
  这是一个只读状态。

Subnet bridging and replay protection
*************************************

Subnet Bridge 功能启用子网之间的消息中继，需要有效的重放保护以确保网络安全。需要考虑的关键要点如下所述。

Relay buffer considerations
===========================

当消息由 Subnet Bridge 在子网之间中继时，它从 relay 缓冲区池分配。relay 缓冲区数量可使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_RELAY_BUF_COUNT` 配置。

当启用 :kconfig:option:`CONFIG_BT_MESH_ADV_EXT` 时，消息将通过 relay 广播集传输。广播集数量可使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_RELAY_ADV_SETS` 配置。

即使禁用了 relay 功能 :kconfig:option:`CONFIG_BT_MESH_RELAY`，relay 缓冲区池和广播集仍可使用。

Replay protection and Bridging Table
===================================

Subnet Bridge 节点必须为所有发往被桥接子网的 Access 和 Transport Control 消息实现重放保护。

Replay Protection List（RPL）与 Bridging Table 协同工作以确保安全性：

- Subnet Bridge 为每个被授权向被桥接子网发送消息的源地址存储最新的 IVISeq。

- IVISeq 小于或等于已存储值的消息被丢弃，而有效消息在转发前更新已存储的 IVISeq。

为确保正确运行，RPL 和 Bridging Table 必须保持同步，因为每条被桥接的消息在转发前都必须通过重放保护机制。

.. note::

   RPL 大小应随 Bridging Table 扩展。随着被桥接子网数量增加，必须跟踪更多源地址和 IVISeq 值，需要更大的 RPL 才能保持有效的重放保护。

Subnet Bridge and Directed Forwarding
*************************************

Bluetooth Mesh Directed Forwarding（MDF）通过优化中继路径，实现跨子网节点之间的高效路由。虽然 MDF 可通过处理路径发现和转发来增强 Subnet Bridging，但当前实现不支持该功能。

API reference
*************

本节包含 Bridge Configuration model 共用的类型和定义。

.. doxygengroup:: bt_mesh_brg_cfg