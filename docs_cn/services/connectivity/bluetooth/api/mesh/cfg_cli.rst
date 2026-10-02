.. _bluetooth_mesh_models_cfg_cli:

Configuration Client
####################

Configuration Client model 是由 Bluetooth Mesh 规范定义的基础 model。它提供配置 mesh 节点大多数参数的功能，包括加密密钥、model 配置和功能启用。

Configuration Client model 使用目标节点的设备密钥与 :ref:`bluetooth_mesh_models_cfg_srv` model 通信。Configuration Client model 可与其他节点上的 server 通信，或通过本地 Configuration Server model 进行自配置。

Configuration Client API 中的所有配置函数都以 ``net_idx`` 和 ``addr`` 作为其第一个参数。这些参数应设置为目标节点配准时所使用的网络索引和主单播地址。

Configuration Client model 是可选的，如果存在于 Composition Data 中，则只能在主 element 上实例化。

API reference
*************

.. doxygengroup:: bt_mesh_cfg_cli