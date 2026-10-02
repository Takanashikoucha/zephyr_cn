.. _bluetooth_mesh_cfg:

Runtime Configuration
#####################

运行时配置 API 允许应用程序直接更改其运行时配置，而不通过 Configuration model。

Bluetooth Mesh 节点通常由带有 :ref:`bluetooth_mesh_models_cfg_cli` model 的中央网络配置器设备配置。每个 mesh 节点实例化一个 :ref:`bluetooth_mesh_models_cfg_srv` model，Configuration Client 可与该 model 通信以更改节点配置。在某些情况下，mesh 节点无法依赖 Configuration Client 检测或确定本地约束，例如低电量或拓扑变化。对于这些场景，可使用该 API 在本地更改配置。

.. note::
   节点配准之前的运行时配置更改不会存储在 :ref:`persistent storage <bluetooth_mesh_persistent_storage>` 中。

API reference
*************

.. doxygengroup:: bt_mesh_cfg