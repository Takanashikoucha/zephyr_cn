.. _cbor_api:

CBOR
####

`CBOR
<https://cbor.io/>`_
（Concise
Binary
Object
Representation）
是
一
个
data
format
它
的
design
goals
包括
extremely
small
的
code
size
的
possibility、
fairly
small
的
message
size、
和
extensibility
而
不
需要
version
negotiation。

Zephyr
通过
`zcbor`_
library
provide
对
CBOR
的
support
它
被
pulled
in
作为
一
个
West
module。

Configuration
*************

要
enable
CBOR
support
enable
:kconfig:option:`CONFIG_ZCBOR`
Kconfig
option。

API
Reference
*************

Zcbor
library
provide
它
自己
的
API
documentation
参考
它
获取
更多
information。

.. _`zcbor`:
   https://github.com/zephyrproject-rtos/zcbor
