.. _dhcpv4_interface:

DHCPv4
######

.. contents::
    :local:
    :depth:
    2

Overview
********

Dynamic
Host
Configuration
Protocol
（DHCP）
是
一
个
network
management
protocol
被
used
在
IPv4
networks
上。
一
个
DHCPv4
server
dynamically
assign
一
个
IPv4
address
和
其他
network
configuration
parameters
到
network
上
的
每个
device
使
它们
can
communicate
与
其他
IP
networks。
参考
这
个
`DHCP
Wikipedia
article
<https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol>`_
获取
关于
DHCP
如何
work
的
detailed
overview。

注意
Zephyr
support
DHCPv4
client
和
server
两
个
functionality。

Sample
usage
************

参考
:zephyr:code-sample:`dhcpv4-client`
sample
application
获取
details。

API
Reference
*************

.. doxygengroup::
   dhcpv4
