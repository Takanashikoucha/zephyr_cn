.. _net_mgmt_interface:

网络管理
##################

.. contents::
    :local:
    :depth: 2

概述
********

网络管理 API 允许应用程序，以及网络
层代码本身，在 IP 栈的任何层级调用定义好的网络例程，
或者接收相关网络事件的通告。例如，使用这些 API，
应用代码可以请求对基于 Wi-Fi 或蓝牙的网络接口
执行扫描，或者在网络接口 IP 地址发生变化时
请求接收通告。

网络管理 API 的实现旨在通过
在编译期消除未使用的管理例程代码来节省内存。
不会使用用于网络管理
流程的独立且静态定义的 API。
相反，定义的流程处理器
通过 :c:macro:`NET_MGMT_REGISTER_REQUEST_HANDLER`
宏进行注册。流程请求通过单一的 :c:func:`net_mgmt` API
发出，该 API 会调用与对应请求相关联的已注册处理器。

当前实现是实验性的，
在未来版本中可能发生变化并改进。

请求一个已定义的流程
******************************

所有网络管理请求的形式都是
``net_mgmt(mgmt_request, ...)``。``mgmt_request`` 参数是一个位
掩码，它指明目标栈层是哪个、是否涉及
``net_if`` 对象，以及所请求的具体管理流程。
可用的流程请求取决于栈中
已实现了哪些内容。

为避免额外开销，所有 :c:func:`net_mgmt` 调用都是直接调用。虽然
未来版本中这一点可能改变，但这不会影响
该函数的使用者。

.. _net_mgmt_listening:

监听网络事件
***************************

可以通过注册一个回调函数并指定一组用于
过滤回调何时被调用的事件，来接收网络事件的
通告。回调函数对于"层 + 代码"这一对组合必须是
唯一的，而命令部分则是一个事件
掩码。

在运行时提供两个函数：:c:func:`net_mgmt_add_event_callback`
用于注册回调函数，:c:func:`net_mgmt_del_event_callback`
用于注销回调。辅助函数
:c:func:`net_mgmt_init_event_callback` 可用于
简化回调结构的初始化。

此外，还可以使用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER`
在编译期注册回调处理器。

当发生的事件与某个回调的事件集匹配时，
关联的回调函数会携带实际的事件
代码被调用。这样，如果希望的话，
不同事件可以由同一个回调函数处理。

.. warning::

   事件集过滤对于具有相同
   层和层代码的事件可能出现误报。回调处理器函数**必须**
   将事件代码（作为参数传入）与其将处理的具体网络
   事件进行比对，**无论**传给 :c:func:`net_mgmt_init_event_callback`
   的事件集中包含多少个事件。

   注意，要接收来自多个层的事件，必须注册
   多个监听器，每个被监听的层各注册一个。
   回调处理器函数可以在不同层的事件之间共享。

   （具有相同层和层代码的事件可能出现误报。）

下面给出一个示例。

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

或者类似地，使用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER`。

.. note::

   ``info`` 和 ``info_length`` 参数只有在
   :kconfig:option:`CONFIG_NET_MGMT_EVENT_INFO` 启用时才可用。否则它们为
   ``NULL`` 和零。

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

可监听到的可用通用核心事件参见 :zephyr_file:`include/zephyr/net/net_event.h`。


定义一个网络管理流程
***************************************

可以通过定义一个处理器并将其与
关联的 mgmt_request 代码一起注册，
来为你的栈实现提供特定的额外管理流程。

管理请求代码根据其目标层，或者（如果目标层是 L2）
根据技术，在相应位置定义。例如，所有 IP 层的管理请求代码
都会找到在 :zephyr_file:`include/zephyr/net/net_event.h` 头文件中。但如果是
L2 技术，比如以太网，则它们会找到在
:zephyr_file:`include/zephyr/net/ethernet.h` 中。

你的处理器按以下签名定义：

.. code-block:: c

   static int your_handler(uint64_t mgmt_event, struct net_if *iface,
                           void *data, size_t len);

然后将其与关联的 mgmt_request 代码一起注册：

.. code-block:: c

   NET_MGMT_REGISTER_REQUEST_HANDLER(<mgmt_request code>, your_handler);

之后就可以通过以下方式调用这个新的管理流程：

.. code-block:: c

   net_mgmt(<mgmt_request code>, ...);


通告一个网络事件
*************************

可以使用 :c:func:`net_mgmt_event_notify`
函数并给出网络事件代码来通告一个特定的网络事件。
详见
:zephyr_file:`include/zephyr/net/net_mgmt.h`。与管理请求
代码一样，事件代码也可以找到在特定 L2 技术的管理头文件中，
例如如果 802.15.4 L2 是想要监听其事件的技术，
那么 :zephyr_file:`include/zephyr/net/ieee802154_mgmt.h` 就是正确的位置。

API 参考
*************

.. doxygengroup:: net_mgmt
