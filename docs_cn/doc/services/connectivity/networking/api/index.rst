.. _networking_api:

网络 API
###############

Zephyr 为应用程序提供对标准 BSD 套接字 API（定义在
:zephyr_file:`include/zephyr/net/socket.h`）的支持。有关更多详细信息，请参阅 :ref:`BSD 套接字 API <bsd_sockets_interface>`。

除标准 API 外，Zephyr 还提供一组自定义网络 API 和库供应用程序使用。有关详细信息，请参阅以下列表。

.. note::
   应用程序不应使用 :zephyr_file:`include/zephyr/net/net_context.h` 中的旧版连接性 API。

.. toctree::
   :maxdepth: 2

   apis.rst
   buf_mgmt.rst
   net_tech.rst
   protocols.rst
   quic.rst
   system_mgmt.rst
   tsn.rst
   zperf.rst
