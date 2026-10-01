.. _dns_resolve_interface:

DNS Resolve
###########

.. contents::
    :local:
    :depth: 2

Overview
********

DNS resolver 按 :rfc:`1035` 实现基本 DNS resolver。支持的 DNS answers 为 IPv4/IPv6 addresses 和 CNAME。

若收到 CNAME（DNS resolver 将创建另一 DNS query。额外 queries 数由 :kconfig:option:`CONFIG_DNS_RESOLVER_ADDITIONAL_QUERIES` Kconfig variable 控制。

Multicast DNS（mDNS）client resolver support 可通过设置 :kconfig:option:`CONFIG_MDNS_RESOLVER` Kconfig option 启用。mDNS 更多细节参见 :rfc:`6762`。

Link-local multicast name resolution（LLMNR）client resolver support 可通过设置 :kconfig:option:`CONFIG_LLMNR_RESOLVER` Kconfig variable 启用。LLMNR 更多细节参见 :rfc:`4795`。

DNS configuration variables 的更多信息参见 :zephyr_file:`subsys/net/lib/dns/Kconfig`。DNS resolver API 可在 :zephyr_file:`include/zephyr/net/dns_resolve.h` 找到。

:rfc:`6763` 中描述的 DNS-based service discovery queries 可由 :c:func:`dns_resolve_service` API 执行。返回的 service descriptions 传递给 user 提供的 callback（且 API 将 address family 设为 :c:macro:`AF_LOCAL` 以指示值非 IPv4 或 IPv6 address 而是 service description。

示例：

.. code-block:: c

   #include <zephyr/net/dns_resolve.h>

   #define MAX_STR_LEN CONFIG_DNS_RESOLVER_MAX_NAME_LEN

   static void dns_result_cb(enum dns_resolve_status status,
                             struct dns_addrinfo *info,
                             void *user_data)
   {
        if (status == DNS_EAI_CANCELED) {
                /* dns: Timeout while resolving name */
                return;
	}

        if (status == DNS_EAI_INPROGRESS && info) {
                char str[MAX_STR_LEN + 1];

                if (info->ai_family == NET_AF_INET) {
                        net_addr_ntop(NET_AF_INET,
                                      &net_sin(&info->ai_addr)->sin_addr,
                                      str, NET_IPV4_ADDR_LEN);
                } else if (info->ai_family == NET_AF_INET6) {
                        net_addr_ntop(NET_AF_INET6,
                                      &net_sin6(&info->ai_addr)->sin6_addr,
                                      str, NET_IPV6_ADDR_LEN);
                } else if (info->ai_family == AF_LOCAL) {
                        /* service discovery */
                        memset(str, 0, MAX_STR_LEN);
                        memcpy(str, info->ai_canonname,
                               MIN(info->ai_addrlen, MAX_STR_LEN));
                } else {
                        strncpy(str, "Invalid proto family", MAX_STR_LEN + 1);
                }

                str[MAX_STR_LEN] = '\0';

                printk("dns: %s\n", str);
                return;
        }

        if (status == DNS_EAI_ALLDONE) {
                printk("dns: All results received\n");
                return;
        }

        if (status == DNS_EAI_FAIL) {
                printk("dns: No such name found.\n");
                return;
        }

        printk("dns: Unhandled status %d received (errno %d)\n", status, errno);
   }

   #define DNS_TIMEOUT (MSEC_PER_SEC * 5) /* in ms */

   static void discover_service(void)
   {
        int ret = dns_resolve_service(dns_resolve_get_default(),
                                      "_http._tcp.dns-sd.org",
                                      NULL, dns_result_cb,
                                      NULL, DNS_TIMEOUT);
        ...
   }

上述 query 将返回如下输出：

.. code-block: console

    Query for '_http._tcp.dns-sd.org' sent.
    dns: . * cnn, world news._http._tcp.dns-sd.org
    dns: .source de télévision, département de langues._http._tcp.dns-sd.org
    dns: . * multicast dns._http._tcp.dns-sd.org
    dns: . * amazon.com, on-line shopping._http._tcp.dns-sd.org
    dns: . * google, searching the web._http._tcp.dns-sd.org
    dns: . * ebay, online auctions._http._tcp.dns-sd.org
    dns: . * apple, makers of the ipod._http._tcp.dns-sd.org
    dns: . * yahoo, maps, weather, and stock quotes._http._tcp.dns-sd.org
    dns: .about bonjour in web browsers._http._tcp.dns-sd.org
    dns: .π._http._tcp.•bullets•.dns-sd.org
    dns: . * dns service discovery._http._tcp.dns-sd.org
    dns: . * wired, technology, culture, business, politics._http._tcp.dns-sd.org
    dns: . * slashdot, news for nerds, stuff that matters._http._tcp.dns-sd.org
    dns: . * bbc, world news._http._tcp.dns-sd.org
    dns: .stuart’s printer._http._tcp.dns-sd.org
    dns: . * zeroconf._http._tcp.dns-sd.org
    dns: All results received

由于 service discovery query 可能返回长 strings 且 packet size 可能较大（您可能需调整以下 Kconfig options：

- :kconfig:option:`CONFIG_DNS_RESOLVER_MAX_ANSWER_SIZE`。其指示 answer 的最大 size（此 option 的典型值可为 1024。此 option 的默认 size 为 512 bytes。

- :kconfig:option:`CONFIG_DNS_RESOLVER_MAX_NAME_LEN`。其指示返回 name 的最大长度。值取决于您的预期 data size（典型值可能为 128 bytes。

Network management events
*************************

DNS resolver 触发以下 :c:macro:`NET_MGMT_EVENT` events：

- :c:macro:`NET_EVENT_DNS_SERVER_ADD` — 单个 DNS server slot 被添加到 resolver。每 slot 触发一次（以 originating interface 作为 event payload。
- :c:macro:`NET_EVENT_DNS_SERVER_DEL` — 单个 DNS server slot 被移除（以 originating interface 作为 event payload。
- :c:macro:`NET_EVENT_DNS_SERVERS_RECONFIGURED` — DNS server configuration 通过 :c:func:`dns_resolve_reconfigure` 或 :c:func:`dns_resolve_reconfigure_with_interfaces` 刷新。无论 individual server slots 是否实际变化（每次成功调用均触发（以 ``NULL`` iface（system-level event）。

``ADD`` 和 ``DEL`` 为 *delta* events：当 :c:func:`dns_resolve_reconfigure` 以与现有相同的 server set 调用时（``ADD`` 和 ``DEL`` 均不触发 — resolver 有意抑制它们以避免在 DHCP-offer retransmit 和 IPv6 RA 时取消 in-flight queries。在网络 event 后（例如 PPP iface 重新建立后在每个 PM resume cycle 通过 IPCP 推送相同 DNS servers）需要"DNS configuration 再次就绪"gate 的 consumers 应监听 ``NET_EVENT_DNS_SERVERS_RECONFIGURED`` 而非 ``NET_EVENT_DNS_SERVER_ADD``。

Sample usage
************

参见 :zephyr:code-sample:`dns-resolve` sample application 以了解细节。

API Reference
*************

.. doxygengroup:: dns_resolve
