.. _bluetooth_mesh_models_priv_beacon_cli:

私有信标客户端
#####################

私有信标客户端模型是蓝牙 Mesh 规范定义的基础模型。该模型通过
:kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_CLI` 选项启用。

私有信标客户端模型在蓝牙 Mesh 协议规范 1.1 版中引入，提供用于配置
:ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的功能。

私有信标功能通过周期性随机化信标输入数据，为不同的蓝牙 Mesh 信标增加隐私保护。
这可防止 Mesh 节点被 Mesh 网络外的设备跟踪，并隐藏网络的 IV index、IV update
和 Key Refresh 状态。

私有信标客户端模型使用目标节点的 device key 与 :ref:`bluetooth_mesh_models_priv_beacon_srv`
模型进行通信。私有信标客户端模型可以与其它节点上的服务器通信，
也可以通过本地私有信标服务器模型进行自配置。

私有信标客户端 API 中的所有配置函数都以 ``net_idx`` 和 ``addr`` 作为第一个参数。
这些值应设置为目标节点在配置时使用的网络索引和主单播地址。

如果存在，私有信标客户端模型只能实例化在主元素上。

API 参考
*************

.. doxygengroup:: bt_mesh_priv_beacon_cli
