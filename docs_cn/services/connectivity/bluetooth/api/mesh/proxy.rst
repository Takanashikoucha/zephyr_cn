.. _bt_mesh_proxy:

代理
#####

代理功能允许手机等遗留设备通过
GATT 访问蓝牙 Mesh 网络。只有当 :kconfig:option:`CONFIG_BT_MESH_GATT_PROXY`
选项设置时才编译代理功能。代理功能状态由 :ref:`bluetooth_mesh_models_cfg_srv` 控制，
初始值可通过 :c:member:`bt_mesh_cfg_srv.gatt_proxy` 设置。

启用代理功能的节点可以使用网络身份和节点身份广播，
由 :ref:`bluetooth_mesh_models_cfg_cli` 控制。

GATT 代理状态表示是否支持代理功能。

私有代理
*************

支持代理功能和 :ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的节点
可以使用私有网络身份和私有节点身份类型广播，
由 :ref:`bluetooth_mesh_models_priv_beacon_cli` 控制。通过使用该组身份类型广播，
节点允许遗留设备通过 GATT 连接到网络，同时保持
网络的隐私。

私有 GATT 代理状态表示是否支持私有代理功能。

代理 Solicitation
******************

在 GATT 代理和私有 GATT 代理状态在节点上均禁用的情况下，
遗留设备无法连接到该节点。支持 :ref:`bluetooth_mesh_od_srv` 的节点
可以接受 solicitation 以广播可连接广告事件，而无需启用私有 GATT 代理状态。
要 solicitation 节点，遗留设备可以通过调用
:func:`bt_mesh_proxy_solicit` 函数发送 Solicitation PDU。要启用此功能，设备必须以
:kconfig:option:`CONFIG_BT_MESH_PROXY_SOLICITATION` 选项设置进行编译。

Solicitation PDU 是非 Mesh、不可连接、无方向广告消息，
包含 Proxy Solicitation UUID，使用遗留设备想要
连接到的子网的网络密钥加密。PDU 包含遗留设备的源地址和序列号。
序列号由遗留设备维护，每发送一个新的 Solicitation PDU
递增。

每个支持接收 Solicitation PDU 的节点持有自己的 Solicitation 重放保护
列表（SRPL）。SRPL 通过存储节点处理的有效 Solicitation PDU
的 solicitation 序列号（SSEQ）和 solicitation 源（SSRC）对来保护 solicitation 机制免受重放攻击。
更新 SRPL 和将更改存储到持久存储之间的延迟由 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 定义。

Solicitation PDU RPL 配置模型，:ref:`bluetooth_mesh_srpl_cli` 和
:ref:`bluetooth_mesh_srpl_srv`，提供保存和清除 SRPL 条目的功能。
支持 Solicitation PDU RPL 配置客户端模型的节点可以通过调用 :func:`bt_mesh_sol_pdu_rpl_clear` 函数
清除目标上 SRPL 的一部分。Solicitation PDU RPL 配置客户端和服务器之间的通信使用应用密钥加密，
因此，Solicitation PDU RPL 配置客户端可以实例化在
网络中的任何设备上。

当节点接收 Solicitation PDU 并成功认证时，
它将开始使用私有网络身份类型广播可连接广告。
广告持续时间可由按需私有代理客户端模型配置。

API 参考
*************

.. doxygengroup:: bt_mesh_proxy
