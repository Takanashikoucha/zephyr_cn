.. _bt_mesh_proxy:

代理
#####

代理（Proxy）功能允许手机等旧式设备通过 GATT 访问蓝牙 Mesh 网络。
只有设置 :kconfig:option:`CONFIG_BT_MESH_GATT_PROXY` 选项时，代理功能才会被编译。
代理功能的状态由 :ref:`bluetooth_mesh_models_cfg_srv` 控制，
初始值可通过 :c:member:`bt_mesh_cfg_srv.gatt_proxy` 设置。

启用代理功能的节点可以以 Network Identity 和 Node Identity 类型广播，
由 :ref:`bluetooth_mesh_models_cfg_cli` 控制。

GATT Proxy 状态表示是否支持代理功能。

私有代理
*************

支持代理功能和 :ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的节点
可以以 Private Network Identity 和 Private Node Identity 类型广播，
由 :ref:`bluetooth_mesh_models_priv_beacon_cli` 控制。通过以这组身份类型广播，
节点允许旧式设备通过 GATT 连接到网络，同时保持网络的隐私。

Private GATT Proxy 状态表示是否支持私有代理功能。

代理 Solicitation
******************

如果某节点上 GATT Proxy 和 Private GATT Proxy 状态均被禁用，旧式设备无法连接到该节点。
支持 :ref:`bluetooth_mesh_od_srv` 的节点可以被请求（solicited），
在不启用 Private GATT Proxy 状态的情况下广播可连接广播事件。
要请求该节点，旧式设备可以调用 :func:`bt_mesh_proxy_solicit` 函数
发送 Solicitation PDU。要启用该功能，设备必须编译时设置
:kconfig:option:`CONFIG_BT_MESH_PROXY_SOLICITATION` 选项。

Solicitation PDU 是非 Mesh、不可连接、无方向的广播消息，包含 Proxy Solicitation UUID，
并使用旧式设备想要连接到的子网的网络密钥加密。PDU 中包含旧式设备的源地址和序列号。
序列号由旧式设备维护，每发送一个新的 Solicitation PDU 时递增。

每个支持接收 Solicitation PDU 的节点都维护自己的 Solicitation Replay Protection List（SRPL）。
SRPL 通过存储节点已处理的有效 Solicitation PDU 的 solicitation 序列号（SSEQ）
和 solicitation 源（SSRC）对，保护 solicitation 机制免受重放攻击。
SRPL 更新与将变更存储到持久存储之间的延迟由
:kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 定义。

Solicitation PDU RPL 配置模型 :ref:`bluetooth_mesh_srpl_cli` 和
:ref:`bluetooth_mesh_srpl_srv` 提供保存和清除 SRPL 条目的功能。
支持 Solicitation PDU RPL 配置客户端模型的节点可以调用
:func:`bt_mesh_sol_pdu_rpl_clear` 函数清除目标节点 SRPL 的一部分。
Solicitation PDU RPL 配置客户端与服务器之间的通信使用 application key 加密，
因此 Solicitation PDU RPL 配置客户端可以实例化在网络中的任意设备上。

当节点收到 Solicitation PDU 并成功认证后，它会开始以 Private Network Identity 类型
广播可连接广播。广播时长可由按需私有代理客户端模型配置。

API 参考
*************

.. doxygengroup:: bt_mesh_proxy
