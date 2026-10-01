.. _conn_mgr_overview:

Overview
########

Connection Manager 为可选 Zephyr features 的集合（旨在允许 applications 以最小关注底层 network technologies 的 specifics 监控和控制 connectivity（对 IP-capable networks 的访问。

用 Connection Manager（applications 可用单个 abstract API 控制 network association（并监控 Internet access（避免过度使用 technology-specific boilerplate。

这允许 application 潜在用单个 codebase 支持若干非常不同的 connectivity technologies（例如 Wi-Fi 和 LTE。

Applications 还可用 Connection Manager 通用管理和同时使用多个 connectivity technologies。

Structure
=========

Connection Manager 分为以下两个 subsystems：

* :ref:`Connectivity monitoring <conn_mgr_monitoring>`（header file :file:`include/zephyr/net/conn_mgr_monitoring.h`）监控所有可用 :ref:`Zephyr network interfaces (ifaces) <net_if_interface>`（并触发指示获得或失去 IP connectivity 时机的 :ref:`network management <net_mgmt_interface>` events。

* :ref:`Connectivity control <conn_mgr_control>`（header file :file:`include/zephyr/net/conn_mgr_connectivity.h`）提供控制 iface network association 的 abstract API。

.. _conn_mgr_integration_diagram_simple:

.. figure:: figures/integration_diagram_simplified.svg
    :alt: A simplified view of how Connection Manager integrates with Zephyr and the application.
    :figclass: align-center

    A simplified view of how Connection Manager integrates with Zephyr and the application.

    更详细版本参见 :ref:`here <conn_mgr_integration_diagram_detailed>`。

.. _conn_mgr_monitoring:

Connectivity monitoring
#######################

Connectivity monitoring 跟踪所有可用 ifaces（无论是否支持 :ref:`Connectivity control <conn_mgr_control>`）（当其通过各种 :ref:`operational states <net_if_interface_state_management>` 转换并获得或失去分配的 IP addresses。

每个可用 iface 在满足以下 criteria 时视为 ready：

* Iface 为 admin-up

  * 这意味着 iface 已被指示变为 operational-up（ready for use）。这通过调用 :c:func:`net_if_up` 完成。

* Iface 为 oper-up

  * 这意味着 interface 完全 ready for use；其在线（且若适用（已与 network 关联。
  * 细节参见 :ref:`net_if_interface_state_management`。

* Iface 至少有一个分配的 IP address

  * IPv4 和 IPv6 addresses 均可接受。
    只要分配了其中一个或两者即满足此条件。
  * Iface IP 分配细节参见 :ref:`net_if_interface`。

* Iface 未被 ignored

  * Ignored ifaces 始终视为 unready。
  * 更多细节参见 :ref:`conn_mgr_monitoring_ignoring_ifaces`。

.. note::

   通常（iface state 和 IP assignment 由 iface 的 :ref:`L2 implementation <net_l2_interface>` 或绑定的 :ref:`connectivity implementation <conn_mgr_impl>` 更新。

   细节参见 :ref:`conn_mgr_impl_guidelines_iface_state_reporting`。

Ready iface 在任一上述条件失去的瞬间不再 ready。

当至少一个 iface ready 时（触发 :c:macro:`NET_EVENT_L4_CONNECTED` :ref:`network management <net_mgmt_interface>` event（且 IP connectivity 视为 ready。

之后（ifaces 可在不触发额外 events 的情况下变为 ready 或 unready（只要始终至少保留一个 ready iface。

当不再有 ready ifaces 时（触发 :c:macro:`NET_EVENT_L4_DISCONNECTED` :ref:`network management <net_mgmt_interface>` event（且 IP connectivity 视为 unready。

.. note::

   Connection Manager 还触发以下更具体的 ``CONNECTED`` / ``DISCONNECTED`` events：

   - :c:macro:`NET_EVENT_L4_IPV4_CONNECTED`
   - :c:macro:`NET_EVENT_L4_IPV4_DISCONNECTED`
   - :c:macro:`NET_EVENT_L4_IPV6_CONNECTED`
   - :c:macro:`NET_EVENT_L4_IPV6_DISCONNECTED`

   这些类似 :c:macro:`NET_EVENT_L4_CONNECTED` 和 :c:macro:`NET_EVENT_L4_DISCONNECTED`（但专门跟踪 IPv4-capable 和 IPv6-capable ifaces 是否 ready。

.. _conn_mgr_monitoring_usage:

Usage
=====

若启用 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER` Kconfig option（则启用 connectivity monitoring。

要接收 connectivity 更新（为 :c:macro:`NET_EVENT_L4_CONNECTED` 和 :c:macro:`NET_EVENT_L4_DISCONNECTED` :ref:`network management <net_mgmt_interface>` events 创建并注册 listener：

.. code-block:: c

   /* Callback struct where the callback will be stored */
   struct net_mgmt_event_callback l4_callback;

   /* Callback handler */
   static void l4_event_handler(struct net_mgmt_event_callback *cb,
                                uint32_t event, struct net_if *iface)
   {
           if (event == NET_EVENT_L4_CONNECTED) {
                   LOG_INF("Network connectivity gained!");
           } else if (event == NET_EVENT_L4_DISCONNECTED) {
                   LOG_INF("Network connectivity lost!");
           }

           /* Otherwise, it's some other event type we didn't register for. */
   }

   /* Call this before Connection Manager monitoring initializes */
   static void my_application_setup(void)
   {
           /* Configure the callback struct to respond to (at least) the L4_CONNECTED
            * and L4_DISCONNECTED events.
            *
            *
            * Note that the callback may also be triggered for events other than those specified here!
            * (See the net_mgmt documentation)
            */
           net_mgmt_init_event_callback(
                   &l4_callback, l4_event_handler,
                   NET_EVENT_L4_CONNECTED | NET_EVENT_L4_DISCONNECTED
           );

           /* Register the callback */
           net_mgmt_add_event_callback(&l4_callback);
   }

也可用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER` 在 compile time（而非 runtime）注册 callback handler。这样（可确保在 Connection Manager monitoring 初始化前注册 callback。

.. code-block:: c

   static void l4_event_handler(uint64_t event, struct net_if *iface, void *info,
                                size_t info_length, void *user_data)
   {
           if (event == NET_EVENT_L4_CONNECTED) {
                   LOG_INF("Network connectivity gained!");
           } else if (event == NET_EVENT_L4_DISCONNECTED) {
                   LOG_INF("Network connectivity lost!");
           }

           /* Otherwise, it's some other event type we didn't register for. */
   }

   NET_MGMT_REGISTER_EVENT_HANDLER(l4_callback, l4_event_handler,
                                   NET_EVENT_L4_CONNECTED | NET_EVENT_L4_DISCONNECTED, NULL);

监听 net_mgmt events 更多细节参见 :ref:`net_mgmt_listening`。

.. note::
   为避免错过初始 connectivity events（应在 Connection Manager monitoring 初始化前注册 listener(s)。确保此策略参见 :ref:`conn_mgr_monitoring_missing_notifications`。

.. _conn_mgr_monitoring_missing_notifications:

Avoiding missed notifications
=============================

Connectivity monitoring 可能在初始化时立即触发 events。

若 application 在 connectivity monitoring 初始化后注册 event listeners（可能错过此第一波 events（且首次获得 network connectivity 时未被告知。

若此为 concern（application 应在 connectivity monitoring 初始化前 :ref:`register its event listeners <conn_mgr_monitoring_usage>`。

Connectivity monitoring 用 :c:macro:`SYS_INIT` ``APPLICATION`` 初始化 priority 初始化（由 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER_MONITOR_PRIORITY` Kconfig option 指定。

可用以下方式在此初始化前注册 callbacks：

* 用 :c:macro:`SYS_INIT` 以低于 Connection Manager monitoring 的 priority 注册 setup function（其中注册 callbacks。
* 用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER` 在 compile time 注册 callbacks。

.. _conn_mgr_monitoring_ignoring_ifaces:

Ignoring ifaces
===============

可用 :c:func:`conn_mgr_if_ignore` 忽略 iface。Ignored ifaces 被 connectivity monitoring 排除（且从不视为 ready。

可用 :c:func:`conn_mgr_if_unignore` 取消忽略。

.. _conn_mgr_control:

Connectivity control
####################

Connectivity control 为 applications 提供控制 iface network association 的 abstract API。

Applications 可用 :c:func:`conn_mgr_connect` 请求 iface 关联（用 :c:func:`conn_mgr_disconnect` 请求其取消关联。

Connection Manager 将此类请求翻译为绑定到 iface 的 :ref:`connectivity implementation <conn_mgr_impl>` 的 operations。

.. _conn_mgr_control_flags:

Flags
-----

可用 :c:func:`conn_mgr_if_set_flag` 为 iface 设置 connectivity flags。

* :c:enumerator:`CONN_MGR_IF_NO_AUTO_CONNECT` — 阻止 Connection Manager 在 connection loss 后自动重新关联该 iface。
* :c:enumerator:`CONN_MGR_IF_NO_AUTO_DOWN` — 阻止 Connection Manager 在放弃关联后将 iface admin-down。

可用 :c:func:`conn_mgr_if_clear_flag` 清除 flag。

.. _conn_mgr_control_persistence_timeouts:

Persistence and timeouts
------------------------

Connection Manager 支持 persistence（connection loss 后自动重试）和 timeouts（放弃 connection attempt）。

Persistence 和 timeout 行为由绑定的 :ref:`connectivity implementation <conn_mgr_impl>` 实现。

.. _conn_mgr_control_auto_down:

Auto admin-down
---------------

默认（Connection Manager 在 iface 放弃关联时自动将其 admin-down。

Applications 可通过禁用 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER_AUTO_IF_DOWN` Kconfig option 为所有 ifaces 禁用（或用 :c:func:`conn_mgr_if_set_flag` 设置 :c:enumerator:`CONN_MGR_IF_NO_AUTO_DOWN` connectivity flag 为单个 ifaces 禁用。

.. _conn_mgr_control_api:

Connectivity control API
========================

包含 header file :file:`include/zephyr/net/conn_mgr_connectivity.h` 以访问这些。

.. doxygengroup:: conn_mgr_connectivity

.. _conn_mgr_control_api_bulk:

Bulk API
--------

Connectivity control 提供若干 bulk functions（允许一次控制所有 ifaces。

若需要（可将这些 functions 限制为仅操作非 :ref:`ignored <conn_mgr_monitoring_ignoring_ifaces>` ifaces。

包含 header file :file:`include/zephyr/net/conn_mgr_connectivity.h` 以访问这些。

.. doxygengroup:: conn_mgr_connectivity_bulk
