.. _bluetooth_mesh_models_op_agg_cli:

操作码聚合器客户端
#########################

操作码聚合器客户端模型是蓝牙 Mesh 规范定义的基础模型。该模型为可选项，
通过 :kconfig:option:`CONFIG_BT_MESH_OP_AGG_CLI` 选项启用。

操作码聚合器客户端模型在蓝牙 Mesh 协议规范 1.1 版中引入，用于支持向支持
:ref:`bluetooth_mesh_models_op_agg_srv` 模型的节点分发一系列访问层消息的功能。

操作码聚合器客户端模型使用目标节点的 device key 或配置客户端配置的 application key，
与操作码聚合器服务器模型进行通信。

如果存在，操作码聚合器客户端模型只能实例化在主元素上。

操作码聚合器客户端模型在初始化时隐式绑定到 device key。它应绑定到与用于生成
该系列消息的客户端模型相同的 application key。

要能够聚合来自客户端模型的消息，该客户端模型应支持异步 API，例如通过回调实现。

API 参考
*************

.. doxygengroup:: bt_mesh_op_agg_cli
