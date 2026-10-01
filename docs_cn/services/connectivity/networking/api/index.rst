.. _networking_api:

Networking APIs
###############

Zephyr 为 applications 使用提供支持标准 BSD socket APIs（定义在 :zephyr_file:`include/zephyr/net/socket.h`）。更多细节参见 :ref:`BSD socket API <bsd_sockets_interface>`。

标准 API 之外（Zephyr 提供一组 custom networking APIs 和 libraries 供 application 使用。更多细节参见以下列表。

.. note::
   :zephyr_file:`include/zephyr/net/net_context.h` 中的 legacy connectivity API 不应被 applications 使用。

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
