.. _conn_mgr_impl:

Connectivity
Implementations
############################

.. _conn_mgr_impl_overview:

Overview
========

Connectivity
implementations
是
technology
specific
的
modules
它们
允许
特定
的
Zephyr
ifaces
support
:ref:`Connectivity
Control
<conn_mgr_control>`。
它们
负责
将
generic
的
:ref:`connectivity
control
API
<conn_mgr_control_api>`
calls
translate
到
hardware
specific
的
operations。
它们
也
负责
implement
standardized
的
:ref:`persistence
and
timeout
<conn_mgr_control_persistence_timeouts>`
behaviors。

参考
:ref:`implementation
guidelines
<conn_mgr_impl_guidelines>`
获取
关于
write
conformant
的
connectivity
implementations
的
details。

.. _conn_mgr_impl_architecture:

Architecture
============

:ref:`implementation
API
<conn_mgr_impl_api>`
允许
connectivity
implementations
在
build
time
用
:c:macro:`CONN_MGR_CONN_DEFINE`
被
:ref:`defined
<conn_mgr_impl_defining>`。

这
create
一
个
:c:struct:`conn_mgr_conn_impl`
struct
的
static
instance
它
然后
store
对
passed
in
的
:c:struct:`conn_mgr_conn_api`
struct
（应该
被
populated
with
implementation
callbacks）
的
reference。

一
旦
defined
你
可以
用
name
reference
implementations
并
用
:c:macro:`CONN_MGR_BIND_CONN`
bind
它们
到
任何
unbound
的
iface。
注意
不要
accidentally
bind
两
个
connectivity
implementations
到
单
个
iface。

一
旦
iface
被
bound
:ref:`connectivity
control
API
<conn_mgr_control_api>`
functions
可以
在
iface
上
被
called
它们
将
被
translate
到
:c:struct:`conn_mgr_conn_api`
中
对应
的
implementation
functions。

Bind
一
个
iface
不
直接
modify
它
的
:c:struct:`iface
struct
<net_if>`。

相反
一
个
:c:struct:`conn_mgr_conn_binding`
的
instance
被
created
并
appended
到
internal
的
:ref:`iterable
section
<iterable_sections_api>`。

这
个
binding
structure
将
contain
对
bound
的
iface、
它
bound
到
的
connectivity
implementation
以及
per
iface
的
:ref:`context
pointer
<conn_mgr_impl_ctx>`
的
pointer
的
references。

这
个
iterable
section
然后
可以
被
iterated
over
用于
find
out
什么
（如果
有
）
connectivity
implementation
被
bound
到
给定
的
iface。
这
个
search
process
被
:ref:`connectivity
control
API
<conn_mgr_control_api>`
中
大多数
的
functions
used。
因此
这些
functions
应该
被
sparingly
called
因为
它们
相对
较高
的
search
cost。


.. note::

   以下为原文（待翻译）


   For instance, if an application directly instructs an underlying technology to disassociate, it would be acceptable for the connectivity implementation to interpret this as an unexpected connection loss and immediately attempt to re-associate.

.. _conn_mgr_impl_guidelines_non_blocking:

*Remain non-blocking*
---------------------

All connectivity implementation callbacks should be non-blocking.

For instance, calls to :c:member:`conn_mgr_conn_api.connect` should initiate a connection process and return immediately.

One exception is :c:member:`conn_mgr_conn_api.init`, whose implementations are permitted to block.

However, bear in mind that blocking during this callback will delay system init, so still consider offloading time-consuming tasks to a background thread.

.. _conn_mgr_impl_guidelines_immediate_api_readiness:

*Make API immediately ready*
----------------------------

Connectivity implementations must be ready to receive API calls immediately after :c:member:`conn_mgr_conn_api.init`.

For instance, a call to :c:member:`conn_mgr_conn_api.connect` must eventually lead to an association attempt, even if called immediately after :c:member:`conn_mgr_conn_api.init`.

If the underlying technology cannot be made ready for connect commands immediately when :c:member:`conn_mgr_conn_api.init` is called, calls to :c:member:`conn_mgr_conn_api.connect` must be queued in a non-blocking fashion, and then executed later when ready.

.. _conn_mgr_impl_guidelines_context_pointer:

*Do not store state information outside the context pointer*
------------------------------------------------------------

Connection Manager provides a context pointer to each binding.

Connectivity implementations should store all state information in this context pointer.

The only exception is connectivity implementations that are meant to be bound to only a single iface.
Such implementations may use statically declared state instead.

See also :ref:`conn_mgr_impl_guidelines_no_instancing`.

.. _conn_mgr_impl_guidelines_iface_access:

*Access ifaces only through binding structs*
--------------------------------------------

Do not use statically declared ifaces or externally acquire references to ifaces.

For example, do not use :c:func:`net_if_get_default` under the assumption that the bound iface will be the default iface.

Instead, always use the :c:member:`iface pointer <conn_mgr_conn_binding.iface>` provided by the relevant :c:struct:`binding struct <conn_mgr_conn_binding>`.
See also :ref:`conn_mgr_impl_guidelines_binding_access`.

.. _conn_mgr_impl_guidelines_bindings_optional:

*Make implementations optional at compile-time*
-----------------------------------------------

Connectivity implementations should provide a Kconfig option to enable or disable the implementation without affecting bound iface availability.

In other words, it should be possible to configure builds that include Connectivity Manager, as well as the iface that would have been bound to the implementation, but not the implementation itself, nor its binding.

.. _conn_mgr_impl_guidelines_no_instancing:

*Do not instance implementations*
---------------------------------

Do not declare a separate connectivity implementation for every iface you are going to bind to.

Instead, bind one global connectivity implementation to all of your ifaces, and use the context pointer to store state relevant to individual ifaces.

See also :ref:`conn_mgr_impl_guidelines_binding_access` and :ref:`conn_mgr_impl_guidelines_iface_access`.

.. _conn_mgr_impl_guidelines_binding_access:

*Do not access bindings without locking them*
---------------------------------------------

Bindings may be accessed and modified at random by multiple threads, so modifying or reading from a binding without first :c:func:`locking it <conn_mgr_binding_lock>` may lead to unpredictable behavior.

This applies to all descendents of the binding, including anything in the :ref:`context container <conn_mgr_impl_ctx>`.

Make sure to :c:func:`unlock <conn_mgr_binding_unlock>` the binding when you are done accessing it.

.. note::

   A possible exception to this rule is if the resource in question is inherently thread-safe.

   However, be careful taking advantage of this exception.
   It may still be possible to create a race condition, for instance when accessing multiple thread-safe resources simultaneously.

   Therefore, it is recommended to simply always lock the binding, whether or not the resource being accessed is inherently thread-safe.

.. _conn_mgr_impl_guidelines_support_builtins:

*Do not disable built-in features*
----------------------------------

Do not attempt to prevent the use of built-in features (such as :ref:`conn_mgr_control_persistence_timeouts` or :ref:`conn_mgr_control_automations`).

All connectivity implementations must fully support these features.
Implementations must not attempt to force certain features to be always enabled or always disabled.

.. _conn_mgr_impl_guidelines_trigger_events:

*Trigger connectivity control events*
-------------------------------------

Connectivity control :ref:`network management <net_mgmt_interface>` events are not triggered automatically by Connection Manager.

Connectivity implementations must trigger these events themselves.

Trigger :c:macro:`NET_EVENT_CONN_CMD_IF_TIMEOUT` when a connection :ref:`timeout <conn_mgr_control_timeouts>` occurs.
See :ref:`conn_mgr_control_events_timeout` for details.

Trigger :c:macro:`NET_EVENT_CONN_IF_FATAL_ERROR` when a fatal (non-recoverable) connection error occurs.
See :ref:`conn_mgr_control_events_fatal_error` for details.

See :ref:`net_mgmt_interface` for details on firing network management events.

.. _conn_mgr_impl_timeout_persistence:

Implementing timeouts and persistence
=====================================

First, see :ref:`conn_mgr_control_persistence_timeouts` for a high-level description of the expected behavior of timeouts and persistence.

Connectivity implementations must fully conform to that description, regardless of the behavior of the underlying connectivity technology.

Sometimes this means writing extra logic in the connectivity implementation to fake certain behaviors.
The following sections discuss various common edge-cases and nuances and how to handle them.

.. _conn_mgr_impl_tp_inherent_persistence:

*Inherently persistent technologies*
------------------------------------

If the underlying technology automatically attempts to reconnect or retry connection after connection loss or failure, the connectivity implementation must manually cancel such attempts when they are in conflict with timeout or persistence settings.

For example:

  * If the underlying technology automatically attempts to reconnect after losing connection, and persistence is disabled for the iface, the connectivity implementation should immediately cancel this reconnection attempt.
  * If a connection attempt times out on an iface whose underlying technology does not have a built-in timeout, the connectivity implementation must simulate a timeout by cancelling the connection attempt manually.

.. _conn_mgr_impl_tp_inherent_nonpersistence:

*Technologiess that give up on connection attempts*
---------------------------------------------------

If the underlying technology has no mechanism to retry connection attempts, or would give up on them before the user-configured timeout, or would not reconnect after connection loss, the connectivity implementation must manually re-request connection to counteract these deviances.

* If your underlying technology is not persistent, you must manually trigger reconnect attempts when persistence is enabled.
* If your underlying technology does not support a timeout, you must manually cancel connection attempts if the timeout is enabled.
* If your underlying technology forces a timeout, you must manually trigger a new connection attempts if that timeout is shorter than the Connection Manager timeout.

.. _conn_mgr_impl_tp_assoc_retry:

*Technologies with association retry*
-------------------------------------

Many underlying technologies do not usually associate in a single attempt.

Instead, these underlying technologies may need to make multiple back-to-back association attempts in a row, usually with a small delay.

In these situations, the connectivity implementation should treat this series of back-to-back association sub-attempts as a single unified connection attempt.

For instance, after a sub-attempt failure, persistence being disabled should not prevent further sub-attempts, since they all count as one single overall connection attempt.
See also :ref:`conn_mgr_impl_tp_persistence_during_connect`.

At which point a series of failed sub-attempts should be considered a failure of the connection attempt as a whole is up to each implementation to decide.

If the connection attempt crosses this threshold, but the configured timeout has not yet elapsed, or there is no timeout, sub-attempts should continue.

.. _conn_mgr_impl_tp_persistence_during_connect:

*Persistence during connection attempts*
----------------------------------------

Persistence should not affect any aspect of implementation behavior during a connection attempt.
Persistence should only affect whether or not connection attempts are automatically triggered after a connection loss.

The configured timeout should fully determine whether connection retry should be performed.

.. _conn_mgr_impl_api:

Implementation API
==================

Include header file :file:`include/zephyr/net/conn_mgr_connectivity_impl.h` to access these.

Only for use by connectivity implementations.

.. doxygengroup:: conn_mgr_connectivity_impl
