.. _ethernet_interface:

Ethernet
########

.. contents::
    :local:
    :depth:
    2

.. toctree::
   :maxdepth:
   1

   mac_config.rst
   vlan.rst
   lldp.rst
   8021Qav.rst

Overview
********

Ethernet
是
一
个
commonly
used
在
local
area
networks
（LAN）
中
的
networking
technology。
参考
这
个
`Ethernet
Wikipedia
article
<https://en.wikipedia.org/wiki/Ethernet>`_
获取
更多
information。

Zephyr
support
以下
Ethernet
features：

*
10、
100
和
1000
Mbit/sec
links
*
Auto
negotiation
*
Half/full
duplex
*
Promiscuous
mode
*
TX
和
RX
checksum
offloading
*
MAC
address
filtering
*
:ref:`MAC
address
configuration
<mac_address_config>`
*
:ref:`Virtual
LANs
<vlan_interface>`
*
:ref:`Priority
queues
<traffic-class-support>`
*
:ref:`IEEE
802.1AS
（gPTP）
<gptp_interface>`
*
:ref:`IEEE
802.1Qav
（credit
based
shaping）
<8021Qav>`
*
:ref:`LLDP
（Link
Layer
Discovery
Protocol）
<lldp_interface>`

不
是
所有
的
Ethernet
device
drivers
support
所有
这些
features。
你
可以
