.. _net_mgmt_interface:

Network Management
##################

.. contents::
    :local:
    :depth: 2

Overview
********

Network Management APIs 允许 applications（以及 network layer 代码本身）在 IP stack 的任何层调用定义的 network routines（或接收相关 network events 的通知。例如（用这些 APIs（application 代码可请求在 Wi-Fi 或 Bluetooth-based network interface 上执行 scan（或请求在 network interface IP address 变化时接收通知。

Network Management API 实现设计为通过 build time 消除未使用的 management routines 的代码以节省 memory。不使用 network management procedures 的 distinct 和静态定义的 APIs。相反（用 :c:macro:`NET_MGMT_REGISTER_REQUEST_HANDLER` macro 注册定义的 procedure handlers。Procedure requests 通过单个 :c:func:`net_mgmt` API 执行（其调用对应 request 的注册 handler。

当前实现为 experimental（可能在未来 releases 中变化和改进。

Requesting a defined procedure
******************************

所有 network management requests 的形式为 ``net_mgmt(mgmt_request, ...)``。``mgmt_request`` parameter 为 bit mask（指示目标 stack layer（是否隐含 ``net_if`` 对象（以及请求的特定 management procedure。可用的 procedure requests 取决于 stack 中实现了什么。

为避免额外开销（所有 :c:func:`net_mgmt` calls 为直接调用。虽然这可能在未来 release 中变化（但不影响此 function 的 users。

.. _net_mgmt_listening:

Listening to network events
***************************

可通过注册 callback function（并指定用于过滤 callback 调用时机的 event 集来接收 network events 的通知。Callback 对 layer 和 code 的对须唯一（而 command 部分为 events 的 mask。

Runtime 有两个 functions 可用：注册 callback function 的 :c:func:`net_mgmt_add_event_callback`（以及注销 callback 的 :c:func:`net_mgmt_del_event_callback`。Helper function :c:func:`net_mgmt_init_event_callback` 可用于简化 callback structure 的初始化。

此外（:c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER` 可用于在 compile time 注册 callback handler。

当发生匹配 callback 的 event set 的 event 时（关联的 callback function 用实际 event code 调用。这使得（若需要（不同 events 可由同一 callback function 处理。

.. warning::

   Event set 过滤对具有相同 layer 和 layer code 的 events 允许 false positives。Callback handler function **必须**将 event code（作为 argument 传递）与其将处理的具体 network events 对照检查（**无论**传递给 :c:func:`net_mgmt_init_event_callback` 的 set 中有多少 events。

   注意为接收来自多个 layers 的 events（须注册多个 listeners（每个监听的 layer 一个。Callback handler function 可在不同 layer events 之间共享。

   （False positives 可对具有相同 layer 和 layer code 的 events 发生。）

示例如下。

.. code-block:: c

	/*
	 * Set of events to handle.
	 * See e.g. include/zephyr/net/net_event.h for some NET_EVENT_xxx values.
	 */
	#define EVENT_IFACE_SET (NET_EVENT_IF_xxx | NET_EVENT_IF_yyy)
	#define EVENT_IPV4_SET (NET_EVENT_IPV4_xxx | NET_EVENT_IPV4_yyy)

	struct net_mgmt_event_callback iface_callback;
	struct net_mgmt_event_callback ipv4_callback;

	void callback_handler(struct net_mgmt_event_callback *cb,
			      uint64_t mgmt_event,
			      struct net_if *iface)
	{
		if (mgmt_event == NET_EVENT_IF_xxx) {
			/* Handle NET_EVENT_IF_xxx */
		} else if (mgmt_event == NET_EVENT_IF_yyy) {
			/* Handle NET_EVENT_IF_yyy */
		} else if (mgmt_event == NET_EVENT_IPV4_xxx) {
			/* Handle NET_EVENT_IPV4_xxx */
		} else if (mgmt_event == NET_EVENT_IPV4_yyy) {
			/* Handle NET_EVENT_IPV4_yyy */
		} else {
			/* Spurious (false positive) invocation. */
		}
	}

	void register_cb(void)
	{
		net_mgmt_init_event_callback(&iface_callback, callback_handler,
					     EVENT_IFACE_SET);
		net_mgmt_init_event_callback(&ipv4_callback, callback_handler,
					     EVENT_IPV4_SET);
		net_mgmt_add_event_callback(&iface_callback);
		net_mgmt_add_event_callback(&ipv4_callback);
	}

或类似地用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER`。

.. note::

   ``info`` 和 ``info_length`` arguments 仅当启用 :kconfig:option:`CONFIG_NET_MGMT_EVENT_INFO` 时可用。否则这些为 ``NULL`` 和 zero。

.. code-block:: c

	/*
	 * Set of events to handle.
	 */
	#define EVENT_IFACE_SET (NET_EVENT_IF_xxx | NET_EVENT_IF_yyy)
	#define EVENT_IPV4_SET (NET_EVENT_IPV4_xxx | NET_EVENT_IPV4_yyy)

	static void event_handler(uint64_t mgmt_event, struct net_if *iface,
				  void *info, size_t info_length,
				  void *user_data)
	{
		if (mgmt_event == NET_EVENT_IF_xxx) {
			/* Handle NET_EVENT_IF_xxx */
		} else if (mgmt_event == NET_EVENT_IF_yyy) {
			/* Handle NET_EVENT_IF_yyy */
		} else if (mgmt_event == NET_EVENT_IPV4_xxx) {
			/* Handle NET_EVENT_IPV4_xxx */
		} else if (mgmt_event == NET_EVENT_IPV4_yyy) {
			/* Handle NET_EVENT_IPV4_yyy */
		} else {
			/* Spurious (false positive) invocation. */
		}
	}

	NET_MGMT_REGISTER_EVENT_HANDLER(iface_event_handler, EVENT_IFACE_SET,
					event_handler, NULL);
	NET_MGMT_REGISTER_EVENT_HANDLER(ipv4_event_handler, EVENT_IPV4_SET,
					event_handler, NULL);

可监听的可用 generic core events 参见 :zephyr_file:`include/zephyr/net/net_event.h`。


Defining a network management procedure
***************************************

可通过定义 handler（并用关联的 mgmt_request code 注册来提供特定于 stack 实现的额外 management procedures。

Management request codes 根据目标 layer 或（若 l2 为 layer）甚至 technology 在相关位置定义。例如（所有 IP layer management request codes 可在 :zephyr_file:`include/zephyr/net/net_event.h` header file 中找到。但 L2 technology（如 Ethernet）的情况下（这些可在 :zephyr_file:`include/zephyr/net/ethernet.h` 找到。

按此 signature 建模定义 handler：

.. code-block:: c

   static int your_handler(uint64_t mgmt_event, struct net_if *iface,
                           void *data, size_t len);

然后用关联的 mgmt_request code 注册：

.. code-block:: c

   NET_MGMT_REGISTER_REQUEST_HANDLER(<mgmt_request code>, your_handler);

此新 management procedure 然后可用以下调用：

.. code-block:: c

   net_mgmt(<mgmt_request code>, ...);


Signaling a network event
*************************

可用 :c:func:`net_mgmt_event_notify` function 信号特定 network event（并提供 network event code。细节参见 :zephyr_file:`include/zephyr/net/net_mgmt.h`。与 management request code 一样（event code 也可在特定 L2 technology mgmt headers 找到（例如（若 802.15.4 L2 为想监听 events 的 technology（:zephyr_file:`include/zephyr/net/ieee802154_mgmt.h` 将为此处的正确位置。

API Reference
*************

.. doxygengroup:: net_mgmt
