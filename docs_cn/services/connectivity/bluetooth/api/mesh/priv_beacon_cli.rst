.. _bluetooth_mesh_models_priv_beacon_cli:

私有信标客户端
#####################

私有信标客户端模型是蓝牙 Mesh 规范定义的基础模型。通过
:kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_CLI` 选项启用。

私有信标客户端模型引入于蓝牙 Mesh 协议规范
版本 1.1，提供配置 :ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的功能。

私有信标功能通过定期随机化信标输入数据为不同的蓝牙 Mesh 信标添加隐私。这保护
Mesh 节点不被 Mesh 网络外的设备跟踪，并隐藏
网络的 IV 索引、IV 更新和密钥刷新状态。

私有信标客户端模型使用目标节点的设备密钥与
:ref:`bluetooth_mesh_models_priv_beacon_srv` 模型通信。私有信标客户端模型可以与
其他节点上的服务器通信，或通过本地私有信标服务器模型进行自配置。

私有信标客户端 API 中的所有配置函数都以 ``net_idx``
和 ``addr`` 作为第一个参数。这些应设置为目标节点配置时使用的网络
索引和主单播地址。

如果存在，私有信标客户端模型只能实例化在主元素上。

API 参考
*************

.. doxygengroup:: bt_mesh_priv_beacon_cli
