.. _mdio_api:

Management
Data
Input/Output
（MDIO）
###################################

Overview
********

MDIO
是
常用
于
与
ethernet
PHY
devices
通信
的
bus。
许多
ethernet
MAC
controllers
也
提供
通过
MDIO
bus
与
peripheral
device
通信
的
hardware。

这
个
API
旨在
主要
被
PHY
drivers
使用
但
也
可以
被
user
firmware
使用。

API
Reference
*************

.. doxygengroup::
   mdio_interface
