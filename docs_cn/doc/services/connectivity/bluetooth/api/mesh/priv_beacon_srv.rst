.. _bluetooth_mesh_models_priv_beacon_srv:

私有信标服务器
#####################

私有信标服务器模型是蓝牙 Mesh 规范定义的基础模型。该模型通过
:kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_SRV` 选项启用。

私有信标服务器模型在蓝牙 Mesh 协议规范 1.1 版中引入，用于控制 Mesh 节点的
私有信标状态、私有 GATT 代理状态和私有节点身份状态。

私有信标功能通过周期性随机化信标输入数据，为不同的蓝牙 Mesh 信标增加隐私保护。
这可防止 Mesh 节点被 Mesh 网络外的设备跟踪，并隐藏网络的 IV index、IV update
和 Key Refresh 状态。要支持发送私有信标，必须实例化私有信标服务器，
但即使没有该模型，节点也会处理接收到的私有信标。

私有信标服务器没有自己的 API，依赖 :ref:`bluetooth_mesh_models_priv_beacon_cli`
来控制它。私有信标服务器模型只接受使用节点 device key 加密的消息。

应用程序可通过传递给 :c:macro:`BT_MESH_MODEL_PRIV_BEACON_SRV` 的
:c:struct:`bt_mesh_priv_beacon_srv` 实例来配置私有信标服务器模型的初始参数。
需要注意的是，如果 Mesh 节点将对此配置的修改存储到了设置子系统，
初始值在加载时可能会被覆盖。

如果存在，私有信标服务器模型只能实例化在主元素上。

API 参考
*************

.. doxygengroup:: bt_mesh_priv_beacon_srv
