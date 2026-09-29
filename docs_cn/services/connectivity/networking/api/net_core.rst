.. _net_core_interface:

Network
Core
Helpers
####################

.. contents::
    :local:
    :depth:
    2

Overview
********

Network
subsystem
包含
两
个
functions
用于
send
和
receive
来自
network
的
data。
``net_recv_data()``
通常
被
network
device
driver
used
当
received
的
network
data
需要
被
pushed
up
到
network
stack
中
用于
further
processing。
所有
的
data
通过
一
个
network
interface
received
它
通常
由
device
driver
created。

对于
sending
``net_send_data()``
可
被
used。
通常
applications
不
直接
call
这
个
function
因为
有
:ref:`bsd_sockets_interface`
API
用于
send
和
receive
network
data。

API
Reference
*************

.. doxygengroup::
   net_core
