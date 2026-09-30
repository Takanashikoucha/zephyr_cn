.. _conn_mgr_overview:

Overview
########

Connection
Manager
是
一
组
optional
的
Zephyr
features
它们
aim
允许
applications
monitor
和
control
connectivity
（access
到
IP
capable
的
networks）
而
minimal
concern
underlying
network
technologies
的
specifics。

Use
Connection
Manager
applications
可以
use
单
个
abstract
的
API
control
network
association
并
monitor
Internet
access
并
avoid
过度
use
technology
specific
的
boilerplate。

这
允许
一
个
application
可能
support
几
个
非常
不同
的
connectivity
technologies
（例如
Wi
Fi
和
LTE）
用
单
个
codebase。

Applications
也
可以
use
Connection
Manager
generically
manage
并
同时
use
多
个
connectivity
technologies。

Structure
=========

Connection
Manager
被
split
成
以下
两
个
subsystems：

*
:ref:`Connectivity
monitoring
<conn_mgr_monitoring>`
（header
file
:file:`include/zephyr/net/conn_mgr_monitoring.h`）
monitor
所有
available
的
:ref:`Zephyr
network
interfaces
（ifaces）
<net_if_interface>`
并
trigger
:ref:`network
management
<net_mgmt_interface>`
events
indicate
当
IP
connectivity
被
gained
或
lost
时。

*
:ref:`Connectivity
control
<conn_mgr_control>`
（header
file
:file:`include/zephyr/net/conn_mgr_connectivity.h`）
provide
一
个
abstract
的
API
用于
control
iface
network
association。

.. _conn_mgr_integration_diagram_simple:

.. figure::
   figures/integration_diagram_simplified.svg
   :alt:
   Connection
   Manager
   如何
   与
   Zephyr
   和
   application
   integrate
   的
   simplified
   view
   :figclass:
   align-center

   Connection
   Manager
   如何
   与
   Zephyr
   和
   application
   integrate
   的
   simplified
   view。

   参考
   :ref:`这里
   <conn_mgr_integration_diagram_detailed>`
   获取
   更
   detailed
   的
   version。

.. _conn_mgr_monitoring:

Connectivity
monitoring
#######################

Connectivity
monitoring
track
所有
available
的
ifaces
（不管
它们
是否
support
:ref:`Connectivity
control
<conn_mgr_control>`）
当
它们
transition
通过
各种
:ref:`operational
states
<net_if_interface_state_management>`
并
acquire
或
lose
assigned
的
IP
addresses
时。

每个
available
的
iface
如果
meet
以下
criteria
则
被
considered
ready：


.. note::

   以下为原文（待翻译）


.. note::

  To avoid inconsistent behavior, all connectivity implementations must adhere to the :ref:`implementation guidelines <conn_mgr_impl_guidelines>`.

.. _conn_mgr_control_operation_connecting:

Connecting
----------

Once a bound iface is admin-up (see :ref:`net_if_interface_state_management`), :c:func:`conn_mgr_if_connect` can be called to cause it to associate with a network.

If association succeeds, the connectivity implementation will mark the iface as operational-up (see :ref:`net_if_interface_state_management`).

If association fails unrecoverably, the :ref:`fatal error event <conn_mgr_control_events_fatal_error>` will be triggered.

You can configure an optional :ref:`timeout <conn_mgr_control_timeouts>` for this process.

.. note::
   The :c:func:`conn_mgr_if_connect` function is intentionally minimalistic, and does not take any kind of configuration.
   Each connectivity implementation should provide a way to pre-configure or automatically configure any required association settings or credentials.
   See :ref:`conn_mgr_impl_guidelines_preconfig` for details.

.. _conn_mgr_control_operation_loss:

Connection loss
---------------

If connectivity is lost due to external factors, the connectivity implementation will mark the iface as operational-down.

Depending on whether :ref:`persistence <conn_mgr_control_persistence>` is set, the iface may then attempt to reconnect.

.. _conn_mgr_control_operation_disconnection:

Manual disconnection
--------------------

The application can also request that connectivity be intentionally abandoned by calling :c:func:`conn_mgr_if_disconnect`.

In this case, the connectivity implementation will disassociate the iface from its network and mark the iface as operational-down (see :ref:`net_if_interface_state_management`).
A new connection attempt will not be initiated, regardless of whether persistence is enabled.

.. _conn_mgr_control_persistence_timeouts:

Timeouts and Persistence
========================

Connection Manager requires that all connectivity implementations support the following standard key features:

* :ref:`Connection timeouts <conn_mgr_control_timeouts>`
* :ref:`Connection persistence <conn_mgr_control_persistence>`

These features describe how ifaces should behave during connect and disconnect events.
You can individually set them for each iface.

.. note::
   It is left to connectivity implementations to successfully and accurately implement these two features as described below.
   See :ref:`conn_mgr_impl_timeout_persistence` for more details from the connectivity implementation perspective.

The Connection Manager also implements the following optional feature:

* :ref:`Interface idle timeouts <conn_mgr_control_idle_timeout>`

.. note::
   The only requirement on the connectivity implementation to implement idle timeouts is to call :c:func:`conn_mgr_if_used` each
   time the interface is used.

.. _conn_mgr_control_timeouts:

Connection Timeouts
-------------------

When :c:func:`conn_mgr_if_connect` is called on an iface, a connection attempt begins.

The connection attempt continues indefinitely until it succeeds, unless a timeout has been specified for the iface (using :c:func:`conn_mgr_if_set_timeout`).

In that case, the connection attempt will be abandoned if the timeout elapses before it succeeds.
If this happens, the :ref:`timeout event<conn_mgr_control_events_timeout>` is raised.

.. _conn_mgr_control_idle_timeout:

Interface Idle Timeout
----------------------

The connection manager enables users to apply an inactivity timeout on an interface (:c:func:`conn_mgr_if_set_idle_timeout`).
Once connected, if the interface goes for the configured number of seconds without any activity, the interface is automatically disconnected.
If this happens, the :ref:`idle timeout event<conn_mgr_control_events_idle_timeout>` is raised.
An idle timeout is considered an unintentional connection loss for the purposes of :ref:`Connection persistence <conn_mgr_control_persistence>`.

.. _conn_mgr_control_persistence:

Connection Persistence
----------------------

Each iface also has a connection persistence setting that you can enable or disable by setting the :c:enumerator:`CONN_MGR_IF_PERSISTENT` flag with :c:func:`conn_mgr_binding_set_flag`.

This setting specifies how the iface should handle unintentional connection loss.

If persistence is enabled, any unintentional connection loss will initiate a new connection attempt, with a new timeout if applicable.

Otherwise, the iface will not attempt to reconnect.

.. note::
   Persistence not does affect connection attempt behavior.
   Only the timeout setting affects this.

   For instance, if a connection attempt on an iface times out, the iface will not attempt to reconnect, even if it is persistent.

   Conversely, if there is not a specified timeout, the iface will try to connect forever until it succeeds, even if it is not persistent.

   See :ref:`conn_mgr_impl_tp_persistence_during_connect` for the equivalent implementation guideline.

.. _conn_mgr_control_events:

Control events
==============

Connectivity control triggers :ref:`network management <net_mgmt_interface>` events to inform the application of important state changes.

See :ref:`conn_mgr_impl_guidelines_trigger_events` for the corresponding connectivity implementation guideline.

.. _conn_mgr_control_events_fatal_error:

Fatal Error
-----------

The :c:macro:`NET_EVENT_CONN_IF_FATAL_ERROR` event is raised when an iface encounters an error from which it cannot recover (meaning any subsequent attempts to associate are guaranteed to fail, and all such attempts should be abandoned).

Handlers of this event will be passed a pointer to the iface for which the fatal error occurred.
Individual connectivity implementations may also pass an application-specific data pointer.

.. _conn_mgr_control_events_timeout:

Timeout
-------

The :c:macro:`NET_EVENT_CONN_IF_TIMEOUT` event is raised when an :ref:`iface association <conn_mgr_control_operation_connecting>` attempt :ref:`times out <conn_mgr_control_timeouts>`.

Handlers of this event will be passed a pointer to the iface that timed out attempting to associate.

.. _conn_mgr_control_events_idle_timeout:

Idle Timeout
------------

The :c:macro:`NET_EVENT_CONN_IF_IDLE_TIMEOUT` event is raised when an interface is considered :ref:`inactive <conn_mgr_control_idle_timeout>`.

Handlers of this event will be passed a pointer to the iface that timed out attempting to associate.

.. _conn_mgr_control_events_listening:

Listening for control events
----------------------------

You can listen for control events as follows:

.. code-block:: c

   /* Declare a net_mgmt callback struct to store the callback */
   struct net_mgmt_event_callback my_conn_evt_callback;

   /* Declare a handler to receive control events */
   static void my_conn_evt_handler(struct net_mgmt_event_callback *cb,
                                   uint32_t event, struct net_if *iface)
   {
           if (event == NET_EVENT_CONN_IF_TIMEOUT) {
                   /* Timeout occurred, handle it */
           } else if (event == NET_EVENT_CONN_IF_FATAL_ERROR) {
                   /* Fatal error occurred, handle it */
           }

           /* Otherwise, it's some other event type we didn't register for. */
   }

   int main()
   {
           /* Configure the callback struct to respond to (at least) the CONN_IF_TIMEOUT
            * and CONN_IF_FATAL_ERROR events.
            *
            * Note that the callback may also be triggered for events other than those specified here!
            * (See the net_mgmt documentation)
            */

           net_mgmt_init_event_callback(
                   &conn_mgr_conn_callback, conn_mgr_conn_handler,
                       NET_EVENT_CONN_IF_TIMEOUT | NET_EVENT_CONN_IF_FATAL_ERROR
           );

           /* Register the callback */
           net_mgmt_add_event_callback(&conn_mgr_conn_callback);
           return 0;
   }

See :ref:`net_mgmt_listening` for more details on listening for net_mgmt events.

.. _conn_mgr_control_automations:

Automated behaviors
===================

There are a few actions related to connectivity that are (by default at least) performed automatically for the user.

.. _conn_mgr_control_automations_auto_up:

.. topic:: Automatic admin-up

   In Zephyr, ifaces are automatically taken admin-up (see :ref:`net_if_interface_state_management` for details on iface states) during initialization.

   Applications can disable this behavior by setting the :c:enumerator:`NET_IF_NO_AUTO_START` interface flag with :c:func:`net_if_flag_set`.

.. _conn_mgr_control_automations_auto_connect:

.. topic:: Automatic connect

   By default, Connection Manager will automatically connect any :ref:`bound <conn_mgr_impl_binding>` iface that becomes admin-up.

   Applications can disable this by setting the :c:enumerator:`CONN_MGR_IF_NO_AUTO_CONNECT` connectivity flag with :c:func:`conn_mgr_if_set_flag`.

.. _conn_mgr_control_automations_auto_down:

.. topic:: Automatic admin-down

   By default, Connection Manager will automatically take any bound iface admin-down if it has given up on associating.

   Applications can disable this for all ifaces by disabling the :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER_AUTO_IF_DOWN` Kconfig option, or for individual ifaces by setting the :c:enumerator:`CONN_MGR_IF_NO_AUTO_DOWN` connectivity flag with :c:func:`conn_mgr_if_set_flag`.

.. _conn_mgr_control_api:

Connectivity control API
========================

Include header file :file:`include/zephyr/net/conn_mgr_connectivity.h` to access these.

.. doxygengroup:: conn_mgr_connectivity

.. _conn_mgr_control_api_bulk:

Bulk API
--------

Connectivity control provides several bulk functions allowing all ifaces to be controlled at once.

You can restrict these functions to operate only on non-:ref:`ignored <conn_mgr_monitoring_ignoring_ifaces>` ifaces if desired.

Include header file :file:`include/zephyr/net/conn_mgr_connectivity.h` to access these.

.. doxygengroup:: conn_mgr_connectivity_bulk
