.. _socks5_interface:

SOCKS5
Proxy
Support
####################

.. contents::
    :local:
    :depth:
    2

Overview
********

SOCKS
library
implement
SOCKS5
support
它
允许
Zephyr
通过
network
proxy
connect
到
peer
devices。

参考
这
个
`SOCKS5
Wikipedia
article
<https://en.wikipedia.org/wiki/SOCKS#SOCKS5>`_
获取
关于
SOCKS5
如何
work
的
detailed
overview。

关于
protocol
本身
的
更多
information
参考
:rfc:`1928`。

SOCKS5
API
**********

SOCKS5
support
由
:kconfig:option:`CONFIG_SOCKS`
Kconfig
variable
enabled。
想
use
SOCKS5
的
Application
必须
通过
call
:c:func:`setsockopt()`
set
SOCKS5
proxy
host
address
如
这
个：

.. code-block::
   c

   static
   int
   set_proxy(int
   sock,
   const
   struct
   sockaddr
   *proxy_addr,
              socklen_t
   proxy_addrlen)
   {
       int
   ret;

       ret
   =
   setsockopt(sock,
   SOL_SOCKET,
   SO_SOCKS5,
              proxy_addr,
   proxy_addrlen);
       if
   (ret
   <
   0)
   {
               return
   -errno;
       }
