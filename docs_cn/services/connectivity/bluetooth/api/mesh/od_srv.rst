.. _bluetooth_mesh_od_srv:

按需私有代理服务器
##############################

按需私有代理服务器模型是蓝牙 Mesh 规范定义的基础模型。通过 :kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_SRV` 选项启用。

按需私有代理服务器模型引入于蓝牙 Mesh 协议规范
版本 1.1，支持通过管理其按需私有 GATT 代理状态来配置接收 Solicitation PDU 的节点的私有网络身份类型广播。

启用时，:ref:`bluetooth_mesh_srpl_srv` 也会启用。按需私有代理服务器
依赖于 :ref:`bluetooth_mesh_models_priv_beacon_srv` 存在于节点上。

按需私有代理服务器没有自己的 API，依赖于
:ref:`bluetooth_mesh_od_cli` 来控制。按需私有代理服务器模型只接受
使用节点设备密钥加密的消息。

如果存在，按需私有代理服务器模型只能实例化在主元素上。

API 参考
*************

.. doxygengroup:: bt_mesh_od_priv_proxy_srv
