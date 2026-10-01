.. _promiscuous_interface:

Promiscuous Mode
################

.. contents::
    :local:
    :depth: 2

Overview
********

Promiscuous mode 为 network interface controller 的 mode（使其将接收到的所有 traffic 传递给 application（而非仅传递 controller 专门编程以接收的 frames。此 mode 通常用于 packet sniffing（通过向 application 显示网络上传输的所有 data 来诊断 network connectivity issues。（更多信息参见 `Wikipedia article on promiscuous mode
<https://en.wikipedia.org/wiki/Promiscuous_mode>`_。）

Network promiscuous APIs 用于启用和禁用此 mode（以及等待和接收 network data 到达。并非所有 network technologies 或 network device drivers 支持 promiscuous mode。

Sample usage
************

首先 application 须如下开启 promiscuous mode：

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


若无 error（application 可开始等待 network data：

.. code-block:: c

	while (true) {
		pkt = net_promisc_mode_wait_data(K_FOREVER);
		if (pkt) {
			print_info(pkt);
		}

		net_pkt_unref(pkt);
	}


最后 application 可如下关闭 promiscuous mode：

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


更全面的示例参见 :zephyr:code-sample:`net-promiscuous-mode`。


API Reference
*************

.. doxygengroup:: promiscuous
