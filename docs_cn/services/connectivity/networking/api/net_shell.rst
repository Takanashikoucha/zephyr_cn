.. _net_shell:

Network Shell
#############

Network shell 及其伴生 shells 提供 helpers 以查明 network status（启用/禁用 features（并发出如 ping 或 DNS resolving 的命令。注意 ``net-shell`` 可能不应在生产代码中使用（其将需要额外 memory。详细 shell 信息参见 :ref:`generic shell <shell_api>`。

注意默认启用或禁用的 net-shell commands 均对 user 可用。这帮助 user 发现哪些 commands 可用以及如何启用它们。此额外 help 可通过禁用 :kconfig:option:`CONFIG_NET_SHELL_SHOW_DISABLED_COMMANDS` option 关闭。

以下 net-shell commands 已实现：

.. csv-table:: net-shell commands
   :header: "Command", "Description"
   :widths: 15 85

   "net allocs", "打印 network memory allocations。仅当设置 :kconfig:option:`CONFIG_NET_DEBUG_NET_PKT_ALLOC` 时可用。"
   "net arp", "打印关于 IPv4 ARP cache 的信息。仅当在 IPv4 启用的 networks 中设置 :kconfig:option:`CONFIG_NET_ARP` 时可用。"
   "net bridge", "打印信息并操作 Ethernet bridges。仅当设置 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE_SHELL` 时可用。"
   "net capture", "监控 network traffic。细节参见 :ref:`network_monitoring`。"
   "net cm", "Connection manager shell。仅当设置 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER` 时可用。"
   "net conn", "打印关于 network connections 的信息。"
   "net dhcpv4", "启用/禁用 DHCPv4 client 或 server 支持。仅当设置 :kconfig:option:`CONFIG_NET_DHCPV4_SERVER` 或 :kconfig:option:`CONFIG_NET_DHCPV4` 时可用。"
   "net dhcpv6", "启用/禁用 DHCPv6 client 支持。仅当设置 :kconfig:option:`CONFIG_NET_DHCPV6` 时可用。"
   "net dns", "显示 DNS 如何配置。Command 还可用于解析 DNS name。仅当设置 :kconfig:option:`CONFIG_DNS_RESOLVER` 时可用。"
   "net events", "启用 network event 监控。仅当设置 :kconfig:option:`CONFIG_NET_MGMT_EVENT_MONITOR` 时可用。"
   "net filter", "查看 network packet filter rules。仅当设置 :kconfig:option:`CONFIG_NET_PKT_FILTER` 时可用。"
   "net ftp", "连接 FTP server 以传输 files。仅当设置 :kconfig:option:`CONFIG_FTP_CLIENT` 时可用。"
   "net gptp", "打印关于 gPTP 支持的信息。仅当设置 :kconfig:option:`CONFIG_NET_GPTP` 时可用。"
   "net http", "显示 HTTP server 信息（或发送 HTTP GET/POST/PUT/DELETE requests。仅当设置 :kconfig:option:`CONFIG_HTTP_SERVER` 或 :kconfig:option:`CONFIG_HTTP_CLIENT` 时可用。"
   "net iface", "打印关于 network interfaces 的信息。"
   "net ipv4", "打印 IPv4 特定信息和 configuration。仅当设置 :kconfig:option:`CONFIG_NET_IPV4` 时可用。"
   "net ipv6", "打印 IPv6 特定信息和 configuration。仅当设置 :kconfig:option:`CONFIG_NET_IPV6` 时可用。"
   "net mem", "打印关于 network memory 使用的信息。若设置 :kconfig:option:`CONFIG_NET_BUF_POOL_USAGE`（command 将打印更多信息。"
   "net nbr", "打印 neighbor 信息。仅当设置 :kconfig:option:`CONFIG_NET_IPV6` 时可用。"
   "net ping", "Ping network host。"
   "net pkt", "打印低层 network packet 信息以用于调试目的。"
   "net pmtu", "打印 MTU path discovery 信息。仅当设置 :kconfig:option:`CONFIG_NET_IPV6_PMTU` 或 :kconfig:option:`CONFIG_NET_IPV4_PMTU` 时可用。"
   "net ppp", "打印 Point-to-Point protocol 信息。仅当设置 :kconfig:option:`CONFIG_NET_L2_PPP` 和 :kconfig:option:`CONFIG_NET_PPP` 时可用。"
   "net ptp", "打印关于 PTP 支持的信息。用 ``net ptp <port>`` 获取详细 per-port view。仅当设置 :kconfig:option:`CONFIG_PTP` 时可用。"
   "net qbv", "显示并配置 IEEE 802.1Qbv Time-Aware Shaper（TAS）信息。仅当设置 :kconfig:option:`CONFIG_NET_QBV` 时可用。"
   "net quic", "显示并配置 QUIC transport。仅当设置 :kconfig:option:`CONFIG_QUIC` 时可用。"
   "net resume", "若启用 network power management（恢复 network interface。"
   "net route", "显示 IPv6 或 IPv4 network routes。仅当设置 :kconfig:option:`CONFIG_NET_IPV6_ROUTING` 或 :kconfig:option:`CONFIG_NET_IPV4_ROUTING` 时可用。"
   "net sockets", "显示 network socket 信息和 statistics。仅当设置 :kconfig:option:`CONFIG_NET_SOCKETS_OBJ_CORE` 和 :kconfig:option:`CONFIG_OBJ_CORE` 时可用。"
   "net ssh", "SSH client 支持。仅当设置 :kconfig:option:`CONFIG_SSH_CLIENT` 时可用。"
   "net sshd", "SSH server 支持。仅当设置 :kconfig:option:`CONFIG_SSH_SERVER` 时可用。"
   "net ssh_key", "SSH key 生成/移除/保存/加载支持。仅当设置 :kconfig:option:`CONFIG_SSH_CLIENT` 或 :kconfig:option:`CONFIG_SSH_SERVER` 时可用。"
   "net stats", "显示 network statistics。"
   "net suspend", "若启用 network power management（挂起 network interface。"
   "net tcp", "连接/发送 data/关闭 TCP connection。仅当设置 :kconfig:option:`CONFIG_NET_TCP` 时可用。"
   "net udp", "直接从 shell 发送 UDP data。仅当设置 :kconfig:option:`CONFIG_NET_UDP` 时可用。"
   "net virtual", "显示并操作 network virtual interfaces。仅当设置 :kconfig:option:`CONFIG_NET_L2_VIRTUAL` 时可用。"
   "net vlan", "显示 Ethernet virtual LAN 信息。仅当设置 :kconfig:option:`CONFIG_NET_VLAN` 时可用。"
   "net websocket", "打印 websocket 信息。仅当设置 :kconfig:option:`CONFIG_WEBSOCKET_CLIENT` 时可用。"
   "net wg", "显示 WireGuard VPN 信息（并设置 VPNs。仅当设置 :kconfig:option:`CONFIG_WIREGUARD` 时可用。"

Wi-Fi shell 提供扫描、连接、断开和配置 Wi-Fi networks 的命令。以下 Wi-Fi shell commands 已实现：

.. csv-table:: wifi-shell commands
   :header: "Command", "Description"
   :widths: 15 85

   "wifi <cmd>", "Wi-Fi network 连接、断开、扫描和配置的多个 commands。仅当设置 :kconfig:option:`CONFIG_NET_L2_WIFI_SHELL` 时可用。"
   "wifi cred", "显示/添加/删除 Wi-Fi network credentials。仅当设置 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_SHELL` 时可用。细节参见 :ref:`lib_wifi_credentials`。"

TLS credentials shell 提供列出、添加、删除和获取 TLS credential 信息的命令（来自 volatile 或 protected backend storage。以下 TLS credentials shell commands 已实现。这些 commands 仅当设置 :kconfig:option:`CONFIG_TLS_CREDENTIALS_SHELL` 时可用。细节参见 :ref:`tls_credentials_shell`。

.. csv-table:: tls-credentials-shell commands
   :header: "Command", "Description"
   :widths: 15 85

   "cred buf", "Buffer credential data 以可添加。"
   "cred add", "添加 TLS credential。"
   "cred del", "删除 TLS credential。"
   "cred get", "获取 TLS credential 的内容。"
   "cred list", "列出存储的 TLS credentials。"
