.. _dsa:

Distributed
Switch
Architecture
（DSA）
#####################################

.. contents::
    :local:
    :depth:
    2

Distributed
Switch
Architecture
（DSA）
不
是
什么
新
的
东西。
它
已
在
Linux
中
是
一
个
mature
的
subsystem
很
多年
了。
这
个
document
只
skip
background、
terms
和
任何
knowledge
related
的
description
因为
user
可能
在
`Linux
DSA
documentation`_
中
find
所有
这些。


DSA
switch
TX/RX
process
************************

DSA
switch
TX/RX
process
如
下。

.. image::
   dsa_txrx_process.svg

Host
interface
**************

Host
interface
network
devices
use
regular
和
unmodified
的
ethernet
driver
work
作为
DSA
conduit
port
它
通过
processor
manage
switch。

Switch
interface
****************

Switch
interfaces
也
在
zephyr
中
被
exposed
作为
standard
的
ethernet
interfaces。
connect
到
conduit
port
的
work
作为
CPU
port
其他
用于
user
purpose
的
work
作为
user
ports。

Switch
tagging
protocols
************************

通常
switch
tagging
protocols
是
vendor
specific
的。
它们
都
contain
某
个
东西
它：
