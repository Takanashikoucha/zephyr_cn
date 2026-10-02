.. _usbd_cdc_acm:

USB 设备 CDC ACM
##################

USB 设备栈提供的 CDC ACM 功能仅实现了
抽象控制模型（Abstract Control Model）串行仿真。
顾名思义，它的唯一用途是仿真串行线路。
大多数现代操作系统都应开箱即用地支持它。

CDC ACM 功能在主机侧和设备侧均表示为一个串行接口，
而用户或应用接口是 :ref:`uart_api`
驱动 API。这使得已经使用 UART API 的应用程序
无需修改负责数据通信的代码，即可使用
CDC ACM 功能提供的串行接口。只需要
额外的配置和 USB 设备栈初始化即可。

CDC ACM UART 配置
==========================

与真实的 UART 控制器类似，虚拟的 CDC ACM UART
在设备树中描述。CDC ACM UART 的设备树
compatible 属性为
:dtcompatible:`zephyr,cdc-acm-uart`。

当启用 USB 设备支持且设备树源中存在
compatible 节点时，会自动选中 CDC ACM 支持。
如有必要，可以通过 :kconfig:option:`CONFIG_USBD_CDC_ACM_CLASS`
显式禁用 CDC ACM 支持。
可能的 CDC ACM 实例数量取决于
USB 设备控制器支持的端点数量。
每个 CDC ACM 实例需要三个
端点：两个批量（bulk）端点（一个 IN、一个 OUT）
和一个 MaxPacketSize 为 16 的
中断 IN 端点。
CDC ACM 节点可以使用 ``label`` 属性
来区分主机侧的不同接口。
下面是一个设备树 overlay 文件的示例。

.. code-block:: devicetree

	&zephyr_udc0 {
		cdc_acm_uart0: cdc_acm_uart0 {
			compatible = "zephyr,cdc-acm-uart";
			label = "CDC_ACM_0";
		};
	};

在应用程序使用 CDC ACM UART 之前，
可能希望等待 DTR
信号。有关如何实现
该功能，请参见 :zephyr:code-sample:`usb-cdc-acm`。

.. note::
   要与主机通信，除了 UART 配置之外，应用程序
   还必须启用 USB 设备栈，
   请参阅 :ref:`usb_device_next_howto_configure` 并仔细阅读
   下一章。对于从旧版栈迁移的用户和应用程序，
   这是他们唯一需要适配的部分。

.. _cdc_acm_uart_as_serial_backend:

将 CDC ACM UART 用作串行后端
==============================

使用上述示例和 ``zephyr,console`` chosen 节点属性，
你可以
将 CDC ACM UART 配置为控制台设备。

.. code-block:: devicetree

	/ {
		chosen {
			zephyr,console = &cdc_acm_uart0;
		};
	};

	&zephyr_udc0 {
		cdc_acm_uart0: cdc_acm_uart0 {
			compatible = "zephyr,cdc-acm-uart";
			label = "CDC_ACM_0";
		};
	};

与上述示例中配置控制台使用
CDC ACM UART 的方式相同，``zephyr,shell-uart``
chosen 节点属性可用于
配置 shell 使用 CDC ACM UART 作为串行后端。
参见示例
:zephyr:code-sample:`shell-module` 和 :ref:`chosen 节点文档
<devicetree-chosen-nodes>`。

由于作为串行后端的使用场景非常常见，
且 CDC ACM UART 在运行时无需任何配置，
栈提供了一个辅助函数，
执行 :ref:`usb_device_next_howto_configure` 中
描述的步骤。
该辅助函数通过 :kconfig:option:`CONFIG_CDC_ACM_SERIAL_INITIALIZE_AT_BOOT`
启用，并使用单个 CDC ACM 实例
初始化 USB 设备栈。
示例
:zephyr:code-sample:`usb-cdc-acm-console` 演示了如何使用它。

像 :zephyr:board:`nrf52840dongle` 这类
没有调试适配器但具有 USB 设备控制器、
并希望将 CDC ACM UART 用作日志和 shell
默认串行后端的板级，也应使用
:kconfig:option:`CONFIG_CDC_ACM_SERIAL_INITIALIZE_AT_BOOT`。
由于任何板级的配置都相同，
存在公共的
:zephyr_file:`设备树文件 <boards/common/usb/cdc_acm_serial.dtsi>` 和
:zephyr_file:`Kconfig 文件 <boards/common/usb/Kconfig.cdc_acm_serial.defconfig>`，
必须包含在板级的设备树和 Kconfig.defconfig 文件中。

在应用程序中使用 CDC ACM UART
=====================================

CDC ACM 实现了一个虚拟 UART 控制器，
提供中断驱动（Interrupt-driven）UART
API 和轮询（Polling）UART API。尚不支持
ASYNC API。如果
应用程序想通过 CDC ACM UART 通信，
首选方式是
使用中断驱动 UART API。理解 API 文档是
必要的，但下面也有一些注意事项。

中断驱动 UART API
-------------------------

CDC ACM UART 实现在内部使用两个环形缓冲区。
这些缓冲区从 :ref:`uart_interrupt_api`
接管了 TX/RX FIFO（TX/RX 缓冲区）的功能。

如 :ref:`uart_interrupt_api` 所述，
函数
:c:func:`uart_irq_update()`、:c:func:`uart_irq_is_pending`、
:c:func:`uart_irq_rx_ready()`、:c:func:`uart_irq_tx_ready()`、
:c:func:`uart_fifo_read()` 和 :c:func:`uart_fifo_fill()`
应从中断处理程序中调用，参见
:c:func:`uart_irq_callback_user_data_set()`。
为防止未定义行为，
这些函数的实现会检查其被调用的上下文，
如果调用方不是中断处理程序则失败。

此外，如 UART API 所述，:c:func:`uart_irq_is_pending`、
:c:func:`uart_irq_rx_ready()` 和 :c:func:`uart_irq_tx_ready()`
只能在 :c:func:`uart_irq_update()` 之后调用。

简化来看，应用程序的中断处理程序应类似如下：

.. code-block:: c

	static void interrupt_handler(const struct device *dev, void *user_data)
	{
		while (true) {
			uart_irq_update(dev);

			if (uart_irq_is_pending(dev) <= 0) {
				break;
			}

			if (uart_irq_rx_ready(dev)) {
				int len;
				int n;

				/* ... */
				n = uart_fifo_read(dev, buffer, len);
				/* ... */
			}

			if (uart_irq_tx_ready(dev)) {
				int len;
				int n;

				/* ... */
				n = uart_fifo_fill(dev, buffer, len);
			  /* ... */
			}
		}
	}

所有这些函数都不直接依赖于 USB 设备的状态。
填充 TX FIFO 并不意味着数据正在
发送往主机。
成功读取 RX FIFO 也不意味着设备仍然
连接在主机上。如果 TX FIFO 中有空闲空间，
且 TX 中断已启用，:c:func:`uart_irq_tx_ready()`
将返回成功。如果
RX FIFO 中有数据，
且 RX 中断已启用，:c:func:`uart_irq_rx_ready()`
将返回成功。函数 :c:func:`uart_irq_tx_complete()`
尚未实现。

轮询 UART API
----------------

CDC ACM 轮询输出（poll out）实现遵循 :ref:`uart_polling_api`，
仅当 hw-flow-control 属性已启用
且从非 ISR 上下文调用时，
才在 TX FIFO 满时阻塞。
