.. _net_offload_interface:

Network
Traffic
Offloading
==========================

.. contents::
    :local:
    :depth:
    2

Network
Offloading
##################

Overview
********

Network
offloading
API
提供
hooks
device
vendor
可以
use
来
provide
一
个
alternative
的
implementation
用于
一
个
IP
stack。
这
意味着
实际
的
network
connection
creation、
data
transfer
等
在
vendor
HAL
中
done
而
不
在
Zephyr
network
stack
中。

API
Reference
*************

.. doxygengroup::
   net_offload

.. _net_socket_offloading:

Socket
Offloading
#################

Overview
********

除了
network
offloading
API
Zephyr
允许
在
socket
API
level
offload
networking
functionality。
用
这
个
approach
provide
networking
stack
的
alternative
implementation
并
为
它们
的
networking
devices
expose
socket
API
的
vendors
可以
轻松
将它
与
Zephyr
integrate。

参考
:zephyr_file:`drivers/wifi/simplelink/simplelink_sockets.c`
获取
一
个
sample
implementation
关于
如何
在
socket
level
integrate
network
offloading。
