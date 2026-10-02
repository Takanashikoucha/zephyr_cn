.. _bluetooth_mesh_sar_cfg_cli:

SAR 配置客户端
########################

SAR 配置客户端模型是由 Bluetooth Mesh 规范定义的基础模型。它是一个可选模型，通过 :kconfig:option:`CONFIG_BT_MESH_SAR_CFG_CLI` 配置选项启用。

SAR 配置客户端模型是在 Bluetooth Mesh 协议规范 1.1 版本中引入的，它支持对支持 :ref:`bluetooth_mesh_sar_cfg_srv` 模型的节点的较低传输层行为进行配置。

该模型可以发送消息，使用 SAR 配置消息查询或更改 SAR 配置服务器（SAR 发射器和 SAR 接收器）所支持的状态。

SAR 发射器流程用于确定并配置 SAR 配置服务器的 SAR 发射器状态。函数调用 :c:func:`bt_mesh_sar_cfg_cli_transmitter_get` 和 :c:func:`bt_mesh_sar_cfg_cli_transmitter_set` 分别用于获取和设置目标节点的 SAR 发射器状态。

SAR 接收器流程用于确定并配置 SAR 配置服务器的 SAR 接收器状态。函数调用 :c:func:`bt_mesh_sar_cfg_cli_receiver_get` 和 :c:func:`bt_mesh_sar_cfg_cli_receiver_set` 分别用于获取和设置目标节点的 SAR 接收器状态。

有关这两个状态的更多信息，请参见 :ref:`bt_mesh_sar_cfg_states`。

一个元素可以在任何时间发送任意 SAR 配置客户端消息，以查询或更改对等节点上 SAR 配置服务器模型所支持的状态。SAR 配置客户端模型仅接受使用支持 SAR 配置服务器模型的节点的设备密钥加密的消息。

如果存在，SAR 配置客户端模型仅可在主元素上实例化。

API 参考
*************

.. doxygengroup:: bt_mesh_sar_cfg_cli
