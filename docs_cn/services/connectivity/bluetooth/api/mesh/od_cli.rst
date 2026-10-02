.. _bluetooth_mesh_od_cli:

按需私有代理客户端
##############################

按需私有代理客户端模型是蓝牙 Mesh 规范定义的基础模型。该模型是可选的，通过
:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI` 选项启用。

按需私有代理客户端模型引入于蓝牙 Mesh 协议规范
版本 1.1，用于设置和获取按需私有 GATT 代理状态。该状态
定义了节点在接收 Solicitation PDU 后广播 Mesh 代理服务（私有网络身份类型）的持续时间。

按需私有代理客户端模型使用包含目标按需私有代理服务器模型
实例的节点的设备密钥与按需私有代理服务器模型通信。

如果存在，按需私有代理客户端模型只能实例化在主元素上。

配置
**************

按需私有代理客户端模型行为可通过传输超时选项
:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI_TIMEOUT` 配置。
:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI_TIMEOUT` 控制客户端等待状态响应消息到达的毫秒数。该值可在运行时通过
:c:func:`bt_mesh_od_priv_proxy_cli_timeout_set` 更改。


API 参考
*************

.. doxygengroup:: bt_mesh_od_priv_proxy_cli
