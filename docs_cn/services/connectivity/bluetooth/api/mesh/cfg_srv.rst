.. _bluetooth_mesh_models_cfg_srv:

Configuration Server
####################

Configuration Server model 是 Bluetooth Mesh specification 定义的 foundation model。Configuration Server model 控制 mesh node 的大多数 parameters。它没有自己的 API（但依赖 :ref:`bluetooth_mesh_models_cfg_cli` 控制它。

Configuration Server model 在所有 Bluetooth Mesh nodes 上为 mandatory（且仅须实例化在 primary element 上。

API reference
*************

.. doxygengroup:: bt_mesh_cfg_srv
