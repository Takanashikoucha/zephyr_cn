.. _conn_mgr_impl:

连接性实现
############################

.. _conn_mgr_impl_overview:

概述
========

连接性实现是技术特定模块，允许特定 Zephyr 接口支持 :ref:`连接性控制 <conn_mgr_control>`。
它们负责将通用的 :ref:`连接性控制 API <conn_mgr_control_api>` 调用翻译为硬件特定操作。
它们还负责实现标准化的 :ref:`持久性和超时 <conn_mgr_control_persistence_timeouts>` 行为。

编写符合规范的连接性实现的细节参见 :ref:`实现指南 <conn_mgr_impl_guidelines>`。

.. _conn_mgr_impl_architecture:

架构
============

:ref:`实现 API <conn_mgr_impl_api>` 允许在构建时用 :c:macro:`CONN_MGR_CONN_DEFINE` :ref:`定义 <conn_mgr_impl_defining>` 连接性实现。

这创建 :c:struct:`conn_mgr_conn_impl` 结构体的静态实例，然后存储对传入的 :c:struct:`conn_mgr_conn_api` 结构体（应填充实现回调）的引用。

定义后，可以按名称引用实现，并用 :c:macro:`CONN_MGR_BIND_CONN` 绑定到任何未绑定的接口。
确保不意外将两个连接性实现绑定到单个接口。

接口绑定后，可以在接口上调用 :ref:`连接性控制 API <conn_mgr_control_api>` 函数，
它们将被翻译为 :c:struct:`conn_mgr_conn_api` 中对应的实现函数。

绑定接口不直接修改其 :c:struct:`接口结构体 <net_if>`。

相反，创建 :c:struct:`conn_mgr_conn_binding` 的实例并追加到内部 :ref:`可迭代区段 <iterable_sections_api>`。

此绑定结构体将包含对绑定接口的引用、它绑定的连接性实现，
以及指向每接口 :ref:`上下文指针 <conn_mgr_impl_ctx>` 的指针。

然后可以遍历此可迭代区段以查明（若有）已绑定到给定接口的连接性实现。
此搜索过程由 :ref:`连接性控制 API <conn_mgr_control_api>` 中大多数函数使用。
因此，由于其相对较高的搜索成本，应谨慎调用这些函数。

单个连接性实现可绑定到多个接口。
更多细节参见 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_integration_diagram_detailed:

.. figure:: figures/integration_diagram_detailed.svg
    :alt: 连接管理器如何与 Zephyr 和应用程序集成的详细视图。
    :figclass: align-center

    连接管理器如何与 Zephyr 和应用程序集成的详细视图。

    简化版本参见 :ref:`此处 <conn_mgr_integration_diagram_simple>`。

.. _conn_mgr_impl_ctx:

上下文指针
==============

由于单个连接性实现可由若干 Zephyr 接口共享，每个绑定实例化
一个唯一于该绑定的上下文容器（:ref:`可配置类型 <conn_mgr_impl_declaring>`）。
然后每个绑定用对该容器的引用实例化，实现
然后可用其访问每接口状态信息。

参见 :ref:`conn_mgr_impl_guidelines_binding_access` 和 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_impl_defining:

定义实现
==========================

连接性实现可按如下定义：

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
   除非还 :ref:`声明上下文指针类型 <conn_mgr_impl_declaring_ctx>`，否则此不工作。

.. _conn_mgr_impl_declaring:

公开声明实现
====================================

定义后，可通过如下声明（在头文件中）使连接性实现
对其他编译单元可用：

.. code-block:: c
   :caption: ``my_connectivity_header.h``

   CONN_MGR_CONN_DECLARE_PUBLIC(MY_CONNECTIVITY_IMPL);

包含此声明的头文件须包含在需引用实现的任何编译单元中。

.. _conn_mgr_impl_declaring_ctx:

声明上下文类型
========================

为使 :c:macro:`CONN_MGR_CONN_DEFINE` 工作，须声明对应的上下文指针类型。
这是因为所有连接性绑定包含其关联上下文指针类型的 :ref:`conn_mgr_impl_ctx`。

若使用 :c:macro:`CONN_MGR_CONN_DECLARE_PUBLIC`，在声明旁声明此类型：

.. code-block:: c
   :caption: ``my_connectivity_impl.h``

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE struct my_context_type *
   CONN_MGR_CONN_DECLARE_PUBLIC(MY_CONNECTIVITY_IMPL);

然后，确保在调用 :c:macro:`CONN_MGR_CONN_DEFINE` 前包含头文件：

.. code-block:: c
   :caption: ``my_connectivity_impl.c``

   #include "my_connectivity_impl.h"

   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

否则，仅须在 :c:macro:`CONN_MGR_CONN_DEFINE` 调用前声明上下文指针类型即可：

.. code-block:: c

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE struct my_context_type *
   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

.. note::

   命名很重要。
   上下文指针类型声明须用与实现声明相同的名称，但加 ``_CTX_TYPE``。

   前例中，上下文类型名为 ``MY_CONNECTIVITY_IMPL_CTX_TYPE``，
   因为 ``MY_CONNECTIVITY_IMPL`` 用作连接性实现名称。

若连接性实现不需上下文指针，仅将类型声明为 void：

.. code-block:: c

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE void *

.. _conn_mgr_impl_binding:

将接口绑定到实现
=====================================

已定义的连接性实现可在接口的设备定义后任何位置
调用 :c:macro:`CONN_MGR_BIND_CONN` 绑定到接口：

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

连接性实现指南
=====================================

而非集中实现所有功能，连接管理器依赖每个连接性实现
单独实现许多行为和功能。

此方法允许连接管理器保持精简，并允许每个连接性实现
为这些行为选择最适合自身的方法。
然而，它依赖信任所有连接性实现将忠实实现被委托给它们的功能。

为保持所有连接性实现之间的一致性，编写自己的实现时遵循以下指南：

.. _conn_mgr_impl_guidelines_timeout_persistence:

*完全实现超时和持久性*
----------------------------------------------

所有连接性实现必须提供对 :ref:`超时和持久性 <conn_mgr_control_persistence_timeouts>` 的完整支持，
使用户可以禁用或启用这些功能，无论底层技术的固有行为如何。
换句话说，无论底层技术如何表现，你的实现必须使其
对最终用户看起来完全按照 :ref:`conn_mgr_control_persistence_timeouts` 章节指定的行为表现。

实现超时和持久性的详细技术讨论参见 :ref:`conn_mgr_impl_timeout_persistence`。

.. _conn_mgr_impl_guidelines_conformity:

*符合 API 规范*
-------------------------------

你实现的每个 :c:struct:`实现 API 函数 <conn_mgr_conn_api>`
应表现为对应连接性控制 API 函数所描述的。

例如，你对 :c:member:`conn_mgr_conn_api.connect` 的实现
应符合 :c:func:`conn_mgr_if_connect` 描述的行为。

.. _conn_mgr_impl_guidelines_preconfig:

*允许连接性预配置*
--------------------------------------

连接性实现应提供方法，使应用程序在调用
:c:func:`conn_mgr_if_connect` 之前预配置所有必要的连接参数
（例如，网络 SSID 或 PSK，如适用）。
不应需要在 :c:func:`conn_mgr_if_connect` 调用中或之后
提供此信息，尽管实现 :ref:`在未提供时应等待此信息 <conn_mgr_impl_guidelines_await_config>`。

.. _conn_mgr_impl_guidelines_await_config:

*等待有效的连接性配置*
----------------------------------------

如果由于应用程序预配置了无效的连接参数
或根本没有配置连接参数而导致网络关联失败，
这应被视为网络故障。

换句话说，即使未配置有效的连接参数，
连接性实现也不应放弃连接尝试。

相反，连接性实现应异步等待有效的连接参数
被配置，要么无限期，要么直到配置的
:ref:`连接性超时 <conn_mgr_control_timeouts>` 过期。

一个例外是如果网络接口被配置为非持久的
并且连接性实现定义了 :c:member:`conn_mgr_conn_api.has_connection_config` 的实现。

在这种情况下，为减少功耗并防止不必要的状态转换，
如果 :c:member:`conn_mgr_conn_api.has_connection_config` 返回
``false``，:c:func:`conn_mgr_if_connect` 将提前退出而不
启动接口。将发出 :c:enum:`NET_EVENT_CONN_IF_NO_CONFIGURATION` 事件
以通知订阅者配置错误。

.. _conn_mgr_impl_guidelines_iface_state_reporting:

*实现接口状态报告*
---------------------------------

所有连接性实现必须保持绑定接口状态最新。

具体来说：

* 在 :c:member:`绑定初始化 <conn_mgr_conn_api.init>` 期间将接口设置为休眠、载波关闭或两者。

  * 关于接口载波和休眠状态的细节参见 :ref:`net_if_interface_state_management`。

* 更新休眠和载波状态，使接口（仅当）关联完成且连接性就绪时为非休眠和载波开启。
* 一旦检测到服务中断，立即将接口设置为休眠或载波关闭。

  * 对于服务通常间歇性的网络技术，可以接受将此门控在小型超时（与连接超时分开）之后。

* 如果技术还处理 IP 分配，确保那些 IP 地址 :ref:`分配给接口 <net_if_interface_ip_management>`。

.. note::

   接口状态更新不一定需要由连接性实现直接执行。

   例如：

   * 如果接口使用 :ref:`DHCP <dhcpv4_interface>`，则不需要 IP 分配。
   * 如果底层 :ref:`L2 实现 <net_l2_interface>` 已经更新接口休眠，则连接性实现不需要更新接口休眠。

.. _conn_mgr_impl_guidelines_iface_state_writeonly:

*不要将接口状态用作实现状态*
------------------------------------------------

Zephyr 接口可能从其他线程访问而不尊重绑定互斥锁。
因此，Zephyr 接口状态可能在连接性实现回调期间不可预测地变化。

因此，不要基于接口状态实现行为。

保持接口状态更新以反映网络可用性，但不要出于任何目的读取接口状态。

如果需要跟踪休眠或 IP 分配，使用存储在 :ref:`上下文指针 <conn_mgr_impl_ctx>` 中的单独状态变量。

.. _conn_mgr_impl_guidelines_non_interference:

*保持非干扰*
------------------------

连接性实现不应阻止应用程序直接与关联的技术特定 API 交互。

换句话说，应用程序应能直接使用你的底层技术而不破坏你的连接性实现。

如果绝对需要此例外，应限制在特定 API 调用并应记录。

.. note::

   虽然连接性实现不得破坏，但如果应用程序尝试直接控制关联状态，
   实现具有潜在意外行为是可接受的。

   例如，如果应用程序直接指示底层技术断开关联，
   连接性实现将此解释为意外连接丢失并立即尝试重新关联是可接受的。

.. _conn_mgr_impl_guidelines_non_blocking:

*保持非阻塞*
---------------------

所有连接性实现回调应是非阻塞的。

例如，对 :c:member:`conn_mgr_conn_api.connect` 的调用应
启动连接过程并立即返回。

一个例外是 :c:member:`conn_mgr_conn_api.init`，其实现被允许阻塞。

然而，请记住在此回调期间阻塞将延迟系统初始化，
因此仍考虑将耗时任务卸载到后台线程。

.. _conn_mgr_impl_guidelines_immediate_api_readiness:

*使 API 立即就绪*
----------------------------

连接性实现必须在 :c:member:`conn_mgr_conn_api.init` 之后
立即准备接收 API 调用。

例如，对 :c:member:`conn_mgr_conn_api.connect` 的调用
必须最终导致关联尝试，即使在 :c:member:`conn_mgr_conn_api.init` 后立即调用。

如果底层技术在 :c:member:`conn_mgr_conn_api.init` 调用时
无法立即准备接收连接命令，对 :c:member:`conn_mgr_conn_api.connect` 的调用
必须以非阻塞方式排队，然后在就绪时执行。

.. _conn_mgr_impl_guidelines_context_pointer:

*不要在上下文指针外存储状态信息*
------------------------------------------------------------

连接管理器为每个绑定提供上下文指针。

连接性实现应在此上下文指针中存储所有状态信息。

唯一例外是旨在仅绑定到单个接口的连接性实现。
此类实现可以使用静态声明的状态。

参见 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_impl_guidelines_iface_access:

*仅通过绑定结构体访问接口*
--------------------------------------------

不要使用静态声明的接口或外部获取接口引用。

例如，不要使用 :c:func:`net_if_get_default` 并假设绑定的接口
将是默认接口。

相反，始终使用相关 :c:struct:`绑定结构体 <conn_mgr_conn_binding>`
提供的 :c:member:`接口指针 <conn_mgr_conn_binding.iface>`。
参见 :ref:`conn_mgr_impl_guidelines_binding_access`。

.. _conn_mgr_impl_guidelines_bindings_optional:

*使实现在编译时可选*
-----------------------------------------------

连接性实现应提供 Kconfig 选项，
在不影响绑定接口可用性的情况下启用或禁用实现。

换句话说，应能配置包含连接管理器的构建，
以及本应绑定到实现的接口，但不包含实现本身
或其绑定。

.. _conn_mgr_impl_guidelines_no_instancing:

*不要实例化实现*
---------------------------------

不要为每个要绑定的接口声明单独的
连接性实现。

相反，将一个全局连接性实现绑定到你所有的接口，
并使用上下文指针存储与单个接口相关的状态。

参见 :ref:`conn_mgr_impl_guidelines_binding_access` 和 :ref:`conn_mgr_impl_guidelines_iface_access`。

.. _conn_mgr_impl_guidelines_binding_access:

*不要在不锁定绑定的情况下访问绑定*
---------------------------------------------

绑定可能被多个线程随机访问和修改，
因此在不先 :c:func:`锁定 <conn_mgr_binding_lock>` 的情况下
修改或读取绑定可能导致不可预测的行为。

这适用于绑定的所有后代，
包括 :ref:`上下文容器 <conn_mgr_impl_ctx>` 中的任何内容。

确保在访问完绑定后 :c:func:`解锁 <conn_mgr_binding_unlock>` 绑定。

.. note::

   此规则的一个可能例外是如果相关资源
   固有地是线程安全的。

   然而，小心利用此例外。
   仍可能创建竞争条件，例如同时访问多个线程安全资源时。

   因此，建议始终锁定绑定，
   无论被访问的资源是否固有地是线程安全的。

.. _conn_mgr_impl_guidelines_support_builtins:

*不要禁用内置功能*
----------------------------------

不要尝试阻止使用内置功能
（如 :ref:`conn_mgr_control_persistence_timeouts` 或 :ref:`conn_mgr_control_automations`）。

所有连接性实现必须完全支持这些功能。
实现不得尝试强制某些功能始终启用或始终禁用。

.. _conn_mgr_impl_guidelines_trigger_events:

*触发连接性控制事件*
-------------------------------------

连接性控制 :ref:`网络管理 <net_mgmt_interface>` 事件
不会由连接管理器自动触发。

连接性实现必须自行触发这些事件。

当发生连接 :ref:`超时 <conn_mgr_control_timeouts>` 时
触发 :c:macro:`NET_EVENT_CONN_CMD_IF_TIMEOUT`。
细节参见 :ref:`conn_mgr_control_events_timeout`。

当发生致命的（不可恢复的）连接错误时
触发 :c:macro:`NET_EVENT_CONN_IF_FATAL_ERROR`。
细节参见 :ref:`conn_mgr_control_events_fatal_error`。

触发网络管理事件的细节参见 :ref:`net_mgmt_interface`。

.. _conn_mgr_impl_timeout_persistence:

实现超时和持久性
====================================

首先，参见 :ref:`conn_mgr_control_persistence_timeouts`
了解超时和持久性预期行为的高级描述。

连接性实现必须完全符合该描述，
无论底层连接性技术的行为如何。

有时这意味着在连接性实现中编写额外逻辑
来模拟某些行为。以下章节讨论各种常见边缘情况
和细微之处以及如何处理它们。

.. _conn_mgr_impl_tp_inherent_persistence:

*固有持久性技术*
------------------------------------

如果底层技术在连接丢失或失败后
自动尝试重新连接或重试连接，
连接性实现必须在它们与超时或持久性设置冲突时
手动取消此类尝试。

例如：

  * 如果底层技术在失去连接后自动尝试重新连接，
    并且接口的持久性被禁用，
    连接性实现应立即取消此重新连接尝试。
  * 如果接口的连接尝试超时，
    而底层技术没有内置超时，
    连接性实现必须通过手动取消连接尝试
    来模拟超时。

.. _conn_mgr_impl_tp_inherent_nonpersistence:

*放弃连接尝试的技术*
---------------------------------------------------

如果底层技术没有机制重试连接尝试，
或会在用户配置的超时之前放弃，
或不会在连接丢失后重新连接，
连接性实现必须手动重新请求连接
以抵消这些偏差。

* 如果你的底层技术不是持久的，
  你必须在启用持久性时手动触发重新连接尝试。
* 如果你的底层技术不支持超时，
  你必须在启用超时时手动取消连接尝试。
* 如果你的底层技术强制超时，
  你必须在该超时短于连接管理器超时时
  手动触发新的连接尝试。

.. _conn_mgr_impl_tp_assoc_retry:

*带关联重试的技术*
-------------------------------------

许多底层技术通常不在单次尝试中关联。

相反，这些底层技术可能需要连续进行
多个背靠背的关联尝试，通常带小型延迟。

在这些情况下，连接性实现应将
此系列背靠背的关联子尝试视为
单个统一的连接尝试。

例如，在子尝试失败后，禁用持久性
不应阻止进一步的子尝试，
因为它们都算作一个单一的整体连接尝试。
参见 :ref:`conn_mgr_impl_tp_persistence_during_connect`。

一系列失败的子尝试何时应被视为
连接尝试整体的失败由每个实现决定。

如果连接尝试超过此阈值，
但配置的超时尚未过期，
或没有超时，子尝试应继续。

.. _conn_mgr_impl_tp_persistence_during_connect:

*连接尝试期间的持久性*
----------------------------------------

持久性不应影响连接尝试期间
实现行为的任何方面。
持久性应仅影响连接丢失后
是否自动触发连接尝试。

配置的超时应完全决定是否
应执行连接重试。

.. _conn_mgr_impl_api:

实现 API
==================

包含头文件 :file:`include/zephyr/net/conn_mgr_connectivity_impl.h`
以访问这些。

仅供连接性实现使用。

.. doxygengroup:: conn_mgr_connectivity_impl
