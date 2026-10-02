.. _ethernet_interface:

以太网
########

.. contents::
    :local:
    :depth: 2

.. toctree::
   :maxdepth: 1

   mac_config.rst
   vlan.rst
   lldp.rst
   8021Qav.rst

概述
****

以太网是一种常用于局域网（LAN）的网络技术。
有关更多信息，请参阅这篇
`以太网维基百科文章 <https://en.wikipedia.org/wiki/Ethernet>`_。

Zephyr 支持以下以太网功能：

* 10、100 和 1000 Mbit/sec 链路
* 自动协商
* 半双工/全双工
* 混杂模式
* 发送和接收校验和卸载
* MAC 地址过滤
* :ref:`MAC 地址配置 <mac_address_config>`
* :ref:`虚拟局域网 <vlan_interface>`
* :ref:`优先级队列 <traffic-class-support>`
* :ref:`IEEE 802.1AS (gPTP) <gptp_interface>`
* :ref:`IEEE 802.1Qav（基于信用的整形）<8021Qav>`
* :ref:`LLDP（链路层发现协议）<lldp_interface>`

并非所有以太网设备驱动程序都支持所有这些功能。
您可以通过 ``net iface`` net-shell 命令查看支持的功能。该命令会打印当前支持的以太网功能。

API 参考
*********

.. doxygengroup:: ethernet

.. doxygengroup:: ethernet_mii
