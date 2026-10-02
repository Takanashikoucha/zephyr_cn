.. _net_hostname_interface:

主机名配置
######################

.. contents::
    :local:
    :depth: 2

概述
********

联网设备可能需要主机名，例如，如果设备被配置为 mDNS 响应器（细节参见 :ref:`dns_resolve_interface`）并且需要响应 ``<hostname>.local`` DNS 查询。

必须设置 :kconfig:option:`CONFIG_NET_HOSTNAME_ENABLE` 才能存储主机名并启用相关 API。如果该选项已启用，则默认主机名由 :kconfig:option:`CONFIG_NET_HOSTNAME` 选项设置为 ``zephyr``。

如果相同的固件镜像用于刷写多块板卡，则不实际在所有板卡中使用相同的主机名。在这种情况下，可以启用 :kconfig:option:`CONFIG_NET_HOSTNAME_UNIQUE`，该选项将向主机名添加唯一后缀。默认使用第一个网络接口的链路本地地址作为后缀。在以太网中，链路本地地址指的是 MAC 地址。例如，如果链路本地地址为 ``01:02:03:04:05:06``，则唯一主机名可以是 ``zephyr010203040506``。如果想自行设置前缀，则需要在创建网络接口之前调用 ``net_hostname_set_postfix_str()``。或者，如果偏好前缀的十六进制转换，则调用 ``net_hostname_set_postfix()``。例如对于以太网，初始化优先级由 :kconfig:option:`CONFIG_ETH_INIT_PRIORITY` 设置，因此您需要在该优先级之前设置后缀。后缀只能设置一次。

API 参考
*************

.. doxygengroup:: net_hostname
