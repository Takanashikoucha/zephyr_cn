.. _bluetooth_mesh_models_cfg_srv:

Configuration
Server
####################

Configuration
Server
model
是
Bluetooth
Mesh
specification
定义
的
foundation
model。
Configuration
Server
model
控制
mesh
node
的
大多数
parameters。
它
没有
自己
的
API
但
依赖
:ref:`bluetooth_mesh_models_cfg_cli`
来
控制
它。

Configuration
Server
model
在
所有
Bluetooth
Mesh
nodes
上
是
mandatory
的
并
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
   bt_mesh_cfg_srv
