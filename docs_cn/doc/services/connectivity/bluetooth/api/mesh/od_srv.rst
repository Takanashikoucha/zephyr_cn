.. _bluetooth_mesh_od_srv:

按需私有代理服务器
##############################

按需私有代理服务器模型是蓝牙 Mesh 规范定义的基础模型。该模型通过
:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_SRV` 选项启用。

按需私有代理服务器模型在蓝牙 Mesh 协议规范 1.1 版中引入，用于通过管理其按需私有 GATT 代理状态，
支持配置作为 Solicitation PDU 接收方的节点以私有网络身份类型进行广播。

启用后，:ref:`bluetooth_mesh_srpl_srv` 也会同时启用。按需私有代理服务器依赖于
:ref:`bluetooth_mesh_models_priv_beacon_srv` 存在于该节点上。

按需私有代理服务器没有自己的 API，依赖 :ref:`bluetooth_mesh_od_cli` 来控制它。
按需私有代理服务器模型只接受使用节点 device key 加密的消息。

如果存在，按需私有代理服务器模型只能实例化在主元素上。

API 参考
*************

.. doxygengroup:: bt_mesh_od_priv_proxy_srv
