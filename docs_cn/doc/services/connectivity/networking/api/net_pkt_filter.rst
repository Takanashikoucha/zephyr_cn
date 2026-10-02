.. _net_pkt_filter_interface:

网络数据包过滤
########################

.. contents::
    :local:
    :depth: 2

概述
********

网络数据包过滤（Network Packet Filtering）设施提供了基础设施，
用于构建自定义规则以接受和/或拒绝数据包的
发送与接收。它还允许修改传入
网络数据包的优先级。这可以用于创建基础防火墙、控制网络
流量等。

必须设置 :kconfig:option:`CONFIG_NET_PKT_FILTER` 才能
启用相关 API。

发送路径和接收路径都可以有一个过滤规则列表。
每条规则由一组条件和数据包处理结果组成。每个数据包
都会接受规则所附带条件的检测。当某条规则的
所有条件都为真时，数据包的处理结果立即
由当前规则指定，并且不再考虑其他规则。如果某个
条件为假，则考虑列表中的下一条规则。

数据包处理结果要么是 ``NET_OK``（接受数据包）、``NET_DROP``
（丢弃它），要么是 ``NET_CONTINUE``（临时修改其优先级）。

当结果为 ``NET_CONTINUE`` 时，优先级会被更新，但最终
结果尚未确定，处理会继续。如果
多条规则的所有条件都为真，则数据包获得
最后被考虑的那条规则的优先级。

规则由 :c:struct:`npf_rule` 对象表示。可以使用
:c:func:`npf_insert_rule()`、
:c:func:`npf_append_rule()` 和 :c:func:`npf_remove_rule()`
将其插入、追加或移除到包含在
:c:struct:`npf_rule_list` 对象中的规则列表里。

网络栈中不同层有不同的规则集。
有些规则应用于 L2 层（如以太网），有些则应用于
处理 IPv4 或 IPv6 协议的 L3 层。``local_in`` 规则用于匹配
运行在 IPv4 或 IPv6 之上的 UDP 或 TCP 等
传入协议类型。不同层的规则支持
可以通过下面提到的相关 Kconfig 选项
进行控制。

* ``npf_send_rules`` 是应用于 L2 层出站数据包的规则列表
* ``npf_recv_rules`` 是应用于 L2 层传入数据包的规则列表
* ``npf_ipv4_recv_rules`` 是应用于传入 IPv4 数据包的规则列表。可
  通过 :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV4_HOOK` 选项启用或禁用。
* ``npf_ipv6_recv_rules`` 是应用于传入 IPv6 数据包的规则列表。可
  通过 :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV6_HOOK` 选项启用或禁用。
* ``npf_local_in_recv_rules`` 是应用于传入 UDP 或 TCP 数据包的规则列表。
  可通过 :kconfig:option:`CONFIG_NET_PKT_FILTER_LOCAL_IN_HOOK` 选项启用或禁用。

如果过滤规则列表为空，则默认视为 ``NET_OK``。如果非空
规则列表执行到末尾，则默认视为 ``NET_DROP``。不过
建议始终用一个显式的默认终止规则
（``npf_default_ok`` 或 ``npf_default_drop``）来结束非空规则列表。

规则条件由 :c:struct:`npf_test` 表示。当某个特定条件需要
额外测试数据时，该结构体可以嵌入到更大的结构体中。对于此类条件，
由其测试函数负责从提供的 ``npf_test`` 结构体指针
中获取外层结构体。

:zephyr_file:`include/zephyr/net/net_pkt_filter.h` 中提供了便捷宏，
用于静态定义各种条件的实例，
以及用于创建具有即时结果或优先级变更的规则实例的
:c:macro:`NPF_RULE()` 和 :c:macro:`NPF_PRIORITY()`。

另请参见 :zephyr:code-sample:`net-pkt-filter` 示例，了解如何创建和
管理数据包过滤器的示例。网络 shell 有一个 ``net filter`` 命令，可用于
在运行时查看已安装规则。

示例
********

下面是一个使用示例：

.. code-block:: c

    static NPF_SIZE_MAX(maxsize_200, 200);
    static NPF_ETH_TYPE_MATCH(ip_packet, NET_ETH_PTYPE_IP);

    static NPF_RULE(small_ip_pkt, NET_OK, ip_packet, maxsize_200);

    void install_my_filter(void)
    {
        npf_insert_recv_rule(&npf_default_drop);
        npf_insert_recv_rule(&small_ip_pkt);
    }

上面代码会接受 200 字节或更小的 IP 数据包，
并丢弃所有其他数据包。

另一种（效率较低的）实现相同结果的方式可以是：

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

此示例为不同的网络流量分配优先级。它给
``ptp`` 数据包分配网络控制优先级（``NET_PRIORITY_NC``），
给版本 6 的互联网流量分配关键应用优先级（``NET_PRIORITY_CA``），
给互联网协议版本 4
流量分配尽力而为优先级（``NET_PRIORITY_EE``），
给 ``lldp`` 和 ``arp`` 分配最低的背景优先级（``NET_PRIORITY_BK``）。

只有当项目配置 :kconfig:option:`CONFIG_NET_TC_RX_COUNT`
启用了多个流量类别队列时，优先级规则才真正有用。
从数据包优先级到流量类别队列的映射
遵循标准 802.1Q，并取决于
:kconfig:option:`CONFIG_NET_TC_RX_COUNT`。

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

API 参考
*************

.. doxygengroup:: net_pkt_filter

.. doxygengroup:: npf_basic_cond

.. doxygengroup:: npf_eth_cond
