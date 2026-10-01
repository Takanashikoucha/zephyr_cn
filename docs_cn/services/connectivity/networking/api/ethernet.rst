.. _ethernet_interface:

Ethernet
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

Overview
********

Ethernet 是常用于 local area networks（LAN）的 networking technology。更多信息参见此 `Ethernet Wikipedia article <https://en.wikipedia.org/wiki/Ethernet>`_。

Zephyr 支持以下 Ethernet features：

* 10、100 和 1000 Mbit/sec links
* Auto negotiation
* Half/full duplex
* Promiscuous mode
* TX 和 RX checksum offloading
* MAC address filtering
* :ref:`MAC address configuration <mac_address_config>`
* :ref:`Virtual LANs <vlan_interface>`
* :ref:`Priority queues <traffic-class-support>`
* :ref:`IEEE 802.1AS（gPTP）<gptp_interface>`
* :ref:`IEEE 802.1Qav（credit based shaping）<8021Qav>`
* :ref:`LLDP（Link Layer Discovery Protocol）<lldp_interface>`

并非所有 Ethernet device drivers 支持所有这些 features。您可用 ``net iface`` net-shell command 查看支持什么。它将打印当前支持的 Ethernet features。

API Reference
*************

.. doxygengroup:: ethernet

.. doxygengroup:: ethernet_mii
