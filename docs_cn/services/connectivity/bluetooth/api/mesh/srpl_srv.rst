.. _bluetooth_mesh_srpl_srv:

Solicitation PDU RPL 配置服务器
#########################################

Solicitation PDU RPL 配置服务器模型是由 Bluetooth Mesh 规范定义的基础模型。如果节点启用了 :ref:`bluetooth_mesh_od_srv`，则该模型被启用。

Solicitation PDU RPL 配置服务器模型是在 Bluetooth Mesh 协议规范 1.1 版本中引入的，它管理保存在设备上的 Solicitation 重放保护列表（SRPL）。SRPL 用于拒绝节点已经处理过的 Solicitation PDU。当一条有效的 Solicitation PDU 消息被节点成功处理后，该消息的 SSRC 字段和 SSEQ 字段会被存储在节点的 SRPL 中。

Solicitation PDU RPL 配置服务器没有自己的 API，而是依赖 :ref:`bluetooth_mesh_srpl_cli` 对其进行控制。该模型仅接受使用由 Configuration Client 配置的应用密钥加密的消息。

如果存在，Solicitation PDU RPL 配置服务器模型仅可在主元素上实例化。

配置
**************

对于 Solicitation PDU RPL 配置服务器模型，可配置 :kconfig:option:`CONFIG_BT_MESH_PROXY_SRPL_SIZE` 选项以设置 SRPL 的大小。

API 参考
*************

.. doxygengroup:: bt_mesh_sol_pdu_rpl_srv
