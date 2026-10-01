.. _net_pkt_filter_interface:

Network Packet Filtering
########################

.. contents::
    :local:
    :depth: 2

Overview
********

Network Packet Filtering facility 提供构建接受和/或拒绝 packet 传输和接收的 custom rules 的基础设施。其还允许修改 incoming network packets 的 priority。这可创建基本 firewall（控制 network traffic 等。

须设置 :kconfig:option:`CONFIG_NET_PKT_FILTER` 以启用相关 APIs。

Transmission 和 reception paths 均可有 filter rules 列表。每个 rule 由一组 conditions 和 packet outcome 组成。每个 packet 接受附于 rule 的 conditions。当给定 rule 的所有 conditions 为 true（packet outcome 立即按当前 rule 指定确定（且不再考虑更多 rules。若一个 condition 为 false（考虑列表中下一个 rule。

Packet outcome 为 ``NET_OK`` 接受 packet（``NET_DROP`` 丢弃（或 ``NET_CONTINUE`` 在线修改其 priority。

Outcome 为 ``NET_CONTINUE`` 时（priority 更新（但最终 outcome 尚未确定（处理继续。若多个 rules 的所有 conditions 为 true（packet 获得最后考虑的 rule 的 priority。

Rule 由 :c:struct:`npf_rule` 对象表示。可用 :c:func:`npf_insert_rule()`、:c:func:`npf_append_rule()` 和 :c:func:`npf_remove_rule()` 插入、追加到或从包含在 :c:struct:`npf_rule_list` 对象中的 rule list 移除。

Network stack 中不同 layers 有不同的 rules 集。某些 rules 应用于 L2 layer（如 Ethernet）（某些应用于处理 IPv4 或 IPv6 protocol 的 L3 layer。``local_in`` rules 用于匹配 incoming protocol types（如运行在 IPv4 或 IPv6 之上的 UDP 或 TCP packets。不同 layers 的 rule 支持可由下文提到的相关 Kconfig options 控制。

* ``npf_send_rules`` 为应用于 L2 layer 中 outgoing packets 的 rule list
* ``npf_recv_rules`` 为应用于 L2 layer 中 incoming packets 的 rule list
* ``npf_ipv4_recv_rules`` 为应用于 incoming IPv4 packets 的 rule list。可用 :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV4_HOOK` option 启用或禁用。
* ``npf_ipv6_recv_rules`` 为应用于 incoming IPv6 packets 的 rule list。可用 :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV6_HOOK` option 启用或禁用。
* ``npf_local_in_recv_rules`` 为应用于 incoming UDP 或 TCP packets 的 rule list。可用 :kconfig:option:`CONFIG_NET_PKT_FILTER_LOCAL_IN_HOOK` option 启用或禁用。

若 filter rule list 为空（假设 ``NET_OK``。若非空 rule list 运行到末尾（假设 ``NET_DROP``。然而（推荐总是用显式 default termination rule（``npf_default_ok`` 或 ``npf_default_drop``）终止非空 rule list。

Rule conditions 由 :c:struct:`npf_test` 表示。此 structure 在特定 condition 需额外 test data 时可嵌入更大的 structure。由此类 conditions 的 test function 负责从提供的 ``npf_test`` structure pointer 获取外层 structure。

:zephyr_file:`include/zephyr/net/net_pkt_filter.h` 中提供 convenience macros 以静态定义各种 conditions 的 condition instances（以及 :c:macro:`NPF_RULE()` 和 :c:macro:`NPF_PRIORITY()` 以创建带 immediate outcome 或 priority 变化的 rule instance。

如何创建和管理 packet filters 的示例参见 :zephyr:code-sample:`net-pkt-filter` sample。Network shell 有 ``net filter`` command（可用于在 runtime 查看安装的 rules。

Examples
********

使用示例：

.. code-block:: c

    static NPF_SIZE_MAX(maxsize_200, 200);
    static NPF_ETH_TYPE_MATCH(ip_packet, NET_ETH_PTYPE_IP);

    static NPF_RULE(small_ip_pkt, NET_OK, ip_packet, maxsize_200);

    void install_my_filter(void)
    {
        npf_insert_recv_rule(&npf_default_drop);
        npf_insert_recv_rule(&small_ip_pkt);
    }

上述将接受 200 bytes 或更小的 IP packets（并丢弃所有其他 packets。

另一种（效率较低）实现相同结果的方式可为：

.. code-block:: c

    static NPF_SIZE_MIN(minsize_201, 201);
    static NPF_ETH_TYPE_UNMATCH(not_ip_packet, NET_ETH_PTYPE_IP);

    static NPF_RULE(reject_big_pkts, NET_DROP, minsize_201);
    static NPF_RULE(reject_non_ip, NET_DROP, not_ip_packet);

    void install_my_filter(void) {
        npf_append_recv_rule(&reject_big_pkts);
        npf_append_recv_rule(&reject_non_ip);
        npf_append_recv_rule(&npf_default_ok);
    }

此示例为不同 network traffic 分配 priorities。其给予 ``ptp`` packets network control priority（``NET_PRIORITY_NC``）（version 6 的 internet traffic critical applications priority（``NET_PRIORITY_CA``）（internet protocol version 4 traffic excellent effort（``NET_PRIORITY_EE``）（``lldp`` 和 ``arp`` 最低 background priority（``NET_PRIORITY_BK``）。

仅当项目配置 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 中启用多个 traffic class queues 时（priority rules 才真正有用。从 packet 的 priority 到 traffic class queue 的映射符合标准 802.1Q（并取决于 :kconfig:option:`CONFIG_NET_TC_RX_COUNT`。

.. code-block:: c

    static NPF_ETH_TYPE_MATCH(is_arp, NET_ETH_PTYPE_ARP);
    static NPF_ETH_TYPE_MATCH(is_lldp, NET_ETH_PTYPE_LLDP);
    static NPF_ETH_TYPE_MATCH(is_ptp, NET_ETH_PTYPE_PTP);
    static NPF_ETH_TYPE_MATCH(is_ipv4, NET_ETH_PTYPE_IP);
    static NPF_ETH_TYPE_MATCH(is_ipv6, NET_ETH_PTYPE_IPV6);

    static NPF_PRIORITY(priority_bk, NET_PRIORITY_BK, is_arp, is_lldp);
    static NPF_PRIORITY(priority_ee, NET_PRIORITY_EE, is_ipv4);
    static NPF_PRIORITY(priority_ca, NET_PRIORITY_CA, is_ipv6);
    static NPF_PRIORITY(priority_nc, NET_PRIORITY_NC, is_ptp);

    void install_my_filter(void) {
        npf_append_recv_rule(&priority_bk);
        npf_append_recv_rule(&priority_ee);
        npf_append_recv_rule(&priority_ca);
        npf_append_recv_rule(&priority_nc);
        npf_append_recv_rule(&npf_default_ok);
    }

API Reference
*************

.. doxygengroup:: net_pkt_filter

.. doxygengroup:: npf_basic_cond

.. doxygengroup:: npf_eth_cond
