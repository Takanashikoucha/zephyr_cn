.. _vulnerabilities:

Vulnerabilities
###############

本页面汇总了在每次发布中已发现并修复的所有漏洞。
此处通常比发布说明包含更多细节。某些漏洞被认为
敏感，在修复前有足够时间之前不会公开讨论。由于
发布说明被锁定到某个版本，保密期（embargo）解除后
本处的信息仍可更新。

往年的漏洞汇总在单独的页面中：

.. toctree::
   :maxdepth: 1

   vulnerabilities/2017
   vulnerabilities/2019
   vulnerabilities/2020
   vulnerabilities/2021
   vulnerabilities/2022
   vulnerabilities/2023
   vulnerabilities/2024
   vulnerabilities/2025

CVE-2026
========

:cve:`2026-0849`
----------------

crypto: ATAES132A 响应长度导致栈缓冲区溢出

长度字段过大的畸形 ATAES132A 响应会使 Zephyr 加密驱动中
一个 52 字节的栈缓冲区溢出，使被入侵的设备或总线攻击者
能够破坏内核内存，并可能劫持执行。

- `Zephyr 项目缺陷跟踪器 GHSA-ff4p-3ggg-prp6
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-ff4p-3ggg-prp6>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 103163 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/103163>`_

:cve:`2026-1677`
----------------

net: 在 TLS 1.3 套接字上允许 TLS 1.2 连接

使用 ``IPPROTO_TLS_1_3`` 创建的 Zephyr 套接字，在 Kconfig
中同时启用两个 TLS 版本时，仍可能协商出 TLS 1.2 连接，
因为套接字层的协议选择未被传递到 mbedTLS（例如通过
``mbedtls_ssl_conf_min_tls_version``）。ClientHello 会同时
通告两个版本，对端可建立 TLS 1.2 连接，因此假定
``IPPROTO_TLS_1_3`` 强制使用 TLS 1.3 的应用可能静默地
退化为 TLS 1.2，从而继续暴露于 TLS 1.2 特有的弱点。

- `Zephyr 项目缺陷跟踪器 GHSA-23r2-m5wx-4rvq
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-23r2-m5wx-4rvq>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 102570 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/102570>`_


:cve:`2026-1678`
----------------

dns: DNS 名称解析器中的内存安全问题

``dns_unpack_name()`` 在追加 DNS 标签时一次性缓存缓冲区的剩余空间
并复用。随着缓冲区增长，缓存的大小变得不正确，最终的
空终止符可能被写到缓冲区之外。在断言被禁用（默认）时，
恶意 DNS 响应可在启用 ``CONFIG_DNS_RESOLVER`` 的情况下
触发越界写入。


- `Zephyr 项目缺陷跟踪器 GHSA-536f-h63g-hj42
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-536f-h63g-hj42>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 99683 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/99683>`_

- `PR 99830 4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/99830>`_

- `PR 99829 4.2 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/99829>`_

- `PR 99828 3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/99828>`_

:cve:`2026-1679`
----------------

eswifi 套接字卸载驱动将用户提供的负载拷贝到固定缓冲区时
未检查可用空间；过大的发送会使 eswifi->buf 溢出，
破坏内核内存（CWE-120）。利用需要能够调用套接字
发送 API 的本地代码；远程攻击者无法直接触达。

- `Zephyr 项目缺陷跟踪器 GHSA-qx3g-5g22-fq5w
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qx3g-5g22-fq5w>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 102119 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/102119>`_

:cve:`2026-1681`
----------------

net: 通过 Shell 对自身 IP 地址 Ping 导致栈溢出

通过 ``net ping`` shell 命令向设备自身的 IPv4 地址发起
ICMP ping 时，网络栈会在同一个系统工作队列栈上
递归地重新进入输入路径。由于目标被识别为本地地址，
echo 请求与产生的 echo 应答都在当前帧返回之前
内联处理。嵌套的输入路径帧超出工作队列栈并
触发栈溢出。

- `Zephyr 项目缺陷跟踪器 GHSA-6fcc-8rwr-w7xx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6fcc-8rwr-w7xx>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 102268 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/102268>`_

:cve:`2026-4179`
----------------

stm32: usb: 中断处理程序中的无限 while 循环

stm32 USB 设备驱动中的问题可导致无限 while 循环。

- `Zephyr 项目缺陷跟踪器 GHSA-9xg7-g3q3-9prf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9xg7-g3q3-9prf>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104390 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104390>`_

:cve:`2026-5066`
----------------

net: sockets: tls: socket_op_vtable::connect 函数中潜在的越界写入/读取

网络套接字子系统（``subsys/net/lib/sockets/sockets_tls.c``）的
TLS 套接字连接路径中存在潜在的越界写入/读取。当启用
TLS 会话缓存时，``tls_session_store()`` 与 ``tls_session_restore()``
使用调用者控制的 ``addrlen`` 值将调用者提供的地址 ``memcpy``
到一个固定大小的缓冲区，而未将其与目标大小进行校验。
由于 ``struct net_sockaddr`` 是不透明类型，应用可以传入
大于 ``sizeof(struct net_sockaddr)`` 的 ``addrlen``（例如
将 128 字节拷入 24 字节的栈缓冲区），导致 ``memcpy``
读取并写入超出 TLS 会话缓存所用地址内存的末尾。
这可能导致崩溃与拒绝服务，并可能引发任意代码执行。

- `Zephyr 项目缺陷跟踪器 GHSA-wgrc-jrf6-24f3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wgrc-jrf6-24f3>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104871 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104871>`_

- `PR 105044 4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/105044>`_

- `PR 105043 4.2 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/105043>`_

- `PR 105042 3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/105042>`_

:cve:`2026-5067`
----------------

HTTP WebSocket 升级中通过非空终止的 Sec-WebSocket-Key
导致越界读取/写入

远程、未认证的发送者可通过发送一个构造的
``Sec-WebSocket-Key`` 头触发 Zephyr HTTP 服务器
WebSocket 升级路径中的内存破坏：该头被拷贝时
不保证 NUL 终止，随后被传给 ``strlen()``。
这可能导致栈内存的越界读取与越界写入，
导致崩溃（拒绝服务）并可能引发代码执行。
当启用 ``CONFIG_HTTP_SERVER_WEBSOCKET`` 时该路径可达。

- `Zephyr 项目缺陷跟踪器 GHSA-wgr4-9pwq-94vj
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wgr4-9pwq-94vj>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104740 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104740>`_

- `PR 107927 4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107927>`_

- `PR 107926 3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107926>`_

:cve:`2026-5068`
----------------

Bluetooth: L2CAP LE CoC：通过存储在 net_buf user_data 中的
分段计数器触发远程越界写入

远程、未认证的 BLE 对端可在 L2CAP LE CoC SDU 重组期间
触发 Bluetooth 主机中 2 字节的越界写入。当应用启用
分段（通过 ``chan_ops.alloc_buf``）且所选 RX 池的
``user_data_size`` 小于 2 字节时，存储在 ``net_buf``
user_data 区域的分段计数器会在 ``l2cap_chan_le_recv_seg``
（``subsys/bluetooth/host/l2cap.c``）中越界写入。
这可能导致堆破坏与致命错误。

- `Zephyr 项目缺陷跟踪器 GHSA-qrcq-hxwj-mqxm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qrcq-hxwj-mqxm>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104913 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104913>`_

- `PR 108335 4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108335>`_

- `PR 108336 3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108336>`_

:cve:`2026-5071`
----------------

can: 通过 SocketCAN 发送触发本地拒绝服务

SocketCAN 发送路径（``zcan_sendto_ctx``）使用 ``NET_ASSERT``
而非真正的运行时检查来校验调用者提供的缓冲区长度。
在断言被编译掉的发布构建中，用户空间应用可以传入
短于 ``struct socketcan_frame`` 的缓冲区，
``socketcan_to_can_frame()`` 会解引用该缓冲区末尾之外的
字段——一次越界读取，可能使系统崩溃（本地 DoS），
并且由于解析出的帧随后被发送出去，还可能泄露相邻内存。

- `Zephyr 项目缺陷跟踪器 GHSA-c3w6-x7m3-3c58
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c3w6-x7m3-3c58>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104654 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104654>`_

- `PR 104679 4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104679>`_

- `PR 104678 4.2 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104678>`_

- `PR 104677 3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104677>`_

:cve:`2026-5072`
----------------

net: ptp: 通过 PTP 间隔移位触发潜在拒绝服务

一个按位移位漏洞允许远程攻击者通过发送一个包含
大的、未校验的负 log_announce_interval 的构造
PTP Management 或 Delay Response 报文，在 PTP 子系统中
导致未定义行为与潜在崩溃，该值被用于按位移位操作。

- `Zephyr 项目缺陷跟踪器 GHSA-3v98-458v-388r
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3v98-458v-388r>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104613 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104613>`_

- `PR 108337 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108337>`_

- `PR 108338 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108338>`_

:cve:`2026-5589`
----------------

Bluetooth: Mesh：整数下溢导致的越界写入

Bluetooth Mesh 请求处理（``subsys/bluetooth/mesh/solicitation.c``）
中 ``bt_mesh_sol_recv()`` 的整数下溢导致越界写入。
当启用 ``CONFIG_BT_MESH_OD_PRIV_PROXY_SRV`` 时，
该函数从原始 BLE 广告负载中解析请求 PDU。
AD 解析循环读取一个攻击者控制的长度字节，
并计算 ``reported_len - 3``，而未检查 ``reported_len``
是否至少为 3。当该值更小时，有符号减法产生一个
负数，绕过长度保护，随后被隐式转换为一个非常大的
``size_t``，使缓冲区指针前进到远超边界的位置，
后续读取解引用无效内存。附近的 BLE 设备可通过携带
一个 UUID16 AD 结构与构造长度字节的不可连接广告
触发该漏洞，无需配对或先前关联，可能导致拒绝服务
或任意代码执行。

- `Zephyr 项目缺陷跟踪器 GHSA-4pm9-4v7f-x6gr
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4pm9-4v7f-x6gr>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 105585 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/105585>`_

- `PR 108334 4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108334>`_

- `PR 108333 3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108333>`_

:cve:`2026-5590`
----------------

net: ip/tcp: 竞态条件可触发空指针解引用

TCP 连接拆除期间的竞态条件可能导致 tcp_recv() 操作一个
已被释放的连接。如果在处理 SYN 报文时 tcp_conn_search()
返回 NULL，则从过期上下文数据派生的空指针被传给
tcp_backlog_is_full() 并在未校验的情况下被解引用，
导致崩溃。

- `Zephyr 项目缺陷跟踪器 GHSA-4vqm-pw24-g9jp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4vqm-pw24-g9jp>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 102110 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/102110>`_

:cve:`2026-8718`
----------------

Zephyr net sockets/TLS 中 DTLS 对端 Connection ID getsockopt
（``TLS_DTLS_PEER_CID_VALUE``）的越界写入

``subsys/net/lib/sockets/sockets_tls.c`` 中处理
``getsockopt(SOL_TLS, TLS_DTLS_PEER_CID_VALUE)`` 的
``tls_opt_dtls_peer_connection_id_value_get()``，
将调用者提供的 ``optval`` 直接传给
``mbedtls_ssl_get_peer_cid()``，而未校验缓冲区
是否至少为 ``MBEDTLS_SSL_CID_OUT_LEN_MAX``（默认 32）字节。
``mbedtls_ssl_get_peer_cid()`` 将对端协商的 DTLS
Connection ID（长度 1..``MBEDTLS_SSL_CID_OUT_LEN_MAX``）
拷贝到该缓冲区，没有目标大小参数，因此调用者提供的
``optlen`` 小于 CID 长度时，会导致最多 31 字节的写入
越过缓冲区末尾。

在 ``CONFIG_USERSPACE`` 构建中，getsockopt 系统调用校验器
（``z_vrfy_zsock_getsockopt``）将用户的 ``optval``
通过 bounce 缓冲区拷贝到恰好 ``optlen`` 字节的内核分配
（``k_usermode_alloc_from_copy`` -> ``z_thread_malloc``），
因此一个在非特权用户线程上对启用了 Connection ID 的
已连接 DTLS 套接字传入较小 ``optlen`` 的操作会诱发
内核堆缓冲区溢出，溢出内容为远程对端的 CID。

该缺陷需要 ``CONFIG_MBEDTLS_SSL_DTLS_CONNECTION_ID``、
一个已建立并协商出对端 CID 的 DTLS 会话，以及
（对于跨内核情形）``CONFIG_USERSPACE``。
该缺陷在添加 ``TLS_DTLS_CID`` 选项时（v3.5.0）引入。

修复以 -EINVAL 拒绝 ``optlen`` 低于
``MBEDTLS_SSL_CID_OUT_LEN_MAX`` 的调用者。

- `Zephyr 项目缺陷跟踪器 GHSA-p3r6-mx6c-33gq
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p3r6-mx6c-33gq>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109244 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109244>`_

- `PR 109624 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109624>`_

- `PR 113749 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113749>`_

- `PR 113750 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113750>`_

:cve:`2026-9263`
----------------

Bluetooth 控制器 ISOAL 分帧 RX 重组中的越界读取
将相邻内存泄露到主机 HCI ISO 报文

Zephyr Bluetooth 控制器 ISO 适配层
（``subsys/bluetooth/controller/ll_sw/isoal.c``）
未校验分帧 ISO PDU 起始段的长度字段。按 Bluetooth 规范，
起始段（``sc=0``）始终携带 3 字节的 ``time_offset``，
因此其段头 ``len`` 必须至少为
``PDU_ISO_SEG_TIMEOFFSET_SIZE``（3）。
``isoal_check_seg_header()`` 将 ``len`` < 3 的起始段
视为有效，随后 ``isoal_rx_framed_consume()`` 在
``uint8_t`` 中计算 ``length = seg_hdr->len - 3``，
当 ``len`` 为 0-2 时下溢为 253-255。该过大的长度
被传给 ``isoal_rx_append_to_sdu()``，其拷贝仅针对
目标 SDU 缓冲区大小钳制，而非源 PDU 长度，
因此接收 PDU 之后最多约 255 字节的控制器内存
（通过 ``sink_sdu_write_hci()``/``net_buf_add_mem``）
被拷贝到一个 HCI ISO 数据报文中并交付给主机。
PDU 及其段头完全由攻击者控制并经空中到达，
可通过 CIS 与 BIS-sync HCI 数据路径（``hci_driver.c``）
以及厂商数据路径（``ull_iso.c``）触达，
因此远程 CIS 对端或设备所同步的广播器可触发
越界读取，导致向主机泄露信息并可能引发拒绝服务
（故障或畸形超大 HCI ISO 报文）。该缺陷影响自
v3.0.0 引入分帧 ISO 接收以来的所有 Zephyr 发布。
修复在 ``isoal_check_seg_header()`` 中拒绝 ``len`` < 3
的 ``sc=0`` 段，并在 ``isoal_rx_framed_consume()``
的减法前添加保护。

- `Zephyr 项目缺陷跟踪器 GHSA-6gvp-pmh8-fjh2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6gvp-pmh8-fjh2>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109369 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109369>`_

- `PR 109617 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109617>`_

- `PR 109619 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109619>`_

- `PR 109618 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109618>`_

:cve:`2026-10593`
-----------------

Bluetooth LE Audio BAP 单播客户端 QoS 状态处理中
可远程触发的空指针解引用

Zephyr Bluetooth LE Audio Basic Audio Profile (BAP)
单播客户端未正确处理对端提供的 ASE 状态通知。
在 ``unicast_client_ep_qos_state()``
（``subsys/bluetooth/audio/bap_unicast_client.c``）中，
处理程序仅以 ``stream != NULL`` 作为保护，
通过 ``stream->qos`` 指针写入攻击者控制的 QoS 字段
（``interval``、``framing``、``phy``、``sdu``、``rtn``、
``latency``、``pd``）。对于任何已通过
``bt_bap_stream_config()`` 完成编解码器配置
但尚未加入单播组的流，``stream->qos`` 为 ``NULL``
（它仅由 ``unicast_group_add_stream()`` 设置）。

一个恶意或有缺陷的远程 ASCS 服务器（本地设备作为
BAP 单播客户端与其连接）可在本地端点仍处于
Codec Configured 状态时，发送一个宣告 ASE 已进入
QoS Configured 状态的 GATT 通知——一个分发器
明确允许的转换——在该窗口内触发通过空指针的写入
与崩溃（拒绝服务）。所写入的数据本身即由远程控制。

该缺陷随 v4.3.0 与 v4.4.0（及更早版本）发布。
修复将所有 BAP QoS 存储重新指向始终有效的
内嵌 ``ep->qos`` 结构，消除空指针解引用。

- `Zephyr 项目缺陷跟踪器 GHSA-22q8-m94g-2pwh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-22q8-m94g-2pwh>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 104887 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104887>`_

- `PR 110779 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110779>`_

- `PR 110777 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110777>`_

:cve:`2026-10634`
-----------------

Zephyr 原生 TCP ``net_tcp_foreach()`` 中因回调期间
释放 ``tcp_lock`` 导致的释放后使用（use-after-free）

Zephyr 原生 TCP 协议栈在 ``net_tcp_foreach()``
（``subsys/net/ip/tcp.c``）中使用
``SYS_SLIST_FOR_EACH_CONTAINER_SAFE`` 宏遍历全局
连接列表，该宏会缓存一个指向下一个列表节点的指针。
修复前，该函数在调用每连接回调时释放 ``tcp_lock``，
之后再重新获取。在该窗口内，一个并发的
``tcp_conn_release()``——在连接引用计数降为零时
（例如远程对端关闭或重置连接）运行于专用 TCP
工作队列线程——可移除并 ``k_mem_slab_free()`` 该
被缓存的下一个连接。当迭代器前进时，它解引用
已释放（且可能已被重新分配）的 slab 内存——
一次释放后使用，可使系统崩溃（拒绝服务），
并且若该槽位已被复用，可使回调操作一个
受攻击者影响的对象（潜在信息泄露或进一步故障）。
``net_tcp_foreach()`` 在生产中可通过 ``net conn``
网络 shell 命令以及接口 down 时的
``net_tcp_close_all_for_iface()`` 触达；
释放侧由普通 TCP 流量驱动。修复将
``tcp_conn_release()`` 中的连接/上下文拆除
移入 ``tcp_lock`` 临界区，并在 ``net_tcp_foreach()``
中跨回调保持持有 ``tcp_lock``。该缺陷随 2020 年的
现代（TCP2）协议栈引入，影响直至 v4.4.0（含）的发布。

- `Zephyr 项目缺陷跟踪器 GHSA-6c57-xfhw-j26x
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6c57-xfhw-j26x>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 106992 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/106992>`_

- `PR 107287 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107287>`_

- `PR 107288 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107288>`_

- `PR 107289 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107289>`_

:cve:`2026-10635`
-----------------

Xtensa MMU 页表代码中内存域反初始化时的
悬空内存域指针（释放后使用）

在启用 ``CONFIG_USERSPACE`` 与 ``CONFIG_XTENSA_MMU``
的 Xtensa 目标上，页表代码
（``arch/xtensa/core/ptables.c``）维护一个全局列表
``xtensa_domain_list``，记录活跃的内存域，
使用内嵌于调用者拥有的 ``struct k_mem_domain``
中的列表节点。当一个域通过 ``k_mem_domain_deinit()`` ->
``arch_mem_domain_deinit()`` 销毁时，页表被拆除
并将 ``domain->arch.ptables`` 置为 ``NULL``，
但该域的节点并未从 ``xtensa_domain_list`` 中移除。
因此被释放/反初始化的域作为指向调用者拥有的
存储（随后可能被释放或复用）的悬空指针
仍链接在全局列表中。

任何后续的 ``arch_mem_map()``/``arch_mem_unmap()``
操作（由内核内存映射与按需分页代码广泛调用）
会遍历过期节点并解引用 ``domain->ptables``：
至少导致一次引发致命 MMU 异常（拒绝服务）的
空指针解引用；若 ``k_mem_domain`` 存储已被释放
或复用，则导致一次释放后使用，其中过期/受控的
``ptables`` 值在页表遍历期间被解引用并写入
（``l2_page_table_map`` 写入 ``l1_table[...]`` 与
``l2_table[...]``，``xtensa_mmu_compute_domain_regs``
写入域结构与 L1 表），产生页表内存破坏，
可能破坏用户空间隔离。

易受攻击的路径仅可从特权内核/监督者代码
（``k_mem_domain_deinit`` 不是系统调用）触达，
不能直接从未特权用户线程或远程触达。
受影响版本：Zephyr v4.4.0（Xtensa 内存域
反初始化特性在 commit 3032b58f52d 引入，
首次随 v4.4.0 发布）；在 ``main`` 上通过在
``arch_mem_domain_deinit()`` 中添加
``sys_slist_find_and_remove()`` 修复。
Xtensa MPU 路径不受影响。

- `Zephyr 项目缺陷跟踪器 GHSA-39v7-cx8j-gq82
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-39v7-cx8j-gq82>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 106923 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/106923>`_

- `PR 110758 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110758>`_

:cve:`2026-10636`
-----------------

Zephyr IPv4 IGMP 发送路径（``igmp_send``）中的释放后使用

在 Zephyr 的 IPv4 IGMP 实现中，
``subsys/net/ip/igmp.c`` 的 ``igmp_send()``
在报文已交给 ``net_send_data()`` 之后
通过 ``net_pkt_iface(pkt)`` 从报文中读回网络接口。
在发送成功路径上，报文的最后一个引用
可能已被 L2 驱动或网络栈的 TX 处理
（在默认 ``NET_TC_TX_COUNT=0`` 立即发送配置下
同步地）释放，使 ``net_pkt`` slab 块返回其
空闲链表。后续的 ``net_pkt_iface(pkt)``
解引用已释放的报文，一次释放后使用读取；
在 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 下，
产生的悬空接口指针会被进一步解引用
用于统计计数器写入。IGMP 发送路径可在无需认证
的情况下从发往 224.0.0.1 的入站 IPv4 IGMP
成员资格查询（``net_ipv4_igmp_input`` ->
``send_igmp_report``/``send_igmp_v3_report`` ->
``igmp_send``）以及本地多播加入/离开/重新加入
操作触达。现实影响是未定义行为与潜在拒绝服务
（零星崩溃或统计破坏）；可控写入需要
异步 TX 路径加并发 slab 复用。该缺陷随
IGMPv2 支持引入，影响 v2.6.0 至 v4.4.0 的发布。
修复在发送前缓存接口指针。注意类似的
IPv6 MLD 路径（``subsys/net/ip/ipv6_mld.c`` 的
``mld_send``）保留了同样的未修复模式。

- `Zephyr 项目缺陷跟踪器 GHSA-fj6q-975v-65c9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fj6q-975v-65c9>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107100 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10637`
-----------------

IPv6 MLD 发送路径中 ``net_pkt`` 的释放后使用
可被链路本地 MLD Query 触发

``subsys/net/ip/ipv6_mld.c``:``mld_send()``
在 ``net_send_data(pkt)`` 成功返回之后
通过 ``net_pkt_iface(pkt)`` 读取报文接口。
按网络栈的所有权契约（``include/zephyr/net/net_core.h``，
以及 ``subsys/net/ip/net_core.c``:453-460 中
"do not use pkt after that call" 的明确警告），
发送成功会转移 ``net_pkt`` 的所有权，
L2 驱动将其释放（例如 ``ethernet_send()``
在成功时 unref 报文，``subsys/net/l2/ethernet/ethernet.c``:790），
使其返回其 ``k_mem_slab``。因此后续的
``net_pkt_iface(pkt)`` 是对已释放对象的读取；
取回的接口指针随后在启用
``CONFIG_NET_STATISTICS_PER_INTERFACE`` 时
被每接口统计路径（``net_stats.h`` 的
``UPDATE_STAT``/``SET_STAT``）解引用并自增。
若被释放的槽位被并发重新分配，``pkt->iface``
可能读回为 ``NULL``（空指针解引用/崩溃）
或为过期/垃圾指针（游离自增写入/内存破坏）。
该路径可在本地链路上无需认证地远程触达：
``handle_mld_query()``（为 ``NET_ICMPV6_MLD_QUERY``
注册）通过调用 ``send_mld_report()`` ->
``mld_send()`` 响应一个有效的 MLDv2 General Query
（未指定多播地址，hop limit 1）。
结果是网络栈可远程触发的拒绝服务，
并伴有狭窄的内存破坏可能性。
修复在发送前将接口缓存到局部变量，
不再在 ``net_send_data()`` 之后接触报文。
IPv4/IGMP 姊妹路径（``igmp_send``）
已使用修正后的模式。

- `Zephyr 项目缺陷跟踪器 GHSA-m23w-34pp-4h92
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m23w-34pp-4h92>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107100 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10638`
-----------------

Zephyr ICMPv6 RX 路径中在发送 echo 应答或错误后
更新统计时的释放后使用

``subsys/net/ip/icmpv6.c`` 在报文已交给
``net_try_send_data()`` 之后从 ``net_pkt`` 读取
网络接口。在 ``icmpv6_handle_echo_request()``
与 ``net_icmpv6_send_error()`` 中，
发送后的统计更新对刚发送的报文调用
``net_pkt_iface(reply)``/``net_pkt_iface(pkt)``。
发送路径（``net_try_send_data`` -> ``net_if_tx``）
在返回前 unref 并可能释放该报文回其内存 slab——
在未配置 TX 队列（``CONFIG_NET_TC_TX_COUNT`` == 0）
时于 RX 线程中同步地，否则驱动/L2 可能
已异步释放。因此 ``net_pkt_iface()``
解引用一个已释放（且可能已被复用）的 ``net_pkt``；
在 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 下，
过期的 ``iface`` 指针被进一步解引用并写入
（``iface->stats.icmp.sent++``），使释放后使用读取
变为通过一个受攻击者影响指针的写入。核心协议栈
已在 ``net_core.c`` 中记录了该危险（"do not use pkt
after that call"）并在发送前缓存 ``iface``；
ICMPv6 调用方未这样做。未认证的远程攻击者仅通过
发送一个 ICMPv6 Echo Request（ping）或一个会引发
ICMPv6 错误的 IPv4 报文（未知下一报头、分片重组
超时、目标不可达）即可触发该缺陷，导致通过崩溃
的拒绝服务与潜在内存破坏。受影响版本：启用
``CONFIG_NET_NATIVE_IPV6`` 的 Zephyr 网络，
大致为 v4.2.0 至 v4.4.0。修复在发送前缓存
接口指针并用于所有统计更新；姊妹 commit
86e21665d46 修复了 ICMPv4 中相同的 bug。

- `Zephyr 项目缺陷跟踪器 GHSA-m92g-94xv-wvw2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m92g-94xv-wvw2>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107100 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10639`
-----------------

``icmpv4_handle_echo_request()`` 中读取已发送
ICMPv4 echo 应答报文的 ``net_pkt_iface()`` 的释放后使用

在 Zephyr 原生 IPv4 协议栈中，
``subsys/net/ip/icmpv4.c`` 的
``icmpv4_handle_echo_request()`` 构建一个
echo 应答报文（``reply``），将其交给
``net_try_send_data()``，随后在成功时调用
``net_stats_update_icmp_sent(net_pkt_iface(reply))``。
``net_try_send_data()`` 将 ``reply`` 的所有权
转移给 TX 路径（``net_if_try_queue_tx`` ->
``net_if_tx`` -> L2/驱动发送，或异步的
``net_if_tx_thread``），该路径可将其 unref 至
引用计数 0，并在统计行执行前将 ``struct net_pkt``
返回其 slab（``net_pkt_unref`` ->
``k_mem_slab_free``）。``net_core.c`` 记录了
这一确切契约（'the pkt might contain garbage
already ... do not use pkt after that call'）。

因此发送后的 ``net_pkt_iface(reply)``
从一个已释放（且可能已被重新分配）的 ``net_pkt``
中读取 ``reply->iface``，一次释放后使用读取；
在 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 下，
统计宏还会通过该值自增一个计数器，
即通过一个过期或回收槽位指针的解引用/写入。

该路径可被任何 ping 该设备的远程主机
（``net_icmpv4_input`` ->
``net_icmp_call_ipv4_handlers`` ->
``icmpv4_handle_echo_request``）无需认证地触达，
并受 ``CONFIG_NET_STATISTICS_ICMP`` 门控。
影响是概率性地读取回收的报文内存，
加上时序竞态下可能的野指针写入，
最可能导致损坏的接口统计或可远程触发的
崩溃（DoS）。

该缺陷于 2019 年（v1.14）引入，存在于
v4.4.0（含）为止。``net_icmpv4_send_error()``
中的配套变更不是释放后使用，因为它读取
``net_pkt_iface(orig)``——调用者拥有的接收报文，
该报文在发送期间保持存活。修复在发送前
从存活的接收报文缓存接口指针，
并用于发送后的统计更新。

- `Zephyr 项目缺陷跟踪器 GHSA-qhrf-w466-qmpw
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qhrf-w466-qmpw>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107100 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10640`
-----------------

IPv6 邻居发现（``ipv6_nbr.c``）中发送后读取
``net_pkt`` ``iface`` 的释放后使用

Zephyr 的 IPv6 邻居发现发送路径
（``subsys/net/ip/ipv6_nbr.c`` 的
``net_ipv6_send_na``、``net_ipv6_send_ns``、
``net_ipv6_send_rs``）在 ``net_send_data(pkt)``
已成功返回之后调用 ``net_pkt_iface(pkt)``
更新每接口 ICMP 发送统计。在成功路径上，
网络栈拥有并释放报文的引用（L2/驱动发送
将其 unref，例如 ``ethernet_send`` ->
``net_pkt_unref``），因此对于一个引用计数为 1
的新分配报文，``net_pkt`` slab 块可能在
统计行执行前被释放（在未配置 TX 队列线程时
同步地，否则通过并发 TX 线程）。

随后 ``net_pkt_iface(pkt)`` 从已释放的 slab 块
读取 ``pkt->iface``，在启用
``CONFIG_NET_STATISTICS_PER_INTERFACE`` 时，
该加载的指针被解引用以自增
``iface->stats.icmp.sent``，一次释放后使用
（CWE-416）。若 slab 块在此期间被重新分配，
读取/自增的目标为无关或受攻击者影响的内存，
导致损坏的统计、故障/崩溃（拒绝服务），
或潜在的有限内存破坏。

易受攻击的 Neighbor Advertisement 路径
可被任何未认证的链路内节点仅通过向启用了
原生 IPv6 的 Zephyr 节点发送 ICMPv6 Neighbor
Solicitations 触达（``handle_ns_input`` ->
``net_ipv6_send_na``）。

受影响版本为 v3.3.0 至 v4.4.0；修复使用
已可用的 ``iface`` 参数而非接触已发送的报文。
无每接口统计的配置仅解引用一个全局计数器，
不受内存安全方面影响。

- `Zephyr 项目缺陷跟踪器 GHSA-r74c-mr4m-7g9g
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r74c-mr4m-7g9g>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107100 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10641`
-----------------

Bluetooth HFP Hands-Free CIND 指示符解析
（cind_handle_values）中的越界写入

Zephyr 的 Bluetooth Classic Hands-Free Profile (HFP)
Hands-Free 角色解析器
（subsys/bluetooth/host/classic/hfp_hf.c）
包含一个越界写入。在 Service Level Connection
建立期间，HF 发送 AT+CIND=? 并在 cind_handle()
中解析 AG 的 +CIND: 响应，该函数为每个条目
分配一个计数器 ``index`` 并对每个列表元素调用
cind_handle_values()。cind_handle_values()
随后在未校验 ``index`` 是否位于
struct bt_hfp_hf 的 20 元素 int8_t ind_table[]
数组范围内时写入 ``hf->ind_table[index] = i``。
由于解析器对 +CIND: 列表条目数量不设上限，
远程 Attendant Gateway（设备通过 Bluetooth
连接的恶意、被入侵或伪装的对端）可发送一个
包含超过 20 个被识别指示符条目的响应，
将 ``index`` 驱动到任意大，
将一个小的、攻击者定位的值越过数组写入
相邻结构体字段（feature 掩码、SDP/版本状态、
calls[] 数组、work/atomic 簿记）并可能
超出静态连接池槽位。这导致内存破坏，
至少导致 Bluetooth 主机的拒绝服务，
由单个畸形 AT 响应触发，无需用户交互。
姊妹消费者 ag_indicator_handle_values()
已执行等价的边界检查；本 commit 为关闭该缺口
添加相同的 ``index >=
ARRAY_SIZE(hf->ind_table)`` 保护。
影响启用 CONFIG_BT_HFP_HF 的构建；
随原始 HFP HF CIND 解析器（约 v1.7）引入，
存在于 v4.4.0（含）为止。

- `Zephyr 项目缺陷跟踪器 GHSA-wx5j-q6f2-59p3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wx5j-q6f2-59p3>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107331 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107331>`_

- `PR 110765 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110765>`_

- `PR 110764 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110764>`_

- `PR 110763 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110763>`_

:cve:`2026-10642`
-----------------

Zephyr PL011 UART 驱动在 CTS 硬件流控下的
无界 TX 忙循环拒绝服务

Zephyr PL011 UART 驱动（``drivers/serial/uart_pl011.c``）
在 ``pl011_irq_tx_enable()`` 中包含一个无界软件循环，
在 TX 中断掩码位（``PL011_IMSC_TXIM``）被设置时
反复调用中断驱动的应用回调，
以规避控制器电平跳变的 TX 中断行为。

当启用 CTS 硬件流控（devicetree ``hw-flow-control``
或运行时 ``UART_CFG_FLOW_CTRL_RTS_CTS``）且
连接的串行对端解除 CTS 断言时，
控制器停止排空 TX FIFO；``pl011_fifo_fill()``
随后在应用仍有待发数据时每次调用都返回 0，
因此从不禁用 TX 中断。循环条件永不清除，
因此调用 ``uart_irq_tx_enable()`` 的线程
（例如 Bluetooth HCI H4 驱动中的 ``h4_send()``）
无限自旋，挂起执行上下文并阻塞传输——
一次拒绝服务（CWE-835）。

控制连接到 UART CTS 线的设备的攻击者
可通过在传输期间扣留 CTS 触发挂起。
由于该对端是连接到 UART 的设备——
它可能是可移除或外部模块（例如 HCI H4 链路上的
板外 Bluetooth 控制器），而非永久焊接在 PCB 上的部件——
攻击向量被评定为 Adjacent（AV:A）而非 Physical；
安全小组委员会应针对具体部署确认该向量。
影响仅为可用性；无内存安全、机密性或完整性后果。

易受攻击的循环在 commit b783bc8448ef（2025 年 2 月）
引入，随 v4.1.0 至 v4.4.0 的发布发布。
修复在 CTS 阻塞时跳出循环，
并使能 CTS 调制解调器状态中断，
以便在 CTS 重新断言时恢复传输。

- `Zephyr 项目缺陷跟踪器 GHSA-3fgh-73jh-2q5j
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3fgh-73jh-2q5j>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 103684 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/103684>`_

- `PR 110768 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110768>`_

- `PR 110767 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110767>`_

:cve:`2026-10643`
-----------------

Zephyr ``recvmsg()`` 辅助数据路径中的越界堆写入
（``insert_pktinfo`` 使控制缓冲区容量检查偏小）

Zephyr 的 IP 套接字 ``recvmsg()`` 实现
（``subsys/net/lib/sockets/sockets_inet.c``，
``insert_pktinfo()``）在写入一条由对齐的 cmsg 头
加负载组成的完整控制消息之前，
仅使用负载长度（``msg->msg_controllen`` <
``pktinfo_len``）校验用户提供的辅助
（``msg_control``）缓冲区。由于检查遗漏了
cmsg 头大小，长度落入未充分检查窗口
（例如 64 位目标上 IPv4 ``IP_PKTINFO`` 的
16-27 字节，其中单个元素实际占 28 字节）的
控制缓冲区通过保护，却导致一个固定大小的
越界写入，最多越过缓冲区末尾一个 cmsg 头
（约 12 字节）。

在 ``CONFIG_USERSPACE`` 下，``recvmsg`` 校验器
分配一个按 ``msg_controllen`` 定长的内核堆
控制缓冲区副本并对其实行实现，
因此溢出破坏内核堆内存，可从未特权
用户空间线程触发；在监督者模式下
它破坏调用者的缓冲区。

当应用以偏小的控制缓冲区调用 ``recvmsg()``
且收到一个数据报时，该路径在启用
``IP_PKTINFO``/``IPV6_RECVPKTINFO``（或
hoplimit/时间戳）的 UDP/IP 套接字上可达；
被覆盖字节的一部分（``ipi_addr`` 中的
目标 IP）受接收报文影响。

修复使容量检查使用 ``NET_CMSG_SPACE(pktinfo_len)``
（对齐头 + 对齐数据），并在缓冲区过小时
返回 ``-ENOMEM``。受影响版本：v3.6.0 至 v4.4.0。

- `Zephyr 项目缺陷跟踪器 GHSA-pvf7-7mrp-35w7
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-pvf7-7mrp-35w7>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 106464 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/106464>`_

- `PR 110668 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110668>`_

- `PR 110669 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110669>`_

- `PR 110670 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110670>`_

:cve:`2026-10644`
-----------------

Microchip SERCOM-G1 (PIC32CM-JH) 异步 UART RX
使用 1 字节缓冲区的越界写入

Microchip SERCOM-G1 UART 驱动
（``drivers/serial/uart_mchp_sercom_g1.c``），
由 PIC32CM-JH SoC 家族使用，
在其异步（DMA）接收路径中包含一个越界写入。
当以 1 字节接收缓冲区（``len == 1``）调用
``uart_rx_enable()`` 且启用 ``CONFIG_UART_MCHP_ASYNC``
时，RX 完成 ISR 在 SERCOM DATA 寄存器中
已有一个待接收字节时启动一个单拍 DMA 传输。
在该 SoC 上，外设触发的 DMA 启动时序
随后将 1 字节写入调用者提供的缓冲区末尾之外
（CWE-787）。

溢出字节值由连接的串行对端（相邻攻击者）
提供的 UART RX 数据决定，
而其大小与位置固定为缓冲区之后紧邻的 1 字节。

利用需要异步 UART 配置（树内 PIC32CM-JH
开发板默认未启用）以及一个以 1 字节缓冲区
启用 RX 的消费者；影响限于 RX 缓冲区相邻的
单字节内存破坏（可能崩溃/拒绝服务）。

该缺陷随 v4.4.0 发布。修复用 CPU 读取
首字节，对 1 字节缓冲区完全不执行 DMA；
对更大的缓冲区，为剩余 ``len-1`` 字节
定长 DMA。

- `Zephyr 项目缺陷跟踪器 GHSA-xv2x-56j7-6wc3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xv2x-56j7-6wc3>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107400 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107400>`_

- `PR 110750 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110750>`_

:cve:`2026-10645`
-----------------

Zephyr ext2 目录项遍历中来自构造文件系统镜像的
越界读取

Zephyr ext2 文件系统驱动（``subsys/fs/ext2``）
在遍历目录块时信任磁盘上的目录项字段
``de_rec_len`` 与 ``de_name_len``。
``ext2_fetch_direntry()`` 仅以
``de_name_len > EXT2_MAX_FILE_NAME`` 作为保护，
但 ``de_name_len`` 是 ``uint8_t`` 而
``EXT2_MAX_FILE_NAME`` 为 255，因此该检查
恒为假；该函数随后 ``memcpy`` 最多 255 个
名称字节，查找/readdir 路径以未校验的
``de_rec_len`` 推进遍历。每个目录块被读入
一个 ``block_size`` 大小的 slab 缓冲区，
``block_off`` 可被前序条目的 ``rec_len``
驱动到接近块末尾，因此 8 字节头读取与
随后的名称 ``memcpy`` 可从块缓冲区末尾之外
读取最多约 263 字节到相邻堆/slab 内存。
在 readdir 路径上，那些字节被返回到调用者的
``fs_dirent.name``，泄露相邻内核堆内存；
``de_rec_len`` 为 0 还会导致零进度无限循环
（拒绝服务），而 unlink 路径对未校验记录的
``memmove(de, next, next_reclen)``
是额外的 OOB 读/写来源。该缺陷可由任何
基于路径的操作（open、stat、unlink、rename、
mkdir）或对已挂载 ext2 卷的目录列表触达，
因此攻击者提供的存储（SD 卡、USB 大容量存储，
或以其他方式挂载的镜像）上的构造或损坏的
ext2 镜像会触发它。受影响版本：Zephyr ext2
自 v3.5.0 引入至 v4.4.0。修复在解析器中
校验 ``rec_len`` 与 ``name_len``，
并在每个遍历调用方中拒绝头不适合
剩余块或 ``rec_len`` 跨越块边界的条目。

- `Zephyr 项目缺陷跟踪器 GHSA-hwrh-9h3x-vccm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hwrh-9h3x-vccm>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108226 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108226>`_

- `PR 110031 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110031>`_

- `PR 110033 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110033>`_

- `PR 110030 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110030>`_

:cve:`2026-10646`
-----------------

``zsock_getaddrinfo()`` 中未取消的超时 DNS 查询
重试导致的返回后使用（use-after-return）

Zephyr 的 BSD 套接字 ``getaddrinfo()`` 实现
（``subsys/net/lib/sockets/getaddrinfo.c``）
将一个栈分配状态对象
（``struct getaddrinfo_state ai_state``）的指针
作为异步 DNS 解析器查询的 ``user_data`` 传入。
套接字层在一个故意设置为略长于解析器
自身每查询超时的信号量上等待。当该信号量
等待仍然超时（``-EAGAIN``）——当解析器的
超时工作被工作队列争用延迟时可能发生，
或在文档化的多重试配置中
``CONFIG_NET_SOCKETS_DNS_TIMEOUT`` 超过
``CONFIG_NET_SOCKETS_DNS_BACKOFF_INTERVAL`` 时——
修复前的代码在取消先前查询且
不重置信号量的情况下重试该查询
（``goto again``）。

先前查询槽在解析器中保持活跃，
其回调与栈指针作为 ``user_data``，
且 ``ai_state->dns_id`` 被覆盖，
使过期查询无法再被取消。随后通过 UDP 送达并
由其 16 位事务 id 匹配的 DNS 响应
（在 ``dispatcher_cb()``/``dns_read()`` 中），
或解析器自身的延迟查询超时工作，
随后对现已超出作用域的栈帧调用
``dns_resolve_cb()``，通过过期指针写入
（``state->status``、``state->idx``、
``state->ai_arr[]`` 与 ``k_sem_give()``）。

由于触发响应经网络送达且其 16 位 id 可被
在途或离路攻击者伪造/重放，
这是一次网络可影响的返回后使用，
可破坏复用的栈内存，导致崩溃/拒绝服务
或内存破坏。

修复在重试前按名称与类型取消超时的查询
并重置本地信号量，消除过期回调路径。
受影响版本：Zephyr v4.0.0 至 v4.4.0。

- `Zephyr 项目缺陷跟踪器 GHSA-h752-vhmf-29w6
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-h752-vhmf-29w6>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107609 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107609>`_

- `PR 110774 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110774>`_

- `PR 110773 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110773>`_

:cve:`2026-10647`
-----------------

USB CDC-NCM 设备类在 TX 入队失败时的死锁拒绝服务

USB CDC-NCM 设备类
（``subsys/usb/device_next/class/usbd_cdc_ncm.c``）
在其以太网发送回调 ``cdc_ncm_send()`` 中
忽略 ``usbd_ep_enqueue()`` 的返回值。
当入队失败时，该函数仍调用
``k_sem_take(&data->sync_sem, K_FOREVER)``，
阻塞在一个完成信号量上，而该信号量
仅从 bulk-IN 传输完成回调发出信号。
由于没有东西被入队，该回调永不触发，
调用线程——一个共享的网络流量类 TX 线程——
在持有接口 TX 锁的同时永久死锁，
使传输停止直至重启（并泄露发送缓冲区）。

入队在由连接的 USB 主机控制的条件失败：
``usbd_ep_enqueue()`` 在总线挂起时
（一种标准的、持久的主机操作）始终返回
``-EPERM``，且底层 ``udc_ep_enqueue()``
在断开、总线复位或端点禁用时返回
``-EPERM``/``-ENODEV``。
``cdc_ncm_send()`` 的保护仅检查
``DATA_IFACE_ENABLED`` 与 ``IFACE_UP`` 标志，
不检查挂起状态，因此当主机保持总线挂起时
发送的报文到达失败的入队并使 TX 路径死锁。

现实的触发是发生在导出的网络接口
处于活跃且有流量要发送时的总线挂起——
主机睡眠、USB 选择性/自动挂起或集线器
电源管理——此后任何设备发起的报文
都使路径死锁，仅可通过重启恢复。
影响是主机 NCM 接口与 Zephyr 设备之间
虚拟网络连接持久丢失；由于死锁线程
是共享的流量类 TX 线程，
其他网络接口的出站也可能停止。
无内存破坏或信息泄露。

该缺陷随 CDC-NCM 驱动引入，
随发布至 v4.4.0 发布；
通过检查 ``usbd_ep_enqueue()`` 返回值
并在阻塞等待前释放缓冲区修复。

- `Zephyr 项目缺陷跟踪器 GHSA-xcf7-r86m-5q9f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xcf7-r86m-5q9f>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107126 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107126>`_

- `PR 110652 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110652>`_

- `PR 110653 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110653>`_

:cve:`2026-10648`
-----------------

MCUmgr 串行/控制台 SMP 传输在缓冲区池耗尽时的
空指针解引用

``subsys/mgmt/mcumgr/transport/src/serial_util.c``
的 ``mcumgr_serial_process_frag()``
在检查 ``smp_packet_alloc()`` 结果是否为
``NULL`` 之前对其调用 ``net_buf_reset()``。
``smp_packet_alloc()`` 对共享的 MCUmgr
报文池（``CONFIG_MCUMGR_TRANSPORT_NETBUF_COUNT``，
默认 4）使用 ``net_buf_alloc(K_NO_WAIT)``，
在池耗尽时返回 ``NULL``。在默认构建中，
``net_buf_reset`` 中的 ``__ASSERT_NO_MSG``
是空操作，因此 ``net_buf_simple_reset``
通过 ``NULL`` 指针写入
（``buf->len = 0; buf->data = buf->__buf``），
导致故障/崩溃。

分片数据从 MCUmgr 串行/UART/shell-控制台
传输（``smp_uart.c``、``smp_raw_uart.c``、
``smp_shell.c``）的攻击者控制字节到达
该代码，且几乎每个新报文开始时
都分配一个新鲜缓冲区。串行/控制台链路上的
攻击者可淹没传输，使 4 条目缓冲区池
耗尽并诱发 ``NULL`` 解引用，
使设备崩溃（拒绝服务）。

该缺陷在原始 MCUmgr 重构后引入，
随 Zephyr v4.4.0 发布。
修复将 ``NULL`` 检查移到 ``net_buf_reset``
之前。

- `Zephyr 项目缺陷跟踪器 GHSA-j64f-h3ww-f32c
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j64f-h3ww-f32c>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107812 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107812>`_

- `PR 108026 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108026>`_

:cve:`2026-10651`
-----------------

Bluetooth Classic SDP 属性解析
（``bt_sdp_parse_attribute``）中的越界读取

``subsys/bluetooth/host/classic/sdp.c`` 的
``bt_sdp_parse_attribute()`` 仅校验
SDP 记录缓冲区持有类型标记字节加
2 字节属性 ID（``buf->len < 3`` 的检查），
但随后通过 ``net_buf_simple_pull_u8()``
读取第四个字节——数据元素描述符
（``type``）。由于 ``net_buf_simple_pull_u8()``
在其唯一的边界保护（一个在禁用
``CONFIG_ASSERT``——发布默认——时
被编译掉的 ``__ASSERT_NO_MSG``）之前
解引用 ``buf->data[0]``，
一个恰好 3 字节的记录（0x09 后跟
2 字节属性 ID）导致越过逻辑缓冲区末尾
的 1 字节读取。解析器可从入站、
远程控制的数据触达：作为 SDP 服务器
的 Bluetooth BR/EDR 对端返回的发现响应
记录被原样存储在客户端接收缓冲区中，
并通过公共
``bt_sdp_get_attr()``/``bt_sdp_has_attr()``/
``bt_sdp_record_parse()`` 助手解析。
越界读取被限定为单字节，
仅用作内部长度选择器，
从不泄露给攻击者；随后的长度检查
随后拒绝畸形记录。因此现实影响限于
边缘情况拒绝服务（仅当记录恰好结束于
映射内存边界时故障，或在
``CONFIG_ASSERT=y`` 时确定性断言 panic）。
影响 Zephyr v4.3.0 与 v4.4.0；
通过在长度检查中添加 ``sizeof(type)`` 修复。

- `Zephyr 项目缺陷跟踪器 GHSA-p93g-3r68-cj53
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p93g-3r68-cj53>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107325 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107325>`_

- `PR 110850 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110850>`_

- `PR 110851 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110851>`_

:cve:`2026-10652`
-----------------

Zephyr DNS 解析器 TXT/SRV 记录解析中的越界读取
（未校验的 ``rdlength``）

Zephyr 的 DNS 解析器（``subsys/net/lib/dns``）
在 ``dns_unpack_answer()`` 中从 DNS 响应
解析资源记录，该函数仅校验固定 RR 头
（type、class、TTL、``rdlength``）并
接受任何攻击者声明的 ``rdlength``，
包括一个延伸越过接收数据报末尾的值。
``dns_validate_record()``（``resolve.c``）中
的 TXT 与 SRV 消费者随后通过 ``memcpy``
从接收缓冲区读取最多 ``rdlength`` 字节
（仅钳制到记录类型最大值，例如
``DNS_MAX_TEXT_SIZE``，默认 64，
而非钳制到报文），没有自身的边界检查，
并将结果传给应用的解析回调。
恶意或伪装的 DNS 服务器、在途攻击者
伪造 UDP DNS 响应，或（在启用
mDNS/LLMNR 时）任何 LAN 节点，
可构造一个截断的 TXT 或 SRV 响应，
导致相邻接收池内存的越界读取；
泄露的过期字节（先前 DNS 报文的
残留内容/未初始化池内存）作为
TXT/SRV 记录内容返回给应用，
一次信息泄露，且在某些配置下
可能跨越分配边界并故障，
导致拒绝服务。读取被限定
（TXT 约 64 字节，SRV 约 6）且
只读（无写入）。修复在
``dns_unpack_answer()`` 的单一咽喉点
拒绝任何声明的 rdata 延伸越过
``dns_msg->msg_size`` 的记录。
受影响版本：v4.3.0 与 v4.4.0。

- `Zephyr 项目缺陷跟踪器 GHSA-3jxq-xx8g-q8j2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3jxq-xx8g-q8j2>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107977 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107977>`_

- `PR 108844 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108844>`_

- `PR 108843 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108843>`_

- `PR 108845 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108845>`_

:cve:`2026-10653`
-----------------

非原子 ``net_buf`` 引用计数在并发 unref 下
导致双重释放/空闲链表破坏

Zephyr ``net_buf`` 库（``lib/net_buf/buf.c``）
以普通非原子 C 运算符操作其两个
引用计数——每头 ``buf->ref`` 与
每个变量/堆数据分配起始处的
``ref_count``——（``buf->ref++``、
``if (--buf->ref > 0)``、
``if (--(*ref_count))``）。

该 API 文档说明为自同步：
调用者可跨线程共享一个缓冲区
（例如通过 ``k_fifo``），
每个持有者独立调用 ``net_buf_unref()``，
无周围锁。在真正并发下
（SMP，或单核上在非原子加载与存储之间
另一上下文 unref 同一缓冲区时的抢占），
两个持有者可观察到相同的先前引用值
并都得出自己是最后一个引用的结论。

对于堆/变量数据池（``mem_pool_data_unref``/
``heap_data_unref``，由 zbus 消息订阅者、
``CONFIG_NET_BUF_FIXED_DATA_SIZE=n`` 时
的 IP 协议栈 RX/TX 缓冲区、capture、
wireguard、ISO-TP 与 usbip 使用），
这产生对同一块的双重
``k_heap_free()``/``k_free()``——
堆元数据破坏与堆加固毒化模式上的
释放后使用。

对于每头引用计数，
任何池类型（包括 Bluetooth 与网络
使用的固定数据池）的缓冲区
被两次返回池空闲 LIFO，
破坏空闲链表，使后续分配
将同一缓冲区交给两个所有者。

修复将两个引用计数转换为
``atomic_inc``/``atomic_dec``
（在一个 ``atomic_t`` 大小的 union 中
覆盖 ``buf->ref``，
并将数据块引用计数从 ``uint8_t``
改为 ``atomic_t``）。

影响受真正并发以及一个在多个独立
unref 者间共享一个缓冲区的应用架构门控；
触发是引用计数/时序竞态而非报文内容，
因此外部攻击者对竞态窗口
至多有弱的间接影响。
影响所有 Zephyr 发布至 v4.4.0。

- `Zephyr 项目缺陷跟踪器 GHSA-284j-5jm9-55hh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-284j-5jm9-55hh>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108065 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108065>`_

- `PR 110853 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110853>`_

- `PR 110852 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110852>`_

:cve:`2026-10654`
-----------------

Zephyr Bluetooth Classic 中 RFCOMM 会话断开竞态
泄露会话/L2CAP 并拒绝进一步 RFCOMM 服务

Zephyr Bluetooth Classic RFCOMM 主机协议栈
（``subsys/bluetooth/host/classic/rfcomm.c``）中的
竞态条件不当处理同时双向的会话断开。
当本地设备已发起会话拆除（状态
``BT_RFCOMM_STATE_DISCONNECTING``，DISC 已发送，
RTX 定时器已武装）且连接的对端并发地
为其 dlci 0 发送自己的 DISC 帧时，
``rfcomm_handle_disc()`` 调用
``rfcomm_session_disconnected()``，
后者无条件地将会话强制为
``BT_RFCOMM_STATE_DISCONNECTED``，
从未调用 ``bt_l2cap_chan_disconnect()``。

由于恢复定时器也被取消，
且稍后的 UA 在 DISCONNECTED 状态被忽略，
会话永久卡死：底层 L2CAP 信道
从不被释放，固定
``bt_rfcomm_pool[CONFIG_BT_MAX_CONN]``
数组中的会话槽位从不被回收
（其 ``conn`` 指针保持设置）。

后续对该连接的 ``bt_rfcomm_dlc_connect()``
调用因无效会话状态以 ``-EINVAL`` 失败，
因此该对端的 RFCOMM 服务被拒绝，
且重复发生可耗尽会话池。
DISC 帧由对端经空中控制，
但利用需要对端的 DISC 与
本地发起的断开碰撞
（高复杂度的时序竞态）。
影响仅为可用性/资源泄露；
无内存安全、机密性或完整性后果。
该缺陷随发布版本发布
（存在于 v4.4.0 及更早版本）。

修复仅在会话尚不处于
DISCONNECTING 时才转换到
DISCONNECTED，保留正确的 L2CAP 拆除路径。

- `Zephyr 项目缺陷跟踪器 GHSA-4m37-wp5x-hq4h
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4m37-wp5x-hq4h>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108089 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108089>`_

- `PR 110865 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110865>`_

- `PR 110864 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110864>`_

- `PR 110863 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110863>`_

:cve:`2026-10655`
-----------------

Zephyr SNTP 异步客户端在套接字服务
仍在轮询其套接字时关闭套接字的
释放后使用竞态

Zephyr 中的异步 SNTP 客户端
（``subsys/net/lib/sntp/sntp.c``，
``sntp_close_async``）在将其从
网络套接字服务分离后，
直接从调用线程关闭 UDP 套接字文件描述符，
未与套接字服务轮询线程同步。

套接字服务线程通过 ``zvfs_poll``
轮询每个套接字，后者
（在 ``zsock_poll_prepare_ctx`` 中）
注册一个指向套接字
``net_context``（``&ctx->recv_q``）的
``k_poll_event``，随后在 ``k_poll``
中阻塞而不持有引用或锁。
``net_context`` 对象从固定池
（``contexts[CONFIG_NET_MAX_CONTEXTS]``）
分配并在关闭后复用。

当 ``sntp_close_async`` 从不同于
轮询线程的线程调用时（在树内消费者
``subsys/net/lib/config/init_clock_sntp.c`` 中，
SNTP 超时处理程序运行于系统工作队列，
而套接字服务线程阻塞在
同一 fd 的轮询上），
关闭释放并可能复用 ``net_context``，
而轮询线程仍有一个 poller 节点
链接到已释放对象中，
导致内核 poll 结构的
释放后使用/对象混淆。

SNTP 超时路径是正常无响应失败模式，
因此丢弃或延迟 SNTP/NTP 响应的
网络对端或离路攻击者可反复驱动
竞态关闭（在 ``NET_CONFIG_SNTP_INIT_RESYNC``
下周期性）。最可能的后果是
网络线程崩溃（拒绝服务），
并在已释放上下文槽位被重新分配时
存在潜在内存破坏。

修复通过 ``net_socket_service_close``
（``NET_SOCKET_SERVICE_CLOSE_SOCKETS``）
将关闭延迟到套接字服务线程本身，
因此执行轮询的同一线程执行关闭，
消除竞态。受影响版本：v4.2.0 至 v4.4.0。

- `Zephyr 项目缺陷跟踪器 GHSA-34wr-cg29-c4mw
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-34wr-cg29-c4mw>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108180 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108180>`_

- `PR 110860 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110860>`_

- `PR 110858 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110858>`_

:cve:`2026-10656`
-----------------

MAX32 USB 设备控制器传输完成处理程序中的
空指针解引用拒绝服务

MAX32xxx USB 设备控制器驱动
（``drivers/usb/udc/udc_max32.c``，
compatible ``adi_max32_usbhs``）
在其 OUT 与 IN 传输完成处理程序中
解引用端点缓冲区而未检查其是否为 ``NULL``。
``udc_event_xfer_out_done()`` 在
``buf = udc_buf_get(ep_cfg)`` 之后立即
调用 ``net_buf_add(buf, ep_request->actlen)``，
而 ``udc_buf_get()`` 在端点 FIFO 为空时
返回 ``NULL``。

传输完成事件从中断上下文入队，
由驱动线程异步处理；
在入队与处理之间，
端点 FIFO 可被主机控制的控制流排空——
特别是 ``udc_setup_received()``
每当新 SETUP 报文到达时
排空 EP0 OUT/IN FIFO，
且 dequeue/disable/purge 路径
同样排空它。

因此，以新 SETUP 报文中止
进行中的 EP0 控制传输（合法 USB 行为）的
USB 主机可导致一个过期的
``XFER_OUT_DONE`` 事件针对空 FIFO 被处理，
产生 ``net_buf_add(NULL, ...)``，
一次近 NULL 指针解引用，
故障并使设备崩溃。无需认证；
攻击者是设备所连接的 USB 主机
（物理总线访问）。影响为拒绝服务
（设备崩溃）。

该缺陷在 MAX32 UDC 驱动添加时引入，
随 Zephyr v4.4.0 发布。
修复在 OUT-done 与 IN-done 处理程序中
添加 NULL 缓冲区检查，
以 ``UDC_EVT_ERROR``/-ENOBUFS 提前返回。

- `Zephyr 项目缺陷跟踪器 GHSA-58p9-6mjq-rf2m
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-58p9-6mjq-rf2m>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108447 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108447>`_

- `PR 109517 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109517>`_

:cve:`2026-10657`
-----------------

Zephyr DNS 解析器 mDNS 后缀检查中的
越界读取（``memcmp`` 越过字符串 NUL）

Zephyr 的 DNS 解析器在
``dns_resolve_name_internal()``
（``subsys/net/lib/dns/resolve.c``）中
通过 ``memcmp(strrchr(query, '.'), ".local", 7)``
检测 mDNS（.local）查询，
该调用始终从后缀指针读取固定 7 字节。
当解析主机名的最终标签短于 7 字节时
（例如以 .org、.com、.net、.io 结尾
或末尾带点的名称），
比较在字符串 NUL 终止符之后
读取 1-2 字节。

主机名（``query``）是调用者提供的名称，
通过标准 ``getaddrinfo()``/
``dns_get_addr_info()``/``dns_resolve_name()``
路径传入，可受操作员或远程输入影响
（配置中的服务器名称、解析的 URL
或面向应用的接口）。

在紧凑定长且无余量的缓冲区上
（例如用户空间 ``getaddrinfo`` 调用，
其中主机名通过
``k_usermode_string_alloc_copy``
拷贝为恰好 ``strlen+1`` 字节），
越读跨越分配边界；
若该边界未映射（保护页、
MPU 下的内存域边界，或地址 sanitizer），
越读故障，导致拒绝服务。
越读字节从不被返回，
因此无信息泄露。

该缺陷仅在启用 ``CONFIG_MDNS_RESOLVER``
时编译，自 v1.10.0 存在，
通过用 NUL 安全的 ``strcmp(ptr, ".local")``
替换定长 ``memcmp`` 修复。

- `Zephyr 项目缺陷跟踪器 GHSA-76jh-3j5f-9vq4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-76jh-3j5f-9vq4>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108372 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108372>`_

- `PR 110870 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110870>`_

- `PR 110867 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110867>`_

- `PR 110868 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110868>`_

:cve:`2026-10658`
-----------------

Bluetooth ISO 接收（``bt_iso_recv``）中的
越界访问，源于缺少 SDU 头长度校验

``subsys/bluetooth/host/iso.c`` 的
``bt_iso_recv()`` 通过 ``net_buf_pull_mem()``
从入站 HCI ISO Data 缓冲区拉取
ISO SDU 头（4 字节），或在时间戳标志
被设置时拉取带时间戳的 SDU 头（8 字节），
而未先检查 ``buf->len``。
上游 ``hci_iso()`` 处理程序强制
``buf->len`` == 控制器声明的
ISO Data_Load 长度，因此恶意或有缺陷的
控制器/已建立 CIS/BIS 上的相邻 BLE 对端
可呈现一个短于 SDU 头的
首片（``BT_ISO_START``）或单片
（``BT_ISO_SINGLE``）PDU。
由于 ``net_buf_simple_pull_mem``
仅以 ``__ASSERT_NO_MSG`` 保护长度
（在禁用 ``CONFIG_ASSERT`` 时
被编译掉，生产默认值），
拉取使 ``buf->len`` 下溢
（``uint16_t``，例如 ``0 - 8 = 0xFFF8``）
并使 ``buf->data`` 越过有效数据前进：
随后对 ``hdr->slen`` 与 ``hdr->sn`` 的读取
是相邻池内存的越界读取。
对多片（START）情形，
损坏的缓冲区被保留为 ``iso->rx``，
随后 CONT/END 片的 ``net_buf_tailroom()``
保护下溢到近 ``SIZE_MAX`` 值，
使边界检查失效，
导致 ``net_buf_add_mem()`` 通过
``memcpy`` 将攻击者提供的片数据
远远拷贝到 RX 池缓冲区之外
（越界写入）。该缺陷影响 ISO 接收构建
（``CONFIG_BT_ISO_RX``，
由默认关闭的 LE Audio 选项
``BT_ISO_PERIPHERAL``/``BT_ISO_CENTRAL``/
``BT_ISO_SYNC_RECEIVER`` 选择），
自 ISO 子系统引入（v2.6.0）
至 v4.4.0 存在。
修复添加显式的
``buf->len < sizeof(*ts_hdr)`` 与
``buf->len < sizeof(*hdr)`` 检查，
在拉取前丢弃缓冲区。

- `Zephyr 项目缺陷跟踪器 GHSA-26g8-rmpf-j6cw
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-26g8-rmpf-j6cw>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108603 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108603>`_

- `PR 111024 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111024>`_

- `PR 110959 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110959>`_

- `PR 110958 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110958>`_

:cve:`2026-10659`
-----------------

Zephyr Dhara FTL 磁盘驱动在日志恢复期间
flash 读取错误时的空指针解引用

Dhara flash 转换层磁盘驱动
（``drivers/disk/ftl_dhara.c``）
实现 ``dhara_nand_*`` 回调，
使得在 flash 错误时，
错误码无条件地通过调用者提供的
``dhara_error_t *err`` 指针写入
（例如 ``dhara_nand_read`` 中的
``*err = DHARA_E_ECC``，
以及 ``dhara_nand_erase``/``prog``/
``copy`` 中类似的）。

上游 Dhara 库在其日志恢复
二分搜索中以 ``err == NULL``
调用这些回调：
``find_last_checkblock()`` 调用
``find_checkblock(j, mid, &found, NULL)``，
后者将 NULL 指针转发到
``dhara_nand_read()``。
该路径在挂载/初始化 FTL 磁盘时
的 ``disk_ftl_access_init()`` ->
``dhara_map_resume()`` 期间运行。

如果一个 flash 读取错误（不可纠正的 ECC、
坏块、控制器错误）发生在某个被探测的
检查点页上，驱动解引用并写入 ``NULL``，
使内核故障（拒绝服务）。触发条件受
NAND 介质内容/健康状况制约，
可受介质磨损、诱导故障或
损坏/构造的 flash 上镜像影响。

修复将所有错误赋值路由到库的
NULL 安全 ``dhara_set_error()`` 助手。
影响 Zephyr v4.4.0，即驱动引入的版本。

- `Zephyr 项目缺陷跟踪器 GHSA-q28v-3729-f82g
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-q28v-3729-f82g>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108594 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108594>`_

- `PR 110955 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110955>`_

:cve:`2026-10660`
-----------------

Bluetooth BAP Broadcast Assistant 中的共享重组缓冲区
使跨连接内存破坏成为可能

``subsys/bluetooth/audio/bap_broadcast_assistant.c``
中的 Bluetooth BAP Broadcast Assistant
GATT 客户端将远程 Broadcast Receive State
数据重组到一个由所有连接实例共享的
单一文件静态 ``net_buf_simple``
（``att_buf``，``BT_ATT_MAX_ATTRIBUTE_LEN``
= 512 字节）中，而 BUSY 标志、
长读句柄与复位/偏移状态
是每连接的。

当设备作为连接到多个 Scan Delegator
外设的 Broadcast Assistant 时，
来自不同连接的通知与长读回调
在共享缓冲区上交错：
``notify_handler`` 中的追加
（非忙分支的 ``net_buf_simple_add_mem``）
不执行剩余空间检查，
因此来自两个或多个 delegator 的
接收状态通知累积在同一个 512 字节缓冲区上，
在足够大的配置 ATT MTU
（``BT_L2CAP_TX_MTU`` 至 2000）
与两到三个并发连接的情况下，
越过缓冲区写入相邻 .bss
（``net_buf_simple_add``
仅在调试构建中断言）。

即使在溢出阈值之下，
一个连接的 ``net_buf_simple_reset``
在另一个连接的重组与 GATT 读偏移
进行中时清零共享长度，
将一个对端的数据混入另一个的解析。
恶意或被入侵的 Scan Delegator
（或两个串谋对端）经 BLE 可触发，
导致越界写入（内存破坏/拒绝服务）
与跨连接数据损坏。

修复将缓冲区移入每连接实例结构，
使每个连接重组到自己的缓冲区。
影响随共享缓冲区发布
Broadcast Assistant 的 Zephyr 发布，
包括 v4.4.0 及更早版本。

- `Zephyr 项目缺陷跟踪器 GHSA-73c7-3rh7-v5p9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-73c7-3rh7-v5p9>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107563 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107563>`_

- `PR 111066 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111066>`_

- `PR 111065 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111065>`_

- `PR 111182 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111182>`_

:cve:`2026-10663`
-----------------

实验性 USB 主机协议栈中根 USB 设备的
释放后使用/双重释放

在 Zephyr 实验性 USB 主机协议栈
（``CONFIG_USB_HOST_STACK``）中，
``usbh_device_disconnect()``
（``subsys/usb/host/usbh_device.c``）
在不清除缓存指针 ``ctx->root`` 的情况下
释放根 ``usb_device`` slab 对象。
总线移除处理程序 ``dev_removed_handler()``
（``subsys/usb/host/usbh_core.c``）
仅从 ``ctx->root`` 决定拆除什么，
仅检查其非 NULL。

由于 UHC 控制器驱动
（例如 ``uhc_max3421e``、``uhc_mcux_common``）
直接从物理总线线路状态合成
``UHC_EVT_DEV_REMOVED``，
无去抖或状态保护，
具有物理 USB 访问权限的攻击者
（或一个反弹其连接的流氓设备）
可在根设备断开后
投递第二个设备移除事件。
处理程序随后带着悬空指针
重新进入 ``usbh_device_disconnect()``，
在已释放对象内部锁定互斥锁
（释放后使用），
从设备列表移除已释放节点，
并对已释放块调用 ``k_mem_slab_free()``
（双重释放）。如果 slab 块在期间
被重新发放给新连接的设备，
这会破坏一个存活对象。

影响为拒绝服务（崩溃）与内存破坏；
攻击向量为物理/本地。
该缺陷在 v4.4.0 由
连接/断开重构引入，
通过在 ``usbh_device_disconnect()`` 中
释放前清除 ``ctx->root`` 修复。

- `Zephyr 项目缺陷跟踪器 GHSA-26q8-xjq3-f5p6
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-26q8-xjq3-f5p6>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108796 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108796>`_

- `PR 111021 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111021>`_

:cve:`2026-10664`
-----------------

nRF70 Wi-Fi 驱动省电事件处理程序中的
越界写入（无界 TWT 流计数）

nRF70 Wi-Fi 驱动的省电事件处理程序
``nrf_wifi_event_proc_get_power_save_info()``
（``drivers/wifi/nrf_wifi/src/wifi_mgmt.c``）
将 TWT（Target Wake Time）流条目
从 ``nrf_wifi_umac_event_power_save_info``
事件拷贝到调用者提供的 ``struct wifi_ps_config``
的定长 ``twt_flows[WIFI_MAX_TWT_FLOWS]``
（8 元素）数组中，
遍历事件提供的 ``num_twt_flows``
而未将其与 ``WIFI_MAX_TWT_FLOWS`` 校验
或检查 ``event_len``。
当 ``num_twt_flows`` 超过 8 时，
处理程序越过目标数组写入
（通常位于调用者栈上，
例如 ``wifi ps`` shell 命令）——
约 40 字节 TWT 条目的越界写入——
并越过事件缓冲区读取
``twt_flow_info[i]``。
事件由 nRF70 协处理器固件
响应主机发起的省电 GET 投递，
因此触达溢出需要固件发出
畸形或超范围事件；
信任边界是主机到可信协处理器，
而非直接的远程 AP 写入，
对空中流计数的影响是间接的，
受 3 位 TWT 流-id 空间限制。
受影响版本：启用 ``CONFIG_NRF70_STA_MODE``
至 v4.4.0 的构建。
修复拒绝 ``num_twt_flows`` >
``WIFI_MAX_TWT_FLOWS`` 或
``event_len`` 短于所声明条目的事件，
并为调用者缓冲区添加 NULL 检查。

- `Zephyr 项目缺陷跟踪器 GHSA-3r6j-pm38-r43m
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3r6j-pm38-r43m>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108849 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108849>`_

- `PR 109067 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109067>`_

- `PR 109068 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109068>`_

:cve:`2026-10665`
-----------------

WireGuard 接收路径中通过无界入站报文长度的
堆缓冲区溢出

在 Zephyr 的 WireGuard 子系统
（``subsys/net/lib/wireguard``）中，
``wg_crypto.c`` 的
``wg_process_data_message()``
在解密前将入站传输数据负载
线性化到一个 ``CONFIG_WIREGUARD_BUF_LEN``
字节的固定池缓冲区中。
调用 ``net_buf_linearize(buf->data, data_len,
pkt->buffer, ..., data_len)``
将攻击者派生的 ``data_len``
同时作为目标容量与拷贝长度传入，
使函数内部的 ``len = min(len, dst_len)``
边界失效。``data_len``
派生自接收 UDP 数据报长度，
仅由 ``wg_ctrl_recv()`` 下界限定
（无上界）。当 ``data_len`` 超过
``CONFIG_WIREGUARD_BUF_LEN``——
例如当缓冲区长度被降低到链路 MTU 以下、
在 MTU 大于缓冲区大小的链路上，
或通过超过它的重组 IPv4/IPv6 分片——
底层 ``memcpy`` 越过池缓冲区末尾写入，
一次越界写入（CWE-787）。
溢出发生在 Poly1305 认证检查之前，
因此仅需要一个有效的接收方会话索引
而非有效认证器，
并可由恶意或被入侵的对端
（或驱动已建立会话的在途攻击者）
经网络触达，
产生远程内存破坏，
至少一次可靠的拒绝服务。
该缺陷存在于 Zephyr 4.4.0
发布的 WireGuard 实现中。
修复添加显式的
``data_len > CONFIG_WIREGUARD_BUF_LEN``
拒绝，并修正 linearize 调用
以传入 ``net_buf_max_len(buf)``
作为目标容量。

- `Zephyr 项目缺陷跟踪器 GHSA-3wqm-wgx2-9367
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3wqm-wgx2-9367>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108841 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108841>`_

- `PR 111084 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111084>`_

:cve:`2026-10667`
-----------------

Zephyr ``CONFIG_USERSPACE`` 动态内核对象跟踪中的
SMP 释放后使用，可从未特权用户线程触达

Zephyr 的动态内核对象跟踪
（``kernel/userspace/userspace.c``，
原 ``kernel/userspace.c``）
维护一个动态分配内核对象的双向链表
（``obj_list``）。
``k_object_wordlist_foreach()`` 中
对该列表的遍历在 ``lists_lock`` 下
使用 SAFE 迭代器（缓存下一个节点）执行，
但节点的列表移除与释放在
不同的、互不相交的自旋锁下执行：
``k_object_free()`` 中的 ``objfree_lock``
与 ``unref_check()`` 中的 ``obj_lock``。
在 SMP 系统上，当一个 CPU 在
``lists_lock`` 下遍历 ``obj_list`` 时，
另一个 CPU 可解链并 ``k_free()``
迭代器已缓存为下一指针的
``dyn_obj`` 节点，
导致迭代器解引用已释放的内核内存
（释放后使用/悬空列表遍历）。
所有竞态操作均可从未特权用户模式线程
经系统调用触达：
``k_object_alloc``/``k_object_alloc_size``
与 ``k_object_release`` 通过
``unref_check()``（在 ``obj_lock`` 下）
驱动移除，而 ``k_thread_abort``
与线程创建通过
``k_thread_perms_all_clear()``/
``k_thread_perms_inherit()``
（在 ``lists_lock`` 下）驱动遍历。
因此 ``CONFIG_SMP`` + ``CONFIG_USERSPACE``
构建上的降权用户线程
可跨用户空间安全边界
破坏内核的对象跟踪结构，
产生内核内存破坏（潜在权限提升）
或内核崩溃（拒绝服务）。
修复移除 ``objfree_lock``，
在 ``lists_lock`` 下序列化
所有 ``obj_list`` 修改，
包括在 ``k_object_free()`` 中
跨查找+移除持有它，
以及在 ``k_thread_perms_clear()`` 中
环绕 ``unref_check()`` 持有它。
影响 ``CONFIG_SMP``+``CONFIG_USERSPACE``+
``CONFIG_DYNAMIC_OBJECTS`` 配置；
缺陷可追溯到 2019 年的自旋锁化
（commit 8a3d57b6cc6，首次随
v1.14.0 发布）并随发布至 v4.4.0。

- `Zephyr 项目缺陷跟踪器 GHSA-9x5j-h3rh-x579
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9x5j-h3rh-x579>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108721 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108721>`_

- `PR 111067 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111067>`_

- `PR 111019 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111019>`_

- `PR 111018 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111018>`_

:cve:`2026-10668`
-----------------

Nuvoton NuMaker HSUSBD UDC 驱动中
主机可触发的控制端点卡死（DoS）

Nuvoton NuMaker HSUSBD USB 设备控制器驱动
（``drivers/usb/udc/udc_numaker.c``）
无条件地武装控制 Data IN 阶段
（``numaker_hsusbd_ep_trigger`` 中的
``base->CEPTXCNT = len``）。
由于 HSUSBD 硬件无法解除
已为先前传输武装的控制 Data IN，
取消一个进行中的控制传输（超时）
然后发出新 SETUP 报文的 USB 主机
可使驱动失同步：
新传输中可能发送过期数据，
且控制端点可永久卡死，
对每个后续控制传输 NAK。

恶意或有缺陷的主机
（驱动总线的物理/相邻攻击者）
可反复取消+重新 SETUP
卡死设备的 USB 控制端点，
拒绝设备 USB 功能的服务
（设备停止在控制管上枚举/响应）
直至 USB 复位或重新插入。
该缺陷为仅可用性的拒绝服务；
FIFO 拷贝循环（受 ``net_buf`` 长度
与硬件 BUFFULL 标志限制）
与 ``net_buf`` 生命周期
独立于武装失同步，
因此无越界访问、释放后使用
或信息泄露。

修复监视 IN-token 与新-SETUP 事件
（``k_event``），
仅在存在 IN token 且
未到达新 SETUP 时武装
控制 Data IN，
在新 SETUP 时取消当前传输。
影响使用 Nuvoton NuMaker HSUSBD
控制器的开发板
（``CONFIG_UDC_NUMAKER`` 与
``DT_HAS_NUVOTON_NUMAKER_HSUSBD_ENABLED``）；
随 v4.4.0 发布。

- `Zephyr 项目缺陷跟踪器 GHSA-rm28-x84j-4qrx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rm28-x84j-4qrx>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107010 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107010>`_

- `PR 110646 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110646>`_

:cve:`2026-10669`
-----------------

Xtensa MPU ``arch_buffer_validate()`` 整数溢出
使用户线程绕过系统调用指针校验

在构建 ``CONFIG_XTENSA_MPU`` 与
``CONFIG_USERSPACE`` 的 Xtensa SoC 上，
``arch/xtensa/core/mpu.c`` 的
``arch_buffer_validate()``——
架构钩子，用于验证用户模式提供的
缓冲区对调用用户线程以所请求权限
可访问——将其返回值默认为 0（允许访问），
仅在其每 MPU 区域探测循环内
设置拒绝结果。当缓冲区的
取整范围环绕 32 位地址空间
（size + 对齐偏移接近 ``SIZE_MAX``，
或 ``ROUND_UP(size + offset)``
溢出为 0）时，
循环执行零次，
函数返回 0 = 允许，
未探测任何 MPU 区域。

系统调用层预检
（``K_SYSCALL_MEMORY_SIZE_CHECK`` /
``Z_DETECT_POINTER_OVERFLOW``）
仅捕获原始 ``addr+size`` 环绕，
不覆盖 ``ROUND_UP`` 诱导的环绕，
且字符串路径
（``arch_user_string_nlen`` ->
``arch_buffer_validate``）
完全没有系统调用层保护。

因此非特权用户模式线程
可向任何通过
``k_usermode_from_copy``/``to_copy``
或 ``k_usermode_string_copy``
验证用户缓冲区的系统调用
传入构造的 ``(addr, size)``，
并使对其不应访问的内存
的验证成功；
内核随后从中读取（泄露）
或，在 ``write=1`` 时写入（破坏）
攻击者在线程代表下选择的内核
或其他分区内存，
使信息泄露、内存破坏、
权限提升与拒绝服务成为可能。

受影响版本：v3.7.0（添加
Xtensa MPU 用户空间支持时）
至 v4.4.0。
修复将默认值改为 ``-EINVAL``
（默认拒绝），
添加显式 ``size_add_overflow``
检查，
并在完整范围验证后
才设置成功值。

- `Zephyr 项目缺陷跟踪器 GHSA-4r4p-gh69-v6w4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4r4p-gh69-v6w4>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109000 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109000>`_

- `PR 109239 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109239>`_

- `PR 109238 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109238>`_

- `PR 109236 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109236>`_

:cve:`2026-10670`
-----------------

``k_thread_name_copy()`` 系统调用校验器中
用户可触发的内核空指针解引用（DoS）

``k_thread_name_copy()`` 系统调用的
``CONFIG_USERSPACE`` 验证处理程序
（``kernel/thread.c`` 的
``z_vrfy_k_thread_name_copy()``）
对调用者提供的线程指针调用
``k_object_find()``，
随后在未检查其是否为 ``NULL``
的情况下解引用返回的
``struct k_object``。
每当提供的指针不是已注册的
（静态或动态）内核对象时，
``k_object_find()`` 返回 ``NULL``。

修复前的保护测试的是
``thread == NULL`` 而非 ``ko == NULL``，
因此以任意非 NULL 但未注册的指针
（例如任意地址）调用
``k_thread_name_copy()`` 的
非特权用户模式线程通过 NULL 测试，
随后校验器通过 NULL 指针
读取 ``ko->type``。

由于系统调用校验器以监督者模式运行，
该 NULL 解引用是一次内核模式故障，
使系统停止或重启，
使不受信任的用户代码
跨越用户空间安全边界
使内核崩溃（拒绝服务）。
marshaller 在不做任何先前
``K_SYSCALL_OBJ`` 验证的情况下
将线程参数传给校验器，
因此坏指针直接到达该缺陷。

该缺陷影响启用 ``CONFIG_USERSPACE``
与 ``CONFIG_THREAD_NAME`` 的构建，
自约 v2.0.0 引入特殊查找以来存在，
存在于 v4.4.0 及更早版本。
修复将保护改为在解引用前
检查 ``k_object_find()`` 返回值
（``ko == NULL``）。

- `Zephyr 项目缺陷跟踪器 GHSA-82h2-v4vm-q2g9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-82h2-v4vm-q2g9>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109076 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109076>`_

- `PR 111088 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111088>`_

- `PR 111089 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111089>`_

- `PR 109364 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109364>`_

:cve:`2026-10671`
-----------------

用户线程可重新初始化使用中的 ``k_pipe``，
破坏内核等待队列（``CONFIG_USERSPACE``）

在 Zephyr 内核管道实现中，
用户空间系统调用校验器
``kernel/pipe.c`` 的
``z_vrfy_k_pipe_init()``
使用 ``K_SYSCALL_OBJ()``
（要求内核对象已初始化）
而非 ``K_SYSCALL_OBJ_NEVER_INIT()``
（拒绝已初始化的对象）。
结果是，在 ``CONFIG_USERSPACE``
构建上，
被授予访问 ``k_pipe`` 对象的
非特权用户线程
可调用 ``k_pipe_init`` 系统调用
重新初始化一个已在使用中的管道。

``z_impl_k_pipe_init()``
无条件重置环形缓冲区，
将 ``pipe->waiting`` 置 0，
并重新初始化两个等待队列
（``pipe->data`` 与
``pipe->space`` 上的 ``z_waitq_init``），
未唤醒或计入当前阻塞在管道上的线程。
任何已在 ``k_pipe_read()``/
``k_pipe_write()`` 中挂起的线程
被遗留孤立：
仍被标记为挂起，
``pended_on`` 指向被清空的等待队列，
且带有指向（现已重新初始化的）
内嵌列表头部的过期
``qnode_dlist`` 链接。

当这样一个孤立的等待者
稍后被超时或唤醒时，
调度器对其过期节点调用
``sys_dlist_remove()``，
通过悬空 ``prev``/``next`` 指针
写入内核等待队列/调度器结构，
导致列表损坏
（攻击者驱动的无效内核写入）、
丢失的唤醒、
无限期阻塞的线程
与静默数据丢失。
该缺陷使降权用户线程
破坏与其他线程/分区共享的
内核对象状态。

修复将校验器切换为
``K_SYSCALL_OBJ_NEVER_INIT()``，
匹配现有的 ``k_msgq_init`` 校验器，
使用户线程无法再重新初始化
一个存活的管道。
易受攻击的代码随 v4.1.0 发布，
持续至 v4.4.0。

- `Zephyr 项目缺陷跟踪器 GHSA-p8w8-3x99-mg8f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p8w8-3x99-mg8f>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109091 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109091>`_

- `PR 111101 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111101>`_

- `PR 111102 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111102>`_

:cve:`2026-10672`
-----------------

未终止的 URI 缓冲区导致 LwM2M 固件拉取
（Package URI）中的越界读取

``subsys/net/lib/lwm2m/lwm2m_pull_context.c``
通过 ``memcpy(context.uri, uri,
LWM2M_PACKAGE_URI_LEN)``
将固件更新 Package URI
拷贝到一个固定静态缓冲区
（``context.uri``，大小
``CONFIG_LWM2M_SWMGMT_PACKAGE_URI_LEN``，
默认 128），
精确拷贝目标大小且
无长度校验。
Firmware-Update 对象将服务器提供的
Package URI（/5/0/1）
存储在 255 字节缓冲区中，
因此 LwM2M 管理服务器
（或缺乏强 DTLS 会话上的在途攻击者）
可 WRITE 一个 128-254 字符的 URI；
随后仅前 128 字节被拷贝到
``context.uri``，无 NUL 终止符。
该缓冲区随后作为 C 字符串被
``http_parser_parse_url(context.uri,
strlen(context.uri), ...)``、
基于 ``strlen`` 的 CoAP
URI-path/PROXY-URI 选项追加
与 ``lwm2m_parse_peerinfo()``
消费，导致相邻静态内存的越界读取。
越读字节被追加到出站 CoAP 请求
（向服务器/代理泄露相邻设备内存
的信息）并可使设备崩溃
（拒绝服务）。
易受攻击的拷贝由 pull-context
重构引入（首次随 v3.0.0 发布），
存在于 v4.4.0（含）为止；
默认启用的
``CONFIG_LWM2M_FIRMWARE_UPDATE_PULL_SUPPORT``
路径受影响。
修复添加返回 ``-ENOMEM`` 的
``strlen(uri) >= sizeof(context.uri)``
检查，
并切换为 ``strcpy()``，
保证一个有界的、NUL 终止的缓冲区。

- `Zephyr 项目缺陷跟踪器 GHSA-rf6j-4mpp-j9mf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rf6j-4mpp-j9mf>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108964 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108964>`_

- `PR 109235 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109235>`_

- `PR 109234 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109234>`_

- `PR 109233 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109233>`_

:cve:`2026-10674`
-----------------

NXP LPUART 驱动中的拒绝服务（硬故障）：
不支持的运行时 UART 配置使时钟保持禁用

NXP LPUART 串行驱动
（``drivers/serial/uart_mcux_lpuart.c``）
在启用 ``CONFIG_UART_USE_RUNTIME_CONFIGURE``
时，
在 ``mcux_lpuart_configure()`` 开头
调用 ``LPUART_Deinit()``，
该函数禁用 LPUART 外设时钟。
所请求的配置仅在此之后
（在 ``mcux_lpuart_configure_basic`` 中）
验证，
且不支持的奇偶/数据位/停止位/流控值
在时钟重新启用前返回 ``-ENOTSUP``。

结果是，
一个携带不支持配置的
``uart_configure()`` 请求
使 LPUART 停留在时钟禁用状态；
随后任何对 LPUART 寄存器的访问
（``poll_out``/``poll_in``、中断处理
或稍后的重新配置）
在门控的外设上故障
并升级为硬故障，使系统崩溃。

``uart_configure()``
是一个 Zephyr 系统调用，
其校验器（``z_vrfy_uart_configure``）
仅检查 ``cfg`` 为可读用户内存
并无变化地转发调用者提供的配置，
因此有 LPUART 设备访问权限的
非特权用户空间线程
可确定性地触发该故障，
一次持久性的系统级拒绝服务。

在 v2.5.0 引入，
存在于此后所有发布直至本修复，
该修复移除 ``LPUART_Deinit()`` 调用，
改为仅禁用发送器/接收器，
使时钟保持运行。

- `Zephyr 项目缺陷跟踪器 GHSA-mw68-r353-m3vf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-mw68-r353-m3vf>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107186 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107186>`_

- `PR 111106 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111106>`_

- `PR 111105 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111105>`_

- `PR 111104 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111104>`_

:cve:`2026-10675`
-----------------

Bluetooth Mesh PB-ADV：失效的配网链路
被无限期保活，阻塞（重新）配网（DoS）

在 Zephyr 的 Bluetooth Mesh PB-ADV
配网承载（``subsys/bluetooth/mesh/pb_adv.c``）中，
``prov_msg_recv()``
无条件地在函数顶部、
FCS 检查与 ``ADV_LINK_INVALID``
检查之前重新调度配网协议看门狗定时器。
一旦配网尝试失败，
``prov_failed()`` 设置 ``ADV_LINK_INVALID``，
唯一恢复路径是协议定时器触发
（``protocol_timeout`` ->
``prov_link_close`` -> ``close_link`` ->
``reset_adv_link`` 以及扫描与
未配网设备信标的重新启用）。

BLE 广告信道上的远程、未认证攻击者
可首先诱发一次配网失败
（例如通过一个畸形的
generic-provisioning PDU），
然后以高于每协议超时
（60 秒，或 OOB 输入/输出为 120 秒）
一次的频率在同一链路 ID 上
发送任何 FCS 有效的 PB-ADV 事务 PDU。
由于每个这样的报文
即使在失效链路上也重置定时器，
``protocol_timeout`` 永不触发，
死链路从不被拆除，
设备被固定在不可配网状态，
其未配网信标被禁用
且新的 Link Open 请求被拒绝。

PB-ADV PDU 在无认证的情况下处理，
且 FCS 是无密钥 CRC，
因此无需配对或先前信任，
且攻击者自行选择链路 ID。
影响是配网/重新配网服务的持久拒绝；
无内存安全、机密性或完整性影响。

易受攻击的代码随发布至 v4.4.1 发布。
修复将定时器重新调度
移到 ``ADV_LINK_INVALID`` 检查之后
（以及重置前的 FCS 检查），
使失效链路无法再被
入站报文保活。

- `Zephyr 项目缺陷跟踪器 GHSA-4rwg-6mr4-55hc
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4rwg-6mr4-55hc>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109324 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109324>`_

- `PR 110910 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110910>`_

- `PR 110909 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110909>`_

- `PR 110911 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110911>`_

:cve:`2026-10677`
-----------------

``z_vrfy_k_poll()`` 中的内核堆内存泄露
使非特权用户线程耗尽内核资源池

``kernel/poll.c`` 中的
``CONFIG_USERSPACE`` 系统调用校验器
``z_vrfy_k_poll()``
通过 ``z_thread_malloc()``
分配用户提供的 ``k_poll_event[]``
的内核侧副本，
然后验证每个事件的对象句柄。
在本修复之前，
验证在循环内联使用
``K_OOPS(K_SYSCALL_OBJ(...))``，
该宏杀死调用线程而不释放
``events_copy``。

用户线程可传入 ``num_events >= 1``
与一个伪造对象句柄来泄露该分配；
由于新派生的用户线程
继承父线程的 ``resource_pool``
（``kernel/thread.c``），
攻击者派生牺牲线程
重复泄露直至共享内核堆耗尽。
一旦耗尽，
来自该池的合法内核分配
（``k_queue`` 分配节点、``k_msgq`` 缓冲区、
未来的 ``k_poll`` 调用等）
失败，
导致系统级拒绝服务。

修复将每个内联 ``K_OOPS``
替换为条件 ``goto oops_free``，
使线程被杀死前缓冲区被释放。
影响 Zephyr 发布：
自 v1.12.0（``k_poll``
首次暴露给用户模式）
至 v4.4.1。

- `Zephyr 项目缺陷跟踪器 GHSA-r3cc-8wcr-xfj9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r3cc-8wcr-xfj9>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109361 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109361>`_

- `PR 111111 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111111>`_

- `PR 111112 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111112>`_

- `PR 109535 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109535>`_

:cve:`2026-10678`
-----------------

由未认证 I2C 控制器驱动的 Zephyr MCTP I2C+GPIO
目标绑定中的空指针/越界写入

Zephyr 中的 MCTP-over-I2C+GPIO 目标绑定
（``subsys/pmci/mctp/mctp_i2c_gpio_target.c``）
在 ``mctp_i2c_gpio_target_write_received()`` 中
逐字节处理来自 I2C 总线主机的伪寄存器写入，
不验证顺序或接收缓冲区。
在受影响版本中，
``MCTP_I2C_GPIO_RX_MSG_ADDR``（数据）处理程序
在未检查接收缓冲区是否已分配的情况下
解引用并通过 ``b->rx_pkt`` 写入：
一个选择数据寄存器并在未先发送
长度寄存器（即分配缓冲区的那个）的情况下
写入一个字节的控制器，
导致通过一个 NULL/未分配的
``mctp_pktbuf`` 指针
写入一个攻击者选择的字节
（即写入地址 0 上方一个
攻击者可推进的小偏移处），
产生内存破坏或硬故障。

同一处理程序还执行
先写后检查的边界测试，
在发送超过 255 个数据字节时
允许 ``data[255]`` 处的
单字节堆溢出。

由于 I2C 目标回调
以总线主设备提供的原始字节调用，
且该绑定不做认证，
总线上的恶意或故障控制器
可无需任何先前协议状态
触发这些，
导致目标设备上的内存破坏
和/或拒绝服务。

易受攻击的代码在
I2C+GPIO 目标绑定添加时引入，
随 Zephyr v4.3.0 与 v4.4.0 发布。
修复将分配延迟到第一个数据字节
并带 NULL 检查，
将缺失长度视为
被 libmctp 拒绝的零大小报文，
并将边界检查移到存储之前。

- `Zephyr 项目缺陷跟踪器 GHSA-pmwm-5rcm-39rr
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-pmwm-5rcm-39rr>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109428 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109428>`_

- `PR 111118 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111118>`_

- `PR 111117 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111117>`_

:cve:`2026-10679`
-----------------

DesignWare SPI 驱动中可从
spi_transceive 系统调用触达的
除零（本地 DoS）

DesignWare SPI 驱动（``drivers/spi/spi_dw.c``）
计算 SPI BAUDR 时钟分频器为
``info->clock_frequency / config->frequency``，
不验证 ``config->frequency``。

``spi_transceive``
是一个 Zephyr ``__syscall``，
其验证处理程序
（``drivers/spi/spi_handlers.c``）
从用户空间拷贝调用者提供的
``spi_config``，不检查频率字段，
因此被授予访问 DesignWare SPI 设备
内核对象的用户空间线程
可传入 ``frequency = 0``，
在 ``spi_dw_configure()`` 中触发
无符号整数除零。

在 Cortex-M Mainline
（``z_arm_fault_init()`` 中设置
``SCB->CCR.DIV_0_TRP``）
与 ARC（专用的 ``__ev_div_zero`` 向量）上，
这引发 CPU 异常，
导致内核故障与本地拒绝服务。

修复以 ``-EINVAL`` 拒绝零频率
与高于 ``clock_frequency / 2``
（DesignWare SSI 数据手册最小 SCKDIV 2）
的频率。该缺陷影响所有
Zephyr 发布至 v4.4.0（含）；
利用需要 ``CONFIG_USERSPACE=y``
与一个已被授予 SPI 驱动权限的
非特权线程。
无内存破坏或信息泄露影响。

- `Zephyr 项目缺陷跟踪器 GHSA-3qcm-qwh2-v4hq
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3qcm-qwh2-v4hq>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 105452 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/105452>`_

- `PR 111121 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111121>`_

- `PR 111120 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111120>`_

:cve:`2026-10680`
-----------------

Zephyr BR/EDR L2CAP 配置请求处理中
通过 ``uint16_t`` 长度下溢的越界访问

Classic（BR/EDR）L2CAP 信令处理程序
``subsys/bluetooth/host/classic/l2cap_br.c``
的 ``l2cap_br_conf_req()`` 与
``l2cap_br_conf_rsp()``
将最小命令大小与 ``buf->len``
（整个接收 PDU 中剩余的字节）
而非 ``len``（来自 L2CAP 信令头的
每命令数据长度）校验。
由于多个信令命令可打包进一个 PDU，
``buf->len`` 可能超过
命令的 ``len``。
攻击者可发送一个头部长度
小于配置请求结构
（例如 0）的 ``CONF_REQ`` 命令，
后跟另一个命令，
使 ``buf->len`` 仍满足检查。
检查随后错误通过，
``opt_len = len - sizeof(*req)``
使 ``uint16_t`` 下溢为
接近 0xFFFF 的值。
缺少 ``opt_len`` 对 ``buf->len``
保护的配置选项循环
随后使用不执行运行时边界检查的
``net_buf`` pull 原语
远远越过池化 ACL 接收缓冲区末尾，
产生主机内存的越界读取，
且当越界选项字节编码
MTU 或 flush-timeout 选项时，
一次越界写入。
BR/EDR 信令信道在
配对/加密之前处理，
且可打开到 SDP 等 L0 服务的
L2CAP 信道而无需配对，
因此能在无线电范围内建立 ACL 连接的
未认证对端可触发该缺陷，
导致内存破坏与拒绝服务
（主机/设备崩溃）。
该缺陷存在于包括 v4.4.0 在内的
发布版本中。
修复在两个处理程序中
改为对 ``len`` 而非 ``buf->len``
校验。

- `Zephyr 项目缺陷跟踪器 GHSA-vrwx-p97q-8854
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vrwx-p97q-8854>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109308 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109308>`_

- `PR 110661 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110661>`_

- `PR 110662 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110662>`_

- `PR 111405 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111405>`_

:cve:`2026-10681`
-----------------

``thread_idx_alloc()`` 中的 SMP 竞态
使并发 ``k_object_alloc(K_OBJ_THREAD)``
调用者共享一个内核对象权限槽

在 Zephyr 用户空间动态对象子系统中，
``kernel/userspace/userspace.c``
的 ``thread_idx_alloc()``
在未持有 ``lists_lock`` 的情况下
从全局 ``_thread_idx_map[]`` 位图
分配一个新的线程权限索引。

在 SMP 系统上，
两个并发调用
``k_object_alloc(K_OBJ_THREAD)``
系统调用的用户模式线程
可观察到同一个低位空闲位，
执行相同的非原子 RMW 清除它，
并返回相同的 ``tidx``。

两个新创建的 ``K_OBJ_THREAD`` 对象
随后被分配相同的 ``thread_id``，
因此两个用户线程
在每个内核对象的 ``perms[]``
位域中别名一个单位置：
随后对任一线程在内核对象上
的任何访问授权
隐式也是对另一线程的授权，
破坏用户空间 ACL 隔离。
在 alloc 中无锁的 ``&=~BIT()``
与 ``thread_idx_free()`` 中
加锁的 ``|= BIT()`` 之间
一个次要的丢失更新窗口
也可从线程索引池泄露条目。

该缺陷可从任何用户模式线程
通过不受限的 ``__syscall``
``k_object_alloc`` 触达，
并受 ``CONFIG_USERSPACE``、
``CONFIG_DYNAMIC_OBJECTS``
与 ``CONFIG_SMP`` 门控。
该缺陷在 2018 年添加
每线程权限索引时引入，
存在于每个发布至 v4.4.0（含）。
通过跨位图 RMW 与
权限清除持有 ``lists_lock``
（并内联先前自行取锁的
``obj_list`` 遍历）修复。

- `Zephyr 项目缺陷跟踪器 GHSA-j693-5rh5-8g8h
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j693-5rh5-8g8h>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109616 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109616>`_

- `PR 111409 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111409>`_

- `PR 111410 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111410>`_

- `PR 111408 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111408>`_

:cve:`2026-10682`
-----------------

Zephyr ``log_filter_set`` 系统调用校验器中
可从用户空间触达的越界写入

``subsys/logging/log_mgmt.c`` 中
``log_filter_set`` 系统调用的
用户空间校验器
``z_vrfy_log_filter_set()``
对 ``int16_t`` ``src_id`` 参数
执行有符号比较：
``src_id < (int16_t)log_src_cnt_get(domain_id)``。
``src_id`` 的任何负值
（例如 -1）
平凡地满足该检查，
并被转发到 ``z_impl_log_filter_set``，
后者传播到 ``filter_set()``，
最终到 ``get_dynamic_filter()``，
后者将 ``source_id``
作为无符号索引
用于链接器节数组
``&TYPE_SECTION_START(log_dynamic)[source_id].filters``。

通过 ``uint32_t`` 隐式转换后，
``int16_t`` -1 变为 0xFFFFFFFF，
使 ``log_dynamic`` 索引远远越界，
导致内核对 ``log_dynamic`` 节
相邻内存执行一次 OOB 读取
与一次 OOB 读-改-写
（``LOG_FILTER_SLOT_GET/SET``）。

所写值是在目标 32 位字内
一个受限的 3 位日志级别槽，
但目标地址由攻击者选择
（``log_dynamic`` 上方一个小负偏移），
且写入发生在
来自非特权用户线程的系统调用之后
的监督者模式，
提供一个内核内存破坏/权限提升原语。

该缺陷在任何 ``CONFIG_USERSPACE=y``
与 ``CONFIG_LOG_RUNTIME_FILTERING=y``
的构建上可触达。
存在于 Zephyr v3.3.0 至 v4.4.1。
修复将有符号边界检查
替换为无符号比较：
``(uint32_t)src_id <
log_src_cnt_get(domain_id)``，
正确拒绝负输入。

- `Zephyr 项目缺陷跟踪器 GHSA-6vqh-mg7h-58qh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6vqh-mg7h-58qh>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109690 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109690>`_

- `PR 111418 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111418>`_

- `PR 111419 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111419>`_

- `PR 111417 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111417>`_

:cve:`2026-10683`
-----------------

DesignWare I2C 目标驱动可被
总线上主机卡入永久卡死状态（DoS）

在 Synopsys DesignWare I2C 驱动
（``drivers/i2c/i2c_dw.c``）
以目标/从机模式运行时，
``rx_full`` 中断处理程序
以 ``dw->state`` != ``CMD_SEND``
门控 ``write_requested()`` 回调，
而 ``dw->state``
仅在 STOP 中断时
重置为 READY。
``START_DET`` 中断——
其 ``i2c_dw_slave_read_clear_intr_bits()``
中的处理程序
会在每次 (re)START 时
重置状态——
从未被添加到
``i2c_dw_slave_register()``
中的启用中断掩码，
因此该恢复路径是死代码。

结果是，
如果 STOP 中断丢失
（总线毛刺/复位，
或并发主机驱动 STOP）
或总线主机发出
合法的 WRITE-重复START-WRITE
序列且方向相同，
驱动永久停留在 ``CMD_SEND``，
在其目标生命周期内
不再调用 ``write_requested()``。

同一物理总线上的 I2C 主机
可故意触发，
导致 I2C 目标功能
对所有后续写事务故障
并使消费者分帧状态失同步
（例如 MCTP-over-I2C），
一次可通过复位恢复的
目标外设拒绝服务。

修复解除 ``START_DET`` 掩码，
使状态在每次总线 (re)START 时重置。
影响仅为本地板级总线上
的可用性；
树内消费者无内存破坏结果，
其逐字节缓冲区写入
独立地边界检查。

- `Zephyr 项目缺陷跟踪器 GHSA-fj9c-r5qw-3639
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fj9c-r5qw-3639>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107537 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107537>`_

- `PR 111415 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111415>`_

- `PR 111414 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111414>`_

:cve:`2026-10684`
-----------------

coredump shell 在打印存储转储目标代码时的
越界读取

在 ``subsys/debug/coredump/coredump_shell.c`` 中，
``print_coredump_hdr()``
将存储的 Zephyr coredump 头的
16 位 ``tgt_code`` 字段
直接用作
``coredump_target_code2str[]``
——一个固定 7 元素的
字符串指针数组——的索引，
无边界检查。

``tgt_code`` >= 7 的存储 coredump
导致越界读取一个 ``char*``，
最多越过数组约 64K 个条目；
该值作为 ``%s`` 参数传给
``shell_print``，
后者将其解引用并作为字符串遍历。
结果是向 shell 用户
泄露设备内存内容，
或在越界指针未映射时崩溃。

该缺陷通过 ``coredump print``
shell 命令触达
（``cmd_coredump_print_stored_dump`` ->
``pretty_print_coredump`` ->
``parse_and_print_coredump`` ->
``print_coredump_hdr``）。
``tgt_code`` 字段
在正常崩溃处理中
由设备生成且在范围内，
因此触发需要本地 shell 访问
加在 flash/内存后端中
暂存或损坏存储 coredump 的能力。

在 v4.2.0 引入（commit 13abd7fe730），
存在于 v4.4.0（含）为止；
通过将越界代码钳制到
'unknown'（索引 0）条目修复。

- `Zephyr 项目缺陷跟踪器 GHSA-9fw2-4429-49q8
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9fw2-4429-49q8>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109630 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109630>`_

- `PR 111421 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111421>`_

- `PR 111422 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111422>`_

:cve:`2026-10685`
-----------------

Bluetooth 主机 CCC 写响应处理程序中
GATT 订阅参数的释放后使用

Zephyr Bluetooth GATT 客户端
CCC 写响应处理程序
``subsys/bluetooth/host/gatt.c`` 的
``gatt_write_ccc_rsp()``
在已调用
``params->notify(conn, params, NULL, 0)``
之后调用应用的
``params->subscribe()`` 回调。

按公共 GATT API，
``data`` 为 ``NULL`` 的
notify 回调
是文档化的信号，
表示订阅已终止
且 ``bt_gatt_subscribe_params``
结构可被应用释放或复用；
之后对该结构调用 ``subscribe()``
是释放后使用，
包括通过已释放的
``params->subscribe``
函数指针的间接调用。

错误分支可被远程（相邻）触达：
一个作为 GATT 客户端调用
``bt_gatt_subscribe()`` 的
Zephyr 设备
可被驱动到该顺序，
当连接的 GATT 服务器对端
以 ATT Error Response
应答 CCC 写时
（对端提供的错误码
通过 ``att_error_rsp`` ->
``att_handle_rsp``
流入 ``gatt_write_ccc_rsp``）。

对于在通知终止处理程序中
释放或回收订阅参数的应用，
这导致内存破坏、
崩溃（拒绝服务）
或潜在受攻击者影响的控制流。
修复重新排序处理程序，
使 ``subscribe()`` 回调
在错误与退订路径中
终止的 ``notify(NULL)``
之前运行。

- `Zephyr 项目缺陷跟踪器 GHSA-29xh-jm2m-4qvx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-29xh-jm2m-4qvx>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 99920 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/99920>`_

- `PR 111430 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111430>`_

- `PR 111429 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111429>`_

- `PR 111428 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111428>`_

:cve:`2026-10686`
-----------------

Zephyr 路由器中 IPv6 转发路径
缺少 hop-limit 递减
允许无界报文循环（DoS）

Zephyr 的 IPv6 转发路径
重新发送路由的组播报文时
从不递减 IPv6 hop limit。
``ipv6_route_packet()``
（``subsys/net/ip``）的
两个路由分支均受影响：
显式路由路径
（``net_route_packet()``）
与链路内跨接口路径
（``net_route_packet_if()``）。
每个设置报文转发标志
并以未触碰的 hop limit
与无过期检查调用
``net_send_data()``。

按 RFC 8200，
hop-limit 递减
是限制报文生命周期
并终止路由循环的机制；
没有它，
作为 IPv6 路由器的设备
无限期中继循环报文。
能诱发或利用瞬时 L3 循环的
在途攻击者
将其变为永久转发风暴，
导致转发器与相邻链路上
CPU/带宽资源耗尽
（可用性 DoS）；
依赖 hop-limit 过期的
路径发现与循环诊断
也被击败。

**受影响配置。**
在所有受影响发布中，
转发路径通过
``CONFIG_NET_ROUTE``
（设置 ``CONFIG_NET_IPV6_NBR_CACHE``
时默认启用）
与用于跨接口路由的
``CONFIG_NET_ROUTING`` 触达。
注意 ``CONFIG_NET_IPV6_FORWARDING``
与 ``CONFIG_NET_IPV4_FORWARDING``——
它们出现在修复与本通告的
证据注释中——
是在 v4.4.0 之后引入的，
当时路由选项被拆分并重命名；
它们不存在于任何受影响发布中。
审计 v4.4.1 或更早的配置时，
查找 ``CONFIG_NET_ROUTE``
与 ``CONFIG_NET_ROUTING``。

**IPv4 在任何发布中均不受影响。**
IPv4 转发路径
（``route_ipv4.c`` 的
``net_route_ipv4_packet()``）
在 v4.4.0 之后添加
且从未随发布发布。
其 TTL 递减与
IPv4 头校验和重计算
作为同一修复的一部分
落在 ``main`` 上，
因此下文证据注释讨论它，
但没有发布版本
可通过 IPv4 触达。

受影响发布为 v1.8.0 至 v4.4.1：
v1.8.0 引入 ``net_route_packet()``，
v2.2.0 添加 ``net_route_packet_if()``，
两者均不递减 hop limit。
v4.3.1 携带显式路由修复
但不携带链路内修复，
因此同样受影响。
在 ``main`` 上由
7d8f1afa7345（显式路由路径）
与 589eadc74efa（链路内路径）修复。

- `Zephyr 项目缺陷跟踪器 GHSA-4cg6-6jc4-2r6h
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4cg6-6jc4-2r6h>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109585 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109585>`_

- `PR 111451 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111451>`_

- `PR 111450 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111450>`_

- `PR 111449 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111449>`_

:cve:`2026-10687`
-----------------

在 2026-08-01 之前处于保密期（embargo）

:cve:`2026-10772`
-----------------

在 2026-08-01 之前处于保密期（embargo）

:cve:`2026-10773`
-----------------

DHCPv4 客户端报文类型名称查找
（net_dhcpv4_msg_type_name）中的越界读取

``subsys/net/lib/dhcpv4/dhcpv4.c``
中的 DHCPv4 客户端助手
``net_dhcpv4_msg_type_name()``
在有缺陷的边界检查之后
索引一个静态 8 元素的
``const char *`` 名称表。
保护使用
``msg_type <= sizeof(name)``
而非 ``msg_type <= ARRAY_SIZE(name)``；
``sizeof`` 返回指针数组的
字节大小（32 位目标 32，
64 位目标 64）
而非 8 的元素计数，
因此 9 至该字节大小的
报文类型值通过检查，
导致 ``name[msg_type - 1]``
读取越过数组末尾。

``msg_type`` 值
源自 DHCP MESSAGE TYPE 选项，
该选项从接收报文
作为未检查的原始字节读取
（``net_pkt_read_u8``）
并无修改地传入查找。
因此 DHCP 服务器
或任何能在客户端链路上
注入伪造 DHCP 应答的主机
可使索引越界。
越界槽位产生一个
垃圾 ``const char *``，
随后被 ``%s`` 日志转换解引用。

查找仅从调试日志语句
（``NET_DBG`` / ``LOG_DBG``）触达，
因此越界读取
仅在 DHCPv4 日志模块
以 DEBUG 级别构建时
（``CONFIG_NET_DHCPV4_LOG_LEVEL_DBG``）
可触发，
这不是默认配置。
当该条件成立时，
结果是越界读取
与野指针解引用：
最可能是 DHCP 客户端崩溃
（拒绝服务），
并可能通过日志输出
泄露相邻指针的内容。
修复以 ``ARRAY_SIZE``
替换 ``sizeof``，
恢复正确的 1..8 接受窗口。

- `Zephyr 项目缺陷跟踪器 GHSA-r5hq-xq42-wcfq
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r5hq-xq42-wcfq>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110135 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110135>`_

- `PR 112423 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112423>`_

- `PR 115146 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/115146>`_

:cve:`2026-10774`
-----------------

Bluetooth Mesh 子网删除中的 PSA 密钥槽泄露
导致资源耗尽 DoS

Zephyr 的 Bluetooth Mesh 子网密钥管理
在每次子网密钥拆除时
泄露一个 PSA Crypto 密钥槽。
在 ``subsys/bluetooth/mesh/subnet.c`` 中，
``net_keys_create()``
在 ``CONFIG_BT_MESH_PRIV_BEACONS``
（默认启用）下
将 Private Beacon Key
导入 PSA 密钥槽，
但 ``subnet_keys_destroy()``
以 ``CONFIG_BT_MESH_V1d1``
保护对应的 ``psa_destroy_key()``。
该 Kconfig 符号在
移除显式 Mesh 1.0.1 支持时
被移除，
因此销毁分支成为永久死代码，
导入从不被销毁平衡。

不平衡的拆除
在每次子网密钥被销毁时触达：
删除子网（Config Server NetKey Delete）、
完成 Key Refresh Procedure
（退役旧密钥集）
以及重置/重新配网节点。
空中触发仅在该节点的设备密钥下
处理，
因此可被拥有该节点的
配网器或网络管理员
经 Bluetooth Mesh 网络触达。

在默认
``CONFIG_MBEDTLS_PSA_KEY_SLOT_COUNT``
16 下，
重复的添加/删除或密钥刷新循环
在约一轮之后耗尽
共享 PSA 密钥槽池。
一旦耗尽，
``bt_mesh_private_beacon_key()``
及因此子网创建失败：
节点无法再添加子网
或完成密钥刷新，
且设备上的其他 PSA crypto
消费者可能被饿死，
直至设备重启。
修复使销毁保护
与导入保护
（``CONFIG_BT_MESH_PRIV_BEACONS``）
对齐，
使每个槽位被释放。

- `Zephyr 项目缺陷跟踪器 GHSA-6q7g-798f-76p2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6q7g-798f-76p2>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110235 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110235>`_

- `PR 110438 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110438>`_

- `PR 110437 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110437>`_

- `PR 110436 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110436>`_

:cve:`2026-10848`
-----------------

Zephyr OCPP 1.6 RPC 报文解析器
（parse_rpc_msg）中的越界读取

``subsys/net/lib/ocpp`` 中的
OCPP 1.6 客户端
在 ``parse_rpc_msg()``
（``subsys/net/lib/ocpp/ocpp_j.c``）中
使用一个手写助手
``extract_string_field()``
解析入站 WAMP RPC 帧，
后者以
``strncpy(out_buf, token + 1, outlen - 1)``
拷贝报文的 ``uid`` 与 ``action`` 字段，
随后用
``strchr(out_buf, '"')``
扫描结果。
由于 ``strncpy``
在源长度至少为 ``outlen - 1``
（127）字节时
不 NUL 终止目标，
随后的 ``strchr``
越过 128 字节目标缓冲区
读取到相邻栈内存；
如果在缓冲区之外找到 ``"`` 字节，
还会发生一次单字节越界 NUL 写入。
``extract_payload()`` 中
一个相关缺陷
在接收缓冲区上运行
``strchr``/``strrchr``，
当最大长度帧填满该缓冲区时
它可能未 NUL 终止。

被解析字节
直接来自 OCPP 中央系统服务器
经 websocket：
读取线程通过
``websocket_recv_msg()``
填充 ``recv_buf``
并对每个入站 DATA 帧
调用 ``parse_rpc_msg()``
（``subsys/net/lib/ocpp/ocpp.c``）。
恶意或被入侵的中央服务器
或在途攻击者
（OCPP 通常部署在
明文 ``ws://`` 上）
可发送一个
``uid`` 或 ``action`` 字段
为 127+ 字节且
无闭合引号的 RPC 帧，
触发越界访问。

主要影响是
可远程触发的拒绝服务：
无界扫描
可在未映射页上故障，
且杂散 NUL 写入
可破坏相邻栈状态。
越读数据
不反映给对端，
因此泄露有限。
该特性为 EXPERIMENTAL
且必须显式启用
（``CONFIG_OCPP``）。
修复以
尊重边界的
``json_mixed_arr_parse()``
替换手动解析器，
并以显式 NUL 终止的缓冲区
拷贝提取的 ``uid``，
消除两次越读。

- `Zephyr 项目缺陷跟踪器 GHSA-jgqq-7mjj-w642
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jgqq-7mjj-w642>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 95399 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/95399>`_

- `PR 112426 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112426>`_

:cve:`2026-10849`
-----------------

Zephyr hawkBit OTA 客户端在
终止服务器响应体时的
堆越界写入

``subsys/mgmt/hawkbit`` 中的
hawkBit 设备管理客户端
在 ``response_json_cb()``
（``subsys/mgmt/hawkbit/hawkbit.c``）中
将来自更新服务器的
HTTP 响应体累积到一个堆缓冲区。
缓冲区被定长以容纳
接收的体字节，
但不为终止 NUL 保留空间。
当完整响应到达时，
代码写入
``response_data[downloaded_size] = '\0'``——
每当累积体长度等于分配时，
该终止符落在
堆对象末尾之后一个字节
（基于堆的越界写入，
CWE-122 / CWE-787）。

体长度与分片
直接取自解析的 HTTP 响应
（``rsp->body_frag_start`` /
``rsp->body_frag_len``），
完全由远程 hawkBit 服务器控制，
后者选择自己的响应长度。
精确触发
取决于缓冲区如何增长，
两种形式均可远程触达。
自 v4.0.0 起，
重新分配被定长为
恰好 ``downloaded_size + body_len``，
因此**任何**
大于 1100 字节初始缓冲区的
响应体
使越界写入确定性地发生；
这样的响应大小
对 hawkBit 部署元数据
是常见的。
在 v4.0.0 之前，
缓冲区通过倍增增长
且增长检查
（``(downloaded_size + body_len)
> response_buffer_size``）
在相等时为假，
因此体长度
恰好等于当前分配——
默认初始缓冲区为 1100 字节——
的响应体
完全跳过重新分配
并在 1100 字节对象的
``response_data[1100]``
写入终止符。
HTTP 长度不匹配检查
不捕获此，
因为声明与接收长度
确实一致。
两种形式
均可被恶意、被入侵
或中间人的更新服务器触达
（TLS 是可选的，
且启用时
不防对抗性服务器），
无响应内容认证
且无客户端长度上限
保护该写入。

越界写入是
分配之后紧邻的
固定单 NUL 字节，
破坏相邻分配器元数据
或下一个分配。
实际影响是
导致拒绝服务的堆破坏
（后续分配或释放时故障），
带有有界的、
依赖分配器的
进一步破坏可能性。
修复将缓冲区
定长为体长度加一
并以 ``memcpy`` 拷贝，
确保终止符
始终落在分配内。

- `Zephyr 项目缺陷跟踪器 GHSA-39h3-7phx-pwhv
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-39h3-7phx-pwhv>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109285 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109285>`_

- `PR 112429 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112429>`_

- `PR 112428 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112428>`_

- `PR 115262 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/115262>`_

:cve:`2026-11368`
-----------------

Bluetooth 主机 ATT 在
传输中断开时
TX 完成的释放后使用

Bluetooth 主机 ATT 层
（``subsys/bluetooth/host/att.c``）
通过静态
``tx_meta_data_storage[]`` 数组
（``data->att_chan = chan``）
将每个进行中的 ATT TX 缓冲区
与其所属信道关联。
当缓冲区的最后一个引用被丢弃时，
其 net-buf 销毁回调
将完成处理
延迟到系统工作队列
（``att_tx_destroy`` ->
``att_tx_destroy_work_handler`` ->
``att_on_sent_cb`` ->
``bt_att_sent``），
其中 ``bt_att_sent``
解引用信道及其 ATT 上下文
（``sys_slist_get(&att->reqs)``）。

当对端在
一个 ATT PDU
（服务器通知/指示
或任何响应）
仍在控制器 TX 路径中
进行中时断开，
L2CAP 在 ``l2cap_chan_del()``
拆除信道：
它运行 disconnected 回调
然后 released 回调
（``bt_att_released``），
后者释放信道 slab 槽位。
由于进行中的缓冲区
由连接 TX 路径
而非信道自身队列持有，
其延迟的销毁工作
可在信道被释放后运行。
``att_on_sent_cb`` 保护
本意丢弃过期回调本身
却解引用 ``meta->att_chan``，
该指针现在是
指向已释放
（且可能已被复用）
slab 槽位的悬空指针。

拥有 ATT 连接的远程对端
可通过在常规 ATT 流量期间
断开驱动该；
触达 ATT 承载
无需配对或用户交互。
结果是
对已释放信道内存的
释放后使用读/写，
可靠地使 Bluetooth 主机崩溃
（拒绝服务），
且由于信道 slab 槽位
可能被复用，
潜在破坏存活内存。

修复使
``bt_att_released()``
在释放之前
将所有仍引用该信道的
``tx_meta_data_storage[]`` 条目的
``att_chan`` 字段
置为 ``NULL``，
使延迟保护
观察到 ``NULL`` 指针
并丢弃回调。
拆除与销毁工作
都在协作式系统工作队列上运行，
因此数组更新
被序列化
且无需锁。

- `Zephyr 项目缺陷跟踪器 GHSA-85vg-gwc4-77g7
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-85vg-gwc4-77g7>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110416 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110416>`_

- `PR 112431 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112431>`_

:cve:`2026-11742`
-----------------

内核 ``k_queue_peek_head/tail``
中因缺少自旋锁的
释放后使用竞态

内核队列助手
``kernel/queue.c`` 的
``z_queue_node_peek()``
解引用从队列 ``data_q`` 列表
取出的节点，
读取节点的标志字节
以及，对于通过
``k_queue_alloc_append``/
``alloc_prepend`` 入队的项，
内部分配的
``alloc_node`` 结构
的数据指针。
``z_impl_k_queue_peek_head()``
与 ``z_impl_k_queue_peek_tail()``
的实现
在未持有队列自旋锁的情况下
执行该读取与解引用，
而同一列表的
所有其他访问者——
包括解链节点
并 ``k_free()`` 其
后备 ``alloc_node`` 的
``k_queue_get()``——
都在该锁下操作。

由于 peek 未同步，
同一队列上
（在 SMP 构建上，
或在抢占/ISR 并发下）
并发的 ``k_queue_get()``
可在 peek 取得节点指针
与解引用它之间
释放该节点。
peek 随后
从已释放、
可能被重新分配的堆内存中
读取标志位与数据指针，
并向其调用者
返回一个过期或悬空指针。
``k_fifo`` 与 ``k_lifo``
是 ``k_queue`` 的
薄封装，
因此这影响
贯穿 ``net_buf``、
Bluetooth、USB
与网络子系统的
缓冲区队列；
peek 操作也是
可从 ``CONFIG_USERSPACE``
线程触达的系统调用。

后果是
一次可泄露过期堆内容
（一个指针字）的
释放后使用读取，
以及，当返回的悬空指针
随后作为存活缓冲区被消费时，
一次可使系统崩溃
或破坏内存的解引用。
利用需要
以本地访问
赢得一个小竞态窗口
（例如用户空间进程
在共享队列上
将 ``k_queue_peek_*``
与 ``k_queue_get`` 竞速，
或两个 CPU），
因此实际影响
有界且严重度低。

修复用
``k_spin_lock``/``k_spin_unlock``
在队列锁上
包裹两个 peek 实现，
使读取与解引用
相对于并发
解链并释放
是原子的，
并使 peek
与队列其余
锁纪律对齐。

- `Zephyr 项目缺陷跟踪器 GHSA-8xm3-4w69-29mm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8xm3-4w69-29mm>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110576 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110576>`_

- `PR 112439 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112439>`_

- `PR 112438 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112438>`_

- `PR 112437 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112437>`_

:cve:`2026-11743`
-----------------

SF32LB MPI QSPI NOR flash 驱动
缺少负偏移/溢出检查
允许越界读取与写入

SF32LB MPI QSPI NOR flash 驱动
（drivers/flash/flash_sf32lb_mpi_qspi_nor.c）
在其读取与写入路径上
以测试
``(offset + size) > data->size``
校验 flash 偏移与长度。
由于 ``offset``
是有符号 ``off_t``
而 ``size`` 是无符号，
负偏移
被转换为大无符号值，
且加法
可环绕为
通过检查的小结果。
读取路径随后执行
``memcpy(dst, (void *)(data->base + offset), size)``，
写入路径在 ``offset``
编程 flash
并对 ``data->base + offset``
缓存失效，
两种情况下
都访问
映射 flash 窗口之外的内存。
驱动的擦除路径
已拒绝负偏移，
但读取与写入未。

在启用 ``CONFIG_USERSPACE`` 的构建中，
``flash_read`` 与 ``flash_write``
是系统调用，
其校验器
验证设备对象与调用者缓冲区
但有意将偏移边界检查
委托给驱动。
因此被授予访问该 flash 设备的
非特权线程
可以携带构造的负偏移
与其自身内存域中
有效的缓冲区
调用系统调用，
触达未检查的访问。

最直接的影响
在读取路径上：
通过选择负偏移与匹配的大小，
攻击者
将 ``memcpy`` 源
滑到 flash 基址之下，
将其自身缓冲区中
拷贝任意 CPU 可寻址内存，
泄露其未被授权读取的内存。
写入路径
额外允许
在越界地址编程 flash
并使攻击者选择的
缓存范围失效，
影响完整性与可用性。
触达需要
启用用户空间
且原始 flash 设备对象
被授予给不受信任的线程。

修复以
``qspi_nor_range_is_valid()``
替换该检查，
后者拒绝负偏移
并在两条路径上
以溢出安全的 64 位算术
执行边界比较，
并额外添加
SRAM DMA bounce 缓冲区
加源/目标重叠拒绝，
以防一个
独立的 DMA 总线挂起条件。

- `Zephyr 项目缺陷跟踪器 GHSA-c6wh-gwg4-fj5j
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c6wh-gwg4-fj5j>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107793 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107793>`_

- `PR 112433 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112433>`_

- `PR 112434 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112434>`_

:cve:`2026-11809`
-----------------

UpdateHub probe：
未初始化堆的
网络提供元数据的越界读取

``subsys/mgmt/updatehub/updatehub.c`` 中的
UpdateHub OTA 客户端
在 ``z_impl_updatehub_probe()`` 中
包含一次越界/未初始化内存读取。
来自 UpdateHub 服务器的
probe 响应
被拷贝到一个
正确 NUL 终止的
堆缓冲区（``metadata``），
但第二个缓冲区（``metadata_copy``）
以 ``k_malloc``（未清零）分配
并通过
``memcpy(metadata_copy, metadata,
strlen(metadata))``
填充，
后者省略了终止 NUL。
拷贝内容之后的所有
都保持未初始化堆。

当对数组描述符的
第一个 ``json_obj_parse()``
失败时，
代码回退到
``json_obj_parse(metadata_copy,
strlen(metadata_copy), ...)``。
``strlen()`` 调用
越过拷贝字节
扫描未初始化堆，
如果在分配末尾之前
未找到零字节，
则越过缓冲区读取；
产生的过长长度
随后作为 JSON 解析。
probe 负载
完全由
（恶意、被入侵的，
或——无可选
``CONFIG_UPDATEHUB_DTLS`` 时——
在途的）UpdateHub 服务器控制，
后者可构造
一个使第一次解析失败
以驱动该路径的
大负载。

后果是
一次未初始化堆的读取，
最坏情况是
越过 ``metadata_copy`` 分配的
越界读取，
可故障并使
更新线程/设备崩溃，
产生网络可触发的
拒绝服务。
越读数据
仅在内部被消费
以评估更新
且不返回给攻击者，
因此无直接信息泄露
且无越界写入。

修复在拷贝前
以 ``memset``
清零 ``metadata_copy``，
保证 NUL 终止
并使 ``strlen()``
限定在分配内。

- `Zephyr 项目缺陷跟踪器 GHSA-6r86-hvv2-h6g4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6r86-hvv2-h6g4>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 104704 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11810`
-----------------

UpdateHub OTA agent 在
空内部元数据数组时
的空指针解引用（远程 DoS）

UpdateHub 固件更新 agent 的
probe 处理程序
（``subsys/mgmt/updatehub/updatehub.c``
的 ``z_impl_updatehub_probe()``）
将更新服务器返回的
JSON 元数据
解析到一个
固定两级嵌套数组结构。
解析后
仅验证外部数组长度
（``objects_len != 2``），
随后
通过 ``strlen()``
解引用
``objects[1].objects[0].objects.sha256sum``，
未检查
元素 ``[1]`` 的
内部对象数组
非空。

元数据是
受攻击者影响的
网络输入：
agent 在常规 OTA probe 期间
经 CoAP
从配置的 UpdateHub 服务器
获取它。
恶意或被入侵的更新服务器
（或在 DTLS 禁用时
网络中间人）
可返回一个
其第二个外部对象数组
为空的响应。
由于解析目标
是零初始化的，
对应的
``objects[1].objects[0].objects.sha256sum``
指针为 NULL，
随后的 ``strlen()``
解引用地址零。
同一缺陷
存在于
'any boards'
与 'some boards'
元数据布局中。

产生的 CPU 故障
在 Zephyr 默认错误处理下
是致命的，
使设备停止或复位，
因此该缺陷是
可远程触发的拒绝服务。
影响限于可用性；
它是一次
来自 NULL 的读取
且无越界写入、
内存破坏
或信息泄露。
修复在
任何解引用之前
拒绝
其内部对象数组
为空的元数据，
在两种布局上。

- `Zephyr 项目缺陷跟踪器 GHSA-jfpc-324j-84ww
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jfpc-324j-84ww>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 104704 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11811`
-----------------

UpdateHub OTA 客户端
start_coap_client() 中的
套接字文件描述符泄露
导致资源耗尽 DoS

``subsys/mgmt/updatehub/updatehub.c`` 中
UpdateHub 空中更新客户端的
``start_coap_client()``
在其连接建立
失败路径上
泄露 CoAP/DTLS 套接字描述符。
共享的 ``error:``
清理
以 ``ret > 0`` 标志
门控套接字关闭，
但 ``ret``
在套接字创建后
立即被设为 ``-1``，
因此当
``zsock_setsockopt()``（DTLS）
或 ``zsock_connect()``
随后失败时
门控为假
且
``cleanup_connection()``
从不被调用。
全局 ``ctx.sock`` 中的
打开描述符
随后被
下一次尝试覆盖，
从套接字/net_context 池
永久泄露
直至重启。

失败建立路径
在每次 OTA 客户端
尝试联系
UpdateHub 服务器
且连接无法建立时
触达——
由周期性
``autohandler()`` 轮询
自动驱动
（以及按需
通过
``updatehub_probe()``/
``updatehub_update()`` API
或 ``updatehub run``
shell 命令）。
DTLS 握手/连接结果
可被
丢弃、重置
或以其他方式
干扰到服务器流量的
网络或在途攻击者
影响，
且当服务器不可达时
也自然失败。

每次失败尝试
永久泄露一个描述符；
一旦共享套接字池
耗尽，
网络在设备范围
退化直至
设备重启，
一次拒绝服务条件。
严重度低
因为泄露速率
受配置的 OTA 轮询间隔
（默认每 24 小时一次）
限制，
效果渐进
且通过重启恢复，
且仅启用
UpdateHub 客户端的构建
受影响。
无内存破坏、
信息泄露
或认证影响。

- `Zephyr 项目缺陷跟踪器 GHSA-q3mh-4wj7-mq7f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-q3mh-4wj7-mq7f>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 104704 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11812`
-----------------

UpdateHub：
共享上下文上的竞态条件
导致越界写入与 DoS

UpdateHub 管理子系统
（subsys/mgmt/updatehub/updatehub.c）
通过
单一文件范围的 ``ctx`` 结构
驱动
每个更新操作，
后者持有
CoAP 块上下文、
负载缓冲区、
状态码、
套接字
与
单元素 poll-fd 数组
``fds[1]``。
对 ``ctx`` 的访问
未被序列化，
且 ``prepare_fds()``
写入 ``ctx.fds[ctx.nfds]``
并自增 ``ctx.nfds``
无边界检查。

两条独立路径
并发修改 ``ctx``：
运行在
系统工作队列上的
后台 autohandler
与
经 ``updatehub run``
shell 命令、
直接 API 调用
或——由于操作
被暴露为系统调用——
用户空间线程
触达的
用户触发操作。
当 ``ctx.nfds``
已为 1 时
第二个流
进入 ``prepare_fds()``，
写入落在
数组之外一个元素；
按结构布局
它重叠
相邻的
``ctx.sock``/``ctx.nfds``
成员。
更广泛地，
未同步的共享
使两个流
交错
连接建立与拆除，
双重关闭
一个套接字描述符
或在共享缓冲区上
乱写。

结果是
更新子系统
内部状态的损坏
与
固件更新路径的
拒绝服务；
越界写入
被限定在
``ctx`` 结构内
且无已证明路径
到其外部内存
或代码执行。
触发需要
能调用
更新操作的
本地行为者
（或在
CONFIG_USERSPACE 下
非特权用户空间线程）
并
赢得
与后台处理程序
的时序竞态；
远程对端
无法控制
竞态时序。
修复
以互斥锁
序列化
入口点
并为
``prepare_fds()``
添加边界检查。

- `Zephyr 项目缺陷跟踪器 GHSA-vprh-rff6-46xp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vprh-rff6-46xp>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 104704 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11893`
-----------------

Bouffalo Lab HCI 驱动
send() 错误路径中的
双重释放/释放后使用（hci_bflb）

Bouffalo Lab 片内 BLE 控制器
（BL60x/BL70x/BL61x）的
Bluetooth HCI 驱动
``drivers/bluetooth/hci/hci_bflb.c``
的 ``bt_bflb_send()``
违反
``bt_hci_driver_api.send()``
缓冲区所有权契约。
该契约
（记录于
``include/zephyr/drivers/bluetooth.h``）
要求
仅在成功时
消费缓冲区引用；
出错时
调用者
仍拥有引用
并 unref 它。
驱动反而
将所有错误路径
路由到一个
无条件调用
``net_buf_unref(buf)``
的共享标签
然后返回错误码，
在失败时
也消费缓冲区。

当 ``send()``
返回错误时，
主机 TX 路径
（``subsys/bluetooth/host/conn.c``
的 ``send_buf()``）
再次 unref
同一缓冲区，
认为它
仍拥有它。
该双重 unref
过度递减
net_buf 引用计数。
由于缓冲区
是一个 TX 分片
其销毁回调
也递减
其仍在队列中的
父缓冲区，
父缓冲区
在连接 TX 队列上
仍可达时
被过早释放，
产生
释放后使用
与
共享 net_buf 池的
损坏
而非良性泄露。

错误条件
在
主机到控制器
传输路径上
（控制器发送失败，
或不支持的 H:4 报文类型），
因此
不由
攻击者提供的
无线电字节
直接驱动；
远程/相邻对端
仅能
间接影响
它们，
例如
通过
在
重负载链路下
诱发
控制器 TX 失败。
触达时
后果是
BLE 协议栈
拒绝服务
（崩溃/池损坏）
带有
可能的
进一步内存破坏，
限定于
使用
这些
Bouffalo Lab
片内控制器之一
的设备。

- `Zephyr 项目缺陷跟踪器 GHSA-ph42-6rqx-728c
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-ph42-6rqx-728c>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110711 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110711>`_

- `PR 112558 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112558>`_

:cve:`2026-11894`
-----------------

Realtek BEE Bluetooth HCI 驱动
``send()`` 错误路径中的
双重释放/释放后使用

Realtek BEE Bluetooth HCI 驱动的
发送回调
``drivers/bluetooth/hci/hci_bee.c``
的 ``bt_hci_bee_send()``
违反 ``bt_hci_driver_api``
缓冲区所有权契约。
该契约要求
驱动仅在成功时
消费（unref）
发送 ``net_buf``；
错误返回时
主机调用者
保留所有权
并自行 unref 缓冲区。
修复前代码
将所有错误路径
路由到一个
无条件调用
``net_buf_unref(buf)``
的共享清理标签
然后返回错误码。

由于主机 TX 路径
（在 ``subsys/bluetooth/host/hci_core.c`` 中）
在 ``send()`` 返回错误后
再次 unref 缓冲区，
缓冲区被释放两次：
驱动将其
返回其 ``net_buf`` 池
且主机随后
unref 已释放的缓冲区，
破坏共享池/
下溢引用计数
（CWE-415）。
同一错误分支
额外
在缓冲区
已被 unref 之后
在 ``LOG_ERR`` 调用内
解引用 ``buf->len``，
一次
已释放内存的读取
（CWE-416），
在
默认错误日志级别
被编译进来。

失败边
在
控制器的
主机到控制器
缓冲区分配失败
或
控制器发送失败
（资源耗尽/IO 条件）
时触达。
远程 Bluetooth 对端
可通过
驱动
重主机
发送活动
间接
将设备
推向
这些条件，
此时
双重释放
破坏
主机 ``net_buf`` 池
且最可能
使设备崩溃，
带有
残余的
进一步
内存破坏
潜力。
影响
限定于
使用
该特定
Realtek BEE HCI 驱动
的构建。

修复
从
每个
错误路径
提前返回
不 unref
且
仅在
成功路径
unref 缓冲区，
恢复
所有权契约
并
消除
双重释放
与
释放后使用
读取
两者。

- `Zephyr 项目缺陷跟踪器 GHSA-v9mj-h2m6-v9c6
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-v9mj-h2m6-v9c6>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110711 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110711>`_

- `PR 112558 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112558>`_

:cve:`2026-11985`
-----------------

ARM 上启用 FPU 但无寄存器共享时的
跨线程 FPU 寄存器泄露

在 Zephyr ARM 移植中，
启用硬件 FPU
（``CONFIG_FPU``）
强制
"Floating point ABI"
选择，
其默认为
``CONFIG_FP_HARDABI``。
``FP_HARDABI``
与 ``FP_SOFTABI``
均允许
编译器
在
任何函数中
发出
硬件 FP 指令，
甚至
从不使用
浮点类型的
代码。
然而，
被调用者保存的
FP 寄存器
（s16-s31 / d8-d15）
仅在
启用
``CONFIG_FPU_SHARING`` 时
（``arch/arm/core/cortex_m/swap_helper.S``
与
``arch/arm/core/cortex_a_r/swap_helper.S``）
在
上下文切换
之间
保存
并恢复，
且
在本修复之前
选择
一个 ABI
不
启用
FPU 寄存器
共享，
其
默认
关闭。

在
启用
FPU 且
默认
ABI 但
保持
``CONFIG_FPU_SHARING``
禁用
的
构建中，
内核
在线程
切换
之间
不
保留
任何
被调用者保存的
FP 寄存器
状态。
该
"非共享"
模式
的
文档化
前提——
仅
单个线程
执行
FP 指令——
被
静默
违反，
因为
编译器
可能
在
每个线程中
生成
FP 指令。

在
``CONFIG_USERSPACE``
下，
线程
相互
隔离，
这
成为
一次
信息泄露
边界
跨越：
受害线程
可
将
秘密派生值
留在
s16-s31 中，
且
共驻的
非特权
线程
可
直接
读取
那些寄存器
（FP 寄存器
访问
不
受
特权
门控），
恢复
由
另一个
线程
留下
的
数据。
无
用户空间
时
同一
缺陷
导致
跨线程
FP 状态
损坏
（正确性
故障）。
泄露
被
限定于
16 个
被调用者保存的
单精度
寄存器
且
是
机会性的，
因此
影响
低。

修复
使
``FP_HARDABI``
与 ``FP_SOFTABI``
选择
``CONFIG_FPU_SHARING``
并
在
创建
时
为
每个线程
标记
``K_FP_REGS``，
使
被调用者保存的
FP 状态
在
编译器
可能
发出
FP 指令
时
始终
在
上下文切换
之间
保留。

- `Zephyr 项目缺陷跟踪器 GHSA-qxr9-wh3c-hvgv
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qxr9-wh3c-hvgv>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110300 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110300>`_

- `PR 112547 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112547>`_

- `PR 112551 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112551>`_

- `PR 112550 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112550>`_

:cve:`2026-12051`
-----------------

USB DFU device_next 下载处理程序
（handle_download）中的
空指针解引用

Zephyr 新（实验性）
``device_next`` USB
设备栈中
USB DFU 类实现
在
``handle_download()``
（subsys/usb/device_next/class/usbd_dfu.c）
中
包含
一次
空指针
解引用。
处理程序
计算
``MIN(setup->wLength, buf->len)``
并
将
``buf->data``
传给
镜像
写
回调
而不
检查
``buf``
net_buf
指针
非
NULL。

处理程序
经
USB
控制
端点
触达
由
USB
主机
驱动。
对
无
Data OUT
阶段的
``DFU_DNLOAD``
（下载）
请求——
特别是
DFU 协议
用于
结束
固件
传输
的
零长度
终止
下载——
USB
核心
以
NULL
缓冲区
调用
类
处理程序。
在
设备
已
被
推进到
``DFU_DNLOAD_IDLE``
状态
（通过
发送
一个
有效
下载
块
与
``GET_STATUS``）
之后，
零长度
``DFU_DNLOAD``
以
``buf == NULL``
到达
``handle_download()``
并
解引用
它。

结果是
一次
NULL+偏移
读取
触发
致命
CPU
故障，
即
一次
拒绝服务
（设备
崩溃/复位）。
攻击者
是
控制
设备
所连接
的
USB 主机
的
任何
实体；
DFU
下载
支持
必须
以
已注册
镜像
启用。
无
内存
破坏
或
信息
泄露——
影响
限于
可用性。
修复
添加
显式
``if (buf != NULL)``
保护
使
回调
接收
零长度、
NULL-data
传输
而非
崩溃。

- `Zephyr 项目缺陷跟踪器 GHSA-vhvq-q6rw-jvm4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vhvq-q6rw-jvm4>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110830 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110830>`_

- `PR 112560 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112560>`_

:cve:`2026-12052`
-----------------

USB CDC NCM 控制处理程序中
主机 wLength
小于
响应
时的
越界写入

USB 设备侧
CDC NCM 类
控制到主机
处理程序
``subsys/usb/device_next/class/usbd_cdc_ncm.c``
的 ``usbd_cdc_ncm_cth``
为
``GET_NTB_PARAMETERS``
（28 字节
``struct ntb_parameters``）
与
``GET_NTB_INPUT_SIZE``
（8 字节
``struct ntb_input_size``）
类
请求
构建
固定大小
响应
并
通过
``net_buf_add_mem(buf, ..., sizeof(...))``
将
整个
结构
拷贝
到
控制
DATA IN
缓冲区
忽略
主机
提供的
``wLength``。

控制
DATA IN
缓冲区
由
USB
栈
以
恰好
``wLength``
字节
容量
分配
（``usbd_ep_ctrl_data_in_alloc`` ->
``udc_ctrl_data_alloc`` ->
``net_buf_alloc_len(&udc_ep_pool, wLength)``；
IN
端点
不
应用
向上
取整）。
由于
``net_buf_add_mem``/
``net_buf_simple_add``
仅
以
``__ASSERT_NO_MSG``
限定
拷贝
其
在
生产
构建中
被
编译掉，
发出
一个
这些
标准
CDC NCM
控制
请求
且
``wLength``
小于
响应
结构
（例如
``wLength = 1``）
的
主机
使
处理程序
``memcpy``
最多
27 字节
越过
已分配
池
缓冲区
末尾。

请求
字段
直接
来自
USB SETUP
报文
因此
Zephyr 设备
枚举
所对的
任何
主机
（或
USB
拦截器）
可
在
无
认证
情况下
触发
溢出
一旦
以
device_next
USB
栈
与
CDC NCM
类
构建
的
镜像
被
连接。
越界
写入
破坏
共享
``udc_ep_pool`` 中
相邻
分配
与
元数据
主要
导致
内存
破坏
与
USB
栈
的
拒绝服务；
溢出
长度
有界
（<= 27 字节）
且
写入
内容
为
固定
设备
常量
且
bug
不
读回
任何
因此
无
信息
泄露。
修复
以
``MIN(sizeof(...), setup->wLength)``
钳制
拷贝
匹配
现有
CDC ACM
处理程序。

- `Zephyr 项目缺陷跟踪器 GHSA-vr4p-6rg5-qgpx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vr4p-6rg5-qgpx>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110831 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110831>`_

- `PR 112615 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112615>`_

- `PR 112614 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112614>`_

:cve:`2026-12232`
-----------------

Intel ALH DAI get_properties 中
未验证
stream_id
的
越界读取

Intel ALH
数字
音频
接口
驱动
函数
``drivers/dai/intel/alh/alh.c``
的
``dai_alh_get_properties()``
使用
调用者
提供的
``int stream_id``
无
范围
验证。
该值
索引
固定大小
``static const uint8_t
alh_handshake_map[64]``
数组
并
缩放
一个
FIFO
寄存器
地址
因此
越界
``stream_id``
产生
一次
在
攻击者
选择的
有符号
偏移处
的
单字节
越界
读取
从
数组
偏移。
该字节
被
写入
``prop->dma_hs_id``
且
产生的
``struct dai_properties``
被
拷贝
回
调用者
泄露
它。

``dai_get_properties_copy()``
是
一个
Zephyr
``__syscall``
其
校验器
``z_vrfy_dai_get_properties_copy()``
（``drivers/dai/dai_handlers.c``）
仅
验证
设备
对象
权限
与
目标
缓冲区
不
验证
``stream_id``。
因此
被授予
访问
ALH DAI
设备
对象
的
用户
模式
线程
可
以
任意
``stream_id``
调用
系统调用
跨越
用户空间/内核
沙箱
边界。

影响
是
每次
调用
一字节
的
任意
偏移
内核
信息
泄露
（以及
通过
``fifo_address``
泄露
一个
计算
的
内核
地址）；
解析到
未
映射
页
的
``stream_id``
在
内核
上下文
故障
提供
一次
本地
拒绝服务。
利用
需要
``CONFIG_USERSPACE``
与
设备
访问
使
这
成为
一次
本地、
中等
严重度
问题。
修复
在
前端
拒绝
负
与
过大
``stream_id``
值
并
返回
NULL
拷贝
封装器
将其
映射到
``-ENOENT``。

- `Zephyr 项目缺陷跟踪器 GHSA-3557-j848-pv24
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3557-j848-pv24>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110946 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110946>`_

- `PR 112747 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112747>`_

- `PR 112745 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112745>`_

:cve:`2026-12233`
-----------------

TLS 可信
凭证
后端
中
未初始化
互斥锁
在
争用
下
导致
内核
NULL 解引用
DoS

PSA
Protected
Storage
凭证
后端
（subsys/net/lib/tls_credentials/tls_credentials_trusted.c）
将其
凭证
存储
互斥锁
声明为
普通
零填充
``static struct k_mutex credential_lock;``
且
从不
对其
调用
``k_mutex_init()``。
静态
零填充
``k_mutex``
具有
未初始化
等待
队列
（其
dlist
头/尾
为
NULL
而非
``k_mutex_init``/
``K_MUTEX_DEFINE``
安装
的
自引用
哨兵）。
无
争用
锁
路径
不
触碰
等待
队列
因此
缺陷
潜伏
且
序列化
使用
行为
正确。

当
两个
执行
上下文
在
锁
上
争用
``k_mutex_lock()``
通过
``z_pend_curr()``
将
阻塞
线程
挂起
到
等待
队列
其
对
零
列表
调用
``sys_dlist_append()``
并
解引用
NULL
尾
指针
（``tail->next = node``）
使
内核
故障。
锁
在
TLS
握手
凭证
加载
期间
被
持有
且
由
所有
凭证
添加/获取/删除
操作
持有
因此
执行
并发
TLS
握手
的
部署
（例如
处理
来自
远程
对端
的
多个
并发
连接
的
服务器）
或
与
握手
并发
的
凭证
管理
操作
可
触发
该
解引用。

影响
是
一次
拒绝服务：
首次
争用
时
确定性的
内核
panic/设备
复位。
无
超出
NULL
解引用
的
内存
破坏
且
无
机密性
或
完整性
影响；
快速
路径
上
的
互斥
仍
正确。
暴露
限于
启用
``CONFIG_TLS_CREDENTIALS_BACKEND_PROTECTED_STORAGE``
的
构建
（PSA
Protected
Storage/TF-M
平台）；
默认
易失
RAM
后端
正确
初始化
其
锁
且
不受
影响。

修复
以
``K_MUTEX_DEFINE(credential_lock)``
静态
初始化
互斥锁
提供
一个
有效
等待
队列
使
争用
路径
不再
触碰
NULL
列表。

- `Zephyr 项目缺陷跟踪器 GHSA-57c4-xcq2-fqj7
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-57c4-xcq2-fqj7>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110943 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110943>`_

- `PR 112741 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112741>`_

- `PR 112740 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112740>`_

- `PR 112739 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112739>`_

:cve:`2026-12234`
-----------------

``zsock_sendmsg``/``recvmsg`` 用户空间
校验器
中的
TOCTOU
双重
获取
允许
内核
堆
越界
写入

用户空间
系统调用
校验器
``subsys/net/lib/sockets/sockets.c``
的
``z_vrfy_zsock_sendmsg()``
与
``z_vrfy_zsock_recvmsg()``
通过
``k_usermode_from_copy()``
将
调用者
提供的
``struct net_msghdr``
快照
到
内核侧
副本
但
随后
为
后续
决策
重新
读取
仍
存活
的
用户
结构。
内核
``iovec``
影子
缓冲区
从
一次
``msg->msg_iovlen``
读取
定长
而
填充
循环
由
对
同一
字段
的
第二次
存活
读取
限定。

由于
``msg``
指向
普通
用户
内存
同一
内存
域
中
协作
的
第二个
线程
可
在
定长
读取
与
循环
测试
之间
的
窗口
放大
``msg->msg_iovlen``
（经典
双重
获取/TOCTOU）。
填充
循环
随后
迭代
越过
实际
分配
的
``net_iovec``
槽位
数量
将
受
攻击者
影响
的
``iov_base``/``iov_len``
值
写入
内核
堆
影子
缓冲区
末尾
之外。
``recvmsg``
校验器
在
其
入站
与
结果
写回
两个
循环
上
具有
同一
缺陷。

代码
在
启用
``CONFIG_USERSPACE``
且
``zsock_sendmsg``/
``zsock_recvmsg``
系统调用
可用
时
可
从
非
特权
用户
线程
触达。
成功
竞态
跨越
用户到内核
特权
边界
破坏
内核
管理
的
堆
内存
产生
一次
本地
权限
提升
原语
或
至少
一次
内核
故障
拒绝
服务。
修复
拷贝
头
一次
并
从
快照
派生
所有
大小、
边界
与
门控
原子
拷贝
每个
``iovec``
条目
使
其
基址
与
长度
不再
被
竞态
分离。

- `Zephyr 项目缺陷跟踪器 GHSA-fcp3-vrr2-xfjv
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fcp3-vrr2-xfjv>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108079 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108079>`_

- `PR 112619 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112619>`_

- `PR 112624 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112624>`_

- `PR 112625 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112625>`_

:cve:`2026-12235`
-----------------

Xtensa llext PLT 重定位
中
来自
畸形
ELF
的
越界
写入
（CWE-787）

可
链接
可
加载
扩展
（llext）
子系统
在
链接
可
重定位
（部分
链接）
ELF
扩展
时
不当
处理
PLT/RELA
重定位
条目。
在
``llext_link_plt()``
（subsys/llext/llext_link.c）中
可
重定位
分支
（``tgt != NULL``
用于
Xtensa
可
重定位
对象
的
路径）
计算
补丁
地址
为
``ext->mem[LLEXT_MEM_TEXT] - text.sh_offset + rela.r_offset + tgt->sh_offset``
并
随后
在
该处
执行
重定位
写入
不
验证
``rela.r_offset``。
其
姊妹
共享/动态
分支
已
通过
``llext_file_offset()``
拒绝
越界
偏移。

``rela.r_offset``
直接
从
ELF 的
RELA
表
读取
因此
携带
大于
目标
节
的
偏移
的
构造
条目
使
写入
落在
扩展
文本
缓冲区
之外
任意
远。
结果
是
一次
受
攻击者
影响
的
越界
写入
（位置
经
``r_offset``
写入
值
为
解析
的
符号
地址）
在
链接
时
监督者
上下文
执行
在
任何
扩展
代码
运行
之前。

路径
从
``llext_load()``
触达
每当
应用
在
带
可
写
存储
的
Xtensa 上
加载
受
攻击者
影响
的
ELF
扩展；
llext
文档
记录
其
接受
不受
信任
来源
的
扩展。
影响
是
监督者
上下文
内存
破坏
（完整性
与
可用性
损失
以及
用户
模式
扩展
的
沙箱
边界
逃逸）。
利用
受
Xtensa
可
重定位
PLT
路径
与
可
写
存储
门控
且
将
越界
写入
变为
有用
原语
不
平凡。

修复
添加
一个
边界
检查
拒绝
任何
``r_offset >= tgt->sh_size``
的
RELA
条目
镜像
现有
共享
分支
中
的
验证。

- `Zephyr 项目缺陷跟踪器 GHSA-xv9q-6mrf-8j49
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xv9q-6mrf-8j49>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109875 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109875>`_

- `PR 112635 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112635>`_

- `PR 112634 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112634>`_

- `PR 111541 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111541>`_

:cve:`2026-12236`
-----------------

Bluetooth GATT 客户端
解析
零
数据
长度
的
Read-By-Type
响应
时的
无限
循环
（DoS）

Bluetooth
主机
GATT
客户端
函数
``subsys/bluetooth/host/gatt.c``
的
``parse_read_std_char_desc()``
解析
在
``BT_GATT_DISCOVER_STD_CHAR_DESC``
发现
期间
从
远程
GATT
服务器
接收
的
ATT
Read
By
Type
Response。
每
条目
步长
``rsp->len``
直接
取自
对端
的
PDU
且
解析
循环
既
测试
其
退出
条件
（``length >= rsp->len``）
又
推进
（``length -= rsp->len``、
``pdu += rsp->len``）
使用
该值。
``rsp->len``
的
最小值
在
循环
之前
从未
被
验证。

恶意
或
故障
的
对端
可
以
``rsp->len = 0``
回复。
由于
``length``
无
符号
且
从不
递减
循环
条件
永远
保持
真
且
读取
指针
从不
推进；
只要
体
至少
几
字节
带
非零
句柄
与
匹配
的
描述符
UUID
主机
反复
重新
解析
同一
字节
并
调用
发现
回调
从不
终止。
这
挂起
Bluetooth
主机
处理
线程
（CWE-835
退出
条件
不可
达
的
循环）。

条件
在
本地
设备
发起
标准
描述符
值
发现
后
可
被
任何
已连接
对端
触达；
GATT
发现
不
需要
绑定
或
加密
因此
设备
连接
的
未
认证
相邻
攻击者
可
触发
它。
影响
是
Bluetooth
子系统
的
拒绝
服务
（以及
在
受限
目标上
可能
的
看门狗
复位）；
无
内存
泄露
或
破坏。

修复
在
循环
前
添加
``rsp->len < sizeof(struct bt_att_data)``
检查
拒绝
短
长度
响应
使
步长
始终
非零
且
循环
终止。
姊妹
解析器
``parse_include()``
与
``parse_characteristic()``
已
验证
``rsp->len``
且
不受
影响。

- `Zephyr 项目缺陷跟踪器 GHSA-483r-jq2x-5cp9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-483r-jq2x-5cp9>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109066 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109066>`_

- `PR 112840 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112840>`_

- `PR 112839 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112839>`_

- `PR 112841 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112841>`_

:cve:`2026-7007`
----------------

Zephyr ext2
超级块
解析
中
的
除零
允许
通过
构造
文件系统
镜像
的
DoS

Zephyr
ext2
文件系统
在
完成
挂载
前
在
``ext2_verify_disk_superblock()``
（``subsys/fs/ext2/ext2_impl.c``）中
验证
磁盘
上
的
超级块。
验证器
检查
魔数、
块
大小、
修订
与
特性
标志
但
未
验证
磁盘
上
字段
``s_blocks_per_group``
与
``s_inodes_per_group``
非零。
两个
字段
都
直接
从
镜像
读取
且
稍后
在
挂载
时
初始化
中
作为
除数
使用。

挂载
期间
``get_ngroups()``
将
``s_blocks_count``
除以
``s_blocks_per_group``
（经
``ext2_init_fs()``
的
``ext2_fetch_block_group()``
触达）
且
``get_itable_entry()``
在
获取
根
inode 时
将
``(ino - 1)``
除以
``s_inodes_per_group``
（两者
均在
``subsys/fs/ext2/ext2_diskops.c`` 中）。
任一
字段
设为
零
的
超级块
因此
在
挂载
序列
期间
导致
整数
除零。

能
向
挂载
ext2 的
设备
呈现
构造
ext2 镜像
的
攻击者
可
触发
此——
可
移除
介质
如
SD 卡
或
USB
大容量
存储
设备。
在
ARMv7-M/
ARMv8-M-mainline
Cortex-M
目标上
除零
捕获
被
启用
（``SCB_CCR_DIV_0_TRP``）
因此
除法
引发
一个
Zephyr
视为
致命
错误
的
UsageFault
产生
一次
拒绝
服务。
影响
限于
可用性；
畸形
值
仅
作为
除数
被
消费。

修复
在
超级块
验证器
中
拒绝
零
``s_blocks_per_group``
或
``s_inodes_per_group``
返回
``-EINVAL``
使
挂载
在
任何
块
组
或
inode
I/O
发生
前
失败。

- `Zephyr 项目缺陷跟踪器 GHSA-wrf2-79mm-cvw5
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wrf2-79mm-cvw5>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107929 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107929>`_

- `PR 113331 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113331>`_

- `PR 110884 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110884>`_

- `PR 110883 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110883>`_

:cve:`2026-8023`
----------------

Zephyr HTTP 服务器
静态
文件系统
资源
处理程序
中
的
路径
遍历
允许
未
认证
远程
任意
文件
读取

Zephyr 的
HTTP
服务器
（``subsys/net/lib/http``）
提供
一种
静态
文件系统
资源
类型
（``HTTP_RESOURCE_TYPE_STATIC_FS``
在
``CONFIG_FILE_SYSTEM``
启用
时
可用）
从
配置
的
根
目录
提供
文件。
在
本
修复
之前
HTTP/1
与
HTTP/2
两个
前端
都
将
原始
攻击者
控制
的
请求
路径
放入
``client->url_buffer``
（HTTP/1
在
``on_url()``
中
组装
HTTP/2
从
``:path``
伪
头
逐字
拷贝）
不
解析
``.``/``..``
段。
静态
FS
处理程序
随后
通过
直接
拼接
配置
根
与
该
原始
URL
构建
磁盘
上
文件
名
（``snprintk(fname, ..., "%s%s",
static_fs_detail->fs_path, client->url_buffer)``
在
``http_server_http1.c:603``
与
``http_server_http2.c:490``）
并
以
``fs_open(fname, FS_O_READ)``
打开
它。
由于
处理程序
经
通配符/前导
目录
（``fnmatch``
``FNM_LEADING_DIR``）
或
回退
资源
匹配
触达
``GET /<prefix>/../../<file>``
这样的
请求
被
分发
到
处理程序
且
在
底层
文件系统
（例如
LittleFS/FAT）
解析
``..``
段
后
逃逸
配置
的
web
根
使
未
认证
远程
客户端
读取
挂载
卷上
任意
可
读
文件
（信息
泄露）。
HTTP
服务器
触达
该
路径
不
需要
TLS
或
认证。
修复
添加
``http_server_remove_dot_segments()``
在
两个
协议
处理程序
中
资源
查找
前
规范化
URL 的
路径
部分
中和
该
遍历。
影响
发布
v4.0.0 至
v4.4.0
针对
注册
静态
文件系统
资源
的
部署。

- `Zephyr 项目缺陷跟踪器 GHSA-hch3-53g6-jj3h
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hch3-53g6-jj3h>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108531 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108531>`_

- `PR 111347 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111347>`_

- `PR 111346 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111346>`_

:cve:`2026-9728`
----------------

mbox_send 系统调用
校验器
中
的
TOCTOU
竞态
允许
用户空间
泄露
内核
内存

用户空间
系统调用
校验器
``drivers/mbox/mbox_handlers.c``
的
``z_vrfy_mbox_send()``
通过
直接
从
存活
用户空间
内存
读取
嵌套
``msg->data``/``msg->size``
字段
验证
它们
然后
将
原始
仍
可变
的
用户空间
``struct mbox_msg *``
指针
转发
到
``z_impl_mbox_send()``
与
底层
驱动。
在
访问
检查
与
驱动
使用
``msg->data``
之间
被
验证
的
指针
可
被
替换
留下
一个
检查
时/使用
时
窗口。

在
构建
``CONFIG_USERSPACE``
的
系统上
任何
非
特权
用户空间
线程
可
调用
``mbox_send()``
系统调用。
共享
调用者
地址
空间
的
第二个
线程
可
竞速
在
校验器
边界
检查
通过
但
驱动
解引用
之前
用
监督者
（内核）
地址
覆盖
``msg->data``。
驱动
随后
在
监督者
上下文
从
攻击者
选择
的
地址
读取
（例如
NXP
mailbox
驱动
的
``memcpy(&data32, msg->data, msg->size)``
其
字节
随后
被
发出
到
对端
mailbox
端点）。

影响
是
用户空间到监督者
访问
控制
绕过：
内核
内存
内容
泄露
（高
机密性
影响）
或
对
无效/未
映射
目标
地址
的
故障
内核
读取
导致
拒绝
服务。
修复
通过
``k_usermode_from_copy()``
将
整个
``struct mbox_msg``
快照
到
内核
栈
副本
并
验证
与
转发
该
不可
变
副本
关闭
该
竞态。

- `Zephyr 项目缺陷跟踪器 GHSA-47q2-w832-7w67
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-47q2-w832-7w67>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109946 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109946>`_

- `PR 110657 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110657>`_

- `PR 110656 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110656>`_

- `PR 113308 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113308>`_

:cve:`2026-9771`
----------------

flash_copy() 系统调用
中
缺少
设备
指针
验证
允许
用户空间
权限
提升

``flash_copy()``
系统调用
由
``drivers/flash/flash_util.c``
的
``z_vrfy_flash_copy()``
验证。
在
启用
``CONFIG_USERSPACE``
的
构建上
该
处理程序
是
用户
模式
调用者
的
内核侧
信任
边界。
在
修复
之前
其
仅
验证
输出
缓冲区
（``K_SYSCALL_MEMORY_WRITE``）
并
将
两个
``struct device *``
参数
``src_dev``
与
``dst_dev``
直接
传入
实现
不
做
任何
对象
验证——
不同于
每个
姊妹
flash
系统调用
其
以
``K_SYSCALL_DRIVER_FLASH``
保护
其
设备
指针。

用户
模式
线程
完全
控制
``src_dev``/``dst_dev``
的
值
与
其
自身
地址
空间
的
内容。
实现
``z_impl_flash_copy()``
解引用
这些
指针
并
通过
其
驱动
API
函数
表
调用
（例如
``api->get_parameters(dst_dev)``、
``flash_read(src_dev, ...)``、
``flash_write(dst_dev, ...)``）。
通过
提供
指向
伪造
``struct device``
的
指针
其
``api``
表
包含
攻击者
选择
的
函数
指针
非
特权
线程
可
使
内核
在
监督者
模式
调用
任意
代码；
传入
任何
任意
或
无效
地址
否则
产生
内核
崩溃
或
越界
读取。

结果
是
一次
本地
权限
提升
出
用户空间
沙箱
（内核
拒绝
服务
与
信息
泄露
为
较小
结果）。
修复
为
``z_vrfy_flash_copy()``
添加
``K_SYSCALL_DRIVER_FLASH(src_dev, read)``
与
``K_SYSCALL_DRIVER_FLASH(dst_dev, write)``
其
在
任何
解引用
前
验证
每个
设备
是
调用
线程
被
允许
使用
的
已
注册
flash
驱动
内核
对象
完全
关闭
该
路径。

- `Zephyr 项目缺陷跟踪器 GHSA-68cj-3hg4-5vpm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-68cj-3hg4-5vpm>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109962 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109962>`_

- `PR 110874 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110874>`_

- `PR 110873 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110873>`_

:cve:`2026-12363`
-----------------

LoRaWAN
分片
传输
中
来自
分片
索引
0
的
越界
写入

LoRaWAN
Fragmented
Data
Block
Transport
服务
（``subsys/lorawan/services/frag_transport.c``）
在
将
接收
``DATA_FRAGMENT``
命令
中
的
分片
计数器
转发
到
配置
的
解码器
前
不
验证
它。
在
``frag_transport_package_callback()``
中
值
``frag_counter = hdr->frag_index_n & 0x3FFF``
直接
取自
下行
负载
并
传给
解码器
后者
派生
``frag_counter - 1``
的
数组
索引
与
flash
偏移。
DataFragment
分片
是
1
索引
因此
``frag_counter``
为
``0``
使
该
算术
下溢。

在
默认
Semtech/LoRaMAC-node
解码器
这
触达
``FragDecoderProcess()``
的
``FragDecoder.FragNbMissingIndex[fragCounter - 1] = 0;``
其中
``fragCounter - 1``
求值为
``-1``
并
将
一个
``uint16_t``
零
越界
写入
刚好
在
数组
之前
进入
静态
解码器
对象
相邻
的
``MatrixM2B``
恢复
矩阵
状态
（``CWE-787``）。
一个
伴随
写入
派生
一个
野
flash
偏移
但
该
路径
被
``flash_area_write()``
边界
检查
拒绝。
树内
低
内存
解码器
（``frag_dec()``）
不
被
破坏：
其
越界
位
数组
与
flash
访问
被
``sys_bitarray_*``
与
``flash_area_*``
边界
检查
捕获。

处理程序
是
分片
传输
端口
的
已
注册
下行
回调
在
存在
活跃
分片
会话
时
可
触达
因此
触发
字节
是
受
攻击者
影响
的
LoRaWAN/FUOTA
网络
输入。
触发
其
需要
已
认证
下行
（LoRaWAN
MAC
会话
密钥
或
恶意/被
入侵
的
网络
或
FUOTA
服务器）
与
一个
活跃
分片
会话。
影响
被
包含：
解码器
状态
损坏
与
固件
更新
（FUOTA）
会话
拒绝
而非
可
控制
内存
破坏
或
代码
执行。
修复
添加
一个
传输
层
检查
拒绝
``frag_counter == 0``
为
两个
解码器
后端
关闭
该
缺陷。

- `Zephyr 项目缺陷跟踪器 GHSA-fvm7-7whg-8gj6
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fvm7-7whg-8gj6>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111287 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111287>`_

- `PR 112928 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112928>`_

:cve:`2026-12364`
-----------------

日志
系统调用
z_log_msg_static_create
中
缺少
用户空间
指针
验证
允许
内核
内存
泄露
与
拒绝
服务

用户空间
系统调用
校验器
``subsys/logging/log_msg.c``
的
``z_vrfy_z_log_msg_static_create()``
是
一个
纯
直通：
其
将
调用者
提供
的
``source``、``desc``、``package``
与
``data``
参数
直接
转发
到
内核
模式
实现
``z_impl_z_log_msg_static_create()``
不
执行
任何
强制
``K_SYSCALL_*``
检查。
由于
``z_log_msg_static_create()``
被
声明
``__syscall``
在
``CONFIG_USERSPACE``
下
任何
非
特权
用户
模式
线程
可
以
完全
受
攻击者
控制
的
参数
直接
调用
它。

内核
模式
处理程序
解引用
每个
这些
不受
信任
值：
``frontend_runtime_filtering()``
将
``source``
指针
作为
``struct log_source_dynamic_data``
读取
``cbprintf_package_copy()``
从
``package``
指针
读取
``desc.package_len``
字节
``z_log_msg_finalize()``
从
``data``
指针
执行
``desc.data_len``
字节
的
``memcpy()``。
无
验证
用户
线程
可
提供
任意
内核
地址
与
任意
长度
内核
将
从
它们
读取。

影响
是
内核
模式
拒绝
服务
（内核
在
解引用
攻击者
选择
的
指针
时
故障）
以及
在
日志
后端
输出
可
被
攻击者
观察
处
拷贝
到
发出
日志
消息
的
任意
内核
内存
泄露——
一次
跨越
用户/内核
边界
的
机密性
违规
用户空间
沙箱
本应
强制
它。
读取
不
破坏
内核
内存
因此
无
越界
写入
原语。

修复
为
校验器
添加
所需
验证：
其
以
``Z_LOG_MSG_MAX_PACKAGE``
限定
``desc.package_len``
拒绝
非
NULL/长度
不匹配
并
对
``package``、``data``
与
（当
启用
带
前端
的
运行时
过滤
时）
``source``
应用
``K_SYSCALL_MEMORY_READ()``
使
任何
越界
或
内核
指针
现在
引发
``K_OOPS``
而非
被
遵从。

- `Zephyr 项目缺陷跟踪器 GHSA-h7rf-g9mg-g23f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-h7rf-g9mg-g23f>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110506 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110506>`_

- `PR 112853 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112853>`_

- `PR 112854 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112854>`_

- `PR 116338 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/116338>`_

:cve:`2026-12365`
-----------------

Zephyr
可
延迟
工作
队列
取消
中
在
SMP
时序
竞态
下
的
释放
后
使用

Zephyr
第二代
工作
队列
（``kernel/work.c``）
在
可
延迟
工作
超时
的
处理
中
存在
一次
释放
后
使用。
当
可
延迟
工作
项
的
超时
已
被
出队
且
其
处理程序
``work_timeout()``
在
进行中
（阻塞
获取
工作
队列
自旋锁）
并发
取消
不
等待
该
处理程序
完成。
在
``unschedule_locked()``
中
修复
前
代码
调用
``z_abort_timeout()``
其
对
已
在
通告
的
记录
返回
``-EINVAL``
不
移除
它；
``cancel_async_locked()``
随后
观察到
工作
为
空闲
因此
即使
``k_work_cancel_delayable_sync()``
与
``k_work_flush_delayable()``
也
不
阻塞
在
进行中
处理程序
上
返回。

由于
那些
是
内核
头
文档
记录
的
在
释放
``k_work_delayable``
前
取消
的
安全
方式
一个
在
成功
同步
取消
后
立即
释放
对象
的
调用者
可
竞速
仍
挂起
的
处理程序。
``work_timeout()``
随后
解引用
已
释放
记录：
其
通过
``z_is_timeout_handler_canceled()``
读取
``to->dticks``
且
如果
已
释放
槽位
被
复用
使
退出
检查
失败
执行
``wp->flags``
（``K_WORK_DELAYED_BIT``）
的
读-改-写
并
对
过期
``dw->queue``
指针
提交
工作——
一次
释放
后
使用
读取
与
写入。

``k_work``
API
仅
内核
模式
（无
``__syscall``
入口点）
因此
这
是
一次
内核
内部
并发
缺陷
而非
用户空间
权限
提升。
触发
其
需要
一个
SMP
构建
与
一个
在
其
超时
通告
的
狭窄
窗口
中
调度
然后
释放
（或
重新
调度）
可
延迟
工作
项
的
子系统；
能
影响
此类
拆除
时序
的
攻击者
（例如
通过
驱动
子系统
定时器
的
连接
变化）
有
一个
合理
但
概率性
的
路径。
影响
是
内核
内存
破坏
或
崩溃
（拒绝
服务）。

修复
使
``unschedule_locked()``
通过
在
``z_try_abort_timeout()``
返回
``-EAGAIN``
时
自旋
同时
释放
并
重新
获取
工作
自旋锁
等待
直到
任何
进行中
处理程序
完成
然后
返回
并
将
``work_timeout()``
切换
到
原子
``K_WORK_DELAYED_BIT``
所有权。
这
关闭
两个
先
释放
后
处理程序
的
释放
后
使用
与
相关
重新
调度
提前
触发
竞态。

- `Zephyr 项目缺陷跟踪器 GHSA-rhmh-r93p-6g99
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rhmh-r93p-6g99>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109977 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109977>`_

- `PR 112961 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112961>`_

:cve:`2026-12366`
-----------------

Zephyr
用户空间
对象
处置
中
释放
一个
已
武装
的
动态
分配
k_timer
的
释放
后
使用

Zephyr 的
动态
内核
对象
处置
路径
``kernel/userspace/userspace.c``
的
``unref_check()``
在
其
引用
计数
达到
零
时
释放
对象
存储
（``k_free(dyn->data)``
在
运行
每
对象
类型
清理
后。
清理
``switch``
仅
处理
``K_OBJ_MSGQ``
与
``K_OBJ_STACK``；
无
``K_OBJ_TIMER``
情况。
一个
动态
分配、
已
初始化
且
已
武装
的
``k_timer``
保持
其
内嵌
``struct _timeout``
dnode
链接
在
全局
超时
队列
（``_timeout_q``）中
因此
在
不
取消
超时
的
情况
下
释放
timer
存储
在
该
队列
中
留下
一个
悬空
节点。

当
timer
下次
过期
超时
机制
遍历
``_timeout_q``
并
对
已
释放
节点
调用
``z_timer_expiration_handler()``
在
内核/ISR
上下文
解引用
并
写入
已
释放
（且
可
复用）
内核
堆。
这
是
一次
确定性
释放
后
使用
不
依赖
SMP：
排队
节点
简单
地
在
释放
时
从不
被
解链。

处置
可
从
``CONFIG_USERSPACE``
+
``CONFIG_DYNAMIC_OBJECTS``
下
的
非
特权
用户
线程
触达：
持有
此类
timer
最后
权限
的
线程
通过
``k_object_release()``
系统调用
（或
通过
退出
经
``k_thread_perms_all_clear()``）
丢弃
它
并
可
通过
``k_timer_start()``
系统调用
自行
武装
timer。
释放
与
过期
处理程序
在
内核
特权
运行
而
行为者
是
用户
线程
因此
bug
是
一次
沙箱
逃逸
内存
破坏
原语
可
用于
权限
提升。
修复
添加
``k_timer_cleanup()``
（取消
超时
并
等待
任何
进行中
处理程序）
并
在
释放
前
为
``K_OBJ_TIMER``
调用
它。

- `Zephyr 项目缺陷跟踪器 GHSA-x96g-542c-gccq
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x96g-542c-gccq>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 109977 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109977>`_

- `PR 112961 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112961>`_

:cve:`2026-12519`
-----------------

Zephyr WNC-M14A2A 调制解调器
socket-notify
解析
中
的
越界
栈
读取
与
写入

WNC-M14A2A
LTE-M
调制解调器
驱动
在
``on_cmd_socknotifyev()``
（``drivers/modem/vendor_standalone/wncm14a2a.c``）中
不当
处理
非
预期
``%NOTIFYEV:``
事件。
响应
行
通过
``net_buf_linearize()``
线性化
到
一个
固定
40 字节
栈
缓冲区
其
将
拷贝
限制
在
39 字节
并
返回
``out_len <= 39``。
然而
两个
引号
分隔符
扫描
循环
由
``len``
限定
——
``net_buf_findcrlf()``
返回
的
完整
CR/LF
分隔
帧
长度
——
而非
``out_len``。

当
一个
长于
39 字节
的
``%NOTIFYEV:``
行
在
线性化
区域
内
不含
``"``
时
循环
索引
``p1``/``p2``
越过
``value[39]``
读取
相邻
栈
内存
直到
找到
一个
杂散
引号
字节
或
索引
达到
``len``。
越读
字符串
随后
被
传给
``strncmp()``/``atoi()``/``LOG_*``
且
如果
一个
引号
字节
在
越界
处
找到
随后
的
``value[p2] = '\0'``
在
一个
受
攻击者
影响
的
偏移
执行
一个
单
NUL
越界
栈
写入。

``%NOTIFYEV:``
负载
携带
网络
派生
内容
（``LTIME``
网络
时间、
``SIB1``
基站
系统
信息、
``CSPS``/``RRCSTATE``）
因此
一个
流氓
蜂窝
基站、
恶意
或
被
入侵
的
调制解调器
模块、
或
诱发
一个
过长
notify
行
的
RF
操纵
在
无
任何
应用
交互
下
触达
该
缺陷；
处理程序
在
调制解调器
RX
线程
中
对
非
预期
事件
自动
运行。

影响
是
越界
栈
泄露
（到
日志
与
解析）
与
栈
破坏
可
使
调制解调器
RX
线程
崩溃
（拒绝
服务）。
写入
偏移
仅
弱
受
控制
因此
内存
安全
代码
执行
未
被
证明。
修复
以
``out_len``
限定
两个
扫描
循环
保持
所有
访问
在
线性化
缓冲区
内。

- `Zephyr 项目缺陷跟踪器 GHSA-8hrc-q8cp-6xhf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8hrc-q8cp-6xhf>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111243 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111243>`_

- `PR 113040 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113040>`_

- `PR 113042 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113042>`_

- `PR 113041 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113041>`_

:cve:`2026-12520`
-----------------

Zephyr HL7800 调制解调器
AT
响应
处理程序
中
的
栈
缓冲区
溢出
与
差一
写入

Sierra
Wireless
HL7800
蜂窝
调制解调器
驱动
（``drivers/modem/vendor_standalone/hl7800.c``
位于
v4.4.0
及
更早
的
``drivers/modem/hl7800.c``）
解析
AT
响应
使用
大约
二十
个
调用
``net_buf_linearize(value, sizeof(value), *buf, 0, len)``
到
一个
128 字节
栈
缓冲区
然后
写入
``value[out_len] = 0``
的
处理程序。
由于
``net_buf_linearize()``
（``lib/net_buf/buf.c``）
可
返回
等于
其
目标
长度
参数
的
计数
一个
恰好
填满
缓冲区
的
字段
使
终止
NUL
落在
末尾
一个
字节
之外
一个
单
字节
越界
写入
到
相邻
栈
内存。

``+KCELLMEAS``
小区
测量
处理程序
``on_cmd_atcmdinfo_rssi()``
更
严重：
其
将
线上
长度
``len``
作为
目标
大小
传入
（``net_buf_linearize(value, len, *buf, 0, len)``）
因此
一个
长于
128 字节
的
响应
行
以
受
攻击者
影响
的
内容
溢出
``value``
栈
缓冲区。
行
长度
来自
``net_buf_findcrlf()``
其
跨
整个
``net_buf``
分片
链
累积
字节
且
不
被
限制
到
128
因此
一个
过长
行
触达
该
缺陷。

数据
来自
经
UART
的
蜂窝
调制解调器
由
网络
驱动：
运营商
扫描
结果、
``+CGCONTRDP``
IP/DNS
信息、
socket
指示
与
``+KCELLMEAS``
邻区
报告。
能
整形
调制解调器
发出
什么
的
攻击者
——
流氓
基站、
被
入侵
的
调制解调器
基带、
或
喂入
超大
响应
分帧
的
远程
对端
——
可
驱动
一行
超过
128 字节。
处理程序
在
驱动
RX
线程
中
以
内核
上下文
运行
因此
破坏
在
内核侧。

``+KCELLMEAS``
路径
是
一次
完整
栈
缓冲区
溢出
其
最坏
情况
是
内核
上下文
代码
执行
且
其
下限
是
一个
可靠
崩溃；
其余
位置
是
单
字节
NUL
越界
写入。
利用
需要
调制解调器
发出
一个
过长
AT
响应
行
在
相邻
（蜂窝
无线电）
向量
上
给出
高
攻击
复杂度。
修复
传入
``sizeof(dst) - 1``
（以及
IMSI
与
``+KCELLMEAS``
位置
的
正确
显式
边界）
使
终止符
始终
保持
在
界内。

- `Zephyr 项目缺陷跟踪器 GHSA-9xc4-j5x8-v6jx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9xc4-j5x8-v6jx>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111243 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111243>`_

- `PR 113040 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113040>`_

- `PR 113042 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113042>`_

- `PR 113041 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113041>`_

:cve:`2026-12521`
-----------------

Zephyr HTTP 服务器
在
``zsock_poll()``
误报
返回
时
的
内核
超时
列表
破坏

HTTP
服务器
核心
循环
``subsys/net/lib/http/http_server_core.c``
的
``http_server_run()``
以
无限
超时
轮询
监听、
停止
与
客户端
套接字
并
将
``zsock_poll()``
返回
``0``
视为
不可能
执行
``break``
并
返回
``0``
不
触达
其
``closing:``
清理。
然而
``zsock_poll()``
（``lib/os/zvfs/zvfs_poll.c``
的
``zvfs_poll_internal()``）
即使
有
无限
超时
也
可
合法
返回
``0``：
在
``k_poll()``
唤醒
后
``ZFD_IOCTL_POLL_UPDATE``
遍
可能
发现
每个
fd
报告
无
``revents``
（误报
唤醒）
产生
``ret == 0``。

在
该
路径
上
``close_all_sockets()``
被
跳过
因此
``close_client_connection()``
中
的
每
客户端
``inactivity_timer``
（``struct k_work_delayable``）
取消
从不
运行。
控制
返回
``http_server_thread()``
``server_running``
仍
为
真
其
重新
进入
``http_server_init()``。
``http_server_init()``
随后
``memset()``
``ctx->clients``
数组——
包括
``k_work_delayable``
超时
节点
——
而
一个
或
多个
那些
timer
仍
已
武装
且
链接
在
内核
sys-timeout
列表
中。

当
内核
稍后
服务
此类
超时
其
操作
一个
重新
初始化
的
对象
并
跟随
现已
清零
的
列表
链接
破坏
内核
超时
列表
并
产生
一个
延迟
故障。
HTTP
服务器
循环
由
未
认证
远程
网络
对端
驱动
（``CONFIG_HTTP_SERVER``
所有
HTTP/1/2/3）
且
连接
变化
提高
误报
唤醒
竞态
的
概率
因此
远程
对端
可
影响
触发。
现实
影响
是
来自
被
破坏
超时
列表
的
拒绝
服务
（内核
崩溃/挂起）。

修复
以
``continue``
替换
``break``
在
误报
``0``
返回
时
重新
轮询
其
使
套接字
与
其
已
武装
timer
保持
完整
且
从不
在
存活
timer
上
重新
初始化
上下文。

- `Zephyr 项目缺陷跟踪器 GHSA-g5v9-xmfp-7gxm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-g5v9-xmfp-7gxm>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111239 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111239>`_

- `PR 112942 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112942>`_

- `PR 112941 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112941>`_

- `PR 112940 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112940>`_

:cve:`2026-12522`
-----------------

Zephyr hl7800 调制解调器
驱动
解析
网络
提供
``+CGCONTRDP``
地址
字段
时
的
栈
缓冲区
溢出

HL7800
蜂窝
调制解调器
驱动
的
``+CGCONTRDP:``
响应
处理程序
``drivers/modem/vendor_standalone/hl7800.c``
的
``on_cmd_atcmdinfo_ipaddr()``
解析
蜂窝
网络
分配
给
设备
的
PDP
上下文
动态
参数
（本地
地址、
子网
掩码、
网关
与
DNS
服务器）。
响应
被
线性化
到
一个
256 字节
栈
缓冲区
之后
每个
地址
字段
长度
从
网络
提供
数据
中
的
逗号/``.``
分隔符
位置
计算
并
直接
作为
长度
参数
传给
``strncpy()``
到
固定
64 字节
栈
缓冲区
``temp_addr_str``
（以及
16 字节
``iface_ctx.dns_v4_string``）。

由于
字段
长度
从
攻击者
控制
的
分隔符
位置
派生
且
未
对照
目标
缓冲区
限定
单个
字段
可
远
大于
64 字节。
恶意
或
被
冒充
的
蜂窝
网络
（例如
流氓
基站）
可
返回
一个
构造
的
``+CGCONTRDP``
响应
带
一个
过长
地址
字段
使
``strncpy()``
在
调制解调器
工作
线程
栈
上
越过
``temp_addr_str``
写入
外加
``temp_addr_str[addr_len]``
处
的
越界
NUL
写入。

不
需要
设备侧
特权
或
用户
交互：
设备
自身
在
正常
网络
附着
期间
发出
``AT+CGCONTRDP=1``
查询
并
解析
网络
返回
的
任何
内容。
溢出
破坏
监督者
上下文
中
的
相邻
栈
内存
产生
至少
一个
可
远程
触发
的
崩溃
且
在
无
栈
保护
的
目标上
潜在
的
控制
流
劫持。

修复
在
每个
拷贝
前
将
每个
字段
长度
对照
其
目标
缓冲区
（``temp_addr_str``
与
``dns_v4_string``）
限定
拒绝
过长
字段。

- `Zephyr 项目缺陷跟踪器 GHSA-hchc-6489-w66v
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hchc-6489-w66v>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111243 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111243>`_

- `PR 113040 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113040>`_

- `PR 113042 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113042>`_

- `PR 113041 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113041>`_

:cve:`2026-7656`
----------------

Zephyr net 协议栈
中
破坏的
IPv6
邻居
发现
输入
验证
允许
接受
伪造
RA/NS/NA

``subsys/net/ip/ipv6_nbr.c``
中
的
IPv6
邻居
发现
处理程序
（``handle_ra_input``、
``handle_ns_input``、
``handle_na_input``）
使用
一个
不正确
的
布尔
表达式
以
错误
的
运算符
优先级
将
RFC 4861
有效性
检查
与
ICMPv6
code
检查
组合：
形式
为
``((length/hop/source/target 检查)
&& (icmp_hdr->code != 0))``。
由于
每个
合法
ND
报文
携带
ICMPv6
code 0
攻击者
设置
``code == 0``
（正常
值）
使
整个
谓词
求值
为
假
因此
报文
从不
被
丢弃
且
所有
其他
检查
被
静默
跳过。
被
绕过
的
检查
包括
强制
的
Hop Limit == 255
验证
（其
证明
一个
ND
报文
源自
链路上
且
未被
转发）
以及
对
路由器
通告
的
源
必须
为
链路
本地
地址
的
要求
外加
多播
目标
健全性
检查。
因此
相邻
链路上
攻击者
——
且
由于
Hop-Limit-255
保护
被
绕过
潜在
的
远程/离路
攻击者
其
报文
否则
会
被
拒绝
——
可
使
伪造
的
路由器
通告、
邻居
请求
与
邻居
通告
报文
被
接受。
伪造
RA
使
攻击者
重新
配置
受害者
的
默认
路由器、
链路上
前缀
（SLAAC）、
MTU、
可达/重传
timer
以及
（带
``CONFIG_NET_IPV6_RA_RDNSS``）
DNS
服务器
而
伪造
NS/NA
使
邻居
缓存
投毒
成为
可能
使
中间人、
流量
重定向
与
拒绝
服务
成为
可能。
该
缺陷
是
一次
输入
验证/认证
弱点
而非
内存
安全
问题：
底层
报文
解析
原语
（``net_pkt_get_data``、
``net_pkt_read``、
``net_pkt_skip``）
独立
地
边界
安全
且
被
验证
的
``length``
是
真实
缓冲区
长度
因此
跳过
长度
检查
不
导致
任何
越界
访问。
该
缺陷
自
2018 年
逻辑
引入
存在
随
所有
发布
至
v4.4.0
发布；
其
通过
拆分
条件
使
任何
失败
检查
丢弃
报文
修复。

- `Zephyr 项目缺陷跟踪器 GHSA-cpjw-rvwx-ph9f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-cpjw-rvwx-ph9f>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 107902 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/107902>`_

- `PR 108131 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108131>`_

- `PR 108192 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108192>`_

- `PR 108195 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108195>`_

:cve:`2026-10666`
-----------------

``subsys/net/ip/utils.c`` 中
``net_ipaddr_parse()``
IPv4 地址带端口
解析
的
栈
缓冲区
溢出

``subsys/net/ip/utils.c``
的
``parse_ipv4()``
（经
``net_ipaddr_parse()``
触达
用于
"a.b.c.d:port"
形式
的
字符串）
以
``str_len - end - 1``
的
长度
将
端口
子串
拷贝
到
一个
固定
17 字节
栈
缓冲区
（``char ipaddr[NET_IPV4_ADDR_LEN + 1]``）
其中
``str_len``
是
完整
无
界
的
输入
长度
且
end
仅
为
（<=15 字节）
``:``
分隔符
的
偏移。
由于
目标
大小
从不
被
查询
一个
构造
的
地址
字符串
带
冒号
后
长
后缀
（例如
"1.2.3.4:"
后
跟
数百
字节）
导致
一次
越界
栈
写入
其
长度
与
内容
完全
受
攻击者
控制
（``memcpy``
后缀
加
一个
尾随
NUL）
使
内存
破坏
与
至少
一次
拒绝
服务
成为
可能
且
潜在
的
控制
流
劫持。
解析器
从
标准
套接字
API
（``zsock_getaddrinfo``/
字面
地址
解析）、
DNS
服务器
字符串
配置
与
eswifi
Wi-Fi
协处理器
DNS
响应
路径
触达
因此
一个
解析
网络
影响
地址
字符串
的
应用
暴露
于
此。
bug
在
解析器
添加
时
引入
（Zephyr v1.9.0）
随
所有
发布
至
v4.4.0
发布。
修复
移除
无
界
拷贝
并
在
拷贝
到
一个
小
专用
缓冲区
前
验证
端口
长度。
注意：
``parse_ipv6()``
中
等价
的
IPv6
"[addr]:port"
路径
在
该
commit
保留
同一
无
界
拷贝
且
保持
一个
独立
的
仍
可
触达
的
缺陷
实例。

- `Zephyr 项目缺陷跟踪器 GHSA-532c-7g7f-jhmh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-532c-7g7f-jhmh>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108529 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108529>`_

- `PR 109058 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109058>`_

- `PR 109072 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109072>`_

- `PR 109065 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/109065>`_

:cve:`2026-10673`
-----------------

ADIN2111/ADIN1110 OA SPI
以太网
RX
帧
重组
中
的
越界
写入

Zephyr
ADIN2111/ADIN1110
10BASE-T1S/T1L
以太网
驱动
（``drivers/ethernet/eth_adin2111.c``）
在
OPEN
Alliance
（OA）SPI
模式
中
通过
将
设备
提供
的
64 字节
数据
块
拷贝
到
一个
固定
静态
缓冲区
``ctx->buf``
（大小
``CONFIG_ETH_ADIN2111_BUFFER_SIZE``
默认
1524
字节）
重组
接收
的
以太网
帧。
在
``eth_adin2111_oa_data_read()``
中
每个
有效
块
被
``memcpy``
到
``ctx->buf[ctx->scur]``
且
写入
游标
``scur``
前进
不
检查
``scur``
+
len
保持
在
缓冲区
内。
块
数量
（至多
255
来自
BUFSTS
RCA
字段）
与
每
块
长度
完全
取自
线上
接收
的
帧
数据；
游标
仅
在
帧
起始
块
时
重置。
因此
单
对
以太网
段
上
的
攻击者
可
发送
一个
重组
大小
超过
配置
缓冲区
的
帧
使
驱动
RX
卸载
线程
将
攻击者
控制
的
帧
字节
越过
静态
缓冲区
末尾
写入
相邻
驱动/内核
内存
（最坏
情况
至多
约
14.8 KB）。
这
是
一次
可
远程/相邻
触达
的
越界
写入
（CWE-787）
可
破坏
内存
并
导致
拒绝
服务
或
潜在
的
代码
执行。
该
缺陷
在
OA
SPI
支持
添加
时
引入
（commit
0ca8b0756b1）
随
发布
v3.7.0 至
v4.4.0
发布。
修复
添加
一个
边界
检查
丢弃
超大
帧
并
在
拷贝
前
重置
游标。

- `Zephyr 项目缺陷跟踪器 GHSA-hm6v-4jh4-3qc4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hm6v-4jh4-3qc4>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 108200 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108200>`_

- `PR 108900 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108900>`_

- `PR 108901 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108901>`_

- `PR 108899 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108899>`_

:cve:`2026-12629`
-----------------

PL011 UART
错误
中断
从不
被
清除
使
外部
对端
中断
风暴
拒绝
服务
成为
可能

``drivers/serial/uart_pl011.c``
中
的
ARM
PL011
UART
驱动
失败
于
确认
接收
错误
中断。
在
PL011 上
帧、
奇偶、
断
与
溢出
错误
中断
（``PL011_IMSC_ERROR_MASK``）
仅
通过
写
中断
清除
寄存器
``UARTICR``
清除；
读
数据
寄存器
清除
RX
中断
与
每
字节
RSR
状态
但
不
清除
``MIS``
中
的
错误
中断
状态。
中断
服务
例程
``pl011_isr()``
仅
确认
CTS
调制解调器
状态
中断
且
从不
为
错误
位
写
``icr``
因此
被
断言
的
错误
中断
在
ISR
返回
后
保持
挂起。

当
应用
通过
公共
``uart_irq_err_enable()``
API
启用
错误
中断
报告
时
控制
串行
对端
的
攻击者
可
通过
在
RX
线
上
注入
线
错误
确定性地
断言
这些
错误
位
——
波特/停止位
不匹配
或
字符
中部
断
（帧/断
错误）、
翻转
的
奇偶
位
（奇偶
错误）
或
FIFO
洪水
（溢出
错误）。
由于
错误
中断
从不
被
清除
中断
线
保持
断言
且
CPU
立即
且
无限期
重新
进入
``pl011_isr()``
产生
一次
中断
风暴
活锁
核心
无
任何
前进
进展。

影响
是
仅
可用性
的
拒绝
服务
（永久
挂起）
可
从
外部
或
可
移除
UART
对端
触达。
利用
受
配置
门控：
错误
中断
默认
关闭
且
无
树内
子系统
启用
它
因此
仅
显式
在
基于
PL011
的
中断
驱动
端口
上
调用
``uart_irq_err_enable()``
的
应用
受
影响。
修复
使
``pl011_isr()``
通过
``uart->icr``
确认
挂起
的
错误
位
打破
循环
并
额外
在
``pl011_err_check()``
中
清除
锁存
的
RSR
状态。

- `Zephyr 项目缺陷跟踪器 GHSA-36rp-2hcp-f5hv
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-36rp-2hcp-f5hv>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111222 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111222>`_

- `PR 112933 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112933>`_

- `PR 112932 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112932>`_

:cve:`2026-12630`
-----------------

6LoWPAN
IPHC
解压
在
保留
目标
寻址
模式
上
的
越界
读取

Zephyr
的
6LoWPAN
IP
头
压缩
（IPHC）
解压
代码
在
``get_ihpc_inlined_size()``
（``subsys/net/ip/6lo.c``）中
包含
一次
越界
读取。
目标
内联
大小
在
``da_inline_size_table``
（有
13 个
条目）中
查找
使用
一个
从
接收
的
IPHC
分发
字
的
``M``、``DAC``
与
``DAM``
位
构建
的
索引
（``iphc & NET_6LO_IPHC_DA_MASK``
一个
0-15
的
4 位
值）。
保留
组合
13、14
与
15
不
被
边界
检查
且
越过
表
末尾
读取。

``iphc``
字
直接
取自
接收
帧
且
``get_ihpc_inlined_size()``
在
每个
入站
6LoWPAN
帧
上
经
``net_6lo_uncompress()``
从
802.15.4
接收
路径
（``subsys/net/l2/ieee802154/ieee802154_6lo.c``
与
``ieee802154_6lo_fragment.c``）
触达。
因此
无线电/相邻
链
上
的
未
认证
攻击者
可
构造
一个
其
目标
寻址
模式
半字节
选择
越界
索引
的
帧
无
特权
或
用户
交互。

越界
值
成为
计算
的
``inline_size``
其
随后
驱动
缓冲区
长度
检查
前
的
头
重建：
其
被
用于
解引用
``*(pkt->buffer->data + sizeof(iphc) + inline_size)``
并
计算
一个
可
下溢
的
``size_t``
``diff``
导致
报文
缓冲区
的
进一步
越界
读取
与
畸形
解压。
现实
影响
是
接收器
上
无线电
可
触发
的
越界
读取/拒绝
服务；
泄露
的
字节
不
被
返回
给
攻击者。
修复
拒绝
任何
超过
表
的
目标
索引
中止
畸形
帧
的
处理。

- `Zephyr 项目缺陷跟踪器 GHSA-45c8-pmgj-6jrc
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-45c8-pmgj-6jrc>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111272 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111272>`_

- `PR 113046 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113046>`_

- `PR 113044 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113044>`_

:cve:`2026-12631`
-----------------

Zephyr 内核
中
k_thread_join/k_thread_abort
系统调用
验证
的
破坏
访问
控制
拒绝

Zephyr
内核
通过
``kernel/thread.c``
的
``thread_obj_validate()``
验证
``k_thread_join()``
与
``k_thread_abort()``
系统调用
（在
``include/zephyr/kernel.h``
中
声明
``__syscall``）。
其
``default``
switch
分支
是
访问
拒绝
路径
在
``k_object_validate()``
返回
``-EPERM``
（调用
用户
线程
从不
被
授予
访问
目标
线程
对象）
或
``-EBADF``
（提供
的
指针
不是
正确
类型
的
已
注册
内核
对象）
时
取
该
分支。
该
分支
调用
``K_OOPS(K_SYSCALL_VERIFY_MSG(ret, "access denied"))``
但
``K_SYSCALL_VERIFY_MSG``
将
真
表达式
视为
成功；
非零
错误
码
``ret``
因此
被
读
为
"验证
OK"
内核
oops
从不
被
引发
且
控制
落入
``CODE_UNREACHABLE``。

由于
``k_thread_join()``
与
``k_thread_abort()``
是
系统调用
非
特权
用户
模式
线程
（在
``CONFIG_USERSPACE``
下）
可
通过
对其
不
拥有
的
线程
对象
调用
任一
系统调用
直接
触达
该
拒绝
路径。
在
违规
线程
被
干净
终止
的
替代
方案
执行
在
监督者
模式
中
在
系统调用
处理程序
内
运行
时
到达
``__builtin_unreachable()``。

在
Clang
构建
上
``CODE_UNREACHABLE``
发出
一个
非法
指令
陷阱
因此
用户
线程
可
确定性地
使
内核
崩溃——
一次
本地
可
触发
的
拒绝
服务
逃逸
用户空间
沙箱。
在
GCC
构建
上
该
路径
是
未
定义
行为：
编译器
可能
丢弃
``thread_obj_validate()``
的
返回
值
处理
因此
其
可
返回
一个
未
定义
的
``bool``；
如果
其
为
``false``
调用者
继续
进入
真实
的
``k_thread_join()``/``k_thread_abort()``
实现
用于
一个
用户
从不
被
授权
访问
的
线程
一次
访问
控制
绕过。

修复
将
验证
表达式
改为
``ret == 0``
使
被
拒绝
（非零）
结果
现在
正确
地
引发
``K_OOPS``
并
终止
违规
调用者。

- `Zephyr 项目缺陷跟踪器 GHSA-crfw-75jw-hjm3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-crfw-75jw-hjm3>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111301 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111301>`_

- `PR 113287 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113287>`_

- `PR 113286 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113286>`_

- `PR 113285 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113285>`_

:cve:`2026-12632`
-----------------

Zephyr PTP
报文
解析
中
来自
未
验证
报文
类型
的
越界
读取

Zephyr
的
精确
时间
协议
接收
处理程序
``subsys/net/lib/ptp/msg.c``
的
``ptp_msg_post_recv()``
通过
``ptp_msg_type()``
（``msg->header.type_major_sdo_id & 0xF``
范围
0-15）
直接
从
线上
取
4 位
报文
类型
并
用
其
索引
``msg_size[]``
表。
该
表
仅
定义
至
``PTP_MSG_MANAGEMENT``
（0xD）
的
条目
使其
``ARRAY_SIZE == 14``。
在
修复
前
不
有
上
界
检查
因此
未
定义
类型
``0xE``
与
``0xF``
索引
一个
或
两个
``int``
槽位
越过
数组
末尾
——
一次
相邻
只读
数据
的
越界
读取。

越界
值
随后
被
复用
为
长度：
其
门控
``msg_size[type] > cnt``
且
当
其
小
或
负
时
使
``cnt - msg_size[type]``
成为
一个
传
给
``msg_tlv_post_recv()``
的
大
正
预算
其
TLV
循环
随后
越过
接收
字节
遍历
报文
后缀
执行
进一步
越界
读取
与
报文
slab
之外
内存
上
的
就地
字节
交换
写入。

该
缺陷
直接
从
网络
触达：
``subsys/net/lib/ptp/port.c``
的
``ptp_port_event_gen()``
通过
``ptp_transport_recv()``
读取
PTP
帧
并
以
攻击者
选择
的
类型
调用
``ptp_msg_post_recv()``。
PTP
使用
UDP
组播
或
原始
以太网
（``0x88F7``）
且
无
认证
因此
同一
链路
上
任何
主机
可
在
启用
``CONFIG_PTP``
的
节点
上
无
前置
条件
触发
索引。

可
可靠
复现
的
影响
是
拒绝
服务
（故障/崩溃）；
存在
一个
有限
的
内存
破坏
路径
但
依赖
``msg_size[]``
相邻
的
构建
特定
值
攻击者
无法
调节
其。
修复
在
任何
索引
前
以
``-EBADMSG``
拒绝
``type >= ARRAY_SIZE(msg_size)``。

- `Zephyr 项目缺陷跟踪器 GHSA-frjr-h396-7wh4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-frjr-h396-7wh4>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111271 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111271>`_

- `PR 111665 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111665>`_

- `PR 111667 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111667>`_

- `PR 111666 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111666>`_

:cve:`2026-12633`
-----------------

通过
未
认证
路由器
通告
的
IPv6
6LoWPAN
Context
Option
处理
中
的
越界
写入

``subsys/net/ip/ipv6_nbr.c``
中
的
IPv6
邻居
发现
代码
处理
携带
在
ICMPv6
路由器
通告
内
的
6LoWPAN
Context
Option
（6CO
RFC 6775）。
在
``handle_ra_6co()``
中
8 位
``context_len``
字段
直接
取自
报文
且
从不
被
限定
到
RFC
最大值
128。
该
函数
计算
``context->context_len / 8``
然后
执行
``memset(context->prefix + context_len, 0, sizeof(context->prefix) - context_len)``
其中
``context->prefix``
是
一个
固定
16 字节
数组。

在
``context_len``
介于
136 与
255 之间
（且
选项
长度
字段
设为
3
修复
前
验证
接受
其）
时
``context_len / 8``
求值
为
17..31
因此
``memset``
长度
``16 - context_len/8``
使
无符号
``size_t``
参数
下溢
到
约
``SIZE_MAX``。
这
产生
一个
无
界
越界
``memset``
将
6lo
context
结构
远
之外
的
内核
内存
清零。

该
缺陷
可
从
未
认证、
链路
本地
输入
触达：
同一
链路
上
任何
主机
可
发送
一个
带
6CO
选项
的
构造
路由器
通告。
RA
处理程序
仅
在
调用
``handle_ra_6co()``
前
验证
选项
长度
字段
因此
单个
报文
触发
该
野
写入。
代码
在
启用
``CONFIG_NET_6LO_CONTEXT``
时
被
编译。

影响
是
通过
内存
破坏
的
可靠
远程
（相邻）
拒绝
服务
附带
完整性
损失
当
``memset``
在
系统
故障
前
清零
连续
内存
时。
路由器
通告
是
链路
范围
且
不
被
转发
因此
攻击者
必须
在
同一
链路
上
（``AV:A``）。
修复
在
长度
计算
前
拒绝
任何
大于
128 的
``context_len``。

- `Zephyr 项目缺陷跟踪器 GHSA-h5m5-hm6j-cgpf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-h5m5-hm6j-cgpf>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111275 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111275>`_

- `PR 113049 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113049>`_

- `PR 113051 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113051>`_

- `PR 113050 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113050>`_

:cve:`2026-12634`
-----------------

settings NVS 后端中 nvs_read 长度报告过大导致的栈缓冲区越界写入

Zephyr 设置子系统的 NVS 后端
（``subsys/settings/src/settings_nvs.c``）将存储的设置名称条目
读取到固定的 74 字节栈缓冲区中，
并用 ``buf[rc] = '\0'`` 进行空终止，
其中 ``rc`` 是 ``nvs_read()`` 的返回值。
根据其约定，``nvs_read()`` 返回*完整存储条目长度*
（``wlk_ate.len``），这可能超过提供的缓冲区长度——
实际只复制 ``MIN(len, stored_len)`` 字节，
但返回值可能大得多，仅受 NVS 扇区大小限制。
三处代码
（``settings_nvs_cache_match()``、``settings_nvs_load()`` 和
``settings_nvs_save()``）直接使用该值作为空终止索引而未做截断，
因此过大的存储名称条目会导致在攻击者可影响的偏移处
向栈缓冲区末尾之外写入单个 ``\0`` 字节（CWE-787）。

过大的条目无法通过常规设置 API 产生，
因为名称受 ``SETTINGS_MAX_NAME_LEN`` 限制。
它需要一个能够写入支撑设置分区的 flash 的参与者——
共享 flash 设备的共存或不可信组件、
恶意设置镜像/恢复，或离线/物理 flash 访问
（共享 flash 威胁模型）。畸形条目在
``settings_load()`` 于启动或子系统初始化时运行，
或在 ``settings_save()`` 期间被解析。

越界写入是在偏移等于伪造条目长度处（最多到 NVS 扇区大小）
的单个空字节，因此实际影响是崩溃或拒绝服务
以及有限的栈损坏，而非可靠的代码执行。
没有机密性影响，且该路径无法通过
常规设置接口从网络到达。
修复方法是在执行空字节存储之前
跳过所有 ``nvs_read()`` 长度大于或等于缓冲区大小的条目。

- `Zephyr 项目缺陷跟踪器 GHSA-q7c8-m2qg-385c
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-q7c8-m2qg-385c>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111314 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111314>`_

- `PR 113298 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113298>`_

- `PR 113296 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113296>`_

- `PR 113297 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113297>`_
:cve:`2026-12999`
-----------------

Infineon Airoc Wi-Fi 驱动在发送失败时泄漏 TX 缓冲区，导致池永久耗尽

Infineon Airoc Wi-Fi 驱动的发送回调 ``airoc_mgmt_send()``
（``drivers/wifi/infineon/airoc_wifi.c``）为每个出站数据包
从固定的 ``airoc_pool`` 分配一个 ``net_buf``。
当 ``whd_network_send_ethernet_data()`` 返回同步失败时，
底层 WHD 库不会接管该缓冲区的所有权，
但修复前的驱动在未释放的情况下返回 ``-EIO``。
因此每次发送失败都会从池中永久泄漏一个缓冲区。

``airoc_pool`` 很小且固定（``AIROC_WIFI_TX_PACKET_POOL_COUNT`` +
``AIROC_WIFI_RX_PACKET_POOL_COUNT``，默认 20 个缓冲区），
由 WHD 的 ``whd_host_buffer_get`` 回调在发送和接收之间共享。
一旦足够的发送失败使池耗尽，
``airoc_wifi_host_buffer_get()`` 对后续所有分配返回
``WHD_BUFFER_ALLOC_FAIL``，因此发送和
WHD 驱动的接收路径都失败，Wi-Fi 连接丢失
直到设备重启。

泄漏仅发生在发送错误路径上。Wi-Fi 相邻攻击者可以影响
导致同步发送失败的条件（例如在本地堆栈继续尝试
发送时解除认证/解除关联站点），
并且设备生命周期内的普通瞬时失败会累积
到相同状态。可靠的按需触发复杂度很高且影响
仅为可用性，但由此产生的拒绝服务是永久的，
不重启无法恢复。

修复在失败分支用 ``airoc_wifi_buffer_release()`` 释放缓冲区，
将其返回池。该提交还移除了
``airoc_mgmt_disconnect()`` 中冗余的 ``k_sem_give()``；
因为 ``data->sema_common`` 是二进制信号量（上限
1），重复的 give 仅在 1 处饱和且无安全影响。

- `Zephyr 项目缺陷跟踪器 GHSA-8w97-ghfm-5wjp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8w97-ghfm-5wjp>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111163 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111163>`_

- `PR 113304 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113304>`_

- `PR 113306 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113306>`_

- `PR 113305 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113305>`_

:cve:`2026-13212`
-----------------

Zephyr virtio 驱动从越界的 used-ring 描述符 id 调用任意函数指针

Zephyr virtio 驱动不验证 virtio
设备写入 used ring 的描述符链头 id。
在 ``virtio_isr()``
（``drivers/virtio/virtio_common.c``）中，
设备写入的 ``vq->used->ring[idx].id`` 被
直接用作 ``vq->recv_cbs[]`` 和 ``vq->desc[]`` 的索引，
两者都恰好分配了 ``vq->num`` 个条目。
``recv_cbs[]`` 保存 ``{cb, opaque}``
回调条目，被索引的回调指针随后作为
``cbe.cb(cbe.opaque, used_len)`` 调用。

因为 id 作为 16 位值被消费且无边界检查，
恶意或被入侵的 virtio 后端（不可信的 hypervisor，
或 PCI 或 MMIO 传输上不可信的
硬件/对等处理器 virtio 设备）可以提供远超
``vq->num`` 的 id。这导致从 ``recv_cbs[]`` 之外的
堆内存越界读取一个 ``{函数指针,
参数}`` 对，之后驱动在客户机的中断上下文中
调用该攻击者构造的指针。无需客户机权限或
用户交互；后端通过写入共享 used ring
并触发队列中断来触发它。

结果是 Zephyr
客户机中的任意/攻击者影响的函数指针调用，
即一个控制流劫持原语，可导致代码执行或
至少可靠的崩溃。修复在任何
索引 ``recv_cbs[]``/``desc[]`` 或调用回调之前
拒绝任何 used-ring id ``>= vq->num``。
这影响使用 ``CONFIG_VIRTIO`` 且采用 PCI 或 MMIO 传输的构建。

- `Zephyr 项目缺陷跟踪器 GHSA-7884-373w-qqhx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7884-373w-qqhx>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111289 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111289>`_

- `PR 113344 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113344>`_

- `PR 113345 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113345>`_

:cve:`2026-13213`
-----------------

Bluetooth HAS：已配对对端在 bt_has_register 之前重连时的空指针解引用拒绝服务

``subsys/bluetooth/audio/has.c`` 中的
Hearing Access Service（HAS）GATT 服务器
通过 ``BT_CONN_CB_DEFINE`` 无条件安装一组连接回调，
因此
``security_changed()`` 在应用调用
``bt_has_register()`` 之前就会为每个建立安全的连接运行。
服务属性指针
``hearing_aid_features_attr``、``preset_control_point_attr`` 和
``active_preset_index_attr`` 保持为 ``NULL``，
直到 ``bt_has_register()`` 解析它们
并设置 ``has.registered``。

启用 ``CONFIG_BT_SETTINGS`` 时，``settings_set_cb()``
在启动时恢复每个已配对客户端的
持久化上下文，并无条件地将 ``context->flags`` 设为
``BONDED_CLIENT_INIT_FLAGS``（非零）。
当之前已配对的对端在
``bt_has_register()`` 被调用之前的启动窗口内
重连并重新建立安全时，
``security_changed()`` 看到非零标志并调度
``notify_work_handler``，后者用仍为 ``NULL`` 的
属性指针调用 ``bt_gatt_is_subscribed()``。
这会触发断言（``bt_gatt_is_subscribed()`` 中的
``__ASSERT(attr, ...)``），或在断言
被编译掉时对 ``attr->uuid`` 进行空指针解引用。

结果是可远程触发的（Bluetooth，相邻）HAS 外设崩溃。
利用需要对端之前已与设备配对，
并在应用注册服务之前的启动时竞争窗口内
重连；持续重连的对端可延长中断。
影响仅为拒绝服务，
无内存损坏或信息泄露。

修复在
``security_changed()`` 中添加早期 ``if (!has.registered) { return; }`` 保护，
因此在 GATT 服务被注册且其属性指针有效之前
不调度任何通知工作。

- `Zephyr 项目缺陷跟踪器 GHSA-9rj8-3fvm-cc9f
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9rj8-3fvm-cc9f>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111767 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111767>`_

- `PR 113349 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113349>`_

- `PR 113347 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113347>`_

- `PR 113348 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113348>`_

:cve:`2026-13214`
-----------------

OCPP GetConfiguration 键解析中的栈缓冲区溢出

``subsys/net/lib/ocpp/ocpp_j.c`` 中的
OCPP 1.6 客户端在 ``parse_getconfig_msg()`` 中包含一个栈缓冲区溢出。
在处理来自中央系统的 ``GetConfiguration`` 请求时，
处理程序用无界 ``strcpy()`` 将攻击者控制的 JSON ``"key"`` 字符串
复制到调用者的固定 50 字节栈缓冲区
（``skey[CISTR50]``，声明在
``subsys/net/lib/ocpp/ocpp.c`` 中）。
解析的键值直接指向接收缓冲区，
因此其长度仅受消息
大小限制（``CONFIG_OCPP_RECV_BUFFER_SIZE``，默认 2048）。

``GetConfiguration`` 消息通过充电站
向其配置的中央系统打开的 WebSocket 连接传递。
读取线程
``ocpp_wsreader()`` 将消息读入 ``ui->recv_buf`` 并通过
PDU 函数表将其分派到
``parse_getconfig_msg()``。控制中央系统端点的攻击者，
或非加密连接上的中间人，可以发送
``"key"`` 字段超过 50 字节的
``GetConfiguration`` 请求并用攻击者选择的字节
溢出读取线程的栈。

后果是 OCPP 读取线程上可远程触发的栈破坏：
至少是拒绝服务，并且根据构建时
强化措施（如栈 canary 和 MPU 配置）
可能可行地远程代码执行。修复用
有界的 ``strncpy(key, payload.key[0], CISTR50 - 1)`` 替换
``strcpy()`` 并显式 NUL 终止，
与姊妹
处理程序已使用的有界复制一致。

- `Zephyr 项目缺陷跟踪器 GHSA-fqhf-6v24-4px2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fqhf-6v24-4px2>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111242 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111242>`_

- `PR 113330 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113330>`_

- `PR 113329 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113329>`_

:cve:`2026-13215`
-----------------

Zephyr ext2 挂载：未验证的 superblock 块大小导致来自构造文件系统镜像的越界写入

Zephyr ext2 文件系统驱动在挂载文件系统时
未验证磁盘 superblock 的 ``s_log_block_size`` 字段。
``subsys/fs/ext2/ext2_impl.c`` 中的
``ext2_verify_disk_superblock()`` 检查魔数、修订版、inode 大小和组
计数，但从不限制 ``s_log_block_size``。
验证成功后，
``subsys/fs/ext2/ext2_ops.c`` 从这个攻击者控制的 ``uint32_t``
计算 ``fs->block_size = 1024 <<
superblock.s_log_block_size``，因此构造的
值要么使移位溢出（未定义行为），
要么产生远大于
``CONFIG_EXT2_MAX_BLOCK_SIZE`` 的块大小。

该块大小随后由 ``ext2_init_blocks_slab()``
传给 ``k_mem_slab_init()``
以从固定静态缓冲区中划分出 ``CONFIG_EXT2_MAX_BLOCK_COUNT`` 个块

``__ext2_block_memory_buffer``，其大小为 ``CONFIG_EXT2_MAX_BLOCK_COUNT *
CONFIG_EXT2_MAX_BLOCK_SIZE``。``k_mem_slab_init()`` 不验证
请求的块是否适合缓冲区，且 ext2 包装器丢弃其返回值，
因此 slab 被布局在静态缓冲区末尾之外。
挂载立即将每个 ``fs->block_size`` 字节的块组、
位图和 inode 块读入这些 slab 块，
在第一次块读取时产生对相邻静态内存的越界写入。

整条路径仅由从挂载镜像读取的数据门控，
因此任何能够向挂载它的设备提供构造 ext2 镜像的攻击者
（例如可移动 SD 卡或存储介质）都可到达。
因为 ext2 驱动在内核模式运行，
提供镜像字节可产生监督者模式内存破坏原语，
影响范围从拒绝服务到潜在代码执行。

修复拒绝使移位溢出（大于 11）的
``s_log_block_size`` 值，或产生超过 ``CONFIG_EXT2_MAX_BLOCK_SIZE``
块大小的值，因此块 slab 再也不能被初始化
得比其支撑缓冲区更大。

- `Zephyr 项目缺陷跟踪器 GHSA-j52j-gfj9-rwjm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j52j-gfj9-rwjm>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111241 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111241>`_

- `PR 113754 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113754>`_

- `PR 113327 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113327>`_

- `PR 113326 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113326>`_

:cve:`2026-13216`
-----------------

Zephyr virtio PCI 驱动中来自未验证设备提供能力长度的栈越界写入

virtio PCI 驱动（``drivers/virtio/virtio_pci.c``）
在驱动初始化期间解析设备的 PCI 能力
列表。在 ``virtio_pci_read_cap()`` 中，
设备提供的能力长度字节 ``cap_len``
（通过 ``pcie_conf_read()`` 从 PCI 配置空间读取）
仅用 ``assert(tmp.cap_len == cap_struct_size)`` 检查。
该 ``assert`` 解析为 ``__ASSERT_NO_MSG()``，
由 ``CONFIG_ASSERT`` 门控，在生产构建中默认关闭，
因此该值完全未验证地到达复制逻辑。

长度随后驱动一个循环，将额外的能力 dword
复制到调用者提供的固定大小
栈缓冲区。低于 24 字节基础 ``struct
virtio_pci_cap`` 的 ``cap_len`` 使无符号 ``extra_data_words`` 计数
下溢到接近 ``SIZE_MAX`` 的值，
产生实际上无界的栈写入；
高于调用者缓冲区的 ``cap_len``（最多 255）
在缓冲区之外写入最多约 228 字节的
设备控制数据。两者都是
在内核模式下于启动时设备探测期间执行的
攻击者控制内容的越界写入。

输入源自 virtio 设备。在 Zephyr 作为
hypervisor 下客户机运行的常见部署中，
设备后端是主机，其权限已完全
高于客户机，因此该缺陷不产生权限提升。
可利用的情况是
相对于 Zephyr 内核不可信的 virtio 设备——
裸机系统上不可信或
物理/直通 virtio PCIe 设备，或
客户机必须防御主机的机密计算姿态——
在那里恶意设备可破坏内核栈并可能
实现代码执行或崩溃。

修复用运行时范围检查替换被编译掉的断言，
在任何算术或复制之前
拒绝 ``[sizeof(struct virtio_pci_cap), cap_struct_size]`` 之外的 ``cap_len``。

- `Zephyr 项目缺陷跟踪器 GHSA-qrh3-4mvv-w667
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qrh3-4mvv-w667>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111240 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111240>`_

- `PR 113325 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113325>`_

- `PR 113324 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113324>`_

- `PR 113323 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113323>`_

:cve:`2026-13217`
-----------------

Zephyr 原生 IPv6 网络栈中来自畸形 IPv6 分片的 RX 缓冲区泄漏

``subsys/net/ip/ipv6.c`` 中的
IPv6 接收路径在分片重组期间
不释放网络数据包缓冲区。
当 ``ipv6_frag_recv()`` 检测到
畸形分片时，它返回
``NET_ERR`` 而不取消引用数据包，
泄漏 RX 网络数据包缓冲区。
每次 ``k_mem_slab_alloc()`` 调用都缺少
对应的 ``k_mem_slab_free()``，
因此重放这样的数据包几次
会耗尽 RX 缓冲区 slab，
之后驱动反复无法获取 RX
缓冲区，导致拒绝服务。

- `Zephyr 项目缺陷跟踪器 GHSA-w234-pcxp-4q8r
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-w234-pcxp-4q8r>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104044 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104044>`_

- `PR 104205 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104205>`_

- `PR 104206 v4.2 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104206>`_

- `PR 104209 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104209>`_

  <https://github.com/zephyrproject-rtos/zephyr/pull/104209>`_

:cve:`2026-13343`
-----------------

MIDI 2.0 UMP Stream 响应器中未初始化栈内存泄露

``lib/midi2/ump_stream_responder.c`` 中的
UMP Stream 响应器库
在
16
字节
``struct midi_ump``
（``uint32_t data[4]``）中
构建
回复
包。
构建器
``make_endpoint_info()``
和
``make_function_block_info()``
仅
填充
前
两个
字
（``res.data[0]``
和
``res.data[1]``），
且
在
修复
前
将
其
结果
声明
为
未
初始化
的
局部
变量
（``struct midi_ump res;``）。
剩余
两个
字
（``res.data[2]``、``res.data[3]``）
保留
过期
栈
内容。

Endpoint
Info
和
Function
Block
Info
通知
是
UMP
Stream
消息
（``UMP_MT_UMP_STREAM``），
长
4
字，
因此
完整
16
字节
包——
包括
两个
未
初始化
的
字——
由
``cfg->send()``
原样
传输。
响应器
由
攻击者
提供
的
UMP
Stream
Endpoint-Discovery
/
Function-Block-Discovery
请求
通过
``ump_stream_respond()``
驱动。
在
树内
Network
MIDI
2.0
服务器
（``subsys/net/lib/midi2/netmidi2.c``）中
这些
请求
作为
UDP
数据报
到达，
且
在
默认
无
认证
端点
下，
远程
对端
可以
建立
会话
并
触发
响应；
同一
库
也
服务
USB
MIDI
2.0
主机。

每个
发现
请求
使
设备
向
对端
泄露
8
字节
其
自身
未
初始化
栈
内存，
且
请求
可
自由
重复。
这是
机密性
的
信息
泄露
（根本
原因
是
未
初始化
变量
的
使用，
CWE-457/CWE-908）；
泄露
的
字
可能
包括
残余
数据
或
指针
值。
无
内存
损坏、
完整性
或
可用性
影响。

修复
零
初始化
两个
结果
结构
（``struct midi_ump res = {0};``），
使
尾部
字
在
传输
前
被
清除。
这是
仅有的
两个
响应器
构建器
留下
尾部
字
未
设置
（``send_string()``
已
零
初始化
其
缓冲区），
因此
泄露
被
完全
关闭。

- `Zephyr 项目缺陷跟踪器 GHSA-4w5x-w7j4-6xxc
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4w5x-w7j4-6xxc>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111286 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111286>`_

- `PR 113341 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113341>`_

:cve:`2026-13351`
-----------------

net：恶意分片的 IPv6 包可阻止接收/处理未来入站包

Zephyr
网络
堆栈
可以
被
阻止
接收
或
处理
未来
入站
包
通过
发送
几个
恶意
分片
的
IPv6
包。
当
``net_ipv6_handle_fragment_hdr()``
对
畸形
分片
触发
ICMPv6
错误
响应
时，
它
返回
``NET_OK``
而
不
取消
引用
包，
泄露
RX
网络
数据包
缓冲区。
每次
``k_mem_slab_alloc()``
调用
都
缺少
对应
的
``k_mem_slab_free()``，
因此
重放
这样
的
包
几次
会
耗尽
RX
缓冲区
slab，
之后
驱动
反复
无法
获取
RX
缓冲区，
导致
拒绝
服务。

- `Zephyr 项目缺陷跟踪器 GHSA-cv4q-2j56-4wqf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-cv4q-2j56-4wqf>`_

该问题已在 main 分支修复，将随 v4.4.0 发布

- `PR 104044 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104044>`_

- `PR 104205 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104205>`_

- `PR 104206 v4.2 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104206>`_

- `PR 104209 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/104209>`_
:cve:`2026-13478`
-----------------

Zephyr ext2 块位图验证中来自构造 s_blocks_count 的越界读取

Zephyr ext2 文件系统驱动在
``ext2_init_fs()``（``subsys/fs/ext2/ext2_impl.c``）中
通过向 ``ext2_bitmap_count_set()`` 传递 ``fs_blocks =
s_blocks_count - s_first_data_block`` 来验证磁盘上的块位图。
该辅助函数（``subsys/fs/ext2/ext2_bitmap.c``）
将其参数视为位数并每八位读取一个
位图字节，但位图缓冲区（``BGROUP_BLOCK_BITMAP``）
是仅 ``fs->block_size`` 字节（容量 ``fs->block_size * 8`` 位）的
单个获取块。``s_blocks_count`` 和 ``s_first_data_block``
原样取自 superblock 且从未针对
此单组容量设置上限；``ext2_verify_disk_superblock()``
检查魔数、修订版和块大小移位，但不检查块计数。

具有过大 ``s_blocks_count``（最多约 40 亿，
对比最大 4096 字节块 / 32768 位位图）的构造 ext2 镜像
使 ``ext2_bitmap_count_set()`` 扫描
位图块之后约 512 MB 的内存——
对静态块 slab 和相邻内存的大规模越界读取。

该缺陷在挂载期间到达：``ext2_init_fs()``
从 ``ext2_mount()``（``subsys/fs/ext2/ext2_ops.c``）
调用，即注册的 ``.mount`` 操作。
任何挂载攻击者提供的 ext2 镜像的路径
（可移动介质、磁盘/flash 分区，或
下载的镜像）都会触发它。
内核权限的解析器处理
攻击者控制的数据，因此该缺陷在任何
不可信 ext2 介质可被挂载的地方都可利用。

影响仅为越界读取：
产生的位计数在内部比较且
挂载被拒绝，因此不返回攻击者控制的字节
（不是有用的信息泄露）。约 512 MB 的过度读取
几乎肯定会跨越未映射或
MPU 保护的边界并触发故障，
使系统崩溃——
由挂载单个畸形镜像触发的拒绝服务。
修复在扫描之前拒绝任何 ``fs_blocks`` 超过
``fs->block_size * 8`` 的镜像。

- `Zephyr 项目缺陷跟踪器 GHSA-gj29-7f7m-4c29
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gj29-7f7m-4c29>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111970 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111970>`_

- `PR 112132 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112132>`_

- `PR 112131 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112131>`_

- `PR 113351 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113351>`_

:cve:`2026-13479`
-----------------

LoRaWAN 时钟同步 AppTimeAns 下行处理程序中的越界读取

LoRaWAN 应用层时钟同步服务在
``clock_sync_package_callback()``（``subsys/lorawan/services/clock_sync.c``）
中解析下行。其
命令循环仅保证一个字节命令 id 在界内；
对于
``CLOCK_SYNC_CMD_APP_TIME``（``AppTimeAns``）命令，
处理程序随后通过 ``sys_get_le32()`` 读取 4 字节
时间校正，外加一个字节 token，
而不检查接收缓冲区（``len - rx_pos``）中
是否还剩 5 字节。
因此短或构造的 ``AppTimeAns``
会在解密负载末尾之外读取最多 5 字节。

负载（``rx_buf``/``len``）是传递给
注册下行回调（``mcps_indication->Buffer``/``BufferSize``）的
解密应用帧。到达
处理程序需要在时钟同步端口上有一个通过 LoRaWAN MAC 完整性
检查和 FRMPayload 解密的帧，
因此实际攻击者是恶意或被入侵的
网络/应用服务器（``AppTimeAns`` 的指定发送者）
或持有会话密钥的一方，
而非任意无线电监听者。

过度读取是有界的：
后备存储是固定 255 字节静态缓冲区，
因此几个杂散字节不会触发故障，
且读取的值（``time_correction``、``token``）
仅在内部使用且从不传输，
因此对攻击者没有泄露
且无崩溃。唯一效果是
匹配 ``ctx.req_token`` 的过期 ``token``
可以将垃圾 ``time_correction`` 应用到
设备自身的时钟偏移
（``ctx.time_offset``），
对受害者的时间估计有轻微完整性影响。
修复添加显式长度检查，
丢弃过短的 ``AppTimeAns``。注意
周期性和强制重同步处理程序中的
姊妹单字节读取
仍以相同可忽略的影响保持无保护。

- `Zephyr 项目缺陷跟踪器 GHSA-2m6g-p3vx-p2fh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2m6g-p3vx-p2fh>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111983 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111983>`_

- `PR 113433 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113433>`_

- `PR 113432 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113432>`_

- `PR 113431 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113431>`_

:cve:`2026-13480`
-----------------

LoRaWAN 分片数据块传输（FUOTA）下行处理程序中的越界读取

LoRaWAN TS004 分片数据块传输处理程序
``frag_transport_package_callback()``（``subsys/lorawan/services/frag_transport.c``）
在每次访问前不验证是否有足够负载字节
就解析下行命令字节。
循环的唯一边界是 ``rx_pos < len``；
在消费一个字节命令 id 后，
处理程序将 ``rx_buf + rx_pos`` 强制转换为
10 字节 ``struct
frag_transport_setup_req``，
对于 ``DATA_FRAGMENT`` 命令，
将 ``&rx_buf[rx_pos]`` 传给分片解码器，
后者恰好读取 ``ctx.frag_size`` 字节
——两种情况下都无剩余长度检查。

分片大小由攻击者在先前
``FRAG_SESSION_SETUP`` 命令中选择
（``ctx.frag_size = req->frag_size``，
上限
``CONFIG_LORAWAN_FRAG_TRANSPORT_MAX_FRAG_SIZE``，
默认 232）。``rx_buf`` 别名
loramac-node MAC 层中 255 字节静态
``MacCtx.RxPayload`` 缓冲区，
而 ``len``
是实际解密负载长度。
通过在负载末尾附近附加一个匹配索引分片，
并用不匹配索引的
``DATA_FRAGMENT`` 填充命令填充下行
（每个使 ``rx_pos`` 前进三字节而不
产生应答），
攻击者可使解码器在
``RxPayload`` 末尾之外读取最多约 ``frag_size`` 字节，
将相邻静态内存复制到解码器缓冲区
和 FUOTA flash 镜像。

处理程序仅在已通过 LoRaWAN 帧 MIC 和
FRMPayload 解密的下游上运行，
因此该缺陷仅可由
持有设备
会话密钥的一方（FUOTA 服务器或
已入侵这些密钥的攻击者）到达。
越界字节从不返回给发送者——
唯一发出的上行是
携带分片计数的状态应答——
因此无直接泄露通道，
且在典型扁平内存 LoRaWAN MCU 上，
过度读取保持在映射内存内，
使崩溃不太可能。
因此影响是有界越界读取，
机密性后果有限且无写入或控制流原语。
修复在每次访问前添加剩余长度保护。

- `Zephyr 项目缺陷跟踪器 GHSA-845m-2m84-g5h2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-845m-2m84-g5h2>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111983 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111983>`_

- `PR 113433 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113433>`_

- `PR 113432 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113432>`_

- `PR 113431 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113431>`_

:cve:`2026-13481`
-----------------

Zephyr net PTP 中 PTP 管理 TLV TIME 解析的越界读取

``subsys/net/lib/ptp/tlv.c`` 中的
IEEE 1588 PTP 管理消息解析器
错误处理
``PTP_MGMT_TIME`` 管理 id。
在 ``tlv_mgmt_post_recv()`` 中，
``PTP_MGMT_TIME``
案例将 ``mgmt_tlv->data`` 强制转换为
10 字节 ``struct ptp_timestamp``
并读取它（然后
字节交换并写回），
而不先检查 TLV 数据字段是否
至少 ``sizeof(struct ptp_timestamp)``。
同一 switch 中每个姊妹管理 id
都先验证其长度；
``PTP_MGMT_TIME`` 是唯一缺少该检查的案例。

传入的长度是管理数据大小（``tlv->length - 2``），
且上游
``ptp_tlv_post_recv()`` 中的保护
仅要求 ``tlv->length > 2``，
而
``msg_tlv_post_recv()`` 仅验证 TLV 适合接收字节计数，
而非按 id 最小值。
因此本地 PTP 段上的对端可以发送
携带短 ``PTP_MGMT_TIME`` TLV（数据小至
2 字节）的
``PTP_MSG_MANAGEMENT`` 消息，
使解析器在验证数据之外读取并写入 8 字节。
消息类型和 TLV 内容直接取自线路，
因此当 ``CONFIG_PTP`` 启用时，
任何相邻攻击者都可到达该路径。

过度读取和写回保持在 ``struct ptp_msg`` 分配内
（``mgmt_tlv->data`` 位于前导 ``mtu[NET_ETH_MTU]`` 联合体成员中，
因此 ``data +
10`` 最多落在 ``mtu[]`` 之后几字节处，
在同一对象内），
因此这是对对象内相邻内存的越界读取
加上
消息已解析时间戳的有界原地损坏，
而非跨分配内存损坏。
影响限于
相邻字节的轻微信息暴露
和设备已解析
管理 TIME 值的损坏；
访问无崩溃且无可到达的引用计数
损坏。

修复在
强制转换前添加 ``if (length < sizeof(struct ptp_timestamp)) { return -EBADMSG; }``，
匹配其他管理 id 案例
并完全关闭接收路径
缺陷。

- `Zephyr 项目缺陷跟踪器 GHSA-mh5r-jxh8-hxwx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-mh5r-jxh8-hxwx>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111969 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111969>`_

- `PR 113353 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113353>`_

- `PR 117480 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/117480>`_

- `PR 117479 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/117479>`_

:cve:`2026-13734`
-----------------

Zephyr WireGuard 在防重放检查之前修改对端状态，使捕获-重放端点劫持成为可能

Zephyr 的 WireGuard VPN 数据平面接收处理程序
``wg_process_data_message()``
（``subsys/net/lib/wireguard/wg_crypto.c``）
太晚验证防重放计数器。
在 ``MESSAGE_TRANSPORT_DATA`` 包的
AEAD 解密成功后，
代码提交了多个对端状态更改——
``update_peer_addr()``（端点漫游更新）、
``keypair->last_rx``/``peer->last_rx`` 存活计时器，
以及 ``keypair_update()``
（将 ``next`` → ``current`` 提升并销毁先前的密钥对）——
之后才调用 ``wg_check_replay()``。
对于重放包，重放检查返回
``-EINVAL``，
但先前没有任何修改被回滚。

AEAD 标签验证内容但不验证新鲜度，
因此重放但真实的
传输包能正确解密。
捕获线路上一个有效密文的攻击者
（在路径上或共享介质观察员）
可以从任意
伪造源地址重新注入它。
到达处理程序无需凭据：
它由
``subsys/net/lib/wireguard/wg.c``
中的分派直接从入站 UDP 数据报驱动。

因为状态修改在重放检查之前提交，
重放将对端端点重新指向
攻击者选择的源地址
（漫游劫持），
重定向受害者的后续出站隧道流量
直到合法对端的下一个包
重新纠正它；
它还会过早销毁先前密钥对
并刷新 RX
存活计时器。隧道负载在会话密钥对下保持加密，
因此这是
完整性/可用性影响
（流量重定向和会话中断），
而非
负载泄露。修复将 ``wg_check_replay()`` 移到
成功解密后、
任何对端状态修改之前，
匹配 WireGuard 规范
和 Linux 参考实现。

- `Zephyr 项目缺陷跟踪器 GHSA-x7q7-fjx9-4vj2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x7q7-fjx9-4vj2>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111043 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111043>`_

- `PR 112250 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112250>`_

:cve:`2026-13735`
-----------------

WireGuard 保活传输数据消息在未经 Poly1305 认证的情况下被接受

Zephyr 的 WireGuard 实现（``subsys/net/lib/wireguard/wg_crypto.c``）
错误处理
保活包。在 ``wg_process_data_message()`` 中，
任何负载恰好 16 字节
（空明文加裸 Poly1305 标签，
即
保活）的类型 4 传输数据消息
都被接受并立即返回，
在
``wg_decrypt_packet()`` 被
调用之前。
因此 Poly1305 认证标签
从未被验证；
唯一
先前门是
明文接收者索引查找
（攻击者提供的 ``data_hdr->receiver`` 上的
``get_peer_keypair_for_index()``）
和非密码学密钥对
有效性/过期检查。

该路径完全可从网络到达：
WireGuard 端口上的入站 UDP
由 ``wg_input()`` 分派到
``handle_transport_data()``
然后
``wg_process_data_message()``。
32 位接收者索引在
WireGuard 握手和数据消息中以明文传输，
因此在路径上观察者直接得知它
且
路径外攻击者可
对 UDP 端口暴力破解它。
给定
该索引的
活动
接收有效会话，
攻击者可发送 16 字节垃圾负载
并在
不持有
会话密钥的情况下
使其被接受。

接受时，
未认证消息
使管理层观察到
伪造的 ``NET_EVENT_VPN_CONNECTED`` 信号
（设置 ``peer->first_valid`` 并通知
任何 ``net_mgmt`` 监听器）
并递增保活-RX 统计。
影响限于
此状态信号的完整性：
不解密或注入任何明文，
不泄露任何密钥，
且
提前返回路径
不更新对端端点或
存活
计时器，
因此
无流量注入、
会话接管
或
可用性后果。

修复移除
解密前
提前返回，
使 16 字节负载
流经
``wg_decrypt_packet()``，
后者
验证
空明文上的
Poly1305 标签，
之后
是
现有
防重放检查；
只有
已认证、
非重放
消息
随后
被识别为
保活。
伪造保活
现在
失败
标签检查
并
被计数为
解密失败。

- `Zephyr 项目缺陷跟踪器 GHSA-xxrw-r78f-f6mx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xxrw-r78f-f6mx>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111043 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111043>`_

- `PR 112250 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112250>`_

:cve:`2026-14366`
-----------------

SiWx91x WiFi 驱动对调用者拥有的 TX net_pkt 双重取消引用/释放后使用

Silicon Labs SiWx917 WiFi 驱动的发送回调
``siwx91x_send()``
（``drivers/wifi/siwx91x/siwx91x_wifi.c``）
释放它不拥有的网络数据包。
在
Zephyr TX 路径中，
``net_pkt`` 由 L2/网络堆栈拥有；
驱动仅
借用它
将帧字节
复制到
本地 ``net_buf``。
修复前，
在
传输后，
``siwx91x_send()`` 还
对
调用者拥有的
包
调用 ``net_pkt_unref(pkt)``，
丢弃其
最后一个
引用
并
过早
将其
返回
共享
包
池。
此
代码
路径
默认
编译
（``CONFIG_WIFI_SILABS_SIWX91X_NET_STACK_NATIVE``）。

调用者
``ethernet_send()``
（``subsys/net/l2/ethernet/ethernet.c``）
在
驱动
返回
后
继续
使用
包：
它
读取
``net_pkt_get_len(pkt)``，
更新
TX
统计，
然后
执行
自己的
``net_pkt_unref(pkt)``。
因为
驱动
已经
释放
包，
这些
是
释放后使用
读取
后
跟
第二个
取消引用
（双重
释放）。
当
并发
网络
活动
在
两个
取消引用
之间
回收
已释放
slab
槽
时，
尾部
取消引用
递减
另一个、
活动
包的
引用
计数
并
释放
它，
破坏
接收
和
发送
路径
共享
的
``net_pkt``
池。

该
缺陷
由
原生
堆栈
SiWx917
WiFi
接口
上的
普通
传输
执行，
且
同一
WiFi
网络
上的
相邻
攻击者
可
诱导
传输
（例如
ARP
或
ICMP
echo
应答，
或
TCP
握手）
以
驱动
路径。
主要
可观察
影响
是
可用性
丢失
（池
破坏
导致
的
传输
挂起
和
崩溃），
以及
竞态
依赖
的
内核
网络
缓冲
池
内存
破坏。
修复
从
``siwx91x_send()``
移除
错误的
``net_pkt_unref(pkt)``；
驱动
的
接收
路径
取消引用，
正确
释放
驱动
自己
分配
的
包，
不受
影响。

- `Zephyr 项目缺陷跟踪器 GHSA-f9qq-jv4w-pqxg
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-f9qq-jv4w-pqxg>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 112180 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112180>`_

- `PR 113523 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113523>`_

- `PR 113522 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113522>`_

:cve:`2026-14367`
-----------------

I3C IBI 工作节点空闲链表在 ISR 与工作队列线程之间的数据竞态

``drivers/i3c/i3c_ibi_workq.c`` 中的
I3C IBI 子系统
通过
实现为
普通
``sys_slist_t``
的
空闲链表
``i3c_ibi_work_nodes_free``
分发
静态
分配
的
工作
节点，
它
不提供
任何
同步。
分配
辅助
（``i3c_ibi_work_enqueue``、``i3c_ibi_work_enqueue_target_irq``、
``i3c_ibi_work_enqueue_hotjoin``、``i3c_ibi_work_enqueue_controller_request``、
``i3c_ibi_work_enqueue_cb``）
从
**ISR 上下文**
直接
调用
``sys_slist_get()``，
而
工作队列
处理程序
``i3c_ibi_work_handler()``
从
**工作队列线程**
用
``sys_slist_append()``
返回
节点，
两侧
均无
锁。

因为
``sys_slist_get()``
和
``sys_slist_append()``
既
非
原子
也
非
中断
安全，
在工作队列
线程
正在
追加
期间
触发的
IBI
中断
（或
``CONFIG_SMP``
下
真正
并行
访问）
在
共享
链表
上
竞态。
这
破坏
链表
链接：
节点
可能
被
交给
两个
消费者，
节点
可能
丢失，
或
头/尾
指针
可能
被
留下
不一致
使
``sys_slist_get()``
返回
过期
或
垃圾
指针。
在
双重
分发
案例
中
后续
``memcpy(ibi_node, ibi_work,
sizeof(*ibi_node))``
覆盖
仍
在
途
的
节点；
垃圾
指针
使
同一
``memcpy``
变成
越界
写入。

竞态
由
I3C
总线
流量
驱动——
IBI、
热加入
和
控制器
角色
请求
源自
总线
上
的
目标
设备，
且
I3C
支持
热加入
设备。
控制
板上
芯片
到
芯片
总线
上
I3C
外设
的
攻击者
可
生成
高频
中断
定时
与
释放
操作
碰撞。
利用
需要
总线
物理
访问
和
赢得
狭窄
定时
窗口；
最
现实
的
影响
是
崩溃
或
挂起
（拒绝
服务），
内存
破坏
可能
但
难以
控制。

修复
用
新
``ibi_work_alloc()``/``ibi_work_free()``
辅助
包装
所有
空闲链表
``sys_slist_get()``/``sys_slist_append()``
操作，
每个
由
``k_spinlock``
（``ibi_work_lock``）
保护，
跨
ISR
和
线程
上下文
关闭
竞态。

- `Zephyr 项目缺陷跟踪器 GHSA-gfj5-gcxv-9jqm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gfj5-gcxv-9jqm>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 110786 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/110786>`_

- `PR 113436 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113436>`_

- `PR 113437 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113437>`_

- `PR 117902 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/117902>`_

:cve:`2026-14368`
-----------------

Zephyr LwM2M JSON 字符串解析器中差一越界 NUL 写入

LwM2M JSON 内容格式化器的 ``get_string()``
（``subsys/net/lib/lwm2m/lwm2m_rw_json.c``）
将
解析的
JSON
字符串
复制到
调用者
提供的
缓冲区
并
NUL 终止
它。
长度
保护
使用
``if (string_length
> buflen)``，
它
接受
长度
恰好
为
``buflen``
的
字符串。
在
``memcpy()``
填满
整个
缓冲区
后，
``buf[string_length] = '\0'``
然后
在
缓冲区
末尾
之外
写入
一个
字节
（CWE-787）。

字符串值及其长度直接取自 LwM2M WRITE 期间
的
入站
CoAP
负载：
``do_write_op_json()``
解析
从
``coap_packet_get_payload()``
获得的
负载，
``get_string()``
从
``lwm2m_write_handler()``
（``subsys/net/lib/lwm2m/lwm2m_message_handling.c``
中的
``engine_get_string()``）
对
``LWM2M_RES_TYPE_STRING``
资源
调用。
目标
``buf``/``buflen``
是
资源
实例
的
固定
数据
缓冲区
（``res_inst->data_ptr``/``max_data_len``）
或
引擎
验证
缓冲区
（``msg->ctx->validate_buf``）。
因此
LwM2M
服务器
（客户端
的
DTLS
对端）
可以
写入
长度
等于
目标
缓冲区
大小
的
字符串
资源
值
并
强制
一个
字节
溢出。

溢出
是
常量
字节
``0x00``
的
单个
越界
写入
恰好
在
资源
或
验证
缓冲区
之后，
破坏
内存
中
的
相邻
字节。
它
不是
信息
泄露
且
写入
值
固定，
因此
不是
直接
代码
执行
原语，
但
它
可以
破坏
相邻
状态
（相邻
资源
值、
长度/标志
字段、
或
结构
字段）
并
导致
数据
损坏
或
崩溃。
触发
写入
是
确定性
的；
产生
的
影响
取决于
内存
布局。

修复
将
保护
改为
``string_length >= buflen``，
拒绝
精确
长度
案例
并
使
JSON
格式化器
与
其他
内容
格式化器
（``lwm2m_rw_plain_text.c``、``lwm2m_rw_oma_tlv.c``、``lwm2m_rw_senml_json.c``、
``lwm2m_rw_cbor.c``、``lwm2m_rw_senml_cbor.c``）
对齐，
后者
已
使用
正确
的
边界
检查。

- `Zephyr 项目缺陷跟踪器 GHSA-vg53-h6qq-xx7h
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vg53-h6qq-xx7h>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 112021 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112021>`_

- `PR 113446 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113446>`_

- `PR 113444 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113444>`_

- `PR 113519 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113519>`_

:cve:`2026-14696`
-----------------

以太网桥 RX 包泄漏使 RX 缓冲池耗尽导致拒绝服务

当
启用
以太网
桥接
（``CONFIG_NET_ETHERNET_BRIDGE``）
时，
``subsys/net/l2/ethernet/bridge/bridge_input.c``
中的
``eth_bridge_input_process()``
决定
每个
在
桥
成员
接口
上
接收
的
帧
如何
处理。
对于
必须
也
交付
给
本地
堆栈
的
帧，
代码
调用
``eth_bridge_handle_locally()``
并
返回
``NET_OK``。
该
辅助
函数
不
消费
包——
它
仅
调用
``bridge_iface_recv()``
（通过
``virtual_recv()``），
后者
返回
``NET_CONTINUE``
而
不
接管
``pkt``
的
所有权。

``NET_OK``
判决
然后
通过
``ethernet_recv()``
传播
到
``subsys/net/ip/net_core.c``
中的
``processing_data()``，
在那里
``NET_OK``
被
解释
为
"包
已
被
消费，
不要
释放
它"。
因为
没有
消费者
实际
接管
所有权，
RX
``net_pkt``
永远
不
被
返回
池
并
被
泄漏。
具体
可
复现
的
泄漏
发生
于
``CONFIG_NET_ETHERNET_FORWARD_UNRECOGNISED_ETHERTYPE``
设置
时
（``CONFIG_NET_SOCKETS_PACKET``
启用
时
默认
``y``）
其
EtherType
没有
注册
L3
处理程序
的
帧：
回退
L3
分派
不
覆盖
``NET_OK``
判决，
因此
``ethernet_recv()``
返回
``NET_OK``
且
缓冲区
永远
不
被
释放。

桥接
L2
段
上
的
任何
设备
都
可以
发出
携带
任意
EtherType
的
广播/多播
帧
而
无
认证。
每个
这样的
帧
永久
消费
有限
RX
池
（``CONFIG_NET_PKT_RX_COUNT``）
的
一个
缓冲区，
因此
短暂
的
广播
洪泛
耗尽
池
且
设备
再
也
无法
接收
流量
直到
重启——
持久
的
拒绝
服务。
没有
机密性
或
完整性
影响。

修复
使
``eth_bridge_handle_locally()``
传播
真实
``net_verdict``
并
对
本地
保留
的
帧
返回
``NET_CONTINUE``，
通过
新
``dst_iface``
输出
参数
将
桥
接口
写回
使
包
遵循
正常
接收
路径
并
恰好
被
取消引用
一次。

- `Zephyr 项目缺陷跟踪器 GHSA-3m4w-wc4v-766q
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3m4w-wc4v-766q>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 111931 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111931>`_

- `PR 113524 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113524>`_

:cve:`2026-14697`
-----------------

IPv6 邻居请求包泄漏导致 TX 池耗尽拒绝服务

``subsys/net/ip/ipv6_nbr.c``
中的
``net_ipv6_send_ns()``
为
邻居
请求
分配
一个
发送
``net_pkt``。
当
它
被
调用
时
有
数据
包
在
未
解析
邻居
上
等待
且
该
邻居
的
``pending_queue``
已
非空
（已
有
NS
在途），
函数
附加
数据
包
并
提前
返回
而
从未
通过
``net_send_data()``
发送
NS
或
用
``net_pkt_unref()``
释放
它。
新
分配
的
NS
``net_pkt``
及其
附加
TX
缓冲区
仅
由
本地
变量
持有
并
被
永久
泄漏，
永远
不
返回
``CONFIG_NET_PKT_TX_COUNT``
/
``CONFIG_NET_BUF_TX_COUNT``。

泄漏
分支
位于
正常
IPv6
发送
路径：
``net_ipv6_prepare_for_send()``
（从
``net_if.c``
调用）
对
任何
下一跳
尚
不
在
邻居
缓存
中
的
出站
或
转发
IPv6
包
调用
``net_ipv6_send_ns()``。
链路
上
（相邻）
攻击者
可以
通过
发送
一批
请求
包
（例如
ICMPv6
echo
请求
或
UDP
数据报）
确定性
地
驱动
它，
所有
都
伪造
单个
不
存在
的
链路
上
源
地址：
节点
为
每个
生成
应答，
第一个
应答
排队
一个
NS，
且
在
大约
三
秒
的
``INCOMPLETE``
解析
窗口
内
的
每个
后续
应答
都
取
泄漏
分支
并
丢失
一个
TX
包。
路由器
配置
的
节点
转发
攻击者
流量
到
不
存在
的
链路
上
主机
时
同样
泄漏。

因为
泄漏
的
包
永远
不
被
回收
且
``CONFIG_NET_PKT_TX_COUNT``
默认
仅
4
（以太网
14），
短暂
的
低
速率
突发
耗尽
TX
池。
一旦
耗尽
节点
再
也
无法
分配
任何
发送
包
且
无法
发送
TCP/UDP、
ARP/ND
或
任何
应答，
产生
完全
且
持久
的
网络
拒绝
服务
在
重启
前
不
自愈。
修复
在
提前
返回
前
用
``net_pkt_unref(pkt)``
释放
未
发送
的
NS
包。

- `Zephyr 项目缺陷跟踪器 GHSA-x956-p489-8mf5
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x956-p489-8mf5>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 112372 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112372>`_

- `PR 113655 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113655>`_

- `PR 113654 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113654>`_

:cve:`2026-14986`
-----------------

在 2026-09-04 之前处于保密期（embargo）

:cve:`2026-15460`
-----------------

Zephyr Bluetooth Classic L2CAP 接收路径中缺少通道状态验证

Bluetooth Classic（BR/EDR）L2CAP 接收处理程序
``bt_l2cap_br_recv()``
（``subsys/bluetooth/host/classic/l2cap_br.c``）
仅
基于
目标
通道
ID
分派
入站
数据
PDU，
而
不
检查
目标
通道
是否
已
达到
``BT_L2CAP_CONNECTED``
状态。
动态
通道
在
仍
处于
``BT_L2CAP_CONNECTING``
（以及
之后
``BT_L2CAP_CONFIG``）
时
被
分配
其
RX CID
并
添加
到
连接
的
通道
列表——
在
配置
完成
之前
且
对
需要
安全
的
PSM
在
对端
被
认证
之前
（``l2cap_br_conn_req()``）。

因为
通道
在此
窗口
内
已
可
被
``bt_l2cap_br_lookup_rx_cid()``
找到，
无线电
范围
内
的
远程
对端
可以
发送
地址
为
该
CID
的
数据
PDU
并
使其
在
尚未
建立
的
通道
上
被
处理。
分派
以
通道
字段
（``BR_CHAN(chan)->rx.mode``、``rx.mps``）
为
键，
这些
字段
仅
在
配置
期间
由
``l2cap_br_conf()``
初始化；
因为
通道
对象
是
池化
的
且
``bt_l2cap_br_chan_del()``
不
重置
``rx.mode``
或
重组
缓冲区
``_sdu``，
复用
的
通道
可以
携带
过期
状态
进入
``CONNECTING``
窗口
并
将
帧
路由
到
重传/流控
路径
（``bt_l2cap_br_ret_fc_recv()``）
携带
过期
参数
和
可能
过期
的
``_sdu``
指针。

影响
是
将
攻击者
数据
交付
给
半
打开
（且
可能
未
认证）
通道
上
的
上层
协议
处理程序，
加上
在
复用
通道
对象
上
对
过期
或
部分
初始化
的
通道
状态
操作——
导致
通道/链路
拆除
（拒绝
服务）
且
在
过期
``_sdu``
案例
中
悬空
指针
条件。
修复
添加
显式
``BR_CHAN(chan)->state < BT_L2CAP_CONNECTED``
保护
丢弃
通道
完全
连接
前
接收
的
任何
数据。

- `Zephyr 项目缺陷跟踪器 GHSA-hx89-rm6c-hjrh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hx89-rm6c-hjrh>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 112394 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112394>`_

- `PR 113700 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113700>`_

- `PR 113701 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113701>`_

- `PR 113710 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113710>`_

:cve:`2026-15461`
-----------------

Zephyr HL78xx GNSS NMEA 驱动中的类型混淆导致来自 GNSS 输入的野指针写入

Sierra Wireless HL78xx 调制解调器 GNSS 驱动
（``drivers/modem/hl78xx/``，
之后
``drivers/modem/vendor_standalone/hl78xx/``）
在
``struct hl78xx_gnss_data``
内
嵌入
通用
``struct
gnss_nmea0183_match_data match_data``。
通用
NMEA0183
匹配
辅助
（``drivers/gnss/gnss_nmea0183_match.c``）
要求
上下文
是
*第一个*
成员
因为
其
回调
将
``user_data``
直接
强制转换
为
``struct
gnss_nmea0183_match_data *``。
在
受
影响
的
发布
中
``match_data``
是
第二个
成员
（在
``const struct device *dev``
之后），
因此
它
位于
非
零
偏移
而
``gnss_nmea0183_match_init()``
在
正确
地址
初始化
它。
注册
的
NMEA
处理程序
反而
传递
整个
设备
数据
对象
（``data->devices.gnss->data``，
偏移
0），
产生
偏移
移位
的
类型
混淆
在
状态
被
初始化
的
位置
和
解析
回调
读取
和
写入
它的
位置
之间。


当
解析
来自
GNSS
接收器
的
NMEA
语句
时，
GGA/RMC
回调
将
解析
的
定位
数据
写入
结构
中
的
错误
位置，
且
GSV
回调
（``gnss_nmea0183_match_gsv_callback``，
在
``CONFIG_GNSS_SATELLITES``
下
活动）
从
错误
偏移
读取
其
``satellites``
指针
和
边界——
``struct hl78xx_gnss_data``
的
非
指针
字节——
然后
通过
该
虚假
指针
写入
解析
的
``struct gnss_satellite``
条目。
这是
通过
未
初始化/野
指针
的
写入
携带
垃圾
边界。

NMEA
处理程序
默认
注册
（``CONFIG_HL78XX_GNSS_SOURCE_NMEA``
是
默认
GNSS
源）
在
使用
HL78xx
GNSS
的
设备
上。
驱动
在
内核
上下文
运行
且
NMEA
数据
源自
GNSS
无线电
前端，
因此
能够
影响
GNSS
信号
的
一方
（例如
无线电
邻近
处
的
GNSS/GPS
欺骗）
可以
驱动
内核
侧
解析器
进入
故障
写入。
最
可能
的
影响
是
崩溃
（拒绝
服务）
因为
虚假
指针
解析
为
固定
的
接近
NULL
值，
在
无
MMU
目标
上
可能
有
相邻
内存
损坏。
机密性
不受
影响。
利用
需要
卫星
特性
被
启用
且
活动，
因此
攻击
复杂度
高。

- `Zephyr 项目缺陷跟踪器 GHSA-vvjg-6rg4-7235
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vvjg-6rg4-7235>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 112937 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112937>`_

- `PR 113705 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113705>`_

:cve:`2026-6682`
----------------

FatFs FAT32 卷挂载（mount_volume）中的整数溢出在 Zephyr 中产生攻击者控制的文件大小和越界访问

Zephyr
捆绑
ChaN 的
FatFs
（通过
``zephyrproject-rtos/fatfs``
west
模块）
作为
支撑
``subsys/fs/fat_fs.c``
的
FAT/exFAT
文件系统。
在
``mount_volume()``
（``modules/fs/fatfs/ff.c``）中，
FAT
区域
大小
被
计算
为
``fasize =
ld_32(BPB_FATSz32); ... fasize *= fs->n_fats;``——
无
溢出
检查
的
32
位
乘法。

设置
``BPB_FATSz32 = 0x80000001``
且
有
两个
FAT
的
构造
FAT32
卷
使
乘积
回绕
（到
``0x00000002``），
因此
计算
的
数据
区域
与
FAT
区域
重叠。
因为
乘法
前
值
被
保留
在
``fs->fsize``，
之后
的
合理性
检查
不
捕获
回绕。

能够
使
设备
挂载
这样
卷
的
攻击者
（恶意
SD
卡
或
USB
介质）
可以
在
重叠
区域
放置
伪造
目录
条目，
使
``f_stat()``/目录
读取
返回
攻击者
控制
的
文件
大小；
使用
该
大小
作为
长度
读取
文件
的
应用
代码
然后
溢出
其
缓冲区，
在
普通
文件
操作
期间
产生
堆
或
栈
基础
的
内存
损坏。

这是
核心
FAT32
代码
路径
无
编译时
门
（FAT12/16/32
总是
构建），
因此
默认
Zephyr
FatFs
配置
受
影响。
上游
FatFs
为
安全
目的
不
再
维护
（维护者
未
响应
runZero
或
JPCERT/CC），
因此
Zephyr
在
其
vendored
副本
中
携带
修复。
上游
跟踪
为
CVE-2026-6682。

- `Zephyr 项目缺陷跟踪器 GHSA-m537-wqw2-2wrj
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m537-wqw2-2wrj>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

:cve:`2026-6683`
----------------

FatFs exFAT 同步（sync_fs）中的除以零在构造 exFAT 卷上使 Zephyr 崩溃

Zephyr
捆绑
的
FatFs
（``zephyrproject-rtos/fatfs``）
在
``CONFIG_FS_FATFS_EXFAT``
启用
时
支持
exFAT。
在
``sync_fs()``（``modules/fs/fatfs/ff.c``）中
空闲
簇
簿记
除以
``(fs->n_fatent - 2)``。

簇
计数
从
exFAT
引导
区域
读取
为
``ncl = ld_32(BPB_NumClusEx)``
且
仅
针对
上限
（``> MAX_EXFAT``）
验证，
从不
针对
下限，
因此
``BPB_NumClusEx = 0``
的
构造
exFAT
卷
产生
``n_fatent = 2``
和
除数
零。

挂载
这样
卷
并
执行
任何
写入/同步
触发
除以
零
（SIGFPE
/
CPU
故障），
拒绝
服务。

缺陷
仅
在
exFAT
被
编译
时
存在，
这
不是
默认
Zephyr
配置；
启用
exFAT
且
挂载
不可信
可移动
介质
的
设备
暴露。
上游
FatFs
为
安全
不
再
维护，
因此
Zephyr
在
其
vendored
副本
中
携带
修复。
上游
跟踪
为
CVE-2026-6683。

- `Zephyr 项目缺陷跟踪器 GHSA-c5j5-mrhx-hjg4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c5j5-mrhx-hjg4>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

:cve:`2026-6685`
----------------

FatFs 脏扇区缓存（f_read/f_write）中的整数下溢在 Zephyr 中构造碎片介质上导致错误扇区 I/O

在
FatFs
的
读取/写入
路径
（``modules/fs/fatfs/ff.c``
中的
``f_read``/``f_write``）中，
脏
扇区
缓存
重新填充
决定
用
无符号
算术
将
``fp->sect - sect``
与
运行
长度
``cc``
比较。
在
分片
FAT
布局
中
之后
的
簇
映射
到
比
当前
缓存
的
更
低
的
绝对
扇区
时，
减法
下溢
（回绕
到
大
无符号
值），
因此
决定
缓存
窗口
是否
与
请求
范围
重叠
的
保护
被
错误
评估。

结果
是
FatFs
刷新
或
复用
错误
的
缓存
扇区，
从
错误
的
磁盘
位置
读取
或
写入
文件
数据——
跨
文件
数据
损坏
和
无关
文件
内容
的
潜在
泄露，
以及
普通
文件
操作
期间
越界
行为
的
路径。

故意
分片
簇
链
的
构造
卷
（攻击者
控制
的
可移动
介质）
触发
条件。
这在
默认
读取/写入
路径
上
（无
exFAT
或
LFN
门控）。
上游
FatFs
为
安全
不
再
维护，
因此
Zephyr
在
其
vendored
副本
中
携带
修复。
上游
跟踪
为
CVE-2026-6685。

- `Zephyr 项目缺陷跟踪器 GHSA-rg3p-32gq-hqw3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rg3p-32gq-hqw3>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

:cve:`2026-6686`
----------------

FatFs f_lseek 越过文件末尾在 Zephyr 中暴露未初始化/过期簇内容（已删除文件数据）

在
FatFs
（``modules/fs/fatfs/ff.c``
中的
``f_lseek``）中，
将
为
写入
打开
的
文件
寻址
到
其
当前
末尾
之后
的
偏移
通过
``create_chain()``
扩展
簇
链
但
不
将
新
分配
的
簇
清零。

FatFs
将
文件
标记
为
更
大
而
不
初始化
支撑
扇区，
因此
之后
读取
增长
区域
返回
之前
在
那些
簇
上
的
任何
内容——
通常
是
已
删除
文件
的
残余
内容。
在
较低
权限
或
之后
参与者
可以
读取
这样
扩展
的
文件
的
设备
上，
之前
已
删除
或
无关
文件
数据
被
泄露
（CWE-908，
未
初始化
资源
的
使用）。
无
内存
安全
损坏；
影响
是
介质
上
数据
的
机密性。

缺陷
在
默认
写入
路径
上
（无
exFAT/LFN
门控）。
上游
FatFs
为
安全
不
再
维护，
因此
Zephyr
在
其
vendored
副本
中
携带
修复。
上游
跟踪
为
CVE-2026-6686。

- `Zephyr 项目缺陷跟踪器 GHSA-rjhg-f2h7-rffm
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rjhg-f2h7-rffm>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

:cve:`2026-6687`
----------------

FatFs exFAT 卷标签读取（f_getlabel）中的栈缓冲区溢出在 Zephyr 中通过未验证的磁盘长度

在
FatFs
的
``f_getlabel()``（``modules/fs/fatfs/ff.c``）中，
exFAT
卷
标签
复制
循环
由
原始
磁盘
字节
``dj.dir[XDIR_NumLabel]``（0–255）
而非
规范
最大
11
个
字符
限定。

将
``XDIR_NumLabel``
设置
为
大
值
（例如
128）
的
构造
exFAT
卷
使
循环
在
32
字节
目录
条目
之后
读取
标签
字符
并
将
最多
该
数量
的
UTF
解码
字符
写入
调用者
提供
的
``label[]``
缓冲区，
溢出
栈
上
典型
固定
大小
标签
数组
（例如
``char label[12]``/``label[24]``）——
可能
有
控制流
影响
的
内存
损坏。

在
Zephyr
中
这
仅
在
下游
应用
中
可
到达：
``f_getlabel``
仅
用
``CONFIG_FS_FATFS_EXTRA_NATIVE_API=y``
编译，
exFAT
必须
启用，
且
树内
Zephyr
代码
不
调用
它
（应用
代码
提供
缓冲区）。
它
仍
是
vendored
库
中
的
真实
缺陷，
且
因为
上游
FatFs
为
安全
不
再
维护
Zephyr
在
其
vendored
副本
中
携带
修复
（限制
标签
长度）
使
选择
加入
的
应用
受
保护。
上游
跟踪
为
CVE-2026-6687。

- `Zephyr 项目缺陷跟踪器 GHSA-fxw6-w668-cgfh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fxw6-w668-cgfh>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

:cve:`2026-15890`
-----------------

在 2026-09-21 之前处于保密期（embargo）

:cve:`2026-15891`
-----------------

Zephyr MQTT-SN 客户端在移除无响应网关时的空指针解引用

MQTT-SN
客户端
保活
处理程序
``process_ping()``
（``subsys/net/lib/mqtt_sn/mqtt_sn.c``）
在
``PINGREQ``
重试
耗尽
后
移除
网关
记录。
它
调用
``SYS_SLIST_PEEK_HEAD_CONTAINER(&client->gateways, gw,
next)``
但
丢弃
结果。
该
宏
是
纯
表达式
不
赋值
给
``gw``，
因此
``gw``
无论
列表
内容
如何
都
保留
其
``NULL``
初始化器。

代码
然后
解引用
NULL
``gw``（``gw->gw_id``）
并
将其
传给
``mqtt_sn_gw_destroy()``，
到达
``k_mem_slab_free(&gateways, NULL)``。
启用
``CONFIG_MEM_SLAB_POINTER_VALIDATE``
时
这
触发
``k_panic()``；
在
默认
配置
中
它
通过
NULL
指针
执行
写入
（``*(char **)mem =
slab->free_list;``）
并
破坏
slab
空闲
列表。
结果
是
崩溃/内核
恐慌
或
在
地址
0
可
写
的
目标
上
静默
的
内存
分配器
损坏。

脆弱
分支
在
已
连接
的
MQTT-SN
网关
未
在
配置
的
重试
次数
内
应答
保活
``PINGREQ``
时
运行。
此
条件
由
远程
对端
控制：
恶意
或
被
入侵
的
网关，
或
将
自己
通告
为
网关
然后
停止
响应
（或
黑洞
真实
网关
的
``PINGRESP``）
的
在
路径/相邻
攻击者，
使
客户端
进入
缺陷。
MQTT-SN
在
UDP
上
运行
且
不
需要
认证。

影响
是
受
影响
MQTT-SN
客户端
的
可
远程
触发
的
拒绝
服务
（可用性）；
无
攻击者
控制
的
数据
被
写入。
姊妹
移除器

``process_advertise()`` 使用 ``SYS_SLIST_FOR_EACH_CONTAINER_SAFE`` 且不受影响。
修复将宏的返回值赋值给 ``gw``。

- `Zephyr 项目缺陷跟踪器 GHSA-c4g8-4f9p-4746
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c4g8-4f9p-4746>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 113142 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113142>`_

- `PR 113718 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113718>`_

- `PR 113723 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113723>`_

:cve:`2026-15892`
-----------------

mcumgr 设置管理处理程序在访问钩子拒绝时的堆内存泄漏导致拒绝服务

mcumgr SMP 设置管理组处理程序 ``settings_mgmt_read()``、
``settings_mgmt_write()`` 和 ``settings_mgmt_delete()``
（``subsys/mgmt/mcumgr/grp/settings_mgmt/src/settings_mgmt.c``）
在
``CONFIG_MCUMGR_GRP_SETTINGS_BUFFER_TYPE_HEAP``
启用
时
通过
``k_malloc()``
分配
``key_name``
缓冲区
（以及
对
读取
的
``data``
缓冲区），
依赖
``end:``
标签
``k_free()``
它们。
当
``CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK``
也
启用
且
应用
访问
钩子
通过
返回
状态
``MGMT_CB_ERROR_RC``
拒绝
请求
时，
处理程序
直接
执行
``return ret_rc;``，
绕过
``end:``
且
在
每个
被
拒绝
的
请求
上
泄漏
堆
分配。

设置
处理程序
可
通过
未
认证
的
SMP
传输
（Bluetooth
LE、
UART、
或
UDP，
取决于
产品
配置）
到达。
访问
钩子
是
应用
用来
拒绝
未
授权
设置
访问
的
机制，
且
``MGMT_CB_ERROR_RC``
是
常见
的
拒绝
风格，
因此
能够
发送
钩子
拒绝
的
``settings
read``/``write``/``delete``
命令
的
攻击者
在
每次
尝试
时
触发
堆
泄漏。

因为
泄漏
的
内存
在
重启
前
永远
不
被
回收，
持续
的
被
拒绝
请求
流
单调
耗尽
内核
堆
直到
``k_malloc()``
失败，
拒绝
mcumgr
服务
且
影响
设备
上
任何
其他
堆
消费者——
拒绝
服务。
影响
仅
为
可用性；
无
内存
损坏
或
信息
披露。
仅
选择
堆
缓冲区
类型、
启用
访问
钩子、
且
注册
返回
``MGMT_CB_ERROR_RC``
的
钩子
的
配置
受
影响
（默认
栈
缓冲区
类型
无法
泄漏）。

- `Zephyr 项目缺陷跟踪器 GHSA-rq68-wgv4-hcq3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rq68-wgv4-hcq3>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 113178 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113178>`_

- `PR 113507 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113507>`_

- `PR 113506 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113506>`_

- `PR 113505 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113505>`_

:cve:`2026-15893`
-----------------

Zephyr IPv6 邻居发现中来自构造路由器通告的零可达时间导致断言/拒绝服务

``subsys/net/ip/net_if.c`` 中的
``net_if_ipv6_calc_reachable_time()``
从
``ipv6->base_reachable_time``
推导
随机化
ND
可达
时间
为
``min_reachable +
sys_rand32_get() % (max_reachable - min_reachable)``，
其中
``min_reachable = base/2``
且
``max_reachable = 3*base/2``
使用
整数
除法。
当
``base_reachable_time``
为
``1``
时，
``min_reachable``
和
模数
都
坍缩
使
函数
返回
``0``，
且
``net_if_ipv6_set_reachable_time()``
将
该
``0``
存储
到
``ipv6->reachable_time``。

``base_reachable_time``
是
攻击者
控制
的：
``subsys/net/ip/ipv6_nbr.c``
中的
``handle_ra_input()``
接受
RA
中
的
``ReachableTime``
字段
并
直接
存储
它
而
不
验证
它
非
零。
发送
``ReachableTime = 1``
的
路由器的
相邻
攻击者
（或
在
路径
上
的
攻击者
修改
真实
RA）
使
节点
将
可达
时间
设为
零。

之后
任何
触发
``net_if_ipv6_set_reachable_time()``
的
事件
（例如
接口
状态
变化
或
新
RA）
在
``min_reachable +
sys_rand32_get() % (max_reachable - min_reachable)``
中
除以
零
（``max_reachable - min_reachable = 0``），
在
启用
``CONFIG_ASSERT``
时
触发
``__ASSERT``，
或
在
断言
被
编译
掉
时
产生
未
定义
行为
（通常
崩溃
或
错误
的
可达
时间）。
结果
是
拒绝
服务
（崩溃）
或
邻居
发现
行为
错误
（错误
的
可达
时间
导致
过度
或
不足
的
邻居
请求
速率）。

修复
在
``handle_ra_input()``
中
添加
``if (ra->reachable_time == 0) { return; }``
保护
拒绝
零
值
且
在
``net_if_ipv6_calc_reachable_time()``
中
添加
``if (max_reachable <= min_reachable) { return; }``
保护。

- `Zephyr 项目缺陷跟踪器 GHSA-8v32-9xf8-r765
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8v32-9xf8-r765>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 113226 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113226>`_

- `PR 113605 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113605>`_

- `PR 113686 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113686>`_

- `PR 113687 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113687>`_

:cve:`2026-15894`
-----------------

在 2026-10-06 之前处于保密期（embargo）

:cve:`2026-15923`
-----------------

Zephyr mbedTLS TLS 客户端会话缓存中的竞态条件导致释放后使用

``subsys/net/lib/mbedtls/mbedtls_client.c`` 中的
TLS
客户端
会话
缓存
（``client_cache``）
在
无
锁
的
情况下
被
多个
线程
并发
访问。
``mbedtls_client_session_cache_get()``
和
``mbedtls_client_session_cache_put()``
直接
操作
``client_cache``
链表
而
不
获取
任何
互斥
锁，
而
``mbedtls_client_session_cache_free()``
遍历
链表
并
释放
每个
会话
也
无
锁。

在
多线程
应用
中
运行
并发
TLS
客户端
连接
时，
一个
线程
可以
在
另一个
线程
释放
会话
时
持有
会话
指针
并
继续
使用
它
（释放后使用），
或
两个
线程
可以
同时
插入/移除
相同
的
会话
导致
链表
损坏
或
双重
释放。

利用
需要
选择
加入
每
套接字
客户端
会话
缓存
的
应用
（``TLS_SESSION_CACHE``
套接字
选项，
默认
关闭）
且
在
多个
线程
上
运行
并发
TLS
客户端
连接；
打开
窗口
的
定时
由
远程
对端
影响，
因此
恶意
或
被
入侵
的
服务器
可以
提高
会话
票据
频率
以
加宽
它。
可
可靠
演示
的
影响
是
导致
崩溃
或
堆
损坏
（拒绝
服务）
的
内存
损坏。
修复
添加
专用
``session_cache_lock``
互斥
锁
在
每个
``client_cache``
访问者
上
获取，
序列化
所有
读取
和
释放
并
关闭
竞态。

- `Zephyr 项目缺陷跟踪器 GHSA-4pvm-wrcp-jjf5
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4pvm-wrcp-jjf5>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 112628 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/112628>`_

- `PR 113730 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113730>`_

- `PR 113731 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113731>`_

- `PR 113732 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113732>`_:cve:`2026-15924`
-----------------

Zephyr sockets 中 TLS 客户端会话缓存的未同步并发访问导致释放后使用/双重释放

Zephyr
的
TLS
套接字
层
（``subsys/net/lib/sockets/sockets_tls.c``）
保持
单个
进程
全局
数组
``client_cache``
的
缓存
客户端
会话，
由
每个
TLS
套接字
上下文
共享。
修改
和
读取
它的
函数——
``tls_session_save()``、``tls_session_get()``、``tls_session_cache_reset()``
和
设置
恢复
处理程序——
分配、
释放
和
解引用
每个
条目
的
堆
缓冲区
（``entry->session``）。
修复
前
这些
访问
仅
由
*每
套接字*
上下文
互斥
锁
``ctx->lock``
（在
``ctx_set_lock()``
中
每
套接字
分配）
序列化，
它
在
不同
套接字
触及
共享
缓存
之间
不提供
任何
互斥。

因为
``CONFIG_NET_SOCKETS_TLS_MAX_CLIENT_SESSION_COUNT``
默认
为
``1``，
任何
两个
并发
客户端
套接字
竞争
同一
槽。
在
``tls_session_get()``
中
读取
``entry->session``
的
线程
（在
``mbedtls_ssl_session_load()``
内）
可以
与
另一个
在
``tls_session_save()``
中
选择
同一
条目
复用
并
在
重新
分配
前
执行
``mbedtls_free(entry->session)``
的
线程
并发
运行——
释放后
使用
读取，
且
当
两个
保存
驱逐
同一
条目
时
双重
释放。
两者
都
破坏
mbedTLS
堆。
缓存
在
普通
客户端
路径
上
到达：
在
连接
时
通过
``tls_session_store()``/``tls_session_restore()``，
且
（在
``main``
上）
每当
TLS
1.3
会话
票据
在
``recv()``/``poll()``
期间
到达
时
通过
``tls_session_store_current()``。

利用
需要
选择
加入
每
套接字
客户端
会话
缓存
的
应用
（``TLS_SESSION_CACHE``
套接字
选项，
默认
关闭）
且
在
多个
线程
上
运行
并发
TLS
客户端
连接；
打开
窗口
的
定时
由
远程
对端
影响，
因此
恶意
或
被
入侵
的
服务器
可以
提高
会话
票据
频率
以
加宽
它。
可
可靠
演示
的
影响
是
导致
崩溃
或
堆
损坏
（拒绝
服务）
的
内存
损坏。
修复
添加
专用
``session_cache_lock``
互斥
锁
在
每个
``client_cache``
访问者
上
获取，
序列化
所有
读取
和
释放
并
关闭
竞态。

- `Zephyr 项目缺陷跟踪器 GHSA-wcgm-pq6x-v2gf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wcgm-pq6x-v2gf>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 113405 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113405>`_

- `PR 113736 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113736>`_

- `PR 113737 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113737>`_

- `PR 113738 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113738>`_
:cve:`2026-16147`
-----------------

it82xx2 USB 设备控制器提交不完整的 OUT 传输缓冲区，导致释放后使用和事件列表损坏

ITE IT82xx2 USB 设备控制器驱动（``drivers/usb/udc/udc_it82xx2.c``）
错误处理
非
控制
端点
上
的
多
包
OUT
传输。
在
``work_handler_out()``
中，
活动
传输
缓冲区
用
``udc_buf_peek()``
获取
（它
不
出队
它）；
当
完整
的
最大
包
大小
包
到达
但
缓冲区
仍
有
尾
空间
（传输
尚未
完成），
修复
前
的
代码
既
重新
武装
端点
通过
``work_handler_xfer_continue()``
继续
填充
同一
``buf``，
又
同时
通过
``udc_submit_ep_event()``
将
同一
仍
在
填充
的
缓冲区
交给
上层
堆栈。

因为
``udc_submit_ep_event()``
将
缓冲区
所有权
转移
给
USB
设备
堆栈
（``usbd_event_carrier()``
将
``&buf->node``
追加
到
``uds_ctx->ep_events``，
之后
类
处理程序
处理
并
``net_buf_unref()``
它），
驱动
继续
将
后续
主机
控制
的
OUT
包
DMA
到
上层
堆栈
可能
已经
释放
并
回收
的
缓冲区——
释放后
使用
写入。
此外，
因为
缓冲区
从未
被
出队，
完成
的
包
对
同一
对象
执行
``udc_buf_get()``
并
第二次
提交
它，
将
``&buf->node``
追加
到
事件
slist
两次
（单
链表
损坏）
并
导致
双重
``net_buf_unref()``。

IT82xx2
是
USB
外设
控制器，
因此
不可信
的
USB
主机
控制
OUT
传输
的
分
包
且
可以
对
任何
排队
缓冲区
超过
一个
包
的
非
控制
OUT
端点
强制
此
路径——
普通
的
批量/中断
模式。
驱动
和
USB
设备
堆栈
在
外部
主机
之上
的
内核
上下文
运行，
给
主机
一个
设备侧
内核
堆
损坏
原语：
可靠
的
拒绝
服务
且
因为
写入
的
字节
是
攻击者
控制
的，
可能
的
相邻
``net_buf``
池
内存
损坏。
攻击
向量
是
物理
的
（USB
连接）。
修复
延迟
提交
直到
缓冲区
完全
填充
并
让
``xfer_work_handler()``
驱动
继续，
使
每个
OUT
缓冲区
恰好
被
提交
给
上层
堆栈
一次。

- `Zephyr 项目缺陷跟踪器 GHSA-3q4g-7w6j-8qfp
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3q4g-7w6j-8qfp>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 113463 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113463>`_

- `PR 113847 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113847>`_

- `PR 113850 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113850>`_

- `PR 113849 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113849>`_

:cve:`2026-16148`
-----------------

it82xx2 USB 设备控制器驱动中通过重新初始化忙碌的可延迟工作项导致内核恐慌

ITE it82xx2 USB 设备控制器驱动在
``it82xx2_enable()``（驱动的 ``.enable`` 操作）
（``drivers/usb/udc/udc_it82xx2.c``）中
用
``k_work_init_delayable(&priv->suspended_work, suspended_handler)``
初始化
其
总线
挂起
检测
工作。
此
工作
项
在
USB
总线
活动
时
基本
持续
调度：
中断
处理程序
在
每个
SOF
帧
上
重新
调度
它
且
``suspended_handler()``
重新
调度
自己，
因此
其
超时
节点
通常
链接
在
内核
超时
列表
/
工作
队列
待
处理
队列
中。

``k_work_init_delayable()``（``kernel/work.c``）
无条件
覆盖
整个
``k_work_delayable``
结构，
包括
其
超时
和
队列
链接，
无
忙碌
检查。
因为
``it82xx2_disable()``
不
取消
工作，
正常
的
禁用
然后
启用
循环
重新
运行
``api->enable()``
（``udc_enable()``
仅
拒绝
冗余
的
启用，
不
拒绝
禁用
后
的
重新
启用）
并
原地
重新
初始化
仍
待
处理
的
工作，
破坏
内核
超时/工作
队列
链接
列表
并
导致
内核
恐慌。

外部
USB
主机——
例如
执行
USB
DFU
分离
（``dfu-util
--detach``）
或
强制
重复
连接/复位/重新
枚举
的
主机——
驱动
``udc_disable()``/``udc_enable()``
转换
且
控制
挂起/恢复
定时，
因此
它
可以
安排
挂起
工作
在
重新
启用
期间
待
处理。
这
产生
未
认证
的
拒绝
服务
（内核
恐慌）
可
通过
USB
边界
从
可
移除、
物理
连接
的
主机
到达，
无
机密性
或
完整性
影响
被
演示。

修复
将
``k_work_init_delayable()``
调用
移
到
一次性
preinit
函数
使
工作
恰好
被
初始化
一次，
消除
对
使用中
项
的
重新
初始化。

- `Zephyr 项目缺陷跟踪器 GHSA-fvp9-j2pq-477x
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fvp9-j2pq-477x>`_

该问题已在 main 分支修复，将随 v4.5.0 发布

- `PR 113463 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113463>`_

- `PR 113847 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113847>`_

- `PR 113850 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113850>`_

- `PR 113849 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/113849>`_

:cve:`2026-16511`
-----------------

在 2026-11-02 之前处于保密期（embargo）

:cve:`2026-16512`
-----------------

在 2026-09-18 之前处于保密期（embargo）

:cve:`2026-16513`
-----------------

在 2026-09-25 之前处于保密期（embargo）

:cve:`2026-16514`
-----------------

在 2026-09-18 之前处于保密期（embargo）

:cve:`2026-16515`
-----------------

在 2026-09-18 之前处于保密期（embargo）

:cve:`2026-17050`
-----------------

在 2026-09-19 之前处于保密期（embargo）

:cve:`2026-17051`
-----------------

在 2026-09-20 之前处于保密期（embargo）

:cve:`2026-17052`
-----------------

在 2026-09-20 之前处于保密期（embargo）

:cve:`2026-17053`
-----------------

在 2026-09-20 之前处于保密期（embargo）

:cve:`2026-17054`
-----------------

在 2026-09-21 之前处于保密期（embargo）

:cve:`2026-2411`
----------------

Bluetooth GATT notify/indicate 强制执行错误属性的权限，绕过特征值上的加密/认证要求

Zephyr 的 Bluetooth 主机将 GATT 特征声明为两个连续属性：
Characteristic Declaration，其权限硬编码为 ``BT_GATT_PERM_READ``，
以及
Characteristic Value 属性，携带应用指定的安全
权限（例如 ``BT_GATT_PERM_READ_ENCRYPT`` / ``READ_AUTHEN`` / ``READ_LESC``）。
公共
notify
和
indicate
API
显式
接受
任一
属性，
且
传递
声明
是
文档
中
的
常见
惯用法。
在
发送
每个
通知
或
指示
之前，
主机
用
``bt_gatt_check_perm()``
对
``gatt_notify()``、``gatt_indicate()``
和
``gatt_notify_multiple_verify_params()``
（``subsys/bluetooth/host/gatt.c``）中
的
``params->attr``
重新
检查
链路
安全。

当
应用
传递
Characteristic
Declaration
属性
时，
主机
正确
重定向
值
句柄
但
留下
``params->attr``
指向
声明，
因此
安全
检查
评估
声明
的
权限
（无
安全
要求）
而非
值
的。
结果
是
配置
在
特征
值
上
的
加密/认证/LESC
要求
被
跳过。
Notify-Multiple
路径
额外
使用
省略
LE
Secure
Connections
要求
的
掩码。

远程
对端
通过
连接
（可选
无
配对
或
加密）
并
写入
Client
Characteristic
Configuration
描述符
以
启用
通知
或
指示
触发
泄露，
使
服务器
在
尚未
达到
所需
安全
级别
的
链路
上
发出
受
保护
的
值。
影响
是
应用
意图
仅
通过
受
保护
的
链路
暴露
的
特征
值
的
信息
披露
/
访问
控制
绕过；
暴露
取决于
应用
声明
加密/认证
要求
的
notify/indicate
特征
且
CCC
在
较低
安全
层
可
写。
无
内存
安全
或
可用性
影响。

修复
添加
``bt_gatt_attr_resolve_value()``，
在
权限
检查
之前
将
声明
属性
映射
到
后续
的
值
属性，
且
将
Notify-Multiple
路径
切换
到
完整
的
``BT_GATT_PERM_READ_ENCRYPT_MASK``
使
LESC
要求
也
被
强制
执行。

- `Zephyr 项目缺陷跟踪器 GHSA-4w3r-v9q9-4462
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4w3r-v9q9-4462>`_

该问题已在 main 分支修复，将随 v4.5.0 发布


- `PR 108371 main 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/108371>`_

- `PR 111535 v4.4 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111535>`_

- `PR 111536 v4.3 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111536>`_

- `PR 111620 v3.7 分支修复
  <https://github.com/zephyrproject-rtos/zephyr/pull/111620>`_

:cve:`2026-18413`
-----------------

在 2026-09-26 之前处于保密期（embargo）

:cve:`2026-18414`
-----------------

在 2026-09-26 之前处于保密期（embargo）

:cve:`2026-18415`
-----------------

在 2026-09-26 之前处于保密期（embargo）

:cve:`2026-18416`
-----------------

在 2026-09-26 之前处于保密期（embargo）

:cve:`2026-18417`
-----------------

在 2026-09-27 之前处于保密期（embargo）

:cve:`2026-18418`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-18746`
-----------------

在 2026-09-28 之前处于保密期（embargo）

:cve:`2026-18747`
-----------------

在 2026-09-28 之前处于保密期（embargo）

:cve:`2026-18748`
-----------------

在 2026-10-20 之前处于保密期（embargo）

:cve:`2026-19184`
-----------------

在 2026-10-04 之前处于保密期（embargo）

:cve:`2026-19185`
-----------------

在 2026-10-04 之前处于保密期（embargo）

:cve:`2026-19186`
-----------------

在 2026-10-07 之前处于保密期（embargo）

:cve:`2026-19569`
-----------------

在 2026-10-09 之前处于保密期（embargo）

:cve:`2026-19570`
-----------------

在 2026-10-09 之前处于保密期（embargo）

:cve:`2026-19571`
-----------------

在 2026-10-09 之前处于保密期（embargo）

:cve:`2026-19574`
-----------------

在 2026-10-09 之前处于保密期（embargo）

:cve:`2026-19575`
-----------------

在 2026-10-09 之前处于保密期（embargo）

:cve:`2026-19576`
-----------------

在 2026-10-10 之前处于保密期（embargo）

:cve:`2026-19577`
-----------------

在 2026-10-10 之前处于保密期（embargo）

:cve:`2026-19595`
-----------------

在 2026-10-18 之前处于保密期（embargo）

:cve:`2026-19669`
-----------------

在 2026-10-10 之前处于保密期（embargo）

:cve:`2026-19673`
-----------------

在 2026-10-14 之前处于保密期（embargo）

:cve:`2026-19676`
-----------------

在 2026-10-17 之前处于保密期（embargo）

:cve:`2026-19735`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-19736`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-19737`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-19738`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-19739`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-19740`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-19741`
-----------------

在 2026-10-22 之前处于保密期（embargo）

:cve:`2026-19742`
-----------------

在 2026-10-25 之前处于保密期（embargo）

:cve:`2026-19809`
-----------------

在 2026-10-19 之前处于保密期（embargo）

:cve:`2026-19935`
-----------------

在 2026-10-11 之前处于保密期（embargo）

:cve:`2026-19936`
-----------------

在 2026-10-12 之前处于保密期（embargo）

:cve:`2026-19937`
-----------------

在 2026-10-12 之前处于保密期（embargo）

:cve:`2026-19938`
-----------------

在 2026-10-12 之前处于保密期（embargo）

:cve:`2026-19939`
-----------------

在 2026-10-13 之前处于保密期（embargo）

:cve:`2026-19940`
-----------------


在 2026-10-13 之前处于保密期（embargo）

:cve:`2026-19947`
-----------------

在 2026-10-21 之前处于保密期（embargo）

:cve:`2026-75083`
-----------------

在 2026-10-14 之前处于保密期（embargo）

:cve:`2026-75084`
-----------------

在 2026-10-14 之前处于保密期（embargo）

:cve:`2026-75085`
-----------------

在 2026-10-14 之前处于保密期（embargo）

:cve:`2026-76787`
-----------------

在 2026-10-16 之前处于保密期（embargo）

:cve:`2026-76788`
-----------------

在 2026-10-16 之前处于保密期（embargo）

:cve:`2026-77684`
-----------------

在 2026-10-18 之前处于保密期（embargo）

:cve:`2026-77685`
-----------------

在 2026-10-18 之前处于保密期（embargo）

:cve:`2026-78116`
-----------------

在 2026-10-20 之前处于保密期（embargo）

:cve:`2026-78117`
-----------------

在 2026-10-20 之前处于保密期（embargo）

:cve:`2026-78118`
-----------------

在 2026-10-20 之前处于保密期（embargo）

:cve:`2026-78119`
-----------------

在 2026-10-20 之前处于保密期（embargo）

:cve:`2026-79976`
-----------------

在 2026-10-21 之前处于保密期（embargo）

:cve:`2026-79977`
-----------------

在 2026-10-22 之前处于保密期（embargo）

:cve:`2026-79978`
-----------------

在 2026-10-23 之前处于保密期（embargo）

:cve:`2026-79979`
-----------------

在 2026-10-23 之前处于保密期（embargo）

:cve:`2026-79980`
-----------------

在 2026-10-23 之前处于保密期（embargo）

:cve:`2026-79981`
-----------------

在 2026-10-23 之前处于保密期（embargo）

:cve:`2026-79982`
-----------------

在 2026-10-23 之前处于保密期（embargo）

:cve:`2026-81038`
-----------------

在 2026-10-24 之前处于保密期（embargo）

:cve:`2026-81039`
-----------------

在 2026-10-24 之前处于保密期（embargo）

:cve:`2026-82388`
-----------------

在 2026-10-26 之前处于保密期（embargo）

:cve:`2026-82389`
-----------------

在 2026-10-26 之前处于保密期（embargo）

:cve:`2026-82390`
-----------------

在 2026-10-26 之前处于保密期（embargo）

:cve:`2026-82391`
-----------------

在 2026-10-26 之前处于保密期（embargo）

:cve:`2026-82961`
-----------------

在 2026-10-27 之前处于保密期（embargo）

:cve:`2026-82962`
-----------------

在 2026-10-27 之前处于保密期（embargo）

:cve:`2026-85032`
-----------------

在 2026-10-30 之前处于保密期（embargo）

:cve:`2026-85033`
-----------------

在 2026-10-31 之前处于保密期（embargo）

:cve:`2026-85034`
-----------------

在 2026-10-31 之前处于保密期（embargo）

:cve:`2026-85035`
-----------------

在 2026-10-31 之前处于保密期（embargo）

:cve:`2026-85036`
-----------------

在 2026-10-31 之前处于保密期（embargo）

:cve:`2026-86086`
-----------------

在 2026-12-01 之前处于保密期（embargo）

:cve:`2026-86092`
-----------------

在 2026-12-03 之前处于保密期（embargo）

:cve:`2026-87038`
-----------------

在 2026-11-02 之前处于保密期（embargo）

:cve:`2026-87039`
-----------------

在 2026-11-02 之前处于保密期（embargo）

:cve:`2026-87040`
-----------------

在 2026-11-02 之前处于保密期（embargo）

:cve:`2026-87041`
-----------------

在 2026-11-02 之前处于保密期（embargo）

:cve:`2026-87042`
-----------------

在 2026-11-03 之前处于保密期（embargo）

:cve:`2026-87043`
-----------------

在 2026-11-03 之前处于保密期（embargo）

:cve:`2026-87044`
-----------------

在 2026-11-03 之前处于保密期（embargo）

:cve:`2026-87045`
-----------------

在 2026-11-06 之前处于保密期（embargo）

:cve:`2026-90585`
-----------------

在 2026-11-07 之前处于保密期（embargo）

:cve:`2026-90586`
-----------------

在 2026-11-08 之前处于保密期（embargo）

:cve:`2026-90587`
-----------------

在 2026-11-08 之前处于保密期（embargo）

:cve:`2026-90588`
-----------------

在 2026-11-08 之前处于保密期（embargo）

:cve:`2026-90589`
-----------------

在 2026-11-08 之前处于保密期（embargo）

:cve:`2026-90590`
-----------------

在 2026-11-09 之前处于保密期（embargo）

:cve:`2026-90591`
-----------------

在 2026-11-09 之前处于保密期（embargo）

:cve:`2026-90832`
-----------------

在 2026-11-10 之前处于保密期（embargo）

:cve:`2026-90833`
-----------------

在 2026-11-10 之前处于保密期（embargo）

:cve:`2026-90834`
-----------------

在 2026-11-10 之前处于保密期（embargo）

:cve:`2026-91007`
-----------------

在 2026-11-12 之前处于保密期（embargo）