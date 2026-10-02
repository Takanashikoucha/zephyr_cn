.. _bluetooth_mesh_srpl_cli:

Solicitation PDU RPL 配置客户端
#########################################

Solicitation PDU RPL 配置客户端模型是由 Bluetooth Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI` 选项启用。

Solicitation PDU RPL 配置客户端模型是在 Bluetooth Mesh 协议规范 1.1 版本中引入的，它支持从支持 :ref:`bluetooth_mesh_srpl_srv` 模型的节点的 solicitation 重放保护列表（SRPL）中移除地址的功能。

Solicitation PDU RPL 配置客户端模型使用由 Configuration Client 配置的应用密钥与 Solicitation PDU RPL 配置服务器模型进行通信。

如果存在，Solicitation PDU RPL 配置客户端模型仅可在主元素上实例化。

配置
**************

Solicitation PDU RPL 配置客户端模型的行为可通过发送超时选项 :kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI_TIMEOUT` 进行配置。:kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI_TIMEOUT` 以毫秒为单位控制 Solicitation PDU RPL 配置客户端等待响应消息到达的时间。该值可在运行时使用 :c:func:`bt_mesh_sol_pdu_rpl_cli_timeout_set` 更改。

API 参考
*************

.. doxygengroup:: bt_mesh_sol_pdu_rpl_cli
