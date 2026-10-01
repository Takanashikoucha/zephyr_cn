.. _socks5_interface:

SOCKS5 Proxy Support
####################

.. contents::
    :local:
    :depth: 2

Overview
********

SOCKS library 实现 SOCKS5 支持（允许 Zephyr 通过 network proxy 连接到 peer devices。

SOCKS5 工作原理的详细概述参见此 `SOCKS5 Wikipedia article <https://en.wikipedia.org/wiki/SOCKS#SOCKS5>`_。

protocol 本身更多信息参见 :rfc:`1928`。

SOCKS5 API
**********

SOCKS5 支持由 :kconfig:option:`CONFIG_SOCKS` Kconfig variable 启用。想用 SOCKS5 的 application 须调用 :c:func:`setsockopt()` 设置 SOCKS5 proxy host address（如下：

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

SOCKS5 Proxy Usage in MQTT
**************************

对 MQTT client（有 :c:func:`mqtt_client_set_proxy()` API（application 可调用以设置 SOCKS5 proxy。使用示例参见 :zephyr:code-sample:`mqtt-publisher` sample application。
