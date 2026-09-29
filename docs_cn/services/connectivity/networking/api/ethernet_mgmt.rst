.. _ethernet_mgmt_interface:

Ethernet
Management
###################

.. contents::
    :local:
    :depth:
    2

Overview
********

Ethernet
management
API
提供
functions
用于
manage
Ethernet
network
interface
的
low
level
status。
这些
functions
的
callers
可以：

*
raise
``carrier
ON``
或
``carrier
OFF``
management
events
*
raise
``VLAN
enabled``
或
``VLAN
disabled``
management
events

通常
``carrier
OFF``
event
由
Ethernet
device
driver
generated
当
它
notices
Ethernet
cable
被
disconnected
时。
``carrier
ON``
event
由
Ethernet
device
driver
generated
当
它
notices
Ethernet
cable
被
re
connected
时。

当前
VLAN
events
由
Ethernet
L2
layer
generated
当
特定
的
VLAN
tag
被
enabled
或
disabled
时。

User
application
可以
monitor
这些
events
如果
它
需要
在
对应
的
status
changes
时
act。

API
Reference
*************

.. doxygengroup::
   ethernet_mgmt
