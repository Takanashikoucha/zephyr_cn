.. _bluetooth_mesh_lcd_cli:

大型 Composition Data 客户端
#############################

大型 Composition Data 客户端模型是蓝牙 Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_LARGE_COMP_DATA_CLI` 选项启用。

大型 Composition Data 客户端模型引入于蓝牙 Mesh 协议规范版本 1.1，支持读取无法容纳在 Config Composition Data Status 消息中的 Composition Data 页，以及读取支持 :ref:`bluetooth_mesh_lcd_srv` 模型的节点上模型实例的元数据。

大型 Composition Data 客户端模型使用包含目标大型 Composition Data 服务器模型实例的节点的设备密钥与大型 Composition Data 服务器模型通信。

如果存在，大型 Composition Data 客户端模型只能在主元素上实例化。

API 参考
*************

.. doxygengroup:: bt_mesh_large_comp_data_cli
