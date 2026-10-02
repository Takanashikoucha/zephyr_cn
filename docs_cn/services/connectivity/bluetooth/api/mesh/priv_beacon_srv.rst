.. _bluetooth_mesh_models_priv_beacon_srv:

私有信标服务器
#####################

私有信标服务器模型是蓝牙 Mesh 规范定义的基础模型。通过
:kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_SRV` 选项启用。

私有信标服务器模型引入于蓝牙 Mesh 协议规范
版本 1.1，控制 Mesh 节点的私有信标状态、
私有 GATT 代理状态和私有节点身份状态。

私有信标功能通过定期随机化信标输入数据为不同的蓝牙 Mesh 信标添加隐私。这保护
Mesh 节点不被 Mesh 网络外的设备跟踪，并隐藏
网络的 IV 索引、IV 更新和密钥刷新状态。私有信标服务器
必须实例化才能使设备支持发送私有信标，
但节点可以在没有它的情况下处理接收的私有信标。

私有信标服务器没有自己的 API，但依赖于
:ref:`bluetooth_mesh_models_priv_beacon_cli` 来控制。私有信标
服务器模型只接受使用节点设备密钥加密的消息。

应用程序可以通过传递给
:c:macro:`BT_MESH_MODEL_PRIV_BEACON_SRV` 的 :c:struct:`bt_mesh_priv_beacon_srv` 实例配置私有信标
服务器模型的初始参数。注意，如果 Mesh 节点在设置子系统中存储了
对此配置的更改，初始值可能在加载时被覆盖。

如果存在，私有信标服务器模型只能实例化在主元素上。

API 参考
*************

.. doxygengroup:: bt_mesh_priv_beacon_srv
