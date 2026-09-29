.. _networking_with_ieee802154_qemu:

Networking
with
QEMU
and
IEEE
802.15.4
######################################

.. contents::
    :local:
    :depth:
    2

这
个
page
describe
如何
set
up
一
个
virtual
network
在
两
个
QEMUs
之间
它们
通过
UART
connect
在一起
并
在
它们
之间
run
IEEE
802.15.4
link
layer。
注意
这
只
在
Linux
host
中
work。

Basic
Setup
***********

对于
下面
的
steps
你
将
需要
两
个
terminal
windows：

*
Terminal
#1
是
带
``echo-server``
Zephyr
sample
application
的
terminal
window。
*
Terminal
#2
是
带
``echo-client``
Zephyr
sample
application
的
terminal
window。

如果
你
想
capture
transferred
的
network
data
你
必须
compile
``tools/net-tools``
directory
中
的
``monitor_15_4``
program。

Open
一
个
terminal
window
并
type：

.. code-block::
   console

   cd
   $ZEPHYR_BASE/../tools/net-tools
   make
   monitor_15_4


Step
1
-
Compile
and
start
echo-server
======================================

在
terminal
#1
中
type：

.. zephyr-app-commands::
   :zephyr-app:
   samples/net/sockets/echo_server
   :host-os:
   unix
