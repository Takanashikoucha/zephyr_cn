.. _net_hostname_interface:

Hostname Configuration
######################

.. contents::
    :local:
    :depth: 2

Overview
********

联网 device 可能需要 hostname（例如（若 device 配置为 mDNS responder（细节参见 :ref:`dns_resolve_interface`）（且需响应 ``<hostname>.local`` DNS queries。

须设置 :kconfig:option:`CONFIG_NET_HOSTNAME_ENABLE` 以存储 hostname（并启用相关 APIs。若 option 启用（则默认 hostname 由 :kconfig:option:`CONFIG_NET_HOSTNAME` option 设为 ``zephyr``。

若相同 firmware image 用于 flash 多个 boards（则在所有 boards 中使用相同 hostname 不实际。此情况下（可启用 :kconfig:option:`CONFIG_NET_HOSTNAME_UNIQUE`（其向 hostname 添加唯一 postfix。默认使用第一个 network interface 的 link local address 作为 postfix。Ethernet networks 中（link local address 指 MAC address。例如（若 link local address 为 ``01:02:03:04:05:06``（则唯一 hostname 可为 ``zephyr010203040506``。若想自行设置 prefix（则在 network interfaces 创建前调用 ``net_hostname_set_postfix_str()``。或者（若偏好 prefix 的 hexadecimal 转换（则调用 ``net_hostname_set_postfix()``。例如对 Ethernet networks（initialization priority 由 :kconfig:option:`CONFIG_ETH_INIT_PRIORITY` 设置（因此您需在那之前设置 postfix。Postfix 仅可设置一次。

API Reference
*************

.. doxygengroup:: net_hostname
