.. _bluetooth_mesh_lcd_srv:

大型 Composition Data 服务器
#############################

大型 Composition Data 服务器模型是蓝牙 Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_LARGE_COMP_DATA_SRV` 选项启用。

大型 Composition Data 服务器模型引入于蓝牙 Mesh 协议规范版本 1.1，用于支持暴露无法容纳在 Config Composition Data Status 消息中的 Composition Data 页，以及暴露模型实例的元数据。

大型 Composition Data 服务器没有自己的 API，而是依赖 :ref:`bluetooth_mesh_lcd_cli` 来控制它。该模型仅接受使用节点设备密钥加密的消息。

如果存在，大型 Composition Data 服务器模型只能在主元素上实例化。

模型元数据
================

大型 Composition Data 服务器模型允许每个模型拥有一份模型特定元数据列表，可被大型 Composition Data 客户端模型读取。元数据列表可通过 :c:member:`bt_mesh_model.metadata` 字段与 :c:struct:`bt_mesh_model` 关联。元数据列表由一个或多个 :c:struct:`bt_mesh_models_metadata_entry` 结构定义的条目组成。每个条目包含元数据的长度和 ID，以及指向原始数据的指针。可使用 :c:macro:`BT_MESH_MODELS_METADATA_ENTRY` 宏创建条目。:c:macro:`BT_MESH_MODELS_METADATA_END` 宏标记元数据列表的结束，必须始终存在。如果模型没有元数据，可以使用辅助宏 :c:macro:`BT_MESH_MODELS_METADATA_NONE` 代替。

API 参考
*************

.. doxygengroup:: bt_mesh_large_comp_data_srv
