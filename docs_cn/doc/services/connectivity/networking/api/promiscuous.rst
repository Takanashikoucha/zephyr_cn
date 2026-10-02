.. _promiscuous_interface:

混杂模式
################

.. contents::
    :local:
    :depth: 2

概述
********

混杂模式是网络接口控制器的一种工作模式，使控制器将其收到的所有流量都传递给应用程序，而不是只传递控制器被专门编程接收的那些帧。该模式通常用于数据包嗅探，通过向应用程序展示网络上正在传输的所有数据来诊断网络连接问题。（更多信息请参见
`维基百科关于混杂模式的文章
<https://en.wikipedia.org/wiki/Promiscuous_mode>`_。）

网络混杂 API 用于启用和禁用该模式，并用于等待和接收到达的网络数据。并非所有网络技术或网络设备驱动都支持混杂模式。

示例用法
************

首先，应用程序需要像下面这样开启混杂模式：

.. code-block:: c

	ret = net_promisc_mode_on(iface);
	if (ret < 0) {
		if (ret == -EALREADY) {
			printf("Promiscuous mode already enabled\n");
		} else {
			printf("Cannot enable promiscuous mode for "
			       "interface %p (%d)\n", iface, ret);
		}
	}


如果没有错误，应用程序就可以开始等待网络数据：

.. code-block:: c

	while (true) {
		pkt = net_promisc_mode_wait_data(K_FOREVER);
		if (pkt) {
			print_info(pkt);
		}

		net_pkt_unref(pkt);
	}


最后，应用程序可以像下面这样关闭混杂模式：

.. code-block:: c

	ret = net_promisc_mode_off(iface);
	if (ret < 0) {
		if (ret == -EALREADY) {
			printf("Promiscuous mode already disabled\n");
		} else {
			printf("Cannot disable promiscuous mode for "
			       "interface %p (%d)\n", iface, ret);
		}
	}


更完整的示例请参见 :zephyr:code-sample:`net-promiscuous-mode`。


API 参考
*************

.. doxygengroup:: promiscuous
