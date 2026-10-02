.. _bluetooth_mesh_models_brg_cfg_srv:

Bridge Configuration Server
###########################

Bridge Configuration Server model 是由 Bluetooth Mesh 规范定义的基础 model。它是一个可选 model，通过配置项 :kconfig:option:`CONFIG_BT_MESH_BRG_CFG_SRV` 启用。该 model 扩展 :ref:`bluetooth_mesh_models_cfg_srv` model。

Bridge Configuration Server model 在 Bluetooth Mesh Protocol Specification 版本 1.1 中引入，用于支持和配置 Subnet Bridge 功能。

Bridge Configuration Server model 依赖 :ref:`bluetooth_mesh_models_brg_cfg_cli` 进行配置。Bridge Configuration Server model 只接受使用节点设备密钥加密的消息。

如果存在，Bridge Configuration Server model 必须在主 element 上实例化。

Bridge Configuration Server model 提供对以下三个状态的访问：

* Subnet Bridge
* Bridging Table
* Bridging Table Size

有关这些状态的更多信息，参见 :ref:`bluetooth_mesh_brg_cfg_states`。

API reference
*************

.. doxygengroup:: bt_mesh_brg_cfg_srv