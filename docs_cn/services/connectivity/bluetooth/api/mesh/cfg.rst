.. _bluetooth_mesh_cfg:

Runtime Configuration
#####################

Runtime configuration API 允许 applications 直接更改其 runtime configuration（而不通过 Configuration models。

Bluetooth Mesh nodes 通常由带 :ref:`bluetooth_mesh_models_cfg_cli` model 的 central network configurator device 配置。每个 mesh node 实例化 :ref:`bluetooth_mesh_models_cfg_srv` model（Configuration Client 可与其中通信以更改 node configuration。在某些情况下（mesh node 无法依赖 Configuration Client 检测或确定 local constraints（如低 battery 或 topology 变化。对这些 scenarios（此 API 可用于本地更改 configuration。

.. note::
   Node 被 provisioned 之前的 runtime configuration 更改不会存储在 :ref:`persistent storage <bluetooth_mesh_persistent_storage>` 中。

API reference
*************

.. doxygengroup:: bt_mesh_cfg
