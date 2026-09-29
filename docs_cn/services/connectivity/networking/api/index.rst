.. _networking_api:

Networking
APIs
###############

Zephyr
提供
support
standard
的
BSD
socket
APIs
（defined
in
:zephyr_file:`include/zephyr/net/socket.h`）
供
applications
use。
参考
:ref:`BSD
socket
API
<bsd_sockets_interface>`
获取
更多
details。

除了
standard
API
Zephyr
提供
一
组
custom
的
networking
APIs
和
libraries
供
application
use。
参考
下面
的
list
获取
details。

.. note::
   在
   :zephyr_file:`include/zephyr/net/net_context.h`
   中
   的
   legacy
   connectivity
   API
   不
   应该
   被
   applications
   used。

.. toctree::
   :maxdepth:
   2

   apis.rst
   buf_mgmt.rst
   net_tech.rst
   protocols.rst
   quic.rst
   system_mgmt.rst
   tsn.rst
   zperf.rst
