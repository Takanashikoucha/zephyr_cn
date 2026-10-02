.. _socks5_interface:

SOCKS5 代理支持
####################

.. contents::
    :local:
    :depth: 2

概述
********

SOCKS 库实现了 SOCKS5 支持，允许 Zephyr 通过网络代理连接对等设备。

有关 SOCKS5 工作原理的详细概述，请参见
`SOCKS5 维基百科文章 <https://en.wikipedia.org/wiki/SOCKS#SOCKS5>`_。

有关协议本身的更多信息，请参见 :rfc:`1928`。

SOCKS5 API
**********

SOCKS5 支持通过 :kconfig:option:`CONFIG_SOCKS` Kconfig 变量启用。
希望使用 SOCKS5 的应用程序必须像这样通过调用 :c:func:`setsockopt()`
来设置 SOCKS5 代理主机地址：

.. code-block:: c

    static int set_proxy(int sock, const struct sockaddr *proxy_addr,
                         socklen_t proxy_addrlen)
    {
        int ret;

        ret = setsockopt(sock, SOL_SOCKET, SO_SOCKS5,
                         proxy_addr, proxy_addrlen);
        if (ret < 0) {
                return -errno;
        }

        return 0;
    }

MQTT 中的 SOCKS5 代理使用
**************************

对于 MQTT 客户端，有 :c:func:`mqtt_client_set_proxy()` API，
应用程序可以调用它来设置 SOCKS5 代理。用法示例请参见 :zephyr:code-sample:`mqtt-publisher`
示例应用。
