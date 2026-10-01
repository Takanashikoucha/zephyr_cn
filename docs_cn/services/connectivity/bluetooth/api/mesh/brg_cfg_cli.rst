.. _bluetooth_mesh_models_brg_cfg_cli:

Bridge Configuration Client
###########################

Bridge Configuration Client 是 Bluetooth Mesh specification 定义的 foundation model。该 model 为 optional（通过 :kconfig:option:`CONFIG_BT_MESH_BRG_CFG_CLI` option 启用。

Bridge Configuration Client model 提供配置另一个包含 :ref:`bluetooth_mesh_models_brg_cfg_srv` 的 Mesh node 的 subnet bridge 功能的功能。包含 target Bridge Configuration Server 的 node 的 device key 用于 access layer security。

若存在（Bridge Configuration Client model 仅须实例化在 primary element 上。

API reference
*************

.. doxygengroup:: bt_mesh_brg_cfg_cli
