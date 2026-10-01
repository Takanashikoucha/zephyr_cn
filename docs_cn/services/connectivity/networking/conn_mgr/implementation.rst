.. _conn_mgr_impl:

Connectivity Implementations
############################

.. _conn_mgr_impl_overview:

Overview
========

Connectivity implementations 为 technology-specific modules（允许特定 Zephyr ifaces 支持 :ref:`Connectivity Control <conn_mgr_control>`。其负责将 generic :ref:`connectivity control API <conn_mgr_control_api>` calls 翻译为 hardware-specific operations。其还负责实现标准化的 :ref:`persistence 和 timeout <conn_mgr_control_persistence_timeouts>` behaviors。

编写符合规范的 connectivity implementations 的细节参见 :ref:`implementation guidelines <conn_mgr_impl_guidelines>`。

.. _conn_mgr_impl_architecture:

Architecture
============

:ref:`implementation API <conn_mgr_impl_api>` 允许在 build time 用 :c:macro:`CONN_MGR_CONN_DEFINE` :ref:`定义 <conn_mgr_impl_defining>` connectivity implementations。

这创建 :c:struct:`conn_mgr_conn_impl` struct 的静态 instance（然后存储对传入 :c:struct:`conn_mgr_conn_api` struct（应填充 implementation callbacks）的引用。

定义后（可按名称引用 implementations（并用 :c:macro:`CONN_MGR_BIND_CONN` 绑定到任何 unbound iface。确保不意外将两个 connectivity implementations 绑定到单个 iface。

Iface 绑定后（可在 iface 上调用 :ref:`connectivity control API <conn_mgr_control_api>` functions（其将翻译为 :c:struct:`conn_mgr_conn_api` 中对应的 implementation functions。

绑定 iface 不直接修改其 :c:struct:`iface struct <net_if>`。

相反（创建 :c:struct:`conn_mgr_conn_binding` 的 instance（并追加到内部 :ref:`iterable section <iterable_sections_api>`。

此 binding structure 将包含对绑定的 iface（其绑定的 connectivity implementation（以及指向 per-iface :ref:`context pointer <conn_mgr_impl_ctx>` 的 pointer。

然后可遍历此 iterable section 以查明（若有）已绑定到给定 iface 的 connectivity implementation。此搜索过程由 :ref:`connectivity control API <conn_mgr_control_api>` 中大多数 functions 使用。因此（由于其相对较高的搜索成本（应谨慎调用这些 functions。

单个 connectivity implementation 可绑定到多个 ifaces。更多细节参见 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_integration_diagram_detailed:

.. figure:: figures/integration_diagram_detailed.svg
    :alt: A detailed view of how Connection Manager integrates with Zephyr and the application.
    :figclass: align-center

    A detailed view of how Connection Manager integrates with Zephyr and the application.

    简化版本参见 :ref:`here <conn_mgr_integration_diagram_simple>`。

.. _conn_mgr_impl_ctx:

Context Pointer
===============

由于单个 connectivity implementation 可由若干 Zephyr ifaces 共享（每个 binding 实例化（:ref:`configurable type <conn_mgr_impl_declaring>`）唯一于该 binding 的 context container。然后每个 binding 用对该 container 的引用实例化（implementations 然后可用其访问 per-iface state 信息。

参见 :ref:`conn_mgr_impl_guidelines_binding_access` 和 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_impl_defining:

Defining an implementation
==========================

Connectivity implementation 可按如下定义：

.. code-block:: c

   /* Create the API implementation functions */
   int my_connect_impl(struct conn_mgr_conn_binding *const binding) {
           /* Cause your underlying technology to associate */
   }
   int my_disconnect_impl(struct conn_mgr_conn_binding *const binding) {
           /* Cause your underlying technology to disassociate */
   }
   void my_init_impl(struct conn_mgr_conn_binding *const binding) {
           /* Perform any required initialization for your underlying technology */
   }

   /* Declare the API struct */
   static struct conn_mgr_conn_api my_impl_api = {
           .connect = my_connect_impl,
           .disconnect = my_disconnect_impl,
           .init = my_init_impl,
           /* ... so on */
   };

   /* Define the implementation (named MY_CONNECTIVITY_IMPL) */
   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

.. note::
   除非还 :ref:`declare the context pointer type <conn_mgr_impl_declaring_ctx>`（否则此不工作。

.. _conn_mgr_impl_declaring:

Declaring an implementation publicly
====================================

定义后（可通过如下声明（在 header file 中）使 connectivity implementation 对其他 compilation units 可用：

.. code-block:: c
   :caption: ``my_connectivity_header.h``

   CONN_MGR_CONN_DECLARE_PUBLIC(MY_CONNECTIVITY_IMPL);

包含此声明的 header file 须包含在需引用 implementation 的任何 compilation units 中。

.. _conn_mgr_impl_declaring_ctx:

Declaring a context type
========================

为使 :c:macro:`CONN_MGR_CONN_DEFINE` 工作（须声明对应的 context pointer type。这是因为所有 connectivity bindings 包含其关联 context pointer type 的 :ref:`conn_mgr_impl_ctx`。

若使用 :c:macro:`CONN_MGR_CONN_DECLARE_PUBLIC`（在声明旁声明此 type：

.. code-block:: c
   :caption: ``my_connectivity_impl.h``

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE struct my_context_type *
   CONN_MGR_CONN_DECLARE_PUBLIC(MY_CONNECTIVITY_IMPL);

然后（确保在调用 :c:macro:`CONN_MGR_CONN_DEFINE` 前包含 header file：

.. code-block:: c
   :caption: ``my_connectivity_impl.c``

   #include "my_connectivity_impl.h"

   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

否则（仅须在 :c:macro:`CONN_MGR_CONN_DEFINE` 调用前声明 context pointer type 即可：

.. code-block:: c

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE struct my_context_type *
   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

.. note::

   命名很重要。
   Context pointer type 声明须用与 implementation 声明相同的 name（但加 ``_CTX_TYPE``。

   前例中（context type 名为 ``MY_CONNECTIVITY_IMPL_CTX_TYPE``（因为 ``MY_CONNECTIVITY_IMPL`` 用作 connectivity implementation name。

若 connectivity implementation 不需 context pointer（仅将 type 声明为 void：

.. code-block:: c

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE void *

.. _conn_mgr_impl_binding:

Binding an iface to an implementation
=====================================

已定义的 connectivity implementation 可在 iface 的 device 定义后任何位置调用 :c:macro:`CONN_MGR_BIND_CONN` 绑定到 iface：

.. code-block:: c

	/* Define an iface */
	NET_DEVICE_INIT(my_iface,
		/* ... the specifics here don't matter ... */
	);

	/* Now bind MY_CONNECTIVITY_IMPL to that iface --
	 * the name used should match with the above
	 */
	CONN_MGR_BIND_CONN(my_iface, MY_CONNECTIVITY_IMPL);

.. _conn_mgr_impl_guidelines:

Connectivity implementation guidelines
======================================

而非集中实现所有 features（Connection Manager 依赖每个 connectivity implementation 单独实现许多 behaviors 和 features。

此 approach 允许 Connection Manager 保持精简（并允许每个 connectivity implementation 为这些 behaviors 选择最适合自身的 approach。然而（其依赖信任（所有 connectivity implementations 将忠实实现被委托给它们的 features。

为保持所有 connectivity implementations 之间的一致性（编写自己的 implementation 时遵循以下 guidelines：

.. _conn_mgr_impl_guidelines_timeout_persistence:

*完全实现 timeout 和 persistence 行为*
----------------------------------------

每个 connectivity implementation 须完整实现 :ref:`persistence 和 timeout <conn_mgr_control_persistence_timeouts>` behaviors。Connection Manager 不提供默认实现（也不回退到任何默认行为。

*Persistence*

Persistence 须实现为在 connection loss 后自动触发新的 connection attempt。Implementation 须负责决定何时触发新的 connection attempt（以及是否触发。

*Timeout*

Timeout 须实现为在指定时长后放弃 connection attempt。Implementation 须负责决定 timeout 何时过期（以及过期后做什么。

.. _conn_mgr_impl_guidelines_no_instancing:

*不要为每个 iface 实例化 implementation*
----------------------------------------

单个 connectivity implementation 实例可（且应）绑定到多个 ifaces。不要为每个 iface 创建新 implementation 实例。

.. _conn_mgr_impl_guidelines_binding_access:

*通过 binding 访问 per-iface 状态*
----------------------------------------

Per-iface 状态须通过 binding 的 context pointer 访问。不要使用全局状态或 static variables 存储 per-iface 状态。

.. _conn_mgr_impl_guidelines_retry_threshold:

*Retry 阈值*
------------

Implementation 须定义何为 connection attempt 失败。连续 sub-attempts 失败达到阈值后（应视为 connection attempt 整体失败。

若 connection attempt 超过此阈值（但配置的 timeout 尚未过期（或无 timeout（sub-attempts 应继续。

.. _conn_mgr_impl_tp_persistence_during_connect:

*Connection attempts 期间的 persistence*
----------------------------------------

Persistence 不应影响 connection attempt 期间 implementation 行为的任何方面。Persistence 应仅影响 connection loss 后是否自动触发 connection attempts。

配置的 timeout 应完全决定是否应执行 connection retry。

.. _conn_mgr_impl_api:

Implementation API
==================

包含 header file :file:`include/zephyr/net/conn_mgr_connectivity_impl.h` 以访问这些。

仅供 connectivity implementations 使用。

.. doxygengroup:: conn_mgr_connectivity_impl
