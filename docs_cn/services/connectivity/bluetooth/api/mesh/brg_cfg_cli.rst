.. _bluetooth_mesh_models_brg_cfg_cli:

Bridge
Configuration
Client
###########################

Bridge
Configuration
Client
是
Bluetooth
Mesh
specification
定义
的
foundation
model。
该
model
是
optional
的
通过
:kconfig:option:`CONFIG_BT_MESH_BRG_CFG_CLI`
option
启用。

Bridge
Configuration
Client
model
提供
配置
包含
:ref:`bluetooth_mesh_models_brg_cfg_srv`
的
其他
Mesh
node
的
subnet
bridge
functionality
的
functionality。
包含
target
Bridge
Configuration
Server
的
node
的
device
key
用
于
access
layer
security。

如果
存在
Bridge
Configuration
Client
model
必须
只
在
primary
element
上
被
instantiated。

API
reference
*************

.. doxygengroup::
   bt_mesh_brg_cfg_cli
